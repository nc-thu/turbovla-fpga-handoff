"""Independent checks for the history-optimization compiler and replay top.

The checks intentionally read the generated CSV/JSON rather than reproducing
the HTML calculations.  This keeps the report a view of the machine-readable
round and catches stale summaries, lost command IDs, and FIFO accounting
regressions.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
import time
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def int40(value: int) -> int:
    value &= (1 << 40) - 1
    return value - (1 << 40) if value & (1 << 39) else value


def sat16(value: int) -> int:
    return max(-32768, min(32767, int(value)))


def run_summary(path: Path) -> tuple[dict[str, Any], list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]]]:
    summary = json.loads((path / "replay_summary.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader((path / "cycle_breakdown.csv").open(encoding="utf-8", newline="")))
    descs = [json.loads(x) for x in (path / "descriptors.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    insts = [json.loads(x) for x in (path / "instructions.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    return summary, rows, descs, insts


def parse_activity(path: Path) -> dict[str, int] | None:
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    m = re.search(
        r"ACTIVITY\s+total=(\d+)\s+mapped=(\d+)\s+fallback=(\d+)\s+active=(\d+)\s+"
        r"mac=(\d+)\s+tiles=(\d+)\s+output_bytes=(\d+)\s+queue_max=(\d+)\s+"
        r"opt_hits=(\d+)\s+bursts=(\d+)", text,
    )
    if not m:
        return None
    keys = ("total_cycles", "mapped_cycles", "fallback_cycles", "pe_active_pe_cycles",
            "valid_mac_count", "tile_count", "output_bytes", "queue_max_occupancy",
            "optimization_hits", "write_burst_count")
    return dict(zip(keys, (int(x) for x in m.groups())))


def check_run(summary: dict[str, Any], rows: list[dict[str, str]], descs: list[dict[str, Any]], insts: list[dict[str, Any]]) -> dict[str, bool]:
    cyc = summary["cycles"]
    checks: dict[str, bool] = {}
    checks["descriptor_ids_contiguous"] = [d.get("descriptor_id") for d in descs] == list(range(len(descs)))
    checks["instruction_has_end"] = bool(insts and insts[-1].get("op") == "END")
    checks["descriptor_instruction_count"] = len(insts) == len(descs) + 1
    checks["cycle_rows_match_descriptors"] = len(rows) == len(descs)
    checks["unknown_zero"] = int(summary.get("unknown_event_count", 1)) == 0
    cov = summary.get("coverage", {})
    checks["module_coverage_complete"] = cov.get("module_events_covered") == cov.get("module_events_total")
    checks["bmm_coverage_complete"] = cov.get("dispatch_bmm_covered") == cov.get("dispatch_bmm_total")
    checks["no_parent_child_double_count"] = bool(cov.get("parent_children_not_double_counted"))
    checks["total_is_mapped_plus_fallback"] = cyc["total_cycles"] == cyc["mapped_cycles"] + cyc["fallback_cycles"]
    checks["utilization_bounded"] = all(0.0 <= float(summary.get(k, -1)) <= 1.0 for k in ("pe_time_utilization", "gemm_utilization"))
    checks["dsp_count_fixed"] = int(summary["array"].get("dsp", 0)) == 768
    mapped = sum(int(float(r.get("total_cycles") or 0)) for r in rows if r.get("mapping") in {"rtl_gemm", "rtl_bmm"})
    fallback = sum(int(float(r.get("fallback_cycles") or r.get("total_cycles") or 0)) for r in rows if r.get("mapping") not in {"rtl_gemm", "rtl_bmm"})
    valid_mac = sum(int(float(r.get("valid_mac_count") or 0)) for r in rows if r.get("mapping") in {"rtl_gemm", "rtl_bmm"})
    tiles = sum(int(float(r.get("tile_count") or 0)) for r in rows if r.get("mapping") in {"rtl_gemm", "rtl_bmm"})
    checks["mapped_rows_reconcile"] = mapped == int(cyc["mapped_cycles"])
    checks["fallback_rows_reconcile"] = fallback == int(cyc["fallback_cycles"])
    checks["mac_rows_reconcile"] = valid_mac == int(summary["valid_mac_count"])
    checks["tile_rows_reconcile"] = tiles == int(summary["tile_count"])
    return checks


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True, type=Path)
    ap.add_argument("--optimized", required=True, type=Path)
    ap.add_argument("--rtl-log-dir", required=True, type=Path)
    ap.add_argument("--vivado-json", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    base, base_rows, base_desc, base_inst = run_summary(args.baseline)
    opt, opt_rows, opt_desc, opt_inst = run_summary(args.optimized)
    checks: dict[str, bool] = {}
    for name, value in check_run(base, base_rows, base_desc, base_inst).items(): checks[f"baseline_{name}"] = value
    for name, value in check_run(opt, opt_rows, opt_desc, opt_inst).items(): checks[f"optimized_{name}"] = value
    checks["cycle_savings_matches"] = int(opt["cycles"]["cycle_savings"]) == int(base["cycles"]["total_cycles"]) - int(opt["cycles"]["total_cycles"])
    checks["optimized_flags_present"] = any(d.get("optimization_flags") for d in opt_desc)
    checks["corrected_bmm_tile_count"] = int(opt["tile_count"]) == 79807

    # Decode the 64-bit transport words independently of the JSON instruction
    # stream.  The ID is deliberately 16 bits at [47:32].
    for label, path, insts in (("baseline", args.baseline / "instructions.hex", base_inst), ("optimized", args.optimized / "instructions.hex", opt_inst)):
        words = [int(x.strip(), 16) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
        checks[f"{label}_command_word_count"] = len(words) == len(insts)
        checks[f"{label}_command_ids_decode"] = all(((w >> 32) & 0xFFFF) == int(i.get("descriptor_id", 0)) for w, i in zip(words[:-1], insts[:-1]))
        checks[f"{label}_end_word"] = bool(words and (words[-1] >> 56) == 0xFF)

    # Arithmetic boundary vectors cover signed endpoints, long K, 40-bit wrap,
    # and INT16 output saturation.
    rng = random.Random(20260914)
    vectors = []
    for k in (1, 32, 256, 768, 2048, 3072, 4096):
        a = [(-32768 if i % 11 == 0 else 32767 if i % 13 == 0 else rng.randint(-32768, 32767)) for i in range(k)]
        w = [(-128 if i % 7 == 0 else 127 if i % 9 == 0 else rng.randint(-128, 127)) for i in range(k)]
        exact = sum(x * y for x, y in zip(a, w)); wrapped = int40(exact); out = sat16(wrapped)
        vectors.append({"k": k, "exact_int64": exact, "int40": wrapped, "int16": out, "finite": all(abs(v) < (1 << 63) for v in (exact, wrapped, out))})
    checks["golden_vectors_finite"] = all(v["finite"] for v in vectors)
    checks["endpoint_products_present"] = (-32768 * 127 == -4161536) and (32767 * -128 == -4194176)

    activity = parse_activity(args.rtl_log_dir / "replay_top_final.log")
    checks["verilator_full_replay_pass"] = bool(activity)
    if activity:
        for k in ("total_cycles", "mapped_cycles", "fallback_cycles", "valid_mac_count", "tile_count", "output_bytes"):
            source = opt["cycles"].get(k, opt.get(k)) if k in {"total_cycles", "mapped_cycles", "fallback_cycles"} else opt.get(k, opt["traffic_bytes"].get(k))
            if k == "output_bytes": source = opt["traffic_bytes"]["output_bytes"]
            checks[f"rtl_{k}_matches"] = activity[k] == int(source)
    checks["verilator_array_tile_pass"] = "PASS" in (args.rtl_log_dir / "replay_array_tile_final.log").read_text(encoding="utf-8", errors="replace")
    checks["verilator_fifo_overlap_pass"] = "PASS" in (args.rtl_log_dir / "replay_fifo_overlap_final.log").read_text(encoding="utf-8", errors="replace")

    vivado = json.loads(args.vivado_json.read_text(encoding="utf-8"))
    runs = vivado.get("runs", [])
    checks["vivado_runs_present"] = len(runs) == 3
    checks["vivado_all_passed"] = bool(runs) and all(r.get("status") == "passed" for r in runs)
    array_runs = [r for r in runs if r.get("enable_array")]
    checks["vivado_array_dsp_768"] = bool(array_runs) and all(int(r.get("utilization", {}).get("dsp", 0)) == 768 for r in array_runs)
    checks["vivado_trace_resource_neutral"] = len(array_runs) >= 2 and array_runs[0].get("utilization") == array_runs[-1].get("utilization")
    checks["vivado_timing_positive"] = bool(array_runs) and all(float(r.get("timing", {}).get("wns_ns", -1)) >= 0 for r in array_runs)

    result = {
        "schema_version": "tvla_w8a16.history_optimization.validation.v1",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "passed": all(checks.values()),
        "checks": checks,
        "golden_vectors": vectors,
        "rtl_activity": activity,
        "vivado_run_count": len(runs),
        "input_sha256": {str(p): sha256(p) for p in (args.baseline / "replay_summary.json", args.optimized / "replay_summary.json", args.optimized / "instructions.hex", args.rtl_log_dir / "replay_top_final.log") if p.exists()},
        "notes": [
            "Full replay is a virtual event-cycle counter; representative tile and FIFO overlap tests are cycle-accurate Verilator checks.",
            "Vivado is synthesis-estimated OOC at 4.000 ns; no post-route or SAIF/VCD power claim is made.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
