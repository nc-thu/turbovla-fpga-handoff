// Camera-ready integration top for the TurboVLA W8A16 tile.
//
// The top has one command stream and two explicit DMA backends.  The runtime
// owns command ordering; the array feed/drain interface remains visible for
// the production 16x48 GEMM schedule, while the small action path is used by
// the compiler-to-RTL smoke and by the control-plane test.
module w8a16_system_top #(
  parameter int K = 8,
  parameter int N = 7,
  parameter int VEC_N = 16,
  parameter int GEMM_ROWS = 16,
  parameter int GEMM_COLS = 48
) (
  input  logic                         clk,
  input  logic                         rst_n,
  input  logic [63:0]                  instr_word,
  input  logic                         instr_valid,
  output logic                         instr_ready,

  input  logic                         state_we,
  input  logic [((K <= 1) ? 1 : $clog2(K))-1:0] state_index,
  input  logic signed [15:0]            state_data,
  input  logic                         weight_we,
  input  logic [((N*K <= 1) ? 1 : $clog2(N*K))-1:0] weight_index,
  input  logic signed [7:0]             weight_data,
  input  logic                         bias_we,
  input  logic [((N <= 1) ? 1 : $clog2(N))-1:0] bias_index,
  input  logic signed [15:0]            bias_data,

  input  logic                         vec_we,
  input  logic [((VEC_N <= 1) ? 1 : $clog2(VEC_N))-1:0] vec_index,
  input  logic signed [15:0]            vec_data,
  input  logic signed [15:0]            vec_aux_data,
  input  logic signed [15:0]            vec_scale_data,

  output logic                         action_valid,
  output logic signed [N*16-1:0]        action_out,
  output logic signed [VEC_N*16-1:0]    vector_out,
  output logic                         vector_valid,
  output logic signed [15:0]            requant_out,
  output logic                         requant_valid,
  output logic                         runtime_busy,
  output logic                         runtime_done,

  // Activation DMA: 256-bit CTX beat.
  input  logic [255:0]                 act_stream_in_data,
  input  logic                         act_stream_in_valid,
  output logic                         act_stream_in_ready,
  output logic [255:0]                 act_stream_out_data,
  output logic                         act_stream_out_valid,
  input  logic                         act_stream_out_ready,
  output logic                         act_mem_req,
  output logic                         act_mem_write,
  output logic [31:0]                  act_mem_addr,
  output logic [255:0]                 act_mem_wdata,
  input  logic [255:0]                 act_mem_rdata,
  input  logic                         act_mem_rvalid,
  output logic                         act_dma_busy,
  output logic                         act_dma_done,

  // Weight DMA: 384-bit WRAM beat.
  input  logic [383:0]                 weight_stream_in_data,
  input  logic                         weight_stream_in_valid,
  output logic                         weight_stream_in_ready,
  output logic [383:0]                 weight_stream_out_data,
  output logic                         weight_stream_out_valid,
  input  logic                         weight_stream_out_ready,
  output logic                         weight_mem_req,
  output logic                         weight_mem_write,
  output logic [31:0]                  weight_mem_addr,
  output logic [383:0]                 weight_mem_wdata,
  input  logic [383:0]                 weight_mem_rdata,
  input  logic                         weight_mem_rvalid,
  output logic                         weight_dma_busy,
  output logic                         weight_dma_done,

  // Production array feed/drain contract.
  input  logic                         gemm_start,
  input  logic                         gemm_clr,
  input  logic                         gemm_feed_vld,
  input  logic                         gemm_feed_pulse,
  input  logic [GEMM_ROWS*16-1:0]      gemm_a_feed,
  input  logic [GEMM_COLS*8-1:0]       gemm_b_feed,
  input  logic [((GEMM_ROWS <= 1) ? 1 : $clog2(GEMM_ROWS))-1:0] gemm_drain_row,
  output logic [GEMM_COLS*40-1:0]      gemm_snap_row,
  output logic                         gemm_busy,
  output logic                         gemm_done
);
  logic act_cmd_valid, act_cmd_write, act_cmd_ready;
  logic [31:0] act_cmd_addr;
  logic [15:0] act_cmd_len;
  logic weight_cmd_valid, weight_cmd_write, weight_cmd_ready;
  logic [31:0] weight_cmd_addr;
  logic [15:0] weight_cmd_len;
  logic [255:0] act_rt_out_data, act_rt_in_data;
  logic act_rt_out_valid, act_rt_out_ready;
  logic act_rt_in_valid, act_rt_in_ready;
  logic [383:0] weight_rt_out_data;
  logic weight_rt_out_valid, weight_rt_out_ready;
  logic [255:0] act_dma_in_data, act_dma_out_data;
  logic act_dma_in_valid, act_dma_in_ready;
  logic act_dma_out_valid, act_dma_out_ready;
  logic [383:0] weight_dma_out_data;
  logic weight_dma_out_valid, weight_dma_out_ready;
  logic rt_gemm_start;

  w8a16_runtime #(.K(K), .N(N), .VEC_N(VEC_N)) u_runtime (
    .clk(clk), .rst_n(rst_n), .instr_word(instr_word), .instr_valid(instr_valid),
    .instr_ready(instr_ready), .state_we(state_we), .state_index(state_index),
    .state_data(state_data), .weight_we(weight_we), .weight_index(weight_index),
    .weight_data(weight_data), .bias_we(bias_we), .bias_index(bias_index),
    .bias_data(bias_data), .vec_we(vec_we), .vec_index(vec_index),
    .vec_data(vec_data), .vec_aux_data(vec_aux_data), .vec_scale_data(vec_scale_data),
    .action_valid(action_valid), .action_out(action_out), .vector_out(vector_out),
    .vector_valid(vector_valid), .requant_out(requant_out),
    .requant_valid(requant_valid), .busy(runtime_busy), .done(runtime_done),
    .act_cmd_valid(act_cmd_valid), .act_cmd_write(act_cmd_write),
    .act_cmd_addr(act_cmd_addr), .act_cmd_len(act_cmd_len),
    .act_cmd_ready(act_cmd_ready), .act_dma_done(act_dma_done),
    .weight_cmd_valid(weight_cmd_valid), .weight_cmd_write(weight_cmd_write),
    .weight_cmd_addr(weight_cmd_addr), .weight_cmd_len(weight_cmd_len),
    .weight_cmd_ready(weight_cmd_ready), .weight_dma_done(weight_dma_done),
    .act_stream_out_data(act_rt_out_data), .act_stream_out_valid(act_rt_out_valid),
    .act_stream_out_ready(act_rt_out_ready), .act_stream_in_data(act_rt_in_data),
    .act_stream_in_valid(act_rt_in_valid), .act_stream_in_ready(act_rt_in_ready),
    .weight_stream_out_data(weight_rt_out_data), .weight_stream_out_valid(weight_rt_out_valid),
    .weight_stream_out_ready(weight_rt_out_ready),
    .gemm_start_cmd(rt_gemm_start), .gemm_done_cmd(gemm_done)
  );

  // Route a DMA beat to the runtime on LOAD and expose the normal host-side
  // stream when no runtime load is consuming it.  STORE payloads are supplied
  // by the runtime; a raw host stream is used only while the runtime is not
  // presenting a store beat.
  assign act_rt_out_data = act_dma_out_data;
  assign act_rt_out_valid = act_dma_out_valid;
  assign act_dma_out_ready = act_rt_out_ready | act_stream_out_ready;
  assign act_stream_out_data = act_dma_out_data;
  assign act_stream_out_valid = act_dma_out_valid & ~act_rt_out_ready;
  assign act_dma_in_data = act_rt_in_valid ? act_rt_in_data : act_stream_in_data;
  assign act_dma_in_valid = act_rt_in_valid | act_stream_in_valid;
  assign act_rt_in_ready = act_dma_in_ready;
  assign act_stream_in_ready = act_dma_in_ready & ~act_rt_in_valid;
  assign weight_rt_out_data = weight_dma_out_data;
  assign weight_rt_out_valid = weight_dma_out_valid;
  assign weight_dma_out_ready = weight_rt_out_ready | weight_stream_out_ready;
  assign weight_stream_out_data = weight_dma_out_data;
  assign weight_stream_out_valid = weight_dma_out_valid & ~weight_rt_out_ready;

  w8a16_dma #(.DATA_W(256), .ADDR_W(32)) u_act_dma (
    .clk(clk), .rst_n(rst_n), .cmd_valid(act_cmd_valid), .cmd_write(act_cmd_write),
    .cmd_addr(act_cmd_addr), .cmd_len(act_cmd_len), .cmd_ready(act_cmd_ready),
    .stream_in_data(act_dma_in_data), .stream_in_valid(act_dma_in_valid),
    .stream_in_ready(act_dma_in_ready), .stream_out_data(act_dma_out_data),
    .stream_out_valid(act_dma_out_valid), .stream_out_ready(act_dma_out_ready),
    .mem_req(act_mem_req), .mem_write(act_mem_write), .mem_addr(act_mem_addr),
    .mem_wdata(act_mem_wdata), .mem_rdata(act_mem_rdata), .mem_rvalid(act_mem_rvalid),
    .busy(act_dma_busy), .done(act_dma_done)
  );

  w8a16_dma #(.DATA_W(384), .ADDR_W(32)) u_weight_dma (
    .clk(clk), .rst_n(rst_n), .cmd_valid(weight_cmd_valid), .cmd_write(weight_cmd_write),
    .cmd_addr(weight_cmd_addr), .cmd_len(weight_cmd_len), .cmd_ready(weight_cmd_ready),
    .stream_in_data(weight_stream_in_data), .stream_in_valid(weight_stream_in_valid),
    .stream_in_ready(weight_stream_in_ready), .stream_out_data(weight_dma_out_data),
    .stream_out_valid(weight_dma_out_valid), .stream_out_ready(weight_dma_out_ready),
    .mem_req(weight_mem_req), .mem_write(weight_mem_write), .mem_addr(weight_mem_addr),
    .mem_wdata(weight_mem_wdata), .mem_rdata(weight_mem_rdata),
    .mem_rvalid(weight_mem_rvalid), .busy(weight_dma_busy), .done(weight_dma_done)
  );

  w8a16_gemm #(.ROWS(GEMM_ROWS), .PCOLS(GEMM_COLS), .ACC_W(40)) u_gemm (
    .clk(clk), .rst_n(rst_n), .start(gemm_start | rt_gemm_start), .clr(gemm_clr),
    .feed_vld(gemm_feed_vld), .feed_pulse(gemm_feed_pulse),
    .a_feed(gemm_a_feed), .b_feed(gemm_b_feed), .drain_row(gemm_drain_row),
    .snap_row(gemm_snap_row), .busy(gemm_busy), .done(gemm_done)
  );
endmodule
