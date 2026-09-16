// Token embedding, positional encoding and deterministic sin/cos helper.
// The table is a true writable on-chip memory; a deployment can preload it
// through the table write port or replace the functions with an FP16 IP.
`ifndef TVLA_EMBEDDING_POSENC_SV
`define TVLA_EMBEDDING_POSENC_SV
module tvla_embedding_posenc #(
  parameter int LANES = 16,
  parameter int DW = 16,
  parameter int TABLE_DEPTH = 256
) (
  input  logic clk,
  input  logic rst_n,
  input  logic in_valid,
  output logic in_ready,
  input  logic [1:0] mode,
  input  logic [15:0] token_index,
  input  logic [15:0] position,
  input  logic table_wr_en,
  input  logic [$clog2(TABLE_DEPTH)-1:0] table_wr_index,
  input  logic [LANES*DW-1:0] table_wr_data,
  output logic out_valid,
  input  logic out_ready,
  output logic signed [LANES*DW-1:0] out_data
);
  localparam logic [1:0] MODE_EMBED = 2'd0;
  localparam logic [1:0] MODE_POS = 2'd1;
  localparam logic [1:0] MODE_COS = 2'd2;
  localparam logic [1:0] MODE_SIN = 2'd3;
  (* ram_style = "block" *) logic signed [LANES*DW-1:0] table_mem [0:TABLE_DEPTH-1];
  logic busy;
  integer i;
  integer signed phase;
  integer signed sample;
  function automatic integer signed wave(input integer signed p, input logic cosine);
    integer signed q;
    begin
      // A bounded triangular approximation is cheap, deterministic and keeps
      // the interface identical when a vendor FP16 implementation is used.
      q = p % 32768;
      if (q < 0) q = q + 32768;
      if (cosine) begin
        if (q < 8192) wave = 32767 - (q*2);
        else if (q < 24576) wave = -32767 + ((q-8192)*2);
        else wave = 32767 - ((q-24576)*2);
      end else begin
        if (q < 16384) wave = -32768 + (q*4);
        else wave = 32767 - ((q-16384)*4);
      end
    end
  endfunction
  assign in_ready = !busy || (out_valid && out_ready);
  assign out_valid = busy;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      busy <= 1'b0;
      out_data <= '0;
      for (i = 0; i < TABLE_DEPTH; i = i + 1) table_mem[i] <= '0;
    end else begin
      if (table_wr_en) table_mem[table_wr_index] <= table_wr_data;
      if (busy && out_ready) busy <= 1'b0;
      if (in_valid && in_ready) begin
        for (i = 0; i < LANES; i = i + 1) begin
          phase = $signed(position) + i*257;
          if (mode == MODE_EMBED)
            out_data[i*DW +: DW] <= table_mem[token_index % TABLE_DEPTH][i*DW +: DW];
          else if (mode == MODE_POS)
            out_data[i*DW +: DW] <= wave(phase, 1'b0);
          else if (mode == MODE_COS)
            out_data[i*DW +: DW] <= wave(phase, 1'b1);
          else
            out_data[i*DW +: DW] <= wave(phase, 1'b0);
        end
        busy <= 1'b1;
      end
    end
  end
endmodule
`endif
