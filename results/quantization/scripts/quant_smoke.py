"""One-observation quantization smoke test before LIBERO batch runs."""
from __future__ import annotations

import argparse
import datetime as dt
import gc
import json
import os
from pathlib import Path
import sys
import time

import numpy as np
import torch


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--libero-root", required=True)
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--dino", required=True)
    p.add_argument("--bert", required=True)
    p.add_argument("--stats", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--modes", default="fp32,w8a8,w8a16,w8afp16")
    return p.parse_args()


def patch_checkpoint_loader():
    import turbovla.evaluation.policy as policy_module

    def load_state(checkpoint):
        if isinstance(checkpoint, dict):
            if isinstance(checkpoint.get("ema_model_state_dict"), dict):
                return checkpoint["ema_model_state_dict"]
            if isinstance(checkpoint.get("model_state_dict"), dict):
                return checkpoint["model_state_dict"]
        raise KeyError("checkpoint has neither ema_model_state_dict nor model_state_dict")

    policy_module._checkpoint_state_dict = load_state


def get_obs(libero_root: str, seed: int):
    sys.path.insert(0, libero_root)
    from libero.libero import benchmark, get_libero_path
    from libero.libero.envs import OffScreenRenderEnv

    suite = benchmark.get_benchmark_dict()["libero_spatial"]()
    task = suite.get_task(0)
    initial_state = suite.get_task_init_states(0)[0]
    bddl = Path(get_libero_path("bddl_files")) / task.problem_folder / task.bddl_file
    env = OffScreenRenderEnv(bddl_file_name=str(bddl), camera_heights=256, camera_widths=256)
    env.seed(seed)
    env.reset()
    obs = env.set_init_state(initial_state)
    return obs, task.language, env


def main():
    args = parse_args()
    os.environ.setdefault("MUJOCO_GL", "egl")
    os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
    sys.path.insert(0, args.source)
    sys.path.insert(0, str(Path(args.source) / "third_party" / "vla_adapter"))
    sys.path.insert(0, str(Path(__file__).parent))
    patch_checkpoint_loader()

    import turbovla.evaluation.suite_policy as suite_policy
    from turbovla.evaluation.suite_policy import rotate_libero_image, set_seed_everywhere
    from turbovla.evaluation.policy import build_dinov3_manual_processor
    from run_eval_quant import make_policy_class

    obs, instruction, env = get_obs(args.libero_root, args.seed)
    primary = rotate_libero_image(obs["agentview_image"])
    wrist = rotate_libero_image(obs["robot0_eye_in_hand_image"])
    modes = tuple(x.strip().lower() for x in args.modes.split(",") if x.strip())
    if not modes or any(x not in {"fp32", "w8a8", "w8a16", "w8afp16"} for x in modes):
        raise ValueError(f"invalid --modes={args.modes!r}")
    outputs = {}
    records = {
        "status": "started",
        "started": dt.datetime.now().isoformat(timespec="seconds"),
        "suite": "libero_spatial",
        "task_id": 0,
        "initial_state_index": 0,
        "seed": args.seed,
        "instruction": instruction,
        "image_shapes": [list(primary.shape), list(wrist.shape)],
        "modes": {},
    }
    try:
        for mode in modes:
            set_seed_everywhere(args.seed)
            cls = make_policy_class(suite_policy.TurboVLAPolicy, mode)
            t0 = time.perf_counter()
            policy = cls(
                ckpt_path=args.checkpoint,
                dinov3_path=args.dino,
                bert_path=args.bert,
                stats_path=args.stats,
                stats_key="libero_all4_no_noops",
                device="cuda",
                precision="fp32",
                allow_hf_download=False,
                verbose=False,
            )
            with torch.inference_mode():
                out = policy.predict_normalized_action_chunk(primary, wrist, instruction, obs)
            outputs[mode] = np.asarray(out, dtype=np.float32)
            records["modes"][mode] = {
                "status": "passed",
                "elapsed_s": time.perf_counter() - t0,
                "output_shape": list(outputs[mode].shape),
                "output_finite": bool(np.isfinite(outputs[mode]).all()),
                "output_dtype": policy.runtime_dtype,
                "quantization": policy.quantization_summary,
            }
            del policy
            gc.collect()
            torch.cuda.empty_cache()
        if "fp32" in outputs:
            ref = outputs["fp32"]
            for mode in modes:
                if mode == "fp32":
                    continue
                delta = np.abs(outputs[mode] - ref)
                records["modes"][mode]["max_abs_vs_fp32"] = float(delta.max())
                records["modes"][mode]["mean_abs_vs_fp32"] = float(delta.mean())
        records["status"] = "passed"
    except Exception as exc:
        records["status"] = "failed"
        records["error_type"] = type(exc).__name__
        records["error"] = str(exc)
        raise
    finally:
        env.close()
        records["finished"] = dt.datetime.now().isoformat(timespec="seconds")
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(records, indent=2, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
