# Vivado synthesis flow

生成时间：2026-09-13 10:52:55（Asia/Shanghai）

`run_top_synth.ps1` 调用本机 Vivado 2021.2 的 `syn_top.tcl`，使用非工程 batch 流程。目标器件为 `xczu7ev-ffvc1156-2-e`，时钟约束为 3.298 ns。它先综合 `w8a16_system_top`，再综合 `w8a16_array_top` 的 1×1、4×4 和 16×48 三个规模；每个规模单独保留 `vivado.log`、`utilization.rpt`、`timing.rpt`、`drc.rpt` 和 `post_synth.dcp`。

本轮运行目录为 `runs/2026-09-13_104234/`。四个配置的 `synth_design` 均完成。16×48 阵列的综合资源为 57,331 LUT、110,656 FF 和 768 DSP；综合 WNS 为 2.149 ns，对应约 870 MHz 的综合估算。系统顶层的资源为 52,743 LUT、2,814 FF 和 35 DSP，但 WNS 为 -4.528 ns；关键路径落在动作路径的饱和／输出打包逻辑。综合 DRC 没有 Error，但有 DSP 输入／输出流水相关 warning。

这些数只证明 RTL 可以由 Vivado 展开和综合。还没有执行 `place_design`、`route_design`、post-route `phys_opt`、功耗分析或最终板级时序收敛。
