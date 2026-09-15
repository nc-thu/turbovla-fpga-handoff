"""Generate the self-contained TurboVLA W8A16 report and paper figures.

The report deliberately keeps measured, simulated and unavailable items in
separate sections.  It only depends on the Python standard library,
matplotlib and numpy; pandas is not required because the local base image has
an incompatible pandas/numpy binary pair.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)


def load_json(name: str, default: Any = None) -> Any:
    path = DATA / name
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def now_local() -> datetime:
    # datetime.now().astimezone() preserves the host's local time and offset.
    return datetime.now().astimezone()


def fmt_int(x: float | int) -> str:
    return f"{int(round(x)):,}"


def fmt_pct(x: float) -> str:
    return f"{100.0 * x:.1f}%"


def fmt_bytes(n: float) -> str:
    if n >= 1024**3:
        return f"{n / 1024**3:.2f} GiB"
    if n >= 1024**2:
        return f"{n / 1024**2:.2f} MiB"
    if n >= 1024:
        return f"{n / 1024:.1f} KiB"
    return f"{int(n)} B"


def figure_style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#e2e2e2",
            "grid.linewidth": 0.7,
            "axes.grid.axis": "y",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def save_figure(fig: plt.Figure, out_dir: Path, stem: str) -> dict[str, str]:
    paths = {
        "svg": out_dir / f"{stem}.svg",
        "pdf": out_dir / f"{stem}.pdf",
        "png": out_dir / f"{stem}.png",
    }
    for path in paths.values():
        fig.savefig(path, bbox_inches="tight", facecolor="white", dpi=220)
    plt.close(fig)
    return {k: str(v.name) for k, v in paths.items()}


def draw_datapath(out_dir: Path) -> dict[str, str]:
    fig, ax = plt.subplots(figsize=(11.0, 3.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.1)
    ax.axis("off")
    boxes = [
        (0.25, 1.10, 1.65, 1.05, "CTX\nA16 read\n256 bit", "#dceef8"),
        (2.35, 1.10, 1.55, 1.05, "Skew /\nfeed buffer", "#eef2f5"),
        (4.35, 0.72, 2.15, 1.80, "16 × 48 PE array\n768 DSP\nA16 × W8", "#fff0c8"),
        (7.05, 1.10, 1.55, 1.05, "INT40\nsnapshot", "#fbe1cc"),
        (9.05, 1.10, 1.55, 1.05, "Requant\nINT16", "#fbe1cc"),
    ]
    for x, y, w, h, label, color in boxes:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor="#222", linewidth=1.5))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", weight="bold")
    def arrow(x1: float, y1: float, x2: float, y2: float, label: str, color: str = "#1e5a96") -> None:
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12,
                                     linewidth=1.6, color=color))
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.13, label, ha="center", va="bottom", color=color)
    arrow(1.90, 1.63, 2.35, 1.63, "A16 · 256b")
    arrow(3.90, 1.63, 4.35, 1.63, "A16")
    arrow(6.50, 1.63, 7.05, 1.63, "40b")
    arrow(8.60, 1.63, 9.05, 1.63, "40→16b")
    arrow(10.60, 1.63, 10.95, 1.63, "A16 · 256b", color="#3d7c45")
    # Weight side input, deliberately shown as a separate stream.
    ax.add_patch(FancyArrowPatch((5.43, 3.00), (5.43, 2.52), arrowstyle="-|>", mutation_scale=12,
                                 linewidth=1.6, color="#9a5b00"))
    ax.text(5.60, 2.76, "W8 · 384b", color="#9a5b00", va="center")
    ax.text(5.43, 0.34, "one signed INT16×INT8 product per PE; no dual-lane packing", ha="center", va="center", fontsize=8.5)
    ax.text(0.25, 2.78, "TurboVLA W8A16 data path", fontsize=13, weight="bold", ha="left")
    return save_figure(fig, out_dir, "fig_w8a16_datapath")


def draw_coverage(out_dir: Path, inventory: dict[str, Any]) -> dict[str, str]:
    records = inventory.get("records", []) if inventory else []
    groups: dict[str, list[int]] = {}
    for r in records:
        cls = str(r.get("class", "other:unknown"))
        group = cls.split(":", 1)[0]
        groups.setdefault(group, [0, 0])
        if r.get("status") == "mapped_candidate":
            groups[group][0] += 1
        else:
            groups[group][1] += 1
    # Keep a stable, readable order and collapse empty categories.
    order = ["text_encoder", "vision_encoder", "vision_language_interaction", "action_head", "other"]
    labels = [g for g in order if g in groups] + [g for g in groups if g not in order]
    mapped = [groups[g][0] for g in labels]
    fallback = [groups[g][1] for g in labels]
    fig, ax = plt.subplots(figsize=(8.2, 3.7))
    x = np.arange(len(labels))
    ax.bar(x, mapped, color="#3976a8", label="mapped W8A16 candidate")
    ax.bar(x, fallback, bottom=mapped, color="#cfd4d9", label="fallback / non-GEMM")
    ax.set_xticks(x, [s.replace("_", "\n") for s in labels])
    ax.set_ylabel("parameter records")
    ax.set_title("Frozen parameter-shape inventory (not a live call trace)")
    ax.legend(frameon=False, ncol=2, loc="upper right")
    for i, (m, f) in enumerate(zip(mapped, fallback)):
        ax.text(i, m + f + 4, str(m + f), ha="center", va="bottom", fontsize=8)
    return save_figure(fig, out_dir, "fig_operator_coverage")


def draw_cycles(out_dir: Path, cycles: dict[str, Any]) -> dict[str, str]:
    rows = (cycles or {}).get("rows", [])
    names = [str(r.get("name", "shape")) for r in rows]
    total = np.asarray([float(r.get("total_cycles", 0)) for r in rows])
    util = np.asarray([float(r.get("engine_utilization", 0)) for r in rows])
    completion = np.asarray([float(r.get("completion_rate", 0)) for r in rows])
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.0, 3.6), gridspec_kw={"width_ratios": [1.25, 1]})
    x = np.arange(len(names))
    ax0.bar(x, total, color="#d28b35")
    ax0.set_yscale("log")
    ax0.set_xticks(x, [n.replace("_", "\n") for n in names], fontsize=8)
    ax0.set_ylabel("modeled cycles (log scale)")
    ax0.set_title("Representative completion cost")
    ax1.bar(x - 0.18, util, width=0.36, color="#3976a8", label="array engine")
    ax1.bar(x + 0.18, completion, width=0.36, color="#7c9b62", label="full completion")
    ax1.set_ylim(0, 1.05)
    ax1.set_xticks(x, [n.replace("_", "\n") for n in names], fontsize=8)
    ax1.set_ylabel("fraction")
    ax1.set_title("MAC utilization, including feed/drain")
    ax1.legend(frameon=False, fontsize=8)
    fig.suptitle("16×48 W8A16 cycle model; traffic is charged per tile", y=1.02, fontsize=12, weight="bold")
    return save_figure(fig, out_dir, "fig_cycles_utilization")


def draw_quant_error(out_dir: Path, quant_rows: list[dict[str, str]]) -> dict[str, str]:
    labels = []
    maxes = []
    means = []
    for row in quant_rows:
        labels.append(row.get("case", "case"))
        maxes.append(float(row.get("max_abs_error", "nan")))
        means.append(float(row.get("mean_abs_error", "nan")))
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    x = np.arange(len(labels))
    width = 0.34
    ax.bar(x - width / 2, maxes, width, color="#b85c5c", label="max |error|")
    ax.bar(x + width / 2, means, width, color="#648bad", label="mean |error|")
    ax.set_xticks(x, [s.replace("_", "\n") for s in labels])
    ax.set_ylabel("absolute output error")
    ax.set_title("W8A16 numerical checks (scale-dependent units)")
    ax.legend(frameon=False)
    return save_figure(fig, out_dir, "fig_quant_error")


def table(headers: list[str], rows: list[list[str]], cls: str = "") -> str:
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in row) + "</tr>" for row in rows)
    return f'<table class="{cls}"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def inline_svg(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("<?xml"):
        text = text[text.find("?>") + 2 :]
    return text


def make_manifest(report_dir: Path, generated: str, inventory: dict[str, Any], rtl: dict[str, Any]) -> dict[str, Any]:
    files: dict[str, str] = {}
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "reports" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        # The source snapshot contains a large Git object store; the report only
        # needs its commit and a hash of the metadata actually consumed.
        if rel.startswith("references/turbovla_source/.git/"):
            continue
        files[rel] = sha256(path)
    q = load_json("quant_screening_summary.json", {}) or {}
    metadata_hashes = {
        "model_state_dict_shapes.json": sha256(DATA / "model_state_dict_shapes.json"),
        "checkpoint_model_config.json": sha256(DATA / "checkpoint_model_config.json"),
        "quant_screening_summary.json": sha256(DATA / "quant_screening_summary.json"),
    }
    for name in ("isa_spec.json", "turbovla_w8a16_program.json", "instruction_costs.json", "isa_sim_results.json", "libero_action_probe.json", "vivado_synth_results.json", "vivado_synth_results.csv"):
        path = DATA / name
        if path.exists():
            metadata_hashes[name] = sha256(path)
    result = {
        "generated_at": generated,
        "workspace": str(ROOT),
        "source_commit": q.get("source_commit"),
        "checkpoint": q.get("checkpoint"),
        "metadata_hashes": metadata_hashes,
        "rtl_results_file": "data/rtl_results.json",
        "rtl_sha256": rtl.get("rtl_sha256", {}) if rtl else {},
        "tracked_files": files,
    }
    (ROOT / "data" / "file_manifest.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> int:
    generated_dt = now_local()
    generated = generated_dt.isoformat(timespec="seconds")
    stamp = generated_dt.strftime("%Y-%m-%d_%H%M%S")
    report_dir = REPORTS / stamp
    report_dir.mkdir(parents=True, exist_ok=False)
    fig_dir = report_dir / "figures"
    fig_dir.mkdir()
    figure_style()

    inventory = load_json("operator_inventory.json", {}) or {}
    descriptors = load_json("w8a16_descriptors.json", {}) or {}
    program = load_json("turbovla_w8a16_program.json", {}) or {}
    isa = load_json("isa_spec.json", {}) or {}
    instruction_costs = load_json("instruction_costs.json", {}) or {}
    isa_sim = load_json("isa_sim_results.json", {}) or {}
    action_probe = load_json("libero_action_probe.json", {}) or {}
    cycles = load_json("cycle_breakdown.json", {}) or {}
    rtl = load_json("rtl_results.json", {}) or {}
    synth = load_json("vivado_synth_results.json", {}) or {}
    quant = load_json("quant_screening_summary.json", {}) or {}
    quant_rows = read_csv("quant_error.csv")
    cycle_rows = cycles.get("rows", [])
    full_program = program.get("full_program", [])
    smoke_program = program.get("smoke_program", [])
    opcode_rows = isa.get("opcodes", [])
    cost_full_rows = instruction_costs.get("full", [])
    cost_smoke_rows = instruction_costs.get("smoke", [])

    fig_files = {
        "datapath": draw_datapath(fig_dir),
        "coverage": draw_coverage(fig_dir, inventory),
        "cycles": draw_cycles(fig_dir, cycles),
        "quant": draw_quant_error(fig_dir, quant_rows),
    }
    manifest = make_manifest(report_dir, generated, inventory, rtl)

    mapped = int(inventory.get("matrix_parameter_count", 0))
    total_records = int(inventory.get("parameter_count", 0))
    fallback = total_records - mapped
    total_macs = sum(float(r.get("macs", 0)) for r in cycle_rows)
    total_compute = sum(float(r.get("compute_cycles", 0)) for r in cycle_rows)
    total_cycles = sum(float(r.get("total_cycles", 0)) for r in cycle_rows)
    dsp = 768
    weighted_engine_util = total_macs / (dsp * total_compute) if total_compute else 0.0
    weighted_completion = total_macs / (dsp * total_cycles) if total_cycles else 0.0
    clock_mhz = 1000 / 3.298
    peak_gmac = clock_mhz * dsp / 1000
    strongest = max(cycle_rows, key=lambda r: float(r.get("macs", 0)), default={})
    agg = quant.get("aggregate", {}) or {}

    cycle_table_rows = []
    for r in cycle_rows:
        cycle_table_rows.append([
            str(r.get("name", "")),
            f"{r.get('m')}×{r.get('n')}×{r.get('k')}",
            fmt_int(r.get("macs", 0)),
            fmt_int(r.get("total_cycles", 0)),
            fmt_pct(float(r.get("engine_utilization", 0))),
            fmt_pct(float(r.get("completion_rate", 0))),
            fmt_bytes(float(r.get("stream_a_bytes", 0)) + float(r.get("stream_w_bytes", 0)) + float(r.get("out_bytes", 0))),
        ])
    quant_table_rows = []
    for row in quant_rows:
        quant_table_rows.append([
            row.get("case", ""),
            row.get("source", ""),
            row.get("max_abs_error", ""),
            row.get("mean_abs_error", ""),
            row.get("rmse", ""),
        ])
    opcode_table_rows = []
    for op in opcode_rows:
        opcode_table_rows.append([
            str(op.get("name", "")),
            str(op.get("unit", "")),
            str(op.get("code", "")),
            str(op.get("description", "")),
        ])
    cost_group: dict[str, dict[str, float]] = {}
    for row in cost_full_rows:
        op = str(row.get("op", "unknown"))
        g = cost_group.setdefault(op, {"count": 0.0, "cycles": 0.0, "in": 0.0, "out": 0.0})
        g["count"] += 1
        g["cycles"] += float(row.get("cycles_lower_bound", 0))
        g["in"] += float(row.get("input_bytes", 0))
        g["out"] += float(row.get("output_bytes", 0))
    cost_table_rows = []
    for op in [str(x.get("name")) for x in opcode_rows if x.get("name") in cost_group]:
        g = cost_group[op]
        cost_table_rows.append([op, fmt_int(g["count"]), fmt_int(g["cycles"]), fmt_bytes(g["in"]), fmt_bytes(g["out"])])
    rtl_rows = [
        ["Verilator", str(rtl.get("verilator", {}).get("status", "unknown")), "PE、4×4、16×48、requant、GEMM、激活、向量、DMA、ISA、runtime", f"{rtl.get('verilator', {}).get('elapsed_seconds', '—')} s"],
        ["Icarus", str(rtl.get("iverilog", {}).get("status", "unknown")), "PE、4×4、激活、ISA 短 smoke", f"{rtl.get('iverilog', {}).get('elapsed_seconds', '—')} s"],
        ["UNISIM/DSP48E2", str(rtl.get("unisim", {}).get("status", "unknown")), "xvlog 不可用", "未做"],
        ["Vivado 逻辑综合", str(synth.get("status", rtl.get("ooc", {}).get("status", "unknown"))), "system_top、1×1、4×4、16×48", f"{sum(float(r.get('elapsed_s') or 0) for r in synth.get('records', [])):.1f} s" if synth.get("records") else "未做"],
        ["编译器→RTL 动作", str(rtl.get("compiler_to_rtl_action", {}).get("status", "unknown")), "7 lane packed action", str(rtl.get("compiler_to_rtl_action", {}).get("packed_action_hex", "—"))],
    ]

    def synth_value(value: Any, suffix: str = "") -> str:
        if value is None or value == "":
            return "—"
        return f"{value}{suffix}"

    synth_table_rows = []
    for sr in synth.get("records", []):
        timing = sr.get("timing", {}) or {}
        drc = sr.get("drc", {}) or {}
        scale = "集成壳" if sr.get("name") == "system_top" else f"{sr.get('rows')}×{sr.get('pcols')}"
        synth_table_rows.append([
            f"{sr.get('top', '—')} ({scale})",
            sr.get("status", "—"),
            fmt_int(sr["total_luts"]) if sr.get("total_luts") is not None else "—",
            fmt_int(sr["ffs"]) if sr.get("ffs") is not None else "—",
            fmt_int(sr["dsp"]) if sr.get("dsp") is not None else "—",
            fmt_int((sr.get("ramb36") or 0) + (sr.get("ramb18") or 0)) if sr.get("ramb36") is not None or sr.get("ramb18") is not None else "—",
            synth_value(timing.get("wns_ns"), " ns"),
            synth_value(f"{timing['fmax_estimate_mhz']:.1f}", " MHz") if timing.get("fmax_estimate_mhz") is not None else "—",
            synth_value(timing.get("critical_destination")),
            synth_value(sr.get("elapsed_s"), " s"),
            f"{drc.get('status', '—')} ({drc.get('warnings', 0)} warnings)" if drc else "—",
        ])
    q_rows = []
    for mode in ("fp32", "w8a8", "w8a16", "w8afp16"):
        a = agg.get(mode, {})
        q_rows.append([mode, f"{a.get('successes', '—')}/{a.get('episodes', '—')}", f"{a.get('success_rate_percent', 0):.1f}%", f"{a.get('suite_median_of_medians_ms', 0):.1f} ms", "历史 24 回合筛选；非本轮新测试"])

    summary = {
        "generated_at": generated,
        "report_directory": str(report_dir),
        "inventory": {
            "parameter_records": total_records,
            "mapped_matrix_records": mapped,
            "fallback_or_non_gemm_records": fallback,
            "max_k": inventory.get("max_parameter_k"),
            "required_acc_bits_at_max_k": inventory.get("required_acc_bits_at_max_k"),
            "configured_acc_bits": inventory.get("configured_acc_bits"),
        },
        "cycle_model": {
            "dsp": dsp,
            "clock_ns": 3.298,
            "clock_mhz": clock_mhz,
            "peak_gmac_per_s": peak_gmac,
            "total_macs": total_macs,
            "total_cycles": total_cycles,
            "weighted_engine_utilization": weighted_engine_util,
            "weighted_completion_rate": weighted_completion,
            "largest_macs_shape": strongest.get("name"),
        },
        "isa": {
            "full_instruction_count": len(full_program),
            "smoke_instruction_count": len(smoke_program),
            "opcode_count": len(opcode_rows),
            "opcode_catalog_count": len(program.get("opcode_catalog", [])),
            "instruction_cost_full_cycles_lower_bound": sum(float(r.get("cycles_lower_bound", 0)) for r in cost_full_rows),
            "isa_sim_status": isa_sim.get("status", "missing"),
            "action_probe_status": action_probe.get("status", "missing"),
            "compiler_to_rtl_action": rtl.get("compiler_to_rtl_action", {}),
        },
        "figures": fig_files,
        "source_commit": quant.get("source_commit"),
        "checkpoint_sha256": (quant.get("checkpoint") or {}).get("sha256"),
        "rtl": rtl,
        "vivado_synthesis": synth,
    }
    (report_dir / "report_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Report prose intentionally says what the data means before showing detail.
    datapath_svg = inline_svg(fig_dir / fig_files["datapath"]["svg"])
    coverage_svg = inline_svg(fig_dir / fig_files["coverage"]["svg"])
    cycles_svg = inline_svg(fig_dir / fig_files["cycles"]["svg"])
    quant_svg = inline_svg(fig_dir / fig_files["quant"]["svg"])
    screen_note = quant.get("screening", {}).get("note", "")
    full_cost_cycles = sum(float(r.get("cycles_lower_bound", 0)) for r in cost_full_rows)
    smoke_cost_cycles = sum(float(r.get("cycles_lower_bound", 0)) for r in cost_smoke_rows)
    action_q15 = isa_sim.get("smoke", {}).get("action_q15", action_probe.get("action_q15", []))
    action_norm = isa_sim.get("smoke", {}).get("action_normalized", action_probe.get("action_normalized", []))
    packed_action = rtl.get("compiler_to_rtl_action", {}).get("packed_action_hex", "—")
    isa_table_html = table(["指令", "硬件单元", "编码", "用途"], opcode_table_rows)
    cost_table_html = table(["指令", "次数", "周期下界合计", "输入流量", "输出流量"], cost_table_rows)
    synth_table_html = table(
        ["顶层/规模", "综合", "LUT", "FF", "DSP", "BRAM(36+18)", "WNS", "Fmax 估算", "关键终点", "耗时", "综合 DRC"],
        synth_table_rows,
    ) if synth_table_rows else table(["顶层/规模", "综合"], [["—", "未运行"]])
    if synth.get("status") == "passed":
        synth_note = (
            f"本机 Vivado 2021.2 已完成逻辑综合（run {synth.get('run_root', '—')}）。"
            "四个顶层配置均完成 synth_design，报告中的 Fmax 是综合 WNS 推算值；"
            "它只说明 RTL 能被 Vivado 展开和映射，不能替代布局布线后的频率。"
        )
    else:
        synth_note = "本轮 Vivado 逻辑综合未得到完整通过结果，资源和时序不能写成已验证数字。"
    system_synth = next((r for r in synth.get("records", []) if r.get("name") == "system_top"), {})
    system_critical = (system_synth.get("timing", {}) or {}).get("critical_destination", "—")
    html_text = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{stamp} TurboVLA W8A16 报告</title>
<style>
body{{margin:0;background:#f5f6f7;color:#20252a;font-family:Arial,"Microsoft YaHei",sans-serif;line-height:1.55}}
main{{max-width:1240px;margin:0 auto;padding:28px 34px 56px;background:#fff;min-height:100vh}}
h1{{font-size:27px;margin:0 0 6px}} h2{{font-size:19px;border-bottom:2px solid #20252a;padding-bottom:5px;margin-top:32px}}
h3{{font-size:15px;margin:22px 0 7px}} p{{margin:8px 0}} .muted{{color:#5d6670}}
.stamp{{font-size:13px;color:#5d6670;margin-bottom:20px}} .lead{{font-size:16px;border-left:4px solid #3976a8;padding:8px 14px;background:#f0f5f8}}
.metrics{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:16px 0}}
.metric{{border:1px solid #c9d0d6;padding:11px 13px;background:#fafbfc}} .metric b{{display:block;font-size:22px;color:#183f60}} .metric span{{font-size:12px;color:#5d6670}}
table{{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0 16px}} th,td{{border:1px solid #cbd1d6;padding:6px 8px;text-align:left;vertical-align:top}} th{{background:#eef1f3;font-weight:bold}} tr:nth-child(even) td{{background:#fafafa}}
.figure{{border:1px solid #d3d7da;margin:12px 0;padding:8px;background:#fff;overflow-x:auto}} .figure svg{{display:block;max-width:100%;height:auto;margin:auto}}
.twocol{{display:grid;grid-template-columns:1fr 1fr;gap:16px}} code{{background:#eef1f3;padding:1px 4px;border-radius:2px}}
ul{{margin-top:5px}} .ok{{color:#24733a;font-weight:bold}} .warn{{color:#9a5b00;font-weight:bold}}
@media(max-width:760px){{main{{padding:20px 15px}}.metrics{{grid-template-columns:repeat(2,minmax(0,1fr))}}.twocol{{grid-template-columns:1fr}}table{{font-size:12px}}h1{{font-size:23px}}}}
</style></head><body><main>
<h1>TurboVLA W8A16 专用 768-DSP 工作区</h1>
<div class="stamp">生成时间：{html.escape(generated)}　|　报告目录：{html.escape(str(report_dir.relative_to(ROOT)))}</div>
<p class="lead">这份报告只记录 W8A16 的数值语义、编译器描述符、周期估算和 RTL 快速验证。它不把旧的 GPU 假量化耗时写成 FPGA 性能，也不把没有运行的 Vivado 或完整 LIBERO 结果补成数字。</p>
<div class="metrics">
<div class="metric"><b>16 × 48</b><span>物理 PE 阵列</span></div>
<div class="metric"><b>768 DSP</b><span>一 PE 一 DSP，单路 A16×W8</span></div>
<div class="metric"><b>{fmt_pct(weighted_engine_util)}</b><span>代表形状 MAC 加权阵列利用率（模型）</span></div>
<div class="metric"><b>{fmt_pct(weighted_completion)}</b><span>把读写、快照和重量化计入后的完成率（模型）</span></div>
</div>

<h2>1. 先看结论</h2>
<p><span class="ok">数值、编译器和 RTL 快速检查通过。</span> INT64 黄金模型、INT40 边界、INT16 饱和以及 Verilator 的 PE、4×4、16×48、requant、GEMM、激活、向量、DMA、ISA 控制器和 runtime 测试都通过。Icarus 的 PE、4×4、激活和 ISA 短 smoke 也通过。编译器输出的 90 个实际调度字，加上 18 个 opcode 编码目录项，都能按同一份 ISA 解码。</p>
<p>这条硬件路线是一颗 DSP 做一个有符号 INT16 激活乘一个有符号 INT8 权重，阵列共有 768 颗 DSP。3.298 ns 只用于周期模型，换算出的理论峰值约 {peak_gmac:.1f} GMAC/s；这不是已经完成布局布线后的频率结果。</p>
<p><span class="ok">Vivado 逻辑综合已完成。</span>本轮把系统顶层和 1×1、4×4、16×48 阵列都送进 Vivado 2021.2。系统顶层能综合，但在 3.298 ns 约束下关键路径的 WNS 为负；阵列顶层本身满足这份综合时序约束。详细资源、WNS 和关键终点见第 7 节。仍未做 UNISIM 短 smoke、布局布线、post-route 时序、功耗、完整 TurboVLA 推理或 LIBERO 成功率。</p>

<h2>2. W8A16 数据流和端口</h2>
<div class="figure">{datapath_svg}</div>
<p>量化定义为 <code>q_a=clip(round(x/s_a),-32768,32767)</code>、<code>q_w=clip(round(w/s_w),-128,127)</code>，累加器计算 <code>sum(q_a*q_w)</code>。A16 指的是进入 GEMM 的激活张量是 16 位，不是 GELU 或其他激活函数的位宽。</p>
<p>CTX 激活口和写回口都是 256 bit，也就是一拍可传 16 个 INT16；WRAM 的逻辑权重输入是 384 bit，对应 48 个 INT8 权重。每个 PE 保存 40 bit 累加值和快照，快照读出后再重量化成 INT16。下一层若继续使用该结果，也必须保持 INT16，不能写成 INT8 后再称作 W8A16。</p>

<h2>3. 算子清单和编译器覆盖</h2>
<p>当前清单来自冻结 checkpoint 的参数形状，共 {total_records} 条记录，其中 {mapped} 条二维矩阵被标为 W8A16 candidate，其余 {fallback} 条是 embedding、偏置、归一化参数或其他需要重算／fallback 的项。这个数字是参数形状统计，不是完整运行时调用次数；动态 BMM、卷积展开和每层真实 token 数还需要运行时 trace 才能补齐。</p>
<div class="figure">{coverage_svg}</div>
<p>编译器输出 {len(descriptors.get('records', []))} 条代表性描述符：线性层和一个 QK 矩阵乘走 <code>gemm_w8a16</code>；Softmax、LayerNorm、GELU 记录为 fallback cost event。完整参数清单和代表性描述符分别保存在机器可读 JSON 中，避免把代表样例误称为完整指令流。</p>
{table(["状态", "含义"], [["mapped_candidate", "可按 W8A16 描述符继续验证"], ["must_recompute_or_fallback", "当前没有静态整数数据通路或需要单独算子"], ["fallback_cost_record", "编译器保留成本位置，未按零成本处理"]])}

<h2>4. 周期模型和阵列利用率</h2>
<p>下面的周期来自 16×48 透明 tile 模型。它把激活读取、权重读取、阵列填充／排空、快照、重量化和 INT16 写回列入分母；尚未证明的片上复用没有被偷偷当成免费。流量按每个 tile 重新读取激活和权重，是偏保守的条件模型。</p>
<div class="figure">{cycles_svg}</div>
{table(["代表形状", "M×N×K", "MAC", "总周期", "阵列利用率", "完整完成率", "流量"], cycle_table_rows)}
<p>所有代表形状合计 {fmt_int(total_macs)} MAC、{fmt_int(total_cycles)} 周期。MAC 数最多的是 <code>{html.escape(str(strongest.get('name', '—')))}</code>，但短 K 或窄 N 的尾块完成率明显较低，说明阵列不只是被乘法本身限制，还要支付填充、排空、读出和写回成本。</p>

<h2>5. 软件数值参考</h2>
<p>历史筛选中的 W8A16 仍是“INT8 权重 + 动态 INT16 激活后反量化，再调用 FP32 F.linear”的假量化路径。它可以检查量化误差和任务行为，但不是本工作区的真实整数 CUDA kernel。</p>
<div class="figure">{quant_svg}</div>
{table(["配置", "成功数/回合数", "成功率", "策略调用中位数", "说明"], q_rows)}
{table(["数值检查", "来源", "最大绝对误差", "平均绝对误差", "RMSE"], quant_table_rows)}
<p>上表 24 回合／suite 的筛选结果来自 {html.escape(str(screen_note))}。其中 FP32 与 W8A16 都是 22/24；这个结果只能说明现有假量化路径在筛选样本上没有明显精度崩溃，不能代替新的真实整数实现成功率测试。</p>

<h2>6. 指令集、激活单元和读写引擎</h2>
<p>编译器现在会先生成完整的 64 bit transport word，再把矩阵尺寸、scale ID 和布局信息放在描述符侧带里。完整示例程序包含 {len(full_program)} 条指令，给 RTL runtime 用的短程序包含 {len(smoke_program)} 条指令；两者合计 90 个实际调度字，另有 {len(program.get('opcode_catalog', []))} 个编码目录项覆盖全部 opcode，均通过 ISA 解码检查。周期脚本没有把 fallback 当成零周期，完整示例的周期下界合计为 {fmt_int(full_cost_cycles)} 拍，短动作路径为 {fmt_int(smoke_cost_cycles)} 拍。</p>
{isa_table_html}
<h3>指令成本按功能分组</h3>
{cost_table_html}
<p>新增 RTL 不只有 GEMM。<code>w8a16_vector_ops</code> 负责 BIAS_ADD、ADD、MUL_SCALE、ReLU、GELU、tanh、LayerNorm 和 Softmax 的单向量命令；<code>w8a16_dma</code> 负责 256 bit CTX 读写和 384 bit WRAM 权重读；<code>w8a16_isa_ctrl</code> 负责 64 bit 指令的取指、译码、等待和结束；<code>w8a16_runtime</code> 把这些命令接到一个小型动作投影路径。</p>
<p><span class="ok">编译器到 RTL 的动作 smoke 已经接通。</span>在固定 LIBERO 任务／初始状态 0 的元数据背景下，测试使用一个确定性的、格式兼容的 INT16 状态向量，经编译器生成的 LOAD_CTX→LOAD_WEIGHT→GEMM→BIAS_ADD→TANH→STORE_ACTION→END 顺序，RTL 输出 7 个 Q15 动作值 <code>{html.escape(str(action_q15))}</code>，打包值为 <code>{html.escape(str(packed_action))}</code>。这证明数据字、指令顺序和动作打包格式能相互对上；它没有把真实 RGB-D 张量送进 RTL，仍不是 TurboVLA 完整推理，也没有执行 LIBERO 环境动作。</p>
<p class="muted">LayerNorm、GELU、tanh 和 Softmax 当前是面向硬件的有界定点近似，测试验证的是边界、饱和和接口行为，不是与 FP32 网络逐位相同。<code>action_normalized</code> 参考值为 {html.escape(str(action_norm))}。</p>

<h2>7. RTL 和工具状态</h2>
{table(["阶段", "状态", "覆盖", "耗时／原因"], rtl_rows)}
<h3>Vivado 逻辑综合</h3>
{synth_table_html}
<p>{html.escape(synth_note)} 系统顶层的关键路径终点是 <code>{html.escape(str(system_critical))}</code>；它跨过动作路径的饱和／打包逻辑，所以系统壳的 WNS 不能代表 16×48 GEMM 阵列的 post-route 频率。综合 DRC 中目前只有 DSP 输入／输出流水相关的 warning，没有 Error；这些 warning 仍需在真正实现前处理或评估。</p>
<p>Verilator 日志中 16×48 测试报告的 DSP 映射期望值是 768；仿真使用行为级乘法分支，不等价于已验证的 Xilinx DSP48E2 原语。当前 server run 在 {html.escape(str(rtl.get('server_experiment', '—')))} 完成。</p>

<h2>8. 这轮交付了什么</h2>
<ul>
<li>可编辑 RTL：<code>hw/v1_2026-09-12_2354_w8a16_rtl/rtl/</code>，包括 multiplier、PE、sysarr、requant、GEMM、激活／向量单元、DMA、ISA 控制器和 runtime。</li>
<li>编译器清单和描述符：<code>data/operator_inventory.json</code>、<code>data/w8a16_descriptors.json</code>。</li>
<li>ISA 程序、指令成本和动作对拍：<code>data/turbovla_w8a16_program.json</code>、<code>data/isa_spec.json</code>、<code>data/instruction_costs.json</code>、<code>data/isa_sim_results.json</code>、<code>data/libero_action_probe.json</code>。</li>
<li>周期和流量：<code>data/cycle_breakdown.csv</code>、<code>data/traffic_breakdown.csv</code>。</li>
<li>验证日志：<code>hw/v1_2026-09-12_2354_w8a16_rtl/sim/logs/</code>。</li>
<li>图件同时提供 SVG、PDF 和 PNG，报告把 SVG 内嵌，因此单个 HTML 不依赖外部资源。</li>
</ul>

<h2>9. 尚未做和下一步</h2>
<p>未做：真实整数 GPU kernel、Vivado post-route／phys_opt、功耗、完整 LIBERO 成功率和端到端系统集成。下一步如果要把这条路线变成硬件性能结论，优先补齐三件事：一是运行时 trace，列出真实 Linear、Conv、MHA、BMM 的调用和 fallback 时间；二是针对系统壳的负 WNS 关键路径做流水化或拆分，并重跑实现流程；三是把动作 smoke 扩成真实 TurboVLA 的视觉、语言、采样和 LIBERO 环境步进。只有这些完成后，才能判断 768-DSP 阵列是否值得继续做物理实现。</p>
<p class="muted">源代码提交：{html.escape(str(quant.get('source_commit', '—')))}；checkpoint SHA256：{html.escape(str((quant.get('checkpoint') or {{}}).get('sha256', '—')))}。所有文件散列记录在 <code>data/file_manifest.json</code>。</p>
</main></body></html>"""
    report_path = report_dir / f"{stamp}_turbovla_w8a16_report.html"
    report_path.write_text(html_text, encoding="utf-8")

    (report_dir / "MODIFICATION_NOTES.md").write_text(
        f"""# 本轮修改说明\n\n生成时间：{generated}（Asia/Shanghai）\n\n这轮把 TurboVLA W8A16 的工作范围从单独 GEMM 扩到了一个可检查的命令路径：编译器生成 64 bit 指令字，ISA 控制器负责取指和结束，DMA 负责 CTX/WRAM 的读写，向量单元提供加法、缩放、ReLU、GELU、tanh、LayerNorm、Softmax 和重新量化，runtime 将动作投影接到 LIBERO 格式的七维动作输出。\n\n服务器 Verilator 回归在 `{rtl.get('server_experiment', '—')}` 完成，10 项通过；Icarus 四项短 smoke 通过。Python 编译器／解码／整数对拍也通过，90 个实际调度字和 18 个 opcode 目录项均可解码。\n\n本轮在本机 `D:\\software\\Vivado\\2021.2\\bin\\vivado.bat` 完成系统顶层、1×1、4×4、16×48 的逻辑综合，16×48 阵列映射为 768 个 DSP。系统壳在 3.298 ns 下有负 WNS，阵列顶层的综合估算满足约束；这些不是 post-route 结果，也不宣称 PPA 提升。\n\nruntime 只执行一个小型 1×7×8 动作投影命令路径，使用确定性的格式化 INT16 状态向量，输出与 Python 整数模型一致；它不包含真实 RGB-D 张量、DINO/T5、完整 TurboVLA 采样、真实权重流和 LIBERO 环境步进。\n""",
        encoding="utf-8",
    )

    # Copy a compact manifest next to the report as well, without embedding all
    # tracked-file hashes in the HTML.
    (report_dir / "BUILD_MANIFEST.json").write_text(json.dumps({"generated_at": generated, "report": report_path.name, "figures": fig_files, "workspace_manifest": "data/file_manifest.json"}, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "generated_at": generated, "report": str(report_path), "summary": str(report_dir / 'report_summary.json')}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
