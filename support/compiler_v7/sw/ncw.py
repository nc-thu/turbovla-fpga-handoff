# -*- coding: utf-8 -*-
"""ncw.py —— GEMM 逐列 requant 系数字的统一编解码（编译器 + 双解释器共用）

格式（= RTL 24_pcw_rtn 已验证的格式，位序照抄 sim/gen_vectors.py）：
  GEMM 族描述符（op∈{0,1,2}）占 1+NCW 个 256b 字（NCW = ceil(COLS*24/256)，
  COLS=12→2 字、96→9 字、108→11 字）。头字后平铺逐列系数 blob：
    列 c 的 s（8b）在 blob bit[c*24 +: 8]
    列 c 的 m（有符号 Q8.8 补码 16b）在 blob bit[c*24+8 +: 16]
    字 w = blob bit[w*256 +: 256]（位序 = ae_gemm rq_coeff 总线位序）
  头字 bit28 = RTN 使能（rn_en）；原 rq_m/rq_s 字段对 GEMM 族保留不用。
  非 GEMM 族描述符仍是单字。

2026-09-09（compiler v6）统一裁决：软件链从「OP_SF(op=14) 独立装载 +
rq_s bit7/rq_m bit15 标志」切到本格式，op=14 退役（解释器保留读兼容）。
算术语义零变化——RTN 恒等式与逐列 requant 公式两侧早已逐位对齐（60k 向量门），
本轮只换"系数放在哪、标志读哪一位"。
"""
import numpy as np


def ncw_words(cols):
    """COLS 列的系数字数 NCW = ceil(COLS*24/256)。"""
    return (cols * 24 + 255) // 256


def coeff_words(coef, cols):
    """逐列系数 [(m_c, s_c)]*cols → NCW 个 256b 字（位序 = RTL rq_coeff 总线）。
    与 gen_vectors.coeff_words 逐位一致；m 允许有符号 16b（SW 实际只用正值）。"""
    assert len(coef) == cols, f'coef {len(coef)} 列 != cols {cols}'
    blob = 0
    for c, (mc, sc) in enumerate(coef):
        assert -(1 << 15) <= mc < (1 << 15) and 0 <= sc <= 255, \
            f'列 {c} 系数非法 (m={mc},s={sc})'
        blob |= (mc & 0xFFFF) << (c * 24 + 8)
        blob |= (sc & 0xFF) << (c * 24)
    return [(blob >> (w * 256)) & ((1 << 256) - 1)
            for w in range(ncw_words(cols))]


def parse_coeff(words, cols):
    """coeff_words 的逆：NCW 个 256b 字 → [(m_c, s_c)]*cols（m 转有符号）。
    带 dict 缓存（uniform blob 与同层重发的 pcW blob 高度重复，缓存命中率高）。"""
    key = (tuple(words), cols)
    hit = parse_coeff.cache.get(key)
    if hit is not None:
        return hit
    assert len(words) == ncw_words(cols), \
        f'系数字数 {len(words)} != NCW {ncw_words(cols)} (cols={cols})'
    blob = 0
    for w, wd in enumerate(words):
        blob |= wd << (w * 256)
    coef = []
    for c in range(cols):
        mv = (blob >> (c * 24 + 8)) & 0xFFFF
        if mv >= 0x8000:
            mv -= 0x10000
        coef.append((mv, (blob >> (c * 24)) & 0xFF))
    if len(parse_coeff.cache) > 200000:
        parse_coeff.cache.clear()
    parse_coeff.cache[key] = coef
    return coef


parse_coeff.cache = {}


def uniform(m, s, cols):
    """per-tensor (m,s) 广播成全列 blob（语义 = 旧 per-tensor requant）。"""
    return [(m, s)] * cols


def requant_pc(acc, coef, rn_en):
    """逐列 requant（位精确镜像 rq_v2 / golden 语义）：
    列 c 用 (m_c, s_c)；rn_en=1 且 s_c>=9 加 2^(s_c-1) 就近舍入，否则截断。
    acc: [m, nl] int64（nl <= len(coef)）。"""
    nl = acc.shape[1]
    Y = np.zeros(acc.shape, dtype=np.int64)
    for c in range(nl):
        mc, sc = coef[c]
        prod = acc[:, c] * np.int64(mc)
        if rn_en and sc >= 9:
            prod = prod + np.int64(1 << (sc - 1))
        Y[:, c] = np.clip(prod >> np.int64(sc), -128, 127)
    return Y
