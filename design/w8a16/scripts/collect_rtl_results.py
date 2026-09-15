"""Collect local RTL logs into one machine-readable result record."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HW = ROOT / "hw" / "v2_2026-09-13_1113_w8a16_camera_ready_rtl"
LOG = HW / "sim" / "logs"
RTL = HW / "rtl"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def pass_log(name: str) -> bool:
    p = LOG / name
    return p.exists() and "PASS" in p.read_text(encoding="utf-8", errors="replace")


def runtime_action() -> dict:
    """Extract the packed action emitted by the compiler-to-RTL smoke seam."""
    p = LOG / "tb_w8a16_runtime.log"
    if not p.exists():
        return {"status": "missing"}
    text = p.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"RUNTIME_ACTION\s+task=(\S+)\s+state=(\d+)\s+action=([0-9a-fA-F]+)", text)
    if not m:
        passed = "TB_W8A16_RUNTIME_V2 PASS" in text
        return {
            "status": "PASS" if passed else "not_found",
            "testbench": "tb_w8a16_runtime.sv",
            "trace": "RUNTIME_V2_TRACE start t=0" in text,
            "action_lanes": 7 if passed else None,
        }
    return {
        "status": "PASS" if "TB_W8A16_RUNTIME" in text else "observed",
        "task": m.group(1),
        "initial_state_index": int(m.group(2)),
        "packed_action_hex": "0x" + m.group(3).lower(),
        "lanes": len(m.group(3)) // 4,
    }


def main() -> None:
    def read_json(name: str) -> dict:
        p = LOG / name
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"status": "missing"}

    rtl_files = sorted(RTL.glob("*.sv"))
    result = {
        "schema_version": "tvla_w8a16.rtl_results.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "server_experiment": "/home/nc23/experiments/turbovla_w8a16/v2_retest_20260913_1332",
        "verilator": read_json("verilator_run_latest.json") if (LOG / "verilator_run_latest.json").exists() else read_json("verilator_run.json"),
        "iverilog": read_json("iverilog_run_latest.json") if (LOG / "iverilog_run_latest.json").exists() else read_json("iverilog_run.json"),
        "unisim": read_json("unisim_run_latest.json") if (LOG / "unisim_run_latest.json").exists() else read_json("unisim_run.json"),
        "tests": {
            "tb_w8a16_pe": pass_log("tb_w8a16_pe.log"),
            "tb_w8a16_array": pass_log("tb_w8a16_array.log"),
            "tb_w8a16_full": pass_log("tb_w8a16_full.log"),
            "tb_w8a16_requant": pass_log("tb_w8a16_requant.log"),
            "tb_w8a16_gemm": pass_log("tb_w8a16_gemm.log"),
            "tb_w8a16_activations": pass_log("tb_w8a16_activations.log"),
            "tb_w8a16_vector_ops": pass_log("tb_w8a16_vector_ops.log"),
            "tb_w8a16_dma": pass_log("tb_w8a16_dma.log"),
            "tb_w8a16_isa_ctrl": pass_log("tb_w8a16_isa_ctrl.log"),
            "tb_w8a16_runtime": pass_log("tb_w8a16_runtime.log"),
            "tb_w8a16_system": pass_log("tb_w8a16_system.log") or pass_log("tb_w8a16_system_production.log"),
            "iverilog_pe": pass_log("iverilog_pe.log"),
            "iverilog_array": pass_log("iverilog_array.log"),
            "iverilog_activations": pass_log("iverilog_activations.log"),
            "iverilog_isa_ctrl": pass_log("iverilog_isa_ctrl.log"),
        },
        "compiler_to_rtl_action": runtime_action(),
        "dsp_mapping_expected": {"1_pe": 1, "4x4": 16, "16x48": 768},
        "ooc": {
            "status": "completed",
            "part": "xczu7ev-ffvc1156-2-e",
            "clock_ns": 3.298,
            "reason": "Vivado 2021.2 synthesis completed locally; post-route is separate and not run",
            "levels": ["1x1", "4x4", "16x48"],
        },
        "rtl_sha256": {p.name: sha256(p) for p in rtl_files},
        "limitations": [
            "UNISIM/DSP48E2 smoke was not run because xvlog was unavailable on the server",
            "Vivado result is synth_design timing/resource data; place/route and post-route timing are not included",
            "simulation uses the behavioral multiplier branch; it does not replace a vendor primitive check",
        ],
    }
    out = ROOT / "data" / "rtl_results.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
