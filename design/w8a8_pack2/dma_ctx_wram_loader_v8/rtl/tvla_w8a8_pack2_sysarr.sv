// 16x48 TurboVLA W8A8 Pack2 array adapter.
`ifndef TVLA_W8A8_PACK2_SYSARR_SV
`define TVLA_W8A8_PACK2_SYSARR_SV
module tvla_w8a8_pack2_sysarr #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48
)(
  input logic clk, input logic rst_n, input logic clr,
  input logic feed_vld, input logic feed_pulse,
  input logic [ROWS*8-1:0] a_feed,
  input logic [PCOLS*16-1:0] b_feed,
  input logic [((PCOLS+3)/4)*4-1:0] drain_row_rep,
  output logic [PCOLS*2*32-1:0] acc_row
);
  ae_sysarr_p2 #(.ROWS(ROWS), .PCOLS(PCOLS)) u_ref (
    .clk(clk), .rst_n(rst_n), .clr(clr), .feed_vld(feed_vld),
    .feed_pulse(feed_pulse), .a_feed(a_feed), .b_feed(b_feed),
    .drain_row_rep(drain_row_rep), .acc_row(acc_row)
  );
endmodule
`endif
