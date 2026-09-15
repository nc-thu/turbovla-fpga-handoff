# 修改说明

生成时间：2026-09-13T14:52:54+08:00

本版在 v2 的动作后处理、LayerNorm/Softmax 迭代路径、DMA 数据落地和生产阵列启动基础上，加入 v3 编译器的 tile shape/grid、长流完整偏移和扩展地址标记。LayerNorm/Softmax 的除法最后一位与饱和分开，系统 top v13 在 3.298 ns synth_design 约束下 WNS 为 0.067 ns，0 个 setup 失败端点；Verilator 11 项和 Icarus 5 项短 smoke 已通过。报告没有把行为级乘法、综合 Fmax 或小动作 smoke 写成完整 TurboVLA/LIBERO 结果。NSTD-1/UCIO-1 仍需板级 pin 约束后才能生成 bitstream。
