"""Emit the camera-ready W8A16 descriptor sideband."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OUT = Path(__file__).resolve().parent
DEFAULT_DATA = OUT / "data"
SCHEMA = "tvla_w8a16.camera_ready.v3"


def descriptor(name: str, m: int, n: int, k: int, *, op: str = "gemm_w8a16",
               layout: str = "row_major", transpose: bool = False,
               status: str = "mapped", fallback_reason: str | None = None,
               bias_mode: str = "separate_bias_event") -> dict[str, Any]:
    is_fallback = status.startswith("fallback")
    return {
        "schema_version": SCHEMA,
        "id": name,
        "op": op,
        "m": m,
        "n": n,
        "k": k,
        "a_bits": 16 if not is_fallback else None,
        "w_bits": 8 if not is_fallback else None,
        "out_bits": 16 if not is_fallback else None,
        "acc_bits": 40 if not is_fallback else None,
        "a_scale_id": f"{name}.a_scale" if not is_fallback else None,
        "w_scale_id": f"{name}.w_scale" if not is_fallback else None,
        "out_scale_id": f"{name}.out_scale" if not is_fallback else None,
        "bias_mode": bias_mode,
        "layout": layout,
        "transpose": transpose,
        "tile_rows": 16 if not is_fallback else None,
        "tile_cols": 48 if not is_fallback else None,
        "status": status,
        "fallback_reason": fallback_reason,
        "traffic": {"activation_bytes": (m * k * 2) if not is_fallback else 0,
                     "weight_bytes": (k * n) if not is_fallback else 0,
                     "output_bytes": (m * n * 2) if not is_fallback else 0},
    }


def build() -> dict[str, Any]:
    records = [
        descriptor("vision_projection_0", 256, 1024, 768),
        descriptor("fusion_ffn_0", 21, 2048, 256),
        descriptor("fusion_attention_qk", 21, 21, 64, op="bmm_w8a16",
                   layout="head_major", status="mapped_candidate"),
        descriptor("fusion_attention_softmax", 21, 21, 1, op="softmax",
                   status="fallback_cost_record",
                   fallback_reason="dynamic normalization is outside the GEMM tile"),
        descriptor("action_decoder_ffn_0", 12, 2048, 256),
        descriptor("action_projection", 12, 7, 512),
        descriptor("layernorm_tile", 21, 256, 1, op="layer_norm",
                   status="mapped_candidate", bias_mode="explicit_gamma_beta"),
        descriptor("gelu_tile", 21, 2048, 1, op="gelu",
                   status="mapped_candidate", bias_mode="none"),
    ]
    return {
        "schema_version": f"{SCHEMA}.descriptors",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "engine": {"rows": 16, "physical_cols": 48, "logical_cols": 48,
                   "dsp": 768, "clock_ns": 3.298},
        "format": {"a_bits": 16, "w_bits": 8, "out_bits": 16, "acc_bits": 40},
        "records": records,
        "coverage": {"records": len(records),
                      "mapped": sum(r["status"] == "mapped" for r in records),
                      "candidate": sum(r["status"] == "mapped_candidate" for r in records),
                      "fallback": sum(r["status"] == "fallback_cost_record" for r in records)},
        "note": "Shape records are representative; live call coverage comes from the profiled operator inventory.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DATA)
    args = parser.parse_args()
    out_dir = args.output_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    result = build()
    payload = json.dumps(result, indent=2, ensure_ascii=False)
    (out_dir / "w8a16_descriptors.json").write_text(payload, encoding="utf-8")
    (OUT / "w8a16_descriptors.json").write_text(payload, encoding="utf-8")
    manifest = {"schema_version": f"{SCHEMA}.descriptor_manifest",
                "generated_at": result["generated_at"],
                "sha256": hashlib.sha256(payload.encode()).hexdigest(),
                "output_dir": str(out_dir), "records": len(result["records"])}
    (out_dir / "descriptor_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "records": len(result["records"]),
                      "output_dir": str(out_dir)}, indent=2))


if __name__ == "__main__":
    main()
