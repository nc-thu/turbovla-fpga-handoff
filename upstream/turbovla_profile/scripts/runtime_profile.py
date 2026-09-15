"""Runtime profiling on one real LIBERO observation.

The observation comes from LIBERO Spatial task 0, initial state 0.  This is a
runtime/profile measurement, not a success-rate benchmark.  The policy and
environment are instantiated once per process; CUDA is synchronized around
each call.
"""
from __future__ import annotations

import argparse
import gc
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch


def patch_checkpoint_loader() -> None:
    import turbovla.evaluation.policy as policy_module

    def checkpoint_state_dict(checkpoint):
        if isinstance(checkpoint, dict):
            if isinstance(checkpoint.get("ema_model_state_dict"), dict):
                return checkpoint["ema_model_state_dict"]
            if isinstance(checkpoint.get("model_state_dict"), dict):
                return checkpoint["model_state_dict"]
        raise KeyError("checkpoint has neither ema_model_state_dict nor model_state_dict")

    policy_module._checkpoint_state_dict = checkpoint_state_dict


def get_observation(libero_root: str, seed: int) -> tuple[dict, str, object]:
    sys.path.insert(0, libero_root)
    from libero.libero import benchmark, get_libero_path
    from libero.libero.envs import OffScreenRenderEnv

    suite = benchmark.get_benchmark_dict()["libero_spatial"]()
    task = suite.get_task(0)
    initial_state = suite.get_task_init_states(0)[0]
    bddl = Path(get_libero_path("bddl_files")) / task.problem_folder / task.bddl_file
    env = OffScreenRenderEnv(
        bddl_file_name=str(bddl), camera_heights=256, camera_widths=256
    )
    env.seed(seed)
    env.reset()
    obs = env.set_init_state(initial_state)
    return obs, task.language, env


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--libero-root", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--dino", required=True)
    ap.add_argument("--bert", required=True)
    ap.add_argument("--stats", required=True)
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--precision", choices=["fp32", "bf16"], default="fp32")
    ap.add_argument("--warmup", type=int, default=5)
    ap.add_argument("--repeat", type=int, default=10)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--output", required=True)
    ap.add_argument("--trace", required=True)
    args = ap.parse_args()
    os.environ.setdefault("MUJOCO_GL", "egl")
    os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
    sys.path.insert(0, args.source)
    patch_checkpoint_loader()
    from turbovla.evaluation.suite_policy import TurboVLAPolicy, rotate_libero_image, set_seed_everywhere

    result: dict = {
        "status": "started",
        "precision": args.precision,
        "device": args.device,
        "seed": args.seed,
        "task_suite": "libero_spatial",
        "task_id": 0,
        "initial_state_index": 0,
        "warmup": args.warmup,
        "repeat": args.repeat,
        "observation_resolution": [256, 256],
        "source": os.path.abspath(args.source),
        "checkpoint": os.path.abspath(args.checkpoint),
    }
    t0 = time.perf_counter()
    env = None
    try:
        set_seed_everywhere(args.seed)
        obs, instruction, env = get_observation(args.libero_root, args.seed)
        primary = rotate_libero_image(obs["agentview_image"])
        wrist = rotate_libero_image(obs["robot0_eye_in_hand_image"])
        policy = TurboVLAPolicy(
            ckpt_path=args.checkpoint,
            dinov3_path=args.dino,
            bert_path=args.bert,
            stats_path=args.stats,
            stats_key="libero_all4_no_noops",
            device=args.device,
            precision=args.precision,
            allow_hf_download=False,
            verbose=False,
        )
        result["instruction"] = instruction
        result["image_shapes"] = [list(primary.shape), list(wrist.shape)]
        result["parameters"] = int(sum(p.numel() for p in policy.model.parameters()))
        result["parameter_dtypes"] = sorted({str(p.dtype) for p in policy.model.parameters()})
        for _ in range(args.warmup):
            _ = policy.predict_normalized_action_chunk(primary, wrist, instruction, obs)
        torch.cuda.synchronize(policy.device)
        torch.cuda.reset_peak_memory_stats(policy.device)
        # One short trace is kept for operator attribution.  It is separate
        # from the synchronized timing loop below and is never included in
        # the reported median/P90.
        try:
            from torch.profiler import ProfilerActivity, profile

            with profile(
                activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
                record_shapes=True,
                profile_memory=True,
                with_stack=False,
            ) as prof:
                _ = policy.predict_normalized_action_chunk(primary, wrist, instruction, obs)
            torch.cuda.synchronize(policy.device)
            Path(args.trace).parent.mkdir(parents=True, exist_ok=True)
            prof.export_chrome_trace(args.trace)
            Path(args.trace + ".txt").write_text(
                prof.key_averages().table(sort_by="self_cuda_time_total", row_limit=40),
                encoding="utf-8",
            )
            result["trace_status"] = "passed"
        except Exception as trace_exc:
            result["trace_status"] = "failed"
            result["trace_error"] = f"{type(trace_exc).__name__}: {trace_exc}"
        wall_ms: list[float] = []
        gpu_ms: list[float] = []
        outputs: list[np.ndarray] = []
        for _ in range(args.repeat):
            torch.cuda.synchronize(policy.device)
            start = time.perf_counter()
            ev0 = torch.cuda.Event(enable_timing=True)
            ev1 = torch.cuda.Event(enable_timing=True)
            ev0.record()
            out = policy.predict_normalized_action_chunk(primary, wrist, instruction, obs)
            ev1.record()
            torch.cuda.synchronize(policy.device)
            wall_ms.append((time.perf_counter() - start) * 1000.0)
            gpu_ms.append(float(ev0.elapsed_time(ev1)))
            outputs.append(np.asarray(out, dtype=np.float32))
        result["wall_ms"] = wall_ms
        result["gpu_ms"] = gpu_ms
        for name, vals in [("wall_ms", wall_ms), ("gpu_ms", gpu_ms)]:
            arr = np.asarray(vals, dtype=np.float64)
            result[name + "_median"] = float(np.median(arr))
            result[name + "_p90"] = float(np.percentile(arr, 90))
            result[name + "_min"] = float(np.min(arr))
            result[name + "_max"] = float(np.max(arr))
        result["output_shape"] = list(outputs[0].shape)
        result["output_finite"] = bool(all(np.isfinite(x).all() for x in outputs))
        result["repeat_max_abs_delta"] = float(max(np.max(np.abs(outputs[i] - outputs[0])) for i in range(len(outputs))))
        result["peak_cuda_allocated_bytes"] = int(torch.cuda.max_memory_allocated(policy.device))
        result["peak_cuda_reserved_bytes"] = int(torch.cuda.max_memory_reserved(policy.device))
        result["status"] = "passed"
    except Exception as exc:
        result["status"] = "failed"
        result["error_type"] = type(exc).__name__
        result["error"] = str(exc)
        raise
    finally:
        if env is not None:
            env.close()
        result["elapsed_seconds"] = time.perf_counter() - t0
        Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2), flush=True)
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
