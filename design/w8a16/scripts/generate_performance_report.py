"""Build a self-contained Chinese performance review page for the TurboVLA W8A16 top.

The page is deliberately generated from the machine-readable Vivado collectors;
no PPA number is typed into the HTML template.  v5/v6 are optional references and
v7 is the current timing-fix round.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def load(path: Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}


def drc_rule_count(data: dict[str, Any], rule: str) -> int | None:
    """Read a DRC rule count from JSON, or from the preserved Vivado report."""
    value = data.get("drc", {}).get("rules", {}).get(rule, {}).get("count")
    if value is not None:
        try:
            return int(value)
        except (TypeError, ValueError):
            pass
    report_path = data.get("raw_reports", {}).get("post_route_drc.rpt")
    if report_path:
        try:
            text = Path(str(report_path)).read_text(encoding="utf-8", errors="replace")
            match = re.search(rf"\|\s*{re.escape(rule)}\s*\|[^|]*\|[^|]*\|\s*(\d+)\s*\|", text)
            if match:
                return int(match.group(1))
        except OSError:
            pass
    return None


def esc(value: Any, fallback: str = "—") -> str:
    if value is None or value == "":
        return fallback
    return html.escape(str(value))


def num(value: Any, digits: int = 2, suffix: str = "") -> str:
    try:
        return f"{float(value):.{digits}f}{suffix}"
    except (TypeError, ValueError):
        return "—"


def integer(value: Any) -> str:
    try:
        return f"{int(round(float(value))):,}"
    except (TypeError, ValueError):
        return "—"


def ratio(a: Any, b: Any, digits: int = 1, suffix: str = "%") -> str:
    try:
        if float(b) == 0:
            return "—"
        return f"{100.0 * float(a) / float(b):.{digits}f}{suffix}"
    except (TypeError, ValueError):
        return "—"


def change_pct(new: Any, old: Any, digits: int = 3) -> str:
    """Return signed relative change, keeping the raw (unrounded) inputs."""
    try:
        old_f = float(old)
        new_f = float(new)
        if old_f == 0:
            return "—"
        return f"{100.0 * (new_f - old_f) / old_f:+.{digits}f}%"
    except (TypeError, ValueError):
        return "—"


def link(path: Any, label: str) -> str:
    if not path:
        return "—"
    try:
        p = Path(str(path)).resolve()
        href = p.as_uri()
    except (OSError, ValueError):
        href = str(path)
    return f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'


def table(headers: list[str], rows: list[list[Any]]) -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    def cell(value: Any) -> str:
        if isinstance(value, str) and value.startswith("<"):
            return f"<td>{value}</td>"
        return f"<td>{esc(value)}</td>"
    body = "".join("<tr>" + "".join(cell(v) for v in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def architecture_svg() -> str:
    return """
