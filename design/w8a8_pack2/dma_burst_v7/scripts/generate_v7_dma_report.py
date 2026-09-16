"""Generate the v7 DMA-burst handoff page from machine-readable results.

The page intentionally separates compiler coverage, RTL smoke tests, synthesis
results, and the parts of full TurboVLA inference that are still missing.
"""
from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "2026-09-16_080520_dma_burst_compile"
V7 = ROOT / "hw" / "v7_2026-09-16_073705_dma_burst_memory_rtl"
OUT_ROOT = ROOT / "reports"


def esc(value: object) -> str:
    return html.escape(str(value))


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def bar(label: str, value: float, maximum: float, color: str) -> str:
    width = 2.0 if maximum <= 0 else max(2.0, min(100.0, 100.0 * value / maximum))
    return (
        f'<div class="barrow"><span>{esc(label)}</span><div class="bar">'
        f'<i style="width:{width:.2f}%;background:{color}"></i></div>'
        f'<b>{value:,.0f}</b></div>'
    )


def main() -> None:
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    human_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = load("cycle_summary.json")
    inv = load("operator_inventory.json")
    dma = load("dma_results.json")
    viv = load("vivado_v7_summary.json")
    matrix = load("support_matrix.json")
    units = summary["execution_unit_counts"]
    total = summary["total_cycles"]
    pe = summary["pe_time_utilization"] * 100.0
    gemm = summary["gemm_utilization"] * 100.0
    peak = summary["peak_gops_250mhz"]
    eff = summary["effective_gops_250mhz"]
    out_dir = OUT_ROOT / stamp
    out = out_dir / f"{stamp}_TurboVLA全模型v7_DMA突发与硬件支持状态.html"
    unit_html = "".join(
        bar(k, float(v), max(units.values()), "#2b6cb0" if "pack2" in k else "#7c9e69")
        for k, v in units.items()
    )
    support_html = "".join(
        f"<tr><td>{esc(row['module'])}</td><td>{esc(row['compiler'])}</td>"
        f"<td>{esc(row['rtl'])}</td><td>{esc(row['full_model'])}</td></tr>"
        for row in matrix["items"]
    )
    html_text = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{stamp} TurboVLA 全模型 v7 DMA 突发与硬件支持状态</title>
