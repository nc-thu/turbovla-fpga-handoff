// Elementwise signed INT16 ReLU.  The operation is combinational so the
// controller can place a register wherever the selected schedule needs it.
`ifndef TVLA_W8A16_RELU_SV
`define TVLA_W8A16_RELU_SV
module w8a16_relu #(parameter int N = 16) (
  input  logic signed [N*16-1:0] x,
  output logic signed [N*16-1:0] y
);
  integer i;
  always_comb begin
    y = '0;
    for (i = 0; i < N; i = i + 1)
      y[i*16 +: 16] = x[i*16 + 15] ? 16'sd0 : x[i*16 +: 16];
  end
endmodule
`endif
