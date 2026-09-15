"""Build local DINOv3 and BERT assets from the released TurboVLA checkpoint.

The TurboVLA release contains both encoder state dictionaries.  DINOv3's
official HF repository is gated on the server, so this script instantiates the
public Transformers architecture and loads the matching state from the policy
checkpoint.  The experiment therefore does not substitute DINOv2 weights.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import torch
from transformers import BertConfig, BertModel, DINOv3ViTConfig, DINOv3ViTModel


def save_dino(checkpoint: dict, output: Path) -> dict:
    state = {
        k[len("vision_encoder.backbone.") :]: v
        for k, v in checkpoint["model_state_dict"].items()
        if k.startswith("vision_encoder.backbone.")
    }
    cfg = DINOv3ViTConfig(
        hidden_size=768,
        image_size=256,
        intermediate_size=3072,
        num_attention_heads=12,
        num_hidden_layers=12,
        num_register_tokens=4,
        patch_size=16,
        query_bias=True,
        key_bias=False,
        value_bias=True,
        proj_bias=True,
        mlp_bias=True,
        layerscale_value=1.0,
        rope_theta=100.0,
        layer_norm_eps=1e-5,
    )
    model = DINOv3ViTModel(cfg)
    missing, unexpected = model.load_state_dict(state, strict=False)
    if missing or unexpected:
        raise RuntimeError(f"DINOv3 state mismatch: missing={missing}, unexpected={unexpected}")
    output.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output, safe_serialization=True)
    return {"tensors": len(state), "parameters": sum(v.numel() for v in state.values())}


def save_bert(checkpoint: dict, output: Path) -> dict:
    state = {
        k[len("text_encoder.bert.") :]: v
        for k, v in checkpoint["model_state_dict"].items()
        if k.startswith("text_encoder.bert.")
    }
    cfg = BertConfig(
        vocab_size=30522,
        hidden_size=768,
        num_hidden_layers=12,
        num_attention_heads=12,
        intermediate_size=3072,
        hidden_act="gelu",
        hidden_dropout_prob=0.1,
        attention_probs_dropout_prob=0.1,
        max_position_embeddings=512,
        type_vocab_size=2,
        initializer_range=0.02,
        layer_norm_eps=1e-12,
        pad_token_id=0,
    )
    model = BertModel(cfg)
    missing, unexpected = model.load_state_dict(state, strict=False)
    if missing or unexpected:
        raise RuntimeError(f"BERT state mismatch: missing={missing}, unexpected={unexpected}")
    output.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output, safe_serialization=True)
    return {"tensors": len(state), "parameters": sum(v.numel() for v in state.values())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--dino-out", required=True)
    parser.add_argument("--bert-out", required=True)
    parser.add_argument("--manifest", required=True)
    args = parser.parse_args()
    checkpoint = torch.load(args.checkpoint, map_location="cpu", weights_only=True)
    dino = save_dino(checkpoint, Path(args.dino_out))
    bert = save_bert(checkpoint, Path(args.bert_out))
    manifest = {
        "checkpoint": os.path.abspath(args.checkpoint),
        "dino": dino,
        "bert": bert,
        "transformers": __import__("transformers").__version__,
    }
    Path(args.manifest).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == "__main__":
    main()
