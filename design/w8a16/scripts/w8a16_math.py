"""Bit-exact reference helpers for the TurboVLA W8A16 path.

The old screening wrapper is intentionally not imported here: it quantizes and
then calls a floating point ``F.linear``.  This module keeps the integer
accumulator visible so that software, compiler and RTL can share one contract.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any

import numpy as np


@dataclass(frozen=True)
class Quantized:
    q: np.ndarray
    scale: Any
    bits: int
    qmin: int
    qmax: int


def _bounds(bits: int, allow_signed_min: bool = True) -> tuple[int, int]:
    if bits < 2 or bits > 31:
        raise ValueError(f"unsupported signed width: {bits}")
    return (-(1 << (bits - 1)) if allow_signed_min else -((1 << (bits - 1)) - 1),
            (1 << (bits - 1)) - 1)


def quantize_symmetric(x: np.ndarray, bits: int, *, allow_signed_min: bool = True) -> Quantized:
    """Per-tensor symmetric quantization with deterministic round-to-nearest.

    ``allow_signed_min=True`` is the hardware contract from the work plan.
    The previous fake-quant wrapper used a symmetric ``[-qmax, qmax]`` range;
    callers can set it to False to reproduce that historical reference.
    """
    arr = np.asarray(x, dtype=np.float64)
    qmin, qmax = _bounds(bits, allow_signed_min)
    scale = max(float(np.max(np.abs(arr))) / float(qmax), 1.0e-8)
    q = np.rint(arr / scale).clip(qmin, qmax)
    dtype = np.int8 if bits <= 8 else np.int16
    return Quantized(q.astype(dtype), scale, bits, qmin, qmax)


def quantize_weight_per_output(weight: np.ndarray, *, allow_signed_min: bool = True) -> Quantized:
    """Per-output-channel INT8 weights, matching the screening convention."""
    w = np.asarray(weight, dtype=np.float64)
    if w.ndim < 2:
        raise ValueError("weight must have an output-channel dimension and K")
    qmin, qmax = _bounds(8, allow_signed_min)
    flat = w.reshape(w.shape[0], -1)
    scale = np.maximum(np.max(np.abs(flat), axis=1) / float(qmax), 1.0e-8)
    q = np.rint(flat / scale[:, None]).clip(qmin, qmax).astype(np.int8)
    return Quantized(q.reshape(w.shape), scale.astype(np.float64), 8, qmin, qmax)


def integer_linear(q_a: np.ndarray, q_w: np.ndarray, *, bias: np.ndarray | None = None,
                   acc_bits: int = 40) -> np.ndarray:
    """Signed integer XW^T with a checked accumulator width.

    NumPy accumulates in int64, then checks the configured hardware width.  A
    real RTL implementation must not silently wrap here.
    """
    a = np.asarray(q_a)
    w = np.asarray(q_w)
    if a.shape[-1] != w.shape[-1]:
        raise ValueError(f"K mismatch: {a.shape[-1]} vs {w.shape[-1]}")
    acc64 = np.matmul(a.astype(np.int64), np.swapaxes(w.astype(np.int64), -1, -2))
    lo, hi = -(1 << (acc_bits - 1)), (1 << (acc_bits - 1)) - 1
    if np.any(acc64 < lo) or np.any(acc64 > hi):
        bad = int(np.max(np.abs(acc64)))
        raise OverflowError(f"accumulator overflow for {acc_bits} bits; max_abs={bad}")
    out = acc64.astype(np.int64)
    if bias is not None:
        out = out + np.asarray(bias, dtype=np.int64)
    return out


def dequantized_linear(q_a: np.ndarray, a_scale: float | np.ndarray,
                       q_w: np.ndarray, w_scale: np.ndarray | float,
                       *, bias: np.ndarray | None = None,
                       acc_bits: int = 40) -> tuple[np.ndarray, np.ndarray]:
    """Return the integer accumulator and its dequantized FP64 result."""
    acc = integer_linear(q_a, q_w, acc_bits=acc_bits)
    result = acc.astype(np.float64)
    result *= np.asarray(a_scale, dtype=np.float64)
    result *= np.asarray(w_scale, dtype=np.float64)
    if bias is not None:
        result += np.asarray(bias, dtype=np.float64)
    return acc, result


def requantize(acc: np.ndarray, multiplier: int, shift: int, *, bits: int = 16) -> np.ndarray:
    """Integer arithmetic-shift requantization with saturation."""
    if shift < 0:
        raise ValueError("shift must be non-negative")
    qmin, qmax = _bounds(bits, allow_signed_min=True)
    t = np.asarray(acc, dtype=np.int64) * int(multiplier)
    if shift:
        t = t >> int(shift)
    return np.clip(t, qmin, qmax).astype(np.int16 if bits > 8 else np.int8)


def required_acc_bits(k: int, a_bits: int = 16, w_bits: int = 8) -> int:
    """Conservative signed width for a full-K worst-case dot product."""
    if k < 1:
        raise ValueError("K must be positive")
    max_product = (1 << (a_bits - 1)) * (1 << (w_bits - 1))
    max_sum = int(k) * max_product
    return max(1, int(math.ceil(math.log2(max_sum + 1))) + 1)


def contract_summary() -> dict[str, Any]:
    return {
        "weights": {"bits": 8, "signed_range": [-128, 127], "per": "output_channel"},
        "activations": {"bits": 16, "signed_range": [-32768, 32767], "per": "tensor"},
        "accumulator_bits": 40,
        "output_bits": 16,
        "bias": "separate integer or FP32 fallback; never silently dropped",
        "old_fake_quant_note": "historical wrapper uses symmetric [-qmax,qmax] and FP32 F.linear",
    }
