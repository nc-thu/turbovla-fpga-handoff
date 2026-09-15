# TurboVLA 十项优化：架构和周期模型

完成时刻：2026-09-14 02:03:37。

`compile_trace.py` 生成的 432 个 descriptor 进入这里的周期核算。模型固定为 16 行 × 48 物理列、768 DSP、250 MHz、每颗 DSP 每拍一个 INT16×INT8 MAC。基线按读、算、快照、重量化、写回和 fallback 串行记账；优化方案对读、算和后处理取最大值并加启动保护拍，因此优化阶段的串行小计不能再次相加。

`selected_optimizations.json` 是本轮十个点的冻结清单。`build_history_summary.py` 从 JSON/CSV 生成阶段、模块、资源和优化效果数据。优化后的 2.070× 是条件模型值，必须用真实双缓冲、端口仲裁和背压 RTL 再验证。
