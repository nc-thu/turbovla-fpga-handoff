"""Bit-level checks for the HB Pack2 INT8xINT8 arithmetic."""
from __future__ import annotations

import json
import random
import time
from pathlib import Path


def signed(value: int, bits: int) -> int:
    value &= (1 << bits) - 1
    return value - (1 << bits) if value & (1 << (bits - 1)) else value


def pack2(a: int, w0: int, w1: int) -> tuple[int, int, int]:
    q0, q1 = w0 + 128, w1 + 128
    q = (q1 << 16) | q0
    r = q - 128 * ((1 << 16) + 1)
    p = a * r
    low = signed(p & 0xFFFF, 16)
    high = signed((p >> 16) & 0x1FFFF, 17) + ((p >> 15) & 1)
    return low, high, p


def main() -> None:
    ap = __import__("argparse").ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--samples", type=int, default=100000)
    args = ap.parse_args()
    out = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    start = time.time()
    vectors = [(a, w0, w1) for a in (-128, -127, -1, 0, 1, 126, 127) for w0 in (-128, -127, -1, 0, 1, 126, 127) for w1 in (-128, -127, -1, 0, 1, 126, 127)]
    rng = random.Random(20260914)
    vectors.extend((rng.randint(-128, 127), rng.randint(-128, 127), rng.randint(-128, 127)) for _ in range(args.samples))
    failures = []
    max_abs = 0
    for a, w0, w1 in vectors:
        p0, p1, p = pack2(a, w0, w1)
        if (p0, p1) != (a * w0, a * w1):
            failures.append({"a": a, "w0": w0, "w1": w1, "got": [p0, p1], "want": [a * w0, a * w1], "packed_product": p})
            if len(failures) >= 10:
                break
        max_abs = max(max_abs, abs(p))
    k_bounds = {}
    for k in (1, 32, 256, 3072, 4096):
        worst = k * 128 * 128
        k_bounds[str(k)] = {"worst_abs_int32": worst, "fits_int32": worst < 2**31, "fits_signed27": worst <= 2**26 - 1}
    result = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "sample_count": len(vectors), "failure_count": len(failures), "failures": failures,
        "max_packed_product_abs_seen": max_abs,
        "pack_formula": "Q=(w1+128)*2^16+(w0+128); R=Q-128*(2^16+1); P=a*R; prod0=P[15:0]; prod1=P[31:16]+P[15]",
        "k_bounds": k_bounds,
        "status": "PASS" if not failures else "FAIL",
        "elapsed_seconds": time.time() - start,
    }
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if not failures else 1)


if __name__ == "__main__":
    main()
