# -*- coding: utf-8 -*-
"""f4_anchor.py — F4 前提证明的 VCD 实测锚点（2026-09-10）。

对当前（单缓冲）build 的 swin 段跑 Verilator --trace，dump 子作用域 VCD，
提取三类事件并用时间戳验证结构性证明的三条顺序：

  A_k: t_lastread(STORE k)  < t_issue(STORE k+1)      ← S1a（!wr_busy 发射门）
  B_k: t_issue(STORE k+1)  < t_firstwrite(GEMM k+2)   ← S2（按流序执行）
  R_k: t_firstwrite(GEMM k+1) < t_lastread(STORE k)   ← 今天单缓冲的竞态本体

A+B 合起来 = 乒乓下缓冲 k%2 的写（GEMM k+2）严格晚于它的最后一次读
（STORE k）——"两块暂存区覆盖写回存活期"的实测版。
R 解释今天为什么咬：GEMM k+1（写同一块缓冲）的写回先于写引擎读完。

Verilator 的 $dumpvars 连作用域参数也忽略（本轮实测：dut 全层级 dump 3.75GB，
上轮 vcd_sweep 的"子作用域"实际也是全量、靠解析时按名字过滤），所以一次仿真
出全量 VCD、解析时按全路径名取两组信号：
  dut.u_dma.start + cmd_is_wr = STORE/LOAD 发射
  dut.u_dma.wr_st==W_RD(2) 且 ctxa_wr_bank=1 = 写引擎一行 16B CTX 读被服务
  （地址 dut.u_dma.ctx_raddr）
  dut.u_gemm.ctxb_we=1 且 ctxb_addr 落在 y 区间 = GEMM 写回

用法（服务器 /tmp/hw_v7）:
  python f4_anchor.py /tmp/compiler_v6/build_s000_v6_96 seg_0003 [--reuse]
  --reuse：run 目录里已有 vcd_f4.vcd 时跳过仿真只重解析（VCD ~3.5GB，仿真 98s、
  解析 ~280s，都在 10 分钟内；跑完记得删 VCD，服务器 /tmp 只剩 ~41G）
"""
import sys, os, json, shutil, subprocess, zlib, time
import numpy as np

sys.path.insert(0, '/tmp/compiler_v6/sw')
import golden_interp as gi
from rtl_seg import write_sparse_mem

BIN = '/tmp/hw_v7/obj_f4/Vtb_ae_f4'
RUNROOT = '/tmp/hw_v7/run'
LUTS = '/tmp/pcw_rtl_v6'
FULL = {'dut.u_dma.start', 'dut.u_dma.cmd_is_wr', 'dut.u_dma.wr_st',
        'dut.u_dma.ctxa_wr_bank', 'dut.u_dma.ctx_raddr',
        'dut.g_ctxb_we', 'dut.g_ctxb_addr', 'clk'}
W_RD = 2                                      # enum {W_IDLE,W_AW,W_RD,W_RD2,...}


