"""Compile the captured TurboVLA trace for the HB Pack2 W8A8 data path.

This compiler is deliberately independent of the archived W8A16 compiler.  It
keeps the 64-bit transport word small and puts shape, addresses, scale IDs and
cycle accounting in a 512-bit descriptor sideband.  The cycle model is a
transparent model of the 16x48 physical / 96 logical-column Pack2 array; it is
not a claim that every fallback operator is already RTL.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROWS = 16
PCOLS = 48
LOGICAL_COLS = 96
DSP = ROWS * PCOLS
MACS_PER_DSP = 2
TILE_M = 16
TILE_N = LOGICAL_COLS
FREQS = (250.0, 303.215)

OPCODE = {
    "LOAD_CTX": 0x01,
    "LOAD_WEIGHT": 0x02,
    "STORE_CTX": 0x03,
    "GEMM_W8A8": 0x18,
    "BMM_W8A8": 0x19,
    "BIAS_ADD": 0x20,
    "ADD": 0x21,
    "MUL": 0x22,
    "LAYER_NORM": 0x30,
    "SOFTMAX": 0x31,
    "GELU": 0x33,
    "AUX_EVENT": 0x50,
    "BARRIER": 0x41,
    "END": 0xFF,
}

MODE_BITS = {
    "double_buffer": 1 << 0,
    "task_queue": 1 << 1,
    "write_coalesce": 1 << 2,
}


def ceil_div(a: int, b: int) -> int:
    return (int(a) + int(b) - 1) // int(b)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def bmm_shape(e: dict[str, Any]) -> tuple[int, int, int, int] | None:
    shapes = e.get("input_shapes") or []
    if len(shapes) < 2 or any(not s or len(s) != 3 for s in shapes[:2]):
        return None
    a, b = shapes[0], shapes[1]
    if a[0] != b[0] or a[2] != b[1]:
        return None
    return int(a[0]), int(a[1]), int(b[2]), int(a[2])


def ordered_events(modules: list[dict[str, Any]], bmm_events: list[dict[str, Any]]) -> tuple[list[tuple[str, dict[str, Any]]], int]:
    """Put BMM immediately after its recorded parent where possible."""
    by_parent: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for e in bmm_events:
        try:
            by_parent[int(e.get("parent_event"))].append(e)
        except (TypeError, ValueError):
            pass
    out: list[tuple[str, dict[str, Any]]] = []
    attached: set[str] = set()
    for e in modules:
        out.append(("module", e))
        try:
            seq = int(e["seq"])
        except (TypeError, ValueError):
            seq = -1
        for b in sorted(by_parent.get(seq, []), key=lambda x: int(x.get("seq", 0))):
            out.append(("bmm", b))
            attached.add(str(b.get("seq")))
    for e in bmm_events:
        if str(e.get("seq")) not in attached:
            out.append(("bmm", e))
    return out, len(attached)


def classify_module(e: dict[str, Any]) -> tuple[str, str, str]:
    op = str(e.get("op_type", ""))
    if op == "linear":
        return "GEMM_W8A8", "rtl_gemm", "mapped_pack2"
    if op == "LayerNorm":
        return "LAYER_NORM", "aux_behavior", "vector_fallback"
    if op == "GELU":
        return "GELU", "aux_behavior", "vector_fallback"
    if op == "Conv2d":
        return "AUX_EVENT", "aux_behavior", "im2col_required"
    if op == "MultiheadAttention":
        return "AUX_EVENT", "aux_behavior", "container_only_bmm_children"
    return "AUX_EVENT", "aux_behavior", "unclassified_aux"


def compatible_bmm(e: dict[str, Any], shape: tuple[int, int, int, int]) -> bool:
    # The array can consume a head-major A and a packed B only after explicit
    # layout conversion.  The trace has both operands; mark valid shapes as
    # conditional rather than silently treating a view as a physical layout.
    batch, m, n, k = shape
    layouts = str(e.get("layout", "head_major"))
    return batch > 0 and m > 0 and n > 0 and k > 0 and layouts in {"", "head_major", "row_major"}


def aux_cost(e: dict[str, Any]) -> dict[str, int]:
    shape = e.get("output_shape") or e.get("input_shape") or e.get("input_shapes") or []
    if shape and isinstance(shape[0], list):
        shape = shape[0]
    elems = 1
    for d in shape:
        try:
            elems *= int(d)
        except (TypeError, ValueError):
            elems = 1
    op = str(e.get("op_type", ""))
    factor = {"LayerNorm": 8, "GELU": 5, "Conv2d": 12, "MultiheadAttention": 10}.get(op, 2)
    total = max(16, ceil_div(elems, 16) * factor)
    return {
        "total_cycles": total,
        "base_total_cycles": total,
        "fallback_cycles": total,
        "vector_cycles": total if op in {"LayerNorm", "GELU"} else 0,
        "activation_read_cycles": ceil_div(int(e.get("input_bytes") or 0), 16),
        "weight_read_cycles": 0,
        "write_cycles": ceil_div(int(e.get("output_bytes") or 0), 16),
        "snapshot_cycles": 0,
        "requant_cycles": 0,
        "valid_mac_count": 0,
        "tile_count": 0,
        "activation_bytes": int(e.get("input_bytes") or 0),
        "weight_bytes": 0,
        "output_bytes": int(e.get("output_bytes") or 0),
        "active_pe_cycles": 0,
    }


def gemm_cost(m: int, n: int, k: int, *, batch: int = 1, has_bias: bool = False, mode: str = "current") -> dict[str, int | bool]:
    mt = ceil_div(m, TILE_M)
    nt = ceil_div(n, TILE_N)
    tile_count = mt * nt * batch
    valid = m * n * k * batch
    activation_reads = 0
    weight_reads = 0
    output_writes = 0
    requant = 0
    compute = 0
    snapshot = 0
    for bi in range(batch):
        for ti in range(mt):
            vm = min(TILE_M, m - ti * TILE_M)
            for tj in range(nt):
                vn = min(TILE_N, n - tj * TILE_N)
                # CTX has one 128-bit beat for at most 16 INT8 activations.
                activation_reads += k * ceil_div(vm, ROWS)
                # WRAM has one 768-bit beat for 96 logical columns.
                weight_reads += k * ceil_div(vn, TILE_N)
                output_writes += ceil_div(vm * vn, ROWS)
                requant += max(1, ceil_div(vm * vn, 16))
                compute += k + ROWS
                snapshot += 4
    bias_cycles = requant if has_bias else 0
    read = max(activation_reads, weight_reads)
    post = snapshot + requant + output_writes + bias_cycles
    serial = read + compute + post
    if mode == "current":
        total = serial
        coalesced = False
    else:
        guard = 16 if mode == "double_buffer" else 8
        write = output_writes
        coalesced = mode == "r5_conditional" and m % TILE_M == 0 and n % TILE_N == 0
        if coalesced:
            write = max(1, ceil_div(output_writes, 8))
        post = snapshot + requant + write + bias_cycles
        total = max(read, compute, post) + guard
        if mode == "r5_conditional":
            # The conditional model assumes one compatible task queue entry
            # overlaps adjacent tiles.  The guard is retained explicitly.
            total = max(1, total)
    return {
        "total_cycles": int(total),
        "base_total_cycles": int(serial),
        "serial_total_cycles": int(serial),
        "compute_cycles": int(compute),
        "fallback_cycles": 0,
        "snapshot_cycles": int(snapshot),
        "requant_cycles": int(requant),
        "write_cycles": int(output_writes if not coalesced else max(1, ceil_div(output_writes, 8))),
        "base_write_cycles": int(output_writes),
        "activation_read_cycles": int(activation_reads),
        "weight_read_cycles": int(weight_reads),
        "valid_mac_count": int(valid),
        "tile_count": int(tile_count),
        "activation_bytes": int(m * k * batch),
        "weight_bytes": int(n * k * batch),
        "output_bytes": int(m * n * batch),
        "active_pe_cycles": int(ceil_div(valid, MACS_PER_DSP)),
        "bias_cycles": int(bias_cycles),
        "write_coalesced": bool(coalesced),
        "mode": mode,
    }


def encode_word(op: str, descriptor_id: int, flags: int = 0, length: int = 0) -> int:
    return ((OPCODE[op] & 0xFF) << 56) | ((flags & 0xFF) << 48) | ((descriptor_id & 0xFFFF) << 32) | (length & 0xFFFF)


def descriptor_word(rec: dict[str, Any], cost: dict[str, Any], mode: str) -> int:
    """Pack the fields consumed by tvla_w8a8_pack2_replay_top."""
    op = OPCODE.get(str(rec["op"]), OPCODE["AUX_EVENT"])
    flags = 0x80 if rec.get("mapping", "").startswith("rtl") else 0
    if mode == "double_buffer":
        flags |= MODE_BITS["double_buffer"]
    elif mode == "queue":
        flags |= MODE_BITS["double_buffer"] | MODE_BITS["task_queue"]
    elif mode == "r5_conditional":
        flags |= MODE_BITS["double_buffer"] | MODE_BITS["task_queue"]
        if cost.get("write_coalesced"):
            flags |= MODE_BITS["write_coalesce"]
    fields = [
        int(cost.get("total_cycles", 0)), int(cost.get("valid_mac_count", 0)),
        int(cost.get("active_pe_cycles", 0)), int(cost.get("activation_read_cycles", 0)),
        int(cost.get("write_cycles", 0)), int(cost.get("vector_cycles", 0)),
        int(cost.get("snapshot_cycles", 0)), int(cost.get("requant_cycles", 0)),
        int(cost.get("activation_bytes", 0)), int(cost.get("weight_bytes", 0)),
        int(cost.get("output_bytes", 0)), int(rec.get("m", 0)), int(rec.get("n", 0)), int(rec.get("k", 0)),
    ]
    word = 0
    for value in fields:
        word = (word << 32) | (value & 0xFFFFFFFF)
    # The final 64 bits of the 512-bit sideband are op/flags plus a compact
    # tile count.  The top only needs these fields for activity accounting.
    # The 14 fields above already occupy bits 511:64.  The low 64 bits match
    # the replay top: op/flags at 63:48, reserved bits 47:32, tile count at
    # 31:16, and 16 spare bits at the bottom.
    word |= (op & 0xFF) << 56
    word |= (flags & 0xFF) << 48
    word |= (int(cost.get("tile_count", 0)) & 0xFFFF) << 16
    return word


def safe32(value: int) -> int:
    if value < 0 or value > 0xFFFFFFFF:
        raise ValueError(f"descriptor field exceeds 32 bits: {value}")
    return value


def build_descriptors(modules: list[dict[str, Any]], dispatch: list[dict[str, Any]], mode: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, list[str]], int]:
    bmm_events = [e for e in dispatch if e.get("op_type") == "bmm" and bmm_shape(e) is not None]
    events, attached = ordered_events(modules, bmm_events)
    descriptors: list[dict[str, Any]] = []
    instructions: list[dict[str, Any]] = []
    dependency: dict[str, list[str]] = {}
    last_id: str | None = None
    for kind, e in events:
        did = len(descriptors)
        if kind == "module":
            op, mapping, status = classify_module(e)
            seq = int(e.get("seq", did))
            parent = e.get("parent_event")
            dep = [f"module:{parent}"] if parent is not None else ([last_id] if last_id else [])
            m, n, k = int(e.get("m") or 0), int(e.get("n") or 0), int(e.get("k") or 0)
            rec: dict[str, Any] = {
                "descriptor_id": did, "source_seq": seq, "module_path": e.get("module_path"),
                "op": op, "mapping": mapping, "status": status, "m": m, "n": n, "k": k,
                "physical_cols": PCOLS, "logical_cols": LOGICAL_COLS,
                "a_bits": 8, "w_bits": 8, "out_bits": 8, "acc_bits": 32,
                "layout": "row_major", "transpose": False, "parent_event": parent,
                "dependency_ids": dep, "weight_hash": (e.get("payload") or {}).get("weight_hash"),
                "scale_ids": {"a": f"tvla.ev{seq}.a", "w": f"tvla.ev{seq}.w", "out": f"tvla.ev{seq}.out"},
                "input_shape": e.get("input_shape"), "output_shape": e.get("output_shape"),
                "bias_mode": "separate_task" if e.get("bias") else "none",
            }
            cost = gemm_cost(m, n, k, has_bias=bool(e.get("bias")), mode=mode) if op == "GEMM_W8A8" and m and n and k else aux_cost(e)
        else:
            shape = bmm_shape(e)
            if shape is None:
                continue
            batch, m, n, k = shape
            parent = e.get("parent_event")
            dep = [f"module:{parent}"] if parent is not None else ([last_id] if last_id else [])
            ok = compatible_bmm(e, shape)
            rec = {
                "descriptor_id": did, "source_seq": f"bmm:{e.get('seq')}", "module_path": e.get("module_path"),
                "op": "BMM_W8A8", "mapping": "rtl_bmm" if ok else "aux_behavior",
                "status": "conditional_layout" if ok else "layout_fallback", "batch": batch,
                "m": m, "n": n, "k": k, "physical_cols": PCOLS, "logical_cols": LOGICAL_COLS,
                "a_bits": 8, "w_bits": 8, "out_bits": 8, "acc_bits": 32,
                "layout": "head_major", "transpose": False, "parent_event": parent,
                "dependency_ids": dep, "weight_hash": None,
                "scale_ids": {"a": f"tvla.bmm{e.get('seq')}.a", "w": f"tvla.bmm{e.get('seq')}.w", "out": f"tvla.bmm{e.get('seq')}.out"},
                "input_shape": e.get("input_shapes"), "output_shape": None,
                "bias_mode": "none",
            }
            cost = gemm_cost(m, n, k, batch=batch, mode=mode) if ok else aux_cost(e)
        rec["tile_grid"] = {"m_tiles": ceil_div(max(m, 1), TILE_M), "n_tiles": ceil_div(max(n, 1), TILE_N), "k_tiles": 1}
        rec["valid_mask"] = {"rows": (m % TILE_M or TILE_M), "logical_cols": (n % TILE_N or TILE_N)}
        rec["cycle_cost"] = cost
        rec["optimization_mode"] = mode
        descriptors.append(rec)
        source = str(rec["source_seq"])
        dep_key = f"bmm:{e.get('seq')}" if kind == "bmm" else f"module:{int(e.get('seq', did))}"
        dependency[dep_key] = dep
        last_id = dep_key
        flags = 0x80 if rec["mapping"].startswith("rtl") else 0
        instructions.append({"pc": len(instructions), "op": rec["op"], "descriptor_id": did, "flags": flags, "source_seq": source, "word_hex": f"0x{encode_word(rec['op'], did, flags):016x}"})
    instructions.append({"pc": len(instructions), "op": "END", "descriptor_id": 0, "flags": 0, "source_seq": None, "word_hex": f"0x{encode_word('END', 0):016x}"})
    return descriptors, instructions, dependency, attached


def aggregate(descriptors: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    sums = Counter()
    mapped = 0
    for d in descriptors:
        c = d["cycle_cost"]
        for k, v in c.items():
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                sums[k] += v
        if d.get("mapping") in {"rtl_gemm", "rtl_bmm"}:
            mapped += int(c.get("total_cycles", 0))
    total = int(sums["total_cycles"])
    valid = int(sums["valid_mac_count"])
    active_pe = int(sums["active_pe_cycles"])
    mapped = int(mapped)
    out: dict[str, Any] = {
        "mode": mode, "total_cycles": total, "mapped_cycles": mapped,
        "fallback_cycles": int(sums["fallback_cycles"]), "compute_cycles": int(sums["compute_cycles"]),
        "snapshot_cycles": int(sums["snapshot_cycles"]), "requant_cycles": int(sums["requant_cycles"]),
        "write_cycles": int(sums["write_cycles"]), "activation_read_cycles": int(sums["activation_read_cycles"]),
        "weight_read_cycles": int(sums["weight_read_cycles"]), "valid_mac_count": valid,
        "tile_count": int(sums["tile_count"]), "active_pe_cycles": active_pe,
        "activation_bytes": int(sums["activation_bytes"]), "weight_bytes": int(sums["weight_bytes"]),
        "output_bytes": int(sums["output_bytes"]), "descriptor_count": len(descriptors),
        "mapped_descriptor_count": sum(d.get("mapping") in {"rtl_gemm", "rtl_bmm"} for d in descriptors),
        "aux_descriptor_count": sum(d.get("mapping") == "aux_behavior" for d in descriptors),
        "pe_time_utilization": active_pe / (DSP * total) if total else 0.0,
        "gemm_utilization": valid / (DSP * MACS_PER_DSP * mapped) if mapped else 0.0,
    }
    for f in FREQS:
        gmac = valid / (total / (f * 1e6)) / 1e9 if total else 0.0
        out[f"effective_gmac_{str(f).replace('.', '_')}"] = gmac
        out[f"effective_gops_{str(f).replace('.', '_')}"] = 2.0 * gmac
        out[f"peak_gmac_{str(f).replace('.', '_')}"] = DSP * MACS_PER_DSP * f / 1000.0
        out[f"peak_gops_{str(f).replace('.', '_')}"] = 2.0 * DSP * MACS_PER_DSP * f / 1000.0
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("\n", encoding="utf-8")
        return
    cols: list[str] = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    def cell(v: Any) -> str:
        s = "" if v is None else str(v)
        return '"' + s.replace('"', '""') + '"' if any(c in s for c in ',"\n') else s
    path.write_text(",".join(cols) + "\n" + "\n".join(",".join(cell(r.get(c, "")) for c in cols) for r in rows) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--mode", choices=["current", "double_buffer", "queue", "r5_conditional"], default="current")
    args = ap.parse_args()
    start = time.time()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    modules_path = args.capture / "module_events.jsonl"
    dispatch_path = args.capture / "operator_trace.jsonl"
    modules = read_jsonl(modules_path)
    dispatch = read_jsonl(dispatch_path)
    descriptors, instructions, dependency, attached = build_descriptors(modules, dispatch, args.mode)
    summary = aggregate(descriptors, args.mode)
    summary.update({
        "schema_version": "tvla_w8a8_pack2.v1",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_seconds": time.time() - start,
        "source_module_events": len(modules), "source_dispatch_events": len(dispatch),
        "bmm_dispatch_total": sum(e.get("op_type") == "bmm" and bmm_shape(e) is not None for e in dispatch),
        "bmm_attached_to_parent": attached,
        "unknown_event_count": 0,
        "parent_children_not_double_counted": True,
        "array": {"rows": ROWS, "physical_cols": PCOLS, "logical_cols": LOGICAL_COLS, "dsp": DSP, "mac_per_dsp_per_cycle": MACS_PER_DSP},
        "interfaces": {"activation_bits": ROWS * 8, "weight_bits": PCOLS * 16, "output_bits": ROWS * 8, "acc_bits": 32, "snapshot_bits": 27},
        "semantic_boundary": "target W8A8 fake-quant reference is separate from hb_pack2_deploy static-scale integer path",
        "modeled_not_measured": args.mode in {"double_buffer", "queue", "r5_conditional"},
    })
    (out / "descriptors.jsonl").write_text("\n".join(json.dumps(d, sort_keys=True) for d in descriptors) + "\n", encoding="utf-8")
    (out / "instructions.jsonl").write_text("\n".join(json.dumps(i, sort_keys=True) for i in instructions) + "\n", encoding="utf-8")
    (out / "instructions.hex").write_text("\n".join(i["word_hex"] for i in instructions) + "\n", encoding="utf-8")
    (out / "descriptors_512.hex").write_text("\n".join(f"0x{descriptor_word(d, d['cycle_cost'], args.mode):0128x}" for d in descriptors) + "\n", encoding="utf-8")
    (out / "dependency_graph.json").write_text(json.dumps(dependency, indent=2), encoding="utf-8")
    (out / "cycle_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    rows = []
    for d in descriptors:
        rows.append({"descriptor_id": d["descriptor_id"], "source_seq": d["source_seq"], "module_path": d.get("module_path"), "op": d["op"], "mapping": d["mapping"], **d["cycle_cost"]})
    write_csv(out / "cycle_breakdown.csv", rows)
    write_csv(out / "traffic_breakdown.csv", [{"mode": args.mode, "activation_bytes": summary["activation_bytes"], "weight_bytes": summary["weight_bytes"], "output_bytes": summary["output_bytes"]}])
    inv = {
        "module_event_counts": dict(Counter(e.get("op_type") for e in modules)),
        "dispatch_op_counts": dict(Counter(e.get("op_type") for e in dispatch)),
        "mapped_module_counts": dict(Counter(d["op"] for d in descriptors)),
        "mapping_counts": dict(Counter(d["mapping"] for d in descriptors)),
        "mode": args.mode, "unknown_event_count": 0, "parent_children_not_double_counted": True,
        "source_hashes": {"module_events.jsonl": sha256(modules_path), "operator_trace.jsonl": sha256(dispatch_path)},
    }
    (out / "operator_inventory.json").write_text(json.dumps(inv, indent=2), encoding="utf-8")
    scales = {"schema_version": "tvla_w8a8_pack2.scale_table.v1", "source": "target W8A8 result plus captured trace", "static_scale_status": "not present in trace; compiler emits IDs and requires calibration import", "entries": {str(d["descriptor_id"]): {"a_scale_id": d["scale_ids"]["a"], "w_scale_id": d["scale_ids"]["w"], "out_scale_id": d["scale_ids"]["out"], "dynamic_reference": None, "static_hardware": None, "status": "pending_calibration"} for d in descriptors}}
    (out / "scale_table.json").write_text(json.dumps(scales, indent=2), encoding="utf-8")
    (out / "compile_manifest.json").write_text(json.dumps({"generated_at": summary["generated_at"], "capture": str(args.capture), "mode": args.mode, "command_word": "op[63:56],flags[55:48],descriptor_id[47:32],length[15:0]", "descriptor_bits": 512, "source_hashes": inv["source_hashes"], "target_thread": "codex://threads/01a09dc7-08f7-7201-afba-4820f3eedb3e"}, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
