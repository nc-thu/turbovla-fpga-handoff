// ae_pe_pp.sv — Pack2 脉动 PE + 快照双 bank（hw/v8 第1件"累加器乒乓"）
// ----------------------------------------------------------------------------
// 与 ae_pe_p2（hw/v5 H1 门定版）的唯一差别：快照寄存器翻倍成 A/B 两个 bank，
// 每个 PE 本地维护一个奇偶位 par_r，脉冲到拍写 snap[par_r] 后翻转。
// 动机（arch v8 三层拆账的"排队层"45.0M 拍）：原版快照单 bank，脉冲(g+1)
// 必须等 drain(g) 读到第 12 行才敢发射（逃生舱条款），读出链 drain→写回又是
// 串行单 tile_buf —— 行组稳态周期被 max(k+2, 68+wb) 卡住。双 bank 后脉冲(g+1)
// 只需 drain(g-1) 整体读完（那半边快照再无人读），读出链拆成 drain / 写回
// 两级流水（双 tile_buf，见 ae_gemm_pp.sv），稳态周期降为
// max(k+2, 64+DALIGN+LAT, wb)——requant 套数不加倍时的物理下限。
// 其余（链寄存 / pack2_mult_dsp 6 拍积落地 / 脉冲快照语义 / 27b 口径）
// 与 ae_pe_p2 逐字一致。par_r 由 clr（描述符起点的 arr_clr 单拍）同步复位：
// 全阵列所有 PE 同拍清零，与引擎侧 gd[0]（drain 组序号奇偶）对齐——
// 组 g 的快照必落在 bank g%2，两边奇偶永不失步（每个脉冲每 PE 恰好见一次）。
`ifndef AE_PE_PP_SV
`define AE_PE_PP_SV
module ae_pe_pp (
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
  output logic signed [26:0]     snap0_a,   // 逻辑列 2j 快照 bank A（组偶）
  output logic signed [26:0]     snap0_b,   //            bank B（组奇）
  output logic signed [26:0]     snap1_a,   // 逻辑列 2j+1 快照 bank A
  output logic signed [26:0]     snap1_b    //            bank B
);
  // ---- 脉动链寄存（与 ae_pe_p2 同构；b 链 16b）----
  logic signed [7:0] a_r;
  logic [15:0]       b_r;
  logic              av_r, bv_r, pulse_r;

  // ---- Pack2 乘法（显式 DSP48E2；Verilator 下自动换位精确行为模型）----
  logic [47:0] P;
  logic        v_p;
  logic signed [7:0] a_p;
  pack2_mult_dsp #(.M_REG(1), .P_REG(1)) u_mul (
    .clk(clk), .v_in(av_r & bv_r), .row_in(1'b0),
    .a_in(a_r), .w0_in(b_r[7:0]), .w1_in(b_r[15:8]),
    .P(P), .v_p(v_p), .row_p(), .a_p(a_p)
  );

  // ---- stage1：packed field 抽取/偏置校正 -> 16b 真实有符号积 ----
  wire signed [15:0] corr = a_p <<< 7;
  wire signed [17:0] lo_e = $signed({{2{P[15]}}, P[15:0]}) - corr;
  wire signed [17:0] hi_e = $signed({{2{P[31]}}, P[31:16]})
                            + (P[15] ? 18'sd1 : 18'sd0) - corr;
  logic signed [15:0] prod0_r, prod1_r;
  logic               v_r;

  // ---- stage2：2× 32b 累加（单 bank——脉冲清 acc 后下一组立刻从零积累，
  //      在飞积不受清零影响；需要双 bank 的是快照侧，不是累加器侧）----
  (* use_dsp = "no" *) logic signed [31:0] acc0_r, acc1_r;
  wire signed [31:0] prod0_ext = {{16{prod0_r[15]}}, prod0_r};
  wire signed [31:0] prod1_ext = {{16{prod1_r[15]}}, prod1_r};

  // ---- 快照双 bank + 本地奇偶 ----
  logic signed [26:0] s0a_r, s0b_r, s1a_r, s1b_r;
  logic               par_r;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      a_r <= '0; b_r <= '0; av_r <= 1'b0; bv_r <= 1'b0; pulse_r <= 1'b0;
      prod0_r <= '0; prod1_r <= '0; v_r <= 1'b0;
      acc0_r <= '0; acc1_r <= '0;
      s0a_r <= '0; s0b_r <= '0; s1a_r <= '0; s1b_r <= '0;
      par_r <= 1'b0;
    end else begin
      a_r <= a_in;  b_r <= b_in;
      av_r <= av_in; bv_r <= bv_in;
      pulse_r <= pulse_in;
      prod0_r <= lo_e[15:0];
      prod1_r <= hi_e[15:0];
      v_r     <= v_p;
      if (pulse_in) begin
        // 快照拍：acc 已含本组全部积（操作数 ≤ t_p-6），写 par_r 指向的 bank
        if (!par_r) begin
          s0a_r <= acc0_r[26:0];
          s1a_r <= acc1_r[26:0];
        end else begin
          s0b_r <= acc0_r[26:0];
          s1b_r <= acc1_r[26:0];
        end
        acc0_r <= '0;
        acc1_r <= '0;
        par_r  <= ~par_r;
      end else if (clr) begin
        acc0_r <= '0; acc1_r <= '0;
        par_r  <= 1'b0;          // 描述符起点：全阵列奇偶对齐到 bank A = 组 0
      end else if (v_r) begin
        acc0_r <= acc0_r + prod0_ext;
        acc1_r <= acc1_r + prod1_ext;
      end
    end
  end
  assign a_out = a_r;    assign av_out = av_r;
  assign b_out = b_r;    assign bv_out = bv_r;
  assign pulse_out = pulse_r;
  assign snap0_a = s0a_r; assign snap0_b = s0b_r;
  assign snap1_a = s1a_r; assign snap1_b = s1b_r;
endmodule
`endif
