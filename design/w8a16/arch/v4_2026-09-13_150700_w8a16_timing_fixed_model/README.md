# TurboVLA W8A16 架构（v4 timing-fixed camera-ready candidate）

更新时间：2026-09-13 15:23:11

主计算阵列是 16 行 × 48 物理列。每个 PE 使用一颗 DSP，计算一个 INT16 activation × INT8 weight，并用 40 bit 保存累加结果。输入从 CTX 以 256 bit beat 进入，权重从 WRAM 以 384 bit beat 进入；输出在写回前保持 INT16。

系统 top 由四块组成：64 bit 指令接收器、带本地 scratch bank 的 runtime、两条 DMA ready/valid 通道和生产 GEMM 阵列。runtime 会等待对应单元的 done 信号；LayerNorm、Softmax、tanh 和向量乘法都采用多拍／寄存器路径，不把宽除法或乘法放在一拍里。

矩阵指令的 `flags[7]` 选择路径。清零时使用小型 1×7×8 动作投影，便于逐位对拍；置位时由 runtime 发出 `gemm_start_cmd`，等待 16×48 阵列完成，外部 tile scheduler 通过 feed/drain 接口提供实际张量切片。这样一个 64 bit word 不会被误解成能携带完整大矩阵。

DMA LOAD 返回的数据会写入 runtime 的 16-lane INT16 scratch 和 48-byte INT8 weight window；STORE 在命令接收时锁存 beat，遇到 back-pressure 仍保持数据不变。超过本地窗口的模型张量必须由上层 scheduler 以多个 tile 命令搬运。v4 的 `MUL_SCALE` 结果增加一级寄存器，runtime 的 valid/done 握手已经在 Verilator 回归中覆盖。

归一化和 Softmax 的硬件 primitive 使用有界整数统计、指数查表和逐位除法。它们的 gamma、beta、mask 仍通过 descriptor sideband 传入；没有这些 sideband 时，编译器会标记 `mapped_candidate`，不会声称与 FP32 网络逐位一致。DINO、T5、采样循环和 LIBERO 环境步进不在本 RTL top 内。
