// Small streaming im2col window.  Larger kernels can be tiled by repeating
// the same primitive; the line-buffer protocol stays unchanged.
`ifndef TVLA_CONV_IM2COL_SV
`define TVLA_CONV_IM2COL_SV
module tvla_conv_im2col #(
  parameter int DW = 16,
  parameter int WINDOW = 9,
  parameter int COUNT_W = (WINDOW <= 2) ? 1 : $clog2(WINDOW)
) (
  input logic clk,
  input logic rst_n,
  input logic start,
  input logic in_valid,
  output logic in_ready,
  input logic signed [DW-1:0] in_data,
  output logic out_valid,
  input logic out_ready,
  output logic signed [WINDOW*DW-1:0] out_data,
  output logic out_last
);
  logic signed [DW-1:0] shift_reg [0:WINDOW-1];
  logic [COUNT_W-1:0] count;
  logic active;
  integer i;
  assign in_ready = active && (!out_valid || out_ready);
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      active <= 1'b0;
      out_valid <= 1'b0;
      out_last <= 1'b0;
      count <= '0;
      out_data <= '0;
      for (i = 0; i < WINDOW; i = i + 1) shift_reg[i] <= '0;
    end else begin
      if (start) begin
        active <= 1'b1;
        count <= '0;
        out_valid <= 1'b0;
        out_last <= 1'b0;
      end
      if (out_valid && out_ready) begin
        out_valid <= 1'b0;
        out_last <= 1'b0;
      end
      if (in_valid && in_ready) begin
        for (i = 0; i < WINDOW-1; i = i + 1) shift_reg[i] <= shift_reg[i+1];
        shift_reg[WINDOW-1] <= in_data;
        if (count == WINDOW-1) begin
          for (i = 0; i < WINDOW; i = i + 1) begin
            if (i == WINDOW-1) out_data[i*DW +: DW] <= in_data;
            else out_data[i*DW +: DW] <= shift_reg[i+1];
          end
          out_valid <= 1'b1;
          out_last <= 1'b1;
          count <= '0;
        end else count <= count + 1'b1;
      end
    end
  end
endmodule
`endif
