# TurboVLA FPGA accelerator handoff

生成时间：2026-09-16 03:33:14（交接包整理时刻）

这个仓库把目前 TurboVLA 相关的四部分工作放在一起：软件量化与 profiling、Pack2 编译器、周期模拟器，以及可综合的 W8A8 Pack2 RTL。它用于架构师接手和复现实验，不把旧的 HoloBrain 工程混进来。对应的 GitHub 仓库是 `nc-thu/turbovla-fpga-handoff`，当前可见性为 **PUBLIC**。

## 先看哪些文件

- `docs/ARCHITECTURE.md`：当前硬件、指令格式和软件到 RTL 的关系。
- `docs/FULL_MODEL_COVERAGE.md`：逐项说明全模型哪些算子已有电路、哪些只有编译器占位、哪些还没有进入指令流。
- `docs/RESULTS.md`：已经跑过的功能检查、Vivado 实现结果和仍未验证的部分。
- `design/w8a8_pack2/`：当前主线。包括黄金模型、编译器、16×48 Pack2 阵列、时序版 top、Vivado Tcl 和报告。
- `design/w8a8_pack2/full_model_v2/`：2026-09-16 的全模型 trace 编译器、Pack2/向量/布局/存储/AUX 集成顶层和回放报告。这里的 AUX 仍是行为级时间线，不等于专用电路。
- `design/w8a16/`：此前的 W8A16 版本，只作为参考，不代表当前 W8A8 设计。
- `upstream/turbovla_profile/`：TurboVLA 官方代码快照、LIBERO profiling 结果和版本信息。
- `results/`：量化筛选、W8A8 整数恢复和 profiling 的机器可读结果。
- `scripts/`：不依赖本机绝对路径的复现入口。

## 当前 W8A8 Pack2 实现结果

本交接包使用 `xczu7ev-ffvc1156-2-e` 和 Vivado 2021.2。`design/w8a8_pack2/hw/v3_2026-09-15_174639_vivado_impl/` 保留了原始报告。

| 时钟约束 | post-route WNS | 推导 Fmax | LUT | FF | DSP | BRAM | vectorless 功耗 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 4.000 ns（250 MHz） | +0.241 ns | 266.0 MHz | 77,770 | 179,363 | 768 | 0 | 5.310 W |
| 3.298 ns（303.215 MHz） | +0.103 ns | 313.0 MHz | 77,860 | 179,320 | 768 | 0 | 6.924 W |

两个运行都完成了综合、布局和布线，routing error 为 0。顶层是 generic wrapper，尚未绑定开发板的 LOC/IOSTANDARD；Vivado DRC 因此有 I/O critical warning。功耗是 vectorless 估算，没有 SAIF/VCD 时不能换算成 TOPS/W。

## 2026-09-16 全模型集成结果

`design/w8a8_pack2/full_model_v2/` 使用一次真实 TurboVLA dispatch trace：6836 个 dispatch 全部被编译器分类（`unknown=0`），其中 331 个进入 Pack2 GEMM/BMM，973 个是布局，561 个是向量，3 个是存储，6505 个仍为 AUX/fallback。周期模型得到 565,587,640 cycles、1.794% PE 时间利用率和 13.78 GOPS@250 MHz；这些是 trace 驱动模型，不是 FPGA 板上端到端测量。

同一 full-model generic top 的最终 Vivado 实现资源为 89,795 LUT、193,533 FF、784 DSP、25.5 BRAM，vectorless power 5.733 W。实现已完成布线但 4 ns setup WNS=-0.303 ns，250 MHz 约束未通过；DRC 无 Error，但仍有 generic top 的 I/O critical warning。完整说明见 `design/w8a8_pack2/full_model_v2/reports/` 和 `docs/FULL_MODEL_COVERAGE.md`。

## 快速复现

下面的命令都在仓库根目录执行。

```powershell
# Python Pack2 数学检查
python design/w8a8_pack2/algo/v1_2026-09-14_115230_w8a8_semantics/test_pack2_golden.py

# 编译 TurboVLA trace（需要提供本地 trace 文件）
python design/w8a8_pack2/compiler/compile_w8a8_pack2.py --help

# 全模型 descriptor、周期和覆盖检查
python design/w8a8_pack2/full_model_v2/scripts/validate_full_model.py

# Icarus 秒级功能冒烟
powershell -ExecutionPolicy Bypass -File design/w8a8_pack2/hw/v3_2026-09-15_174639_vivado_impl/sim/run_timing_smoke.ps1

# Windows Vivado 2021.2 实现（输出目录按需填写）
& 'D:/software/Vivado/2021.2/bin/vivado.bat' -mode batch `
  -source design/w8a8_pack2/hw/v3_2026-09-15_174639_vivado_impl/vivado/run_vivado_impl.tcl `
  -tclargs 4.000 design/w8a8_pack2/hw/v3_2026-09-15_174639_vivado_impl/reports/reproduce_250
```

303.215 MHz 只需将 `-tclargs` 的周期改为 `3.298`。完整实现会占用较长时间；原始运行分别用了 1,497 秒和 2,022 秒，不能当作模型推理时间。

## 证据边界

- RTL smoke 是功能证据；Vivado post-route 是当前 generic top 的实现证据；旧 trace 周期是 Python 模型证据。
- TurboVLA 的 DINO、语言编码、未映射辅助算子没有被伪装成已经综合的 FPGA 电路。
- 仓库不包含模型 checkpoint、原始大张量、私有服务器路径下的权重、Vivado `.dcp` 和仿真缓存。它们的来源、哈希和排除原因在 `HANDOFF_MANIFEST.md` 中记录。
- 当前没有新的纯整数全模型 LIBERO 成功率、板级 DDR、完整 post-route 系统功耗或 TOPS/W 结果。

## 许可与使用

本仓库中的新脚本和 RTL 用于项目内部复现。`upstream/` 下的代码保留原项目许可文件；使用前请按相应上游仓库的许可执行。
