# TurboVLA W8A8 Pack2 时序版构建清单

生成时间：2026-09-15 16:18:22  
版本目录：`hw/v2_2026-09-15_155202_timing_pipeline/`

## RTL

- `rtl/pack2_mult_padd.sv`：HB Pack2 预加器 DSP48E2 数学核（只读复制）。
- `rtl/ae_pe_p2_pa_timing.sv`：加入 DSP P 输出寄存器的时序版 PE。
- `rtl/ae_sysarr_p2.sv`、`rtl/tvla_w8a8_pack2_sysarr.sv`：16×48 Pack2 阵列。
- `rtl/tvla_w8a8_pack2_timing_array_top.sv`：阵列输入／输出寄存器壳。
- `rtl/tvla_w8a8_pack2_replay_top_timing.sv`：带时序阵列的 descriptor 回放顶层。
- `rtl/tvla_w8a8_pack2_system_top.sv`：Vivado 入口 top。

## 检查与报告

- `sim/run_timing_smoke.ps1`：Icarus 秒级冒烟和 system_top 展开。
- `data/functional/functional_checks.json`：本地检查结果。
- `vivado/run_vivado_impl.tcl`：单频率 Vivado 综合、布局、物理优化、布线和报告脚本。
- `vivado/run_two_freqs.sh`：按 250 MHz 和 303.215 MHz 顺序运行两个独立工程。
- `vivado/collect_vivado_results.py`：收集资源、WNS/TNS、路由、DRC 和 vectorless power。
- `scripts/hash_version.py`：为本版本 RTL、仿真、Vivado 脚本和数据生成 SHA256 清单。
- `reports/generate_timing_report.py`：生成单文件中文 HTML。
- `../../reports/2026-09-15_163224/2026-09-15_163224_timing_pipeline_report.html`：本轮报告。
- `data/version_hashes.json`：本版本文件 SHA256，生成时间以 JSON 内的 `generated_at` 为准。

## 证据边界

- 本地 Icarus 结果是行为和端口展开检查，不是 Vivado 综合结果。
- 历史 v1 的 16×48 OOC 数字（78,249 LUT、148,168 FF、768 DSP、WNS +1.433 ns @3.298 ns、4.604 W vectorless）只作比较基线。
- 本轮两个 Vivado 频率点尚未运行，因此没有新的 Fmax、WNS、布局布线、DRC 或功耗数字。
- 没有 SAIF/VCD，不报告 TOPS/W。
