// Final action formatter.  This is deliberately a narrow interface: the
// policy may stream one action vector at a time, while the robot side sees a
// stable, clamped target and a step-valid pulse.
`ifndef TVLA_ACTION_POST_SV
`define TVLA_ACTION_POST_SV
module tvla_action_post #(
  parameter int ACTION_DIM = 7,
  parameter int DW = 16,
  parameter int STEP_W = 8
) (
  input logic clk,
  input logic rst_n,
  input logic in_valid,
  output logic in_ready,
  input logic signed [ACTION_DIM*DW-1:0] in_action,
  input logic [STEP_W-1:0] step_index,
  input logic [DW-1:0] pos_min,
  input logic [DW-1:0] pos_max,
  output logic out_valid,
  input logic out_ready,
  output logic signed [ACTION_DIM*DW-1:0] robot_target,
  output logic [STEP_W-1:0] robot_step,
  output logic robot_gripper
);
  logic holding;
  integer i;
  integer signed v;
  integer signed lo;
  integer signed hi;
  assign in_ready = !holding || (out_valid && out_ready);
  assign out_valid = holding;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      holding <= 1'b0;
      robot_target <= '0;
      robot_step <= '0;
      robot_gripper <= 1'b0;
    end else begin
      if (holding && out_ready) holding <= 1'b0;
      if (in_valid && in_ready) begin
        lo = $signed(pos_min);
        hi = $signed(pos_max);
        for (i = 0; i < ACTION_DIM; i = i + 1) begin
          v = $signed(in_action[i*DW +: DW]);
          if (i == ACTION_DIM-1) begin
            robot_target[i*DW +: DW] <= (v < 0) ? 16'sh0000 : 16'sh7fff;
            robot_gripper <= (v >= 0);
          end else if (v < lo) robot_target[i*DW +: DW] <= pos_min;
          else if (v > hi) robot_target[i*DW +: DW] <= pos_max;
          else robot_target[i*DW +: DW] <= in_action[i*DW +: DW];
        end
        robot_step <= step_index;
        holding <= 1'b1;
      end
    end
  end
endmodule
`endif
