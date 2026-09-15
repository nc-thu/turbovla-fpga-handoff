#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERSION_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SIM="$VERSION_DIR/sim"
RTL="$VERSION_DIR/rtl"
mkdir -p "$SIM/logs"
RUN_START_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_START_EPOCH="$(date +%s)"
command -v verilator >/dev/null 2>&1 || { echo "VERILATOR_UNAVAILABLE"; exit 2; }
verilator --version | tee "$SIM/logs/verilator_version.txt"
rm -rf "$SIM/obj_pe" "$SIM/obj_array" "$SIM/obj_full" "$SIM/obj_requant" "$SIM/obj_gemm" \
  "$SIM/obj_activations" "$SIM/obj_vector_ops" "$SIM/obj_dma" "$SIM/obj_isa_ctrl" "$SIM/obj_runtime" "$SIM/obj_system"
MAKE_OVERRIDES=()
if [ -x /usr/bin/g++-10 ]; then
  MAKE_OVERRIDES=(-MAKEFLAGS "CXX=/usr/bin/g++-10 LINK=/usr/bin/g++-10 AR=/usr/bin/ar")
fi
WARN_OPTS=(-Wno-fatal -Wno-TIMESCALEMOD -Wno-MULTIDRIVEN -Wno-WIDTHTRUNC -Wno-WIDTHEXPAND)
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_pe \
  "$RTL/w8a16_mult.sv" "$RTL/w8a16_pe.sv" "$SIM/tb_w8a16_pe.sv" \
  -Mdir "$SIM/obj_pe" -o sim_pe
"$SIM/obj_pe/sim_pe" | tee "$SIM/logs/tb_w8a16_pe.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_array \
  "$RTL/w8a16_mult.sv" "$RTL/w8a16_pe.sv" "$RTL/w8a16_sysarr.sv" "$SIM/tb_w8a16_array.sv" \
  -Mdir "$SIM/obj_array" -o sim_array
"$SIM/obj_array/sim_array" | tee "$SIM/logs/tb_w8a16_array.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_full \
  "$RTL/w8a16_mult.sv" "$RTL/w8a16_pe.sv" "$RTL/w8a16_sysarr.sv" "$SIM/tb_w8a16_full.sv" \
  -Mdir "$SIM/obj_full" -o sim_full
"$SIM/obj_full/sim_full" | tee "$SIM/logs/tb_w8a16_full.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_requant \
  "$RTL/w8a16_requant.sv" "$SIM/tb_w8a16_requant.sv" \
  -Mdir "$SIM/obj_requant" -o sim_requant
"$SIM/obj_requant/sim_requant" | tee "$SIM/logs/tb_w8a16_requant.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_gemm \
  "$RTL/w8a16_mult.sv" "$RTL/w8a16_pe.sv" "$RTL/w8a16_sysarr.sv" "$RTL/w8a16_gemm.sv" "$SIM/tb_w8a16_gemm.sv" \
  -Mdir "$SIM/obj_gemm" -o sim_gemm
"$SIM/obj_gemm/sim_gemm" | tee "$SIM/logs/tb_w8a16_gemm.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_activations \
  "$RTL/w8a16_relu.sv" "$RTL/w8a16_gelu.sv" "$RTL/w8a16_tanh.sv" "$RTL/w8a16_vector_add.sv" \
  "$RTL/w8a16_layernorm.sv" "$RTL/w8a16_softmax.sv" "$SIM/tb_w8a16_activations.sv" \
  -Mdir "$SIM/obj_activations" -o sim_activations
"$SIM/obj_activations/sim_activations" | tee "$SIM/logs/tb_w8a16_activations.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_vector_ops \
  "$RTL/w8a16_relu.sv" "$RTL/w8a16_gelu.sv" "$RTL/w8a16_tanh_pipe.sv" "$RTL/w8a16_layernorm.sv" \
  "$RTL/w8a16_softmax.sv" "$RTL/w8a16_vector_add.sv" "$RTL/w8a16_vector_mul.sv" "$RTL/w8a16_vector_ops.sv" \
  "$SIM/tb_w8a16_vector_ops.sv" -Mdir "$SIM/obj_vector_ops" -o sim_vector_ops
