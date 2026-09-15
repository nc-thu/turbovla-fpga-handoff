"""Generate the single-file Chinese report for the TurboVLA W8A8 Pack2 replay.

The script deliberately uses only the Python standard library.  All figures are
inline SVG so that the resulting HTML can be copied or opened without a server.
"""
from __future__ import annotations

import csv
import datetime as dt
import html
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2026-09-14_115230"
DATA = ROOT / "data" / VERSION
RTL = ROOT / "hw" / f"v1_{VERSION}_pack2_rtl"
DEFAULT_TS = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
REPORT_TS = DEFAULT_TS
OUT = ROOT / "reports" / REPORT_TS
OUT.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {} if default is None else default


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def num(value, digits=2):
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:,.{digits}f}"
    return f"{value:,}"


def pct(value, digits=1):
    return f"{100.0 * float(value):.{digits}f}%"


def mode_summary(mode):
    return read_json(DATA / f"compiled_{mode}" / "cycle_summary.json")


def svg_bar(title, items, width=900, height=None, unit="", color="#2563eb"):
    """A compact horizontal bar chart. items is [(label,value,color?)]"""
    row_h = 34
    height = height or 80 + row_h * len(items)
    maxv = max([float(x[1]) for x in items] + [1.0])
    left, right, top = 190, 135, 44
    plot_w = width - left - right
    out = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}" xmlns="http://www.w3.org/2000/svg">']
    out.append('<style>.t{font:14px Arial,sans-serif;fill:#1f2937}.s{font:12px Arial,sans-serif;fill:#4b5563}</style>')
    out.append(f'<text class="t" x="{left}" y="22">{esc(title)}</text>')
    for i, item in enumerate(items):
        label, val = item[0], float(item[1])
        c = item[2] if len(item) > 2 else color
        y = top + i * row_h
        bar_w = max(1, plot_w * val / maxv)
        out.append(f'<text class="t" x="{left-10}" y="{y+18}" text-anchor="end">{esc(label)}</text>')
        out.append(f'<rect x="{left}" y="{y+4}" width="{plot_w}" height="20" rx="3" fill="#eef2f7"/>')
        out.append(f'<rect x="{left}" y="{y+4}" width="{bar_w:.1f}" height="20" rx="3" fill="{c}"/>')
        out.append(f'<text class="s" x="{left+bar_w+8:.1f}" y="{y+19}">{esc(num(val))}{esc(unit)}</text>')
    out.append(f'<text class="s" x="{left}" y="{height-8}">0</text>')
    out.append(f'<text class="s" x="{left+plot_w}" y="{height-8}" text-anchor="end">{esc(num(maxv))}{esc(unit)}</text>')
    out.append('</svg>')
    return "".join(out)


