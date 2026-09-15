# -*- coding: utf-8 -*-
"""f4_pong_proof.py — F4 编译器侧 y_base 乒乓的前提证明（2026-09-10 开轮）。

用户裁决的前提：y_base 乒乓（两块暂存区）成立，当且仅当"两块暂存区足够
覆盖写回存活期"。证明是结构性的，不依赖拍数余量：

  S1a (ae_sched.sv:246-254)：op=5 STORE 的**发射**门槛是 !wr_busy —— 上一条
     STORE 写引擎排空（对 CTX 的读全部完成）前，下一条 STORE 不能发射。
  S1b (ae_sched.sv T_EXEC)：op=4 LOAD 的发射门槛是 !dma_busy
     (= rd_busy | wr_busy，ae_dma.sv:310) —— LOAD 发射前写引擎同样已排空。
  S2 (ae_sched.sv:237-312)：调度器严格按流序执行（T_EXEC 逐条推进，
     COPY 等 cp_done、GEMM 等 g_done；fire-and-forget 只免等完成，不改顺序）。
  S3 (本脚本验证)：对每个 y 链的每个读者 r_j，它与下一个同奇偶写者 w 之间
     存在另一条 op∈{4,5} 发射 s（r_j < s < w）。s 的发射时刻 wr 已排空
     （S1a/S1b），w 的执行又在 s 的发射之后（S2）⇒ r_j 的存活期被完全覆盖。
     注：门控只算 op=5 会把"LOAD 排空"类段误报为违反（它们本来就安全，
     f4_scan2 的危险对判据=STORE 后无 op=4 清除即被同 y GEMM 命中，不含它们）。

乒乓分配：每个 y 链内，写者按流序编号 i → 缓冲 i%2；读者按流序编号 j →
缓冲 j%2（swin 相位一 [COPY GEMM STORE]*nb 形态下写者 j 与读者 j 同号）。

用法（服务器）:
  python f4_pong_proof.py /tmp/compiler_v6/build_s000_v6_96 96
  python f4_pong_proof.py /tmp/compiler_v6/build_s000_v6_full_fix1 108
"""
import sys, os, json
from collections import defaultdict

sys.path.insert(0, '/tmp/compiler_v6/sw')
import golden_interp as gi


def walk_segment(sdir, name, cols):
    """返回事件流 [(pc, op, y_base, extra)]。GEMM 族跨 NCW 系数字步进。"""
    ncw = (cols * 24 + 255) // 256
    seq = gi.load_seq(os.path.join(sdir, name))
    evs = []
    pc = 0
    while pc < len(seq):
        f = gi.decode(seq[pc])
        op = f['op']
        if op == 15:
            evs.append((pc, 15, None, None))
            break
        if op in (0, 1, 2):
            evs.append((pc, op, f['y_base'], (f['m'], f['n'], f['k'])))
            pc += 1 + ncw
        else:
            if op == 5:
                evs.append((pc, 5, f['y_base'], f['dma_len']))
            elif op == 6:
                evs.append((pc, 6, f['y_base'], None))  # ACTV 张量基址同 y 位
            else:
                evs.append((pc, op, None, None))
            pc += 1
    return evs


def analyze(evs):
    """乒乓模拟 + S3 门控性质检查。返回 (violations, actv_hits, writers, readers)。"""
    writers = defaultdict(list)   # y -> [pc]（流序）
    readers = defaultdict(list)   # y -> [(pc, dma_len)]（流序）
    actv_touch = defaultdict(int)
    for pc, op, y, ex in evs:
        if op in (0, 1, 2):
            writers[y].append(pc)
        elif op == 5:
            readers[y].append((pc, ex))
        elif op == 6 and y is not None:
            actv_touch[y] += 1
    store_pcs = [pc for pc, op, y, ex in evs if op == 5]
    gate_pcs = [pc for pc, op, y, ex in evs if op in (4, 5)]  # 两类发射都排空写引擎
    violations = []
    strict5 = []
    for y, rlist in readers.items():
        wlist = writers.get(y, [])
        if not wlist:
            continue              # 无写者：无 F4 形态
        wpos = {pc: i for i, pc in enumerate(wlist)}   # 位置 → 链内序号
        for j, (rpc, L) in enumerate(rlist):
            later = [wpc for wpc in wlist if wpc > rpc]
            same_par = next((wpc for wpc in later
                             if wpos[wpc] % 2 == j % 2), None)
            if same_par is None:
                continue          # 之后无同缓冲写者（链尾）
            if not any(rpc < s < same_par for s in gate_pcs):
                violations.append(dict(y=y, reader_pc=rpc, store_len=L,
                                       next_same_parity_writer=same_par))
            elif not any(rpc < s < same_par for s in store_pcs):
                strict5.append((y, rpc, same_par))   # 靠 LOAD 排空（本就安全）
    actv_hits = {y: c for y, c in actv_touch.items()
                 if y in writers or y in readers}
    return violations, strict5, actv_hits, writers, readers


