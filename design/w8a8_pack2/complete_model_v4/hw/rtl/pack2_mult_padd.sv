// pack2_mult_padd.sv — 2-lane 打包 INT8×INT8 乘法核（DSP48E2 预加器消除偏置版）
// ----------------------------------------------------------------------------
// 与基线 pack2_mult_dsp.sv 的唯一差异：把 -128·(2^16+1) 偏置搬进 DSP 预加器，
// 使 P 直接就是真值打包积，外部 stage1 只剩字段抽取 + 高场借位，无需 -128·a。
//
// 数学（预加器版 offset-free packing）：
//   Q  = w1·2^16 + w0 的偏置打包 = (w1+128)·2^16 + (w0+128)（无符号 < 2^24）
//   A  = -128·(2^16+1) = -8388736 = 27'h77FFF80（常数，进 DSP A 口）
//   D  = Q（进 DSP D 口）；预加器算 AD = D + A = Q - 8388736 = w1·2^16 + w0 =: R
//   B  = 符号扩展的共享操作数 a
//   P  = a · R   （乘法器两侧均按有符号处理：A 侧 27b / B 侧 18b）
//   低场 prod0 = signed(P[15:0])                    = a·w0
//   高场 prod1 = signed(P[31:16]) + P[15]           = a·w1
//   借位 P[15] 来源：a·w0 ∈ [-16384, +16384]，为负时 floor(P/2^16) 少 1，
//   而 P[15] 恰好当 a·w0 < 0 时为 1（a·w0 落在 signed16 内）。
//
// DSP 配置核对（对照 Vivado 2021.2 自带 unisim 行为模型 DSP48E2.v 逐行核对，
//   非凭 UG579 表格转抄）：
//   * AMULTSEL="AD"  -> a_mult_mux = AD_DATA（预加器输出进乘法器 A 侧）
//   * INMODE=5'b00100：bit2=1 打开 D 口（D_DATA_mux = D）；bit3=0 选 D+A；
//     bit1=0 打开 A 口（PREADD_AB = A_ALU，AREG=0 即 A 端口直通）；bit4=0 走 B 端口。
//   * DREG=0 / ADREG=0：预加器组合进 Booth 乘法器，MREG/PREG=1 不变
//     -> 输入到 P 的流水深度与基线完全相同（延迟不变）。
//   * OPMODE=9'b000000101 不变：unisim X mux 解码 OPMODE[1:0]=01 -> U_DATA
//     （Booth 部分和）、Y mux OPMODE[3:2]=01 -> V_DATA、Z=0 -> ALU 输出=乘积。
//   * 预加器是 27b 补码按位加：D(无符号解释亦可) + A(补码 -8388736) mod 2^27
//     = R ∈ [-8388736, +8323199]，R 落在 signed27 内无回绕。
//   注意：unisim 中 AMULTSEL="A" 且 BMULTSEL="B" 时 DREG/ADREG 被强制 0——
//   换成 "AD" 后这两个寄存器参数才生效，本设计仍取 0，不新增流水级。
`ifndef PACK2_MULT_PADD_SV
`define PACK2_MULT_PADD_SV
module pack2_mult_padd #(
  parameter int M_REG = 1,    // DSP48E2 MREG
  parameter int P_REG = 1     // DSP48E2 PREG
)(
  input  logic              clk,
  input  logic              v_in,     // 本拍积有效
  input  logic              row_in,   // 0: a0 行 / 1: a1 行（接口兼容保留）
  input  logic signed [7:0] a_in,     // 共享行激活（B 口）
  input  logic signed [7:0] w0_in,    // 列 0 权重（低 lane）
  input  logic signed [7:0] w1_in,    // 列 1 权重（高 lane）
  output logic [47:0]       P,        // DSP P 输出（PREG 后）
  output logic              v_p,      // 与 P 对齐的有效标志
  output logic              row_p,
  output logic signed [7:0] a_p       // 与 P 对齐的共享操作数（本方案校正不需要，接口保留）
);
  localparam int LAT = 1 + M_REG + P_REG;   // 输入 → P 的总延迟（与基线相同）

  // ---- S0 输入寄存（与基线相同） ----
  logic signed [7:0] a_s0, w0_s0, w1_s0;
  logic              v_s0, row_s0;
  always_ff @(posedge clk) begin
    a_s0 <= a_in;  w0_s0 <= w0_in;  w1_s0 <= w1_in;
    v_s0 <= v_in;  row_s0 <= row_in;
  end

  // ---- 打包（纯线网，同基线） ----
  wire [7:0] wt0 = {~w0_s0[7], w0_s0[6:0]};   // w̃0 = w0 + 128
  wire [7:0] wt1 = {~w1_s0[7], w1_s0[6:0]};   // w̃1 = w1 + 128
  wire [26:0] dq = {3'b000, wt1, 8'b0, wt0};  // Q = w̃1·2^16 + w̃0  -> D 口
  wire [26:0] aconst = 27'h77FFF80;           // -8388736 = -128·(2^16+1) -> A 口
  wire [29:0] aconst_ext = {{3{aconst[26]}}, aconst};
  wire [17:0] bx = {{10{a_s0[7]}}, a_s0};     // B 口：符号扩展的 a

  // ---- DSP48E2（显式原语，预加器版） ----
  wire [47:0] p_out;