def prep_run(build, segname):
    """照 gate_v7.run_one 口径准备运行目录；返回 (wd, seg_dir, y_base, y_words)。"""
    seg_dir = os.path.join(build, 'segments', segname)
    man = json.load(open(os.path.join(seg_dir, 'manifest.json')))
    P = man['profile']
    act = {}
    for e in man['inputs']:
        rng = np.random.default_rng(zlib.crc32(e['name'].encode()))
        act[e['name']] = rng.integers(-128, 128, size=e['words'] * 16,
                                      dtype=np.int16).astype(np.int8)
    ddr0 = gi.build_ddr_image(seg_dir, os.path.join(build, 'weights_blob.bin'),
                              act, P)
    seq = gi.load_seq(seg_dir)
    y_base, y_words = None, None
    pc = 0
    while pc < len(seq):                    # 正确跳过 GEMM 头后的 NCW 系数字
        f = gi.decode(seq[pc])
        op = f['op']
        if op == 15:
            break
        if op in (0, 1, 2):
            if y_base is None:
                y_base = f['y_base']       # 首个 GEMM 的 y = swin 的 sreg
            pc += 1 + (P['COLS'] * 24 + 255) // 256
            continue
        if op == 5 and y_words is None:
            y_words = (f['dma_len'] + 15) // 16
        pc += 1
    wd = os.path.join(RUNROOT, segname + '_f4')
    os.makedirs(wd, exist_ok=True)
    for f_ in ('rsqrt_lut.mem', 'exp2_lut.mem'):
        dst = os.path.join(wd, f_)
        if not os.path.exists(dst):
            shutil.copy(os.path.join(LUTS, f_), dst)
    shutil.copy(os.path.join(seg_dir, 'seq.mem'), os.path.join(wd, 'seq.mem'))
    dmem = os.path.join(wd, 'ddr_init.mem')
    if not os.path.exists(dmem):
        write_sparse_mem(dmem, ddr0, gap=64)
    return wd, seg_dir, y_base, y_words


def run_rtl(wd, seg_dir, binpath, tmo=400):
    dump = os.path.join(wd, 'dump.mem')
    if os.path.exists(dump):
        os.remove(dump)
    r = subprocess.run([binpath, '+MODE=1', '+PF=1',
                        '+SEQ=' + os.path.join(seg_dir, 'seq.mem'),
                        '+DDRIMG=' + os.path.join(wd, 'ddr_init.mem'),
                        '+DUMP=' + dump],
                       cwd=wd, capture_output=True, text=True, timeout=tmo)
    return r.stdout


def collect_events(path, on_ts):
    """只在 clk 上升沿时间戳调用 on_ts(ts, cur, code_of)。
    为什么：VCD 每拍有两个时间戳（clk=1 与 clk=0 的半拍），快照式逐时间戳
    求值会把持续一整拍的高电平（如 start 脉冲）记两次——上一轮 n_iter=192
    （真值 96）就是双计。改成"本时间戳变更集里 clk 变为 1 才求值"后每拍恰一次，
    求值用的 cur 是该上升沿后的落定值。
    注意：Verilator 给别名信号（如端口线与父层连线）复用同一 id 码，
    同一码可挂多个名字——必须按 码→[名字们] 收集，否则后声明者覆盖前者。"""
    from collections import defaultdict
    code_names, scope = defaultdict(list), []
    fh = open(path, 'r', errors='replace')
    for line in fh:
        s = line.strip()
        if s.startswith('$scope'):
            scope.append(s.split()[2])
        elif s.startswith('$upscope'):
            scope.pop()
        elif s.startswith('$var'):
            p = s.split()
            code_names[p[3]].append('.'.join(scope[1:] + [p[4]]))
        elif s.startswith('$enddefinitions'):
            break
    code_of = {}
    for c, ns in code_names.items():
        for n in ns:
            if n in FULL:
                code_of[n] = c
    missing = FULL - set(code_of)
    if missing:
        raise RuntimeError('%s 缺信号 %s' % (path, sorted(missing)))
    clk = code_of['clk']
    cur, chg, ts = {}, {}, None

    def flush():
        if ts is not None and chg.get(clk) == '1':   # 本拍 clk 升到 1 才求值
            on_ts(ts, cur, code_of)
        chg.clear()

    for line in fh:
        s = line.strip()
        if not s or s[0] == '$':
            continue
        if s[0] == '#':
            flush()
            ts = int(s[1:])
            continue
        if s[0] in 'bB':
            parts = s.split()
            if len(parts) != 2:
                continue
            val, code = parts[0][1:], parts[1]
        elif s[0] in '01xzXZ':
            val, code = s[0], s[1:]
        else:
            continue
        cur[code] = val
        chg[code] = val
    flush()
    fh.close()


def iv(cur, code):
    v = cur.get(code)
    return None if v is None or any(ch in v for ch in 'xzXZ') else int(v, 2)


