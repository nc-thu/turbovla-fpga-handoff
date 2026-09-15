"""Collect the v5 Vivado post-route run into JSON and CSV.

The raw Vivado reports are the evidence.  This parser only extracts the
numbers needed by the report and keeps the distinction between real
post-route timing/utilization and vectorless power estimation.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
V4_RESULTS = ROOT / "data" / "v4_2026-09-13_150700" / "vivado_synth_results.json"


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return default


def as_float(value: str) -> float | None:
    value = value.strip().replace(",", "")
    try:
        return float(value)
    except ValueError:
        return None


def as_int(value: str) -> int | None:
    value = value.strip().replace(",", "")
    try:
        return int(value)
    except ValueError:
        return None


def parse_utilization(path: Path) -> dict[str, int | None]:
    keys = ["total_luts", "logic_luts", "lutram", "srl", "ffs", "ramb36", "ramb18", "uram", "dsp"]
    result = {key: None for key in keys}
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|") or "w8a16_system_top" not in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        # Instance, module, then the nine numeric columns in the report.
        if len(cells) < 11 or cells[0] != "w8a16_system_top":
            continue
        values = cells[2:11]
        for key, value in zip(keys, values):
            result[key] = as_int(value)
        break
    return result


def parse_timing(path: Path, period_ns: float) -> dict[str, Any]:
    result: dict[str, Any] = {
        "target_period_ns": period_ns,
        "target_frequency_mhz": 1000.0 / period_ns if period_ns else None,
        "clock_frequency_mhz": None,
        "wns_ns": None,
        "tns_ns": None,
        "whs_ns": None,
        "ths_ns": None,
        "timing_met": None,
        "data_path_delay_ns": None,
        "logic_delay_ns": None,
        "logic_delay_percent": None,
        "route_delay_ns": None,
        "route_delay_percent": None,
        "fmax_estimate_mhz": None,
        "critical_source": None,
        "critical_destination": None,
        "failing_endpoints": None,
    }
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    clock = re.search(r"^\s*clk\s+\{[^}]+\}\s+([0-9.]+)\s+([0-9.]+)", text, re.MULTILINE)
    if clock:
        result["target_period_ns"] = float(clock.group(1))
        result["clock_frequency_mhz"] = float(clock.group(2))
    setup = re.search(
        r"Setup\s*:\s+(\d+)\s+Failing Endpoints,\s+Worst Slack\s+(-?[0-9.]+)ns,\s+Total Violation\s+(-?[0-9.]+)ns",
        text,
    )
    if setup:
        result["failing_endpoints"] = int(setup.group(1))
        result["wns_ns"] = float(setup.group(2))
        result["tns_ns"] = float(setup.group(3))
        result["timing_met"] = result["wns_ns"] >= 0.0
        required = float(result["target_period_ns"]) - result["wns_ns"]
        if required > 0:
            result["fmax_estimate_mhz"] = 1000.0 / required
    hold = re.search(r"Hold\s*:\s+\S+\s+Failing Endpoints,\s+Worst Slack\s+(-?[0-9.]+)ns", text)
    if hold:
        result["whs_ns"] = float(hold.group(1))
    path_delay = re.search(
        r"Data Path Delay:\s+([0-9.]+)ns\s+\(logic\s+([0-9.]+)ns\s+\(([0-9.]+)%\)\s+route\s+([0-9.]+)ns\s+\(([0-9.]+)%\)\)",
        text,
    )
    if path_delay:
        result["data_path_delay_ns"] = float(path_delay.group(1))
        result["logic_delay_ns"] = float(path_delay.group(2))
        result["logic_delay_percent"] = float(path_delay.group(3))
        result["route_delay_ns"] = float(path_delay.group(4))
        result["route_delay_percent"] = float(path_delay.group(5))
    source = re.search(r"^\s*Source:\s*(.+)$", text, re.MULTILINE)
    destination = re.search(r"^\s*Destination:\s*(.+)$", text, re.MULTILINE)
    if source:
        result["critical_source"] = source.group(1).strip()
    if destination:
        result["critical_destination"] = destination.group(1).strip()
    # The timing summary table is the most reliable source for TNS when the
    # detailed section changes wording between Vivado releases.
    summary = re.search(
        r"^\s*(-?[0-9.]+)\s+(-?[0-9.]+)\s+(\d+)\s+\d+\s+(-?[0-9.]+)\s+(-?[0-9.]+)",
        text,
        re.MULTILINE,
    )
    if summary and result["wns_ns"] is None:
        result["wns_ns"] = float(summary.group(1))
        result["tns_ns"] = float(summary.group(2))
        result["whs_ns"] = float(summary.group(5))
        result["ths_ns"] = float(summary.group(6))
        result["timing_met"] = result["wns_ns"] >= 0.0
    return result


def parse_power(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "total_on_chip_w": None,
        "dynamic_w": None,
        "static_w": None,
        "confidence": None,
        "activity_file": None,
        "is_vectorless": True,
        "evidence": "missing",
    }
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    for key, pattern in {
        "total_on_chip_w": r"Total On-Chip Power \(W\)\s*\|\s*([0-9.]+)",
        "dynamic_w": r"\| Dynamic \(W\)\s*\|\s*([0-9.]+)",
        "static_w": r"\| Device Static \(W\)\s*\|\s*([0-9.]+)",
    }.items():
        found = re.search(pattern, text)
        if found:
            result[key] = float(found.group(1))
    confidence = re.search(r"\| Confidence Level\s*\|\s*([^|\r\n]+)", text)
    if confidence:
        result["confidence"] = confidence.group(1).strip()
    activity = re.search(r"\| Simulation Activity File\s*\|\s*([^|\r\n]+)", text)
    if activity:
        result["activity_file"] = activity.group(1).strip()
        result["is_vectorless"] = activity.group(1).strip() in {"---", "", "NA"}
    result["evidence"] = "vectorless_estimate" if result["is_vectorless"] else "activity_file_estimate"
    return result


def parse_route(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"logical_nets": None, "routable_nets": None, "fully_routed_nets": None, "unrouted_nets": 0, "routing_errors": 0, "status": "missing"}
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    patterns = {
        "logical_nets": r"# of logical nets[^:]*:\s*(\d+)",
        "routable_nets": r"# of routable nets[^:]*:\s*(\d+)",
        "fully_routed_nets": r"# of fully routed nets[^:]*:\s*(\d+)",
        "routing_errors": r"# of nets with routing errors[^:]*:\s*(\d+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            result[key] = int(match.group(1))
    if result["routable_nets"] is not None and result["fully_routed_nets"] is not None:
        result["unrouted_nets"] = result["routable_nets"] - result["fully_routed_nets"]
        result["status"] = "passed" if result["unrouted_nets"] == 0 and result["routing_errors"] == 0 else "failed"
    return result


def parse_drc(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"violations": None, "errors": 0, "warnings": 0, "advisories": 0, "status": "missing"}
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    found = re.search(r"Violations found:\s*(\d+)", text)
    if found:
        result["violations"] = int(found.group(1))
    result["errors"] = len(re.findall(r"\|[^|]+\|\s*Error\s*\|", text, re.IGNORECASE))
    result["warnings"] = len(re.findall(r"\|[^|]+\|\s*Warning\s*\|", text, re.IGNORECASE))
    result["advisories"] = len(re.findall(r"\|[^|]+\|\s*Advisory\s*\|", text, re.IGNORECASE))
    result["status"] = "error" if result["errors"] else ("pass_with_warnings" if result["violations"] else "passed")
    return result


def locate_run(path: Path) -> tuple[Path, Path]:
    path = path.resolve()
    if (path / "status.json").exists():
        return path, path.parent
    candidate = path / "system_top"
    if (candidate / "status.json").exists():
        return candidate, path
    raise FileNotFoundError(f"status.json not found under {path}")


def collect(run_root: Path) -> dict[str, Any]:
    out, launcher_root = locate_run(run_root)
    status = read_json(out / "status.json", {})
    launcher = read_json(launcher_root / "run_summary.json", {})
    period = float(status.get("target_period_ns", launcher.get("target_period_ns", 3.298)))
    timing = parse_timing(out / "post_route_timing.rpt", period)
    util = parse_utilization(out / "post_route_utilization.rpt")
    power = parse_power(out / "post_route_power.rpt")
    route = parse_route(out / "post_route_status.rpt")
    drc = parse_drc(out / "post_route_drc.rpt")

    v4 = read_json(V4_RESULTS, {})
    v4_top = next((r for r in v4.get("records", []) if r.get("top") == "w8a16_system_top"), {})
    v4_timing = v4_top.get("timing", {}) if isinstance(v4_top, dict) else {}
    v4_util = {key: v4_top.get(key) for key in ("total_luts", "logic_luts", "ffs", "dsp", "ramb36", "ramb18", "uram")}
    deltas = {}
    for key in v4_util:
        if isinstance(util.get(key), (int, float)) and isinstance(v4_util.get(key), (int, float)):
            deltas[key] = util[key] - v4_util[key]

    return {
        "schema_version": "tvla_w8a16.vivado_implementation.v5",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tool": "Vivado 2021.2",
        "part": status.get("part", launcher.get("part", "xczu7ev-ffvc1156-2-e")),
        "top": status.get("top", "w8a16_system_top"),
        "rows": status.get("rows", 16),
        "pcols": status.get("pcols", 48),
        "target_period_ns": period,
        "status": status.get("status", launcher.get("status", "unknown")),
        "started": launcher.get("started", status.get("started")),
        "finished": launcher.get("finished", status.get("finished")),
        "elapsed_s": launcher.get("elapsed_s", status.get("elapsed_s")),
        "run_root": str(launcher_root),
        "output_dir": str(out),
        "resources": util,
        "timing": timing,
        "power": power,
        "route": route,
        "drc": drc,
        "comparison_v4_synth": {
            "resources": v4_util,
            "timing": {key: v4_timing.get(key) for key in ("wns_ns", "tns_ns", "fmax_estimate_mhz", "data_path_delay_ns")},
            "deltas": deltas,
            "note": "v4 是同一顶层的综合结果；v5 是 post-route implementation，不能把两者当作同一阶段的直接 PPA 对比。",
        },
        "raw_reports": {name: str(out / name) for name in [
            "post_route_timing.rpt", "post_route_critical_paths.rpt", "post_route_utilization.rpt",
            "post_route_power.rpt", "post_route_status.rpt", "post_route_congestion.rpt", "post_route_drc.rpt",
            "post_route_methodology.rpt", "post_route_qor_assessment.rpt", "post_route.dcp", "vivado.log",
        ]},
        "evidence_notes": [
            "timing/utilization/route 是真实 post-route implementation 报告。",
            "power 使用 report_power 的 vectorless activity propagation，没有仿真 SAIF/VCD，属于估算而非板上实测。",
            "OOC wrapper 没有板级 pin、AXI/DDR 和时钟缓冲约束；NSTD/UCIO 类 DRC 不能代表板级设计已就绪。",
            "本轮没有生成 bitstream，也没有修改 v4 RTL。",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    result = collect(args.run_root)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output = (args.output_dir or (ROOT / "data" / f"v5_{stamp}_implementation")).resolve()
    output.mkdir(parents=True, exist_ok=True)
    (output / "implementation_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    fields = ["top", "part", "status", "elapsed_s", "total_luts", "logic_luts", "ffs", "dsp", "ramb36", "ramb18", "uram", "wns_ns", "tns_ns", "timing_met", "fmax_estimate_mhz", "data_path_delay_ns", "logic_delay_percent", "route_delay_percent", "total_on_chip_w", "dynamic_w", "static_w", "power_confidence", "power_evidence", "fully_routed_nets", "unrouted_nets", "routing_errors", "drc_violations", "drc_errors", "drc_warnings", "drc_advisories"]
    timing, power, route, drc = result["timing"], result["power"], result["route"], result["drc"]
    row = {
        "top": result["top"], "part": result["part"], "status": result["status"], "elapsed_s": result["elapsed_s"],
        **result["resources"], "wns_ns": timing["wns_ns"], "tns_ns": timing["tns_ns"], "timing_met": timing["timing_met"],
        "fmax_estimate_mhz": timing["fmax_estimate_mhz"], "data_path_delay_ns": timing["data_path_delay_ns"],
        "logic_delay_percent": timing["logic_delay_percent"], "route_delay_percent": timing["route_delay_percent"],
        "total_on_chip_w": power["total_on_chip_w"], "dynamic_w": power["dynamic_w"], "static_w": power["static_w"],
        "power_confidence": power["confidence"], "power_evidence": power["evidence"], **route,
        "drc_violations": drc["violations"], "drc_errors": drc["errors"], "drc_warnings": drc["warnings"], "drc_advisories": drc["advisories"],
    }
    with (output / "implementation_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({field: row.get(field) for field in fields})
    print(json.dumps({"output_dir": str(output), "status": result["status"], "timing": result["timing"], "power": result["power"], "resources": result["resources"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
