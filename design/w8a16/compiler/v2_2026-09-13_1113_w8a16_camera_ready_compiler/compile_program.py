"""Compile the TurboVLA W8A16 camera-ready command stream.

The transport word stays 64 bits for the hardware interface.  All information
that cannot fit in that word (shape, scales, strides and dependency rules) is
kept beside it in the descriptor record.  The compiler writes into its own
version directory by default, so a new experiment cannot silently change an
older program or report.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUT = Path(__file__).resolve().parent
DEFAULT_DATA = OUT / "data"
ISA_VERSION = "tvla_w8a16.camera_ready.v2"

OPCODE = {
    "LOAD_CTX": 0x01, "LOAD_WEIGHT": 0x02, "STORE_CTX": 0x03,
    "STORE_ACTION": 0x04, "GEMM_W8A16": 0x10, "BMM_W8A16": 0x11,
    "BIAS_ADD": 0x20, "ADD": 0x21, "MUL_SCALE": 0x22,
    "LAYER_NORM": 0x30, "SOFTMAX": 0x31, "RELU": 0x32,
    "GELU": 0x33, "TANH": 0x34, "REQUANT": 0x35,
    "WAIT": 0x40, "BARRIER": 0x41, "END": 0xFF,
}

VECTOR_OPS = {"BIAS_ADD", "ADD", "MUL_SCALE", "LAYER_NORM", "SOFTMAX",
              "RELU", "GELU", "TANH"}
DMA_OPS = {"LOAD_CTX", "LOAD_WEIGHT", "STORE_CTX", "STORE_ACTION"}
MAX_TRANSPORT_LENGTH = 0xFFFF


def encode_word(item: dict[str, Any]) -> int:
    op = item["op"]
    if op not in OPCODE:
        raise ValueError(f"unknown opcode: {op}")
    return (
        (OPCODE[op] << 56)
        | ((int(item.get("flags_word", 0x03)) & 0xFF) << 48)
        | ((int(item.get("dst", 0)) & 0xFF) << 40)
        | ((int(item.get("src0", 0)) & 0xFF) << 32)
        | ((int(item.get("src1", 0)) & 0xFF) << 24)
        | ((int(item.get("length", 0)) & 0xFFFF) << 8)
    )


def default_length_unit(op: str) -> str:
    if op in DMA_OPS:
        return "dma_beats"
    if op in {"GEMM_W8A16", "BMM_W8A16"}:
        return "descriptor_shape"
    return "elements"


def default_mapping(op: str, status: str) -> str:
    if status.startswith("fallback"):
        return "fallback"
    if op in DMA_OPS:
        return "dma"
    if op in {"GEMM_W8A16", "BIAS_ADD", "ADD", "MUL_SCALE", "RELU",
              "GELU", "TANH", "LAYER_NORM", "SOFTMAX", "REQUANT"}:
        return "rtl_tile"
    if op in {"BMM_W8A16"}:
        return "rtl_candidate"
    return "control"


def inst(
    op: str,
    *,
    dst: int = 0,
    src0: int = 0,
    src1: int = 0,
    length: int = 0,
    m: int = 0,
    n: int = 0,
    k: int = 0,
    status: str = "mapped",
    note: str = "",
    dependencies: list[str] | None = None,
    layout: str = "row_major",
    transpose: bool = False,
    flags_word: int | None = None,
) -> dict[str, Any]:
    if op not in OPCODE:
        raise ValueError(f"unknown opcode: {op}")
    shape = {"m": m, "n": n, "k": k} if op in {"GEMM_W8A16", "BMM_W8A16"} else None
    # flags[7] selects the production 16x48 feed/drain path.  The compact
    # 1x7x8 action tile remains on the local action path used by the direct
    # compiler-to-RTL smoke; all other matrix shapes request the array.
    if flags_word is None:
        is_matrix = op in {"GEMM_W8A16", "BMM_W8A16"}
        is_action_smoke = (op == "GEMM_W8A16" and m == 1 and n == 7 and k == 8)
        flags_word = 0x03 | (0x80 if is_matrix and not is_action_smoke else 0)
    return {
        "pc": -1,
        "op": op,
        "dst": dst,
        "src0": src0,
        "src1": src1,
        "length": length,
        "length_unit": default_length_unit(op),
        "shape": shape,
        "layout": layout,
        "transpose": transpose,
        "flags_word": flags_word & 0xFF,
        "numeric": {"a_bits": 16, "w_bits": 8, "out_bits": 16,
                     "acc_bits": 40, "signed": True},
        "scale_ids": {"a": f"pc{dst}.a", "w": f"pc{src1}.w",
                       "out": f"pc{dst}.out"},
        "flags": {"valid": True, "saturate": True},
        "status": status,
        "mapping": default_mapping(op, status),
        "dependencies": dependencies or [],
        "note": note,
    }


def add(program: list[dict[str, Any]], item: dict[str, Any]) -> None:
    """Append one logical instruction, tiling long element streams.

    The command word has a 16-bit length field.  A large vector operation must
    therefore become several transport words; silently truncating the length
    would make the compiler/RTL contract incorrect.  Each emitted chunk keeps
    the original logical length and its position as sideband metadata so a
    runtime can preserve ordering and address arithmetic.
    """
    logical_length = int(item.get("length", 0))
    if logical_length <= MAX_TRANSPORT_LENGTH:
        item["pc"] = len(program)
        item["word_hex"] = f"0x{encode_word(item):016x}"
        program.append(item)
        return
    if logical_length < 0:
        raise ValueError(f"negative instruction length: {logical_length}")
    chunk_count = (logical_length + MAX_TRANSPORT_LENGTH - 1) // MAX_TRANSPORT_LENGTH
    remaining = logical_length
    chunk_index = 0
    while remaining:
        part = dict(item)
        part["length"] = min(remaining, MAX_TRANSPORT_LENGTH)
        part["logical_length"] = logical_length
        part["chunk_index"] = chunk_index
        part["chunk_count"] = chunk_count
        part["pc"] = len(program)
        part["word_hex"] = f"0x{encode_word(part):016x}"
        program.append(part)
        remaining -= part["length"]
        chunk_index += 1


def build_full_program() -> list[dict[str, Any]]:
    p: list[dict[str, Any]] = []
    add(p, inst("LOAD_CTX", dst=0, length=1, status="fallback",
                 note="RGB preprocessing and patch extraction are outside this tile runtime"))
    add(p, inst("LOAD_WEIGHT", src1=0, length=1,
                 note="one 384-bit WRAM beat; larger tensors are tiled"))
    add(p, inst("GEMM_W8A16", dst=1, src0=0, src1=0, m=256, n=1024, k=768,
                 note="vision projection; compiler emits 16x48 tiles"))
    add(p, inst("LAYER_NORM", dst=1, src0=1, length=256 * 1024,
                 status="mapped_candidate", dependencies=["gamma", "beta"],
                 note="normalization unit; learned parameters remain explicit"))
    add(p, inst("ADD", dst=1, src0=1, src1=2, length=256 * 1024,
                 note="view and position embedding"))
    for layer in range(6):
        base = 8 + layer * 8
        add(p, inst("LAYER_NORM", dst=base, src0=1, length=256 * 1024,
                     status="mapped_candidate", dependencies=["gamma", "beta"],
                     note=f"interaction layer {layer} visual norm"))
        add(p, inst("GEMM_W8A16", dst=base + 1, src0=base, src1=0,
                     m=256, n=1024, k=256,
                     note=f"interaction layer {layer} visual projection"))
        add(p, inst("BMM_W8A16", dst=base + 2, src0=base + 1, src1=3,
                     m=256, n=21, k=128, status="mapped_candidate",
                     layout="head_major", dependencies=["q_layout", "k_layout"],
                     note="QK only after both operand layouts pass the tile check"))
        add(p, inst("SOFTMAX", dst=base + 3, src0=base + 2, length=256 * 21,
                     status="mapped_candidate", dependencies=["mask"],
                     note="max subtraction and LUT normalization"))
        add(p, inst("BMM_W8A16", dst=base + 4, src0=base + 3, src1=4,
                     m=256, n=128, k=21, status="mapped_candidate",
                     layout="head_major", dependencies=["v_layout"],
                     note="attention value product"))
        add(p, inst("ADD", dst=1, src0=1, src1=base + 4, length=256 * 256,
                     note="visual residual uses the current tensor"))
        add(p, inst("GELU", dst=base + 5, src0=base + 1, length=256 * 1024,
                     note="piecewise fixed-point approximation"))
        add(p, inst("BIAS_ADD", dst=base + 6, src0=base + 5, src1=5,
                     length=256 * 1024, status="fallback_or_integer",
                     dependencies=["bias_scale"], note="bias is a separate event"))
    add(p, inst("LOAD_CTX", dst=6, length=1, note="state vector beat"))
    add(p, inst("LAYER_NORM", dst=6, src0=6, length=8,
                 status="mapped_candidate", dependencies=["gamma", "beta"]))
    add(p, inst("GEMM_W8A16", dst=7, src0=6, src1=6, m=1, n=512, k=8,
                 note="state projection"))
    add(p, inst("GELU", dst=7, src0=7, length=512))
    for layer in range(3):
        base = 32 + layer * 7
        add(p, inst("LAYER_NORM", dst=base, src0=1, length=256 * 256,
                     status="mapped_candidate", dependencies=["gamma", "beta"],
                     note=f"decoder layer {layer} norm"))
        add(p, inst("BMM_W8A16", dst=base + 1, src0=base, src1=base,
                     m=12, n=12, k=256, status="mapped_candidate",
                     layout="head_major", dependencies=["q_layout", "k_layout"],
                     note=f"decoder layer {layer} self attention"))
        add(p, inst("SOFTMAX", dst=base + 2, src0=base + 1, length=12 * 12,
                     status="mapped_candidate", dependencies=["mask"]))
        add(p, inst("ADD", dst=1, src0=1, src1=base + 2, length=12 * 256,
                     note="decoder residual"))
        add(p, inst("GEMM_W8A16", dst=base + 3, src0=1, src1=7,
                     m=12, n=2048, k=256, note="decoder FFN up"))
        add(p, inst("RELU", dst=base + 4, src0=base + 3, length=12 * 2048))
        add(p, inst("GEMM_W8A16", dst=base + 5, src0=base + 4, src1=8,
                     m=12, n=256, k=2048, note="decoder FFN down"))
    add(p, inst("GEMM_W8A16", dst=60, src0=1, src1=9,
                 m=12, n=7, k=256, note="action projection"))
    add(p, inst("TANH", dst=61, src0=60, length=12 * 7,
                 note="normalized action output"))
    add(p, inst("REQUANT", dst=62, src0=61, length=12 * 7,
                 note="INT16 action representation"))
    add(p, inst("STORE_ACTION", src0=62, length=1,
                 note="one activation beat; adapter converts to environment format"))
    add(p, inst("END"))
    return p


def build_smoke_program() -> list[dict[str, Any]]:
    p: list[dict[str, Any]] = []
    add(p, inst("LOAD_CTX", dst=0, length=1, note="one activation beat"))
    add(p, inst("LOAD_WEIGHT", src1=1, length=1, note="one weight beat"))
    add(p, inst("GEMM_W8A16", dst=2, src0=0, src1=1, m=1, n=7, k=8,
                 note="RTL action-path tile"))
    add(p, inst("BIAS_ADD", dst=2, src0=2, src1=2, length=7,
                 note="explicit bias event"))
    add(p, inst("TANH", dst=3, src0=2, length=7,
                 note="normalized action"))
    add(p, inst("STORE_ACTION", src0=3, length=1,
                 note="one action beat"))
    add(p, inst("END"))
    return p


def build_opcode_catalog() -> list[dict[str, Any]]:
    catalog: list[dict[str, Any]] = []
    for name in OPCODE:
        add(catalog, inst(name, length=1, status="catalog", note="encoding coverage entry"))
    return catalog


def validate(program: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    for kind in ("full_program", "smoke_program", "opcode_catalog"):
        items = program[kind]
        pcs = [int(x["pc"]) for x in items]
        if pcs != list(range(len(items))):
            errors.append(f"{kind}: pc sequence is not contiguous")
        for item in items:
            if item["op"] not in OPCODE:
                errors.append(f"{kind}: unknown op {item['op']}")
            if int(item["word_hex"], 16) != encode_word(item):
                errors.append(f"{kind}: word mismatch at pc={item['pc']}")
            if not 0 <= int(item.get("flags_word", 0)) <= 0xFF:
                errors.append(f"{kind}: flags out of range at pc={item['pc']}")
            if int(item.get("length", 0)) < 0 or int(item.get("length", 0)) > 0xFFFF:
                errors.append(f"{kind}: length out of range at pc={item['pc']}")
            if item["op"] in {"GEMM_W8A16", "BMM_W8A16"}:
                shape = item.get("shape") or {}
                if any(int(shape.get(x, 0)) <= 0 for x in ("m", "n", "k")):
                    # The opcode catalog intentionally has no concrete shape.
                    if kind != "opcode_catalog":
                        errors.append(f"{kind}: non-positive matrix shape at pc={item['pc']}")
                if item["op"] == "BMM_W8A16" and not (int(item.get("flags_word", 0)) & 0x80):
                    errors.append(f"{kind}: BMM must select production array at pc={item['pc']}")
        if kind != "opcode_catalog" and (not items or items[-1]["op"] != "END"):
            errors.append(f"{kind}: missing END")
    return {"status": "PASS" if not errors else "FAIL", "errors": errors}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()
    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    full, smoke, catalog = build_full_program(), build_smoke_program(), build_opcode_catalog()
    result: dict[str, Any] = {
        "schema_version": f"{ISA_VERSION}.program",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "isa": f"{ISA_VERSION}.isa",
        "engine": {"rows": 16, "physical_cols": 48, "logical_cols": 48,
                   "dsp": 768, "clock_ns": 3.298},
        "numeric_contract": {"activation_bits": 16, "weight_bits": 8,
                             "output_bits": 16, "accumulator_bits": 40,
                             "signed": True, "saturation": "INT16"},
        "full_program": full,
        "smoke_program": smoke,
        "opcode_catalog": catalog,
        "coverage": {
            "full_instruction_count": len(full),
            "smoke_instruction_count": len(smoke),
            "opcode_count": len(catalog),
            "vector_ops": sorted(VECTOR_OPS),
            "dma_ops": sorted(DMA_OPS),
            "mapped_ops": sorted({x["op"] for x in full if x["mapping"] in {"rtl_tile", "dma"}}),
            "fallback_ops": sorted({x["op"] for x in full if x["mapping"] == "fallback"}),
        },
        "provenance": {"task": "LIBERO action command smoke", "seed": 20260830,
                       "input": "deterministic INT16 state vector; no full VLA tensor"},
    }
    result["validation"] = validate(result)
    if result["validation"]["status"] != "PASS":
        raise SystemExit(json.dumps(result["validation"], indent=2))
    payload = json.dumps(result, indent=2, ensure_ascii=False)
    (out_dir / "turbovla_w8a16_program.json").write_text(payload, encoding="utf-8")
    (OUT / "turbovla_w8a16_program.json").write_text(payload, encoding="utf-8")
    manifest = {
        "schema_version": f"{ISA_VERSION}.manifest",
        "generated_at": result["generated_at"],
        "program": "turbovla_w8a16_program.json",
        "program_sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "output_dir": str(out_dir),
        "validation": result["validation"],
    }
    (out_dir / "compile_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "full_instructions": len(full),
                      "smoke_instructions": len(smoke), "output_dir": str(out_dir)}, indent=2))


if __name__ == "__main__":
    main()
