# TurboVLA W8A8 Pack2 v7 DMA burst handoff

这是公开交接包中的独立 v7 版本。它包含 Pack2、全模型 descriptor 编译器、DMA bounded burst、64-bit package bridge、Vivado 综合脚本和当前支持矩阵。

## 证据边界

- v7 DMA standalone 和 package bridge smoke 已通过。
- Vivado 2021.2 synthesis 已完成 0 errors/0 critical warnings；4 ns WNS=-0.783 ns，尚未达到 250 MHz，也未做 place/route。
- package top 已支持 host kind 7 的真实 64-bit payload 输入，以及 host kind 2/3 的 DMA 读回输出；但 descriptor 驱动的 CTX/WRAM 自动装载、完整 BMM、精确 FP16 逐位回放、板级 DDR 和 LIBERO FPGA 成功率仍未完成。
- 当前 payload-connected synthesis：138,170 LUT、204,228 FF、849 DSP、46 BRAM tile、vectorless 6.043 W；4 ns WNS=-0.783 ns，仍未达到 250 MHz。

## 目录

- `arch/ARCHITECTURE.md`：架构和支持矩阵。
- `compiler/`：v5 DMA burst compiler。
- `hw/rtl/`：v7 RTL。
- `hw/sim/`：DMA 和 64-bit bridge testbench。
- `hw/vivado/`：Vivado synthesis script and XDC。
- `data/`：machine-readable summary。
- `reports/`：中文状态页。
