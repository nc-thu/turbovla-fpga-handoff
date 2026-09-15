// Piecewise signed INT16 tanh primitive for the normalized action output.
// The input/output scale is Q1.15.  The four segments use only compares,
// subtracts and shifts.  This is intentionally a hardware approximation: it
// keeps the action range bounded while avoiding a multiplier/divider cone in
// the vector write-back path.
`ifndef TVLA_W8A16_TANH_SV
`define TVLA_W8A16_TANH_SV
module w8a16_tanh #(parameter int N = 16) (
  input  logic signed [N*16-1:0] x,
  output logic signed [N*16-1:0] y
);
  integer i;
  integer ax;
  integer yi;
  always_comb begin
    y = '0;
    for (i = 0; i < N; i = i + 1) begin
      // A variable part-select is unsigned by default; cast it or every
      // negative input would look like a large positive magnitude.
      ax = $signed(x[i*16 +: 16]);
      if (ax < 0) ax = -ax;
      if (ax >= 16'sd24576) yi = 32767;
      else if (ax >= 16'sd16384) yi = 24576 + (ax - 16384);
      else if (ax >= 16'sd8192) yi = 12288 + ((ax - 8192) + ((ax - 8192) >>> 1));
      else yi = ax + (ax >>> 1);
      if (x[i*16 + 15]) yi = -yi;
      if (yi > 32767) y[i*16 +: 16] = 16'sh7fff;
      else if (yi < -32768) y[i*16 +: 16] = -16'sh8000;
      else y[i*16 +: 16] = yi[15:0];
    end
  end
endmodule
`endif
