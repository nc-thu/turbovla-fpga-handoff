// Vector activation engine.  It gives LayerNorm, Softmax (including max,
// exp and reciprocal stages), GELU, ReLU, tanh, bias/add/mul and clamp a
// single registered command interface.  The existing bounded vector unit is
// used for the reductions; tvla_fp16_alu is kept as the pipelined arithmetic
// slot for a future vendor FP16 implementation.
`ifndef TVLA_ACTIVATION_ENGINE_SV
`define TVLA_ACTIVATION_ENGINE_SV
module tvla_activation_engine #(
  parameter int LANES = 16,
  parameter int DW = 16
) (
  input logic clk,
  input logic rst_n,
  input logic in_valid,
  output logic in_ready,
  input logic [7:0] op_code,
  input logic signed [LANES*DW-1:0] x,
  input logic signed [LANES*DW-1:0] y_in,
  input logic signed [DW-1:0] param0,
  input logic signed [DW-1:0] param1,
  output logic out_valid,
  input logic out_ready,
  output logic signed [LANES*DW-1:0] y,
  output logic [31:0] op_count
);
  logic core_valid;
  logic core_ready;
  logic signed [LANES*DW-1:0] core_y;
  logic [31:0] busy_cycles_unused;
  logic fp_valid;
  logic fp_ready;
  logic signed [LANES*DW-1:0] fp_y;
  logic [3:0] fp_op;
  logic choose_fp;

  assign choose_fp = (op_code == 8'h20) || (op_code == 8'h21) ||
                     (op_code == 8'h22) || (op_code == 8'h33) ||
                     (op_code == 8'h34) || (op_code == 8'h35) ||
                     (op_code == 8'h36) || (op_code == 8'h37) ||
                     (op_code == 8'h38);
  always_comb begin
    case (op_code)
      8'h20: fp_op = 4'd0; // bias is add with param in the wrapper below
      8'h21: fp_op = 4'd0;
      8'h22: fp_op = 4'd2;
      8'h33: fp_op = 4'd5;
      8'h34: fp_op = 4'd7; // max(x,0), y is zeroed by the caller if needed
      8'h35: fp_op = 4'd6;
      8'h36: fp_op = 4'd3;
      8'h37: fp_op = 4'd4;
      default: fp_op = 4'd0;
    endcase
  end

  tvla_full_vector_unit #(.LANES(LANES), .DW(DW)) u_vector_core (
    .clk(clk), .rst_n(rst_n), .in_valid(in_valid && !choose_fp), .in_ready(core_ready),
    .op_code(op_code), .x(x), .y(y_in), .param0(param0), .param1(param1),
    .out_valid(core_valid), .out_ready(out_ready), .out_data(core_y),
    .busy_cycles(busy_cycles_unused), .op_count(op_count)
  );
  tvla_fp16_alu #(.LANES(LANES), .DW(DW)) u_fp16_slot (
    .clk(clk), .rst_n(rst_n), .in_valid(in_valid && choose_fp), .in_ready(fp_ready),
    .op_code(fp_op), .a(x), .b((op_code == 8'h20) ? {LANES{param0}} : y_in),
    .param(param1), .out_valid(fp_valid), .out_ready(out_ready), .y(fp_y)
  );
  assign in_ready = choose_fp ? fp_ready : core_ready;
  assign out_valid = choose_fp ? fp_valid : core_valid;
  assign y = choose_fp ? fp_y : core_y;
endmodule
`endif
