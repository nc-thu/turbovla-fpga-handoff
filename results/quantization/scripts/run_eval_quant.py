"""Run one or more official LIBERO suites with TurboVLA fake quantization.

The evaluator and episode protocol are imported from the released source.  A
local policy subclass only adds numerical fake-quantization and per-call wall
timing; task generation, initial states, action chunking, and success
judgement stay in the official evaluator.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys
import time
from typing import Any


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


def make_policy_class(base_cls, mode: str):
    import time as _time

    from quantization import apply_fake_quant, finalize_model_dtype, model_quantization_summary

    class QuantizedTurboVLAPolicy(base_cls):
        def __init__(self, *args, **kwargs):
            # The upstream policy accepts fp32/bf16 only.  Start from its
            # verified FP32 path, then install the requested fake-quant mode.
            kwargs["precision"] = "fp32"
            super().__init__(*args, **kwargs)
            self.quant_mode = mode
            self.call_wall_ms: list[float] = []
            if mode == "fp32":
                from quantization import QuantizationStats

                self.quantization_stats = QuantizationStats(
                    mode="fp32",
                    weight_bits=32,
                    activation_format="FP32",
                    activation_bits=None,
                    weight_scheme="none",
                    unsupported_weight_modules=[],
                )
                self.quantization_summary = model_quantization_summary(self.model, self.quantization_stats)
                self.runtime_dtype = "torch.float32"
            else:
                self.quantization_stats = apply_fake_quant(self.model, mode)
                runtime_dtype = finalize_model_dtype(self.model, mode)
                self.model_dtype = runtime_dtype
                self.precision = mode
                self.quantization_summary = model_quantization_summary(self.model, self.quantization_stats)
                self.runtime_dtype = str(runtime_dtype)
            type(self)._last_instance = self

        def _prepare_model_inputs(self, samples, states):
            samples, states = super()._prepare_model_inputs(samples, states)
            # The base class uses self.model_dtype, which is changed to FP16
            # for W8A(FP16) after the wrappers are installed.  The explicit
            # override documents the intended input contract and protects
            # against future upstream changes to the base helper.
            if self.quant_mode == "w8afp16":
                samples = {
                    key: value.to(dtype=__import__("torch").float16)
                    if value.is_floating_point()
                    else value
                    for key, value in samples.items()
                }
                states = states.to(dtype=__import__("torch").float16)
            return samples, states

        def predict_normalized_action_chunk(self, *args, **kwargs):
            start = _time.perf_counter()
            out = super().predict_normalized_action_chunk(*args, **kwargs)
            self.call_wall_ms.append((_time.perf_counter() - start) * 1000.0)
            return out

    QuantizedTurboVLAPolicy.__name__ = f"TurboVLAPolicy_{mode}"
    return QuantizedTurboVLAPolicy


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="TurboVLA LIBERO fake-quant evaluation")
    p.add_argument("--source", required=True)
    p.add_argument("--libero-root", required=True)
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--dino", required=True)
    p.add_argument("--bert", required=True)
    p.add_argument("--stats", required=True)
    p.add_argument("--stats-key", default="libero_all4_no_noops")
    p.add_argument("--mode", choices=("fp32", "w8a8", "w8a16", "w8afp16"), required=True)
    p.add_argument("--suite", required=True)
    p.add_argument("--task-ids", default="0,1")
    p.add_argument("--episodes", type=int, default=3)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--num-open-loop-steps", type=int, default=12)
    p.add_argument("--chunk-size", type=int, default=12)
    p.add_argument("--num-steps-wait", type=int, default=10)
    p.add_argument("--output", required=True)
    p.add_argument("--log", required=True)
    p.add_argument("--video-root", required=True)
    p.add_argument("--save-video", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    os.environ.setdefault("MUJOCO_GL", "egl")
    os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
    sys.path.insert(0, args.source)
    sys.path.insert(0, str(Path(args.source) / "third_party" / "vla_adapter"))
    patch_checkpoint_loader()

    import turbovla.evaluation.suite_policy as suite_policy
    import vla_adapter.rollout as rollout

    BasePolicy, dummy, rotate, seed_fn = rollout._import_turbovla_adapter()
    QuantPolicy = make_policy_class(BasePolicy, args.mode)
    last_policy: dict[str, Any] = {}

    def patched_import():
        return QuantPolicy, dummy, rotate, seed_fn

    rollout._import_turbovla_adapter = patched_import
    cfg = rollout.GenerateConfig(
        ckpt_path=args.checkpoint,
        libero_root=args.libero_root,
        dinov3_path=args.dino,
        bert_path=args.bert,
        stats_path=args.stats,
        stats_key=args.stats_key,
        task_suite_name=args.suite,
        task_ids=args.task_ids,
        num_trials_per_task=args.episodes,
        num_steps_wait=args.num_steps_wait,
        num_open_loop_steps=args.num_open_loop_steps,
        chunk_size=args.chunk_size,
        seed=args.seed,
        precision="fp32",
        mujoco_gl="egl",
        pyopengl_platform="egl",
        save_video=args.save_video,
        video_out_path=args.video_root,
        result_json_path=args.output,
        log_path=args.log,
    )

    started = dt.datetime.now().isoformat(timespec="seconds")
    t0 = time.perf_counter()
    final_rate = rollout.eval_libero(cfg)
    elapsed = time.perf_counter() - t0
    payload = json.loads(Path(args.output).read_text(encoding="utf-8"))
    # eval_libero creates the policy inside its local scope.  Recover it from
    # the class-level registry used below when available; otherwise timing is
    # explicitly marked unavailable rather than guessed from episode count.
    policy = getattr(QuantPolicy, "_last_instance", None)
    quant_summary = getattr(policy, "quantization_summary", None)
    call_times = getattr(policy, "call_wall_ms", None)
    payload["quantization_mode"] = args.mode
    payload["quantization"] = quant_summary
    payload["experiment_started"] = started
    payload["experiment_finished"] = dt.datetime.now().isoformat(timespec="seconds")
    payload["experiment_elapsed_seconds"] = elapsed
    if call_times:
        arr = sorted(float(x) for x in call_times)
        payload["policy_call_timing_ms"] = {
            "count": len(arr),
            "median": arr[len(arr) // 2] if len(arr) % 2 else (arr[len(arr)//2-1] + arr[len(arr)//2]) / 2.0,
            "p90": arr[max(0, int(0.9 * len(arr) + 0.999999) - 1)],
            "min": arr[0],
            "max": arr[-1],
        }
    else:
        payload["policy_call_timing_ms"] = {"status": "unavailable"}
    Path(args.output).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"suite": args.suite, "mode": args.mode, "rate": final_rate, "elapsed_s": elapsed}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
