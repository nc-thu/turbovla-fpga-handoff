`timescale 1ns/1ps
module tb_w8a16_activations;
  localparam int N = 4;
  logic clk = 0; always #5 clk = ~clk;
  logic rst_n = 0;
  logic signed [N*16-1:0] x, y_relu, y_gelu, y_tanh, y_ln;
  logic signed [N*16-1:0] a, b, y_add;
  logic [N*16-1:0] y_sm;
  logic in_vld, ln_vld, sm_vld;
  w8a16_relu #(.N(N)) u_relu(.x(x), .y(y_relu));
  w8a16_gelu #(.N(N)) u_gelu(.x(x), .y(y_gelu));
  w8a16_tanh #(.N(N)) u_tanh(.x(x), .y(y_tanh));
  w8a16_vector_add #(.N(N)) u_add(.a(a), .b(b), .y(y_add));
  w8a16_layernorm #(.N(N)) u_ln(.clk(clk), .rst_n(rst_n), .in_vld(in_vld), .x(x), .out_vld(ln_vld), .y(y_ln));
  w8a16_softmax #(.N(N)) u_sm(.clk(clk), .rst_n(rst_n), .in_vld(in_vld), .x(x), .out_vld(sm_vld), .y(y_sm));
  logic ln_seen, sm_seen;
  integer guard;
  always @(posedge clk) begin
    if (ln_vld) ln_seen = 1'b1;
    if (sm_vld) sm_seen = 1'b1;
  end
  integer signed s0, s1, s2, s3;
  initial begin
    // Explicit lane assignment avoids packed-vector direction ambiguity:
    // lane 0 is the least-significant 16 bits and is the largest input.
    ln_seen = 1'b0; sm_seen = 1'b0;
    x = '0;
    x[16*0 +: 16] = 16'sd8192;
    x[16*1 +: 16] = 16'sd0;
    x[16*2 +: 16] = -16'sd8192;
    x[16*3 +: 16] = -16'sd24576;
    a = '0; b = '0;
    a[16*0 +: 16] = 16'sd30000;  b[16*0 +: 16] = 16'sd10000;
    a[16*1 +: 16] = 16'sd30000;  b[16*1 +: 16] = -16'sd10000;
    a[16*2 +: 16] = -16'sd30000; b[16*2 +: 16] = -16'sd10000;
    a[16*3 +: 16] = -16'sd30000; b[16*3 +: 16] = 16'sd10000;
    #12; rst_n = 1; in_vld = 1;
    #10; in_vld = 0;
    if (y_relu[16*0 +: 16] !== 16'sd8192) $fatal(1, "relu positive failed");
    if (y_relu[16*1 +: 16] !== 16'sd0) $fatal(1, "relu zero failed");
    if (y_relu[16*2 +: 16] !== 16'sd0 || y_relu[16*3 +: 16] !== 16'sd0) $fatal(1, "relu negative failed");
    if (y_add[16*0 +: 16] !== 16'sh7fff) $fatal(1, "add positive saturation failed");
    if (y_add[16*2 +: 16] !== -16'sd32768) $fatal(1, "add negative saturation failed");
    guard = 0;
    // The bit-serial normalizers take a bounded but deliberately long path:
    // N lanes x (15 numerator-build + 32 quotient) cycles.  Keep the smoke
    // test guard above that latency instead of treating a valid late result
    // as a functional failure.
    while (!(ln_seen && sm_seen) && guard < 320) begin
      @(posedge clk); #1; guard = guard + 1;
    end
    if (!(ln_seen && sm_seen)) $fatal(1, "activation valid pipeline failed");
    s0 = y_sm[16*0 +: 16]; s1 = y_sm[16*1 +: 16];
    s2 = y_sm[16*2 +: 16]; s3 = y_sm[16*3 +: 16];
    if (s0 < 0 || s1 < 0 || s2 < 0 || s3 < 0) $fatal(1, "softmax sign failed");
    if (!(s0 >= s1 && s1 >= s2 && s2 >= s3)) $fatal(1, "softmax ordering failed");
    $display("TB_W8A16_ACTIVATIONS PASS relu=%h gelu=%h tanh=%h ln=%h softmax_sum=%0d", y_relu, y_gelu, y_tanh, y_ln, s0+s1+s2+s3);
    $finish;
  end
endmodule
