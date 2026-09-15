// Four-column time-multiplexed requantizer adapter from HB v10.
`ifndef TVLA_W8A8_PACK2_REQUANT_SV
`define TVLA_W8A8_PACK2_REQUANT_SV
module tvla_w8a8_pack2_requant #(
  parameter int SHARE = 4,
  parameter int XW = 27,
  parameter int T_MAX = 39
)(
  input logic clk, input logic rst_n,
  input logic [SHARE-1:0] in_vld,
  input logic [SHARE*XW-1:0] x_bus,
  input logic signed [15:0] m,
  input logic [7:0] s,
  output logic [SHARE-1:0] out_vld,
  output logic [SHARE*8-1:0] y_bus,
  output logic [$clog2(SHARE)-1:0] slot_o
);
  rq_ms_x #(.SHARE(SHARE), .XW(XW), .T_MAX(T_MAX)) u_ref (
    .clk(clk), .rst_n(rst_n), .in_vld(in_vld), .x_bus(x_bus),
    .m(m), .s(s), .out_vld(out_vld), .y_bus(y_bus), .slot_o(slot_o)
  );
endmodule
`endif
