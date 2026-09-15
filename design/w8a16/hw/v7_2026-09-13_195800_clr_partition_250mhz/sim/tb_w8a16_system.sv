`timescale 1ns/1ps
// Top-level wiring smoke.  The GEMM array is reduced to 1x1 for simulation;
// the synthesis flow still elaborates the production 16x48 instance.
module tb_w8a16_system;
  // Exercise the same 16x48 production array interface used by the synthesis
  // top.  The action-path command still uses the small K/N smoke dimensions.
  localparam int K = 8, N = 7, VEC_N = 16, GR = 16, GC = 48;
  localparam int KIW = (K <= 1) ? 1 : $clog2(K);
  localparam int WIW = (N*K <= 1) ? 1 : $clog2(N*K);
  localparam int NIW = (N <= 1) ? 1 : $clog2(N);
  localparam int VIW = (VEC_N <= 1) ? 1 : $clog2(VEC_N);
  localparam int GRIW = (GR <= 1) ? 1 : $clog2(GR);

  logic clk = 0; always #5 clk = ~clk;
  logic rst_n = 0;
  logic [63:0] instr_word = 0; logic instr_valid = 0, instr_ready;
  logic state_we = 0, weight_we = 0, bias_we = 0;
  logic [KIW-1:0] state_index = '0; logic signed [15:0] state_data = 0;
  logic [WIW-1:0] weight_index = '0; logic signed [7:0] weight_data = 0;
  logic [NIW-1:0] bias_index = '0; logic signed [15:0] bias_data = 0;
  logic vec_we = 0; logic [VIW-1:0] vec_index = '0;
  logic signed [15:0] vec_data = 0, vec_aux_data = 0, vec_scale_data = 1;
  logic action_valid; logic signed [N*16-1:0] action_out;
  logic signed [VEC_N*16-1:0] vector_out; logic vector_valid;
  logic signed [15:0] requant_out; logic requant_valid;
  logic runtime_busy, runtime_done;
  logic [255:0] act_stream_in_data = '0; logic act_stream_in_valid = 0, act_stream_in_ready;
  logic [255:0] act_stream_out_data; logic act_stream_out_valid; logic act_stream_out_ready = 1;
  logic act_mem_req, act_mem_write; logic [31:0] act_mem_addr; logic [255:0] act_mem_wdata;
  logic [255:0] act_mem_rdata = '0; logic act_mem_rvalid = 0; logic act_dma_busy, act_dma_done;
  logic [383:0] weight_stream_in_data = '0; logic weight_stream_in_valid = 0, weight_stream_in_ready;
  logic [383:0] weight_stream_out_data; logic weight_stream_out_valid; logic weight_stream_out_ready = 1;
  logic weight_mem_req, weight_mem_write; logic [31:0] weight_mem_addr; logic [383:0] weight_mem_wdata;
  logic [383:0] weight_mem_rdata = '0; logic weight_mem_rvalid = 0; logic weight_dma_busy, weight_dma_done;
  logic gemm_start = 0, gemm_clr = 0, gemm_feed_vld = 0, gemm_feed_pulse = 0;
  logic [GR*16-1:0] gemm_a_feed = '0; logic [GC*8-1:0] gemm_b_feed = '0;
  logic [GRIW-1:0] gemm_drain_row = '0; logic [GC*40-1:0] gemm_snap_row;
  logic gemm_busy, gemm_done;

  w8a16_system_top #(.K(K), .N(N), .VEC_N(VEC_N), .GEMM_ROWS(GR), .GEMM_COLS(GC)) dut (.*);

  logic act_read_pending = 0, weight_read_pending = 0;
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      act_mem_rvalid <= 0; weight_mem_rvalid <= 0;
      act_read_pending <= 0; weight_read_pending <= 0;
      act_mem_rdata <= '0; weight_mem_rdata <= '0;
    end else begin
      act_mem_rvalid <= 0; weight_mem_rvalid <= 0;
      if (act_mem_req && !act_mem_write) act_read_pending <= 1;
      if (weight_mem_req && !weight_mem_write) weight_read_pending <= 1;
      if (act_read_pending) begin act_mem_rvalid <= 1; act_read_pending <= 0; end
      if (weight_read_pending) begin weight_mem_rvalid <= 1; weight_read_pending <= 0; end
    end
  end

  function automatic [63:0] word(input [7:0] code, input [7:0] dst,
                                  input [7:0] src0, input [7:0] src1,
                                  input [15:0] length);
    word = {code, 8'h03, dst, src0, src1, length, 8'h00};
  endfunction
  function automatic [63:0] word_flags(input [7:0] code, input [7:0] flags,
                                        input [7:0] dst, input [7:0] src0,
                                        input [7:0] src1, input [15:0] length);
    word_flags = {code, flags, dst, src0, src1, length, 8'h00};
  endfunction
  task automatic write_state(input integer idx, input integer signed value);
    begin @(negedge clk); state_index=idx; state_data=value; state_we=1; @(negedge clk); state_we=0; end
  endtask
  task automatic write_weight(input integer idx, input integer signed value);
    begin @(negedge clk); weight_index=idx; weight_data=value; weight_we=1; @(negedge clk); weight_we=0; end
  endtask
  task automatic write_bias(input integer idx, input integer signed value);
    begin @(negedge clk); bias_index=idx; bias_data=value; bias_we=1; @(negedge clk); bias_we=0; end
  endtask
  task automatic send(input [63:0] w);
    begin @(negedge clk); while(!instr_ready) @(negedge clk); instr_word=w; instr_valid=1;
      @(negedge clk); instr_valid=0; while(!instr_ready) @(negedge clk); end
  endtask

  integer i, j; logic action_seen=0; logic signed [N*16-1:0] action_latched='0;
  always @(negedge clk) if(action_valid) begin action_seen=1; action_latched=action_out; end

  // Production-array command smoke.  A compiler word with flags[7]=1 must
  // launch the 16x48 array and wait for its done pulse.  The tile feed is an
  // explicit scheduler-side stream, so the testbench supplies one legal beat
  // after busy rises instead of pretending the 64-bit command contains data.
  logic prod_feed_enable = 0, prod_fed = 0, prod_done_seen = 0;
  always @(negedge clk) begin
    gemm_feed_vld = 0;
    gemm_feed_pulse = 0;
    if (gemm_done) prod_done_seen = 1;
    if (prod_feed_enable && gemm_busy && !prod_fed) begin
      gemm_a_feed = '0;
      gemm_b_feed = '0;
      gemm_feed_vld = 1;
      gemm_feed_pulse = 1;
      prod_fed = 1;
    end
  end

  initial begin
    repeat(2) @(negedge clk); rst_n=1;
    for(i=0;i<K;i=i+1) write_state(i,(i+1)*10*((i%2)?-1:1));
    for(j=0;j<N;j=j+1) begin write_bias(j,j-3); for(i=0;i<K;i=i+1) write_weight(j*K+i,((j+2*i)%5)-2); end
    send(word(8'h01,0,0,0,1)); send(word(8'h02,1,0,1,1));
    send(word(8'h10,2,0,1,0));
    if(!action_seen) $fatal(1,"system top action timeout");
    prod_feed_enable = 1;
    prod_fed = 0;
    send(word_flags(8'h10,8'h83,2,0,1,1));
    prod_feed_enable = 0;
    if (!prod_fed) $fatal(1,"production array feed was not accepted");
    if (!prod_done_seen) $fatal(1,"production array done was not observed");
    // STORE_ACTION is covered by the runtime test, where the stream source is
    // driven explicitly.  This top-level smoke keeps the focus on command,
    // memory-read and GEMM wiring and must not hang on an undriven write beat.
    send(word(8'hff,0,0,0,0));
    @(posedge clk); #1;
    $display("TB_W8A16_SYSTEM_V2 PASS action=%h production_array_feed=%0d production_array_done=%0d", action_latched, prod_fed, prod_done_seen);
    $finish(0);
  end
endmodule
