`timescale 1ns/1ps
module tb_w8a16_vector_ops;
  localparam int N = 4;
  logic clk = 0; always #5 clk = ~clk;
  logic rst_n = 0, start = 0;
  logic [3:0] op;
  logic signed [N*16-1:0] x, aux, y;
  logic signed [15:0] scale;
  logic out_valid, done;
  w8a16_vector_ops #(.N(N)) dut(.*);

  task automatic run_op(input logic [3:0] code);
    begin
      @(negedge clk); op = code; start = 1'b1;
      @(posedge clk); #1;
      if (!out_valid || !done) $fatal(1, "vector op handshake failed op=%0d", code);
      @(negedge clk); start = 1'b0;
    end
  endtask

  initial begin
    x = '0; aux = '0; scale = 16'sd16384; op = '0;
    x[0 +: 16] = 16'sd30000; aux[0 +: 16] = 16'sd10000;
    x[16 +: 16] = -16'sd30000; aux[16 +: 16] = -16'sd10000;
    x[32 +: 16] = 16'sd8192; aux[32 +: 16] = 16'sd0;
    x[48 +: 16] = -16'sd8192; aux[48 +: 16] = 16'sd0;
    repeat (2) @(negedge clk); rst_n = 1'b1;
    run_op(4'd0); // BIAS_ADD
    if ($signed(y[0 +: 16]) !== 16'sh7fff || $signed(y[16 +: 16]) !== -16'sh8000) $fatal(1, "bias saturation");
    run_op(4'd2); // MUL_SCALE
    if ($signed(y[32 +: 16]) !== 16'sd4096) $fatal(1, "scale mismatch");
    run_op(4'd3); // RELU
    if ($signed(y[16 +: 16]) !== 0 || $signed(y[0 +: 16]) !== 30000) $fatal(1, "relu mismatch");
    run_op(4'd4); // GELU approximation
    run_op(4'd5); // TANH approximation
    run_op(4'd6); // bounded layer normalization
    run_op(4'd7); // softmax LUT
    if ($unsigned(y[0 +: 16]) < $unsigned(y[32 +: 16])) $fatal(1, "softmax order");
    $display("TB_W8A16_VECTOR_OPS PASS");
    $finish(0);
  end
endmodule
