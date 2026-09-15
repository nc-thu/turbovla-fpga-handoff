`timescale 1ns/1ps
module tb_w8a16_pe;
  logic clk = 0, rst_n = 0, clr = 0, pulse_in = 0, av_in = 0, bv_in = 0;
  logic signed [15:0] a_in;
  logic signed [7:0] b_in;
  logic av_out, bv_out, pulse_out;
  logic signed [15:0] a_out;
  logic signed [7:0] b_out;
  logic signed [39:0] acc, snap;
  always #5 clk = ~clk;

  w8a16_pe #(.ACC_W(40)) dut (
    .clk(clk), .rst_n(rst_n), .clr(clr), .pulse_in(pulse_in),
    .av_in(av_in), .bv_in(bv_in), .a_in(a_in), .b_in(b_in),
    .av_out(av_out), .bv_out(bv_out), .pulse_out(pulse_out), .a_out(a_out), .b_out(b_out),
    .acc(acc), .snap(snap)
  );

  integer i;
  integer signed expected;
  integer signed avalue;
  integer signed bvalue;

  task drive_one(input integer signed aa, input integer signed bb);
    begin
      @(negedge clk); a_in = aa; b_in = bb; av_in = 1'b1; bv_in = 1'b1;
      @(negedge clk); av_in = 1'b0; bv_in = 1'b0; a_in = 0; b_in = 0;
    end
  endtask

  initial begin
    a_in = 0; b_in = 0; expected = 0;
    repeat (3) @(negedge clk);
    rst_n = 1;
    // Endpoint products.
    drive_one(-32768, -128); expected = expected + (-32768)*(-128);
    drive_one(32767, 127);   expected = expected + 32767*127;
    drive_one(-1, 1);        expected = expected - 1;
    drive_one(0, -128);
    repeat (10) @(negedge clk);
    if ($signed(acc) !== expected) begin
      $display("PE_ACC_FAIL got=%0d exp=%0d", $signed(acc), expected);
      $finish(1);
    end
    // Snapshot must capture the live state and then clear it.
    @(negedge clk); pulse_in = 1'b1;
    @(negedge clk); pulse_in = 1'b0;
    repeat (2) @(negedge clk);
    if ($signed(snap) !== expected || $signed(acc) !== 0) begin
      $display("PE_SNAPSHOT_FAIL snap=%0d acc=%0d exp=%0d", $signed(snap), $signed(acc), expected);
      $finish(1);
    end
    // Bubble and random signed products after a clear.
    @(negedge clk); clr = 1'b1;
    @(negedge clk); clr = 1'b0;
    expected = 0;
    for (i = 0; i < 16; i = i + 1) begin
      avalue = ((i * 7919) % 65536) - 32768;
      bvalue = ((i * 37) % 256) - 128;
      drive_one(avalue, bvalue);
      expected = expected + avalue*bvalue;
      if ((i % 3) == 0) repeat (2) @(negedge clk);
    end
    repeat (10) @(negedge clk);
    if ($signed(acc) !== expected) begin
      $display("PE_RANDOM_FAIL got=%0d exp=%0d", $signed(acc), expected);
      $finish(1);
    end
    $display("TB_W8A16_PE PASS acc=%0d", $signed(acc));
    $finish(0);
  end
endmodule
