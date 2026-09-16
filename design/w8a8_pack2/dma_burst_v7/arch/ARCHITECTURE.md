# TurboVLA W8A8 全模型架构状态（v5 DMA burst 版本）

生成时间：2026-09-16 08:20:00

这份说明对应 `hw/v7_2026-09-16_073705_dma_burst_memory_rtl/` 和
`compiler/v5_2026-09-16_073705_dma_burst_compiler/`。这一版的重点是把 DMA
从“每拍一个地址的接口壳”改成可验证的有界 burst 路径，同时保留之前的
Pack2、向量、BMM staging、CTX/WRAM 和控制器。它不是说 TurboVLA 的所有
算子已经有精确硬件实现。

## 已经接上的数据路径

命令字仍为 64 bit，矩阵尺寸、地址、stride、scale、布局和依赖仍放在
descriptor sideband。Pack2 阵列是 16 行×48 物理列，共 768 个 DSP；每个
物理列对应两个逻辑输出列。CTX 使用 128 bit beat，WRAM 使用 768 bit beat。

DMA 内部使用 128 bit AXI beat。一次请求最多发送 16 个 beat，并且在 4 KB
边界处自动拆分。v7 package wrapper 对外保留 64 bit DDR 流：读方向两拍拼成
一个内部 128 bit beat，写方向把一个内部 beat 拆成两拍。这个桥已经用 80 B
读写测试逐位核对。

## 证据边界

| 级别 | 含义 |
|---|---|
| 精确 RTL | 有可综合模块，且有针对该模块的功能测试。 |
| 行为级辅助 | 顶层能按周期占住时间线并传递摘要或结果，但还没有完整算术电路。 |
| 编译器已分类 | trace 事件有 descriptor 和成本，不等于 RTL 已经实现。 |
| 未完成 | 仍缺真实 payload、完整数据依赖或板级接口，不能写成已支持。 |

## 当前支持矩阵

| 模块 | 编译器 | RTL | 当前能证明的范围 | 仍缺什么 |
|---|---|---|---|---|
| Pack2 GEMM | `GEMM_W8A8` | 16×48 阵列 | Pack2 数学、尾块和顶层 smoke | 全 trace 逐位回放、真实权重流 |
| BMM/attention | `BMM_W8A8` | 双输入 staging、transpose、mask | 2×2 小例子和依赖检查 | QK、softmax、AV 两阶段完整数据流 |
| LayerNorm/Softmax/GELU/tanh | 向量 descriptor | 有界 vector primitive；可选 FP16 IP wrapper | 接口、周期和小例子 | 精确 FP16 IP 工程闭环和逐位对拍 |
| Add/Mul/ReLU/Clamp | 向量 descriptor | 16-lane 基本路径 | 功能 smoke | 所有真实 layout 和广播规则 |
| Conv2d | `CONV_IM2COL` | 小型 im2col/行为级路径 | 形状和搬运成本可记录 | 通用 stride/padding/权重流 |
| Embedding/position | `EMBED`/`POSENC` | 部分地址和位置路径 | 小例子 | 完整表、cos/sin 和缓存一致性 |
| Layout | `LAYOUT` | 部分 transpose/gather/scatter | descriptor 可发出 | 通用 reshape/permute/slice/cat |
| CTX/WRAM | memory descriptor | BRAM 推断、双结果缓冲 | Vivado 能推断 46 个 BRAM tile | 真实 activation/weight payload 装载 |
| DMA/AXI | `DMA_READ/WRITE` | v7 有界 burst + 64-bit 桥 | standalone 与 package bridge 测试 | 板级 DDR 控制器、真实 payload 端口 |
| DINO/T5/action head | GEMM + AUX 分类 | 没有完整专用电路 | compiler 可拆事件 | 层循环、残差、权重和中间张量 |
| 全 trace replay | descriptor 全覆盖 | 未完成 | Python 周期模型对账 | Verilator 全 trace 和真实结果回放 |
| LIBERO/FPGA 闭环 | 记录为外部任务 | 未完成 | 软件 fake-quant 背景数据 | 板级运行和新的 W8A8 成功率 |

## v7 DMA 设计取舍

burst 长度上限设为 16 beat，是为了先验证地址、4 KB 边界、尾 beat strobe
和 backpressure，而不是假设 DDR 一定能持续满带宽。当前 TurboVLA trace 没有
显式 `dma_read`/`dma_write` dispatch，因此这轮编译器新增的 DMA 字段尚未在
真实 trace 周期里产生节省；DMA 单元测试负责证明路径本身可用。

package top 没有板级 128 bit payload 端口。为避免未驱动输入在综合时变成
不可控状态，当前内部 stream 使用确定性的零填充 tie-off。这是安全的验证默认值，
不是生产 payload 路径。下一步应把 CTX/WRAM 的实际加载 FIFO 接到这个端口，
再做真实 DDR 回放。

## Vivado 观察

v7 在 `xczu7ev-ffvc1156-2-e` 上完成综合，目标时钟 4.000 ns。综合没有 error，
但 WNS 为 -0.783 ns，所以 250 MHz 仍未通过。综合资源为 138,068 LUT、203,455 FF、
849 DSP 和 46 BRAM tile。849 个 DSP 中除了 768 个 Pack2 DSP，还包括向量、布局和
其它辅助乘法器；不能把它写成“整个顶层只有 768 DSP”。vectorless 功耗是 5.966 W，
没有 SAIF/VCD 且尚未 place/route，只能作为低置信度估计。

后续优先级是：先补真实 payload FIFO，再把 FP16 向量 IP 与时序寄存器接好；然后
实现 BMM 的 QK/AV 全链路，最后才做完整 trace 的 RTL 回放和板级 DDR。
