// One-cycle command wrapper for the non-GEMM vector instructions.
// It shares the standalone activation primitives so that the compiler's
// BIAS_ADD/ADD/MUL_SCALE/RELU/GELU/TANH/LAYER_NORM/SOFTMAX operations have a
// common handshake and a single place to account for their latency.
`ifndef TVLA_W8A16_VECTOR_OPS_SV
`define TVLA_W8A16_VECTOR_OPS_SV
module w8a16_vector_ops #(parameter int N = 16) (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   start,
  input  logic [3:0]             op,
  input  logic signed [N*16-1:0] x,
  input  logic signed [N*16-1:0] aux,
  input  logic signed [15:0]     scale,
  output logic signed [N*16-1:0] y,
  output logic                   out_valid,
  output logic                   done
);
  localparam logic [3:0] OP_BIAS = 4'd0;
  localparam logic [3:0] OP_ADD = 4'd1;
  localparam logic [3:0] OP_MUL = 4'd2;
  localparam logic [3:0] OP_RELU = 4'd3;
  localparam logic [3:0] OP_GELU = 4'd4;
  localparam logic [3:0] OP_TANH = 4'd5;
  localparam logic [3:0] OP_LN = 4'd6;
  localparam logic [3:0] OP_SOFTMAX = 4'd7;

  logic signed [N*16-1:0] y_relu, y_gelu, y_tanh, y_ln;
  logic [N*16-1:0] y_softmax;
  logic signed [N*16-1:0] y_mul;
  logic signed [N*16-1:0] selected;
  w8a16_relu #(.N(N)) u_relu(.x(x), .y(y_relu));
  w8a16_gelu #(.N(N)) u_gelu(.x(x), .y(y_gelu));
  w8a16_tanh #(.N(N)) u_tanh(.x(x), .y(y_tanh));
  w8a16_layernorm #(.N(N)) u_ln(.clk(clk), .rst_n(rst_n), .in_vld(1'b0), .x(x), .out_vld(), .y(y_ln));
  w8a16_softmax #(.N(N)) u_softmax(.clk(clk), .rst_n(rst_n), .in_vld(1'b0), .x(x), .out_vld(), .y(y_softmax));
  w8a16_vector_mul #(.N(N)) u_mul(.x(x), .scale(scale), .y(y_mul));

  integer i;
  integer signed sum;
  always_comb begin
    // Saturating add is deliberately kept here instead of using a wrapping
    // vector '+'; residual overflow must be visible to the numeric contract.
    selected = '0;
    sum = 0;
    case (op)
      OP_BIAS, OP_ADD: begin
        for (i = 0; i < N; i = i + 1) begin
          sum = $signed(x[i*16 +: 16]) + $signed(aux[i*16 +: 16]);
          if (sum > 32767) selected[i*16 +: 16] = 16'sh7fff;
          else if (sum < -32768) selected[i*16 +: 16] = -16'sh8000;
          else selected[i*16 +: 16] = sum[15:0];
        end
      end
      OP_MUL: selected = y_mul;
      OP_RELU: selected = y_relu;
      OP_GELU: selected = y_gelu;
      OP_TANH: selected = y_tanh;
      OP_LN: selected = y_ln;
      OP_SOFTMAX: selected = $signed(y_softmax);
      default: selected = x;
    endcase
  end

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      y <= '0;
      out_valid <= 1'b0;
      done <= 1'b0;
    end else begin
      out_valid <= start;
      done <= start;
      if (start) y <= selected;
    end
  end
endmodule
`endif
