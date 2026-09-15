"""Software-only W8A8/W8A16/W8A(FP16) fake-quantization for TurboVLA.

The wrappers deliberately keep the released model and checkpoint untouched.  A
weight is quantized symmetrically per output channel and immediately
dequantized for the CUDA reference operator.  W8A8 and W8A16 additionally
quantize each linear/conv/MHA input at call time with a per-tensor scale.  The
FP16-activation mode converts the model to FP16 after the INT8 weight grid has
been fixed.  This is a numerical screening path, not an INT8 CUDA kernel or a
claim about FPGA latency.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import torch
from torch import nn
from torch.nn import functional as F


MODES = ("fp32", "w8a8", "w8a16", "w8afp16")


@dataclass
class QuantizationStats:
    mode: str
    weight_bits: int
    activation_format: str
    activation_bits: int | None
    weight_scheme: str
    quantized_linear: int = 0
    quantized_conv: int = 0
    quantized_mha: int = 0
    quantized_embedding: int = 0
    quantized_weight_values: int = 0
    quantized_weight_bytes: int = 0
    fp32_bias_values: int = 0
    unsupported_weight_modules: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _validate_mode(mode: str) -> str:
    mode = str(mode).lower()
    if mode not in MODES:
        raise ValueError(f"unsupported quantization mode {mode!r}; expected one of {MODES}")
    return mode


def _activation_bits(mode: str) -> int | None:
    return {"fp32": None, "w8a8": 8, "w8a16": 16, "w8afp16": None}[mode]


def _fake_quant_tensor(x: torch.Tensor, bits: int) -> torch.Tensor:
    """Symmetric per-tensor fake quantization, preserving the input shape."""
    if not x.is_floating_point():
        return x
    qmax = float((1 << (int(bits) - 1)) - 1)
    x32 = x.float()
    scale = x32.detach().abs().amax().clamp_min(1.0e-8) / qmax
    q = torch.round(x32 / scale).clamp(-qmax, qmax)
    return q * scale


def _quantize_weight(weight: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """Return int8 weights, per-output-channel scales, and FP32 dequantized weights."""
    w = weight.detach().float()
    flat = w.reshape(w.shape[0], -1)
    qmax = 127.0
    scale = flat.abs().amax(dim=1).clamp_min(1.0e-8) / qmax
    q = torch.round(flat / scale[:, None]).clamp(-qmax, qmax).to(torch.int8)
    deq = (q.float() * scale[:, None]).reshape_as(w)
    return q, scale, deq


def _quantize_embedding(weight: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    w = weight.detach().float()
    scale = w.abs().amax(dim=1, keepdim=True).clamp_min(1.0e-8) / 127.0
    q = torch.round(w / scale).clamp(-127.0, 127.0).to(torch.int8)
    return q, q.float() * scale


class _QuantBase(nn.Module):
    def __init__(self, mode: str) -> None:
        super().__init__()
        self.mode = _validate_mode(mode)
        self.act_bits = _activation_bits(self.mode)

    def _quant_activation(self, x: torch.Tensor) -> torch.Tensor:
        if self.mode == "w8afp16":
            return x.to(dtype=torch.float16)
        if self.act_bits is None:
            return x
        return _fake_quant_tensor(x, self.act_bits)

    @staticmethod
    def _compute_dtype(mode: str) -> torch.dtype:
        return torch.float16 if mode == "w8afp16" else torch.float32


class FakeQuantLinear(_QuantBase):
    def __init__(self, source: nn.Linear, mode: str) -> None:
        super().__init__(mode)
        q, scale, deq = _quantize_weight(source.weight)
        self.register_buffer("qweight", q)
        self.register_buffer("weight_scale", scale)
        self.register_buffer("dequant_weight", deq)
        if source.bias is None:
            self.register_buffer("bias", None)
        else:
            self.register_buffer("bias", source.bias.detach().float().clone())
        self.in_features = source.in_features
        self.out_features = source.out_features

    @property
    def weight(self) -> torch.Tensor:
        # A few released model helpers inspect ``module.weight.dtype`` when
        # choosing the surrounding activation dtype.  Expose the dequantized
        # view without making it a trainable Parameter.
        return self.dequant_weight

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = self._compute_dtype(self.mode)
        xq = self._quant_activation(x).to(dtype=dtype)
        weight = self.dequant_weight.to(dtype=dtype)
        bias = None if self.bias is None else self.bias.to(dtype=dtype)
        return F.linear(xq, weight, bias)


class FakeQuantConv(_QuantBase):
    def __init__(self, source: nn.modules.conv._ConvNd, mode: str) -> None:
        super().__init__(mode)
        q, scale, deq = _quantize_weight(source.weight)
        self.register_buffer("qweight", q)
        self.register_buffer("weight_scale", scale)
        self.register_buffer("dequant_weight", deq)
        if source.bias is None:
            self.register_buffer("bias", None)
        else:
            self.register_buffer("bias", source.bias.detach().float().clone())
        self.stride = source.stride
        self.padding = source.padding
        self.dilation = source.dilation
        self.groups = source.groups
        self.in_channels = source.in_channels
        self.out_channels = source.out_channels
        self.kernel_size = source.kernel_size

    @property
    def weight(self) -> torch.Tensor:
        return self.dequant_weight

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        dtype = self._compute_dtype(self.mode)
        xq = self._quant_activation(x).to(dtype=dtype)
        weight = self.dequant_weight.to(dtype=dtype)
        bias = None if self.bias is None else self.bias.to(dtype=dtype)
        if self.dequant_weight.ndim == 3:
            return F.conv1d(xq, weight, bias, self.stride, self.padding, self.dilation, self.groups)
        if self.dequant_weight.ndim == 4:
            return F.conv2d(xq, weight, bias, self.stride, self.padding, self.dilation, self.groups)
        if self.dequant_weight.ndim == 5:
            return F.conv3d(xq, weight, bias, self.stride, self.padding, self.dilation, self.groups)
        raise RuntimeError(f"unsupported convolution weight shape {tuple(self.dequant_weight.shape)}")


class FakeQuantEmbedding(_QuantBase):
    def __init__(self, source: nn.Embedding, mode: str) -> None:
        super().__init__(mode)
        q, deq = _quantize_embedding(source.weight)
        self.register_buffer("qweight", q)
        self.register_buffer("dequant_weight", deq)
        self.num_embeddings = source.num_embeddings
        self.embedding_dim = source.embedding_dim
        self.padding_idx = source.padding_idx
        self.max_norm = source.max_norm
        self.norm_type = source.norm_type
        self.scale_grad_by_freq = source.scale_grad_by_freq
        self.sparse = source.sparse

    @property
    def weight(self) -> torch.Tensor:
        return self.dequant_weight

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        dtype = self._compute_dtype(self.mode)
        return F.embedding(
            input,
            self.dequant_weight.to(dtype=dtype),
            self.padding_idx,
            self.max_norm,
            self.norm_type,
            self.scale_grad_by_freq,
            self.sparse,
        )


class FakeQuantMHA(_QuantBase):
    """MHA wrapper that feeds quantized projections to PyTorch's reference MHA."""

    def __init__(self, source: nn.MultiheadAttention, mode: str) -> None:
        super().__init__(mode)
        self.inner = source
        self.batch_first = source.batch_first
        self.embed_dim = source.embed_dim
        self.num_heads = source.num_heads
        self._separate = source.in_proj_weight is None
        if source.in_proj_weight is not None:
            q, scale, deq = _quantize_weight(source.in_proj_weight)
            self.register_buffer("q_in_proj_weight", q)
            self.register_buffer("in_proj_scale", scale)
            self.register_buffer("in_proj_weight_deq", deq)
        else:
            self.register_buffer("q_in_proj_weight", None)
            self.register_buffer("in_proj_scale", None)
            self.register_buffer("in_proj_weight_deq", None)
        if source._qkv_same_embed_dim:
            self.register_buffer("q_q_proj_weight", None)
            self.register_buffer("q_k_proj_weight", None)
            self.register_buffer("q_v_proj_weight", None)
            self.register_buffer("q_proj_scale", None)
            self.register_buffer("k_proj_scale", None)
            self.register_buffer("v_proj_scale", None)
            self.register_buffer("q_proj_weight_deq", None)
            self.register_buffer("k_proj_weight_deq", None)
            self.register_buffer("v_proj_weight_deq", None)
        else:
            parts = []
            for name in ("q_proj_weight", "k_proj_weight", "v_proj_weight"):
                weight = getattr(source, name)
                q, scale, deq = _quantize_weight(weight)
                parts.append((q, scale, deq))
            for prefix, (q, scale, deq) in zip(("q", "k", "v"), parts):
                self.register_buffer(f"{prefix}_proj_weight", q)
                self.register_buffer(f"{prefix}_proj_scale", scale)
                self.register_buffer(f"{prefix}_proj_weight_deq", deq)

    def _swap_weights(self, dtype: torch.dtype) -> dict[str, Any]:
        params = self.inner._parameters
        saved: dict[str, Any] = {}
        if self.in_proj_weight_deq is not None:
            saved["in_proj_weight"] = params.get("in_proj_weight")
            params["in_proj_weight"] = self.in_proj_weight_deq.to(dtype=dtype)
        else:
            for name, buf in (
                ("q_proj_weight", self.q_proj_weight_deq),
                ("k_proj_weight", self.k_proj_weight_deq),
                ("v_proj_weight", self.v_proj_weight_deq),
            ):
                saved[name] = params.get(name)
                params[name] = buf.to(dtype=dtype)
        out_params = self.inner.out_proj._parameters
        saved["out_proj.weight"] = out_params.get("weight")
        out_params["weight"] = self._out_proj_weight_deq.to(dtype=dtype)
        return saved

    def _restore_weights(self, saved: dict[str, Any]) -> None:
        for name, value in saved.items():
            if name == "out_proj.weight":
                self.inner.out_proj._parameters["weight"] = value
            else:
                self.inner._parameters[name] = value

    @property
    def _out_proj_weight_deq(self) -> torch.Tensor:
        # The cache is created lazily because the source module is already on
        # its final device when this wrapper is installed.  Do not recompute
        # the projection quantization on every attention call.
        if not hasattr(self, "_cached_out_proj_weight"):
            _q, _scale, deq = _quantize_weight(self.inner.out_proj.weight)
            self.register_buffer("_cached_out_proj_weight", deq)
        return self._cached_out_proj_weight

    def forward(
        self,
        query: torch.Tensor,
        key: torch.Tensor,
        value: torch.Tensor,
        key_padding_mask: torch.Tensor | None = None,
        need_weights: bool = True,
        attn_mask: torch.Tensor | None = None,
        average_attn_weights: bool = True,
        is_causal: bool = False,
    ):
        dtype = self._compute_dtype(self.mode)
        q = self._quant_activation(query).to(dtype=dtype)
        k = self._quant_activation(key).to(dtype=dtype)
        v = self._quant_activation(value).to(dtype=dtype)
        saved = self._swap_weights(dtype)
        try:
            return self.inner(
                q,
                k,
                v,
                key_padding_mask=key_padding_mask,
                need_weights=need_weights,
                attn_mask=attn_mask,
                average_attn_weights=average_attn_weights,
                is_causal=is_causal,
            )
        finally:
            self._restore_weights(saved)


