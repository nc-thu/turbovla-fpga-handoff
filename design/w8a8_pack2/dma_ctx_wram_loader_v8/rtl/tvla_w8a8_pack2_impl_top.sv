// Board-facing implementation wrapper for Vivado placement.
//
// The replay top keeps wide internal snapshot/output/activity buses because
// they are useful for RTL verification.  Exposing those buses as package pins
// would create thousands of I/Os and makes a real device implementation
// impossible.  This wrapper keeps the full replay/array logic inside the
// device and presents narrow streaming ports suitable for the target package.
`ifndef TVLA_W8A8_PACK2_IMPL_TOP_SV
`define TVLA_W8A8_PACK2_IMPL_TOP_SV
module tvla_w8a8_pack2_impl_top #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int DESC_W = 512,
  parameter int DESC_ID_W = 8,
  parameter int DESC_FIFO_DEPTH = 16,
  parameter bit ENABLE_ARRAY = 1'b1
)(
  input  logic clk,
  input  logic rst_n,
  input  logic [63:0] cmd_word,
  input  logic cmd_valid,
  output logic cmd_ready,
  input  logic desc_valid,
  output logic desc_ready,
  input  logic [DESC_ID_W-1:0] desc_id,
  // A compact descriptor ingress is expanded into the internal sideband.
  input  logic [15:0] desc_data,
  input  logic [63:0] activation_data,
  input  logic activation_valid,
  output logic activation_ready,
  // One 128-bit ingress beat is fanned out to the six internal 128-bit
  // slices that make up the 48-column (768-bit) weight bus.  The array still
  // contains one DSP per physical column; this is only a package interface.
  input  logic [63:0] weight_data,
  input  logic weight_valid,
  output logic weight_ready,
  input  logic feed_pulse,
  input  logic [((ROWS <= 1) ? 1 : $clog2(ROWS))-1:0] drain_row,
  output logic output_valid,
  input  logic output_ready,
  output logic [31:0] output_data,
  input  logic fallback_valid,
  output logic fallback_ready,
  input  logic [15:0] fallback_data,
  output logic replay_done,
  output logic [15:0] activity_snapshot,
  output logic [15:0] activity_output_bytes,
  output logic [15:0] activity_queue_max_occupancy,
  output logic [15:0] activity_optimization_hits,
  output logic [15:0] activity_write_burst_count
);
  logic [DESC_W-1:0] desc_bus;
  logic [PCOLS*16-1:0] weight_bus;
  logic [PCOLS*2*32-1:0] snapshot_bus;
  logic [PCOLS*2*32-1:0] output_bus;
  logic output_valid_i;
  logic [1023:0] activity_bus;
  logic [63:0] activity_output_bytes_i;
  logic [63:0] activity_queue_max_occupancy_i;
  logic [63:0] activity_optimization_hits_i;
  logic [63:0] activity_write_burst_count_i;

  // Repeat the compact ingress beat to keep all physical weight lanes
  // exercised during implementation.  A production DMA supplies distinct
  // slices; this wrapper only changes the package-facing width.
  always_comb begin
    desc_bus = '0;
    desc_bus[15:0] = desc_data;
    for (int r = 1; r < DESC_W/16; r++) begin
      desc_bus[r*16 +: 16] = desc_data;
    end
    weight_bus = '0;
    for (int c = 0; c < PCOLS; c++) begin
      weight_bus[c*16 +: 16] = weight_data[(c % 4)*16 +: 16];
    end
  end

  logic [ROWS*8-1:0] activation_bus;
  always_comb begin
    activation_bus = '0;
    for (int r = 0; r < ROWS; r++) begin
      activation_bus[r*8 +: 8] = activation_data[(r % 8)*8 +: 8];
    end
  end

  logic [63:0] fallback_bus;
  assign fallback_bus = {48'b0, fallback_data};

  tvla_w8a8_pack2_system_top #(
    .ROWS(ROWS), .PCOLS(PCOLS), .DESC_W(DESC_W), .DESC_ID_W(DESC_ID_W),
    .DESC_FIFO_DEPTH(DESC_FIFO_DEPTH), .ENABLE_ARRAY(ENABLE_ARRAY)
  ) u_system (
    .clk(clk), .rst_n(rst_n),
    .cmd_word(cmd_word), .cmd_valid(cmd_valid), .cmd_ready(cmd_ready),
    .desc_valid(desc_valid), .desc_ready(desc_ready), .desc_id(desc_id),
    .desc_data(desc_bus),
    .activation_data(activation_bus), .activation_valid(activation_valid),
    .activation_ready(activation_ready),
    .weight_data(weight_bus), .weight_valid(weight_valid),
    .weight_ready(weight_ready), .feed_pulse(feed_pulse),
    .drain_row(drain_row), .snapshot_row(snapshot_bus),
    .output_valid(output_valid_i), .output_ready(output_ready),
    .output_data(output_bus), .fallback_valid(fallback_valid),
    .fallback_ready(fallback_ready), .fallback_data(fallback_bus),
    .replay_done(replay_done), .activity_snapshot(activity_bus),
    .activity_output_bytes(activity_output_bytes_i),
    .activity_queue_max_occupancy(activity_queue_max_occupancy_i),
    .activity_optimization_hits(activity_optimization_hits_i),
    .activity_write_burst_count(activity_write_burst_count_i)
  );

  assign output_valid = output_valid_i;
  // Fold every internal result slice into the narrow monitor port.  This is
  // deliberate: otherwise Vivado could legally prune the unobserved output
  // columns and the implementation would no longer contain all 768 DSPs.
  always_comb begin
    output_data = '0;
    for (int s = 0; s < (PCOLS*2*32)/32; s++) begin
      output_data = output_data ^ output_bus[s*32 +: 32];
    end
  end
  assign activity_snapshot = activity_bus[15:0];
  assign activity_output_bytes = activity_output_bytes_i[15:0];
  assign activity_queue_max_occupancy = activity_queue_max_occupancy_i[15:0];
  assign activity_optimization_hits = activity_optimization_hits_i[15:0];
  assign activity_write_burst_count = activity_write_burst_count_i[15:0];
endmodule
`endif
