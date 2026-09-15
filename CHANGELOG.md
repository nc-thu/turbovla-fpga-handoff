# 交接包变更记录

## 2026-09-15 19:39:43

- 建立 `turbovla-fpga-handoff` 独立目录，汇总 TurboVLA 的 W8A8 Pack2、W8A16 参考实现、编译器、周期模型、profiling、论文模板和验证资料。
- 只复制可复现所需的源码、脚本、机器可读结果和报告；没有复制 checkpoint、原始大张量、Vivado 工程缓存、`.dcp` 或板级产物。
- 纳入新的 Vivado 2021.2 实现记录：250 MHz 约束下 post-route WNS +0.241 ns、推导 Fmax 266.0 MHz；303.215 MHz 目标下 post-route WNS +0.103 ns、推导 Fmax 313.0 MHz。两次 routing error 均为 0。
- 功耗仍是 vectorless 估算，顶层 I/O 尚未绑定开发板约束，因此不把该结果写成板级可用性或 TOPS/W。

## 2026-09-15 23:41:16

- 新增 `docs/FULL_MODEL_COVERAGE.md`，把 408 个模块事件、6836 个 dispatch 事件、432 个 descriptor 以及当前 RTL 实际识别的命令范围逐项拆开。
- 明确 `unknown_event_count=0` 只表示模块分类没有落入未知分支，不代表所有底层 dispatch 都已经有硬件指令；LayerNorm、Softmax、GELU、Conv/im2col、embedding、布局变换、DMA/DDR 和动作后处理仍未形成当前 Pack2 的完整硬件路径。

## 交接后的第一步

先阅读 `README.md`、`docs/RESULTS.md` 和 `HANDOFF_MANIFEST.md`，再运行 `scripts/run_pack2_checks.ps1 -What all`。如果需要重做 Vivado，实现脚本和原始 Tcl 位于 `design/w8a8_pack2/hw/v3_2026-09-15_174639_vivado_impl/`。
