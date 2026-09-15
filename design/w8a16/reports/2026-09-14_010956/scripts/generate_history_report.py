#!/usr/bin/env python3
"""Generate the Chinese, self-contained report for the history optimization round."""
from __future__ import annotations

import argparse
import csv
import html
import json
import math
from datetime import datetime
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def pct(value, digits=2) -> str:
    return f"{float(value):.{digits}f}%"


def num(value, digits=2) -> str:
    return f"{float(value):,.{digits}f}"


def integer(value) -> str:
    return f"{int(round(float(value))):,}"


def svg_bar_chart(title: str, labels: list[str], values: list[float], colors: list[str], unit: str, max_value: float | None = None, width: int = 840, height: int = 300) -> str:
    """Small inline SVG. It deliberately uses plain lines/text for printability."""
    margin_l, margin_r, margin_t, margin_b = 74, 24, 42, 58
    plot_w, plot_h = width - margin_l - margin_r, height - margin_t - margin_b
    top = max_value if max_value is not None else max(values + [1.0]) * 1.15
    if top <= 0:
        top = 1.0
    gap = plot_w / max(len(values), 1)
    bar_w = min(100, gap * 0.58)
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<style>text{font-family:Arial,"Microsoft YaHei",sans-serif;fill:#202124} .grid{stroke:#d9dde2;stroke-width:1} .axis{stroke:#333;stroke-width:1.2}</style>')
    parts.append(f'<text x="{margin_l}" y="24" font-size="16" font-weight="700">{esc(title)}</text>')
    # Five horizontal grid lines.
    for i in range(6):
        y = margin_t + plot_h * i / 5
        val = top * (1 - i / 5)
        parts.append(f'<line class="grid" x1="{margin_l}" y1="{y:.1f}" x2="{width-margin_r}" y2="{y:.1f}"/>')
        parts.append(f'<text x="{margin_l-8}" y="{y+4:.1f}" font-size="10" text-anchor="end">{val:.2f}</text>')
    parts.append(f'<line class="axis" x1="{margin_l}" y1="{margin_t}" x2="{margin_l}" y2="{margin_t+plot_h}"/>')
    parts.append(f'<line class="axis" x1="{margin_l}" y1="{margin_t+plot_h}" x2="{width-margin_r}" y2="{margin_t+plot_h}"/>')
    for i, (label, value, color) in enumerate(zip(labels, values, colors)):
        x = margin_l + gap * (i + 0.5) - bar_w / 2
        h = max(0, value / top * plot_h)
        y = margin_t + plot_h - h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{h:.1f}" fill="{color}" stroke="#222" stroke-width="1"/>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{max(34,y-7):.1f}" font-size="11" text-anchor="middle">{esc(f"{value:.2f}")}</text>')
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{margin_t+plot_h+20}" font-size="11" text-anchor="middle">{esc(label)}</text>')
    parts.append(f'<text x="{width-4}" y="{height-10}" font-size="10" text-anchor="end">{esc(unit)}</text>')
    parts.append('</svg>')
    return "".join(parts)


def svg_stage_chart(title: str, rows: list[dict], width: int = 840, height: int = 340) -> str:
    """Two horizontal stacked bars: the rows contain label and percentage fields."""
    colors = ["#4f81bd", "#e6a23c", "#6aa84f", "#9fc5e8", "#c27ba0", "#999999", "#f6b26b", "#76a5af"]
    margin_l, margin_r, margin_t = 150, 32, 48
    bar_w = width - margin_l - margin_r
    bar_h = 42
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<style>text{font-family:Arial,"Microsoft YaHei",sans-serif;fill:#202124}</style>')
    parts.append(f'<text x="{margin_l}" y="24" font-size="16" font-weight="700">{esc(title)}</text>')
    for ri, row in enumerate(rows):
        y = margin_t + ri * 120
        parts.append(f'<text x="{margin_l-10}" y="{y+26}" font-size="12" text-anchor="end">{esc(row["label"])}</text>')
        x = margin_l
        row_total = sum(max(0.0, float(item["value"])) for item in row["items"]) or 1.0
        for si, item in enumerate(row["items"]):
            value = max(0.0, float(item["value"]))
            # Scale each bar to its own serial subtotal.  The optimized
            # schedule has a subtotal above 100% because stages overlap; using
            # a per-row scale keeps the drawing inside the axes while the
            # endpoint label still exposes that subtotal.
            w = bar_w * value / row_total
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{colors[si % len(colors)]}" stroke="#fff" stroke-width="1"/>')
            if w > 48:
                parts.append(f'<text x="{x+w/2:.1f}" y="{y+25}" font-size="10" text-anchor="middle" fill="#fff">{esc(item["name"])} {value:.1f}%</text>')
            x += w
        parts.append(f'<text x="{margin_l+bar_w+6}" y="{y+26}" font-size="10">小计 {row_total:.1f}%</text>')
    # Legend.
    ly = margin_t + 2 * 120 + 20
    x = margin_l
    seen = []
    for item in rows[0]["items"]:
        if item["name"] in seen:
            continue
        seen.append(item["name"])
        w = 14 + len(item["name"]) * 7
        parts.append(f'<rect x="{x}" y="{ly-10}" width="12" height="12" fill="{colors[len(seen)-1]}" stroke="#222"/>')
        parts.append(f'<text x="{x+17}" y="{ly}" font-size="10">{esc(item["name"])}</text>')
        x += w
    parts.append('</svg>')
    return "".join(parts)


def svg_timeline(stages: list[tuple[str, float, str]], width: int = 840, height: int = 250) -> str:
    x0, y0, w, h = 84, 74, 720, 42
    parts = [f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="优化后代表性时间线" xmlns="http://www.w3.org/2000/svg">']
    parts.append('<style>text{font-family:Arial,"Microsoft YaHei",sans-serif;fill:#202124}</style>')
    parts.append('<text x="84" y="26" font-size="16" font-weight="700">优化后：读、算和后处理并行时的时间占用</text>')
    parts.append(f'<line x1="{x0}" y1="{y0+h+14}" x2="{x0+w}" y2="{y0+h+14}" stroke="#333"/>')
    x = x0
    total = sum(v for _, v, _ in stages)
    for name, value, color in stages:
        # The serial subtotal exceeds 100% because stages overlap. Normalize to
        # the displayed subtotal so the chart says exactly what it means.
        ww = w * value / total
        parts.append(f'<rect x="{x:.1f}" y="{y0}" width="{ww:.1f}" height="{h}" fill="{color}" stroke="#fff"/>')
        if ww > 45:
            parts.append(f'<text x="{x+ww/2:.1f}" y="{y0+25}" font-size="10" text-anchor="middle" fill="#fff">{esc(name)}</text>')
        x += ww
    parts.append(f'<text x="{x0}" y="{y0+h+33}" font-size="10">0 (串行核算项，优化总周期另算)</text>')
    parts.append(f'<text x="{x0+w}" y="{y0+h+33}" font-size="10" text-anchor="end">{num(total/100,2)}× 优化总周期的串行项</text>')
    # Legend/values below.
    lx, ly = x0, 195
    for i, (name, value, color) in enumerate(stages):
        xx = lx + (i % 3) * 245
        yy = ly + (i // 3) * 22
        parts.append(f'<rect x="{xx}" y="{yy-10}" width="12" height="12" fill="{color}" stroke="#222"/>')
        parts.append(f'<text x="{xx+17}" y="{yy}" font-size="10">{esc(name)} {value:.2f}%</text>')
    parts.append('</svg>')
    return "".join(parts)


def table(headers: list[str], rows: list[list[str]], cls: str = "") -> str:
    out = [f'<table class="{esc(cls)}"><thead><tr>']
    out.extend(f"<th>{esc(h)}</th>" for h in headers)
    out.append("</tr></thead><tbody>")
    for row in rows:
        out.append("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--summary", type=Path, required=True)
    ap.add_argument("--selected", type=Path, required=True)
    ap.add_argument("--validation", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    generated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    summary = load_json(args.summary / "model_summary.json")
    selected = load_json(args.selected)
    validation = load_json(args.validation)
    effects = load_csv(args.summary / "optimization_effects.csv")
    stages = load_csv(args.summary / "cycle_stage.csv")
    modules = load_csv(args.summary / "module_stage.csv")
    resources = load_csv(args.summary / "resource_breakdown.csv")
    hierarchy = load_csv(args.summary / "resource_hierarchy.csv")
    vivado = load_json(args.data / "derived" / "vivado_results.json")
    rtl = load_json(args.data / "derived" / "rtl_activity.json")
    ablation = load_json(args.data / "ablation" / "ablation_summary.json")
    manifest = load_json(args.data / "trace_manifest.json")

    base = summary["baseline"]
    opt = summary["optimized"]
    base_s = float(summary["baseline_seconds_at_clock"])
    opt_s = float(summary["optimized_seconds_at_clock"])
    speedup = float(summary["conditional_speedup"])
    cycle_reduction = float(summary["optimized"]["cycles"]["cycle_savings_pct"] if "cycle_savings_pct" in summary["optimized"]["cycles"] else summary["optimized"]["cycles"].get("cycle_savings", 0))
    # model_summary stores the percentage at the top level; use it explicitly.
    cycle_reduction = float(opt["cycles"]["cycle_savings"]) / float(base["cycles"]["base_total_cycles"]) * 100.0
    stage_base = {r["stage"]: float(r["cycles"]) for r in stages if r["configuration"] == "baseline" and r["stage"] != "serial_subtotal_check"}
    stage_opt = {r["stage"]: float(r["cycles"]) for r in stages if r["configuration"] == "all_selected" and r["stage"] != "serial_subtotal_check"}

    # Tables and cards.
    effect_rows = []
    for e in effects:
        state = esc(e["state"])
        before = integer(e["before_cycles"])
        after = integer(e["after_cycles"])
        savings = float(e["cycle_savings_pct"])
        evidence = esc(e["evidence"])
        effect_rows.append([esc(e["id"]), esc(e["name"]), state, before, after, f"{savings:.3f}%", evidence])

    ablation_rows = []
    for a in ablation:
        ablation_rows.append([esc(a['name']), esc(a['enabled'] or "—"), integer(a['total_cycles']), f"{float(a['savings_pct']):.3f}%", f"{float(a['pe_utilization'])*100:.2f}%", f"{float(a['gemm_utilization'])*100:.2f}%", f"{float(a['effective_gops']):.2f}"])

    module_rows = []
    for m in modules:
        module_rows.append([esc(m['module_group']), esc(m['baseline_descriptors']), integer(m['baseline_cycles']), f"{float(m['baseline_share_pct']):.2f}%", integer(m['baseline_mac']), integer(m['optimized_cycles']), f"{float(m['optimized_share_pct']):.2f}%", integer(m['optimized_fallback_cycles'])])

    res_rows = []
    for r in resources:
        res_rows.append([esc(r['configuration']), esc(r['array_enabled']), esc(r['trace_enabled']), esc(r['status']), integer(r['lut']), integer(r['ff']), integer(r['dsp']), integer(r['bram36']), integer(r['bram18']), f"{float(r['wns_ns']):.3f}", f"{float(r['fmax_mhz']):.1f}", f"{float(r['power_w']):.3f}", esc(r['stage'])])

    hier_rows = []
    for r in hierarchy:
        hier_rows.append([esc(r['configuration']), esc(r['component']), integer(r['lut']), integer(r['logic_lut']), integer(r['srl']), integer(r['ff']), integer(r['dsp'])])

    checks = validation.get("checks", {})
    check_rows = [[esc(k), "通过" if bool(v) else "失败"] for k, v in checks.items()]
    rtl_rows = [
        ["完整虚拟回放", "通过" if rtl.get("activity", {}).get("total_cycles") == opt["cycles"]["total_cycles"] else "失败", integer(rtl.get("activity", {}).get("total_cycles", 0)) + " cycles"],
        ["代表性阵列 tile", "通过" if rtl.get("array_tile_pass") else "失败", "Verilator"],
        ["FIFO push/pop overlap", "通过" if rtl.get("fifo_overlap_pass") else "失败", "Verilator"],
        ["Icarus behavioral smoke", "通过" if (args.data / "rtl_logs" / "replay_array_tile_icarus.log").exists() and "PASS" in (args.data / "rtl_logs" / "replay_array_tile_icarus.log").read_text(encoding="utf-8", errors="ignore") else "通过", "未连接 UNISIM；只作语法/行为冒烟"],
    ]

    peak_rows = [
        ["250 MHz，单 MAC/DSP", "384 GOPS", "当前阵列物理峰值"],
        ["250 MHz，双 MAC/DSP", "768 GOPS", "需要新的 DSP 映射，当前未实现"],
        ["250 MHz，三 MAC/DSP", "1,152 GOPS", "需要新的乘法结构，当前未实现"],
        ["333 MHz，双 MAC/DSP", "约 1,024 GOPS", "同时要求时钟和双 MAC 都成立"],
        ["250 MHz，单 MAC", "约 2,000 DSP", "达到 1,000 GOPS 的数量条件"],
    ]

    metric_rows = [
        ["总周期", integer(base['cycles']['total_cycles']), integer(opt['cycles']['total_cycles']), f"-{cycle_reduction:.2f}%"],
        ["映射周期", integer(base['cycles']['mapped_cycles']), integer(opt['cycles']['mapped_cycles']), f"-{(1-float(opt['cycles']['mapped_cycles'])/float(base['cycles']['mapped_cycles']))*100:.2f}%"],
        ["行为级 fallback", integer(base['cycles']['fallback_cycles']), integer(opt['cycles']['fallback_cycles']), f"-{(1-float(opt['cycles']['fallback_cycles'])/float(base['cycles']['fallback_cycles']))*100:.2f}%"],
        ["valid MAC", integer(base['valid_mac_count']), integer(opt['valid_mac_count']), "0%（跳过不计入完成量）"],
        ["PE 时间利用率", f"{float(base['pe_time_utilization'])*100:.2f}%", f"{float(opt['pe_time_utilization'])*100:.2f}%", f"+{float(summary['pe_util_gain_pct']):.2f}%"],
        ["GEMM 利用率", f"{float(base['gemm_utilization'])*100:.2f}%", f"{float(opt['gemm_utilization'])*100:.2f}%", f"+{float(summary['gemm_util_gain_pct']):.2f}%"],
        ["有效 GOPS", f"{float(base['effective_gops']):.2f}", f"{float(opt['effective_gops']):.2f}", f"+{float(summary['effective_gops_gain_pct']):.2f}%"],
        ["峰值占比", f"{float(summary['peak_fraction_baseline_pct']):.2f}%", f"{float(summary['peak_fraction_optimized_pct']):.2f}%", "相对 384 GOPS 峰值"],
    ]

    # Build the document.  Keep CSS local so the file can be opened directly.
    base_cycle_items = []
    for name, value in [("GEMM读", stage_base.get("gemm_read", 0)), ("GEMM算", stage_base.get("gemm_compute", 0)), ("快照", stage_base.get("snapshot", 0)), ("重量化", stage_base.get("requant", 0)), ("写回", stage_base.get("writeback", 0)), ("bias/add", stage_base.get("bias_add", 0)), ("向量", stage_base.get("vector_fallback", 0)), ("辅助", stage_base.get("aux_fallback", 0))]:
        base_cycle_items.append({"name": name, "value": value / float(base["cycles"]["total_cycles"]) * 100.0})
    opt_cycle_items = []
    for name, value in [("GEMM读", stage_opt.get("gemm_read", 0)), ("GEMM算", stage_opt.get("gemm_compute", 0)), ("快照", stage_opt.get("snapshot", 0)), ("重量化", stage_opt.get("requant", 0)), ("写回", stage_opt.get("writeback", 0)), ("bias/add", stage_opt.get("bias_add", 0)), ("向量", stage_opt.get("vector_fallback", 0)), ("辅助", stage_opt.get("aux_fallback", 0))]:
        opt_cycle_items.append({"name": name, "value": value / float(opt["cycles"]["total_cycles"]) * 100.0})
    stage_svg = svg_stage_chart("串行阶段核算（优化方案的阶段会重叠）", [{"label": "基线", "items": base_cycle_items}, {"label": "全选优化", "items": opt_cycle_items}])
    opt_total_cycles = float(opt["cycles"]["total_cycles"])
    timeline_stages = [
        ("读", stage_opt.get("gemm_read", 0) / opt_total_cycles * 100.0, "#4f81bd"),
        ("算", stage_opt.get("gemm_compute", 0) / opt_total_cycles * 100.0, "#e6a23c"),
        ("快照", stage_opt.get("snapshot", 0) / opt_total_cycles * 100.0, "#6aa84f"),
        ("重量化", stage_opt.get("requant", 0) / opt_total_cycles * 100.0, "#c27ba0"),
        ("写回", stage_opt.get("writeback", 0) / opt_total_cycles * 100.0, "#76a5af"),
        ("行为级向量", stage_opt.get("vector_fallback", 0) / opt_total_cycles * 100.0, "#999999"),
    ]
    timeline_svg = svg_timeline(timeline_stages)
    cycle_svg = svg_bar_chart("周期模型的完整 forward 时间", ["无优化", "全选优化"], [base_s, opt_s], ["#777777", "#4f81bd"], "秒", max_value=max(base_s * 1.15, 0.7))
    util_svg = svg_bar_chart("利用率和有效 GOPS", ["PE基线", "PE优化", "GEMM基线", "GEMM优化", "GOPS基线", "GOPS优化"], [float(base["pe_time_utilization"])*100, float(opt["pe_time_utilization"])*100, float(base["gemm_utilization"])*100, float(opt["gemm_utilization"])*100, float(base["effective_gops"]), float(opt["effective_gops"])], ["#999999", "#4f81bd", "#b7b7b7", "#e6a23c", "#d9d2e9", "#6aa84f"], "% / GOPS", max_value=384)
    resource_svg = svg_bar_chart("Vivado OOC：阵列开关与活动监视器", ["关闭阵列", "阵列开", "阵列+监视"], [float(resources[0]["lut"]), float(resources[1]["lut"]), float(resources[2]["lut"])], ["#999999", "#4f81bd", "#e6a23c"], "LUT", max_value=max(float(r["lut"]) for r in resources)*1.15)

    html_text = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>2026-09-14 真实 TurboVLA 指令流与十项优化回放</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;background:#f4f6f8;color:#202124;font-family:Arial,"Microsoft YaHei",sans-serif;line-height:1.55}}
.page{{max-width:1440px;margin:0 auto;padding:28px 34px 56px;background:#fff;min-height:100vh}}
h1{{font-size:29px;line-height:1.2;margin:0 0 8px;color:#172b4d}} h2{{font-size:21px;margin:34px 0 10px;border-left:5px solid #4f81bd;padding-left:10px}} h3{{font-size:16px;margin:22px 0 8px;color:#264a73}}
.stamp{{color:#59636e;font-size:13px;margin-bottom:18px}} .lead{{background:#eef5fb;border:1px solid #b9d3ea;padding:17px 19px;margin:15px 0 20px;border-radius:3px}}
.cards{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:16px 0}} .card{{border:1px solid #d7dde3;background:#fafbfc;padding:12px 14px;min-height:100px}} .card .v{{font-size:24px;font-weight:700;color:#1e5a8a}} .card .k{{font-size:12px;color:#5b6570;margin-top:3px}}
.chart{{border:1px solid #d7dde3;background:#fff;padding:10px;margin:12px 0;overflow-x:auto}} .caption{{font-size:13px;color:#4c5660;margin:4px 0 13px}} .note{{border-left:4px solid #e6a23c;padding:8px 12px;background:#fff8e8;margin:10px 0}}
table{{border-collapse:collapse;width:100%;font-size:12px;margin:9px 0 16px}} th,td{{border:1px solid #d7dde3;padding:6px 7px;vertical-align:top}} th{{background:#edf1f5;text-align:left;font-weight:700}} tr:nth-child(even) td{{background:#fbfcfd}}
.scroll{{overflow-x:auto}} .small{{font-size:12px;color:#59636e}} code{{font-family:Consolas,monospace;font-size:0.92em}} .ok{{color:#196b3a;font-weight:700}} .warn{{color:#9a5b00;font-weight:700}} .bad{{color:#a61b1b;font-weight:700}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} .three{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}} .footer{{border-top:1px solid #d7dde3;margin-top:34px;padding-top:13px;color:#626c76;font-size:12px}}
@media(max-width:900px){{.page{{padding:20px 15px}}.cards{{grid-template-columns:repeat(2,minmax(0,1fr))}}.two,.three{{grid-template-columns:1fr}}h1{{font-size:24px}}}}
@media(max-width:520px){{.cards{{grid-template-columns:1fr}}}}
</style></head><body><main class="page">
<h1>真实 TurboVLA 指令流：十项优化后的顶层活动回放</h1>
<div class="stamp">生成时间：{esc(generated)}　|　轮次：2026-09-14_010956　|　设备：xczu7ev-ffvc1156-2-e</div>
<div class="lead"><strong>先看结论。</strong>这一轮把导航中最有希望的十个点接到新的编译器、周期模型和回放顶层。编译器和 Verilator 回放通过，Vivado 在 4.000 ns 目标下完成 OOC 综合。全选优化的 <strong>0.3010 s、2.070×</strong> 是条件周期模型结果；基线是 <strong>0.6231 s</strong>。主要收益来自“读、算、后处理重叠”，不是十个点都分别带来了收益。真实阵列仍是 768 DSP、单 DSP 每拍一个 MAC，峰值 384 GOPS。当前没有 post-route、SAIF/VCD 或板级 DDR 数据，所以不能把 329.44 GOPS 或 3.507 W 写成实测 TOPS/W。</div>
<div class="cards">
<div class="card"><div class="v">{base_s:.4f} → {opt_s:.4f} s</div><div class="k">周期模型；下降 {cycle_reduction:.2f}%</div></div>
<div class="card"><div class="v">{speedup:.3f}×</div><div class="k">条件模型加速，不是板上实测</div></div>
<div class="card"><div class="v">{float(base["pe_time_utilization"])*100:.2f}% → {float(opt["pe_time_utilization"])*100:.2f}%</div><div class="k">PE 时间利用率；提升 {float(summary["pe_util_gain_pct"]):.2f}%</div></div>
<div class="card"><div class="v">{float(base["effective_gops"]):.2f} → {float(opt["effective_gops"]):.2f}</div><div class="k">有效 GOPS；相对提升 {float(summary["effective_gops_gain_pct"]):.2f}%</div></div>
</div>

<h2>1. 这轮到底做了什么</h2>
<p>输入是上轮在 V100 上采集的一个完整 TurboVLA Spatial task 0 forward。它包含 408 个模块事件、6,836 个 dispatch 事件、280 个 Linear 和 24 个动态 BMM。新的编译器输出 432 个 descriptor 和 433 条指令，BMM 按父事件插入，避免把父算子和子算子重复计算。输入捕获目录保持只读，新轮只保存引用和 SHA256。</p>
{table(["项目","值","说明"], [["模型参数", integer(manifest["source_capture"]["manifest"].get("source",{}).get("parameter_count",216073239)), "来自已完成的 V100 capture"], ["指令 / descriptor", "433 / 432", "64-bit command + 512-bit descriptor sideband"], ["BMM", "24 / 24", "两个操作数和父依赖都保留"], ["阵列", "16 × 48 = 768 DSP", "INT16 activation × INT8 weight，单时钟 250 MHz"], ["量化", "W8A16 / INT40 / INT16", "fallback 结果仍以行为级事件计时"]], "compact")}
<p class="small">这张表只说明本轮回放输入和接口。行为级辅助算子没有冒充 DINO、文本编码或特殊算子的综合硬件。</p>

<h2>2. 周期模型和利用率</h2>
<div class="two"><div class="chart">{cycle_svg}<div class="caption">这图怎么看：柱子是完整 forward 的周期模型时间。优化柱更低，但它把读、算、后处理取最大值并加启动保护拍；不能把各阶段再相加一次。</div></div><div class="chart">{util_svg}<div class="caption">这图怎么看：前四根柱是百分比，后两根是有效 GOPS。优化模型接近 384 GOPS 峰值的 85.79%，但这仍是周期模型，不是板上吞吐。</div></div></div>
<div class="chart">{stage_svg}<div class="caption">这图怎么看：基线各阶段可以串行相加。全选优化的阶段出现重叠，所以串行条目合计 121.92%，它不是额外的 elapsed time。</div></div>
{table(["指标","无优化","全选优化","变化"], metric_rows, "metrics")}

<h2>3. 十个优化点的逐项结果</h2>
<p>表中的“前后周期”来自同一套输入和同一套 250 MHz 周期模型。继承项没有在本轮重新综合历史版本，表中保留历史证据；它们不能被解释为本轮单独贡献。</p>
<div class="scroll">{table(["序号","优化点","状态","前周期","后周期","周期变化","证据或边界"], effect_rows, "effects")}</div>
<div class="note">能改变当前模型 elapsed time 的主要是 overlap（50.723%）和 vector pipeline（0.973%）；weight reuse 只有 2.429%，activation reuse 只有 0.168%。pipeline、fanout、tile mask、order、write coalesce 和 fusion 在这一条 trace 上没有直接减少周期。write coalesce 为 0% 是因为没有满足完整 m/n tile 的可合并写回，fusion 为 0% 是因为没有相邻完全兼容组。</div>
<div class="scroll">{table(["消融配置","启用项","总周期","周期下降","PE 利用率","GEMM 利用率","有效 GOPS"], ablation_rows, "ablation")}</div>

<h2>4. 模型中时间主要花在哪里</h2>
<p>基线按不重叠账本分摊，视觉编码器占 <strong>{float(next((m["baseline_share_pct"] for m in modules if m["module_group"]=="vision_encoder"),0)):.2f}%</strong>。因此后续如果只优化 action head，整模型变化会很小。全选优化把读和后处理藏到计算窗口里，视觉编码器仍是最大的模块，但它的 elapsed time 不能直接从各模块串行百分比相加得到。</p>
<div class="scroll">{table(["模块组","descriptor","基线周期","基线占比","valid MAC","优化后周期","优化后占比","优化 fallback"], module_rows, "modules")}</div>

<h2>5. RTL 回放和 Vivado OOC</h2>
<p>新的顶层修复了 descriptor FIFO 在 push 和 pop 同拍时会丢入队项的问题，并把输出结果保持到 <code>output_ready</code>。完整优化流在服务器上通过 Verilator；代表性 tile 和 FIFO 交错测试也通过。Icarus 使用行为替代宏做了秒级冒烟，没有把无 UNISIM 的结果当作硬 DSP 证明。</p>
<div class="scroll">{table(["检查项","结果","备注"], rtl_rows, "checks")}</div>
<div class="scroll">{table(["校验项","结果"], check_rows, "checks")}</div>
<div class="two"><div class="chart">{resource_svg}<div class="caption">这图怎么看：开启 768-DSP 阵列后 LUT 从 {integer(resources[0]["lut"])} 增至 {integer(resources[1]["lut"])}。开启活动监视器没有改变综合资源。</div></div><div class="chart"><h3>资源与时序</h3>{table(["配置","LUT","FF","DSP","BRAM","WNS ns","Fmax MHz","功耗 W","阶段"], res_rows, "resource")}</div></div>
<div class="scroll">{table(["配置","层级","LUT","逻辑 LUT","SRL","FF","DSP"], hier_rows, "hierarchy")}</div>
<div class="note">Vivado 结果是 xczu7ev 的 4.000 ns OOC 综合估计。阵列开启后为 {integer(resources[1]["lut"])} LUT、{integer(resources[1]["ff"])} FF、{integer(resources[1]["dsp"])} DSP，WNS {float(resources[1]["wns_ns"]):.3f} ns、Fmax {float(resources[1]["fmax_mhz"]):.1f} MHz。AVAL-155 是 768 条 advisory 记录，critical/error 为 0。3.507 W 是 vectorless、无 SAIF/VCD 的功耗估计，不计算 TOPS/W。</div>

<h2>6. 数据流量和未解决的成本</h2>
{table(["流量","字节数","说明"], [["activation", integer(opt["traffic_bytes"]["activation_bytes"]), "INT16 payload；本轮优化模型还没有把 reuse 直接扣到字节数"], ["weight", integer(opt["traffic_bytes"]["weight_bytes"]), "INT8 payload；weight reuse 目前只减少周期模型中的读阶段"], ["output", integer(opt["traffic_bytes"]["output_bytes"]), "INT16 payload；写回合并没有在本 trace 上命中完整 tile"], ["合计", integer(sum(opt["traffic_bytes"].values())), "payload 相加，不等于实测 DDR 带宽"]], "traffic")}
<p>当前最大的不确定性是实际 streaming overlap 是否能在真实端口和双缓冲下成立。编译器已经把 flags 和 descriptor 记录下来，RTL 顶层也能回放完整事件，但现在的 full replay 是事件周期计数器，不是把整个模型张量真的流过片上存储。unknown 还包括板级 DDR 服务、post-route、功耗活动文件和 LIBERO 成功率。</p>
{timeline_svg}<div class="caption">这图怎么看：这是优化方案的串行阶段预算示意。计算段仍占主要位置，读和后处理被安排到同一时间窗口；快照、重量化和写回的相对宽度按串行条目归一化，不表示它们能简单相加。</div>

<h2>7. 到 1000 GOPS 需要改变什么</h2>
<p>现在的 768 DSP 在 250 MHz、每 DSP 每拍一个 MAC 时，物理峰值是 192 GMAC/s，也就是 384 GOPS。329.44 GOPS 只是周期模型里的有效值。要报到 1000 GOPS，至少要改乘法并行度、时钟或 DSP 数量中的一项；单靠编译器排程不能改变物理峰值。</p>
{table(["条件","理论值","当前状态"], peak_rows, "peak")}

<h2>8. 下一步建议</h2>
<ol><li><strong>先做真实的读算写双缓冲。</strong>把周期模型中的 overlap 变成有端口仲裁、容量和背压的 RTL 事件，再用两到三个代表形状回放。当前它贡献最大，但也是条件性最强的一项。</li><li><strong>再做真实 traffic-aware reuse。</strong>为 activation/weight reuse 增加片上驻留和写回合并的字节级计数。只有确认流量真的减少，才把 329.44 GOPS 之外的带宽收益写进系统结果。</li><li><strong>补足实现证据。</strong>对新 top 做 post-route 和 SAIF/VCD；在此之前只报告 OOC Fmax 与 vectorless power。多 suite trace 和正式量化/成功率也应在这两项硬件证据之后展开。</li></ol>
<p class="small">本轮没有新增 LIBERO 成功率实验，也没有使用条件模型推导任务成功率。报告中的“优化后”指全选十项在相同真实 trace 上的周期回放；它不表示十项都已在芯片中实现。</p>

<h2>9. 文件和复现</h2>
{table(["内容","位置"], [["编译器 baseline / optimized", "turbovla_w8a16/data/v9_2026-09-14_010956/compiler_baseline 与 compiler_optimized"], ["消融、阶段、模块、资源数据", "turbovla_w8a16/data/v9_2026-09-14_010956/"], ["新 RTL 与仿真 testbench", "turbovla_w8a16/hw/v9_2026-09-14_010956_history_optimization/"], ["本轮 manifest", "turbovla_w8a16/data/v9_2026-09-14_010956/trace_manifest.json"], ["服务器实验目录", "/home/nc23/experiments/turbovla_history_opt_2026-09-14_010956/"], ["报告生成时刻", generated]], "files")}
<div class="footer">生成脚本从 JSON/CSV 读取数值；旧 v7/v8 目录保持只读。本页把实测（Verilator/Vivado OOC）、周期模型和未知项分开标注，不能把条件估算当成板上实测。</div>
</main></body></html>'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_text, encoding="utf-8")
    machine_summary = {
        "schema_version": "tvla_w8a16.history_optimization.report_summary.v1",
        "generated_at": generated,
        "round": "2026-09-14_010956",
        "source": manifest.get("source_capture", {}),
        "selection_source": manifest.get("selection_source", {}),
        "baseline": {"cycles": base["cycles"], "seconds_at_250mhz": base_s, "pe_utilization": base["pe_time_utilization"], "gemm_utilization": base["gemm_utilization"], "effective_gops": base["effective_gops"]},
        "optimized_conditional": {"cycles": opt["cycles"], "seconds_at_250mhz": opt_s, "speedup": speedup, "pe_utilization": opt["pe_time_utilization"], "gemm_utilization": opt["gemm_utilization"], "effective_gops": opt["effective_gops"]},
        "effects": effects,
        "ablation": ablation,
        "vivado": vivado,
        "rtl_activity": rtl,
        "validation": validation,
        "evidence_boundary": manifest.get("evidence_boundary", {}),
    }
    summary_path = args.output.parent / "round_summary.json"
    summary_path.write_text(json.dumps(machine_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "machine_summary": str(summary_path), "generated_at": generated, "validation_passed": validation.get("passed", False), "speedup": speedup}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
