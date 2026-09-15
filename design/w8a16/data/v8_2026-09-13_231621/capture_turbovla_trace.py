"""Capture one real TurboVLA LIBERO forward into a replay-friendly trace.

The wrapper is deliberately separate from the historical profiler.  It records
module boundaries and low-level ATen operations, while saving only quantised
linear payloads and deduplicated weights needed by the replay compiler.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def shape_of(x: Any) -> list[int] | None:
    try:
        return [int(v) for v in x.shape]
    except Exception:
        return None


def dtype_of(x: Any) -> str | None:
    try:
        return str(x.dtype).replace("torch.", "")
    except Exception:
        return None


def first_tensor(obj: Any):
    import torch

    if isinstance(obj, torch.Tensor):
        return obj
    if isinstance(obj, (tuple, list)):
        for item in obj:
            found = first_tensor(item)
            if found is not None:
                return found
    if isinstance(obj, dict):
        for item in obj.values():
            found = first_tensor(item)
            if found is not None:
                return found
    return None


def patch_checkpoint_loader() -> None:
    # Released checkpoints in the historical directory use EMA weights.  The
    # helper keeps this wrapper compatible with both old and new checkpoint
    # containers without changing the source tree.
    import turbovla.evaluation.policy as policy_module

    def checkpoint_state_dict(checkpoint):
        if isinstance(checkpoint, dict):
            for key in ("ema_model_state_dict", "model_state_dict"):
                if isinstance(checkpoint.get(key), dict):
                    return checkpoint[key]
        raise KeyError("checkpoint has no model_state_dict or ema_model_state_dict")

    policy_module._checkpoint_state_dict = checkpoint_state_dict


class Recorder:
    def __init__(self, out_dir: Path):
        self.out_dir = out_dir
        self.events: list[dict[str, Any]] = []
        self.module_events: list[dict[str, Any]] = []
        self.module_stack: list[str] = []
        self.seq = 0
        self.mod_seq = 0
        self.weight_records: dict[str, dict[str, Any]] = {}
        self.payload_path = out_dir / "activation_payload.bin"
        self.weight_path = out_dir / "weight_payload.bin"
        self.payload_path.write_bytes(b"")
        self.weight_path.write_bytes(b"")
        self.scales: dict[str, Any] = {}

    @property
    def current_module(self) -> str:
        return self.module_stack[-1] if self.module_stack else "<top>"

    def _write(self, path: Path, data: bytes) -> tuple[int, int]:
        offset = path.stat().st_size
        with path.open("ab") as f:
            f.write(data)
        return int(offset), int(len(data))

    def quantize_activation(self, tensor, scale_id: str) -> tuple[np.ndarray, float]:
        arr = tensor.detach().float().cpu().numpy().astype(np.float32, copy=False)
        scale = float(np.max(np.abs(arr)) / 32767.0) if arr.size else 1.0
        scale = max(scale, 1e-6)
        q = np.clip(np.rint(arr / scale), -32768, 32767).astype("<i2")
        self.scales[scale_id] = {"kind": "activation", "bits": 16, "scale": scale}
        return q, scale

    def quantize_weight(self, tensor, scale_prefix: str) -> tuple[np.ndarray, list[float]]:
        arr = tensor.detach().float().cpu().numpy().astype(np.float32, copy=False)
        if arr.ndim >= 2:
            flat = arr.reshape(arr.shape[0], -1)
            scales = np.maximum(np.max(np.abs(flat), axis=1) / 127.0, 1e-6)
            q = np.clip(np.rint(flat / scales[:, None]), -128, 127).astype("i1")
            q = q.reshape(arr.shape)
        else:
            scale = max(float(np.max(np.abs(arr)) / 127.0) if arr.size else 1.0, 1e-6)
            scales = np.asarray([scale], dtype=np.float32)
            q = np.clip(np.rint(arr / scale), -128, 127).astype("i1")
        self.scales[scale_prefix] = {"kind": "weight", "bits": 8, "scale": scales.tolist()}
        return q, scales.tolist()

    def save_linear_payload(self, module_name: str, x, weight, seq: int) -> dict[str, Any]:
        qx, _ = self.quantize_activation(x, f"ev{seq}.a")
        qw, _ = self.quantize_weight(weight, f"ev{seq}.w")
        xb = qx.tobytes(order="C")
        wh = sha256_bytes(qw.tobytes(order="C"))
        if wh in self.weight_records:
            wr = self.weight_records[wh]
        else:
            woff, wlen = self._write(self.weight_path, qw.tobytes(order="C"))
            wr = {"hash": wh, "offset": woff, "length": wlen, "shape": list(qw.shape), "dtype": "int8"}
            self.weight_records[wh] = wr
        aoff, alen = self._write(self.payload_path, xb)
        return {
            "activation_offset": aoff,
            "activation_length": alen,
            "activation_shape": list(qx.shape),
            "activation_dtype": "int16",
            "weight_hash": wh,
            "weight_offset": wr["offset"],
            "weight_length": wr["length"],
            "weight_shape": wr["shape"],
            "weight_dtype": "int8",
        }

    def add_module_event(self, name: str, module, inputs, output, elapsed_ns: int, kind: str):
        import torch

        x = first_tensor(inputs)
        y = first_tensor(output)
        rec: dict[str, Any] = {
            "seq": self.mod_seq,
            "module_path": name,
            "op_type": kind,
            "input_shape": shape_of(x),
            "output_shape": shape_of(y),
            "dtype": dtype_of(y),
            "elapsed_ns": int(elapsed_ns),
            "parent_event": self.events[-1]["seq"] if self.events else None,
            "status": "aux_behavior",
            "mapping": "aux_behavior",
        }
        if isinstance(module, torch.nn.Linear) and x is not None and x.numel() > 0:
            k = int(module.weight.shape[1])
            n = int(module.weight.shape[0])
            m = int(x.numel() // k) if k else 0
            payload = self.save_linear_payload(name, x, module.weight, self.mod_seq)
            rec.update({
                "op_type": "linear",
                "m": m,
                "n": n,
                "k": k,
                "status": "mapped",
                "mapping": "rtl_gemm",
                "payload": payload,
                "bias": bool(module.bias is not None),
                "input_bytes": int(x.numel() * x.element_size()),
                "output_bytes": int(y.numel() * y.element_size()) if y is not None else 0,
            })
        elif y is not None:
            rec["input_bytes"] = int(x.numel() * x.element_size()) if x is not None else 0
            rec["output_bytes"] = int(y.numel() * y.element_size())
        self.module_events.append(rec)
        self.mod_seq += 1

    def add_dispatch(self, func, args, kwargs):
        name = str(getattr(func, "_overloadpacket", func)).replace("aten::", "aten.")
        op = name.split(".")[-1]
        tensors = []
        for obj in list(args) + list(kwargs.values()):
            t = first_tensor(obj)
            if t is not None:
                tensors.append(t)
        out_shape = None
        event = {
            "seq": self.seq,
            "module_path": self.current_module,
            "parent_event": self.module_events[-1]["seq"] if self.module_events else None,
            "op_type": op,
            "aten": name,
            "input_shapes": [shape_of(t) for t in tensors],
            "dtype": dtype_of(tensors[0]) if tensors else None,
            "status": "mapped" if op in {"mm", "bmm", "matmul", "addmm", "convolution", "convolution_overrideable"} else "aux_behavior",
            "mapping": "rtl_bmm" if op == "bmm" else ("rtl_gemm" if op in {"mm", "matmul", "addmm", "convolution", "convolution_overrideable"} else "aux_behavior"),
            "input_bytes": int(sum(t.numel() * t.element_size() for t in tensors)),
        }
        self.events.append(event)
        self.seq += 1


def install_hooks(model, recorder: Recorder):
    import torch

    handles = []
    timed: dict[int, int] = {}

    def pre(name):
        def _pre(module, inputs):
            recorder.module_stack.append(name)
            timed[id(module)] = time.perf_counter_ns()
        return _pre

    def post(name):
        def _post(module, inputs, output):
            start = timed.pop(id(module), time.perf_counter_ns())
            recorder.add_module_event(name, module, inputs, output, time.perf_counter_ns() - start, module.__class__.__name__)
            if recorder.module_stack:
                recorder.module_stack.pop()
        return _post

    for name, module in model.named_modules():
        if not name:
            continue
        if isinstance(module, (torch.nn.Linear, torch.nn.Conv1d, torch.nn.Conv2d, torch.nn.LayerNorm, torch.nn.GELU, torch.nn.ReLU, torch.nn.MultiheadAttention)):
            handles.append(module.register_forward_pre_hook(pre(name)))
            handles.append(module.register_forward_hook(post(name)))

    class Dispatch(torch.utils._python_dispatch.TorchDispatchMode):
        def __torch_dispatch__(self, func, types, args=(), kwargs=None):
            kwargs = kwargs or {}
            recorder.add_dispatch(func, args, kwargs)
            return func(*args, **kwargs)

    return handles, Dispatch()


def get_observation(libero_root: str, seed: int):
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--libero-root", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--dino", required=True)
    ap.add_argument("--bert", required=True)
    ap.add_argument("--stats", required=True)
    ap.add_argument("--stats-key", default="libero_all4_no_noops")
    ap.add_argument("--device", default="cuda:3")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MUJOCO_GL", "egl")
    os.environ.setdefault("PYOPENGL_PLATFORM", "egl")
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
    sys.path.insert(0, args.source)
    import torch

    patch_checkpoint_loader()
    from turbovla.evaluation.suite_policy import TurboVLAPolicy, rotate_libero_image, set_seed_everywhere

    result: dict[str, Any] = {
        "status": "started",
        "capture_version": "tvla_activity.v1",
        "seed": args.seed,
        "device": args.device,
        "suite": "libero_spatial",
        "task_id": 0,
        "image_resolution": [256, 256],
        "source": str(Path(args.source).resolve()),
        "checkpoint": str(Path(args.checkpoint).resolve()),
        "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    env = None
    t0 = time.perf_counter()
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
            stats_key=args.stats_key,
            device=args.device,
            precision="fp32",
            allow_hf_download=False,
            verbose=False,
        )
        recorder = Recorder(out)
        handles, dispatch = install_hooks(policy.model, recorder)
        with dispatch:
            with torch.inference_mode():
                action = policy.predict_normalized_action_chunk(primary, wrist, instruction, obs)
        for h in handles:
            h.remove()
        torch.cuda.synchronize(policy.device)
        result.update({
            "status": "passed",
            "instruction": instruction,
            "action_shape": list(np.asarray(action).shape),
            "action_finite": bool(np.isfinite(action).all()),
            "parameters": int(sum(p.numel() for p in policy.model.parameters())),
            "module_event_count": len(recorder.module_events),
            "dispatch_event_count": len(recorder.events),
            "linear_event_count": int(sum(e.get("mapping") == "rtl_gemm" for e in recorder.module_events)),
            "weight_unique_count": len(recorder.weight_records),
            "activation_payload_bytes": recorder.payload_path.stat().st_size,
            "weight_payload_bytes": recorder.weight_path.stat().st_size,
            "ended_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        (out / "action_output.json").write_text(json.dumps(np.asarray(action).tolist()), encoding="utf-8")
        (out / "operator_trace.jsonl").write_text("\n".join(json.dumps(e, sort_keys=True) for e in recorder.events) + "\n", encoding="utf-8")
        (out / "module_events.jsonl").write_text("\n".join(json.dumps(e, sort_keys=True) for e in recorder.module_events) + "\n", encoding="utf-8")
        (out / "scale_table.json").write_text(json.dumps(recorder.scales, indent=2), encoding="utf-8")
        (out / "weight_manifest.json").write_text(json.dumps(list(recorder.weight_records.values()), indent=2), encoding="utf-8")
    except Exception as exc:
        result.update({"status": "failed", "error_type": type(exc).__name__, "error": str(exc)})
        raise
    finally:
        if env is not None:
            env.close()
        result["elapsed_seconds"] = time.perf_counter() - t0
        result["ended_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        (out / "capture_result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2), flush=True)


if __name__ == "__main__":
    main()
