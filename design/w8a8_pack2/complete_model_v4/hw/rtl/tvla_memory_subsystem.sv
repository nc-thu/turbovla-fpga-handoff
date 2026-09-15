// CTX/WRAM plus a real AXI4 one-beat transaction controller.  The replay top
// uses the same ports for activity replay; this module makes the storage and
// external-memory boundary explicit for integration and timing analysis.
`ifndef TVLA_MEMORY_SUBSYSTEM_SV
`define TVLA_MEMORY_SUBSYSTEM_SV
module tvla_memory_subsystem #(
  parameter int CTX_DEPTH = 1024,
  parameter int WRAM_DEPTH = 1024,
  parameter int AXI_DW = 128
) (
  input logic clk,
  input logic rst_n,
  input logic ctx_wr_en,
  input logic [9:0] ctx_wr_addr,
  input logic [127:0] ctx_wr_data,
  input logic [9:0] ctx_rd_addr,
  output logic [127:0] ctx_rd_data,
  input logic wram_wr_en,
  input logic [9:0] wram_wr_addr,
  input logic [767:0] wram_wr_data,
  input logic [9:0] wram_rd_addr,
  output logic [767:0] wram_rd_data,
  input logic dma_read_start,
  input logic dma_write_start,
  input logic [63:0] dma_base_addr,
  input logic [31:0] dma_length_bytes,
  output logic dma_busy,
  output logic dma_done,
  output logic [63:0] m_axi_araddr,
  output logic m_axi_arvalid,
  input logic m_axi_arready,
  input logic m_axi_rvalid,
  input logic [AXI_DW-1:0] m_axi_rdata,
  input logic m_axi_rlast,
  output logic m_axi_rready,
  output logic [63:0] m_axi_awaddr,
  output logic m_axi_awvalid,
  input logic m_axi_awready,
  output logic m_axi_wvalid,
  input logic m_axi_wready,
  output logic [AXI_DW-1:0] m_axi_wdata,
  output logic m_axi_wlast,
  input logic m_axi_bvalid,
  output logic m_axi_bready,
  input logic scale_wr_en,
  input logic [11:0] scale_wr_index,
  input logic [15:0] scale_wr_a,
  input logic [15:0] scale_wr_w,
  input logic [15:0] scale_wr_out,
  input logic signed [31:0] scale_wr_bias,
  input logic [11:0] scale_rd_index,
  output logic [15:0] scale_rd_a,
  output logic [15:0] scale_rd_w,
  output logic [15:0] scale_rd_out,
  output logic signed [31:0] scale_rd_bias,
  output logic [31:0] scale_table_version
);
  logic [127:0] ctx_rdata_i;
  logic [767:0] wram_rdata_i;
  logic stream_out_valid, stream_out_ready;
  logic [AXI_DW-1:0] stream_out_data;
  logic stream_in_ready;
  logic [31:0] read_cycles_unused, write_cycles_unused;
  logic [7:0] arlen_unused, awlen_unused;
  logic [AXI_DW/8-1:0] wstrb_unused;
  logic [AXI_DW-1:0] stream_in_zero;
  assign stream_in_zero = '0;
  tvla_ctx_wram #(.CTX_DEPTH(CTX_DEPTH), .WRAM_DEPTH(WRAM_DEPTH)) u_buffers (
    .clk(clk), .rst_n(rst_n), .ctx_wr_en(ctx_wr_en), .ctx_wr_addr(ctx_wr_addr),
    .ctx_wr_data(ctx_wr_data), .ctx_rd_en(1'b1), .ctx_rd_addr(ctx_rd_addr),
    .ctx_rd_data(ctx_rdata_i), .wram_wr_en(wram_wr_en), .wram_wr_addr(wram_wr_addr),
    .wram_wr_data(wram_wr_data), .wram_rd_en(1'b1), .wram_rd_addr(wram_rd_addr),
    .wram_rd_data(wram_rdata_i)
  );
  assign ctx_rd_data = ctx_rdata_i;
  assign wram_rd_data = wram_rdata_i;
  tvla_scale_bias_table u_scale_bias_table (
    .clk(clk), .rst_n(rst_n), .wr_valid(scale_wr_en),
    .wr_index(scale_wr_index), .wr_a_scale(scale_wr_a), .wr_w_scale(scale_wr_w),
    .wr_out_scale(scale_wr_out), .wr_bias(scale_wr_bias),
    .rd_index(scale_rd_index), .rd_a_scale(scale_rd_a), .rd_w_scale(scale_rd_w),
    .rd_out_scale(scale_rd_out), .rd_bias(scale_rd_bias),
    .version(scale_table_version)
  );
  tvla_dma_axi #(.DW(AXI_DW)) u_dma (
    .clk(clk), .rst_n(rst_n), .start_read(dma_read_start),
    .start_write(dma_write_start), .base_addr(dma_base_addr),
    .length_bytes(dma_length_bytes), .busy(dma_busy), .done(dma_done),
    .read_cycles(read_cycles_unused), .write_cycles(write_cycles_unused),
    .m_axi_arvalid(m_axi_arvalid), .m_axi_arready(m_axi_arready),
    .m_axi_araddr(m_axi_araddr), .m_axi_arlen(arlen_unused),
    .m_axi_rready(m_axi_rready), .m_axi_rvalid(m_axi_rvalid),
    .m_axi_rdata(m_axi_rdata), .m_axi_rlast(m_axi_rlast),
    .m_axi_awvalid(m_axi_awvalid), .m_axi_awready(m_axi_awready),
    .m_axi_awaddr(m_axi_awaddr), .m_axi_awlen(awlen_unused),
    .m_axi_wvalid(m_axi_wvalid), .m_axi_wready(m_axi_wready),
    .m_axi_wdata(m_axi_wdata), .m_axi_wstrb(wstrb_unused),
    .m_axi_wlast(m_axi_wlast), .m_axi_bvalid(m_axi_bvalid),
    .m_axi_bready(m_axi_bready), .stream_out_valid(stream_out_valid),
    .stream_out_ready(stream_out_ready), .stream_out_data(stream_out_data),
    .stream_in_valid(1'b0), .stream_in_ready(stream_in_ready), .stream_in_data(stream_in_zero)
  );
  assign stream_out_ready = 1'b1;
endmodule
`endif
