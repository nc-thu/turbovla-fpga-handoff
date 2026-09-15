`timescale 1ns/1ps
// Full-shape smoke: instantiate the production 16x48 array (768 PEs/DSPs)
// but use K=4 so the test remains a short, repeatable simulation.
module tb_w8a16_full;
  localparam int ROWS = 16;
  localparam int COLS = 48;
  localparam int K = 4;
  logic clk = 0, rst_n = 0, clr = 0, feed_vld = 0, feed_pulse = 0;
  logic [ROWS*16-1:0] a_feed;
  logic [COLS*8-1:0] b_feed;
  logic [$clog2(ROWS)-1:0] drain_row;
  logic [COLS*40-1:0] snap_row;
  always #1 clk = ~clk;

  w8a16_sysarr #(.ROWS(ROWS), .PCOLS(COLS), .ACC_W(40)) dut (
    .clk(clk), .rst_n(rst_n), .clr(clr), .feed_vld(feed_vld), .feed_pulse(feed_pulse),
    .a_feed(a_feed), .b_feed(b_feed), .drain_row(drain_row), .snap_row(snap_row)
  );

  integer A[0:ROWS-1][0:K-1];
  integer B[0:K-1][0:COLS-1];
  integer signed G[0:ROWS-1][0:COLS-1];
  integer i, j, k;
  integer signed got;
  initial begin
    a_feed = '0; b_feed = '0; drain_row = '0;
    for (i = 0; i < ROWS; i = i + 1)
      for (k = 0; k < K; k = k + 1) A[i][k] = ((i*3 + k*5) % 17) - 8;
    for (k = 0; k < K; k = k + 1)
      for (j = 0; j < COLS; j = j + 1) B[k][j] = ((k*7 + j*2) % 13) - 6;
    for (i = 0; i < ROWS; i = i + 1)
      for (j = 0; j < COLS; j = j + 1) begin
        G[i][j] = 0;
        for (k = 0; k < K; k = k + 1) G[i][j] = G[i][j] + A[i][k]*B[k][j];
      end

    repeat (4) @(negedge clk); rst_n = 1;
    @(negedge clk); clr = 1;
    @(negedge clk); clr = 0; feed_vld = 1;
    for (k = 0; k < K; k = k + 1) begin
      for (i = 0; i < ROWS; i = i + 1) a_feed[i*16 +: 16] = A[i][k];
      for (j = 0; j < COLS; j = j + 1) b_feed[j*8 +: 8] = B[k][j];
      @(negedge clk);
    end
    feed_vld = 0; a_feed = '0; b_feed = '0;
    // The longest path is row skew + column propagation + PE pipeline.
    repeat (ROWS + COLS + 12) @(negedge clk);
    feed_pulse = 1; @(negedge clk); feed_pulse = 0;
    repeat (ROWS + COLS + 12) @(negedge clk);
    for (i = 0; i < ROWS; i = i + 1) begin
      drain_row = i[$clog2(ROWS)-1:0];
      #1;
      for (j = 0; j < COLS; j = j + 1) begin
        got = $signed(snap_row[j*40 +: 40]);
        if (got !== G[i][j]) begin
          $display("FULL_ARRAY_FAIL row=%0d col=%0d got=%0d exp=%0d", i, j, got, G[i][j]);
          $finish(1);
        end
      end
    end
    $display("TB_W8A16_FULL PASS rows=%0d cols=%0d dsp=%0d", ROWS, COLS, ROWS*COLS);
    $finish(0);
  end
endmodule
