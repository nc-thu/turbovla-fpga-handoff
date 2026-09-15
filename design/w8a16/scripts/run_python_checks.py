"""Fast, dependency-light acceptance checks for the new work area."""
from __future__ import annotations

import json
import csv
import argparse
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from w8a16_math import (dequantized_linear, integer_linear, quantize_symmetric,
                        quantize_weight_per_output, required_acc_bits,
                        requantize, contract_summary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data")
    args = parser.parse_args()
    data = args.data_dir.resolve()
    data.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20260830)
    a = rng.normal(0, 0.7, size=(5, 37))
    w = rng.normal(0, 0.2, size=(11, 37))
    qa = quantize_symmetric(a, 16)
    qw = quantize_weight_per_output(w)
    acc, out = dequantized_linear(qa.q, qa.scale, qw.q, qw.scale)
    direct = qa.q.astype(np.int64) @ qw.q.astype(np.int64).T
    assert np.array_equal(acc, direct)
    assert np.all(np.isfinite(out))
    assert required_acc_bits(4096) <= 40
    endpoints = np.array([-32768, -32767, -1, 0, 1, 32767], dtype=np.int16)
    assert int(endpoints.min()) == -32768 and int(endpoints.max()) == 32767
    r = requantize(np.array([-2**34, -1, 0, 1, 2**34], dtype=np.int64), 3, 2)
    assert int(r.min()) >= -32768 and int(r.max()) <= 32767
    fp32 = a @ w.T
    err = out - fp32
    rms = float(np.sqrt(np.mean(err * err)))
    rows = [{
        "case": "random_matrix_sanity", "source": "run_python_checks.py",
        "shape": "5x37x11", "max_abs_error": float(np.max(np.abs(err))),
        "mean_abs_error": float(np.mean(np.abs(err))), "rmse": rms,
    }]
    # The previous server screening used the same logical W8A16 fake-quant
    # boundary but dequantized into FP32 F.linear.  Preserve it as a clearly
    # labeled reference; it is not evidence of a hardware integer kernel.
    summary_path = data / "quant_screening_summary.json"
    if not summary_path.exists():
        summary_path = ROOT / "data" / "quant_screening_summary.json"
    if summary_path.exists():
        screening = json.loads(summary_path.read_text(encoding="utf-8"))
        spot = screening.get("spot", {}).get("modes", {}).get("w8a16", {})
        if spot:
            rows.append({
                "case": "historical_libero_spot", "source": "data/quant_screening_summary.json",
                "shape": "TurboVLA output (recorded)",
                "max_abs_error": spot.get("max_abs_vs_fp32"),
                "mean_abs_error": spot.get("mean_abs_vs_fp32"), "rmse": None,
            })
    summary = {
        "status": "PASS",
        "seed": 20260830,
        "checks": ["integer_matmul", "dequantized_path_finite", "40bit_bound_at_k4096", "int16_saturation"],
        "contract": contract_summary(),
    }
    out = data / "python_checks.json"
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with (data / "quant_error.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["case", "source", "shape", "max_abs_error", "mean_abs_error", "rmse"])
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
