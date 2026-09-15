`timescale 1ns/1ps
module tb_w8a16_gemm;
  localparam int ROWS=2, COLS=3, K=2;
  logic clk=0, rst_n=0, start=0, clr=0, feed_vld=0, feed_pulse=0;
  logic [ROWS*16-1:0] a_feed;
  logic [COLS*8-1:0] b_feed;
  logic [$clog2(ROWS)-1:0] drain_row;
  logic [COLS*40-1:0] snap_row;
  logic busy, done;
  always #5 clk=~clk;
  w8a16_gemm #(.ROWS(ROWS),.PCOLS(COLS),.ACC_W(40)) dut (.*);
  integer A[0:ROWS-1][0:K-1], B[0:K-1][0:COLS-1], G[0:ROWS-1][0:COLS-1];
  integer i,j,k,t;
  initial begin
    a_feed='0; b_feed='0; drain_row='0;
    for (i=0;i<ROWS;i=i+1) for(k=0;k<K;k=k+1) A[i][k]=(i+1)*(k+1);
    for(k=0;k<K;k=k+1) for(j=0;j<COLS;j=j+1) B[k][j]=j-k;
    for(i=0;i<ROWS;i=i+1) for(j=0;j<COLS;j=j+1) begin
      G[i][j]=0; for(k=0;k<K;k=k+1) G[i][j]=G[i][j]+A[i][k]*B[k][j];
    end
    repeat(3) @(negedge clk); rst_n=1;
    @(negedge clk); clr=1; @(negedge clk); clr=0; start=1;
    @(negedge clk); start=0; feed_vld=1;
    for(k=0;k<K;k=k+1) begin
      for(i=0;i<ROWS;i=i+1) a_feed[i*16 +:16]=A[i][k];
      for(j=0;j<COLS;j=j+1) b_feed[j*8 +:8]=B[k][j];
      @(negedge clk);
    end
    feed_vld=0; a_feed='0; b_feed='0;
    repeat(ROWS+COLS+8) @(negedge clk);
    feed_pulse=1; @(negedge clk); feed_pulse=0;
    for(t=0;t<80;t=t+1) begin @(negedge clk); if(done) t=80; end
    if(!done) begin $display("GEMM_FAIL no_done busy=%b",busy); $finish(1); end
    for(i=0;i<ROWS;i=i+1) begin
      drain_row=i[$clog2(ROWS)-1:0]; #1;
      for(j=0;j<COLS;j=j+1)
        if($signed(snap_row[j*40 +:40]) !== G[i][j]) begin
          $display("GEMM_FAIL row=%0d col=%0d got=%0d exp=%0d",i,j,$signed(snap_row[j*40 +:40]),G[i][j]); $finish(1);
        end
    end
    $display("TB_W8A16_GEMM PASS"); $finish(0);
  end
endmodule