<style>
body{{margin:0;background:#f4f6f8;color:#20252b;font:15px/1.65 Arial,"Microsoft YaHei",sans-serif}}
main{{max-width:1220px;margin:0 auto;padding:26px 30px 56px}}
h1{{font-size:30px;line-height:1.25;margin:0 0 6px}} h2{{font-size:22px;margin:32px 0 10px;border-left:5px solid #2f6f9f;padding-left:10px}}
h3{{font-size:17px;margin:20px 0 7px}} p{{margin:8px 0}} .muted{{color:#65717d}}
.facts{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0}}
.fact{{background:#fff;border:1px solid #d7dde4;padding:13px 15px;border-radius:4px}} .fact b{{display:block;font-size:24px;color:#135d91}}
table{{border-collapse:collapse;width:100%;background:#fff;margin:9px 0 16px}} th,td{{border:1px solid #d7dde4;padding:7px 9px;text-align:left;vertical-align:top}} th{{background:#eaf0f5}}
.ok{{color:#126b42;font-weight:700}} .warn{{color:#9b5600;font-weight:700}} .bad{{color:#a62f2f;font-weight:700}}
.note{{background:#fff8e6;border-left:4px solid #d99b21;padding:10px 13px;margin:12px 0}}
.cols{{display:grid;grid-template-columns:1fr 1fr;gap:18px}} .barrow{{display:grid;grid-template-columns:170px 1fr 84px;gap:8px;align-items:center;margin:6px 0}}
.bar{{height:14px;background:#e4e8ed;border-radius:2px;overflow:hidden}} .bar i{{display:block;height:100%}}
.barrow b{{text-align:right;font-weight:600}} .diagram{{background:#fff;border:1px solid #cfd7df;padding:13px;margin:12px 0}}
.small{{font-size:13px}} code{{background:#eef1f4;padding:1px 4px;border-radius:3px}} li{{margin:5px 0}}
@media(max-width:760px){{main{{padding:17px 13px}}.facts{{grid-template-columns:repeat(2,1fr)}}.cols{{grid-template-columns:1fr}}h1{{font-size:24px}}table{{font-size:13px}}}}
</style></head><body><main>
<h1>TurboVLA 全模型 v7：DMA 突发路径和硬件支持状态</h1>
<p class="muted">生成时间：{human_stamp}　|　工作区：<code>turbovla_w8a8_pack2</code>　|　公共交接仓库：<code>nc-thu/turbovla-fpga-handoff</code></p>
<div class="note"><b>先看结论：</b>仓库已经设为公开。v7 的 DMA 单元和 64-bit 板级桥已经通过小规模 Verilator/Icarus 级功能检查，Vivado 综合也完成且 0 errors；但 4 ns 约束的 WNS 为 {viv['wns_ns']:.3f} ns，不能说已经达到 250 MHz。全模型仍缺真实 payload 装载、完整 BMM、精确 FP16 非线性、通用 layout、DINO/T5/action head 数据流和板级 DDR 回放。</div>
<div class="facts"><div class="fact"><span>公开仓库</span><b>是</b><small>nc-thu/turbovla-fpga-handoff</small></div><div class="fact"><span>v7 综合</span><b>0 errors</b><small>0 critical warnings</small></div><div class="fact"><span>综合资源</span><b>{viv['lut']:,} LUT</b><small>{viv['ff']:,} FF / {viv['dsp']:,} DSP / {viv['bram_tiles']} BRAM tile</small></div><div class="fact"><span>vectorless 功耗</span><b>{viv['power_w_vectorless']:.3f} W</b><small>低置信度，未做实现</small></div></div>

<h2>1. 这轮实际做了什么</h2>
<p>之前的 DMA 更像一个“每拍发一个地址”的接口壳。v7 改成了有限长度的 AXI burst。一次请求最多连续发 16 个 128-bit beat，并在 4 KB 边界处自动拆分。这样后面接 DDR 时，地址握手不会重复占用每个数据拍。</p>
<div class="diagram"><svg viewBox="0 0 1120 250" width="100%" role="img" aria-label="DMA burst data path">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#26323a"/></marker></defs>
<rect x="20" y="75" width="160" height="90" fill="#e5eff9" stroke="#26323a" stroke-width="2"/><text x="100" y="108" text-anchor="middle" font-size="17" font-weight="700">64-bit DDR 流</text><text x="100" y="133" text-anchor="middle" font-size="12">板级桥接接口</text>
<rect x="255" y="44" width="220" height="150" fill="#fff3d6" stroke="#26323a" stroke-width="2"/><text x="365" y="76" text-anchor="middle" font-size="17" font-weight="700">v7 package bridge</text><text x="365" y="106" text-anchor="middle" font-size="12">读：两拍拼 128 bit</text><text x="365" y="129" text-anchor="middle" font-size="12">写：128 bit 拆两拍</text><text x="365" y="152" text-anchor="middle" font-size="12">等待最后一对响应</text>
<rect x="550" y="44" width="220" height="150" fill="#e9f6e9" stroke="#26323a" stroke-width="2"/><text x="660" y="76" text-anchor="middle" font-size="17" font-weight="700">bounded-burst DMA</text><text x="660" y="106" text-anchor="middle" font-size="12">内部 128-bit beat</text><text x="660" y="129" text-anchor="middle" font-size="12">最多 16 beat</text><text x="660" y="152" text-anchor="middle" font-size="12">4 KB 边界 / 尾 strobe</text>
<rect x="845" y="75" width="250" height="90" fill="#fbe9dc" stroke="#26323a" stroke-width="2"/><text x="970" y="108" text-anchor="middle" font-size="17" font-weight="700">CTX / WRAM / AXI</text><text x="970" y="133" text-anchor="middle" font-size="12">数据最终还要接真实 payload FIFO</text>
<path d="M180 120 H255" stroke="#26323a" stroke-width="3" marker-end="url(#arrow)"/><path d="M475 120 H550" stroke="#26323a" stroke-width="3" marker-end="url(#arrow)"/><path d="M770 120 H845" stroke="#26323a" stroke-width="3" marker-end="url(#arrow)"/>
</svg><p class="small muted">这图怎么看：DMA 的地址和数据已经能成 burst 走通，但 package top 目前没有真实 128-bit payload 输入，所以内部 stream 用了确定性的零填充。这个 tie-off 只用于综合和握手验证，不代表生产数据已经从 DDR 进入 CTX/WRAM。</p></div>
<table><tr><th>检查</th><th>结果</th><th>说明</th></tr><tr><td>DMA standalone</td><td class="ok">PASS</td><td>80 B、最大 4 beat，读 5 beat / 写 5 beat，读 8 cycles / 写 9 cycles。</td></tr><tr><td>64-bit package bridge</td><td class="ok">PASS</td><td>10 个 64-bit 读 beat、10 个写 beat，5 个内部 128-bit 响应。</td></tr><tr><td>真实 trace 显式 DMA</td><td class="warn">0 个</td><td>编译器已经支持 DMA_READ/DMA_WRITE，但当前 trace 没有显式 DMA 事件，所以本轮周期总数没有因为 burst 变化。</td></tr></table>

<h2>2. 真实 TurboVLA trace 现在能编译到什么程度</h2>
<p>编译器读入一次真实 forward 的 {summary['source_dispatch_events']:,} 个 dispatch 和 {summary['source_module_events']:,} 个模块事件，输出 {summary['descriptor_count']:,} 个 descriptor 和 {summary['instruction_count']:,} 条 command。所有事件都有类别，所以 <code>unknown=0</code>。这个数字只表示“每个事件都被记账”，不表示每个事件都已经有精确 RTL。</p>
<div class="cols"><div><h3>执行单元数量</h3>{unit_html}</div><div><h3>这组数字意味着什么</h3><table><tr><th>项目</th><th>数值</th></tr><tr><td>Pack2 GEMM</td><td>{summary['execution_unit_counts']['pack2_gemm']:,} 个</td></tr><tr><td>Pack2 BMM</td><td>{summary['execution_unit_counts']['pack2_bmm']:,} 个</td></tr><tr><td>向量单元</td><td>{summary['execution_unit_counts']['fp16_vector']:,} 个</td></tr><tr><td>layout / meta</td><td>{summary['execution_unit_counts']['layout_engine']:,} / {summary['execution_unit_counts']['meta_engine']:,}</td></tr><tr><td>周期模型</td><td>{total:,} cycles，250 MHz 下约 {total/250_000_000*1000:.2f} ms</td></tr><tr><td>PE 时间利用率</td><td>{pe:.2f}%</td></tr><tr><td>GEMM 内部利用率</td><td>{gemm:.2f}%</td></tr><tr><td>完整模型有效吞吐</td><td>{eff:.2f} GOPS，峰值 {peak:.1f} GOPS 的 {100*eff/peak:.2f}%</td></tr></table></div></div>
<p class="muted">这张图要注意：GEMM 区间本身并不差，真正拉低完整模型结果的是大量 meta、layout、向量和行为级辅助事件。它们现在有周期预算，但还没有都变成能逐位处理真实张量的专用电路。</p>

<h2>3. 全模型还有哪些没有做成电路或没有被编译器完整支持</h2>
<table><tr><th>模块</th><th>编译器</th><th>RTL 当前状态</th><th>全模型还缺什么</th></tr>{support_html}</table>
<p class="small muted">编译器的“已分类”和 RTL 的“已实现”是两件不同的事。论文或架构报告只能把右侧明确标成“缺失”的部分写成后续工作，不能用 <code>unknown=0</code> 代替。</p>

<h2>4. Vivado 综合结果</h2>
<table><tr><th>资源/指标</th><th>v7 综合值</th><th>解释</th></tr><tr><td>器件 / top</td><td>{esc(viv['device'])}<br><code>{esc(viv['top'])}</code></td><td>package top，64-bit host/DDR stream。</td></tr><tr><td>时钟</td><td>4.000 ns / 250 MHz</td><td>WNS {viv['wns_ns']:.3f} ns、TNS {viv['tns_ns']:.3f} ns，setup 没有过。</td></tr><tr><td>LUT / FF</td><td>{viv['lut']:,} / {viv['ff']:,}</td><td>包含 Pack2、向量、控制、存储和 DMA burst 逻辑。</td></tr><tr><td>DSP</td><td>{viv['dsp']:,}</td><td>不是 768。除 Pack2 阵列外，向量和其它辅助乘法器也被综合成 DSP。</td></tr><tr><td>BRAM</td><td>{viv['bram_tiles']}</td><td>CTX/WRAM 和缓冲被推断为片上 RAM。</td></tr><tr><td>功耗</td><td>{viv['power_w_vectorless']:.3f} W</td><td>vectorless、低置信度，没有 SAIF/VCD，也没有 place/route。</td></tr></table>
<p class="small muted">报告来源：<code>hw/v7_2026-09-16_073705_dma_burst_memory_rtl/vivado/v7_synth_20260916_0810/</code>。Vivado 日志显示 synthesis 完成 0 errors、0 critical warnings；这不能替代实现后的布线时序和板卡 I/O 检查。</p>

<h2>5. 下一步按什么顺序补</h2>
<ol><li><b>真实 payload：</b>给 package top 增加 CTX/WRAM 的 128-bit 输入 FIFO，删除零填充 tie-off，并用实际 activation/weight beat 做读写回放。</li><li><b>精确向量：</b>把 LayerNorm、Softmax、GELU、tanh 的 vendor FP16 IP 接到已有控制接口，补均值、方差、mask、exp、倒数和饱和的逐位对拍。</li><li><b>完整 attention：</b>实现 BMM 的 QK、scale/mask、softmax、AV 和输出写回，不再只做 staging。</li><li><b>通用 layout：</b>补齐 reshape、permute、slice、cat、gather/scatter 的地址生成，并用真实 trace 的布局事件对账。</li><li><b>完整模型回放：</b>把 DINO/T5/action head 的权重加载、残差、层循环和中间张量接起来，再做 Verilator full trace 和 FPGA/DDR 运行。</li></ol>
<div class="note"><b>现在可以对外说什么：</b>公开仓库里已经有一条可综合的 TurboVLA W8A8 Pack2 顶层、一个可测试的 DMA burst 路径和一套能读真实 trace 的编译器。<b>现在不能说什么：</b>不能说完整 TurboVLA 已经在 FPGA 上运行，不能说 250 MHz 已通过，不能说有端到端 W8A8 LIBERO 成功率，也不能把 vectorless 功耗换算成 TOPS/W。</div>
<p class="muted">本页生成时间：{human_stamp}。数字来自 JSON、CSV、Icarus/Verilator 日志和 Vivado 报告；没有把估算值写成实测值。</p>
</main></body></html>"""
    out_dir.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
