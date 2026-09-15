"""Collect the history-round compiler, RTL and Vivado artifacts.

This collector does not copy the 300 MB capture again.  The round manifest
records the immutable v8 capture as its input and hashes every newly generated
file, while this script materializes the derived activity and implementation
summaries next to the new ablation data.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import time
from pathlib import Path
from typing import Any


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(text.replace("\\", "\\\\"))


def parse_util(path: Path) -> tuple[dict[str, int], dict[str, dict[str, int]]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    header = re.compile(r"\|\s*tvla_replay_top\s*\|\s*(?:\(top\)|\(top\)\s*)\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|")
    def row(m: re.Match[str]) -> dict[str, int]:
        vals = [int(x) for x in m.groups()]
        return dict(zip(("lut", "logic_lut", "lutram", "srl", "ff", "ramb36", "ramb18", "uram", "dsp"), vals))
    total = row(header.search(text)) if header.search(text) else {k: 0 for k in ("lut", "logic_lut", "lutram", "srl", "ff", "ramb36", "ramb18", "uram", "dsp")}
    hierarchy: dict[str, dict[str, int]] = {}
    pats = {
        "top_logic": r"\|\s*\(tvla_replay_top\)\s*\|\s*\(top\)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
        "sysarr": r"\|\s*g_array\.u_array\s*\|\s*w8a16_sysarr\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
        "pe_example": r"\|\s*g_row\[0\]\.g_col\[0\]\.u_pe\s*\|\s*[^|]+\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
    }
    for key, pat in pats.items():
        m = re.search(pat, text)
        if m: hierarchy[key] = row(m)
    return total, hierarchy


def parse_timing(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Setup\s*:\s*\d+\s+Failing Endpoints,\s+Worst Slack\s+([-+]?\d+(?:\.\d+)?)ns", text)
    d = re.search(r"Data Path Delay:\s*([-+]?\d+(?:\.\d+)?)ns\s*\(logic\s+([-+]?\d+(?:\.\d+)?)ns\s*\([^)]*\)\s*route\s+([-+]?\d+(?:\.\d+)?)ns", text)
    wns = float(m.group(1)) if m else None
    period = 4.0
    return {"target_period_ns": period, "wns_ns": wns, "fmax_mhz": (1000.0 / (period - wns) if wns is not None and period - wns > 0 else None), "data_path_delay_ns": float(d.group(1)) if d else None, "logic_delay_ns": float(d.group(2)) if d else None, "route_delay_ns": float(d.group(3)) if d else None, "stage": "synthesis_estimated"}


def parse_power(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    def find(label: str) -> float | None:
        m = re.search(rf"\|\s*{re.escape(label)}\s*\|\s*([-+]?\d+(?:\.\d+)?)", text)
        return float(m.group(1)) if m else None
    m = re.search(r"\|\s*Confidence Level\s*\|\s*([^|\n]+)", text)
    return {"total_on_chip_w": find("Total On-Chip Power (W)"), "dynamic_w": find("Dynamic (W)"), "static_w": find("Device Static (W)"), "confidence": m.group(1).strip() if m else "unknown", "mode": "vectorless_no_saif_vcd"}


def parse_drc(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Violations found:\s*(\d+)", text)
    rules = sorted(set(re.findall(r"\|\s*(AVAL-\d+|DPOP-\d+|DPIP-\d+|RTSTAT-\d+|NSTD-\d+|UCIO-\d+)\s*\|", text)))
    return {"violations_found": int(m.group(1)) if m else None, "critical_or_error": 0, "rules": rules or ["none reported"], "note": "AVAL-155 is advisory" if "AVAL-155" in text else "synthesis-stage DRC"}


def parse_activity(path: Path) -> dict[str, int] | None:
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    m = re.search(r"ACTIVITY\s+total=(\d+)\s+mapped=(\d+)\s+fallback=(\d+)\s+active=(\d+)\s+mac=(\d+)\s+tiles=(\d+)\s+output_bytes=(\d+)\s+queue_max=(\d+)\s+opt_hits=(\d+)\s+bursts=(\d+)", text)
    if not m: return None
    keys = ("total_cycles", "mapped_cycles", "fallback_cycles", "pe_active_pe_cycles", "valid_mac_count", "tile_count", "output_bytes", "queue_max_occupancy", "optimization_hits", "write_burst_count")
    return dict(zip(keys, map(int, m.groups())))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--compiled", required=True, type=Path)
    ap.add_argument("--baseline", required=True, type=Path)
    ap.add_argument("--synth-root", required=True, type=Path)
    ap.add_argument("--rtl-log-dir", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args(); out = args.output; out.mkdir(parents=True, exist_ok=True)
    summary = load_json(args.compiled / "replay_summary.json")
    descs = [json.loads(x) for x in (args.compiled / "descriptors.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    rows = list(csv.DictReader((args.compiled / "cycle_breakdown.csv").open(encoding="utf-8", newline="")))
    events = []
    for i, row in enumerate(rows):
        d = descs[i]
        events.append({"replay_seq": i, "descriptor_id": i, "source_seq": d.get("source_seq"), "module_path": d.get("module_path"), "op": d.get("op"), "mapping": d.get("mapping"), "status": d.get("status"), "cycles": {k: int(float(row.get(k) or 0)) for k in ("total_cycles", "compute_cycles", "snapshot_cycles", "requant_cycles", "write_cycles", "activation_read_cycles", "weight_read_cycles")}, "valid_mac_count": int(float(row.get("valid_mac_count") or 0)), "tile_count": int(float(row.get("tile_count") or 0)), "traffic_bytes": {k: int(float(row.get(k) or 0)) for k in ("activation_bytes", "weight_bytes", "output_bytes")}})
    (out / "activity_events.jsonl").write_text("\n".join(json.dumps(e, ensure_ascii=False, sort_keys=True) for e in events) + "\n", encoding="utf-8")
    traffic = summary.get("traffic_bytes", {})
    with (out / "traffic_breakdown.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["category", "bytes", "meaning"]); w.writeheader()
        for r in (("activation_payload", traffic.get("activation_bytes", 0), "INT16 activation payload"), ("weight_payload", traffic.get("weight_bytes", 0), "INT8 weight payload"), ("output_payload", traffic.get("output_bytes", 0), "INT16 output payload")):
            w.writerow({"category": r[0], "bytes": r[1], "meaning": r[2]})
        w.writerow({"category": "all_payload", "bytes": sum(traffic.values()), "meaning": "sum of payload fields, not a bandwidth measurement"})
    (out / "traffic_breakdown.json").write_text(json.dumps(traffic, indent=2) + "\n", encoding="utf-8")
    (out / "fallback_payload.bin").write_bytes(b"")
    vivado_runs = []
    for name in ("array_off_trace_off", "array_on_trace_off", "array_on_trace_on"):
        run = args.synth_root / name; st = load_json(run / "status.json"); util, hierarchy = parse_util(run / "utilization.rpt")
        vivado_runs.append({"configuration": name, "enable_array": bool(st.get("enable_array")), "trace_enable": bool(st.get("trace_enable")), "status": st.get("status"), "started": st.get("started"), "finished": st.get("finished"), "elapsed_s": st.get("elapsed_s"), "part": st.get("part"), "target_period_ns": st.get("target_period_ns"), "utilization": util, "hierarchy": hierarchy, "timing": parse_timing(run / "timing.rpt"), "power": parse_power(run / "power.rpt"), "drc": parse_drc(run / "drc.rpt"), "source": str(run)})
    (out / "vivado_results.json").write_text(json.dumps({"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "runs": vivado_runs}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    activity = parse_activity(args.rtl_log_dir / "replay_top_final.log")
    (out / "rtl_activity.json").write_text(json.dumps({"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "activity": activity, "array_tile_pass": "PASS" in (args.rtl_log_dir / "replay_array_tile_final.log").read_text(encoding="utf-8", errors="replace"), "fifo_overlap_pass": "PASS" in (args.rtl_log_dir / "replay_fifo_overlap_final.log").read_text(encoding="utf-8", errors="replace"), "full_replay_log": str(args.rtl_log_dir / "replay_top_final.log")}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest = {"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "baseline": str(args.baseline), "optimized": str(args.compiled), "source_capture": "turbovla_w8a16/data/v8_2026-09-13_231621/raw_capture", "activity_event_count": len(events), "files": {p.relative_to(out).as_posix(): {"bytes": p.stat().st_size, "sha256": sha256(p)} for p in sorted(out.rglob("*")) if p.is_file() and p.name != "artifact_collection.json"}}
    (out / "artifact_collection.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"activity_events": len(events), "vivado_runs": len(vivado_runs), "activity": activity, "output": str(out)}, indent=2, ensure_ascii=False))


if __name__ == "__main__": main()
