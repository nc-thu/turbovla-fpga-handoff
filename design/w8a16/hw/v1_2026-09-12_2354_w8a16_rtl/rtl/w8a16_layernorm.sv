// Resource-conscious integer normalization primitive.
// It subtracts the vector mean and scales by the largest absolute deviation.
// This bounded form is used for the first RTL path; learned gamma/beta remain
// explicit ports and can be applied by w8a16_vector_add/w8a16_mul.
`ifndef TVLA_W8A16_LAYERNORM_SV
`define TVLA_W8A16_LAYERNORM_SV
module w8a16_layernorm #(parameter int N = 16) (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   in_vld,
  input  logic signed [N*16-1:0] x,
  output logic                   out_vld,
  output logic signed [N*16-1:0] y
);
  integer i;
  integer signed total;
  integer signed mean;
  integer signed delta;
  integer signed max_abs;
  integer signed scaled;
  always_comb begin
    total = 0;
    for (i = 0; i < N; i = i + 1) total = total + $signed(x[i*16 +: 16]);
    mean = total / N;
    max_abs = 1;
    for (i = 0; i < N; i = i + 1) begin
      delta = $signed(x[i*16 +: 16]) - mean;
      if (delta < 0) begin
        if (-delta > max_abs) max_abs = -delta;
      end else if (delta > max_abs) max_abs = delta;
    end
    y = '0;
    for (i = 0; i < N; i = i + 1) begin
      delta = $signed(x[i*16 +: 16]) - mean;
      scaled = (delta * 32767) / max_abs;
      if (scaled > 32767) y[i*16 +: 16] = 16'sh7fff;
      else if (scaled < -32768) y[i*16 +: 16] = -16'sh8000;
      else y[i*16 +: 16] = scaled[15:0];
    end
  end
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) out_vld <= 1'b0;
    else out_vld <= in_vld;
  end
endmodule
`endif
