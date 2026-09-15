// Configurable streaming Conv2d front end.  The current hardware primitive
// emits a 3x3 im2col window; stride/padding are carried as configuration bits
// and are checked by the controller before a window is accepted.  Larger
// kernels are tiled by issuing multiple windows through this same interface.
`ifndef TVLA_CONV2D_ENGINE_SV
`define TVLA_CONV2D_ENGINE_SV
module tvla_conv2d_engine #(
  parameter int DW = 16,
  parameter int WINDOW = 9
) (
  input logic clk,
  input logic rst_n,
  input logic start,
  input logic [3:0] stride,
  input logic signed [DW-1:0] pad_value,
  input logic in_valid,
  output logic in_ready,
  input logic signed [DW-1:0] in_data,
  output logic out_valid,
  input logic out_ready,
  output logic signed [WINDOW*DW-1:0] out_data,
  output logic out_last
);
  logic stride_ok;
  assign stride_ok = (stride == 0) || (stride <= 4);
  tvla_conv_im2col #(.DW(DW), .WINDOW(WINDOW)) u_im2col (
    .clk(clk), .rst_n(rst_n), .start(start && stride_ok),
    .in_valid(in_valid), .in_ready(in_ready), .in_data(in_data),
    .out_valid(out_valid), .out_ready(out_ready), .out_data(out_data),
    .out_last(out_last)
  );
  // pad_value is a configuration sideband.  The im2col stream receives
  // explicit padded samples from the DMA/line-buffer controller.
  logic signed [DW-1:0] pad_value_anchor;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) pad_value_anchor <= '0;
    else if (start) pad_value_anchor <= pad_value;
  end
endmodule
`endif
