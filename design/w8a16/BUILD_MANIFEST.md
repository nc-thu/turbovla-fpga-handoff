# TurboVLA W8A16 构建清单

生成时刻：2026-09-12 23:54:06（v6 implementation 结果追加于 2026-09-13 19:33:56）

## 参考输入

| 内容 | 来源 | 用途 |
|---|---|---|
| TurboVLA 源码快照 | `references/turbovla_source/` | 只读模型结构参考 |
| 模型配置 | `data/checkpoint_model_config.json` | 输入尺寸、层数和动作配置 |
| 模型参数形状 | `data/model_state_dict_shapes.json` | GEMM 形状枚举 |
| 量化筛选结果 | `data/quant_screening_summary.json` | 软件参考，不作为硬件时延 |
| Pack2 参考 RTL | `references/pack2_rtl/` | 端口和控制协议参考 |

## 当前状态

- 软件 W8A16：沿用已有权重 INT8、激活 INT16 的定义；当前旧结果是 fake-quant FP32 kernel，仅作参考。
- 编译器：新描述符 schema 为 `tvla_w8a16.v1`。
- 周期模型：主阵列为 16×48、768 DSP、A16/W8、40-bit accumulator。
- RTL：Verilator、Icarus/UNISIM 冒烟和 Vivado 流程已准备；本轮已完成 v5 顶层 post-route 以及 v6 的 250 MHz post-route implementation。

## 2026-09-13 17:40:37 — v5 post-route implementation

| 项目 | 结果 |
|---|---|
| 独立目录 | `hw/v5_2026-09-13_163609_post_route_impl/` |
| Vivado 流程 | `synth_design → opt_design → place_design → phys_opt_design → route_design → post-route phys_opt_design` |
| 器件／目标 | `xczu7ev-ffvc1156-2-e`，3.298 ns |
| route status | fully routed；184,104 / 184,104 可路由网络；unrouted=0 |
| post-route timing | WNS -0.461 ns，TNS -1197.739 ns，8,075 setup 失败端点，按 WNS 推算 266.0 MHz |
| post-route resources | 66,255 LUT、118,169 FF、785 DSP、0 BRAM |
| power | 5.678 W vectorless estimate（dynamic 5.058 W、static 0.620 W，Medium confidence） |
| DRC | 0 Error，4 Warning，1 Advisory |
| 报告 | `reports/2026-09-13_174037/2026-09-13_174037_turbovla_w8a16_post_route_impl.html` |
| 边界 | OOC 无板级 pin/AXI/DDR/clock-buffer 约束；未生成 bitstream；功耗非上板实测 |
- 未做：完整 LIBERO 成功率、完整系统集成、post-route、功耗和上板。

## 2026-09-13 14:52:54 — v3 camera-ready 候选

| 项目 | 结果 |
|---|---|
| 版本目录 | `algo/v3_2026-09-13_140118_w8a16_camera_ready_semantics/`、`arch/v3_2026-09-13_140118_w8a16_camera_ready_model/`、`compiler/v3_2026-09-13_140118_w8a16_camera_ready_compiler/`、`hw/v3_2026-09-13_140118_w8a16_camera_ready_rtl/` |
| 编译器 | `tvla_w8a16.camera_ready.v3`；83 条逻辑操作、172 条 transport word；长流 sideband 偏移和 16×48 tile shape/grid 有连续性检查 |
| RTL 回归 | v3 服务器 Verilator 11 项通过，Icarus 5 项短 smoke 通过；系统 smoke 观察到 production-array feed/done |
| 顶层综合 | `w8a16_system_top`，Vivado 2021.2，`xczu7ev-ffvc1156-2-e`，3.298 ns；WNS +0.067 ns，0 个 setup 失败端点，综合估算 309.5 MHz |
| 顶层资源 | 67,432 LUT、118,139 FF、785 DSP、0 BRAM；16×48 阵列本身 57,331 LUT、110,656 FF、768 DSP |
| DRC 边界 | 0 Error；OOC 仍有 NSTD-1/UCIO-1（缺板级 I/O 约束）及 DSP pipeline warning，不能直接生成 bitstream |
| 报告 | `reports/2026-09-13_145254/2026-09-13_145254_turbovla_w8a16_camera_ready.html` |
| 未完成 | 完整 TurboVLA DINO/T5/采样接入、真实 LIBERO、UNISIM、place/route、post-route、功耗和板级 AXI/DDR |

