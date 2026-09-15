# TurboVLA W8A16 架构 v4

生成时间：2026-09-13 14:52:54

`w8a16_system_top` 是一个单时钟、tile 级的硬件壳。它把 64-bit 指令控制器、runtime、256-bit 激活 DMA、384-bit 权重 DMA、向量／激活单元、REQUANT 和 16×48 GEMM 接在同一时钟域。

## 数据路径

1. runtime 接受一个 transport word，按 `flags[7]` 选择小动作路径或生产阵列。
2. LOAD/STORE 命令通过 ready/valid 与 DMA 握手。读回 beat 在 runtime 的 INT16 scratch bank 中落地，写 beat 在背压期间保持稳定。
3. GEMM 由上层 tile scheduler 提供 16 行激活和 48 列权重 feed；阵列完成后从 40-bit snapshot drain。64-bit 指令只负责启动和等待，不携带完整张量。
4. 向量、LayerNorm、Softmax、tanh、GELU、REQUANT 都以有寄存器输出的多拍单元执行。runtime 只在相应单元 `done` 后应答。

## 时序修复

v4 保留 LayerNorm/Softmax 的 `S_SATURATE` 状态，并在向量 `MUL_SCALE` 中加入“32-bit 乘积寄存器→移位/饱和寄存器”一级流水。Vivado 2021.2 对 3.298 ns 目标报告系统 top WNS +0.310 ns、数据路径 2.978 ns；这是逻辑综合估算，尚未经过 place/route。

## 已知集成边界

当前 top 的本地 scratch 是动作 tile 级存储，不是完整 TurboVLA 片上张量存储。长向量由编译器分片，并用 sideband 偏移交给上层 tile scheduler。DINO/T5、真实 RGB-D 搬运、AXI/DDR 板级 pin、功耗、UNISIM 和 LIBERO 环境还没有接入，因此本目录的“camera-ready”指 RTL/ISA 候选版本，不表示整机已经上板。
