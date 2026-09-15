// Minimal AXI4 master used by the full-model top.  It issues one-beat
// transactions and keeps the stream-side protocol independent of DDR width.
`ifndef TVLA_DMA_AXI_SV
`define TVLA_DMA_AXI_SV
module tvla_dma_axi #(
  parameter int DW = 128
) (
  input logic clk,
  input logic rst_n,
  input logic start_read,
  input logic start_write,
  input logic [63:0] base_addr,
  input logic [31:0] length_bytes,
  output logic busy,
  output logic done,
  output logic [31:0] read_cycles,
  output logic [31:0] write_cycles,
  output logic m_axi_arvalid,
  input logic m_axi_arready,
  output logic [63:0] m_axi_araddr,
  output logic [7:0] m_axi_arlen,
  output logic m_axi_rready,
  input logic m_axi_rvalid,
  input logic [DW-1:0] m_axi_rdata,
  input logic m_axi_rlast,
  output logic m_axi_awvalid,
  input logic m_axi_awready,
  output logic [63:0] m_axi_awaddr,
  output logic [7:0] m_axi_awlen,
  output logic m_axi_wvalid,
  input logic m_axi_wready,
  output logic [DW-1:0] m_axi_wdata,
  output logic [DW/8-1:0] m_axi_wstrb,
  output logic m_axi_wlast,
  input logic m_axi_bvalid,
  output logic m_axi_bready,
  output logic stream_out_valid,
  input logic stream_out_ready,
  output logic [DW-1:0] stream_out_data,
  input logic stream_in_valid,
  output logic stream_in_ready,
  input logic [DW-1:0] stream_in_data
);
  typedef enum logic [2:0] {S_IDLE, S_AR, S_R, S_AW, S_W, S_B} state_t;
  state_t state;
  logic [63:0] addr_r;
  logic [31:0] remaining_r;
  logic read_mode;
  assign busy = (state != S_IDLE);
  assign m_axi_arvalid = (state == S_AR);
  assign m_axi_araddr = addr_r;
  assign m_axi_arlen = 8'd0;
  assign m_axi_rready = (state == S_R) && (!stream_out_valid || stream_out_ready);
  assign m_axi_awvalid = (state == S_AW);
  assign m_axi_awaddr = addr_r;
  assign m_axi_awlen = 8'd0;
  assign m_axi_wvalid = (state == S_W) && stream_in_valid;
  assign m_axi_wdata = stream_in_data;
  assign m_axi_wstrb = {(DW/8){1'b1}};
  assign m_axi_wlast = 1'b1;
  assign m_axi_bready = (state == S_B);
  assign stream_in_ready = (state == S_W) && m_axi_wready;
  assign done = (state == S_IDLE) && (read_cycles != 0 || write_cycles != 0);
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= S_IDLE; addr_r <= '0; remaining_r <= '0; read_mode <= 1'b0;
      read_cycles <= '0; write_cycles <= '0;
      stream_out_valid <= 1'b0; stream_out_data <= '0;
    end else begin
      if (state != S_IDLE) begin
        if (read_mode) read_cycles <= read_cycles + 1'b1;
        else write_cycles <= write_cycles + 1'b1;
      end
      if (stream_out_valid && stream_out_ready) stream_out_valid <= 1'b0;
      case (state)
        S_IDLE: begin
          if (start_read && length_bytes != 0) begin
            addr_r <= base_addr; remaining_r <= length_bytes; read_mode <= 1'b1; state <= S_AR;
          end else if (start_write && length_bytes != 0) begin
            addr_r <= base_addr; remaining_r <= length_bytes; read_mode <= 1'b0; state <= S_AW;
          end
        end
        S_AR: if (m_axi_arready) state <= S_R;
        S_R: if (m_axi_rvalid && (!stream_out_valid || stream_out_ready)) begin
          stream_out_data <= m_axi_rdata; stream_out_valid <= 1'b1;
          addr_r <= addr_r + (DW/8); remaining_r <= (remaining_r > (DW/8)) ? remaining_r - (DW/8) : 0;
          if (m_axi_rlast || remaining_r <= (DW/8)) state <= S_IDLE; else state <= S_AR;
        end
        S_AW: if (m_axi_awready) state <= S_W;
        S_W: if (stream_in_valid && m_axi_wready) begin
          addr_r <= addr_r + (DW/8); remaining_r <= (remaining_r > (DW/8)) ? remaining_r - (DW/8) : 0;
          if (remaining_r <= (DW/8)) state <= S_B; else state <= S_AW;
        end
        S_B: if (m_axi_bvalid) state <= S_IDLE;
        default: state <= S_IDLE;
      endcase
    end
  end
endmodule
`endif
