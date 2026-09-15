# TurboVLA W8A16 工作区记录

每轮只写入新的版本目录，旧目录保持不动。报告和机器可读数据均带生成时间。

## 2026-09-12 23:54:06 — v1 工作区建立

- 建立独立的算法、架构、编译器、RTL 和报告目录。
- 记录 TurboVLA 源码、模型形状、已有 W8A16 筛选结果和当前单时钟 Pack2 RTL 为只读参考。
- 主路线固定为 16×48、每 PE 一颗 DSP、INT16×INT8 单路乘法、256-bit CTX 激活读写、40-bit 累加。

## 2026-09-13 01:27:06 — v2 指令到动作路径

- 补齐 64-bit TurboVLA W8A16 指令字、GEMM/BMM、DMA、向量加法／缩放、ReLU、GELU、tanh、LayerNorm、Softmax、REQUANT、WAIT、BARRIER 和 END 的描述与包装。
- Verilator 十项测试通过；Icarus 四项短 smoke 通过。16×48 阵列仍为 768 DSP，没有增加乘法器数量。
- 编译器 83 条完整示例和 7 条动作 smoke 均通过 Python 解码检查。小型 LIBERO 来源动作路径输出与 Python 整数模型逐位一致。
- 未声称完整 TurboVLA 或 LIBERO 已由 RTL 执行；UNISIM、Vivado OOC、真实整数 GPU kernel 和端到端环境仍未做。

## 2026-09-13 01:33:37 — 明确动作输入来源

- `isa_sim_results.json` 和 `libero_action_probe.json` 区分 LIBERO 任务元数据与实际输入：当前 smoke 使用确定性的 INT16 格式化向量，不冒充真实 RGB-D 推理。

## 2026-09-13 10:52:55 — Vivado 顶层逻辑综合

- 使用本机 `D:\software\Vivado\2021.2\bin\vivado.bat`，器件 `xczu7ev-ffvc1156-2-e`，3.298 ns 目标时钟，采用非工程 batch 脚本综合系统壳和 1×1、4×4、16×48 阵列。
- `w8a16_system_top`、1×1、4×4、16×48 均 `synth_design` 通过；16×48 统计为 57,331 LUT、110,656 FF、768 DSP，综合 WNS 2.149 ns（约 870 MHz 综合估算）。
- 系统壳统计为 52,743 LUT、2,814 FF、35 DSP，WNS -4.528 ns；关键路径在动作路径输出打包／饱和逻辑。综合 DRC 没有 Error，但有 DSP 流水相关 warning。
- 运行目录：`hw/v1_2026-09-12_2354_w8a16_rtl/synth/runs/2026-09-13_104234/`。这些数字是逻辑综合结果，不是 post-route PPA，提升仍记为 0%。

## 2026-09-13 11:02:37 — 归档综合汇总

- 重新从四个 `status.json` 和完整 launcher 记录生成 `data/vivado_synth_results.json/.csv`，耗时采用包含 Vivado 启动和退出的墙钟时间。
- 生成报告 `reports/2026-09-13_110237/`。报告继续把系统壳的负 WNS 和阵列的综合正 WNS 分开列出，没有把综合估算写成 post-route 频率。

## 2026-09-13 13:40:00 — v2 camera-ready 候选：时序、数据链和编译器分片

- 将动作后处理、LayerNorm 和 Softmax 的长组合运算改成寄存器／迭代路径。v11 系统顶层在 3.298 ns 约束下综合通过，0 个 setup 失败端点，最差数据路径 3.288 ns，余量约 0.010 ns；这是 synth_design 结果，不是 post-route。
- `w8a16_system_top` 现在同时展开 runtime、256-bit 激活 DMA、384-bit 权重 DMA、向量／激活单元、REQUANT 和 16×48 生产阵列。阵列保持 768 DSP；系统综合总计 785 DSP、67,086 LUT、118,088 FF，BRAM 0。
- 修复 DMA 返回数据落地：CTX beat 写入 INT16 scratch bank，WRAM beat 按固定首／次目的地写入权重 bank，STORE 数据在 ready/valid 背压期间保持稳定。矩阵指令的 `flags[7]` 会启动阵列并等待 done；系统 smoke 新增生产阵列 feed。
- 编译器增加超长向量分片。83 条逻辑操作展开为 172 条 transport word，片段保存 `logical_length`、`chunk_index`、`chunk_count`；Python 编译、描述符生成、ISA 解码、成本模型均通过。
- 服务器 Verilator 11 项回归和 Icarus 5 项短 smoke 通过；UNISIM 因服务器无 `xvlog` 保留为 unavailable。完整 TurboVLA 视觉／语言／采样、LIBERO 环境和板级 AXI/DDR 仍未接入。

