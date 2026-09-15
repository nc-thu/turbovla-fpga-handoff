# TurboVLA W8A16 算法语义 v4

生成时间：2026-09-13 15:23:11

本目录固定 TurboVLA 专用的整数边界，不修改原始模型和量化实验。进入矩阵引擎的激活是有符号 INT16，权重是有符号 INT8，乘积在 40-bit 累加器中完成，输出再按静态 scale 饱和为 INT16。

```text
qa = clip(round(x / sa), -32768, 32767)
qw = clip(round(w / sw), -128, 127)
acc = sum(qa * qw)                 # signed INT40
qout = saturate_int16(requant(acc))
```

GELU、LayerNorm、Softmax、tanh 和 bias/add 是独立算子。`A16` 只表示 GEMM 的激活输入宽度，不表示激活函数的位宽。动态 FP32 fake-quant 结果只作数值参考；硬件路径使用编译器 descriptor 中的静态 scale。

## 输入与输出边界

- CTX 每拍提供 16 个 INT16 激活（256 bit），WRAM 每拍提供 48 个 INT8 权重（384 bit）。
- 阵列固定 16 行 × 48 物理列，768 个 DSP；每个 PE 做一路 INT16×INT8。
- GEMM 输出先留在 INT40 快照，重量化后写回 INT16，不能把中间值写成 INT8 再当作 W8A16 输入。
- LayerNorm/Softmax 的除法使用逐位迭代，最后一位和饱和分开，避免把长组合除法接到输出寄存器。
- 向量 scale 使用“乘积寄存器→移位／饱和寄存器”两级路径，顶层时序修复不改变数值公式，只增加一个内部 valid 延迟。

完整 TurboVLA 的 DINO、T5、采样循环和 LIBERO 动作适配尚未放入本目录；对应边界保留在报告中。
