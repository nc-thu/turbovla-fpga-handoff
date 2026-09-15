"""Run compiler ablations for the ten selected history optimizations."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[2]
COMPILER = ROOT / "compiler" / "v6_2026-09-14_010956_history_optimization" / "compile_trace.py"
CAPTURE = ROOT / "data" / "v8_2026-09-13_231621" / "raw_capture"
OUTROOT = ROOT / "data" / "v9_2026-09-14_010956" / "ablation"
CONFIGS = {
    "baseline": "",
    "pipeline": "pipeline",
    "fanout": "fanout",
    "tile_mask": "tile_mask",
    "order": "order",
    "act_reuse": "act_reuse",
    "weight_reuse": "weight_reuse",
    "overlap": "overlap",
    "write_coalesce": "write_coalesce",
    "fusion": "fusion",
    "vector_pipeline": "vector_pipeline",
    "all_selected": ",".join(["pipeline","fanout","tile_mask","order","act_reuse","weight_reuse","overlap","write_coalesce","fusion","vector_pipeline"]),
    "reuse_plus_overlap": "order,act_reuse,weight_reuse,overlap,write_coalesce",
}

def main() -> None:
    OUTROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, enabled in CONFIGS.items():
        out = OUTROOT / name; out.mkdir(parents=True, exist_ok=True)
        cmd = [sys.executable, str(COMPILER), "--capture", str(CAPTURE), "--output", str(out), "--enabled", enabled or "none"]
        done = subprocess.run(cmd, capture_output=True, text=True, check=True)
        summary = json.loads((out / "replay_summary.json").read_text(encoding="utf-8"))
        c = summary["cycles"]
        rows.append({"name": name, "enabled": enabled, "total_cycles": c["total_cycles"], "base_cycles": c["base_total_cycles"], "savings_pct": c["cycle_savings_pct"], "mapped_cycles": c["mapped_cycles"], "fallback_cycles": c["fallback_cycles"], "pe_utilization": summary["pe_time_utilization"], "gemm_utilization": summary["gemm_utilization"], "effective_gops": summary["effective_gops"], "activation_bytes": summary["traffic_bytes"]["activation_bytes"], "weight_bytes": summary["traffic_bytes"]["weight_bytes"], "output_bytes": summary["traffic_bytes"]["output_bytes"], "descriptor_count": summary["descriptor_count"], "instruction_count": summary["instruction_count"], "bmm_attached": summary["coverage"]["bmm_attached_to_parent"], "fusion_groups": summary["fusion_group_count"]})
    (OUTROOT / "ablation_summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    cols = list(rows[0])
    def cell(x):
        s = str(x); return '"'+s.replace('"','""')+'"' if ',' in s else s
    (OUTROOT / "ablation_summary.csv").write_text(','.join(cols)+'\n'+'\n'.join(','.join(cell(r.get(c,'')) for c in cols) for r in rows)+'\n', encoding='utf-8')
    print(json.dumps(rows, indent=2))

if __name__ == "__main__": main()
