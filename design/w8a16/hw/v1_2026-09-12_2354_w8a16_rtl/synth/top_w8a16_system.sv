// Synthesis-only integration shell for the TurboVLA W8A16 command path.
// It exposes the handshakes of runtime, both DMA widths, vector operations,
// and scalar requantization so Vivado elaborates the complete unit set in one
// top.  It is not the final board-level AXI/DDR wrapper.
module w8a16_system_top #(
  parameter int K = 8,
  parameter int N = 7,
  parameter int VEC_N = 16
) (
  input  logic                         clk,
  input  logic                         rst_n,
  input  logic [63:0]                  instr_word,
  input  logic                         instr_valid,
  output logic                         instr_ready,
  input  logic                         state_we,
  input  logic [$clog2(K)-1:0]         state_index,
  input  logic signed [15:0]           state_data,
  input  logic                         weight_we,
  input  logic [$clog2(N*K)-1:0]       weight_index,
  input  logic signed [7:0]            weight_data,
  input  logic                         bias_we,
  input  logic [$clog2(N)-1:0]         bias_index,
  input  logic signed [15:0]           bias_data,
  output logic                         action_valid,
  output logic signed [N*16-1:0]       action_out,
  output logic                         runtime_busy,
  output logic                         runtime_done,

  input  logic                         act_cmd_valid,
  input  logic                         act_cmd_write,
  input  logic [31:0]                  act_cmd_addr,
  input  logic [15:0]                  act_cmd_len,
  output logic                         act_cmd_ready,
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

  input  logic                         w_cmd_valid,
  input  logic                         w_cmd_write,
  input  logic [31:0]                  w_cmd_addr,
  input  logic [15:0]                  w_cmd_len,
  output logic                         w_cmd_ready,
  input  logic [383:0]                 w_stream_in_data,
  input  logic                         w_stream_in_valid,
  output logic                         w_stream_in_ready,
  output logic [383:0]                 w_stream_out_data,
  output logic                         w_stream_out_valid,
  input  logic                         w_stream_out_ready,
  output logic                         w_mem_req,
  output logic                         w_mem_write,
  output logic [31:0]                  w_mem_addr,
  output logic [383:0]                 w_mem_wdata,
  input logic [383:0]                  w_mem_rdata,
  input logic                         w_mem_rvalid,
  output logic                         w_dma_busy,
  output logic                         w_dma_done,

  input  logic                         vec_start,
  input  logic [3:0]                   vec_op,
  input  logic signed [VEC_N*16-1:0]   vec_x,
  input  logic signed [VEC_N*16-1:0]   vec_aux,
  input  logic signed [15:0]           vec_scale,
  output logic signed [VEC_N*16-1:0]   vec_y,
  output logic                         vec_valid,
  output logic                         vec_done,

  input  logic                         rq_start,
  input  logic signed [39:0]           rq_x,
  input  logic signed [15:0]           rq_multiplier,
  input  logic [7:0]                   rq_shift,
  output logic signed [15:0]           rq_y,
  output logic                         rq_valid
);
  w8a16_runtime #(.K(K), .N(N)) u_runtime (
    .clk(clk), .rst_n(rst_n), .instr_word(instr_word), .instr_valid(instr_valid),
    .instr_ready(instr_ready), .state_we(state_we), .state_index(state_index),
    .state_data(state_data), .weight_we(weight_we), .weight_index(weight_index),
    .weight_data(weight_data), .bias_we(bias_we), .bias_index(bias_index),
    .bias_data(bias_data), .action_valid(action_valid), .action_out(action_out),
    .busy(runtime_busy), .done(runtime_done)
  );

  w8a16_dma #(.DATA_W(256), .ADDR_W(32)) u_act_dma (
    .clk(clk), .rst_n(rst_n), .cmd_valid(act_cmd_valid), .cmd_write(act_cmd_write),
    .cmd_addr(act_cmd_addr), .cmd_len(act_cmd_len), .cmd_ready(act_cmd_ready),
    .stream_in_data(act_stream_in_data), .stream_in_valid(act_stream_in_valid),
    .stream_in_ready(act_stream_in_ready), .stream_out_data(act_stream_out_data),
    .stream_out_valid(act_stream_out_valid), .stream_out_ready(act_stream_out_ready),
    .mem_req(act_mem_req), .mem_write(act_mem_write), .mem_addr(act_mem_addr),
    .mem_wdata(act_mem_wdata), .mem_rdata(act_mem_rdata), .mem_rvalid(act_mem_rvalid),
    .busy(act_dma_busy), .done(act_dma_done)
  );

  w8a16_dma #(.DATA_W(384), .ADDR_W(32)) u_weight_dma (
    .clk(clk), .rst_n(rst_n), .cmd_valid(w_cmd_valid), .cmd_write(w_cmd_write),
    .cmd_addr(w_cmd_addr), .cmd_len(w_cmd_len), .cmd_ready(w_cmd_ready),
    .stream_in_data(w_stream_in_data), .stream_in_valid(w_stream_in_valid),
    .stream_in_ready(w_stream_in_ready), .stream_out_data(w_stream_out_data),
    .stream_out_valid(w_stream_out_valid), .stream_out_ready(w_stream_out_ready),
    .mem_req(w_mem_req), .mem_write(w_mem_write), .mem_addr(w_mem_addr),
    .mem_wdata(w_mem_wdata), .mem_rdata(w_mem_rdata), .mem_rvalid(w_mem_rvalid),
    .busy(w_dma_busy), .done(w_dma_done)
  );

  w8a16_vector_ops #(.N(VEC_N)) u_vector_ops (
    .clk(clk), .rst_n(rst_n), .start(vec_start), .op(vec_op), .x(vec_x),
    .aux(vec_aux), .scale(vec_scale), .y(vec_y), .out_valid(vec_valid), .done(vec_done)
  );

  w8a16_requant u_requant (
    .clk(clk), .rst_n(rst_n), .in_vld(rq_start), .x(rq_x),
    .multiplier(rq_multiplier), .shift(rq_shift), .out_vld(rq_valid), .y(rq_y)
  );
endmodule