def is_swin_phase1(evs):
    """识别 swin 相位一形态：LOAD* 头 + 严格 (COPY GEMM STORE) 循环 + DONE，
    且 GEMM/STORE 共用唯一 y。返回 (nb, store_len, (m,n,k)) 或 None。"""
    ops = [(op, y) for pc, op, y, ex in evs]
    if not ops or ops[-1][0] != 15:
        return None
    body = ops[:-1]
    n_head = 0
    while n_head < len(body) and body[n_head][0] == 4:
        n_head += 1
    tail = body[n_head:]
    if not tail or any(o not in (3, 0, 5) for o, y in tail):
        return None
    if not ({o for o, y in tail} == {3, 0, 5}):
        return None
    # 循环周期必须正好是 COPY GEMM STORE
    if len(tail) % 3:
        return None
    for k in range(0, len(tail), 3):
        if [tail[k][0], tail[k + 1][0], tail[k + 2][0]] != [3, 0, 5]:
            return None
    gemm_ys = {y for o, y in tail if o == 0}
    store_ys = {y for o, y in tail if o == 5}
    if len(gemm_ys) != 1 or gemm_ys != store_ys:
        return None
    nb = len(tail) // 3
    L = next(ex for pc, op, y, ex in evs if op == 5)
    shape = next(ex for pc, op, y, ex in evs if op == 0)
    return nb, L, shape


def main():
    build = sys.argv[1]
    cols = int(sys.argv[2]) if len(sys.argv) > 2 else 96
    sdir = os.path.join(build, 'segments')
    seg_files = sorted(f for f in os.listdir(sdir) if f.startswith('seg_'))
    agg = dict(build=build, cols=cols, n_seg=len(seg_files),
               segs_with_y_chain=0, segs_swin_phase1=0, segs_violation=0,
               violations=[], actv_touch_segs=0, chain_shapes={},
               strict5_pairs=0, strict5_segs=0,
               examples=[], load_errors=[])
    for s in seg_files:
        try:
            evs = walk_segment(sdir, s, cols)
        except Exception as e:
            agg['load_errors'].append((s, str(e)))
            continue
        violations, strict5, actv_hits, writers, readers = analyze(evs)
        if strict5:
            agg['strict5_segs'] += 1
            agg['strict5_pairs'] += len(strict5)
        if any(y in writers for y in readers):
            agg['segs_with_y_chain'] += 1
        if violations:
            agg['segs_violation'] += 1
            agg['violations'].extend(dict(seg=s, **v)
                                     for v in violations[:4])
        if actv_hits:
            agg['actv_touch_segs'] += 1
        sw = is_swin_phase1(evs)
        if sw:
            nb, L, shape = sw
            agg['segs_swin_phase1'] += 1
            key = f'm={shape[0]},n={shape[1]},k={shape[2]},len={L},nb={nb}'
            agg['chain_shapes'][key] = agg['chain_shapes'].get(key, 0) + 1
            if len(agg['examples']) < 6:
                agg['examples'].append(dict(seg=s, nb=nb, len=L, shape=shape))
    agg['verdict'] = ('PASS: S3 holds on all segments'
                      if agg['segs_violation'] == 0 and not agg['load_errors']
                      else 'FAIL')
    print(json.dumps(agg, indent=1, ensure_ascii=False, default=str))


if __name__ == '__main__':
    main()
