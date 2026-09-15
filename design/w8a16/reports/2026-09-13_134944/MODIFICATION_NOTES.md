# 修改说明

生成时间：2026-09-13T13:49:44+08:00

本版把 v2 的动作后处理、LayerNorm/Softmax 迭代路径、DMA 数据落地、生产阵列启动和长向量分片统一归档。v11 系统 top 在 3.298 ns synth_design 约束下 0 个 setup 失败端点；Verilator 11 项和 Icarus 5 项短 smoke 已通过。报告没有把行为级乘法、综合 Fmax 或小动作 smoke 写成完整 TurboVLA/LIBERO 结果。
