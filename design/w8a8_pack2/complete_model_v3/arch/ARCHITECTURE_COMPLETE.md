# TurboVLA W8A8 Pack2 完整执行架构

生成时间：2026-09-16 03:46:53

## 目标

这一版把 TurboVLA 的一次完整推理拆成可以执行的硬件任务，而不是只给未支持算子记一个 fallback 周期。编译器为每个任务生成 descriptor，顶层根据 opcode 把任务送到 Pack2、向量/FP16、布局、卷积、Embedding、BMM、片上存储或 DMA 单元。

Pack2 阵列保持 16 行×48 物理列、768 DSP 和 96 个逻辑列。Linear 以及满足布局条件的 BMM 使用 INT8×INT8、INT32 累加。归一化、Softmax、GELU 等数值敏感算子可选择 FP16 参考单元或有界定点单元；两条路径使用同一握手协议，便于在 Vivado 工程中替换。

## 完整执行单元

| 单元 | 负责的工作 | 结果格式 | 当前版本 |
|---|---|---|---|
| Pack2 GEMM | Linear、兼容 BMM 的乘加 | INT32 → INT8 | 16×48 可综合阵列 |
| FP16/vector ALU | LayerNorm、Softmax scaling/mask/exp、GELU、ReLU、tanh、Bias/Add/Mul | FP16 或 INT16 | 可综合参考实现，FP16 IP 预留接口 |
| Conv/im2col | Conv2d 窗口展开和输出流 | INT16/INT8 | 流式窗口单元 |
| Embedding/position | token embedding、位置表、cos/sin | FP16/INT16 | 可写表 + 查表接口 |
| Layout | transpose、permute、reshape、slice、cat、gather/scatter | 原格式 | 地址/数据重排单元 |
| BMM scheduler | 双输入检查、转置、mask、缩放、QK/AV 阶段依赖 | INT8/INT32/FP16 | 显式阶段控制 |
| CTX/WRAM | 激活、权重和中间结果片上缓存 | 256/768-bit beat | 双口 BRAM 接口 |
| DMA/AXI | DDR 与片上缓存之间的 burst 读写 | 128/256-bit beat | AXI master 事务状态机 |
| Model controllers | DINO、语言编码器和 action head 的层循环 | descriptor stream | 共享计算单元，不复制整套阵列 |
| Action post | 采样、反量化、clamp、gripper 和机器人接口 | FP16/定点 action | 顺序输出接口 |

## 运行方式

1. 编译器读取 dispatch trace，保留原始顺序、shape、stride、scale、layout 和依赖。
2. scheduler 检查依赖和资源冲突；需要重排的 BMM 先经过 layout/BMM 单元。
3. 片上缓存提供当前 tile。Pack2 或向量/FP16 单元执行，结果写回 CTX。
4. barrier 在残差、归一化、激活和采样边界处保证顺序；双结果缓冲允许读、算、写重叠。
5. action post 输出完整 action chunk，同时 activity monitor 记录每类单元的周期、流量和等待原因。

## 数值边界

- W8A8 部署路径：signed INT8 activation/weight、INT32 accumulator、INT8 output。
- LayerNorm/Softmax/GELU 等可以走 FP16 IP 插槽；未生成 vendor IP 时使用同接口的定点参考路径，报告必须把两者分开。
- bias、动态 scale 和反量化不再按零成本处理，必须由 descriptor 指定来源和周期。
- 动态 BMM 必须同时检查两个输入和布局。任何不满足条件的任务进入 BMM 重排路径，而不是只检查一个操作数。

## 证据边界

本目录描述的是完整执行架构和接口；真正的逐位回放、Vivado 资源和时序以同一时间戳的 `hw/`、`data/` 和 `reports/` 为准。只有通过 RTL 仿真并在 Vivado 中实现的模块，才能称为“已有电路”。
