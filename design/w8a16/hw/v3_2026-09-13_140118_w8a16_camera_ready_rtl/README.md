# TurboVLA W8A16 RTL v3

生成时间：2026-09-13 14:52:54

## 入口

- `synth/top_w8a16_system.sv`：包含 runtime、双 DMA、向量／激活单元、REQUANT 和 16×48 GEMM 的系统 top。
- `synth/top_w8a16_array.sv`：只展开 GEMM 阵列，用于 1×1、4×4、16×48 资源和时序对照。
- `synth/syn_top.tcl`：Vivado 2021.2 非工程综合脚本，目标时钟 3.298 ns。
- `sim/run_verilator.sh`：服务器快速回归；`sim/run_iverilog_smoke.sh`：秒级短 smoke。

## v3 验证记录

- Verilator：11 项通过；包含 PE、阵列、完整阵列 wrapper、GEMM、REQUANT、激活、向量、DMA、ISA、runtime 和 system。
- Icarus：5 项短 smoke 通过。
- Vivado：1×1/4×4/16×48 阵列和 system top 的 `synth_design` 均通过；系统 top 785 DSP、67,432 LUT、118,139 FF、0 BRAM，WNS +0.067 ns。
- DSP 对应关系保持 1 PE = 1 DSP、4×4 = 16 DSP、16×48 = 768 DSP。system top 多出的 DSP 来自动作路径中的小型乘法单元。

## 不能省略的边界

仿真使用行为级乘法，服务器没有 `xvlog`，所以 UNISIM/DSP48E2 仍未跑。Vivado OOC 没有板级 I/O pin 约束，NSTD-1/UCIO-1 需要在具体板卡工程中处理；当前结果不是 bitstream-ready，也不是 post-route 频率。
