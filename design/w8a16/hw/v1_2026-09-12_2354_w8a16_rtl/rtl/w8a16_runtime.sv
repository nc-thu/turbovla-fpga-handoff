// Minimal command-to-action runtime.  It wires the ISA sequencer to the
// serialized action path so a compiler-generated smoke program can produce
// one 7-D LIBERO action.  Large vision/attention operators still use the
// 16×48 array/fallback units in the full schedule; this top is the integration
// seam, not a claim that the entire DINO/BERT graph fits in one RTL file.
`ifndef TVLA_W8A16_RUNTIME_SV
`define TVLA_W8A16_RUNTIME_SV
module w8a16_runtime #(
  parameter int K = 8,
  parameter int N = 7
) (
  input  logic                    clk,
  input  logic                    rst_n,
  input  logic [63:0]             instr_word,
  input  logic                    instr_valid,
  output logic                    instr_ready,
  input  logic                    state_we,
  input  logic [$clog2(K)-1:0]    state_index,
  input  logic signed [15:0]       state_data,
  input  logic                    weight_we,
  input  logic [$clog2(N*K)-1:0]  weight_index,
  input  logic signed [7:0]        weight_data,
  input  logic                    bias_we,
  input  logic [$clog2(N)-1:0]    bias_index,
  input  logic signed [15:0]       bias_data,
  output logic                    action_valid,
  output logic signed [N*16-1:0] action_out,
  output logic                    busy,
  output logic                    done
);
  localparam logic [7:0] OP_LOAD_CTX = 8'h01;
  localparam logic [7:0] OP_LOAD_WEIGHT = 8'h02;
  localparam logic [7:0] OP_STORE_CTX = 8'h03;
  localparam logic [7:0] OP_STORE_ACTION = 8'h04;
  localparam logic [7:0] OP_GEMM = 8'h10;
  localparam logic [7:0] OP_BIAS = 8'h20;
  localparam logic [7:0] OP_ADD = 8'h21;
  localparam logic [7:0] OP_LN = 8'h30;
  localparam logic [7:0] OP_SOFTMAX = 8'h31;
  localparam logic [7:0] OP_RELU = 8'h32;
  localparam logic [7:0] OP_GELU = 8'h33;
  localparam logic [7:0] OP_TANH = 8'h34;
  localparam logic [7:0] OP_REQUANT = 8'h35;
  localparam logic [7:0] OP_WAIT = 8'h40;
  localparam logic [7:0] OP_BARRIER = 8'h41;

  logic signed [15:0] state_mem [0:K-1];
  logic signed [7:0] weight_mem [0:N*K-1];
  logic signed [15:0] bias_mem [0:N-1];
  logic [K*16-1:0] state_flat;
  logic [N*K*8-1:0] weight_flat;
  logic [N*16-1:0] bias_flat;
  integer i_comb;
  integer i_seq;
  always_comb begin
    state_flat = '0;
    for (i_comb = 0; i_comb < K; i_comb = i_comb + 1) state_flat[i_comb*16 +: 16] = state_mem[i_comb];
    weight_flat = '0;
    for (i_comb = 0; i_comb < N*K; i_comb = i_comb + 1) weight_flat[i_comb*8 +: 8] = weight_mem[i_comb];
    bias_flat = '0;
    for (i_comb = 0; i_comb < N; i_comb = i_comb + 1) bias_flat[i_comb*16 +: 16] = bias_mem[i_comb];
  end

  logic [7:0] op_code;
  logic [7:0] op_flags, op_dst, op_src0, op_src1;
  logic [15:0] op_length;
  logic op_valid, op_done;
  logic engine_start, engine_busy, engine_done, engine_action_valid;
  logic signed [N*16-1:0] engine_action;
  w8a16_isa_ctrl u_ctrl (
    .clk(clk), .rst_n(rst_n), .instr_word(instr_word), .instr_valid(instr_valid),
    .instr_ready(instr_ready), .op_code(op_code), .op_flags(op_flags),
    .op_dst(op_dst), .op_src0(op_src0), .op_src1(op_src1), .op_length(op_length),
    .op_valid(op_valid), .op_done(op_done), .busy(), .done(done)
  );
  w8a16_action_path #(.K(K), .N(N)) u_action (
    .clk(clk), .rst_n(rst_n), .start(engine_start),
    .state_in(state_flat), .weight_in(weight_flat), .bias_in(bias_flat),
    .action_valid(engine_action_valid), .action_out(engine_action),
    .busy(engine_busy), .done(engine_done)
  );

  // All non-GEMM instructions in the command-path smoke are accepted as
  // one-cycle unit events.  Real schedules may replace these immediate
  // acknowledgements with the activation/DMA unit done signals.
  always_comb begin
    engine_start = 1'b0;
    op_done = 1'b0;
    if (op_valid) begin
      if (op_code == OP_GEMM) engine_start = !engine_busy;
      if (op_code != OP_GEMM) op_done = 1'b1;
    end
    if (engine_done) op_done = 1'b1;
  end
  assign action_valid = engine_action_valid;
  assign action_out = engine_action;
  assign busy = engine_busy | op_valid;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      for (i_seq = 0; i_seq < K; i_seq = i_seq + 1) state_mem[i_seq] <= '0;
      for (i_seq = 0; i_seq < N*K; i_seq = i_seq + 1) weight_mem[i_seq] <= '0;
      for (i_seq = 0; i_seq < N; i_seq = i_seq + 1) bias_mem[i_seq] <= '0;
    end else begin
      if (state_we) state_mem[state_index] <= state_data;
      if (weight_we) weight_mem[weight_index] <= weight_data;
      if (bias_we) bias_mem[bias_index] <= bias_data;
    end
  end
endmodule
`endif
