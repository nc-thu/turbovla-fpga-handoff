// Registered element-wise INT16 scale.  The multiplier is Q1.15, so this unit
// is used for gamma/scale terms without allocating another DSP per lane.  A
// registered result keeps the wide multiply and saturation off the vector
// command's start-to-writeback timing path.
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
  integer signed product;
  integer signed value;
  logic signed [N*16-1:0] y_next;
  always_comb begin
    y_next = '0;
    for (i = 0; i < N; i = i + 1) begin
      product = $signed(x[i*16 +: 16]) * $signed(scale);
      value = product >>> 15;
      if (value > 32767) y_next[i*16 +: 16] = 16'sh7fff;
      else if (value < -32768) y_next[i*16 +: 16] = -16'sh8000;
      else y_next[i*16 +: 16] = value[15:0];
    end
  end
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      y <= '0;
      out_vld <= 1'b0;
    end else begin
      out_vld <= in_vld;
      if (in_vld) y <= y_next;
    end
  end
endmodule
`endif
