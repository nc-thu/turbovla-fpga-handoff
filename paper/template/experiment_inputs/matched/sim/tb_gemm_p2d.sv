// tb_gemm_p2d.sv — ae_gemm_p2d（第3件：A 双读口 + 2× 核心时钟阵列）引擎级
// 位精确对拍（hw/v8）
// ----------------------------------------------------------------------------
// 与 tb_gemm_pp 同构，差别：
//   * DUT 换 ae_gemm_p2d，多 cclk（2× 核心时钟）与 A/WRAM 双读口。
//   * 时钟：clk 周期 10ns（posedge 5,15,25…）、cclk 周期 5ns 相位错开
//     （posedge 2.5,7.5,12.5…）——每个接口拍恰含两个 cclk 步，且 cclk
//     边沿不与 clk 边沿重合（避开 NBA 同沿竞争；sel=~clk 的选片相位即
//     由此时序锚定：拍前半呈交偶切片、后半呈交奇切片）。
//   * PULSE_DLY2_TB：末切片呈交步 -> 脉冲注入步的 cclk 步数（理论窗
//     [6,11]，默认 6；如对拍失败先扫这个参数）。
// 判定：TB_GEMM_P2D ALL PASS / FAIL；黄金模型与 tb_gemm_p2 逐字一致。
`timescale 1ns/1ps
module tb_gemm_p2d #(
  parameter int PCOLS_TB = 4,
  parameter int PULSE_DLY2_TB = 6,
  parameter bit WB2_TB = 1'b1
);
  localparam int PCOLS = PCOLS_TB, LC = PCOLS_TB*2;
  localparam int CTX_WORDS = 16384, W_WORDS = 4096;

  reg clk = 0, rst_n = 0;
  always #5 clk = ~clk;          // posedge 5,15,25…

  reg cclk = 0;
  always #2.5 cclk = ~cclk;      // posedge 2.5,7.5,12.5…（与 clk 错开半拍）

  logic start = 0, busy, done;
  logic [15:0] m, n, n_loc, j0, k;
  logic [19:0] a_base, b_base, y_base;
  logic        y_tr;
  logic signed [15:0] rq_m;
  logic [7:0]  rq_s;
  logic [19:0] ctxa_addr0, ctxa_addr1;
  logic [16*8-1:0] ctxa_rd0, ctxa_rd1;
  logic        ctxb_we0, ctxb_we1;
  logic [15:0] ctxb_welane0, ctxb_welane1;
  logic [19:0] ctxb_addr0, ctxb_addr1;
  logic [16*8-1:0] ctxb_wd0, ctxb_wd1;
  logic [11:0] w_addr0, w_addr1;
  logic [PCOLS*16-1:0] w_rd0, w_rd1;
  logic [31:0] mac_cnt;
  logic        wb_active;

  ae_gemm_p2d #(.PCOLS(PCOLS), .PULSE_DLY2(PULSE_DLY2_TB), .WB2(WB2_TB)) dut (
    .clk(clk), .cclk(cclk), .rst_n(rst_n),
    .start(start), .busy(busy), .done(done),
    .m(m), .n(n), .n_loc(n_loc), .j0(j0), .k(k),
    .a_base(a_base), .b_base(b_base), .y_base(y_base), .y_tr(y_tr),
    .rq_m(rq_m), .rq_s(rq_s),
    .ctxa_addr0(ctxa_addr0), .ctxa_addr1(ctxa_addr1),
    .ctxa_rdata0(ctxa_rd0), .ctxa_rdata1(ctxa_rd1),
    .ctxb_we0(ctxb_we0), .ctxb_we1(ctxb_we1),
    .ctxb_welane0(ctxb_welane0), .ctxb_welane1(ctxb_welane1),
    .ctxb_addr0(ctxb_addr0), .ctxb_addr1(ctxb_addr1),
    .ctxb_wdata0(ctxb_wd0), .ctxb_wdata1(ctxb_wd1),
    .w_addr0(w_addr0), .w_addr1(w_addr1),
    .w_rdata0(w_rd0), .w_rdata1(w_rd1),
    .mac_cnt(mac_cnt), .wb_active(wb_active)
  );

  // ---- 行为级 CTX：A 口双读（各自 1 拍回数）；B 口双写口（同拍地址必不同）----
  logic [16*8-1:0] ctx [0:CTX_WORDS-1];
  always_ff @(posedge clk) ctxa_rd0 <= ctx[ctxa_addr0];
  always_ff @(posedge clk) ctxa_rd1 <= ctx[ctxa_addr1];
  always_ff @(posedge clk) begin
    if (ctxb_we0)
      for (int L = 0; L < 16; L = L + 1)
        if (ctxb_welane0[L]) ctx[ctxb_addr0][L*8 +: 8] <= ctxb_wd0[L*8 +: 8];
    if (ctxb_we1)
      for (int L = 0; L < 16; L = L + 1)
        if (ctxb_welane1[L]) ctx[ctxb_addr1][L*8 +: 8] <= ctxb_wd1[L*8 +: 8];
  end

  // ---- 行为级 WRAM：双读口，每物理列 16b ----
  logic [PCOLS*16-1:0] wmem [0:W_WORDS-1];
  always_ff @(posedge clk) w_rd0 <= wmem[w_addr0];
  always_ff @(posedge clk) w_rd1 <= wmem[w_addr1];

  // ---- LCG ----
  integer seed_r;
  function integer lcg(input integer s);
    begin lcg = (s * 1103515245 + 12345) & 16'h7fff; end
  endfunction

  // 黄金模型状态
  integer A [0:63][0:2048];      // A[m][k]
  integer B [0:2048][0:95];      // B[k][l]（逻辑列，宽 ≤96）
  logic [16*8-1:0] gold_ctx [0:CTX_WORDS-1];
  integer err_total, i, l, kk, mm, t_i0, t_i1;
  longint acc;
  logic [7:0] y8;
  integer t0, cyc_cnt;

  function [7:0] rq_l(input longint x, input integer mmul, input integer sh);
    longint t;
    begin
      t = x * mmul >>> sh;
      if (t > 127)       rq_l = 8'd127;
      else if (t < -128) rq_l = 8'd128;
      else               rq_l = t[7:0];
    end
  endfunction

  // 跑一个描述符并对拍（da/dy = A 区 / Y 区基址）
  task run_desc(input integer dm, input integer dn, input integer dnl,
                input integer dj0, input integer dk, input integer dtr,
                input integer dmq, input integer dsh,
                input integer da_base, input integer dy_base,
                input [127:0] tag);
    begin
      for (i = 0; i < CTX_WORDS; i = i + 1) begin
        seed_r = lcg(seed_r + i*7);
        t_i0 = (seed_r % 11) - 5;
        t_i1 = (seed_r % 13) - 6;
        ctx[i] = {112'd0, t_i1[7:0], t_i0[7:0]};
        gold_ctx[i] = ctx[i];
      end
      a_base = da_base[19:0]; b_base = 20'd30; y_base = dy_base[19:0];
      for (mm = 0; mm < dm; mm = mm + 1)
        for (kk = 0; kk < dk; kk = kk + 1) begin
          seed_r = lcg(seed_r + mm*131 + kk*17);
          A[mm][kk] = (seed_r % 13) - 6;
        end
      for (kk = 0; kk < dk; kk = kk + 1)
        for (l = 0; l < LC; l = l + 1) begin
          seed_r = lcg(seed_r + kk*57 + l*3);
          B[kk][l] = (seed_r % 15) - 7;
        end
      for (mm = 0; mm < dm; mm = mm + 1)
        for (kk = 0; kk < dk; kk = kk + 1)
          ctx[a_base + (mm/16)*dk + kk][(mm%16)*8 +: 8] = A[mm][kk][7:0];
      for (kk = 0; kk < dk; kk = kk + 1)
        for (l = 0; l < LC; l = l + 1)
          wmem[b_base + kk][ (l/2)*16 + (l%2)*8 +: 8 ] = B[kk][l][7:0];
      for (i = 0; i < CTX_WORDS; i = i + 1) gold_ctx[i] = ctx[i];

      for (mm = 0; mm < dm; mm = mm + 1)
        for (l = 0; l < dnl; l = l + 1) begin
          acc = 0;
          for (kk = 0; kk < dk; kk = kk + 1)
            acc = acc + A[mm][kk] * B[kk][l];
          y8 = rq_l(acc, dmq, dsh);
          if (dtr == 0) begin
            gold_ctx[y_base + (mm/16)*dn + dj0 + l][(mm%16)*8 +: 8] = y8;
          end else begin
            kk = dj0 + l;
            gold_ctx[y_base + (kk/16)*((dm+15)/16*16) + mm][(kk%16)*8 +: 8] = y8;
          end
        end

      @(negedge clk);
      m = dm[15:0]; n = dn[15:0]; n_loc = dnl[15:0]; j0 = dj0[15:0]; k = dk[15:0]; y_tr = dtr[0];
      rq_m = dmq[15:0]; rq_s = dsh[7:0];
      start = 1;
      t0 = 0;
      @(negedge clk); start = 0; t0 = 1;
      while (!done && t0 < 500000) begin
        @(negedge clk); t0 = t0 + 1;
        if (t0 < 60 || t0 % 300 == 0)
          $display("[%0s dbg t=%0d] st_f=%0d pj=%0d iss=%0d me=%0d mo=%0d | st_d=%0d gd=%0d avail=%0d | st_w=%0d gw=%0d | arr:pd=%0d pinj=%0d ptap2=%b swp=%0d",
                   tag, t0, dut.st_f, dut.pj, dut.issue_d, dut.m_even, dut.m_odd,
                   dut.st_d, dut.gd, dut.u_arr.sweep_avail,
                   dut.st_w, dut.gw, dut.u_arr.pd_run, dut.u_arr.pulse_inj,
                   dut.u_arr.ptap2, dut.u_arr.swept_cnt);
      end
      cyc_cnt = t0;
      @(negedge clk); @(negedge clk);

      for (i = 0; i < CTX_WORDS; i = i + 1)
        for (l = 0; l < 16; l = l + 1)
          if (ctx[i][l*8 +: 8] !== gold_ctx[i][l*8 +: 8]) begin
            err_total = err_total + 1;
            if (err_total <= 12)
              $display("[%0s FAIL] word=%0d lane=%0d got=%0d exp=%0d",
                       tag, i, l, $signed(ctx[i][l*8 +: 8]),
                       $signed(gold_ctx[i][l*8 +: 8]));
          end
      if (err_total == 0)
        $display("[%0s] cycles=%0d mac=%0d m=%0d n=%0d nl=%0d j0=%0d k=%0d tr=%0d wb2=%0d pd2=%0d",
                 tag, cyc_cnt, mac_cnt, dm, dn, dnl, dj0, dk, dtr, WB2_TB, PULSE_DLY2_TB);
      else
        $display("[%0s] err_total=%0d (cycles=%0d)", tag, err_total, cyc_cnt);
    end
  endtask

  initial begin
    err_total = 0; seed_r = 16'hb00b;
    repeat (3) @(negedge clk); rst_n = 1;
    repeat (5) @(negedge clk);

    run_desc(32, 8, 8, 0, 5, 0, 448, 8, 100, 12000, "shortK");
    run_desc(32, 8, 8, 0, 64, 0, 448, 8, 100, 12000, "mediumK");
    run_desc(32, 8, 8, 0, 2049, 0, 448, 8, 100, 12000, "deepK");
    run_desc(32, 8, 6, 0, 64, 0, 448, 8, 100, 12000, "narrowN");
    if (err_total == 0) $display("MATCHED ALL PASS");
    else $display("MATCHED FAIL err=%0d",err_total);
    $finish;
  end
endmodule
