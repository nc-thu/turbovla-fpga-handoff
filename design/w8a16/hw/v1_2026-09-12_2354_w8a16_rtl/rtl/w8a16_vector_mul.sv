// Element-wise INT16 scale.  The multiplier is Q1.15, so this unit is used
// for gamma/scale terms without allocating another DSP per lane.
`ifndef TVLA_W8A16_VECTOR_MUL_SV
`define TVLA_W8A16_VECTOR_MUL_SV
module w8a16_vector_mul #(parameter int N = 16) (
  input  logic signed [N*16-1:0] x,
  input  logic signed [15:0] scale,
  output logic signed [N*16-1:0] y
);
  integer i;
  integer signed product;
  integer signed value;
  always_comb begin
    y = '0;
    for (i = 0; i < N; i = i + 1) begin
      product = $signed(x[i*16 +: 16]) * $signed(scale);
      value = product >>> 15;
      if (value > 32767) y[i*16 +: 16] = 16'sh7fff;
      else if (value < -32768) y[i*16 +: 16] = -16'sh8000;
      else y[i*16 +: 16] = value[15:0];
    end
  end
endmodule
`endif
