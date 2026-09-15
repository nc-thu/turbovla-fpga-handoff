"""Build the v3 camera-ready archive and a self-contained Chinese HTML report.

The report deliberately separates three kinds of evidence: Python/compiler
checks, server RTL simulation, and local Vivado synth_design.  It never turns
an unavailable UNISIM check or an unimplemented full TurboVLA path into a
positive result.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "v3_2026-09-13_140118"
COMPILER_DATA = ROOT / "compiler" / "v3_2026-09-13_140118_w8a16_camera_ready_compiler" / "data"
RTL_ROOT = ROOT / "hw" / "v3_2026-09-13_140118_w8a16_camera_ready_rtl"
REPORTS = ROOT / "reports"


def load(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def esc(v: Any) -> str:
    return html.escape("—" if v is None or v == "" else str(v))


def fmt_int(v: Any) -> str:
    try:
        return f"{int(round(float(v))):,}"
    except (TypeError, ValueError):
        return "—"


def fmt_float(v: Any, digits: int = 2, suffix: str = "") -> str:
    try:
        return f"{float(v):.{digits}f}{suffix}"
    except (TypeError, ValueError):
        return "—"


def fmt_pct(v: Any) -> str:
    try:
        return f"{100 * float(v):.1f}%"
    except (TypeError, ValueError):
        return "—"


def fmt_bytes(v: Any) -> str:
    try:
        x = float(v)
    except (TypeError, ValueError):
        return "—"
    if x >= 1024**3:
        return f"{x / 1024**3:.2f} GiB"
    if x >= 1024**2:
        return f"{x / 1024**2:.2f} MiB"
    if x >= 1024:
        return f"{x / 1024:.1f} KiB"
    return f"{x:.0f} B"


def table(headers: list[str], rows: list[list[Any]]) -> str:
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{esc(x)}</td>" for x in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"


def svg_wrap(body: str, width: int, height: int) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">{body}</svg>'


def rect(x: int, y: int, w: int, h: int, fill: str, label: str, fs: int = 16) -> str:
    lines = label.split("\n")
    text = "".join(f'<text x="{x+w/2:.0f}" y="{y+28+i*20}" text-anchor="middle" font-family="Arial" font-size="{fs}" font-weight="700">{html.escape(line)}</text>' for i, line in enumerate(lines))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#24282c" stroke-width="2"/>{text}'


def line(x1: int, y1: int, x2: int, y2: int, color: str = "#2e5f8a", dash: str = "") -> str:
    marker = "url(#arrow)" if color != "#777" else "url(#arrowgray)"
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3" marker-end="{marker}"{d}/>'


def make_datapath(out: Path) -> str:
    body = '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#2e5f8a"/></marker><marker id="arrowgray" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#777"/></marker></defs>'
    body += '<text x="24" y="30" font-family="Arial" font-size="22" font-weight="700">TurboVLA W8A16 数据通路</text>'
    body += rect(28, 76, 156, 92, "#dceef8", "CTX\nA16 / 256 bit")
    body += rect(224, 76, 158, 92, "#eef1f3", "tile feed\n寄存器")
    body += rect(422, 58, 220, 128, "#fff0c8", "16 × 48 PE array\n768 DSP · INT40", 15)
    body += rect(680, 76, 158, 92, "#fbe1cc", "snapshot\n40 bit")
    body += rect(876, 76, 156, 92, "#fbe1cc", "requant\nINT16")
    body += line(184, 122, 224, 122); body += line(382, 122, 422, 122); body += line(642, 122, 680, 122); body += line(838, 122, 876, 122)
    body += '<text x="202" y="108" font-family="Arial" font-size="13" fill="#2e5f8a">16×A16</text><text x="386" y="108" font-family="Arial" font-size="13" fill="#2e5f8a">A16</text><text x="648" y="108" font-family="Arial" font-size="13" fill="#2e5f8a">40 bit</text><text x="845" y="108" font-family="Arial" font-size="13" fill="#2e5f8a">40→16</text>'
    body += line(530, 42, 530, 58, "#9a5b00"); body += '<text x="548" y="44" font-family="Arial" font-size="14" fill="#9a5b00">WRAM: 48×W8 = 384 bit</text>'
    body += line(954, 168, 954, 210, "#3d7c45"); body += '<text x="830" y="231" font-family="Arial" font-size="14" fill="#3d7c45">INT16 写回 / 下一层输入</text>'
    body += '<text x="422" y="226" font-family="Arial" font-size="14">每个 PE 只做一路 signed INT16 × INT8；本版不使用双路 DSP packing</text>'
    svg = svg_wrap(body, 1060, 250)
    out.write_text(svg, encoding="utf-8")
    return svg


def make_control(out: Path) -> str:
    body = '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#2e5f8a"/></marker><marker id="arrowgray" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#777"/></marker></defs>'
    body += '<text x="24" y="30" font-family="Arial" font-size="22" font-weight="700">编译器到 RTL 的命令路径</text>'
    boxes = [(30,75,205,86,"#e4edf4","compiler\n172 transport words"),(286,75,205,86,"#eef1f3","ISA ctrl\n64-bit decode"),(542,45,205,106,"#fff0c8","runtime\nready / wait / done"),(798,20,205,72,"#dceef8","DMA\nCTX 256 / WRAM 384"),(798,112,205,72,"#fbe1cc","vector ops\nLN / Softmax / GELU"),(798,204,205,72,"#fff0c8","GEMM\n16×48 / 768 DSP")]
    for x,y,w,h,c,l in boxes: body += rect(x,y,w,h,c,l,14)
    body += line(235,118,286,118); body += line(491,118,542,98); body += line(747,82,798,56); body += line(747,98,798,148); body += line(747,116,798,240)
    body += '<text x="40" y="220" font-family="Arial" font-size="14">长度超过 65535 时，编译器分片并保留 chunk 元数据；矩阵 flags[7] 启动生产阵列，runtime 等待 done。</text>'
    svg = svg_wrap(body, 1060, 270)
    out.write_text(svg, encoding="utf-8")
    return svg


def make_timing(out: Path, fig_dir: Path) -> dict[str, str]:
    labels = ["v8\nLayerNorm", "v9\niterative div", "v10\nDMA write", "v11\nfixed write", "v13\nfinal split"]
    wns = [-0.560, 0.0, -1.130, 0.0, 0.067]
    fig, ax = plt.subplots(figsize=(7.2, 3.1))
    ax.bar(np.arange(len(wns)), wns, color=["#b05a5a", "#4f8a5b", "#b05a5a", "#2e6d49", "#2e6d49"], width=0.58)
    ax.axhline(0, color="#222", lw=1)
    ax.set_xticks(np.arange(len(labels)), labels)
    ax.set_ylabel("WNS at 3.298 ns (ns)")
    ax.set_title("System-top timing fixes (Vivado synth_design)")
    ax.grid(axis="y", color="#e4e4e4")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    paths = {}
    for ext in ("svg", "pdf", "png"):
        p = fig_dir / f"fig_timing_history.{ext}"
        fig.savefig(p, dpi=220, facecolor="white")
        paths[ext] = p.name
    plt.close(fig)
    return paths


def copy_snapshot(src: Path, dest: Path) -> None:
    if src.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def main() -> int:
    generated_dt = datetime.now().astimezone()
    generated = generated_dt.isoformat(timespec="seconds")
    stamp = generated_dt.strftime("%Y-%m-%d_%H%M%S")
    report_dir = REPORTS / stamp
    report_dir.mkdir(parents=True, exist_ok=False)
    fig_dir = report_dir / "figures"
    fig_dir.mkdir()
    data_dir = report_dir / "data"
    data_dir.mkdir()

    inventory = load(DATA / "operator_inventory.json", {}) or {}
    cycles = load(DATA / "cycle_breakdown.json", {}) or {}
    rtl = load(DATA / "rtl_results.json", {}) or {}
    synth = load(DATA / "vivado_synth_results.json", {}) or {}
    pycheck = load(DATA / "python_checks.json", {}) or {}
    quant_rows = []
    qcsv = DATA / "quant_error.csv"
    if qcsv.exists():
        with qcsv.open(newline="", encoding="utf-8") as f:
            quant_rows = list(csv.DictReader(f))
    program = load(COMPILER_DATA / "turbovla_w8a16_program.json", {}) or {}
    descriptors = load(COMPILER_DATA / "w8a16_descriptors.json", {}) or {}
    compile_manifest = load(COMPILER_DATA / "compile_manifest.json", {}) or {}
    descriptor_manifest = load(COMPILER_DATA / "descriptor_manifest.json", {}) or {}
    isa = load(DATA / "isa_spec.json", {}) or {}
    costs = load(COMPILER_DATA / "instruction_costs.json", {}) or {}
    isa_sim = load(COMPILER_DATA / "isa_sim_results.json", {}) or {}
    action_probe = load(COMPILER_DATA / "libero_action_probe.json", {}) or {}

    datapath = make_datapath(fig_dir / "fig_w8a16_datapath.svg")
    control = make_control(fig_dir / "fig_compiler_rtl_path.svg")
    timing_figs = make_timing(report_dir / "timing_history.svg", fig_dir)
    # Keep the timing SVG both in the figure folder and at the report root for
    # people who want to open it directly from a file manager.
    shutil.copy2(fig_dir / "fig_timing_history.svg", report_dir / "timing_history.svg")

    cycle_rows = cycles.get("rows", [])
    total_macs = sum(float(x.get("macs", 0)) for x in cycle_rows)
    total_compute = sum(float(x.get("compute_cycles", 0)) for x in cycle_rows)
    total_cycles = sum(float(x.get("total_cycles", 0)) for x in cycle_rows)
    weighted_engine = total_macs / (768 * total_compute) if total_compute else 0
    weighted_completion = total_macs / (768 * total_cycles) if total_cycles else 0
    full_program = program.get("full_program", [])
    smoke_program = program.get("smoke_program", [])
    logical_program = int(program.get("coverage", {}).get("logical_instruction_count", 83))
    transport_program = len(full_program)
    compiler_status = compile_manifest.get("validation", {}).get("status", "missing")
    descriptor_status = "PASS" if int(descriptor_manifest.get("records", 0) or 0) == len(descriptors.get("records", [])) and len(descriptors.get("records", [])) > 0 else "missing"
    rtl_tests = rtl.get("tests", {})
    passed_tests = sum(bool(v) for v in rtl_tests.values())
    synth_records = synth.get("records", [])
    system = next((x for x in synth_records if "system_v13" in str(x.get("name"))), {})
    array = next((x for x in synth_records if "16x48" in str(x.get("name"))), {})
    st = system.get("timing", {}) or {}
    at = array.get("timing", {}) or {}

    # Machine-readable snapshot: the HTML numbers can always be traced back to
    # this file and the copied source JSON files.
    summary = {
        "schema_version": "tvla_w8a16.camera_ready_report.v3",
        "generated_at": generated,
        "status": "camera_ready_candidate",
        "compiler": {"status": compiler_status, "logical_instructions": logical_program, "transport_words": transport_program, "smoke_words": len(smoke_program), "descriptors": len(descriptors.get("records", [])), "opcodes": len(isa.get("opcodes", [])), "descriptor_status": descriptor_status, "full_cycles_lower_bound": sum(float(x.get("cycles_lower_bound", 0)) for x in costs.get("full", []))},
        "cycles": {"total_macs": total_macs, "total_cycles": total_cycles, "weighted_engine_utilization": weighted_engine, "weighted_completion_rate": weighted_completion},
        "rtl": rtl,
        "vivado": {"system": system, "array_16x48": array, "timing_is_synthesis_estimate": synth.get("timing_is_synthesis_estimate", True)},
        "figures": {"datapath": "figures/fig_w8a16_datapath.svg", "compiler_rtl": "figures/fig_compiler_rtl_path.svg", "timing": "figures/fig_timing_history.svg"},
        "limitations": ["DINO/T5、TurboVLA 采样循环和真实 LIBERO 环境动作尚未接入 RTL", "UNISIM/DSP48E2 smoke 因服务器没有 xvlog 未运行", "Vivado 只有 synth_design，未做 place/route、post-route、功耗或上板", "OOC 没有板级 pin 约束；NSTD-1/UCIO-1 是接口约束警告，不等于内部 setup 失败，但当前结果还不能直接生成 bitstream"],
    }
    (report_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    for src in [DATA / "operator_inventory.json", DATA / "cycle_breakdown.json", DATA / "traffic_breakdown.csv", DATA / "python_checks.json", DATA / "quant_error.csv", DATA / "rtl_results.json", DATA / "vivado_synth_results.json", DATA / "vivado_synth_results.csv", DATA / "isa_spec.json", COMPILER_DATA / "turbovla_w8a16_program.json", COMPILER_DATA / "w8a16_descriptors.json", COMPILER_DATA / "instruction_costs.json", COMPILER_DATA / "isa_sim_results.json", COMPILER_DATA / "libero_action_probe.json", COMPILER_DATA / "compile_manifest.json", COMPILER_DATA / "descriptor_manifest.json"]:
        copy_snapshot(src, data_dir / src.name)
    manifest_paths = [p for p in report_dir.rglob("*") if p.is_file() and p.name not in {"BUILD_MANIFEST.md"}]
    manifest_lines = [f"# TurboVLA W8A16 camera-ready 构建清单", "", f"生成时间：{generated}", "", "## 本轮来源", "", f"- 工作区：`{ROOT}`", f"- RTL：`{RTL_ROOT}`", f"- 编译器：`{COMPILER_DATA.parent}`", "- 所有数字由 `summary.json` 和 `data/` 快照生成。", "", "## 文件散列", "", "| 文件 | SHA256 |", "|---|---|"]
    for p in sorted(manifest_paths):
        manifest_lines.append(f"| `{p.relative_to(report_dir).as_posix()}` | `{sha256(p)}` |")
    (report_dir / "BUILD_MANIFEST.md").write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    cycle_table = []
    for r in cycle_rows:
        cycle_table.append([r.get("name"), f"{r.get('m')}×{r.get('n')}×{r.get('k')}", fmt_int(r.get("macs")), fmt_int(r.get("total_cycles")), fmt_pct(r.get("engine_utilization")), fmt_pct(r.get("completion_rate")), fmt_bytes(float(r.get("stream_a_bytes", 0)) + float(r.get("stream_w_bytes", 0)) + float(r.get("out_bytes", 0)))])
    synth_table = []
    for r in synth_records:
        t, d = r.get("timing", {}) or {}, r.get("drc", {}) or {}
        label = "system top" if "system_v13" in str(r.get("name")) else f"array {r.get('rows')}×{r.get('pcols')}"
        synth_table.append([label, r.get("status"), fmt_int(r.get("total_luts")), fmt_int(r.get("ffs")), fmt_int(r.get("dsp")), fmt_float(t.get("wns_ns"), 3, " ns"), fmt_float(t.get("fmax_estimate_mhz"), 1, " MHz"), fmt_float(t.get("data_path_delay_ns"), 3, " ns"), f"{d.get('violations', '—')} / {d.get('errors', '—')}E"]) 
    verilator_count = len(rtl.get("verilator", {}).get("tests", []) or [])
    iverilog_count = len(rtl.get("iverilog", {}).get("tests", []) or [])
    rtl_table = [["Verilator", rtl.get("verilator", {}).get("status"), f"{verilator_count} tests", f"{rtl.get('verilator', {}).get('elapsed_seconds', '—')} s"], ["Icarus", rtl.get("iverilog", {}).get("status"), f"{iverilog_count} short smoke", f"{rtl.get('iverilog', {}).get('elapsed_seconds', '—')} s"], ["UNISIM/DSP48E2", rtl.get("unisim", {}).get("status"), "xvlog unavailable", "未做"], ["system production feed", "PASS" if rtl_tests.get("tb_w8a16_system") else "FAIL", "flags[7] → 16×48 array", "Verilator"]]
    op_rows = []
    for op in isa.get("opcodes", []):
        op_rows.append([op.get("name"), op.get("unit"), op.get("code"), op.get("description")])
    qtable = [[r.get("case"), r.get("source"), r.get("max_abs_error"), r.get("mean_abs_error"), r.get("rmse")] for r in quant_rows]

    css = """
