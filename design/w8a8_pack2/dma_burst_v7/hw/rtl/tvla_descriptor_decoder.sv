// First-beat decoder for the TurboVLA descriptor sideband.
//
// The command word stays 64 bits.  A descriptor is transferred as one or more
// sideband beats by the surrounding FIFO; this small block decodes the first
// beat early so the vector engine can choose its numeric path without waiting
// for a complete GEMM payload.  Later beats are still consumed by the replay
// shell, which owns the 512-bit accounting fields.
`ifndef TVLA_DESCRIPTOR_DECODER_SV
`define TVLA_DESCRIPTOR_DECODER_SV
module tvla_descriptor_decoder #(
  parameter int ID_W = 16
) (
  input  logic clk,
  input  logic rst_n,
  input  logic in_valid,
  output logic in_ready,
  input  logic consume,
  input  logic [ID_W-1:0] in_id,
  input  logic [15:0] in_data,
  output logic valid,
  output logic [ID_W-1:0] descriptor_id,
  output logic fp16_mode,
  output logic [1:0] numeric_format,
  output logic barrier,
  output logic transpose,
  output logic mask_enable,
  output logic [7:0] opcode_hint
);
  // One first-beat register is enough because a command cannot consume a new
  // descriptor until the replay FIFO has accepted the current one.
  // The replay FIFO already supplies the backpressure.  This sideband tap
  // never stalls that FIFO; it simply remembers the most recent first beat.
  assign in_ready = 1'b1;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      valid          <= 1'b0;
      descriptor_id  <= '0;
      fp16_mode      <= 1'b0;
      numeric_format  <= 2'd0;
      barrier        <= 1'b0;
      transpose      <= 1'b0;
      mask_enable    <= 1'b0;
      opcode_hint    <= 8'd0;
    end else begin
      // A decoder token is consumed when the associated command is accepted.
      // The top-level currently clears it with the next descriptor beat; the
      // explicit valid bit remains observable for formal/simulation checks.
      if (in_valid && in_ready) begin
        valid         <= 1'b1;
        descriptor_id <= in_id;
        numeric_format <= in_data[1:0];
        fp16_mode     <= in_data[15];
        barrier       <= in_data[14];
        transpose     <= in_data[10];
        mask_enable   <= in_data[11];
        opcode_hint   <= in_data[7:0];
      end
      // The descriptor FIFO uses a new descriptor beat as the release point.
      // Keeping the current value for one extra cycle makes it safe for a
      // command and its vector payload to observe the same format bit.
      else if (consume) begin
        valid <= 1'b0;
      end
    end
  end
endmodule
`endif
