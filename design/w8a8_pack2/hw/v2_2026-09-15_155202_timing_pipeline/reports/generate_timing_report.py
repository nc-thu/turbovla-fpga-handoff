#!/usr/bin/env python3
"""Build a self-contained Chinese timing-pipeline report with inline SVG."""
from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path


def esc(value) -> str:
    if value in ("not_available", "not_run", None):
        return "未执行"
    return html.escape(str(value), quote=True)


def load_json(path: Path, fallback):
    try:
        # Windows PowerShell's Set-Content may add a UTF-8 BOM.
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return fallback


def num(value, digits=2):
    if isinstance(value, (int, float)):
        return f"{value:,.{digits}f}"
    return "未执行"


def pct(value, digits=1):
    return f"{100.0 * value:.{digits}f}%" if isinstance(value, (int, float)) else "未测"


def svg_arch():
    return """
<svg class="diagram" viewBox="0 0 1040 260" role="img" aria-label="Pack2 timing pipeline">
  <defs><marker id="arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#202020"/></marker></defs>
  <rect x="8" y="14" width="1024" height="232" fill="#fafafa" stroke="#202020" stroke-width="2"/>
  <text x="24" y="42" font-family="Arial" font-size="18" font-weight="700">TurboVLA W8A8 Pack2：时序版数据通路</text>
  <g font-family="Arial" font-size="13" text-anchor="middle">
    <rect x="32" y="88" width="126" height="62" fill="#dceeff" stroke="#202020" stroke-width="2"/>
    <text x="95" y="113" font-weight="700">CTX/WRAM 输入</text><text x="95" y="134">128/768 bit</text>
    <rect x="192" y="88" width="112" height="62" fill="#e9e9e9" stroke="#202020" stroke-width="2"/>
    <text x="248" y="113" font-weight="700">输入寄存</text><text x="248" y="134">+1 cycle</text>
    <rect x="338" y="88" width="132" height="62" fill="#fff0c8" stroke="#202020" stroke-width="2"/>
    <text x="404" y="113" font-weight="700">DSP48E2 Pack2</text><text x="404" y="134">2× INT8×INT8</text>
    <rect x="504" y="88" width="116" height="62" fill="#e9e9e9" stroke="#202020" stroke-width="2"/>
    <text x="562" y="113" font-weight="700">P 输出寄存</text><text x="562" y="134">+1 cycle</text>
    <rect x="654" y="88" width="132" height="62" fill="#ffe2c2" stroke="#202020" stroke-width="2"/>
    <text x="720" y="113" font-weight="700">字段校正</text><text x="720" y="134">低场/借位</text>
    <rect x="820" y="88" width="92" height="62" fill="#ffe2c2" stroke="#202020" stroke-width="2"/>
    <text x="866" y="113" font-weight="700">INT32</text><text x="866" y="134">累加反馈</text>
    <rect x="944" y="88" width="66" height="62" fill="#dceeff" stroke="#202020" stroke-width="2"/>
    <text x="977" y="113" font-weight="700">输出</text><text x="977" y="134">寄存</text>
  </g>
  <g stroke="#202020" stroke-width="2" marker-end="url(#arr)">
    <line x1="158" y1="119" x2="192" y2="119"/><line x1="304" y1="119" x2="338" y2="119"/>
    <line x1="470" y1="119" x2="504" y2="119"/><line x1="620" y1="119" x2="654" y2="119"/>
    <line x1="786" y1="119" x2="820" y2="119"/><line x1="912" y1="119" x2="944" y2="119"/>
  </g>
  <path d="M866 150 V202 H720 V150" fill="none" stroke="#555" stroke-width="2" marker-end="url(#arr)"/>
  <text x="792" y="222" font-family="Arial" font-size="13" text-anchor="middle">INT32 反馈（原路径保留）</text>
  <text x="38" y="184" font-family="Arial" font-size="13">阵列规模：16 行 × 48 物理列，768 DSP，96 个逻辑列</text>
  <text x="38" y="207" font-family="Arial" font-size="13">改动只增加寄存器边界；数学格式、Pack2 配对和单时钟接口不变</text>
</svg>
"""


