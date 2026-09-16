// AXI4 master for the TurboVLA memory path.
//
// v6 used one AXI beat per address handshake and hard-wired the write stream
// to zero in the memory wrapper.  That was enough to keep the ports visible,
// but it did not represent a usable DDR path: a write could wait forever for
// data and a long transfer paid one address phase per 128-bit word.  This
// version keeps the same stream-side interface and adds bounded bursts,
// byte strobes for the final beat, and a one-cycle done pulse.
`ifndef TVLA_DMA_AXI_SV
`define TVLA_DMA_AXI_SV
module tvla_dma_axi #(
  parameter int DW = 128,
  parameter int MAX_BURST_BEATS = 16,
  parameter int BEAT_BYTES = DW / 8
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
  localparam int BW = (MAX_BURST_BEATS <= 2) ? 1 : $clog2(MAX_BURST_BEATS + 1);

  typedef enum logic [3:0] {S_IDLE, S_AR, S_R, S_R_DRAIN,
                            S_AW, S_W, S_B} state_t;
  state_t state;
  logic [63:0] addr_r;
  logic [31:0] remaining_r;
  logic [BW-1:0] burst_beats_r;
  logic [BW-1:0] burst_left_r;
  logic read_mode_r;
  logic done_r;

  function automatic [BW-1:0] burst_for(
      input logic [63:0] addr, input logic [31:0] bytes);
    integer by_len;
    integer by_4k;
    integer by_limit;
    begin
      if (bytes == 0) begin
        burst_for = '0;
      end else begin
        by_len = (bytes + BEAT_BYTES - 1) / BEAT_BYTES;
        by_4k = (4096 - addr[11:0]) / BEAT_BYTES;
        if (by_4k < 1) by_4k = 1;
        by_limit = by_len;
        if (by_limit > MAX_BURST_BEATS) by_limit = MAX_BURST_BEATS;
        if (by_limit > by_4k) by_limit = by_4k;
        if (by_limit < 1) by_limit = 1;
        burst_for = by_limit[BW-1:0];
      end
    end
  endfunction

  function automatic [DW/8-1:0] final_strobe(input logic [31:0] bytes);
    integer valid_bytes;
    integer k;
    begin
      valid_bytes = (bytes < BEAT_BYTES) ? bytes : BEAT_BYTES;
      final_strobe = '0;
      for (k = 0; k < DW/8; k = k + 1)
        if (k < valid_bytes) final_strobe[k] = 1'b1;
    end
  endfunction

  assign busy = (state != S_IDLE);
  assign done = done_r;
  assign m_axi_arvalid = (state == S_AR);
  assign m_axi_araddr = addr_r;
  assign m_axi_arlen = (burst_beats_r == 0) ? 8'd0 : burst_beats_r - 1'b1;
  assign m_axi_rready = (state == S_R) &&
                        (!stream_out_valid || stream_out_ready);
  assign m_axi_awvalid = (state == S_AW);
  assign m_axi_awaddr = addr_r;
  assign m_axi_awlen = (burst_beats_r == 0) ? 8'd0 : burst_beats_r - 1'b1;
  assign m_axi_wvalid = (state == S_W) && stream_in_valid;
  assign m_axi_wdata = stream_in_data;
  assign m_axi_wstrb = (remaining_r < BEAT_BYTES) ?
                       final_strobe(remaining_r) : {(DW/8){1'b1}};
  assign m_axi_wlast = (state == S_W) && (burst_left_r == 1);
  assign m_axi_bready = (state == S_B);
  assign stream_in_ready = (state == S_W) && m_axi_wready;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= S_IDLE;
      addr_r <= '0;
      remaining_r <= '0;
      burst_beats_r <= '0;
      burst_left_r <= '0;
      read_mode_r <= 1'b0;
      done_r <= 1'b0;
      read_cycles <= '0;
      write_cycles <= '0;
      stream_out_valid <= 1'b0;
      stream_out_data <= '0;
    end else begin
      done_r <= 1'b0;
      if (stream_out_valid && stream_out_ready)
        stream_out_valid <= 1'b0;
      if (state != S_IDLE) begin
        if (read_mode_r) read_cycles <= read_cycles + 1'b1;
        else write_cycles <= write_cycles + 1'b1;
      end
      case (state)
        S_IDLE: begin
          if (start_read && (length_bytes != 0)) begin
            addr_r <= base_addr;
            remaining_r <= length_bytes;
            burst_beats_r <= burst_for(base_addr, length_bytes);
            burst_left_r <= burst_for(base_addr, length_bytes);
            read_mode_r <= 1'b1;
            read_cycles <= '0;
            state <= S_AR;
          end else if (start_write && (length_bytes != 0)) begin
            addr_r <= base_addr;
            remaining_r <= length_bytes;
            burst_beats_r <= burst_for(base_addr, length_bytes);
            burst_left_r <= burst_for(base_addr, length_bytes);
            read_mode_r <= 1'b0;
            write_cycles <= '0;
            state <= S_AW;
          end
        end
        S_AR: begin
          if (m_axi_arready) state <= S_R;
        end
        S_R: begin
          if (m_axi_rvalid && m_axi_rready) begin
            stream_out_data <= m_axi_rdata;
            stream_out_valid <= 1'b1;
            addr_r <= addr_r + BEAT_BYTES;
            remaining_r <= (remaining_r > BEAT_BYTES) ?
                           remaining_r - BEAT_BYTES : 0;
            if (m_axi_rlast || (burst_left_r == 1)) begin
              if (remaining_r > BEAT_BYTES) begin
                burst_beats_r <= burst_for(addr_r + BEAT_BYTES,
                                           remaining_r - BEAT_BYTES);
                burst_left_r <= burst_for(addr_r + BEAT_BYTES,
                                          remaining_r - BEAT_BYTES);
                state <= S_AR;
              end else begin
                state <= S_R_DRAIN;
              end
            end else begin
              burst_left_r <= burst_left_r - 1'b1;
            end
          end
        end
        S_R_DRAIN: begin
          if (!stream_out_valid || stream_out_ready) begin
            done_r <= 1'b1;
            state <= S_IDLE;
          end
        end
        S_AW: begin
          if (m_axi_awready) state <= S_W;
        end
        S_W: begin
          if (stream_in_valid && m_axi_wready) begin
            addr_r <= addr_r + BEAT_BYTES;
            remaining_r <= (remaining_r > BEAT_BYTES) ?
                           remaining_r - BEAT_BYTES : 0;
            if (burst_left_r == 1) state <= S_B;
            else burst_left_r <= burst_left_r - 1'b1;
          end
        end
        S_B: begin
          if (m_axi_bvalid) begin
            if (remaining_r != 0) begin
              burst_beats_r <= burst_for(addr_r, remaining_r);
              burst_left_r <= burst_for(addr_r, remaining_r);
              state <= S_AW;
            end else begin
              done_r <= 1'b1;
              state <= S_IDLE;
            end
          end
        end
        default: state <= S_IDLE;
      endcase
    end
  end
endmodule
`endif
