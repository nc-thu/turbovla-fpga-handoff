`timescale 1ns/1ps
// One signed INT8xINT8 product mapped explicitly to one DSP48E2 in hardware.
// Verilator sees the mathematically identical multiply for fast RTL checks.
module w8a8_dsp_mult (
    input  logic signed [7:0]  a_in,
    input  logic signed [7:0]  w_in,
    output logic signed [31:0] p_out
);
    wire signed [26:0] ax = {{19{a_in[7]}}, a_in};
    wire signed [17:0] bx = {{10{w_in[7]}}, w_in};
`ifdef VERILATOR
    always_comb p_out = $signed(a_in) * $signed(w_in);
`else
    wire signed [47:0] dsp_p;
    DSP48E2 #(
        .ACASCREG(0), .ADREG(0), .ALUMODEREG(0), .AMULTSEL("A"), .AREG(0),
        .AUTORESET_PATDET("NO_RESET"), .AUTORESET_PRIORITY("RESET"),
        .BCASCREG(0), .BMULTSEL("B"), .BREG(0), .B_INPUT("DIRECT"),
        .CARRYINREG(0), .CARRYINSELREG(0), .CREG(0), .DREG(0),
        .INMODEREG(0), .MREG(0), .OPMODEREG(0), .PREG(0),
        .PREADDINSEL("A"), .USE_MULT("MULTIPLY"), .USE_SIMD("ONE48"),
        .USE_PATTERN_DETECT("NO_PATDET")
    ) u_dsp (
        .CLK(1'b0), .A(ax), .B(bx), .C(48'b0), .D(27'b0),
        .ACIN(30'b0), .BCIN(18'b0), .PCIN(48'b0),
        .ALUMODE(4'b0000), .INMODE(5'b00000), .OPMODE(9'b000000101),
        .CARRYIN(1'b0), .CARRYINSEL(3'b000), .CARRYCASCIN(1'b0),
        .MULTSIGNIN(1'b0), .CEA1(1'b0), .CEA2(1'b0), .CEAD(1'b0),
        .CEALUMODE(1'b0), .CEB1(1'b0), .CEB2(1'b0), .CEC(1'b0),
        .CECARRYIN(1'b0), .CECTRL(1'b0), .CED(1'b0), .CEINMODE(1'b0),
        .CEM(1'b0), .CEP(1'b0), .RSTA(1'b0), .RSTALLCARRYIN(1'b0),
        .RSTALUMODE(1'b0), .RSTB(1'b0), .RSTC(1'b0), .RSTCTRL(1'b0),
        .RSTD(1'b0), .RSTINMODE(1'b0), .RSTM(1'b0), .RSTP(1'b0), .P(dsp_p)
    );
    always_comb p_out = dsp_p[31:0];
`endif
endmodule
