"""Attach transparent cost events to the compiler's TurboVLA ISA program.

The values are capacity-model cycles, not a claim of a finished full-model
RTL implementation.  Every instruction still appears in the event list, so
fallback operators cannot silently disappear from the system estimate.
"""
from __future__ import annotations

import csv
import json
import math
import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_cycles import tile_cycles


VECTOR_OPS = {"BIAS_ADD", "ADD", "MUL_SCALE", "RELU", "GELU", "TANH", "REQUANT"}


def event(item: dict) -> dict:
    op = str(item["op"])
    length = int(item.get("length", 0) or 0)
    cycles = 1
    traffic_in = 0
    traffic_out = 0
    status = item.get("status", "mapped")
    note = "control event"
    if op == "LOAD_CTX":
        # `length` is a beat count for DMA commands.  One CTX beat carries
        # sixteen INT16 values (32 bytes); it is not an element count.
        cycles = max(1, length)
        traffic_out = length * 32
        note = "256-bit CTX activation read (one beat = 32 bytes)"
    elif op == "LOAD_WEIGHT":
        cycles = max(1, length)
        traffic_out = length * 48
        note = "384-bit WRAM weight read (one beat = 48 bytes)"
    elif op in {"STORE_CTX", "STORE_ACTION"}:
        cycles = max(1, length)
        traffic_in = length * 32
        note = "256-bit INT16 write beat; action adapter is downstream"
    elif op in {"GEMM_W8A16", "BMM_W8A16"}:
        m, n, k = int(item.get("m", 1) or 1), int(item.get("n", 1) or 1), int(item.get("k", 1) or 1)
        c = tile_cycles(m, n, k)
        cycles = int(c["total_cycles"])
        traffic_in = int(c["stream_a_bytes"] + c["stream_w_bytes"])
        traffic_out = int(c["out_bytes"])
        note = "16×48 array capacity model" if op == "GEMM_W8A16" else "BMM only when layouts/dependencies are compatible"
    elif op in VECTOR_OPS:
        lanes = max(1, math.ceil(length / 16))
        if op == "MUL_SCALE":
            cycles = lanes
        elif op in {"GELU", "TANH", "RELU", "REQUANT", "BIAS_ADD", "ADD"}:
            cycles = lanes
        note = "vector primitive; exact latency requires unit implementation"
    elif op == "LAYER_NORM":
        cycles = max(1, 3 * math.ceil(max(length, 1) / 16))
        note = "mean/deviation/scale; current bounded integer RTL primitive"
    elif op == "SOFTMAX":
        cycles = max(1, 4 * math.ceil(max(length, 1) / 16))
        note = "max, LUT exp, sum and normalize"
    elif op in {"WAIT", "BARRIER", "END"}:
        cycles = 1
    return {
        "pc": int(item.get("pc", -1)), "op": op, "status": status,
        "cycles_lower_bound": cycles, "input_bytes": traffic_in,
        "output_bytes": traffic_out, "m": item.get("m", 0),
        "n": item.get("n", 0), "k": item.get("k", 0), "note": note,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=DATA)
    args = parser.parse_args()
    data = args.data_dir.resolve()
    program = json.loads((data / "turbovla_w8a16_program.json").read_text(encoding="utf-8"))
    result = {
        "schema_version": "tvla_w8a16.instruction_costs.v1",
        "assumptions": {
            "ctx_bytes_per_cycle": 32, "wram_bytes_per_cycle": 48,
            "output_bytes_per_cycle": 32, "array": "16x48, one A16xW8 product per DSP",
            "unknown_or_fallback": "kept as an explicit event; not set to zero",
        },
        "smoke": [event(x) for x in program.get("smoke_program", [])],
        "full": [event(x) for x in program.get("full_program", [])],
    }
    (data / "instruction_costs.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    rows = [{"program": p, **e} for p in ("smoke", "full") for e in result[p]]
    with (data / "instruction_costs.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    print(json.dumps({"status": "PASS", "smoke_events": len(result["smoke"]), "full_events": len(result["full"]), "full_cycles": sum(x["cycles_lower_bound"] for x in result["full"])}, indent=2))


if __name__ == "__main__":
    main()
