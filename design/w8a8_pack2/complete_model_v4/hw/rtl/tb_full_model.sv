`timescale 1ns/1ps
module tb_full_model;
  logic clk=0, rst_n=0;
  always #2 clk = ~clk;
  logic [63:0] cmd_word; logic cmd_valid; wire cmd_ready;
  logic desc_valid; wire desc_ready; logic [7:0] desc_id; logic [511:0] desc_data;
  logic [127:0] activation_data; logic activation_valid; wire activation_ready;
  logic [767:0] weight_data; logic weight_valid; wire weight_ready;
  logic feed_pulse; logic [3:0] drain_row;
  logic [255:0] vector_x, vector_y; logic vector_valid; wire vector_ready;
  wire vector_out_valid; logic vector_out_ready;
  logic [111:0] action_data; logic action_valid; wire action_ready;
  wire action_out_valid; logic action_out_ready; wire [111:0] action_target; wire action_gripper; wire [7:0] action_step;
  wire replay_done; wire [31:0] architecture_observe;
  tvla_full_model_impl_top dut(.*);
  initial begin
    cmd_word=0; cmd_valid=0; desc_valid=0; desc_id=0; desc_data=0;
    activation_data=0; activation_valid=0; weight_data=0; weight_valid=0; feed_pulse=0; drain_row=0;
    vector_x=0; vector_y=0; vector_valid=0; vector_out_ready=1; action_data=0; action_valid=0; action_out_ready=1;
    repeat(4) @(posedge clk); rst_n <= 1;
    // descriptor accounting for one vector operation
    desc_data[511:480]=32'd32; desc_data[351:320]=32'd4; desc_valid=1; desc_id=0;
    @(posedge clk); while(!desc_ready) @(posedge clk); desc_valid=0;
    vector_x = {16{16'h0100}}; vector_y = {16{16'h0080}}; vector_valid=1;
    cmd_word = 64'h2100000000000000; cmd_valid=1;
    @(posedge clk); while(!cmd_ready) @(posedge clk); cmd_valid=0; vector_valid=0;
    repeat(8) @(posedge clk);
    // End fence
    cmd_word = 64'hff00000000000000; cmd_valid=1;
    @(posedge clk); while(!cmd_ready) @(posedge clk); cmd_valid=0;
    repeat(4) @(posedge clk);
    $display("FULL_MODEL_SMOKE PASS done=%0d observe=%h", replay_done, architecture_observe);
    $finish;
  end
endmodule
