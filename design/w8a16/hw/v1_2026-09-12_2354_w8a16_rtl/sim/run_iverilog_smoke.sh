#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SIM="$ROOT/hw/v1_2026-09-12_2354_w8a16_rtl/sim"
RTL="$ROOT/hw/v1_2026-09-12_2354_w8a16_rtl/rtl"
mkdir -p "$SIM/logs"
RUN_START_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_START_EPOCH="$(date +%s)"
command -v iverilog >/dev/null 2>&1 || { echo "IVERILOG_UNAVAILABLE"; exit 2; }
command -v vvp >/dev/null 2>&1 || { echo "VVP_UNAVAILABLE"; exit 2; }
iverilog -g2012 -DVERILATOR -s tb_w8a16_pe -o "$SIM/pe.vvp" \
  "$RTL/w8a16_mult.sv" "$RTL/w8a16_pe.sv" "$SIM/tb_w8a16_pe.sv"
vvp "$SIM/pe.vvp" | tee "$SIM/logs/iverilog_pe.log"
iverilog -g2012 -DVERILATOR -s tb_w8a16_array -o "$SIM/array.vvp" \
  "$RTL/w8a16_mult.sv" "$RTL/w8a16_pe.sv" "$RTL/w8a16_sysarr.sv" "$SIM/tb_w8a16_array.sv"
vvp "$SIM/array.vvp" | tee "$SIM/logs/iverilog_array.log"
iverilog -g2012 -DVERILATOR -s tb_w8a16_activations -o "$SIM/activations.vvp" \
  "$RTL/w8a16_relu.sv" "$RTL/w8a16_gelu.sv" "$RTL/w8a16_tanh.sv" "$RTL/w8a16_vector_add.sv" \
  "$RTL/w8a16_layernorm.sv" "$RTL/w8a16_softmax.sv" "$SIM/tb_w8a16_activations.sv"
vvp "$SIM/activations.vvp" | tee "$SIM/logs/iverilog_activations.log"
iverilog -g2012 -DVERILATOR -s tb_w8a16_isa_ctrl -o "$SIM/isa_ctrl.vvp" \
  "$RTL/w8a16_isa_ctrl.sv" "$SIM/tb_w8a16_isa_ctrl.sv"
vvp "$SIM/isa_ctrl.vvp" | tee "$SIM/logs/iverilog_isa_ctrl.log"
RUN_END_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_END_EPOCH="$(date +%s)"
RUN_SECONDS=$((RUN_END_EPOCH - RUN_START_EPOCH))
printf '{"status":"passed","tool":"iverilog","started":"%s","finished":"%s","elapsed_seconds":%s,"tests":["tb_w8a16_pe","tb_w8a16_array","tb_w8a16_activations","tb_w8a16_isa_ctrl"]}\n' \
  "$RUN_START_UTC" "$RUN_END_UTC" "$RUN_SECONDS" > "$SIM/logs/iverilog_run.json"
