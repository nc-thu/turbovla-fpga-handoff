# TurboVLA FPGA 交接包清单

生成时间：2026-09-15 19:39:43

## 包含内容

| 目录 | 内容 | 来源 |
|---|---|---|
| `design/w8a8_pack2/` | W8A8 Pack2 黄金模型、编译器、周期数据、RTL、仿真和 Vivado 报告 | `E:/GPU ARCH/vector_core_sim/turbovla_w8a8_pack2/` |
| `design/w8a16/` | W8A16 算法、编译器、RTL 源和文本报告（不含权重/DCP） | `E:/GPU ARCH/vector_core_sim/turbovla_w8a16/` |
| `upstream/turbovla_profile/` | 官方源码快照、配置、profiling 结果和 LIBERO 评测 JSON | `E:/GPU ARCH/vector_core_sim/algo/turbovla_profile/2026-09-12_192541/` |
| `results/quantization/` | W8A8/W8A16/W8A-FP16 量化筛选结果 | `E:/GPU ARCH/vector_core_sim/algo/turbovla_quant/2026-09-12_215112/` |
| `results/w8a8_recovery/` | W8A8 整数恢复、误差和周期结果（不含观测 `.pt`） | `E:/GPU ARCH/vector_core_sim/algo/turbovla_w8a8_recovery/2026-09-14_104416/` |
| `paper/template/` | TurboVLA FPGA 论文模板和证据索引 | `E:/GPU ARCH/vector_core_sim/paper/2026-09-12_vla_fpga_r3/` |

## 有意排除

- TurboVLA/HoloBrain checkpoint、`.pt`、`.pth`、`.bin`、`.safetensors` 和原始大张量：体积大，且不适合直接公开。
- Vivado `.dcp`、`.bit`、`.wdb`、`.Xil` 和工程缓存：可由 Tcl 重新生成，单个文件超过 GitHub 普通仓库的实用范围。
- 虚拟环境、Python `__pycache__`、临时日志和重复的旧中间结果。
- GPU 服务器上的私有绝对路径和账号信息。

排除的文件仍在本地原目录保留；需要时可按原目录和报告中的 SHA256 重新取回。

## 证据层级

1. `functional_checks.json`：RTL/Icarus 秒级功能检查。
2. `reports/*_real4/reports/`：Vivado 2021.2 post-route 报告。
3. `data/2026-09-14_115230/`：TurboVLA trace 和 Python 周期模型。
4. `results/`：软件量化、profiling 和误差筛选。

报告中的“实测”仅指对应工具确实运行过的项目；条件模型、行为级 fallback 和 vectorless power 都在文档中单独标出。
