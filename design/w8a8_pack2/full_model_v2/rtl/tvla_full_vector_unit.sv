// TurboVLA full-model vector primitive.
//
// The W8A8 GEMM path keeps INT8 products and INT32 accumulation.  Operations
// that are numerically sensitive (normalization and attention softmax) use a
// signed INT16 intermediate here.  This is a synthesizable, bounded reference
// implementation: the production design may replace the LUT functions with a
// vendor FP16 IP without changing the command protocol.
`ifndef TVLA_FULL_VECTOR_UNIT_SV
`define TVLA_FULL_VECTOR_UNIT_SV
module tvla_full_vector_unit #(
  parameter int LANES = 16,
  parameter int DW = 16
) (
  input  logic clk,
  input  logic rst_n,
  input  logic in_valid,
  output logic in_ready,
  input  logic [7:0] op_code,
  input  logic signed [LANES*DW-1:0] x,
  input  logic signed [LANES*DW-1:0] y,
  input  logic signed [DW-1:0] param0,
  input  logic signed [DW-1:0] param1,
  output logic out_valid,
  input  logic out_ready,
  output logic signed [LANES*DW-1:0] out_data,
  output logic [31:0] busy_cycles,
  output logic [31:0] op_count
);
  localparam logic [7:0] OP_BIAS = 8'h20;
  localparam logic [7:0] OP_ADD = 8'h21;
  localparam logic [7:0] OP_MUL = 8'h22;
  localparam logic [7:0] OP_LN = 8'h30;
  localparam logic [7:0] OP_SOFTMAX = 8'h31;
  localparam logic [7:0] OP_GELU = 8'h33;
  localparam logic [7:0] OP_RELU = 8'h34;
  localparam logic [7:0] OP_TANH = 8'h35;
  localparam logic [7:0] OP_EXP = 8'h36;
  localparam logic [7:0] OP_DIV = 8'h37;
  localparam logic [7:0] OP_CLAMP = 8'h38;

  typedef enum logic [3:0] {S_IDLE, S_FAST, S_LN_SUM, S_LN_SCALE,
                            S_SM_MAX, S_SM_EXP, S_SM_NORM, S_EMIT} state_t;
  state_t state;
  logic [7:0] op_r;
  logic signed [DW-1:0] xr [0:LANES-1];
  logic signed [DW-1:0] yr [0:LANES-1];
  logic signed [DW-1:0] rr [0:LANES-1];
  logic signed [DW-1:0] p0_r, p1_r;
  integer idx;
  integer signed sum_r;
  integer signed mean_r;
  integer signed max_abs_r;
  integer unsigned exp_r [0:LANES-1];
  integer unsigned exp_sum_r;
  integer signed max_r;
  integer signed delta_i;
  integer signed work_i;
  integer unsigned exp_i;
  integer unsigned norm_i;
  integer signed mul_i;
  integer i;

  function automatic integer signed sat16(input integer signed v);
    begin
      if (v > 32767) sat16 = 32767;
      else if (v < -32768) sat16 = -32768;
      else sat16 = v;
    end
  endfunction

  function automatic integer unsigned exp_lut(input integer signed d);
    integer signed bucket;
    begin
      // d is max(x)-x in the input scale.  The table is monotonic and
      // bounded; values beyond the last bucket map to a small positive tail.
      bucket = d >>> 10;
      if (bucket <= 0) exp_lut = 32767;
      else if (bucket == 1) exp_lut = 24800;
      else if (bucket == 2) exp_lut = 18700;
      else if (bucket == 3) exp_lut = 14100;
      else if (bucket == 4) exp_lut = 10600;
      else if (bucket == 5) exp_lut = 7900;
      else if (bucket == 6) exp_lut = 5900;
      else if (bucket == 7) exp_lut = 4400;
      else if (bucket == 8) exp_lut = 3250;
      else if (bucket == 9) exp_lut = 2400;
      else if (bucket == 10) exp_lut = 1750;
      else if (bucket == 11) exp_lut = 1280;
      else if (bucket == 12) exp_lut = 930;
      else if (bucket == 13) exp_lut = 680;
      else if (bucket == 14) exp_lut = 500;
      else exp_lut = 256;
    end
  endfunction

  function automatic integer signed gelu_approx(input integer signed v);
    begin
      // Piecewise approximation in the signed INT16 domain.  The positive
      // branch is linear; the negative tail is attenuated instead of clipped
      // to zero so that small negative activations remain representable.
      if (v >= 8192) gelu_approx = v;
      else if (v >= 0) gelu_approx = (v * 3) >>> 2;
      else if (v > -8192) gelu_approx = v >>> 2;
      else gelu_approx = v >>> 3;
    end
  endfunction

  function automatic integer signed tanh_approx(input integer signed v);
    begin
      if (v >= 12288) tanh_approx = 32767;
      else if (v <= -12288) tanh_approx = -32768;
      else if (v >= 4096) tanh_approx = 24576;
      else if (v <= -4096) tanh_approx = -24576;
      else tanh_approx = (v * 3) >>> 2;
    end
  endfunction

  // Bounded reciprocal approximations keep the control path synthesizable at
  // the array clock.  The software compiler still records the exact FP16
  // fallback cost; this RTL primitive is the integer hardware slot that can
  // later be replaced by a vendor FP16/LN IP without changing the interface.
  function automatic integer signed norm_approx(input integer signed d,
                                                  input integer signed scale);
    integer signed ad;
    begin
      ad = (scale < 0) ? -scale : scale;
      if (ad <= 2048) norm_approx = d <<< 3;
      else if (ad <= 4096) norm_approx = d <<< 2;
      else if (ad <= 8192) norm_approx = d <<< 1;
      else if (ad <= 16384) norm_approx = d;
      else if (ad <= 24576) norm_approx = d >>> 1;
      else norm_approx = d >>> 2;
    end
  endfunction

  function automatic integer signed div_approx(input integer signed num,
                                                input integer signed den);
    integer signed ad;
    begin
      ad = (den < 0) ? -den : den;
      if (den == 0) div_approx = 0;
      else if (ad <= 2048) div_approx = (den < 0) ? -(num <<< 4) : (num <<< 4);
      else if (ad <= 4096) div_approx = (den < 0) ? -(num <<< 3) : (num <<< 3);
      else if (ad <= 8192) div_approx = (den < 0) ? -(num <<< 2) : (num <<< 2);
      else if (ad <= 16384) div_approx = (den < 0) ? -(num <<< 1) : (num <<< 1);
      else div_approx = (den < 0) ? -(num >>> 1) : (num >>> 1);
    end
  endfunction

  assign in_ready = (state == S_IDLE);

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= S_IDLE;
      op_r <= 0;
      p0_r <= 0;
      p1_r <= 0;
      idx <= 0;
      sum_r <= 0;
      mean_r <= 0;
      max_abs_r <= 1;
      exp_sum_r <= 0;
      max_r <= -32768;
      out_valid <= 1'b0;
      out_data <= '0;
      busy_cycles <= 0;
      op_count <= 0;
      for (i = 0; i < LANES; i = i + 1) begin
        xr[i] <= 0;
        yr[i] <= 0;
        rr[i] <= 0;
        exp_r[i] <= 0;
      end
    end else begin
      out_valid <= 1'b0;
      if (state != S_IDLE) busy_cycles <= busy_cycles + 1'b1;
      case (state)
        S_IDLE: begin
          if (in_valid) begin
            op_r <= op_code;
            p0_r <= param0;
            p1_r <= param1;
            for (i = 0; i < LANES; i = i + 1) begin
              xr[i] <= $signed(x[i*DW +: DW]);
              yr[i] <= $signed(y[i*DW +: DW]);
            end
            idx <= 0;
            sum_r <= 0;
            max_abs_r <= 1;
            max_r <= -32768;
            exp_sum_r <= 0;
            op_count <= op_count + 1'b1;
            if (op_code == OP_LN) state <= S_LN_SUM;
            else if (op_code == OP_SOFTMAX) state <= S_SM_MAX;
            else state <= S_FAST;
          end
        end
        S_FAST: begin
          for (i = 0; i < LANES; i = i + 1) begin
            if (op_r == OP_BIAS) work_i = $signed(xr[i]) + $signed(p0_r);
            else if (op_r == OP_ADD) work_i = $signed(xr[i]) + $signed(yr[i]);
            else if (op_r == OP_MUL) work_i = ($signed(xr[i]) * $signed(yr[i])) >>> 8;
            else if (op_r == OP_GELU) work_i = gelu_approx($signed(xr[i]));
            else if (op_r == OP_RELU) work_i = ($signed(xr[i]) < 0) ? 0 : $signed(xr[i]);
            else if (op_r == OP_TANH) work_i = tanh_approx($signed(xr[i]));
            else if (op_r == OP_EXP) work_i = exp_lut(-$signed(xr[i]));
            else if (op_r == OP_DIV) work_i = div_approx($signed(xr[i]) <<< 8, $signed(p1_r));
            else if (op_r == OP_CLAMP) begin
              if ($signed(xr[i]) < $signed(p0_r)) work_i = $signed(p0_r);
              else if ($signed(xr[i]) > $signed(p1_r)) work_i = $signed(p1_r);
              else work_i = $signed(xr[i]);
            end else work_i = $signed(xr[i]);
            rr[i] <= sat16(work_i);
          end
          state <= S_EMIT;
        end
        S_LN_SUM: begin
          sum_r <= sum_r + $signed(xr[idx]);
          if (idx == LANES-1) begin
            mean_r <= (sum_r + $signed(xr[idx])) >>> 4;
            idx <= 0;
            max_abs_r <= 1;
            state <= S_LN_SCALE;
          end else idx <= idx + 1;
        end
        S_LN_SCALE: begin
          delta_i = $signed(xr[idx]) - mean_r;
          work_i = (delta_i < 0) ? -delta_i : delta_i;
          if (work_i > max_abs_r) max_abs_r <= work_i;
          // Normalize to a signed INT16 range.  Registering one lane per
          // cycle keeps the reduction and divide out of the GEMM path.
          rr[idx] <= sat16(norm_approx(delta_i, max_abs_r));
          if (idx == LANES-1) state <= S_EMIT;
          else idx <= idx + 1;
        end
        S_SM_MAX: begin
          if ($signed(xr[idx]) > max_r) max_r <= $signed(xr[idx]);
          if (idx == LANES-1) begin
            idx <= 0;
            exp_sum_r <= 0;
            state <= S_SM_EXP;
          end else idx <= idx + 1;
        end
        S_SM_EXP: begin
          exp_i = exp_lut(max_r - $signed(xr[idx]));
          exp_r[idx] <= exp_i;
          exp_sum_r <= exp_sum_r + exp_i;
          if (idx == LANES-1) begin
            idx <= 0;
            state <= S_SM_NORM;
          end else idx <= idx + 1;
        end
        S_SM_NORM: begin
          // A coarse reciprocal keeps this fallback path bounded.  Exact
          // softmax remains a software/FP16 reference until the vendor IP is
          // instantiated in the same protocol slot.
          if (exp_sum_r == 0) norm_i = 0;
          else if (exp_sum_r > 262144) norm_i = exp_r[idx] >>> 3;
          else if (exp_sum_r > 131072) norm_i = exp_r[idx] >>> 2;
          else if (exp_sum_r > 65536) norm_i = exp_r[idx] >>> 1;
          else norm_i = exp_r[idx];
          rr[idx] <= sat16(norm_i);
          if (idx == LANES-1) state <= S_EMIT;
          else idx <= idx + 1;
        end
        S_EMIT: begin
          for (i = 0; i < LANES; i = i + 1) out_data[i*DW +: DW] <= rr[i];
          out_valid <= 1'b1;
          if (out_ready) state <= S_IDLE;
        end
        default: state <= S_IDLE;
      endcase
    end
  end
endmodule
`endif
