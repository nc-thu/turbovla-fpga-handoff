// TurboVLA W8A8 Pack2 activity-replay top.
// The command stream is compact; all matrix and timing fields arrive in the
// 512-bit descriptor sideband.  A GEMM descriptor is counted with the real
// 16x48 Pack2 array feed ports, while non-mapped operators remain explicit
// behavior-level events.
`ifndef TVLA_W8A8_PACK2_REPLAY_TOP_TIMING_SV
`define TVLA_W8A8_PACK2_REPLAY_TOP_TIMING_SV
module tvla_w8a8_pack2_replay_top_timing #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int DESC_W = 512,
  parameter int DESC_ID_W = 16,
  parameter int DESC_FIFO_DEPTH = 16,
  parameter bit ENABLE_ARRAY = 1'b1
)(
  input logic clk, input logic rst_n,
  input logic [63:0] cmd_word, input logic cmd_valid, output logic cmd_ready,
  input logic desc_valid, output logic desc_ready,
  input logic [DESC_ID_W-1:0] desc_id, input logic [DESC_W-1:0] desc_data,
  input logic [ROWS*8-1:0] activation_data, input logic activation_valid,
  output logic activation_ready,
  input logic [PCOLS*16-1:0] weight_data, input logic weight_valid,
  output logic weight_ready,
  input logic feed_pulse,
  input logic [((ROWS <= 1) ? 1 : $clog2(ROWS))-1:0] drain_row,
  output logic [PCOLS*2*32-1:0] snapshot_row,
  output logic output_valid, input logic output_ready,
  output logic [PCOLS*2*32-1:0] output_data,
  input logic fallback_valid, output logic fallback_ready,
  input logic [63:0] fallback_data,
  output logic replay_done,
  output logic [1023:0] activity_snapshot,
  output logic [63:0] activity_output_bytes,
  output logic [63:0] activity_queue_max_occupancy,
  output logic [63:0] activity_optimization_hits,
  output logic [63:0] activity_write_burst_count
);
  localparam int FIFO_PTR_W = (DESC_FIFO_DEPTH <= 2) ? 1 : $clog2(DESC_FIFO_DEPTH);
  localparam int LOGICAL = PCOLS * 2;
  localparam logic [7:0] OP_GEMM = 8'h18;
  localparam logic [7:0] OP_BMM  = 8'h19;
  localparam logic [7:0] OP_END  = 8'hff;

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

  logic [DESC_ID_W-1:0] id_fifo [0:DESC_FIFO_DEPTH-1];
  logic [DESC_W-1:0] data_fifo [0:DESC_FIFO_DEPTH-1];
  logic [FIFO_PTR_W-1:0] fifo_head, fifo_tail;
  logic [FIFO_PTR_W:0] fifo_count;
  wire fifo_full = fifo_count == DESC_FIFO_DEPTH;
  wire fifo_empty = fifo_count == 0;
  assign desc_ready = !fifo_full;
  wire desc_push = desc_valid && desc_ready;
  wire [7:0] cmd_op = cmd_word[63:56];
  wire cmd_is_end = cmd_op == OP_END;
  wire cmd_is_gemm = (cmd_op == OP_GEMM) || (cmd_op == OP_BMM);

  logic result_valid_r;
  logic [LOGICAL*32-1:0] result_data_r;
  wire result_slot_free = !result_valid_r || output_ready;
  // END is a fence after the descriptor FIFO drains, so it must be accepted
  // when the FIFO is empty.  Ordinary commands still require a queued
  // descriptor and, for mapped work, a free result slot.
  assign cmd_ready = !replay_done &&
                     ((cmd_is_end && fifo_empty) ||
                      (!cmd_is_end && !fifo_empty && (!cmd_is_gemm || result_slot_free)));
  wire cmd_fire = cmd_valid && cmd_ready;
  wire cmd_pop = cmd_fire && !cmd_is_end;
  assign output_valid = result_valid_r;
  assign output_data = result_data_r;
  assign fallback_ready = !replay_done;

  logic array_feed_enable;
  assign activation_ready = array_feed_enable;
  assign weight_ready = array_feed_enable;
  wire array_feed_vld = array_feed_enable && activation_valid && weight_valid;
  wire [15:0] drain_row_ext = {{(16-$bits(drain_row)){1'b0}}, drain_row};
  logic [((PCOLS+3)/4)*4-1:0] drain_row_rep;
  always_comb begin
    for (int r = 0; r < (PCOLS+3)/4; r++) drain_row_rep[r*4 +: 4] = drain_row_ext[3:0];
  end
  logic array_clr;

  generate
    if (ENABLE_ARRAY) begin : g_array
      tvla_w8a8_pack2_timing_array_top #(.ROWS(ROWS), .PCOLS(PCOLS)) u_array (
        .clk(clk), .rst_n(rst_n), .clr(array_clr),
        .feed_vld(array_feed_vld), .feed_pulse(feed_pulse && array_feed_enable),
        .a_feed(activation_data), .b_feed(weight_data),
        .drain_row_rep(drain_row_rep), .acc_row(snapshot_row)
      );
    end else begin : g_no_array
      always_comb snapshot_row = '0;
    end
  endgenerate

  logic [63:0] total_cycles_r, mapped_cycles_r, fallback_cycles_r;
  logic [63:0] dma_read_cycles_r, dma_write_cycles_r, scheduler_wait_r, backpressure_r;
  logic [63:0] snapshot_cycles_r, requant_cycles_r, vector_cycles_r;
  logic [63:0] active_pe_cycles_r, busy_pe_cycles_r, valid_mac_r, tile_count_r;
  logic [63:0] activation_bytes_r, weight_bytes_r, output_bytes_r;
  logic [63:0] queue_max_r, optimization_hits_r, write_burst_r;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      fifo_head <= '0; fifo_tail <= '0; fifo_count <= '0;
      result_valid_r <= 1'b0; result_data_r <= '0; replay_done <= 1'b0;
      array_feed_enable <= 1'b0; array_clr <= 1'b0;
      total_cycles_r <= '0; mapped_cycles_r <= '0; fallback_cycles_r <= '0;
      dma_read_cycles_r <= '0; dma_write_cycles_r <= '0; scheduler_wait_r <= '0;
      backpressure_r <= '0; snapshot_cycles_r <= '0; requant_cycles_r <= '0;
      vector_cycles_r <= '0; active_pe_cycles_r <= '0; busy_pe_cycles_r <= '0;
      valid_mac_r <= '0; tile_count_r <= '0; activation_bytes_r <= '0;
      weight_bytes_r <= '0; output_bytes_r <= '0; queue_max_r <= '0;
      optimization_hits_r <= '0; write_burst_r <= '0;
    end else begin
      array_clr <= 1'b0;
      if (result_valid_r && output_ready) result_valid_r <= 1'b0;
      if (desc_push) begin
        id_fifo[fifo_tail] <= desc_id;
        data_fifo[fifo_tail] <= desc_data;
        fifo_tail <= (fifo_tail == DESC_FIFO_DEPTH-1) ? '0 : fifo_tail + 1'b1;
        if (fifo_count + 1'b1 > queue_max_r) queue_max_r <= fifo_count + 1'b1;
      end
      if (cmd_fire) begin
        if (cmd_is_end) begin
          replay_done <= 1'b1;
        end else begin
          total_cycles_r <= total_cycles_r + data_fifo[fifo_head][511:480];
          valid_mac_r <= valid_mac_r + data_fifo[fifo_head][479:448];
          active_pe_cycles_r <= active_pe_cycles_r + data_fifo[fifo_head][447:416];
          activation_bytes_r <= activation_bytes_r + data_fifo[fifo_head][255:224];
          weight_bytes_r <= weight_bytes_r + data_fifo[fifo_head][223:192];
          output_bytes_r <= output_bytes_r + data_fifo[fifo_head][191:160];
          dma_read_cycles_r <= dma_read_cycles_r + data_fifo[fifo_head][415:384];
          dma_write_cycles_r <= dma_write_cycles_r + data_fifo[fifo_head][383:352];
          if (data_fifo[fifo_head][55:48] != 8'h00) optimization_hits_r <= optimization_hits_r + 1'b1;
          if (data_fifo[fifo_head][55]) write_burst_r <= write_burst_r + 1'b1;
          if (data_fifo[fifo_head][63:56] == OP_GEMM || data_fifo[fifo_head][63:56] == OP_BMM) begin
            mapped_cycles_r <= mapped_cycles_r + data_fifo[fifo_head][511:480];
            busy_pe_cycles_r <= busy_pe_cycles_r + data_fifo[fifo_head][511:480] * ROWS * PCOLS;
            tile_count_r <= tile_count_r + data_fifo[fifo_head][31:16];
            snapshot_cycles_r <= snapshot_cycles_r + data_fifo[fifo_head][319:288];
            requant_cycles_r <= requant_cycles_r + data_fifo[fifo_head][287:256];
            array_feed_enable <= 1'b1;
            array_clr <= 1'b1;
            if (result_slot_free) begin result_valid_r <= 1'b1; result_data_r <= snapshot_row; end
          end else if (data_fifo[fifo_head][63:56] == 8'h30 || data_fifo[fifo_head][63:56] == 8'h31 || data_fifo[fifo_head][63:56] == 8'h33) begin
            vector_cycles_r <= vector_cycles_r + data_fifo[fifo_head][351:320];
            fallback_cycles_r <= fallback_cycles_r + data_fifo[fifo_head][351:320];
          end else begin
            fallback_cycles_r <= fallback_cycles_r + data_fifo[fifo_head][511:480];
          end
          fifo_head <= (fifo_head == DESC_FIFO_DEPTH-1) ? '0 : fifo_head + 1'b1;
        end
      end
      case ({desc_push, cmd_pop})
        2'b10: fifo_count <= fifo_count + 1'b1;
        2'b01: fifo_count <= fifo_count - 1'b1;
        default: fifo_count <= fifo_count;
      endcase
      if (array_feed_enable && feed_pulse) array_feed_enable <= 1'b0;
      if (output_valid && !output_ready) backpressure_r <= backpressure_r + 1'b1;
      if (fallback_valid && !fallback_ready) backpressure_r <= backpressure_r + 1'b1;
      if (cmd_valid && !cmd_ready) scheduler_wait_r <= scheduler_wait_r + 1'b1;
    end
  end

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
    activity_optimization_hits = optimization_hits_r;
    activity_write_burst_count = write_burst_r;
  end
endmodule
`endif