## 2026-09-13 14:52:54 — v3 camera-ready 候选：top 时序和完整 sideband

- LayerNorm/Softmax 的逐位除法最后一拍与 INT16 饱和分开，系统 top `w8a16_system_top` 在 3.298 ns 目标下由 v12 的 -0.014 ns 变为 WNS +0.067 ns，0 个 setup 失败端点；最差综合路径为 `vec_scale_r_reg` 到向量乘法输出寄存器，数据路径 3.220 ns。该结果仍是 `synth_design`，不是 place/route。
- v3 系统 top 综合得到 67,432 LUT、118,139 FF、785 DSP、0 BRAM；16×48 阵列本体为 57,331 LUT、110,656 FF、768 DSP。1×1 与 4×4 分别保持 1 和 16 DSP。
- 编译器 schema 更新到 `tvla_w8a16.camera_ready.v3`。每条矩阵指令带 16×48 tile shape/grid；长向量片段带 `logical_id`、首尾连续的元素／beat 偏移、`address_mode` 和扩展地址标记。83 条逻辑操作仍展开为 172 条 transport word，Python 成本模型和 ISA 解码重新通过。
- v3 服务器 Verilator 11 项、Icarus 5 项短 smoke 仍通过；系统 smoke 实际观察到 production-array feed 和 done。Vivado DRC 没有 Error，但 OOC 没有板级 pin 约束，NSTD-1/UCIO-1 和 DSP pipeline warning 仍需在板级工程处理。
- 报告：`reports/2026-09-13_145254/2026-09-13_145254_turbovla_w8a16_camera_ready.html`。未完成项仍包括完整 TurboVLA DINO/T5/采样接入、LIBERO 成功率、UNISIM、place/route、功耗和板级 AXI/DDR。

## 2026-09-13 15:37:31 — v4 top timing-fixed camera-ready candidate

- 在独立 `v4_2026-09-13_150700_*` 目录中把 `MUL_SCALE` 的 32-bit 乘积寄存器和移位／饱和寄存器分开。v4 系统 top `w8a16_system_top` 使用 Vivado 2021.2、`xczu7ev-ffvc1156-2-e`、3.298 ns 目标，WNS 从 v3 的 +0.067 ns 提升到 +0.310 ns，数据路径 2.978 ns，0 个 setup 失败端点。
- v4 系统 top 资源为 67,448 LUT、118,149 FF、785 DSP、0 BRAM；按综合 WNS 换算的 Fmax 约 334.7 MHz。1×1、4×4、16×48 阵列记录沿用 v3 的真实结果，并在 JSON 中标记为 `v3_unchanged_array_top`，因为本次改动不在阵列 top 的实例化路径上。
- v4 编译器 schema 为 `tvla_w8a16.camera_ready.v4`，83 条逻辑操作仍展开为 172 条 transport word；编译器、Python 数值检查、Verilator 11 项和 Icarus 5 项短 smoke 均通过。服务器没有 `xvlog`，UNISIM 仍为 unavailable。
- 报告：`reports/2026-09-13_153731/2026-09-13_153731_turbovla_w8a16_camera_ready.html`。结果仍是逻辑综合和行为仿真；未做 place/route、post-route、功耗、板级 pin/AXI/DDR 和完整 TurboVLA/LIBERO 集成。

## 2026-09-13 17:40:37 — v5 顶层 post-route implementation

