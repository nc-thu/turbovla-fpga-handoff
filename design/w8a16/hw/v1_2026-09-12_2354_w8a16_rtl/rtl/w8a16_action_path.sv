// Serialized action-head path used by the compiler-to-RTL smoke.
// Production mapping sends the same GEMM through the 16×48 array.  This
// standalone path deliberately uses LUT multipliers (use_dsp=no) so the
// advertised 768-DSP budget is unchanged while the command protocol can be
// tested without a full model image in RTL simulation.
`ifndef TVLA_W8A16_ACTION_PATH_SV
`define TVLA_W8A16_ACTION_PATH_SV
module w8a16_action_path #(
  parameter int K = 8,
  parameter int N = 7
) (
  input  logic                         clk,
  input  logic                         rst_n,
  input  logic                         start,
  input  logic [K*16-1:0]              state_in,
  input  logic [N*K*8-1:0]             weight_in,
  input  logic [N*16-1:0]              bias_in,
  output logic                         action_valid,
  output logic signed [N*16-1:0]       action_out,
  output logic                         busy,
  output logic                         done
);
  integer col_comb;
  integer col_seq;
  integer kk_seq;
  logic [3:0] col_r;
  logic [3:0] k_r;
  logic signed [39:0] acc_r [0:N-1];
  logic signed [15:0] state_r [0:K-1];
  logic signed [7:0] weight_r [0:N-1][0:K-1];
  logic signed [15:0] bias_r [0:N-1];
  logic signed [31:0] prod;
  logic signed [N*16-1:0] raw_action;
  logic signed [N*16-1:0] tanh_action;
  logic finish_pending;
  (* use_dsp = "no" *) logic signed [39:0] bias_sum;
  w8a16_tanh #(.N(N)) u_tanh (.x(raw_action), .y(tanh_action));

  always_comb begin
    for (col_comb = 0; col_comb < N; col_comb = col_comb + 1) begin
      bias_sum = acc_r[col_comb] + $signed(bias_r[col_comb]);
      if (bias_sum > 32767) raw_action[col_comb*16 +: 16] = 16'sh7fff;
      else if (bias_sum < -32768) raw_action[col_comb*16 +: 16] = -16'sh8000;
      else raw_action[col_comb*16 +: 16] = bias_sum[15:0];
    end
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      col_r <= '0; k_r <= '0; busy <= 1'b0; done <= 1'b0; action_valid <= 1'b0; finish_pending <= 1'b0;
      action_out <= '0;
      for (col_seq = 0; col_seq < N; col_seq = col_seq + 1) acc_r[col_seq] <= '0;
    end else begin
      done <= 1'b0;
      action_valid <= 1'b0;
      if (finish_pending) begin
        // The final accumulator write happened on the previous clock edge;
        // sample the updated value here before publishing the action.
        action_out <= tanh_action;
        action_valid <= 1'b1;
        done <= 1'b1;
        finish_pending <= 1'b0;
      end
      if (start && !busy) begin
        busy <= 1'b1; col_r <= '0; k_r <= '0; finish_pending <= 1'b0;
      for (col_seq = 0; col_seq < N; col_seq = col_seq + 1) acc_r[col_seq] <= '0;
      for (kk_seq = 0; kk_seq < K; kk_seq = kk_seq + 1) state_r[kk_seq] <= $signed(state_in[kk_seq*16 +: 16]);
      for (col_seq = 0; col_seq < N; col_seq = col_seq + 1) begin
          bias_r[col_seq] <= $signed(bias_in[col_seq*16 +: 16]);
          for (kk_seq = 0; kk_seq < K; kk_seq = kk_seq + 1)
            weight_r[col_seq][kk_seq] <= $signed(weight_in[(col_seq*K+kk_seq)*8 +: 8]);
        end
      end else if (busy) begin
        prod = $signed(state_r[k_r]) * $signed(weight_r[col_r][k_r]);
        // A concatenation is unsigned in SystemVerilog unless cast back.
        // The explicit $signed is required for negative INT16×INT8 products.
        acc_r[col_r] <= acc_r[col_r] + $signed({{8{prod[31]}}, prod});
        if (k_r == K-1) begin
          k_r <= '0;
          if (col_r == N-1) begin
            busy <= 1'b0;
            finish_pending <= 1'b1;
          end else col_r <= col_r + 1'b1;
        end else k_r <= k_r + 1'b1;
      end
    end
  end
endmodule
`endif
