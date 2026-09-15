// 512-bit descriptor sideband receiver.
//
// The command word remains 64 bits.  This FIFO receives eight 64-bit beats
// before a command is allowed to enter the replay core.  Keeping addresses,
// shapes, strides and scale IDs out of the command word prevents silent
// truncation when a full TurboVLA trace is compiled.
`ifndef TVLA_DESCRIPTOR_SIDEBAND_FIFO_SV
`define TVLA_DESCRIPTOR_SIDEBAND_FIFO_SV
module tvla_descriptor_sideband_fifo #(
  parameter int BUS_W = 512,
  parameter int BEAT_W = 64,
  parameter int BEATS = BUS_W / BEAT_W
) (
  input  logic clk,
  input  logic rst_n,
  input  logic in_valid,
  output logic in_ready,
  input  logic [BEAT_W-1:0] in_data,
  input  logic in_last,
  output logic out_valid,
  input  logic out_ready,
  output logic [BUS_W-1:0] out_data,
  output logic [3:0] out_beats
);
  localparam int CW = (BEATS <= 2) ? 1 : $clog2(BEATS);
  logic [BUS_W-1:0] collect;
  logic [CW-1:0] beat;
  logic collecting;
  logic [BUS_W-1:0] assembled;

  always_comb begin
    // A completed descriptor is held until the command scheduler consumes it.
    in_ready = !out_valid;
    assembled = collect;
    assembled[beat*BEAT_W +: BEAT_W] = in_data;
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      collect <= '0;
      beat <= '0;
      collecting <= 1'b0;
      out_valid <= 1'b0;
      out_data <= '0;
      out_beats <= '0;
    end else begin
      if (out_valid && out_ready)
        out_valid <= 1'b0;
      if (in_valid && in_ready) begin
        collect <= assembled;
        collecting <= 1'b1;
        if (in_last || beat == BEATS-1) begin
          out_data <= assembled;
          out_valid <= 1'b1;
          out_beats <= beat + 1'b1;
          beat <= '0;
          collecting <= 1'b0;
        end else begin
          beat <= beat + 1'b1;
        end
      end
    end
  end
endmodule
`endif
