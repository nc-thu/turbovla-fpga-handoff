// Camera-ready command runtime for the TurboVLA W8A16 tile.
//
// This module is deliberately explicit about completion.  GEMM/BMM wait for
// the action engine, vector operations wait for the vector unit, REQUANT waits
// for its registered result, and memory instructions hold a DMA command until
// the corresponding backend reports done.  The 64-bit ISA word carries the
// scheduling fields; tensor shapes and scale IDs remain in compiler metadata.
`ifndef TVLA_W8A16_RUNTIME_SV
`define TVLA_W8A16_RUNTIME_SV
module w8a16_runtime #(
  parameter int K = 8,
  parameter int N = 7,
  parameter int VEC_N = 16
) (
  input  logic                         clk,
  input  logic                         rst_n,
  input  logic [63:0]                  instr_word,
  input  logic                         instr_valid,
  output logic                         instr_ready,

  input  logic                         state_we,
  input  logic [((K <= 1) ? 1 : $clog2(K))-1:0] state_index,
  input  logic signed [15:0]            state_data,
  input  logic                         weight_we,
  input  logic [((N*K <= 1) ? 1 : $clog2(N*K))-1:0] weight_index,
  input  logic signed [7:0]             weight_data,
  input  logic                         bias_we,
  input  logic [((N <= 1) ? 1 : $clog2(N))-1:0] bias_index,
  input  logic signed [15:0]            bias_data,

  input  logic                         vec_we,
  input  logic [((VEC_N <= 1) ? 1 : $clog2(VEC_N))-1:0] vec_index,
  input  logic signed [15:0]            vec_data,
  input  logic signed [15:0]            vec_aux_data,
  input  logic signed [15:0]            vec_scale_data,

  output logic                         action_valid,
  output logic signed [N*16-1:0]        action_out,
  output logic signed [VEC_N*16-1:0]    vector_out,
  output logic                         vector_valid,
  output logic signed [15:0]            requant_out,
  output logic                         requant_valid,
  output logic                         busy,
  output logic                         done,

  output logic                         act_cmd_valid,
  output logic                         act_cmd_write,
  output logic [31:0]                  act_cmd_addr,
  output logic [15:0]                  act_cmd_len,
  input  logic                         act_cmd_ready,
  input  logic                         act_dma_done,
  output logic                         weight_cmd_valid,
  output logic                         weight_cmd_write,
  output logic [31:0]                  weight_cmd_addr,
  output logic [15:0]                  weight_cmd_len,
  input  logic                         weight_cmd_ready,
  input  logic                         weight_dma_done,

  // Stream side of the command runtime.  LOAD commands consume the beat
  // returned by DMA; STORE commands drive a beat from the selected local
  // vector bank.  Completion is therefore tied to payload movement, not just
  // to accepting the command word.
  input  logic [255:0]                 act_stream_out_data,
  input  logic                         act_stream_out_valid,
  output logic                         act_stream_out_ready,
  output logic [255:0]                 act_stream_in_data,
  output logic                         act_stream_in_valid,
  input  logic                         act_stream_in_ready,
  input  logic [383:0]                 weight_stream_out_data,
  input  logic                         weight_stream_out_valid,
  output logic                         weight_stream_out_ready,

  // A matrix command with flags[7]=1 launches the production 16x48 array.
  // The feed/drain data path remains at the system top because its beats come
  // from the compiler-selected tile scheduler.  Small action tiles keep the
  // local action path used by the command smoke.
  output logic                         gemm_start_cmd,
  input  logic                         gemm_done_cmd
);
  localparam logic [7:0] OP_LOAD_CTX    = 8'h01;
  localparam logic [7:0] OP_LOAD_WEIGHT = 8'h02;
  localparam logic [7:0] OP_STORE_CTX   = 8'h03;
  localparam logic [7:0] OP_STORE_ACTION= 8'h04;
  localparam logic [7:0] OP_GEMM        = 8'h10;
  localparam logic [7:0] OP_BMM         = 8'h11;
  localparam logic [7:0] OP_BIAS        = 8'h20;
  localparam logic [7:0] OP_ADD         = 8'h21;
  localparam logic [7:0] OP_MUL         = 8'h22;
  localparam logic [7:0] OP_LN          = 8'h30;
  localparam logic [7:0] OP_SOFTMAX     = 8'h31;
  localparam logic [7:0] OP_RELU        = 8'h32;
  localparam logic [7:0] OP_GELU        = 8'h33;
  localparam logic [7:0] OP_TANH        = 8'h34;
  localparam logic [7:0] OP_REQUANT     = 8'h35;
  localparam logic [7:0] OP_WAIT        = 8'h40;
  localparam logic [7:0] OP_BARRIER     = 8'h41;
  localparam logic       FLAG_ARRAY     = 1'b1; // flags[7]

  localparam int V_IDX_W = (VEC_N <= 1) ? 1 : $clog2(VEC_N);

  logic signed [15:0] state_mem [0:K-1];
  logic signed [7:0]  weight_mem [0:N*K-1];
  logic signed [15:0] bias_mem [0:N-1];
  logic signed [15:0] vec_mem [0:VEC_N-1];
  logic signed [15:0] vec_aux_mem [0:VEC_N-1];
  logic signed [15:0] vec_scale_r;
  logic [K*16-1:0] state_flat;
  logic [N*K*8-1:0] weight_flat;
  logic [N*16-1:0] bias_flat;
  logic signed [VEC_N*16-1:0] vec_x_flat;
  logic signed [VEC_N*16-1:0] vec_aux_flat;
  integer c;
  localparam int ACT_LANES = 16;
  localparam int WEIGHT_BYTES = 48;
  logic [15:0] weight_load_offset_r;
  logic [255:0] act_store_data_r;
  logic [255:0] act_store_data_next;
  logic act_payload_seen_r;
  logic weight_payload_seen_r;

  always_comb begin
    state_flat = '0;
    for (c = 0; c < K; c = c + 1) state_flat[c*16 +: 16] = state_mem[c];
    weight_flat = '0;
    for (c = 0; c < N*K; c = c + 1) weight_flat[c*8 +: 8] = weight_mem[c];
    bias_flat = '0;
    for (c = 0; c < N; c = c + 1) bias_flat[c*16 +: 16] = bias_mem[c];
    vec_x_flat = '0;
    vec_aux_flat = '0;
    for (c = 0; c < VEC_N; c = c + 1) begin
      vec_x_flat[c*16 +: 16] = vec_mem[c];
      vec_aux_flat[c*16 +: 16] = vec_aux_mem[c];
    end
  end

  // A store beat is assembled once when the command is accepted.  The
  // payload remains stable while DMA applies back-pressure, which is the
  // same ready/valid rule used by the external CTX interface.
  always_comb begin
    act_store_data_next = '0;
    for (c = 0; c < VEC_N; c = c + 1)
      act_store_data_next[c*16 +: 16] = vec_mem[c];
  end

  logic [7:0] op_code, op_flags, op_dst, op_src0, op_src1;
  logic [15:0] op_length;
  logic op_valid, op_done;
  logic ctrl_busy;
  w8a16_isa_ctrl u_ctrl (
    .clk(clk), .rst_n(rst_n), .instr_word(instr_word), .instr_valid(instr_valid),
    .instr_ready(instr_ready), .op_code(op_code), .op_flags(op_flags),
    .op_dst(op_dst), .op_src0(op_src0), .op_src1(op_src1), .op_length(op_length),
    .op_valid(op_valid), .op_done(op_done), .busy(ctrl_busy), .done(done)
  );

  logic engine_start, engine_done, engine_busy;
  logic signed [N*16-1:0] engine_action;
  w8a16_action_path #(.K(K), .N(N)) u_action (
    .clk(clk), .rst_n(rst_n), .start(engine_start),
    .state_in(state_flat), .weight_in(weight_flat), .bias_in(bias_flat),
    .action_valid(action_valid), .action_out(engine_action),
    .busy(engine_busy), .done(engine_done)
  );
  assign action_out = engine_action;

  localparam logic [3:0] VOP_BIAS = 4'd0;
  localparam logic [3:0] VOP_ADD  = 4'd1;
  localparam logic [3:0] VOP_MUL  = 4'd2;
  localparam logic [3:0] VOP_RELU = 4'd3;
  localparam logic [3:0] VOP_GELU = 4'd4;
  localparam logic [3:0] VOP_TANH = 4'd5;
  localparam logic [3:0] VOP_LN  = 4'd6;
  localparam logic [3:0] VOP_SMX = 4'd7;
  logic [3:0] vector_op;
  logic vector_start, vector_done;
  logic signed [VEC_N*16-1:0] vector_y;
  w8a16_vector_ops #(.N(VEC_N)) u_vector (
    .clk(clk), .rst_n(rst_n), .start(vector_start), .op(vector_op),
    .x(vec_x_flat), .aux(vec_aux_flat), .scale(vec_scale_r),
    .y(vector_y), .out_valid(vector_valid), .done(vector_done)
  );
  assign vector_out = vector_y;

  logic requant_start, requant_done;
  logic signed [15:0] requant_y;
  logic signed [39:0] requant_x;
  w8a16_requant u_requant (
    .clk(clk), .rst_n(rst_n), .in_vld(requant_start), .x(requant_x),
    .multiplier(vec_scale_r), .shift(8'd0), .out_vld(requant_done), .y(requant_y)
  );
  assign requant_out = requant_y;
  assign requant_valid = requant_done;

  typedef enum logic [3:0] {
    E_IDLE, E_ACTION, E_GEMM_WAIT, E_VECTOR, E_REQUANT,
    E_ACT_CMD, E_ACT_WAIT, E_WEIGHT_CMD, E_WEIGHT_WAIT, E_CONTROL
  } exec_state_t;
  exec_state_t exec_state;
  logic [31:0] dma_addr_r;
  logic [15:0] dma_len_r;
  logic [7:0]  dma_op_r;
  logic [1:0]  control_delay_r;
  integer s;

  always_comb begin
    engine_start = 1'b0;
    gemm_start_cmd = 1'b0;
    vector_start = 1'b0;
    requant_start = 1'b0;
    vector_op = VOP_ADD;
    requant_x = $signed({{24{vec_mem[0][15]}}, vec_mem[0]});
    act_cmd_valid = (exec_state == E_ACT_CMD);
    act_cmd_write = (dma_op_r == OP_STORE_CTX) || (dma_op_r == OP_STORE_ACTION);
    act_cmd_addr = dma_addr_r;
    act_cmd_len = (dma_len_r == 0) ? 16'd1 : dma_len_r;
    weight_cmd_valid = (exec_state == E_WEIGHT_CMD);
    weight_cmd_write = 1'b0;
    weight_cmd_addr = dma_addr_r;
    weight_cmd_len = (dma_len_r == 0) ? 16'd1 : dma_len_r;

    // DMA read data is consumed only by the matching LOAD command.  Store
    // data is held in a register so the DMA can pause without changing the
    // beat presented to it.
    act_stream_out_ready = (exec_state == E_ACT_WAIT && dma_op_r == OP_LOAD_CTX);
    weight_stream_out_ready = (exec_state == E_WEIGHT_WAIT && dma_op_r == OP_LOAD_WEIGHT);
    act_stream_in_valid = (exec_state == E_ACT_WAIT &&
                           (dma_op_r == OP_STORE_CTX || dma_op_r == OP_STORE_ACTION));
    act_stream_in_data = act_store_data_r;

    if (op_valid && exec_state == E_IDLE) begin
      if ((op_code == OP_GEMM || op_code == OP_BMM) && op_flags[7] == FLAG_ARRAY)
        gemm_start_cmd = 1'b1;
      else if (op_code == OP_GEMM || op_code == OP_BMM)
        engine_start = 1'b1;
      else if (op_code == OP_BIAS || op_code == OP_ADD || op_code == OP_MUL ||
               op_code == OP_RELU || op_code == OP_GELU || op_code == OP_TANH ||
               op_code == OP_LN || op_code == OP_SOFTMAX) vector_start = 1'b1;
      else if (op_code == OP_REQUANT) requant_start = 1'b1;
    end
    case (op_code)
      OP_BIAS: vector_op = VOP_BIAS;
      OP_ADD: vector_op = VOP_ADD;
      OP_MUL: vector_op = VOP_MUL;
      OP_RELU: vector_op = VOP_RELU;
      OP_GELU: vector_op = VOP_GELU;
      OP_TANH: vector_op = VOP_TANH;
      OP_LN: vector_op = VOP_LN;
      OP_SOFTMAX: vector_op = VOP_SMX;
      default: vector_op = VOP_ADD;
    endcase
  end

  // Completion is generated only by the unit that owns the current command.
  // This prevents a stale vector/DMA pulse from acknowledging a later word.
  always_comb begin
    op_done = 1'b0;
    case (exec_state)
      E_ACTION: op_done = engine_done;
      E_GEMM_WAIT: op_done = gemm_done_cmd;
      E_VECTOR: op_done = vector_done;
      E_REQUANT: op_done = requant_done;
      E_ACT_WAIT: op_done = act_dma_done;
      E_WEIGHT_WAIT: op_done = weight_dma_done;
      E_CONTROL: op_done = (control_delay_r == 0);
      default: op_done = 1'b0;
    endcase
  end

  assign busy = ctrl_busy | (exec_state != E_IDLE) | engine_busy;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      exec_state <= E_IDLE;
      dma_addr_r <= '0;
      dma_len_r <= '0;
      dma_op_r <= '0;
      control_delay_r <= '0;
      vec_scale_r <= 16'sd1;
      weight_load_offset_r <= '0;
      act_store_data_r <= '0;
      act_payload_seen_r <= 1'b0;
      weight_payload_seen_r <= 1'b0;
      for (s = 0; s < K; s = s + 1) state_mem[s] <= '0;
      for (s = 0; s < N*K; s = s + 1) weight_mem[s] <= '0;
      for (s = 0; s < N; s = s + 1) bias_mem[s] <= '0;
      for (s = 0; s < VEC_N; s = s + 1) begin
        vec_mem[s] <= '0;
        vec_aux_mem[s] <= '0;
      end
    end else begin
      if (state_we) state_mem[state_index] <= state_data;
      if (weight_we) weight_mem[weight_index] <= weight_data;
      if (bias_we) bias_mem[bias_index] <= bias_data;
      if (vec_we) begin
        vec_mem[vec_index] <= vec_data;
        vec_aux_mem[vec_index] <= vec_aux_data;
        vec_scale_r <= vec_scale_data;
      end

      // Capture each returned CTX beat into the local INT16 bank.  The first
      // K lanes also refresh the compact action-state bank used by the
      // command-path GEMM smoke.  A larger tensor is handled as successive
      // DMA commands by the compiler; this tile keeps the current beat in
      // the 16-lane scratch window.
      if (act_stream_out_valid && act_stream_out_ready && dma_op_r == OP_LOAD_CTX) begin
        act_payload_seen_r <= 1'b1;
        for (s = 0; s < VEC_N; s = s + 1)
          vec_mem[s] <= $signed(act_stream_out_data[s*16 +: 16]);
        for (s = 0; s < K; s = s + 1)
          state_mem[s] <= $signed(act_stream_out_data[s*16 +: 16]);
      end

      // WRAM beats carry 48 signed INT8 weights.  The runtime tile is
      // deliberately small (N*K=56 in the command-path instance), so use
      // fixed destinations for the first and second beat.  A variable array
      // index here creates a 56-way write decoder and was the worst top-level
      // timing path after the stream bridge was added.  The two explicit
      // cases preserve multi-beat behaviour while allowing Vivado to map each
      // byte write directly to its destination register.
      if (weight_stream_out_valid && weight_stream_out_ready && dma_op_r == OP_LOAD_WEIGHT) begin
        weight_payload_seen_r <= 1'b1;
        if (weight_load_offset_r == 16'd0) begin
          for (s = 0; s < WEIGHT_BYTES; s = s + 1)
            if (s < N*K)
              weight_mem[s] <= $signed(weight_stream_out_data[s*8 +: 8]);
        end else if (weight_load_offset_r == WEIGHT_BYTES) begin
          for (s = 0; s < WEIGHT_BYTES; s = s + 1)
            if ((WEIGHT_BYTES + s) < N*K)
              weight_mem[WEIGHT_BYTES + s] <=
                $signed(weight_stream_out_data[s*8 +: 8]);
        end
        weight_load_offset_r <= weight_load_offset_r + WEIGHT_BYTES;
      end

      // Capture vector output after the vector unit's registered result is
      // visible.  The write is intentionally separate from vector_valid.
      if (exec_state == E_VECTOR && vector_done)
        for (s = 0; s < VEC_N; s = s + 1) vec_mem[s] <= vector_y[s*16 +: 16];

      case (exec_state)
        E_IDLE: begin
          if (op_valid) begin
            dma_addr_r <= {(op_code == OP_LOAD_WEIGHT) ? op_src1 : op_src0, 24'h0};
            dma_len_r <= op_length;
            dma_op_r <= op_code;
            if (op_code == OP_LOAD_WEIGHT) begin
              weight_load_offset_r <= '0;
              weight_payload_seen_r <= 1'b0;
            end
            if (op_code == OP_LOAD_CTX || op_code == OP_STORE_CTX ||
                op_code == OP_STORE_ACTION)
              act_payload_seen_r <= 1'b0;
            if (op_code == OP_STORE_CTX || op_code == OP_STORE_ACTION)
              act_store_data_r <= act_store_data_next;
            if (op_code == OP_GEMM || op_code == OP_BMM) begin
              if (op_flags[7] == FLAG_ARRAY) exec_state <= E_GEMM_WAIT;
              else exec_state <= E_ACTION;
            end
            else if (op_code == OP_BIAS || op_code == OP_ADD || op_code == OP_MUL ||
                     op_code == OP_RELU || op_code == OP_GELU || op_code == OP_TANH ||
                     op_code == OP_LN || op_code == OP_SOFTMAX) exec_state <= E_VECTOR;
            else if (op_code == OP_REQUANT) exec_state <= E_REQUANT;
            else if (op_code == OP_LOAD_WEIGHT) exec_state <= E_WEIGHT_CMD;
            else if (op_code == OP_LOAD_CTX || op_code == OP_STORE_CTX ||
                     op_code == OP_STORE_ACTION) exec_state <= E_ACT_CMD;
            else exec_state <= E_CONTROL;
            if (op_code == OP_WAIT || op_code == OP_BARRIER) control_delay_r <= 1;
            else control_delay_r <= 0;
          end
        end
        E_ACTION: if (engine_done) exec_state <= E_IDLE;
        E_GEMM_WAIT: if (gemm_done_cmd) exec_state <= E_IDLE;
        E_VECTOR: if (vector_done) exec_state <= E_IDLE;
        E_REQUANT: if (requant_done) exec_state <= E_IDLE;
        E_ACT_CMD: if (act_cmd_ready) exec_state <= E_ACT_WAIT;
        E_ACT_WAIT: begin
          // A DMA completion is not enough by itself.  Reads must have
          // transferred their payload into the local bank; writes must have
          // consumed the held payload.  This prevents a backend done pulse
          // from dropping a beat when the stream is back-pressured.
          if (act_dma_done &&
              (((dma_op_r == OP_LOAD_CTX) &&
                (act_payload_seen_r || (act_stream_out_valid && act_stream_out_ready))) ||
               (((dma_op_r == OP_STORE_CTX) || (dma_op_r == OP_STORE_ACTION)) &&
                (act_payload_seen_r || (act_stream_in_valid && act_stream_in_ready)))))
            exec_state <= E_IDLE;
        end
        E_WEIGHT_CMD: if (weight_cmd_ready) exec_state <= E_WEIGHT_WAIT;
        E_WEIGHT_WAIT: begin
          if (weight_dma_done &&
              (weight_payload_seen_r || (weight_stream_out_valid && weight_stream_out_ready)))
            exec_state <= E_IDLE;
        end
        E_CONTROL: begin
          if (control_delay_r != 0) control_delay_r <= control_delay_r - 1'b1;
          else exec_state <= E_IDLE;
        end
        default: exec_state <= E_IDLE;
      endcase
    end
  end
endmodule
`endif
