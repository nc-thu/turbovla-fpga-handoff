"""TurboVLA W8A16 16×48 cycle and traffic model.

This is a transparent tile model, not a claim that a full system has already
been integrated.  It includes feed, drain, requant and writeback events so
that the array utilization denominator is not silently reduced to MAC time.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ARCH = ROOT / "arch" / "v2_2026-09-13_1113_w8a16_camera_ready_model"
ARCH.mkdir(parents=True, exist_ok=True)


ROWS = 16
COLS = 48
DSP = ROWS * COLS


def tile_cycles(m: int, n: int, k: int, *, a_bytes: int = 2, w_bytes: int = 1,
                out_bytes: int = 2, ctx_read_bytes_per_cycle: int = 32,
                w_read_bytes_per_cycle: int = 48,
                ctx_write_bytes_per_cycle: int = 32) -> dict[str, Any]:
    if min(m, n, k) <= 0:
        raise ValueError("M/N/K must be positive")
    mt = math.ceil(m / ROWS)
    nt = math.ceil(n / COLS)
    # One full wavefront cycle consumes one K slice.  A matrix larger than the
    # physical array is serialized as mt*nt tiles.  We charge activation and
    # weight traffic per tile: without a proven on-chip reuse path, an
    # activation block is read again for each output-column tile and a weight
    # block is read again for each output-row tile.
    feed = k + ROWS - 1
    drain = COLS - 1
    compute_per_tile = feed + drain
    tile_count = mt * nt
    compute_total = tile_count * compute_per_tile
    a_bytes_total = m * k * a_bytes
    w_bytes_total = k * n * w_bytes
    out_bytes_total = m * n * out_bytes
    a_stream_bytes = tile_count * min(m, ROWS) * k * a_bytes
    w_stream_bytes = tile_count * k * min(n, COLS) * w_bytes
    read_a = math.ceil(a_stream_bytes / ctx_read_bytes_per_cycle)
    read_w = math.ceil(w_stream_bytes / w_read_bytes_per_cycle)
    write = math.ceil(out_bytes_total / ctx_write_bytes_per_cycle)
    # A row select/clear is charged once per valid output row in each tile.
    snapshot = tile_count * min(m, ROWS)
    # Requantization is modeled as one 256-bit result group per cycle.  This is
    # a capacity model, not a claim about a finished requantizer pipeline.
    requant = math.ceil(out_bytes_total / ctx_write_bytes_per_cycle)
    overlapped_front = max(compute_total, read_a, read_w)
    total = overlapped_front + snapshot + requant + write
    macs = m * n * k
    peak_compute = DSP * compute_total
    peak_completion = DSP * total
    return {
        "m": m, "n": n, "k": k, "rows": ROWS, "logical_cols": COLS,
        "dsp": DSP, "tiles_m": mt, "tiles_n": nt, "tile_count": tile_count,
        "macs": macs, "compute_cycles_per_tile": compute_per_tile,
        "compute_cycles": compute_total, "read_activation_cycles": read_a,
        "read_weight_cycles": read_w, "snapshot_cycles": snapshot,
        "requant_cycles": requant, "writeback_cycles": write,
        "total_cycles": total,
        "engine_utilization": macs / peak_compute if peak_compute else 0.0,
        "completion_rate": macs / peak_completion if peak_completion else 0.0,
        "a_bytes": a_bytes_total, "w_bytes": w_bytes_total,
        "out_bytes": out_bytes_total, "stream_a_bytes": a_stream_bytes,
        "stream_w_bytes": w_stream_bytes,
        "note": "one INT16×INT8 product per DSP; 48 logical columns",
    }


def representative_shapes() -> list[tuple[str, int, int, int]]:
    return [
        ("vision_projection", 256, 1024, 768),
        ("fusion_ffn", 21, 2048, 256),
        ("fusion_projection", 256, 256, 1024),
        ("action_decoder_ffn", 12, 2048, 256),
        ("action_projection", 12, 7, 512),
        ("short_k_tail", 16, 17, 32),
    ]


def build() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, m, n, k in representative_shapes():
        r = tile_cycles(m, n, k)
        r["name"] = name
        rows.append(r)
    (DATA / "cycle_breakdown.json").write_text(json.dumps({"schema_version": "tvla_w8a16.cycles.v1", "rows": rows}, indent=2), encoding="utf-8")
    with (DATA / "cycle_breakdown.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    traffic = []
    for r in rows:
        traffic.append({"name": r["name"], "a_bytes": r["a_bytes"], "w_bytes": r["w_bytes"], "out_bytes": r["out_bytes"], "stream_a_bytes": r["stream_a_bytes"], "stream_w_bytes": r["stream_w_bytes"], "total_bytes": r["stream_a_bytes"] + r["stream_w_bytes"] + r["out_bytes"], "format": "A16/W8/O16"})
    fields = ["name", "a_bytes", "w_bytes", "out_bytes", "stream_a_bytes", "stream_w_bytes", "total_bytes", "format"]
    with (DATA / "traffic_breakdown.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(traffic)
    return rows


if __name__ == "__main__":
    rows = build()
    for r in rows:
        print(f'{r["name"]}: {r["total_cycles"]} cycles, engine_util={r["engine_utilization"]:.3f}, completion={r["completion_rate"]:.3f}')
