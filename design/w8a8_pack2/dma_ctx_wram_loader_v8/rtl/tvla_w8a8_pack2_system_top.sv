// Synthesizable command/descriptor top for the TurboVLA Pack2 replay path.
// The wrapper keeps the public stream protocol of replay_top while selecting
// the timing-pipelined array implementation in this version.
`ifndef TVLA_W8A8_PACK2_SYSTEM_TOP_SV
`define TVLA_W8A8_PACK2_SYSTEM_TOP_SV
module tvla_w8a8_pack2_system_top #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int DESC_W = 512,
  parameter int DESC_ID_W = 16,
  parameter int DESC_FIFO_DEPTH = 16,
  parameter bit ENABLE_ARRAY = 1'b1
)(
  input logic clk, input logic rst_n,
  input logic [63:0] cmd_word, input logic cmd_valid, output logic cmd_ready,
  input logic desc_valid, output logic desc_ready,
  input logic [DESC_ID_W-1:0] desc_id, input logic [DESC_W-1:0] desc_data,
  input logic [ROWS*8-1:0] activation_data, input logic activation_valid,
  output logic activation_ready,
  input logic [PCOLS*16-1:0] weight_data, input logic weight_valid,
  output logic weight_ready,
  input logic feed_pulse,
  input logic [((ROWS <= 1) ? 1 : $clog2(ROWS))-1:0] drain_row,
  output logic [PCOLS*2*32-1:0] snapshot_row,
  output logic output_valid, input logic output_ready,
  output logic [PCOLS*2*32-1:0] output_data,
  input logic fallback_valid, output logic fallback_ready,
  input logic [63:0] fallback_data,
  output logic replay_done,
  output logic [1023:0] activity_snapshot,
  output logic [63:0] activity_output_bytes,
  output logic [63:0] activity_queue_max_occupancy,
  output logic [63:0] activity_optimization_hits,
  output logic [63:0] activity_write_burst_count
);
  // The timing-specific replay top is kept separate from the v1 module so
  // old RTL and old reports remain untouched.
  tvla_w8a8_pack2_replay_top_timing #(
    .ROWS(ROWS), .PCOLS(PCOLS), .DESC_W(DESC_W),
    .DESC_ID_W(DESC_ID_W), .DESC_FIFO_DEPTH(DESC_FIFO_DEPTH),
    .ENABLE_ARRAY(ENABLE_ARRAY)
  ) u_replay (
    .clk(clk), .rst_n(rst_n),
    .cmd_word(cmd_word), .cmd_valid(cmd_valid), .cmd_ready(cmd_ready),
    .desc_valid(desc_valid), .desc_ready(desc_ready),
    .desc_id(desc_id), .desc_data(desc_data),
    .activation_data(activation_data), .activation_valid(activation_valid),
    .activation_ready(activation_ready),
    .weight_data(weight_data), .weight_valid(weight_valid),
    .weight_ready(weight_ready), .feed_pulse(feed_pulse),
    .drain_row(drain_row), .snapshot_row(snapshot_row),
    .output_valid(output_valid), .output_ready(output_ready),
    .output_data(output_data), .fallback_valid(fallback_valid),
    .fallback_ready(fallback_ready), .fallback_data(fallback_data),
    .replay_done(replay_done), .activity_snapshot(activity_snapshot),
    .activity_output_bytes(activity_output_bytes),
    .activity_queue_max_occupancy(activity_queue_max_occupancy),
    .activity_optimization_hits(activity_optimization_hits),
    .activity_write_burst_count(activity_write_burst_count)
  );
endmodule
`endif
