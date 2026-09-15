// Explicit CTX activation and WRAM weight buffers.
`ifndef TVLA_CTX_WRAM_SV
`define TVLA_CTX_WRAM_SV
module tvla_ctx_wram #(
  parameter int CTX_DEPTH = 1024,
  parameter int WRAM_DEPTH = 1024,
  parameter int ADDR_W = (CTX_DEPTH <= 2) ? 1 : $clog2(CTX_DEPTH),
  parameter int WADDR_W = (WRAM_DEPTH <= 2) ? 1 : $clog2(WRAM_DEPTH)
) (
  input logic clk,
  input logic rst_n,
  input logic ctx_wr_en,
  input logic [ADDR_W-1:0] ctx_wr_addr,
  input logic [127:0] ctx_wr_data,
  input logic ctx_rd_en,
  input logic [ADDR_W-1:0] ctx_rd_addr,
  output logic [127:0] ctx_rd_data,
  input logic wram_wr_en,
  input logic [WADDR_W-1:0] wram_wr_addr,
  input logic [767:0] wram_wr_data,
  input logic wram_rd_en,
  input logic [WADDR_W-1:0] wram_rd_addr,
  output logic [767:0] wram_rd_data
);
  (* ram_style = "block" *) logic [127:0] ctx_mem [0:CTX_DEPTH-1];
  (* ram_style = "block" *) logic [767:0] wram_mem [0:WRAM_DEPTH-1];
  // Keep reset away from the RAM array so Vivado can infer BRAM.  Only the
  // registered read outputs are reset, so a smoke test never propagates an X
  // before software has loaded the first word.
  always_ff @(posedge clk) begin
    if (!rst_n) begin
      ctx_rd_data <= '0;
      wram_rd_data <= '0;
    end else begin
      if (ctx_wr_en) ctx_mem[ctx_wr_addr] <= ctx_wr_data;
      if (ctx_rd_en) ctx_rd_data <= ctx_mem[ctx_rd_addr];
      if (wram_wr_en) wram_mem[wram_wr_addr] <= wram_wr_data;
      if (wram_rd_en) wram_rd_data <= wram_mem[wram_rd_addr];
    end
  end
endmodule
`endif
