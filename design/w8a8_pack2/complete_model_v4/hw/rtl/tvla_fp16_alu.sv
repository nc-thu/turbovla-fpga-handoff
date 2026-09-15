// Pipelined arithmetic slot for numerically sensitive TurboVLA operators.
//
// The default implementation is a bounded signed-16 fixed-point datapath. It
// deliberately keeps the same handshake and lane shape as a Xilinx FP16 IP
// block, so a generated floating-point instance can replace the function
// bodies without changing the top-level command protocol.  The slot is
// synthesized in this build; it is not a claim that a vendor FP16 macro is
// already present in the checkpoint.
`ifndef TVLA_FP16_ALU_SV
`define TVLA_FP16_ALU_SV
module tvla_fp16_alu #(
  parameter int LANES = 16,
  parameter int DW = 16
) (
  input  logic clk,
  input  logic rst_n,
  input  logic in_valid,
  output logic in_ready,
  input  logic [3:0] op_code,
  input  logic signed [LANES*DW-1:0] a,
  input  logic signed [LANES*DW-1:0] b,
  input  logic signed [DW-1:0] param,
  output logic out_valid,
  input  logic out_ready,
  output logic signed [LANES*DW-1:0] y
);
  localparam logic [3:0] OP_ADD = 4'd0;
  localparam logic [3:0] OP_SUB = 4'd1;
  localparam logic [3:0] OP_MUL = 4'd2;
  localparam logic [3:0] OP_EXP = 4'd3;
  localparam logic [3:0] OP_RECIP = 4'd4;
  localparam logic [3:0] OP_GELU = 4'd5;
  localparam logic [3:0] OP_TANH = 4'd6;
  localparam logic [3:0] OP_MAX = 4'd7;

  logic holding;
  integer i;
  integer signed av;
  integer signed bv;
  integer signed pv;
  integer signed work;

  function automatic integer signed sat16(input integer signed v);
    begin
      if (v > 32767) sat16 = 32767;
      else if (v < -32768) sat16 = -32768;
      else sat16 = v;
    end
  endfunction

  function automatic integer signed exp_approx(input integer signed v);
    integer signed z;
    begin
      // Input and output use Q1.15.  The table is monotonic and bounded.
      z = v;
      if (z <= -16384) exp_approx = 0;
      else if (z <= -8192) exp_approx = 4096;
      else if (z <= -4096) exp_approx = 8192;
      else if (z <= 0) exp_approx = 16384 + (z >>> 1);
      else if (z <= 4096) exp_approx = 16384 + (z >>> 1);
      else exp_approx = 32767;
    end
  endfunction

  function automatic integer signed reciprocal_approx(input integer signed v);
    integer signed avv;
    begin
      avv = (v < 0) ? -v : v;
      if (avv < 256) reciprocal_approx = (v < 0) ? -32768 : 32767;
      else reciprocal_approx = (v < 0) ? -((32767 <<< 8) / avv) : ((32767 <<< 8) / avv);
    end
  endfunction

  function automatic integer signed gelu_approx(input integer signed v);
    begin
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

  assign in_ready = !holding || (out_valid && out_ready);
  assign out_valid = holding;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      holding <= 1'b0;
      y <= '0;
    end else begin
      if (holding && out_ready) holding <= 1'b0;
      if (in_valid && in_ready) begin
        for (i = 0; i < LANES; i = i + 1) begin
          av = $signed(a[i*DW +: DW]);
          bv = $signed(b[i*DW +: DW]);
          pv = $signed(param);
          case (op_code)
            OP_ADD: work = av + bv;
            OP_SUB: work = av - bv;
            OP_MUL: work = (av * bv) >>> 8;
            OP_EXP: work = exp_approx(av);
            OP_RECIP: work = reciprocal_approx(av);
            OP_GELU: work = gelu_approx(av);
            OP_TANH: work = tanh_approx(av);
            OP_MAX: work = (av > bv) ? av : bv;
            default: work = av + pv;
          endcase
          y[i*DW +: DW] <= sat16(work);
        end
        holding <= 1'b1;
      end
    end
  end
endmodule
`endif
