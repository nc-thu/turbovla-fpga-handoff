// Integer softmax primitive.  Differences are mapped through a small exp LUT
// and normalized to unsigned Q1.15 probabilities.  A max-subtract step keeps
// the sum bounded; the LUT is a replaceable calibration point.
`ifndef TVLA_W8A16_SOFTMAX_SV
`define TVLA_W8A16_SOFTMAX_SV
module w8a16_softmax #(parameter int N = 16) (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   in_vld,
  input  logic signed [N*16-1:0] x,
  output logic                   out_vld,
  output logic        [N*16-1:0] y
);
  integer i;
  integer signed max_v;
  integer signed d;
  integer unsigned e;
  integer unsigned sum_e;
  integer unsigned lut_e;
  integer unsigned norm_v;
  always_comb begin
    max_v = -2147483647;
    for (i = 0; i < N; i = i + 1)
      if ($signed(x[i*16 +: 16]) > max_v) max_v = $signed(x[i*16 +: 16]);
    sum_e = 0;
    for (i = 0; i < N; i = i + 1) begin
      d = max_v - $signed(x[i*16 +: 16]);
      case (d >>> 12)
        0: lut_e = 32767; 1: lut_e = 25500; 2: lut_e = 19800; 3: lut_e = 15400;
        4: lut_e = 12000; 5: lut_e = 9300; 6: lut_e = 7200; 7: lut_e = 5600;
        8: lut_e = 4300; 9: lut_e = 3300; 10: lut_e = 2500; 11: lut_e = 1900;
        12: lut_e = 1400; 13: lut_e = 1000; 14: lut_e = 700; default: lut_e = 400;
      endcase
      sum_e = sum_e + lut_e;
    end
    if (sum_e == 0) sum_e = 1;
    y = '0;
    for (i = 0; i < N; i = i + 1) begin
      d = max_v - $signed(x[i*16 +: 16]);
      case (d >>> 12)
        0: lut_e = 32767; 1: lut_e = 25500; 2: lut_e = 19800; 3: lut_e = 15400;
        4: lut_e = 12000; 5: lut_e = 9300; 6: lut_e = 7200; 7: lut_e = 5600;
        8: lut_e = 4300; 9: lut_e = 3300; 10: lut_e = 2500; 11: lut_e = 1900;
        12: lut_e = 1400; 13: lut_e = 1000; 14: lut_e = 700; default: lut_e = 400;
      endcase
      norm_v = (lut_e * 32767) / sum_e;
      if (norm_v > 32767) norm_v = 32767;
      y[i*16 +: 16] = norm_v[15:0];
    end
  end
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) out_vld <= 1'b0;
    else out_vld <= in_vld;
  end
endmodule
`endif
