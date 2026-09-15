// Dual-input BMM staging with explicit transpose, causal mask and scale.
// A and B are loaded independently.  Output is held until both operands for
// the selected row exist, so one-sided attention inputs are never counted.
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
  input logic mask_enable,
  input logic signed [DW-1:0] scale,
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
  logic [ROWS-1:0] a_seen;
  logic [COLS-1:0] b_seen;
  logic [RW-1:0] emit_idx;
  logic active;
  logic all_b_seen;
  integer i;
  integer j;

  // Either operand may be loaded before start.  During emission, the caller
  // must wait for in_ready before replacing the staging buffers.
  assign in_ready = !out_valid || out_ready;
  always_comb begin
    all_b_seen = &b_seen;
  end

  function automatic signed [DW-1:0] scale_q88(input signed [DW-1:0] v);
    logic signed [(2*DW)-1:0] p;
    logic signed [(2*DW)-1:0] q;
    begin
      p = v * scale;
      q = p >>> 8;
      if (q > $signed({1'b0, {(DW-1){1'b1}}}))
        scale_q88 = {1'b0, {(DW-1){1'b1}}};
      else if (q < $signed({1'b1, {(DW-1){1'b0}}}))
        scale_q88 = {1'b1, {(DW-1){1'b0}}};
      else scale_q88 = q[DW-1:0];
    end
  endfunction

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      active <= 1'b0;
      out_valid <= 1'b0;
      out_last <= 1'b0;
      emit_idx <= '0;
      out_a <= '0;
      out_b <= '0;
      out_index <= '0;
      a_seen <= '0;
      b_seen <= '0;
      for (i = 0; i < ROWS; i = i + 1) a_mem[i] <= '0;
      for (i = 0; i < COLS; i = i + 1) b_mem[i] <= '0;
    end else begin
      if (a_valid && a_index < ROWS) begin
        a_mem[a_index] <= a_row;
        a_seen[a_index] <= 1'b1;
      end
      if (b_valid && b_index < COLS) begin
        b_mem[b_index] <= b_row;
        b_seen[b_index] <= 1'b1;
      end
      if (start && !active) begin
        active <= 1'b1;
        emit_idx <= '0;
        out_valid <= 1'b0;
        out_last <= 1'b0;
      end else if (active && (!out_valid || out_ready)) begin
        // Hold if a required row has not arrived.  This makes the dependency
        // visible to the scheduler instead of silently inserting zeros.
        if (a_seen[emit_idx] && ((!transpose_b && b_seen[emit_idx]) ||
                                 (transpose_b && all_b_seen))) begin
          for (i = 0; i < ROWS; i = i + 1)
            out_a[i*DW +: DW] <= scale_q88($signed(a_mem[emit_idx][i*DW +: DW]));
          for (j = 0; j < COLS; j = j + 1) begin
            if (mask_enable && (j > emit_idx))
              out_b[j*DW +: DW] <= '0;
            else if (transpose_b)
              out_b[j*DW +: DW] <= b_mem[j][emit_idx*DW +: DW];
            else
              out_b[j*DW +: DW] <= b_mem[emit_idx][j*DW +: DW];
          end
          out_index <= emit_idx;
          out_last <= (emit_idx == ROWS-1);
          out_valid <= 1'b1;
          if (emit_idx == ROWS-1) active <= 1'b0;
          else emit_idx <= emit_idx + 1'b1;
        end
      end else if (out_valid && out_ready) begin
        out_valid <= 1'b0;
      end
    end
  end
endmodule
`endif
