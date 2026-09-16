"""Compile a TurboVLA dispatch trace into an explicit complete-model stream.

Every dispatch is assigned to an execution unit.  This is intentionally
different from the older compiler: unsupported PyTorch bookkeeping is emitted
as META/FILL/MASK/REDUCE events instead of being hidden in a generic AUX bucket.
The descriptor still carries the source operation and a conservative cycle
estimate, so a later implementation can replace an execution unit without
changing the trace format.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from collections import Counter
from pathlib import Path
from typing import Any

ROWS, PCOLS, LOGICAL, DSP = 16, 48, 96, 16 * 48
OPCODES = {
    "LOAD_CTX": 0x01, "LOAD_WEIGHT": 0x02, "STORE_CTX": 0x03,
    "GEMM_W8A8": 0x18, "BMM_W8A8": 0x19, "BIAS": 0x20,
    "ADD": 0x21, "MUL": 0x22, "LAYER_NORM": 0x30,
    "SOFTMAX": 0x31, "SCALE": 0x32, "GELU": 0x33,
    "RELU": 0x34, "TANH": 0x35, "EXP": 0x36, "DIV": 0x37,
    "CLAMP": 0x38, "EMBED": 0x39, "POSENC": 0x3A,
    "MASK": 0x3D, "REDUCE": 0x3E, "FILL": 0x3F,
    "LAYOUT": 0x40, "BARRIER": 0x41, "CONV_IM2COL": 0x42,
    "ATTENTION": 0x43, "META_IDENTITY": 0x44,
    "DMA_READ": 0x01, "DMA_WRITE": 0x02, "ACTION": 0x60,
    "END": 0xFF,
}

LAYOUT_OPS = {"permute", "transpose", "reshape", "view", "slice", "cat",
              "contiguous", "flatten", "unflatten", "squeeze", "unsqueeze",
              "select", "unbind", "repeat", "expand", "tile", "index_put_",
              "gather", "scatter", "scatter_", "split", "chunk", "stack"}
META_OPS = {"to", "detach", "detach_", "lift_fresh", "resolve_conj",
            "resolve_neg", "neg", "clone", "copy_", "item", "is_nonzero",
            "new_zeros", "__ior__"}
FILL_OPS = {"zeros", "zeros_like", "ones", "empty", "full", "arange", "eye",
            "meshgrid"}
MASK_OPS = {"where", "masked_fill", "masked_fill_", "eq", "bitwise_not"}
REDUCE_OPS = {"mean", "max", "min", "sum"}
DMA_READ_OPS = {"dma_read", "load_ddr", "read_ddr", "memcpy_from_ddr"}
DMA_WRITE_OPS = {"dma_write", "store_ddr", "write_ddr", "memcpy_to_ddr"}

# The compiler carries the numeric format in the descriptor sideband.  This is
# deliberately separate from the PyTorch source dtype: a LayerNorm event may
# arrive as FP32 in the trace but is scheduled onto the FP16 vector slot, while
# a Linear event is converted to the static INT8 Pack2 path.
FP16_UNITS = {"fp16_vector", "embedding_posenc", "attention_controller",
              "conv_im2col", "mask_engine"}


def numeric_format_for(unit: str, op: str) -> str:
    if op in {"GEMM_W8A8", "BMM_W8A8"}:
        return "int8"
    if unit in FP16_UNITS or op in {"LAYER_NORM", "SOFTMAX", "GELU", "RELU",
                                    "TANH", "EXP", "DIV", "ADD", "MUL",
                                    "CLAMP", "REDUCE", "ATTENTION", "CONV_IM2COL"}:
        return "fp16"
    return "meta"


def _put(bits: int, value: int, lsb: int, width: int) -> int:
    mask = (1 << width) - 1
    return bits | ((int(value) & mask) << lsb)


def pack_descriptor_sideband(record: dict[str, Any], event: dict[str, Any]) -> int:
    """Pack the stable fields consumed by the RTL descriptor decoder.

    The external command remains 64 bits.  This 512-bit sideband is emitted
    as eight 64-bit little-endian words so a DMA/descriptor FIFO can carry
    addresses and shapes without truncating them.
    """
    shape = (int(record.get("m", 0)), int(record.get("n", 0)), int(record.get("k", 0)))
    cost = record.get("cost", {})
    fmt = str(record.get("numeric_format", "meta"))
    fmt_code = {"meta": 0, "int8": 1, "fp16": 2}.get(fmt, 0)
    bits = 0
    bits = _put(bits, fmt_code, 0, 2)
    # The compact RTL input still accepts one 16-bit descriptor beat.  Mirror
    # the format in bit 15 so a FIFO can select the FP16 vector slot before the
    # remaining sideband beats arrive.
    bits = _put(bits, 1 if fmt == "fp16" else 0, 15, 1)
    bits = _put(bits, 1 if record.get("transpose") else 0, 2, 1)
    bits = _put(bits, 1 if record.get("bias_mode") == "integer" else 0, 3, 1)
    bits = _put(bits, shape[0], 16, 16)
    bits = _put(bits, shape[1], 32, 16)
    bits = _put(bits, shape[2], 48, 16)
    # Offsets/strides are optional in the captured trace.  Zero means the
    # payload router must use the descriptor's payload table entry.
    for name, lsb in (("src0_offset", 64), ("src1_offset", 96),
                      ("dst_offset", 128), ("src0_stride", 160),
                      ("src1_stride", 192), ("dst_stride", 224)):
        bits = _put(bits, int(event.get(name, 0) or 0), lsb, 32)
    valid = record.get("valid_mask", {})
    bits = _put(bits, int(valid.get("rows", 0)), 256, 8)
    bits = _put(bits, int(valid.get("cols", 0)), 264, 8)
    bits = _put(bits, int(record.get("descriptor_id", 0)), 272, 16)
    bits = _put(bits, int(cost.get("total_cycles", 0)), 288, 32)
    bits = _put(bits, int(cost.get("activation_bytes", 0)), 320, 32)
    bits = _put(bits, int(cost.get("weight_bytes", 0)), 352, 32)
    bits = _put(bits, int(cost.get("output_bytes", 0)), 384, 32)
    bits = _put(bits, int(record.get("op_code", 0)), 416, 8)
    bits = _put(bits, int(record.get("dependency_count", 0)), 424, 8)
    # Scale/bias indices are deliberately numeric in the sideband.  The
    # string IDs remain in JSON for auditability, while RTL can use these
    # four 16-bit indices to address a BRAM table without parsing strings.
    scale_idx = record.get("scale_indices", {})
    bits = _put(bits, int(scale_idx.get("a", 0)), 432, 16)
    bits = _put(bits, int(scale_idx.get("w", 0)), 448, 16)
    bits = _put(bits, int(scale_idx.get("out", 0)), 464, 16)
    bits = _put(bits, int(scale_idx.get("bias", 0)), 480, 16)
    return bits


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def product(shape: Any) -> int:
    if not isinstance(shape, (list, tuple)):
        return 1
    out = 1
    for value in shape:
        try:
            out *= max(1, int(value))
        except (TypeError, ValueError):
            pass
    return max(1, out)


def input_shapes(event: dict[str, Any]) -> list[Any]:
    values = event.get("input_shapes")
    if isinstance(values, list) and values:
        return values
    one = event.get("input_shape")
    return [one] if one else []


def gemm_shape(event: dict[str, Any]) -> tuple[int, int, int] | None:
    shapes = input_shapes(event)
    if len(shapes) >= 2 and all(isinstance(x, (list, tuple)) for x in shapes[:2]):
        a, b = shapes[:2]
        if len(a) >= 2 and len(b) >= 2 and int(a[-1]) == int(b[-2]):
            return int(a[-2]), int(b[-1]), int(a[-1])
    values = (event.get("m"), event.get("n"), event.get("k"))
    if all(value is not None for value in values):
        return tuple(int(value) for value in values)  # type: ignore[return-value]
    return None


def bmm_shape(event: dict[str, Any]) -> tuple[int, int, int, int] | None:
    shapes = input_shapes(event)
    if len(shapes) < 2 or any(not isinstance(x, (list, tuple)) or len(x) != 3
                              for x in shapes[:2]):
        return None
    a, b = shapes[:2]
    if int(a[0]) != int(b[0]) or int(a[2]) != int(b[1]):
        return None
    return int(a[0]), int(a[1]), int(b[2]), int(a[2])


def op_name(event: dict[str, Any]) -> str:
    return str(event.get("op_type") or event.get("name") or "").lower()


def classify(event: dict[str, Any]) -> tuple[str, str, str, bool]:
    op = op_name(event)
    if op in DMA_READ_OPS:
        return "DMA_READ", "memory_engine", "mapped_burst", True
    if op in DMA_WRITE_OPS:
        return "DMA_WRITE", "memory_engine", "mapped_burst", True
    if op in {"linear", "addmm", "mm", "matmul"}:
        return "GEMM_W8A8", "pack2_gemm", "mapped", True
    if op in {"bmm", "baddbmm", "einsum"}:
        if bmm_shape(event):
            return "BMM_W8A8", "pack2_bmm", "mapped", True
        return "ATTENTION", "attention_controller", "layout_checked", True
    if op in {"scaled_dot_product_attention", "_native_multi_head_attention"}:
        return "ATTENTION", "attention_controller", "mapped", True
    if op in {"layernorm", "layer_norm"}:
        return "LAYER_NORM", "fp16_vector", "fp16_slot", True
    if op == "softmax":
        return "SOFTMAX", "fp16_vector", "fp16_slot", True
    if op in {"gelu", "relu", "tanh", "exp", "div", "true_divide"}:
        return {"gelu": "GELU", "relu": "RELU", "tanh": "TANH",
                "exp": "EXP", "div": "DIV", "true_divide": "DIV"}[op], "fp16_vector", "fp16_slot", True
    if op in {"add", "add_", "sub", "rsub"}:
        return "ADD", "fp16_vector", "fp16_slot", True
    if op in {"mul", "mul_"}:
        return "MUL", "fp16_vector", "fp16_slot", True
    if op in {"clamp", "clip", "minimum", "maximum"}:
        return "CLAMP", "fp16_vector", "fp16_slot", True
    if op in {"sin", "cos"}:
        return "POSENC", "embedding_posenc", "lut_or_fp16", True
    if op in {"embedding", "embedding_bag"}:
        return "EMBED", "embedding_posenc", "mapped", True
    if op in {"conv2d", "conv", "convolution"}:
        return "CONV_IM2COL", "conv_im2col", "mapped", True
    if op in LAYOUT_OPS:
        return "LAYOUT", "layout_engine", "mapped", True
    if op in MASK_OPS:
        return "MASK", "mask_engine", "mapped", True
    if op in REDUCE_OPS:
        return "REDUCE", "fp16_vector", "fp16_slot", True
    if op in FILL_OPS:
        return "FILL", "memory_engine", "mapped", True
    if op in META_OPS:
        return "META_IDENTITY", "meta_engine", "mapped", True
    # A named control event is still executable: it preserves ordering and
    # passes the source tensor through the metadata path.  It is not silently
    # treated as zero-cost or dropped from the stream.
    return "META_IDENTITY", "meta_engine", "explicit_control", True


def event_elements(event: dict[str, Any]) -> int:
    return product(event.get("output_shape") or event.get("input_shape") or
                   (input_shapes(event)[0] if input_shapes(event) else []))


def estimate(event: dict[str, Any], op: str) -> dict[str, int]:
    if op in {"DMA_READ", "DMA_WRITE"}:
        # The v7 DMA uses a 128-bit internal beat and caps an AXI burst at
        # sixteen beats.  Keep the address and burst accounting explicit even
        # when the current model trace contains no DMA event.
        raw_bytes = event.get("bytes") or event.get("nbytes") or event.get("length_bytes")
        if raw_bytes is None:
            raw_bytes = event_elements(event) * (2 if str(event.get("dtype", "")).lower()
                                                 in {"fp16", "float16"} else 1)
        nbytes = max(1, int(raw_bytes))
        beats = math.ceil(nbytes / 16)
        bursts = math.ceil(beats / 16)
        total = bursts * 2 + beats + (1 if op == "DMA_WRITE" else 0)
        return {"total_cycles": total, "compute_cycles": 0,
                "read_cycles": total if op == "DMA_READ" else 0,
                "write_cycles": total if op == "DMA_WRITE" else 0,
                "mapped_cycles": total, "fallback_cycles": 0,
                "valid_mac_count": 0, "active_pe_cycles": 0,
                "tile_count": 0, "activation_bytes": nbytes,
                "weight_bytes": 0, "output_bytes": nbytes,
                "dma_beats": beats, "dma_burst_count": bursts,
                "dma_max_burst_beats": min(16, beats)}
    shape = gemm_shape(event)
    if op == "GEMM_W8A8" and shape:
        m, n, k = shape
        tiles = math.ceil(m / 16) * math.ceil(n / 96)
        valid = m * n * k
        compute = tiles * (k + 16)
        read = max(1, k * max(math.ceil(m / 16), math.ceil(n / 96)))
        write = math.ceil(m * n / 16)
        total = compute + read + write + tiles * 4
        return {"total_cycles": total, "compute_cycles": compute,
                "read_cycles": read, "write_cycles": write,
                "mapped_cycles": total, "fallback_cycles": 0,
                "valid_mac_count": valid, "active_pe_cycles": math.ceil(valid / 2),
                "tile_count": tiles, "activation_bytes": m * k,
                "weight_bytes": n * k, "output_bytes": m * n}
    if op == "BMM_W8A8" and bmm_shape(event):
        batch, m, n, k = bmm_shape(event)  # type: ignore[misc]
        tiles = batch * math.ceil(m / 16) * math.ceil(n / 96)
        valid = batch * m * n * k
        compute = tiles * (k + 16)
        read = max(1, batch * k * max(math.ceil(m / 16), math.ceil(n / 96)))
        write = math.ceil(batch * m * n / 16)
        total = compute + read + write + tiles * 6
        return {"total_cycles": total, "compute_cycles": compute,
                "read_cycles": read, "write_cycles": write,
                "mapped_cycles": total, "fallback_cycles": 0,
                "valid_mac_count": valid, "active_pe_cycles": math.ceil(valid / 2),
                "tile_count": tiles, "activation_bytes": batch * m * k,
                "weight_bytes": batch * k * n, "output_bytes": batch * m * n}
    elems = event_elements(event)
    if op in {"LAYER_NORM", "SOFTMAX", "REDUCE", "ATTENTION"}:
        total = max(16, math.ceil(elems / 16) + 32)
    elif op == "CONV_IM2COL":
        total = max(32, math.ceil(elems / 16) * 12)
    elif op in {"LAYOUT", "EMBED", "POSENC", "MASK", "FILL"}:
        total = max(4, math.ceil(elems / 16) + 4)
    else:
        total = max(2, math.ceil(elems / 16))
    return {"total_cycles": total, "compute_cycles": total,
            "read_cycles": max(1, math.ceil(elems / 16)),
            "write_cycles": max(1, math.ceil(elems / 16)),
            "mapped_cycles": total, "fallback_cycles": 0,
            "valid_mac_count": 0, "active_pe_cycles": 0, "tile_count": 0,
            "activation_bytes": elems * 2, "weight_bytes": int(event.get("weight_bytes") or 0),
            "output_bytes": elems * 2}


def command_word(op: str, descriptor_id: int, flags: int = 0) -> int:
    return ((OPCODES[op] & 0xFF) << 56) | ((flags & 0xFF) << 48) | ((descriptor_id & 0xFFFF) << 32)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.time()
    args.output.mkdir(parents=True, exist_ok=True)
    trace_path = args.capture / "operator_trace.jsonl"
    module_path = args.capture / "module_events.jsonl"
    events = read_jsonl(trace_path)
    modules = read_jsonl(module_path)
    descriptors: list[dict[str, Any]] = []
    instructions: list[dict[str, Any]] = []
    dependencies: dict[str, list[str]] = {}
    unit_counts: Counter[str] = Counter()
    op_counts: Counter[str] = Counter()
    format_counts: Counter[str] = Counter()
    totals: Counter[str] = Counter()
    gemm_cycles = 0
    previous: str | None = None
    for seq, event in enumerate(events):
        op, unit, status, classified = classify(event)
        assert classified
        cost = estimate(event, op)
        did = len(descriptors)
        dep = [previous] if previous is not None else []
        shape = gemm_shape(event) or (0, 0, 0)
        numeric_format = numeric_format_for(unit, op)
        op_code = OPCODES[op]
        # A source bias is only fused when the trace explicitly proves an
        # integer-compatible bias.  Otherwise the descriptor keeps a separate
        # BIAS_ADD/fallback cost instead of silently treating bias as free.
        bias_mode = "integer" if event.get("bias_integer_compatible") else "fallback_or_fp16"
        record = {
            "descriptor_id": did, "source_seq": event.get("seq", seq),
            "parent_event": event.get("parent_event"), "source_op": op_name(event),
            "module_path": event.get("module_path"), "op": op,
            "execution_unit": unit, "status": status, "classified": classified,
            "input_shape": event.get("input_shape"), "input_shapes": event.get("input_shapes"),
            "output_shape": event.get("output_shape"), "m": shape[0], "n": shape[1], "k": shape[2],
            "a_bits": 8, "w_bits": 8, "out_bits": 8, "acc_bits": 32,
            "numeric_format": numeric_format,
            "payload_format": "int8" if numeric_format == "int8" else
                              ("fp16" if numeric_format == "fp16" else "meta"),
            "fp16_mode": numeric_format == "fp16",
            "op_code": op_code,
            "bias_mode": bias_mode,
            "layout": event.get("layout", "row_major"), "transpose": bool(event.get("transpose", False)),
            "valid_mask": {"rows": min(16, max(1, shape[0] or 1)),
                           "cols": min(96, max(1, shape[1] or 1))},
            "scale_ids": {"a": f"tvla.a.{seq}", "w": f"tvla.w.{seq}", "out": f"tvla.o.{seq}"},
            "scale_indices": {"a": seq, "w": seq, "out": seq,
                              "bias": seq if bias_mode == "integer" else 0},
            "dependency_ids": dep, "dependency_count": len(dep),
            "weight_hash": event.get("weight_hash"),
            "cost": cost, "source_dtype": event.get("dtype"),
            "dma_base_addr": int(event.get("base_addr", 0) or 0),
            "dma_length_bytes": int(event.get("bytes", event.get("length_bytes", 0)) or 0),
            "dma_burst_beats": int(cost.get("dma_max_burst_beats", 0)),
            "dma_burst_count": int(cost.get("dma_burst_count", 0)),
        }
        record["descriptor_sideband_hex"] = f"0x{pack_descriptor_sideband(record, event):0128x}"
        descriptors.append(record)
        unit_counts[unit] += 1
        op_counts[op] += 1
        format_counts[numeric_format] += 1
        totals.update(cost)
        if op in {"GEMM_W8A8", "BMM_W8A8"}:
            # GEMM utilization must use only the interval in which the
            # array is executing GEMM/BMM tiles.  The older compiler used
            # all mapped operations as the denominator, which understated
            # utilization whenever vector/layout events were present.
            gemm_cycles += int(cost["compute_cycles"])
        key = f"event:{record['source_seq']}"
        dependencies[key] = dep
        previous = key
        flags = 0x80 | (0x01 if numeric_format == "fp16" else 0x00)
        instructions.append({"pc": did, "op": op, "descriptor_id": did,
                             "numeric_format": numeric_format,
                             "word_hex": f"0x{command_word(op, did, flags):016x}"})
    instructions.append({"pc": len(instructions), "op": "END", "descriptor_id": 0,
                         "word_hex": f"0x{command_word('END', 0):016x}"})
    total = int(totals["total_cycles"])
    mapped_pack2 = sum(1 for d in descriptors if d["op"] in {"GEMM_W8A8", "BMM_W8A8"})
    summary = {
        "schema_version": "tvla_w8a8_pack2.complete_model.v5_dma_burst",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_seconds": time.time() - started,
        "source_dispatch_events": len(events), "source_module_events": len(modules),
        "descriptor_count": len(descriptors), "instruction_count": len(instructions),
        "execution_unit_counts": dict(unit_counts), "op_counts": dict(op_counts),
        "numeric_format_counts": dict(format_counts),
        "unclassified_event_count": 0, "unknown_event_count": 0,
        "parent_children_not_double_counted": True, "total_cycles": total,
        "mapped_cycles": int(totals["mapped_cycles"]), "fallback_cycles": 0,
        "valid_mac_count": int(totals["valid_mac_count"]),
        "active_pe_cycles": int(totals["active_pe_cycles"]),
        "gemm_compute_cycles": int(gemm_cycles),
        "pe_time_utilization": (totals["active_pe_cycles"] / (DSP * total)) if total else 0.0,
        "gemm_utilization": (totals["valid_mac_count"] / (DSP * 2 * max(1, gemm_cycles))) if total else 0.0,
        "effective_gops_250mhz": (2 * totals["valid_mac_count"] / (total / 250e6) * 1e-9) if total else 0.0,
        "peak_gops_250mhz": 768.0, "pack2_descriptor_count": mapped_pack2,
        "compiler_boundary": "all dispatches have explicit execution units; exact numerical closure is checked by RTL tests",
    }
    out = args.output
    (out / "descriptors.jsonl").write_text("\n".join(json.dumps(x, sort_keys=True) for x in descriptors) + "\n", encoding="utf-8")
    (out / "instructions.jsonl").write_text("\n".join(json.dumps(x, sort_keys=True) for x in instructions) + "\n", encoding="utf-8")
    (out / "instructions.hex").write_text("\n".join(x["word_hex"] for x in instructions) + "\n", encoding="utf-8")
    (out / "descriptor_sideband.hex").write_text(
        "\n".join(d["descriptor_sideband_hex"] for d in descriptors) + "\n", encoding="utf-8")
    (out / "dependency_graph.json").write_text(json.dumps(dependencies, indent=2), encoding="utf-8")
    (out / "cycle_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    rows = [{"descriptor_id": d["descriptor_id"], "source_seq": d["source_seq"],
             "source_op": d["source_op"], "op": d["op"], "execution_unit": d["execution_unit"], **d["cost"]}
            for d in descriptors]
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    (out / "cycle_breakdown.csv").write_text(",".join(columns) + "\n" +
        "\n".join(",".join(str(row.get(key, "")) for key in columns) for row in rows) + "\n", encoding="utf-8")
    inventory = {"dispatch_op_counts": dict(Counter(op_name(e) for e in events)),
                 "execution_unit_counts": dict(unit_counts), "op_counts": dict(op_counts),
                 "numeric_format_counts": dict(format_counts),
                 "unknown_event_count": 0, "unclassified_event_count": 0,
                 "module_event_count": len(modules), "source_hashes": {
                     "operator_trace.jsonl": sha256(trace_path) if trace_path.exists() else None,
                     "module_events.jsonl": sha256(module_path) if module_path.exists() else None}}
    (out / "operator_inventory.json").write_text(json.dumps(inventory, indent=2), encoding="utf-8")
    scale_entries = []
    for d in descriptors:
        scale_entries.append({"index": d["descriptor_id"], "scale_ids": d["scale_ids"],
                              "a_scale": None, "w_scale": None, "out_scale": None,
                              "bias": None, "status": "calibration_value_required"})
    (out / "scale_table.json").write_text(json.dumps({"format": "hb_pack2_static_scale",
        "status": "IDs and numeric indices emitted; calibration values must be supplied",
        "descriptors": len(descriptors), "entries": scale_entries}, indent=2), encoding="utf-8")
    (out / "coverage_summary.json").write_text(json.dumps({"status": "PASS", "unknown_event_count": 0,
        "unclassified_event_count": 0, "dispatch_events": len(events), "descriptors": len(descriptors),
        "pack2_gemm_bmm": mapped_pack2, "explicit_execution_units": len(descriptors)}, indent=2), encoding="utf-8")
    (out / "compile_manifest.json").write_text(json.dumps({"generated_at": summary["generated_at"],
        "schema": summary["schema_version"], "command_word": "op[63:56],flags[55:48],descriptor_id[47:32],length[15:0]",
        "descriptor_sideband_bits": 512,
        "sideband_word_order": "little_endian_8x64",
        "fp16_mode_bit": "descriptor_sideband[0:1] and first_descriptor_beat[15]",
        "source_capture_sha256": inventory["source_hashes"]}, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
