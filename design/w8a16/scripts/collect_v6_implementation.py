"""Collect the v6 250 MHz Vivado implementation run.

The parser keeps post-route evidence separate from intermediate estimates.  The
v6 round adds DSP A/B input registers and a registered product/accumulator
boundary; it is compared with v5 only as a directional reference because the
target period and RTL are different.
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
V5_RESULTS = ROOT / "data" / "v5_2026-09-13_173359_implementation" / "implementation_results.json"
SIM_JSON = ROOT / "hw" / "v6_2026-09-13_182745_dsp_pipeline_250mhz" / "sim" / "logs" / "verilator_run.json"


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return default


def number(value: str) -> float | None:
    try:
        return float(value.strip().replace(",", ""))
    except (TypeError, ValueError):
        return None


def integer(value: str) -> int | None:
    try:
        return int(value.strip().replace(",", ""))
    except (TypeError, ValueError):
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
        if len(cells) < 11 or cells[0] != "w8a16_system_top":
            continue
        for key, value in zip(keys, cells[2:11]):
            result[key] = integer(value)
        return result
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
        result["target_period_ns"] = number(clock.group(1))
        result["clock_frequency_mhz"] = number(clock.group(2))
    # The clock summary row is stable across the Vivado 2021.2 reports.
    summary = re.search(
        r"^\s*clk\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s+(\d+)\s+(\d+)\s+(-?[0-9.]+)\s+(-?[0-9.]+)",
        text,
        re.MULTILINE,
    )
    if summary:
        result["wns_ns"] = number(summary.group(1))
        result["tns_ns"] = number(summary.group(2))
        result["failing_endpoints"] = integer(summary.group(3))
        result["whs_ns"] = number(summary.group(5))
        result["ths_ns"] = number(summary.group(6))
    if result["wns_ns"] is not None:
        result["timing_met"] = result["wns_ns"] >= 0.0
        required = float(result["target_period_ns"] or period_ns) - float(result["wns_ns"])
        if required > 0:
            result["fmax_estimate_mhz"] = 1000.0 / required
    path_delay = re.search(
        r"Data Path Delay:\s+([0-9.]+)ns\s+\(logic\s+([0-9.]+)ns\s+\(([0-9.]+)%\)\s+route\s+([0-9.]+)ns\s+\(([0-9.]+)%\)\)",
        text,
    )
    if path_delay:
        result["data_path_delay_ns"] = number(path_delay.group(1))
        result["logic_delay_ns"] = number(path_delay.group(2))
        result["logic_delay_percent"] = number(path_delay.group(3))
        result["route_delay_ns"] = number(path_delay.group(4))
        result["route_delay_percent"] = number(path_delay.group(5))
    source = re.search(r"^\s*Source:\s*(.+)$", text, re.MULTILINE)
    destination = re.search(r"^\s*Destination:\s*(.+)$", text, re.MULTILINE)
    if source:
        result["critical_source"] = source.group(1).strip()
    if destination:
        result["critical_destination"] = destination.group(1).strip()
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
            result[key] = number(found.group(1))
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
    result: dict[str, Any] = {
        "logical_nets": None,
        "routable_nets": None,
        "fully_routed_nets": None,
        "unrouted_nets": None,
        "routing_errors": None,
        "status": "missing",
    }
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    for key, pattern in {
        "logical_nets": r"# of logical nets[^:]*:\s*(\d+)",
        "routable_nets": r"# of routable nets[^:]*:\s*(\d+)",
        "fully_routed_nets": r"# of fully routed nets[^:]*:\s*(\d+)",
        "routing_errors": r"# of nets with routing errors[^:]*:\s*(\d+)",
    }.items():
        found = re.search(pattern, text)
        if found:
            result[key] = integer(found.group(1))
    if result["routable_nets"] is not None and result["fully_routed_nets"] is not None:
        result["unrouted_nets"] = result["routable_nets"] - result["fully_routed_nets"]
        result["status"] = "passed" if result["unrouted_nets"] == 0 and result["routing_errors"] == 0 else "failed"
    return result


def parse_drc(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"violations": None, "errors": 0, "warnings": 0, "advisories": 0, "status": "missing", "rules": {}}
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    found = re.search(r"Violations found:\s*(\d+)", text)
    if found:
        result["violations"] = integer(found.group(1))
    # Count rule rows, not every occurrence in the details section.
    summary = re.search(r"Violations found:.*?\n(.*?)\n\s*2\. REPORT DETAILS", text, re.S)
    if summary:
        for rule, severity, count in re.findall(r"\|\s*([A-Z0-9-]+)\s*\|\s*(Error|Critical Warning|Warning|Advisory)\s*\|.*?\|\s*(\d+)\s*\|", summary.group(1)):
            result["rules"][rule] = {"severity": severity, "count": integer(count)}
        result["errors"] = sum(1 for row in result["rules"].values() if row["severity"] == "Error")
        result["warnings"] = sum(1 for row in result["rules"].values() if row["severity"] in {"Warning", "Critical Warning"})
        result["advisories"] = sum(1 for row in result["rules"].values() if row["severity"] == "Advisory")
    result["status"] = "error" if result["errors"] else ("pass_with_warnings" if result["violations"] else "passed")
    return result


def locate_run(path: Path) -> Path:
    path = path.resolve()
    if (path / "status.json").exists():
        return path
    raise FileNotFoundError(f"status.json not found under {path}")


def collect(run_root: Path) -> dict[str, Any]:
    out = locate_run(run_root)
    status = read_json(out / "status.json", {})
    period = float(status.get("target_period_ns", 4.0))
    timing = parse_timing(out / "post_route_timing.rpt", period)
    resources = parse_utilization(out / "post_route_utilization.rpt")
    power = parse_power(out / "post_route_power.rpt")
    route = parse_route(out / "post_route_status.rpt")
    drc = parse_drc(out / "post_route_drc.rpt")
    v5 = read_json(V5_RESULTS, {})
    v5_t = v5.get("timing", {}) if isinstance(v5, dict) else {}
    v5_r = v5.get("resources", {}) if isinstance(v5, dict) else {}
    v5_drc_path = Path(v5.get("raw_reports", {}).get("post_route_drc.rpt", "")) if isinstance(v5, dict) else Path()
    v5_drc = parse_drc(v5_drc_path) if v5_drc_path.exists() else {}
    delta = {key: resources.get(key) - v5_r.get(key) for key in ("total_luts", "logic_luts", "ffs", "dsp", "ramb36", "ramb18", "uram") if isinstance(resources.get(key), (int, float)) and isinstance(v5_r.get(key), (int, float))}
    simulation = read_json(SIM_JSON, {"status": "missing", "path": str(SIM_JSON)})
    if isinstance(simulation, dict):
        simulation = {**simulation, "path": str(SIM_JSON)}
    vivado_log = out / "vivado.log"
    if not vivado_log.exists():
        vivado_log = out.parents[2] / "vivado.log"
    return {
        "schema_version": "tvla_w8a16.vivado_implementation.v6",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tool": "Vivado 2021.2",
        "part": status.get("part", "xczu7ev-ffvc1156-2-e"),
        "top": status.get("top", "w8a16_system_top"),
        "rows": status.get("rows", 16),
        "pcols": status.get("pcols", 48),
        "target_period_ns": period,
        "status": status.get("status", "unknown"),
        "started": status.get("started"),
        "finished": status.get("finished"),
        "elapsed_s": status.get("elapsed_s"),
        "run_root": str(out.parent),
        "output_dir": str(out),
        "resources": resources,
        "timing": timing,
        "power": power,
        "route": route,
        "drc": drc,
        "simulation": simulation,
        "pipeline_changes": [
            "w8a16_mult: DSP AREG/BREG=1, MREG/PREG=1",
            "w8a16_pe: product_r/product_v 保持寄存，输入使用一拍对齐",
            "w8a16_action_path: mac operand/product register and two-cycle accumulation drain",
        ],
        "comparison_v5_post_route": {
            "resources": v5_r,
            "timing": {
                "target_period_ns": v5.get("target_period_ns", v5_t.get("target_period_ns")),
                "wns_ns": v5_t.get("wns_ns"),
                "tns_ns": v5_t.get("tns_ns"),
                "fmax_estimate_mhz": v5_t.get("fmax_estimate_mhz"),
                "data_path_delay_ns": v5_t.get("data_path_delay_ns"),
            },
            "route": v5.get("route", {}),
            "drc": v5_drc,
            "deltas": delta,
            "note": "v5 与 v6 都是 post-route，但目标周期和 RTL 不同；差值只用于方向判断，不是隔离的单变量因果实验。",
        },
        "raw_reports": {name: str(out / name) for name in [
            "post_synth_timing.rpt", "post_synth_utilization.rpt", "post_place_timing.rpt", "post_place_utilization.rpt",
            "post_route_timing.rpt", "post_route_critical_paths.rpt", "post_route_utilization.rpt", "post_route_power.rpt",
            "post_route_status.rpt", "post_route_congestion.rpt", "post_route_drc.rpt", "post_route_methodology.rpt",
            "post_route_qor_assessment.rpt", "post_route.dcp",
        ]} | {"vivado.log": str(vivado_log)},
        "evidence_notes": [
            "timing/utilization/route 是 250 MHz 约束下的真实 post-route implementation 报告。",
            "route 的 184306 条可路由网络全部完成，routing errors=0；WNS 仍为负，因此 4.000 ns 目标未通过。",
            "power 是 Vivado vectorless activity propagation 的估算，没有 SAIF/VCD，也不是板上实测。",
            "OOC wrapper 没有板级 pin、AXI/DDR、时钟 buffer 和 I/O delay 约束；不能据此生成 bitstream。",
            "本轮只复制并修改 v4/v5 工作区中的 v6 RTL；旧目录未覆盖。",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()
    result = collect(args.run_root)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output = (args.output_dir or (ROOT / "data" / f"v6_{stamp}_implementation")).resolve()
    output.mkdir(parents=True, exist_ok=True)
    json_path = output / "implementation_results.json"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    timing, power, route, drc = result["timing"], result["power"], result["route"], result["drc"]
    fields = ["top", "part", "status", "elapsed_s", "total_luts", "logic_luts", "ffs", "dsp", "ramb36", "ramb18", "uram", "wns_ns", "tns_ns", "timing_met", "fmax_estimate_mhz", "data_path_delay_ns", "logic_delay_percent", "route_delay_percent", "total_on_chip_w", "dynamic_w", "static_w", "power_confidence", "power_evidence", "fully_routed_nets", "unrouted_nets", "routing_errors", "drc_violations", "drc_errors", "drc_warnings", "drc_advisories"]
    row = {
        "top": result["top"], "part": result["part"], "status": result["status"], "elapsed_s": result["elapsed_s"], **result["resources"],
        "wns_ns": timing["wns_ns"], "tns_ns": timing["tns_ns"], "timing_met": timing["timing_met"], "fmax_estimate_mhz": timing["fmax_estimate_mhz"],
        "data_path_delay_ns": timing["data_path_delay_ns"], "logic_delay_percent": timing["logic_delay_percent"], "route_delay_percent": timing["route_delay_percent"],
        "total_on_chip_w": power["total_on_chip_w"], "dynamic_w": power["dynamic_w"], "static_w": power["static_w"], "power_confidence": power["confidence"], "power_evidence": power["evidence"],
        **route, "drc_violations": drc["violations"], "drc_errors": drc["errors"], "drc_warnings": drc["warnings"], "drc_advisories": drc["advisories"],
    }
    with (output / "implementation_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({field: row.get(field) for field in fields})
    print(json.dumps({"output_dir": str(output), "status": result["status"], "timing": result["timing"], "power": result["power"], "resources": result["resources"], "drc": result["drc"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
