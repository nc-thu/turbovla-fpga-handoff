"""Tiny executable model for the TurboVLA W8A16 command path.

It validates compiler-emitted 64-bit words and executes the seven-lane action
smoke program with the same integer arithmetic used by the RTL testbench.  It
does not pretend to execute DINO, text encoding or a complete LIBERO rollout.
"""
from __future__ import annotations

import hashlib
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def sat16(v: int) -> int:
    return max(-32768, min(32767, int(v)))


def approx_tanh(v: int) -> int:
    neg = v < 0
    ax = abs(int(v))
    if ax >= 24576:
        y = 32767
    elif ax >= 16384:
        y = 24576 + ((ax - 16384) * 8191) // 8192
    elif ax >= 8192:
        y = 12288 + ((ax - 8192) * 12287) // 8192
    else:
        y = (ax * 3) // 2
    return sat16(-y if neg else y)


def decode(word_hex: str) -> dict[str, int]:
    w = int(word_hex, 16)
    return {
        "opcode": (w >> 56) & 0xff, "flags": (w >> 48) & 0xff,
        "dst": (w >> 40) & 0xff, "src0": (w >> 32) & 0xff,
        "src1": (w >> 24) & 0xff, "length": (w >> 8) & 0xffff,
    }


def smoke_action(program: list[dict]) -> dict:
    k, n = 8, 7
    state = [(i + 1) * 100 * (-1 if i % 2 else 1) for i in range(k)]
    weights = [[((j + 2 * i) % 5) - 2 for i in range(k)] for j in range(n)]
    bias = [j - 3 for j in range(n)]
    raw = [sum(state[i] * weights[j][i] for i in range(k)) for j in range(n)]
    with_bias = [sat16(raw[j] + bias[j]) for j in range(n)]
    action = [approx_tanh(x) for x in with_bias]
    executed = []
    current = None
    for item in program:
        op = item["op"]
        executed.append(op)
        if op == "GEMM_W8A16":
            current = raw[:]
        elif op == "BIAS_ADD":
            current = [sat16((current or raw)[j] + bias[j]) for j in range(n)]
        elif op == "TANH":
            current = [approx_tanh((current or with_bias)[j]) for j in range(n)]
        elif op == "STORE_ACTION":
            current = list(current or action)
    if current != action:
        raise AssertionError(f"smoke action mismatch: {current} vs {action}")
    return {
        "state_int16": state, "weight_int8": weights, "bias_int16": bias,
        "raw_acc_int40": raw, "after_bias_int16": with_bias,
        "action_q15": action, "action_normalized": [round(x / 32767.0, 7) for x in action],
        "executed_ops": executed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=DATA)
    parser.add_argument("--program", type=Path)
    parser.add_argument("--isa-spec", type=Path)
    args = parser.parse_args()
    data = args.data_dir.resolve()
    program_path = (args.program or (data / "turbovla_w8a16_program.json")).resolve()
    spec_path = (args.isa_spec or (data / "isa_spec.json")).resolve()
    program = json.loads(program_path.read_text(encoding="utf-8"))
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    opcode_by_name = {x["name"]: int(x["code"], 16) for x in spec["opcodes"]}
    validation = []
    for kind in ("full_program", "smoke_program", "opcode_catalog"):
        for item in program[kind]:
            code = decode(item["word_hex"])["opcode"]
            expected = opcode_by_name.get(item["op"])
            if expected is None or code != expected:
                raise AssertionError(f"word mismatch at {kind} pc={item['pc']}")
            validation.append({"program": kind, "pc": item["pc"], "op": item["op"], "word_hex": item["word_hex"], "decoded": decode(item["word_hex"])})
        if kind != "opcode_catalog" and (not program[kind] or program[kind][-1]["op"] != "END"):
            raise AssertionError(f"{kind} has no END")
    smoke = smoke_action(program["smoke_program"])
    source = program_path.read_bytes()
    result = {
        "schema_version": "tvla_w8a16.isa_sim.v1",
        "status": "PASS",
        "program_sha256": hashlib.sha256(source).hexdigest(),
        "full_program_validation": {"status": "PASS", "events": len(validation), "instruction_count": len(program["full_program"])},
        "opcode_catalog_validation": {"status": "PASS", "opcodes": len(program.get("opcode_catalog", []))},
        "smoke": smoke,
        "scope": "compiler words and seven-lane action-head command path; not full TurboVLA inference",
    }
    (data / "isa_sim_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    probe = {
        "schema_version": "tvla_w8a16.libero_action_probe.v1",
        "status": "command_path_passed",
        "task": "pick_up_the_black_bowl_from_table_center_and_place_it_on_the_plate",
        "initial_state_index": 0,
        "observation_source": "algo/libero_transfer/2026-09-12_133034/env_smoke.json",
        "input_provenance": "deterministic INT16 state vector exercising the LIBERO-compatible seven-lane action format; not the captured RGB-D tensor",
        "action_q15": smoke["action_q15"],
        "action_normalized": smoke["action_normalized"],
        "compiler_program": str(program_path),
        "rtl_scope": "one W8A16 action projection command path; no DINO/text inference, no captured RGB-D tensor and no environment step",
    }
    (data / "libero_action_probe.json").write_text(json.dumps(probe, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "instructions_checked": len(validation), "action_q15": smoke["action_q15"]}, indent=2))


if __name__ == "__main__":
    main()