def main():
    build, segname = sys.argv[1], sys.argv[2]
    wd, seg_dir, y_base, y_words = prep_run(build, segname)

    ev = dict(store_issues=[], load_issues=[], wr_reads=[], wb_y=[])
    t0 = time.time()
    vcd = os.path.join(wd, 'vcd_f4.vcd')
    if '--reuse' in sys.argv and os.path.exists(vcd):
        out = '(复用已存在的 vcd_f4.vcd，未重跑仿真)'
    else:
        out = run_rtl(wd, seg_dir, BIN)

    def on_ts(ts, cur, code_of):
        def val(name):
            c = code_of.get(name)
            return cur.get(c) if c else None
        if (val('dut.u_dma.start') or '0')[-1] == '1':
            iswr = (val('dut.u_dma.cmd_is_wr') or '0')[-1]
            (ev['store_issues'] if iswr == '1' else
             ev['load_issues']).append(ts)
        wrst = val('dut.u_dma.wr_st')
        if wrst is not None and int(wrst, 2) == W_RD and \
           (val('dut.u_dma.ctxa_wr_bank') or '0')[-1] == '1':
            a = iv(cur, code_of.get('dut.u_dma.ctx_raddr'))
            if a is not None:
                ev['wr_reads'].append((ts, a))
        if (val('dut.g_ctxb_we') or '0')[-1] == '1':
            a = iv(cur, code_of.get('dut.g_ctxb_addr'))
            if a is not None and y_base <= a < y_base + y_words:
                ev['wb_y'].append(ts)
    vcd = os.path.join(wd, 'vcd_f4.vcd')
    size_mb = os.path.getsize(vcd) // (1 << 20)
    collect_events(vcd, on_ts)
    t_all = time.time() - t0

    issues = ev['store_issues']
    reads = [t for t, a in ev['wr_reads']]
    wb_y = ev['wb_y']
    n = len(issues)
    last_rd, ri = [], 0
    for k in range(n):
        lim = issues[k + 1] if k + 1 < n else 10 ** 12
        last = -1
        while ri < len(reads) and reads[ri] < lim:
            last = reads[ri]
            ri += 1
        last_rd.append(last)
    fw_after, wi = [], 0
    for k in range(n):
        while wi < len(wb_y) and wb_y[wi] < issues[k]:
            wi += 1
        fw_after.append(wb_y[wi] if wi < len(wb_y) else None)
    A, B, R = [], [], []
    for k in range(n - 1):
        if last_rd[k] < 0:
            continue
        A.append(issues[k + 1] - last_rd[k])
        if fw_after[k] is not None:
            R.append(1 if fw_after[k] < last_rd[k] else 0)
    for k in range(n - 2):
        if fw_after[k + 1] is not None:
            B.append(fw_after[k + 1] - issues[k + 1])
    res = dict(seg=segname, n_iter=n, n_loads=len(ev['load_issues']),
               y_base=y_base, y_words=y_words, vcd_mb=size_mb,
               t_run_parse=round(t_all, 1),
               A_min=min(A) if A else None,
               A_neg=sum(1 for x in A if x <= 0),
               B_min=min(B) if B else None,
               B_neg=sum(1 for x in B if x <= 0),
               race_true=sum(R), race_total=len(R),
               A_sample=A[:5], B_sample=B[:5],
               stdout_tail=out.strip().splitlines()[-1] if out.strip() else '')
    if res['A_neg'] or res['B_neg']:
        res['verdict'] = 'FAIL: 存在违反（A/B 有 ≤0 项）'
    elif res['B_min'] is None or res['race_total'] == 0:
        res['verdict'] = ('VACUOUS: B/R 为空（y 区间没抓到写回事件，'
                          'y_base/y_words 可疑），不能当 PASS')
    else:
        res['verdict'] = 'PASS: 末读<下一发射<隔代首写 全部成立且非空'
    print(json.dumps(res, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
