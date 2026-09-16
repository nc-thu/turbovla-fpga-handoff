// Full TurboVLA command replay top.  GEMM/BMM use the existing Pack2 array;
// vector, layout, embedding, im2col, memory and action units are explicit
// blocks so the compiler has a real destination for every instruction class.
`ifndef TVLA_FULL_MODEL_REPLAY_TOP_SV
`define TVLA_FULL_MODEL_REPLAY_TOP_SV
module tvla_full_model_replay_top #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int DESC_W = 512,
  parameter int DESC_ID_W = 8
) (
  input logic clk, input logic rst_n,
  input logic [63:0] cmd_word, input logic cmd_valid, output logic cmd_ready,
  input logic desc_valid, output logic desc_ready,
  input logic [DESC_ID_W-1:0] desc_id, input logic [DESC_W-1:0] desc_data,
  input logic [127:0] activation_data, input logic activation_valid,
  output logic activation_ready,
  input logic [767:0] weight_data, input logic weight_valid,
  output logic weight_ready, input logic feed_pulse,
  input logic [3:0] drain_row,
  input logic [255:0] vector_x, input logic [255:0] vector_y,
  input logic vector_valid, output logic vector_ready,
  output logic vector_out_valid, input logic vector_out_ready,
  output logic [255:0] vector_out,
  input logic [111:0] action_data, input logic action_valid,
  output logic action_ready, output logic action_out_valid,
  input logic action_out_ready, output logic [111:0] action_target,
  output logic action_gripper, output logic [7:0] action_step,
  output logic replay_done,
  output logic [1023:0] activity_snapshot,
  output logic [31:0] architecture_observe
);
  localparam logic [7:0] OP_GEMM=8'h18, OP_BMM=8'h19, OP_END=8'hff;
  localparam logic [7:0] OP_LAYOUT=8'h40, OP_CONV=8'h42, OP_EMBED=8'h39;
  localparam logic [7:0] OP_POS=8'h3a, OP_COS=8'h3b, OP_SIN=8'h3c;
  localparam logic [7:0] OP_ACTION=8'h60;
  wire [7:0] cmd_op = cmd_word[63:56];
  wire vector_op = (cmd_op==8'h20)||(cmd_op==8'h21)||(cmd_op==8'h22)||
                   (cmd_op>=8'h30 && cmd_op<=8'h38);
  wire layout_op = (cmd_op==OP_LAYOUT);
  wire embed_op = (cmd_op==OP_EMBED)||(cmd_op==OP_POS)||(cmd_op==OP_COS)||(cmd_op==OP_SIN);
  wire action_op = (cmd_op==OP_ACTION);
  logic [255:0] vec_unit_out;
  logic vec_unit_valid, vec_unit_ready;
  logic layout_valid, layout_ready;
  logic [255:0] layout_out;
  logic embed_valid, embed_ready;
  logic [255:0] embed_out;
  logic conv_out_valid, conv_in_ready;
  logic [143:0] conv_out;
  logic bmm_out_valid, bmm_out_ready;
  logic [255:0] bmm_a;
  logic [767:0] bmm_b;
  logic [3:0] bmm_index;
  logic bmm_last;
  logic [127:0] ctx_rdata;
  logic [767:0] wram_rdata;
  logic dma_busy, dma_done;
  logic [31:0] dma_rcycles, dma_wcycles;
  logic [127:0] dma_stream_data;
  logic dma_stream_valid;
  logic dma_arvalid, dma_rready, dma_awvalid, dma_wvalid, dma_wlast, dma_bready;
  // The board wrapper currently models an always-available AXI memory endpoint.
  // These are wires rather than unconnected logic so Vivado cannot infer that
  // the DMA datapath is dead and remove it from the integrated top.
  wire dma_arready = 1'b1;
  wire dma_rvalid = 1'b0;
  wire dma_rlast = 1'b1;
  wire dma_awready = 1'b1;
  wire dma_wready = 1'b1;
  wire dma_bvalid = 1'b0;
  logic [63:0] dma_araddr, dma_awaddr;
  logic [7:0] dma_arlen, dma_awlen;
  wire [127:0] dma_rdata = '0;
  logic [127:0] dma_wdata;
  logic [15:0] dma_wstrb;
  logic dma_stream_ready;
  logic [63:0] fallback_zero;
  logic [7:0] embed_idx_zero;
  logic [255:0] embed_data_zero;
  logic [127:0] dma_stream_zero;
  assign fallback_zero = '0;
  assign embed_idx_zero = '0;
  assign embed_data_zero = '0;
  assign dma_stream_zero = '0;
  logic fp16_valid, fp16_ready;
  logic [255:0] fp16_out;
  logic action_valid_i;
  wire special_ready = vector_op ? (vector_valid && vec_unit_ready) :
                        layout_op ? (vector_valid && layout_ready) :
                        // The producer is ready before a result exists.  The
                        // old gate used embed_valid here and could deadlock
                        // the first embedding/position command.
                        embed_op ? embed_ready :
                        action_op ? (action_valid && action_ready) : 1'b1;
  wire gated_cmd_valid = cmd_valid && special_ready;
  wire gated_cmd_fire = gated_cmd_valid && cmd_ready;

  // The legacy replay shell owns the descriptor FIFO, Pack2 array and the
  // accounting fields.  Non-GEMM commands are still counted as fallback;
  // the explicit blocks below execute the corresponding payload in parallel.
  logic [1023:0] base_activity;
  // Keep the complete Pack2 array in the full-model implementation.  Without
  // this boundary Vivado can legally prune idle PE lanes when a replay trace
  // does not toggle every command in the small board wrapper.
  (* DONT_TOUCH = "yes" *) logic [PCOLS*2*32-1:0] pack2_snapshot;
  (* DONT_TOUCH = "yes" *) logic [PCOLS*2*32-1:0] pack2_output;
  logic pack2_output_valid;
  (* DONT_TOUCH = "yes" *) tvla_w8a8_pack2_replay_top_timing #(.ROWS(ROWS), .PCOLS(PCOLS), .DESC_W(DESC_W),
    .DESC_ID_W(DESC_ID_W), .DESC_FIFO_DEPTH(16), .ENABLE_ARRAY(1'b1)) u_pack2 (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(gated_cmd_valid),
    .cmd_ready(cmd_ready), .desc_valid(desc_valid), .desc_ready(desc_ready),
    .desc_id(desc_id), .desc_data(desc_data), .activation_data(activation_data),
    .activation_valid(activation_valid), .activation_ready(activation_ready),
    .weight_data(weight_data), .weight_valid(weight_valid), .weight_ready(weight_ready),
    .feed_pulse(feed_pulse), .drain_row(drain_row), .snapshot_row(pack2_snapshot),
    .output_valid(pack2_output_valid), .output_ready(1'b1), .output_data(pack2_output), .fallback_valid(1'b0),
    .fallback_ready(), .fallback_data(fallback_zero), .replay_done(replay_done),
    .activity_snapshot(base_activity), .activity_output_bytes(),
    .activity_queue_max_occupancy(), .activity_optimization_hits(),
    .activity_write_burst_count()
  );

  tvla_full_vector_unit #(.LANES(16), .DW(16)) u_vector (
    .clk(clk), .rst_n(rst_n), .in_valid(gated_cmd_fire && vector_op),
    .in_ready(vec_unit_ready), .op_code(cmd_op), .x(vector_x), .y(vector_y),
    .param0($signed(desc_data[31:16])), .param1($signed(desc_data[15:0])),
    .out_valid(vec_unit_valid), .out_ready(vector_out_ready), .out_data(vec_unit_out),
    .busy_cycles(), .op_count()
  );
  tvla_layout_unit #(.LANES(16), .DW(16)) u_layout (
    .clk(clk), .rst_n(rst_n), .in_valid(gated_cmd_fire && layout_op),
    .in_ready(layout_ready), .mode(desc_data[35:32]), .in_data(vector_x),
     .index_data({32'd0, desc_data[31:0]}), .out_valid(layout_valid), .out_ready(vector_out_ready),
    .out_data(layout_out)
  );
  tvla_embedding_posenc #(.LANES(16), .DW(16)) u_embed (
    .clk(clk), .rst_n(rst_n), .in_valid(gated_cmd_fire && embed_op),
    .in_ready(embed_ready), .mode((cmd_op==OP_EMBED)?2'd0:(cmd_op==OP_POS)?2'd1:(cmd_op==OP_COS)?2'd2:2'd3),
    .token_index(desc_data[15:0]), .position(desc_data[31:16]), .table_wr_en(1'b0),
    .table_wr_index(embed_idx_zero), .table_wr_data(embed_data_zero), .out_valid(embed_valid),
    .out_ready(vector_out_ready), .out_data(embed_out)
  );
  tvla_conv_im2col #(.DW(16), .WINDOW(9)) u_im2col (
    .clk(clk), .rst_n(rst_n), .start(gated_cmd_fire && cmd_op==OP_CONV),
    .in_valid(vector_valid), .in_ready(conv_in_ready), .in_data(vector_x[15:0]),
    .out_valid(conv_out_valid), .out_ready(vector_out_ready), .out_data(conv_out), .out_last()
  );
  tvla_bmm_layout #(.ROWS(16), .COLS(48), .DW(16)) u_bmm_layout (
    .clk(clk), .rst_n(rst_n), .start(gated_cmd_fire && (cmd_op==OP_BMM)),
    .a_valid(vector_valid), .a_row(vector_x), .a_index(desc_data[3:0]),
     .b_valid(weight_valid), .b_row(weight_data), .b_index(desc_data[9:4]),
    .transpose_b(desc_data[10]), .in_ready(), .out_valid(bmm_out_valid),
    .out_ready(bmm_out_ready), .out_a(bmm_a), .out_b(bmm_b), .out_index(bmm_index), .out_last(bmm_last)
  );
  assign bmm_out_ready = 1'b1;
  wire [9:0] mem_addr = desc_data[31:22];
  wire ctx_store = activation_valid && activation_ready;
  wire wram_store = weight_valid && weight_ready;
  tvla_ctx_wram #(.CTX_DEPTH(1024), .WRAM_DEPTH(1024)) u_mem (
    .clk(clk), .rst_n(rst_n), .ctx_wr_en(ctx_store), .ctx_wr_addr(mem_addr), .ctx_wr_data(activation_data),
    .ctx_rd_en(1'b1), .ctx_rd_addr(desc_data[31:22]), .ctx_rd_data(ctx_rdata),
    .wram_wr_en(wram_store), .wram_wr_addr(mem_addr), .wram_wr_data(weight_data), .wram_rd_en(1'b1),
    .wram_rd_addr(desc_data[31:22]), .wram_rd_data(wram_rdata)
  );
  localparam logic [7:0] OP_DMA_READ = 8'h01;
  localparam logic [7:0] OP_DMA_WRITE = 8'h02;
  tvla_dma_axi #(.DW(128)) u_dma (
    .clk(clk), .rst_n(rst_n), .start_read(cmd_valid && cmd_op==OP_DMA_READ),
    .start_write(cmd_valid && cmd_op==OP_DMA_WRITE),
    .base_addr({32'd0, desc_data[31:0]}), .length_bytes(desc_data[63:32]), .busy(dma_busy), .done(dma_done),
    .read_cycles(dma_rcycles), .write_cycles(dma_wcycles), .m_axi_arvalid(dma_arvalid),
    .m_axi_arready(dma_arready), .m_axi_araddr(dma_araddr), .m_axi_arlen(dma_arlen),
    .m_axi_rready(dma_rready), .m_axi_rvalid(dma_rvalid), .m_axi_rdata(dma_rdata),
    .m_axi_rlast(dma_rlast), .m_axi_awvalid(dma_awvalid), .m_axi_awready(dma_awready),
    .m_axi_awaddr(dma_awaddr), .m_axi_awlen(dma_awlen), .m_axi_wvalid(dma_wvalid),
    .m_axi_wready(dma_wready), .m_axi_wdata(dma_wdata), .m_axi_wstrb(dma_wstrb),
    .m_axi_wlast(dma_wlast), .m_axi_bvalid(dma_bvalid), .m_axi_bready(dma_bready),
    .stream_out_valid(dma_stream_valid), .stream_out_ready(dma_stream_ready),
    .stream_out_data(dma_stream_data), .stream_in_valid(1'b0), .stream_in_ready(),
    .stream_in_data(dma_stream_zero)
  );
  tvla_fp16_activation_wrap #(.LANES(16), .USE_VENDOR_FP16(1'b0)) u_fp16 (
    .clk(clk), .rst_n(rst_n), .in_valid(gated_cmd_fire && vector_op), .in_ready(fp16_ready),
    .in_data(vec_unit_out), .out_valid(fp16_valid), .out_ready(1'b1), .out_data(fp16_out)
  );
  tvla_action_post #(.ACTION_DIM(7), .DW(16)) u_action (
    .clk(clk), .rst_n(rst_n), .in_valid(gated_cmd_fire && action_op), .in_ready(action_ready),
    .in_action(action_data), .step_index(desc_data[39:32]), .pos_min(16'h8000), .pos_max(16'h7fff),
    .out_valid(action_valid_i), .out_ready(action_out_ready), .robot_target(action_target),
    .robot_step(action_step), .robot_gripper(action_gripper)
  );
  assign vector_ready = vec_unit_ready;
  assign vector_out_valid = vec_unit_valid | layout_valid | embed_valid;
  always_comb begin
    if (vec_unit_valid) vector_out = vec_unit_out;
    else if (layout_valid) vector_out = layout_out;
    else vector_out = embed_out;
  end
  // Fold every wide sideband into a registered observation word.  This is not
  // a functional result path; it is an activity anchor so synthesis keeps the
  // complete 128-bit CTX, 768-bit WRAM and auxiliary datapaths instead of
  // trimming their unused upper bits in the compact board wrapper.
  logic [31:0] observe_aux_r;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) observe_aux_r <= '0;
    else observe_aux_r <= (ctx_store ? {31'd0, ^ctx_rdata} : 32'd0)
      ^ (wram_store ? {31'd0, ^wram_rdata} : 32'd0)
      ^ (vector_out_valid ? {31'd0, ^vector_out} : 32'd0)
      ^ (embed_valid ? {31'd0, ^embed_out} : 32'd0)
      ^ (bmm_out_valid ? ({31'd0, ^bmm_a} ^ {31'd0, ^bmm_b}) : 32'd0)
      ^ (conv_out_valid ? {31'd0, ^conv_out} : 32'd0)
      ^ (dma_stream_valid ? {31'd0, ^dma_stream_data} : 32'd0)
      ^ (action_valid_i ? {31'd0, ^action_target} : 32'd0)
      ^ (fp16_valid ? {31'd0, ^fp16_out} : 32'd0);
  end
  // Do not expose uninitialised BRAM contents when no array result has been
  // produced yet.  The valid guard keeps the smoke checksum deterministic
  // while still anchoring every wide result bus after a real output beat.
  assign architecture_observe = base_activity[31:0] ^ observe_aux_r
      ^ (pack2_output_valid ? pack2_snapshot[31:0] : 32'd0)
      ^ (pack2_output_valid ? pack2_output[31:0] : 32'd0)
      ^ {27'b0, pack2_output_valid, bmm_out_valid, conv_out_valid, dma_busy, dma_done};
  assign action_out_valid = action_valid_i;
  assign activity_snapshot = base_activity;
  assign dma_stream_ready = 1'b1;
endmodule
`endif
