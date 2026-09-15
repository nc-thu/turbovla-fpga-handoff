// TurboVLA W8A16 action projection with explicit post-accumulation stages.
//
// The old smoke path exposed acc+bias+tanh directly to action_out.  That was
// easy to simulate, but made the system top's longest path cross the whole
// post-processing chain.  This version keeps the same integer result and
// protocol, while registering three boundaries:
//   ACCUM -> bias/saturation -> tanh approximation -> output.
// A new start is accepted only after the output pulse, so the extra latency
// cannot overwrite the state used by the previous command.
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
  localparam int K_IDX_W = (K <= 1) ? 1 : $clog2(K);
  localparam int N_IDX_W = (N <= 1) ? 1 : $clog2(N);

  typedef enum logic [2:0] {S_IDLE, S_ACCUM, S_BIAS, S_TANH, S_TANH_WAIT,
                            S_EMIT} state_t;
  state_t state;

  logic [N_IDX_W-1:0] col_r;
  logic [K_IDX_W-1:0] k_r;
  logic signed [39:0] acc_r [0:N-1];
  logic signed [15:0] state_r [0:K-1];
  logic signed [7:0]  weight_r [0:N-1][0:K-1];
  logic signed [15:0] bias_r [0:N-1];

  logic signed [31:0] product_comb;
  logic signed [39:0] acc_next;
  logic signed [N*16-1:0] bias_stage_next;
  logic signed [N*16-1:0] bias_stage_r;
  logic signed [N*16-1:0] tanh_stage_next;
  logic signed [N*16-1:0] tanh_stage_r;
  logic tanh_done;

  integer i, j;

  function automatic signed [15:0] sat16_40(input logic signed [39:0] v);
    begin
      if (v > 40'sd32767) sat16_40 = 16'sh7fff;
      else if (v < -40'sd32768) sat16_40 = -16'sh8000;
      else sat16_40 = v[15:0];
    end
  endfunction

  always_comb begin
    product_comb = $signed(state_r[k_r]) * $signed(weight_r[col_r][k_r]);
    acc_next = acc_r[col_r] + $signed({{8{product_comb[31]}}, product_comb});
    bias_stage_next = '0;
    for (i = 0; i < N; i = i + 1)
      bias_stage_next[i*16 +: 16] = sat16_40(
        acc_r[i] + $signed({{24{bias_r[i][15]}}, bias_r[i]})
      );
  end

  // The tanh approximation has its own three-stage registered pipeline.  It
  // is launched after bias saturation and acknowledged before the action is
  // emitted, so the 40-bit accumulator never shares a long path with it.
  w8a16_tanh_pipe #(.N(N)) u_tanh (
    .clk(clk), .rst_n(rst_n), .in_vld(state == S_TANH), .x(bias_stage_r),
    .out_vld(tanh_done), .y(tanh_stage_next)
  );

  assign busy = (state != S_IDLE);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= S_IDLE;
      col_r <= '0;
      k_r <= '0;
      bias_stage_r <= '0;
      tanh_stage_r <= '0;
      action_out <= '0;
      action_valid <= 1'b0;
      done <= 1'b0;
      for (j = 0; j < N; j = j + 1) acc_r[j] <= '0;
      for (j = 0; j < K; j = j + 1) state_r[j] <= '0;
      for (j = 0; j < N; j = j + 1) bias_r[j] <= '0;
      for (j = 0; j < N; j = j + 1)
        for (i = 0; i < K; i = i + 1) weight_r[j][i] <= '0;
    end else begin
      action_valid <= 1'b0;
      done <= 1'b0;
      case (state)
        S_IDLE: begin
          if (start) begin
            col_r <= '0;
            k_r <= '0;
            for (j = 0; j < N; j = j + 1) begin
              acc_r[j] <= '0;
              bias_r[j] <= $signed(bias_in[j*16 +: 16]);
              for (i = 0; i < K; i = i + 1)
                weight_r[j][i] <= $signed(weight_in[(j*K+i)*8 +: 8]);
            end
            for (i = 0; i < K; i = i + 1)
              state_r[i] <= $signed(state_in[i*16 +: 16]);
            state <= S_ACCUM;
          end
        end
        S_ACCUM: begin
          acc_r[col_r] <= acc_next;
          if (k_r == K-1) begin
            k_r <= '0;
            if (col_r == N-1) state <= S_BIAS;
            else col_r <= col_r + 1'b1;
          end else begin
            k_r <= k_r + 1'b1;
          end
        end
        S_BIAS: begin
          bias_stage_r <= bias_stage_next;
          state <= S_TANH;
        end
        S_TANH: begin
          state <= S_TANH_WAIT;
        end
        S_TANH_WAIT: begin
          if (tanh_done) begin
            tanh_stage_r <= tanh_stage_next;
            state <= S_EMIT;
          end
        end
        S_EMIT: begin
          action_out <= tanh_stage_r;
          action_valid <= 1'b1;
          done <= 1'b1;
          state <= S_IDLE;
        end
        default: state <= S_IDLE;
      endcase
    end
  end
endmodule
`endif