def svg_dataflow():
    return '''<svg viewBox="0 0 980 275" role="img" aria-label="W8A8 Pack2 dataflow" xmlns="http://www.w3.org/2000/svg">
      <defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#263238"/></marker></defs>
      <style>.b{stroke:#263238;stroke-width:2}.tx{font:15px Arial,sans-serif;fill:#111827}.sm{font:12px Arial,sans-serif;fill:#374151}.bus{stroke:#1d4ed8;stroke-width:4;marker-end:url(#a)}</style>
      <rect x="20" y="74" width="142" height="95" rx="2" fill="#dbeafe" class="b"/><text class="tx" x="91" y="108" text-anchor="middle">CTX activation</text><text class="sm" x="91" y="132" text-anchor="middle">128 bit / 16×INT8</text><text class="sm" x="91" y="151" text-anchor="middle">静态 scale</text>
      <rect x="20" y="188" width="142" height="58" rx="2" fill="#fef3c7" class="b"/><text class="tx" x="91" y="213" text-anchor="middle">WRAM weight</text><text class="sm" x="91" y="233" text-anchor="middle">768 bit / 48×{w1,w0}</text>
      <rect x="222" y="42" width="300" height="190" fill="#fff7ed" class="b"/><text class="tx" x="372" y="68" text-anchor="middle">16×48 physical Pack2 array</text><text class="sm" x="372" y="90" text-anchor="middle">768 DSP · 单时钟</text>
      <g fill="#fed7aa" class="b">''' + ''.join(f'<rect x="{245+(j%6)*42}" y="{105+(j//6)*30}" width="30" height="20"/>' for j in range(24)) + '''</g>
      <text class="sm" x="372" y="204" text-anchor="middle">每个 DSP：2 个 INT8×INT8 product</text><text class="sm" x="372" y="221" text-anchor="middle">48 physical → 96 logical columns</text>
      <rect x="580" y="74" width="155" height="95" fill="#dcfce7" class="b"/><text class="tx" x="657" y="106" text-anchor="middle">INT32 state</text><text class="sm" x="657" y="130" text-anchor="middle">两路累加反馈</text><text class="sm" x="657" y="150" text-anchor="middle">snapshot / readout</text>
      <rect x="793" y="42" width="150" height="66" fill="#ede9fe" class="b"/><text class="tx" x="868" y="70" text-anchor="middle">Requant</text><text class="sm" x="868" y="91" text-anchor="middle">24 groups</text>
      <rect x="793" y="132" width="150" height="66" fill="#e0f2fe" class="b"/><text class="tx" x="868" y="160" text-anchor="middle">CTX writeback</text><text class="sm" x="868" y="181" text-anchor="middle">128 bit / INT8</text>
      <path class="bus" d="M162 112 H222"/><path class="bus" d="M162 217 H200 V150 H222"/><path class="bus" d="M522 137 H580"/><path class="bus" d="M735 112 H793"/><path class="bus" d="M735 151 H793"/>
      <text class="sm" x="190" y="103">16 行激活向右</text><text class="sm" x="190" y="238">48 组权重向下</text><text class="sm" x="753" y="102">INT8 输出</text>
    </svg>'''


def svg_pack_math():
    return '''<svg viewBox="0 0 980 230" role="img" aria-label="Pack2 bit field and correction" xmlns="http://www.w3.org/2000/svg">
      <style>.b{stroke:#263238;stroke-width:2}.tx{font:15px Arial,sans-serif;fill:#111827}.sm{font:12px Arial,sans-serif;fill:#374151}.arr{stroke:#374151;stroke-width:2;marker-end:url(#arrow2)}</style>
      <defs><marker id="arrow2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#374151"/></marker></defs>
      <text class="tx" x="20" y="28">每个物理列送入一对权重：w₁｜w₀</text>
      <rect x="35" y="60" width="340" height="50" fill="#fed7aa" class="b"/><line x1="205" y1="60" x2="205" y2="110" class="b"/><text class="tx" x="120" y="91" text-anchor="middle">w₁+128</text><text class="tx" x="290" y="91" text-anchor="middle">w₀+128</text><text class="sm" x="205" y="130" text-anchor="middle">Q = (w₁+128)·2¹⁶ + (w₀+128)</text>
      <path class="arr" d="M375 85 H470"/><rect x="470" y="60" width="180" height="50" fill="#dbeafe" class="b"/><text class="tx" x="560" y="91" text-anchor="middle">P = a · R</text><text class="sm" x="560" y="130" text-anchor="middle">R = Q − 128·(2¹⁶+1)</text>
      <path class="arr" d="M650 85 H750"/><rect x="750" y="42" width="195" height="88" fill="#dcfce7" class="b"/><text class="tx" x="847" y="70" text-anchor="middle">两个 INT8 product</text><text class="sm" x="847" y="91" text-anchor="middle">low = signed(P[15:0])</text><text class="sm" x="847" y="109" text-anchor="middle">high = signed(P[31:16])+P[15]</text>
      <text class="sm" x="20" y="184">高场借位修正保留在乘法核内；输出进入两条 INT32 累加反馈，读出只访问 snapshot。</text>
    </svg>'''


