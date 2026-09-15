// Array-only top used for the 768-DSP resource and timing point.
module w8a16_array_top #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int ACC_W = 40
) (
  input  logic                    clk,
  input  logic                    rst_n,
  input  logic                    clr,
  input  logic                    feed_vld,
  input  logic                    feed_pulse,
  input  logic [ROWS*16-1:0]      a_feed,
  input  logic [PCOLS*8-1:0]      b_feed,
  input  logic [((ROWS <= 1) ? 1 : $clog2(ROWS))-1:0] drain_row,
  output logic [PCOLS*ACC_W-1:0] snap_row
);
  w8a16_sysarr #(.ROWS(ROWS), .PCOLS(PCOLS), .ACC_W(ACC_W)) u_array (
    .clk(clk), .rst_n(rst_n), .clr(clr), .feed_vld(feed_vld),
    .feed_pulse(feed_pulse), .a_feed(a_feed), .b_feed(b_feed),
    .drain_row(drain_row), .snap_row(snap_row)
  );
endmodule
