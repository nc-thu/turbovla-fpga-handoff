// TurboVLA W8A16 multiplier: one signed INT16 activation by one signed INT8
// weight.  There is deliberately no two-lane packing in this module.  The
// valid pipeline mirrors the DSP M/P register choices, so a bubble stays
// aligned with its product.
`ifndef TVLA_W8A16_MULT_SV
`define TVLA_W8A16_MULT_SV
module w8a16_mult #(
  // Keep one explicit register on each DSP input.  The old v4/v5 primitive
  // left A and B combinational at the DSP boundary, which is exactly the
  // DPIP warning and a large part of the long routed path.  These parameters
  // are kept visible so an OOC experiment can turn a boundary off, although
  // the production PE uses A_REG=B_REG=1.
  parameter int A_REG = 1,
  parameter int B_REG = 1,
  parameter int M_REG = 1,
  parameter int P_REG = 1
)(
  input  logic                   clk,
  input  logic                   v_in,
  input  logic signed [15:0]     a_in,
  input  logic signed [7:0]      w_in,
  output logic signed [47:0]     p_out,
  output logic                   v_out
);
  logic signed [15:0] a_pipe;
  logic signed [7:0]  b_pipe;
  logic               v_a;
  logic               v_b;
`ifdef VERILATOR
  wire signed [15:0] a_stage = A_REG ? a_pipe : a_in;
  wire signed [7:0]  b_stage = B_REG ? b_pipe : w_in;
`else
  // In hardware the DSP's own AREG/BREG are the input boundary.  Keeping the
  // external simulation registers out of this expression avoids adding a
  // second physical stage; the shared valid pipeline below still models that
  // primitive latency.
  wire signed [15:0] a_stage = a_in;
  wire signed [7:0]  b_stage = w_in;
`endif
  wire               v_a_stage = A_REG ? v_a : v_in;
  wire               v_b_stage = B_REG ? v_b : v_in;
  wire               v_stage = v_a_stage & v_b_stage;
  wire signed [26:0] ax = {{11{a_stage[15]}}, a_stage};
  wire signed [17:0] bx = {{10{b_stage[7]}}, b_stage};
  wire signed [47:0] product_comb = ax * bx;

  logic signed [47:0] m_pipe;
  logic signed [47:0] p_pipe;
  logic               v_m;
  logic               v_p;

  // This block is shared by simulation and the primitive implementation.  It
  // is deliberately separate from the product pipeline so that the RTL and
  // the DSP48E2 AREG/BREG settings have the same transaction boundary.
  always_ff @(posedge clk) begin
    a_pipe <= a_in;
    b_pipe <= w_in;
    v_a <= v_in;
    v_b <= v_in;
  end

`ifdef VERILATOR
  // Behavioral equivalent used for fast bit-accurate simulation.  The input
  // registers model DSP AREG/BREG, while m_pipe/p_pipe model MREG/PREG.  A
  // valid bit follows every stage, so bubbles remain attached to products.
  always_ff @(posedge clk) begin
    if (M_REG) begin
      m_pipe <= product_comb;
      v_m <= v_stage;
    end
    if (P_REG) begin
      if (M_REG) begin
        p_pipe <= m_pipe;
        v_p <= v_m;
      end else begin
        p_pipe <= product_comb;
        v_p <= v_stage;
      end
    end
  end
  generate
    if (P_REG) begin : g_ver_p
      assign p_out = p_pipe;
      assign v_out = v_p;
    end else if (M_REG) begin : g_ver_m
      assign p_out = m_pipe;
      assign v_out = v_m;
    end else begin : g_ver_comb
      assign p_out = product_comb;
      assign v_out = v_in;
    end
  endgenerate
`else
  // Hardware implementation.  DSP48E2 performs the signed product; its MREG
  // and PREG parameters are kept in the same configuration as the valid
  // pipeline above.  The result is wider than the PE's 40-bit accumulator,
  // and the PE performs the checked sign extension.
  wire signed [47:0] dsp_p;
  DSP48E2 #(
    .ACASCREG(A_REG), .ADREG(0), .ALUMODEREG(0), .AMULTSEL("A"), .AREG(A_REG),
    .AUTORESET_PATDET("NO_RESET"), .AUTORESET_PRIORITY("RESET"),
    .BCASCREG(B_REG), .BMULTSEL("B"), .BREG(B_REG), .B_INPUT("DIRECT"),
    .CARRYINREG(0), .CARRYINSELREG(0), .CREG(0), .DREG(0), .INMODEREG(0),
    .MREG(M_REG), .OPMODEREG(0), .PREG(P_REG), .PREADDINSEL("A"),
    .USE_MULT("MULTIPLY"), .USE_SIMD("ONE48"), .USE_PATTERN_DETECT("NO_PATDET")
  ) u_dsp (
    .CLK(clk), .A(ax), .B(bx), .C(48'b0), .D(27'b0),
    .ACIN(30'b0), .BCIN(18'b0), .PCIN(48'b0),
    .ALUMODE(4'b0000), .INMODE(5'b00000), .OPMODE(9'b000000101),
    .CARRYIN(1'b0), .CARRYINSEL(3'b000), .CARRYCASCIN(1'b0), .MULTSIGNIN(1'b0),
    .CEA1(1'b1), .CEA2(1'b1), .CEAD(1'b1), .CEALUMODE(1'b1),
    .CEB1(1'b1), .CEB2(1'b1), .CEC(1'b1), .CECARRYIN(1'b1), .CECTRL(1'b1),
    .CED(1'b1), .CEINMODE(1'b1), .CEM(1'b1), .CEP(1'b1),
    .RSTA(1'b0), .RSTALLCARRYIN(1'b0), .RSTALUMODE(1'b0), .RSTB(1'b0),
    .RSTC(1'b0), .RSTCTRL(1'b0), .RSTD(1'b0), .RSTINMODE(1'b0),
    .RSTM(1'b0), .RSTP(1'b0), .P(dsp_p)
  );
  always_ff @(posedge clk) begin
    if (M_REG) v_m <= v_stage;
    if (P_REG) v_p <= M_REG ? v_m : v_stage;
  end
  assign p_out = dsp_p;
  assign v_out = P_REG ? v_p : (M_REG ? v_m : v_in);
`endif
endmodule
`endif
