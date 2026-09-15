# 当前 TurboVLA 软硬件交接说明

更新时间：2026-09-16 03:33:14

## 一句话说明

TurboVLA 的真实算子记录先由专用编译器变成 64-bit command word 加 descriptor sideband，再由 Pack2 16×48 阵列执行能映射的 W8A8 GEMM/BMM。LayerNorm、GELU、Softmax、DINO、语言编码和其他还没有对应 RTL 的部分，仍以 fallback/AUX 事件保留在周期时间线中。

## 数据流

1. `upstream/turbovla_profile/` 保存官方 TurboVLA 代码快照、输入形状和 LIBERO profiling 结果。
2. `design/w8a8_pack2/compiler/` 读取 operator trace，枚举 Linear、GEMM、BMM、Conv 和向量算子。
3. 编译器输出 `instructions.hex`、`descriptors.jsonl`、依赖图、scale 表和周期/流量明细。
4. RTL 的 replay top 先从 descriptor FIFO 取任务，再从 CTX/WRAM 读取 INT8 activation/weight，交给 16×48 Pack2 阵列。
5. 一个 DSP 产生两个 INT8×INT8 乘积；字段校正后进入两条 INT32 累加反馈，结果经过 snapshot、requant 和 INT8 写回。
6. 暂无专用硬件的算子通过 AUX/fallback 占用事件周期，并能把软件结果写回 CTX，供后续 GEMM 使用。

## 指令和接口

command word 只放 opcode、flags、descriptor id 和短长度。矩阵尺寸、地址、stride、scale、layout、valid mask 和依赖全部放在 sideband，避免把 64-bit 指令塞满后丢字段。

| 接口 | 宽度 | 作用 |
|---|---:|---|
| activation | 128 bit | 16 个 INT8 激活输入 |
| weight | 768 bit | 48 组 Pack2 权重 |
| output | 128 bit | 16 个 INT8 输出 |
| accumulator | 32 bit | 每个逻辑输出的精确累加 |
| snapshot | 27 bit | 行级读出快照，K 很大时由编译器做边界保护 |

## 资源组织

主阵列共有 768 个 DSP，物理尺寸为 16 行 × 48 列，每个物理列对应两个逻辑输出列，总计 96 个逻辑列。输入寄存、DSP P 输出寄存、校正寄存和阵列读出寄存器把长路径切开。双结果缓冲、读算写重叠和兼容任务队列属于调度/周期模型选项，不能直接等同于已测得的端到端吞吐。

## 版本关系

- `design/w8a8_pack2/` 是当前主线，包含最终重跑的 Vivado v3 实现结果。
- `design/w8a16/` 是前一条 W8A16 研究线，不能与 W8A8 的 DSP 峰值混写。
- `results/` 是软件实验快照。它们支持量化和形状分析，不自动证明 FPGA 上已经完成相同算子。

## 2026-09-16 全模型版本

`design/w8a8_pack2/full_model_v2/` 在同一 Pack2 阵列外增加了向量、布局、embedding/position、im2col、BMM 行缓存、CTX/WRAM、行为级 DMA、FP16 接口占位和动作后处理。它的目的，是把真实 TurboVLA trace 的事件顺序送入一个可综合 generic top；它不是已经能在开发板上独立执行全模型的设计。

编译器对 6836 个 dispatch 逐条生成 descriptor，统计为 301 个 Pack2 GEMM、30 个 Pack2 BMM、973 个 layout、561 个 vector、3 个 memory，以及 4968 个 AUX/fallback。`unknown=0` 只表示每个事件都有分类，不能理解为每个事件都有专用 RTL。最终实现使用 784 个 DSP（768 个 Pack2 + 16 个向量乘法）、25.5 BRAM，4 ns setup WNS=-0.303 ns，尚未达到 250 MHz。
