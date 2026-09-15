# TurboVLA W8A16 指令路径

更新时间：2026-09-13 13:08:00（v2 camera-ready 修订）

这一版把编译器发出的命令和硬件实际接收的内容写清楚。每条 transport word 为 64 bit：`opcode[63:56]`、`flags[55:48]`、`dst[47:40]`、`src0[39:32]`、`src1[31:24]`、`length[23:8]`，最低 8 bit 保留。矩阵尺寸、stride、scale ID 和 fallback 原因放在 JSON 描述符里，不挤进固定宽度的命令字。

## 指令分组

| 组 | 指令 | 实际硬件单元 |
|---|---|---|
| 读写 | `LOAD_CTX`、`LOAD_WEIGHT`、`STORE_CTX`、`STORE_ACTION` | DMA；CTX 256 bit，WRAM 384 bit |
| 矩阵 | `GEMM_W8A16`、`BMM_W8A16` | 16×48 阵列；A16×W8；INT40 |
| 向量 | `BIAS_ADD`、`ADD`、`MUL_SCALE` | 饱和加法和定点乘缩放 |
| 激活 | `RELU`、`GELU`、`TANH` | 定点、分段或查表近似 |
| 归一化 | `LAYER_NORM`、`SOFTMAX` | 有界定点统计、指数查表和归一化 |
| 控制 | `WAIT`、`BARRIER`、`END` | 顺序、依赖和任务结束 |

## 当前可验证范围

`compile_program.py` 先生成 83 条逻辑指令，再把超过 16 bit transport length 的向量搬运拆成连续片段，得到 172 条可发送的完整 transport word；另外生成 7 条小型动作 smoke 指令和 18 条 opcode catalog 项。每个拆分片段保留 `logical_length`、`chunk_index`、`chunk_count` sideband，因此拆分不会改变逻辑张量范围。`isa_sim.py` 会从同一份 `isa_spec.json` 检查 transport word 的 opcode、字段和结束标记，再用固定 1×7×8 整数矩阵生成七维 Q15 动作。Verilator runtime 使用同样的 word 顺序，输出打包值与 Python 结果逐位相同。

矩阵 word 的 `flags[7]` 选择 16×48 生产阵列；动作 smoke 清零该位，使用本地 1×7×8 路径。阵列输入和快照输出是独立的 ready/valid 流，由 tile scheduler 根据 descriptor 的 M/N/K、布局和 scale sideband 驱动。这样不会把小型动作验证误报成完整 TurboVLA 张量已经在阵列上运行。

这条路径仍不是完整 TurboVLA 推理：DINO、T5、采样循环和 LIBERO 环境步进没有接到 RTL。DMA 的片上 beat 已接入 runtime 的本地向量／权重 bank，但完整模型的张量切片和外部 tile scheduler 仍需上层系统提供。向量单元的测试证明命令和饱和边界正确，不能证明定点 GELU、LayerNorm 或 Softmax 与 FP32 网络的输出逐位相同。
