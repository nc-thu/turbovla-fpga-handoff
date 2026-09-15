#!/usr/bin/env python3
"""Build the immutable manifest for the history-optimization round.

The large v8 capture is intentionally referenced by path and checksum instead
of copied into the new round.  This keeps the round reproducible without
duplicating nearly 300 MB of payload data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path


def sha256(path: Path) -> dict:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            size += len(block)
            h.update(block)
    return {"bytes": size, "sha256": h.hexdigest()}


def collect_files(root: Path, paths: list[Path]) -> dict:
    result = {}
    for path in paths:
        if path.is_file():
            result[str(path.relative_to(root)).replace("\\", "/")] = sha256(path)
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--round-root", type=Path, required=True)
    ap.add_argument("--source-root", type=Path, required=True)
    ap.add_argument("--compiler-baseline", type=Path, required=True)
    ap.add_argument("--compiler-optimized", type=Path, required=True)
    ap.add_argument("--ablation", type=Path, required=True)
    ap.add_argument("--rtl-root", type=Path, required=True)
    ap.add_argument("--derived", type=Path, required=True)
    ap.add_argument("--selected", type=Path, required=True)
    ap.add_argument("--validation", type=Path, required=True)
    ap.add_argument("--navigation", type=Path, default=Path("NAVIGATION.html"))
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    round_root = args.round_root.resolve()
    source_root = args.source_root.resolve()
    source_manifest_path = source_root.parent / "trace_manifest.json"
    source_manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))

    source_names = [
        "capture_result.json",
        "operator_trace.jsonl",
        "module_events.jsonl",
        "scale_table.json",
        "weight_manifest.json",
        "activation_payload.bin",
        "weight_payload.bin",
        "action_output.json",
    ]
    source_files = collect_files(source_root, [source_root / n for n in source_names])
    navigation = args.navigation.resolve()

    new_paths = [
        args.compiler_baseline / "replay_summary.json",
        args.compiler_baseline / "cycle_breakdown.csv",
        args.compiler_baseline / "operator_inventory.json",
        args.compiler_baseline / "descriptors.jsonl",
        args.compiler_baseline / "instructions.hex",
        args.compiler_optimized / "replay_summary.json",
        args.compiler_optimized / "cycle_breakdown.csv",
        args.compiler_optimized / "operator_inventory.json",
        args.compiler_optimized / "descriptors.jsonl",
        args.compiler_optimized / "instructions.hex",
        args.ablation / "ablation_summary.csv",
        args.ablation / "ablation_summary.json",
        args.rtl_root / "rtl" / "tvla_replay_top.sv",
        args.rtl_root / "rtl" / "w8a16_sysarr.sv",
        args.rtl_root / "sim" / "tb_replay_top.sv",
        args.rtl_root / "sim" / "tb_replay_array_tile.sv",
        args.rtl_root / "sim" / "tb_fifo_overlap.sv",
        args.derived / "rtl_activity.json",
        args.derived / "vivado_results.json",
        args.derived / "traffic_breakdown.csv",
        args.selected,
        args.validation,
        round_root / "reports" / "2026-09-14_010956" / "2026-09-14_010956_turbovla_history_optimization_report.html",
        round_root / "reports" / "2026-09-14_010956" / "round_summary.json",
        round_root / "reports" / "2026-09-14_010956" / "scripts" / "generate_history_report.py",
    ]
    new_files = collect_files(round_root, [p.resolve() for p in new_paths])

    # Keep paths relative to the workspace when possible; absolute paths are
    # retained only for the immutable source location on the server side.
    generated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    manifest = {
        "schema_version": "tvla_w8a16.history_optimization.manifest.v1",
        "generated_at": generated,
        "round": "2026-09-14_010956",
        "purpose": "Select and replay ten navigation-derived optimization points without changing the v8 source capture.",
        "selection_source": {"navigation_path": str(navigation), "navigation_sha256": sha256(navigation) if navigation.is_file() else None},
        "source_capture": {
            "local_readonly_root": "turbovla_w8a16/data/v8_2026-09-13_231621/raw_capture",
            "server_readonly_root": "/home/nc23/experiments/turbovla_activity_2026-09-13_231621/raw_capture",
            "manifest": source_manifest,
            "files": source_files,
            "copied_into_round": False,
        },
        "selected_optimizations": json.loads(args.selected.read_text(encoding="utf-8")),
        "hardware": {
            "array": {"rows": 16, "physical_cols": 48, "dsp": 768, "mac_per_dsp_per_cycle": 1},
            "clock_mhz": 250.0,
            "target_period_ns": 4.0,
            "device": "xczu7ev-ffvc1156-2-e",
            "command_word_bits": 64,
            "descriptor_word_bits": 512,
            "fifo_depth": 16,
            "full_replay": "virtual event-cycle counter",
            "representative_tile": "cycle-accurate Verilator",
            "synthesis": "Vivado OOC, synthesis-estimated timing; no post-route in this round",
        },
        "software": {
            "model": "TurboVLA",
            "suite": "libero_spatial",
            "task_id": 0,
            "capture_seed": source_manifest.get("source", {}).get("seed"),
            "quantization": {"activation_bits": 16, "weight_bits": 8, "accumulator_bits": 40, "output_bits": 16},
            "descriptor_count": 432,
            "instruction_count": 433,
            "bmm_descriptor_count": 24,
            "unknown_event_count": 0,
        },
        "files": {"source_readonly": source_files, "round_outputs": new_files},
        "evidence_boundary": {
            "measured": [
                "v8 compiler baseline and optimized summaries",
                "Verilator full virtual replay counters",
                "Verilator representative array tile",
                "Verilator FIFO push/pop overlap",
                "Vivado synthesis-estimated OOC resources and timing",
            ],
            "conditional_model": [
                "activation/weight reuse",
                "read-compute-post overlap",
                "contiguous write coalescing",
                "optimized effective GOPS",
            ],
            "unknown": [
                "post-route timing for this top",
                "SAIF/VCD activity power and TOPS/W",
                "board DDR bandwidth",
                "full LIBERO success-rate impact",
            ],
        },
        "notes": [
            "All selected optimizations keep one INT16 x INT8 MAC per DSP; unsafe dual-MAC preadder packing is excluded.",
            "The optimized schedule uses max(read, compute, post)+guard in the cycle model; its serial stage subtotal is not an additional elapsed time.",
            "The synthesis source glob also reads the FIFO regression testbench; the selected top remains tvla_replay_top and the reported top resources are unchanged.",
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.output), "source_files": len(source_files), "round_files": len(new_files)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
