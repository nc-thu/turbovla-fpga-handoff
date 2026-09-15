"""Collect the v2 camera-ready Vivado runs without modifying old summaries.

The v2 launcher intentionally stores one directory per configuration rather
than a single project run.  This collector assembles those reports into one
machine-readable file and keeps synthesis timing separate from post-route
timing.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RUNS = ROOT / "hw" / "v2_2026-09-13_1113_w8a16_camera_ready_rtl" / "synth" / "runs"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from collect_vivado_synth import parse_drc, parse_timing, parse_utilization, read_json  # noqa: E402


RUN_NAMES = [
    "2026-09-13_130000_array_1x1",
    "2026-09-13_125300_array_4x4",
    "2026-09-13_125500_array_16x48",
    "2026-09-13_153000_system_v11",
]


def collect() -> dict:
    records = []
    for name in RUN_NAMES:
        root = RUNS / name
        status = read_json(root / "status.json", {})
        if not status:
            records.append({"name": name, "status": "missing", "output_dir": str(root)})
            continue
        timing = parse_timing(root / "timing.rpt", float(status.get("target_period_ns", 3.298)))
        util = parse_utilization(root / "utilization.rpt")
        drc = parse_drc(root / "drc.rpt")
        records.append({
            "name": name,
            "top": status.get("top"),
            "rows": status.get("rows"),
            "pcols": status.get("pcols"),
            "part": status.get("part", "xczu7ev-ffvc1156-2-e"),
            "status": status.get("status", "unknown"),
            "started": status.get("started"),
            "finished": status.get("finished"),
            "elapsed_s": status.get("elapsed_s"),
            "output_dir": str(root),
            **util,
            "timing": timing,
            "drc": drc,
            "raw_reports": {
                "utilization": str(root / "utilization.rpt"),
                "timing": str(root / "timing.rpt"),
                "drc": str(root / "drc.rpt"),
                "checkpoint": str(root / "post_synth.dcp"),
            },
        })
    return {
        "schema_version": "tvla_w8a16.vivado_synth.v2",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tool": "Vivado 2021.2",
        "part": "xczu7ev-ffvc1156-2-e",
        "target_period_ns": 3.298,
        "timing_is_synthesis_estimate": True,
        "status": "passed" if records and all(r.get("status") == "passed" for r in records) else "incomplete_or_failed",
        "records": records,
        "notes": [
            "v11 是包含 runtime、DMA、vector_ops、requant 和 16×48 GEMM 阵列的系统 top。",
            "array 记录分别来自 1×1、4×4 和 16×48 wrapper。",
            "WNS/Fmax 来自 synth_design；未执行 place_design、route_design、post-route phys_opt 或功耗分析。",
            "OOC 输入没有板级 I/O 位置和电气约束，NSTD/UCIO 不能解释为内部时序失败。",
        ],
    }


def main() -> int:
    result = collect()
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "vivado_synth_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    fields = ["name", "top", "rows", "pcols", "status", "elapsed_s", "total_luts", "ffs", "dsp", "ramb36", "ramb18", "uram", "wns_ns", "timing_met", "fmax_estimate_mhz", "data_path_delay_ns", "logic_delay_percent", "route_delay_percent", "drc_status", "drc_errors", "drc_warnings"]
    with (DATA / "vivado_synth_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in result["records"]:
            t, d = r.get("timing", {}), r.get("drc", {})
            writer.writerow({
                "name": r.get("name"), "top": r.get("top"), "rows": r.get("rows"), "pcols": r.get("pcols"), "status": r.get("status"), "elapsed_s": r.get("elapsed_s"), "total_luts": r.get("total_luts"), "ffs": r.get("ffs"), "dsp": r.get("dsp"), "ramb36": r.get("ramb36"), "ramb18": r.get("ramb18"), "uram": r.get("uram"), "wns_ns": t.get("wns_ns"), "timing_met": t.get("timing_met"), "fmax_estimate_mhz": t.get("fmax_estimate_mhz"), "data_path_delay_ns": t.get("data_path_delay_ns"), "logic_delay_percent": t.get("logic_delay_percent"), "route_delay_percent": t.get("route_delay_percent"), "drc_status": d.get("status"), "drc_errors": d.get("errors"), "drc_warnings": d.get("warnings"),
            })
    print(json.dumps({"status": result["status"], "records": len(result["records"]), "output": str(DATA / "vivado_synth_results.json")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
