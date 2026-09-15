#!/usr/bin/env bash
set -euo pipefail
VERSION_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SIM="$VERSION_DIR/sim"
RTL="$VERSION_DIR/rtl"
mkdir -p "$SIM/logs"
RUN_START_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_START_EPOCH="$(date +%s)"
if ! command -v xvlog >/dev/null 2>&1; then
  echo "UNISIM_UNAVAILABLE" | tee "$SIM/logs/unisim_smoke.log"
  printf '{"status":"unavailable","tool":"xvlog","started":"%s","finished":"%s","elapsed_seconds":0,"reason":"Vivado/UNISIM executable not found on server"}\n' \
    "$RUN_START_UTC" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$SIM/logs/unisim_run.json"
  exit 2
fi
# The normal PE test uses the behavioral macro.  This short compile is kept
# separate because only Vivado supplies the DSP48E2/UNISIM library.
xvlog -sv "$RTL/w8a16_mult.sv" "$RTL/w8a16_pe.sv" "$SIM/tb_w8a16_pe.sv" \
  -d TVLA_UNISIM_SMOKE 2>&1 | tee "$SIM/logs/unisim_smoke.log"
RUN_END_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_END_EPOCH="$(date +%s)"
RUN_SECONDS=$((RUN_END_EPOCH - RUN_START_EPOCH))
printf '{"status":"passed","tool":"xvlog","started":"%s","finished":"%s","elapsed_seconds":%s}\n' \
  "$RUN_START_UTC" "$RUN_END_UTC" "$RUN_SECONDS" > "$SIM/logs/unisim_run.json"
