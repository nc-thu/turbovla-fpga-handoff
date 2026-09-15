# TurboVLA 十项优化：回放顶层和综合

完成时刻：2026-09-14 02:03:37。

本目录从 v8 replay top 独立复制而来。`tvla_replay_top.sv` 增加了结果保持、FIFO push/pop 同拍计数修正、优化标志计数和写 burst 计数；DSP 数量仍为 768。`sim/` 中的完整事件回放是虚拟周期计数，代表性 tile 和 FIFO 交错测试才逐拍经过 Verilator 阵列。

Vivado 2021.2 使用 `xczu7ev-ffvc1156-2-e` 和 4.000 ns 目标，分别综合 array off、array on/trace off、array on/trace on。三项均通过；阵列开启后的资源为 60,419 LUT、119,214 FF、768 DSP，WNS 1.884 ns，Fmax 472.6 MHz（synthesis-estimated）。活动监视器在这三个配置中没有改变资源。这个目录没有做 post-route 和 SAIF/VCD 功耗。

`synth/run_replay_synth.ps1` 可复现综合，运行输出应放到独立的 `data/v9_.../vivado_runs_*` 目录。
