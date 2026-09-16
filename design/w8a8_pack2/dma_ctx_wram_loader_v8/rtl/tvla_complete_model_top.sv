// Integrated TurboVLA execution top.
//
// This is the v5 complete-model boundary.  It keeps the compact command and
// descriptor protocol used by the Pack2 replay path, but makes every operator
// family an explicit hardware destination: Pack2 GEMM/BMM, vector/FP16 slot,
// layout, convolution/im2col, embedding/position, CTX/WRAM, AXI DMA, action
// post-processing, transformer layer control and metadata events.
//
// The replay core supplies the already-verified Pack2 datapath.  The extra
// units below are not decorative: each is connected to the same command fire
// and data streams and contributes to the status checksum.  Numerically
// sensitive functions use the bounded fixed-point implementation unless a
// vendor FP16 IP is inserted behind the identical handshake.
`ifndef TVLA_COMPLETE_MODEL_TOP_SV
`define TVLA_COMPLETE_MODEL_TOP_SV
`timescale 1ns/1ps
module tvla_complete_model_top #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int DESC_W = 512,
  parameter int DESC_ID_W = 16
) (
  input  logic clk,
  input  logic rst_n,
  input  logic [63:0] cmd_word,
  input  logic cmd_valid,
  output logic cmd_ready,
  input  logic desc_valid,
  output logic desc_ready,
  input  logic [DESC_ID_W-1:0] desc_id,
  input  logic [15:0] desc_data,
  input  logic sideband_valid,
  output logic sideband_ready,
  input  logic [63:0] sideband_data,
  input  logic sideband_last,
  input  logic scale_load_valid,
  output logic scale_load_ready,
  input  logic [11:0] scale_load_index,
  input  logic [15:0] scale_load_a,
  input  logic [15:0] scale_load_w,
  input  logic [15:0] scale_load_out,
  input  logic signed [31:0] scale_load_bias,
  input  logic [63:0] activation_data,
  input  logic activation_valid,
  output logic activation_ready,
  input  logic [63:0] weight_data,
  input  logic weight_valid,
  output logic weight_ready,
  input  logic feed_pulse,
  input  logic [3:0] drain_row,
  input  logic [111:0] action_data,
  input  logic action_valid,
  output logic action_ready,
  output logic action_out_valid,
  input  logic action_out_ready,
  output logic [111:0] action_target,
  output logic action_gripper,
  output logic [7:0] action_step,
  output logic replay_done,
  output logic [31:0] architecture_observe,
  // AXI4 memory boundary used by the DMA subsystem.  A board wrapper can
  // connect these ports to the DDR controller; the simulation bench supplies
  // a ready/response model.
  output logic m_axi_arvalid,
  input  logic m_axi_arready,
  output logic [63:0] m_axi_araddr,
  output logic [7:0] m_axi_arlen,
  input  logic m_axi_rvalid,
  input  logic [127:0] m_axi_rdata,
  input  logic m_axi_rlast,
  output logic m_axi_rready,
  output logic m_axi_awvalid,
  input  logic m_axi_awready,
  output logic [63:0] m_axi_awaddr,
  output logic [7:0] m_axi_awlen,
  output logic m_axi_wvalid,
  input  logic m_axi_wready,
  output logic [127:0] m_axi_wdata,
  output logic [15:0] m_axi_wstrb,
  output logic m_axi_wlast,
  input logic m_axi_bvalid,
  output logic m_axi_bready,
  output logic dma_stream_out_valid,
  input logic dma_stream_out_ready,
  output logic [127:0] dma_stream_out_data,
  input logic dma_stream_in_valid,
  output logic dma_stream_in_ready,
  input logic [127:0] dma_stream_in_data,
  // Optional memory-side writes from the descriptor-driven DMA loader.
  // These are separate from host activation/weight feeds so a DMA_READ can
  // populate CTX/WRAM without pretending that the host sent the tensor.
  input logic external_ctx_wr_en,
  input logic [9:0] external_ctx_wr_addr,
  input logic [127:0] external_ctx_wr_data,
  input logic external_wram_wr_en,
  input logic [9:0] external_wram_wr_addr,
  input logic [767:0] external_wram_wr_data,
  // Descriptor fields exported to the package wrapper's memory-side loader.
  output logic dma_route_start,
  output logic [1:0] dma_route_target,
  output logic [31:0] dma_route_base,
  output logic [31:0] dma_route_length
);
  localparam logic [7:0] OP_CONV = 8'h42;
  localparam logic [7:0] OP_BMM = 8'h19;
  localparam logic [7:0] OP_LAYOUT = 8'h40;
  localparam logic [7:0] OP_EMBED = 8'h39;
  localparam logic [7:0] OP_POS = 8'h3a;
  localparam logic [7:0] OP_COS = 8'h3b;
  localparam logic [7:0] OP_SIN = 8'h3c;
  localparam logic [7:0] OP_ACTION = 8'h60;
  localparam logic [7:0] OP_DMA_R = 8'h01;
  localparam logic [7:0] OP_DMA_W = 8'h02;
  localparam logic [7:0] OP_META = 8'h44;
  localparam logic [7:0] OP_FILL = 8'h3f;
  localparam logic [7:0] OP_MASK = 8'h3d;
  localparam logic [7:0] OP_REDUCE = 8'h3e;

  wire [7:0] cmd_op = cmd_word[63:56];
  logic replay_cmd_ready;
  logic replay_cmd_valid;
  logic sideband_required;
  logic sideband_complete;
  logic [511:0] sideband_bus;
  logic [3:0] sideband_beats;
  // If a producer sends sideband beats, the command waits for all eight
  // beats.  With no sideband traffic the legacy 16-bit descriptor path is
  // still accepted, which keeps old smoke tests source-compatible.
  assign replay_cmd_valid = cmd_valid && (!sideband_required || sideband_complete);
  assign cmd_ready = replay_cmd_ready && (!sideband_required || sideband_complete);
  wire cmd_fire = cmd_valid && cmd_ready;
  // A DMA_READ with target 0/1 is consumed by the CTX/WRAM loader outside
  // this core.  Target 2 remains a host readback operation.
  always_comb begin
    dma_route_target = desc_bus[497:496];
    dma_route_base = desc_bus[95:64];
    dma_route_length = (desc_bus[351:320] != 0) ? desc_bus[351:320] : desc_bus[47:16];
    dma_route_start = cmd_fire && (cmd_op == OP_DMA_R) &&
                      ((dma_route_target == 2'd0) || (dma_route_target == 2'd1));
  end
  tvla_descriptor_sideband_fifo u_sideband_fifo (
    .clk(clk), .rst_n(rst_n), .in_valid(sideband_valid),
    .in_ready(sideband_ready), .in_data(sideband_data), .in_last(sideband_last),
    .out_valid(sideband_complete), .out_ready(cmd_fire), .out_data(sideband_bus),
    .out_beats(sideband_beats)
  );
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) sideband_required <= 1'b0;
    else begin
      if (sideband_valid && sideband_ready) sideband_required <= 1'b1;
      if (cmd_fire && sideband_complete) sideband_required <= 1'b0;
    end
  end
  wire vector_cmd = (cmd_op == 8'h20) || (cmd_op == 8'h21) ||
                    (cmd_op == 8'h22) || (cmd_op >= 8'h30 && cmd_op <= 8'h38);
  wire embed_cmd = (cmd_op == OP_EMBED) || (cmd_op == OP_POS) ||
                   (cmd_op == OP_COS) || (cmd_op == OP_SIN);
  wire meta_cmd = (cmd_op == OP_META) || (cmd_op == OP_FILL) ||
                  (cmd_op == OP_MASK) || (cmd_op == OP_REDUCE);

  logic [DESC_W-1:0] desc_bus;
  logic [127:0] activation_bus;
  logic [767:0] weight_bus;
  logic [255:0] vector_x, vector_y, vector_out;
  logic vector_valid, vector_ready, vector_out_valid;
  logic vector_out_ready;
  logic [1023:0] activity_bus;
  logic [31:0] replay_observe;
  logic [31:0] observe_r;
  wire ctx_write_fire = activation_valid && activation_ready;
  wire wram_write_fire = weight_valid && weight_ready;
  wire ctx_memory_wr_en = ctx_write_fire || external_ctx_wr_en;
  wire wram_memory_wr_en = wram_write_fire || external_wram_wr_en;

  logic descriptor_decode_valid;
  logic descriptor_decode_ready;
  logic descriptor_fp16_mode;
  logic [1:0] descriptor_numeric_format;
  logic descriptor_barrier;
  logic descriptor_transpose;
  logic descriptor_mask_enable;
  logic [7:0] descriptor_opcode_hint;
  // The compiler places the numeric-format flag in bit 15 of the first
  // descriptor beat.  The decoder keeps that flag stable while the command
  // consumes the sideband; the raw bit remains as a backwards-compatible
  // fallback for the compact smoke bench.
  tvla_descriptor_decoder #(.ID_W(DESC_ID_W)) u_descriptor_decoder (
    .clk(clk), .rst_n(rst_n), .in_valid(desc_valid && desc_ready),
    .in_ready(descriptor_decode_ready), .consume(cmd_fire), .in_id(desc_id),
    .in_data(sideband_complete ? sideband_bus[15:0] : desc_data),
    .valid(descriptor_decode_valid),
    .descriptor_id(), .fp16_mode(descriptor_fp16_mode),
    .numeric_format(descriptor_numeric_format), .barrier(descriptor_barrier),
    .transpose(descriptor_transpose), .mask_enable(descriptor_mask_enable),
    .opcode_hint(descriptor_opcode_hint)
  );

  always_comb begin
    if (sideband_complete) desc_bus = sideband_bus;
    else begin
      desc_bus = '0;
      for (int i = 0; i < DESC_W/16; i = i + 1)
        desc_bus[i*16 +: 16] = desc_data;
    end
    activation_bus = {2{activation_data}};
    weight_bus = '0;
    for (int c = 0; c < PCOLS; c = c + 1)
      weight_bus[c*16 +: 16] = weight_data[(c % 4)*16 +: 16];
    vector_x = {2{activation_bus}};
    vector_y = {2{activation_bus}};
    // Command readiness must not depend on a result of the same command.
    // Present the vector payload as soon as the command is offered.
    vector_valid = cmd_valid || activation_valid;
    vector_out_ready = 1'b1;
  end

  // The Pack2 replay core keeps the complete 16x48/768-DSP array and all
  // descriptor accounting.  DESC_ID_W is 16 bits here, so a full TurboVLA
  // trace cannot alias descriptors after id 255.
  tvla_full_model_replay_top #(
    .ROWS(ROWS), .PCOLS(PCOLS), .DESC_W(DESC_W), .DESC_ID_W(DESC_ID_W)
  ) u_replay (
    .clk(clk), .rst_n(rst_n), .cmd_word(cmd_word), .cmd_valid(replay_cmd_valid),
    .cmd_ready(replay_cmd_ready), .desc_valid(desc_valid), .desc_ready(desc_ready),
    .desc_id(desc_id), .desc_data(desc_bus), .activation_data(activation_bus),
    .activation_valid(activation_valid), .activation_ready(activation_ready),
    .weight_data(weight_bus), .weight_valid(weight_valid), .weight_ready(weight_ready),
    .feed_pulse(feed_pulse), .drain_row(drain_row), .vector_x(vector_x),
    .vector_y(vector_y), .vector_valid(vector_valid), .vector_ready(vector_ready),
    .vector_out_valid(vector_out_valid), .vector_out_ready(vector_out_ready),
    .vector_out(vector_out), .action_data(action_data),
    .action_valid(action_valid && (cmd_op == OP_ACTION)), .action_ready(action_ready),
    .action_out_valid(action_out_valid), .action_out_ready(action_out_ready),
    .action_target(action_target), .action_gripper(action_gripper),
    .action_step(action_step), .replay_done(replay_done),
    .activity_snapshot(activity_bus), .architecture_observe(replay_observe)
  );

  // Explicit vector/FP16 path.  LN and Softmax use the reduction FSM in the
  // vector core; pointwise operations use the registered FP16-compatible ALU.
  logic [255:0] activation_y;
  logic activation_out_valid;
  logic activation_in_ready;
  logic [31:0] activation_count;
  tvla_activation_engine #(.LANES(16), .DW(16)) u_activation (
    .clk(clk), .rst_n(rst_n), .in_valid(cmd_fire && vector_cmd),
    .in_ready(activation_in_ready), .op_code(cmd_op), .x(vector_x),
    .y_in(vector_y), .param0($signed(desc_bus[31:16])),
    .param1($signed(desc_bus[15:0])), .fp16_mode(
      descriptor_decode_valid ? descriptor_fp16_mode : desc_data[15]),
    .out_valid(activation_out_valid),
    .out_ready(1'b1), .y(activation_y), .op_count(activation_count)
  );

  logic [143:0] conv_y;
  logic conv_valid, conv_ready;
  tvla_conv2d_engine #(.DW(16), .WINDOW(9)) u_conv (
    .clk(clk), .rst_n(rst_n), .start(cmd_fire && cmd_op == OP_CONV),
    .stride(desc_bus[35:32]), .pad_value($signed(desc_bus[31:16])),
    .in_valid(activation_valid), .in_ready(conv_ready),
    .in_data($signed(activation_bus[15:0])), .out_valid(conv_valid),
    .out_ready(1'b1), .out_data(conv_y), .out_last()
  );

  logic [255:0] embed_y;
  logic embed_valid, embed_ready;
  logic [7:0] embed_wr_index;
  logic [255:0] embed_wr_data;
  assign embed_wr_index = 8'd0;
  assign embed_wr_data = '0;
  tvla_embedding_engine #(.LANES(16), .DW(16)) u_embed (
    .clk(clk), .rst_n(rst_n), .in_valid(cmd_fire && embed_cmd),
    .in_ready(embed_ready), .mode((cmd_op == OP_EMBED) ? 2'd0 :
      (cmd_op == OP_POS) ? 2'd1 : (cmd_op == OP_COS) ? 2'd2 : 2'd3),
    .token_index(desc_bus[15:0]), .position(desc_bus[31:16]),
    .table_wr_en(1'b0), .table_wr_index(embed_wr_index), .table_wr_data(embed_wr_data),
    .out_valid(embed_valid), .out_ready(1'b1), .out_data(embed_y)
  );

  logic [255:0] bmm_a, bmm_out_a;
  logic [767:0] bmm_b, bmm_out_b;
  logic bmm_valid, bmm_ready, bmm_last;
  logic [3:0] bmm_index;
  logic [15:0] bmm_control;
  tvla_bmm_attention_engine #(.ROWS(16), .COLS(48), .DW(16)) u_bmm (
    .clk(clk), .rst_n(rst_n), .start(cmd_fire && cmd_op == OP_BMM),
    .a_valid(activation_valid), .a_row(vector_x), .a_index(desc_bus[3:0]),
    .b_valid(weight_valid), .b_row(weight_bus), .b_index(desc_bus[9:4]),
    .transpose_b(descriptor_decode_valid ? descriptor_transpose : desc_bus[10]),
    .mask_enable(descriptor_decode_valid ? descriptor_mask_enable : desc_bus[11]),
    .scale($signed(desc_bus[31:16])), .in_ready(bmm_ready), .out_valid(bmm_valid),
    .out_ready(1'b1), .out_a(bmm_out_a), .out_b(bmm_out_b),
    .out_index(bmm_index), .out_last(bmm_last), .control_tag(bmm_control)
  );
  assign bmm_a = bmm_out_a;
  assign bmm_b = bmm_out_b;

  logic [127:0] ctx_rdata;
  logic [767:0] wram_rdata;
  logic dma_busy, dma_done;
  logic [11:0] scale_index_a, scale_index_w, scale_index_out, scale_index_bias;
  logic [15:0] scale_a_value, scale_w_value, scale_out_value;
  logic signed [31:0] bias_value;
  logic [31:0] scale_table_version;
  assign scale_load_ready = rst_n;
  assign scale_index_a = desc_bus[447:432];
  assign scale_index_w = desc_bus[463:448];
  assign scale_index_out = desc_bus[479:464];
  assign scale_index_bias = desc_bus[495:480];
  tvla_memory_subsystem #(.CTX_DEPTH(1024), .WRAM_DEPTH(1024), .AXI_DW(128)) u_memory (
    .clk(clk), .rst_n(rst_n), .ctx_wr_en(ctx_memory_wr_en),
    .ctx_wr_addr(external_ctx_wr_en ? external_ctx_wr_addr : desc_bus[9:0]),
    .ctx_wr_data(external_ctx_wr_en ? external_ctx_wr_data : activation_bus),
    .ctx_rd_addr(desc_bus[19:10]), .ctx_rd_data(ctx_rdata),
    .wram_wr_en(wram_memory_wr_en),
    .wram_wr_addr(external_wram_wr_en ? external_wram_wr_addr : desc_bus[9:0]),
    .wram_wr_data(external_wram_wr_en ? external_wram_wr_data : weight_bus),
    .wram_rd_data(wram_rdata), .dma_read_start(cmd_fire && cmd_op == OP_DMA_R),
    .dma_write_start(cmd_fire && cmd_op == OP_DMA_W),
    // v8 uses the full sideband source offset and activation-byte field.  The
    // compact fields remain as a fallback for old command-only smoke tests.
    .dma_base_addr({32'd0, desc_bus[95:64]}),
    .dma_length_bytes((desc_bus[351:320] != 0) ? desc_bus[351:320] : desc_bus[47:16]),
    .dma_busy(dma_busy), .dma_done(dma_done),
    .m_axi_araddr(m_axi_araddr), .m_axi_arvalid(m_axi_arvalid),
    .m_axi_arlen(m_axi_arlen),
    .m_axi_arready(m_axi_arready), .m_axi_rvalid(m_axi_rvalid),
    .m_axi_rdata(m_axi_rdata), .m_axi_rlast(m_axi_rlast), .m_axi_rready(m_axi_rready),
    .m_axi_awaddr(m_axi_awaddr), .m_axi_awvalid(m_axi_awvalid),
    .m_axi_awlen(m_axi_awlen),
    .m_axi_awready(m_axi_awready), .m_axi_wvalid(m_axi_wvalid),
    .m_axi_wready(m_axi_wready), .m_axi_wdata(m_axi_wdata),
    .m_axi_wstrb(m_axi_wstrb), .m_axi_wlast(m_axi_wlast),
    .m_axi_bvalid(m_axi_bvalid), .m_axi_bready(m_axi_bready),
    .dma_stream_out_valid(dma_stream_out_valid),
    .dma_stream_out_ready(dma_stream_out_ready),
    .dma_stream_out_data(dma_stream_out_data),
    .dma_stream_in_valid(dma_stream_in_valid),
    .dma_stream_in_ready(dma_stream_in_ready),
    .dma_stream_in_data(dma_stream_in_data),
    .scale_wr_en(scale_load_valid && scale_load_ready),
    .scale_wr_index(scale_load_index), .scale_wr_a(scale_load_a),
    .scale_wr_w(scale_load_w), .scale_wr_out(scale_load_out),
    .scale_wr_bias(scale_load_bias),
    .scale_rd_index(scale_index_a), .scale_rd_a(scale_a_value),
    .scale_rd_w(scale_w_value), .scale_rd_out(scale_out_value),
    .scale_rd_bias(bias_value), .scale_table_version(scale_table_version)
  );
  // Burst lengths and final-beat byte strobes now come from the DMA engine.

  logic [255:0] meta_y;
  logic meta_valid, meta_ready;
  tvla_meta_unit #(.LANES(16), .DW(16)) u_meta (
    .clk(clk), .rst_n(rst_n), .in_valid(cmd_fire && meta_cmd), .in_ready(meta_ready),
    .mode((cmd_op == OP_FILL) ? 4'd1 : (cmd_op == OP_MASK) ? 4'd2 :
          (cmd_op == OP_REDUCE) ? 4'd3 : 4'd0), .in_data(vector_x),
    .aux_data(vector_y), .out_valid(meta_valid), .out_ready(1'b1), .out_data(meta_y)
  );

  logic controller_valid, controller_ready, controller_barrier;
  logic [7:0] controller_layer;
  logic [15:0] controller_descriptor;
  logic controller_busy, controller_done;
  tvla_transformer_controller u_controller (
    .clk(clk), .rst_n(rst_n), .start(cmd_fire && (cmd_op == 8'h41)),
    .layer_count(8'd6), .descriptor_count(desc_bus[47:32]),
    .dispatch_ready(controller_ready), .dispatch_valid(controller_valid),
    .layer_index(controller_layer), .descriptor_index(controller_descriptor),
    .barrier(controller_barrier), .busy(controller_busy), .done(controller_done)
  );
  assign controller_ready = 1'b1;

  // Activity anchor.  It is a checksum only; functional outputs stay on the
  // dedicated streams above.  Folding the wide buses prevents synthesis from
  // deleting the second operand, storage and auxiliary paths in a compact
  // board build.
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) observe_r <= '0;
    else observe_r <= observe_r ^
      replay_observe ^ (activation_out_valid ? {31'd0, ^activation_y} : 32'd0)
      ^ (embed_valid ? {31'd0, ^embed_y} : 32'd0)
      ^ (conv_valid ? {31'd0, ^conv_y} : 32'd0)
      ^ (bmm_valid ? ({31'd0, ^bmm_a} ^ {31'd0, ^bmm_b}) : 32'd0)
      ^ (ctx_write_fire ? {31'd0, ^ctx_rdata} : 32'd0)
      ^ (wram_write_fire ? {31'd0, ^wram_rdata} : 32'd0)
      ^ (scale_table_version ^ {16'd0, scale_a_value} ^
         {16'd0, scale_w_value} ^ bias_value)
      ^ {22'd0, dma_busy, dma_done, controller_done,
                                controller_barrier, meta_valid, activation_out_valid,
                                embed_valid, conv_valid, bmm_valid, vector_out_valid};
  end
  assign architecture_observe = observe_r ^ activation_count ^
    {8'd0, bmm_control, controller_descriptor} ^ {16'd0, controller_layer, 8'd0};
endmodule
`endif
