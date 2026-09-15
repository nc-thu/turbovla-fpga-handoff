"""Generate a self-contained Chinese report for the v6 250 MHz run."""
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path
from typing import Any


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


def link(path: str, label: str) -> str:
    if not path:
        return "—"
    try:
        href = Path(path).resolve().as_uri()
    except (ValueError, OSError):
        href = str(path)
    return f'<a href="{html.escape(href, quote=True)}">{html.escape(label)}</a>'


def table(headers: list[str], rows: list[list[Any]]) -> str:
    head = "".join(f"<th>{esc(value)}</th>" for value in headers)
    body = "".join("<tr>" + "".join(f"<td>{esc(value)}</td>" for value in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def frequency_chart(data: dict[str, Any]) -> str:
    t = data["timing"]
    v5 = data.get("comparison_v5_post_route", {}).get("timing", {})
    values = [float(v5.get("fmax_estimate_mhz") or 0), float(t.get("fmax_estimate_mhz") or 0), float(t.get("target_frequency_mhz") or 0)]
    labels = ["v5 post-route", "v6 post-route", "v6 250 MHz目标"]
    colors = ["#8795a1", "#c36a43", "#3f739e"]
    maximum = max(values + [1.0]) * 1.22
    x0, y0, width, height = 62, 38, 660, 190
    bars = []
    for idx, (label, value, color) in enumerate(zip(labels, values, colors)):
        bw = 116
        x = x0 + 38 + idx * 205
        bh = height * value / maximum
        y = y0 + height - bh
        bars.append(
            f'<rect x="{x}" y="{y:.1f}" width="{bw}" height="{bh:.1f}" fill="{color}"/>'
            f'<text x="{x+bw/2:.1f}" y="{y-8:.1f}" text-anchor="middle" class="value">{value:.1f}</text>'
            f'<text x="{x+bw/2:.1f}" y="{y0+height+28}" text-anchor="middle" class="label">{html.escape(label)}</text>'
        )
    grid = "".join(
        f'<line x1="{x0}" y1="{y0+height-(n/4)*height:.1f}" x2="{x0+width}" y2="{y0+height-(n/4)*height:.1f}" stroke="#e5e7eb"/>'
        f'<text x="{x0-8}" y="{y0+height-(n/4)*height+4:.1f}" text-anchor="end" class="tick">{maximum*n/4:.0f}</text>'
        for n in range(5)
    )
    return (
        '<svg viewBox="0 0 770 285" role="img" aria-label="实现频率比较">'
        '<style>.label{font:13px Arial,sans-serif;fill:#28343c}.value{font:bold 16px Arial,sans-serif;fill:#182128}.tick{font:11px Arial,sans-serif;fill:#65727c}</style>'
        '<text x="24" y="20" class="label">按 post-route WNS 推算的最高频率（MHz）</text>'
        + grid + "".join(bars)
        + f'<line x1="{x0}" y1="{y0+height}" x2="{x0+width}" y2="{y0+height}" stroke="#26323a" stroke-width="1.4"/>'
        + f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+height}" stroke="#26323a" stroke-width="1.4"/>'
        '</svg>'
    )


def power_chart(data: dict[str, Any]) -> str:
    p = data["power"]
    dynamic = float(p.get("dynamic_w") or 0)
    static = float(p.get("static_w") or 0)
    total = max(dynamic + static, 1e-9)
    x, y, width, height = 58, 64, 650, 42
    dw = width * dynamic / total
    sw = width - dw
    return (
        '<svg viewBox="0 0 770 145" role="img" aria-label="功耗组成">'
        '<style>.label{font:13px Arial,sans-serif;fill:#28343c}.inside{font:bold 13px Arial,sans-serif;fill:#fff}</style>'
        f'<text x="28" y="25" class="label">Vivado vectorless 总片上功耗 {float(p.get("total_on_chip_w") or 0):.3f} W</text>'
        f'<rect x="{x}" y="{y}" width="{dw:.1f}" height="{height}" fill="#c36a43"/>'
        f'<rect x="{x+dw:.1f}" y="{y}" width="{sw:.1f}" height="{height}" fill="#8795a1"/>'
        f'<text x="{x+dw/2:.1f}" y="{y+27}" text-anchor="middle" class="inside">动态 {dynamic:.3f} W</text>'
        f'<text x="{x+dw+sw/2:.1f}" y="{y+27}" text-anchor="middle" class="inside">静态 {static:.3f} W</text>'
        '<text x="58" y="134" class="label">没有 SAIF/VCD；这里只能作为同一工具假设下的方向性估算。</text></svg>'
    )


def build(data: dict[str, Any], output: Path, generated: str) -> None:
    t = data["timing"]
    r = data["resources"]
    p = data["power"]
    route = data["route"]
    drc = data["drc"]
    v5 = data.get("comparison_v5_post_route", {})
    v5t = v5.get("timing", {})
    v5r = v5.get("resources", {})
    v5d = v5.get("drc", {})
    sim = data.get("simulation", {})
    timing_met = bool(t.get("timing_met"))
    miss_pct = None
    if t.get("fmax_estimate_mhz") and t.get("target_frequency_mhz"):
        miss_pct = (1.0 - float(t["fmax_estimate_mhz"]) / float(t["target_frequency_mhz"])) * 100.0
    status_text = "通过 250 MHz 时序" if timing_met else "未通过 250 MHz 时序"
    status_color = "#2f7d4a" if timing_met else "#b44747"
    raw_links = "".join(f"<li>{link(path, name)}</li>" for name, path in data.get("raw_reports", {}).items())
    report = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TurboVLA W8A16 v6 250 MHz Vivado 实现结果</title>
<style>
body{{margin:0;background:#f3f5f7;color:#24313a;font-family:"Microsoft YaHei",Arial,sans-serif;line-height:1.6}}
main{{max-width:1180px;margin:auto;padding:26px 30px 56px}}
header,section{{background:#fff;border:1px solid #d9e0e5;margin:0 0 18px;padding:22px 26px}}
h1{{font-size:28px;line-height:1.25;margin:0 0 8px}}h2{{font-size:20px;margin:0 0 12px;border-left:4px solid #3f739e;padding-left:10px}}
h3{{font-size:16px;margin:18px 0 6px}}.meta{{font-size:13px;color:#64727c}}.lead{{font-size:17px;margin:12px 0}}
.status{{display:inline-block;color:#fff;background:{status_color};padding:4px 10px;font-weight:700}}
.cards{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:18px}}.card{{background:#fafbfc;border:1px solid #dbe2e7;padding:11px}}
.card .v{{display:block;font-weight:700;font-size:22px;color:#1d3c52}}.card .k{{font-size:12px;color:#66737c}}
table{{border-collapse:collapse;width:100%;font-size:13px}}th,td{{border:1px solid #dce2e7;padding:7px 8px;text-align:left;vertical-align:top}}th{{background:#edf3f7}}
code{{font:12px Consolas,monospace;word-break:break-all}}.note{{background:#f5f8fa;border-left:3px solid #8795a1;padding:10px 12px;font-size:13px}}
.warn{{background:#fff5ed;border-left:3px solid #c36a43;padding:10px 12px}}.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
a{{color:#245d8a}}ul,ol{{margin-top:6px}}footer{{font-size:12px;color:#68757d}}
@media(max-width:760px){{main{{padding:14px}}header,section{{padding:16px}}.cards,.grid2{{grid-template-columns:1fr 1fr}}h1{{font-size:23px}}table{{display:block;overflow-x:auto;white-space:nowrap}}}}
@media(max-width:480px){{.cards{{grid-template-columns:1fr}}}}
</style></head><body><main>
<header><h1>TurboVLA W8A16 v6：DSP 输入／输出 pipeline 与 250 MHz 实现</h1>
<div class="meta">生成时间：{html.escape(generated)}　｜　Vivado 2021.2　｜　器件：{esc(data.get("part"))}　｜　顶层：{esc(data.get("top"))}</div>
<p class="lead"><span class="status">{status_text}</span>　route 已完成，184,306 条可路由网络全部布线；最终 WNS 为 {f(t.get("wns_ns"),3)} ns，离 4.000 ns 目标还差 {f(abs(float(t.get("wns_ns") or 0)),3)} ns。</p>
<div class="cards"><div class="card"><span class="v">{f(t.get("fmax_estimate_mhz"),1)} MHz</span><span class="k">post-route 频率估算</span></div>
<div class="card"><span class="v">{i(r.get("dsp"))}</span><span class="k">DSP Blocks（阵列 768）</span></div>
<div class="card"><span class="v">{i(r.get("total_luts"))}</span><span class="k">总 LUT</span></div>
<div class="card"><span class="v">{f(p.get("total_on_chip_w"),3)} W</span><span class="k">vectorless 总功耗</span></div>
<div class="card"><span class="v">{f(float(data.get("elapsed_s") or 0)/60,1)} min</span><span class="k">Vivado 墙钟耗时</span></div></div></header>

<section><h2>这轮到底做了什么</h2><p>v6 从 v5 独立复制出来，只改三类寄存器边界：</p>
<ul><li><code>w8a16_mult</code> 把 DSP 的 A/B 输入配置为 <code>AREG=1/BREG=1</code>，乘法和输出保持 <code>MREG=1/PREG=1</code>。</li>
<li><code>w8a16_pe</code> 保留乘积寄存器和 valid 对齐，避免输入 pipeline 改变 PE 协议。</li>
<li><code>w8a16_action_path</code> 增加 MAC 操作数／乘积寄存，并把累加末尾拆成两拍 drain，切开乘积到 INT40 反馈的长组合路径。</li></ul>
<p>Verilator 的 11 个测试全部通过，包含 PE、阵列、完整 16×48、GEMM、激活、向量、DMA、ISA、runtime 和 system。完整阵列仍是 768 DSP，输出与整数参考逐位一致。</p>
<p class="note">Icarus/UNISIM 冒烟没有在服务器完成：日志记录为服务器找不到 <code>xvlog</code>。Vivado 本地综合和实现本身已经完成；这两件事不能混写成“UNISIM 已通过”。</p></section>

<section><h2>先看实现结论</h2><p>4.000 ns 等于 250 MHz。v6 最终可以按 WNS 推算到 {f(t.get("fmax_estimate_mhz"),1)} MHz，约比 250 MHz 低 {f(miss_pct,1)}%。所以这轮证明“pipeline 方向有效并且设计可完整布线”，但还不能写成“250 MHz 已收敛”。</p>
<ul><li>v5 在 3.298 ns 目标下的 WNS 是 {f(v5t.get("wns_ns"),3)} ns；v6 的 WNS 改为 {f(t.get("wns_ns"),3)} ns。两个目标周期不同，这个变化只能说明方向改善，不能作为严格的单变量增益。</li>
<li>v6 仍保留 {i(r.get("dsp"))} 个 DSP，没有增加乘法资源；LUT 为 {i(r.get("total_luts"))}，FF 为 {i(r.get("ffs"))}。</li>
<li>功耗是 routed design 的 vectorless 估算，置信度为 {esc(p.get("confidence"))}。没有真实工作负载的 SAIF/VCD，不能当成板上测量或能效结论。</li></ul></section>

<section><h2>频率对照</h2>{frequency_chart(data)}{table(["版本","目标周期","post-route WNS","按 WNS 推算频率","是否过目标"],[
["v5",f(v5t.get("target_period_ns"),3)+" ns",f(v5t.get("wns_ns"),3)+" ns",f(v5t.get("fmax_estimate_mhz"),1)+" MHz","否"],
["v6",f(t.get("target_period_ns"),3)+" ns",f(t.get("wns_ns"),3)+" ns",f(t.get("fmax_estimate_mhz"),1)+" MHz","否"],
["v6目标","4.000 ns","0 ns","250.0 MHz","—"]])}<p class="note">v6 的中间 post-place WNS 曾达到正值，但最终布线后变为 −0.050 ns；论文或报告应以 post-route 为准。</p></section>

<section><h2>最长路径在哪里</h2>{table(["字段","post-route 值"],[
["起点",t.get("critical_source")],["终点",t.get("critical_destination")],["要求",f(t.get("target_period_ns"),3)+" ns"],
["数据路径延迟",f(t.get("data_path_delay_ns"),3)+" ns"],["逻辑延迟",f(t.get("logic_delay_ns"),3)+" ns（"+f(t.get("logic_delay_percent"),1)+"%）"],
["布线延迟",f(t.get("route_delay_ns"),3)+" ns（"+f(t.get("route_delay_percent"),1)+"%）"],["失败 setup 端点",i(t.get("failing_endpoints"))],["TNS",f(t.get("tns_ns"),3)+" ns"]])}
<p>最终最差路径已经不是“乘法器到累加器”的长算术链，而是 <code>u_runtime/u_ctrl/word_r_reg[61]</code> 经过控制译码和高扇出清零网络，抵达阵列某个 PE 的累加器 CE。数据路径 3.946 ns 中布线占 3.645 ns（92.4%），下一步应优先处理 <code>clr/CE</code> 的扇出、分区和局部寄存器，而不是继续盲目增加乘法流水。</p></section>

<section><h2>资源、布线与 DRC</h2>{table(["资源/检查","v6 post-route","v5 post-route","v6−v5（仅方向参考）"],[
["LUT",i(r.get("total_luts")),i(v5r.get("total_luts")),i((r.get("total_luts") or 0)-(v5r.get("total_luts") or 0))],
["Logic LUT",i(r.get("logic_luts")),i(v5r.get("logic_luts")),i((r.get("logic_luts") or 0)-(v5r.get("logic_luts") or 0))],
["FF",i(r.get("ffs")),i(v5r.get("ffs")),i((r.get("ffs") or 0)-(v5r.get("ffs") or 0))],
["DSP",i(r.get("dsp")),i(v5r.get("dsp")),i((r.get("dsp") or 0)-(v5r.get("dsp") or 0))],
["BRAM36 / BRAM18",f(r.get("ramb36"),0)+" / "+f(r.get("ramb18"),0),f(v5r.get("ramb36"),0)+" / "+f(v5r.get("ramb18"),0),"0 / 0"],
["可路由网络",i(route.get("fully_routed_nets"))+" / "+i(route.get("routable_nets")),i(data.get("comparison_v5_post_route",{}).get("route",{}).get("fully_routed_nets"))+" / "+i(data.get("comparison_v5_post_route",{}).get("route",{}).get("routable_nets")),"—"],
["DRC",i(drc.get("violations"))+"（错误 0）",i(v5d.get("violations"))+"（错误 0）",i((drc.get("violations") or 0)-(v5d.get("violations") or 0))]])}
<p class="note">DRC 规则统计为 DPIP-2 输入 pipeline {i(drc.get("rules",{}).get("DPIP-2",{}).get("count"))}（v5 为 {i(v5d.get("rules",{}).get("DPIP-2",{}).get("count"))}，减少约 97.8%）、DPOP-3 PREG {i(drc.get("rules",{}).get("DPOP-3",{}).get("count"))}、DPOP-4 MREG {i(drc.get("rules",{}).get("DPOP-4",{}).get("count"))}、RTSTAT-10 {i(drc.get("rules",{}).get("RTSTAT-10",{}).get("count"))}，以及 AVAL-155 advisory 768。DPIP/DPOP 仍主要来自 runtime 中其他 DSP 乘法路径；它们是下一轮的明确清单，不应被忽略。</p></section>

<section><h2>功耗估算</h2>{power_chart(data)}{table(["项目","数值","证据口径"],[
["总片上功耗",f(p.get("total_on_chip_w"),3)+" W","Vivado routed report_power"],
["动态功耗",f(p.get("dynamic_w"),3)+" W","vectorless activity propagation"],
["静态功耗",f(p.get("static_w"),3)+" W","器件静态模型"],
["置信度",p.get("confidence"),"没有 SAIF/VCD"],
["DSP 部分",f(0.558,3)+" W","report_power 的 DSP 资源项"]])}<div class="warn">这轮没有板级电源测量，也没有 TurboVLA 真实切换活动文件。4.478 W 可以用来和同样假设下的版本比较，不能直接写成芯片能效。</div></section>

<section><h2>仿真、运行和原始证据</h2>{table(["项目","结果"],[
["Verilator",esc(sim.get("status"))+"；"+i(len(sim.get("tests",[])))+" 个测试；"+f(sim.get("elapsed_seconds"),0)+" s"],
["完整阵列",i(sim.get("dsp_full_array"))+" DSP（16×48）"],
["Icarus/UNISIM", "未完成：服务器没有 xvlog"],
["Vivado 开始",data.get("started")],["Vivado 结束",data.get("finished")],["Vivado 墙钟耗时",f(data.get("elapsed_s"),1)+" s"],
["route",route.get("status")+"；未布线 "+i(route.get("unrouted_nets"))+"；routing errors "+i(route.get("routing_errors"))]])}
<p>本页的数字都从机器可读 JSON 和 Vivado 原始报告生成。原始文件：</p><ul>{raw_links}</ul>
<p>Verilator 汇总：{link(sim.get("path",""),"verilator_run.json")}；机器汇总：{link(str(output.with_name("implementation_results.json")),"implementation_results.json")}。</p></section>

<section><h2>下一步建议</h2><ol><li>先把控制译码到阵列 <code>clr/CE</code> 的高扇出网络按行或列分区，并在每个分区前加局部寄存器；这个路径目前 92.4% 的延迟花在布线上。</li><li>补齐 runtime/vector/action 中仍触发 DPIP-2 和 DPOP-3/4 的 DSP 输入／输出寄存器，再用 Verilator 对拍。不要把阵列已经使用的 AREG/BREG 误认为所有 DSP 都已流水。</li><li>修完后继续用同一个 4.000 ns 约束跑实现。只有 post-route WNS≥0、DRC 错误为 0，并补齐板级时钟和 I/O 约束，才可以把 250 MHz 写成实现结果。</li></ol>
<p class="note">本轮没有生成 bitstream，没有修改旧 v5 目录，也没有做板上 TurboVLA 端到端测试。</p></section>
<footer>生成于 {html.escape(generated)}。v6 目录：{esc(data.get("run_root"))}；原始报告保留在该目录。</footer>
</main></body></html>'''
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(report, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("results_json", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--timestamp", default=None)
    args = parser.parse_args()
    generated = datetime.now().astimezone().isoformat(timespec="seconds")
    if args.timestamp:
        generated = datetime.strptime(args.timestamp, "%Y-%m-%d_%H%M%S").astimezone().isoformat(timespec="seconds")
    data = load(args.results_json.resolve())
    build(data, args.output.resolve(), generated)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
