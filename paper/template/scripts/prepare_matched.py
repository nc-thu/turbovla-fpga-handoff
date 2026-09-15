from pathlib import Path
import shutil, tarfile, hashlib, json
P=Path(__file__).resolve().parents[1]; R=P.parents[1]
O=P/'experiment_inputs'/'matched'; O.mkdir(exist_ok=True)
S=R/'hw/v8_2026-09-12_0054_rtl_util_r5'
shutil.copytree(S/'rtl_p2',O/'rtl',dirs_exist_ok=True)
(O/'sim').mkdir(exist_ok=True)
calls='''
    run_desc(32, 8, 8, 0, 5, 0, 448, 8, 100, 12000, "shortK");
    run_desc(32, 8, 8, 0, 64, 0, 448, 8, 100, 12000, "mediumK");
    run_desc(32, 8, 8, 0, 2049, 0, 448, 8, 100, 12000, "deepK");
    run_desc(32, 8, 6, 0, 64, 0, 448, 8, 100, 12000, "narrowN");
    if (err_total == 0) $display("MATCHED ALL PASS");
    else $display("MATCHED FAIL err=%0d",err_total);
    $finish;
  end
endmodule
'''
for top in ['tb_gemm_p2','tb_gemm_pp','tb_gemm_p2d']:
 t=(S/'sim'/f'{top}.sv').read_text(encoding='utf8')
 start=t.rfind('  initial begin'); assert start>0
 t=t[:start]+'''  initial begin
    err_total = 0; seed_r = 16'hb00b;
    repeat (3) @(negedge clk); rst_n = 1;
    repeat (5) @(negedge clk);
'''+calls
 (O/'sim'/f'{top}.sv').write_text(t,encoding='utf8')
script='''#!/usr/bin/env bash
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
'''
(O/'run.sh').write_text(script,encoding='utf8',newline='\n')
with tarfile.open(P/'experiment_inputs/matched.tar.gz','w:gz') as tar:tar.add(O,arcname='matched')
print(P/'experiment_inputs/matched.tar.gz')
