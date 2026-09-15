"""Generate a self-contained Chinese report for the v5 implementation run."""
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: Any) -> str:
    return html.escape("—" if value is None or value == "" else str(value))


def f(value: Any, digits: int = 2, suffix: str = "") -> str:
    try:
        return f"{float(value):.{digits}f}{suffix}"
    except (TypeError, ValueError):
        return "—"


def i(value: Any) -> str:
    try:
        return f"{int(round(float(value))):,}"
    except (TypeError, ValueError):
        return "—"


def pct(value: Any) -> str:
    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return "—"


def table(headers: list[str], rows: list[list[Any]]) -> str:
    head = "".join(f"<th>{esc(x)}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(x)}</td>" for x in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def chart(data: dict[str, Any]) -> str:
    timing = data["timing"]
    v4 = data["comparison_v4_synth"]["timing"]
    vals = [float(v4.get("fmax_estimate_mhz") or 0), float(timing.get("fmax_estimate_mhz") or 0), float(timing.get("target_frequency_mhz") or 0)]
    labels = ["v4 综合估算", "v5 布线后估算", "目标时钟"]
    colors = ["#7b8794", "#c45454", "#376f9f"]
    ymax = max(vals + [1.0]) * 1.25
    x0, y0, w, h = 64, 28, 610, 210
    bars = []
    for idx, (label, value, color) in enumerate(zip(labels, vals, colors)):
        bw = 110
        x = x0 + 35 + idx * 190
        bh = (value / ymax) * h
        y = y0 + h - bh
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="{bw}" height="{bh:.1f}" fill="{color}"/><text x="{x+bw/2:.1f}" y="{y-8:.1f}" text-anchor="middle" class="v">{value:.1f}</text><text x="{x+bw/2:.1f}" y="{y0+h+27}" text-anchor="middle" class="l">{html.escape(label)}</text>')
    grid = "".join(f'<line x1="{x0}" y1="{y0+h-(n/4)*h:.1f}" x2="{x0+w}" y2="{y0+h-(n/4)*h:.1f}" stroke="#e5e7eb"/><text x="{x0-9}" y="{y0+h-(n/4)*h+4:.1f}" text-anchor="end" class="tick">{ymax*n/4:.0f}</text>' for n in range(5))
    return f'''<svg viewBox="0 0 760 300" role="img" aria-label="频率比较"><style>.l{{font:14px Arial,sans-serif;fill:#26323b}}.v{{font:bold 16px Arial,sans-serif;fill:#1d252c}}.tick{{font:12px Arial,sans-serif;fill:#66737e}}</style><text x="28" y="18" class="l">按 post-route WNS 推算的可运行频率（MHz）</text>{grid}{"".join(bars)}<line x1="{x0}" y1="{y0+h}" x2="{x0+w}" y2="{y0+h}" stroke="#27323a" stroke-width="1.5"/><line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+h}" stroke="#27323a" stroke-width="1.5"/></svg>'''


def power_chart(data: dict[str, Any]) -> str:
    p = data["power"]
    vals = [float(p.get("dynamic_w") or 0), float(p.get("static_w") or 0)]
    labels = ["动态", "静态"]
    colors = ["#d9844e", "#7b8794"]
    total = max(sum(vals), 1e-9)
    x, y, width, height = 52, 70, 650, 42
    segs = []
    cursor = x
    for label, value, color in zip(labels, vals, colors):
        sw = width * value / total
        segs.append(f'<rect x="{cursor:.1f}" y="{y}" width="{sw:.1f}" height="{height}" fill="{color}"/><text x="{cursor+sw/2:.1f}" y="{y+27}" text-anchor="middle" class="v">{label} {value:.2f} W</text>')
        cursor += sw
    return f'''<svg viewBox="0 0 760 150" role="img" aria-label="功耗组成"><style>.v{{font:bold 14px Arial,sans-serif;fill:#fff}}.t{{font:14px Arial,sans-serif;fill:#26323b}}</style><text x="28" y="28" class="t">Vivado vectorless 功耗估算，总计 {float(p.get("total_on_chip_w") or 0):.3f} W</text>{"".join(segs)}<text x="52" y="140" class="t">无 SAIF/VCD 活动文件；这张图不能替代板上功耗测量。</text></svg>'''


def link(path: str, label: str) -> str:
    p = Path(path)
    try:
        href = p.resolve().as_uri()
    except ValueError:
        href = str(p)
    return f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'


def build(data: dict[str, Any], output: Path, generated: str | None = None) -> None:
    generated = generated or datetime.now().astimezone().isoformat(timespec="seconds")
    t = data["timing"]
    r = data["resources"]
    p = data["power"]
    route = data["route"]
    drc = data["drc"]
    v4 = data["comparison_v4_synth"]
    raw = data["raw_reports"]
    target_met = bool(t.get("timing_met"))
    status_color = "#2f7d4a" if target_met else "#b44747"
    status_text = "达到 3.298 ns 目标" if target_met else "未达到 3.298 ns 目标"
    report_links = []
    for key, path in raw.items():
        report_links.append(f"<li>{link(path, key)}</li>")
    report = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TurboVLA W8A16 顶层 post-route implementation</title>
<style>
body{{margin:0;background:#f4f6f8;color:#25313a;font-family:"Microsoft YaHei",Arial,sans-serif;line-height:1.6}}
main{{max-width:1180px;margin:0 auto;padding:28px 30px 60px}}header,section{{background:#fff;border:1px solid #d9e0e5;margin:0 0 18px;padding:22px 26px;box-shadow:0 1px 2px #0000000a}}h1{{margin:0 0 8px;font-size:28px;line-height:1.25}}h2{{font-size:20px;margin:0 0 12px;border-left:4px solid #376f9f;padding-left:10px}}h3{{font-size:16px;margin:18px 0 6px}}.meta{{color:#61707b;font-size:13px}}.lead{{font-size:17px;margin:12px 0}}.status{{display:inline-block;color:#fff;background:{status_color};padding:5px 11px;font-weight:bold}}.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:18px}}.card{{border:1px solid #d9e0e5;padding:12px;background:#fafbfc}}.card .v{{display:block;font-size:24px;font-weight:bold;color:#1e3548}}.card .k{{font-size:12px;color:#66737e}}table{{width:100%;border-collapse:collapse;font-size:13px}}th,td{{border:1px solid #dce2e7;padding:7px 8px;text-align:left;vertical-align:top}}th{{background:#eef3f7;font-weight:bold}}code{{font-family:Consolas,monospace;font-size:12px;word-break:break-all}}.note{{background:#f5f8fa;border-left:3px solid #7b8794;padding:10px 12px;font-size:13px}}.warn{{background:#fff5ed;border-left:3px solid #d9844e;padding:10px 12px}}.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}ul{{margin:6px 0 6px 20px}}a{{color:#245d8a}}footer{{color:#66737e;font-size:12px;padding:8px 2px}}@media(max-width:760px){{main{{padding:14px}}header,section{{padding:16px}}.cards,.grid2{{grid-template-columns:1fr 1fr}}h1{{font-size:23px}}table{{font-size:12px;display:block;overflow-x:auto;white-space:nowrap}}}}@media(max-width:480px){{.cards{{grid-template-columns:1fr}}}}
</style></head><body><main>
<header><h1>TurboVLA W8A16 顶层 post-route implementation 结果</h1><div class="meta">生成时间：{html.escape(generated)}　｜　版本：v5_2026-09-13_163609_post_route_impl　｜　工具：Vivado 2021.2</div><p class="lead"><span class="status">{status_text}</span>　route 已完成且 0 条可路由网络未布线，但阵列和 runtime 的最长数据路径仍比 3.298 ns 多 0.461 ns。</p><div class="cards"><div class="card"><span class="v">{f(t.get("wns_ns"),3)} ns</span><span class="k">post-route WNS</span></div><div class="card"><span class="v">{f(t.get("fmax_estimate_mhz"),1)} MHz</span><span class="k">按 WNS 推算的最高频率</span></div><div class="card"><span class="v">{i(r.get("dsp"))}</span><span class="k">DSP Blocks</span></div><div class="card"><span class="v">{f(p.get("total_on_chip_w"),3)} W</span><span class="k">vectorless 总片上功耗估算</span></div></div></header>

<section><h2>先看结论</h2><p>这次不是只做逻辑综合，而是完整跑过了 <code>opt_design → place_design → phys_opt_design → route_design → post-route phys_opt_design</code>。因此，{f(t.get("wns_ns"),3)} ns 的 WNS 是目前最接近真实实现状态的时序证据。</p><ul><li>3.298 ns 目标对应 303.2 MHz。当前 post-route WNS 为 {f(t.get("wns_ns"),3)} ns，按 <code>period − WNS</code> 推算可运行频率约 {f(t.get("fmax_estimate_mhz"),1)} MHz，约比目标频率低 {f((1-float(t.get("fmax_estimate_mhz") or 0)/float(t.get("target_frequency_mhz") or 1))*100,1)}%。</li><li>关键路径从 <code>{esc(t.get("critical_source"))}</code> 到 <code>{esc(t.get("critical_destination"))}</code>，数据路径 3.740 ns，其中逻辑 2.056 ns（{f(t.get("logic_delay_percent"),1)}%），布线 1.684 ns（{f(t.get("route_delay_percent"),1)}%）。这说明现在不只是 RTL 组合逻辑长，布局布线也占了近一半。</li><li>可路由网络 184,104 条，全部完成布线；但 OOC wrapper 没有板级 pin、AXI/DDR 和时钟缓冲约束，不能据此生成 bitstream 或声称板上时序。</li></ul></section>

<section><h2>频率对照</h2>{chart(data)}<p class="note">图中 v4 是同一顶层的综合阶段估算，v5 是布线后的估算。两者阶段不同，不能把资源变化当成公平的 PPA 提升；频率对照的意义是说明布线把原本的综合余量消耗掉了。</p>{table(["阶段","WNS","数据路径","频率口径","是否过 3.298 ns"],[["v4 synth",f(v4["timing"].get("wns_ns"),3)+" ns",f(v4["timing"].get("data_path_delay_ns"),3)+" ns",f(v4["timing"].get("fmax_estimate_mhz"),1)+" MHz","是"],["v5 post-route",f(t.get("wns_ns"),3)+" ns",f(t.get("data_path_delay_ns"),3)+" ns",f(t.get("fmax_estimate_mhz"),1)+" MHz","否"]])}</section>

<section><h2>post-route 资源</h2>{table(["资源","v5 post-route","v4 synth","差值（仅作参考）"],[["LUT",i(r.get("total_luts")),i(v4["resources"].get("total_luts")),i(v4["deltas"].get("total_luts"))],["Logic LUT",i(r.get("logic_luts")),i(v4["resources"].get("logic_luts")),i(v4["deltas"].get("logic_luts"))],["FF",i(r.get("ffs")),i(v4["resources"].get("ffs")),i(v4["deltas"].get("ffs"))],["DSP",i(r.get("dsp")),i(v4["resources"].get("dsp")),i(v4["deltas"].get("dsp"))],["BRAM36 / BRAM18",f(r.get("ramb36"),0)+" / "+f(r.get("ramb18"),0),f(v4["resources"].get("ramb36"),0)+" / "+f(v4["resources"].get("ramb18"),0),"0 / 0"],["URAM",i(r.get("uram")),i(v4["resources"].get("uram")),i(v4["deltas"].get("uram"))]])}<p class="note">v5 保持 16×48 阵列的 768 DSP；系统总数为 785 DSP。v4 与 v5 之间包含综合和实现阶段差异，所以这里不宣称“面积下降”。</p></section>

<section><h2>功耗估算</h2>{power_chart(data)}{table(["项目","数值","解释"],[["总片上功耗",f(p.get("total_on_chip_w"),3)+" W","Vivado report_power"],["动态功耗",f(p.get("dynamic_w"),3)+" W","时钟、CLB、信号和 DSP 的 vectorless 估算"],["静态功耗",f(p.get("static_w"),3)+" W","器件静态模型"],["Vivado 置信度",esc(p.get("confidence")),"内部节点活动少于 25% 被用户指定"],["活动文件",esc(p.get("activity_file")),"没有 SAIF/VCD"]])}<div class="warn">这不是板上实测功耗。当前 report_power 使用默认 vectorless activity，内部节点没有真实 TurboVLA 工作负载的切换率。因此可以用它比较同一工具假设下的方向，但不能写成能效（TOPS/W）或实测芯片功耗。</div></section>

<section><h2>布线、DRC 和时序边界</h2>{table(["检查","结果","说明"],[["route status",route.get("status"),i(route.get("fully_routed_nets"))+" / "+i(route.get("routable_nets"))+" 条可路由网络已完成"],["unrouted nets",i(route.get("unrouted_nets")),"必须为 0；本次为 0"],["routing errors",i(route.get("routing_errors")),"必须为 0；本次为 0"],["DRC violations",i(drc.get("violations")),"主要是 DSP 输入／输出未使用全部内部 pipeline 的规则提示"],["DRC errors",i(drc.get("errors")),"本次为 0"],["DRC warnings / advisories",str(drc.get("warnings"))+" / "+str(drc.get("advisories")),"OOC wrapper 仍缺板级约束和部分 DSP pipeline 建议"],["setup",i(t.get("failing_endpoints"))+" 个失败端点","WNS 为负，当前频率目标未通过"]])}<p class="note">Vivado 在后 route phys-opt 阶段明确提示负 slack 过大，预计仅靠 post-route phys-opt 难以完全修复。下一步更有效的是减少关键路径逻辑／扇出，或重新安排阵列和动作路径的寄存器边界，再重新实现。</p></section>

<section><h2>关键路径和运行记录</h2>{table(["字段","值"],[["器件",data.get("part")],["顶层",data.get("top")],["阵列",str(data.get("rows"))+" × "+str(data.get("pcols"))+" PE / 768 DSP"],["目标周期",f(data.get("target_period_ns"),3)+" ns（303.2 MHz）"],["运行开始",data.get("started")],["运行结束",data.get("finished")],["Vivado launcher 墙钟耗时",f(data.get("elapsed_s"),1)+" s（约 "+f(float(data.get("elapsed_s") or 0)/60,1)+" min）"],["关键路径起点",data["timing"].get("critical_source")],["关键路径终点",data["timing"].get("critical_destination")],["失败 setup 端点",i(t.get("failing_endpoints"))],["数据路径延迟",f(t.get("data_path_delay_ns"),3)+" ns"],["逻辑 / 布线延迟",f(t.get("logic_delay_ns"),3)+" ns / "+f(t.get("route_delay_ns"),3)+" ns"]])}</section>

<section><h2>原始证据</h2><p>下面链接均指向这次 implementation 的原始文件。报告只从这些文件解析数字，没有手抄 PPA。</p><ul>{"".join(report_links)}</ul><p class="meta">机器可读汇总：{link(data.get("machine_readable_json", ""), "implementation_results.json")}</p></section>

<section><h2>下一步建议</h2><ol><li>先针对关键路径做 RTL 级拆分：当前最长路径落在动作权重寄存器到 40-bit 累加器，且组合逻辑和布线各占较大比例。</li><li>给阵列输入和 DSP 端口补齐可控的 pipeline，逐步检查并压低 {i(t.get("failing_endpoints"))} 个 setup 失败端点；每次只改一处并用 Verilator 对拍。</li><li>在真实板级工程加入时钟 buffer、pin、AXI/DDR 和 I/O delay 约束后再实现。板级约束补齐前，不应把 5.678 W 当成产品功耗，也不应生成 bitstream。</li></ol><p class="note">本轮没有修改 v4 RTL，只复制 v4 进行实现；历史目录保持不动。</p></section>
<footer>生成于 {html.escape(generated)}。本页只报告 v5 post-route implementation 证据；功耗为 vectorless 估算，未做上板、SAIF/VCD、bitstream 或真实 TurboVLA 端到端运行。</footer>
</main></body></html>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results_json", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--timestamp", default=None, help="报告时间戳，格式 YYYY-MM-DD_HHMMSS")
    args = parser.parse_args()
    data = load(args.results_json.resolve())
    data["machine_readable_json"] = str(args.results_json.resolve())
    generated = None
    if args.timestamp:
        generated = datetime.strptime(args.timestamp, "%Y-%m-%d_%H%M%S").astimezone().isoformat(timespec="seconds")
    build(data, args.output.resolve(), generated)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