- 从 v4 RTL 独立复制出 `hw/v5_2026-09-13_163609_post_route_impl/`，使用 Vivado 2021.2 在 `xczu7ev-ffvc1156-2-e` 上完成 `opt/place/phys_opt/route/post-route phys_opt`。命令成功结束，184,104 条可路由网络全部完成，unrouted=0。
- 3.298 ns 目标未通过：post-route WNS=-0.461 ns，TNS=-1197.739 ns，8,075 个 setup 失败端点；关键数据路径 3.740 ns，其中逻辑 54.973%、布线 45.027%。按 WNS 推算最高频率约 266.0 MHz。
- post-route 资源为 66,255 LUT、118,169 FF、785 DSP、0 BRAM；DSP 数量相对 v4 综合结果不变。v4 与 v5 处于不同阶段，不宣称面积提升。
- `report_power` 给出 5.678 W（动态 5.058 W、静态 0.620 W，Medium confidence），但没有 SAIF/VCD，是 vectorless 估算，不是板上功耗或能效实测。
- DRC 0 Error、4 Warning、1 Advisory；仍有 DSP pipeline 和 OOC I/O 约束提示。未生成 bitstream。机器可读结果：`data/v5_2026-09-13_173359_implementation/implementation_results.json`；报告：`reports/2026-09-13_174037/2026-09-13_174037_turbovla_w8a16_post_route_impl.html`。
## 2026-09-13 19:33:56 — v6 DSP pipeline 与 250 MHz implementation

- 从 v5 独立复制到 hw/v6_2026-09-13_182745_dsp_pipeline_250mhz/。w8a16_mult 使用 DSP AREG=1/BREG=1、MREG=1/PREG=1；PE 保留乘积寄存和 valid 对齐；action path 增加 MAC 操作数／乘积寄存并把末尾累加 drain 拆成两拍。
- 服务器 Verilator 11/11 通过（153 s），16×48 阵列保持 768 DSP；Icarus/UNISIM 因服务器没有 xvlog 未完成。
- Vivado 2021.2 在 xczu7ev-ffvc1156-2-e 上使用 4.000 ns（250 MHz）完成 synth、opt、place、phys_opt、route 和 post-route phys_opt。184,306 条可路由网络全部完成，routing errors=0。
- post-route WNS=-0.050 ns、TNS=-4.464 ns、192 个 setup 失败端点，按 WNS 推算 Fmax 246.9 MHz，250 MHz 目标尚未通过。最长路径已转为控制字到阵列累加器 CE，数据路径 3.946 ns 中布线占 92.372%。
- 资源为 66,368 LUT、117,105 FF、785 DSP、0 BRAM；vectorless 功耗 4.478 W（动态 3.865 W、静态 0.613 W，Medium confidence），不是板上实测。
- DRC 821 项、0 Error；包括 DPIP-2 34（v5 为 1,571，减少约 97.8%）、DPOP-3 1、DPOP-4 17、RTSTAT-10 1 和 AVAL-155 advisory 768。机器汇总：data/v6_2026-09-13_193556_implementation/implementation_results.json；报告：reports/2026-09-13_193800/2026-09-13_193800_turbovla_w8a16_v6_250mhz_implementation.html。
- 下一轮优先按行／列分区控制清零和 CE 高扇出，再补 runtime/vector/action 中剩余的 DSP pipeline。OOC 没有板级 pin、时钟和 AXI/DDR 约束，本轮没有生成 bitstream。

## 2026-09-13 22:00:48 — v7 `clr` 扇出分区与 250 MHz 通过

