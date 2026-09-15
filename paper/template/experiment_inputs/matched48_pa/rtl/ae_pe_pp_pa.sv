// ae_pe_pp_pa.sv — Pack2 脉动 PE + 快照双 bank + 预加器乘法核（hw/v10）
// ----------------------------------------------------------------------------
// = ae_pe_pp（hw/v8 第1件，pp/p2d 两引擎共用）换装 hw/v9 预加器乘法核：
//   * 乘法核 pack2_mult_dsp -> pack2_mult_padd（DSP 预加器吃掉 -128·(2^16+1)
//     打包偏置，P 已是真值积；AMULTSEL=AD / INMODE=00100 / DREG=ADREG=0，
//     流水深度不变）；
//   * stage1 删掉两路 -128·a 校正减法，只剩字段抽取 + 高场借位：
//       prod0 = signed(P[15:0])
//       prod1 = signed(P[31:16]) + P[15]
// 快照双 bank / par_r 奇偶 / 累加 / 脉冲 / 清零语义与 ae_pe_pp 逐拍相同。
// 数值边界同 v9 记录：27b 快照在 K=4096 全 (-128)×(-128) 时 +2^26 恰回绕
// （基线同语义，不改）。
`ifndef AE_PE_PP_PA_SV
`define AE_PE_PP_PA_SV
module ae_pe_pp_pa (
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
  // ---- 脉动链寄存（与 ae_pe_pp 同构；b 链 16b）----
  logic signed [7:0] a_r;
  logic [15:0]       b_r;
  logic              av_r, bv_r, pulse_r;

  // ---- Pack2 乘法（预加器版；Verilator 下自动换位精确行为模型）----
  logic [47:0] P;
  logic        v_p;
  pack2_mult_padd #(.M_REG(1), .P_REG(1)) u_mul (
    .clk(clk), .v_in(av_r & bv_r), .row_in(1'b0),
    .a_in(a_r), .w0_in(b_r[7:0]), .w1_in(b_r[15:8]),
    .P(P), .v_p(v_p), .row_p(), .a_p()      // a_p 校正不再需要，不接
  );

  // ---- stage1：字段抽取 + 高场借位（无 -128·a 校正）----
  wire signed [16:0] hi_e = $signed({P[31], P[31:16]}) + (P[15] ? 17'sd1 : 17'sd0);
  logic signed [15:0] prod0_r, prod1_r;
  logic               v_r;

  // ---- stage2：2× 32b 累加（单 bank，与 ae_pe_pp 相同）----
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
      prod0_r <= $signed(P[15:0]);
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
