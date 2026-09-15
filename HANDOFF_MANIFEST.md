# TurboVLA FPGA 交接包清单

生成时间：2026-09-16 03:33:14

## 包含内容

| 目录 | 内容 | 来源 |
|---|---|---|
| `design/w8a8_pack2/` | W8A8 Pack2 黄金模型、编译器、周期数据、RTL、仿真和 Vivado 报告 | `E:/GPU ARCH/vector_core_sim/turbovla_w8a8_pack2/` |
| `design/w8a16/` | W8A16 算法、编译器、RTL 源和文本报告（不含权重/DCP） | `E:/GPU ARCH/vector_core_sim/turbovla_w8a16/` |
| `upstream/turbovla_profile/` | 官方源码快照、配置、profiling 结果和 LIBERO 评测 JSON | `E:/GPU ARCH/vector_core_sim/algo/turbovla_profile/2026-09-12_192541/` |
| `results/quantization/` | W8A8/W8A16/W8A-FP16 量化筛选结果 | `E:/GPU ARCH/vector_core_sim/algo/turbovla_quant/2026-09-12_215112/` |
| `results/w8a8_recovery/` | W8A8 整数恢复、误差和周期结果（不含观测 `.pt`） | `E:/GPU ARCH/vector_core_sim/algo/turbovla_w8a8_recovery/2026-09-14_104416/` |
| `paper/template/` | TurboVLA FPGA 论文模板和证据索引 | `E:/GPU ARCH/vector_core_sim/paper/2026-09-12_vla_fpga_r3/` |
| `support/arch_gemm_util_v8/` | GEMM 利用率和写回周期模型的辅助脚本 | `E:/GPU ARCH/vector_core_sim/arch/v8_2026-09-11_2315_gemm_util_design/` |
| `support/compiler_v7/` | 兼容任务队列和描述符编译的历史参考 | `E:/GPU ARCH/vector_core_sim/compiler/v7_2026-09-10_1258_f4_ybase_pong/` |
| `scripts/`、`package_inventory.json` | 交接包复现入口和逐文件 SHA256 清单 | 本交接包生成 |

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

## 2026-09-16 新增全模型版本

- `design/w8a8_pack2/full_model_v2/`：真实 TurboVLA trace 的全模型编译器、descriptor/ISA 说明、Pack2/向量/布局/存储/AUX 集成 RTL、XSim smoke 和最终中文报告。
- 全模型报告：`design/w8a8_pack2/full_model_v2/reports/2026-09-16_033314_TurboVLA全模型电路与编译器分析.html`。
- 报告摘要中的 Vivado 目录是本地生成目录 `vivado_runs_20260916_0248`；仓库只保留可复现脚本和必要的文本报告，不公开 `.dcp`、`.bit`、模型权重或仿真缓存。
- 这一版的 setup WNS=-0.303 ns，250 MHz 未通过；DRC 没有 Error，但 generic top 仍有未绑定板级 I/O 的 Critical Warning。

报告中的“实测”仅指对应工具确实运行过的项目；条件模型、行为级 fallback 和 vectorless power 都在文档中单独标出。

## 2026-09-16 05:51:14 新增完整算子版本

- `design/w8a8_pack2/complete_model_v3/`：完整算子编译器、架构说明、RTL、Icarus smoke、周期数据和中文报告。
- 输入来自一次真实 TurboVLA forward。编译器生成 6,836 descriptors、6,837 command words，`unknown=0`；`data/` 中保留机器可读摘要，不包含模型权重或大张量。
- 实现入口为 `rtl/tvla_complete_model_package_top.sv`。Vivado 2021.2 已完成综合、布局布线、DRC 和 vectorless power；资源 117,482 LUT、198,003 FF、817 DSP、46 BRAM、247 IOB，4 ns WNS=-0.522 ns，vectorless power=6.885 W。
- 报告：`design/w8a8_pack2/complete_model_v3/reports/2026-09-16_055114_TurboVLA全模型电路与编译器分析.html`。
- 明确未包含：DCP/bitstream、checkpoint、真实板级 DDR/PHY、精确 FP16 IP、完整 DINO/T5/action-head 专用电路、Verilator 全 trace 和 LIBERO 端到端成功率。

## 2026-09-16 07:20:00 新增 complete_model_v4

- `design/w8a8_pack2/complete_model_v4/` 是 v6 的公开交接快照，包含 TurboVLA 完整 trace 编译器、512-bit descriptor sideband、BMM 双输入 staging、scale/bias 两拍 loader、RTL 小测试、Vivado 综合脚本/报告和中文状态页。
- 编译器输出：6,836 descriptors、6,837 command words、`unknown=0`；数据文件不包含 checkpoint 或原始大张量。
- Icarus：`COMPLETE_MODEL_SMOKE PASS`、`DESCRIPTOR_SIDEBAND PASS`、`BMM_LAYOUT PASS`、`SCALE_TABLE PASS`、`PACKAGE_SCALE PASS`。
- Vivado project-mode synthesis：127,303 LUT、200,791 FF、854 DSP、46 BRAM；4 ns setup WNS=-0.751 ns、TNS=-153.891 ns。综合 0 Error，但没有通过 250 MHz，也没有完成 v6 place/route。
- 公布边界：LayerNorm/Softmax/GELU/tanh 完整数值链、DINO/T5/action-head 专用电路、真实 checkpoint payload/DDR、full-trace Verilator、板级动作回放和 LIBERO W8A8 成功率仍未完成。报告与 README 将这些项目逐项列出，没有把 fallback 或接口占位写成已完成电路。
- 报告：`design/w8a8_pack2/complete_model_v4/reports/2026-09-16_070844_TurboVLA全模型v6架构与实现状态.html`。
