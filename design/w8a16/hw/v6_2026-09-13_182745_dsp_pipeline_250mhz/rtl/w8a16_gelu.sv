// Small fixed-point GELU approximation for the activation instruction.
// Inputs and outputs use signed INT16 with the same tensor scale.  The
// approximation is intentionally piecewise and deterministic; calibrated
// software may replace the breakpoints without changing the ISA.
`ifndef TVLA_W8A16_GELU_SV
`define TVLA_W8A16_GELU_SV
module w8a16_gelu #(parameter int N = 16) (
  input  logic signed [N*16-1:0] x,
  output logic signed [N*16-1:0] y
);
  integer i;
  logic signed [15:0] xi;
  logic signed [31:0] yi;
  always_comb begin
    y = '0;
    for (i = 0; i < N; i = i + 1) begin
      xi = $signed(x[i*16 +: 16]);
      // x/8 for the negative tail, x/2 near zero, and x for the positive
      // region.  This is a hardware primitive, not an FP32 exact GELU.
      if (xi < -16'sd16384) yi = xi >>> 3;
      else if (xi < 0) yi = xi >>> 1;
      else yi = xi;
      if (yi > 32767) y[i*16 +: 16] = 16'sh7fff;
      else if (yi < -32768) y[i*16 +: 16] = -16'sh8000;
      else y[i*16 +: 16] = yi[15:0];
    end
  end
endmodule
`endif
