`timescale 1ns/1ps
// Runtime integration smoke.  It checks the real command handshakes:
// action GEMM waits for the pipelined post-processing path, vector operations
// publish a registered result, and DMA commands wait for backend completion.
// It is a tile-level compiler-to-RTL check, not a full TurboVLA rollout.
module tb_w8a16_runtime;
  localparam int K = 8, N = 7, VEC_N = 16;
  localparam int KIW = (K <= 1) ? 1 : $clog2(K);
  localparam int NIW = (N <= 1) ? 1 : $clog2(N);
  localparam int WIW = (N*K <= 1) ? 1 : $clog2(N*K);
  localparam int VIW = (VEC_N <= 1) ? 1 : $clog2(VEC_N);

  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 0;
  logic [63:0] instr_word = 0;
  logic instr_valid = 0, instr_ready;
  logic state_we = 0, weight_we = 0, bias_we = 0;
  logic [KIW-1:0] state_index = '0;
  logic [WIW-1:0] weight_index = '0;
  logic [NIW-1:0] bias_index = '0;
  logic signed [15:0] state_data = 0, bias_data = 0;
  logic signed [7:0] weight_data = 0;
  logic vec_we = 0;
  logic [VIW-1:0] vec_index = '0;
  logic signed [15:0] vec_data = 0, vec_aux_data = 0, vec_scale_data = 1;
  logic action_valid;
  logic signed [N*16-1:0] action_out;
  logic signed [VEC_N*16-1:0] vector_out;
  logic vector_valid;
  logic signed [15:0] requant_out;
  logic requant_valid;
  logic busy, done;

  logic act_cmd_valid, act_cmd_write, act_cmd_ready = 1'b1;
  logic [31:0] act_cmd_addr;
  logic [15:0] act_cmd_len;
  logic act_dma_done = 0;
  logic weight_cmd_valid, weight_cmd_write, weight_cmd_ready = 1'b1;
  logic [31:0] weight_cmd_addr;
  logic [15:0] weight_cmd_len;
  logic weight_dma_done = 0;
  logic [255:0] act_stream_out_data = '0;
  logic act_stream_out_valid, act_stream_out_ready;
  logic [255:0] act_stream_in_data;
  logic act_stream_in_valid, act_stream_in_ready = 1'b1;
  logic [383:0] weight_stream_out_data = '0;
  logic weight_stream_out_valid, weight_stream_out_ready;
  logic gemm_start_cmd;
  logic gemm_done_cmd = 0;

  w8a16_runtime #(.K(K), .N(N), .VEC_N(VEC_N)) dut (.*);

  logic act_pending = 0, weight_pending = 0;
  logic store_seen = 0, weight_seen = 0;
  logic [255:0] store_payload = '0;

  // The testbench models the payload side of the DMA contract.  A read is
  // presented until the runtime accepts it; a write is counted only after
  // the runtime's held beat is accepted.
  always_comb begin
    act_stream_out_valid = act_pending && !act_cmd_write;
    weight_stream_out_valid = weight_pending;
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      act_pending <= 1'b0;
      weight_pending <= 1'b0;
      act_dma_done <= 1'b0;
      weight_dma_done <= 1'b0;
    end else begin
      act_dma_done <= 1'b0;
      weight_dma_done <= 1'b0;
      if (act_cmd_valid && act_cmd_ready) act_pending <= 1'b1;
      if (weight_cmd_valid && weight_cmd_ready) weight_pending <= 1'b1;
      if (act_pending) begin
        if (act_cmd_write) begin
          if (act_stream_in_valid && act_stream_in_ready) begin
            act_dma_done <= 1'b1;
            act_pending <= 1'b0;
          end
        end else if (act_stream_out_valid && act_stream_out_ready) begin
          act_dma_done <= 1'b1;
          act_pending <= 1'b0;
        end
      end
      if (weight_pending && weight_stream_out_valid && weight_stream_out_ready) begin
        weight_dma_done <= 1'b1;
        weight_pending <= 1'b0;
        weight_seen <= 1'b1;
      end
      if (act_stream_in_valid && act_stream_in_ready) begin
        store_seen <= 1'b1;
        store_payload <= act_stream_in_data;
      end
    end
  end

  function automatic [63:0] word(input [7:0] code, input [7:0] dst,
                                  input [7:0] src0, input [7:0] src1,
                                  input [15:0] length);
    word = {code, 8'h03, dst, src0, src1, length, 8'h00};
  endfunction

  task automatic write_state(input integer idx, input integer signed value);
    begin
      @(negedge clk); state_index = idx; state_data = value; state_we = 1'b1;
      @(negedge clk); state_we = 1'b0;
    end
  endtask
  task automatic write_weight(input integer idx, input integer signed value);
    begin
      @(negedge clk); weight_index = idx; weight_data = value; weight_we = 1'b1;
      @(negedge clk); weight_we = 1'b0;
    end
  endtask
  task automatic write_bias(input integer idx, input integer signed value);
    begin
      @(negedge clk); bias_index = idx; bias_data = value; bias_we = 1'b1;
      @(negedge clk); bias_we = 1'b0;
    end
  endtask
  task automatic write_vec(input integer idx, input integer signed value,
                           input integer signed aux_value);
    begin
      @(negedge clk); vec_index = idx; vec_data = value; vec_aux_data = aux_value;
      vec_scale_data = 16'sd1; vec_we = 1'b1;
      @(negedge clk); vec_we = 1'b0;
    end
  endtask
  task automatic send(input [63:0] w);
    begin
      @(negedge clk); while (!instr_ready) @(negedge clk);
      instr_word = w; instr_valid = 1'b1;
      @(negedge clk); instr_valid = 1'b0;
      while (!instr_ready) @(negedge clk);
    end
  endtask

  function automatic integer sat16_i(input integer signed v);
    begin
      if (v > 32767) sat16_i = 32767;
      else if (v < -32768) sat16_i = -32768;
      else sat16_i = v;
    end
  endfunction
  function automatic integer tanh_i(input integer signed v);
    integer signed ax, yi;
    begin
      ax = (v < 0) ? -v : v;
      if (ax >= 24576) yi = 32767;
      else if (ax >= 16384) yi = 24576 + ((ax - 16384) * 8191) / 8192;
      else if (ax >= 8192) yi = 12288 + ((ax - 8192) * 12287) / 8192;
      else yi = (ax * 3) / 2;
      tanh_i = sat16_i((v < 0) ? -yi : yi);
    end
  endfunction

  integer i, j, t;
  integer signed state_v [0:K-1];
  integer signed weight_v [0:N-1][0:K-1];
  integer signed bias_v [0:N-1];
  integer signed expected;
  logic action_seen = 1'b0;
  logic signed [N*16-1:0] action_latched = '0;
  logic vector_seen = 1'b0;
  logic requant_seen = 1'b0;
  logic done_seen = 1'b0;
  always @(negedge clk) begin
    if (action_valid) begin
      action_seen = 1'b1;
      action_latched = action_out;
    end
    if (vector_valid) vector_seen = 1'b1;
    if (requant_valid) requant_seen = 1'b1;
    if (done) done_seen = 1'b1;
  end

  initial begin
    $display("RUNTIME_V2_TRACE start t=%0t", $time);
    repeat (2) @(negedge clk); rst_n = 1'b1;
    for (i = 0; i < K; i = i + 1) begin
      state_v[i] = (i + 1) * 100 * ((i % 2) ? -1 : 1);
      write_state(i, state_v[i]);
    end
    for (j = 0; j < N; j = j + 1) begin
      bias_v[j] = j - 3;
      write_bias(j, bias_v[j]);
      for (i = 0; i < K; i = i + 1) begin
        weight_v[j][i] = ((j + 2*i) % 5) - 2;
        write_weight(j*K+i, weight_v[j][i]);
      end
    end
    for (i = 0; i < VEC_N; i = i + 1)
      if (i < K) act_stream_out_data[i*16 +: 16] = state_v[i];
      else act_stream_out_data[i*16 +: 16] = 16'sd0;
    for (i = 0; i < 48; i = i + 1)
      if (i < N*K) weight_stream_out_data[i*8 +: 8] = weight_v[i/K][i%K];
      else weight_stream_out_data[i*8 +: 8] = 8'sd0;
    for (i = 0; i < VEC_N; i = i + 1) write_vec(i, (i - 8) * 100, i * 10);

    // Memory commands must wait for their backend acknowledgement.
    send(word(8'h01, 0, 0, 0, 1));
    send(word(8'h02, 1, 0, 0, 1));
    send(word(8'h03, 0, 0, 0, 1));
    if (!weight_seen) $fatal(1, "weight payload was not accepted");
    if (!store_seen || $signed(store_payload[15:0]) !== state_v[0])
      $fatal(1, "activation payload was not transferred through runtime");

    send(word(8'h10, 2, 0, 1, 0));
    if (!action_seen) $fatal(1, "runtime action timeout");
    for (j = 0; j < N; j = j + 1) begin
      expected = 0;
      for (i = 0; i < K; i = i + 1) expected = expected + state_v[i] * weight_v[j][i];
      expected = tanh_i(sat16_i(expected + bias_v[j]));
      if ($signed(action_latched[j*16 +: 16]) !== expected)
        $fatal(1, "action mismatch lane=%0d got=%0d exp=%0d", j,
               $signed(action_latched[j*16 +: 16]), expected);
    end

    send(word(8'h32, 0, 0, 0, VEC_N));
    if (!vector_seen) $fatal(1, "vector result was not registered");
    for (i = 0; i < VEC_N; i = i + 1)
      if ($signed(vector_out[i*16 +: 16]) < 0)
        $fatal(1, "relu mismatch lane=%0d", i);

    send(word(8'h35, 0, 0, 0, 1));
    if (!requant_seen) $fatal(1, "requant result was not registered");
    send(word(8'h04, 0, 0, 0, 1));
    send(word(8'h40, 0, 0, 0, 1));
    send(word(8'h41, 0, 0, 0, 1));
    send(word(8'hff, 0, 0, 0, 0));
    @(posedge clk); #1;
    if (!done_seen) $fatal(1, "runtime END timeout");
    $display("TB_W8A16_RUNTIME_V2 PASS action_lanes=%0d dma_handshake=1 vector=1 requant=1", N);
    $finish(0);
  end
endmodule
