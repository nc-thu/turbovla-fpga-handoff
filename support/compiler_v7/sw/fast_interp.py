# -*- coding: utf-8 -*-
"""fast_interp.py — 段解释器的向量化版（与 golden_interp.run_segment 逐位一致）。

golden_interp 是纯 Python 循环，一个真实段（~100 描述符、m=49/k=32）要跑
十几秒，3102 段不现实。本模块把五种 op 全部 numpy 向量化：

  LOAD CTX  字节流 k-major：byte b → ctx[b%16, b_base+b//16]
  LOAD W    字节流按「每 k 恰好 COLS 字节」路由（列主序）
  STORE     字节流 word-major（word w 的 16 lane 连续 16 字节）
  COPY      wram[j, a_base+kk] = ctx[(s+j)%16, b_base+((s+j)//16)*spad+kk]
  GEMM      A=CTX 行主（pitch=k），B=WRAM 列取（b_base..+k，前 n_loc 列），
            requant 恒逐列：v6 统一格式 GEMM 头字后挂 NCW 个系数字
            （ncw.py 解码），y[:,j]=sat8(acc·m_j + rn_j >> s_j)，
            rn_j=2^(s_j-1) 当头字 bit28=1 且 s_j>=9；散射 y_tr / 普通 两种，
            op=1 后接硬 softmax。
  旧格式（op=14 OP_SF + rq_s bit7/rq_m bit15）保留只读兼容：看 DONE 字
            bit27 判格式（编译器 v6 发 1，旧 build 全 0），旧流走旧路径。
            详见 golden_interp 头注释。

所有寻址公式与 golden_interp.run_segment 逐字相同（只是把循环换成 fancy
索引），fast_selftest.py 在真实 build 段上做过逐位对拍。

用法：
  from fast_interp import run_segment_fast      # (seq, ddr, P) -> (ctx, ddr)
"""
import numpy as np

from golden_interp import EXP, decode, sat8, _s8
from ncw import ncw_words, parse_coeff

_EXPNP = np.array(EXP, dtype=np.int64)


def _softmax_rows_fast(S, n_cols, causal):
    """golden_interp.softmax_rows 的向量化版（逐位一致）。"""
    m = S.shape[0]
    P = np.zeros_like(S)
    if m == 0 or n_cols == 0:
        return P
    if causal:
        vlen = np.minimum(np.arange(m) + 1, n_cols)
    else:
        vlen = np.full(m, n_cols)
    S64 = S.astype(np.int64)
    # 行最大值只看前 vlen 列：不足处用 +inf 语义（exp=0）
    NEG = 1 << 60
    masked = np.where(np.arange(n_cols)[None, :] < vlen[:, None], S64, NEG)
    mx = masked.max(axis=1)
    di = np.minimum(mx[:, None] - S64, 128)
    di = np.where(np.arange(n_cols)[None, :] < vlen[:, None], di, 0)
    e = _EXPNP[di]
    e = np.where(np.arange(n_cols)[None, :] < vlen[:, None], e, 0)
    se = e.sum(axis=1)
    quo = (np.int64(127) << np.int64(30)) // se
    p = (e * quo[:, None]) >> np.int64(30)
    p = np.minimum(p, 127)
    P = np.where(np.arange(n_cols)[None, :] < vlen[:, None], p, 0)
    return P.astype(np.int64)


