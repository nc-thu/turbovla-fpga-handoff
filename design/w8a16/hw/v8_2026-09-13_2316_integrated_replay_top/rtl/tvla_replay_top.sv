// TurboVLA activity-replay top (v8, 2026-09-13 23:16:21).
//
// The descriptor stream carries the wide shape/cycle sideband; the command
// word remains a compact 64-bit transport token.  A replay command adds one
// virtual event to the activity counters in a single clock.  A GEMM command
// also opens the real 16x48 W8A16 array feed ports, so representative payloads
// can be driven through the same top.  Large DINO/text events are represented
// by AUX_EVENT descriptors and are intentionally not claimed as synthesized
// accelerator blocks.
`ifndef TVLA_REPLAY_TOP_SV
`define TVLA_REPLAY_TOP_SV
module tvla_replay_top #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int ACC_W = 40,
  parameter int DESC_W = 512,
  parameter int DESC_ID_W = 16,
  parameter int DESC_FIFO_DEPTH = 16,
  parameter bit TRACE_ENABLE = 1'b1,
  parameter bit ENABLE_ARRAY = 1'b1
) (
  input  logic clk,
  input  logic rst_n,
  input  logic [63:0] cmd_word,
  input  logic cmd_valid,
  output logic cmd_ready,
  input  logic desc_valid,
  output logic desc_ready,
  input  logic [DESC_ID_W-1:0] desc_id,
  input  logic [DESC_W-1:0] desc_data,
  input  logic [ROWS*16-1:0] activation_data,
  input  logic activation_valid,
  output logic activation_ready,
  input  logic [PCOLS*8-1:0] weight_data,
  input  logic weight_valid,
  output logic weight_ready,
  input  logic feed_pulse,
  input  logic [((ROWS <= 1) ? 1 : $clog2(ROWS))-1:0] drain_row,
  output logic [PCOLS*ACC_W-1:0] snapshot_row,
  output logic output_valid,
  input  logic output_ready,
  output logic [PCOLS*ACC_W-1:0] output_data,
  input  logic fallback_valid,
  output logic fallback_ready,
  input  logic [63:0] fallback_data,
  output logic replay_done,
  output logic [1023:0] activity_snapshot,
  // The compact 1024-bit snapshot keeps the original software contract. Two
  // counters that used to be internal are exported separately so a host can
  // reconcile output traffic and queue pressure without overloading it.
  output logic [63:0] activity_output_bytes,
  output logic [63:0] activity_queue_max_occupancy
);
  localparam int FIFO_PTR_W = (DESC_FIFO_DEPTH <= 2) ? 1 : $clog2(DESC_FIFO_DEPTH);
  localparam logic [7:0] OP_GEMM = 8'h10;
  localparam logic [7:0] OP_BMM = 8'h11;
  localparam logic [7:0] OP_END = 8'hff;

  // Descriptor field map (MSB first).  The host compiler writes these fields
  // in a stable format; low-level modules never need to unpack a 64-bit word.
  wire [31:0] d_total_cycles = desc_data[511:480];
  wire [31:0] d_valid_mac = desc_data[479:448];
  wire [31:0] d_active_pe = desc_data[447:416];
  wire [31:0] d_dma_read = desc_data[415:384];
  wire [31:0] d_dma_write = desc_data[383:352];
  wire [31:0] d_vector = desc_data[351:320];
  wire [31:0] d_snapshot = desc_data[319:288];
  wire [31:0] d_requant = desc_data[287:256];
  wire [31:0] d_act_bytes = desc_data[255:224];
  wire [31:0] d_weight_bytes = desc_data[223:192];
  wire [31:0] d_output_bytes = desc_data[191:160];
  wire [31:0] d_m = desc_data[159:128];
  wire [31:0] d_n = desc_data[127:96];
  wire [31:0] d_k = desc_data[95:64];
  wire [7:0] d_op = desc_data[63:56];

  logic [DESC_ID_W-1:0] id_fifo [0:DESC_FIFO_DEPTH-1];
  logic [DESC_W-1:0] data_fifo [0:DESC_FIFO_DEPTH-1];
  logic [FIFO_PTR_W-1:0] fifo_head, fifo_tail;
  logic [FIFO_PTR_W:0] fifo_count;
  wire fifo_full = (fifo_count == DESC_FIFO_DEPTH);
  wire fifo_empty = (fifo_count == 0);
  assign desc_ready = ~fifo_full;

  wire [7:0] cmd_op = cmd_word[63:56];
  wire [DESC_ID_W-1:0] cmd_desc_id = cmd_word[47:32];
  wire cmd_matches_head = ~fifo_empty && (id_fifo[fifo_head] == cmd_desc_id);
  // The stream is ordered by the compiler.  Do not make a variable-indexed
  // equality comparator part of the timing path; retain the ID for logging and
  // consume the oldest descriptor whenever the FIFO is non-empty.
  wire cmd_is_end = (cmd_word[63:56] == 8'hff);
  assign cmd_ready = (replay_done == 1'b0) && (cmd_is_end || (fifo_count != 0));

  logic [DESC_W-1:0] current_desc;
  logic current_valid;
  logic array_feed_enable;
  wire [7:0] current_op = current_desc[63:56];
  wire current_is_gemm = (current_op == OP_GEMM) || (current_op == OP_BMM);

  wire array_feed_vld = array_feed_enable && activation_valid && weight_valid;
  assign activation_ready = array_feed_enable;
  assign weight_ready = array_feed_enable;
  assign fallback_ready = ~replay_done;
  assign output_valid = current_valid && current_is_gemm;
  assign output_data = snapshot_row;

  logic array_clr;
  generate
    if (ENABLE_ARRAY) begin : g_array
      w8a16_sysarr #(.ROWS(ROWS), .PCOLS(PCOLS), .ACC_W(ACC_W)) u_array (
        .clk(clk), .rst_n(rst_n), .clr(array_clr),
        .feed_vld(array_feed_vld), .feed_pulse(feed_pulse && array_feed_enable),
        .a_feed(activation_data), .b_feed(weight_data), .drain_row(drain_row),
        .snap_row(snapshot_row)
      );
    end else begin : g_no_array
      always_comb snapshot_row = '0;
    end
  endgenerate

  // Activity counters use 64-bit accumulators so a full trace does not wrap.
  logic [63:0] total_cycles_r, mapped_cycles_r, fallback_cycles_r;
  logic [63:0] dma_read_cycles_r, dma_write_cycles_r, scheduler_wait_r;
  logic [63:0] backpressure_r, snapshot_cycles_r, requant_cycles_r, vector_cycles_r;
  logic [63:0] active_pe_cycles_r, busy_pe_cycles_r, valid_mac_r, tile_count_r;
  logic [63:0] activation_bytes_r, weight_bytes_r, output_bytes_r;
  logic [63:0] queue_max_r;

  // A descriptor is consumed in one control clock for activity replay.  The
  // virtual time in d_total_cycles still reports the measured/modelled cycle
  // budget; this avoids a 150-million-cycle RTL test for one forward while a
  // separate representative tile test exercises the arithmetic cycle by cycle.
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      fifo_head <= '0; fifo_tail <= '0; fifo_count <= '0;
      current_desc <= '0; current_valid <= 1'b0; array_feed_enable <= 1'b0;
      array_clr <= 1'b0; replay_done <= 1'b0;
      total_cycles_r <= '0; mapped_cycles_r <= '0; fallback_cycles_r <= '0;
      dma_read_cycles_r <= '0; dma_write_cycles_r <= '0; scheduler_wait_r <= '0;
      backpressure_r <= '0; snapshot_cycles_r <= '0; requant_cycles_r <= '0;
      vector_cycles_r <= '0; active_pe_cycles_r <= '0; busy_pe_cycles_r <= '0;
      valid_mac_r <= '0; tile_count_r <= '0; activation_bytes_r <= '0;
      weight_bytes_r <= '0; output_bytes_r <= '0; queue_max_r <= '0;
    end else begin
      array_clr <= 1'b0;
      current_valid <= 1'b0;
      if (desc_valid && desc_ready) begin
        id_fifo[fifo_tail] <= desc_id;
        data_fifo[fifo_tail] <= desc_data;
        if (fifo_tail == DESC_FIFO_DEPTH-1) fifo_tail <= '0;
        else fifo_tail <= fifo_tail + 1'b1;
        fifo_count <= fifo_count + 1'b1;
        if ((fifo_count + 1'b1) > queue_max_r) queue_max_r <= fifo_count + 1'b1;
      end
      if (cmd_valid && cmd_ready) begin
        if (cmd_op == OP_END) begin
          replay_done <= 1'b1;
        end else begin
          current_desc <= data_fifo[fifo_head];
          current_valid <= 1'b1;
          total_cycles_r <= total_cycles_r + data_fifo[fifo_head][511:480];
          valid_mac_r <= valid_mac_r + data_fifo[fifo_head][479:448];
          active_pe_cycles_r <= active_pe_cycles_r + data_fifo[fifo_head][447:416];
          if (data_fifo[fifo_head][63:56] == OP_GEMM || data_fifo[fifo_head][63:56] == OP_BMM)
            busy_pe_cycles_r <= busy_pe_cycles_r + (data_fifo[fifo_head][511:480] * PCOLS * ROWS);
          activation_bytes_r <= activation_bytes_r + data_fifo[fifo_head][255:224];
          weight_bytes_r <= weight_bytes_r + data_fifo[fifo_head][223:192];
          output_bytes_r <= output_bytes_r + data_fifo[fifo_head][191:160];
          if (data_fifo[fifo_head][63:56] == OP_GEMM || data_fifo[fifo_head][63:56] == OP_BMM) begin
            mapped_cycles_r <= mapped_cycles_r + data_fifo[fifo_head][511:480];
            tile_count_r <= tile_count_r + data_fifo[fifo_head][31:16];
            snapshot_cycles_r <= snapshot_cycles_r + data_fifo[fifo_head][319:288];
            requant_cycles_r <= requant_cycles_r + data_fifo[fifo_head][287:256];
            array_feed_enable <= 1'b1;
            array_clr <= 1'b1;
          end else if (data_fifo[fifo_head][63:56] == 8'h30 || data_fifo[fifo_head][63:56] == 8'h31 || data_fifo[fifo_head][63:56] == 8'h33) begin
            vector_cycles_r <= vector_cycles_r + data_fifo[fifo_head][351:320];
            // Keep the aggregate fallback bucket consistent with the
            // compiler's cycle ledger.  Vector operators have their own
            // subtotal above, but they still occupy behavior-level cycles.
            fallback_cycles_r <= fallback_cycles_r + data_fifo[fifo_head][351:320];
          end else begin
            fallback_cycles_r <= fallback_cycles_r + data_fifo[fifo_head][511:480];
          end
          dma_read_cycles_r <= dma_read_cycles_r + data_fifo[fifo_head][415:384];
          dma_write_cycles_r <= dma_write_cycles_r + data_fifo[fifo_head][383:352];
          if (fifo_head == DESC_FIFO_DEPTH-1) fifo_head <= '0;
          else fifo_head <= fifo_head + 1'b1;
          fifo_count <= fifo_count - 1'b1;
        end
      end
      if (array_feed_enable && feed_pulse) array_feed_enable <= 1'b0;
      if (fallback_valid && !fallback_ready) backpressure_r <= backpressure_r + 1'b1;
      if (fifo_count > queue_max_r) queue_max_r <= fifo_count;
    end
  end

  // Keep a stable, software-readable counter layout.  The first 64-bit words
  // are the values used in the report; the remaining bits are reserved.
  always_comb begin
    activity_snapshot = '0;
    activity_snapshot[63:0] = total_cycles_r;
    activity_snapshot[127:64] = mapped_cycles_r;
    activity_snapshot[191:128] = fallback_cycles_r;
    activity_snapshot[255:192] = dma_read_cycles_r;
    activity_snapshot[319:256] = dma_write_cycles_r;
    activity_snapshot[383:320] = scheduler_wait_r;
    activity_snapshot[447:384] = backpressure_r;
    activity_snapshot[511:448] = snapshot_cycles_r;
    activity_snapshot[575:512] = requant_cycles_r;
    activity_snapshot[639:576] = vector_cycles_r;
    activity_snapshot[703:640] = active_pe_cycles_r;
    activity_snapshot[767:704] = busy_pe_cycles_r;
    activity_snapshot[831:768] = valid_mac_r;
    activity_snapshot[895:832] = tile_count_r;
    activity_snapshot[959:896] = activation_bytes_r;
    activity_snapshot[1023:960] = weight_bytes_r;
    activity_output_bytes = output_bytes_r;
    activity_queue_max_occupancy = queue_max_r;
  end
endmodule
`endif
