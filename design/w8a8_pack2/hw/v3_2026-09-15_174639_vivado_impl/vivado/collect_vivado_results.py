#!/usr/bin/env python3
"""Collect the two single-config Vivado runs without inventing missing data."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


NUM = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"


def number(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return "not_available"


def read_meta(run: Path, label: str, period: float):
    meta_path = run / "run_metadata.json"
    if meta_path.exists():
        try:
            data = json.loads(meta_path.read_text(encoding="utf-8-sig"))
            data.setdefault("label", label)
            data.setdefault("period_ns", period)
            data.setdefault("frequency_mhz", 1000.0 / period)
            return data
        except Exception as exc:  # keep collection usable after a partial run
            return {"status": "invalid_metadata", "error": str(exc), "label": label}
    return {
        "status": "not_run",
        "reason": "run_metadata.json not present",
        "label": label,
        "period_ns": period,
        "frequency_mhz": 1000.0 / period,
    }


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def table_value(content: str, names):
    """Find a value in either a Vivado pipe table or a labelled line."""
    for name in names:
        pipe = re.search(r"\|\s*" + re.escape(name) + r"\s*\|\s*(" + NUM + r")", content, re.I)
        if pipe:
            return number(pipe.group(1))
        line = re.search(r"^\s*" + re.escape(name) + r"\s*[:|]\s*(" + NUM + r")", content, re.I | re.M)
        if line:
            return number(line.group(1))
    return "not_available"


def parse_run(run: Path, label: str, period: float):
    meta = read_meta(run, label, period)
    reports = run / "reports"
    util = text(reports / "impl_utilization.rpt") or text(reports / "synth_utilization.rpt")
    timing = text(reports / "impl_timing_summary.rpt") or text(reports / "synth_timing_summary.rpt")
    power = text(reports / "impl_power_vectorless.rpt")
    route = text(reports / "route_status.rpt")
    drc = text(reports / "impl_drc.rpt")

    # Vivado changes the resource row spelling slightly between releases.
    resources = {
        "lut": table_value(util, ["Slice LUTs", "CLB LUTs", "LUT as Logic"]),
        "ff": table_value(util, ["Slice Registers", "CLB Registers", "Registers"]),
        "dsp": table_value(util, ["DSPs", "DSP48E2"]),
        "bram": table_value(util, ["Block RAM Tile", "Block RAMs", "RAMB36/FIFO"]),
    }
    timing_result = {
        "wns_ns": table_value(timing, ["Worst Negative Slack (WNS)", "WNS(ns)", "Setup"]),
        "tns_ns": table_value(timing, ["Total Negative Slack (TNS)", "TNS(ns)"]),
        "whs_ns": table_value(timing, ["Worst Hold Slack (WHS)", "WHS(ns)", "Hold"]),
        "ths_ns": table_value(timing, ["Total Hold Slack (THS)", "THS(ns)"]),
    }
    # A summary row often has all four numbers but no individual labels.
    if timing_result["wns_ns"] == "not_available":
        row = re.search(r"\|\s*.*?(?:MET|PASS|FAIL)\s*\|\s*(" + NUM + r")\s*\|\s*(" + NUM + r")\s*\|\s*(" + NUM + r")\s*\|\s*(" + NUM + r")", timing, re.I)
        if row:
            timing_result = {"wns_ns": number(row.group(1)), "tns_ns": number(row.group(2)),
                             "whs_ns": number(row.group(3)), "ths_ns": number(row.group(4))}
    total_power = table_value(power, ["Total On-Chip Power", "Total Power"])
    if total_power == "not_available":
        match = re.search(r"Total On-Chip Power\s*\(W\).*?((?:" + NUM + r"))", power, re.I | re.S)
        if match:
            total_power = number(match.group(1))

    return {
        "label": label,
        "period_ns": period,
        "frequency_mhz": 1000.0 / period,
        "run": meta,
        "resources": resources,
        "timing": timing_result,
        "power": {"total_on_chip_w": total_power, "source": "vectorless report" if power else "not_available"},
        "route_report_present": bool(route),
        "drc_report_present": bool(drc),
        "report_files": sorted(str(p.relative_to(run)) for p in run.rglob("*.rpt")),
    }


def main():
    here = Path(__file__).resolve().parent
    root = here.parent
    output = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root / "data" / "vivado_results.json"
    runs = [
        ("250MHz", 4.000, root / "reports" / "250MHz"),
        ("303MHz", 3.298, root / "reports" / "303MHz"),
    ]
    result = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "part": "xczu7ev-ffvc1156-2-e",
        "top": "tvla_w8a8_pack2_system_top",
        "runs": [parse_run(path, label, period) for label, period, path in runs],
        "evidence_boundary": "Vivado values are implementation results only when run.status=passed; missing runs are not estimates.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
