"""Emit a small, explicit descriptor stream for the TurboVLA W8A16 engine."""
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = Path(__file__).resolve().parent


def descriptor(name: str, m: int, n: int, k: int, *, layout: str = "row_major",
               transpose: bool = False, fallback: bool = False) -> dict[str, Any]:
    return {
        "schema_version": "tvla_w8a16.v1",
        "id": name,
        "op": "fallback" if fallback else "gemm_w8a16",
        "m": m,
        "n": n,
        "k": k,
        "a_bits": None if fallback else 16,
        "w_bits": None if fallback else 8,
        "out_bits": None if fallback else 16,
        "acc_bits": None if fallback else 40,
        "a_scale_id": None if fallback else f"{name}.a_scale",
        "w_scale_id": None if fallback else f"{name}.w_scale",
        "out_scale_id": None if fallback else f"{name}.out_scale",
        "bias_mode": "fallback_or_integer" if fallback else "separate_bias_event",
        "layout": layout,
        "transpose": transpose,
        "tile_rows": 16 if not fallback else None,
        "tile_cols": 48 if not fallback else None,
        "status": "fallback_cost_record" if fallback else "mapped_candidate",
    }


def build() -> dict[str, Any]:
    # These are intentionally representative TurboVLA shapes.  The inventory
    # is the full parameter list; runtime hooks can append exact token M/N
    # records without changing the descriptor schema.
    descriptors = [
        descriptor("vision_projection_0", 256, 1024, 768),
        descriptor("fusion_ffn_0", 21, 2048, 256),
        descriptor("fusion_attention_qk", 21, 21, 64, layout="head_major"),
        descriptor("fusion_attention_softmax", 21, 21, 1, fallback=True),
        descriptor("action_decoder_ffn_0", 12, 2048, 256),
        descriptor("action_projection", 12, 7, 512),
        descriptor("layernorm_fallback", 21, 256, 1, fallback=True),
        descriptor("gelu_fallback", 21, 2048, 1, fallback=True),
    ]
    result = {
        "schema_version": "tvla_w8a16.v1",
        "engine": {"rows": 16, "physical_cols": 48, "logical_cols": 48, "dsp": 768},
        "format": {"a_bits": 16, "w_bits": 8, "out_bits": 16, "acc_bits": 40},
        "records": descriptors,
        "coverage_note": "Representative descriptor stream; runtime inventory remains the source of full call coverage.",
    }
    (DATA / "w8a16_descriptors.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (OUT / "w8a16_descriptors.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    result = build()
    print(json.dumps({"records": len(result["records"]), "schema": result["schema_version"]}, indent=2))
