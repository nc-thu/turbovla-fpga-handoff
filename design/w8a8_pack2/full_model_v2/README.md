# TurboVLA W8A8 Pack2 全模型回放版本

更新时间：2026-09-16 03:33:14

这一版把一次真实 TurboVLA dispatch trace 送入一个可综合的 generic top。编译器为 6836 个 dispatch 逐条生成 descriptor，并把矩阵尺寸、地址、stride、scale、布局和依赖放在 descriptor sideband。

## 目前真正进入 RTL 的部分

- 301 个 `GEMM_W8A8` 和 30 个 `BMM_W8A8` 使用 16×48 Pack2 阵列；768 个 Pack2 DSP 每拍产生两个 INT8×INT8 乘积。
- 973 个布局事件、561 个向量事件和 3 个存储事件有对应的 RTL primitive 或存储接口。
- 其余 4968 个事件进入 `AUX_EVENT`/fallback。它们有事件顺序、周期和 payload 位置，但没有被写成完整的 DINO、T5、LayerNorm、Softmax、GELU 或板级 DDR 专用电路。

## 结果边界

- 周期模型：565,587,640 cycles，1.794% PE 时间利用率，61.13% GEMM 利用率，13.78 GOPS@250 MHz。这些数字来自 trace 驱动的 Python 模型。
- Vivado 2021.2：89,795 LUT、193,533 FF、784 DSP、25.5 BRAM、vectorless power 5.733 W。实现已布线，但 4 ns setup WNS=-0.303 ns，250 MHz 约束未通过。
- XSim 宽接口 smoke 通过；generic top 仍未绑定开发板 I/O，尚未进行板级 DDR、bitstream、整模型 FPGA forward 或新的 LIBERO 成功率测试。

不要把 `unknown=0` 当成“所有算子都有专用硬件”。它只表示 trace 中的每个事件都有明确分类。
