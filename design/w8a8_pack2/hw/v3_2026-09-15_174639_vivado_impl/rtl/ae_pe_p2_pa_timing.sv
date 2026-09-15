// Timing-closed candidate for the TurboVLA Pack2 PE.
//
// The v1 PE had a single register at the DSP output boundary.  Its critical
// path was DSP P -> high-field carry correction -> product register.  This
// version keeps the Pack2 arithmetic unchanged, but inserts a register between
// the DSP P output and the correction logic.  The pulse used for snapshot is
// delayed by the same extra cycle.  The A/B/valid chains still have the same
// one-register systolic hop, so the array geometry and the two-MAC/DSP
// contract do not change.
`ifndef AE_PE_P2_PA_TIMING_SV
`define AE_PE_P2_PA_TIMING_SV
module ae_pe_p2_pa_timing (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   clr,
  input  logic                   pulse_in,
  input  logic                   av_in,
  input  logic                   bv_in,
  input  logic signed [7:0]      a_in,
  input  logic [15:0]            b_in,
  output logic                   av_out,
  output logic                   bv_out,
  output logic                   pulse_out,
  output logic signed [7:0]      a_out,
  output logic [15:0]            b_out,
  output logic signed [31:0]     acc0,
  output logic signed [31:0]     acc1,
  output logic signed [26:0]     snap0,
  output logic signed [26:0]     snap1
);
  // Systolic hop registers.  These remain one cycle so neighboring PEs keep
  // the original wavefront schedule.
  logic signed [7:0] a_r;
  logic [15:0]       b_r;
  logic              av_r, bv_r, pulse_r;

  logic [47:0] P;
  logic        v_p;
  pack2_mult_padd #(.M_REG(1), .P_REG(1)) u_mul (
    .clk(clk), .v_in(av_r & bv_r), .row_in(1'b0),
    .a_in(a_r), .w0_in(b_r[7:0]), .w1_in(b_r[15:8]),
    .P(P), .v_p(v_p), .row_p(), .a_p()
  );

  // New boundary: DSP P and its valid bit are first captured here.  This
  // removes the DSP-output-to-correction combinational path from the
  // accumulator-facing register boundary.
  logic [47:0] P_pipe_r;
  logic        v_p_pipe_r;
  wire signed [16:0] hi_e_pipe =
      $signed({P_pipe_r[31], P_pipe_r[31:16]}) +
      (P_pipe_r[15] ? 17'sd1 : 17'sd0);

  logic signed [15:0] prod0_r, prod1_r;
  logic               v_r;
  (* use_dsp = "no" *) logic signed [31:0] acc0_r, acc1_r;
  wire signed [31:0] prod0_ext = {{16{prod0_r[15]}}, prod0_r};
  wire signed [31:0] prod1_ext = {{16{prod1_r[15]}}, prod1_r};

  logic signed [26:0] snap0_r, snap1_r;
  logic                pulse_snap_r;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      a_r <= '0; b_r <= '0; av_r <= 1'b0; bv_r <= 1'b0; pulse_r <= 1'b0;
      P_pipe_r <= '0; v_p_pipe_r <= 1'b0;
      prod0_r <= '0; prod1_r <= '0; v_r <= 1'b0;
      pulse_snap_r <= 1'b0;
      acc0_r <= '0; acc1_r <= '0; snap0_r <= '0; snap1_r <= '0;
    end else begin
      // Systolic data/control hop.
      a_r <= a_in; b_r <= b_in; av_r <= av_in; bv_r <= bv_in;
      pulse_r <= pulse_in;

      // DSP-output pipeline stage.
      P_pipe_r <= P;
      v_p_pipe_r <= v_p;

      // Registered Pack2 field extraction and borrow correction.
      prod0_r <= $signed(P_pipe_r[15:0]);
      prod1_r <= hi_e_pipe[15:0];
      v_r <= v_p_pipe_r;

      // Match the extra product stage before taking a snapshot.  pulse_out
      // intentionally remains the one-cycle systolic hop for the next PE.
      pulse_snap_r <= pulse_in;
      if (pulse_snap_r) begin
        snap0_r <= acc0_r[26:0];
        snap1_r <= acc1_r[26:0];
        acc0_r <= '0;
        acc1_r <= '0;
      end else if (clr) begin
        acc0_r <= '0;
        acc1_r <= '0;
      end else if (v_r) begin
        acc0_r <= acc0_r + prod0_ext;
        acc1_r <= acc1_r + prod1_ext;
      end
    end
  end

  assign a_out = a_r;
  assign b_out = b_r;
  assign av_out = av_r;
  assign bv_out = bv_r;
  assign pulse_out = pulse_r;
  assign acc0 = acc0_r;
  assign acc1 = acc1_r;
  assign snap0 = snap0_r;
  assign snap1 = snap1_r;
endmodule
`endif
