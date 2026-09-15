// TurboVLA W8A8 Pack2 PE.  Ports are intentionally identical to HB ae_pe_p2_pa.
`ifndef TVLA_W8A8_PACK2_PE_SV
`define TVLA_W8A8_PACK2_PE_SV
module tvla_w8a8_pack2_pe (
  input logic clk, input logic rst_n,
  input logic clr, input logic pulse_in,
  input logic av_in, input logic bv_in,
  input logic signed [7:0] a_in, input logic [15:0] b_in,
  output logic av_out, output logic bv_out, output logic pulse_out,
  output logic signed [7:0] a_out, output logic [15:0] b_out,
  output logic signed [31:0] acc0, output logic signed [31:0] acc1,
  output logic signed [26:0] snap0, output logic signed [26:0] snap1
);
  ae_pe_p2_pa u_ref (
    .clk(clk), .rst_n(rst_n), .clr(clr), .pulse_in(pulse_in),
    .av_in(av_in), .bv_in(bv_in), .a_in(a_in), .b_in(b_in),
    .av_out(av_out), .bv_out(bv_out), .pulse_out(pulse_out),
    .a_out(a_out), .b_out(b_out), .acc0(acc0), .acc1(acc1),
    .snap0(snap0), .snap1(snap1)
  );
endmodule
`endif
