// Package-friendly wrapper for implementation.  The replay top still owns
// the complete 512-bit descriptors and 768-bit weight path internally; this
// wrapper prevents an artificial 600+ pin demo interface from blocking IO
// placement on the XCZU7EV package.
`ifndef TVLA_FULL_MODEL_BOARD_TOP_SV
`define TVLA_FULL_MODEL_BOARD_TOP_SV
module tvla_full_model_board_top (
  input logic clk, input logic rst_n,
  input logic [63:0] cmd_word, input logic cmd_valid, output logic cmd_ready,
  input logic desc_valid, output logic desc_ready, input logic [7:0] desc_id,
  input logic [15:0] desc_data,
  input logic [63:0] activation_data, input logic activation_valid, output logic activation_ready,
  input logic [63:0] weight_data, input logic weight_valid, output logic weight_ready,
  input logic feed_pulse, input logic [3:0] drain_row,
  output logic replay_done, output logic [31:0] architecture_observe
);
  logic [511:0] desc_bus;
  logic [127:0] activation_bus;
  logic [767:0] weight_bus;
  logic [255:0] vector_x_bus, vector_y_bus;
  logic [111:0] action_bus, action_target_bus;
  logic [255:0] vector_out_bus;
  logic vector_ready_i, vector_out_valid_i, action_ready_i, action_out_valid_i;
  logic action_gripper_i; logic [7:0] action_step_i;
  always_comb begin
    desc_bus = '0;
    desc_bus[15:0] = desc_data;
    for (int i=1;i<32;i=i+1) desc_bus[i*16 +: 16] = desc_data;
    activation_bus = {2{activation_data}};
    for (int i=0;i<12;i=i+1) weight_bus[i*64 +: 64] = weight_data;
    vector_x_bus = {2{activation_bus}};
    vector_y_bus = {2{activation_bus}};
    action_bus = '0;
  end
  tvla_full_model_replay_top u_full (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(cmd_valid), .cmd_ready(cmd_ready),
    .desc_valid(desc_valid), .desc_ready(desc_ready), .desc_id(desc_id), .desc_data(desc_bus),
    .activation_data(activation_bus), .activation_valid(activation_valid), .activation_ready(activation_ready),
    .weight_data(weight_bus), .weight_valid(weight_valid), .weight_ready(weight_ready),
    .feed_pulse(feed_pulse), .drain_row(drain_row), .vector_x(vector_x_bus), .vector_y(vector_y_bus),
    .vector_valid(cmd_valid), .vector_ready(vector_ready_i), .vector_out_valid(vector_out_valid_i),
    .vector_out_ready(1'b1), .vector_out(vector_out_bus), .action_data(action_bus),
    .action_valid(cmd_valid && (cmd_word[63:56] == 8'h60)), .action_ready(action_ready_i), .action_out_valid(action_out_valid_i),
    .action_out_ready(1'b1), .action_target(action_target_bus), .action_gripper(action_gripper_i),
    .action_step(action_step_i), .replay_done(replay_done), .activity_snapshot(),
    .architecture_observe(architecture_observe)
  );
endmodule
`endif
