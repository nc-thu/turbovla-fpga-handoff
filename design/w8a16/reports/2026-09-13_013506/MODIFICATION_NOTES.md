# 本轮修改说明

生成时间：2026-09-13T01:35:06+08:00（Asia/Shanghai）

这轮把 TurboVLA W8A16 的工作范围从单独 GEMM 扩到了一个可检查的命令路径：编译器生成 64 bit 指令字，ISA 控制器负责取指和结束，DMA 负责 CTX/WRAM 的读写，向量单元提供加法、缩放、ReLU、GELU、tanh、LayerNorm、Softmax 和重新量化，runtime 将动作投影接到 LIBERO 格式的七维动作输出。

服务器 Verilator 回归在 `/home/nc23/experiments/turbovla_w8a16/2026-09-13_010117` 完成，10 项通过；Icarus 四项短 smoke 通过。Python 编译器／解码／整数对拍也通过，90 个实际调度字和 18 个 opcode 目录项均可解码。

这轮没有获得 PPA 提升数字：Vivado、UNISIM 和 post-route 工具不可用，因此资源、频率、功耗仍是“未做”。runtime 只执行一个小型 1×7×8 动作投影命令路径，使用确定性的格式化 INT16 状态向量，输出与 Python 整数模型一致；它不包含真实 RGB-D 张量、DINO/T5、完整 TurboVLA 采样、真实权重流和 LIBERO 环境步进。
