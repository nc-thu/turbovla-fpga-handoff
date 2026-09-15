`timescale 1ns/1ps
// Small, cycle-by-cycle top-level check.  The full trace uses ENABLE_ARRAY=0
// to accumulate virtual event time; this test turns the 2x3 array on and
// checks the real feed, wavefront, snapshot and readout path.
module tb_replay_array_tile;
  localparam int ROWS=2, COLS=3, K=5;
  logic clk=0, rst_n=0;
  always #5 clk=~clk;
  logic [63:0] cmd_word; logic cmd_valid; wire cmd_ready;
  logic desc_valid; wire desc_ready; logic [15:0] desc_id; logic [511:0] desc_data;
  logic [ROWS*16-1:0] activation_data; logic activation_valid; wire activation_ready;
  logic [COLS*8-1:0] weight_data; logic weight_valid; wire weight_ready;
  logic feed_pulse; logic [$clog2(ROWS)-1:0] drain_row;
  wire [COLS*40-1:0] snapshot_row; wire output_valid; logic output_ready=1; wire [COLS*40-1:0] output_data;
  logic fallback_valid=0; wire fallback_ready; logic [63:0] fallback_data=0;
  wire replay_done; wire [1023:0] activity_snapshot; wire [63:0] activity_output_bytes; wire [63:0] activity_queue_max_occupancy;
  tvla_replay_top #(.ROWS(ROWS),.PCOLS(COLS),.DESC_FIFO_DEPTH(4),.ENABLE_ARRAY(1'b1)) dut(
    .clk(clk),.rst_n(rst_n),.cmd_word(cmd_word),.cmd_valid(cmd_valid),.cmd_ready(cmd_ready),
    .desc_valid(desc_valid),.desc_ready(desc_ready),.desc_id(desc_id),.desc_data(desc_data),
    .activation_data(activation_data),.activation_valid(activation_valid),.activation_ready(activation_ready),
    .weight_data(weight_data),.weight_valid(weight_valid),.weight_ready(weight_ready),.feed_pulse(feed_pulse),
    .drain_row(drain_row),.snapshot_row(snapshot_row),.output_valid(output_valid),.output_ready(output_ready),.output_data(output_data),
    .fallback_valid(fallback_valid),.fallback_ready(fallback_ready),.fallback_data(fallback_data),
    .replay_done(replay_done),.activity_snapshot(activity_snapshot),.activity_output_bytes(activity_output_bytes),.activity_queue_max_occupancy(activity_queue_max_occupancy));
  integer A[0:ROWS-1][0:K-1], B[0:K-1][0:COLS-1], G[0:ROWS-1][0:COLS-1];
  integer i,j,k;
  initial begin
    cmd_word='0; cmd_valid=0; desc_valid=0; desc_id=0; desc_data='0;
    activation_data='0; activation_valid=0; weight_data='0; weight_valid=0; feed_pulse=0; drain_row=0;
    for(i=0;i<ROWS;i=i+1) for(k=0;k<K;k=k+1) A[i][k]=(i+1)*(k-2);
    for(k=0;k<K;k=k+1) for(j=0;j<COLS;j=j+1) B[k][j]=(j-1)*(k+1);
    for(i=0;i<ROWS;i=i+1) for(j=0;j<COLS;j=j+1) begin G[i][j]=0; for(k=0;k<K;k=k+1) G[i][j]=G[i][j]+A[i][k]*B[k][j]; end
    repeat(3) @(negedge clk); rst_n=1;
    // one descriptor: total=64, valid MAC=ROWS*COLS*K, active=the same,
    // bytes are included so the top's sideband unpacking is exercised.
    @(negedge clk); desc_id=16'd0; desc_data='0; desc_data[511:480]=64; desc_data[479:448]=ROWS*COLS*K; desc_data[447:416]=ROWS*COLS*K; desc_data[415:384]=ROWS*K*2; desc_data[383:352]=K*COLS; desc_data[191:160]=ROWS*COLS*2; desc_data[159:128]=ROWS; desc_data[127:96]=COLS; desc_data[95:64]=K; desc_data[63:56]=8'h10; desc_data[31:16]=1; desc_valid=1;
    @(negedge clk); desc_valid=0;
    @(negedge clk); cmd_word=64'b0; cmd_word[63:56]=8'h10; cmd_word[47:32]=0; cmd_valid=1;
    while(!cmd_ready) @(negedge clk);
    @(negedge clk); cmd_valid=0;
    // Feed one K slice per cycle.  A and B are signed two's-complement.
    activation_valid=1; weight_valid=1;
    for(k=0;k<K;k=k+1) begin
      for(i=0;i<ROWS;i=i+1) activation_data[i*16 +: 16]=A[i][k];
      for(j=0;j<COLS;j=j+1) weight_data[j*8 +: 8]=B[k][j];
      @(negedge clk);
    end
    activation_valid=0; weight_valid=0; activation_data='0; weight_data='0;
    repeat(8) @(negedge clk);
    feed_pulse=1; @(negedge clk); feed_pulse=0;
    repeat(24) @(negedge clk);
    for(i=0;i<ROWS;i=i+1) begin
      drain_row=i[$clog2(ROWS)-1:0]; #1;
      for(j=0;j<COLS;j=j+1) if($signed(snapshot_row[j*40 +: 40]) !== G[i][j]) begin
        $display("ARRAY_TOP_FAIL row=%0d col=%0d got=%0d exp=%0d",i,j,$signed(snapshot_row[j*40 +: 40]),G[i][j]); $fatal(1);
      end
    end
    $display("TB_REPLAY_ARRAY_TILE PASS"); $finish;
  end
endmodule
