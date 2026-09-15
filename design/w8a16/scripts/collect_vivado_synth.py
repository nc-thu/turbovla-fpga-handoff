"""Collect the local Vivado synthesis run into machine-readable summaries.

The raw Vivado reports remain the source of truth.  This parser only extracts
the top-level row and the first setup path so the HTML can show a compact
summary without copying report text into prose.  Timing values are synthesis
estimates at 3.298 ns; they are deliberately not presented as post-route Fmax.
"""
from __future__ import annotations

import csv
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RTL_RESULTS = DATA / "rtl_results.json"


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def number(value: str) -> int | None:
    value = value.strip().replace(",", "")
    if not re.fullmatch(r"-?\d+", value):
        return None
    return int(value)


def parse_utilization(path: Path) -> dict[str, int | None]:
    result: dict[str, int | None] = {
        "total_luts": None,
        "logic_luts": None,
        "lutram": None,
        "srl": None,
        "ffs": None,
        "ramb36": None,
        "ramb18": None,
        "uram": None,
        "dsp": None,
    }
    if not path.exists():
        return result
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "(top)" not in line or not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        try:
            top_idx = next(i for i, c in enumerate(cells) if "(top)" in c)
        except StopIteration:
            continue
        vals = cells[top_idx + 1 : top_idx + 10]
        if len(vals) < 9:
            continue
        keys = list(result)
        for key, value in zip(keys, vals):
            result[key] = number(value)
        break
    return result


def parse_timing(path: Path, period_ns: float) -> dict[str, Any]:
    result: dict[str, Any] = {
        "target_period_ns": period_ns,
        "target_frequency_mhz": 1000.0 / period_ns,
        "clock_frequency_mhz": None,
        "wns_ns": None,
        "tns_ns": None,
        "timing_met": None,
        "data_path_delay_ns": None,
        "logic_delay_ns": None,
        "logic_delay_percent": None,
        "route_delay_ns": None,
        "route_delay_percent": None,
        "fmax_estimate_mhz": None,
        "critical_source": None,
        "critical_destination": None,
    }
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    clock = re.search(r"^\s*clk\s+\{[^}]+\}\s+([0-9.]+)\s+([0-9.]+)", text, re.MULTILINE)
    if clock:
        result["target_period_ns"] = float(clock.group(1))
        result["clock_frequency_mhz"] = float(clock.group(2))
    setup = re.search(
        r"Setup\s*:\s+\S+\s+Failing Endpoints,\s+Worst Slack\s+(-?[0-9.]+)ns",
        text,
    )
    if setup:
        result["wns_ns"] = float(setup.group(1))
        result["timing_met"] = result["wns_ns"] >= 0.0
        available = result["target_period_ns"] - result["wns_ns"]
        if available > 0:
            result["fmax_estimate_mhz"] = 1000.0 / available
    tns = re.search(r"Total Violation\s+(-?[0-9.]+)ns", text)
    if tns:
        result["tns_ns"] = float(tns.group(1))
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
    return result


