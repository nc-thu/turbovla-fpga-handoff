"""Build a TurboVLA operator/shape inventory from the frozen model metadata."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from w8a16_math import required_acc_bits

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "compiler" / "v2_2026-09-13_1113_w8a16_camera_ready_compiler"
OUT.mkdir(parents=True, exist_ok=True)


def load_shapes() -> list[dict[str, Any]]:
    obj = json.loads((DATA / "model_state_dict_shapes.json").read_text(encoding="utf-8"))
    if not isinstance(obj, list):
        raise TypeError("model_state_dict_shapes.json must be a list")
    return obj


def classify(name: str, shape: list[int]) -> str:
    n = name.lower()
    # Check the composite interaction/action namespaces before the broader
    # vision/text matches.  Otherwise `vision_language_interaction.text_*`
    # would incorrectly be counted as a vision encoder parameter.
    if "interaction" in n or "fusion" in n or "cross" in n:
        group = "vision_language_interaction"
    elif "action_head" in n or "decoder" in n:
        group = "action_head"
    elif "dinov" in n or "vision" in n:
        group = "vision_encoder"
    elif "bert" in n or "text" in n or "language" in n:
        group = "text_encoder"
    else:
        group = "other"
    if "embedding" in n or "position_embeddings" in n or "token_type" in n:
        kind = "embedding_lookup_table"
    elif len(shape) == 2 and ("weight" in n or "in_proj" in n or "out_proj" in n):
        kind = "gemm_w8a16"
    elif len(shape) == 4:
        kind = "conv_or_tensor_weight"
    else:
        kind = "non_gemm_parameter"
    return f"{group}:{kind}"


def build() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for i, item in enumerate(load_shapes()):
        name = str(item.get("name", f"parameter_{i}"))
        shape = [int(x) for x in item.get("shape", [])]
        if not shape:
            continue
        kind = classify(name, shape)
        lname = name.lower()
        is_matrix = (len(shape) == 2 and ("weight" in lname or "proj" in lname)
                     and "embedding" not in lname and "position_embeddings" not in lname
                     and "token_type" not in lname and "norm" not in lname)
        rec: dict[str, Any] = {
            "id": i,
            "name": name,
            "shape": shape,
            "dtype_source": item.get("dtype", "unknown"),
            "class": kind,
            "status": "mapped_candidate" if is_matrix else "must_recompute_or_fallback",
            "a_bits": 16 if is_matrix else None,
            "w_bits": 8 if is_matrix else None,
            "out_bits": 16 if is_matrix else None,
            "acc_bits": 40 if is_matrix else None,
        }
        if is_matrix:
            rec.update({"out_features": shape[0], "k": shape[1], "m_source": "runtime_tokens"})
        records.append(rec)
    matrices = [r for r in records if r["a_bits"] == 16]
    max_k = max((r["k"] for r in matrices), default=0)
    groups: dict[str, int] = {}
    for r in records:
        groups[r["class"]] = groups.get(r["class"], 0) + 1
    result = {
        "schema_version": "tvla_w8a16.inventory.v2",
        "generated_from": "data/model_state_dict_shapes.json",
        "parameter_count": len(records),
        "matrix_parameter_count": len(matrices),
        "max_parameter_k": max_k,
        "required_acc_bits_at_max_k": required_acc_bits(max_k) if max_k else None,
        "configured_acc_bits": 40,
        "class_counts": groups,
        "mapping_policy": {
            "linear_and_supported_bmm": "gemm_w8a16",
            "conv": "im2col_plus_gemm_with_explicit_traffic",
            "norm_gelu_softmax_sampling": "fallback_cost_record",
            "bias": "integer_if_fits_else_fallback",
        },
        "records": records,
    }
    (OUT / "operator_inventory.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (DATA / "operator_inventory.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    result = build()
    print(json.dumps({k: result[k] for k in ("parameter_count", "matrix_parameter_count", "max_parameter_k", "class_counts")}, indent=2))
