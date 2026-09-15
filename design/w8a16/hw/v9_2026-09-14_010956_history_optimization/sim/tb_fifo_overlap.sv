`timescale 1ns/1ps
// Ready/valid regression for the descriptor FIFO.  The first version of the
// replay top assigned fifo_count twice in one clock; this test exercises the
// push+pop case that a real instruction stream uses.
module tb_fifo_overlap;
  logic clk = 0, rst_n = 0;
  always #2 clk = ~clk;
  logic [63:0] cmd_word = 0;
  logic cmd_valid = 0;
  wire cmd_ready;
  logic desc_valid = 0;
  wire desc_ready;
  logic [15:0] desc_id = 0;
  logic [511:0] desc_data = 0;
  wire replay_done;
  wire [1023:0] activity_snapshot;
  wire [63:0] activity_output_bytes, activity_queue_max_occupancy;
  wire [63:0] activity_optimization_hits, activity_write_burst_count;
  tvla_replay_top #(.DESC_FIFO_DEPTH(4), .ENABLE_ARRAY(1'b0), .TRACE_ENABLE(1'b0)) dut (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(cmd_valid), .cmd_ready(cmd_ready),
    .desc_valid(desc_valid), .desc_ready(desc_ready), .desc_id(desc_id), .desc_data(desc_data),
    .activation_data('0), .activation_valid(1'b0), .activation_ready(),
    .weight_data('0), .weight_valid(1'b0), .weight_ready(), .feed_pulse(1'b0), .drain_row('0),
    .snapshot_row(), .output_valid(), .output_ready(1'b1), .output_data(),
    .fallback_valid(1'b0), .fallback_ready(), .fallback_data('0), .replay_done(replay_done),
    .activity_snapshot(activity_snapshot), .activity_output_bytes(activity_output_bytes),
    .activity_queue_max_occupancy(activity_queue_max_occupancy),
    .activity_optimization_hits(activity_optimization_hits), .activity_write_burst_count(activity_write_burst_count)
  );

  task automatic put_desc(input integer id, input [7:0] op);
    integer guard;
    begin
      @(negedge clk); desc_id = id[15:0]; desc_data = '0; desc_data[63:56] = op; desc_data[511:480] = 32'd7; desc_data[351:320] = 32'd7; desc_data[479:448] = 32'd3; desc_valid = 1'b1;
      guard = 0; while (!desc_ready) begin @(negedge clk); guard = guard + 1; if (guard > 20) $fatal(1, "descriptor ready timeout count=%0d", dut.fifo_count); end
      @(negedge clk); desc_valid = 1'b0;
    end
  endtask

  task automatic pop_cmd(input integer id, input [7:0] op);
    integer guard;
    begin
      @(negedge clk); cmd_word = '0; cmd_word[63:56] = op; cmd_word[47:32] = id[15:0]; cmd_valid = 1'b1;
      guard = 0; while (!cmd_ready) begin @(negedge clk); guard = guard + 1; if (guard > 20) $fatal(1, "command ready timeout id=%0d count=%0d", id, dut.fifo_count); end
      @(negedge clk); cmd_valid = 1'b0;
    end
  endtask

  initial begin
    repeat (3) @(negedge clk); rst_n = 1'b1;
    // Seed the FIFO.  Afterwards push descriptor 2 while popping descriptor 1.
    put_desc(1, 8'h50);
    $display("after first put count=%0d ready=%b", dut.fifo_count, cmd_ready);
    @(negedge clk); desc_id = 2; desc_data = '0; desc_data[63:56] = 8'h50; desc_data[511:480] = 32'd11; desc_data[351:320] = 32'd11; desc_valid = 1'b1;
    cmd_word = '0; cmd_word[63:56] = 8'h50; cmd_word[47:32] = 16'd1; cmd_valid = 1'b1;
    if (!desc_ready || !cmd_ready) $fatal(1, "push+pop was not accepted");
    @(negedge clk); desc_valid = 1'b0; cmd_valid = 1'b0;
    $display("after push+pop count=%0d ready=%b", dut.fifo_count, cmd_ready);
    if (dut.fifo_count != 1) $fatal(1, "push+pop count=%0d", dut.fifo_count);
    pop_cmd(2, 8'h50);
    $display("after second pop count=%0d ready=%b", dut.fifo_count, cmd_ready);
    if (dut.fifo_count != 0) $fatal(1, "second pop count=%0d", dut.fifo_count);
    @(negedge clk); cmd_word = 64'hff00000000000000; cmd_valid = 1'b1; #1ps;
    $display("END probe word=%h is_end=%b slot_free=%b ready=%b count=%0d done=%b", cmd_word, dut.cmd_is_end, dut.result_slot_free, cmd_ready, dut.fifo_count, replay_done);
    if (!cmd_ready) $fatal(1, "END was not ready count=%0d done=%b", dut.fifo_count, replay_done);
    @(negedge clk); cmd_valid = 1'b0;
    repeat (2) @(negedge clk);
    if (!replay_done) $fatal(1, "END not accepted");
    $display("TB_FIFO_OVERLAP PASS count=%0d queue_max=%0d", dut.fifo_count, activity_queue_max_occupancy);
    $finish;
  end
endmodule