def _replace_modules(root: nn.Module, mode: str, stats: QuantizationStats, prefix: str = "") -> None:
    for name, child in list(root.named_children()):
        full_name = f"{prefix}.{name}" if prefix else name
        replacement: nn.Module | None = None
        if isinstance(child, nn.MultiheadAttention):
            replacement = FakeQuantMHA(child, mode)
            stats.quantized_mha += 1
            stats.quantized_weight_values += int(child.in_proj_weight.numel() if child.in_proj_weight is not None else 0)
            stats.quantized_weight_values += int(child.out_proj.weight.numel())
        elif isinstance(child, nn.Linear):
            replacement = FakeQuantLinear(child, mode)
            stats.quantized_linear += 1
            stats.quantized_weight_values += int(child.weight.numel())
        elif isinstance(child, (nn.Conv1d, nn.Conv2d, nn.Conv3d)):
            replacement = FakeQuantConv(child, mode)
            stats.quantized_conv += 1
            stats.quantized_weight_values += int(child.weight.numel())
        elif isinstance(child, nn.Embedding):
            replacement = FakeQuantEmbedding(child, mode)
            stats.quantized_embedding += 1
            stats.quantized_weight_values += int(child.weight.numel())
        if replacement is not None:
            setattr(root, name, replacement)
        else:
            _replace_modules(child, mode, stats, full_name)


