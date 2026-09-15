# TurboVLA complete-model v3

更新时间：2026-09-16 05:51:14

这一版把真实 TurboVLA forward 的 6,836 个 dispatch 逐项编译成 descriptor，并在一个可综合顶层中放入 Pack2 GEMM/BMM、vector/FP16 槽、Conv/im2col、Embedding/position、layout、mask、CTX/WRAM、DMA/AXI、控制器和 action post。

## 运行结果

- 编译器：`unknown=0`，331 个 Pack2 GEMM/BMM，输出见 `data/`。
- Icarus：`COMPLETE_MODEL_SMOKE PASS`（只覆盖算子连接和握手，不是完整 trace 逐位回放）。
- Vivado 2021.2、`xczu7ev-ffvc1156-2-e`、4.000 ns：117,482 LUT、198,003 FF、817 DSP、46 BRAM tile、247 IOB；post-route WNS=-0.522 ns，250 MHz 未通过。
- vectorless power=6.885 W；没有 SAIF/VCD，不能换算 TOPS/W。

## 证据边界

这些文件支持架构和编译器复现。它们不包含 checkpoint、DCP、bitstream 或服务器绝对路径。当前仍未完成精确 FP16 IP、完整 DINO/语言 encoder/action head、训练权重和 scale 的真实流入、板级 DDR/PHY、Verilator 全 trace 回放和 LIBERO 闭环。请先读 `reports/` 下的中文说明页。

```powershell
python compiler/compile_complete_model.py --help
python -m py_compile compiler/compile_complete_model.py
```