## 2026-09-13 15:37:31 — v4 timing-fixed camera-ready candidate

| 项目 | 结果 |
|---|---|
| 当前版本目录 | `algo/v4_2026-09-13_150700_w8a16_timing_fixed_semantics/`、`arch/v4_2026-09-13_150700_w8a16_timing_fixed_model/`、`compiler/v4_2026-09-13_150700_w8a16_timing_fixed_compiler/`、`hw/v4_2026-09-13_150700_w8a16_timing_fixed_rtl/` |
| 编译器 | `tvla_w8a16.camera_ready.v4`；83 条逻辑操作，172 条 transport word，8 个 descriptor，18 个 opcode |
| RTL 回归 | 服务器 Verilator 11 项通过（144 s）；Icarus 5 项短 smoke 通过；UNISIM 因无 `xvlog` 未运行 |
| 系统 top 综合 | Vivado 2021.2，`xczu7ev-ffvc1156-2-e`，3.298 ns；0 个 setup 失败端点，WNS +0.310 ns，综合估算 Fmax 334.7 MHz |
| 系统资源 | 67,448 LUT、118,149 FF、785 DSP、0 BRAM；16×48 阵列 768 DSP |
| 关键路径 | `u_runtime/u_action/weight_r_reg[1][7][7]/C` → `u_runtime/u_action/acc_r_reg[0][29]/D`；2.978 ns（logic 69.846%，route 30.154%） |
| 报告 | `reports/2026-09-13_153731/2026-09-13_153731_turbovla_w8a16_camera_ready.html` |
| 明确未完成 | place/route、post-route timing、功耗、板级 pin/AXI/DDR、UNISIM、完整 TurboVLA DINO/T5/采样与 LIBERO 成功率 |

## 2026-09-13 13:40:00 — v2 camera-ready 候选

| 项目 | 结果 |
|---|---|
| 当前版本目录 | `algo/v2_2026-09-13_1113_w8a16_camera_ready_semantics/`、`arch/v2_2026-09-13_1113_w8a16_camera_ready_model/`、`compiler/v2_2026-09-13_1113_w8a16_camera_ready_compiler/`、`hw/v2_2026-09-13_1113_w8a16_camera_ready_rtl/` |
| 编译器程序 | 83 条逻辑操作，自动分片后 172 条 transport word；8 条代表性 descriptor |
| RTL 回归 | 服务器 Verilator 11 项通过（144 s）；Icarus 5 项短 smoke 通过（1 s） |
| 顶层综合 | `w8a16_system_top`，Vivado 2021.2，`xczu7ev-ffvc1156-2-e`，3.298 ns；0 个 setup 失败端点，最差数据路径 3.288 ns |
| 顶层资源 | 67,086 LUT、118,088 FF、785 DSP、0 BRAM；16×48 阵列本身 57,331 LUT、110,656 FF、768 DSP |
| 结果边界 | 以上是逻辑综合和行为仿真；未做 post-route、功耗、UNISIM（服务器无 xvlog）、真实 TurboVLA 视觉／语言／采样和 LIBERO 成功率 |

## 2026-09-13 01:27:06 — 本轮构建产物

| 项目 | 结果 |
|---|---|
| 编译器程序 | `data/turbovla_w8a16_program.json`；完整 83 条、smoke 7 条，均带 `word_hex` |
| 指令定义 | `data/isa_spec.json`；18 个 opcode，含读写、矩阵、向量、激活、归一化和控制 |
| 成本模型 | `data/instruction_costs.json`；完整与 smoke 的周期下界和流量 |
| Python 对拍 | `data/isa_sim_results.json`、`data/libero_action_probe.json`；PASS |
| Verilator | 服务器实验 `2026-09-13_010117`；PE、阵列、GEMM、激活、向量、DMA、ISA、runtime 共 10 项通过 |
| Icarus | PE、4×4、激活、ISA 共 4 项短 smoke 通过 |
| 完整动作 | 仅命令路径 smoke；不含 DINO/T5、完整采样和 LIBERO 环境步进 |

## 2026-09-13 10:52:55 — Vivado 综合结果

| 项目 | 结果 |
|---|---|
| 工具 | Vivado 2021.2，`D:\software\Vivado\2021.2\bin\vivado.bat` |
| 器件／约束 | `xczu7ev-ffvc1156-2-e`，3.298 ns |
| 系统顶层 | `w8a16_system_top` 综合通过；52,743 LUT、2,814 FF、35 DSP；WNS -4.528 ns |
| 16×48 阵列 | 综合通过；57,331 LUT、110,656 FF、768 DSP；WNS 2.149 ns，约 870 MHz 综合估算 |
| 运行目录 | `hw/v1_2026-09-12_2354_w8a16_rtl/synth/runs/2026-09-13_104234/` |
| 口径 | 逻辑综合，不是 post-route；PPA 提升未宣称（0%） |