def parse_drc(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {"violations": None, "errors": 0, "warnings": 0, "status": "missing"}
    if not path.exists():
        return result
    text = path.read_text(encoding="utf-8", errors="replace")
    found = re.search(r"Violations found:\s*(\d+)", text)
    if found:
        result["violations"] = int(found.group(1))
    # Synthesis DRC for this design currently reports DPIP/DPOP as warnings.
    result["errors"] = len(re.findall(r"\|[^|]+\|\s*Error\s*\|", text, re.IGNORECASE))
    result["warnings"] = len(re.findall(r"\|[^|]+\|\s*Warning\s*\|", text, re.IGNORECASE))
    result["status"] = "pass" if result["errors"] == 0 else "error"
    return result


def collect(run_root: Path) -> dict[str, Any]:
    summary = read_json(run_root / "run_summary.json", {})
    records = []
    for rec in summary.get("records", []):
        out = Path(rec.get("output_dir", run_root / rec.get("name", "unknown")))
        status = read_json(out / "status.json", {})
        period = float(status.get("target_period_ns", summary.get("target_period_ns", 3.298)))
        util = parse_utilization(out / "utilization.rpt")
        timing = parse_timing(out / "timing.rpt", period)
        drc = parse_drc(out / "drc.rpt")
        row: dict[str, Any] = {
            "name": rec.get("name"),
            "top": rec.get("top"),
            "rows": rec.get("rows"),
            "pcols": rec.get("pcols"),
            "status": status.get("status", rec.get("status", "unknown")),
            "exit_code": rec.get("exit_code"),
            # run_summary covers the complete launcher invocation; status.json
            # covers synth_top.tcl itself.  Prefer the launcher timestamps so
            # the report's duration includes Vivado startup and shutdown.
            "started": rec.get("started", status.get("started")),
            "finished": rec.get("finished", status.get("finished")),
            "elapsed_s": rec.get("elapsed_s", status.get("elapsed_s")),
            "message": status.get("message", ""),
            "output_dir": str(out),
            **util,
            "timing": timing,
            "drc": drc,
            "raw_reports": {
                "utilization": str(out / "utilization.rpt"),
                "timing": str(out / "timing.rpt"),
                "drc": str(out / "drc.rpt"),
                "checkpoint": str(out / "post_synth.dcp"),
            },
        }
        records.append(row)
    result = {
        "schema_version": "tvla_w8a16.vivado_synth.v1",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "tool": "Vivado 2021.2",
        "vivado": summary.get("vivado"),
        "part": summary.get("part", "xczu7ev-ffvc1156-2-e"),
        "target_period_ns": summary.get("target_period_ns", 3.298),
        "run_root": str(run_root),
        "status": "passed" if records and all(r["status"] == "passed" for r in records) else "incomplete_or_failed",
        "timing_is_synthesis_estimate": True,
        "records": records,
        "notes": [
            "逻辑综合已运行；Fmax 由综合 WNS 按 target_period - WNS 计算，仅作估算。",
            "未执行 place_design、route_design、post-route phys_opt 或功耗分析。",
            "系统顶层是包含 runtime、DMA、vector_ops、requant 的集成壳，不是最终板级 AXI/DDR 顶层。",
        ],
    }
    return result


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", type=Path)
    args = parser.parse_args()
    result = collect(args.run_root.resolve())
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "vivado_synth_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    fields = [
        "name", "top", "rows", "pcols", "status", "elapsed_s", "total_luts", "logic_luts",
        "ffs", "dsp", "ramb36", "ramb18", "uram", "wns_ns", "timing_met", "fmax_estimate_mhz",
        "data_path_delay_ns", "logic_delay_percent", "route_delay_percent", "drc_status", "drc_errors", "drc_warnings",
    ]
    with (DATA / "vivado_synth_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in result["records"]:
            t = row.get("timing", {})
            d = row.get("drc", {})
            writer.writerow({
                "name": row.get("name"), "top": row.get("top"), "rows": row.get("rows"), "pcols": row.get("pcols"),
                "status": row.get("status"), "elapsed_s": row.get("elapsed_s"), "total_luts": row.get("total_luts"),
                "logic_luts": row.get("logic_luts"), "ffs": row.get("ffs"), "dsp": row.get("dsp"),
                "ramb36": row.get("ramb36"), "ramb18": row.get("ramb18"), "uram": row.get("uram"),
                "wns_ns": t.get("wns_ns"), "timing_met": t.get("timing_met"),
                "fmax_estimate_mhz": t.get("fmax_estimate_mhz"), "data_path_delay_ns": t.get("data_path_delay_ns"),
                "logic_delay_percent": t.get("logic_delay_percent"), "route_delay_percent": t.get("route_delay_percent"),
                "drc_status": d.get("status"), "drc_errors": d.get("errors"), "drc_warnings": d.get("warnings"),
            })
    rtl = read_json(RTL_RESULTS, {})
    if rtl:
        rtl["generated_at"] = result["generated_at"]
        rtl["ooc"] = {
            "status": result["status"],
            "tool": "Vivado 2021.2 local",
            "part": result["part"],
            "clock_ns": result["target_period_ns"],
            "run_root": result["run_root"],
            "timing_is_synthesis_estimate": True,
            "levels": [
                {"name": r["name"], "status": r["status"], "dsp": r.get("dsp"), "luts": r.get("total_luts"), "ffs": r.get("ffs"), "wns_ns": r.get("timing", {}).get("wns_ns"), "fmax_estimate_mhz": r.get("timing", {}).get("fmax_estimate_mhz"), "drc": r.get("drc", {})}
                for r in result["records"]
            ],
            "reason": "逻辑综合完成；不是 post-route。",
        }
        rtl["limitations"] = [x for x in rtl.get("limitations", []) if "Vivado OOC" not in x and "Vivado/vivado OOC" not in x]
        rtl["limitations"].append("Vivado 逻辑综合已完成，但未运行 post-route、功耗或板级时序收敛。")
        RTL_RESULTS.write_text(json.dumps(rtl, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
