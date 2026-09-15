// BMM staging and transpose helper.  It keeps both operands in explicit
// buffers so the compiler can reject a layout for which only one operand is
// available.  The replay top uses one row per output beat.
`ifndef TVLA_BMM_LAYOUT_SV
`define TVLA_BMM_LAYOUT_SV
module tvla_bmm_layout #(
  parameter int ROWS = 16,
  parameter int COLS = 48,
  parameter int DW = 16,
  parameter int RW = (ROWS <= 2) ? 1 : $clog2(ROWS),
  parameter int CW = (COLS <= 2) ? 1 : $clog2(COLS)
) (
  input logic clk,
  input logic rst_n,
  input logic start,
  input logic a_valid,
  input logic [ROWS*DW-1:0] a_row,
  input logic [RW-1:0] a_index,
  input logic b_valid,
  input logic [COLS*DW-1:0] b_row,
  input logic [CW-1:0] b_index,
  input logic transpose_b,
  output logic in_ready,
  output logic out_valid,
  input logic out_ready,
  output logic [ROWS*DW-1:0] out_a,
  output logic [COLS*DW-1:0] out_b,
  output logic [RW-1:0] out_index,
  output logic out_last
);
  logic [ROWS*DW-1:0] a_mem [0:ROWS-1];
  logic [COLS*DW-1:0] b_mem [0:COLS-1];
  logic [RW-1:0] emit_idx;
  logic active;
  integer i;
  integer j;
  assign in_ready = !active;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      active <= 1'b0;
      out_valid <= 1'b0;
      out_last <= 1'b0;
      emit_idx <= '0;
      out_a <= '0;
      out_b <= '0;
      out_index <= '0;
      for (i = 0; i < ROWS; i = i + 1) a_mem[i] <= '0;
      for (i = 0; i < COLS; i = i + 1) b_mem[i] <= '0;
    end else begin
      if (a_valid) a_mem[a_index] <= a_row;
      if (b_valid) b_mem[b_index] <= b_row;
      if (start && !active) begin
        active <= 1'b1;
        emit_idx <= '0;
        out_valid <= 1'b0;
      end
      if (active && (!out_valid || out_ready)) begin
        out_a <= a_mem[emit_idx];
        for (j = 0; j < COLS; j = j + 1) begin
          if (transpose_b) out_b[j*DW +: DW] <= b_mem[j][emit_idx*DW +: DW];
          else out_b[j*DW +: DW] <= b_mem[j][j*DW +: DW];
        end
        out_index <= emit_idx;
        out_valid <= 1'b1;
        out_last <= (emit_idx == ROWS-1);
        if (emit_idx == ROWS-1) active <= 1'b0;
        else emit_idx <= emit_idx + 1'b1;
      end
      if (out_valid && out_ready) out_valid <= 1'b0;
    end
  end
endmodule
`endif
