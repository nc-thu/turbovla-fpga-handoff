"""Generate the v6 architecture/status page from machine-readable results."""
from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = "2026-09-16_070844"
DATA = ROOT / "data" / "2026-09-16_060349_fp16_memory_complete" / "compiled_v4_sideband"
VIVADO_ROOT = ROOT / "hw" / "v6_2026-09-16_060349_fp16_memory_complete_rtl" / "vivado"
# Vivado output directories are timestamped by the synthesis script.  Pick the
# newest completed directory instead of baking an old run into the report.
_vivado_dirs = sorted(VIVADO_ROOT.glob("fp16_vendor_project_synth_*"), key=lambda p: p.stat().st_mtime, reverse=True)
VIVADO = _vivado_dirs[0] if _vivado_dirs else VIVADO_ROOT / "fp16_vendor_project_synth_missing"
OUT = ROOT / "reports" / STAMP / f"{STAMP}_TurboVLA全模型v6架构与实现状态.html"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def num(pattern: str, text: str, default: str = "未找到") -> str:
    m = re.search(pattern, text)
    return m.group(1) if m else default


def esc(v) -> str:
    return html.escape(str(v))


def bar(label: str, value: float, max_value: float, color: str) -> str:
    width = max(2.0, 100.0 * value / max_value) if max_value else 2.0
    return f'<div class="barrow"><span>{esc(label)}</span><div class="bar"><i style="width:{width:.2f}%;background:{color}"></i></div><b>{value:,.0f}</b></div>'


def main() -> None:
    summary = load("cycle_summary.json")
    inv = load("operator_inventory.json")
    util_path = VIVADO / "synth_utilization.rpt"
    timing_path = VIVADO / "synth_timing.rpt"
    util = util_path.read_text(encoding="utf-8", errors="ignore") if util_path.exists() else ""
    timing = timing_path.read_text(encoding="utf-8", errors="ignore") if timing_path.exists() else ""
    lut = num(r"\| CLB LUTs\*\s*\|\s*([\d,]+)", util)
    ff = num(r"\| CLB Registers\s*\|\s*([\d,]+)", util)
    dsp = num(r"\| DSPs\s*\|\s*([\d,]+)", util)
    bram = num(r"\| Block RAM Tile\s*\|\s*([\d,]+)", util)
    wns = num(r"Design Timing Summary[\s\S]*?\n\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)", timing, default="未生成")
    if wns == "未生成":
        wns = num(r"^\s*(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+\d+\s+\d+\s+(-?\d+\.\d+)", timing, default="未生成")
    dispatch = summary["source_dispatch_events"]
    units = summary["execution_unit_counts"]
    total = summary["total_cycles"]
    html_text = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{STAMP} TurboVLA 全模型 v6 架构与实现状态</title>
