// TurboVLA W8A8 adapter for the HB Pack2 pre-adder multiplier.
// The implementation is kept in pack2_mult_padd.sv so the bit-level reference
// remains identical to the routed HB v10 design.
`ifndef TVLA_W8A8_PACK2_MULT_PADD_SV
`define TVLA_W8A8_PACK2_MULT_PADD_SV
module tvla_w8a8_pack2_mult_padd #(
  parameter int M_REG = 1,
  parameter int P_REG = 1
)(
  input logic clk,
  input logic v_in,
  input logic row_in,
  input logic signed [7:0] a_in,
  input logic signed [7:0] w0_in,
  input logic signed [7:0] w1_in,
  output logic [47:0] P,
  output logic v_p,
  output logic row_p,
  output logic signed [7:0] a_p
);
  pack2_mult_padd #(.M_REG(M_REG), .P_REG(P_REG)) u_ref (
    .clk(clk), .v_in(v_in), .row_in(row_in), .a_in(a_in),
    .w0_in(w0_in), .w1_in(w1_in), .P(P), .v_p(v_p),
    .row_p(row_p), .a_p(a_p)
  );
endmodule
`endif
