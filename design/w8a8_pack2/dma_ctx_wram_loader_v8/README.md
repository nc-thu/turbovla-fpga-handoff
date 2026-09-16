# v8 descriptor-driven DMA to CTX/WRAM

版本时间：2026-09-16 09:32:40

这一版补的是一个具体的数据路径缺口：编译器在 descriptor sideband 中指定 DMA 读回数据的目标，RTL 再把真实 payload 写进片上 CTX 或 WRAM。它不是完整 TurboVLA FPGA 实现，也没有覆盖旧版本目录。

## 已通过的检查

- `scripts/test_v6_dma_descriptor.py`：编译器把 `DMA_READ`、目标和字节长度编码到 sideband，PASS。
- `sim/tb_dma_ctx_wram_loader.sv`：CTX 2 个 128-bit beat 和 WRAM 6 个 128-bit beat，PASS。
- `sim/tb_package_dma_loader.sv`：64-bit 外部流经过 package top 拼成内部 128-bit beat，随后检查 CTX 地址 3/4 和 WRAM 地址 5，PASS。
- package top 用 `iverilog -g2012 -DVERILATOR` 编译，PASS。

## 数据格式

| 字段 | 口径 |
|---|---|
| sideband 目标 | `[497:496]`: `0=CTX`, `1=WRAM`, `2=host` |
| 外部板级流 | 64 bit |
| 内部 DMA beat | 128 bit |
| CTX 写入 | 每个 beat 写一个 128-bit word |
| WRAM 写入 | 6 个 beat 拼成一个 768-bit row |

## 尚未完成

- v8 loader 尚未重新运行 Vivado；仓库中的最新物理数字仍来自 v7 payload package top。
- 还没有把 TurboVLA 的真实 activation/weight payload 从 trace 提取出来并进行完整 RTL replay。
- BMM 的 QK、scale/mask、Softmax、AV 仍未组成完整数值链。
- DINO、语言编码器、action head 的权重流和残差中间张量仍不是专用 FPGA 电路。
- 没有板级 DDR、完整 LIBERO FPGA 闭环或 TOPS/W 测量。

机器可读支持矩阵在 `data/support_matrix_v8.json`，本轮说明页在 `reports/2026-09-16_093240/`。
