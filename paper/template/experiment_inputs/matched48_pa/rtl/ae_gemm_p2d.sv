// ae_gemm_p2d.sv — Pack2 GEMM 引擎：A 双读口 + 2× 核心时钟阵列（hw/v8 第3件）
// ----------------------------------------------------------------------------
// 以 ae_gemm_pp（hw/v8 第1/2件）为底本。第3件要破的是"喂数天花板"：k=2049
// 档接口每拍只喂 1 个 a 切片，而 PE 的 2 MAC/拍需要 2 个——长 K 利用率上限
// 恰 50%。电路件 = 阵列搬进 2× 核心时钟域 cclk（同一 768 DSP，不改 PE 数据
// 通路），接口每拍备好"一对切片"，阵列每 cclk 步吃一片（片率×2）：
//
//   * A 口/WRAM 口各拆两个读地址（ctxa_addr0/1、w_addr0/1，相邻两片）。
//   * 发数 FSM 从"每拍 1 切片"改成"每拍 1 对"（pj 计对数，np = ⌈k/2⌉；
//     k 奇时末对只有偶切片有效 feed_vld1=0）。组周期喂数界 ⌈k/2⌉+2，
//     对齐模型第 3 件公式。
//   * 脉冲不再由接口 FSM 发：FSM 只在"发末对"时置 last_even/last_odd 标记
//     （末切片呈交拍高 1 个接口拍）；阵列内部（cclk 域）在末切片呈交的那
//     个 cclk 步起倒计数 PULSE_DLY2 步后注入脉冲（窗口校准语义同
//     PULSE_DLY∈{5,6}，单位换 cclk 步）。
//   * sweep 事件计数/应答（swept_cnt 2bit 饱和 + 上升沿应答）在阵列侧
//     cclk 域，接口侧 drain FSM 用准静态的 sweep_avail 消费、回 evt_ack。
//   * 跨域形态只有两种：clk 域寄存器整拍稳定的电平进 cclk（选片 sel=~ph1、
//     clr、标记、应答），cclk 域计数器/快照准静态进 clk（读出窗内不变）。
//     时钟相位对齐（同源 2 分频/倍频）下为准静态 CDC，无握手开销。
//
// 快照双 bank / 双 tile_buf 两级读出 / 双写口写链（第1/2件）原样继承——
// 本引擎 = 第1+2+3 件全叠加。
`ifndef AE_GEMM_P2D_SV
`define AE_GEMM_P2D_SV
module ae_gemm_p2d #(
  parameter int PCOLS      = 4,    // 物理列（逻辑列 = 2×PCOLS）
  parameter int PULSE_DLY2 = 6,   // 末切片呈交步 -> 脉冲注入步（cclk 步数）
  parameter bit WB2        = 1'b1 // 第2件：1=双写口
)(
  input  logic clk,                 // 接口时钟
  input  logic cclk,                // 2× 核心时钟（阵列域，与 clk 相位对齐）
  input  logic rst_n,
  input  logic start,
  output logic busy,
  output logic done,
  input  logic [15:0] m,
  input  logic [15:0] n,
  input  logic [15:0] n_loc,
  input  logic [15:0] j0,
  input  logic [15:0] k,
  input  logic [19:0] a_base, b_base, y_base,
  input  logic        y_tr,
  input  logic signed [15:0] rq_m,
  input  logic [7:0]  rq_s,
  // 第3件：A 口双读（相邻两片）
  output logic [19:0] ctxa_addr0, ctxa_addr1,
  input  logic [16*8-1:0] ctxa_rdata0, ctxa_rdata1,
  // 第2件：CTX B 双写口
  output logic        ctxb_we0, ctxb_we1,
  output logic [15:0] ctxb_welane0, ctxb_welane1,
  output logic [19:0] ctxb_addr0, ctxb_addr1,
  output logic [16*8-1:0] ctxb_wdata0, ctxb_wdata1,
  // 第3件：WRAM 双读
  output logic [11:0] w_addr0, w_addr1,
  input  logic [PCOLS*16-1:0] w_rdata0, w_rdata1,
  output logic [31:0] mac_cnt,
  output logic        wb_active
);
  localparam int LOGICAL = PCOLS * 2;

  typedef enum logic [2:0] {SF_IDLE, SF_INIT, SF_FEED, SF_PWAIT, SF_TAIL, SF_FIN} sf_e;
  typedef enum logic [1:0] {SD_WAIT, SD_DALIGN, SD_DRN, SD_LAT} sd_e;
  typedef enum logic [1:0] {SW_WAIT, SW_WB, SW_WBTR, SW_DONE} sw_e;
  sf_e st_f;
  sd_e st_d;
  sw_e st_w;

  logic [15:0] mt_f;
  logic [15:0] gd, gw;
  logic [15:0] pj;             // 已发对数（同时是地址指针：本拍驱动第 pj 对地址）
  logic [15:0] np;             // 本组对数 = ⌈k/2⌉
  logic [15:0] mt_cnt, m16;
  logic [15:0] cgr_lo;
  logic [3:0]  wb_g;
  logic [3:0]  tr_grps;

  logic issue_d;
  logic m_even, m_odd;         // 末切片呈交标记（接口拍宽 1 拍）
  logic arr_clr;
  logic [16*8-1:0] a_feed_c0, a_feed_c1;
  logic [PCOLS*16-1:0] b_feed_c0, b_feed_c1;

  logic [3:0]  drain_row;
  logic        r15_seen;
  localparam int REP_EACH = 4;
  localparam int NREP     = (PCOLS + REP_EACH - 1) / REP_EACH;
  logic [NREP*4-1:0] drain_row_rep;
  logic [3:0]  drain_row_d;
  logic [LOGICAL*32-1:0] acc_row;
  logic [LOGICAL*RQ_XW-1:0] acc_rq, acc_rq_r;
  logic        rq_v;
  logic [LOGICAL-1:0] rq_vld;
  logic [LOGICAL*8-1:0] rq_y;
  logic [7:0]  tile_buf [0:1][0:15][0:LOGICAL-1];
  logic signed [15:0] rq_m_r;
  logic [7:0]  rq_s_r;
  logic [3:0]  drb;
  localparam int RQ_SH = 4;
  localparam int RQ_XW = 27;
  localparam int NGRP  = LOGICAL / RQ_SH;
  logic [1:0]  slot_grp [0:NGRP-1];
  wire  [1:0]  slot_ph = slot_grp[0];
  logic [1:0]  slot_out;
  logic        cap_en, cap_done;
  logic [7:0]  wb_i8, wb_row8;
  logic [31:0] mac_cnt_r;

  // 写回寄存（双口）
  logic        we0_r, we1_r;
  logic [15:0] lanes0_r, lanes1_r;
  (* use_dsp = "no" *) logic [19:0] addr0_r, addr1_r;
  logic [16*8-1:0] data0_r, data1_r;
  (* use_dsp = "no" *) logic [19:0] abase_r;
  (* use_dsp = "no" *) logic [31:0] mtn_r;
  // 转置地址基 cgrm16：底本每拍变乘法 (wb_g+cgr_lo)*m16 直进 addr0/addr1
  // （pp 双口版 OOC 实测 WNS −0.405）。改寄存器步进：SF_INIT 冷路径算
  // cgr_lo_m16，wb_g 归零处整字拷贝、步进处 +m16（与 abase_r 增量同招）。
  (* use_dsp = "no" *) logic [31:0] cgrm16;
  (* use_dsp = "no" *) logic [31:0] cgr_lo_m16;

  // ---- 第1件：级间同步计数器导出（与 ae_gemm_pp 逐字一致）----
  wire [15:0] pend_cnt16 = gd - gw;
  wire        buf_vld0   = (pend_cnt16 >= 16'd2) ||
                           ((pend_cnt16 == 16'd1) && !gw[0]);
  wire        buf_vld1   = (pend_cnt16 >= 16'd2) ||
                           ((pend_cnt16 == 16'd1) &&  gw[0]);
  wire [1:0]  buf_vld    = {buf_vld1, buf_vld0};
  wire pulse_ok = (mt_f <= gd + 16'd1);

  // 末对奇切片有效：呈交拍 pj==np（发数已推进），k 奇时末对只有偶切片
  wire feed_vld1 = issue_d && !(k[0] && (pj == np));

  // ---- 阵列（cclk 域，第3件）----
  ae_sysarr_p2d #(.ROWS(16), .PCOLS(PCOLS), .PULSE_DLY2(PULSE_DLY2)) u_arr (
    .cclk(cclk), .ph1(clk), .rst_n(rst_n),
    .clr(arr_clr),
    .a_feed0(a_feed_c0), .a_feed1(a_feed_c1),
    .b_feed0(b_feed_c0), .b_feed1(b_feed_c1),
    .feed_vld0(issue_d), .feed_vld1(feed_vld1),
    .last_even(m_even), .last_odd(m_odd),
    .sweep_avail(sweep_avail), .evt_ack(evt_ack_r),
    .drain_row_rep(drain_row_rep), .rd_bank(gd[0]), .acc_row(acc_row)
  );

  genvar gq, gc;
  generate
    for (gq = 0; gq < NGRP; gq++) begin : g_rq
      logic [RQ_SH*RQ_XW-1:0] xb;
      for (gc = 0; gc < RQ_SH; gc++) begin : g_x
        assign xb[gc*RQ_XW +: RQ_XW] = acc_rq_r[(gq*RQ_SH+gc)*RQ_XW +: RQ_XW];
      end
      rq_ms_x #(.SHARE(RQ_SH), .XW(RQ_XW), .T_MAX(39)) u_ms (
        .clk(clk), .rst_n(rst_n),
        .in_vld({RQ_SH{rq_v}}),
        .x_bus(xb),
        .m(rq_m_r), .s(rq_s_r),
        .out_vld(rq_vld[gq*RQ_SH +: RQ_SH]),
        .y_bus(rq_y[gq*RQ_SH*8 +: RQ_SH*8]),
        .slot_o(slot_grp[gq])
      );
    end
  endgenerate

  assign busy = (st_f != SF_IDLE);
  assign mac_cnt = mac_cnt_r;
  assign wb_active = (st_w == SW_WB) || (st_w == SW_WBTR);

  // 双读口地址：本拍驱动第 pj 对（偶片 pj*2 / 奇片 pj*2+1）
  assign ctxa_addr0 = abase_r + {1'b0, pj[14:0], 1'b0};
  assign ctxa_addr1 = ctxa_addr0 + 20'd1;
  wire [12:0] wsum = {1'b0, b_base[11:0]} + {1'b0, pj[11:0], 1'b0};
  assign w_addr0 = wsum[11:0];
  assign w_addr1 = wsum[11:0] + 12'd1;

  assign ctxb_we0 = we0_r;  assign ctxb_we1 = we1_r;
  assign ctxb_welane0 = lanes0_r;  assign ctxb_welane1 = lanes1_r;
  assign ctxb_wdata0 = data0_r;    assign ctxb_wdata1 = data1_r;
  always_comb begin
    ctxb_addr0 = we0_r ? addr0_r : '0;
    ctxb_addr1 = we1_r ? addr1_r : '0;
  end

  assign a_feed_c0 = ctxa_rdata0;
  assign a_feed_c1 = ctxa_rdata1;
  assign b_feed_c0 = w_rdata0;
  assign b_feed_c1 = w_rdata1;

  // 读出通路寄存（快照值在 64 拍读出窗内准静态，直接 clk 采样）
  always_comb begin
    for (int c = 0; c < LOGICAL; c++)
      acc_rq[c*RQ_XW +: RQ_XW] = acc_row[c*32 +: RQ_XW];
  end
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) acc_rq_r <= '0;
    else        acc_rq_r <= acc_rq;
  end

  wire sweep_avail;             // 阵列侧 cclk 域计数 != 0（准静态）
  wire sweep_take = (st_d == SD_WAIT) && sweep_avail && !buf_vld[gd[0]];
  // 应答必须打一拍：组合 sweep_take 在 sweep_avail 上升的半个拍内就为 1，
  // cclk 域会在 clk FSM 真正消费之前就把它当应答、把事件数减掉（实测 D0
  // 死锁根因）。寄存一拍后 ack 只在 FSM 已跳转（st_d 离开 SD_WAIT）的
  // 下一拍出现，事件在飞期间 avail 稳定为 1。
  logic evt_ack_r;
  always_ff @(posedge clk or negedge rst_n)
    if (!rst_n) evt_ack_r <= 1'b0;
    else        evt_ack_r <= sweep_take;

  // drain_row 次态（H2 副本 + 换行 slot==1，与 pp 一致）
  always_comb begin
    if (st_d == SD_WAIT && sweep_take)                                  drain_row_d = 4'd0;
    else if (st_d == SD_DRN && slot_ph == 2'd1 && drain_row != 4'd15)   drain_row_d = drain_row + 4'd1;
    else                                                                drain_row_d = drain_row;
  end

  always_comb begin
    cap_en   = |rq_vld[3:0];
    slot_out = rq_vld[1] ? 2'd1 : rq_vld[2] ? 2'd2 : rq_vld[3] ? 2'd3 : 2'd0;
  end

  // ---- 喂数道 FSM（第3件：每拍发一对；末对受银行规则门控）----
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      st_f <= SF_IDLE; done <= 1'b0; arr_clr <= 1'b0;
      mac_cnt_r <= '0;
      issue_d <= 1'b0; m_even <= 1'b0; m_odd <= 1'b0;
    end else begin
      done <= 1'b0; arr_clr <= 1'b0; m_even <= 1'b0; m_odd <= 1'b0;
      case (st_f)
        SF_IDLE: if (start) st_f <= SF_INIT;
        SF_INIT: begin
            mt_f <= '0; pj <= '0; np <= (k + 16'd1) >> 1;
            mac_cnt_r <= '0;
            abase_r <= a_base;
            mt_cnt <= (m + 16'd15) >> 4;
            m16    <= (((m + 16'd15) >> 4) << 4);
            rq_m_r <= rq_m; rq_s_r <= rq_s;
            issue_d <= 1'b0;
            cgr_lo  <= j0 >> 4;
            cgr_lo_m16 <= (j0 >> 4) * (((m + 16'd15) >> 4) << 4);
            tr_grps <= (((j0 + n_loc - 16'd1) >> 4) - (j0 >> 4)) + 4'd1;
            arr_clr <= 1'b1;
            st_f <= SF_FEED;
          end
        // 时间线（对照底本"拍 0 地址引导"）：拍 j+1 驱动第 j 对地址、
        // 拍 j+2 呈交第 j 对（rdata 1 拍）；末对呈交拍 = 标记高 1 拍。
        SF_FEED: begin
            if (pj < np) begin
              if (pj == np - 16'd1 && !pulse_ok) begin
                issue_d <= 1'b0;           // 末对等银行：停发（已发各对均已呈交）
                st_f    <= SF_PWAIT;
              end else begin
                issue_d <= 1'b1;
                pj      <= pj + 16'd1;
                mac_cnt_r <= mac_cnt_r + 32 * LOGICAL;
                if (pj == np - 16'd1) begin
                  m_even <= k[0];          // k 奇：末切片是偶切片（呈交在 sel=0 步）
                  m_odd  <= ~k[0];         // k 偶：末切片是奇切片（sel=1 步）
                end
              end
            end else begin
              issue_d <= 1'b0;
              if (issue_d) st_f <= SF_TAIL;
            end
          end
        SF_PWAIT: begin
            if (pulse_ok) begin
              issue_d <= 1'b1;
              pj      <= pj + 16'd1;
              mac_cnt_r <= mac_cnt_r + 32 * LOGICAL;
              m_even <= k[0];
              m_odd  <= ~k[0];
              st_f   <= SF_TAIL;
            end
          end
        SF_TAIL: begin
            issue_d <= 1'b0;
            if (k[0]) mac_cnt_r <= mac_cnt_r - 16 * LOGICAL;   // 奇 k 末对只 1 片
            if (mt_f + 16'd1 >= mt_cnt) begin
              st_f <= SF_FIN;
            end else begin
              mt_f <= mt_f + 16'd1;
              abase_r <= abase_r + {{4'd0}, k};
              pj <= '0;
              st_f <= SF_FEED;
            end
          end
        SF_FIN: if (st_w == SW_DONE) begin done <= 1'b1; st_f <= SF_IDLE; end
        default: st_f <= SF_IDLE;
      endcase
    end
  end

  // ---- drain 级 FSM（与 pp 一致；事件源换 sweep_avail，应答即 sweep_take）----
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      st_d <= SD_WAIT; rq_v <= 1'b0; drain_row <= '0; drain_row_rep <= '0;
      r15_seen <= 1'b0; gd <= '0;
    end else begin
      drain_row <= drain_row_d;
      for (int ri = 0; ri < NREP; ri++) drain_row_rep[ri*4 +: 4] <= drain_row_d;
      if (st_f == SF_INIT) begin
        st_d <= SD_WAIT; gd <= '0; rq_v <= 1'b0; drain_row <= '0; r15_seen <= 1'b0;
      end else begin
        case (st_d)
          SD_WAIT: if (sweep_take) begin
              st_d <= SD_DALIGN;
              r15_seen <= 1'b0;
            end
          SD_DALIGN: if (slot_ph == 2'd2) begin st_d <= SD_DRN; rq_v <= 1'b1; end
          SD_DRN: begin
            rq_v <= 1'b1;
            if (slot_ph == 2'd0 && drain_row == 4'd15) r15_seen <= 1'b1;
            if (slot_ph == 2'd2 && r15_seen) begin
              rq_v <= 1'b0;
              st_d <= SD_LAT;
            end
          end
          SD_LAT: if (cap_done) begin
              gd <= gd + 16'd1;
              st_d <= SD_WAIT;
            end
          default: st_d <= SD_WAIT;
        endcase
      end
    end
  end

  // ---- tile_buf 捕获（双缓冲，与 pp 一致）----
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      drb <= '0; cap_done <= 1'b0;
    end else if (st_f == SF_INIT) begin
      drb <= '0; cap_done <= 1'b0;
    end else if (sweep_take) begin
      drb <= '0; cap_done <= 1'b0;
    end else if (cap_en) begin
      for (int g = 0; g < NGRP; g++)
        tile_buf[gd[0]][drb][g*RQ_SH + slot_out] <= rq_y[(g*RQ_SH + slot_out)*8 +: 8];
      if (slot_out == 2'd3) begin
        drb <= drb + 4'd1;
        if (drb == 4'd15) cap_done <= 1'b1;
      end
    end
  end

  // ---- 写回级 FSM（与 pp 一致，双写口可退单口）----
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      st_w <= SW_WAIT; gw <= '0; mtn_r <= '0;
      wb_i8 <= '0; wb_row8 <= '0; wb_g <= '0;
      we0_r <= 1'b0; we1_r <= 1'b0;
      lanes0_r <= '0; lanes1_r <= '0;
    end else begin
      we0_r <= 1'b0; we1_r <= 1'b0;
      lanes0_r <= '0; lanes1_r <= '0;
      if (st_f == SF_INIT) begin
        st_w <= SW_WAIT; gw <= '0; mtn_r <= '0;
      end else begin
        case (st_w)
          SW_WAIT: if (buf_vld[gw[0]]) begin
              wb_i8 <= '0; wb_row8 <= '0; wb_g <= '0;
              cgrm16 <= cgr_lo_m16;
              st_w <= y_tr ? SW_WBTR : SW_WB;
            end
          SW_WB: begin
            if (wb_i8 < n_loc[7:0]) begin
              we0_r <= 1'b1;
              lanes0_r <= m_lanes;
              addr0_r <= y_base + mtn_r + j0 + {8'd0, wb_i8};
              for (int i = 0; i < 16; i++) data0_r[i*8 +: 8] <= tile_buf[gw[0]][i][wb_i8];
            end
            if (WB2 && (wb_i8 + 8'd1 < n_loc[7:0])) begin
              we1_r <= 1'b1;
              lanes1_r <= m_lanes;
              addr1_r <= y_base + mtn_r + j0 + {8'd0, wb_i8} + 20'd1;
              for (int i = 0; i < 16; i++) data1_r[i*8 +: 8] <= tile_buf[gw[0]][i][wb_i8 + 8'd1];
            end
            if (wb_i8 + (WB2 ? 8'd2 : 8'd1) >= n_loc[7:0]) begin
              gw <= gw + 16'd1;
              mtn_r <= mtn_r + {{16'd0, n}};
              if (gw + 16'd1 >= mt_cnt) st_w <= SW_DONE;
              else st_w <= SW_WAIT;
            end else wb_i8 <= wb_i8 + (WB2 ? 8'd2 : 8'd1);
          end
          SW_WBTR: begin
            if (gw*16 + {12'd0, wb_row8} < m) begin
              we0_r <= 1'b1;
              addr0_r <= y_base + cgrm16 + (gw*16 + {12'd0, wb_row8});
              for (int L = 0; L < 16; L++) begin
                if ((cgr_lo + wb_g)*16 + L >= j0 &&
                    (cgr_lo + wb_g)*16 + L < j0 + n_loc) begin
                  lanes0_r[L] <= 1'b1;
                  data0_r[L*8 +: 8] <= tile_buf[gw[0]][wb_row8][(cgr_lo + wb_g)*16 + L - j0];
                end
              end
            end
            if (WB2 && (wb_row8 != 8'd15) &&
                (gw*16 + {12'd0, wb_row8} + 17'd1 < m)) begin
              we1_r <= 1'b1;
              addr1_r <= y_base + cgrm16 + (gw*16 + {12'd0, wb_row8}) + 20'd1;
              for (int L = 0; L < 16; L++) begin
                if ((cgr_lo + wb_g)*16 + L >= j0 &&
                    (cgr_lo + wb_g)*16 + L < j0 + n_loc) begin
                  lanes1_r[L] <= 1'b1;
                  data1_r[L*8 +: 8] <= tile_buf[gw[0]][wb_row8 + 8'd1][(cgr_lo + wb_g)*16 + L - j0];
                end
              end
            end
            if (wb_g + 16'd1 < tr_grps) begin
              wb_g <= wb_g + 4'd1;
              cgrm16 <= cgrm16 + {16'd0, m16};
            end
            else begin
              wb_g <= '0;
              cgrm16 <= cgr_lo_m16;
              if (wb_row8 + (WB2 ? 8'd2 : 8'd1) > 8'd15) begin
                gw <= gw + 16'd1;
                mtn_r <= mtn_r + {{16'd0, n}};
                if (gw + 16'd1 >= mt_cnt) st_w <= SW_DONE;
                else st_w <= SW_WAIT;
              end else wb_row8 <= wb_row8 + (WB2 ? 8'd2 : 8'd1);
            end
          end
          SW_DONE: ;
          default: st_w <= SW_WAIT;
        endcase
      end
    end
  end

  logic [15:0] m_lanes;
  always_comb begin
    m_lanes = '0;
    for (int i = 0; i < 16; i++) m_lanes[i] = (gw*16 + i < m);
  end
endmodule
`endif
