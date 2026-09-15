"""Load and one-call smoke test for the released TurboVLA LIBERO checkpoint.

This wrapper only adapts the released checkpoint field name.  The upstream
evaluator currently requires EMA weights, while the unified release exposes
the same model under ``model_state_dict``.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--dino", required=True)
    ap.add_argument("--bert", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--precision", choices=["fp32", "bf16"], default="fp32")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    sys.path.insert(0, args.source)

    import turbovla.evaluation.policy as policy_module

    def checkpoint_state_dict(checkpoint):
        if isinstance(checkpoint, dict):
            if isinstance(checkpoint.get("ema_model_state_dict"), dict):
                return checkpoint["ema_model_state_dict"]
            if isinstance(checkpoint.get("model_state_dict"), dict):
                return checkpoint["model_state_dict"]
        raise KeyError("checkpoint has neither ema_model_state_dict nor model_state_dict")

    policy_module._checkpoint_state_dict = checkpoint_state_dict
    t0 = time.perf_counter()
    result = {
        "source": os.path.abspath(args.source),
        "checkpoint": os.path.abspath(args.checkpoint),
        "dino": os.path.abspath(args.dino),
        "bert": os.path.abspath(args.bert),
        "device": args.device,
        "precision": args.precision,
        "status": "started",
    }
    try:
        policy = policy_module.TurboVLAPolicy(
            ckpt_path=args.checkpoint,
            dinov3_path=args.dino,
            bert_path=args.bert,
            device=args.device,
            precision=args.precision,
            allow_hf_download=False,
            verbose=True,
        )
        result["load_seconds"] = time.perf_counter() - t0
        result["parameters"] = int(sum(p.numel() for p in policy.model.parameters()))
        result["parameters_millions"] = result["parameters"] / 1e6
        result["parameter_dtypes"] = sorted({str(p.dtype) for p in policy.model.parameters()})
        if torch.cuda.is_available() and str(policy.device).startswith("cuda"):
            torch.cuda.reset_peak_memory_stats(policy.device)
        primary = np.zeros((256, 256, 3), dtype=np.uint8)
        wrist = np.full((256, 256, 3), 127, dtype=np.uint8)
        state = np.zeros((8,), dtype=np.float32)
        t1 = time.perf_counter()
        out = policy.predict_normalized_action_chunk(
            primary, wrist, "put the bowl on the plate", state
        )
        if torch.cuda.is_available() and str(policy.device).startswith("cuda"):
            torch.cuda.synchronize(policy.device)
        result["forward_seconds"] = time.perf_counter() - t1
        result["output_shape"] = list(out.shape)
        result["output_finite"] = bool(np.isfinite(out).all())
        result["output_min"] = float(out.min())
        result["output_max"] = float(out.max())
        result["peak_cuda_allocated_bytes"] = int(torch.cuda.max_memory_allocated(policy.device)) if torch.cuda.is_available() and str(policy.device).startswith("cuda") else None
        result["peak_cuda_reserved_bytes"] = int(torch.cuda.max_memory_reserved(policy.device)) if torch.cuda.is_available() and str(policy.device).startswith("cuda") else None
        result["status"] = "passed"
    except Exception as exc:
        result["status"] = "failed"
        result["error_type"] = type(exc).__name__
        result["error"] = str(exc)
        raise
    finally:
        result["elapsed_seconds"] = time.perf_counter() - t0
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
