"""Build the machine-readable figures for the history-optimization report."""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def n(row: dict[str, str], key: str) -> int:
    try: return int(float(row.get(key) or 0))
    except (TypeError, ValueError): return 0


def module_group(path: str) -> str:
    if not path: return "unknown"
    return path.split(".", 1)[0]


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


def stage_aggregate(rows: list[dict[str, str]]) -> dict[str, int]:
    """Use non-overlapping stages for a readable time ledger.

    A GEMM's read stage is max(activation, weight), because the two streams
    are serviced in parallel.  Its post stage contains snapshot, requant and
    write.  This sums to the serial GEMM budget; overlap is reported separately
    and is never added a second time.
    """
    out = defaultdict(int)
    for r in rows:
        mapping = r.get("mapping", "")
        if mapping in {"rtl_gemm", "rtl_bmm"}:
            read = max(n(r, "activation_read_cycles"), n(r, "weight_read_cycles"))
            compute = n(r, "compute_cycles"); snapshot = n(r, "snapshot_cycles"); requant = n(r, "requant_cycles"); write = n(r, "write_cycles")
            out["gemm_read"] += read; out["gemm_compute"] += compute; out["snapshot"] += snapshot; out["requant"] += requant; out["writeback"] += write
            # Bias is not a separate CSV column in the legacy compiler.  It
            # is recoverable from the serial ledger and must not disappear
            # from the stage sum.
            serial = n(r, "serial_total_cycles")
            out["bias_add"] += max(0, serial - (read + compute + snapshot + requant + write))
        elif mapping == "rtl_vector": out["vector_fallback"] += n(r, "total_cycles")
        else: out["aux_fallback"] += n(r, "total_cycles")
    out["mapped_serial_subtotal"] = out["gemm_read"] + out["gemm_compute"] + out["snapshot"] + out["requant"] + out["writeback"] + out["bias_add"]
    out["fallback_subtotal"] = out["vector_fallback"] + out["aux_fallback"]
    out["serial_subtotal"] = out["mapped_serial_subtotal"] + out["fallback_subtotal"]
    return dict(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, type=Path)
    ap.add_argument("--selected", required=True, type=Path)
    ap.add_argument("--vivado", required=True, type=Path)
    ap.add_argument("--validation", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args(); out = args.output; out.mkdir(parents=True, exist_ok=True)
    base_dir = args.data / "compiler_baseline"; opt_dir = args.data / "compiler_optimized"
    base = json.loads((base_dir / "replay_summary.json").read_text(encoding="utf-8")); opt = json.loads((opt_dir / "replay_summary.json").read_text(encoding="utf-8"))
    ablation = json.loads((args.data / "ablation" / "ablation_summary.json").read_text(encoding="utf-8"))
    selected = json.loads(args.selected.read_text(encoding="utf-8")); vivado = json.loads(args.vivado.read_text(encoding="utf-8")); validation = json.loads(args.validation.read_text(encoding="utf-8"))
    base_rows = read_rows(base_dir / "cycle_breakdown.csv"); opt_rows = read_rows(opt_dir / "cycle_breakdown.csv")

    effects = []
    for i, item in enumerate(selected.get("selected", []), 1):
        key = {"DSP input/output pipeline": "pipeline", "Local clr/CE fanout partition": "fanout", "16x48 shape-aware tiling and tail mask": "tile_mask", "Dependency-aware BMM/GEMM ordering": "order", "Activation tile reuse": "act_reuse", "Weight tile reuse/broadcast": "weight_reuse", "Row-group streaming and double buffering": "overlap", "Contiguous write coalescing": "write_coalesce", "Adjacent compatible task merge": "fusion", "Requant/bias/vector stage pipeline and control locality": "vector_pipeline"}.get(item.get("name", ""), "")
        found = next((r for r in ablation if r.get("name") == key), None)
        after = int(found["total_cycles"]) if found else int(base["cycles"]["total_cycles"])
        before = int(base["cycles"]["total_cycles"])
        effects.append({"id": i, "name": item.get("name"), "state": item.get("state"), "config": key or "inherited", "before_cycles": before, "after_cycles": after, "cycle_savings": before - after, "cycle_savings_pct": (100.0 * (before - after) / before if before else 0.0), "evidence": item.get("evidence")})
    all_row = next(r for r in ablation if r.get("name") == "all_selected")
    write_csv(out / "optimization_effects.csv", effects, ["id", "name", "state", "config", "before_cycles", "after_cycles", "cycle_savings", "cycle_savings_pct", "evidence"])

    stage_rows = []
    for label, rows, summary in (("baseline", base_rows, base), ("all_selected", opt_rows, opt)):
        st = stage_aggregate(rows)
        for key in ("gemm_read", "gemm_compute", "snapshot", "requant", "writeback", "bias_add", "vector_fallback", "aux_fallback"):
            stage_rows.append({"configuration": label, "stage": key, "cycles": st.get(key, 0), "share_of_total_pct": 100.0 * st.get(key, 0) / int(summary["cycles"]["total_cycles"]) if summary["cycles"]["total_cycles"] else 0.0, "note": "non-overlap stage subtotal; overlap total is reported separately"})
        stage_rows.append({"configuration": label, "stage": "serial_subtotal_check", "cycles": st["serial_subtotal"], "share_of_total_pct": 100.0 * st["serial_subtotal"] / int(summary["cycles"]["total_cycles"]) if summary["cycles"]["total_cycles"] else 0.0, "note": "baseline equals total; optimized includes max(read,compute,post)+guard and therefore is a separate schedule"})
    write_csv(out / "cycle_stage.csv", stage_rows, ["configuration", "stage", "cycles", "share_of_total_pct", "note"])

    groups: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for label, rows in (("baseline", base_rows), ("all_selected", opt_rows)):
        for r in rows:
            g = module_group(r.get("module_path", "")); groups[g][f"{label}_cycles"] += n(r, "total_cycles"); groups[g][f"{label}_mac"] += n(r, "valid_mac_count"); groups[g][f"{label}_descriptors"] += 1
            if r.get("mapping") not in {"rtl_gemm", "rtl_bmm"}: groups[g][f"{label}_fallback"] += n(r, "total_cycles")
    module_rows = []
    for g, vals in sorted(groups.items(), key=lambda kv: -kv[1]["baseline_cycles"]):
        module_rows.append({"module_group": g, "baseline_descriptors": vals["baseline_descriptors"], "baseline_cycles": vals["baseline_cycles"], "baseline_share_pct": 100.0 * vals["baseline_cycles"] / base["cycles"]["total_cycles"], "baseline_mac": vals["baseline_mac"], "optimized_descriptors": vals["all_selected_descriptors"], "optimized_cycles": vals["all_selected_cycles"], "optimized_share_pct": 100.0 * vals["all_selected_cycles"] / opt["cycles"]["total_cycles"], "optimized_mac": vals["all_selected_mac"], "optimized_fallback_cycles": vals["all_selected_fallback"]})
    write_csv(out / "module_stage.csv", module_rows, list(module_rows[0].keys()) if module_rows else ["module_group"])

    resource_rows = []
    component_rows = []
    for run in vivado.get("runs", []):
        u = run.get("utilization", {}); t = run.get("timing", {}); p = run.get("power", {}); d = run.get("drc", {})
        resource_rows.append({"configuration": run.get("configuration"), "array_enabled": run.get("enable_array"), "trace_enabled": run.get("trace_enable"), "status": run.get("status"), "lut": u.get("lut"), "logic_lut": u.get("logic_lut"), "ff": u.get("ff"), "dsp": u.get("dsp"), "bram36": u.get("ramb36"), "bram18": u.get("ramb18"), "wns_ns": t.get("wns_ns"), "fmax_mhz": t.get("fmax_mhz"), "data_path_ns": t.get("data_path_delay_ns"), "logic_delay_ns": t.get("logic_delay_ns"), "route_delay_ns": t.get("route_delay_ns"), "power_w": p.get("total_on_chip_w"), "dynamic_w": p.get("dynamic_w"), "static_w": p.get("static_w"), "drc_violations": d.get("violations_found"), "drc_critical_or_error": d.get("critical_or_error"), "stage": t.get("stage")})
        for name, vals in run.get("hierarchy", {}).items():
            component_rows.append({"configuration": run.get("configuration"), "component": name, **vals})
    write_csv(out / "resource_breakdown.csv", resource_rows, list(resource_rows[0].keys()) if resource_rows else ["configuration"])
    write_csv(out / "resource_hierarchy.csv", component_rows, list(component_rows[0].keys()) if component_rows else ["configuration", "component"])

    bcycles = int(base["cycles"]["total_cycles"]); ocycles = int(opt["cycles"]["total_cycles"]); freq = float(opt.get("clock_mhz", 250.0));
    metrics = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "baseline": base, "optimized": opt,
        "baseline_seconds_at_clock": bcycles / (freq * 1e6), "optimized_seconds_at_clock": ocycles / (freq * 1e6),
        "conditional_speedup": bcycles / ocycles if ocycles else None, "effective_gops_gain_pct": 100.0 * (opt["effective_gops"] / base["effective_gops"] - 1.0) if base["effective_gops"] else None,
        "pe_util_gain_pct": 100.0 * (opt["pe_time_utilization"] / base["pe_time_utilization"] - 1.0) if base["pe_time_utilization"] else None,
        "gemm_util_gain_pct": 100.0 * (opt["gemm_utilization"] / base["gemm_utilization"] - 1.0) if base["gemm_utilization"] else None,
        "peak_fraction_baseline_pct": 100.0 * base["effective_gops"] / base["physical_peak_gops"], "peak_fraction_optimized_pct": 100.0 * opt["effective_gops"] / opt["physical_peak_gops"],
        "validation_passed": validation.get("passed"), "effects": effects,
        "boundaries": {"measured": ["compiler baseline/optimized summaries", "Verilator representative array tile", "Verilator full virtual replay counters", "Vivado synthesis-estimated OOC"], "conditional": ["reuse, overlap and write coalescing cycle model", "optimized full-trace throughput"], "unknown": ["post-route timing for this round", "SAIF/VCD activity power", "board DDR and end-to-end LIBERO"]},
    }
    (out / "model_summary.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(out), "effects": len(effects), "modules": len(module_rows), "vivado_runs": len(resource_rows), "speedup": metrics["conditional_speedup"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__": main()