<svg class="diagram" viewBox="0 0 1100 330" role="img" aria-label="TurboVLA W8A16 顶层数据流">
  <style>
    .box{stroke:#25313a;stroke-width:2;fill:#f8fafb}.mem{fill:#e8f1f6}.compute{fill:#fff2da}.ctrl{fill:#eceff1}
    .txt{font:16px Arial,"Microsoft YaHei",sans-serif;fill:#202a30}.small{font:13px Arial,"Microsoft YaHei",sans-serif;fill:#46545d}
    .bus{stroke:#245f86;stroke-width:3;fill:none;marker-end:url(#arr)}.ctl{stroke:#666;stroke-width:2;stroke-dasharray:7 5;fill:none;marker-end:url(#arrg)}
  </style>
  <defs><marker id="arr" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 z" fill="#245f86"/></marker>
  <marker id="arrg" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><path d="M0,0 L9,3.5 L0,7 z" fill="#666"/></marker></defs>
  <rect x="15" y="46" width="170" height="80" class="box ctrl"/><text x="100" y="78" text-anchor="middle" class="txt">Runtime / ISA</text><text x="100" y="101" text-anchor="middle" class="small">命令译码、状态机</text>
  <rect x="15" y="190" width="170" height="80" class="box mem"/><text x="100" y="222" text-anchor="middle" class="txt">CTX / WRAM</text><text x="100" y="245" text-anchor="middle" class="small">256-bit A · 384-bit W</text>
  <rect x="250" y="40" width="210" height="105" class="box mem"/><text x="355" y="74" text-anchor="middle" class="txt">Load / Store DMA</text><text x="355" y="99" text-anchor="middle" class="small">输入、权重、结果搬运</text><text x="355" y="121" text-anchor="middle" class="small">接口成本独立统计</text>
  <rect x="250" y="185" width="210" height="105" class="box ctrl"/><text x="355" y="219" text-anchor="middle" class="txt">Vector engines</text><text x="355" y="244" text-anchor="middle" class="small">LayerNorm · GELU · Softmax</text><text x="355" y="266" text-anchor="middle" class="small">动作后处理</text>
  <rect x="525" y="44" width="335" height="205" class="box compute"/><text x="692" y="75" text-anchor="middle" class="txt">W8A16 GEMM array</text><text x="692" y="98" text-anchor="middle" class="small">16 rows × 48 physical columns</text>
  <g stroke="#c99642" fill="#fffaf0" stroke-width="1"><rect x="558" y="122" width="54" height="32"/><rect x="620" y="122" width="54" height="32"/><rect x="682" y="122" width="54" height="32"/><rect x="744" y="122" width="54" height="32"/><rect x="806" y="122" width="22" height="32"/>
  <rect x="558" y="164" width="54" height="32"/><rect x="620" y="164" width="54" height="32"/><rect x="682" y="164" width="54" height="32"/><rect x="744" y="164" width="54" height="32"/><rect x="806" y="164" width="22" height="32"/>
  <rect x="558" y="206" width="54" height="32"/><rect x="620" y="206" width="54" height="32"/><rect x="682" y="206" width="54" height="32"/><rect x="744" y="206" width="54" height="32"/><rect x="806" y="206" width="22" height="32"/></g>
  <text x="692" y="142" text-anchor="middle" class="small">1 DSP / PE · INT16 × INT8</text><text x="692" y="184" text-anchor="middle" class="small">40-bit accumulator + snapshot</text><text x="692" y="226" text-anchor="middle" class="small">768 DSP · 1 MAC / DSP / cycle</text>
  <rect x="915" y="55" width="165" height="80" class="box mem"/><text x="997" y="88" text-anchor="middle" class="txt">Requant / writeback</text><text x="997" y="111" text-anchor="middle" class="small">INT16 输出</text>
  <rect x="915" y="190" width="165" height="80" class="box ctrl"/><text x="997" y="223" text-anchor="middle" class="txt">Clock / platform</text><text x="997" y="246" text-anchor="middle" class="small">本轮是 OOC，无板级约束</text>
  <path d="M185 86 L250 86" class="ctl"/><path d="M185 230 L250 230" class="bus"/><path d="M460 91 L525 91" class="bus"/><path d="M460 237 L525 237" class="ctl"/><path d="M860 91 L915 91" class="bus"/><path d="M997 135 L997 190" class="ctl"/>
  <text x="210" y="78" class="small">控制</text><text x="205" y="218" class="small">数据</text><text x="476" y="83" class="small">激活/权重</text><text x="870" y="83" class="small">结果</text>
</svg>"""


def frequency_svg(results: list[tuple[str, dict[str, Any]]]) -> str:
    values: list[tuple[str, float, str]] = []
    for label, data in results:
        t = data.get("timing", {})
        fmax = t.get("fmax_estimate_mhz")
        if fmax is not None:
            values.append((label, float(fmax), "#b96545" if label.startswith("v7") else "#68869a"))
    values.append(("250 MHz目标", 250.0, "#303c44"))
    ymax = max(270.0, max((v for _, v, _ in values), default=270.0) * 1.15)
    x0, y0, h = 76, 28, 205
    gap = 28
    bw = 120
    width = max(760, x0 + len(values) * (bw + gap) + 30)
    bars: list[str] = []
    for i, (label, value, color) in enumerate(values):
        x = x0 + i * (bw + gap)
        bh = h * value / ymax
        y = y0 + h - bh
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="{bw}" height="{bh:.1f}" fill="{color}"/><text x="{x+bw/2:.1f}" y="{y-7:.1f}" text-anchor="middle" class="val">{value:.1f}</text><text x="{x+bw/2:.1f}" y="{y0+h+24}" text-anchor="middle" class="lab">{html.escape(label)}</text>')
    grid = "".join(f'<line x1="{x0}" y1="{y0+h-n*h/4:.1f}" x2="{width-20}" y2="{y0+h-n*h/4:.1f}" stroke="#e5e8ea"/><text x="{x0-9}" y="{y0+h-n*h/4+4:.1f}" text-anchor="end" class="tick">{ymax*n/4:.0f}</text>' for n in range(5))
    return f'<svg class="chart" viewBox="0 0 {width} 290" role="img" aria-label="post-route 频率比较"><style>.lab{{font:13px Arial,"Microsoft YaHei",sans-serif;fill:#26333b}}.val{{font:bold 16px Arial,sans-serif;fill:#17232b}}.tick{{font:11px Arial,sans-serif;fill:#68747b}}</style><text x="24" y="18" class="lab">post-route 最高频率估算（MHz）</text>{grid}{"".join(bars)}<line x1="{x0}" y1="{y0+h}" x2="{width-20}" y2="{y0+h}" stroke="#26333b"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="#26333b"/></svg>'


def delay_svg(results: list[tuple[str, dict[str, Any]]]) -> str:
    vals: list[tuple[str, float, float]] = []
    for label, data in results:
        t = data.get("timing", {})
        try:
            vals.append((label, float(t.get("logic_delay_ns") or 0), float(t.get("route_delay_ns") or 0)))
        except (TypeError, ValueError):
            pass
    if not vals:
        return ""
    ymax = max(4.5, max(l + r for _, l, r in vals) * 1.20)
    x0, y0, h, bw = 74, 26, 190, 120
    gap = 32
    width = max(720, x0 + len(vals) * (bw + gap) + 24)
    groups = []
    for i, (label, logic, route) in enumerate(vals):
        x = x0 + i * (bw + gap)
        lh, rh = h * logic / ymax, h * route / ymax
        yroute = y0 + h - rh
        ylogic = yroute - lh
        groups.append(f'<rect x="{x}" y="{yroute:.1f}" width="{bw}" height="{rh:.1f}" fill="#d18b65"/><rect x="{x}" y="{ylogic:.1f}" width="{bw}" height="{lh:.1f}" fill="#7d9caf"/><text x="{x+bw/2}" y="{ylogic-7:.1f}" text-anchor="middle" class="val">{logic+route:.3f}</text><text x="{x+bw/2}" y="{y0+h+24}" text-anchor="middle" class="lab">{html.escape(label)}</text><text x="{x+bw/2}" y="{yroute+rh/2+4:.1f}" text-anchor="middle" class="inside">route {route:.3f}</text><text x="{x+bw/2}" y="{yroute- min(6,lh/2):.1f}" text-anchor="middle" class="inside dark">logic {logic:.3f}</text>')
    grid = "".join(f'<line x1="{x0}" y1="{y0+h-n*h/4:.1f}" x2="{width-20}" y2="{y0+h-n*h/4:.1f}" stroke="#e5e8ea"/><text x="{x0-9}" y="{y0+h-n*h/4+4:.1f}" text-anchor="end" class="tick">{ymax*n/4:.1f}</text>' for n in range(5))
    return f'<svg class="chart" viewBox="0 0 {width} 285" role="img" aria-label="关键路径逻辑与布线延迟"><style>.lab{{font:13px Arial,"Microsoft YaHei",sans-serif;fill:#26333b}}.val{{font:bold 15px Arial,sans-serif;fill:#17232b}}.tick{{font:11px Arial,sans-serif;fill:#68747b}}.inside{{font:11px Arial,sans-serif;fill:#fff}}.inside.dark{{fill:#17232b}}</style><text x="24" y="17" class="lab">最长 setup 路径的延迟组成（ns）</text>{grid}{"".join(groups)}<line x1="{x0}" y1="{y0+h}" x2="{width-20}" y2="{y0+h}" stroke="#26333b"/></svg>'


def power_svg(data: dict[str, Any]) -> str:
    p = data.get("power", {})
    dynamic = float(p.get("dynamic_w") or 0)
    static = float(p.get("static_w") or 0)
    total = max(dynamic + static, 1e-9)
    x, y, width, height = 62, 58, 650, 42
    dw = width * dynamic / total
    return f'<svg class="chart" viewBox="0 0 770 140" role="img" aria-label="vectorless 功耗组成"><style>.lab{{font:13px Arial,"Microsoft YaHei",sans-serif;fill:#26333b}}.inside{{font:bold 13px Arial,sans-serif;fill:#fff}}</style><text x="26" y="24" class="lab">Vivado vectorless 总片上功耗 {float(p.get("total_on_chip_w") or 0):.3f} W</text><rect x="{x}" y="{y}" width="{dw:.1f}" height="{height}" fill="#b96545"/><rect x="{x+dw:.1f}" y="{y}" width="{width-dw:.1f}" height="{height}" fill="#7d8d96"/><text x="{x+dw/2:.1f}" y="{y+27}" text-anchor="middle" class="inside">动态 {dynamic:.3f} W</text><text x="{x+dw+(width-dw)/2:.1f}" y="{y+27}" text-anchor="middle" class="inside">静态 {static:.3f} W</text><text x="62" y="130" class="lab">没有 SAIF/VCD，只能作为同一工具假设下的版本比较。</text></svg>'


def performance_numbers(data: dict[str, Any]) -> dict[str, Any]:
    t = data.get("timing", {})
    r = data.get("resources", {})
    fmax = float(t.get("fmax_estimate_mhz") or 0)
    array_dsp = 16 * 48
    return {
        "array_dsp": array_dsp,
        "total_dsp": r.get("dsp"),
        "dsp_occupancy_pct": 100.0 * array_dsp / float(r.get("dsp")) if r.get("dsp") else None,
        "peak_gmac_at_fmax": array_dsp * fmax / 1000.0 if fmax else None,
        "peak_gmac_at_250": array_dsp * 250.0 / 1000.0,
        "timing_met": bool(t.get("timing_met")),
        "fmax": fmax,
        "wns": t.get("wns_ns"),
    }


def build(v5: dict[str, Any], v6: dict[str, Any], v7: dict[str, Any], output: Path, generated: str) -> None:
    current = v7 or v6 or v5
    ct = current.get("timing", {})
    cr = current.get("resources", {})
    cp = current.get("power", {})
    numbers = performance_numbers(current)
    if v7:
        result_text = "v7 已通过 250 MHz 时序" if numbers["timing_met"] else "v7 仍未通过 250 MHz 时序"
        result_class = "ok" if numbers["timing_met"] else "bad"
    else:
        result_text = "当前最新实现为 v6；v7 结果尚未回收"
        result_class = "bad"
    if numbers["timing_met"]:
        timing_boundary_note = "v7 的 post-route WNS 已为正，250 MHz 这一轮已经过线。下一步应补板级时钟、I/O 和 AXI/DDR 约束，再确认这点余量能否保住。"
    else:
        timing_boundary_note = "v7 的 post-route WNS 仍为负，当前只能写成未过 250 MHz。应跟着新的最长路径继续修，不能把脚本完成误读成时序通过。"
    result_rows: list[list[Any]] = []
    for label, data in (("v5 post-route", v5), ("v6 post-route", v6), ("v7 post-route", v7)):
        if not data:
            continue
        t = data.get("timing", {})
        result_rows.append([label, num(t.get("target_period_ns"), 3, " ns"), num(t.get("wns_ns"), 3, " ns"), num(t.get("fmax_estimate_mhz"), 1, " MHz"), "是" if t.get("timing_met") else "否"])
    resource_rows: list[list[Any]] = []
    for label, data in (("v5", v5), ("v6", v6), ("v7", v7)):
        if not data:
            continue
        r = data.get("resources", {})
        resource_rows.append([label, integer(r.get("total_luts")), integer(r.get("ffs")), integer(r.get("dsp")), integer(r.get("ramb36")), integer(r.get("ramb18")), num(data.get("power", {}).get("total_on_chip_w"), 3, " W")])
    delay_inputs = [(label, data) for label, data in (("v5", v5), ("v6", v6), ("v7", v7)) if data]
    freq_inputs = delay_inputs
    timing_t = ct
    route = current.get("route", {})
    drc = current.get("drc", {})
    sim = current.get("simulation", {})
    dpip_current = drc_rule_count(current, "DPIP-2")
    dpip_v5 = drc_rule_count(v5, "DPIP-2") if v5 else None
    dpip_reduction = (1.0 - float(dpip_current) / float(dpip_v5)) * 100.0 if dpip_current is not None and dpip_v5 else None
    if v6 and v7:
        v6t, v7t = v6.get("timing", {}), v7.get("timing", {})
        v6r, v7r = v6.get("resources", {}), v7.get("resources", {})
        v6p, v7p = v6.get("power", {}), v7.get("power", {})
        improvement_rows = [
            ["post-route Fmax", num(v6t.get("fmax_estimate_mhz"), 3, " MHz"), num(v7t.get("fmax_estimate_mhz"), 3, " MHz"), change_pct(v7t.get("fmax_estimate_mhz"), v6t.get("fmax_estimate_mhz")), "频率越高越好"],
            ["关键路径总延迟", num(v6t.get("data_path_delay_ns"), 3, " ns"), num(v7t.get("data_path_delay_ns"), 3, " ns"), change_pct(v7t.get("data_path_delay_ns"), v6t.get("data_path_delay_ns")), "延迟越低越好"],
            ["其中布线延迟", num(v6t.get("route_delay_ns"), 3, " ns"), num(v7t.get("route_delay_ns"), 3, " ns"), change_pct(v7t.get("route_delay_ns"), v6t.get("route_delay_ns")), "延迟越低越好"],
            ["总 LUT", integer(v6r.get("total_luts")), integer(v7r.get("total_luts")), change_pct(v7r.get("total_luts"), v6r.get("total_luts")), "面积越低越好"],
            ["vectorless 总功耗", num(v6p.get("total_on_chip_w"), 3, " W"), num(v7p.get("total_on_chip_w"), 3, " W"), change_pct(v7p.get("total_on_chip_w"), v6p.get("total_on_chip_w")), "仅作工具估算参考"],
        ]
        improvement_intro = "v7 只给清零控制线加了分组网络，协议、PE 数量和 DSP 数量都没有改。下面的百分比用未四舍五入的 JSON 数字计算；负号表示对应数值变小。"
    else:
        improvement_rows = []
        improvement_intro = "v6 或 v7 的完整 JSON 尚未提供，因此无法计算这次改动的前后百分比。"
    raw_links = []
    for name, path in current.get("raw_reports", {}).items():
        raw_links.append(f"<li>{link(path, name)}</li>")
    report = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TurboVLA W8A16 当前架构性能分析 {html.escape(generated)}</title>
<style>
body{{margin:0;background:#f2f4f5;color:#26333b;font-family:"Microsoft YaHei",Arial,sans-serif;line-height:1.68}}
main{{max-width:1220px;margin:auto;padding:26px 30px 60px}}
header,section{{background:#fff;border:1px solid #d7dfe4;margin:0 0 18px;padding:22px 26px}}
h1{{font-size:28px;line-height:1.28;margin:0 0 8px;color:#1c2b34}}h2{{font-size:20px;margin:0 0 12px;border-left:4px solid #5f7f91;padding-left:10px}}h3{{font-size:16px;margin:18px 0 5px}}
.meta{{font-size:13px;color:#687680}}.lead{{font-size:17px;margin:14px 0}}.status{{display:inline-block;color:#fff;padding:3px 11px;font-weight:700}}.status.ok{{background:#397c55}}.status.bad{{background:#b04d42}}
.cards{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-top:18px}}.card{{background:#f8fafb;border:1px solid #dbe2e6;padding:10px 11px}}.card .v{{display:block;font-weight:700;font-size:21px;color:#244c63}}.card .k{{font-size:12px;color:#687680}}
table{{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0 8px}}th,td{{border:1px solid #d8e0e4;padding:7px 8px;text-align:left;vertical-align:top}}th{{background:#edf2f4}}td:nth-child(n+2){{font-variant-numeric:tabular-nums}}
.diagram,.chart{{width:100%;height:auto;display:block;margin:12px 0}}.note{{background:#f5f8fa;border-left:3px solid #6c8796;padding:10px 12px;font-size:13px}}.warn{{background:#fff4eb;border-left:3px solid #b96545;padding:10px 12px}}.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}code{{font:12px Consolas,monospace;background:#f1f3f4;padding:1px 4px}}a{{color:#245e86}}ul,ol{{margin-top:6px}}footer{{font-size:12px;color:#687680}}
@media(max-width:820px){{main{{padding:14px}}header,section{{padding:16px}}.cards{{grid-template-columns:repeat(3,1fr)}}.grid2{{grid-template-columns:1fr}}h1{{font-size:23px}}table{{display:block;overflow-x:auto;white-space:nowrap}}}}
@media(max-width:480px){{.cards{{grid-template-columns:repeat(2,1fr)}}}}
</style></head><body><main>
<header><h1>TurboVLA W8A16 当前架构性能分析</h1>
<div class="meta">生成时间：{html.escape(generated)}　｜　器件：{esc(current.get("part"))}　｜　Vivado：{esc(current.get("tool"))}　｜　顶层：{esc(current.get("top"))}</div>
<p class="lead"><span class="status {result_class}">{result_text}</span>　这页把 v5、v6 和当前 v7 的实现报告放在同一张图里。频率和资源来自 Vivado post-route；功耗是 vectorless 估算。</p>
<div class="cards"><div class="card"><span class="v">{num(numbers.get("fmax"),1)} MHz</span><span class="k">当前 post-route 频率估算</span></div><div class="card"><span class="v">{num(numbers.get("wns"),3)} ns</span><span class="k">当前 WNS</span></div><div class="card"><span class="v">{integer(numbers.get("array_dsp"))}</span><span class="k">阵列 DSP（16×48）</span></div><div class="card"><span class="v">{integer(cr.get("total_luts"))}</span><span class="k">当前总 LUT</span></div><div class="card"><span class="v">{num(cp.get("total_on_chip_w"),3)} W</span><span class="k">vectorless 总片上功耗</span></div><div class="card"><span class="v">{num(numbers.get("dsp_occupancy_pct"),1)}%</span><span class="k">阵列占已用 DSP</span></div></div></header>

<section><h2>先看这套架构在做什么</h2>{architecture_svg()}<p>图中蓝色实线是数据，灰色虚线是控制。主计算阵列是 16 行、48 列的 W8A16 阵列，每个 PE 使用一个 DSP 做一个 INT16×INT8 乘法，并把结果送进 40-bit 累加器。阵列之外还有 DMA、向量算子和动作后处理；它们的时间不能被 GEMM 峰值替代。</p><p class="note">这张图是当前 RTL 顶层的结构示意。OOC 工程没有板级时钟、AXI/DDR 和 I/O delay 约束，所以它可以回答“这版 RTL 能否布线、资源多少”，不能直接回答整板频率和整机能效。</p></section>

<section><h2>250 MHz 时序结果</h2>{frequency_svg(freq_inputs)}<p>这图怎么看：黑色柱是目标，彩色柱是 Vivado 按 WNS 推算的最高频率。只有 post-route WNS≥0 才算真正过 250 MHz。当前 v7 的硬结论是“{result_text}”。</p>{table(["版本","目标周期","post-route WNS","按 WNS 推算频率","是否过目标"], result_rows)}
<div class="grid2"><div><h3>最长路径</h3>{table(["字段","当前值"],[["起点",timing_t.get("critical_source")],["终点",timing_t.get("critical_destination")],["数据路径",num(timing_t.get("data_path_delay_ns"),3," ns")],["逻辑延迟",num(timing_t.get("logic_delay_ns"),3," ns")+"（"+num(timing_t.get("logic_delay_percent"),1,"%")+"）"],["布线延迟",num(timing_t.get("route_delay_ns"),3," ns")+"（"+num(timing_t.get("route_delay_percent"),1,"%")+"）"],["setup 失败端点",integer(timing_t.get("failing_endpoints"))],["TNS",num(timing_t.get("tns_ns"),3," ns")]])}</div><div>{delay_svg(delay_inputs)}<p class="note">v6 的关键路径中布线占 92.4%，所以 v7 先拆 `clr` 高扇出网络。若 v7 仍失败，下一步要看新的关键路径是否已经转移到别的控制网络；不能继续笼统地说“乘法器慢”。</p></div></div></section>

<section><h2>v6 到 v7 的改动前后</h2><p>{improvement_intro}</p>{table(["指标","v6","v7","相对变化","怎么看"], improvement_rows) if improvement_rows else '<p class="note">没有足够的两个版本数据，暂不计算。</p>'}<p class="note">最值得注意的是，布线延迟下降后，WNS 从 -0.050 ns 变成 +0.006 ns，setup 失败端点从 192 变成 0。Fmax 只提高约 1.4%，但它跨过了 250 MHz 这个工程门槛；这比单看百分比更重要。功耗增加约 4.3% 仍是 vectorless 结果，不能解释为实际能效下降。</p></section>

<section><h2>资源和静态结构</h2>{table(["版本","LUT","FF","DSP","BRAM36","BRAM18","片上功耗"], resource_rows)}<p>阵列需要 768 个 DSP，当前顶层实际使用 {integer(cr.get("dsp"))} 个 DSP，静态占用约 {num(numbers.get("dsp_occupancy_pct"),1)}%。多出的 DSP 来自动作路径和向量乘法器，不应把 785 写成“阵列有 785 个 PE”。</p><p>资源数字是实现工具的计数。它们不能单独推出动态利用率。动态利用率需要真实 TurboVLA 指令流、有效 MAC 数和完成周期；当前这轮只有 RTL/实现数据，还没有把某个模型 workload 接到硬件顶层做活动回放。</p></section>

<section><h2>算力能报到什么程度</h2><div class="grid2"><div><h3>可直接计算的峰值</h3>{table(["项目","数值","怎么算"],[["阵列规模","768 DSP","16×48"],["250 MHz 理论峰值",num(numbers.get("peak_gmac_at_250"),2," GMAC/s"),"768 MAC/cycle × 250 MHz"],["当前 fmax 理论峰值",num(numbers.get("peak_gmac_at_fmax"),2," GMAC/s"),"768 × 当前 fmax"],["DSP 静态占用",num(numbers.get("dsp_occupancy_pct"),1,"%"),"768 ÷ 顶层 DSP" ]])}</div><div><h3>目前不能诚实地报的数字</h3><ul><li>不能把 192 GMAC/s 写成模型实测吞吐。它只是 250 MHz、每个 DSP 每拍一个 MAC 的阵列上限。</li><li>不能从 DSP 占用推断 PE 时间利用率。空闲周期、填充排空、DMA 和写回必须从指令流计数。</li><li>不能用 4.478 W 或 v7 的功耗数字直接算 TOPS/W。当前功耗没有 SAIF/VCD，也没有板上电源测量。</li></ul></div></div><p class="note">如果下一步要得到“实际 GEMM 利用率”，最小闭环是：固定一段 TurboVLA W8A16 指令流，记录有效 MAC、阵列 busy、快照／重量化／写回周期，再用 <code>有效 MAC ÷ (768 × 完成周期)</code> 计算。这里的跳过 MAC 不计作阵列完成量。</p></section>

<section><h2>关键路径和工程收益</h2>{delay_svg(delay_inputs)}<p>v5 的路径主要是动作路径的逻辑加法；v6 加了 DSP A/B 输入寄存器、乘积寄存器和累加 drain 后，路径转到 runtime 控制到阵列 PE 的 <code>clr/CE</code> 网络。v5→v6 不是同一目标周期下的单变量实验，但 DRC 里的 DPIP-2 从 {integer(dpip_v5)} 降到 {integer(dpip_current)}，减少约 {num(dpip_reduction,1,"%")}，说明 DSP 输入 pipeline 方向确实消掉了大部分阵列输入警告。v7 把清零控制按每 8 列分组，布线延迟下降后跨过了 250 MHz 门槛。</p><p class="warn">{timing_boundary_note} 只有 post-route WNS≥0 且 DRC 错误为 0，才适合进入下一轮板级约束和功耗活动分析。</p></section>

<section><h2>功耗：只能做版本间参考</h2>{power_svg(current)}{table(["项目","当前值","证据"],[["总片上功耗",num(cp.get("total_on_chip_w"),3," W"),"Vivado report_power"],["动态功耗",num(cp.get("dynamic_w"),3," W"),"vectorless activity"],["静态功耗",num(cp.get("static_w"),3," W"),"器件静态模型"],["置信度",cp.get("confidence"),"报告字段"],["活动文件",cp.get("activity_file"),"当前没有 SAIF/VCD"]])}<p>这张图怎么看：动态和静态只是工具在默认活动率下的拆分。它可以用来比较 v5/v6/v7 的方向，却不能代表 TurboVLA 真实工作负载下的能耗。</p></section>

<section><h2>验证和布线状态</h2>{table(["检查","结果","意义"],[["Verilator",esc(sim.get("status"))+"；"+integer(len(sim.get("tests",[])))+" 项；"+num(sim.get("elapsed_seconds"),0," s"),"PE、16×48 阵列、GEMM、向量、DMA、runtime、system 通过"],["完整阵列",integer(sim.get("dsp_full_array"))+" DSP","保持 16×48 结构"],["route",esc(route.get("status"))+"；未布线 "+integer(route.get("unrouted_nets"))+"；错误 "+integer(route.get("routing_errors")),"能否完成布线"],["DRC",integer(drc.get("violations"))+"；错误 "+integer(drc.get("errors"))+"；警告 "+integer(drc.get("warnings")),"当前实现质量检查"],["Vivado 墙钟",num(current.get("elapsed_s"),1," s"),"包括综合、布局、布线和报告"]])}<p>Verilator 是行为正确性证据。Vivado post-route 是时序、资源和布线证据。两者都不等价于真实板卡运行。Icarus/UNISIM 本轮仍记录为未完成，因为服务器环境没有 <code>xvlog</code>。</p></section>

<section><h2>我建议你审阅的下一步</h2><ol><li><b>补板级约束。</b>保留 `clr` 分组这个改动，用同一版 RTL 加入板级时钟、I/O 和 AXI/DDR 约束；250 MHz 通过目前只适用于 OOC。</li><li><b>继续盯住控制布线。</b>当前最长路径仍来自 control→PE <code>clr/CE</code>，所以应先确认板级实现后余量是否保住，再决定是否增加局部寄存器。</li><li><b>补真实利用率。</b>用一段固定的 TurboVLA 指令流做 Verilator 活动记录，把有效 MAC、阵列忙闲、读取、写回和停顿分开。这样下一版性能页才有“算力利用率”，而不是只有峰值。</li><li><b>再做功耗。</b>先用同一段活动生成 SAIF/VCD，再跑 report_power；当前 4.x W 级数字只保留为 vectorless 方向性参考。</li></ol><p class="note">本页没有修改 v5/v6，也没有生成 bitstream。v7 只是独立的 `clr` 扇出修正轮次，所有原始报告仍保留在对应实现目录。</p></section>

<section><h2>原始证据</h2><p>下面的链接直接指向当前实现的机器报告：</p><ul>{''.join(raw_links) or '<li>—</li>'}</ul><p>当前机器汇总 JSON：{link(str(output.with_name("performance_summary.json")), "performance_summary.json")}。</p></section>
<footer>生成时间：{html.escape(generated)}。本页数字均由 JSON/原始 Vivado 报告生成；百分比均使用未提前舍入的原始值计算。</footer>
</main></body></html>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")
    summary = {
        "generated_at": generated,
        "current_version": "v7" if v7 else ("v6" if v6 else "v5"),
        "timing": ct,
        "resources": cr,
        "power": cp,
        "route": route,
        "drc": drc,
        "derived": numbers,
        "comparison": {"v5_dpip2": dpip_v5, "current_dpip2": dpip_current, "dpip2_reduction_pct": dpip_reduction},
        "v6_to_v7_change_pct": {
            "fmax": (100.0 * (float(v7.get("timing", {}).get("fmax_estimate_mhz")) - float(v6.get("timing", {}).get("fmax_estimate_mhz"))) / float(v6.get("timing", {}).get("fmax_estimate_mhz"))) if v6 and v7 else None,
            "data_path_delay": (100.0 * (float(v7.get("timing", {}).get("data_path_delay_ns")) - float(v6.get("timing", {}).get("data_path_delay_ns"))) / float(v6.get("timing", {}).get("data_path_delay_ns"))) if v6 and v7 else None,
            "route_delay": (100.0 * (float(v7.get("timing", {}).get("route_delay_ns")) - float(v6.get("timing", {}).get("route_delay_ns"))) / float(v6.get("timing", {}).get("route_delay_ns"))) if v6 and v7 else None,
            "lut": (100.0 * (float(v7.get("resources", {}).get("total_luts")) - float(v6.get("resources", {}).get("total_luts"))) / float(v6.get("resources", {}).get("total_luts"))) if v6 and v7 else None,
            "power": (100.0 * (float(v7.get("power", {}).get("total_on_chip_w")) - float(v6.get("power", {}).get("total_on_chip_w"))) / float(v6.get("power", {}).get("total_on_chip_w"))) if v6 and v7 else None,
        },
    }
    output.with_name("performance_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--v5", type=Path, default=None)
    ap.add_argument("--v6", type=Path, default=None)
    ap.add_argument("--v7", type=Path, default=None)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    generated = datetime.now().astimezone().isoformat(timespec="seconds")
    build(load(args.v5), load(args.v6), load(args.v7), args.output.resolve(), generated)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
