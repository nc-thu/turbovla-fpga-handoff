"""Fast, read-only checks for the TurboVLA full-model package.

The script deliberately does not run the long model or modify source data.  It
checks descriptor accounting, coverage, cycle arithmetic and metric bounds.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# The public handoff keeps the compact, generated inputs beside this script;
# the original workspace used a versioned compiler/compiled_full directory.
COMP = ROOT / "data"

def load(name):
    return json.loads((COMP / name).read_text(encoding="utf-8"))

def main():
    cov = load("coverage_summary.json")
    cyc = load("cycle_summary.json")
    desc = (COMP / "descriptors.jsonl").read_text(encoding="utf-8").splitlines()
    instr = (COMP / "instructions.hex").read_text(encoding="utf-8").splitlines()
    assert cov.get("unknown_event_count", -1) == 0
    assert cyc.get("parent_children_not_double_counted") is True
    assert len(desc) == cyc["descriptor_count"] and len(instr) == len(desc) + 1
    assert instr[-1].lower().startswith("0xff")
    assert 0 <= cyc["pe_time_utilization"] <= 1
    assert 0 <= cyc["gemm_utilization"] <= 1
    assert cyc["mapped_cycles"] + cyc["fallback_cycles"] == cyc["total_cycles"]
    assert cyc["valid_mac_count"] >= 0 and cyc["active_pe_cycles"] >= 0
    with (COMP / "cycle_breakdown.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert rows and sum(int(r["total_cycles"]) for r in rows) == cyc["total_cycles"]
    print("FULL_MODEL_VALIDATION PASS")
    print(json.dumps({"descriptors": len(desc), "total_cycles": cyc["total_cycles"],
                      "unknown": cov.get("unknown_event_count"),
                      "pe_utilization": cyc["pe_time_utilization"]}, ensure_ascii=False))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FULL_MODEL_VALIDATION FAIL: {exc}", file=sys.stderr)
        raise
