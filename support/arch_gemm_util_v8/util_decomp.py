# -*- coding: utf-8 -*-
"""util_decomp.py — 架构线 v8（2026-09-11 23:15）：B8-48 GEMM 利用率拆账定版 + 四件套修复设计账
+ R5 写通道设计数据（地址连续分布）+ combo a16 情景账。

背景：B8-48 定版后一帧 0.909s（arch v6/v7），其中 GEMM 185.2M 拍、阵列利用率 26.5%。
本脚本把这 26.5% 的浪费拆成三层、归因到形状、给出四件套修复的台阶（V0→V4）和
与 R5 写整形成对兑现的帧账；并为 R5 写通道设计补两块数据（写回地址连续分布 =
合并突发能拼多长、合并后的协议开销），为算法线 v6 的 combo（激活 int16）补
位宽翻倍的交互情景。

口径声明：
- 全部数字来自周期模型（b8_scan 账本，锚定 a3 实测 X/V/W 三锚点），不是 RTL 实测。
- 拍 = 接口拍 @303.215MHz（336.44/319.99 校准挂在 CAL_G）。
- 帧账用真机 HP 口径：帧 = max(计算, 读 20.1, 写 218.4) + θ40（M 拍）。
- R5 后写腿用 arch v7 的 r5_burst 档 = st/8 = 74.3M 拍（写口 8B/拍纯载荷乐观上界，
  不含裁零收益；本脚本的连续分布数据给这个乐观值补协议开销修正）。
- a16 情景只做一阶外推（喂数字节×2、写回字节×2、非 GEMM 计算×2），DSP 打包兼容性
  是开放问题，情景表按"打包仍撑 4 MAC/PE/拍"的乐观假设记。

锚点来源（arch v5 b8_scan.py）：
  CAL_G=336.44/319.99；COPY=40.3 ACTV=10.0 THETA=40.0（M 拍）
  X_ANCHOR=184.0 V_ANCHOR=108.1 W_ANCHOR=218.4（a3 实测）
  BYTES ctx=680.25 w=606.92 st=594.29 MB；HP64_RD=20.1M
输出：控制台全表 + util_decomp.json（供报告页与论文交接包引用）
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.join(os.path.dirname(HERE), 'v5_2026-09-08_1414_b8_sizing_read_compress')
sys.path.insert(0, V5)
import b8_scan as B                                    # noqa: E402（自带 pe_sizing/acct_a3 路径）

wb_cycles, DRAIN, DALIGN = B.wb_cycles, B.DRAIN, B.DALIGN
LC, PEAK, CAL_G, FIX = 96, 3072, B.CAL_G, 20          # 逻辑列/每拍峰值 MAC/GEMM 校准/每 GEMM 固定开销拍
F_IF = 303.215                                          # 接口时钟 MHz
R5_BURST = B.BYTES['st'] / 8.0                          # 74.29M：写口 8B/拍纯载荷
OUT = os.path.join(HERE, 'util_decomp.json')


def tileize(gl):
    """逻辑 GEMM 列表 → (k, mt, n_sub, wb) 行组 tile 列表。"""
    out = []
    for gm in gl:
        for t in range((gm['W'] + LC - 1) // LC):
            n_sub = min(gm['W'], (t + 1) * LC) - t * LC
            wb = max(1, wb_cycles(n_sub, gm['j0'] + t * LC, gm['y_tr']))
            out.append((gm['k'], gm['mt'], n_sub, wb))
    return out


def account(tiles, costfn, ngems):
    G = (sum(costfn(t) for t in tiles) + FIX * ngems) * CAL_G / 1e6
    return G, B.macs0 / (PEAK * G * 1e6) * 100


def cyc_v0(t):
    k, mt, n, wb = t
    return mt * max(k + 2, DRAIN + DALIGN + 2 + wb)


def frames(G):
    comp = G + B.COPY + B.ACTV
    ab = max(comp, B.HP64_RD, B.W_ANCHOR) + B.THETA
    r5 = max(comp, B.HP64_RD, R5_BURST) + B.THETA
    return comp, ab, r5


def main():
    data = B.collect()
    gems, macs = data['gems'], data['macs']
    B.macs0 = macs                                       # account() 里引用（避免全局散落）
    J = {'meta': {'version': 'arch v8', 'ts': '2026-09-11 23:15:00',
                  'f_iface_MHz': F_IF, 'logical_cols': LC, 'peak_mac_per_cycle': PEAK,
                  'cal_G': CAL_G, 'gems': len(gems), 'segs': data['segs'],
                  'macs_G': macs / 1e9}}

    # ---- 1. 现状拆账：三层缺口 ----
    tiles = tileize(gems)
    ideal = macs / PEAK / 1e6
    G0, u0 = account(tiles, cyc_v0, len(gems))
    L2 = sum(t[1] * max(0, DRAIN + DALIGN + 2 + t[3] - (t[0] + 2)) for t in tiles) / 1e6 * CAL_G
    L3 = sum(cyc_v0(t) * (1 - t[2] / LC) for t in tiles) / 1e6 * CAL_G
    L1 = G0 - ideal - L2 - L3
    gap = G0 - ideal
    print('== B8-48 现状：GEMM %.1fM 拍 / util %.1f%% / 理想 %.1fM / 缺口 %.1fM ==' % (G0, u0, ideal, gap))
    print('缺口三层（拍，占缺口比）：')
    print('  D 排空+写出串行 : %.1fM (%.0f%%)' % (L2, L2 / gap * 100))
    print('  W 尾 tile 空列   : %.1fM (%.0f%%)' % (L3, L3 / gap * 100))
    print('  F 喂数天花板     : %.1fM (%.0f%%)' % (L1, L1 / gap * 100))
    print('  合计 %.1fM = 缺口 %.1f' % (L1 + L2 + L3, gap))
    J['baseline'] = dict(G0=G0, util=u0, ideal=ideal, gap=gap,
                         L1_feed=L1, L2_drain=L2, L3_tail=L3)

    # ---- 2. k 分布（按 tile 拍加权）----
    khw = {}
    for t in tiles:
        khw[t[0]] = khw.get(t[0], 0) + cyc_v0(t)
    tot = sum(khw.values())
    ks = sorted(khw)

    def kp(p):
        acc = 0
        for k in ks:
            acc += khw[k]
            if acc >= tot * p:
                return k

    edges = [1, 8, 32, 64, 128, 256, 512, 1024, 10 ** 9]
    buckets = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        cyc = sum(v for k, v in khw.items() if lo <= k < hi) / 1e6 * CAL_G
        mc = 16 * sum(t[1] * t[2] * t[0] for t in tiles if lo <= t[0] < hi) / 1e9   # ×16 行/行组
        cnt = sum(1 for t in tiles if lo <= t[0] < hi)
        buckets.append(dict(lo=lo, hi=min(hi, 4096), tiles=cnt, cyc_M=cyc,
                            cyc_share=cyc / G0 * 100, mac_G=mc))
    print('\n== k 分布（按拍加权）：p10=%d p50=%d p90=%d ==' % (kp(.1), kp(.5), kp(.9)))
    for b in buckets:
        if b['tiles']:
            print('  k %4d~%-4d : tile %5d 个  拍 %6.1fM (%4.1f%%)  MAC %6.2fG'
                  % (b['lo'], b['hi'], b['tiles'], b['cyc_M'], b['cyc_share'], b['mac_G']))
    J['k_dist'] = dict(p10=kp(.1), p50=kp(.5), p90=kp(.9), buckets=buckets)

    # ---- 3. 形状归因 top（按拍）----
    grp = {}
    for t in tiles:
        feedb = t[0] + 2 >= 68 + t[3]
        key = (t[0], t[2], 'feed' if feedb else 'drain')
        grp.setdefault(key, [0, 0])
        grp[key][0] += cyc_v0(t)
        grp[key][1] += 1
    top = sorted(grp.items(), key=lambda kv: -kv[1][0])[:9]
    print('\n== 形状归因（按拍排序 top9）==')
    shape_rows = []
    for (k, n, leg), (cyc, cnt) in top:
        util_t = 16 * n * k / (PEAK * max(k + 2, 68 + max(1, n))) * 100
        print('k=%-5d n=%-3d %-5s 拍 %5.1fM (%4.1f%%)  tile %5d  该形状util上限 %5.1f%%'
              % (k, n, leg, cyc / 1e6 * CAL_G, cyc / 1e6 * CAL_G / G0 * 100, cnt, util_t))
        shape_rows.append(dict(k=k, n=n, bound=leg, cyc_M=cyc / 1e6 * CAL_G,
                               share=cyc / 1e6 * CAL_G / G0 * 100, tiles=cnt,
                               util_ceiling=util_t))
    J['shapes_top'] = shape_rows

    # ---- 4. 相邻 N-合并（调度相邻 <=8 条才拼宽）----
    def merge_adjacent(gl, max_gap=8):
        groups, last_i, last_g = [], {}, {}
        for i, gm in enumerate(gl):
            key = (gm['m'], gm['k'], gm['a_base'], gm['y_tr'])
            if key in last_i and i - last_i[key] <= max_gap:
                g = groups[last_g[key]]
                g['W'] += gm['W']
                g['cnt'] += 1
            else:
                groups.append(dict(W=gm['W'], k=gm['k'], mt=gm['mt'],
                                   y_tr=gm['y_tr'], j0=gm['j0'], cnt=1))
                last_g[key] = len(groups) - 1
            last_i[key] = i
        return groups

    merged = merge_adjacent(gems)
    multi = [g for g in merged if g['cnt'] > 1]
    print('\n== N-合并（调度相邻<=8 才拼宽）==')
    print('合并组 %d / 其中多切组 %d / 合并后 GEMM %d（原 %d）'
          % (len(merged), len(multi), len(merged), len(gems)))
    for g in sorted(multi, key=lambda g: -g['cnt'])[:6]:
        print('   W_total=%-6d（%d 条，原均宽 %.0f）' % (g['W'], g['cnt'], g['W'] / g['cnt']))
    J['n_merge'] = dict(groups=len(merged), multi=len(multi), orig=len(gems),
                        top=[dict(W=g['W'], cnt=g['cnt']) for g in sorted(multi, key=lambda g: -g['cnt'])[:6]])

    # ---- 5. 修复阶梯 + 帧账（真机 HP 口径，含 R5 成对）----
    V48 = B.V_M(data['w_loads'], data['v108'], 48)
    print('\n== 修复阶梯（util / GEMM 拍 / 帧拍[真机HP口径]）==')
    print('锚：comp=G+%.1f；帧=max(comp, 读20.1, 写218.4|74.3)+40；TB 读腿 X+V=%.1f 不用'
          % (B.COPY + B.ACTV, B.X_ANCHOR + V48))
    ladder = []

    def report(name, tiles_, costfn, ngems, note=''):
        G, u = account(tiles_, costfn, ngems)
        comp, ab, r5 = frames(G)
        print('%-44s util %5.1f%%  GEMM %6.1fM  帧(R5前) %6.1fM=%.3fs  帧(R5后) %6.1fM=%.3fs'
              % (name, u, G, ab, ab / F_IF, r5, r5 / F_IF))
        ladder.append(dict(name=name, util=u, G=G, comp=comp,
                           frame_s=ab / F_IF, frame_r5_s=r5 / F_IF, note=note))
        return G

    report('V0 现状', tiles, cyc_v0, len(gems))
    report('V1 累加器乒乓（排空每 tile 付一次）', tiles,
           lambda t: t[1] * max(t[0] + 2, t[3]) + 68, len(gems))
    report('V1+ 写出链 2 倍宽（wb/2）', tiles,
           lambda t: t[1] * max(t[0] + 2, t[3] / 2) + 68, len(gems))
    c2 = lambda t: t[1] * max((t[0] + 1) // 2 + 2, t[3] / 2) + 68          # noqa: E731
    report('V2 = V1+ + A 喂数 2 倍（k/2）', tiles, c2, len(gems),
           note='峰值口径裁决件：让 4 MAC/PE/拍 的 931 GMAC/s 变成可达')
    mtiles = tileize(merged)
    report('V3 = V2 + 相邻 N-合并（编译器）', mtiles, c2, len(merged))
    v4 = lambda t: (t[1] / 8 if t[0] <= 8 else t[1]) * max(               # noqa: E731
        (t[0] * 8 if t[0] <= 8 else t[0]) // 2 + 2, t[3] / 2) + 68
    report('V4 = V3 + 小K 8 拼段（上界）', mtiles, v4, len(merged))
    G80 = ideal / 0.8
    comp, ab, r5 = frames(G80)
    print('%-44s util 80.0%%  GEMM %6.1fM  帧(R5前) %6.1fM=%.3fs  帧(R5后) %6.1fM=%.3fs'
          % ('（参照：80% 目标落点）', G80, ab, ab / F_IF, r5, r5 / F_IF))
    ladder.append(dict(name='REF 80%', util=80.0, G=G80, comp=comp,
                       frame_s=ab / F_IF, frame_r5_s=r5 / F_IF, note='需第五件（跨段列拼），本轮不做'))
    J['ladder'] = ladder

    # ---- 6. R5 写通道设计数据：写回地址连续分布（扫 op=5 store 指令）----
    # 一条 store 指令 = 一次连续 DMA 写；dma_len 就是"不跨指令能拼出的最长连续段"。
    # 合并突发模型：数据拍 = len/8（写口 8B/拍）；每 2048B 一个 AXI 突发、每突发 2 拍命令开销。
    store_lens = []
    for s in sorted(os.listdir(os.path.join(B.BUILD, 'segments'))):
        for line in open(os.path.join(B.BUILD, 'segments', s, 'seq.mem')):
            line = line.strip()
            if not line:
                continue
            d = B.decode(int(line, 16))
            if d['op'] == 5:
                store_lens.append(d['dma_len'])
    st_b = sum(store_lens)
    rows_tot = st_b / 16
    beats = st_b / 8
    ovh = sum(2 * -(-n // 2048) for n in store_lens)
    hist_edges = [0, 32, 128, 512, 2048, 10 ** 12]
    run_hist = []
    for lo, hi in zip(hist_edges[:-1], hist_edges[1:]):
        sel = [n for n in store_lens if lo < n <= hi]
        run_hist.append(dict(lo=lo, hi=min(hi, 65536), stores=len(sel),
                             bytes_MB=sum(sel) / 1e6, byte_share=sum(sel) / st_b * 100))
    print('\n== R5 写通道：写回连续分布（op=5 store 指令 %d 条）==' % len(store_lens))
    print('总字节 %.2fMB（账本 st=%.2fMB）= 行 %.1fM 条' % (st_b / 1e6, B.BYTES['st'], rows_tot / 1e6))
    for h in run_hist:
        if h['stores']:
            print('  连续段 %5d~%-5dB : %5d 条（%.1f%%）  字节 %6.1fMB（%.1f%%）'
                  % (h['lo'], h['hi'], h['stores'], h['stores'] / len(store_lens) * 100,
                     h['bytes_MB'], h['byte_share']))
    print('合并突发模型：数据 %.1fM 拍 + 突发命令开销 %.2fM 拍 = %.1fM 拍（开销占比 %.2f%%）'
          % (beats / 1e6, ovh / 1e6, (beats + ovh) / 1e6, ovh / (beats + ovh) * 100))
    print('对照：现状逐行 6 拍 = %.1fM 拍；r5_burst 乐观档 %.1fM 拍' % (rows_tot * 6 / 1e6, R5_BURST))
    print('裁零（整行全零不发）：需要运行期数据值，本轮未统计——R5 收益按不含裁零记账')
    # 写地板观察（为什么 V4 只标上界）
    print('写地板：k=4 满宽 tile 理想 2 拍要搬出 1536 个结果 = 768 结果/拍；')
    print('  现写链 16 结果/拍、4 倍宽也只 64/拍 → 小 K 撑满大阵列物理不可能，只能拼 K 或不上大阵列')
    J['write_channel'] = dict(stores=len(store_lens), total_bytes_MB=st_b / 1e6,
                              total_rows_M=rows_tot / 1e6,
                              as_built_M=rows_tot * 6 / 1e6, r5_burst_M=R5_BURST,
                              merged_M=(beats + ovh) / 1e6, burst_overhead_M=ovh / 1e6,
                              overhead_pct=ovh / (beats + ovh) * 100,
                              run_hist=run_hist, zero_skip='未统计（需运行期数据值）')

    # ---- 7. a16 情景（combo：激活 int16 + decoder fp32，权重仍 int8）----
    # 一阶外推：A 喂数字节×2（V2 的 2 倍喂料刚好吸收回 1 a/拍）；写回字节×2；
    # 非 GEMM 计算（COPY+ACTV）×2；读腿 ctx×2 仍远小于计算腿。
    # DSP 打包：int16×int8 能否仍 4 MAC/PE/拍 是开放问题，本表按乐观（能）记。
    print('\n== a16 情景（算法线 v6 combo 的硬件代价，一阶外推）==')
    st2 = B.BYTES['st'] * 2
    r5_a16 = st2 / 8
    rd_a16 = (B.BYTES['ctx'] * 2 + B.BYTES['w']) / 64
    print('喂数字节×2：不修 V2 时 feed k+2 → 2k+2（比现状更糟）；V2 双 bank 恰好吸收回 k+2')
    print('写回字节×2：R5 后写腿 %.1fM 拍（int8 是 %.1fM）' % (r5_a16, R5_BURST))
    print('读腿 %.1fM 拍（int8 是 %.1fM）——仍远小于计算腿，不构成新瓶颈' % (rd_a16, B.HP64_RD))
    a16_rows = []
    scenarios = [('V4+R5（int8 基准）', B.HP64_RD, R5_BURST, 1),
                 ('V4+R5（a16 乐观）', rd_a16, r5_a16, 2),
                 ('V4+R5+写口16B（a16）', rd_a16, st2 / 16, 2)]
    for name, rd, wr, mult in scenarios:
        comp = ladder[-2]['G'] + (B.COPY + B.ACTV) * mult
        fr = max(comp, rd, wr) + B.THETA
        a16_rows.append(dict(name=name, comp_M=comp, write_M=wr, frame_M=fr, frame_s=fr / F_IF))
        print('%-24s comp %.1fM  写腿 %.1fM  帧 %.1fM = %.3fs' % (name, comp, wr, fr, fr / F_IF))
    print('结论：a16 下绑定的是计算腿 %.1fM（非 GEMM 的 COPY/ACTV 翻倍到 %.1fM 占大头），'
          '写腿 %.1fM 紧随；写口加宽到 16B（%.1fM）帧不变（%.3fs，仍计算绑）。'
          '→ a16 的主要代价在计算/搬运侧，写口加宽不是首要矛盾；DSP 打包兼容性需硬件线专项评估'
          % (a16_rows[1]['comp_M'], (B.COPY + B.ACTV) * 2, a16_rows[1]['write_M'],
             a16_rows[2]['write_M'], a16_rows[2]['frame_s']))
    J['a16_scenario'] = dict(rows=a16_rows, rd_M=rd_a16, write_r5_M=r5_a16,
                             write_floor_16B_M=st2 / 16,
                             open_questions=['int16 激活 × int8 权重能否仍 4 MAC/PE/拍 打包（DSP48E2 27×18）',
                                             'decoder fp32 上芯片的单独设计',
                                             'ctx×2 里 decoder 边界的 fp32 部分未单独拆'])

    json.dump(J, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('\nJSON -> %s' % OUT)


if __name__ == '__main__':
    main()
