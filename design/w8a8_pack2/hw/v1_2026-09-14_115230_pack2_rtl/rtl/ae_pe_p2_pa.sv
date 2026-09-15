// ae_pe_p2_pa.sv — Pack2 脉动 PE（预加器候选版）：与基线 ae_pe_p2 逐端口相同，
// ----------------------------------------------------------------------------
// 唯一差异在乘法核与 stage1 校正：
//   * 乘法核换 pack2_mult_padd（DSP 预加器吃掉 -128·(2^16+1) 偏置，P 已是真值积）；
//   * stage1 删掉两路 -128·a 校正减法，只剩字段抽取 + 高场借位：
//       prod0 = signed(P[15:0])
//       prod1 = signed(P[31:16]) + P[15]
// 其余（脉动链、流水深度、快照/清零/脉冲时序、累加器位宽）与基线逐拍相同。
//
// 数值边界（与基线完全一致的既有问题，本实验不改）：
//   |acc| ≤ K·16384，K=4096 且全为 (-128)×(-128) 时 = 2^26，超出 signed27 上限
//   2^26−1 恰好 1——27b 快照在该极端下回绕。基线同此（其注释"27b 无损"不成立，
//   已记录在 v9 报告；两版行为一致，由差分对拍背书）。
`ifndef AE_PE_P2_PA_SV
`define AE_PE_P2_PA_SV
module ae_pe_p2_pa (
  input  logic                   clk,
  input  logic                   rst_n,
  input  logic                   clr,      // 累加器清零（描述符起点幂等发一次；行组清零靠末脉冲）
  input  logic                   pulse_in, // R3C 末脉冲（西侧进入；快照拍 = 本 PE 窗口内）
  input  logic                   av_in,
  input  logic                   bv_in,
  input  logic signed [7:0]      a_in,     // 西侧进入（激活，A 链）
  input  logic [15:0]            b_in,     // 北侧进入（{w1,w0} 两逻辑列权重，B 链）
  output logic                   av_out,
  output logic                   bv_out,
  output logic                   pulse_out,
  output logic signed [7:0]      a_out,
  output logic [15:0]            b_out,
  output logic signed [31:0]     acc0,     // 逻辑列 2j 的累加结果（驻留）
  output logic signed [31:0]     acc1,     // 逻辑列 2j+1
  output logic signed [26:0]     snap0,    // 快照（requant 消费口径）
  output logic signed [26:0]     snap1
);
  // ---- 脉动链寄存（接口时钟域，与基线同构；b 链 16b）----
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

  // ---- stage2：2× 32b 累加（与基线相同）----
  (* use_dsp = "no" *) logic signed [31:0] acc0_r, acc1_r;
  wire signed [31:0] prod0_ext = {{16{prod0_r[15]}}, prod0_r};
  wire signed [31:0] prod1_ext = {{16{prod1_r[15]}}, prod1_r};

  // ---- 快照：2× 27b，脉冲到拍直抄 + 清零（与基线相同）----
  logic signed [26:0] snap0_r, snap1_r;

  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      a_r <= '0; b_r <= '0; av_r <= 1'b0; bv_r <= 1'b0; pulse_r <= 1'b0;
      prod0_r <= '0; prod1_r <= '0; v_r <= 1'b0;
      acc0_r <= '0; acc1_r <= '0; snap0_r <= '0; snap1_r <= '0;
    end else begin
      a_r <= a_in;  b_r <= b_in;
      av_r <= av_in; bv_r <= bv_in;
      pulse_r <= pulse_in;
      prod0_r <= $signed(P[15:0]);
      prod1_r <= hi_e[15:0];
      v_r     <= v_p;
      if (pulse_in) begin
        snap0_r <= acc0_r[26:0];
        snap1_r <= acc1_r[26:0];
        acc0_r  <= '0;
        acc1_r  <= '0;
      end else if (clr) begin
        acc0_r <= '0; acc1_r <= '0;
      end else if (v_r) begin
        acc0_r <= acc0_r + prod0_ext;
        acc1_r <= acc1_r + prod1_ext;
      end
    end
  end
  assign a_out = a_r;    assign av_out = av_r;
  assign b_out = b_r;    assign bv_out = bv_r;
  assign pulse_out = pulse_r;
  assign acc0 = acc0_r;  assign acc1 = acc1_r;
  assign snap0 = snap0_r; assign snap1 = snap1_r;
endmodule
`endif
