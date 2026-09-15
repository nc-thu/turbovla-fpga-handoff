`timescale 1ns/1ps
module tb_w8a16_array;
  localparam int ROWS = 2;
  localparam int COLS = 3;
  localparam int K = 5;
  logic clk = 0, rst_n = 0, clr = 0, feed_vld = 0, feed_pulse = 0;
  logic [ROWS*16-1:0] a_feed;
  logic [COLS*8-1:0] b_feed;
  logic [$clog2(ROWS)-1:0] drain_row;
  logic [COLS*40-1:0] snap_row;
  always #5 clk = ~clk;
  w8a16_sysarr #(.ROWS(ROWS), .PCOLS(COLS), .ACC_W(40)) dut (
    .clk(clk), .rst_n(rst_n), .clr(clr), .feed_vld(feed_vld), .feed_pulse(feed_pulse),
    .a_feed(a_feed), .b_feed(b_feed), .drain_row(drain_row), .snap_row(snap_row)
  );
  integer A[0:ROWS-1][0:K-1];
  integer B[0:K-1][0:COLS-1];
  integer G[0:ROWS-1][0:COLS-1];
  integer i, j, k;
  initial begin
    a_feed = '0; b_feed = '0; drain_row = 0;
    for (i = 0; i < ROWS; i = i + 1)
      for (k = 0; k < K; k = k + 1) A[i][k] = (i+1)*(k-2);
    for (k = 0; k < K; k = k + 1)
      for (j = 0; j < COLS; j = j + 1) B[k][j] = (j-1)*(k+1);
    for (i = 0; i < ROWS; i = i + 1)
      for (j = 0; j < COLS; j = j + 1) begin
        G[i][j] = 0;
        for (k = 0; k < K; k = k + 1) G[i][j] = G[i][j] + A[i][k]*B[k][j];
      end
    repeat (3) @(negedge clk); rst_n = 1;
    @(negedge clk); clr = 1; @(negedge clk); clr = 0; feed_vld = 1;
    for (k = 0; k < K; k = k + 1) begin
      for (i = 0; i < ROWS; i = i + 1) a_feed[i*16 +: 16] = A[i][k];
      for (j = 0; j < COLS; j = j + 1) b_feed[j*8 +: 8] = B[k][j];
      @(negedge clk);
    end
    feed_vld = 0; a_feed = '0; b_feed = '0;
    // Delay the end pulse beyond multiplier and wavefront latency.
    repeat (8) @(negedge clk);
    feed_pulse = 1; @(negedge clk); feed_pulse = 0;
    repeat (16) @(negedge clk);
    for (i = 0; i < ROWS; i = i + 1) begin
      drain_row = i[$clog2(ROWS)-1:0];
      #1;
      for (j = 0; j < COLS; j = j + 1)
        if ($signed(snap_row[j*40 +: 40]) !== G[i][j]) begin
          $display("ARRAY_FAIL row=%0d col=%0d got=%0d exp=%0d", i, j, $signed(snap_row[j*40 +: 40]), G[i][j]);
          $finish(1);
        end
    end
    $display("TB_W8A16_ARRAY PASS");
    $finish(0);
  end
endmodule
