#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
for variant in base overlap read2 core2; do
 case "$variant" in base) top=tb_gemm_p2;; overlap|read2) top=tb_gemm_pp;; core2) top=tb_gemm_p2d;; esac
 date -Is > "results/$variant/rebuild_started.txt"
 if timeout 500s make -C "results/$variant/obj" -f "V$top.mk" -j 4 CXX=/usr/bin/g++-10 AR=/usr/bin/ar LINK=/usr/bin/g++-10 > "results/$variant/rebuild.log" 2>&1; then
  timeout 60s "results/$variant/obj/sim" > "results/$variant/run.log" 2>&1 || true
 fi
 date -Is > "results/$variant/rebuild_finished.txt"
done
