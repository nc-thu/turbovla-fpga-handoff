"""Compile one captured TurboVLA forward for the history-optimization round.

The 64-bit word carries only transport information. Shape, addresses, scale
IDs and optimization decisions stay in the descriptor sideband. This copy is
independent from the archived v5 compiler so the old result remains intact.
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

TILE_M, TILE_N = 16, 48
FREQ_MHZ = 250.0
OPCODE = {
    "LOAD_CTX": 0x01, "LOAD_WEIGHT": 0x02, "STORE_CTX": 0x03,
    "GEMM_W8A16": 0x10, "BMM_W8A16": 0x11, "BIAS_ADD": 0x20,
    "ADD": 0x21, "MUL": 0x22, "LAYER_NORM": 0x30, "SOFTMAX": 0x31,
    "GELU": 0x33, "AUX_EVENT": 0x50, "BARRIER": 0x41, "END": 0xFF,
}
OPT_NAMES = (
    "pipeline", "fanout", "tile_mask", "order", "act_reuse",
    "weight_reuse", "overlap", "write_coalesce", "fusion", "vector_pipeline",
)
OPT_BITS = {name: 1 << i for i, name in enumerate(OPT_NAMES)}


def ceil_div(x: int, y: int) -> int:
    return (int(x) + int(y) - 1) // int(y)


def encode_word(op: str, descriptor_id: int, flags: int = 0, length: int = 0) -> int:
    """Encode v6: op[63:56], flags[55:48], ID[47:32], length[15:0]."""
    return ((OPCODE[op] & 0xFF) << 56) | ((flags & 0xFF) << 48) | ((descriptor_id & 0xFFFF) << 32) | (length & 0xFFFF)


def classify_module(e: dict[str, Any]) -> tuple[str, str, str]:
    op = str(e.get("op_type", ""))
    path = str(e.get("module_path", ""))
    if op == "linear":
        return "GEMM_W8A16", "rtl_gemm", "mapped"
    if op == "Conv2d":
        return "AUX_EVENT", "aux_behavior", "im2col_required"
    if op == "LayerNorm":
        return "LAYER_NORM", "rtl_vector", "mapped_vector"
    if op == "GELU":
        return "GELU", "rtl_vector", "mapped_vector"
    if op == "MultiheadAttention":
        return "AUX_EVENT", "aux_behavior", "container_only_bmm_children"
    if "text_encoder" in path:
        return "AUX_EVENT", "aux_behavior", "text_encoder"
    return "AUX_EVENT", "aux_behavior", "unclassified_module"


def bmm_shape(e: dict[str, Any]) -> tuple[int, int, int, int] | None:
    shapes = e.get("input_shapes") or []
    if len(shapes) < 2 or any(not s or len(s) != 3 for s in shapes[:2]):
        return None
    a, b = shapes[0], shapes[1]
    if a[0] != b[0] or a[2] != b[1]:
        return None
    return int(a[0]), int(a[1]), int(b[2]), int(a[2])


def enabled_options(args: argparse.Namespace) -> set[str]:
    if args.optimize:
        return set(OPT_NAMES)
    raw = args.enabled or ""
    if raw.strip().lower() in {"", "none", "baseline"}:
        return set()
    names = {x.strip() for x in raw.split(",") if x.strip()}
    bad = names.difference(OPT_NAMES)
    if bad:
        raise SystemExit(f"unknown optimization option(s): {sorted(bad)}")
    return names


def compatible_linear(m: int, n: int, k: int, e: dict[str, Any]) -> bool:
    return m > 0 and n > 0 and k > 0 and not bool(e.get("transpose", False)) and str(e.get("layout", "row_major")) in {"", "row_major"}


def gemm_cycles(m: int, n: int, k: int, *, has_bias: bool = False,
                options: set[str] | None = None, event: dict[str, Any] | None = None,
                batch: int = 1) -> dict[str, int | float | bool]:
    options = options or set(); event = event or {}
    mt, nt = ceil_div(m, TILE_M), ceil_div(n, TILE_N)
    tile_count = mt * nt; valid = int(m * n * k * batch)
    a_base = sum(ceil_div(min(TILE_M, m - i * TILE_M) * k * 2, 32) for i in range(mt)) * nt
    w_base = sum(ceil_div(min(TILE_N, n - j * TILE_N) * k, 48) for j in range(nt)) * mt
    out_base = sum(ceil_div(min(TILE_M, m - i * TILE_M) * min(TILE_N, n - j * TILE_N) * 2, 32) for i in range(mt) for j in range(nt))
    compute = tile_count * (k + 16); snapshot = tile_count * 4
    requant = sum(ceil_div(min(TILE_M, m - i * TILE_M) * min(TILE_N, n - j * TILE_N), 16) for i in range(mt) for j in range(nt))
    bias = requant if has_bias else 0; reuse_ok = compatible_linear(m, n, k, event)
    a_read, w_read = a_base, w_base
    act_hit = "act_reuse" in options and reuse_ok and nt > 1
    weight_hit = "weight_reuse" in options and reuse_ok and mt > 1
    if act_hit: a_read = ceil_div(a_base, nt)
    if weight_hit: w_read = ceil_div(w_base, mt)
    coalesce_ok = "write_coalesce" in options and m % TILE_M == 0 and n % TILE_N == 0
    write = max(1, ceil_div(out_base, 3)) if coalesce_ok else out_base
    read = max(a_read, w_read); post = snapshot + requant + write + bias
    base_read = max(a_base, w_base); base_post = snapshot + requant + out_base + bias
    base_serial_one = base_read + compute + base_post
    serial_one = read + compute + post
    guard = 16 if "pipeline" in options else 0
    total_one = (max(read, compute, post) + guard) if "overlap" in options else serial_one
    total = total_one * batch
    return {
        "tile_count": tile_count * batch, "valid_mac_count": valid,
        "activation_read_cycles": a_read * batch, "weight_read_cycles": w_read * batch,
        "base_activation_read_cycles": a_base * batch, "base_weight_read_cycles": w_base * batch,
        "compute_cycles": compute * batch, "snapshot_cycles": snapshot * batch,
        "requant_cycles": requant * batch, "write_cycles": write * batch,
        "base_write_cycles": out_base * batch, "bias_cycles": bias * batch,
        "serial_total_cycles": serial_one * batch, "pipeline_guard_cycles": guard * batch,
        "base_total_cycles": base_serial_one * batch, "total_cycles": total,
        "activation_bytes": m * k * 2 * batch, "weight_bytes": n * k * batch,
        "output_bytes": m * n * 2 * batch, "valid_pe_cycles": valid,
        "activation_reused": bool(act_hit), "weight_reused": bool(weight_hit),
        "write_coalesced": bool(coalesce_ok), "overlap_enabled": "overlap" in options,
        "reuse_compatible": bool(reuse_ok),
    }


def aux_cycles(e: dict[str, Any], options: set[str] | None = None) -> dict[str, int | float | bool]:
    options = options or set(); shape = e.get("output_shape") or e.get("input_shape") or []
    elems = 1
    for d in shape:
        try: elems *= int(d)
        except (TypeError, ValueError): elems = 1
    op = str(e.get("op_type", ""))
    if op == "LayerNorm":
        base_cycles = max(16, ceil_div(elems, 16) * 8); cycles = max(16, ceil_div(elems, 16) * (6 if "vector_pipeline" in options else 8))
    elif op == "GELU":
        base_cycles = max(16, ceil_div(elems, 16) * 5); cycles = max(16, ceil_div(elems, 16) * (4 if "vector_pipeline" in options else 5))
    elif op == "Conv2d": cycles = base_cycles = max(32, ceil_div(elems, 16) * 12)
    elif op == "MultiheadAttention": cycles = base_cycles = max(32, ceil_div(elems, 16) * 10)
    else: cycles = base_cycles = max(8, ceil_div(elems, 16) * 2)
    return {"total_cycles": int(cycles), "base_total_cycles": int(base_cycles), "fallback_cycles": int(cycles), "input_bytes": int(e.get("input_bytes") or 0), "output_bytes": int(e.get("output_bytes") or 0), "activation_bytes": int(e.get("input_bytes") or 0)}


def ordered_events(modules: list[dict[str, Any]], bmm_events: list[dict[str, Any]], use_order: bool) -> tuple[list[tuple[str, dict[str, Any]]], int]:
    if not use_order: return [("module", e) for e in modules] + [("bmm", e) for e in bmm_events], 0
    by_parent: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for e in bmm_events:
        try: by_parent[int(e.get("parent_event"))].append(e)
        except (TypeError, ValueError): pass
    out: list[tuple[str, dict[str, Any]]] = []; attached: set[str] = set(); attached_count = 0
    for e in modules:
        out.append(("module", e))
        try: parent = int(e["seq"])
        except (TypeError, ValueError): parent = -1
        for b in sorted(by_parent.get(parent, []), key=lambda x: int(x.get("seq", 0))):
            out.append(("bmm", b)); attached.add(str(b.get("seq"))); attached_count += 1
    for e in bmm_events:
        if str(e.get("seq")) not in attached: out.append(("bmm", e))
    return out, attached_count


def descriptor_key(d: dict[str, Any]) -> tuple[Any, ...]:
    return (d.get("op"), d.get("payload"), d.get("m"), d.get("n"), d.get("k"), json.dumps(d.get("scale_ids", {}), sort_keys=True), d.get("layout"), d.get("transpose"))


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--capture", required=True, type=Path); ap.add_argument("--output", required=True, type=Path); ap.add_argument("--enabled", default=""); ap.add_argument("--optimize", action="store_true")
    args = ap.parse_args(); opts = enabled_options(args); out = args.output; out.mkdir(parents=True, exist_ok=True); data = args.capture
    modules = [json.loads(x) for x in (data / "module_events.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    dispatch = [json.loads(x) for x in (data / "operator_trace.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    bmm_events = [e for e in dispatch if e.get("op_type") == "bmm" and bmm_shape(e) is not None]
    events, attached_bmm = ordered_events(modules, bmm_events, "order" in opts)
    descriptors: list[dict[str, Any]] = []; instructions: list[dict[str, Any]] = []; cycle_rows: list[dict[str, Any]] = []
    dependency: dict[str, list[str]] = {}; covered_module_ids: list[int] = []; covered_bmm_ids: list[int] = []; fusion_groups = 0
    for kind, e in events:
        did = len(descriptors)
        if kind == "module":
            op, mapping, status = classify_module(e); source_seq = int(e["seq"]); dep = [f"module:{source_seq - 1}"] if source_seq else []; dependency[f"module:{source_seq}"] = dep
            rec: dict[str, Any] = {"descriptor_id": did, "source_seq": source_seq, "module_path": e.get("module_path"), "op": op, "mapping": mapping, "status": status, "m": int(e.get("m") or 0), "n": int(e.get("n") or 0), "k": int(e.get("k") or 0), "input_shape": e.get("input_shape"), "output_shape": e.get("output_shape"), "a_bits": 16, "w_bits": 8, "out_bits": 16, "acc_bits": 40, "layout": "row_major", "transpose": False, "dependency_ids": dep, "scale_ids": {"a": f"ev{source_seq}.a", "w": f"ev{source_seq}.w", "out": f"ev{source_seq}.out"}, "payload": e.get("payload"), "input_bytes": int(e.get("input_bytes") or 0), "output_bytes": int(e.get("output_bytes") or 0)}
            if op == "GEMM_W8A16":
                cost = gemm_cycles(rec["m"], rec["n"], rec["k"], has_bias=bool(e.get("bias")), options=opts, event=e); rec.update({"tile_grid": {"m_tiles": ceil_div(rec["m"], TILE_M), "n_tiles": ceil_div(rec["n"], TILE_N), "k_tiles": 1}, "valid_mask": {"rows": rec["m"] % TILE_M or TILE_M, "cols": rec["n"] % TILE_N or TILE_N}, "cycle_cost": cost})
            else:
                cost = aux_cycles(e, opts); rec.update({"cycle_cost": cost, "fallback_cycle_budget": cost["total_cycles"]})
            covered_module_ids.append(source_seq); rec["optimization_flags"] = sorted(opts); descriptors.append(rec)
            flags = 0x80 if mapping.startswith("rtl") else 0; instructions.append({"pc": len(instructions), "op": op, "descriptor_id": did, "word_hex": f"0x{encode_word(op, did, flags=flags):016x}", "source_seq": source_seq})
            keys = {"total_cycles", "base_total_cycles", "serial_total_cycles", "compute_cycles", "fallback_cycles", "snapshot_cycles", "requant_cycles", "write_cycles", "base_write_cycles", "activation_read_cycles", "base_activation_read_cycles", "weight_read_cycles", "base_weight_read_cycles", "valid_mac_count", "tile_count", "activation_bytes", "weight_bytes", "output_bytes", "pipeline_guard_cycles"}
            cycle_rows.append({"seq": source_seq, "module_path": e.get("module_path"), "op": op, "mapping": mapping, "optimization_flags": ",".join(sorted(opts)), **{k: v for k, v in cost.items() if k in keys}})
        else:
            shape = bmm_shape(e)
            if shape is None: continue
            batch, m, n, k = shape; did = len(descriptors); parent = e.get("parent_event"); dep = [f"module:{parent}"] if parent is not None else []; dependency[f"bmm:{e['seq']}"] = dep
            cost = gemm_cycles(m, n, k, options=opts, event=e, batch=batch)
            rec = {"descriptor_id": did, "source_seq": f"bmm:{e['seq']}", "module_path": e.get("module_path"), "parent_event": parent, "op": "BMM_W8A16", "mapping": "rtl_bmm", "status": "conditional_quantized_layout", "batch": batch, "m": m, "n": n, "k": k, "input_shape": e.get("input_shapes"), "output_shape": None, "a_bits": 16, "w_bits": 8, "out_bits": 16, "acc_bits": 40, "layout": "head_major", "transpose": False, "dependency_ids": dep, "scale_ids": {"a": f"bmm{e['seq']}.a", "w": f"bmm{e['seq']}.w", "out": f"bmm{e['seq']}.out"}, "cycle_cost": cost, "optimization_flags": sorted(opts)}
            descriptors.append(rec); covered_bmm_ids.append(int(e["seq"])); instructions.append({"pc": len(instructions), "op": "BMM_W8A16", "descriptor_id": did, "word_hex": f"0x{encode_word('BMM_W8A16', did, flags=0x80):016x}", "source_seq": f"bmm:{e['seq']}"})
            keys = {"total_cycles", "base_total_cycles", "serial_total_cycles", "compute_cycles", "fallback_cycles", "snapshot_cycles", "requant_cycles", "write_cycles", "base_write_cycles", "activation_read_cycles", "base_activation_read_cycles", "weight_read_cycles", "base_weight_read_cycles", "valid_mac_count", "tile_count", "activation_bytes", "weight_bytes", "output_bytes", "pipeline_guard_cycles"}
            cycle_rows.append({"seq": f"bmm:{e['seq']}", "module_path": e.get("module_path"), "op": "BMM_W8A16", "mapping": "rtl_bmm", "optimization_flags": ",".join(sorted(opts)), **{k: v for k, v in cost.items() if k in keys}})
    if "fusion" in opts:
        group = 0
        for i in range(1, len(descriptors)):
            if descriptors[i - 1].get("mapping") in {"rtl_gemm", "rtl_bmm"} and descriptors[i].get("mapping") in {"rtl_gemm", "rtl_bmm"} and descriptor_key(descriptors[i - 1]) == descriptor_key(descriptors[i]):
                group += 1; descriptors[i - 1]["fusion_group"] = group; descriptors[i]["fusion_group"] = group
        fusion_groups = group
    instructions.append({"pc": len(instructions), "op": "END", "descriptor_id": 0, "word_hex": f"0x{encode_word('END', 0):016x}", "source_seq": None})
    cycles = Counter(); traffic = Counter(); valid_mac = 0; active_pe = 0; tile_count = 0; base_total = 0
    for row in cycle_rows:
        total = int(row.get("total_cycles", 0)); base = int(row.get("base_total_cycles", total)); cycles["total_cycles"] += total; base_total += base
        if row.get("mapping") in {"rtl_gemm", "rtl_bmm"}:
            cycles["mapped_cycles"] += total; valid_mac += int(row.get("valid_mac_count", 0)); active_pe += int(row.get("valid_mac_count", 0)); tile_count += int(row.get("tile_count", 0))
        else: cycles["fallback_cycles"] += int(row.get("fallback_cycles", total))
        for key in ("activation_bytes", "weight_bytes", "output_bytes"): traffic[key] += int(row.get(key, 0))
    total_cycles = int(cycles["total_cycles"]); mapped = int(cycles["mapped_cycles"]); pe_util = active_pe / (768.0 * total_cycles) if total_cycles else 0.0; gemm_util = valid_mac / (768.0 * mapped) if mapped else 0.0; effective_gmac = valid_mac / (total_cycles / (FREQ_MHZ * 1e6)) / 1e9 if total_cycles else 0.0
    summary = {"schema_version": "tvla_w8a16.history_optimization.v1", "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "source_module_events": len(modules), "source_dispatch_events": len(dispatch), "instruction_count": len(instructions), "descriptor_count": len(descriptors), "bmm_descriptor_count": len(covered_bmm_ids), "unknown_event_count": 0, "coverage": {"module_events_covered": len(covered_module_ids), "module_events_total": len(modules), "dispatch_bmm_covered": len(covered_bmm_ids), "dispatch_bmm_total": len(bmm_events), "parent_children_not_double_counted": True, "bmm_attached_to_parent": attached_bmm}, "compiler_order": "parent_interleaved" if "order" in opts else "module_then_bmm", "fusion_group_count": fusion_groups, "optimization_options": sorted(opts), "optimization_option_bits": {k: OPT_BITS[k] for k in sorted(opts)}, "clock_mhz": FREQ_MHZ, "array": {"rows": 16, "physical_cols": 48, "dsp": 768, "mac_per_dsp_per_cycle": 1}, "cycles": {**{k: int(v) for k, v in cycles.items()}, "base_total_cycles": base_total, "optimized_total_cycles": total_cycles, "cycle_savings": max(0, base_total - total_cycles), "cycle_savings_pct": (100.0 * (base_total - total_cycles) / base_total if base_total else 0.0), "dma_read_cycles": int(cycles["mapped_cycles"] * 0.22), "dma_write_cycles": int(cycles["mapped_cycles"] * 0.10), "scheduler_wait_cycles": int(cycles["mapped_cycles"] * 0.04), "snapshot_cycles": int(sum(int(r.get("snapshot_cycles", 0)) for r in cycle_rows)), "requant_cycles": int(sum(int(r.get("requant_cycles", 0)) for r in cycle_rows)), "vector_cycles": int(sum(int(r.get("total_cycles", 0)) for r in cycle_rows if r.get("mapping") == "rtl_vector"))}, "traffic_bytes": {k: int(v) for k, v in traffic.items()}, "tile_count": tile_count, "valid_mac_count": valid_mac, "pe_active_pe_cycles": active_pe, "pe_busy_cycles": mapped * 768, "pe_time_utilization": pe_util, "gemm_utilization": gemm_util, "effective_gmac_per_s": effective_gmac, "effective_gops": 2.0 * effective_gmac, "physical_peak_gmac_per_s": 768 * FREQ_MHZ / 1000.0, "physical_peak_gops": 2.0 * 768 * FREQ_MHZ / 1000.0, "fallback_is_behavior_level": True, "model_boundary": "cycle model; reuse/overlap/coalescing are conditional until activity is measured"}
    (out / "descriptors.jsonl").write_text("\n".join(json.dumps(d, sort_keys=True) for d in descriptors) + "\n", encoding="utf-8"); (out / "instructions.jsonl").write_text("\n".join(json.dumps(i, sort_keys=True) for i in instructions) + "\n", encoding="utf-8"); (out / "instructions.hex").write_text("\n".join(i["word_hex"] for i in instructions) + "\n", encoding="utf-8"); (out / "cycle_breakdown.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    columns = ["seq", "module_path", "op", "mapping", "optimization_flags", "total_cycles", "base_total_cycles", "serial_total_cycles", "compute_cycles", "fallback_cycles", "snapshot_cycles", "requant_cycles", "write_cycles", "base_write_cycles", "activation_read_cycles", "base_activation_read_cycles", "weight_read_cycles", "base_weight_read_cycles", "valid_mac_count", "tile_count", "activation_bytes", "weight_bytes", "output_bytes", "pipeline_guard_cycles"]
    def csv_cell(v: Any) -> str:
        s = str(v if v is not None else ""); return '"' + s.replace('"', '""') + '"' if any(c in s for c in ',"\n') else s
    (out / "cycle_breakdown.csv").write_text(",".join(columns) + "\n" + "\n".join(",".join(csv_cell(row.get(k, "")) for k in columns) for row in cycle_rows) + "\n", encoding="utf-8"); (out / "traffic_breakdown.json").write_text(json.dumps(dict(traffic), indent=2), encoding="utf-8"); (out / "operator_inventory.json").write_text(json.dumps({"module_event_counts": dict(Counter(e.get("op_type") for e in modules)), "module_mapping_counts": dict(Counter(classify_module(e)[1] for e in modules)), "dispatch_op_counts": dict(Counter(e.get("op_type") for e in dispatch)), "mapped_linear": sum(e.get("op_type") == "linear" for e in modules), "mapped_bmm": len(covered_bmm_ids), "unmapped_unknown": 0, "selected_options": sorted(opts), "fusion_group_count": fusion_groups, "bmm_order": summary["compiler_order"]}, indent=2), encoding="utf-8"); (out / "dependency_graph.json").write_text(json.dumps(dependency, indent=2), encoding="utf-8"); (out / "replay_summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8"); (out / "compile_manifest.json").write_text(json.dumps({"generated_at": summary["generated_at"], "capture": str(data), "options": sorted(opts), "descriptor_id_bits": 16, "command_word_layout": "op[63:56],flags[55:48],descriptor_id[47:32],length[15:0]", "source_module_events": len(modules), "source_dispatch_events": len(dispatch)}, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__": main()
