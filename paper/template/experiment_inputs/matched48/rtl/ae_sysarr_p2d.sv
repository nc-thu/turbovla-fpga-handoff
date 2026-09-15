// ae_sysarr_p2d.sv — 16×PCOLS Pack2 脉动阵列（2× 核心时钟域）+ 双 a 喂数
// （hw/v8 第3件"A 双 bank"：喂数 k/2，长 K 利用率 50% 界的电路件）
// ----------------------------------------------------------------------------
// 结构：本模块整体运行在 cclk（接口时钟 clk 的 2 倍频，相位对齐）；喂数/读出
// 的跨域全是"准静态电平"或"计数+应答"两种安全形态：
//   * 喂数：接口侧每拍备好一对切片（a_feed0/1、b_feed0/1，clk 域寄存后整拍
//     稳定），内部用 sel = ~ph1 选片——ph1 就是接口时钟本身的电平：接口拍
//     前半 sel=0 呈交偶切片、后半 sel=1 呈交奇切片。cclk 边沿各采一次，
//     切片序号 s 恰好一步一个（切片 s 在 cclk 步 u=s 呈交，脉动语义与
//     ae_sysarr_p2 的"每接口拍一片"完全同构，只是片率×2）。
//   * 脉冲：接口 FSM 不直接发脉冲，只给 last_even/last_odd（末切片呈交拍
//     有效 1 个接口拍）。内部在末切片呈交的那个 cclk 步起倒计数
//     PULSE_DLY2 步后把脉冲注入偏斜网（窗口校准同 p2 的 PD∈{5,6}，单位
//     换成 cclk 步）。
//   * 读出：sweep 事件（脉冲扫过行 0 全列）用 cclk 域 2bit 饱和计数
//     swept_cnt（到达 +1 / 应答 -1，同拍相抵——hw/v7 F2 的计数语义搬到
//     cclk 域；应答 evt_ack 是接口拍宽电平，用上升沿检测只减一次）。
//     接口侧 drain FSM 消费 sweep_avail，读快照（bank g%2，双 bank 乒乓
//     保证读时无人写，快照值在 64 拍读出窗内准静态）。
// 快照双 bank / drain_row 副本 / 逻辑列展平读出与 ae_sysarr_pp 一致。
`ifndef AE_SYSARR_P2D_SV
`define AE_SYSARR_P2D_SV
module ae_sysarr_p2d #(
  parameter int ROWS  = 16,
  parameter int PCOLS = 4,
  parameter int REP_EACH = 4,
  parameter int PULSE_DLY2 = 6        // 末切片呈交步 -> 脉冲注入步（cclk 步数）
)(
  input  logic                    cclk,       // 2× 核心时钟
  input  logic                    ph1,        // 接口时钟电平（选片相位锚）
  input  logic                    rst_n,
  input  logic                    clr,        // 接口拍宽（arr_clr）：PE 奇偶复位
  input  logic [ROWS*8-1:0]       a_feed0,    // 偶切片（16 行激活）
  input  logic [ROWS*8-1:0]       a_feed1,    // 奇切片
  input  logic [PCOLS*16-1:0]     b_feed0,
  input  logic [PCOLS*16-1:0]     b_feed1,
  input  logic                    feed_vld0,  // 本接口拍偶切片有效
  input  logic                    feed_vld1,  // 本接口拍奇切片有效（k 奇的末对为 0）
  input  logic                    last_even,  // 本接口拍的 step0 切片是组末切片
  input  logic                    last_odd,   // 本接口拍的 step1 切片是组末切片
  output logic                    sweep_avail,// cclk 域计数 != 0（接口侧准静态读）
  input  logic                    evt_ack,    // 接口拍宽：已消费一个 sweep 事件
  input  logic [((PCOLS+REP_EACH-1)/REP_EACH)*4-1:0] drain_row_rep,
  input  logic                    rd_bank,
  output logic [PCOLS*2*32-1:0]   acc_row
);
  localparam int LC = PCOLS * 2;

  // ---- 选片与喂数（sel=0 偶切片呈交窗 / sel=1 奇切片呈交窗）----
  wire sel = ~ph1;
  logic signed [7:0] a_f [0:ROWS-1];
  logic [15:0]       b_f [0:PCOLS-1];
  logic              feed_vld;
  always_comb begin
    for (int i = 0; i < ROWS; i++)  a_f[i] = sel ? a_feed1[i*8 +: 8] : a_feed0[i*8 +: 8];
    for (int j = 0; j < PCOLS; j++) b_f[j] = sel ? b_feed1[j*16 +: 16] : b_feed0[j*16 +: 16];
    feed_vld = sel ? feed_vld1 : feed_vld0;
  end

  // ---- 脉冲发生：末切片呈交步起倒计数 PULSE_DLY2 步注入 ----
  // 末切片呈交步 = last_even 的 sel=0 步 / last_odd 的 sel=1 步（标记整个
  // 接口拍都高，但只有匹配 sel 的那个 cclk 步是呈交步，天然只武装一次）。
  logic [2:0]         pd_cnt;
  logic               pd_run, pulse_inj;
  wire arm = (last_even && !sel && feed_vld0) || (last_odd && sel && feed_vld1);
  always_ff @(posedge cclk or negedge rst_n) begin
    if (!rst_n) begin
      pd_run <= 1'b0; pd_cnt <= '0; pulse_inj <= 1'b0;
    end else begin
      pulse_inj <= 1'b0;
      if (arm && !pd_run) begin
        pd_run <= 1'b1;
        pd_cnt <= PULSE_DLY2[2:0];
      end else if (pd_run) begin
        if (pd_cnt == 3'd1) begin
          pulse_inj <= 1'b1;
          pd_run    <= 1'b0;
        end else pd_cnt <= pd_cnt - 3'd1;
      end
    end
  end

  // ---- 边缘偏斜（全部 cclk 域；行 i 延 i 步、列 j 延 j 步——单位是 cclk）----
  logic signed [7:0] a_skew [0:ROWS-1];
  logic              a_v    [0:ROWS-1];
  logic [15:0]       b_skew [0:PCOLS-1];
  logic              b_v    [0:PCOLS-1];

  logic signed [7:0] adly [0:ROWS-1][0:ROWS-1];
  logic              avdly[0:ROWS-1][0:ROWS-1];
  always_ff @(posedge cclk) begin
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
  always_ff @(posedge cclk) begin
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
  always_ff @(posedge cclk) begin
    for (int i = 0; i < ROWS; i++) begin
      apdly[0][i] <= pulse_inj;
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

  // ---- PE 阵列（ae_pe_pp 原样复用，时钟换 cclk）----
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
      ae_pe_pp u_pe (
        .clk(cclk), .rst_n(rst_n),
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

  // ---- sweep 事件计数（cclk 域 2bit 饱和；应答按接口拍上升沿只减一次）----
  logic [PCOLS:0] ptap2;
  logic [1:0]     swept_cnt;
  logic           ack2;
  wire            ack_rise = evt_ack && !ack2;
  always_ff @(posedge cclk or negedge rst_n) begin
    if (!rst_n) begin
      ptap2 <= '0; swept_cnt <= 2'd0; ack2 <= 1'b0;
    end else begin
      ptap2 <= {ptap2[PCOLS-1:0], pulse_inj};
      ack2  <= evt_ack;
      if (ptap2[PCOLS] && !ack_rise) begin
        if (swept_cnt != 2'd3) swept_cnt <= swept_cnt + 2'd1;
      end else if (!ptap2[PCOLS] && ack_rise) swept_cnt <= swept_cnt - 2'd1;
    end
  end
  assign sweep_avail = (swept_cnt != 2'd0);

  // ---- 逻辑列读出（comb，接口侧 clk 采样；bank = rd_bank）----
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