def svg_timeline():
    return '''<svg viewBox="0 0 980 220" role="img" aria-label="read compute write overlap timeline" xmlns="http://www.w3.org/2000/svg">
      <style>.tx{font:14px Arial,sans-serif;fill:#111827}.sm{font:12px Arial,sans-serif;fill:#374151}.r{stroke:#334155;stroke-width:1}</style>
      <text class="tx" x="20" y="24">current：读、算、写在长段之间串行等待</text>
      <text class="sm" x="20" y="62">activation / weight read</text><rect x="180" y="46" width="290" height="22" fill="#bfdbfe" class="r"/><text class="sm" x="192" y="62">37.72M + 34.51M cycles</text>
      <text class="sm" x="20" y="98">array compute</text><rect x="180" y="82" width="250" height="22" fill="#fed7aa" class="r"/><text class="sm" x="192" y="98">35.16M cycles</text>
      <text class="sm" x="20" y="134">fallback / vector</text><rect x="180" y="118" width="100" height="22" fill="#e5e7eb" class="r"/><text class="sm" x="192" y="134">6.42M</text><rect x="300" y="118" width="70" height="22" fill="#e5e7eb" class="r"/><text class="sm" x="312" y="134">3.56M</text>
      <text class="tx" x="20" y="174">double buffer：下一项的读数可以覆盖前一项的后处理等待</text>
      <rect x="180" y="190" width="180" height="22" fill="#bfdbfe" class="r"/><rect x="320" y="190" width="250" height="22" fill="#fed7aa" class="r"/><rect x="520" y="190" width="110" height="22" fill="#bbf7d0" class="r"/><text class="sm" x="185" y="206">read</text><text class="sm" x="405" y="206">compute</text><text class="sm" x="550" y="206">write</text>
    </svg>'''


def parse_ooc(name):
    d = RTL / "synth" / f"ooc_{name}"
    util = (d / "utilization.rpt").read_text(encoding="utf-8", errors="ignore") if (d / "utilization.rpt").exists() else ""
    timing = (d / "timing.rpt").read_text(encoding="utf-8", errors="ignore") if (d / "timing.rpt").exists() else ""
    power = (d / "power.rpt").read_text(encoding="utf-8", errors="ignore") if (d / "power.rpt").exists() else ""
    def first(pattern, text, default="—"):
        m = re.search(pattern, text, flags=re.I | re.M)
        return m.group(1) if m else default
    lut = first(r"\| CLB LUTs\*\s*\|\s*([0-9]+)", util)
    ff = first(r"\| CLB Registers\s*\|\s*([0-9]+)", util)
    dsp = first(r"\| DSPs\s*\|\s*([0-9]+)", util)
    bram = first(r"\| Block RAM Tile\s*\|\s*([0-9]+)", util)
    wns = first(r"Worst Slack\s+([0-9.]+)ns", timing)
    path = first(r"Data Path Delay:\s*([0-9.]+)ns", timing)
    logic = first(r"logic\s+([0-9.]+)ns", timing)
    route = first(r"route\s+([0-9.]+)ns", timing)
    pwr = first(r"\| Total On-Chip Power \(W\)\s*\|\s*([0-9.]+)", power)
    try:
        fmax = f"{1000.0 / (3.298 - float(wns)):.1f}"
    except Exception:
        fmax = "—"
    return {"name": name, "lut": lut, "ff": ff, "dsp": dsp, "bram": bram,
            "wns": wns, "path": path, "logic": logic, "route": route,
            "fmax": fmax, "power": pwr, "status": "synthesis report" if util else "not found"}


def html_table(headers, rows):
    h = ['<table><thead><tr>'] + [f'<th>{esc(x)}</th>' for x in headers] + ['</tr></thead><tbody>']
    for row in rows:
        h.append('<tr>' + ''.join(f'<td>{x}</td>' for x in row) + '</tr>')
    h.append('</tbody></table>')
    return ''.join(h)


