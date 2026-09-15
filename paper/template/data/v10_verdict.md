# v10 回归存证（新旧 PE 位精确一致性）

日期：2026-09-12　口径：同 TB、同 iverilog（C:/iverilog/bin，-g2012 -DVERILATOR=1）、
同参数，唯一变量 = PE（旧 pack2_mult_dsp+stage1 校正 vs 新 pack2_mult_padd 预加器版）。
对照物：① v8 原 PE 本机同刻重跑（ctl_*.log，排除"存档是老 TB/老工具跑的"干扰）；
② v8 存档日志（hw/v8_2026-09-12_0054_rtl_util_r5/results/）。

## PCOLS=4（四组，全部完成）

| 组 | 对照 | 判据 | 结果 |
|---|---|---|---|
| p2_base4（基线引擎） | ctl_p2_base4.log（v8 原 PE 本机重跑） | 全文 diff | 逐行一致，含 L2b 既有 FAIL err=384、cycles=6245 行为一致 |
| pp4_wb1（乒乓+双写，写口0） | v8 存档 pp4_wb1.log | 归一化 diff（去 \r、去 $finish 诊断行） | 十档（D0~D3/L0~L2）逐行一致，ALL PASS |
| pp4_wb2（同上，写口1） | v8 存档 pp4_wb2.log | 同上 | 逐行一致，ALL PASS |
| p2d4_pd6（2× 时钟域引擎） | v8 存档 p2d4_pd6.log | grep -v dbg 归一化 diff | 逐行一致（唯一差异 = v8 存档多一行 $finish 诊断），ALL PASS |

注：p2_base4 的 L2b FAIL（err=384, got=x）是**对照组同样复现**的既有行为
（当前版 TB 的 L2b 深档 + PCOLS=4 + iverilog 组合 v8 存档从未跑过，存档 p2_base4.log
是老版 TB）。新旧 PE 在该档的失败行为逐行相同，不影响"位精确一致"结论。

## 复现命令（PCOLS=4 例）

    export PATH=/c/iverilog/bin:$PATH
    cd hw/v10_2026-09-12_1148_engfull_preadd/sim
    iverilog -g2012 -DVERILATOR=1 -o p2d4_pd6.vvp tb_gemm_p2d.sv \
      ../rtl/ae_gemm_p2d.sv ../rtl/ae_sysarr_p2d_pa.sv ../rtl/ae_pe_pp_pa.sv \
      ../rtl/pack2_mult_padd.sv ../rtl/rq_ms_x.sv ../rtl/rq_v2.sv
    vvp p2d4_pd6.vvp +PCOLS_TB=4 +PULSE_DLY2_TB=6 > ../results/v10_p2d4_pd6.log

（p2/pp 版：换 tb_gemm_p2/tb_gemm_pp 与对应 sysarr/例化链，PE 链换成旧版
ae_pe_p2/ae_pe_pp/pack2_mult_dsp 得对照组。）

## 全宽 PCOLS=48（+WIDE 档）

在跑：p2_48 / pp48_w1 / pp48_w2 / p2d48 ×（ctl 重跑 vs v10）。结论见
results/*_48.log 与下方补记。
