#!/usr/bin/env bash
set -eu
export PATH="$HOME/.conda/envs/vsim/bin:$PATH"
cd "$(dirname "$0")"
verilator --version > tool.txt
for variant in base overlap read2 core2; do
 mkdir -p "results/$variant"
 case "$variant" in
 base) top=tb_gemm_p2; src="ae_gemm_p2.sv ae_sysarr_p2.sv ae_pe_p2.sv"; par="-GPULSE_DLY_TB=5";;
 overlap|read2) top=tb_gemm_pp; src="ae_gemm_pp.sv ae_sysarr_pp.sv ae_pe_pp.sv"; wb=0; [ "$variant" != read2 ] || wb=1; par="-GPULSE_DLY_TB=5 -GWB2_TB=$wb";;
 core2) top=tb_gemm_p2d; src="ae_gemm_p2d.sv ae_sysarr_p2d.sv ae_pe_pp.sv"; par="-GPULSE_DLY2_TB=6 -GWB2_TB=1";;
 esac
 files="sim/$top.sv"; for f in $src pack2_mult_dsp.sv rq_ms_x.sv rq_v2.sv; do files="$files rtl/$f"; done
 sha256sum $files > "results/$variant/sources.sha256"
 date -Is > "results/$variant/started.txt"
 if timeout 500s verilator --binary --timing -j 4 -Wno-fatal --top-module "$top" -DVERILATOR=1 -GPCOLS_TB=4 $par --Mdir "results/$variant/obj" -o sim $files > "results/$variant/build.log" 2>&1; then
 timeout 60s "results/$variant/obj/sim" > "results/$variant/run.log" 2>&1 || true
 fi
 date -Is > "results/$variant/finished.txt"
 done
