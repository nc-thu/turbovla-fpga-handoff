# TurboVLA 活动回放与周期模型

完成时刻：2026-09-14 00:50:25。

`validate_replay.py` 检查 descriptor、依赖、覆盖、周期和流量对账，并运行 INT64→INT40→INT16 的边界黄金模型。完整 trace 在顶层按 descriptor 累加虚拟周期；代表性 2×3、K=5 tile 走真实阵列逐拍验证。两项 Verilator 检查和顶层 activity counter 对账均通过。
