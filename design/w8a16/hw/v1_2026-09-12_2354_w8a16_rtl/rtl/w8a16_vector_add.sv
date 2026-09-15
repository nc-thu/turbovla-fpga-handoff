// Saturating elementwise INT16 add used by residual and bias events.
`ifndef TVLA_W8A16_VECTOR_ADD_SV
`define TVLA_W8A16_VECTOR_ADD_SV
module w8a16_vector_add #(parameter int N = 16) (
  input  logic signed [N*16-1:0] a,
  input  logic signed [N*16-1:0] b,
  output logic signed [N*16-1:0] y
);
  integer i;
  logic signed [16:0] sum;
  always_comb begin
    y = '0;
    for (i = 0; i < N; i = i + 1) begin
      sum = $signed(a[i*16 +: 16]) + $signed(b[i*16 +: 16]);
      if (sum > 17'sd32767) y[i*16 +: 16] = 16'sh7fff;
      else if (sum < -17'sd32768) y[i*16 +: 16] = -16'sh8000;
      else y[i*16 +: 16] = sum[15:0];
    end
  end
endmodule
`endif