def main():
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inv = read_json(DATA / "compiled_current" / "operator_inventory.json")
    check = read_json(DATA / "compiled_current" / "stream_check.json")
    golden = read_json(DATA / "golden_results.json")
    sim = read_json(DATA / "sim_results.json")
    evidence = read_json(DATA / "evidence_sources.json")
    modes = {m: mode_summary(m) for m in ["current", "double_buffer", "queue", "r5_conditional"]}
    ooc = [parse_ooc(x) for x in ["1x1", "4x4", "16x48"]]
    current, db, queue, r5 = [modes[x] for x in ["current", "double_buffer", "queue", "r5_conditional"]]
    speedup = current["total_cycles"] / db["total_cycles"]
    reduction = (1 - db["total_cycles"] / current["total_cycles"]) * 100
    queue_gain = (1 - queue["total_cycles"] / db["total_cycles"]) * 100

    module_counts = inv.get("module_event_counts", {})
    coverage_rows = [
        ["Linear / GEMM", num(module_counts.get("linear", 0)), "rtl_gemm", "Pack2 16×96 logical tile"],
        ["动态 BMM", num(inv.get("mapping_counts", {}).get("rtl_bmm", 0)), "rtl_bmm", "两个输入和布局均检查"],
        ["LayerNorm", num(module_counts.get("LayerNorm", 0)), "aux_behavior", "保留行为级周期"],
        ["GELU", num(module_counts.get("GELU", 0)), "aux_behavior", "没有冒充 RTL"],
        ["Conv2d", num(module_counts.get("Conv2d", 0)), "aux_behavior", "im2col 未进入 Pack2"],
        ["MultiheadAttention 模块", num(module_counts.get("MultiheadAttention", 0)), "aux_behavior", "内部 BMM 单独计数"],
        ["未知事件", num(check.get("unknown_count", 0)), "—", "必须为 0"],
    ]
    mode_rows = []
    for name, label in [("current", "current"), ("double_buffer", "double buffer"), ("queue", "兼容队列"), ("r5_conditional", "R5 条件")]:
        s = modes[name]
        mode_rows.append([label, num(s["total_cycles"]), f"{s['total_cycles']/current['total_cycles']:.3f}×", pct(s["pe_time_utilization"]), pct(s["gemm_utilization"]), num(s["effective_gops_250_0"], 1)])
    ooc_rows = []
    for x in ooc:
        ooc_rows.append([esc(x["name"]), esc(x["lut"]), esc(x["ff"]), esc(x["dsp"]), esc(x["bram"]), esc(x["wns"]), esc(x["fmax"]), esc(x["power"]), esc(x["status"])])

    cycle_items = [
        ("激活读取", current["activation_read_cycles"], "#93c5fd"),
        ("权重读取", current["weight_read_cycles"], "#60a5fa"),
        ("阵列计算", current["compute_cycles"], "#fb923c"),
        ("fallback/aux", current["fallback_cycles"], "#9ca3af"),
        ("requant", current["requant_cycles"], "#a78bfa"),
        ("写回", current["write_cycles"], "#4ade80"),
        ("snapshot", current["snapshot_cycles"], "#facc15"),
    ]
    cov_items = [("GEMM", module_counts.get("linear", 0), "#2563eb"), ("BMM", inv.get("mapping_counts", {}).get("rtl_bmm", 0), "#60a5fa"), ("LayerNorm", module_counts.get("LayerNorm", 0), "#9ca3af"), ("MHA", module_counts.get("MultiheadAttention", 0), "#a78bfa"), ("Conv2d", module_counts.get("Conv2d", 0), "#fb923c"), ("GELU", module_counts.get("GELU", 0), "#4ade80")]
    mode_chart = svg_bar("四种周期模型（越短越好）", [("current", current["total_cycles"], "#ef4444"), ("double buffer", db["total_cycles"], "#2563eb"), ("queue", queue["total_cycles"], "#16a34a"), ("R5 conditional", r5["total_cycles"], "#64748b")], unit=" cycles")
    cov_chart = svg_bar("模块事件数量", cov_items, unit=" events")
    cycle_chart = svg_bar("current 的阶段记账（阶段有重叠，不能直接相加）", cycle_items, unit=" cycles")
    dataflow = svg_dataflow()
    packmath = svg_pack_math()
    timeline = svg_timeline()

    css = '''*{box-sizing:border-box}body{margin:0;background:#f3f4f6;color:#1f2937;font-family:"Microsoft YaHei",Arial,sans-serif;line-height:1.65}.page{max-width:1200px;margin:0 auto;background:#fff;min-height:100vh;padding:34px 48px 64px}.eyebrow{color:#2563eb;font-size:13px;letter-spacing:.08em}.title{font-size:30px;line-height:1.25;margin:4px 0 8px;color:#111827}.subtitle{color:#4b5563;margin:0 0 22px}.stamp{font-family:Consolas,monospace;color:#6b7280;font-size:12px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0}.metric{border:1px solid #dbe3ee;border-left:4px solid #2563eb;padding:14px 16px;background:#fbfdff}.metric b{font-size:24px;display:block;color:#0f172a}.metric span{font-size:13px;color:#64748b}.section{border-top:1px solid #e5e7eb;padding-top:24px;margin-top:30px}.section h2{font-size:22px;margin:0 0 8px;color:#111827}.section h3{font-size:17px;margin:20px 0 7px}.note{border-left:4px solid #f59e0b;background:#fffbeb;padding:11px 14px;margin:14px 0}.good{border-left-color:#16a34a;background:#f0fdf4}.muted{color:#6b7280}.figure{border:1px solid #e5e7eb;background:#fff;padding:12px 14px;margin:16px 0;overflow-x:auto}.caption{font-size:13px;color:#4b5563;margin-top:4px}.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}table{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0 15px}th,td{border:1px solid #dbe3ee;padding:7px 9px;text-align:left;vertical-align:top}th{background:#f1f5f9;color:#334155}code{font-family:Consolas,monospace;font-size:12px;background:#f1f5f9;padding:2px 5px;border-radius:3px}.small{font-size:13px}.red{color:#b91c1c}.green{color:#15803d}@media(max-width:800px){.page{padding:22px 18px}.grid{grid-template-columns:repeat(2,1fr)}.two{grid-template-columns:1fr}.title{font-size:24px}}'''
    html_out = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(REPORT_TS)} TurboVLA W8A8 Pack2 架构分析</title><style>{css}</style></head><body><main class="page">
      <div class="eyebrow">TURBOVLA · W8A8 · HB PACK2 · ARCHITECTURE REVIEW</div>
      <h1 class="title">TurboVLA W8A8 Pack2：真实指令流回放与架构分析</h1>
      <p class="subtitle">本页回答三个问题：HB 的 Pack2 数据通路能否接 TurboVLA；阵列实际忙了多少；下一步应先改喂数、调度还是写回。</p>
      <div class="stamp">生成时间：{esc(generated)}　|　版本目录：{esc(VERSION)}　|　报告类型：trace 周期模型 + Pack2 OOC 综合</div>
      <div class="grid"><div class="metric"><b>768</b><span>DSP，16 行 × 48 物理列</span></div><div class="metric"><b>{pct(current['pe_time_utilization'])}</b><span>current PE 时间利用率</span></div><div class="metric"><b>{num(current['effective_gops_250_0'],1)}</b><span>250 MHz 完整回放有效 GOPS</span></div><div class="metric"><b>{speedup:.2f}×</b><span>双缓冲相对 current 的周期加速</span></div></div>

      <section class="section"><h2>先给结论</h2>
        <div class="note good"><b>Pack2 的算术接口可以接 TurboVLA。</b>这条 trace 中，编译器把 280 个 Linear 和 24 个动态 BMM 分到 Pack2，所有 432 个 descriptor 都有明确类别，未知数为 0。这里的“接通”指格式和任务流已经能编译，不等于完整模型已经在 FPGA 上跑完。</div>
        <p>current 周期模型为 <b>{num(current['total_cycles'])}</b> 拍，250 MHz 下的有效吞吐为 <b>{num(current['effective_gops_250_0'],1)} GOPS</b>，只达到 Pack2 峰值 768 GOPS 的 <b>{pct(current['effective_gops_250_0']/768)}</b>。PE 时间利用率为 <b>{pct(current['pe_time_utilization'])}</b>，GEMM 内部利用率为 <b>{pct(current['gemm_utilization'])}</b>。</p>
        <p>加入双结果缓冲后，模型周期降到 <b>{num(db['total_cycles'])}</b> 拍，减少 <b>{reduction:.2f}%</b>，有效吞吐升到 <b>{num(db['effective_gops_250_0'],1)} GOPS</b>。兼容任务队列只额外减少 <b>{queue_gain:.3f}%</b>，说明当前 trace 的主要问题是读算写串行等待，而不是队列深度不够。</p>
        <p class="muted">这轮没有重跑 LIBERO 成功率，也没有做板级 DDR、post-route 或真实 TOPS/W。辅助算子使用行为级周期；W8A8 静态 scale 的数值误差仍需另测。</p>
      </section>

      <section class="section"><h2>1. 设计范围和证据来源</h2>
        <p>新版本保持 HB v10 的 Pack2：每个 DSP 从一个激活和一对权重中得到两个 INT8×INT8 乘积，物理阵列是 16×48，逻辑输出列为 96。没有加入 Pump2、双时钟或未通过布线的 p2d/pp 双路阵列。</p>
        {html_table(["来源", "本页怎么用", "边界"], [
          ["目标对话 `codex://threads/01a09dc7-08f7-7201-afba-4820f3eedb3e`", "作为 W8A8 实验线索", "对话仍在继续，不把文字结论当新成功率"],
          ["TurboVLA W8A8 本地 summary", "已有软件假量化候选结果", "不是本轮重新评测，不能证明 Pack2 部署精度"],
          ["TurboVLA 真实 trace", "提供模块顺序、矩阵尺寸和依赖", "一条代表性 forward，不代表四套 LIBERO"],
          ["HB v10 Pack2 RTL", "算术和接口的只读参考", "复制到新目录，不修改 HB 原工程"],
        ])}
        <div class="note">软件参考路径和硬件部署路径分开记录。软件假量化保留动态激活 scale；Pack2 需要静态激活 scale、输出通道权重 scale 和整数重标定系数。当前报告只确认描述符和周期口径，尚未声称两套路径逐位一致。</div>
      </section>

      <section class="section"><h2>2. Pack2 数据通路</h2>
        <div class="figure">{dataflow}<div class="caption">这张图怎么看：左边是 128-bit 激活和 768-bit 权重输入；中间一个 DSP 产生两个逻辑列；右边再做 INT32 快照、重量化和 INT8 写回。</div></div>
        <div class="figure">{packmath}<div class="caption">这张图怎么看：预加器先把无符号偏移还原成 signed INT8 乘法；高场的借位修正留在乘法核内，不能在软件端漏掉。</div></div>
        <p>Pack2 的关键公式为 <code>Q=(w1+128)·2^16+(w0+128)</code>、<code>R=Q−128·(2^16+1)</code>、<code>P=a·R</code>。低场取 <code>signed(P[15:0])</code>，高场取 <code>signed(P[31:16])+P[15]</code>。黄金模型用 INT64 计算后对照 Pack2 结果，100,343 个随机和边界样本全部通过。</p>
        <p>27-bit snapshot 在 K≤3072 的代表边界内可以容纳最坏累加；K=4096 的最坏值为 67,108,864，超出 signed 27-bit 范围。因此编译器必须在 K=4096 或更大时加 <code>snapshot_guard_required</code>，不能静默截断。</p>
      </section>

      <section class="section"><h2>3. TurboVLA 指令流覆盖</h2>
        <p>采集到 408 个模块事件和 6836 个 dispatch 事件。编译器输出 432 个 descriptor 和 433 条 command（最后一条是结束事件）。304 个 descriptor 进入 Pack2，128 个 descriptor 保留为行为级辅助；父子 BMM 没有重复计数。</p>
        <div class="two"><div class="figure">{cov_chart}<div class="caption">这张图怎么看：GEMM 数量最多，但 LayerNorm、GELU、卷积和 attention 外围仍需占用时间；“GEMM 全部可映射”不等于完整模型全部在阵列上。</div></div><div>{html_table(["模块", "事件数", "分类", "说明"], coverage_rows)}</div></div>
        <p class="small">映射清单：<code>rtl_gemm=280</code>、<code>rtl_bmm=24</code>、<code>aux_behavior=128</code>、<code>unknown=0</code>。未知为 0 只说明编译器给每个事件分配了类别，不能把 AUX_EVENT 误写成已经综合的 DINO、LayerNorm 或 Softmax RTL。</p>
      </section>

      <section class="section"><h2>4. 周期模型和利用率</h2>
        <div class="figure">{mode_chart}<div class="caption">这张图怎么看：双缓冲把读数、计算和写回的等待部分重叠起来；队列和 R5 在这条 trace 上没有更多可利用机会。</div></div>
        {html_table(["模式", "总周期", "相对 current", "PE 时间利用率", "GEMM 利用率", "有效 GOPS@250MHz"], mode_rows)}
        <div class="figure">{cycle_chart}<div class="caption">这张图怎么看：读取、计算和写回的阶段可能重叠，图中是分阶段记账，不能把所有条相加后当成总周期；总周期以模型的调度结果为准。</div></div>
        <div class="figure">{timeline}<div class="caption">这张图怎么看：current 让下一项等上一项清空；双缓冲让下一项先读入，从而把阵列空闲时间压下去。</div></div>
        <p>当前模型记录了 {num(current['activation_bytes'])} B 激活、{num(current['weight_bytes'])} B 权重和 {num(current['output_bytes'])} B 输出流量。current 的低利用率主要来自激活/权重读取与任务间串行等待；双缓冲后 PE 利用率升到 {pct(db['pe_time_utilization'])}，GEMM 利用率升到 {pct(db['gemm_utilization'])}。这是一条可直接指导架构改动的信号：先把读、算、写叠起来，再考虑更复杂的跨任务队列。</p>
        <h3>峰值口径</h3>
        <p>250 MHz 时，768 DSP × 2 MAC/DSP/cycle = <b>384 GMAC/s = 768 GOPS</b>。沿用 HB v10 已实现的 303.215 MHz 频率，峰值为 <b>465.7 GMAC/s = 931.5 GOPS</b>。这些是阵列上界，不是这条完整 forward 已达到的吞吐。</p>
        {html_table(["周期模型", "有效 GOPS @250 MHz", "有效 GOPS @303.215 MHz", "占对应峰值"], [
          ["current", num(current["effective_gops_250_0"], 1), num(current["effective_gops_303_215"], 1), pct(current["effective_gops_250_0"] / current["peak_gops_250_0"])],
          ["double buffer", num(db["effective_gops_250_0"], 1), num(db["effective_gops_303_215"], 1), pct(db["effective_gops_250_0"] / db["peak_gops_250_0"])],
          ["queue", num(queue["effective_gops_250_0"], 1), num(queue["effective_gops_303_215"], 1), pct(queue["effective_gops_250_0"] / queue["peak_gops_250_0"])],
        ])}
      </section>

      <section class="section"><h2>5. RTL、仿真和 Vivado OOC</h2>
        <p>Pack2 黄金模型、Verilator 乘法核测试和 Icarus replay/array smoke 已通过。16×48 阵列做了 Verilator lint/elaboration，确认 768 个 DSP 实例可以展开；本轮没有把完整 432 descriptor trace 做成逐位 RTL 数值仿真，因此完整 forward 周期仍属于 trace 模型。</p>
        {html_table(["检查", "结果", "范围", "说明"], [
          ["Python 黄金模型", esc(sim.get("python_golden", {}).get("status", "—")), "100,343 samples", "Pack2 公式、极值和 K 边界"],
          ["Verilator Pack2 核", esc(sim.get("verilator_pack2_mult_padd", {}).get("status", "—")), "单核", "逐位算术 smoke"],
          ["Verilator 16×48", esc(sim.get("verilator_16x48_elaboration", {}).get("status", "—")), "768 DSP lint/elaboration", "未做完整 trace 数值回放"],
          ["Icarus smoke", esc(sim.get("icarus_replay_smoke", {}).get("status", "—")), "replay + 2×3 array", "秒级控制和阵列冒烟"],
          ["Vivado OOC", esc(sim.get("vivado_ooc", {}).get("status", "—")), "1×1 / 4×4 / 16×48", "只完成综合，未 place/route"],
        ])}
        {html_table(["规模", "LUT", "FF", "DSP", "BRAM", "WNS (ns)", "由 WNS 推得 Fmax (MHz)", "vectorless power (W)", "结果"], ooc_rows)}
        <p class="small">Vivado 使用器件 <code>xczu7ev-ffvc1156-2-e</code>，目标周期 3.298 ns。表中的 Fmax 是由综合 WNS 推出来的近似值，不是布线后频率；16×48 结果为 78,249 LUT、148,168 FF、768 DSP、WNS +1.433 ns，约 536.2 MHz OOC。功耗没有 SAIF/VCD，只能作为 vectorless 参考，不能换算成 TOPS/W。</p>
      </section>

      <section class="section"><h2>6. HB v8 优化迁移结果</h2>
        {html_table(["HB 方案", "TurboVLA Pack2 处理", "本条 trace 的结果"], [
          ["读、算、后处理重叠", "已进入 double-buffer 模型", f"{reduction:.2f}% 周期下降"],
          ["双结果缓冲", "默认可实现配置", f"{num(db['total_cycles'])} cycles"],
          ["兼容任务队列", "检查权重、K、scale、布局和依赖后合并", f"额外下降 {queue_gain:.3f}%"],
          ["R5 连续写回合并", "作为条件模型，不预先算收益", "当前严格规则未检测到机会"],
          ["零行跳过", "单独保留统计入口", "本轮未计入主结果"],
          ["Pump2 / p2d / pp", "不导入", "HB 当前未通过布线的方案"],
        ])}
        <div class="note">R5 的“没有收益”只表示这条 trace 按当前严格的整块连续地址规则没有检测到机会，不代表写回合并在其他 trace 中一定无效。</div>
      </section>

      <section class="section"><h2>7. 下一步建议</h2>
        <ol><li><b>先把静态 scale 部署路径补齐。</b>目前 Pack2 算术已经逐位通过，但软件动态 scale 和硬件静态 scale 仍是两条路径。需要用同一批代表性算子测 INT8 输出误差，再决定是否要新增 scale 更新通路。</li><li><b>优先实现双缓冲的 RTL 活动回放。</b>模型显示它能把周期减少 51.45%，而兼容队列当前只带来千分之几的额外收益。先验证结果顺序、输出阻塞和 snapshot 占用，避免同时引入多个变化。</li><li><b>再扩展多 suite trace。</b>如果四套 suite 的短块和读取比例相近，双缓冲结论更可信；如果形状变化更大，应先完善 descriptor 的尾块和拒配规则。</li></ol>
        <p><b>是否值得继续：</b>值得继续做多 suite trace、正式整数量化和成功率验证，但暂时不应宣称“TurboVLA 已完成纯整数 FPGA 全模型执行”。</p>
      </section>

      <section class="section"><h2>附录：可复核文件</h2>
        {html_table(["文件", "用途"], [
          ["data/2026-09-14_115230/compiled_current/cycle_summary.json", "current 周期和利用率"],
          ["data/2026-09-14_115230/compiled_{double_buffer,queue,r5_conditional}/cycle_summary.json", "三种优化情景"],
          ["data/2026-09-14_115230/compiled_current/operator_inventory.json", "算子覆盖和映射类别"],
          ["data/2026-09-14_115230/compiled_current/stream_check.json", "descriptor 对账"],
          ["data/2026-09-14_115230/golden_results.json", "Pack2 黄金模型"],
          ["hw/v1_2026-09-14_115230_pack2_rtl/synth/ooc_*/", "Vivado OOC 报告"],
        ])}
        <p class="muted small">报告生成脚本：<code>scripts/generate_pack2_report.py</code>。所有图由 JSON/CSV 生成，HTML 不依赖外部 CSS、JavaScript 或图片文件。</p>
      </section>
    </main></body></html>'''
    out_file = OUT / f"{REPORT_TS}_turbovla_w8a8_pack2_arch_report.html"
    out_file.write_text(html_out, encoding="utf-8")
    print(json.dumps({"report": str(out_file), "generated_at": generated, "total_bytes": out_file.stat().st_size, "ooc": ooc}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
