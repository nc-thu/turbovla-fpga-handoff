// TurboVLA W8A16 multiplier: one signed INT16 activation by one signed INT8
// weight.  There is deliberately no two-lane packing in this module.  The
// valid pipeline mirrors the DSP M/P register choices, so a bubble stays
// aligned with its product.
`ifndef TVLA_W8A16_MULT_SV
`define TVLA_W8A16_MULT_SV
module w8a16_mult #(
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
  wire signed [26:0] ax = {{11{a_in[15]}}, a_in};
  wire signed [17:0] bx = {{10{w_in[7]}}, w_in};
  wire signed [47:0] product_comb = ax * bx;

  logic signed [47:0] m_pipe;
  logic signed [47:0] p_pipe;
  logic               v_m;
  logic               v_p;

`ifdef VERILATOR
  // Behavioral equivalent used for fast bit-accurate simulation.  M_REG and
  // P_REG are elaboration-time constants; the branches therefore synthesize
  // to exactly the requested number of register stages.
  always_ff @(posedge clk) begin
    if (M_REG) begin
      m_pipe <= product_comb;
      v_m <= v_in;
    end
    if (P_REG) begin
      if (M_REG) begin
        p_pipe <= m_pipe;
        v_p <= v_m;
      end else begin
        p_pipe <= product_comb;
        v_p <= v_in;
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
    .ACASCREG(0), .ADREG(0), .ALUMODEREG(0), .AMULTSEL("A"), .AREG(0),
    .AUTORESET_PATDET("NO_RESET"), .AUTORESET_PRIORITY("RESET"),
    .BCASCREG(0), .BMULTSEL("B"), .BREG(0), .B_INPUT("DIRECT"),
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
    if (M_REG) v_m <= v_in;
    if (P_REG) v_p <= M_REG ? v_m : v_in;
  end
  assign p_out = dsp_p;
  assign v_out = P_REG ? v_p : (M_REG ? v_m : v_in);
`endif
endmodule
`endif