- 从 v6 独立复制到 `hw/v7_2026-09-13_195800_clr_partition_250mhz/`，只在 `w8a16_sysarr.sv` 将阵列清零控制按每 8 列分成 16×6 个保留网络。没有增加时钟周期、PE 或 DSP。
- 服务器 Verilator 11/11 通过，耗时 159 s；完整 16×48 阵列仍为 768 DSP。
- Vivado 2021.2、`xczu7ev-ffvc1156-2-e`、4.000 ns 目标完成综合、布局、物理优化、布线和 post-route phys-opt。184,322 条可路由网络全部完成。
- post-route WNS 从 v6 的 -0.050 ns 变为 +0.006 ns，失败端点从 192 变为 0；按 WNS 推算 Fmax 为 250.38 MHz，**250 MHz 通过**。关键路径仍是 runtime 控制到 PE `clr/CE`，但布线延迟由 3.645 ns 降至 3.417 ns，减少约 6.3%。
- 资源为 66,375 LUT、117,104 FF、785 DSP、0 BRAM。相对 v6，LUT 增 7（约 0.011%），DSP 不变。vectorless 功耗 4.670 W，比 v6 的 4.478 W 增加约 4.3%；没有 SAIF/VCD，不是实测能效。
- DRC 仍为 821 项、0 Error；DPIP-2 保持 34。机器汇总：`data/v7_2026-09-13_220100_implementation/implementation_results.json`。性能页：`reports/2026-09-13_220048/2026-09-13_220048_TurboVLA_W8A16当前架构性能分析.html`。
- 本轮仍是 OOC wrapper，没有板级时钟、I/O、AXI/DDR 约束，没有生成 bitstream；完整 TurboVLA/LIBERO 端到端执行和带活动文件功耗未做。

## 2026-09-13 22:08:12 — 性能分析页补充前后百分比

- 重新从 v5、v6、v7 的机器 JSON 和保留的 Vivado DRC 报告生成性能页，没有改动 RTL 或历史实现结果。
- 新页补充 v6→v7 的前后变化：Fmax +1.402%、关键路径 -1.445%、布线延迟 -6.255%、LUT +0.011%、vectorless 功耗 +4.288%。负号表示数值变小；功耗仍不是板上测量。
- v5 的 DPIP-2 从原始 DRC 报告自动读取为 1,571，v6/v7 为 34，降幅 97.836%。
- 页面：`reports/2026-09-13_220812/2026-09-13_220812_TurboVLA_W8A16当前架构性能分析.html`；机器汇总同目录的 `performance_summary.json`。

## 2026-09-13 22:11:29 — 性能页最终复核

- 修正页面中的条件文字：v7 已过 250 MHz 时显示“补板级约束”，不再显示“如果仍失败”的旧提示。
- 最终页面：`reports/2026-09-13_221129/2026-09-13_221129_TurboVLA_W8A16当前架构性能分析.html`；机器汇总在同目录。

## 2026-09-13 22:13:00 — 性能页文字复核

- 去掉“如果 v7 仍失败”等过时提示，页面现在按实际通过状态给出下一步：先补板级约束，再做活动回放和 SAIF/VCD 功耗。
- 最终页面：`reports/2026-09-13_221300/2026-09-13_221300_TurboVLA_W8A16当前架构性能分析.html`。

## 2026-09-14 00:59:00 — 真实 TurboVLA 指令流顶层活动回放

- 在独立 `algo/v5_2026-09-13_2316_real_trace_capture/`、`compiler/v5_2026-09-13_2316_real_trace_compiler/`、`arch/v3_2026-09-13_2316_activity_replay_model/` 和 `hw/v8_2026-09-13_2316_integrated_replay_top/` 中完成一次 `libero_spatial` Spatial task 0 的真实 forward 采集、编译和顶层回放。
- GPU 3 采集到 408 个模块事件、6,836 个 dispatch 事件、280 个 Linear 和 24 个动态 BMM；编译器生成 432 条 descriptor、433 条指令（含 END），unknown=0，父子事件没有重复计数。
- 周期模型和 top activity counter 对账：155,780,495 cycles、49,584,342,528 个有效 MAC、PE 时间利用率 41.445%、GEMM 段利用率 43.227%、完整 forward 有效吞吐 159.148 GOPS。当前 768 DSP、250 MHz、单 MAC/DSP 的物理峰值为 384 GOPS，因此实测回放有效吞吐约为峰值的 41.44%。
- Verilator full replay 和代表性 2×3、K=5 阵列逐拍测试均通过。Vivado 2021.2 对 array off、array on/trace off、array on/trace on 三个 OOC 配置均综合通过；array on 为 60,364 LUT、116,980 FF、768 DSP，4.000 ns 目标下 synthesis WNS +2.051 ns。功耗为无 SAIF/VCD 的 vectorless 估算，不写成 TOPS/W。
- 新报告：`reports/2026-09-13_231621/2026-09-13_231621_TurboVLA_activity_replay.html`；机器数据在 `data/v8_2026-09-13_231621/`。本轮仍未做多 suite trace、板上 DMA/DDR、post-route、真实功耗和 LIBERO 成功率。

