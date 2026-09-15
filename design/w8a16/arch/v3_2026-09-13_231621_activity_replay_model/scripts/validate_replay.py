"""Validate the TurboVLA activity stream and the W8A16 arithmetic contract.

This is intentionally independent of the RTL simulator.  It checks the
accounting invariants from JSON/CSV and exercises the signed INT16 x INT8
golden model at the same K sizes used by the replay plan.
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


def int40(value: int) -> int:
    """Two's-complement 40-bit accumulator semantics."""
    mask = (1 << 40) - 1
    value &= mask
    return value - (1 << 40) if value & (1 << 39) else value


def sat16(value: int) -> int:
    return max(-32768, min(32767, int(value)))


def golden(a: list[int], w: list[int]) -> tuple[int, int, int]:
    exact = sum(int(x) * int(y) for x, y in zip(a, w))
    wrapped = int40(exact)
    return exact, wrapped, sat16(wrapped)


def parse_activity_line(path: Path) -> dict[str, int] | None:
    """Parse the single full-replay activity line emitted by the testbench."""
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"ACTIVITY\s+total=(\d+)\s+mapped=(\d+)\s+fallback=(\d+)\s+"
                  r"active=(\d+)\s+mac=(\d+)\s+tiles=(\d+)\s+"
                  r"output_bytes=(\d+)\s+queue_max=(\d+)", text)
    if not m:
        return None
    keys = ("total_cycles", "mapped_cycles", "fallback_cycles", "pe_active_pe_cycles",
            "valid_mac_count", "tile_count", "output_bytes", "queue_max_occupancy")
    return dict(zip(keys, (int(x) for x in m.groups())))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, type=Path)
    ap.add_argument("--rtl-log-dir", type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    data = args.data
    compiled = data / "compiled"
    stream = data / "replay_stream"
    summary = json.loads((compiled / "replay_summary.json").read_text(encoding="utf-8"))
    descs = [json.loads(x) for x in (compiled / "descriptors.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    insts = [json.loads(x) for x in (compiled / "instructions.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = list(csv.DictReader((compiled / "cycle_breakdown.csv").open(encoding="utf-8", newline="")))

    checks: dict[str, bool] = {}
    checks["descriptor_ids_contiguous"] = [d["descriptor_id"] for d in descs] == list(range(len(descs)))
    checks["instruction_has_end"] = bool(insts and insts[-1].get("op") == "END")
    checks["descriptor_instruction_count"] = len(insts) == len(descs) + 1
    checks["cycle_rows_match_descriptors"] = len(rows) == len(descs)
    checks["unknown_zero"] = int(summary.get("unknown_event_count", 1)) == 0
    cov = summary.get("coverage", {})
    checks["module_coverage_complete"] = cov.get("module_events_covered") == cov.get("module_events_total")
    checks["bmm_coverage_complete"] = cov.get("dispatch_bmm_covered") == cov.get("dispatch_bmm_total")
    checks["no_parent_child_double_count"] = bool(cov.get("parent_children_not_double_counted"))
    cyc = summary["cycles"]
    checks["total_is_mapped_plus_fallback"] = cyc["total_cycles"] == cyc["mapped_cycles"] + cyc["fallback_cycles"]
    checks["utilization_bounded"] = 0.0 <= summary["pe_time_utilization"] <= 1.0 and 0.0 <= summary["gemm_utilization"] <= 1.0
    checks["dsp_count_fixed"] = summary["array"]["dsp"] == 768

    # Recompute the key sums directly from the rows; this catches a stale
    # summary copied from a previous run.
    mapped = sum(int(r.get("total_cycles") or 0) for r in rows if r.get("mapping") in {"rtl_gemm", "rtl_bmm"})
    fallback = sum(int(r.get("fallback_cycles") or r.get("total_cycles") or 0) for r in rows if r.get("mapping") not in {"rtl_gemm", "rtl_bmm"})
    valid_mac = sum(int(r.get("valid_mac_count") or 0) for r in rows if r.get("mapping") in {"rtl_gemm", "rtl_bmm"})
    tile_count = sum(int(r.get("tile_count") or 0) for r in rows if r.get("mapping") in {"rtl_gemm", "rtl_bmm"})
    checks["mapped_rows_reconcile"] = mapped == cyc["mapped_cycles"]
    checks["fallback_rows_reconcile"] = fallback == cyc["fallback_cycles"]
    checks["mac_rows_reconcile"] = valid_mac == summary["valid_mac_count"]
    checks["tile_rows_reconcile"] = tile_count == summary["tile_count"]

    # Boundary vectors exercise signed endpoints, long K, and INT40 wrapping.
    vectors = []
    rng = random.Random(20260913)
    for k in (1, 32, 256, 768, 2048, 3072, 4096):
        a = [(-32768 if i % 11 == 0 else 32767 if i % 13 == 0 else rng.randint(-32768, 32767)) for i in range(k)]
        w = [(-128 if i % 7 == 0 else 127 if i % 9 == 0 else rng.randint(-128, 127)) for i in range(k)]
        exact, wrapped, out = golden(a, w)
        vectors.append({"k": k, "exact_int64": exact, "int40": wrapped, "int16_saturated": out, "finite": all(abs(v) < (1 << 63) for v in (exact, wrapped, out))})
    checks["golden_vectors_finite"] = all(v["finite"] for v in vectors)
    checks["endpoint_products_present"] = golden([-32768], [127])[0] == -4161536 and golden([32767], [-128])[0] == -4194176

    rtl = {"full_replay": "not_checked", "array_tile": "not_checked", "logs": None}
    if args.rtl_log_dir:
        rtl["logs"] = str(args.rtl_log_dir)
        for key, filename in (("full_replay", "replay_full.status"), ("array_tile", "replay_array_tile.status")):
            p = args.rtl_log_dir / filename
            if p.exists():
                rtl[key] = p.read_text(encoding="utf-8").strip() == "0"
        counters = parse_activity_line(args.rtl_log_dir / "replay_full.log")
        if counters:
            rtl["activity_counters"] = counters
            rtl["activity_matches_summary"] = all(
                counters.get(k) == summary.get(k) or counters.get(k) == cyc.get(k)
                for k in ("total_cycles", "mapped_cycles", "fallback_cycles", "pe_active_pe_cycles", "valid_mac_count", "tile_count")
            )
            rtl["output_bytes_matches_summary"] = counters.get("output_bytes") == summary["traffic_bytes"].get("output_bytes")
        else:
            rtl["activity_counters"] = None
            rtl["activity_matches_summary"] = False
            rtl["output_bytes_matches_summary"] = False
    else:
        rtl["activity_counters"] = None
        rtl["activity_matches_summary"] = False
        rtl["output_bytes_matches_summary"] = False
    checks["verilator_full_replay_pass"] = rtl["full_replay"] is True
    checks["verilator_array_tile_pass"] = rtl["array_tile"] is True
    checks["rtl_activity_matches_summary"] = rtl["activity_matches_summary"] is True
    checks["rtl_output_bytes_matches_summary"] = rtl["output_bytes_matches_summary"] is True

    result = {
        "schema_version": "tvla_w8a16.replay_validation.v1",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "input_sha256": {name: sha256(data / name) for name in ("capture_result.json", "compiled/replay_summary.json", "replay_stream/descriptor_words.hex") if (data / name).exists()},
        "checks": checks,
        "passed": all(v is True for v in checks.values()),
        "golden_vectors": vectors,
        "rtl": rtl,
        "notes": [
            "INT40 is evaluated as signed two's-complement wrap; INT16 is saturating output reference.",
            "The full replay top consumes one descriptor per control clock and reports virtual event cycles; the array tile test is the cycle-by-cycle arithmetic check.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
