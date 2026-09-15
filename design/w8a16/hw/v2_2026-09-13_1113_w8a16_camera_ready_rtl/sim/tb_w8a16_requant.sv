`timescale 1ns/1ps
module tb_w8a16_requant;
  logic clk = 0, rst_n = 0, in_vld = 0;
  logic signed [39:0] x;
  logic signed [15:0] multiplier;
  logic [7:0] shift;
  logic out_vld;
  logic signed [15:0] y;
  always #5 clk = ~clk;
  w8a16_requant #(.ACC_W(40)) dut (.*);

  task send(input integer signed xx, input integer signed mm, input integer ss);
    begin
      @(negedge clk); x = xx; multiplier = mm; shift = ss; in_vld = 1;
      @(negedge clk); in_vld = 0; x = 0; multiplier = 0; shift = 0;
      @(negedge clk);
    end
  endtask

  initial begin
    x = 0; multiplier = 0; shift = 0;
    repeat (2) @(negedge clk); rst_n = 1;
    send(1000, 2, 1);
    if ($signed(y) !== 1000) begin $display("REQUANT_FAIL normal got=%0d", $signed(y)); $finish(1); end
    send(40000, 2, 0);
    if ($signed(y) !== 32767) begin $display("REQUANT_FAIL high got=%0d", $signed(y)); $finish(1); end
    send(-40000, 2, 0);
    if ($signed(y) !== -32768) begin $display("REQUANT_FAIL low got=%0d", $signed(y)); $finish(1); end
    $display("TB_W8A16_REQUANT PASS");
    $finish(0);
  end
endmodule
