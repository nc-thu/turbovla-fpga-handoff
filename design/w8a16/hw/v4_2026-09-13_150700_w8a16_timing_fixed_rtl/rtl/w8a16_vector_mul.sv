// Registered element-wise INT16 scale.  The multiplier is Q1.15, so this unit
// is used for gamma/scale terms without allocating another DSP per lane.  The
// wide product and the shift/saturation are deliberately separated by a
// register.  This keeps the runtime scale register off the long multiply plus
// saturation path in the system top; the extra cycle is part of the ISA
// latency and is accounted for by the runtime handshake.
`ifndef TVLA_W8A16_VECTOR_MUL_SV
`define TVLA_W8A16_VECTOR_MUL_SV
module w8a16_vector_mul #(parameter int N = 16) (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   in_vld,
  input  logic signed [N*16-1:0] x,
  input  logic signed [15:0] scale,
  output logic signed [N*16-1:0] y,
  output logic                   out_vld
);
  integer i;
  integer signed value;
  logic signed [31:0] product_r [0:N-1];
  logic signed [N*16-1:0] y_next;
  logic product_vld_r;
  logic result_vld_r;
  always_comb begin
    y_next = '0;
    for (i = 0; i < N; i = i + 1) begin
      value = $signed(product_r[i]) >>> 15;
      if (value > 32767) y_next[i*16 +: 16] = 16'sh7fff;
      else if (value < -32768) y_next[i*16 +: 16] = -16'sh8000;
      else y_next[i*16 +: 16] = value[15:0];
    end
  end
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      y <= '0;
      out_vld <= 1'b0;
      product_vld_r <= 1'b0;
      result_vld_r <= 1'b0;
      for (i = 0; i < N; i = i + 1) product_r[i] <= '0;
    end else begin
      // Stage 2: register the shifted/saturated result.
      out_vld <= result_vld_r;
      if (result_vld_r) y <= y_next;

      // Stage 1: register the full signed product.  The explicit product
      // register is what breaks the scale -> multiplier -> saturation path.
      result_vld_r <= product_vld_r;
      if (in_vld) begin
        for (i = 0; i < N; i = i + 1)
          product_r[i] <= $signed(x[i*16 +: 16]) * $signed(scale);
      end
      product_vld_r <= in_vld;
    end
  end
endmodule
`endif
