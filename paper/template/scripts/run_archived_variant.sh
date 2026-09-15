#!/usr/bin/env bash
# Reproduce one archived variant in an isolated new output directory.
# This is NOT the new equal-workload ablation; Claude must add that harness.
set -euo pipefail
if [ "$#" -lt 3 ]; then echo 'usage: bash run_archived_variant.sh REPO OUT base|overlap|read2|core2 [PCOLS=4]'; exit 2; fi
repo=$(realpath "$1"); out=$(realpath -m "$2"); variant=$3; cols=${4:-4}
if [ -e "$out" ]; then echo 'OUT must be a new directory (no overwrite).'; exit 2; fi
case "$cols" in 4|48) ;; *) echo 'PCOLS must be 4 or 48'; exit 2;; esac
mkdir -p "$out"
sim="$repo/hw/v8_2026-09-12_0054_rtl_util_r5/sim"
rtl="$repo/hw/v8_2026-09-12_0054_rtl_util_r5/rtl_p2"
params=("-GPCOLS_TB=$cols")
case "$variant" in
 base) top=tb_gemm_p2; sources=(ae_gemm_p2.sv ae_sysarr_p2.sv ae_pe_p2.sv); params+=('-GPULSE_DLY_TB=5');;
 overlap|read2) top=tb_gemm_pp; sources=(ae_gemm_pp.sv ae_sysarr_pp.sv ae_pe_pp.sv); wb=0; [ "$variant" = read2 ] && wb=1; params+=("-GWB2_TB=$wb" '-GPULSE_DLY_TB=5');;
 core2) top=tb_gemm_p2d; sources=(ae_gemm_p2d.sv ae_sysarr_p2d.sv ae_pe_pp.sv); params+=('-GWB2_TB=1' '-GPULSE_DLY2_TB=6');;
 *) echo 'unknown variant'; exit 2;;
esac
files=("$sim/$top.sv")
for f in "${sources[@]}" pack2_mult_dsp.sv rq_ms_x.sv rq_v2.sv; do files+=("$rtl/$f"); done
for f in "${files[@]}"; do [ -f "$f" ] || { echo "Missing source $f"; exit 2; }; done
printf '%s\n' "${files[@]}" > "$out/sources.txt"
sha256sum "${files[@]}" > "$out/source_hashes.txt"
verilator --version > "$out/tool_version.txt"
deadline=$((SECONDS+600))
timeout 540s verilator --binary --timing -j 4 -Wno-fatal --top-module "$top" -DVERILATOR=1 -DWIDE=1 --Mdir "$out/obj" -o sim "${params[@]}" "${files[@]}" > "$out/build.log" 2>&1
remaining=$((deadline-SECONDS)); [ "$remaining" -gt 0 ] || exit 124
timeout "${remaining}s" "$out/obj/sim" > "$out/run.log" 2>&1
if grep -E 'FAIL|Error|got=x' "$out/run.log"; then exit 1; fi
grep 'ALL PASS' "$out/run.log"
