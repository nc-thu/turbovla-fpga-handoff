// Multi-cycle integer softmax primitive.
//
// Max reduction, LUT evaluation and normalization are scheduled one lane at
// a time.  This preserves the existing max-subtract/LUT/Q1.15 semantics but
// avoids a single N-lane divider/adder cone in the system top.
`ifndef TVLA_W8A16_SOFTMAX_SV
`define TVLA_W8A16_SOFTMAX_SV
module w8a16_softmax #(parameter int N = 16) (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   in_vld,
  input  logic signed [N*16-1:0] x,
  output logic                   out_vld,
  output logic        [N*16-1:0] y
);
  typedef enum logic [3:0] {S_IDLE, S_MAX, S_EXP, S_NORM, S_NUM_BUILD, S_DIV, S_EMIT} state_t;
  state_t state;
  logic signed [15:0] x_r [0:N-1];
  integer idx;
  integer signed max_r;
  integer signed max_next;
  integer signed d_i;
  integer unsigned e_i;
  integer unsigned e_r [0:N-1];
  integer unsigned sum_e_r;
  integer unsigned sum_next;
  integer unsigned norm_i;
  logic [31:0] div_num_r;
  logic [31:0] div_den_r;
  logic [31:0] div_quot_r;
  logic [32:0] div_rem_r;
  integer div_bit;
  logic [32:0] rem_next;
  logic [31:0] quot_next;
  logic [31:0] num_mul_acc;
  logic [31:0] num_mul_term;
  integer num_mul_bit;
  logic [31:0] num_acc_next;
  integer i;

  function automatic integer unsigned exp_lut(input integer signed d);
    integer signed bucket;
    begin
      bucket = d >>> 12;
      case (bucket)
        0: exp_lut = 32767; 1: exp_lut = 25500; 2: exp_lut = 19800;
        3: exp_lut = 15400; 4: exp_lut = 12000; 5: exp_lut = 9300;
        6: exp_lut = 7200; 7: exp_lut = 5600; 8: exp_lut = 4300;
        9: exp_lut = 3300; 10: exp_lut = 2500; 11: exp_lut = 1900;
        12: exp_lut = 1400; 13: exp_lut = 1000; 14: exp_lut = 700;
        default: exp_lut = 400;
      endcase
    end
  endfunction

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= S_IDLE;
      idx <= 0;
      max_r <= -2147483647;
      sum_e_r <= 0;
      div_num_r <= 0;
      div_den_r <= 1;
      div_quot_r <= 0;
      div_rem_r <= 0;
      div_bit <= 31;
      num_mul_acc <= 0;
      num_mul_term <= 0;
      num_mul_bit <= 0;
      out_vld <= 1'b0;
      y <= '0;
      for (i = 0; i < N; i = i + 1) begin
        x_r[i] <= '0;
        e_r[i] <= 0;
      end
    end else begin
      out_vld <= 1'b0;
      case (state)
        S_IDLE: begin
          if (in_vld) begin
            for (i = 0; i < N; i = i + 1) x_r[i] <= $signed(x[i*16 +: 16]);
            idx <= 0;
            max_r <= -2147483647;
            sum_e_r <= 0;
            state <= S_MAX;
          end
        end
        S_MAX: begin
          max_next = max_r;
          if ($signed(x_r[idx]) > max_next) max_next = $signed(x_r[idx]);
          max_r <= max_next;
          if (idx == N-1) begin
            idx <= 0;
            sum_e_r <= 0;
            state <= S_EXP;
          end else idx <= idx + 1;
        end
        S_EXP: begin
          d_i = max_r - $signed(x_r[idx]);
          e_i = exp_lut(d_i);
          e_r[idx] <= e_i;
          sum_next = sum_e_r + e_i;
          sum_e_r <= sum_next;
          if (idx == N-1) begin
            idx <= 0;
            state <= S_NORM;
          end else idx <= idx + 1;
        end
        S_NORM: begin
          // Build e*32767 after registering e.  This avoids a wide constant
          // multiplier directly on the exp-memory output path.
          num_mul_acc <= 0;
          num_mul_term <= e_r[idx][31:0];
          num_mul_bit <= 0;
          div_den_r <= (sum_e_r == 0) ? 1 : sum_e_r;
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
          // Bit-serial restoring division keeps the normalization path
          // bounded.  It has the same integer quotient as the former '/'
          // expression, but no variable divider between two registers.
          rem_next = {div_rem_r[31:0], div_num_r[div_bit]};
          quot_next = div_quot_r;
          if (rem_next >= {1'b0, div_den_r}) begin
            rem_next = rem_next - {1'b0, div_den_r};
            quot_next[div_bit] = 1'b1;
          end
          div_rem_r <= rem_next;
          div_quot_r <= quot_next;
          if (div_bit == 0) begin
            norm_i = quot_next;
            if (norm_i > 32767) norm_i = 32767;
            y[idx*16 +: 16] <= norm_i[15:0];
            if (idx == N-1) state <= S_EMIT;
            else begin idx <= idx + 1; state <= S_NORM; end
          end else div_bit <= div_bit - 1;
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