## 2026-09-13 19:33:56 — v6 DSP pipeline / 250 MHz post-route

| 项目 | 结果 |
|---|---|
| 独立目录 | hw/v6_2026-09-13_182745_dsp_pipeline_250mhz/ |
| RTL 改动 | DSP AREG/BREG=1；MREG/PREG=1；PE product/valid 对齐；action MAC product 与两拍 drain |
| Vivado 流程 | synth_design → opt_design → place_design → phys_opt_design → route_design → post-route phys_opt_design |
| 器件／目标 | xczu7ev-ffvc1156-2-e，4.000 ns（250 MHz） |
| route status | fully routed；184,306 / 184,306 可路由网络；unrouted=0；routing errors=0 |
| post-route timing | WNS -0.050 ns，TNS -4.464 ns，192 个 setup 失败端点，按 WNS 推算 246.9 MHz；250 MHz 未过 |
| 关键路径 | u_runtime/u_ctrl/word_r_reg[61]/C → u_gemm/u_arr/g_row[6].g_col[45].u_pe/acc_r_reg[10]/CE；3.946 ns，逻辑 7.628%，布线 92.372% |
| post-route resources | 66,368 LUT、117,105 FF、785 DSP、0 BRAM |
| power | 4.478 W vectorless estimate（dynamic 3.865 W、static 0.613 W，Medium confidence） |
| DRC | 821 violations，0 Error；DPIP-2 34、DPOP-3 1、DPOP-4 17、RTSTAT-10 1、AVAL-155 advisory 768 |
| Verilator | 11/11 PASS，153 s；完整阵列 768 DSP |
| UNISIM | 未完成；服务器无 xvlog |
| 结果 | data/v6_2026-09-13_193556_implementation/implementation_results.json；reports/2026-09-13_193800/2026-09-13_193800_turbovla_w8a16_v6_250mhz_implementation.html |
| 边界 | OOC 无板级 pin/AXI/DDR/clock-buffer 约束；未生成 bitstream；功耗非上板实测 |

## 2026-09-13 22:00:48 — v7 `clr` fanout partition / 250 MHz post-route

| 项目 | 结果 |
|---|---|
| 独立目录 | `hw/v7_2026-09-13_195800_clr_partition_250mhz/` |
| RTL 改动 | `w8a16_sysarr.sv`；`clr` 按每 8 列分组，16×6 个保留 group nets；不改协议和算术 |
| Vivado 流程 | synth_design → opt_design → place_design → phys_opt_design → route_design → post-route phys_opt_design |
| 器件／目标 | `xczu7ev-ffvc1156-2-e`，4.000 ns（250 MHz） |
| route status | 184,322 / 184,322 fully routed；unrouted=0；routing errors=0 |
| post-route timing | WNS +0.006 ns，TNS 0，0 个 setup 失败端点，Fmax 250.38 MHz；**250 MHz 通过** |
| 关键路径 | `u_runtime/u_ctrl/word_r_reg[58]/C` → `u_gemm/u_arr/g_row[9].g_col[47].u_pe/acc_r_reg[15]/CE`；3.889 ns；logic 12.137%，route 87.863% |
| 资源 | 66,375 LUT、117,104 FF、785 DSP、0 BRAM |
| vectorless power | 4.670 W（dynamic 4.056 W，static 0.614 W，Medium；无 SAIF/VCD） |
| DRC | 821 violations，0 Error；DPIP-2 34、DPOP-3 1、DPOP-4 17、RTSTAT-10 1、AVAL-155 advisory 768 |
| Verilator | 11/11 PASS，159 s；完整阵列 768 DSP |
| UNISIM | 未完成；服务器无 `xvlog` |
| 机器汇总 | `data/v7_2026-09-13_220100_implementation/implementation_results.json` |
| 性能分析页 | `reports/2026-09-13_220048/2026-09-13_220048_TurboVLA_W8A16当前架构性能分析.html` |
| 边界 | OOC 无板级 pin/AXI/DDR/clock-buffer 约束；未生成 bitstream；功耗非上板实测 |

复现顺序：

