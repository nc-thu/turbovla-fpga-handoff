// Descriptor-driven DMA read payload router.
//
// A DMA_READ response is a stream of 128-bit beats.  This block turns those
// beats into real writes to CTX (one beat per row) or WRAM (six beats per
// 768-bit weight row).  The previous package bridge returned every read beat
// to the host; this router is the missing memory-side step for model replay.
`ifndef TVLA_DMA_CTX_WRAM_LOADER_SV
`define TVLA_DMA_CTX_WRAM_LOADER_SV
module tvla_dma_ctx_wram_loader #(
  parameter int ADDR_W = 10
) (
  input  logic clk,
  input  logic rst_n,
  input  logic start,
  input  logic [1:0] target,       // 0=CTX, 1=WRAM, 2=host (not accepted)
  input  logic [ADDR_W-1:0] base_addr,
  input  logic [31:0] length_bytes,
  output logic busy,
  output logic done,
  input  logic stream_valid,
  output logic stream_ready,
  input  logic [127:0] stream_data,
  output logic ctx_wr_en,
  output logic [ADDR_W-1:0] ctx_wr_addr,
  output logic [127:0] ctx_wr_data,
  output logic wram_wr_en,
  output logic [ADDR_W-1:0] wram_wr_addr,
  output logic [767:0] wram_wr_data,
  output logic [31:0] words_written
);
  logic [1:0] target_r;
  logic [ADDR_W-1:0] base_r;
  logic [31:0] remaining_r;
  logic [ADDR_W-1:0] row_r;
  logic [2:0] wram_beat_r;
  logic [767:0] wram_accum_r;

  wire start_words_zero = (length_bytes == 0);
  wire [31:0] start_words = (length_bytes + 32'd15) >> 4;
  wire fire = busy && stream_valid && stream_ready;
  wire last_word = (remaining_r <= 1);
  wire wram_flush = (target_r == 2'd1) && ((wram_beat_r == 3'd5) || last_word);
  wire route_ok = (target_r == 2'd0) || (target_r == 2'd1);

  assign stream_ready = busy && route_ok;
  assign ctx_wr_en = fire && (target_r == 2'd0);
  assign ctx_wr_addr = base_r + row_r;
  assign ctx_wr_data = stream_data;
  assign wram_wr_en = fire && wram_flush;
  assign wram_wr_addr = base_r + row_r;
  // The first beat occupies the low 128 bits.  The final OR includes the
  // current stream beat, which is still outside the sequential accumulator.
  assign wram_wr_data = wram_accum_r |
                        ({{640{1'b0}}, stream_data} << (wram_beat_r * 128));

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      busy <= 1'b0;
      done <= 1'b0;
      target_r <= 2'd2;
      base_r <= '0;
      remaining_r <= '0;
      row_r <= '0;
      wram_beat_r <= '0;
      wram_accum_r <= '0;
      words_written <= '0;
    end else begin
      done <= 1'b0;
      if (start && !busy) begin
        target_r <= target;
        base_r <= base_addr;
        remaining_r <= start_words;
        row_r <= '0;
        wram_beat_r <= '0;
        wram_accum_r <= '0;
        words_written <= '0;
        if (!start_words_zero && ((target == 2'd0) || (target == 2'd1)))
          busy <= 1'b1;
        else begin
          busy <= 1'b0;
          done <= 1'b1;
        end
      end
      if (fire) begin
        words_written <= words_written + 1'b1;
        if (target_r == 2'd0) begin
          row_r <= row_r + 1'b1;
        end else begin
          if (wram_flush) begin
            row_r <= row_r + 1'b1;
            wram_beat_r <= '0;
            wram_accum_r <= '0;
          end else begin
            wram_beat_r <= wram_beat_r + 1'b1;
            wram_accum_r <= wram_accum_r |
              ({{640{1'b0}}, stream_data} << (wram_beat_r * 128));
          end
        end
        if (last_word) begin
          remaining_r <= '0;
          busy <= 1'b0;
          done <= 1'b1;
        end else begin
          remaining_r <= remaining_r - 1'b1;
        end
      end
    end
  end
endmodule
`endif
