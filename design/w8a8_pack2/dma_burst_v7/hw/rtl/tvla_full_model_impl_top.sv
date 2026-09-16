// Compact synthesis wrapper.  It exposes the command/data streams and folds
// wide internal activity into a monitor bus so Vivado keeps all blocks.
`ifndef TVLA_FULL_MODEL_IMPL_TOP_SV
`define TVLA_FULL_MODEL_IMPL_TOP_SV
`timescale 1ns/1ps
module tvla_full_model_impl_top (
  input logic clk, input logic rst_n,
  input logic [63:0] cmd_word, input logic cmd_valid, output logic cmd_ready,
  input logic desc_valid, output logic desc_ready, input logic [7:0] desc_id,
  input logic [511:0] desc_data,
  input logic [127:0] activation_data, input logic activation_valid, output logic activation_ready,
  input logic [767:0] weight_data, input logic weight_valid, output logic weight_ready,
  input logic feed_pulse, input logic [3:0] drain_row,
  input logic [255:0] vector_x, input logic [255:0] vector_y, input logic vector_valid,
  output logic vector_ready, output logic vector_out_valid, input logic vector_out_ready,
  input logic [111:0] action_data, input logic action_valid, output logic action_ready,
  output logic action_out_valid, input logic action_out_ready,
  output logic [111:0] action_target, output logic action_gripper, output logic [7:0] action_step,
  output logic replay_done, output logic [31:0] architecture_observe
);
  logic [255:0] vector_out;
  logic [1023:0] activity;
  logic [31:0] architecture_observe_i;
  tvla_full_model_replay_top u_full (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(cmd_valid), .cmd_ready(cmd_ready),
    .desc_valid(desc_valid), .desc_ready(desc_ready), .desc_id(desc_id), .desc_data(desc_data),
    .activation_data(activation_data), .activation_valid(activation_valid), .activation_ready(activation_ready),
    .weight_data(weight_data), .weight_valid(weight_valid), .weight_ready(weight_ready),
    .feed_pulse(feed_pulse), .drain_row(drain_row), .vector_x(vector_x), .vector_y(vector_y),
    .vector_valid(vector_valid), .vector_ready(vector_ready), .vector_out_valid(vector_out_valid),
    .vector_out_ready(vector_out_ready), .vector_out(vector_out), .action_data(action_data),
    .action_valid(action_valid), .action_ready(action_ready), .action_out_valid(action_out_valid),
    .action_out_ready(action_out_ready), .action_target(action_target), .action_gripper(action_gripper),
    .action_step(action_step), .replay_done(replay_done), .activity_snapshot(activity),
    .architecture_observe(architecture_observe_i)
  );
  // The output is intentionally exported as a compact checksum.  The full
  // 1024-bit activity bus remains inside the replay top for simulation.
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) architecture_observe <= '0;
    else architecture_observe <= architecture_observe_i ^ activity[63:32] ^ activity[511:480];
  end
endmodule
`endif
