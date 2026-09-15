// LUT-based INT40 to INT16 requantizer.  The use_dsp attribute is intentional:
// the 768-DSP budget belongs to the MAC array, not the output conversion.
`ifndef TVLA_W8A16_REQUANT_SV
`define TVLA_W8A16_REQUANT_SV
module w8a16_requant #(
  parameter int ACC_W = 40
)(
  input  logic                       clk,
  input  logic                       rst_n,
  input  logic                       in_vld,
  input  logic signed [ACC_W-1:0]    x,
  input  logic signed [15:0]         multiplier,
  input  logic [7:0]                 shift,
  output logic                       out_vld,
  output logic signed [15:0]         y
);
  localparam int PW = ACC_W + 16;
  (* use_dsp = "no" *) logic signed [PW-1:0] product;
  logic signed [PW-1:0] shifted;
  logic signed [15:0] y_r;
  logic v_r;
  always_comb begin
    product = x * multiplier;
    if (shift >= PW) shifted = product[PW-1] ? -1 : 0;
    else shifted = product >>> shift;
  end
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      v_r <= 1'b0; y_r <= '0;
    end else begin
      v_r <= in_vld;
      // Invalid cycles do not overwrite the last converted value.  This is
      // important when a downstream writer samples y after a valid bubble.
      if (in_vld) begin
        if (shifted > 32767) y_r <= 16'sh7fff;
        else if (shifted < -32768) y_r <= -16'sh8000;
        else y_r <= shifted[15:0];
      end
    end
  end
  assign out_vld = v_r;
  assign y = y_r;
endmodule
`endif
