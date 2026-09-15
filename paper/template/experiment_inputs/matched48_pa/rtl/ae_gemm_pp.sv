// ae_gemm_pp.sv — Pack2 GEMM 引擎 + 快照双 bank 乒乓 + 双写口写链（hw/v8 第1/2件）
// ----------------------------------------------------------------------------
// 以 ae_gemm_p2（hw/v5 H2 定版）为底本，按 arch v8 三层拆账的两件电路修复改版：
//
// 第1件"累加器乒乓"（排队层 45.0M 拍的电路件）：
//   * PE 快照双 bank（ae_pe_pp：脉冲写 bank g%2，本地奇偶，clr 对齐）。
//   * 读出链从"单 tile_buf 串行（drain→LAT→写回→才轮到下一组）"拆成两级流水：
//       drain 级（SD_*）：swept 事件 → 对齐 → 64 拍 requant → 双 tile_buf[gd%2]
//       写回级（SW_*）：tile_buf[gw%2] → CTX B 口（普通/转置）
//     级间无握手寄存器——buf 有效/空闲由计数器导出（见 buf_vld）。
//   * 脉冲门控从"逃生舱（drain_row≥12 放行下一脉冲）"换成银行规则：
//       脉冲(g) 允许 ⇔ drain(g-2) 已完成 ⇔ g ≤ gd+1（gd = 已完成 drain 的组数）。
//     稳态行组周期 = max(k+2, 64+DALIGN+LAT(requant 占用), wb)。
//     注意：arch v8 模型第 1 件公式 max(k+2, wb) 里没有 requant 占用这一项——
//     requant 套数不加倍时它是 64 拍硬地板（每拍 24 列 × 4 slot），RTL 实测
//     会对浅段给出比模型保守的数（模型乐观度的实测修正，见 notes/p2_cyc.py）。
//   * swept_r 单 bit → swept_cnt 2bit 饱和（同 hw/v7 F2 修复的计数语义；
//     乒乓下在飞 sweep 事件 ≤2，事件不会再被合并吞掉）。
//
// 第2件"写链 2 倍宽"（排队层的另一半）：
//   * CTX B 口双写口（addr0/addr1 相邻列/相邻行同拍各写 16 lane 字）。
//     物理落地 = ctx_ram 按地址奇偶分两个 TDP bank（每 bank 1 读 1 写），
//     相邻两列地址差 1 天然落在不同 bank——引擎侧本模块即按此契约发双写。
//   * WB2 参数：1 = 双写口（wb/2）；0 = 退回单写口（wb）——供拍数台阶对拍。
//
// 喂数道 FSM / 寻址 / requant 时分复用 / 转置写回语义与底本逐字一致；
// 读出道从单 FSM 拆成 drain/写回两个 FSM（各自独占自己的寄存器组）。
`ifndef AE_GEMM_PP_SV
`define AE_GEMM_PP_SV
module ae_gemm_pp #(
  parameter int PCOLS     = 4,    // 物理列（逻辑列 = 2×PCOLS，须为 4 的倍数）
  parameter int PULSE_DLY = 5,   // 末脉冲发射滞后（与 ae_gemm_p2 相同语义）
  parameter bit WB2       = 1'b1 // 第2件：1=双写口（每拍 2 列/2 行）
)(
  input  logic clk,
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
  output logic [19:0] ctxa_addr,
  input  logic [16*8-1:0] ctxa_rdata,
  // 第2件：CTX B 双写口（地址奇偶分 bank，相邻列/行同拍并行写）
  output logic        ctxb_we0, ctxb_we1,
  output logic [15:0] ctxb_welane0, ctxb_welane1,
  output logic [19:0] ctxb_addr0, ctxb_addr1,
  output logic [16*8-1:0] ctxb_wdata0, ctxb_wdata1,
  output logic [11:0] w_addr,
  input  logic [PCOLS*16-1:0] w_rdata,
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

  logic [15:0] mt_f;          // 喂数道组号（脉冲为组 mt_f 发射，发后 SF_TAIL 递增）
  logic [15:0] gd, gw;        // drain 级下一组 / 写回级下一组（gd 也 = 已完成 drain 数）
  logic [15:0] kk;
  logic [15:0] mt_cnt, m16;
  logic [15:0] cgr_lo;
  logic [3:0]  wb_g;
  logic [3:0]  tr_grps;

  logic issue_d;
  logic feed_pulse_raw;
  logic feed_pulse;
  logic [PULSE_DLY-1:0] pulse_dly;
  logic arr_clr;
  logic [127:0] a_feed_c;
  logic [PCOLS*16-1:0] b_feed_c;

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
  logic [7:0]  tile_buf [0:1][0:15][0:LOGICAL-1];   // 第1件：双缓冲
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
  // 转置地址基 cgrm16：底本是每拍变乘法 (wb_g+cgr_lo)*m16（20b×16b 乘法链
  // 直进 addr0/addr1，双口版 OOC 实测 WNS −0.405）。改成寄存器步进：SF_INIT
  // 从端口冷路径算一次 cgr_lo_m16，wb_g 归零处整字拷贝、步进处 +m16——与
  // abase_r"地址乘法换增量"同一招（底本 118 行注释先例）。
  (* use_dsp = "no" *) logic [31:0] cgrm16;
  (* use_dsp = "no" *) logic [31:0] cgr_lo_m16;

  // 末脉冲延迟线（与底本一致）
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) pulse_dly <= '0;
    else        pulse_dly <= {pulse_dly[PULSE_DLY-2:0], feed_pulse_raw};
  end
  assign feed_pulse = pulse_dly[PULSE_DLY-1];

  // ---- 第1件核心：级间同步全靠三个计数器，无握手标志 ----
  // buf_vld[b] = 还有未写回的组落在 bank b（[gw, gd) 内 g%2==b）
  wire [15:0] pend_cnt16 = gd - gw;
  wire        buf_vld0   = (pend_cnt16 >= 16'd2) ||
                           ((pend_cnt16 == 16'd1) && !gw[0]);
  wire        buf_vld1   = (pend_cnt16 >= 16'd2) ||
                           ((pend_cnt16 == 16'd1) &&  gw[0]);
  wire [1:0]  buf_vld    = {buf_vld1, buf_vld0};
  // 脉冲(g=mt_f) 允许 ⇔ drain(g-2) 完成 ⇔ mt_f ≤ gd+1
  wire pulse_ok = (mt_f <= gd + 16'd1);

  ae_sysarr_pp #(.ROWS(16), .PCOLS(PCOLS)) u_arr (
    .clk(clk), .rst_n(rst_n),
    .clr(arr_clr), .feed_vld(issue_d), .feed_pulse(feed_pulse),
    .a_feed(a_feed_c), .b_feed(b_feed_c),
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

  assign ctxa_addr = abase_r + {{4'd0}, kk};
  assign w_addr    = b_base[11:0] + kk[11:0];
  assign ctxb_we0 = we0_r;  assign ctxb_we1 = we1_r;
  assign ctxb_welane0 = lanes0_r;  assign ctxb_welane1 = lanes1_r;
  assign ctxb_wdata0 = data0_r;    assign ctxb_wdata1 = data1_r;
  always_comb begin
    ctxb_addr0 = we0_r ? addr0_r : '0;
    ctxb_addr1 = we1_r ? addr1_r : '0;
  end

  assign a_feed_c = ctxa_rdata;
  assign b_feed_c = w_rdata;

  // 读出通路寄存（与底本一致）
  always_comb begin
    for (int c = 0; c < LOGICAL; c++)
      acc_rq[c*RQ_XW +: RQ_XW] = acc_row[c*32 +: RQ_XW];
  end
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) acc_rq_r <= '0;
    else        acc_rq_r <= acc_rq;
  end

  // ptap + swept_cnt（2bit 饱和，事件排队深度 ≤2 见上方注释）
  logic [PCOLS:0] ptap;
  logic [1:0]     swept_cnt;
  wire  sweep_evt  = ptap[PCOLS];
  wire  sweep_take = (st_d == SD_WAIT) && (swept_cnt != 2'd0) && !buf_vld[gd[0]];
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      ptap <= '0; swept_cnt <= 2'd0;
    end else begin
      ptap <= {ptap[PCOLS-1:0], feed_pulse};
      if (st_f == SF_INIT) swept_cnt <= 2'd0;
      else if (sweep_evt && !sweep_take) begin
        if (swept_cnt != 2'd3) swept_cnt <= swept_cnt + 2'd1;
      end else if (!sweep_evt && sweep_take) swept_cnt <= swept_cnt - 2'd1;
    end
  end

  // drain_row 次态（H2 ① 副本机制 + 换行 slot==1 原样保留，状态名换 SD_*）
  always_comb begin
    if (st_d == SD_WAIT && sweep_take)                                  drain_row_d = 4'd0;
    else if (st_d == SD_DRN && slot_ph == 2'd1 && drain_row != 4'd15)   drain_row_d = drain_row + 4'd1;
    else                                                                drain_row_d = drain_row;
  end

  always_comb begin
    cap_en   = |rq_vld[3:0];
    slot_out = rq_vld[1] ? 2'd1 : rq_vld[2] ? 2'd2 : rq_vld[3] ? 2'd3 : 2'd0;
  end

  // ---- 喂数道 FSM（与底本逐态一致；仅 pulse_ok 换银行规则）----
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      st_f <= SF_IDLE; done <= 1'b0; arr_clr <= 1'b0;
      mac_cnt_r <= '0;
      issue_d <= 1'b0; feed_pulse_raw <= 1'b0;
    end else begin
      done <= 1'b0; arr_clr <= 1'b0; feed_pulse_raw <= 1'b0;
      case (st_f)
        SF_IDLE: if (start) st_f <= SF_INIT;
        SF_INIT: begin
            mt_f <= '0; kk <= '0; mac_cnt_r <= '0;
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
        SF_FEED: begin
            if (kk < k) begin
              issue_d <= 1'b1;
              kk <= kk + 16'd1;
              mac_cnt_r <= mac_cnt_r + 16 * LOGICAL;
            end else begin
              issue_d <= 1'b0;
              if (issue_d) begin
                if (pulse_ok) begin
                  feed_pulse_raw <= 1'b1;
                  st_f <= SF_TAIL;
                end else begin
                  st_f <= SF_PWAIT;
                end
              end
            end
          end
        SF_PWAIT: begin
            if (pulse_ok) begin
              feed_pulse_raw <= 1'b1;
              st_f <= SF_TAIL;
            end
          end
        SF_TAIL: begin
            if (mt_f + 16'd1 >= mt_cnt) begin
              st_f <= SF_FIN;
            end else begin
              mt_f <= mt_f + 16'd1;
              abase_r <= abase_r + {{4'd0}, k};
              kk <= '0;
              st_f <= SF_FEED;
            end
          end
        SF_FIN: if (st_w == SW_DONE) begin done <= 1'b1; st_f <= SF_IDLE; end
        default: st_f <= SF_IDLE;
      endcase
    end
  end

  // ---- drain 级 FSM：swept → 对齐 → 64 拍 requant →（tile_buf 由捕获块填）----
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
          // H2 相位平移保留：rq_v 提前到 slot==2 发
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
              gd <= gd + 16'd1;       // 本组 drain 完成：buf 有效（导出式）、放行脉冲
              st_d <= SD_WAIT;
            end
          default: st_d <= SD_WAIT;
        endcase
      end
    end
  end

  // ---- tile_buf 捕获（双缓冲：写 gd%2 bank）----
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

  // ---- 写回级 FSM（第2件：双写口；WB2=0 退回单口供拍数对拍）----
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
          // 普通写回：addr = y_base + gw*N + j0 + col，lane = m
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
          // 转置写回：行对 (wb_row8, wb_row8+1) 同拍，全局组 cgr = cgr_lo + wb_g
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
            end else begin
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
          SW_DONE: ;  // SF_FIN 看到后发 done；下一次 SF_INIT 重启
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
