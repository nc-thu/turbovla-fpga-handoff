`timescale 1ns/1ps
module tb_replay_top;
  localparam int N = 432;
  logic clk=0, rst_n=0;
  always #2 clk = ~clk;
  logic [63:0] cmd_word; logic cmd_valid; wire cmd_ready;
  logic desc_valid; wire desc_ready; logic [15:0] desc_id; logic [511:0] desc_data;
  logic [255:0] activation_data=0; logic activation_valid=0; wire activation_ready;
  logic [383:0] weight_data=0; logic weight_valid=0; wire weight_ready;
  logic feed_pulse=0; logic [3:0] drain_row=0;
  wire [1919:0] snapshot_row; wire output_valid; logic output_ready=1; wire [1919:0] output_data;
  logic fallback_valid=0; wire fallback_ready; logic [63:0] fallback_data=0;
  wire replay_done; wire [1023:0] activity_snapshot; wire [63:0] activity_output_bytes; wire [63:0] activity_queue_max_occupancy; wire [63:0] activity_optimization_hits; wire [63:0] activity_write_burst_count;
  logic [511:0] desc_mem [0:N-1];
  logic [7:0] op_mem [0:N];
  integer i;
  tvla_replay_top #(.DESC_FIFO_DEPTH(16), .TRACE_ENABLE(1'b1), .ENABLE_ARRAY(1'b0)) dut (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(cmd_valid), .cmd_ready(cmd_ready),
    .desc_valid(desc_valid), .desc_ready(desc_ready), .desc_id(desc_id), .desc_data(desc_data),
    .activation_data(activation_data), .activation_valid(activation_valid), .activation_ready(activation_ready),
    .weight_data(weight_data), .weight_valid(weight_valid), .weight_ready(weight_ready), .feed_pulse(feed_pulse),
    .drain_row(drain_row), .snapshot_row(snapshot_row), .output_valid(output_valid), .output_ready(output_ready), .output_data(output_data),
    .fallback_valid(fallback_valid), .fallback_ready(fallback_ready), .fallback_data(fallback_data),
    .replay_done(replay_done), .activity_snapshot(activity_snapshot), .activity_output_bytes(activity_output_bytes), .activity_queue_max_occupancy(activity_queue_max_occupancy), .activity_optimization_hits(activity_optimization_hits), .activity_write_burst_count(activity_write_burst_count)
  );
  task send_one(input integer idx);
    reg [7:0] opcode;
    integer guard;
    begin
      opcode = desc_mem[idx][63:56];
      @(negedge clk); desc_valid=1; desc_id=idx[15:0]; desc_data=desc_mem[idx];
      guard=0; while (!desc_ready) begin @(negedge clk); guard=guard+1; if (guard>1000) $fatal(1,"descriptor wait idx=%0d",idx); end
      @(negedge clk); desc_valid=0;
      cmd_word=64'b0; cmd_word[63:56]=opcode; cmd_word[55:48]=8'h80; cmd_word[47:32]=idx[15:0]; cmd_word[15:0]=idx[15:0]; cmd_valid=1;
      guard=0; while (!cmd_ready) begin @(negedge clk); guard=guard+1; if (guard>1000) $fatal(1,"command wait idx=%0d op=%h count=%0d done=%b",idx,opcode,dut.fifo_count,replay_done); end
      @(negedge clk); cmd_valid=0;
    end
  endtask
  initial begin
    $readmemh("../data/descriptor_words.hex", desc_mem);
    repeat (4) @(negedge clk); rst_n=1;
    cmd_valid=0; desc_valid=0; cmd_word=0; desc_id=0; desc_data=0;
    for (i=0; i<N; i=i+1) begin
      if (i >= 400) $display("tail index %0d op=%h", i, desc_mem[i][63:56]);
      send_one(i);
      if ((i % 50) == 0) $display("progress %0d/%0d", i, N);
    end
    @(negedge clk); cmd_word=64'hff00000000000000; cmd_valid=1; #0;
    $display("END start ready=%b done=%b op=%h count=%0d", cmd_ready, replay_done, dut.cmd_op, dut.fifo_count);
    begin : wait_end
      integer end_guard;
      end_guard=0;
      while (!cmd_ready) begin @(negedge clk); end_guard=end_guard+1; if (end_guard>1000) $fatal(1,"END wait ready=%b done=%b op=%h count=%0d",cmd_ready,replay_done,dut.cmd_op,dut.fifo_count); end
    end
    @(negedge clk); cmd_valid=0;
    repeat (3) @(negedge clk);
    $display("ACTIVITY total=%0d mapped=%0d fallback=%0d active=%0d mac=%0d tiles=%0d output_bytes=%0d queue_max=%0d opt_hits=%0d bursts=%0d", activity_snapshot[63:0], activity_snapshot[127:64], activity_snapshot[191:128], activity_snapshot[703:640], activity_snapshot[831:768], activity_snapshot[895:832], activity_output_bytes, activity_queue_max_occupancy, activity_optimization_hits, activity_write_burst_count);
    if (activity_snapshot[63:0] != 64'd75254992) $fatal(1, "total cycle mismatch");
    if (activity_snapshot[127:64] != 64'd70349280) $fatal(1, "mapped cycle mismatch");
    if (activity_snapshot[191:128] != 64'd4905712) $fatal(1, "fallback cycle mismatch");
    if (activity_snapshot[831:768] != 64'd49584342528) $fatal(1, "MAC mismatch");
    if (activity_snapshot[895:832] != 64'd79807) $fatal(1, "tile mismatch");
    if (activity_output_bytes != 64'd164575944) $fatal(1, "output bytes mismatch");
    if (activity_queue_max_occupancy < 64'd1) $fatal(1, "queue max mismatch");
    if (!replay_done) $fatal(1, "replay did not finish");
    $finish;
  end
endmodule
