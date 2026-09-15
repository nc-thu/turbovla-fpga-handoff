# TurboVLA 真实 trace 编译器

完成时刻：2026-09-13 23:29:14。

`compile_trace.py` 读取模块和 dispatch JSONL，按 16×48 tile 生成 W8A16 descriptor、周期和流量；`emit_replay_stream.py` 再生成 512-bit descriptor word 和 64-bit command word。Linear 进入 `rtl_gemm`，满足布局条件的动态 BMM 进入 `rtl_bmm`，向量与暂时没有专用阵列的算子保留行为级事件。

本轮输入覆盖 408 个模块事件和 24 个动态 BMM，生成 432 个 descriptor，unknown=0。编译器不修改共享接口。