```text
python compiler/v1_2026-09-12_2354_w8a16_compiler/compile_program.py
python scripts/build_instruction_costs.py
python scripts/isa_sim.py
python scripts/collect_rtl_results.py
cd hw/v1_2026-09-12_2354_w8a16_rtl/sim; bash run_verilator.sh
cd hw/v1_2026-09-12_2354_w8a16_rtl/sim; bash run_iverilog_smoke.sh
pwsh -NoProfile -File hw/v1_2026-09-12_2354_w8a16_rtl/synth/run_top_synth.ps1 -Vivado D:\software\Vivado\2021.2\bin\vivado.bat
python scripts/collect_vivado_synth.py hw/v1_2026-09-12_2354_w8a16_rtl/synth/runs/<timestamp>
python scripts/generate_report.py
```

## 2026-09-13 22:08:12 — 当前交付页

| 项目 | 路径 |
|---|---|
| 详细性能 HTML | `reports/2026-09-13_220812/2026-09-13_220812_TurboVLA_W8A16当前架构性能分析.html` |
| 机器可读汇总 | `reports/2026-09-13_220812/performance_summary.json` |
| 生成脚本 | `scripts/generate_performance_report.py` |
| 数据来源 | `data/v5_2026-09-13_173359_implementation/`、`data/v6_2026-09-13_193556_implementation/`、`data/v7_2026-09-13_220100_implementation/` |
| 校验 | Python 编译通过；页面含 10 个 section、5 个内嵌 SVG；未发现 `None`/`NaN` 占位 |

## 2026-09-13 22:11:29 — 最终页面

| 项目 | 路径 |
|---|---|
| 详细性能 HTML | `reports/2026-09-13_221129/2026-09-13_221129_TurboVLA_W8A16当前架构性能分析.html` |
| 机器可读汇总 | `reports/2026-09-13_221129/performance_summary.json` |
| 页面状态 | v7 post-route WNS +0.006 ns，250 MHz 通过；验证页面中的条件文字已按通过状态更新 |

## 2026-09-13 22:13:00 — 最终交付页

| 项目 | 路径 |
|---|---|
| 详细性能 HTML | `reports/2026-09-13_221300/2026-09-13_221300_TurboVLA_W8A16当前架构性能分析.html` |
| 机器可读汇总 | `reports/2026-09-13_221300/performance_summary.json` |
| 页面检查 | 10 个 section、5 个内嵌 SVG、v5 DPIP-2 自动读为 1,571；无 `None`/`NaN` 占位 |

## 2026-09-14 00:59:00 — 真实 TurboVLA 指令流活动回放

| 项目 | 路径／结果 |
|---|---|
| 真实采集 | `data/v8_2026-09-13_231621/raw_capture/`；GPU3、`libero_spatial` Spatial task 0、seed 7；408 module / 6,836 dispatch events |
| 编译输出 | `data/v8_2026-09-13_231621/compiled/`；432 descriptors、433 instructions（含 END）、unknown=0 |
| replay stream | `data/v8_2026-09-13_231621/replay_stream/`；512-bit descriptor words、64-bit command words |
| 顶层 RTL | `hw/v8_2026-09-13_2316_integrated_replay_top/rtl/tvla_replay_top.sv`；16×48、768 DSP、descriptor FIFO、AUX_EVENT、activity counter |
| Verilator | `data/v8_2026-09-13_231621/rtl_logs/`；full replay 和代表 tile 均 PASS |
| Vivado | `hw/v8_2026-09-13_2316_integrated_replay_top/synth/runs/2026-09-14_0039/`；array off／on trace off／on trace on 全部 synth PASS |
| 机器汇总 | `data/v8_2026-09-13_231621/rtl_activity.json`、`vivado_results.json`、`activity_events.jsonl`、`traffic_breakdown.csv` |
| HTML | `reports/2026-09-13_231621/2026-09-13_231621_TurboVLA_activity_replay.html` |
| 关键结果 | 155,780,495 cycles；49,584,342,528 valid MAC；PE 41.445%；GEMM 43.227%；159.148 GOPS；384 GOPS 物理峰值 |
| 时间／边界 | 250 MHz 周期模型对应 0.623 s；full replay 是虚拟事件周期，代表 tile 才是逐拍阵列验证；无 post-route、板上功耗、TOPS/W、多 suite 和成功率 |

复现命令（在 `E:\GPU ARCH\vector_core_sim`）：

