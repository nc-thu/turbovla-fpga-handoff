`timescale 1ns/1ps
// Compiler-to-RTL command-path smoke.  The state vector is derived from the
// LIBERO bowl-placement action format; this test exercises one action
// projection and emits the seven normalized action lanes.  It is not a full
// TurboVLA/DINO inference or an environment success-rate test.
module tb_w8a16_runtime;
  localparam int K = 8, N = 7;
  logic clk = 0; always #5 clk = ~clk;
  logic rst_n = 0;
  logic [63:0] instr_word = 0;
  logic instr_valid = 0, instr_ready;
  logic state_we = 0, weight_we = 0, bias_we = 0;
  logic [$clog2(K)-1:0] state_index = 0;
  logic [$clog2(N*K)-1:0] weight_index = 0;
  logic [$clog2(N)-1:0] bias_index = 0;
  logic signed [15:0] state_data = 0, bias_data = 0;
  logic signed [7:0] weight_data = 0;
  logic action_valid, busy, done;
  logic signed [N*16-1:0] action_out;
  integer i, j, t;
  integer signed state_v [0:K-1];
  integer signed weight_v [0:N-1][0:K-1];
  integer signed bias_v [0:N-1];
  logic action_seen = 1'b0;
  logic signed [N*16-1:0] action_latched = '0;

  w8a16_runtime #(.K(K), .N(N)) dut(.*);

  always @(negedge clk) begin
    if (action_valid) begin action_seen = 1'b1; action_latched = action_out; end
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
  task automatic send(input [63:0] w);
    begin
      @(negedge clk); while (!instr_ready) @(negedge clk);
      instr_word = w; instr_valid = 1'b1;
      @(negedge clk); instr_valid = 1'b0;
      while (!instr_ready) @(negedge clk);
    end
  endtask

  initial begin
    $display("RUNTIME_TRACE start t=%0t", $time);
    repeat (2) @(negedge clk); rst_n = 1'b1;
    $display("RUNTIME_TRACE reset_released_for_preload t=%0t ready=%b", $time, instr_ready);
    for (i = 0; i < K; i = i + 1) begin
      state_v[i] = (i + 1) * 100 * ((i % 2) ? -1 : 1);
      write_state(i, state_v[i]);
    end
    $display("RUNTIME_TRACE preload_done t=%0t", $time);
    for (j = 0; j < N; j = j + 1) begin
      bias_v[j] = j - 3;
      write_bias(j, bias_v[j]);
      for (i = 0; i < K; i = i + 1) begin
        weight_v[j][i] = ((j + 2*i) % 5) - 2;
        write_weight(j*K+i, weight_v[j][i]);
      end
    end
    // Preload ports are host-side writes and are only accepted after reset.
    // These words match compiler/.../turbovla_w8a16_program.json smoke_program.
    $display("RUNTIME_TRACE reset_released ready=%b", instr_ready);
    send(word(8'h01, 0, 0, 0, 8));
    $display("RUNTIME_TRACE load_ctx_done t=%0t", $time);
    send(word(8'h02, 1, 0, 0, N*K));
    $display("RUNTIME_TRACE load_weight_done t=%0t", $time);
    send(word(8'h10, 2, 0, 1, 0));
    $display("RUNTIME_TRACE gemm_done t=%0t action_valid=%b", $time, action_valid);
    if (!action_seen) $fatal(1, "runtime action timeout");
    for (j = 0; j < N; j = j + 1)
      if ($signed(action_latched[j*16 +: 16]) > 32767 || $signed(action_latched[j*16 +: 16]) < -32768)
        $fatal(1, "action saturation/width failure");
    $display("RUNTIME_ACTION task=pick_up_the_black_bowl_from_table_center_and_place_it_on_the_plate state=0 action=%h", action_latched);
    send(word(8'h20, 2, 2, 2, N));
    send(word(8'h34, 3, 2, 0, N));
    send(word(8'h04, 0, 3, 0, N));
    // END raises the sequencer done pulse, completing compiler -> RTL.
    @(negedge clk); while (!instr_ready) @(negedge clk);
    instr_word = word(8'hff, 0, 0, 0, 0); instr_valid = 1'b1;
    @(negedge clk); instr_valid = 1'b0;
    for (t = 0; t < 20; t = t + 1) begin @(posedge clk); #1; if (done) t = 20; end
    if (!done) $fatal(1, "runtime END timeout");
    $display("TB_W8A16_RUNTIME PASS action_lanes=%0d", N);
    $finish(0);
  end
endmodule
