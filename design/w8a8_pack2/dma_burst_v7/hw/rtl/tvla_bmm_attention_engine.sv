// Two-input BMM staging and attention control.  Both operands are captured
// before a row is emitted.  Transpose, scale and mask are command sidebands;
// the layout helper performs the address permutation and the Pack2 scheduler
// consumes only rows whose dependencies are ready.
`ifndef TVLA_BMM_ATTENTION_ENGINE_SV
`define TVLA_BMM_ATTENTION_ENGINE_SV
module tvla_bmm_attention_engine #(
  parameter int ROWS = 16,
  parameter int COLS = 48,
  parameter int DW = 16
) (
  input logic clk,
  input logic rst_n,
  input logic start,
  input logic a_valid,
  input logic [ROWS*DW-1:0] a_row,
  input logic [$clog2(ROWS)-1:0] a_index,
  input logic b_valid,
  input logic [COLS*DW-1:0] b_row,
  input logic [$clog2(COLS)-1:0] b_index,
  input logic transpose_b,
  input logic mask_enable,
  input logic signed [DW-1:0] scale,
  output logic in_ready,
  output logic out_valid,
  input logic out_ready,
  output logic [ROWS*DW-1:0] out_a,
  output logic [COLS*DW-1:0] out_b,
  output logic [$clog2(ROWS)-1:0] out_index,
  output logic out_last,
  output logic [DW-1:0] control_tag
);
  tvla_bmm_layout #(.ROWS(ROWS), .COLS(COLS), .DW(DW)) u_layout (
    .clk(clk), .rst_n(rst_n), .start(start), .a_valid(a_valid), .a_row(a_row),
    .a_index(a_index), .b_valid(b_valid), .b_row(b_row), .b_index(b_index),
    .transpose_b(transpose_b), .mask_enable(mask_enable), .scale(scale),
    .in_ready(in_ready), .out_valid(out_valid),
    .out_ready(out_ready), .out_a(out_a), .out_b(out_b), .out_index(out_index),
    .out_last(out_last)
  );
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) control_tag <= '0;
    else if (start) control_tag <= {mask_enable, scale[6:0]};
  end
endmodule
`endif