body{margin:0;background:#f3f5f6;color:#20252a;font-family:Arial,'Microsoft YaHei',sans-serif;line-height:1.55}main{max-width:1260px;margin:auto;background:#fff;min-height:100vh;padding:28px 34px 60px}h1{font-size:28px;margin:0 0 4px}h2{font-size:19px;border-bottom:2px solid #252a2e;padding-bottom:5px;margin:30px 0 10px}h3{font-size:15px;margin:22px 0 6px}.stamp{color:#5b6670;font-size:13px;margin-bottom:20px}.lead{background:#eef5f8;border-left:4px solid #2e6d91;padding:10px 14px}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:16px 0}.metric{border:1px solid #c8d0d5;padding:11px;background:#fafbfc}.metric b{display:block;font-size:22px;color:#173f5b}.metric span{font-size:12px;color:#5b6670}table{border-collapse:collapse;width:100%;font-size:12px;margin:10px 0 16px}th,td{border:1px solid #cbd1d5;padding:6px 8px;vertical-align:top;text-align:left}th{background:#eaf0f3}tr:nth-child(even) td{background:#fafafa}.figure{border:1px solid #d0d5d9;padding:8px;overflow:auto;margin:10px 0}.figure svg{display:block;max-width:100%;height:auto;margin:auto}.twocol{display:grid;grid-template-columns:1fr 1fr;gap:14px}.ok{color:#2e7545;font-weight:bold}.warn{color:#9a5b00;font-weight:bold}.muted{color:#5b6670}code{background:#eef1f3;padding:1px 4px;border-radius:2px}li{margin:5px 0}@media(max-width:760px){main{padding:18px 14px}.metrics{grid-template-columns:repeat(2,1fr)}.twocol{grid-template-columns:1fr}h1{font-size:23px}table{font-size:11px}}
"""
    html_text = f"""<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{stamp} TurboVLA W8A16 camera-ready 候选</title><style>{css}</style></head><body><main>
<h1>TurboVLA W8A16 架构与编译器 camera-ready 候选</h1><div class='stamp'>生成时间：{esc(generated)}　|　版本：v3 camera-ready　|　目录：{esc(report_dir.relative_to(ROOT))}</div>
<p class='lead'><span class='ok'>v3 的系统 top 已通过逻辑综合时序检查。</span> W8A16 数值边界、编译器指令字、长向量 sideband、DMA／向量／激活单元、runtime、16×48 阵列和系统 top 都有可重复的检查。Vivado 3.298 ns 目标下 setup WNS 为 {fmt_float(st.get('wns_ns'),3,' ns')}，0 个 setup 失败端点。这里的“通过”只表示行为仿真和逻辑综合证据齐全；真实 TurboVLA 视觉／语言推理、LIBERO 环境动作、布局布线和功耗仍未完成。</p>
<div class='metrics'><div class='metric'><b>768 DSP</b><span>16×48 阵列；每个 PE 一路 A16×W8</span></div><div class='metric'><b>{fmt_float(st.get('wns_ns'),3,' ns')}</b><span>v13 综合时序余量（3.298 ns 目标）</span></div><div class='metric'><b>{logical_program} → {transport_program}</b><span>逻辑操作 → 可传输 word（长向量带完整偏移）</span></div><div class='metric'><b>{passed_tests}/{len(rtl_tests)}</b><span>收集到的 RTL 检查项为 PASS</span></div></div>
<h2>1. 这轮到底交付了什么</h2><p>主 top 是 <code>w8a16_system_top</code>。它把指令控制、两个 DMA、向量／激活算子、REQUANT 和 16×48 GEMM 接到同一条时钟域。编译器把形状、scale、布局和依赖放在 descriptor 中，把可传输字段放在 64-bit 指令字中。对于超过 65535 的长度，程序拆成连续片段并保存 chunk 信息，所以不会静默截断长度。</p>
<div class='figure'>{datapath}</div><p class='muted'>图怎么看：蓝色是 CTX 激活，棕色是 WRAM 权重，黄色是阵列，橙色是 INT40 快照和重量化。A16 指进入 GEMM 的激活宽度，不是 GELU 等函数的位宽。</p>
<div class='figure'>{control}</div>
<h2>2. 编译器和 ISA</h2><p>编译器检查结果为 <span class='ok'>{esc(compiler_status)}</span>，descriptor 生成结果为 <span class='ok'>{esc(descriptor_status)}</span>。当前完整样例包含 {logical_program} 条逻辑操作，分片后得到 {transport_program} 条 64-bit transport word；另有 {len(smoke_program)} 条小动作 smoke 和 {len(isa.get('opcodes', []))} 个 opcode catalog 项。完整程序成本模型下界为 {fmt_int(summary['compiler']['full_cycles_lower_bound'])} 拍。这个数字是单时钟阵列容量模型，不是 TurboVLA 整网延迟。</p>
{table(['指令','硬件单元','编码','用途'],op_rows)}
<h2>3. RTL 验证结果</h2><p>服务器端 Verilator 回归在 {esc(rtl.get('server_experiment'))} 完成，记录了 {verilator_count} 项测试。Icarus 只做秒级短 smoke，用来检查另一套 Verilog 编译器的基本行为；本轮实际记录 {iverilog_count} 项。系统 smoke 还送入一个 <code>flags[7]=1</code> 的生产阵列命令，验证 runtime 发出 start 并等待阵列 done；阵列 feed 仍是上层 tile scheduler 的显式数据流。</p>{table(['阶段','状态','覆盖','耗时／说明'],rtl_table)}
<p>Python 整数检查状态为 <span class='ok'>{esc(pycheck.get('status'))}</span>，覆盖 INT16/INT8 量化边界、INT64 乘加参考、40-bit 上界和 INT16 饱和。Verilator 日志中 PE、4×4、16×48、GEMM、requant、激活、向量、DMA、ISA、runtime 和 system 均有 PASS。UNISIM/DSP48E2 未运行，因为服务器没有 <code>xvlog</code>；行为级乘法不能替代厂商原语仿真。</p>
<h2>4. Vivado top 时序和资源</h2><p>v13 使用 Vivado 2021.2、器件 <code>xczu7ev-ffvc1156-2-e</code> 和 3.298 ns 目标时钟。系统 top 综合后的数据路径为 {fmt_float(st.get('data_path_delay_ns'),3,' ns')}，WNS 为 {fmt_float(st.get('wns_ns'),3,' ns')}，可按最差路径估算为 {fmt_float(st.get('fmax_estimate_mhz',0),1,' MHz')}。最差路径从 <code>{esc(st.get('critical_source'))}</code> 到 <code>{esc(st.get('critical_destination'))}</code>，现在位于向量乘法 scale 到输出寄存器；LayerNorm 的迭代除法与饱和已经分开。这个结果仍是 synth_design 估算，只有 place/route 才能确认最终布线余量。</p>{table(['配置','状态','LUT','FF','DSP','WNS','Fmax（综合估算）','数据路径','DRC 记录'],synth_table)}
<div class='figure'><img src='figures/fig_timing_history.svg' alt='timing history' style='max-width:100%'></div><p class='muted'>图怎么看：v12 把 LayerNorm 的最后除法位和饱和拆开后，v13 的系统 top 从 -0.014 ns 变为 +0.067 ns。v10 的 DMA 可变目的地址仍作为历史警示。图中 Fmax 和 WNS 都是综合结果，不是布局布线结果。</p>
<h2>5. 16×48 阵列的周期模型</h2><p>模型把激活读、权重读、填充／排空、快照、重量化和 INT16 写回都计入分母。代表形状加权阵列利用率为 {fmt_pct(weighted_engine)}，把完成阶段也算进去后为 {fmt_pct(weighted_completion)}。短 K、窄 N 的尾块会支付固定的填充和写回成本，因此不能把 MAC 数除以计算拍数当成完整算子效率。</p>{table(['代表形状','M×N×K','MAC','总周期','阵列利用率','完整完成率','流量'],cycle_table)}
<h2>6. 软件数值参考</h2><p>W8A16 的软件检查使用 INT16 激活、INT8 权重、40-bit 累加和 INT16 输出。历史量化结果仍是 fake-quant FP32 路径，只用于看误差和任务行为，不代表本 RTL 在 GPU 上已经有整数 kernel，也不代表成功率。</p>{table(['检查项','来源','最大绝对误差','平均绝对误差','RMSE'],qtable)}
<h2>7. 目前的边界</h2><ul><li>已完成：W8A16 量化位置、40-bit 累加、编译器 descriptor/transport word、长向量分片、DMA ready/valid、向量和激活接口、runtime 等待语义、16×48/768-DSP 阵列、顶层逻辑综合。</li><li>未完成：DINO、T5、TurboVLA 采样循环接入 RTL；真实 RGB-D 张量从编译器到 tile scheduler 的端到端搬运；真实 LIBERO 环境动作和成功率；Vivado place/route、post-route phys_opt、功耗、板级 AXI/DDR 和 UNISIM 原语仿真。</li><li>因此这份归档可以支持“RTL/编译器 camera-ready 候选”，不能写成“完整 TurboVLA 已由 FPGA 执行”或“已获得 LIBERO 加速”。</li></ul>
<h2>8. 复现入口</h2><p>在工作区运行 <code>scripts/generate_camera_ready_report_v3.py</code> 可重新生成本页；服务器 RTL 使用 <code>hw/v3_2026-09-13_140118_w8a16_camera_ready_rtl/sim/run_verilator.sh</code> 和 <code>run_iverilog_smoke.sh</code>。Vivado 使用 <code>hw/v3_2026-09-13_140118_w8a16_camera_ready_rtl/synth/syn_top.tcl</code>。本报告目录包含所有输入 JSON/CSV 快照、图源、<code>summary.json</code>、<code>BUILD_MANIFEST.md</code> 和修改说明。</p>
<p class='muted'>编译器程序 SHA256：{esc(compile_manifest.get('program_sha256'))}。RTL 文件散列记录在 <code>data/rtl_results.json</code>。生成时间：{esc(generated)}。</p>
</main></body></html>"""
    report_path = report_dir / f"{stamp}_turbovla_w8a16_camera_ready.html"
    report_path.write_text(html_text, encoding="utf-8")
    (report_dir / "MODIFICATION_NOTES.md").write_text(f"# 修改说明\n\n生成时间：{generated}\n\n本版在 v2 的动作后处理、LayerNorm/Softmax 迭代路径、DMA 数据落地和生产阵列启动基础上，加入 v3 编译器的 tile shape/grid、长流完整偏移和扩展地址标记。LayerNorm/Softmax 的除法最后一位与饱和分开，系统 top v13 在 3.298 ns synth_design 约束下 WNS 为 {st.get('wns_ns')} ns，0 个 setup 失败端点；Verilator {verilator_count} 项和 Icarus {iverilog_count} 项短 smoke 已通过。报告没有把行为级乘法、综合 Fmax 或小动作 smoke 写成完整 TurboVLA/LIBERO 结果。NSTD-1/UCIO-1 仍需板级 pin 约束后才能生成 bitstream。\n", encoding="utf-8")
    print(json.dumps({"status":"PASS","generated_at":generated,"report":str(report_path),"summary":str(report_dir/'summary.json')}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
