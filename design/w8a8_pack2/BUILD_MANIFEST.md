# TurboVLA W8A8 Pack2 构建清单

生成时间：2026-09-14 11:52:30（版本起始时间；报告生成时间见 HTML 头部）

## 目录

- `algo/v1_2026-09-14_115230_w8a8_semantics/`：Pack2 数学黄金模型。
- `compiler/v1_2026-09-14_115230_pack2_compiler/`：TurboVLA trace 编译器和流检查器。
- `arch/v1_2026-09-14_115230_pack2_sync/`：Pack2/接口/周期口径说明。
- `hw/v1_2026-09-14_115230_pack2_rtl/`：Pack2 RTL、仿真 testbench 和 OOC 结果。
- `hw/v2_2026-09-15_155202_timing_pipeline/`：时序版 Pack2 RTL、两个 Vivado 频率点脚本、本地功能检查和结果收集器。
- `hw/v3_2026-09-15_174639_vivado_impl/`：使用本机 Vivado 2021.2 完成两个频率点的综合、布局、布线和报告；generic top 仍未绑定板级 I/O。
- `data/2026-09-14_115230/`：输入摘要、描述符、周期、流量和校验结果。
- `reports/2026-09-14_115230/`：本轮 HTML 报告。
- `reports/2026-09-15_163224/`：时序版电路与架构说明页。
- `reports/2026-09-15_192512/`：真实 Vivado post-route 结果与中文架构分析页（最终版）。

## 主要来源

- 目标对话：`codex://threads/01a09dc7-08f7-7201-afba-4820f3eedb3e`。该对话仍在继续，纯 W8A8 最终成功率尚未作为本轮新结果使用。
- HB Pack2 参考：`hw/v10_2026-09-12_1148_engfull_preadd/rtl/`。
- TurboVLA W8A8 候选结果：`algo/turbovla_quant/2026-09-12_215112/results/summary.json`，完整 sha256 见 `data/2026-09-14_115230/evidence_sources.json`。
- TurboVLA trace：`turbovla_w8a16/data/v8_2026-09-13_231621/`。`module_events.jsonl` 408 行，`operator_trace.jsonl` 6836 行。

## 复现命令

```text
python algo/v1_2026-09-14_115230_w8a8_semantics/test_pack2_golden.py
python compiler/v1_2026-09-14_115230_pack2_compiler/compile_w8a8_pack2.py --help
python compiler/v1_2026-09-14_115230_pack2_compiler/check_compiled_stream.py <compiled_dir>
vivado.bat -mode batch -source scripts/run_vivado_array_ooc.tcl -tclargs <rows> <pcols> <output_dir>
# 本轮实际使用的 Windows Vivado
D:/software/Vivado/2021.2/bin/vivado.bat -mode batch -source hw/v3_2026-09-15_174639_vivado_impl/vivado/run_vivado_impl.tcl -tclargs 4.000 <output_dir>
D:/software/Vivado/2021.2/bin/vivado.bat -mode batch -source hw/v3_2026-09-15_174639_vivado_impl/vivado/run_vivado_impl.tcl -tclargs 3.298 <output_dir>
```

## 设计口径

主阵列是 16 行×48 物理列，共 768 DSP；每个物理列产生两个逻辑输出列。Pack2 峰值为 250 MHz 下 768 GOPS，303.215 MHz 下 931.476 GOPS。双时钟、Pump2、p2d/pp 双路阵列不在本版本中。

## 本轮实现结果哈希

- 最终 HTML：`4530716F3FF63D747EF9B13CBDAF9F53517409724175C0CC9C4A03016C4F3AA0`
- 机器可读结果：`CF53DDCCBD008E86A4BB0E6AA1B2C183D95744642FF1A2513396E5CF3B12B8FC`
- 250 MHz timing report：`CABF5365F231660DEAF0BDA3A7156B447818D568F37F47B1B495EC3FE26B4015`
- 303.215 MHz timing report：`149032E39B6AA0FB5AECF2D6AA63D2B5F08BEB3F750B370A5CBE9FA561C175C7`
