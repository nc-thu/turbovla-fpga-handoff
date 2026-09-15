# TurboVLA W8A8 Pack2 芯片架构报告清单

- 生成时间：2026-09-15 13:47:42
- 报告：`2026-09-15_134742_chip_architecture_report.html`
- 数据版本：`2026-09-14_115230`
- 报告性质：编译器/指令集/RTL 组织说明 + trace 驱动周期模型 + Pack2 OOC 综合

## 证据边界

- trace manifest 的量化元数据仍是 W8A16（activation 16 bit、weight 8 bit、accumulator 40 bit、output 16 bit）。因此本页的 W8A8 周期数字是同一形状和控制流上的 Pack2 W8A8 投影，不是重新采集的纯 W8A8 全模型实测。
- 1×1、4×4、16×48 是 Vivado 2021.2 的 OOC 综合结果，尚未 place/route。4.604 W 是 vectorless power，不换算 TOPS/W。
- LayerNorm、GELU、Conv、attention 外层等在 full trace 中有 AUX/fallback 事件，但当前 OOC 工程只综合 Pack2 阵列。

## 复现

```text
python reports/2026-09-15_134742/generate_architecture_report.py
python algo/v1_2026-09-14_115230_w8a8_semantics/test_pack2_golden.py
python compiler/v1_2026-09-14_115230_pack2_compiler/check_compiled_stream.py data/2026-09-14_115230/compiled_current
```

## 关键来源 SHA256

- `data\2026-09-14_115230\trace_manifest.json`：`e6603c2e32e7a3fb3851bba62851e59a41c400399d6debab6fe5ad9bdfdb5b58`
- `data\2026-09-14_115230\capture_result.json`：`a196bf567e1168a7f61bd4602a01f3deead8fcf3dae7780a3b826b283f6b0f62`
- `data\2026-09-14_115230\operator_inventory.json`：`734dfc7008b04ec3a72789eb77b71c30daa850b3d361a7e31810b5ef2db362ac`
- `data\2026-09-14_115230\compiled_current\descriptors.jsonl`：`8f278ed22c0d9e5d44df234f67a961d9c265eaaa4ad3162838324e29bb8d61e9`
- `data\2026-09-14_115230\compiled_current\instructions.hex`：`7caa0cc1e42ab6026da809b2568b7fb924b91d127c00f7020838f03cffd50900`
- `data\2026-09-14_115230\compiled_current\cycle_summary.json`：`6e70727e85553d9000dc5dabbc2416c7b3d07149c8f2ab9350ad5e873aa42efe`
- `data\2026-09-14_115230\golden_results.json`：`d2123789bddb0277c086df78aaa8c62b048e7941c1c37689be03e96e40106097`
- `data\2026-09-14_115230\sim_results.json`：`33860d623b01b15107275aec7518687d80fb236a4f1c51cbbea21855ad123a8c`
- `hw\v1_2026-09-14_115230_pack2_rtl\rtl\tvla_w8a8_pack2_replay_top.sv`：`bec95902aea59cbc3af1cdd03c7f836d65cf0f99af2033605eaea626b5ce3132`
- `hw\v1_2026-09-14_115230_pack2_rtl\rtl\tvla_w8a8_pack2_pe.sv`：`db7a8de42b9a42f9dd408a6ab681ab294c71f76cace68571beb43bcff2e6cb6e`
- `hw\v1_2026-09-14_115230_pack2_rtl\rtl\pack2_mult_padd.sv`：`2d16dc7d902a2a7a013201142e04ed38d4d04bf608666b1b9d4263f76b9a39c4`
- `hw\v1_2026-09-14_115230_pack2_rtl\synth\ooc_16x48\utilization.rpt`：`6bb73da55260e66df798b8d6267598af08a72096b50f5860dc29fd531c3643e7`
- `hw\v1_2026-09-14_115230_pack2_rtl\synth\ooc_16x48\timing.rpt`：`fa41f9da11421cdf5ffe598c9d9f6afbb3677fe2b08782d17d8c6efc1b603bca`
- `hw\v1_2026-09-14_115230_pack2_rtl\synth\ooc_16x48\power.rpt`：`263c28a3143b40ae103c45b68a6b7bb3cadff28cd019942275bba1d6e047fd79`
