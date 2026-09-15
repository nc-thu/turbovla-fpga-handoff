`timescale 1ns/1ps
// Small, deterministic smoke test for the Verilator/RTL Pack2 arithmetic.
// The full randomized arithmetic check is run by test_pack2_golden.py; this
// test also checks the two-cycle DSP-model pipeline used by the wrapper.
module tb_pack2_mult_padd;
  logic clk = 1'b0;
  always #1 clk = ~clk;
  logic v_in = 1'b0, row_in = 1'b0;
  logic signed [7:0] a_in = '0, w0_in = '0, w1_in = '0;
  wire [47:0] p;
  wire v_p, row_p;
  wire signed [7:0] a_p;
  tvla_w8a8_pack2_mult_padd dut (
    .clk(clk), .v_in(v_in), .row_in(row_in), .a_in(a_in),
    .w0_in(w0_in), .w1_in(w1_in), .P(p), .v_p(v_p),
    .row_p(row_p), .a_p(a_p)
  );

  function automatic signed [47:0] expected_p(
    input integer a, input integer w0, input integer w1);
    integer q;
    begin
      q = (w1 + 128) * 65536 + (w0 + 128);
      expected_p = a * (q - 128 * (65536 + 1));
    end
  endfunction

  initial begin
    // Two idle cycles establish a known invalid prefix.
    repeat (2) @(posedge clk);
    // Exercise a mixed-sign pair and then the two endpoint values.
    @(negedge clk); v_in = 1'b1; a_in = 8'sd7; w0_in = -8'sd3; w1_in = 8'sd5;
    @(negedge clk); v_in = 1'b0;
    repeat (3) @(posedge clk);
    if (!v_p || $signed(p) !== expected_p(7, -3, 5)) begin
      $display("FAIL mixed-sign: v_p=%0d p=%0d expected=%0d", v_p, $signed(p), expected_p(7,-3,5));
      $fatal(1);
    end
    @(negedge clk); v_in = 1'b1; a_in = -8'sd128; w0_in = -8'sd128; w1_in = 8'sd127;
    @(negedge clk); v_in = 1'b0;
    repeat (3) @(posedge clk);
    if (!v_p || $signed(p) !== expected_p(-128, -128, 127)) begin
      $display("FAIL endpoint: v_p=%0d p=%0d expected=%0d", v_p, $signed(p), expected_p(-128,-128,127));
      $fatal(1);
    end
    $display("PASS tb_pack2_mult_padd");
    $finish;
  end
endmodule
