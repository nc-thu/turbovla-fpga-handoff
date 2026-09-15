"""Emit a complete TurboVLA operator program and a small executable action trace.

The full program is an ISA-level schedule.  It intentionally leaves DINO/BERT
convolution and large attention blocks explicit instead of pretending that a
single GEMM descriptor covers them.  The smoke trace is small enough for the
RTL command-path test and uses a real LIBERO observation/state provenance file.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).resolve().parent

# The transport word is intentionally small and stable.  Matrix dimensions,
# scale IDs and memory strides stay in the descriptor sideband; the RTL
# sequencer only needs the operation and the stream addresses to preserve
# ordering.
OPCODE = {
    "LOAD_CTX": 0x01, "LOAD_WEIGHT": 0x02, "STORE_CTX": 0x03,
    "STORE_ACTION": 0x04, "GEMM_W8A16": 0x10, "BMM_W8A16": 0x11,
    "BIAS_ADD": 0x20, "ADD": 0x21, "MUL_SCALE": 0x22,
    "LAYER_NORM": 0x30, "SOFTMAX": 0x31, "RELU": 0x32,
    "GELU": 0x33, "TANH": 0x34, "REQUANT": 0x35,
    "WAIT": 0x40, "BARRIER": 0x41, "END": 0xff,
}


def encode_word(item: dict[str, Any]) -> int:
    """Encode the 64-bit transport word consumed by w8a16_isa_ctrl."""
    op = item["op"]
    if op not in OPCODE:
        raise ValueError(f"unknown opcode: {op}")
    fields = (OPCODE[op] << 56) | (int(item.get("flags_word", 0x03)) << 48)
    fields |= (int(item.get("dst", 0)) & 0xff) << 40
    fields |= (int(item.get("src0", 0)) & 0xff) << 32
    fields |= (int(item.get("src1", 0)) & 0xff) << 24
    fields |= (int(item.get("length", 0)) & 0xffff) << 8
    return fields


def inst(op: str, *, dst: int = 0, src0: int = 0, src1: int = 0,
         length: int = 0, m: int = 0, n: int = 0, k: int = 0,
         status: str = "mapped", note: str = "") -> dict[str, Any]:
    return {
        "pc": -1, "op": op, "dst": dst, "src0": src0, "src1": src1,
        "length": length, "m": m, "n": n, "k": k,
        "flags": {"valid": True, "saturate": True},
        "status": status, "note": note,
    }


def add(program: list[dict[str, Any]], item: dict[str, Any]) -> None:
    item["pc"] = len(program)
    item["word_hex"] = f"0x{encode_word(item):016x}"
    program.append(item)


def build_full_program() -> list[dict[str, Any]]:
    p: list[dict[str, Any]] = []
    add(p, inst("LOAD_CTX", dst=0, length=2 * 256 * 256 * 3, status="fallback", note="RGB preprocessing and patch extraction remain outside the INT16 array"))
    add(p, inst("LOAD_WEIGHT", src1=0, length=768 * 1024, status="mapped", note="vision projection weights"))
    add(p, inst("GEMM_W8A16", dst=1, src0=0, src1=0, m=256, n=1024, k=768, status="mapped", note="representative vision projection"))
    add(p, inst("LAYER_NORM", dst=1, src0=1, length=256 * 1024, status="mapped_candidate", note="normalization unit; scale/bias are separate"))
    add(p, inst("ADD", dst=1, src0=1, src1=2, length=256 * 1024, note="view and position embedding"))
    # Six interaction layers: bidirectional attention followed by text FFN.
    for layer in range(6):
        base = 8 + layer * 8
        add(p, inst("LAYER_NORM", dst=base, src0=1, length=256 * 1024, note=f"interaction layer {layer} visual norm"))
        add(p, inst("GEMM_W8A16", dst=base + 1, src0=base, src1=0, m=256, n=1024, k=256, note=f"interaction layer {layer} visual projection"))
        add(p, inst("BMM_W8A16", dst=base + 2, src0=base + 1, src1=3, m=256, n=21, k=128, status="mapped_candidate", note="QK only when both layouts are compatible"))
        add(p, inst("SOFTMAX", dst=base + 3, src0=base + 2, length=256 * 21, note="attention normalization"))
        add(p, inst("BMM_W8A16", dst=base + 4, src0=base + 3, src1=4, m=256, n=128, k=21, status="mapped_candidate", note="attention value product"))
        add(p, inst("ADD", dst=1, src0=1, src1=base + 4, length=256 * 256, note="visual residual"))
        add(p, inst("GELU", dst=base + 5, src0=base + 1, length=256 * 1024, note="fixed-point approximation"))
        add(p, inst("BIAS_ADD", dst=base + 6, src0=base + 5, src1=5, length=256 * 1024, status="fallback_or_integer", note="bias path is explicit"))
    add(p, inst("LOAD_CTX", dst=6, length=8, note="state vector"))
    add(p, inst("LAYER_NORM", dst=6, src0=6, length=8, note="state projection normalization"))
    add(p, inst("GEMM_W8A16", dst=7, src0=6, src1=6, m=1, n=512, k=8, note="state projection"))
    add(p, inst("GELU", dst=7, src0=7, length=512, note="state projection activation"))
    # Action decoder and projection.  Self/cross attention is explicit.
    for layer in range(3):
        base = 32 + layer * 7
        add(p, inst("LAYER_NORM", dst=base, src0=1, length=256 * 256, note=f"decoder layer {layer} norm"))
        add(p, inst("BMM_W8A16", dst=base + 1, src0=base, src1=base, m=12, n=12, k=256, status="mapped_candidate", note=f"decoder layer {layer} self attention"))
        add(p, inst("SOFTMAX", dst=base + 2, src0=base + 1, length=12 * 12, note="decoder attention"))
        add(p, inst("ADD", dst=1, src0=1, src1=base + 2, length=12 * 256, note="decoder residual"))
        add(p, inst("GEMM_W8A16", dst=base + 3, src0=1, src1=7, m=12, n=2048, k=256, note="decoder FFN up"))
        add(p, inst("RELU", dst=base + 4, src0=base + 3, length=12 * 2048, note="decoder FFN activation"))
        add(p, inst("GEMM_W8A16", dst=base + 5, src0=base + 4, src1=8, m=12, n=256, k=2048, note="decoder FFN down"))
    add(p, inst("GEMM_W8A16", dst=60, src0=1, src1=9, m=12, n=7, k=256, note="action projection"))
    add(p, inst("TANH", dst=61, src0=60, length=12 * 7, note="normalized action output"))
    add(p, inst("REQUANT", dst=62, src0=61, length=12 * 7, note="INT16 action representation"))
    add(p, inst("STORE_ACTION", src0=62, length=12 * 7, note="action adapter converts normalized values to LIBERO format"))
    add(p, inst("END"))
    return p


def build_smoke_program() -> list[dict[str, Any]]:
    p: list[dict[str, Any]] = []
    add(p, inst("LOAD_CTX", dst=0, length=8, note="one LIBERO state-derived INT16 feature vector"))
    add(p, inst("LOAD_WEIGHT", dst=1, length=8 * 7, note="small action projection weight tile"))
    add(p, inst("GEMM_W8A16", dst=2, src0=0, src1=1, m=1, n=7, k=8, note="RTL action-path smoke"))
    add(p, inst("BIAS_ADD", dst=2, src0=2, src1=2, length=7, note="explicit bias event"))
    add(p, inst("TANH", dst=3, src0=2, length=7, note="normalized action"))
    add(p, inst("STORE_ACTION", src0=3, length=7, note="one action, not a complete model rollout"))
    add(p, inst("END"))
    return p


def build_opcode_catalog() -> list[dict[str, Any]]:
    """Emit one encodable word for every ISA opcode without changing the model schedule."""
    catalog: list[dict[str, Any]] = []
    for name in OPCODE:
        item = inst(name, length=1, status="catalog", note="encoding coverage entry")
        add(catalog, item)
    return catalog


def main() -> None:
    full = build_full_program()
    smoke = build_smoke_program()
    catalog = build_opcode_catalog()
    result = {
        "schema_version": "tvla_w8a16.program.v1",
        "isa": "data/isa_spec.json",
        "engine": {"rows": 16, "physical_cols": 48, "dsp": 768, "clock_ns": 3.298},
        "full_program": full,
        "smoke_program": smoke,
        "opcode_catalog": catalog,
        "coverage": {
            "full_instruction_count": len(full),
            "smoke_instruction_count": len(smoke),
            "activation_ops": sorted({x["op"] for x in full if x["op"] in {"RELU", "GELU", "TANH", "LAYER_NORM", "SOFTMAX"}}),
            "dma_ops": sorted({x["op"] for x in full if x["op"] in {"LOAD_CTX", "LOAD_WEIGHT", "STORE_CTX", "STORE_ACTION"}}),
            "fallback_ops_present": sorted({x["op"] for x in full if x["status"] not in {"mapped", "mapped_candidate"}}),
        },
        "smoke_provenance": {
            "observation_source": "algo/libero_transfer/2026-09-12_133034/env_smoke.json",
            "task": "pick_up_the_black_bowl_from_table_center_and_place_it_on_the_plate",
            "initial_state_index": 0,
            "action_semantics": "7-D normalized action; this is a command-path smoke, not full TurboVLA inference",
        },
    }
    (DATA / "turbovla_w8a16_program.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (OUT / "turbovla_w8a16_program.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"full_instructions": len(full), "smoke_instructions": len(smoke), "schema": result["schema_version"]}, indent=2))


if __name__ == "__main__":
    main()
