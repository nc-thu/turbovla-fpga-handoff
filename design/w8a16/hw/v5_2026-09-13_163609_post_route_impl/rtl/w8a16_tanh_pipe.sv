// Three-stage registered tanh approximation for the control/data path.
//
// Stage 1 extracts sign and magnitude, stage 2 selects the piecewise segment,
// and stage 3 evaluates the shift/add slope.  Keeping the approximation in a
// registered pipeline prevents the vector write-back and action paths from
// inheriting a wide combinational chain.  The arithmetic is the same bounded
// Q1.15 approximation used by w8a16_tanh.sv.
`ifndef TVLA_W8A16_TANH_PIPE_SV
`define TVLA_W8A16_TANH_PIPE_SV
module w8a16_tanh_pipe #(parameter int N = 16) (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   in_vld,
  input  logic signed [N*16-1:0] x,
  output logic                   out_vld,
  output logic signed [N*16-1:0] y
);
  logic v1, v2;
  logic [15:0] mag_r [0:N-1];
  logic sign_r [0:N-1];
  logic [1:0] seg_r [0:N-1];
  logic [15:0] base_r [0:N-1];
  logic [15:0] delta_r [0:N-1];
  integer i;
  integer signed mag_i;
  integer signed yi;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      v1 <= 1'b0;
      v2 <= 1'b0;
      out_vld <= 1'b0;
      y <= '0;
      for (i = 0; i < N; i = i + 1) begin
        mag_r[i] <= '0;
        sign_r[i] <= 1'b0;
        seg_r[i] <= 2'd0;
        base_r[i] <= '0;
        delta_r[i] <= '0;
      end
    end else begin
      v1 <= in_vld;
      v2 <= v1;
      out_vld <= v2;

      // Stage 1: signed input -> sign and unsigned magnitude.
      if (in_vld) begin
        for (i = 0; i < N; i = i + 1) begin
          sign_r[i] <= x[i*16 + 15];
          mag_r[i] <= x[i*16 + 15] ? -$signed(x[i*16 +: 16])
                                    : $signed(x[i*16 +: 16]);
        end
      end

      // Stage 2: segment decode.  Only compares and subtracts are on this
      // register-to-register path.
      if (v1) begin
        for (i = 0; i < N; i = i + 1) begin
          if (mag_r[i] >= 16'd24576) begin
            seg_r[i] <= 2'd3; base_r[i] <= 16'd32767; delta_r[i] <= 16'd0;
          end else if (mag_r[i] >= 16'd16384) begin
            seg_r[i] <= 2'd2; base_r[i] <= 16'd24576;
            delta_r[i] <= mag_r[i] - 16'd16384;
          end else if (mag_r[i] >= 16'd8192) begin
            seg_r[i] <= 2'd1; base_r[i] <= 16'd12288;
            delta_r[i] <= mag_r[i] - 16'd8192;
          end else begin
            seg_r[i] <= 2'd0; base_r[i] <= 16'd0; delta_r[i] <= mag_r[i];
          end
        end
      end

      // Stage 3: shift/add slope and sign restoration.
      if (v2) begin
        for (i = 0; i < N; i = i + 1) begin
          case (seg_r[i])
            2'd0, 2'd1: mag_i = base_r[i] + delta_r[i] + (delta_r[i] >>> 1);
            2'd2:      mag_i = base_r[i] + delta_r[i];
            default:  mag_i = 32767;
          endcase
          yi = sign_r[i] ? -mag_i : mag_i;
          if (yi > 32767) y[i*16 +: 16] <= 16'sh7fff;
          else if (yi < -32768) y[i*16 +: 16] <= -16'sh8000;
          else y[i*16 +: 16] <= yi[15:0];
        end
      end
    end
  end
endmodule
`endif
