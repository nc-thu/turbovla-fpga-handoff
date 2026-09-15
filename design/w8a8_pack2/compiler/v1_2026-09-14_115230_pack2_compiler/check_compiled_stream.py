"""Validate the generated W8A8 Pack2 descriptor and command streams."""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(); ap.add_argument("--compiled", type=Path, required=True); ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args(); start = time.time(); root = args.compiled
    ds = [json.loads(x) for x in (root / "descriptors.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    ins = [json.loads(x) for x in (root / "instructions.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    words = [int(x, 16) for x in (root / "descriptors_512.hex").read_text(encoding="utf-8").splitlines() if x.strip()]
    failures = []
    if len(ins) != len(ds) + 1 or ins[-1]["op"] != "END": failures.append("instruction_end_or_count")
    if len(words) != len(ds): failures.append("descriptor_word_count")
    if any(d["a_bits"] != 8 or d["w_bits"] != 8 or d["out_bits"] != 8 or d["acc_bits"] != 32 for d in ds): failures.append("bit_semantics")
    if any(d["physical_cols"] != 48 or d["logical_cols"] != 96 for d in ds if d["mapping"].startswith("rtl")): failures.append("array_geometry")
    # descriptors_512.hex stores the 14 32-bit accounting fields above the
    # low 64-bit control trailer.  The opcode therefore lives in bits
    # [63:56], not in the most-significant byte of the 512-bit integer.
    if any(((w >> 56) & 0xFF) not in {0x18, 0x19, 0x50, 0x30, 0x33, 0xFF} for w in words): failures.append("descriptor_opcode")
    if len({d["descriptor_id"] for d in ds}) != len(ds): failures.append("duplicate_descriptor_id")
    mapped = [d for d in ds if d["mapping"] in {"rtl_gemm", "rtl_bmm"}]
    result = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "descriptor_count": len(ds), "instruction_count": len(ins),
        "mapping_counts": dict(Counter(d["mapping"] for d in ds)), "mapped_count": len(mapped),
        "valid_mac_count": sum(int(d["cycle_cost"].get("valid_mac_count", 0)) for d in mapped),
        "unknown_count": sum(d["mapping"] == "unknown" for d in ds), "failures": failures,
        "status": "PASS" if not failures else "FAIL", "elapsed_seconds": time.time() - start,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps(result, indent=2)); raise SystemExit(0 if not failures else 1)


if __name__ == "__main__": main()
