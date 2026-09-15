# -*- coding: utf-8 -*-
'''diff_builds.py — v6 vs v7 build 逐段差异定位（2026-09-10）。
段级对齐：按段序号对齐（两 build 段数不同时找出合并/拆分点），
报每段 (len, op 直方图, y_base 集合) 三元组差异。'''
import sys, os, json
from collections import Counter
sys.path.insert(0, '/tmp/compiler_v6/sw')
import golden_interp as gi

NCW = 10  # 96 列档：GEMM 头后 9 个系数字

def load(build):
    sdir = os.path.join(build, 'segments')
    out = []
    for s in sorted(f for f in os.listdir(sdir) if f.startswith('seg_')):
        seq = gi.load_seq(os.path.join(sdir, s))
        ops, ys, pc = Counter(), set(), 0
        while pc < len(seq):
            f = gi.decode(seq[pc])
            op = f['op']
            if op == 15:
                ops[15] += 1
                break
            ops[op] += 1
            if op in (0, 1, 2):
                ys.add(f['y_base'])
                pc += NCW
            else:
                if op in (5, 6):
                    ys.add(f['y_base'])
                pc += 1
        out.append((s, len(seq), ops, ys))
    return out

a = load(sys.argv[1])
b = load(sys.argv[2])
print('seg counts:', len(a), len(b))
i = j = 0
ndiff = 0
while i < len(a) and j < len(b):
    sa, la, oa, ya = a[i]
    sb, lb, ob, yb_ = b[j]
    if (la, oa) == (lb, ob) and ya == yb_:
        i += 1; j += 1; continue
    ndiff += 1
    if ndiff <= 12:
        print('DIFF', sa, 'len', la, dict(oa), 'ys', sorted(ya)[:4])
        print('  vs', sb, 'len', lb, dict(ob), 'ys', sorted(yb_)[:4])
    i += 1; j += 1
print('aligned diff segs (by index):', ndiff)