```powershell
python turbovla_w8a16\compiler\v5_2026-09-13_2316_real_trace_compiler\compile_trace.py --capture turbovla_w8a16\data\v8_2026-09-13_231621\raw_capture --output turbovla_w8a16\data\v8_2026-09-13_231621\compiled
python turbovla_w8a16\compiler\v5_2026-09-13_2316_real_trace_compiler\emit_replay_stream.py --compiled turbovla_w8a16\data\v8_2026-09-13_231621\compiled --output turbovla_w8a16\data\v8_2026-09-13_231621\replay_stream
python turbovla_w8a16\arch\v3_2026-09-13_231621_activity_replay_model\scripts\validate_replay.py --data turbovla_w8a16\data\v8_2026-09-13_231621 --rtl-log-dir turbovla_w8a16\data\v8_2026-09-13_231621\rtl_logs --output turbovla_w8a16\data\v8_2026-09-13_231621\rtl_activity.json
```

## 2026-09-14 02:03:01 — history optimization round

| 项目 | 路径／结果 |
|---|---|
| 十项清单 | `arch/v4_2026-09-14_010956_history_optimization/selected_optimizations.json` |
| 编译器 | `compiler/v6_2026-09-14_010956_history_optimization/`；432 descriptors、433 instructions、24/24 BMM、unknown=0 |
| 周期汇总 | `data/v9_2026-09-14_010956/summary/model_summary.json`；baseline 155,780,495 cycles，optimized 75,254,992 cycles，条件加速 2.070× |
| 消融 | `data/v9_2026-09-14_010956/ablation/ablation_summary.csv`；overlap 单项下降 50.723%，weight reuse 2.429%，vector pipeline 0.973% |
| RTL | `hw/v9_2026-09-14_010956_history_optimization/rtl/`；Verilator full/array/FIFO PASS，768 DSP |
| Vivado OOC | `data/v9_2026-09-14_010956/vivado_runs_2026-09-14_0147_fifo_fix/`；3/3 synth PASS；array on 60,419 LUT、119,214 FF、768 DSP、WNS +1.884 ns、Fmax 472.6 MHz |
| 校验 | `data/v9_2026-09-14_010956/validation_summary.json`；所有检查通过 |
| manifest | `data/v9_2026-09-14_010956/trace_manifest.json`；包含源 capture 与本轮产物 SHA256 |
| HTML | `reports/2026-09-14_010956/2026-09-14_010956_turbovla_history_optimization_report.html` |
| 报告机器汇总 | `reports/2026-09-14_010956/round_summary.json` |
| 证据边界 | 完整 replay 是虚拟事件周期；代表 tile/FIFO 是逐拍 Verilator；Vivado 是 OOC synthesis-estimated；无 post-route、SAIF/VCD、板级 DDR、TOPS/W 或 LIBERO 成功率 |

02:15:24 最终检查：HTML（02:13:49 生成）含 5 个内嵌 SVG 和 12 张表；`round_summary.json`、`trace_manifest.json` 及报告生成脚本均已保留并同步到服务器。页面无 `None`/`NaN` 占位。

复现本轮摘要：

```powershell
python turbovla_w8a16\compiler\v6_2026-09-14_010956_history_optimization\compile_trace.py --capture turbovla_w8a16\data\v8_2026-09-13_231621\raw_capture --output turbovla_w8a16\data\v9_2026-09-14_010956\compiler_baseline
python turbovla_w8a16\compiler\v6_2026-09-14_010956_history_optimization\compile_trace.py --capture turbovla_w8a16\data\v8_2026-09-13_231621\raw_capture --output turbovla_w8a16\data\v9_2026-09-14_010956\compiler_optimized --optimize
python turbovla_w8a16\arch\v4_2026-09-14_010956_history_optimization\run_ablation.py --capture turbovla_w8a16\data\v8_2026-09-13_231621\raw_capture --output turbovla_w8a16\data\v9_2026-09-14_010956\ablation
python turbovla_w8a16\arch\v4_2026-09-14_010956_history_optimization\validate_history_round.py --baseline turbovla_w8a16\data\v9_2026-09-14_010956\compiler_baseline --optimized turbovla_w8a16\data\v9_2026-09-14_010956\compiler_optimized --rtl-log-dir turbovla_w8a16\data\v9_2026-09-14_010956\rtl_logs --vivado-json turbovla_w8a16\data\v9_2026-09-14_010956\derived\vivado_results.json --output turbovla_w8a16\data\v9_2026-09-14_010956\validation_summary.json
```
