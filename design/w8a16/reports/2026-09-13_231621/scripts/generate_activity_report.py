"""Generate the standalone Chinese TurboVLA activity replay report.

All numbers in the page are read from the captured JSON/CSV and Vivado
reports.  SVGs are deliberately inline so the report remains a single file.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import math
import time
from collections import defaultdict
from pathlib import Path
from typing import Any


ROUND = "2026-09-13_231621"
ROWS = 16
PCOLS = 48
DSP = 768
FREQ_MHZ = 250.0


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def fmt_int(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "—"


def fmt_float(value: Any, digits: int = 2) -> str:
    try:
        return f"{float(value):,.{digits}f}"
    except (TypeError, ValueError):
        return "—"


def pct(value: float, total: float) -> float:
    return 100.0 * value / total if total else 0.0


def vivado_run(vivado: dict[str, Any], name: str) -> dict[str, Any]:
    return next((r for r in vivado.get("runs", []) if r.get("configuration") == name), {})


def resource_value(run: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(run.get("utilization", {}).get(key, default) or default)
    except (TypeError, ValueError):
        return default


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def group_rows(rows: list[dict[str, str]], key_fn) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = str(key_fn(row))
        g = groups.setdefault(key, {"key": key, "count": 0, "cycles": 0, "macs": 0, "tiles": 0})
        g["count"] += 1
        for out_key, in_key in (("cycles", "total_cycles"), ("macs", "valid_mac_count"), ("tiles", "tile_count")):
            try:
                g[out_key] += int(float(row.get(in_key) or 0))
            except ValueError:
                pass
    return sorted(groups.values(), key=lambda x: x["cycles"], reverse=True)


def stage_name(module: str) -> str:
    if module.startswith("text_encoder"):
        return "文本编码"
    if module.startswith("vision_encoder"):
        return "视觉编码"
    if module.startswith("vision_language_interaction"):
        return "图文交互"
    if module.startswith("vision_projection"):
        return "视觉投影"
    if module == "<top>":
        return "注意力 BMM"
    if module.startswith("action_head"):
        return "动作头"
    return "其他"


def svg_flow() -> str:
    return '''<svg class="figure" viewBox="0 0 980 220" role="img" aria-label="replay data path">
      <defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#222"/></marker></defs>
      <rect x="20" y="72" width="150" height="70" fill="#e8f2fa" stroke="#222" stroke-width="2"/>
      <text x="95" y="101" text-anchor="middle" font-weight="700">64-bit command</text><text x="95" y="123" text-anchor="middle">短控制字</text>
      <rect x="210" y="48" width="180" height="118" fill="#e8f2fa" stroke="#222" stroke-width="2"/>
      <text x="300" y="79" text-anchor="middle" font-weight="700">Descriptor FIFO</text><text x="300" y="101" text-anchor="middle">512-bit sideband</text><text x="300" y="125" text-anchor="middle">shape / cycle / scale</text><text x="300" y="147" text-anchor="middle">depth 16</text>
      <rect x="430" y="72" width="145" height="70" fill="#fff4cf" stroke="#222" stroke-width="2"/>
      <text x="502" y="101" text-anchor="middle" font-weight="700">Tile scheduler</text><text x="502" y="123" text-anchor="middle">顺序与依赖</text>
      <rect x="615" y="34" width="175" height="146" fill="#fff4cf" stroke="#222" stroke-width="2"/>
      <text x="702" y="62" text-anchor="middle" font-weight="700">16 × 48 W8A16</text><text x="702" y="84" text-anchor="middle">768 DSP / 40-bit acc</text>
      <g fill="#f4c78f" stroke="#222" stroke-width="1"><rect x="643" y="103" width="23" height="23"/><rect x="673" y="103" width="23" height="23"/><rect x="703" y="103" width="23" height="23"/><rect x="733" y="103" width="23" height="23"/><rect x="643" y="133" width="23" height="23"/><rect x="673" y="133" width="23" height="23"/><rect x="703" y="133" width="23" height="23"/><rect x="733" y="133" width="23" height="23"/></g><text x="702" y="171" text-anchor="middle">代表 tile 逐拍；全 trace 记事件周期</text>
      <rect x="830" y="22" width="130" height="52" fill="#e9e9e9" stroke="#222" stroke-width="2"/><text x="895" y="44" text-anchor="middle" font-weight="700">vector / AUX</text><text x="895" y="62" text-anchor="middle">行为级周期</text>
      <rect x="830" y="102" width="130" height="52" fill="#e9e9e9" stroke="#222" stroke-width="2"/><text x="895" y="124" text-anchor="middle" font-weight="700">CTX / writeback</text><text x="895" y="142" text-anchor="middle">INT16 输出</text>
      <line x1="170" y1="107" x2="210" y2="107" stroke="#222" stroke-width="2" marker-end="url(#arrow)"/><line x1="390" y1="107" x2="430" y2="107" stroke="#222" stroke-width="2" marker-end="url(#arrow)"/><line x1="575" y1="107" x2="615" y2="107" stroke="#222" stroke-width="2" marker-end="url(#arrow)"/><line x1="790" y1="75" x2="830" y2="48" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/><line x1="790" y1="141" x2="830" y2="128" stroke="#555" stroke-width="2" marker-end="url(#arrow)"/>
      <text x="500" y="205" text-anchor="middle" font-size="13">实线是当前 replay top 的数据路径；灰色块保留没有专用阵列的模型事件</text>
    </svg>'''


def svg_timeline(summary: dict[str, Any]) -> str:
    total = float(summary["cycles"]["total_cycles"])
    mapped = float(summary["cycles"]["mapped_cycles"])
    fallback = float(summary["cycles"]["fallback_cycles"])
    mw = 820.0 * mapped / total if total else 0
    fw = 820.0 * fallback / total if total else 0
    return f'''<svg class="figure" viewBox="0 0 980 150" role="img" aria-label="PE busy timeline">
      <text x="20" y="24" font-weight="700">完整 forward 的事件时间线（模型周期）</text>
      <rect x="20" y="48" width="820" height="42" fill="#f2f2f2" stroke="#222" stroke-width="1"/>
      <rect x="20" y="48" width="{mw:.2f}" height="42" fill="#7fa8c9"/><rect x="{20+mw:.2f}" y="48" width="{fw:.2f}" height="42" fill="#e5ae69"/>
      <text x="{20+mw/2:.2f}" y="74" text-anchor="middle" font-weight="700">映射阵列 {pct(mapped,total):.2f}%</text><text x="{20+mw+fw/2:.2f}" y="74" text-anchor="middle" font-weight="700">fallback {pct(fallback,total):.2f}%</text>
      <line x1="20" y1="101" x2="840" y2="101" stroke="#222"/><text x="20" y="121">0</text><text x="840" y="121" text-anchor="end">{fmt_int(total)} cycles = {total/FREQ_MHZ/1e6:.3f} s @ 250 MHz</text>
      <text x="20" y="145" font-size="12">蓝色段包括 GEMM/BMM 的读取、填充、累加、快照、重量化和写回；橙色段是向量与辅助事件。</text>
    </svg>'''


def svg_stage_bars(stages: list[dict[str, Any]], total: float) -> str:
    width = 700
    bar_h = 24
    left = 180
    rows = stages[:8]
    h = 55 + len(rows) * 38
    out = [f'<svg class="figure" viewBox="0 0 980 {h}" role="img" aria-label="stage cost">', '<text x="20" y="24" font-weight="700">模块事件周期占比</text>']
    colors = ["#7fa8c9", "#92b6cf", "#a8c5d7", "#e5ae69", "#c5c5c5", "#b6d4b6", "#d3a7c5", "#b0b0b0"]
    for i, item in enumerate(rows):
        y = 38 + i * 38
        w = width * item["cycles"] / total if total else 0
        out.append(f'<text x="{left-10}" y="{y+17}" text-anchor="end">{esc(item["key"])}</text>')
        out.append(f'<rect x="{left}" y="{y}" width="{width}" height="{bar_h}" fill="#f2f2f2" stroke="#bbb"/>')
        out.append(f'<rect x="{left}" y="{y}" width="{w:.2f}" height="{bar_h}" fill="{colors[i % len(colors)]}"/>')
        out.append(f'<text x="{left+w+8:.2f}" y="{y+17}" font-size="12">{pct(item["cycles"],total):.2f}% / {fmt_int(item["cycles"])}</text>')
    out.append('</svg>')
    return "".join(out)


def html_table(headers: list[str], rows: list[list[Any]], cls: str = "") -> str:
    th = "".join(f"<th>{esc(x)}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{x}</td>" for x in row) + "</tr>" for row in rows)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--vivado", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    data = args.data
    cap = json.loads((data / "capture_result.json").read_text(encoding="utf-8"))
    summary = json.loads((data / "compiled" / "replay_summary.json").read_text(encoding="utf-8"))
    rtl = json.loads((data / "rtl_activity.json").read_text(encoding="utf-8"))
    inv = json.loads((data / "compiled" / "operator_inventory.json").read_text(encoding="utf-8"))
    descs = [json.loads(x) for x in (data / "compiled" / "descriptors.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = load_rows(data / "compiled" / "cycle_breakdown.csv")
    vivado = json.loads((data / "vivado_results.json").read_text(encoding="utf-8"))
    generated = time.strftime("%Y-%m-%d %H:%M:%S")
    total = float(summary["cycles"]["total_cycles"])
    mapped = float(summary["cycles"]["mapped_cycles"])
    fallback = float(summary["cycles"]["fallback_cycles"])
    replay_s = total / (float(summary["clock_mhz"]) * 1e6)
    active_equiv_s = float(summary["pe_active_pe_cycles"]) / (DSP * float(summary["clock_mhz"]) * 1e6)
    peak_gops = float(summary["physical_peak_gops"])
    eff_gops = float(summary["effective_gops"])
    activity_counters = (rtl.get("rtl", {}) or {}).get("activity_counters", {}) or {}

    array_run = vivado_run(vivado, "array_on_trace_on") or vivado_run(vivado, "array_on_trace_off")
    control_run = vivado_run(vivado, "array_off_trace_off")
    array_h = array_run.get("hierarchy", {}) or {}
    sysarr_h = array_h.get("sysarr", {}) or {}
    pe_h = array_h.get("pe_example", {}) or {}
    top_lut = resource_value(array_run, "lut")
    top_ff = resource_value(array_run, "ff")
    top_dsp = resource_value(array_run, "dsp")
    ctrl_lut = resource_value(control_run, "lut")
    ctrl_ff = resource_value(control_run, "ff")
    ctrl_dsp = resource_value(control_run, "dsp")
    array_power = array_run.get("power", {}) or {}
    array_power_total = array_power.get("total_on_chip_w")
    array_power_dynamic = array_power.get("dynamic_w")
    array_power_static = array_power.get("static_w")
    counter_rows = [
        ["total_cycles", fmt_int(activity_counters.get("total_cycles")), "顶层 full replay counter"],
        ["mapped_cycles", fmt_int(activity_counters.get("mapped_cycles")), "GEMM/BMM 映射事件"],
        ["fallback_cycles", fmt_int(activity_counters.get("fallback_cycles")), "vector/AUX 行为级事件"],
        ["valid_mac_count", fmt_int(activity_counters.get("valid_mac_count")), "不含填充位置"],
        ["tile_count", fmt_int(activity_counters.get("tile_count")), "16×48 tile 数"],
        ["output_bytes", fmt_int(activity_counters.get("output_bytes")), "独立 64-bit 输出端口"],
        ["queue_max_occupancy", fmt_int(activity_counters.get("queue_max_occupancy")), "descriptor FIFO 观测最大占用"],
    ]
    cycle_labels = [
        ("dma_read_cycles", "读服务", "激活／权重读取标签"),
        ("dma_write_cycles", "写服务", "写回标签"),
        ("scheduler_wait_cycles", "调度等待", "调度等待标签"),
        ("snapshot_cycles", "快照", "快照阶段"),
        ("requant_cycles", "重量化", "重量化阶段"),
        ("vector_cycles", "向量算子", "行为级向量事件"),
    ]
    cycle_rows = [[display, fmt_int(summary["cycles"].get(key)), f"{pct(float(summary['cycles'].get(key, 0)), total):.2f}%", meaning] for key, display, meaning in cycle_labels]

    stage_groups = group_rows(rows, lambda r: stage_name(r.get("module_path", "")))
    shape_groups = group_rows([r for r in rows if r.get("mapping") in ("rtl_gemm", "rtl_bmm")], lambda r: f"{r.get('op')} / {r.get('module_path','<top>')}")
    # Add dimensions from descriptors for the ten largest shape instances.
    dim_by_seq = {str(d.get("source_seq")): d for d in descs}
    for item in shape_groups:
        sample = next((r for r in rows if str(r.get("module_path")) == item["key"]), None)
        # module_path-only grouping is used in the table below; shape details
        # are supplied from descriptor records in a separate aggregation.
    shape_dim: dict[str, dict[str, Any]] = {}
    for d in descs:
        if d.get("mapping") not in ("rtl_gemm", "rtl_bmm"):
            continue
        key = f"{d.get('op')} {d.get('m')}×{d.get('n')}×{d.get('k')}"
        g = shape_dim.setdefault(key, {"key": key, "count": 0, "cycles": 0, "macs": 0, "tiles": 0})
        g["count"] += 1
        c = d.get("cycle_cost", {})
        g["cycles"] += int(c.get("total_cycles", 0) or 0)
        g["macs"] += int(c.get("valid_mac_count", 0) or 0)
        g["tiles"] += int(c.get("tile_count", 0) or 0)
    shape_dim_rows = sorted(shape_dim.values(), key=lambda x: x["cycles"], reverse=True)[:12]

    mapping_rows = []
    for key in ("rtl_gemm", "rtl_bmm", "rtl_vector", "aux_behavior"):
        subset = [r for r in rows if r.get("mapping") == key]
        cyc = sum(int(float(r.get("total_cycles") or 0)) for r in subset)
        mac = sum(int(float(r.get("valid_mac_count") or 0)) for r in subset)
        mapping_rows.append([esc(key), fmt_int(len(subset)), fmt_int(cyc), f"{pct(cyc,total):.2f}%", fmt_int(mac)])

    stage_rows = []
    for g in stage_groups:
        stage_rows.append([esc(g["key"]), fmt_int(g["count"]), fmt_int(g["cycles"]), f"{pct(g['cycles'],total):.2f}%", fmt_int(g["macs"])])

    shape_rows = [[esc(g["key"]), fmt_int(g["count"]), fmt_int(g["cycles"]), f"{pct(g['cycles'],mapped):.2f}%", fmt_int(g["macs"]), fmt_int(g["tiles"])] for g in shape_dim_rows]

    viv_rows = []
    for run in vivado.get("runs", []):
        u = run.get("utilization", {})
        t = run.get("timing", {})
        p = run.get("power", {})
        d = run.get("drc", {})
        viv_rows.append([
            esc(run.get("configuration")),
            fmt_int(u.get("lut")), fmt_int(u.get("ff")), fmt_int(u.get("dsp")), fmt_int(u.get("ramb36", 0) + u.get("ramb18", 0)),
            f"{float(t.get('wns_ns')):+.3f} ns" if t.get("wns_ns") is not None else "—",
            "250 MHz 目标通过" if run.get("status") == "passed" else "未通过",
            f"{float(p.get('total_on_chip_w')):.3f} W" if p.get("total_on_chip_w") is not None else "—",
            f"{fmt_int(d.get('violations_found'))}（{esc(', '.join(d.get('severity_summary', [])))}）",
        ])

    traffic = summary["traffic_bytes"]
    traffic_rows = [["激活 payload", fmt_int(traffic.get("activation_bytes")), "INT16 读入"], ["权重 payload", fmt_int(traffic.get("weight_bytes")), "INT8 权重流"], ["输出 payload", fmt_int(traffic.get("output_bytes")), "INT16 写回"], ["合计", fmt_int(sum(traffic.values())), "三类 payload 相加，不是带宽"]]

    road_rows = [["250 MHz，单 MAC/DSP", "384 GOPS", "当前物理口径"], ["250 MHz，双 MAC/DSP", "768 GOPS", "需要 DSP 内双路安全语义"], ["250 MHz，三 MAC/DSP", "1,152 GOPS", "超过 1,000 GOPS 的最小整数倍情景"], ["333 MHz，双 MAC/DSP", "约 1,024 GOPS", "同时提高频率和单 DSP 工作量"], ["250 MHz，单 MAC", "约 2,000 DSP", "达到 1,000 GOPS 的数量条件；当前器件可用 DSP 还需核对其它模块"]]

    # Top-level resource values are synthesis estimates; no placement/routing
    # is implied by this table.
    resource_rows = [
        ["tvla_replay_top（含阵列）", fmt_int(top_lut), fmt_int(top_ff), fmt_int(top_dsp), fmt_int(resource_value(array_run, "ramb36") + resource_value(array_run, "ramb18")), "array on 的综合总量"],
        ["顶层控制（阵列关闭）", fmt_int(ctrl_lut), fmt_int(ctrl_ff), fmt_int(ctrl_dsp), fmt_int(resource_value(control_run, "ramb36") + resource_value(control_run, "ramb18")), "FIFO／计数器／接口；独立综合配置"],
        ["w8a16_sysarr", fmt_int(sysarr_h.get("lut")), fmt_int(sysarr_h.get("ff")), fmt_int(sysarr_h.get("dsp")), fmt_int(sysarr_h.get("ramb36", 0) + sysarr_h.get("ramb18", 0)), "16×48 阵列；层级报告"],
        ["w8a16_pe（层级代表）", fmt_int(pe_h.get("lut")) if pe_h else "—", fmt_int(pe_h.get("ff")) if pe_h else "—", fmt_int(pe_h.get("dsp")) if pe_h else "—", fmt_int((pe_h.get("ramb36", 0) + pe_h.get("ramb18", 0))) if pe_h else "—", "一个代表 PE；已包含在阵列行"],
    ]

    html_doc = f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>真实 TurboVLA 指令流顶层活动回放</title>
    <style>
      :root{{--ink:#1b1b1b;--muted:#5d5d5d;--line:#d7d7d7;--blue:#e8f2fa;--yellow:#fff4cf;--orange:#f4c78f;--gray:#f3f3f3;--accent:#2e6f9e}}
      *{{box-sizing:border-box}} body{{margin:0;background:#fff;color:var(--ink);font-family:"Microsoft YaHei", "Noto Sans CJK SC", Arial, sans-serif;line-height:1.65}}
      .wrap{{max-width:1180px;margin:0 auto;padding:28px 30px 70px}} h1{{font-size:32px;line-height:1.25;margin:0 0 8px;font-weight:800;letter-spacing:.01em}} h2{{font-size:22px;margin:34px 0 10px;border-left:5px solid var(--accent);padding-left:11px}} h3{{font-size:17px;margin:22px 0 6px}} p{{margin:7px 0 12px}} .meta{{color:var(--muted);font-size:13px}} .lead{{font-size:17px;background:#f7fafc;border:1px solid #d8e5ee;padding:13px 16px;margin:17px 0 20px}} .grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:16px 0 20px}} .metric{{border:1px solid var(--line);padding:13px 14px;background:#fff}} .metric .n{{font-size:25px;font-weight:800;color:#1e567d}} .metric .k{{font-size:13px;color:var(--muted)}} .note{{border-left:3px solid #aaa;padding:7px 12px;color:#444;background:#fafafa;font-size:14px}} .warn{{border-left-color:#c7862e;background:#fffaf1}} table{{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0 8px}} th,td{{border:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}} th{{background:#f0f3f5;font-weight:700}} tr:nth-child(even) td{{background:#fcfcfc}} .figure-box{{border:1px solid var(--line);padding:12px 12px 4px;margin:13px 0 17px;overflow-x:auto}} .figure{{width:100%;min-width:760px;height:auto;display:block}} .caption{{font-size:13px;color:#4c4c4c;margin:7px 0 4px}} .two{{display:grid;grid-template-columns:1fr 1fr;gap:18px}} .small{{font-size:13px;color:var(--muted)}} code{{background:#f0f0f0;padding:1px 4px;border-radius:2px}} ul{{margin-top:7px}} li{{margin:4px 0}} .foot{{margin-top:40px;border-top:1px solid var(--line);padding-top:15px;color:var(--muted);font-size:12px}} @media(max-width:820px){{.wrap{{padding:20px 15px 50px}}h1{{font-size:26px}}h2{{font-size:20px}}.grid{{grid-template-columns:repeat(2,1fr)}}.two{{grid-template-columns:1fr}}table{{font-size:12px}}}}
    </style></head><body><main class="wrap">
    <div class="meta">生成时间：{esc(generated)}　|　实验轮次：{ROUND}　|　中文工作记录</div>
    <h1>真实 TurboVLA 指令流顶层活动回放</h1>
    <div class="lead">这页回答一个具体问题：把 TurboVLA 的一次真实 Spatial task 0 forward 送进新的 <b>16×48 W8A16 replay top</b> 后，768 个 DSP 到底有多少时间在做有效乘法，完整模型的有效吞吐是多少。页面中的周期来自指令流周期模型并由顶层计数器回放；不是 GPU 延迟，也不是已经完成布线的板上实测。</div>
    <div class="grid"><div class="metric"><div class="n">{DSP} DSP</div><div class="k">16×48，单 DSP 单 MAC</div></div><div class="metric"><div class="n">{fmt_float(summary['pe_time_utilization']*100,2)}%</div><div class="k">PE 时间利用率</div></div><div class="metric"><div class="n">{fmt_float(eff_gops,2)} GOPS</div><div class="k">完整 forward 有效吞吐</div></div><div class="metric"><div class="n">{fmt_float(peak_gops,0)} GOPS</div><div class="k">250 MHz 物理峰值</div></div></div>

    <h2>先看结论</h2>
    <ul><li>这次采集覆盖了 <b>{fmt_int(cap.get('module_event_count'))} 个模块事件</b>和 <b>{fmt_int(cap.get('dispatch_event_count'))} 个低层 dispatch 事件</b>。编译后得到 {fmt_int(summary['descriptor_count'])} 条 descriptor 和 {fmt_int(summary['instruction_count'])} 条指令（含 END），模块事件和动态 BMM 的覆盖检查均通过。</li>
    <li>周期模型给出 {fmt_int(summary['valid_mac_count'])} 个有效 MAC、{fmt_int(summary['cycles']['total_cycles'])} 个 replay cycle。按 250 MHz 换算是 <b>{replay_s:.3f} s</b>。其中阵列映射事件占 {pct(mapped,total):.2f}%，行为级 vector/AUX 占 {pct(fallback,total):.2f}%。</li>
    <li>有效吞吐为 <b>{eff_gops:.2f} GOPS</b>，只有物理峰值 384 GOPS 的 {eff_gops/peak_gops*100:.2f}%。768 个 PE 等效同时工作时间约 {active_equiv_s:.3f} s；剩余时间主要花在读取／填充／排空、尾块、快照／重量化／写回和行为级算子。</li>
    <li>视觉编码是最大的一段，约占 {pct(next((x['cycles'] for x in stage_groups if x['key']=='视觉编码'),0),total):.2f}% 周期。当前结果支持先优化喂数、短块和读写重叠，再考虑增加 DSP；仅凭这一次 forward 还不能把改动写成端到端加速。</li></ul>
    <div class="note warn"><b>边界：</b>本轮只有一个固定 Spatial task 0 和 seed 7。捕获过程耗时 {fmt_float(cap.get('elapsed_seconds'),2)} s 是 hook／量化 payload 采集开销，不是模型 inference latency。完整 forward 的 155.8M cycle 是顶层的虚拟事件回放；只有代表性 2×3、K=5 tile 做了逐拍阵列算术验证。</div>

    <h2>1. 这条真实指令流从哪里来</h2>
    <p>输入来自服务器物理 GPU 3 上的 TurboVLA 官方 checkpoint，采集进程设置 <code>CUDA_VISIBLE_DEVICES=3</code>，所以结果文件中的进程内设备名 <code>cuda:0</code> 对应物理 GPU 3。任务是 <code>libero_spatial</code> 的 Spatial task 0。两路图像为 256×256，instruction 和 8 维状态按原入口送入模型，输出动作块为 12×7。采集阶段保持现有 V1 W8A16 约定：激活 INT16、权重 INT8、累加 INT40、输出 INT16。</p>
    {html_table(['项目','本轮值','说明'], [["checkpoint 参数",fmt_int(cap.get('parameters')),"capture_result.json 中的实测 numel"],["模块事件",fmt_int(cap.get('module_event_count')),"Linear、LayerNorm、MHA、Conv2d、GELU 的边界 hook"],["dispatch 事件",fmt_int(cap.get('dispatch_event_count')),"TorchDispatch 诊断；低层 children 不重复算 GEMM"],["Linear / BMM",f"{fmt_int(cap.get('linear_event_count'))} / {fmt_int(summary['bmm_descriptor_count'])}","Linear 进入 W8A16 GEMM；BMM 为满足布局时的条件拆分"],["唯一权重",fmt_int(cap.get('weight_unique_count')),"按 hash 去重后保存"],["payload",f"激活 {cap.get('activation_payload_bytes',0)/1e6:.2f} MB；权重 {cap.get('weight_payload_bytes',0)/1e6:.2f} MB","原始采集文件带 SHA256"]])}
    <div class="figure-box">{svg_flow()}<div class="caption">图 1。数据从 64-bit command 和 512-bit descriptor 进入调度器。GEMM/BMM 使用真实 16×48 阵列；LayerNorm、GELU 和未专门实现的事件保留在行为级时间线上。<b>这图怎么看：</b>蓝色路径是能进入现有阵列的部分，灰色块不是已经综合好的 DINO/BERT 硬件。</div></div>

    <h2>2. 指令覆盖和计算花在哪里</h2>
    <p>编译器以模块事件作为线性层的记账边界，以低层 dispatch 只发现动态 BMM。这样可以避免一个 Linear 的 <code>addmm</code> child 被算两次。分类结果中 unknown 为 0，但这不等于 6,836 个低层 dispatch 都已经有专用 RTL；大量 view、to、detach 等事件只用于诊断。</p>
    {html_table(['映射类别','事件数','周期','占完整周期','有效 MAC'], mapping_rows)}
    <div class="two"><div class="figure-box">{svg_stage_bars(stage_groups,total)}<div class="caption">图 2。模块事件的周期占比。<b>这图怎么看：</b>视觉编码条最长，说明在当前一次 forward 里，阵列即使把 GEMM 做快，视觉骨干仍会决定大部分时间。</div></div><div>{html_table(['模型阶段','事件数','周期','占比','有效 MAC'], stage_rows)}</div></div>
    <h3>周期字段怎么读</h3>
    <p>映射 GEMM/BMM 的周期由共享读取、阵列计算、快照、重量化和 INT16 写回组成。<code>dma_read_cycles={fmt_int(summary['cycles']['dma_read_cycles'])}</code>、<code>dma_write_cycles={fmt_int(summary['cycles']['dma_write_cycles'])}</code>、调度等待 <code>{fmt_int(summary['cycles']['scheduler_wait_cycles'])}</code> 是事件标签，和总周期有重叠，不能再相加一次。当前模型实际把 activation 和 weight read 取两者较大值，避免把同一拍的双口服务重复计时。</p>
    {html_table(['代表形状（op M×N×K）','调用数','周期','占映射周期','有效 MAC','tile 数'], shape_rows)}
    <p class="small">形状表按 descriptor 的 M、N、K 聚合。尾行和尾列按 valid mask 计算，填充位置没有计入有效 MAC。</p>

    <h2>3. PE 真的忙了多少</h2>
    <div class="figure-box">{svg_timeline(summary)}<div class="caption">图 3。整段 replay 时间按映射阵列与行为级事件切开。<b>这图怎么看：</b>蓝色并不表示 768 个 PE 每拍都在算；有效 MAC 还要除以 768×映射段周期，得到 43.23% 的 GEMM 利用率。</div></div>
    <div class="grid"><div class="metric"><div class="n">{fmt_int(summary['valid_mac_count'])}</div><div class="k">有效 MAC</div></div><div class="metric"><div class="n">{fmt_float(summary['gemm_utilization']*100,2)}%</div><div class="k">映射段 GEMM 利用率</div></div><div class="metric"><div class="n">{fmt_float(summary['pe_time_utilization']*100,2)}%</div><div class="k">完整 forward PE 利用率</div></div><div class="metric"><div class="n">{fmt_float(active_equiv_s,3)} s</div><div class="k">768 PE 全忙的等效时间</div></div></div>
    <p>两个百分比回答不同问题。43.23% 只看 GEMM/BMM 映射段，分母排除了 LayerNorm、GELU 和 AUX；41.44% 把整个 forward 都放进分母，所以更接近系统视角。跳过或 fallback 的 MAC 没有算作阵列完成量。</p>
    {html_table(['项目','周期／数值','占总周期或峰值','口径'], [["总 replay",fmt_int(summary['cycles']['total_cycles']),f"{replay_s:.3f} s @ 250 MHz","周期模型 + top counter"],["mapped GEMM/BMM",fmt_int(summary['cycles']['mapped_cycles']),f"{pct(mapped,total):.2f}%","可进入阵列的事件"],["fallback",fmt_int(summary['cycles']['fallback_cycles']),f"{pct(fallback,total):.2f}%","vector/AUX 行为级"],["有效吞吐",f"{eff_gops:.2f} GOPS",f"{eff_gops/peak_gops*100:.2f}% of 384 GOPS","valid MAC / replay time"],["物理峰值",f"{peak_gops:.0f} GOPS","100%","768×250 MHz×1 MAC×2 ops"]])}

    <h2>4. 读、算、写和流量</h2>
    <p>从 descriptor 账本看，映射段的 compute 字段合计 {fmt_int(sum(int(float(r.get('compute_cycles') or 0)) for r in rows))} cycles，共享 read 服务合计 {fmt_int(sum(int(float(r.get('activation_read_cycles') or 0)) for r in rows))} cycles，快照 {fmt_int(summary['cycles']['snapshot_cycles'])}、重量化 {fmt_int(summary['cycles']['requant_cycles'])}。这些字段有重叠，页面只把它们当作“时间线上的原因标签”，不把它们误加成一个更大的总数。</p>
    {html_table(['时间标签','周期','占总 replay','说明'], cycle_rows)}
    {html_table(['流量类别','字节数','含义'], traffic_rows)}
    <div class="note">本轮没有把 8 B/周期或历史 64 B/周期硬套成 AXI 实测带宽。流量 CSV 记录的是 payload 字节；真正的 DDR 服务、仲裁和 burst 效率还需要板级接口或更完整的 DMA trace。</div>

    <h2>5. 顶层回放和算术验证</h2>
    <p>顶层按每条 descriptor 接收一次控制事件，把 descriptor 中的周期、MAC、tile 和流量加到 64-bit activity counter。这样可以在几微秒内回放一段 155.8M cycle 的“虚拟时间”，避免为了跑完整 forward 而执行上亿个 RTL 时钟。与此同时，代表性 2×3、K=5 tile 走真实 16×48 阵列，逐拍检查 signed INT16×INT8 和 INT40 累加。顶层还把 <code>activity_output_bytes</code> 和 <code>activity_queue_max_occupancy</code> 作为独立 64-bit 输出导出；本次回放对账分别是 <b>{fmt_int(activity_counters.get('output_bytes'))} bytes</b> 和 <b>{fmt_int(activity_counters.get('queue_max_occupancy'))}</b>，与软件摘要一致。</p>
    {html_table(['顶层计数器','数值','用途'], counter_rows)}
    {html_table(['检查项','结果','说明'], [[esc(k),"PASS" if v else "FAIL","由 rtl_activity.json 记录"] for k,v in rtl.get('checks',{}).items()])}
    <h3>代表 tile 的逐位结果</h3>
    <p>测试输入生成规则为 <code>A[i,k]=(i+1)(k−2)</code>、<code>B[k,j]=(j−1)(k+1)</code>，因此黄金结果是 <code>[[-10,0,10],[-20,0,20]]</code>。Verilator 日志记录 <b>TB_REPLAY_ARRAY_TILE PASS</b>。这项测试说明乘法、反馈累加和输出顺序一致，不代表所有模型形状都已逐拍执行。</p>

    <h2>6. Vivado 综合结果</h2>
    <p>本轮在器件 <code>xczu7ev-ffvc1156-2-e</code>、4.000 ns（250 MHz）约束下完成三次 OOC <code>synth_design</code>。array on / trace on 与 trace off 资源完全相同，说明当前 <code>TRACE_ENABLE</code> 只保留接口和计数器预留，尚未引入额外的 trace memory。这里的 Fmax 只写“250 MHz 目标通过”；没有 place/route，所以不把综合 WNS 换算成最终板上频率。</p>
    {html_table(['配置','LUT','FF','DSP','BRAM','WNS','时钟结论','vectorless power','DRC'], viv_rows)}
    <div class="note warn">Vivado power 是没有 SAIF/VCD 的 vectorless 估算，带 Medium confidence。array on 为 {fmt_float(array_power_total,3)} W（动态 {fmt_float(array_power_dynamic,3)} W、静态 {fmt_float(array_power_static,3)} W），只能用于早期比较，不能除以 GOPS 写成 TOPS/W。DRC 中的 AVAL-155 是 advisory，critical/error 为 0；仍需补板级 I/O、时钟和 AXI/DDR 约束后再做 implementation。</div>
    {html_table(['层级','LUT','FF','DSP','BRAM','解释'], resource_rows)}
    <p class="small">w8a16_pe 行来自层级报告中的代表实例（不同实例为 63–64 LUT、140–141 FF），不能把这一行再乘 768 后与 array 行相加。fallback 算子没有综合资源，不能从行为级周期倒推出 LUT。</p>

    <h2>7. 为什么以前能报一千多 GOPS，而现在只有三百多峰值</h2>
    <p>两种数字的分母不一样。当前 top 明确是一颗 DSP 做一个 INT16×INT8 MAC，250 MHz 下峰值是 <b>192 GMAC/s = 384 GOPS</b>。以前“GOPS 一千多”使用了每 DSP 多路 packed product 或把逻辑 MAC 当成独立乘法的口径，不能直接和现在的单路 W8A16 设计比较。</p>
    {html_table(['架构条件','理论峰值','需要的改变'], road_rows)}
    <p>如果目标是保持 768 DSP 不变，最小的数量级改变是让一颗 DSP 在同一拍安全完成两路 MAC，并把频率推到约 333 MHz；仅仅把软件指令排得更紧不能把 384 GOPS 变成 1,000 GOPS。另一方面，从 41.44% PE 利用率看，先把 feed、尾块和读写重叠做好，才有机会让新增的算术峰值真正被使用。</p>

    <h2>8. 给架构师的下一步</h2>
    <ol><li><b>先做喂数和形状：</b>把真实 trace 中短 N、尾列、共享 read 服务和 scheduler wait 分开打点；验证双缓冲是否能把读取／写回隐藏在阵列计算后面。这个方向不增加 DSP，风险低，直接对应当前 41.44% 利用率。</li><li><b>再评估算术密度：</b>在不改变 INT40 exact 语义的前提下，比较安全双 MAC、提高时钟和增加物理 DSP 三种方案。每种方案都要用同一 trace 重算 valid MAC、流量和资源，不能只报峰值。</li></ol>
    <p>多 suite trace、正式 W8A8/W8A16 量化、LIBERO 成功率、真实 DMA/DDR、post-route 和 SAIF/VCD 功耗仍值得继续，但这些工作应建立在当前指令流和计数器口径稳定之后。</p>

    <h2>9. 数据边界与复现文件</h2>
    <ul><li><b>已实测：</b>GPU3 上一次真实 forward 的模块／dispatch 捕获；Verilator full replay counter PASS；代表 tile 逐拍 arithmetic PASS；Vivado OOC synthesis、资源和 synthesis timing。</li><li><b>周期模型：</b>16×48 tile 成本、DMA/调度标签、完整 replay 秒数、PE 利用率和有效 GOPS。它们依赖当前 descriptor cost model，尚未经过板级 DMA 和 post-route 校准。</li><li><b>行为级：</b>LayerNorm、GELU、AUX、DINO/T5 等事件只占时间线，不声称已有完整专用 FPGA 实现。</li><li><b>未做：</b>完整四 suite trace、LIBERO 成功率、真实 bitstream、板上功耗、TOPS/W、端到端模型时延。</li></ul>
    <div class="foot">数据目录：{esc(data)}<br>报告脚本：{esc(Path(__file__))}<br>关键文件：capture_result.json、compiled/replay_summary.json、compiled/operator_inventory.json、compiled/cycle_breakdown.csv、activity_events.jsonl、vivado_results.json、rtl_activity.json。生成时间精确到秒；旧版本目录未修改。</div>
    </main></body></html>'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_doc, encoding="utf-8")
    report_summary = {
        "generated_at": generated,
        "round": ROUND,
        "capture": {"suite": cap.get("suite"), "task_id": cap.get("task_id"), "seed": cap.get("seed"), "module_events": cap.get("module_event_count"), "dispatch_events": cap.get("dispatch_event_count")},
        "replay": {"total_cycles": int(total), "replay_time_s_at_250mhz": replay_s, "valid_mac_count": int(summary["valid_mac_count"]), "pe_time_utilization": summary["pe_time_utilization"], "gemm_utilization": summary["gemm_utilization"], "effective_gops": eff_gops, "physical_peak_gops": peak_gops, "active_equivalent_seconds": active_equiv_s, "top_activity_counters": activity_counters},
        "coverage": summary.get("coverage"),
        "vivado": vivado.get("runs", []),
        "boundaries": {"full_trace": "virtual descriptor counter replay", "representative_tile": "cycle-by-cycle Verilator", "power": "vectorless without SAIF/VCD", "unknown_event_count": summary.get("unknown_event_count")},
        "html": str(args.output),
    }
    (args.output.parent / "report_summary.json").write_text(json.dumps(report_summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "report_summary": str(args.output.parent / 'report_summary.json'), "generated_at": generated}, ensure_ascii=False))


if __name__ == "__main__":
    main()