"$SIM/obj_vector_ops/sim_vector_ops" | tee "$SIM/logs/tb_w8a16_vector_ops.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_dma \
  "$RTL/w8a16_dma.sv" "$SIM/tb_w8a16_dma.sv" -Mdir "$SIM/obj_dma" -o sim_dma
"$SIM/obj_dma/sim_dma" | tee "$SIM/logs/tb_w8a16_dma.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_isa_ctrl \
  "$RTL/w8a16_isa_ctrl.sv" "$SIM/tb_w8a16_isa_ctrl.sv" -Mdir "$SIM/obj_isa_ctrl" -o sim_isa_ctrl
"$SIM/obj_isa_ctrl/sim_isa_ctrl" | tee "$SIM/logs/tb_w8a16_isa_ctrl.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_runtime \
  "$RTL/w8a16_isa_ctrl.sv" "$RTL/w8a16_tanh.sv" "$RTL/w8a16_tanh_pipe.sv" "$RTL/w8a16_action_path.sv" "$RTL/w8a16_requant.sv" \
  "$RTL/w8a16_relu.sv" "$RTL/w8a16_gelu.sv" "$RTL/w8a16_layernorm.sv" "$RTL/w8a16_softmax.sv" \
  "$RTL/w8a16_vector_add.sv" "$RTL/w8a16_vector_mul.sv" "$RTL/w8a16_vector_ops.sv" "$RTL/w8a16_dma.sv" "$RTL/w8a16_runtime.sv" \
  "$SIM/tb_w8a16_runtime.sv" -Mdir "$SIM/obj_runtime" -o sim_runtime
"$SIM/obj_runtime/sim_runtime" | tee "$SIM/logs/tb_w8a16_runtime.log"
verilator --binary "${MAKE_OVERRIDES[@]}" "${WARN_OPTS[@]}" --top-module tb_w8a16_system \
  "$RTL/w8a16_isa_ctrl.sv" "$RTL/w8a16_tanh.sv" "$RTL/w8a16_tanh_pipe.sv" "$RTL/w8a16_action_path.sv" "$RTL/w8a16_requant.sv" \
  "$RTL/w8a16_relu.sv" "$RTL/w8a16_gelu.sv" "$RTL/w8a16_layernorm.sv" "$RTL/w8a16_softmax.sv" \
  "$RTL/w8a16_vector_add.sv" "$RTL/w8a16_vector_mul.sv" "$RTL/w8a16_vector_ops.sv" "$RTL/w8a16_dma.sv" \
  "$RTL/w8a16_runtime.sv" "$RTL/w8a16_mult.sv" "$RTL/w8a16_pe.sv" "$RTL/w8a16_sysarr.sv" "$RTL/w8a16_gemm.sv" \
  "$SIM/../synth/top_w8a16_system.sv" "$SIM/tb_w8a16_system.sv" \
  -Mdir "$SIM/obj_system" -o sim_system
"$SIM/obj_system/sim_system" | tee "$SIM/logs/tb_w8a16_system.log"
RUN_END_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_END_EPOCH="$(date +%s)"
RUN_SECONDS=$((RUN_END_EPOCH - RUN_START_EPOCH))
printf '{"status":"passed","tool":"verilator","version_file":"logs/verilator_version.txt","started":"%s","finished":"%s","elapsed_seconds":%s,"tests":["tb_w8a16_pe","tb_w8a16_array","tb_w8a16_full","tb_w8a16_requant","tb_w8a16_gemm","tb_w8a16_activations","tb_w8a16_vector_ops","tb_w8a16_dma","tb_w8a16_isa_ctrl","tb_w8a16_runtime","tb_w8a16_system"],"dsp_full_array":768}\n' \
  "$RUN_START_UTC" "$RUN_END_UTC" "$RUN_SECONDS" > "$SIM/logs/verilator_run.json"