def run_segment_fast(seq, ddr_img, P):
    cols, ctxw, ww = P['COLS'], P['CTX_WORDS'], P['W_WORDS']
    ddr = ddr_img.copy()
    ctx = np.zeros((16, ctxw), dtype=np.int64)
    wram = np.zeros((cols, ww), dtype=np.int64)
    sf_m = np.zeros(cols, dtype=np.int64)    # 旧格式逐列系数（OP_SF，读兼容）
    sf_s = np.zeros(cols, dtype=np.int64)
    # 格式自动判别：DONE 字 bit27=1 = v6（GEMM 后挂 NCW 系数字）；否则旧格式
    # （op=14 OP_SF + rq 标志位，含纯 per-tensor 无 op=14 的历史构建）。
    # 只看段末字（DONE 恒为最后字）——系数字高 4 bit 可为 15，扫全流会误判
    # （真实 build 72/1049 段踩中，2026-09-09 修，详见 golden_interp）。
    done = seq[-1] if seq and ((seq[-1] >> 252) & 0xF) == 15 else None
    legacy = not (done is not None and (done >> 27) & 1)
    n_cw = ncw_words(cols)
    macs = 0
    pc = 0
    n_seq = len(seq)
    while pc < n_seq:
        d = seq[pc]
        f = decode(d)
        op = f['op']
        if op == 15:
            break
        m, n, k = f['m'], f['n'], f['k']
        if op == 14:                                   # SF 系数装载（旧格式）
            assert legacy, f'pc={pc}: op=14 只允许出现在旧格式流'
            slot0 = (d >> 240) & 0xFFF
            vals = np.array([(d >> (24 * i)) & 0xFFFFFF for i in range(10)],
                            dtype=np.int64)             # 10 个 24b 槽
            jj = slot0 + np.arange(10)
            ok = jj < cols
            sf_m[jj[ok]] = (vals[ok] >> 8) & 0xFFFF
            sf_s[jj[ok]] = vals[ok] & 0xFF
        elif op == 4:                                  # LOAD
            nB = f['dma_len']
            B = _s8(ddr[f['dma_addr']:f['dma_addr'] + nB]).astype(np.int64)
            if f['b_src'] == 0:                        # CTX k-major
                base = f['b_base']
                fw = nB // 16
                if fw:
                    ctx[:, base:base + fw] = B[:fw * 16].reshape(fw, 16).T
                rem = nB - fw * 16
                if rem:
                    ctx[:rem, base + fw] = B[fw * 16:]
            else:                                      # W 每 k 行 COLS 字节
                base = f['b_base']
                nwd = nB // cols
                if nwd:
                    wram[:, base:base + nwd] = B[:nwd * cols].reshape(nwd,
                                                                     cols).T
                rem = nB - nwd * cols
                if rem:
                    wram[:rem, base + nwd] = B[nwd * cols:]
        elif op == 5:                                  # STORE word-major
            W = f['dma_len'] // 16
            base = f['y_base']
            seg = np.ascontiguousarray(ctx[:, base:base + W].T)
            ddr[f['dma_addr']:f['dma_addr'] + W * 16] = \
                (seg & 0xFF).astype(np.uint8).reshape(-1)
        elif op == 3:                                  # COPY CTX→WRAM
            src_j0 = f['rq_m']
            nr = n & 0xFF
            rows = src_j0 + np.arange(nr)
            lanes = rows % 16
            words = f['b_base'] + (rows // 16) * f['b_spad']
            idx = words[:, None] + np.arange(k)[None, :]
            wram[:nr, f['a_base']:f['a_base'] + k] = ctx[lanes[:, None], idx]
        elif op in (0, 1, 2):                          # GEMM 族
            macs += ((m + 15) // 16) * 16 * cols * k
            ai = np.arange(m)
            idxA = f['a_base'] + (ai // 16)[:, None] * k + \
                np.arange(k)[None, :]
            A = ctx[(ai % 16)[:, None], idxA]
            B = wram[:, f['b_base']:f['b_base'] + k].T[:, :f['b_spad']]
            acc = A @ B
            if legacy:                                 # 旧格式 requant
                if f['rq_pc']:                         # 逐列系数 + RTN
                    nl = f['b_spad']
                    assert int(sf_m[:nl].min()) >= 1, \
                        f'pc={pc}: sf 槽未装载（m=0）'
                    mv = sf_m[:nl][None, :]
                    sv = sf_s[:nl][None, :]
                    rv = (np.int64(1) << (sv - 1)) if f['rq_rn'] else \
                        np.zeros_like(sv)
                    Y = sat8(acc * mv + rv >> sv)
                else:
                    rn = (np.int64(1) << np.int64(f['rq_s'] - 1)) \
                        if f['rq_rn'] else np.int64(0)
                    Y = sat8(acc * np.int64(f['rq_m']) + rn
                             >> np.int64(f['rq_s']))
            else:          # v6：头字后 NCW 字锁逐列系数，恒逐列语义
                nl = f['b_spad']
                coef = parse_coeff(seq[pc + 1:pc + 1 + n_cw], cols)
                assert int(min(c[0] for c in coef[:nl])) >= 1, \
                    f'pc={pc}: 系数字未跟（m=0）'
                mv = np.array([c[0] for c in coef[:nl]],
                              dtype=np.int64)[None, :]
                sv = np.array([c[1] for c in coef[:nl]],
                              dtype=np.int64)[None, :]
                rv = (np.where(sv >= 9, np.int64(1) << np.maximum(sv - 1, 0),
                               np.int64(0)) if f['rn_en']
                      else np.zeros_like(sv))
                Y = sat8(acc * mv + rv >> sv)
            m16 = ((m + 15) // 16) * 16
            nl = f['b_spad']
            if f['y_tr']:
                c = f['j0'] + np.arange(nl)
                valid = np.nonzero(c < n)[0]
                cc = c[valid]
                lanes = (cc % 16)[:, None]
                words = (f['y_base'] + (cc // 16) * m16)[:, None] + \
                    np.arange(m)[None, :]
                ctx[lanes, words] = Y[:, valid].T
            else:
                words = (f['y_base'] + (ai // 16) * n + f['j0'])[:, None] + \
                    np.arange(nl)[None, :]
                ctx[(ai % 16)[:, None], words] = Y
            if op == 1:                                # SM16 softmax
                idxS = (f['y_base'] + (ai // 16) * n)[:, None] + \
                    np.arange(n)[None, :]
                S = ctx[(ai % 16)[:, None], idxS]
                Pm = _softmax_rows_fast(S.astype(np.int8), n, f['sm_causal'])
                ctx[(ai % 16)[:, None], idxS] = Pm
        else:
            raise AssertionError(f'pc={pc}: 未定义 op={op}')
        if op in (0, 1, 2) and not legacy:
            pc += 1 + n_cw               # v6：跨过跟在头字后的 NCW 系数字
        else:
            pc += 1
    return ctx, ddr, dict(macs=macs)