def apply_fake_quant(model: nn.Module, mode: str) -> QuantizationStats:
    mode = _validate_mode(mode)
    if mode == "fp32":
        return QuantizationStats(
            mode=mode,
            weight_bits=32,
            activation_format="FP32",
            activation_bits=None,
            weight_scheme="none",
            unsupported_weight_modules=[],
        )
    stats = QuantizationStats(
        mode=mode,
        weight_bits=8,
        activation_format={"w8a8": "INT8", "w8a16": "INT16", "w8afp16": "FP16"}[mode],
        activation_bits=_activation_bits(mode),
        weight_scheme="symmetric per-output-channel INT8; FP32 bias/normalization",
        unsupported_weight_modules=[],
    )
    _replace_modules(model, mode, stats)
    stats.quantized_weight_bytes = (stats.quantized_weight_values + 1) // 1
    # qweight storage is one byte/value; scales are reported separately so
    # readers can reproduce the logical packed size without claiming a CUDA
    # kernel or a compressed GPU allocator is used by this script.
    stats.fp32_bias_values = int(sum(p.numel() for n, p in model.named_parameters() if n.endswith("bias")))
    return stats


def finalize_model_dtype(model: nn.Module, mode: str) -> torch.dtype:
    mode = _validate_mode(mode)
    if mode == "w8afp16":
        model.half()
        # The released FP32 policy selects BF16 autocast for DINO only.  For
        # this mode we need a genuine FP16 activation path, so disable that
        # context after converting the complete model to half precision.
        vision = getattr(model, "vision_encoder", None)
        if vision is not None and hasattr(vision, "config"):
            vision.config.compute_precision = "fp32"
        return torch.float16
    model.float()
    return torch.float32


def model_quantization_summary(model: nn.Module, stats: QuantizationStats) -> dict[str, Any]:
    return {
        "stats": stats.to_dict(),
        "parameter_count_after_wrapping": int(sum(p.numel() for p in model.parameters())),
        "buffer_count_after_wrapping": int(sum(b.numel() for b in model.buffers())),
        "logical_int8_weight_bytes": int(stats.quantized_weight_bytes),
        "logical_int8_weight_mib": float(stats.quantized_weight_bytes / 2**20),
        "note": "fake quantization on GPU; qweight bytes are logical format accounting, not an INT8 CUDA kernel memory measurement",
    }