<style>
body{{margin:0;background:#f5f6f8;color:#20252b;font:15px/1.65 Arial,"Microsoft YaHei",sans-serif}}
main{{max-width:1180px;margin:0 auto;padding:28px 30px 54px}}h1{{font-size:30px;margin:0 0 6px}}h2{{font-size:22px;margin:34px 0 10px;border-left:5px solid #2b6cb0;padding-left:10px}}h3{{font-size:17px;margin:21px 0 6px}}p{{margin:8px 0}}.muted{{color:#65717d}}.facts{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0}}.fact{{background:white;border:1px solid #d8dde3;padding:14px 15px;border-radius:5px}}.fact b{{display:block;font-size:24px;color:#155e96}}table{{border-collapse:collapse;width:100%;background:white;margin:10px 0 16px}}th,td{{border:1px solid #d8dde3;padding:8px 10px;text-align:left;vertical-align:top}}th{{background:#edf1f5}}.ok{{color:#126b42;font-weight:700}}.warn{{color:#9a4e00;font-weight:700}}.bad{{color:#a42b2b;font-weight:700}}.note{{background:#fff8e6;border-left:4px solid #d99b21;padding:10px 13px;margin:12px 0}}.barrow{{display:grid;grid-template-columns:145px 1fr 75px;gap:8px;align-items:center;margin:6px 0}}.bar{{height:14px;background:#e5e9ee;border-radius:2px;overflow:hidden}}.bar i{{display:block;height:100%}}.barrow b{{text-align:right;font-weight:600}}.diagram{{background:#fff;border:1px solid #ccd4dc;padding:16px;margin:12px 0}}svg text{{font-family:Arial,"Microsoft YaHei",sans-serif}}.cols{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.small{{font-size:13px}}code{{background:#eef1f4;padding:1px 4px;border-radius:3px}}ul{{margin:6px 0 10px 23px}}@media(max-width:760px){{main{{padding:18px 14px}}.facts{{grid-template-columns:repeat(2,1fr)}}.cols{{grid-template-columns:1fr}}h1{{font-size:24px}}}}
</style></head><body><main>
<h1>TurboVLA 全模型 v6：编译器、数据通路和综合结果</h1>
<p class="muted">生成时间：{STAMP[:4]}-{STAMP[5:7]}-{STAMP[8:10]} {STAMP[11:13]}:{STAMP[13:15]}:{STAMP[15:]}　|　工作区：<code>turbovla_w8a8_pack2</code></p>
<div class="note"><b>先看结论：</b>这轮把 512-bit descriptor sideband、双输入 BMM staging、scale/bias BRAM 表和 Xilinx FP16 IP 的工程引用补上了。Icarus smoke 和 Vivado vendor-IP 综合通过；4 ns 综合 WNS={esc(wns)}，所以 250 MHz 仍未通过。完整 TurboVLA 端到端推理还不能宣称完成。</div>
<div class="facts"><div class="fact"><span>dispatch 事件</span><b>{dispatch:,}</b><small>编译器分类全部覆盖</small></div><div class="fact"><span>Pack2 描述符</span><b>{summary['pack2_descriptor_count']:,}</b><small>INT8 GEMM/BMM</small></div><div class="fact"><span>PE 时间利用率</span><b>{summary['pe_time_utilization']*100:.2f}%</b><small>完整 trace 周期模型</small></div><div class="fact"><span>有效吞吐</span><b>{summary['effective_gops_250mhz']:.2f} GOPS</b><small>250 MHz 周期投影</small></div></div>

<h2>1. 当前数据是怎么走的</h2>
<div class="diagram"><svg viewBox="0 0 1080 250" width="100%" role="img" aria-label="TurboVLA data path">
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#29323a"/></marker></defs>
<rect x="18" y="80" width="150" height="76" fill="#e5eff9" stroke="#27333d" stroke-width="2"/><text x="93" y="110" text-anchor="middle" font-size="16" font-weight="700">TurboVLA trace</text><text x="93" y="134" text-anchor="middle" font-size="12">shape / dtype / 依赖</text>
<rect x="220" y="30" width="180" height="176" fill="#fff3d6" stroke="#27333d" stroke-width="2"/><text x="310" y="58" text-anchor="middle" font-size="16" font-weight="700">v4 compiler</text><text x="310" y="88" text-anchor="middle" font-size="12">64-bit command</text><text x="310" y="110" text-anchor="middle" font-size="12">512-bit sideband</text><text x="310" y="132" text-anchor="middle" font-size="12">scale / layout / mask</text><text x="310" y="154" text-anchor="middle" font-size="12">dependency graph</text>
<rect x="452" y="30" width="178" height="176" fill="#e9f6e9" stroke="#27333d" stroke-width="2"/><text x="541" y="58" text-anchor="middle" font-size="16" font-weight="700">scheduler</text><text x="541" y="90" text-anchor="middle" font-size="12">sideband FIFO</text><text x="541" y="112" text-anchor="middle" font-size="12">BMM 双输入等待</text><text x="541" y="134" text-anchor="middle" font-size="12">barrier / backpressure</text><text x="541" y="156" text-anchor="middle" font-size="12">CTX / WRAM</text>
<rect x="682" y="30" width="180" height="176" fill="#fbe9dc" stroke="#27333d" stroke-width="2"/><text x="772" y="58" text-anchor="middle" font-size="16" font-weight="700">执行单元</text><text x="772" y="88" text-anchor="middle" font-size="12">Pack2 GEMM/BMM</text><text x="772" y="110" text-anchor="middle" font-size="12">FP16 add/mul/div</text><text x="772" y="132" text-anchor="middle" font-size="12">layout / im2col</text><text x="772" y="154" text-anchor="middle" font-size="12">embedding / action</text>
<rect x="914" y="80" width="146" height="76" fill="#ececec" stroke="#27333d" stroke-width="2"/><text x="987" y="110" text-anchor="middle" font-size="16" font-weight="700">CTX / DDR</text><text x="987" y="134" text-anchor="middle" font-size="12">结果和权重</text>
<path d="M168 118 H220" stroke="#29323a" stroke-width="3" marker-end="url(#a)"/><path d="M400 118 H452" stroke="#29323a" stroke-width="3" marker-end="url(#a)"/><path d="M630 118 H682" stroke="#29323a" stroke-width="3" marker-end="url(#a)"/><path d="M862 118 H914" stroke="#29323a" stroke-width="3" marker-end="url(#a)"/>
</svg><p class="small muted">这图怎么看：编译器现在能把完整事件送进不同执行单元，但执行单元有接口不等于已经完成每个算子的精确数学实现。</p></div>

<h2>2. 一次真实 trace 的覆盖情况</h2>
<div class="cols"><div><h3>执行单元数量</h3>{''.join(bar(k,v,max(units.values()),'#2b6cb0' if 'pack2' in k else '#79a96b') for k,v in units.items())}</div><div><h3>数字说明</h3><table><tr><th>项目</th><th>结果</th></tr><tr><td>dispatch / descriptor / command</td><td>{summary['source_dispatch_events']:,} / {summary['descriptor_count']:,} / {summary['instruction_count']:,}</td></tr><tr><td>numeric format</td><td>meta {summary['numeric_format_counts']['meta']:,}；FP16 {summary['numeric_format_counts']['fp16']:,}；INT8 {summary['numeric_format_counts']['int8']:,}</td></tr><tr><td>unknown</td><td class="ok">{summary['unknown_event_count']}</td></tr><tr><td>总周期</td><td>{total:,} cycles（Python 周期模型）</td></tr><tr><td>GEMM 利用率</td><td>{summary['gemm_utilization']*100:.2f}%</td></tr></table></div></div>
<p class="muted">这张图要注意：meta、layout 和 fallback 事件很多，所以完整模型的 PE 时间利用率只有 {summary['pe_time_utilization']*100:.2f}%。这不是 Pack2 阵列内部效率；Pack2 GEMM 区间的利用率是 {summary['gemm_utilization']*100:.2f}%。</p>

<h2>3. RTL 和 Vivado 证据</h2>
<table><tr><th>检查</th><th>结果</th><th>能证明什么</th></tr><tr><td>Icarus 完整 smoke</td><td class="ok">PASS</td><td>顶层握手、模块连接和旧兼容协议可运行</td></tr><tr><td>sideband FIFO</td><td class="ok">PASS</td><td>8 个 64-bit beat 逐位拼成 512-bit descriptor</td></tr><tr><td>2×2 BMM</td><td class="ok">PASS</td><td>双输入、transpose、scale 和输出顺序通过小例子</td></tr><tr><td>Vivado vendor FP16 综合</td><td class="ok">PASS</td><td>add/mul/div/exp/sqrt 五个 Xilinx IP 被顶层识别</td></tr><tr><td>4 ns 综合时序</td><td class="bad">WNS {esc(wns)}</td><td>仍不能称为 250 MHz；尚未完成完整布线</td></tr></table>
<table><tr><th>资源</th><th>综合值</th><th>解释</th></tr><tr><td>LUT</td><td>{esc(lut)}</td><td>包含 FP16 IP 和 v6 全模型 top</td></tr><tr><td>FF</td><td>{esc(ff)}</td><td>包含 sideband、BRAM 读寄存器和向量状态</td></tr><tr><td>DSP</td><td>{esc(dsp)}</td><td>768 个 Pack2 阵列 DSP，FP16/向量路径还增加了 DSP</td></tr><tr><td>BRAM</td><td>{esc(bram)} tiles</td><td>CTX/WRAM、scale/bias 和 IP 内部存储</td></tr></table>

<h2>4. 全模型还缺什么</h2>
<table><tr><th>模块</th><th>当前情况</th><th>还要补的工作</th></tr>
<tr><td>LayerNorm / Softmax / GELU / tanh</td><td>有向量接口；FP16 vendor IP 已能综合</td><td>把均值、方差、exp、倒数、mask、非线性串成精确数据流，并逐位对拍</td></tr>
<tr><td>DINO / 语言 encoder / action head</td><td>Linear 子层可拆成 GEMM descriptor</td><td>层循环、权重加载、残差、KV/cache 和完整中间张量流</td></tr>
<tr><td>BMM / attention</td><td>双输入 staging、transpose、scale、mask 已有小例子</td><td>QK/AV 两阶段调度、动态布局、真实输出接 Pack2 和全 trace 对拍</td></tr>
<tr><td>scale / bias / payload</td><td>有 numeric index 和 BRAM 表</td><td>加载真实校准值、偏置、权重和 activation payload；处理格式失配</td></tr>
<tr><td>layout</td><td>有部分 layout unit 和 descriptor</td><td>通用 transpose/permute/reshape/slice/cat/gather/scatter 地址生成与容量验证</td></tr>
<tr><td>DMA / AXI / DDR</td><td>有 AXI transaction shell</td><td>burst、DDR 控制器、带宽/背压、片上容量和板级约束</td></tr>
<tr><td>端到端验证</td><td>仅 smoke 和小 tile</td><td>全 trace Verilator、真实权重、FPGA 回放和 LIBERO W8A8 成功率</td></tr>
</table>

<h2>5. 下一步建议</h2>
<ol><li>先把 scale/bias/payload loader 接到 sideband 和 CTX/WRAM，避免继续用默认 1.0/零 bias。</li><li>把 FP16 vector 单元拆成 LayerNorm、Softmax 和 GELU 三条可独立对拍的流水线，再做寄存器边界优化。</li><li>完成 BMM 的 QK/AV 全链路和 layout DMA 后，再做 full-trace RTL 回放。</li><li>最后再做完整实现和板级 DDR；当前 4 ns WNS 为负，不能从综合报告直接宣称 250 MHz。</li></ol>
<p class="muted">页面中的周期和利用率来自 Python trace 模型；Icarus 是功能冒烟；Vivado 数字是综合结果。没有 SAIF/VCD、板级 DDR 和完整回放时，不报告 TOPS/W 或端到端延迟。</p>
</main></body></html>'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_text, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
