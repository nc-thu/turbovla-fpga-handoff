# TurboVLA W8A16 指令路径

更新时间：2026-09-13 01:25:00（本地工作记录时间）

这一版先把“编译器发什么、硬件收什么、动作怎样出来”固定下来。每条 transport word 为 64 bit：`opcode[63:56]`、`flags[55:48]`、`dst[47:40]`、`src0[39:32]`、`src1[31:24]`、`length[23:8]`，最低 8 bit 保留。矩阵尺寸、stride、scale ID 和 fallback 原因放在 JSON 描述符里，不挤进固定宽度的命令字。

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

`compile_program.py` 生成 83 条完整示例指令和 7 条小型动作指令。`isa_sim.py` 先验证 90 个字都能从同一份 `isa_spec.json` 解码，再用固定 1×7×8 整数矩阵生成七维 Q15 动作。Verilator runtime 使用同样的 word 顺序，输出打包值与 Python 结果逐位相同。

这条路径不是完整 TurboVLA 推理：DINO、T5、采样循环、真实权重搬运、完整动作头和 LIBERO 环境步进还没有接到 RTL。向量单元的测试证明命令和饱和边界正确，不能证明定点 GELU、LayerNorm 或 Softmax 与 FP32 模型的输出逐位相同。
