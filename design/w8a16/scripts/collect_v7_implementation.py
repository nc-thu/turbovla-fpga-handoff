"""Collect the v7 250 MHz clear-fanout partition implementation."""
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
V6_RESULTS = ROOT / "data" / "v6_2026-09-13_193556_implementation" / "implementation_results.json"
SIM_JSON = ROOT / "hw" / "v7_2026-09-13_195800_clr_partition_250mhz" / "sim" / "logs" / "verilator_run.json"


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else default
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


def parse_timing(path: Path, period: float) -> dict[str, Any]:
    out: dict[str, Any] = {"target_period_ns": period, "target_frequency_mhz": 1000 / period if period else None, "clock_frequency_mhz": None, "wns_ns": None, "tns_ns": None, "whs_ns": None, "ths_ns": None, "timing_met": None, "data_path_delay_ns": None, "logic_delay_ns": None, "logic_delay_percent": None, "route_delay_ns": None, "route_delay_percent": None, "fmax_estimate_mhz": None, "critical_source": None, "critical_destination": None, "failing_endpoints": None}
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8", errors="replace")
    clock = re.search(r"^\s*clk\s+\{[^}]+\}\s+([0-9.]+)\s+([0-9.]+)", text, re.MULTILINE)
    if clock:
        out["target_period_ns"], out["clock_frequency_mhz"] = number(clock.group(1)), number(clock.group(2))
    summary = re.search(r"^\s*clk\s+(-?[0-9.]+)\s+(-?[0-9.]+)\s+(\d+)\s+(\d+)\s+(-?[0-9.]+)\s+(-?[0-9.]+)", text, re.MULTILINE)
    if summary:
        out["wns_ns"], out["tns_ns"], out["failing_endpoints"] = number(summary.group(1)), number(summary.group(2)), integer(summary.group(3))
        out["whs_ns"], out["ths_ns"] = number(summary.group(5)), number(summary.group(6))
    if out["wns_ns"] is not None:
        out["timing_met"] = out["wns_ns"] >= 0
        required = float(out["target_period_ns"] or period) - float(out["wns_ns"])
        if required > 0:
            out["fmax_estimate_mhz"] = 1000 / required
    pd = re.search(r"Data Path Delay:\s+([0-9.]+)ns\s+\(logic\s+([0-9.]+)ns\s+\(([0-9.]+)%\)\s+route\s+([0-9.]+)ns\s+\(([0-9.]+)%\)\)", text)
    if pd:
        out["data_path_delay_ns"], out["logic_delay_ns"], out["logic_delay_percent"] = number(pd.group(1)), number(pd.group(2)), number(pd.group(3))
        out["route_delay_ns"], out["route_delay_percent"] = number(pd.group(4)), number(pd.group(5))
    src = re.search(r"^\s*Source:\s*(.+)$", text, re.MULTILINE)
    dst = re.search(r"^\s*Destination:\s*(.+)$", text, re.MULTILINE)
    if src:
        out["critical_source"] = src.group(1).strip()
    if dst:
        out["critical_destination"] = dst.group(1).strip()
    return out


def parse_power(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"total_on_chip_w": None, "dynamic_w": None, "static_w": None, "confidence": None, "activity_file": None, "is_vectorless": True, "evidence": "missing"}
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8", errors="replace")
    for key, pattern in {"total_on_chip_w": r"Total On-Chip Power \(W\)\s*\|\s*([0-9.]+)", "dynamic_w": r"\| Dynamic \(W\)\s*\|\s*([0-9.]+)", "static_w": r"\| Device Static \(W\)\s*\|\s*([0-9.]+)"}.items():
        m = re.search(pattern, text)
        if m:
            out[key] = number(m.group(1))
    m = re.search(r"\| Confidence Level\s*\|\s*([^|\r\n]+)", text)
    if m:
        out["confidence"] = m.group(1).strip()
    m = re.search(r"\| Simulation Activity File\s*\|\s*([^|\r\n]+)", text)
    if m:
        out["activity_file"] = m.group(1).strip()
        out["is_vectorless"] = out["activity_file"] in {"---", "", "NA"}
    out["evidence"] = "vectorless_estimate" if out["is_vectorless"] else "activity_file_estimate"
    return out


