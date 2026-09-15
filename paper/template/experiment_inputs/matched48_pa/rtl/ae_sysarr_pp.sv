// ae_sysarr_pp.sv — 16×PCOLS Pack2 脉动阵列 + 快照双 bank 读出（hw/v8 第1件）
// ----------------------------------------------------------------------------
// 与 ae_sysarr_p2（hw/v5 H2 定版）的差别只有读出侧：
//   * PE 换 ae_pe_pp（快照双 bank，脉冲写 bank 由 PE 本地奇偶定）。
//   * acc_row 读出多一个 rd_bank 输入：drain 组 g 读 bank g%2。rd_bank 与
//     drain_row 同为引擎侧全局信号（读出时该 bank 无人写——脉冲(g+1) 写的是
//     另一半 bank，脉冲(g+2) 被"drain(g) 完成"门住）。
//   * H2 扇出治理（drain_row NREP 副本）原样保留。
// 喂数/偏斜/波前汇合语义（行 i 延 i 拍、列 j 延 j 拍、脉冲沿与 A 网同构）
// 与 ae_sysarr_p2 逐字一致。
`ifndef AE_SYSARR_PP_SV
`define AE_SYSARR_PP_SV
module ae_sysarr_pp #(
  parameter int ROWS  = 16,
  parameter int PCOLS = 4,
  parameter int REP_EACH = 4
)(
  input  logic                    clk,
  input  logic                    rst_n,
  input  logic                    clr,
  input  logic                    feed_vld,
  input  logic                    feed_pulse,
  input  logic [ROWS*8-1:0]       a_feed,
  input  logic [PCOLS*16-1:0]     b_feed,
  input  logic [((PCOLS+REP_EACH-1)/REP_EACH)*4-1:0] drain_row_rep,
  input  logic                    rd_bank,     // drain 组奇偶：读 bank A(0)/B(1)
  output logic [PCOLS*2*32-1:0]   acc_row
);
  localparam int LC = PCOLS * 2;

  logic signed [7:0] a_f [0:ROWS-1];
  logic [15:0]       b_f [0:PCOLS-1];
  always_comb begin
    for (int i = 0; i < ROWS; i++)  a_f[i] = a_feed[i*8 +: 8];
    for (int j = 0; j < PCOLS; j++) b_f[j] = b_feed[j*16 +: 16];
  end

  // ---- 边缘偏斜：行 i 延迟 i 拍、列 j 延迟 j 拍 ----
  logic signed [7:0] a_skew [0:ROWS-1];
  logic              a_v    [0:ROWS-1];
  logic [15:0]       b_skew [0:PCOLS-1];
  logic              b_v    [0:PCOLS-1];

  logic signed [7:0] adly [0:ROWS-1][0:ROWS-1];
  logic              avdly[0:ROWS-1][0:ROWS-1];
  always_ff @(posedge clk) begin
    for (int i = 0; i < ROWS; i++) begin
      adly[0][i] <= a_f[i];
      avdly[0][i] <= feed_vld;
      for (int s = 1; s < ROWS; s++) begin
        if (s <= i) begin
          adly[s][i] <= adly[s-1][i];
          avdly[s][i] <= avdly[s-1][i];
        end
      end
    end
  end
  logic [15:0] bdly [0:PCOLS-1][0:PCOLS-1];
  logic        bvdly[0:PCOLS-1][0:PCOLS-1];
  always_ff @(posedge clk) begin
    for (int j = 0; j < PCOLS; j++) begin
      bdly[0][j] <= b_f[j];
      bvdly[0][j] <= feed_vld;
      for (int s = 1; s < PCOLS; s++) begin
        if (s <= j) begin
          bdly[s][j] <= bdly[s-1][j];
          bvdly[s][j] <= bvdly[s-1][j];
        end
      end
    end
  end
  logic apdly [0:ROWS-1][0:ROWS-1];
  logic a_pulse [0:ROWS-1];
  always_ff @(posedge clk) begin
    for (int i = 0; i < ROWS; i++) begin
      apdly[0][i] <= feed_pulse;
      for (int s = 1; s < ROWS; s++) begin
        if (s <= i) apdly[s][i] <= apdly[s-1][i];
      end
    end
  end
  always_comb begin
    for (int i = 0; i < ROWS; i++) begin
      a_skew[i]  = adly[i][i];
      a_v[i]     = avdly[i][i];
      a_pulse[i] = apdly[i][i];
    end
    for (int j = 0; j < PCOLS; j++) begin
      b_skew[j] = bdly[j][j];
      b_v[j]    = bvdly[j][j];
    end
  end

  // ---- PE 阵列 ----
  logic signed [7:0]  awire [0:ROWS-1][0:PCOLS-1];
  logic [15:0]        bwire [0:ROWS-1][0:PCOLS-1];
  logic               avwire[0:ROWS-1][0:PCOLS-1];
  logic               bvwire[0:ROWS-1][0:PCOLS-1];
  logic               pwire [0:ROWS-1][0:PCOLS-1];
  logic signed [26:0] s0a[0:ROWS-1][0:PCOLS-1];
  logic signed [26:0] s0b[0:ROWS-1][0:PCOLS-1];
  logic signed [26:0] s1a[0:ROWS-1][0:PCOLS-1];
  logic signed [26:0] s1b[0:ROWS-1][0:PCOLS-1];

  logic signed [7:0]  a_in_pe [0:ROWS-1][0:PCOLS-1];
  logic [15:0]        b_in_pe [0:ROWS-1][0:PCOLS-1];
  logic               av_in_pe[0:ROWS-1][0:PCOLS-1];
  logic               bv_in_pe[0:ROWS-1][0:PCOLS-1];
  logic               pl_in_pe[0:ROWS-1][0:PCOLS-1];

  always_comb begin
    for (int i = 0; i < ROWS; i++) begin
      a_in_pe [i][0] = a_skew[i];
      av_in_pe[i][0] = a_v[i];
      pl_in_pe[i][0] = a_pulse[i];
      for (int j = 1; j < PCOLS; j++) begin
        a_in_pe [i][j] = awire [i][j-1];
        av_in_pe[i][j] = avwire[i][j-1];
        pl_in_pe[i][j] = pwire [i][j-1];
      end
    end
    for (int j = 0; j < PCOLS; j++) begin
      b_in_pe [0][j] = b_skew[j];
      bv_in_pe[0][j] = b_v[j];
      for (int i = 1; i < ROWS; i++) begin
        b_in_pe [i][j] = bwire [i-1][j];
        bv_in_pe[i][j] = bvwire[i-1][j];
      end
    end
  end

  generate
  for (genvar gi = 0; gi < ROWS; gi++) begin : g_row
    for (genvar gj = 0; gj < PCOLS; gj++) begin : g_col
      ae_pe_pp_pa u_pe (
        .clk(clk), .rst_n(rst_n),
        .clr   (clr),
        .pulse_in (pl_in_pe[gi][gj]),
        .av_in (av_in_pe[gi][gj]),
        .bv_in (bv_in_pe[gi][gj]),
        .a_in  (a_in_pe[gi][gj]),
        .b_in  (b_in_pe[gi][gj]),
        .av_out(avwire[gi][gj]),
        .bv_out(bvwire[gi][gj]),
        .pulse_out(pwire[gi][gj]),
        .a_out (awire[gi][gj]),
        .b_out (bwire[gi][gj]),
        .snap0_a(s0a[gi][gj]), .snap0_b(s0b[gi][gj]),
        .snap1_a(s1a[gi][gj]), .snap1_b(s1b[gi][gj])
      );
    end
  end
  endgenerate

  // 逻辑列读出：ℓ = 2j + lane；27b 符号扩展回 32b；bank 由 rd_bank 选
  //（脉冲写另一 bank 与本读出并行，无竞争——见 ae_gemm_pp 的脉冲门控）
  always_comb begin
    for (int j = 0; j < PCOLS; j++) begin
      acc_row[(2*j)  *32 +: 32] = rd_bank
        ? {{5{s0b[drain_row_rep[j/REP_EACH*4 +: 4]][j][26]}}, s0b[drain_row_rep[j/REP_EACH*4 +: 4]][j]}
        : {{5{s0a[drain_row_rep[j/REP_EACH*4 +: 4]][j][26]}}, s0a[drain_row_rep[j/REP_EACH*4 +: 4]][j]};
      acc_row[(2*j+1)*32 +: 32] = rd_bank
        ? {{5{s1b[drain_row_rep[j/REP_EACH*4 +: 4]][j][26]}}, s1b[drain_row_rep[j/REP_EACH*4 +: 4]][j]}
        : {{5{s1a[drain_row_rep[j/REP_EACH*4 +: 4]][j][26]}}, s1a[drain_row_rep[j/REP_EACH*4 +: 4]][j]};
    end
  end
endmodule
`endif
