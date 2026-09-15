`timescale 1ns/1ps
// Protocol and accounting smoke test.  It deliberately disables the large
// array so that the test exercises the descriptor FIFO and activity monitor
// independently from the arithmetic regression.
module tb_replay_top;
  localparam int DW = 512;
  logic clk = 1'b0; always #1 clk = ~clk;
  logic rst_n = 1'b0;
  logic [63:0] cmd_word = '0; logic cmd_valid = 1'b0; wire cmd_ready;
  logic desc_valid = 1'b0; wire desc_ready; logic [15:0] desc_id = '0;
  logic [DW-1:0] desc_data = '0;
  logic [127:0] activation_data = '0; logic activation_valid = 1'b0; wire activation_ready;
  logic [767:0] weight_data = '0; logic weight_valid = 1'b0; wire weight_ready;
  logic feed_pulse = 1'b0;
  logic [3:0] drain_row = '0;
  wire [3071:0] snapshot_row;
  wire output_valid; logic output_ready = 1'b1; wire [3071:0] output_data;
  logic fallback_valid = 1'b0; wire fallback_ready; logic [63:0] fallback_data = '0;
  wire replay_done; wire [1023:0] activity_snapshot;
  wire [63:0] activity_output_bytes, activity_queue_max_occupancy,
              activity_optimization_hits, activity_write_burst_count;

  tvla_w8a8_pack2_replay_top_timing #(.ENABLE_ARRAY(1'b0)) dut (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(cmd_valid), .cmd_ready(cmd_ready),
    .desc_valid(desc_valid), .desc_ready(desc_ready), .desc_id(desc_id), .desc_data(desc_data),
    .activation_data(activation_data), .activation_valid(activation_valid), .activation_ready(activation_ready),
    .weight_data(weight_data), .weight_valid(weight_valid), .weight_ready(weight_ready),
    .feed_pulse(feed_pulse), .drain_row(drain_row), .snapshot_row(snapshot_row),
    .output_valid(output_valid), .output_ready(output_ready), .output_data(output_data),
    .fallback_valid(fallback_valid), .fallback_ready(fallback_ready), .fallback_data(fallback_data),
    .replay_done(replay_done), .activity_snapshot(activity_snapshot),
    .activity_output_bytes(activity_output_bytes), .activity_queue_max_occupancy(activity_queue_max_occupancy),
    .activity_optimization_hits(activity_optimization_hits), .activity_write_burst_count(activity_write_burst_count)
  );

  task automatic put_descriptor(input [15:0] id, input [7:0] op, input [7:0] flags,
                                input integer total, input integer valid_mac);
    begin
      desc_id = id; desc_data = '0;
      desc_data[511:480] = total; desc_data[479:448] = valid_mac;
      desc_data[447:416] = valid_mac / 2;
      desc_data[415:384] = 2; desc_data[383:352] = 3;
      desc_data[319:288] = 1; desc_data[287:256] = 1;
      desc_data[255:224] = 16; desc_data[223:192] = 48; desc_data[191:160] = 16;
      desc_data[31:16] = 1; desc_data[63:56] = op; desc_data[55:48] = flags;
      @(negedge clk); desc_valid = 1'b1;
      while (!desc_ready) @(negedge clk);
      @(negedge clk); desc_valid = 1'b0;
    end
  endtask

  task automatic issue_command(input [63:0] word);
    begin
      @(negedge clk); cmd_word = word; cmd_valid = 1'b1;
      // The caller has already queued the matching descriptor (or is issuing
      // END after the FIFO is empty).  Sample one following rising edge for
      // the handshake, then drop valid.  Waiting on ready after END would
      // deadlock because replay_done intentionally deasserts ready.
      @(posedge clk);
      if (!cmd_ready && word[63:56] != 8'hff) begin
        $display("FAIL command not ready op=%h", word[63:56]); $fatal(1);
      end
      @(negedge clk); cmd_valid = 1'b0;
    end
  endtask

  initial begin
    fork
      begin #2000; $display("FAIL watchdog t=%0t ready(d,c)=%0d,%0d count=%0d done=%0d", $time, desc_ready, cmd_ready, dut.fifo_count, replay_done); $fatal(1); end
    join_none
    repeat (2) @(negedge clk); rst_n = 1'b1;
    $display("reset released t=%0t", $time);
    fork
      put_descriptor(16'd1, 8'h18, 8'h80, 10, 20);
    join
    issue_command(64'h1800000100000000);
    $display("command accepted t=%0t", $time);
    repeat (2) @(negedge clk);
    if (activity_snapshot[63:0] !== 64'd10 || activity_snapshot[127:64] !== 64'd10 ||
        activity_snapshot[831:768] !== 64'd20 || activity_queue_max_occupancy < 1) begin
      $display("FAIL accounting total=%0d mapped=%0d mac=%0d qmax=%0d",
        activity_snapshot[63:0], activity_snapshot[127:64], activity_snapshot[831:768], activity_queue_max_occupancy);
      $fatal(1);
    end
    issue_command(64'hff00000000000000);
    @(negedge clk);
    if (!replay_done) begin $display("FAIL replay_done"); $fatal(1); end
    $display("PASS tb_replay_top"); $finish;
  end
endmodule