## 2026-09-14 02:03:01 — 十项历史优化接入新编译器、回放顶层和 OOC 综合

- 从 `NAVIGATION.html` 和历史机器结果中选出十个可落到当前 16×48、768-DSP W8A16 阵列的优化点。新轮次使用 `compiler/v6_2026-09-14_010956_history_optimization/`、`arch/v4_2026-09-14_010956_history_optimization/` 和 `hw/v9_2026-09-14_010956_history_optimization/`，旧 v7/v8 目录保持不动。
- 新编译器修正 64-bit command word 的 descriptor ID 位置，生成 432 个 descriptor 和 433 条指令；24 个 BMM 全部覆盖，unknown=0。BMM tile 数按 batch 修正为 79,807，避免上一轮少算物理 tile。
- 在相同真实 trace 上，基线为 155,780,495 cycles（250 MHz 对应 0.6231 s），全选优化的条件周期模型为 75,254,992 cycles（0.3010 s），下降 51.692%，条件加速 2.070×。主要贡献来自 read/compute/post overlap（单项下降 50.723%）；activation reuse 0.168%，weight reuse 2.429%，vector pipeline 0.973%。其余点在本 trace 上保持 0%，不冒领收益。
- Verilator 完整回放、代表性阵列 tile 和 FIFO push/pop overlap 均通过；顶层 FIFO 修复了 push 与 pop 同拍时丢入队项的问题。RTL 仍为 768 DSP。Icarus 仅作行为 smoke。
- Vivado 2021.2、`xczu7ev-ffvc1156-2-e`、4.000 ns OOC 综合的三种配置均通过。array on 为 60,419 LUT、119,214 FF、768 DSP、WNS +1.884 ns、Fmax 472.6 MHz；TRACE_ENABLE 不改变资源。功耗 3.507 W 是无 SAIF/VCD 的 vectorless 估计，不是 TOPS/W。
- 报告：`reports/2026-09-14_010956/2026-09-14_010956_turbovla_history_optimization_report.html`；机器数据和散列清单在 `data/v9_2026-09-14_010956/`。本轮没有做 post-route、板级 DDR、SAIF/VCD、多 suite 或 LIBERO 成功率。

## 2026-09-14 02:15:24 — 报告和机器汇总最终复核

- 报告脚本在 02:13:49 重新生成，加入 `round_summary.json`，并把阶段图按各自串行小计缩放，避免优化阶段超过 100% 时图形越界。
- HTML 检查通过：5 个内嵌 SVG、12 张表、无 `None`/`NaN` 占位、HTML 结构完整。manifest 已重新记录 HTML、机器汇总和生成脚本 SHA256，并同步到服务器实验目录。
# 2026-09-14 16:21:18 W8A8 scale 子单元 Vivado 综合

- 新增 `hw/v10_2026-09-14_154239_w8a8_scale_subunits/`，不改旧版本。A/B/C 代表性子单元均通过 Vivado 2021.2 OOC 综合和 `opt_design`。
- A：128 DSP、2276 LUT；B：136 DSP、2617 LUT、WNS -0.711 ns；C：136 DSP、3336 LUT、WNS -0.910 ns。目标时钟 4.000 ns，尚未布局布线。
- C 的顶层多驱动问题在第二次综合前修掉，最终结果不含该错误。复核报告和资源明细位于算法轮次 `2026-09-14_154239`。
