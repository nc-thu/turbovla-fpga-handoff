# TurboVLA W8A16 周期模型

主阵列是 16 行 × 48 物理列，每个 PE 只有一路 INT16×INT8 乘法。一个完整 tile 的周期包含波前填充、排空、激活／权重读取、快照、重量化和 INT16 写回。

模型把阵列计算利用率和算子完成率分开。前者只看实际完成的 MAC，后者还包括数据搬运和控制开销。任何未支持的归一化、GELU、Softmax、采样、RGB 预处理或动作后处理都保留为独立成本。`data/isa_spec.json` 是指令与存储口的机器可读定义；真实模型的 BMM、卷积展开和 fallback 仍需要运行时 trace 才能核对。

## 运行时单元

`w8a16_vector_ops` 将 BIAS_ADD、残差 ADD、MUL_SCALE、ReLU、GELU、tanh、LayerNorm 和 Softmax 接到同一个单向量命令接口。GELU、tanh 和 LayerNorm 是有界定点实现，适合先做周期和边界验证，不等价于 FP32 网络。

`w8a16_dma` 使用 256-bit CTX 口和 384-bit WRAM 口；`w8a16_isa_ctrl` 译码 64-bit transport word；`w8a16_runtime` 连接 DMA、阵列、向量单元和动作输出的最小命令路径。
