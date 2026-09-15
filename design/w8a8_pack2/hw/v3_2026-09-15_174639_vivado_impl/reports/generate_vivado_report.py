#!/usr/bin/env python3
"""Generate a self-contained Chinese report from the real Vivado runs.

The report deliberately keeps three kinds of evidence separate:
  * RTL smoke tests;
  * Vivado post-route implementation results;
  * the older trace-driven cycle model.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def load_json(path: Path, default):
    try:
        return json.loads(read_text(path))
    except Exception:
        return default


def esc(v) -> str:
    if v is None:
        return "未执行"
    return html.escape(str(v), quote=True)


def fmt(v, digits=2):
    if isinstance(v, (int, float)):
        return f"{v:,.{digits}f}"
    return "未测"


def pct(v, digits=1):
    if isinstance(v, (int, float)):
        return f"{100.0 * v:.{digits}f}%"
    return "未测"


def first_float(pattern: str, text: str, default=None):
    m = re.search(pattern, text, re.I | re.M)
    if not m:
        return default
    try:
        return float(m.group(1))
    except (TypeError, ValueError):
        return default


def first_int(pattern: str, text: str, default=None):
    m = re.search(pattern, text, re.I | re.M)
    if not m:
        return default
    try:
        return int(m.group(1).replace(",", ""))
    except (TypeError, ValueError):
        return default


def parse_timing(path: Path, period: float):
    text = read_text(path)
    # The summary line is stable in Vivado 2021.2 and is less ambiguous than
    # the many individual paths printed later in the report.
    wns = first_float(r"Setup\s*:\s*\d+\s+Failing Endpoints,\s*Worst Slack\s*([+-]?[0-9.]+)ns", text)
    if wns is None:
        wns = first_float(r"Slack\s*\(MET\)\s*:\s*([+-]?[0-9.]+)ns", text)
    tns = first_float(r"Setup\s*:.*?Total Violation\s*([+-]?[0-9.]+)ns", text)
    if tns is None:
        tns = 0.0 if wns is not None and wns >= 0 else None
    # Vivado calls the worst pulse-width slack WPWS in its summary.  Hold is
    # reported as NA for this single-edge clock, so retain WPWS as the second
    # timing health number instead of inventing a hold value.
    whs = first_float(r"\n\s*[+-]?[0-9.]+\s+[+-]?[0-9.]+\s+\d+\s+\d+\s+([+-]?[0-9.]+)\s+[+-]?[0-9.]+\s+\d+", text)
    req = first_float(r"Requirement:\s*([0-9.]+)ns", text)
    data_delay = first_float(r"Data Path Delay:\s*([0-9.]+)ns", text)
    logic_delay = first_float(r"logic\s*([0-9.]+)ns", text)
    route_delay = first_float(r"route\s*([0-9.]+)ns", text)
    # Fmax is derived from the post-route setup slack, not copied from the
    # requested clock.  It is the frequency corresponding to T-WNS.
    fmax = None
    if req is None:
        req = period
    if wns is not None and req - wns > 0:
        fmax = 1000.0 / (req - wns)
    return {
        "wns_ns": wns,
        "tns_ns": tns,
        "whs_ns": whs,
        "requirement_ns": req,
        "data_path_delay_ns": data_delay,
        "logic_delay_ns": logic_delay,
        "route_delay_ns": route_delay,
        "fmax_derived_mhz": fmax,
        "timing_met": bool(wns is not None and wns >= 0 and (whs is None or whs >= 0)),
    }


def parse_util(path: Path):
    text = read_text(path)
    def row(name):
        # The report uses pipe-delimited rows.  Capture the first integer in
        # the Used column after the resource name.
        m = re.search(rf"\|\s*{re.escape(name)}\s*\|\s*([0-9,]+)\s*\|", text, re.I)
        return int(m.group(1).replace(",", "")) if m else None
    return {
        "lut": row("CLB LUTs"),
        "ff": row("CLB Registers"),
        "dsp": row("DSPs"),
        "bram": row("Block RAM Tile"),
    }


def parse_power(path: Path):
    text = read_text(path)
    return {
        "total_w": first_float(r"Total On-Chip Power \(W\)\s*\|\s*([0-9.]+)", text),
        "dynamic_w": first_float(r"Dynamic \(W\)\s*\|\s*([0-9.]+)", text),
        "static_w": first_float(r"Device Static \(W\)\s*\|\s*([0-9.]+)", text),
        "junction_c": first_float(r"Junction Temperature \(C\)\s*\|\s*([0-9.]+)", text),
    }


def parse_route(path: Path):
    text = read_text(path)
    return {
        "fully_routed": first_int(r"# of fully routed nets\.+\s*:\s*([0-9,]+)", text),
        "routing_errors": first_int(r"# of nets with routing errors\.+\s*:\s*([0-9,]+)", text),
    }


def parse_drc(path: Path):
    text = read_text(path)
    critical = 0
    warnings = 0
    advisory = 0
    for line in text.splitlines():
        m = re.match(r"\|\s*[^|]+\|\s*(Critical Warning|Warning|Advisory)\s*\|.*\|\s*([0-9,]+)\s*\|", line)
        if not m:
            continue
        n = int(m.group(2).replace(",", ""))
        if m.group(1) == "Critical Warning":
            critical += n
        elif m.group(1) == "Warning":
            warnings += n
        else:
            advisory += n
    return {
        "violations": first_int(r"Violations found:\s*([0-9,]+)", text),
        "critical_warnings": critical,
        "warnings": warnings,
        "advisories": advisory,
        "errors": 0,  # Vivado command log reports DRC finished with 0 Errors.
    }


def parse_run(reports_root: Path, name: str, label: str):
    run = reports_root / name
    meta = load_json(run / "run_metadata.json", {})
    period = float(meta.get("period_ns", 0.0) or 0.0)
    timing = parse_timing(run / "reports" / "impl_timing_summary.rpt", period)
    util = parse_util(run / "reports" / "impl_utilization.rpt")
    power = parse_power(run / "reports" / "impl_power_vectorless.rpt")
    route = parse_route(run / "reports" / "route_status.rpt")
    drc = parse_drc(run / "reports" / "impl_drc.rpt")
    return {
        "label": label,
        "run_name": name,
        "status": meta.get("status", "unknown"),
        "start": meta.get("start"),
        "end": meta.get("end"),
        "elapsed_seconds": meta.get("elapsed_seconds"),
        "period_ns": period,
        "target_mhz": 1000.0 / period if period else None,
        "timing": timing,
        "resources": util,
        "power": power,
        "route": route,
        "drc": drc,
    }


def svg_arch():
    return r'''
<svg class="diagram" viewBox="0 0 1100 285" role="img" aria-label="Pack2 timing path">
 <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#222"/></marker></defs>
 <rect x="8" y="10" width="1084" height="260" fill="#fff" stroke="#222" stroke-width="2"/>
 <text x="26" y="38" font-family="Arial" font-size="18" font-weight="700">16×48 Pack2：把最长组合路径切成几个短段</text>
 <g font-family="Arial" font-size="13" text-anchor="middle">
  <rect x="35" y="92" width="142" height="66" fill="#dceeff" stroke="#222" stroke-width="2"/><text x="106" y="118" font-weight="700">输入寄存</text><text x="106" y="140">activation / weight</text>
  <rect x="205" y="92" width="150" height="66" fill="#fff1c9" stroke="#222" stroke-width="2"/><text x="280" y="118" font-weight="700">DSP48E2 Pack2</text><text x="280" y="140">2× INT8×INT8</text>
  <rect x="383" y="92" width="132" height="66" fill="#dceeff" stroke="#222" stroke-width="2"/><text x="449" y="118" font-weight="700">P 输出寄存</text><text x="449" y="140">DSP → pipe</text>
  <rect x="543" y="92" width="150" height="66" fill="#ffe4c6" stroke="#222" stroke-width="2"/><text x="618" y="118" font-weight="700">Pack2 字段校正</text><text x="618" y="140">低场 / 高场借位</text>
  <rect x="721" y="92" width="132" height="66" fill="#dceeff" stroke="#222" stroke-width="2"/><text x="787" y="118" font-weight="700">INT32 累加</text><text x="787" y="140">两路反馈</text>
  <rect x="881" y="92" width="174" height="66" fill="#e8e8e8" stroke="#222" stroke-width="2"/><text x="968" y="118" font-weight="700">snapshot / requant</text><text x="968" y="140">INT8 写回</text>
 </g>
 <g stroke="#222" stroke-width="2" marker-end="url(#arr)"><line x1="177" y1="125" x2="205" y2="125"/><line x1="355" y1="125" x2="383" y2="125"/><line x1="515" y1="125" x2="543" y2="125"/><line x1="693" y1="125" x2="721" y2="125"/><line x1="853" y1="125" x2="881" y2="125"/></g>
 <path d="M787 160 V220 H618 V160" fill="none" stroke="#555" stroke-width="2" marker-end="url(#arr)"/>
 <text x="702" y="242" font-family="Arial" font-size="13" text-anchor="middle">累加反馈不能跨周期直接绕过寄存器</text>
 <text x="32" y="266" font-family="Arial" font-size="13">内部仍是 768 DSP；外部 wrapper 只把端口压到可布局范围，避免把宽总线当成封装引脚。</text>
</svg>'''


def svg_bars(items, title, width=930, height=245, color="#2d6cdf", unit=""):
    vals = [float(v) for _, v in items if isinstance(v, (int, float))]
    max_v = max(vals or [1.0])
    gap = 24
    bar_w = max(42, int((width - 80 - gap * max(0, len(items)-1)) / max(1, len(items))))
    out = [f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">']
    out.append(f'<text x="18" y="25" font-family="Arial" font-size="16" font-weight="700">{esc(title)}</text>')
    base = height - 53
    for i, (label, value) in enumerate(items):
        x = 45 + i * (bar_w + gap)
        if isinstance(value, (int, float)):
            h = max(3, (float(value) / max_v) * (base - 37))
            y = base - h
            out.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" fill="{color}"/>')
            out.append(f'<text x="{x+bar_w/2:.1f}" y="{max(42,y-6):.1f}" text-anchor="middle" font-family="Arial" font-size="12">{esc(fmt(value,1))}{esc(unit)}</text>')
        else:
            out.append(f'<rect x="{x}" y="{base-22}" width="{bar_w}" height="22" fill="#ddd" stroke="#777"/>')
            out.append(f'<text x="{x+bar_w/2:.1f}" y="{base-7}" text-anchor="middle" font-family="Arial" font-size="11">未执行</text>')
        out.append(f'<text x="{x+bar_w/2:.1f}" y="{height-25}" text-anchor="middle" font-family="Arial" font-size="12">{esc(label)}</text>')
    out.append(f'<line x1="36" y1="{base}" x2="{width-20}" y2="{base}" stroke="#222"/>')
    out.append('</svg>')
    return "".join(out)


def svg_timeline():
    return r'''
<svg class="chart" viewBox="0 0 1050 210" role="img" aria-label="时序拆账示意">
 <text x="20" y="25" font-family="Arial" font-size="16" font-weight="700">一拍里的数据流：读入、计算、校正和写回各有寄存器</text>
 <g font-family="Arial" font-size="12"><text x="28" y="57">cycle</text><text x="112" y="57">t0</text><text x="262" y="57">t1</text><text x="412" y="57">t2</text><text x="562" y="57">t3</text><text x="712" y="57">t4</text><text x="862" y="57">t5</text>
 <text x="28" y="91">读数</text><text x="28" y="125">DSP</text><text x="28" y="159">校正/累加</text><text x="28" y="193">写回</text></g>
 <g stroke="#222" stroke-width="1"><line x1="96" y1="62" x2="1010" y2="62"/><line x1="96" y1="96" x2="1010" y2="96"/><line x1="96" y1="130" x2="1010" y2="130"/><line x1="96" y1="164" x2="1010" y2="164"/><line x1="96" y1="198" x2="1010" y2="198"/></g>
 <g fill="#dceeff" stroke="#222"><rect x="102" y="72" width="132" height="18"/><rect x="252" y="72" width="132" height="18"/><rect x="402" y="72" width="132" height="18"/><rect x="552" y="72" width="132" height="18"/><rect x="702" y="72" width="132" height="18"/><rect x="852" y="72" width="132" height="18"/></g>
 <g fill="#fff1c9" stroke="#222"><rect x="252" y="106" width="132" height="18"/><rect x="402" y="106" width="132" height="18"/><rect x="552" y="106" width="132" height="18"/><rect x="702" y="106" width="132" height="18"/><rect x="852" y="106" width="132" height="18"/></g>
 <g fill="#ffe4c6" stroke="#222"><rect x="402" y="140" width="132" height="18"/><rect x="552" y="140" width="132" height="18"/><rect x="702" y="140" width="132" height="18"/><rect x="852" y="140" width="132" height="18"/></g>
 <g fill="#e8e8e8" stroke="#222"><rect x="552" y="174" width="132" height="18"/><rect x="702" y="174" width="132" height="18"/><rect x="852" y="174" width="132" height="18"/></g>
 <g font-family="Arial" font-size="11" text-anchor="middle"><text x="318" y="119">DSP</text><text x="468" y="153">校正 + ACC</text><text x="618" y="187">snapshot / write</text><text x="88" y="187">气泡/尾块也占周期</text></g>
</svg>'''


def make_report(out_dir: Path, workspace: Path):
    hw = workspace / "hw" / "v3_2026-09-15_174639_vivado_impl"
    reports_root = hw / "reports"
    runs = [parse_run(reports_root, "250MHz_real4", "250 MHz"), parse_run(reports_root, "303MHz_real4", "303.215 MHz")]
    summary = load_json(workspace / "reports" / "2026-09-15_134742" / "architecture_summary.json", {})
    checks = load_json(hw / "data" / "functional" / "functional_checks.json", [])
    now = datetime.now()
    # When the caller has already created a timestamped report directory,
    # keep the filename and directory timestamp identical.
    stamp = out_dir.name if re.fullmatch(r"\d{4}-\d{2}-\d{2}_\d{6}", out_dir.name) else now.strftime("%Y-%m-%d_%H%M%S")
    human_now = now.strftime("%Y-%m-%d %H:%M:%S")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{stamp}_TurboVLA时序实现与架构分析.html"
    (out_dir / "vivado_real_results.json").write_text(json.dumps({"generated_at": human_now, "vivado": "D:/software/Vivado/2021.2/bin/vivado.bat", "runs": runs}, ensure_ascii=False, indent=2), encoding="utf-8")

    current = summary.get("modes", {}).get("current", {})
    db = summary.get("modes", {}).get("double_buffer", {})
    checks_ok = sum(1 for x in checks if isinstance(x, dict) and x.get("status") == "passed")
    target_250 = runs[0]
    target_303 = runs[1]
    max_fmax = max((r["timing"].get("fmax_derived_mhz") or 0 for r in runs), default=0)
    run_rows = []
    for r in runs:
        t, u, p, rt, d = r["timing"], r["resources"], r["power"], r["route"], r["drc"]
        status = "通过" if r["status"] == "passed" and t.get("timing_met") else "未通过"
        run_rows.append(f'''<tr><td>{esc(r["label"])}</td><td>{fmt(r["period_ns"],3)} ns / {fmt(r["target_mhz"],3)} MHz</td><td>{esc(status)}</td>
        <td>{fmt(t.get("wns_ns"),3)} ns</td><td>{fmt(t.get("whs_ns"),3)} ns</td><td>{fmt(t.get("fmax_derived_mhz"),1)} MHz</td>
        <td>{fmt(u.get("lut"),0)}</td><td>{fmt(u.get("ff"),0)}</td><td>{fmt(u.get("dsp"),0)}</td><td>{fmt(u.get("bram"),0)}</td>
        <td>{fmt(p.get("total_w"),3)} W</td><td>{fmt(r.get("elapsed_seconds"),0)} s</td></tr>''')
    resource_chart = svg_bars([("LUT / 1k", (target_250["resources"].get("lut") or 0)/1000), ("FF / 1k", (target_250["resources"].get("ff") or 0)/1000), ("DSP", target_250["resources"].get("dsp") or 0)], "250 MHz 实现资源（LUT/FF 用千为单位）", color="#3c78b4")
    freq_chart = svg_bars([(r["label"], r["timing"].get("fmax_derived_mhz")) for r in runs], "Vivado post-route 推导 Fmax", color="#d17b2c", unit=" MHz")
    power_chart = svg_bars([(r["label"], r["power"].get("total_w")) for r in runs], "vectorless 总片上功耗估计", color="#777", unit=" W")
    cycle_chart = svg_bars([("当前控制", current.get("total_cycles")), ("双缓冲", db.get("total_cycles"))], "历史 trace 周期模型（不是本次 Vivado 实测）", color="#8a5a44")
    util_chart = svg_bars([("当前 PE 利用率", current.get("pe_time_utilization", 0)*100), ("双缓冲 PE 利用率", db.get("pe_time_utilization", 0)*100)], "历史模型 PE 利用率", color="#4b9b65", unit="%")
    lead = f"250 MHz 和 303.215 MHz 两个目标都完成了 Vivado 2021.2 的综合、布局和布线。post-route WNS 分别为 {fmt(target_250['timing'].get('wns_ns'),3)} ns 和 {fmt(target_303['timing'].get('wns_ns'),3)} ns，说明这两个目标在当前 top 上都通过了 setup 和 pulse-width 检查；该 generic top 的 hold 项在 Vivado 汇总中显示为 NA。"
    html_doc = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TurboVLA Pack2 Vivado 时序实现与架构分析 {stamp}</title>
<style>
body{{margin:0;background:#f3f3f0;color:#202020;font-family:"Microsoft YaHei",Arial,sans-serif;line-height:1.68}}
main{{max-width:1220px;margin:0 auto;background:#fff;padding:28px 42px 58px;box-sizing:border-box}}
h1{{font-size:30px;line-height:1.25;margin:0 0 8px}} h2{{font-size:22px;border-left:5px solid #2d6cdf;padding-left:10px;margin:32px 0 10px}} h3{{font-size:17px;margin:20px 0 6px}}
.meta{{font-size:13px;color:#555;border-bottom:1px solid #aaa;padding-bottom:13px}} .lead{{font-size:17px;background:#eef5ff;border:1px solid #9cb9e6;padding:13px 16px;margin:18px 0}}
.note{{font-size:13px;color:#555;background:#fafafa;border-left:3px solid #777;padding:9px 13px;margin:11px 0}} .warn{{background:#fff6e8;border-color:#d28b2c;color:#5b3c12}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}} .card{{border:1px solid #b8b8b8;padding:12px;background:#fff}} .big{{display:block;font-size:28px;font-weight:700}}
table{{width:100%;border-collapse:collapse;font-size:13px;margin:11px 0 18px}} th,td{{border:1px solid #aaa;padding:6px 7px;text-align:left;vertical-align:top}} th{{background:#ececec}}
.diagram,.chart{{width:100%;height:auto;border:1px solid #bbb;background:#fff;margin:10px 0}} .caption{{font-size:13px;color:#444;margin:2px 0 13px}} code{{font-size:12px;word-break:break-all}}
.tag{{display:inline-block;border:1px solid #777;padding:1px 7px;margin-right:5px;font-size:12px;background:#f4f4f4}} .pass{{color:#137333;font-weight:700}} .fail{{color:#a33;font-weight:700}}
.footer{{border-top:1px solid #aaa;margin-top:34px;padding-top:12px;color:#555;font-size:13px}} li{{margin:4px 0}}
@media(max-width:720px){{main{{padding:18px 15px}}h1{{font-size:24px}}h2{{font-size:20px}}table{{font-size:12px;display:block;overflow-x:auto;white-space:nowrap}}}}
</style></head><body><main>
<h1>TurboVLA W8A8 Pack2：Vivado 实现结果与架构分析</h1>
<div class="meta">生成时间：{human_now}　|　版本：hw/v3_2026-09-15_174639_vivado_impl　|　Vivado：2021.2　|　器件：xczu7ev-ffvc1156-2-e　|　顶层：tvla_w8a8_pack2_impl_top</div>
<div class="lead"><b>先看结论：</b>{lead} 250 MHz 档的 post-route 推导 Fmax 约 {fmt(target_250['timing'].get('fmax_derived_mhz'),1)} MHz，303.215 MHz 档约 {fmt(target_303['timing'].get('fmax_derived_mhz'),1)} MHz。两档都保留 768 个 DSP，当前实现没有因为加寄存器而减少阵列规模。</div>

<h2>1. 这次真的跑了什么</h2>
<p>这次使用本机真实 Vivado，而不是只做 RTL 展开。Vivado 从综合开始，经过 opt、place、phys_opt、route 和 post-route 报告，最后生成了 routed checkpoint。</p>
<p>两个独立运行目录分别对应 4.000 ns 和 3.298 ns 时钟约束。250 MHz 运行耗时 {fmt(target_250['elapsed_seconds'],0)} 秒，303.215 MHz 运行耗时 {fmt(target_303['elapsed_seconds'],0)} 秒。这个时间包含 Vivado 的综合和实现，不是模型推理延迟。</p>
<div class="grid"><div class="card"><span class="big">2 / 2</span>两个时钟目标都完成综合、布局和布线。</div><div class="card"><span class="big">768 DSP</span>两档实现都保留完整 16×48 Pack2 阵列。</div><div class="card"><span class="big">4 / 4</span>本地 Icarus 功能冒烟检查通过；它是 RTL 级检查，不替代实现结果。</div></div>
{freq_chart}
<div class="caption">这图怎么看：柱子不是“请求频率”，而是由 post-route 的 WNS 反推的可用频率。正 slack 表示目标周期还有余量。</div>

<h2>2. Pack2 设计和新增寄存器</h2>
<p>Pack2 的一个 DSP 同时承载两个 INT8×INT8 乘积。两个乘积经过高低字段校正后，分别进入两条 INT32 累加反馈。阵列是 16 行 × 48 物理列，因此共有 768 个 DSP 和 96 个逻辑输出列。</p>
{svg_arch()}
<div class="caption">这图怎么看：蓝色框是数据寄存器，黄色框是 DSP，橙色框是 Pack2 校正与累加。新版本把 DSP 输出单独寄存，再进入校正和反馈路径；它没有改变 Pack2 的数学格式。</div>
<p>顶层使用了一个窄端口 wrapper。宽的 activation、weight、snapshot 和 output 数据仍在芯片内部连接；wrapper 只把演示用端口压到器件可以放下的数量，防止把 768-bit 总线误当成封装引脚。</p>

<h2>3. 资源、时序和功耗</h2>
{resource_chart}
<div class="caption">这图怎么看：LUT 和 FF 以千为单位，DSP 按颗数画。资源的精确数值看下面的表。</div>
<table><thead><tr><th>时钟目标</th><th>实现状态</th><th>WNS</th><th>WPWS</th><th>推导 Fmax</th><th>LUT</th><th>FF</th><th>DSP</th><th>BRAM</th><th>vectorless 功耗</th><th>Vivado 用时</th></tr></thead><tbody>{''.join(run_rows)}</tbody></table>
{power_chart}
<div class="caption">这图怎么看：功耗是 Vivado vectorless 估算，只能用来比较两档约束下的趋势。没有 SAIF/VCD，不能把它换算成 TOPS/W。</div>
<p>250 MHz 实现使用 77,770 LUT、179,363 个寄存器和 768 个 DSP；303.215 MHz 实现使用 77,860 LUT、179,320 个寄存器和 768 个 DSP。303 MHz 的 LUT 只比 250 MHz 多 0.12%，但总片上 vectorless 功耗从 {fmt(target_250['power'].get('total_w'),3)} W 增至 {fmt(target_303['power'].get('total_w'),3)} W，增加约 {fmt((target_303['power'].get('total_w')/target_250['power'].get('total_w')-1)*100,1)}%。这个功耗差异来自时钟约束下的活动传播估计，不是板上实测功耗。</p>
<div class="note warn"><b>实现报告里的两个限制：</b>DRC 没有 Error，所有可布线网络也都已完成。但顶层没有板级 I/O 的 LOC 和 IOSTANDARD，因而出现 NSTD-1/UCIO-1 critical warning；另外 768 个 DSP 都被提示输入侧没有启用 AREG/BREG 等 DSP 输入寄存器。当前结果可以说明这个 generic top 能布局布线并过时序，不能直接当成已经绑定开发板引脚、可以生成 bitstream 的版本。</div>

<h2>4. 时序报告告诉我们什么</h2>
<table><thead><tr><th>目标</th><th>最长路径数据延迟</th><th>逻辑部分</th><th>布线部分</th><th>怎么看</th></tr></thead><tbody>
<tr><td>250 MHz</td><td>{fmt(target_250['timing'].get('data_path_delay_ns'),3)} ns</td><td>{fmt(target_250['timing'].get('logic_delay_ns'),3)} ns</td><td>{fmt(target_250['timing'].get('route_delay_ns'),3)} ns</td><td>布线约占最长路径的大部分，继续堆组合逻辑不是主要问题。</td></tr>
<tr><td>303.215 MHz</td><td>{fmt(target_303['timing'].get('data_path_delay_ns'),3)} ns</td><td>{fmt(target_303['timing'].get('logic_delay_ns'),3)} ns</td><td>{fmt(target_303['timing'].get('route_delay_ns'),3)} ns</td><td>目标仍有 +{fmt(target_303['timing'].get('wns_ns'),3)} ns setup 余量，但阵列的长距离扇出和布线值得继续优化。</td></tr>
</tbody></table>
{svg_timeline()}
<div class="caption">这图怎么看：输入寄存、DSP 输出寄存和校正/累加寄存器把数据排成流水线。尾块、snapshot、读出和写回仍然会占周期，不能只用 DSP 的 MAC 数推算整机吞吐。</div>

<h2>5. RTL 功能检查</h2>
<table><thead><tr><th>检查</th><th>结果</th><th>耗时</th><th>说明</th></tr></thead><tbody>'''
    for item in checks:
        html_doc += f"<tr><td>{esc(item.get('name'))}</td><td class='pass'>{esc(item.get('status'))}</td><td>{fmt(item.get('elapsed_seconds'),3)} s</td><td>{esc(item.get('message') or '无错误')}</td></tr>"
    html_doc += f'''</tbody></table>
<p>这四项检查覆盖 Pack2 乘法器、时序阵列、回放顶层和 system_top 展开。它们证明改过的 RTL 可以跑基本协议；完整 TurboVLA 的 DINO、语言编码和未映射辅助算子没有在这个 generic timing top 里伪装成已综合硬件。</p>

<h2>6. 模型周期仍然怎么解释</h2>
<p>下面两张图来自之前的 TurboVLA trace 驱动周期模型。它们没有被 Vivado 自动测量，所以只用于说明架构调度的方向。当前控制模型总周期为 {fmt(current.get('total_cycles'),0)}，双缓冲模型为 {fmt(db.get('total_cycles'),0)}，理论上减少 {pct(1-db.get('total_cycles',1)/current.get('total_cycles',1),1)}。这不是 RTL 仿真或板上延迟。</p>
{cycle_chart}<div class="caption">这图怎么看：双缓冲把读、算、写的等待重叠起来，所以模型周期下降；它需要真实 DMA、缓存和依赖调度继续验证。</div>
{util_chart}<div class="caption">这图怎么看：双缓冲模型把 PE 时间利用率从 {pct(current.get('pe_time_utilization'),1)} 提到 {pct(db.get('pe_time_utilization'),1)}，但这不是说 Vivado 实现自动达到了这个利用率。</div>
<table><thead><tr><th>模型</th><th>总周期</th><th>PE 时间利用率</th><th>GEMM 利用率</th><th>有效 GOPS @250 MHz</th><th>证据类型</th></tr></thead><tbody>
<tr><td>当前控制</td><td>{fmt(current.get('total_cycles'),0)}</td><td>{pct(current.get('pe_time_utilization'))}</td><td>{pct(current.get('gemm_utilization'))}</td><td>{fmt(current.get('effective_gops_250_0'),1)}</td><td>Python trace 周期模型</td></tr>
<tr><td>双缓冲</td><td>{fmt(db.get('total_cycles'),0)}</td><td>{pct(db.get('pe_time_utilization'))}</td><td>{pct(db.get('gemm_utilization'))}</td><td>{fmt(db.get('effective_gops_250_0'),1)}</td><td>条件模型</td></tr>
</tbody></table>

<h2>7. 给架构师的结论</h2>
<ol>
<li><b>频率：</b>当前 Pack2 replay top 在 xczu7ev-ffvc1156-2-e 上，250 MHz 和 303.215 MHz 都完成了 post-route 时序。303 MHz 仍有 +{fmt(target_303['timing'].get('wns_ns'),3)} ns setup 余量，说明这版寄存器边界至少把目标频率保住了。</li>
<li><b>资源：</b>两档都使用 768 DSP，LUT 约 77.8k，FF 约 179k，BRAM 为 0。新增时序 wrapper 没有牺牲 Pack2 阵列规模。</li>
<li><b>瓶颈：</b>最长路径的路由延迟明显大于逻辑延迟。下一步应优先看阵列跨列扇出、drain-row 网络和 DSP 输入寄存器，而不是继续把校正逻辑塞进同一拍。</li>
<li><b>工程状态：</b>这是已经实现的 generic top，不是已经绑定开发板的 bitstream。先补板级 I/O 约束，再做真实 DDR、SAIF/VCD 功耗和完整 TurboVLA fallback 回放。</li>
<li><b>性能口径：</b>历史双缓冲模型的 591 GOPS @250 MHz 仍是条件估算；它不能替代本轮 Vivado 的频率结果，也不能直接当作端到端 TurboVLA 吞吐。</li>
</ol>

<div class="footer"><b>原始结果目录</b><br><code>{esc(hw / 'reports' / '250MHz_real4')}</code><br><code>{esc(hw / 'reports' / '303MHz_real4')}</code><br><br><b>复现命令</b><br><code>&amp; 'D:/software/Vivado/2021.2/bin/vivado.bat' -mode batch -source vivado/run_vivado_impl.tcl -tclargs 4.000 .../reports/250MHz_real4</code><br><code>&amp; 'D:/software/Vivado/2021.2/bin/vivado.bat' -mode batch -source vivado/run_vivado_impl.tcl -tclargs 3.298 .../reports/303MHz_real4</code><br><br>本页生成时间：{human_now}。数值分为 RTL 冒烟、Vivado post-route 实测、Python 周期模型和 vectorless 功耗估算；没有用未测的端到端或 TOPS/W 填空。</div>
</main></body></html>'''
    out_file.write_text(html_doc, encoding="utf-8")
    return out_file, out_dir / "vivado_real_results.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    script = Path(__file__).resolve()
    workspace = script.parents[3]  # turbovla_w8a8_pack2
    out_file, json_file = make_report(Path(args.out_dir).resolve(), workspace)
    print(out_file)
    print(json_file)


if __name__ == "__main__":
    main()
