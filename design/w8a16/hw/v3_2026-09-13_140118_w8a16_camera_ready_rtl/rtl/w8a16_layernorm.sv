// Multi-cycle bounded LayerNorm primitive.
//
// The previous implementation reduced and normalized all lanes in one
// combinational block.  That is functionally compact but creates a very long
// reduction/division path when N=16.  This version keeps the same bounded
// integer definition while visiting one lane per cycle.  The public
// in_vld/out_vld handshake therefore makes the extra latency explicit.
`ifndef TVLA_W8A16_LAYERNORM_SV
`define TVLA_W8A16_LAYERNORM_SV
module w8a16_layernorm #(parameter int N = 16) (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   in_vld,
  input  logic signed [N*16-1:0] x,
  output logic                   out_vld,
  output logic signed [N*16-1:0] y
);
  typedef enum logic [3:0] {S_IDLE, S_SUM, S_MAX, S_SCALE, S_NUM_BUILD, S_DIV, S_SATURATE, S_WRITEBACK, S_EMIT} state_t;
  state_t state;
  logic signed [15:0] x_r [0:N-1];
  integer idx;
  integer signed sum_r;
  integer signed mean_r;
  integer signed max_abs_r;
  integer signed sum_next;
  integer signed delta_i;
  integer signed abs_i;
  logic [31:0] div_num_r;
  logic [31:0] div_den_r;
  logic [31:0] div_quot_r;
  logic [32:0] div_rem_r;
  logic div_neg_r;
  integer div_bit;
  logic [32:0] rem_next;
  logic [31:0] quot_next;
  integer signed scaled_q;
  logic [31:0] num_mul_acc;
  logic [31:0] num_mul_term;
  integer num_mul_bit;
  logic [31:0] num_acc_next;
  logic signed [15:0] result_lane_r;
  integer i;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= S_IDLE;
      idx <= 0;
      sum_r <= 0;
      mean_r <= 0;
      max_abs_r <= 1;
      div_num_r <= 0;
      div_den_r <= 1;
      div_quot_r <= 0;
      div_rem_r <= 0;
      div_neg_r <= 1'b0;
      div_bit <= 31;
      num_mul_acc <= 0;
      num_mul_term <= 0;
      num_mul_bit <= 0;
      result_lane_r <= '0;
      out_vld <= 1'b0;
      y <= '0;
      for (i = 0; i < N; i = i + 1) x_r[i] <= '0;
    end else begin
      out_vld <= 1'b0;
      case (state)
        S_IDLE: begin
          if (in_vld) begin
            for (i = 0; i < N; i = i + 1) x_r[i] <= $signed(x[i*16 +: 16]);
            idx <= 0;
            sum_r <= 0;
            state <= S_SUM;
          end
        end
        S_SUM: begin
          sum_next = sum_r + $signed(x_r[idx]);
          sum_r <= sum_next;
          if (idx == N-1) begin
            mean_r <= sum_next / N;
            idx <= 0;
            max_abs_r <= 1;
            state <= S_MAX;
          end else idx <= idx + 1;
        end
        S_MAX: begin
          delta_i = $signed(x_r[idx]) - mean_r;
          abs_i = (delta_i < 0) ? -delta_i : delta_i;
          if (abs_i > max_abs_r) max_abs_r <= abs_i;
          if (idx == N-1) begin
            idx <= 0;
            state <= S_SCALE;
          end else idx <= idx + 1;
        end
        S_SCALE: begin
          delta_i = $signed(x_r[idx]) - mean_r;
          abs_i = (delta_i < 0) ? -delta_i : delta_i;
          // Register the absolute value before forming abs*32767.  A direct
          // constant multiply here put the input register on the critical
          // path.  The following 15-cycle shift/add sequence has the same
          // exact integer product, but keeps each combinational step small.
          num_mul_acc <= 0;
          num_mul_term <= abs_i[31:0];
          num_mul_bit <= 0;
          div_den_r <= (max_abs_r == 0) ? 1 : max_abs_r;
          div_neg_r <= (delta_i < 0);
          state <= S_NUM_BUILD;
        end
        S_NUM_BUILD: begin
          num_acc_next = num_mul_acc + num_mul_term;
          num_mul_acc <= num_acc_next;
          num_mul_term <= num_mul_term << 1;
          if (num_mul_bit == 14) begin
            div_num_r <= num_acc_next;
            div_quot_r <= 0;
            div_rem_r <= 0;
            div_bit <= 31;
            state <= S_DIV;
          end else num_mul_bit <= num_mul_bit + 1;
        end
        S_DIV: begin
          // Restoring unsigned division, one bit per cycle.  The old
          // implementation used a variable '/' here; Vivado mapped it to a
          // long divider.  The registered bit-serial form keeps the same
          // truncation semantics without a multi-nanosecond combinational
          // cone.
          rem_next = {div_rem_r[31:0], div_num_r[div_bit]};
          quot_next = div_quot_r;
          if (rem_next >= {1'b0, div_den_r}) begin
            rem_next = rem_next - {1'b0, div_den_r};
            quot_next[div_bit] = 1'b1;
          end
          div_rem_r <= rem_next;
          div_quot_r <= quot_next;
          if (div_bit == 0) begin
            // Register the last divider quotient before saturation.  This
            // keeps the divider carry chain out of the result-register path.
            state <= S_SATURATE;
          end else div_bit <= div_bit - 1;
        end
        S_SATURATE: begin
          scaled_q = div_neg_r ? -$signed(div_quot_r) : $signed(div_quot_r);
          if (scaled_q > 32767) result_lane_r <= 16'sh7fff;
          else if (scaled_q < -32768) result_lane_r <= -16'sh8000;
          else result_lane_r <= scaled_q[15:0];
          state <= S_WRITEBACK;
        end
        S_WRITEBACK: begin
          y[idx*16 +: 16] <= result_lane_r;
          if (idx == N-1) state <= S_EMIT;
          else begin idx <= idx + 1; state <= S_SCALE; end
        end
        S_EMIT: begin
          out_vld <= 1'b1;
          state <= S_IDLE;
        end
        default: state <= S_IDLE;
      endcase
    end
  end
endmodule
`endif
