# 修改说明

生成时间：2026-09-13T15:30:38+08:00

本版在 v3 的动作后处理、LayerNorm/Softmax 迭代路径、DMA 数据落地、生产阵列启动和完整 sideband 基础上，给 vector_mul 增加‘乘积寄存器→移位／饱和寄存器’一级流水。v4 系统 top 使用 3.298 ns synth_design 约束，WNS 为 0.31 ns，0 个 setup 失败端点；Verilator 11 项和 Icarus 5 项短 smoke 已通过。array_1x1/4x4/16x48 的资源和时序记录继承 v3，因为 array top 不实例化 vector_mul，并在机器可读结果中显式标记。报告没有把行为级乘法、综合 Fmax 或小动作 smoke 写成完整 TurboVLA/LIBERO 结果。NSTD-1/UCIO-1 仍需板级 pin 约束后才能生成 bitstream。