def parse_route(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"logical_nets": None, "routable_nets": None, "fully_routed_nets": None, "unrouted_nets": None, "routing_errors": None, "status": "missing"}
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8", errors="replace")
    for key, pattern in {"logical_nets": r"# of logical nets[^:]*:\s*(\d+)", "routable_nets": r"# of routable nets[^:]*:\s*(\d+)", "fully_routed_nets": r"# of fully routed nets[^:]*:\s*(\d+)", "routing_errors": r"# of nets with routing errors[^:]*:\s*(\d+)"}.items():
        m = re.search(pattern, text)
        if m:
            out[key] = integer(m.group(1))
    if out["routable_nets"] is not None and out["fully_routed_nets"] is not None:
        out["unrouted_nets"] = out["routable_nets"] - out["fully_routed_nets"]
        out["status"] = "passed" if out["unrouted_nets"] == 0 and out["routing_errors"] == 0 else "failed"
    return out


def parse_drc(path: Path) -> dict[str, Any]:
    out: dict[str, Any] = {"violations": None, "errors": 0, "warnings": 0, "advisories": 0, "status": "missing", "rules": {}}
    if not path.exists():
        return out
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Violations found:\s*(\d+)", text)
    if m:
        out["violations"] = integer(m.group(1))
    summary = re.search(r"Violations found:.*?\n(.*?)\n\s*2\. REPORT DETAILS", text, re.S)
    if summary:
        for rule, severity, count in re.findall(r"\|\s*([A-Z0-9-]+)\s*\|\s*(Error|Critical Warning|Warning|Advisory)\s*\|.*?\|\s*(\d+)\s*\|", summary.group(1)):
            out["rules"][rule] = {"severity": severity, "count": integer(count)}
        out["errors"] = sum(1 for r in out["rules"].values() if r["severity"] == "Error")
        out["warnings"] = sum(1 for r in out["rules"].values() if r["severity"] in {"Warning", "Critical Warning"})
        out["advisories"] = sum(1 for r in out["rules"].values() if r["severity"] == "Advisory")
    out["status"] = "error" if out["errors"] else ("pass_with_warnings" if out["violations"] else "passed")
    return out


