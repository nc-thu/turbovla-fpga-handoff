#!/usr/bin/env bash
# Run the two independent timing points for the timing-pipeline top.
# Usage: ./run_two_freqs.sh [output_root]
#
# The script intentionally runs one Vivado configuration at a time.  This is
# the C-cluster convention for reproducible single-config project runs.
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
OUT_ROOT="${1:-$ROOT_DIR/reports}"
mkdir -p "$OUT_ROOT/250MHz" "$OUT_ROOT/303MHz"

run_one() {
  local label="$1"
  local period="$2"
  local out="$OUT_ROOT/$label"
  local start end rc
  start=$(date +%s)
  if ! command -v vivado >/dev/null 2>&1; then
    python3 - "$out" "$period" "$label" <<'PY'
import json, os, sys, time
out, period, label = sys.argv[1:]
os.makedirs(out, exist_ok=True)
meta = {
    "status": "not_run",
    "reason": "vivado command not found on this host",
    "start": time.strftime("%Y-%m-%d %H:%M:%S"),
    "end": time.strftime("%Y-%m-%d %H:%M:%S"),
    "elapsed_seconds": 0,
    "period_ns": float(period),
    "frequency_mhz": 1000.0 / float(period),
    "label": label,
}
with open(os.path.join(out, "run_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)
PY
    echo "[$label] Vivado not found; recorded not_run"
    return 127
  fi
  echo "[$label] start $(date '+%Y-%m-%d %H:%M:%S') period=${period}ns"
  vivado -mode batch -source "$SCRIPT_DIR/run_vivado_impl.tcl" \
    -tclargs "$period" "$out" >"$out/launcher.log" 2>&1
  rc=$?
  end=$(date +%s)
  echo "[$label] end $(date '+%Y-%m-%d %H:%M:%S') elapsed=$((end-start))s rc=$rc"
  return "$rc"
}

overall=0
run_one 250MHz 4.000 || overall=$?
run_one 303MHz 3.298 || overall=$?
exit "$overall"
