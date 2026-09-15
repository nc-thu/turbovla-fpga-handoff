`timescale 1ns/1ps
module tb_replay_debug;
  logic clk=0,rst_n=0; always #2 clk=~clk;
  logic [63:0] cmd_word; logic cmd_valid; wire cmd_ready; logic desc_valid; wire desc_ready; logic [15:0] desc_id; logic [511:0] desc_data;
  wire [1023:0] activity_snapshot; wire replay_done;
  logic [255:0] activation_data=0; logic activation_valid=0; wire activation_ready; logic [383:0] weight_data=0; logic weight_valid=0; wire weight_ready; logic feed_pulse=0; logic [3:0] drain_row=0; wire [1919:0] snapshot_row; wire output_valid; logic output_ready=1; wire [1919:0] output_data; logic fallback_valid=0; wire fallback_ready; logic [63:0] fallback_data=0;
  logic [511:0] mem[0:431]; integer i;
  tvla_replay_top #(.ENABLE_ARRAY(0),.DESC_FIFO_DEPTH(16)) dut(.clk(clk),.rst_n(rst_n),.cmd_word(cmd_word),.cmd_valid(cmd_valid),.cmd_ready(cmd_ready),.desc_valid(desc_valid),.desc_ready(desc_ready),.desc_id(desc_id),.desc_data(desc_data),.activation_data(activation_data),.activation_valid(activation_valid),.activation_ready(activation_ready),.weight_data(weight_data),.weight_valid(weight_valid),.weight_ready(weight_ready),.feed_pulse(feed_pulse),.drain_row(drain_row),.snapshot_row(snapshot_row),.output_valid(output_valid),.output_ready(output_ready),.output_data(output_data),.fallback_valid(fallback_valid),.fallback_ready(fallback_ready),.fallback_data(fallback_data),.replay_done(replay_done),.activity_snapshot(activity_snapshot));
  initial begin
    $readmemh("../data/descriptor_words.hex",mem);
    repeat(3) @(negedge clk); rst_n=1; cmd_valid=0; desc_valid=0;
    for(i=0;i<3;i=i+1) begin
      @(negedge clk); desc_id=i; desc_data=mem[i]; desc_valid=1; $display("desc %0d ready=%b count=%0d",i,desc_ready,dut.fifo_count);
      @(negedge clk); desc_valid=0; $display("after desc count=%0d head=%0d id=%0d",dut.fifo_count,dut.fifo_head,dut.id_fifo[dut.fifo_head]);
      @(negedge clk); cmd_word=0; cmd_word[63:56]=mem[i][63:56]; cmd_word[47:32]=i; cmd_valid=1; $display("cmd %0d op=%h id=%0d headid=%0d empty=%b match=%b done=%b ready=%b head=%0d count=%0d",i,cmd_word[63:56],dut.cmd_desc_id,dut.id_fifo[dut.fifo_head],dut.fifo_empty,dut.cmd_matches_head,dut.replay_done,cmd_ready,dut.fifo_head,dut.fifo_count);
      @(negedge clk); cmd_valid=0; $display("after cmd count=%0d head=%0d total=%0d",dut.fifo_count,dut.fifo_head,activity_snapshot[63:0]);
    end
    @(negedge clk); cmd_word=64'hff00000000000000; cmd_valid=1; $display("end ready=%b",cmd_ready); @(negedge clk); cmd_valid=0; repeat(2) @(negedge clk); $display("done=%b total=%0d",replay_done,activity_snapshot[63:0]); $finish;
  end
endmodule
