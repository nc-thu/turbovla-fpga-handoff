`timescale 1ns/1ps
module tb_array_smoke;
  localparam int R = 2;
  localparam int C = 3;
  logic clk = 1'b0; always #1 clk = ~clk;
  logic rst_n = 1'b0, clr = 1'b0, feed_vld = 1'b0, feed_pulse = 1'b0;
  logic [R*8-1:0] a_feed = '0;
  logic [C*16-1:0] b_feed = '0;
  logic [((C+3)/4)*4-1:0] drain_row_rep = '0;
  wire [C*2*32-1:0] acc_row;
  tvla_w8a8_pack2_array_top #(.ROWS(R), .PCOLS(C)) dut (
    .clk(clk), .rst_n(rst_n), .clr(clr), .feed_vld(feed_vld),
    .feed_pulse(feed_pulse), .a_feed(a_feed), .b_feed(b_feed),
    .drain_row_rep(drain_row_rep), .acc_row(acc_row)
  );
  initial begin
    repeat (2) @(negedge clk); rst_n = 1'b1; clr = 1'b1;
    @(negedge clk); clr = 1'b0; feed_vld = 1'b1;
    a_feed = {8'sd2, 8'sd3};
    b_feed = {16'h0005, 16'h0004, 16'h0003};
    repeat (4) @(negedge clk);
    feed_vld = 1'b0; a_feed = '0; b_feed = '0; feed_pulse = 1'b1;
    @(negedge clk); feed_pulse = 1'b0;
    repeat (4) @(negedge clk);
    if ($isunknown(acc_row)) begin $display("FAIL array X state"); $fatal(1); end
    $display("PASS tb_array_smoke acc_row=%h", acc_row);
    $finish;
  end
endmodule
