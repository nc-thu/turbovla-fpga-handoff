// Registered layout primitive used by the full-model replay top.
// It performs the address permutation selected by the compiler without
// changing the numerical representation of a lane.
`ifndef TVLA_LAYOUT_UNIT_SV
`define TVLA_LAYOUT_UNIT_SV
module tvla_layout_unit #(
  parameter int LANES = 16,
  parameter int DW = 16,
  parameter int INDEX_W = (LANES <= 2) ? 1 : $clog2(LANES)
) (
  input  logic clk,
  input  logic rst_n,
  input  logic in_valid,
  output logic in_ready,
  input  logic [3:0] mode,
  input  logic [LANES*DW-1:0] in_data,
  input  logic [LANES*INDEX_W-1:0] index_data,
  output logic out_valid,
  input  logic out_ready,
  output logic [LANES*DW-1:0] out_data
);
  localparam logic [3:0] MODE_IDENTITY = 4'h0;
  localparam logic [3:0] MODE_TRANSPOSE = 4'h1;
  localparam logic [3:0] MODE_GATHER = 4'h2;
  localparam logic [3:0] MODE_SCATTER = 4'h3;
  localparam logic [3:0] MODE_SLICE = 4'h4;
  logic busy;
  logic [LANES*DW-1:0] data_r;
  logic [LANES*INDEX_W-1:0] index_r;
  logic [3:0] mode_r;
  integer i;
  integer src_idx;
  assign in_ready = !busy || (out_valid && out_ready);
  assign out_valid = busy;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      busy <= 1'b0;
      mode_r <= MODE_IDENTITY;
      data_r <= '0;
      index_r <= '0;
      out_data <= '0;
    end else begin
      if (busy && out_ready) busy <= 1'b0;
      if (in_valid && in_ready) begin
        mode_r <= mode;
        data_r <= in_data;
        index_r <= index_data;
        for (i = 0; i < LANES; i = i + 1) begin
          src_idx = i;
          if (mode == MODE_TRANSPOSE) src_idx = LANES - 1 - i;
          else if ((mode == MODE_GATHER) || (mode == MODE_SCATTER) ||
                   (mode == MODE_SLICE)) src_idx = index_data[i*INDEX_W +: INDEX_W];
          if (src_idx < 0 || src_idx >= LANES) src_idx = 0;
          out_data[i*DW +: DW] <= in_data[src_idx*DW +: DW];
        end
        busy <= 1'b1;
      end
    end
  end
endmodule
`endif
