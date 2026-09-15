// Embedding and positional-encoding engine.  The table is true writable
// memory; POS/COS/SIN use the deterministic phase helper in the underlying
// primitive and can later be replaced by a vendor FP16/LUT implementation.
`ifndef TVLA_EMBEDDING_ENGINE_SV
`define TVLA_EMBEDDING_ENGINE_SV
module tvla_embedding_engine #(
  parameter int LANES = 16,
  parameter int DW = 16,
  parameter int TABLE_DEPTH = 256
) (
  input logic clk,
  input logic rst_n,
  input logic in_valid,
  output logic in_ready,
  input logic [1:0] mode,
  input logic [15:0] token_index,
  input logic [15:0] position,
  input logic table_wr_en,
  input logic [$clog2(TABLE_DEPTH)-1:0] table_wr_index,
  input logic [LANES*DW-1:0] table_wr_data,
  output logic out_valid,
  input logic out_ready,
  output logic signed [LANES*DW-1:0] out_data
);
  tvla_embedding_posenc #(.LANES(LANES), .DW(DW), .TABLE_DEPTH(TABLE_DEPTH)) u_impl (
    .clk(clk), .rst_n(rst_n), .in_valid(in_valid), .in_ready(in_ready),
    .mode(mode), .token_index(token_index), .position(position),
    .table_wr_en(table_wr_en), .table_wr_index(table_wr_index),
    .table_wr_data(table_wr_data), .out_valid(out_valid), .out_ready(out_ready),
    .out_data(out_data)
  );
endmodule
`endif
