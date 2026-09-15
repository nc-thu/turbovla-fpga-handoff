# TurboVLA W8A8 Pack2 全模型编译器（2026-09-16 01:00:24）

`compile_full_model.py` 读取真实 `operator_trace.jsonl`，按一次 dispatch 生成一个 descriptor，避免把 module hook 与子算子重复计算。Linear、可兼容 BMM、向量算子、布局、内存和 action 后处理都有明确分类；暂时没有专用整数电路的算子会落到 `aux_behavior`，不会被默认为零成本。

输出包括 `descriptors.jsonl`、`instructions.hex`、`dependency_graph.json`、`cycle_breakdown.csv` 和 `coverage_summary.json`。命令字只有 64 bit，矩阵尺寸、地址、stride、scale、布局和依赖都在 descriptor sideband 中。
