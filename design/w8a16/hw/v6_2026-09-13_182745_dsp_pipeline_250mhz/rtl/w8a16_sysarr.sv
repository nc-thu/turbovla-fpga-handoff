// 16×48 W8A16 systolic array.  One INT16 activation travels east and one
// INT8 weight travels south.  Each PE owns one DSP and one accumulation state.
`ifndef TVLA_W8A16_SYSARR_SV
`define TVLA_W8A16_SYSARR_SV
module w8a16_sysarr #(
  parameter int ROWS = 16,
  parameter int PCOLS = 48,
  parameter int ACC_W = 40
)(
  input  logic                         clk,
  input  logic                         rst_n,
  input  logic                         clr,
  input  logic                         feed_vld,
  input  logic                         feed_pulse,
  input  logic [ROWS*16-1:0]           a_feed,
  input  logic [PCOLS*8-1:0]            b_feed,
  input  logic [((ROWS <= 1) ? 1 : $clog2(ROWS))-1:0] drain_row,
  output logic [PCOLS*ACC_W-1:0]      snap_row
);
  logic signed [15:0] a_f [0:ROWS-1];
  logic signed [7:0]  b_f [0:PCOLS-1];
  integer i, j, s;
  always_comb begin
    for (i = 0; i < ROWS; i = i + 1) a_f[i] = a_feed[i*16 +: 16];
    for (j = 0; j < PCOLS; j = j + 1) b_f[j] = b_feed[j*8 +: 8];
  end

  logic signed [15:0] adly [0:ROWS-1][0:ROWS-1];
  logic               avdly[0:ROWS-1][0:ROWS-1];
  logic signed [7:0]  bdly [0:PCOLS-1][0:PCOLS-1];
  logic               bvdly[0:PCOLS-1][0:PCOLS-1];
  logic               pdly [0:ROWS-1][0:ROWS-1];
  logic signed [15:0] a_skew [0:ROWS-1];
  logic               a_v [0:ROWS-1];
  logic signed [7:0]  b_skew [0:PCOLS-1];
  logic               b_v [0:PCOLS-1];
  logic               p_skew [0:ROWS-1];

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      for (i = 0; i < ROWS; i = i + 1) begin
        for (s = 0; s < ROWS; s = s + 1) begin
          adly[s][i] <= '0;
          avdly[s][i] <= 1'b0;
          pdly[s][i] <= 1'b0;
        end
      end
      for (j = 0; j < PCOLS; j = j + 1) begin
        for (s = 0; s < PCOLS; s = s + 1) begin
          bdly[s][j] <= '0;
          bvdly[s][j] <= 1'b0;
        end
      end
    end else begin
      for (i = 0; i < ROWS; i = i + 1) begin
        adly[0][i] <= a_f[i];
        avdly[0][i] <= feed_vld;
        pdly[0][i] <= feed_pulse;
        for (s = 1; s < ROWS; s = s + 1) begin
          if (s <= i) begin
            adly[s][i] <= adly[s-1][i];
            avdly[s][i] <= avdly[s-1][i];
            pdly[s][i] <= pdly[s-1][i];
          end
        end
      end
      for (j = 0; j < PCOLS; j = j + 1) begin
        bdly[0][j] <= b_f[j];
        bvdly[0][j] <= feed_vld;
        for (s = 1; s < PCOLS; s = s + 1) begin
          if (s <= j) begin
            bdly[s][j] <= bdly[s-1][j];
            bvdly[s][j] <= bvdly[s-1][j];
          end
        end
      end
    end
  end
  always_comb begin
    for (i = 0; i < ROWS; i = i + 1) begin
      a_skew[i] = adly[i][i];
      a_v[i] = avdly[i][i];
      p_skew[i] = pdly[i][i];
    end
    for (j = 0; j < PCOLS; j = j + 1) begin
      b_skew[j] = bdly[j][j];
      b_v[j] = bvdly[j][j];
    end
  end

  logic signed [15:0] awire [0:ROWS-1][0:PCOLS-1];
  logic signed [7:0]  bwire [0:ROWS-1][0:PCOLS-1];
  logic               avwire[0:ROWS-1][0:PCOLS-1];
  logic               bvwire[0:ROWS-1][0:PCOLS-1];
  logic               pwire [0:ROWS-1][0:PCOLS-1];
  logic signed [ACC_W-1:0] snaps[0:ROWS-1][0:PCOLS-1];
  logic signed [15:0] a_in_pe [0:ROWS-1][0:PCOLS-1];
  logic signed [7:0]  b_in_pe [0:ROWS-1][0:PCOLS-1];
  logic               av_in_pe[0:ROWS-1][0:PCOLS-1];
  logic               bv_in_pe[0:ROWS-1][0:PCOLS-1];
  logic               pl_in_pe[0:ROWS-1][0:PCOLS-1];

  always_comb begin
    for (i = 0; i < ROWS; i = i + 1) begin
      a_in_pe[i][0] = a_skew[i];
      av_in_pe[i][0] = a_v[i];
      pl_in_pe[i][0] = p_skew[i];
      for (j = 1; j < PCOLS; j = j + 1) begin
        a_in_pe[i][j] = awire[i][j-1];
        av_in_pe[i][j] = avwire[i][j-1];
        pl_in_pe[i][j] = pwire[i][j-1];
      end
    end
    for (j = 0; j < PCOLS; j = j + 1) begin
      b_in_pe[0][j] = b_skew[j];
      bv_in_pe[0][j] = b_v[j];
      for (i = 1; i < ROWS; i = i + 1) begin
        b_in_pe[i][j] = bwire[i-1][j];
        bv_in_pe[i][j] = bvwire[i-1][j];
      end
    end
  end

  genvar gi, gj;
  generate
    for (gi = 0; gi < ROWS; gi = gi + 1) begin : g_row
      for (gj = 0; gj < PCOLS; gj = gj + 1) begin : g_col
        w8a16_pe #(.ACC_W(ACC_W)) u_pe (
          .clk(clk), .rst_n(rst_n), .clr(clr), .pulse_in(pl_in_pe[gi][gj]),
          .av_in(av_in_pe[gi][gj]), .bv_in(bv_in_pe[gi][gj]),
          .a_in(a_in_pe[gi][gj]), .b_in(b_in_pe[gi][gj]),
          .av_out(avwire[gi][gj]), .bv_out(bvwire[gi][gj]),
          .pulse_out(pwire[gi][gj]),
          .a_out(awire[gi][gj]), .b_out(bwire[gi][gj]),
          .acc(), .snap(snaps[gi][gj])
        );
      end
    end
  endgenerate

  always_comb begin
    for (j = 0; j < PCOLS; j = j + 1)
      snap_row[j*ACC_W +: ACC_W] = snaps[drain_row][j];
  end
endmodule
`endif