def collect(run_dir: Path) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    status = read_json(run_dir / "status.json", {})
    period = float(status.get("target_period_ns", 4.0))
    timing = parse_timing(run_dir / "post_route_timing.rpt", period)
    resources = parse_utilization(run_dir / "post_route_utilization.rpt")
    power = parse_power(run_dir / "post_route_power.rpt")
    route = parse_route(run_dir / "post_route_status.rpt")
    drc = parse_drc(run_dir / "post_route_drc.rpt")
    v5, v6 = read_json(V5_RESULTS, {}), read_json(V6_RESULTS, {})
    old = v6 or v5
    old_t, old_r, old_drc = old.get("timing", {}), old.get("resources", {}), old.get("drc", {})
    delta = {k: resources.get(k) - old_r.get(k) for k in ("total_luts", "logic_luts", "ffs", "dsp", "ramb36", "ramb18", "uram") if isinstance(resources.get(k), (int, float)) and isinstance(old_r.get(k), (int, float))}
    simulation = read_json(SIM_JSON, {"status": "missing", "path": str(SIM_JSON)})
    if isinstance(simulation, dict):
        simulation = {**simulation, "path": str(SIM_JSON)}
    vivado_log = run_dir / "vivado.log"
    if not vivado_log.exists():
        vivado_log = run_dir.parent.parent / "vivado.log"
    return {"schema_version": "tvla_w8a16.vivado_implementation.v7", "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"), "tool": "Vivado 2021.2", "part": status.get("part", "xczu7ev-ffvc1156-2-e"), "top": status.get("top", "w8a16_system_top"), "rows": status.get("rows", 16), "pcols": status.get("pcols", 48), "target_period_ns": period, "status": status.get("status", "unknown"), "started": status.get("started"), "finished": status.get("finished"), "elapsed_s": status.get("elapsed_s"), "run_root": str(run_dir.parent), "output_dir": str(run_dir), "resources": resources, "timing": timing, "power": power, "route": route, "drc": drc, "simulation": simulation, "pipeline_changes": ["w8a16_sysarr: clr 控制按每 8 列分组，保留 group nets，降低 PE accumulator CE 扇出", "v6 的 DSP AREG/BREG/MREG/PREG 和 action-path product/drain 变化保持不变"], "comparison_v6_post_route": {"resources": v6.get("resources", {}), "timing": {k: v6.get("timing", {}).get(k) for k in ("target_period_ns", "wns_ns", "tns_ns", "fmax_estimate_mhz", "data_path_delay_ns", "logic_delay_ns", "logic_delay_percent", "route_delay_ns", "route_delay_percent")}, "route": v6.get("route", {}), "drc": v6.get("drc", {}), "deltas": delta, "note": "v7 与 v6 目标周期相同，适合看扇出分区的方向；最终仍以 post-route 结果为准。"}, "comparison_v5_post_route": {"resources": v5.get("resources", {}), "timing": {k: v5.get("timing", {}).get(k) for k in ("target_period_ns", "wns_ns", "tns_ns", "fmax_estimate_mhz", "data_path_delay_ns")}, "drc": v5.get("drc", {})}, "raw_reports": {name: str(run_dir / name) for name in ["post_synth_timing.rpt", "post_synth_utilization.rpt", "post_place_timing.rpt", "post_place_utilization.rpt", "post_route_timing.rpt", "post_route_critical_paths.rpt", "post_route_utilization.rpt", "post_route_power.rpt", "post_route_status.rpt", "post_route_congestion.rpt", "post_route_drc.rpt", "post_route_methodology.rpt", "post_route_qor_assessment.rpt", "post_route.dcp"]} | {"vivado.log": str(vivado_log)}, "evidence_notes": ["v7 是 4.000 ns（250 MHz）约束下的真实 post-route implementation。", "clr 按 8 列分组，未插入时钟周期；Verilator 11 项测试通过。", "power 是 vectorless activity propagation 估算，没有 SAIF/VCD。", "OOC 工程没有板级时钟、I/O delay、AXI/DDR 和 pin 约束；没有生成 bitstream。"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    result = collect(args.run_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "implementation_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    fields = ["top", "part", "status", "elapsed_s", "total_luts", "logic_luts", "lutram", "srl", "ffs", "dsp", "ramb36", "ramb18", "uram", "wns_ns", "tns_ns", "timing_met", "fmax_estimate_mhz", "data_path_delay_ns", "logic_delay_percent", "route_delay_percent", "total_on_chip_w", "dynamic_w", "static_w", "power_confidence", "power_evidence", "fully_routed_nets", "unrouted_nets", "routing_errors", "drc_violations", "drc_errors", "drc_warnings", "drc_advisories"]
    t, p, route, drc = result["timing"], result["power"], result["route"], result["drc"]
    row = {"top": result["top"], "part": result["part"], "status": result["status"], "elapsed_s": result["elapsed_s"]}
    row.update({k: result["resources"].get(k) for k in ("total_luts", "logic_luts", "lutram", "srl", "ffs", "ramb36", "ramb18", "uram", "dsp")})
    row.update({k: t.get(k) for k in ("wns_ns", "tns_ns", "timing_met", "fmax_estimate_mhz", "data_path_delay_ns", "logic_delay_percent", "route_delay_percent")})
    row.update({"total_on_chip_w": p["total_on_chip_w"], "dynamic_w": p["dynamic_w"], "static_w": p["static_w"], "power_confidence": p["confidence"], "power_evidence": p["evidence"]})
    row.update({k: route.get(k) for k in ("fully_routed_nets", "unrouted_nets", "routing_errors")})
    row.update({"drc_violations": drc["violations"], "drc_errors": drc["errors"], "drc_warnings": drc["warnings"], "drc_advisories": drc["advisories"]})
    with (args.output_dir / "implementation_results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(row)
    print(json.dumps({"output_dir": str(args.output_dir.resolve()), "timing": result["timing"], "resources": result["resources"], "power": result["power"], "drc": result["drc"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