`ifdef VERILATOR
  // 仿真器不带 AMD UNISIM：与 MREG/PREG 等延迟的位精确行为模型。
  // 只验证数学与流水行为；原语数值正确性另由 xsim + 真 DSP48E2 模型核验。
  wire signed [26:0] r_pre = $signed(dq) + $signed(aconst);   // 预加器 D+A（mod 2^27）
  wire signed [29:0] sim_a = {{3{r_pre[26]}}, r_pre};         // R 可为负，必须符号扩展
  wire signed [17:0] sim_b = bx;                              // （基线 ap 恒正才可零扩展）
  wire signed [47:0] sim_m = sim_a * sim_b;
  logic signed [47:0] sim_m_r, sim_p_r;
  generate
    if (M_REG && P_REG) begin : g_sim_mp
      always_ff @(posedge clk) begin
        sim_m_r <= sim_m;
        sim_p_r <= sim_m_r;
      end
      assign p_out = sim_p_r;
    end else if (M_REG || P_REG) begin : g_sim_one
      always_ff @(posedge clk) sim_p_r <= sim_m;
      assign p_out = sim_p_r;
    end else begin : g_sim_zero
      assign p_out = sim_m;
    end
  endgenerate
`else
  DSP48E2 #(
    .ACASCREG            (0),
    .ADREG               (0),
    .ALUMODEREG          (0),
    .AMULTSEL            ("AD"),
    .AREG                (0),
    .AUTORESET_PATDET    ("NO_RESET"),
    .AUTORESET_PRIORITY  ("RESET"),
    .A_INPUT             ("DIRECT"),
    .BCASCREG            (0),
    .BMULTSEL            ("B"),
    .BREG                (0),
    .B_INPUT             ("DIRECT"),
    .CARRYINREG          (0),
    .CARRYINSELREG       (0),
    .CREG                (0),
    .DREG                (0),
    .INMODEREG           (0),
    .IS_ALUMODE_INVERTED (4'b0000),
    .IS_CARRYIN_INVERTED (1'b0),
    .IS_CLK_INVERTED     (1'b0),
    .IS_INMODE_INVERTED  (5'b00000),
    .IS_OPMODE_INVERTED  (9'b000000000),
    .IS_RSTALLCARRYIN_INVERTED (1'b0),
    .IS_RSTALUMODE_INVERTED    (1'b0),
    .IS_RSTA_INVERTED          (1'b0),
    .IS_RSTB_INVERTED          (1'b0),
    .IS_RSTCTRL_INVERTED       (1'b0),
    .IS_RSTC_INVERTED          (1'b0),
    .IS_RSTD_INVERTED          (1'b0),
    .IS_RSTINMODE_INVERTED     (1'b0),
    .IS_RSTM_INVERTED          (1'b0),
    .IS_RSTP_INVERTED          (1'b0),
    .MASK                (48'h3FFFFFFFFFFF),
    .MREG                (M_REG),
    .OPMODEREG           (0),
    .PATTERN             (48'h000000000000),
    .PREADDINSEL         ("A"),
    .PREG                (P_REG),
    .RND                 (48'h000000000000),
    .SEL_MASK            ("MASK"),
    .SEL_PATTERN         ("PATTERN"),
    .USE_MULT            ("MULTIPLY"),
    .USE_PATTERN_DETECT  ("NO_PATDET"),
    .USE_SIMD            ("ONE48"),
    .USE_WIDEXOR         ("FALSE"),
    .XORSIMD             ("XOR24_48_96")
  ) u_dsp (
    .CLK          (clk),
     .A            (aconst_ext),           // 常数 -8388736（符号扩展到 DSP A 口）
    .B            (bx),
    .C            (48'b0),
    .D            (dq),                   // 打包权重走 D 口（基线此处为 0）
    .ACIN         (30'b0),
    .BCIN         (18'b0),
    .PCIN         (48'b0),
    .ALUMODE      (4'b0000),
    .INMODE       (5'b00100),             // D 口使能 + D+A（基线为 5'b00000）
    .OPMODE       (9'b000000101),         // 与基线相同：U+V+0 = 乘积
    .CARRYIN      (1'b0),
    .CARRYINSEL   (3'b000),
    .CARRYCASCIN  (1'b0),
    .MULTSIGNIN   (1'b0),
    .CEA1         (1'b1),
    .CEA2         (1'b1),
    .CEAD         (1'b1),
    .CEALUMODE    (1'b1),
    .CEB1         (1'b1),
    .CEB2         (1'b1),
    .CEC          (1'b1),
    .CECARRYIN    (1'b1),
    .CECTRL       (1'b1),
    .CED          (1'b1),
    .CEINMODE     (1'b1),
    .CEM          (1'b1),
    .CEP          (1'b1),
    .RSTA         (1'b0),
    .RSTALLCARRYIN(1'b0),
    .RSTALUMODE   (1'b0),
    .RSTB         (1'b0),
    .RSTC         (1'b0),
    .RSTCTRL      (1'b0),
    .RSTD         (1'b0),
    .RSTINMODE    (1'b0),
    .RSTM         (1'b0),
    .RSTP         (1'b0),
    .P            (p_out)
  );
`endif
  assign P = p_out;

  // ---- a/v/row 等深延迟（LAT−1 级，S0 已算 1 级；与基线相同） ----
  logic signed [7:0] a_d [LAT-2:0];
  logic              v_d [LAT-2:0];
  logic              r_d [LAT-2:0];
  generate
    if (LAT >= 2) begin : g_pipe
      integer gi;
      always_ff @(posedge clk) begin
        a_d[0] <= a_s0;  v_d[0] <= v_s0;  r_d[0] <= row_s0;
        for (gi = 1; gi < LAT-1; gi = gi + 1) begin
          a_d[gi] <= a_d[gi-1];  v_d[gi] <= v_d[gi-1];  r_d[gi] <= r_d[gi-1];
        end
      end
      assign a_p  = a_d[LAT-2];
      assign v_p  = v_d[LAT-2];
      assign row_p= r_d[LAT-2];
    end else begin : g_nopipe
      assign a_p  = a_s0;
      assign v_p  = v_s0;
      assign row_p= row_s0;
    end
  endgenerate
endmodule
`endif