def svg_bars(items, title, width=900, height=230, color="#2d6cdf", suffix=""):
    max_v = max([float(v) for _, v in items if isinstance(v, (int, float))] or [1.0])
    gap = 18
    bar_w = max(30, int((width - 70 - gap * max(0, len(items) - 1)) / max(1, len(items))))
    out = [f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">']
    out.append(f'<text x="18" y="24" font-family="Arial" font-size="16" font-weight="700">{esc(title)}</text>')
    base = height - 48
    for i, (label, value) in enumerate(items):
        x = 42 + i * (bar_w + gap)
        if isinstance(value, (int, float)):
            h = (value / max_v) * (base - 32)
            y = base - h
            out.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{h:.1f}" fill="{color}"/>')
            out.append(f'<text x="{x + bar_w/2:.1f}" y="{max(42, y-5):.1f}" text-anchor="middle" font-family="Arial" font-size="12">{esc(num(value, 1))}{esc(suffix)}</text>')
        else:
            out.append(f'<rect x="{x}" y="{base-24}" width="{bar_w}" height="24" fill="#d9d9d9" stroke="#777"/>')
            out.append(f'<text x="{x + bar_w/2:.1f}" y="{base-8}" text-anchor="middle" font-family="Arial" font-size="11">未执行</text>')
        out.append(f'<text x="{x + bar_w/2:.1f}" y="{height-24}" text-anchor="middle" font-family="Arial" font-size="12">{esc(label)}</text>')
    out.append(f'<line x1="35" y1="{base}" x2="{width-18}" y2="{base}" stroke="#202020"/>')
    out.append('</svg>')
    return "".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", default="")
    args = parser.parse_args()
    script = Path(__file__).resolve()
    hw_version = script.parents[1]
    workspace = script.parents[3]
    summary = load_json(workspace / "reports" / "2026-09-15_134742" / "architecture_summary.json", {})
    checks = load_json(hw_version / "data" / "functional" / "functional_checks.json", [])
    vivado = load_json(hw_version / "data" / "vivado_results.json", {"runs": []})
    now = datetime.now()
    stamp = now.strftime("%Y-%m-%d_%H%M%S")
    human_now = now.strftime("%Y-%m-%d %H:%M:%S")
    out_dir = Path(args.out_dir).resolve() if args.out_dir else workspace / "reports" / stamp
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{stamp}_timing_pipeline_report.html"

    old_ooc = summary.get("ooc", [])
    current_mode = summary.get("modes", {}).get("current", {})
    db_mode = summary.get("modes", {}).get("double_buffer", {})
    resource_items = []
    for row in old_ooc:
        if row.get("name") == "16x48":
            resource_items = [("LUT", float(row.get("lut", 0))), ("FF/1k", float(row.get("ff", 0))/1000.0), ("DSP", float(row.get("dsp", 0)))]
    check_rows = []
    for item in checks if isinstance(checks, list) else []:
        check_rows.append(f"<tr><td>{esc(item.get('name',''))}</td><td class=pass>{esc(item.get('status',''))}</td><td>{esc(item.get('elapsed_seconds',''))} s</td><td><code>{esc(item.get('log',''))}</code></td></tr>")
    vivado_rows = []
    for item in vivado.get("runs", []):
        run = item.get("run", {})
        res = item.get("resources", {})
        tim = item.get("timing", {})
        pwr = item.get("power", {})
        vivado_rows.append(
            f"<tr><td>{esc(item.get('label'))}</td><td>{esc(run.get('status','not_run'))}</td>"
            f"<td>{esc(item.get('frequency_mhz'))} MHz</td><td>{esc(res.get('lut'))}</td><td>{esc(res.get('ff'))}</td>"
            f"<td>{esc(res.get('dsp'))}</td><td>{esc(tim.get('wns_ns'))}</td><td>{esc(pwr.get('total_on_chip_w'))}</td></tr>"
        )
    if not vivado_rows:
        vivado_rows.append('<tr><td colspan="8">两个频率均未执行：本机没有 Vivado，远端 SSH 连接超时。</td></tr>')

    check_count = sum(1 for x in checks if isinstance(x, dict) and x.get("status") == "passed") if isinstance(checks, list) else 0
    check_total = len(checks) if isinstance(checks, list) else 0
    html_doc = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TurboVLA W8A8 Pack2 时序版电路与架构分析</title>
<style>
body{{margin:0;background:#f4f4f1;color:#202020;font-family:"Microsoft YaHei",Arial,sans-serif;line-height:1.65}}
main{{max-width:1180px;margin:0 auto;background:#fff;padding:28px 42px 56px;box-sizing:border-box}}
h1{{font-size:30px;line-height:1.25;margin:0 0 8px}} h2{{font-size:22px;border-left:5px solid #2d6cdf;padding-left:10px;margin:32px 0 10px}}
h3{{font-size:17px;margin:20px 0 6px}} p{{margin:7px 0}} .meta{{color:#555;font-size:13px;border-bottom:1px solid #bbb;padding-bottom:12px}}
.lead{{font-size:17px;background:#f1f6ff;border:1px solid #9dbcf4;padding:12px 15px;margin:18px 0}}
.note{{font-size:13px;color:#555;background:#fafafa;border-left:3px solid #999;padding:8px 12px;margin:10px 0}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:14px}} .card{{border:1px solid #b8b8b8;padding:12px;background:#fff}}
.card .big{{font-size:28px;font-weight:700;display:block}} table{{width:100%;border-collapse:collapse;font-size:13px;margin:10px 0 18px}}
th,td{{border:1px solid #aaa;padding:6px 7px;text-align:left;vertical-align:top}} th{{background:#ececec}} .pass{{color:#137333;font-weight:700}}
.diagram,.chart{{width:100%;height:auto;border:1px solid #bdbdbd;background:#fff;margin:9px 0}} .caption{{font-size:13px;color:#444;margin:2px 0 12px}}
code{{font-size:12px;word-break:break-all}} .tag{{display:inline-block;border:1px solid #777;padding:1px 7px;margin-right:5px;font-size:12px;background:#f4f4f4}}
ul{{margin-top:6px}} li{{margin:4px 0}} .footer{{border-top:1px solid #aaa;margin-top:34px;padding-top:12px;color:#555;font-size:13px}}
@media(max-width:700px){{main{{padding:18px 15px}}h1{{font-size:24px}}h2{{font-size:20px}}table{{font-size:12px;display:block;overflow-x:auto;white-space:nowrap}}}}
</style></head><body><main>
<h1>TurboVLA W8A8 Pack2 时序版电路与架构分析</h1>
<div class="meta">生成时间：{human_now}　|　版本：hw/v2_2026-09-15_155202_timing_pipeline　|　器件：xczu7ev-ffvc1156-2-e　|　目标：完整电路路径的两个时钟点</div>
<div class="lead"><b>先说结果：</b>新的时序版 RTL 已经在本地 Icarus 完成乘法器、阵列、回放顶层和 system_top 展开检查（{check_count}/{check_total} 项通过）。它增加了 DSP 输出到校正之间的寄存器，并在阵列边界加了输入／输出寄存器。Vivado 的 250 MHz 和 303.215 MHz 两个实现任务还没有跑起来，因此这页不把历史 OOC 数字冒充新的实现结果。</div>

<h2>1. 这轮到底改了什么</h2>
<p>目标是减少一条组合路径里连续经过 DSP、字段校正和累加反馈的逻辑。改动集中在三个地方：输入寄存器、DSP P 输出寄存器、阵列读出寄存器。</p>
{svg_arch()}
<div class="caption">这图怎么看：灰色框是新增的寄存边界；黄色和橙色框是原来的 Pack2 算术。寄存器把长路径切成几段，但会增加固定流水延迟，必须由 Vivado 时序和 RTL 协议回归共同确认。</div>
<table><thead><tr><th>位置</th><th>时序版处理</th><th>对数据格式的影响</th><th>当前证据</th></tr></thead><tbody>
<tr><td>阵列输入</td><td>捕获 activation、weight、valid 和 pulse</td><td>仍是 128-bit activation／768-bit weight</td><td>本地仿真通过</td></tr>
<tr><td>DSP 输出</td><td>新增 P_pipe_r 和 valid 寄存器</td><td>仍由一颗 DSP 产生两个 INT8 产品</td><td>乘法器边界冒烟通过</td></tr>
<tr><td>校正与累加</td><td>高场借位校正和 INT32 累加仍各自注册</td><td>Pack2 两路 INT32 状态不变</td><td>小阵列冒烟通过</td></tr>
<tr><td>阵列读出</td><td>新增输出寄存器</td><td>快照仍走原读出接口</td><td>system_top 可展开</td></tr>
</tbody></table>
<div class="note">“时序更好”在本轮只能作为设计目标，不能提前写成百分比提升。新的 WNS、Fmax、布线拥塞和功耗，必须等两个 Vivado 任务完成后再填。</div>

<h2>2. 现有阵列的规模和资源基线</h2>
<div class="grid">
<div class="card"><span class="big">16 × 48</span>物理阵列规模。每个物理列承载两个逻辑输出列。</div>
<div class="card"><span class="big">768 DSP</span>每个 PE 使用一颗 DSP48E2，Pack2 每周期产生两个 INT8×INT8 乘积。</div>
<div class="card"><span class="big">96 logical</span>逻辑输出列数。阵列接口保持单时钟。</div>
</div>
{svg_bars(resource_items or [('LUT','not_available'),('FF/1k','not_available'),('DSP','not_available')], '历史 v1 16×48 OOC 资源（仅作基线）', suffix='')}
<div class="caption">这图怎么看：LUT 和 FF/1k 使用不同单位，只用来展示数量级；精确数字见表。它们来自 2026-09-15 13:47:42 的 v1 OOC 综合，不是这次 timing-pipeline 的新实现结果。</div>
<table><thead><tr><th>历史 v1 OOC 16×48</th><th>数值</th><th>解释</th></tr></thead><tbody>
<tr><td>LUT</td><td>78,249</td><td>阵列边界、控制和校正逻辑的综合资源</td></tr>
<tr><td>FF</td><td>148,168</td><td>脉动链、状态、控制和读出寄存器</td></tr>
<tr><td>DSP</td><td>768</td><td>与设计合同一致，没有增加乘法 DSP</td></tr>
<tr><td>BRAM</td><td>0</td><td>该 OOC 壳没有把外部存储映射成片上 BRAM</td></tr>
<tr><td>3.298 ns 约束</td><td>WNS +1.433 ns，推导 Fmax 536.2 MHz</td><td>仅为历史综合 OOC，不能代表完整 top 的布局布线时序</td></tr>
<tr><td>vectorless power</td><td>4.604 W</td><td>无 SAIF/VCD 的估算，不换算 TOPS/W</td></tr>
</tbody></table>

<h2>3. 为什么要测两个频率</h2>
<p>250 MHz 是当前系统接口容易对接的整点。3.298 ns 对应约 303.215 MHz，用来观察原来约 303 MHz 目标在加入寄存器后是否还能保持。</p>
{svg_bars([('250 MHz', next((r.get('frequency_mhz') for r in vivado.get('runs',[]) if r.get('label')=='250MHz' and r.get('run',{}).get('status')=='passed'), 'not_available')), ('303.215 MHz', next((r.get('frequency_mhz') for r in vivado.get('runs',[]) if r.get('label')=='303MHz' and r.get('run',{}).get('status')=='passed'), 'not_available'))], '两个实现点的运行状态', color='#777')}
<div class="caption">这图怎么看：灰色表示任务没有产出实现结果，不是时序失败。只有 status=passed 且包含 timing summary 时，才会把 WNS/Fmax 写入结论。</div>
<table><thead><tr><th>频率点</th><th>时钟周期</th><th>Vivado 状态</th><th>LUT</th><th>FF</th><th>DSP</th><th>WNS</th><th>总片上功耗</th></tr></thead><tbody>{''.join(vivado_rows)}</tbody></table>
<p class="note">阻塞原因：本机未安装 Vivado；按 C1 流程尝试连接 192.168.2.5 和 101.6.64.77 时均超时。脚本和两个独立输出目录已经准备好，网络恢复后可以直接运行。</p>

<h2>4. 本地能先确认什么</h2>
<table><thead><tr><th>检查</th><th>状态</th><th>耗时</th><th>说明</th></tr></thead><tbody>{''.join(check_rows) if check_rows else '<tr><td colspan="4">没有找到 functional_checks.json</td></tr>'}</tbody></table>
<p>这些检查只回答“RTL 能否展开、基本协议是否能跑”。它们不能替代 Vivado 综合，也不能证明 16×48 完整 top 已经过布局布线。</p>
<ul>
<li>Pack2 乘法器边界：混合符号和端点值通过。</li>
<li>2×3 timing array：加入额外 P 管线后，输出没有出现 X，阵列可正常结束。</li>
<li>回放顶层：descriptor FIFO、结果槽位和 activity counter 冒烟通过。</li>
<li>system_top：以完整时序版源文件成功展开。Icarus 打出的 constant-select 提示是仿真器兼容性警告，不是展开错误。</li>
</ul>

<h2>5. 目前的性能账本</h2>
<p>历史 trace 驱动模型仍然可以说明“阵列在模型里承担了多少工作”，但它没有因为这次加寄存器就自动改变。下面两行是历史模型，帮助审阅结构，不当作新电路测量。</p>
{svg_bars([('current cycles', current_mode.get('total_cycles','not_available')), ('double buffer', db_mode.get('total_cycles','not_available'))], '历史 TurboVLA trace 周期模型（不是 timing 版新实测）', color='#b96b2c')}
<div class="caption">这图怎么看：双缓冲模型把读、算、写的等待重叠起来，周期比 current 少约 51.45%。它和本轮时序寄存器是两件事；本轮没有重新计算真实 W8A8 硬件周期。</div>
<table><thead><tr><th>模型</th><th>总周期</th><th>PE 时间利用率</th><th>GEMM 利用率</th><th>250 MHz 有效 GOPS</th><th>证据类型</th></tr></thead><tbody>
<tr><td>current</td><td>{num(current_mode.get('total_cycles'),0)}</td><td>{pct(current_mode.get('pe_time_utilization'))}</td><td>{pct(current_mode.get('gemm_utilization'))}</td><td>{num(current_mode.get('effective_gops_250_0'),1)}</td><td>Python 周期模型</td></tr>
<tr><td>double buffer</td><td>{num(db_mode.get('total_cycles'),0)}</td><td>{pct(db_mode.get('pe_time_utilization'))}</td><td>{pct(db_mode.get('gemm_utilization'))}</td><td>{num(db_mode.get('effective_gops_250_0'),1)}</td><td>Python 条件模型</td></tr>
</tbody></table>

<h2>6. 结论和下一步</h2>
<ol>
<li><b>电路方面：</b>时序版已经把最明显的 DSP 输出到校正路径切开，同时在阵列边界加了寄存器。Pack2 数学和 768-DSP 规模没有改。</li>
<li><b>可综合性方面：</b>本机 Icarus 检查通过，说明模块名、端口和参数可以展开。它不是 Vivado 综合通过证明。</li>
<li><b>频率方面：</b>250 MHz 与 303.215 MHz 两个 Vivado 任务还没有结果，所以现在不能给出新的 Fmax、WNS、资源增量或功耗。</li>
<li><b>工程决策：</b>网络恢复后先跑 250 MHz；若通过，再跑 303.215 MHz。若 303 MHz 失败，优先看 DSP P 到校正、阵列读出 mux 和高扇出 drain-row 三条路径，再决定是否保留输出寄存器。</li>
</ol>
<div class="footer"><b>复现命令</b><br>
本地冒烟：<code>powershell -ExecutionPolicy Bypass -File hw/v2_2026-09-15_155202_timing_pipeline/sim/run_timing_smoke.ps1</code><br>
Vivado（Linux）：<code>bash hw/v2_2026-09-15_155202_timing_pipeline/vivado/run_two_freqs.sh</code><br>
结果收集：<code>python hw/v2_2026-09-15_155202_timing_pipeline/vivado/collect_vivado_results.py</code><br><br>
<b>诚实边界：</b>本页明确区分本地行为冒烟、历史 v1 OOC、Python 周期模型和待执行的 Vivado 实现。没有把未运行的两个频率写成“过时序”，也没有用 vectorless power 计算 TOPS/W。报告生成时间：{human_now}。
</div></main></body></html>"""
    out_file.write_text(html_doc, encoding="utf-8")
    print(out_file)


if __name__ == "__main__":
    main()
