# TurboVLA W8A16 工作日志

## 2026-09-12 23:54:06 — 建立独立工作区

本轮不修改旧算法、旧量化结果、共享编译器接口和正在运行的硬件实验。新工作先用已有 TurboVLA 资料建立真实算子清单，再完成整数黄金模型、描述符、周期模型和 W8A16 PE 的快速验证。

## 2026-09-13 01:27:06 — 增加非 GEMM 指令和 compiler→RTL smoke

这次把工作范围从 GEMM 扩到一条可检查的最小运行时路径。编译器现在发出固定 64 bit 指令字，RTL 端增加 DMA、ISA 控制、向量和激活单元，并由 runtime 串起一条 1×7×8 的动作投影命令。

服务器 `/home/nc23/experiments/turbovla_w8a16/2026-09-13_010117/` 上的 Verilator 回归在 119 秒内通过 10 个测试，Icarus 在秒级通过 4 个短 smoke。当前结果证明的是指令、地址顺序、定点边界和动作打包一致；它没有测完整 TurboVLA 的视觉／语言／采样，也没有给出 LIBERO 成功率。资源与时序没有宣称改善（0% PPA 改善，Vivado 未运行）。

## 2026-09-13 01:33:37 — 收紧动作 smoke 的数据口径

报告和 `libero_action_probe.json` 现在明确写出：RTL smoke 使用的是确定性的 INT16 格式化状态向量，借用 LIBERO 任务／初始状态元数据来标记动作格式，不是把真实 RGB-D 张量送进硬件。这样可以证明编译器字、动作打包和 RTL 数值对拍，但不会把它误报成 TurboVLA 推理或 LIBERO 成功率。

## 2026-09-13 10:52:55 — 完成 Vivado 顶层逻辑综合

本轮先把旧的 project/non-project 混合脚本改成非工程 batch 流程，并新增 `w8a16_system_top` 综合壳。它把 runtime、256-bit 激活 DMA、384-bit 权重 DMA、向量激活和 REQUANT 一起展开，检查这些模块能否由同一次 Vivado 综合读取。

本机 Vivado 2021.2 的四个配置都完成 `synth_design`。16×48 阵列使用 768 个 DSP，综合表为 57,331 LUT 和 110,656 FF；3.298 ns 约束下 WNS 2.149 ns，按综合 slack 推得约 870 MHz。这只是逻辑综合估算，不代表布线后的频率。系统壳为 52,743 LUT、2,814 FF、35 DSP，WNS -4.528 ns；负 slack 主要来自动作路径的宽组合饱和／打包逻辑。综合 DRC 为 0 个 Error，但报告有 DSP 输入／输出流水 warning，后续若做板级实现需处理。

原始日志、DCP 和报告在 `hw/v1_2026-09-12_2354_w8a16_rtl/synth/runs/2026-09-13_104234/`，汇总在 `data/vivado_synth_results.json` 和 `data/vivado_synth_results.csv`。本轮不宣称 PPA 提升（0%），未做 post-route、功耗和完整 LIBERO。

## 2026-09-13 11:02:37 — 重新生成机器可读汇总和 HTML

使用完整 Vivado launcher 时间重新收集四个综合结果，并生成 `reports/2026-09-13_110237/2026-09-13_110237_turbovla_w8a16_report.html`。关键数值未变；本次只是修正归档耗时口径并检查报告中的系统负 WNS、阵列资源和未完成项。

## 2026-09-13 13:40:00 — v2 camera-ready 候选验证

这轮先修 top 的时序，再检查编译器和 RTL 是否真的沿同一条命令路径工作。动作路径的 40-bit 累加、bias、tanh 和输出打包已经拆成多拍；LayerNorm／Softmax 的归一化除法改成逐位迭代，常数乘法改成寄存后的移位加法。v11 系统 top 在 3.298 ns 目标下没有 setup 失败端点，最差路径 3.288 ns，综合频率约 303.2 MHz。最差路径位于 LayerNorm 的除法结果寄存到输出寄存器之间，仍需 post-route 才能判断真实时序余量。

新的数据链把 DMA 的读回 beat 写入 runtime 的 INT16 scratch bank，把权重 beat 写入固定目的地址，避免可变数组索引生成大写译码器。矩阵指令的 `flags[7]` 启动 16×48、768-DSP 阵列并等待 done；系统 smoke 还实际送出一个生产阵列 feed beat。小动作路径仍使用 1×7×8 作为快速对拍，避免把单个 smoke 误写成完整 TurboVLA 张量执行。

服务器 `/home/nc23/experiments/turbovla_w8a16/v2_retest_20260913_1332/` 的 Verilator 11 项回归用时 144 s 并全部通过；Icarus 短 smoke 用时 1 s 并全部通过。编译器现在对长度超过 65535 的向量指令自动分片，83 条逻辑指令变成 172 条 transport word；Python 检查和 ISA 解码通过。UNISIM 因服务器没有 `xvlog`，不能冒充已验证的 DSP48E2 原语。

当前 camera-ready 交付可以证明：W8A16 数值边界、编译器字格式、DMA／向量／激活／runtime／阵列接口和顶层综合是可检查的。仍不能证明：真实 TurboVLA 的 DINO/T5、采样循环、LIBERO 环境动作、板级 AXI/DDR、post-route、功耗或端到端成功率。

## 2026-09-13 15:37:31 — v4 top 时序修复完成

v4 从 v3 复制出独立目录，只改 `w8a16_vector_mul.sv`：把 `MUL_SCALE` 的乘积先写入 32-bit `product_r`，下一拍再做移位和 INT16 饱和。这样没有改变 W8A16 数值公式，只增加了一个 valid 延迟；Verilator runtime、system 和所有激活／向量测试仍通过。

本轮在本机 Vivado 2021.2 上综合 `w8a16_system_top`。目标 3.298 ns，运行 310 s；WNS +0.310 ns，关键路径从动作权重寄存器到 40-bit 累加器，综合估算 Fmax 334.7 MHz。资源是 67,448 LUT、118,149 FF、785 DSP、0 BRAM。这个余量比 v3 的 +0.067 ns 更充足，但仍不能替代布线后的时序。

v4 的编译器 schema、descriptor、成本模型和 ISA 对拍均为 PASS；程序为 83 条逻辑操作、172 条 transport word。服务器 Verilator 11 项（144 s）和 Icarus 5 项短 smoke 通过。array 资源记录继承 v3，并在机器可读文件中保留来源说明。报告为 `reports/2026-09-13_153731/2026-09-13_153731_turbovla_w8a16_camera_ready.html`。

## 2026-09-13 17:40:37 — v5 完成顶层 post-route implementation

用户要求获取实现后的时序和功耗。本轮没有改 v4 RTL，而是复制到 `hw/v5_2026-09-13_163609_post_route_impl/`，按同一 3.298 ns 目标跑完整 Vivado implementation。Vivado 从 16:38:39 开始，到 17:33:13 结束，launcher 墙钟耗时 3274.176 s。

route status 为 fully routed，184,104 条可路由网络全部完成。最终 timing summary 显示 WNS=-0.461 ns、TNS=-1197.739 ns、8,075 个 setup 失败端点；关键路径从 `u_runtime/u_action/k_r_reg[0]_replica_1/C` 到 `u_runtime/u_action/acc_r_reg[4][9]/D`，数据路径 3.740 ns，逻辑 2.056 ns、布线 1.684 ns。按 `1000/(3.298-(-0.461))` 推算的频率约 266.0 MHz，所以当前 303.2 MHz 目标没有过。

实现后资源为 66,255 LUT、118,169 FF、785 DSP、0 BRAM。`report_power` 的 vectorless 估算为 5.678 W，其中动态 5.058 W、静态 0.620 W，置信度 Medium；因为没有 SAIF/VCD，这个数只适合做早期比较，不能当作板上功耗或 TOPS/W。

DRC 有 0 Error、4 Warning、1 Advisory；警告主要是 DSP 输入／输出 pipeline 建议和 OOC 顶层没有板级 I/O 约束。没有生成 bitstream。机器可读结果在 `data/v5_2026-09-13_173359_implementation/implementation_results.json`，报告在 `reports/2026-09-13_174037/2026-09-13_174037_turbovla_w8a16_post_route_impl.html`。

## 2026-09-13 14:52:54 — v3 top 时序修复与编译器 sideband 完整性

这轮把上一轮系统 top 的最后一条负时序路径再拆了一拍。LayerNorm 和 Softmax 在逐位除法结束后先进入 `S_SATURATE`，下一拍才写回结果寄存器。v13 综合使用 3.298 ns 目标时钟，WNS +0.067 ns、0 个 setup failure、关键数据路径 3.220 ns，综合估算 309.5 MHz。这个余量只说明逻辑综合过线；布线后的频率还没有测。

编译器从 v2 升到 v3。长向量不再只有 `chunk_index`，还保存 `logical_id`、`base_length`、`transport_length`、元素／beat 偏移、tile shape/grid 和 `compact_8bit`／`sideband_32` 地址模式。验证器会检查每组分片是否从 0 连续覆盖到逻辑长度。v3 程序 83 条逻辑操作、172 条 transport word、18 个 opcode，成本模型总下界 633,933 拍，ISA 解码和动作 smoke 均 PASS。

重新从 v3 的四个 Vivado run 收集数据：1×1 为 63 LUT/166 FF/1 DSP，4×4 为 1,216 LUT/2,470 FF/16 DSP，16×48 为 57,331 LUT/110,656 FF/768 DSP，系统 top 为 67,432 LUT/118,139 FF/785 DSP。系统 Verilator 11 项和 Icarus 5 项短 smoke 均通过；综合 DRC 为 0 Error，但 OOC 的 2 个板级接口约束问题和 DSP pipeline 提示保留在报告中。

交付目录为 `reports/2026-09-13_145254/`，报告中的数字来自 `data/v3_2026-09-13_140118/` 和 v3 原始综合报告。当前结果可作为 RTL/编译器 camera-ready 候选，但仍不代表完整 TurboVLA 已在 FPGA 上运行。
## 2026-09-13 19:33:56 — v6 DSP 输入／输出 pipeline 与 250 MHz 实现

用户要求先补 DSP 输入／输出 pipeline，并重新安排关键寄存器边界，再用 250 MHz 约束实现。本轮从 v5 复制到 hw/v6_2026-09-13_182745_dsp_pipeline_250mhz/，只改 w8a16_mult.sv、w8a16_pe.sv 和 w8a16_action_path.sv。DSP A/B 输入启用 AREG/BREG=1，乘法与输出保留 MREG/PREG=1；action path 的 MAC 操作数、乘积和累加末尾 drain 分开寄存。

服务器 Verilator 从 10 项扩展到 11 项，PE、2×3、完整 16×48、GEMM、激活、向量、DMA、ISA、runtime 和 system 全部 PASS，完整阵列仍为 768 DSP，运行 153 s。UNISIM 冒烟继续 unavailable：服务器只有 Verilator，没有 xvlog；不能写成 UNISIM 已通过。

Vivado 2021.2 从 2026-09-13 18:38:56 跑到 19:33:55，墙钟 3299 s（约 55.0 min）。目标周期 4.000 ns，综合、布局、物理优化、布线和 post-route phys_opt 全部命令成功。184,306 条可路由网络全部布线，routing errors=0。

最终 post-route timing 为 WNS=-0.050 ns、TNS=-4.464 ns、192 个 setup 失败端点；按 1000/(4.000-0.050) 推算约 246.9 MHz，250 MHz 还差 0.050 ns。关键路径从 u_runtime/u_ctrl/word_r_reg[61]/C 到 u_gemm/u_arr/g_row[6].g_col[45].u_pe/acc_r_reg[10]/CE，3.946 ns 中逻辑 0.301 ns、布线 3.645 ns。pipeline 已切开乘积／累加链，但当前最差路径变成控制清零与 CE 的高扇出布线。

post-route 资源为 66,368 LUT、117,105 FF、785 DSP、0 BRAM。相比 v5 的 66,255 LUT、118,169 FF、785 DSP，LUT 增 113、FF 减 1,064；由于版本和目标时钟同时变化，这只是方向参考。vectorless 功耗 4.478 W（动态 3.865 W、静态 0.613 W、Medium confidence），没有 SAIF/VCD，不是板上实测。

DRC 共有 821 项，0 Error；规则为 DPIP-2 34（v5 为 1,571，减少约 97.8%）、DPOP-3 1、DPOP-4 17、RTSTAT-10 1、AVAL-155 advisory 768。下一步应先把阵列 clr/CE 按行或列分区并加局部寄存器，再处理 runtime/vector/action 中剩余的 DSP pipeline warning。机器汇总在 data/v6_2026-09-13_193556_implementation/，报告在 reports/2026-09-13_193800/2026-09-13_193800_turbovla_w8a16_v6_250mhz_implementation.html。OOC 没有板级 pin、AXI/DDR 和时钟 buffer 约束，也没有生成 bitstream。

## 2026-09-13 22:00:48 — v7 `clr` 扇出分区完成

v7 从 v6 复制到 `hw/v7_2026-09-13_195800_clr_partition_250mhz/`。我先读 v6 的 post-route 最差路径，确认 3.946 ns 中 3.645 ns（92.4%）来自 `clr` 高扇出控制线，而不是 INT16×INT8 乘法或 INT40 加法。于是只在 `w8a16_sysarr.sv` 中把 48 列分为每组 8 列的 `clr_group`，保留这些分组网络，PE 的时钟协议和清零优先级不变。

Verilator 11 项全部通过，耗时 159 s；完整阵列仍为 768 DSP。Vivado post-route 结果为 WNS +0.006 ns、TNS 0、setup 失败端点 0，按 WNS 推算 Fmax 250.38 MHz，4.000 ns（250 MHz）目标通过。相对 v6，关键路径总延迟从 3.946 ns 降到 3.889 ns（约减少 1.4%），其中布线从 3.645 ns 降到 3.417 ns（约减少 6.3%）。这说明小分区解决了最后的控制布线瓶颈，但路径仍落在 runtime→PE `clr/CE`，后续若要留更多余量应补板级约束并继续观察该网络。

资源为 66,375 LUT、117,104 FF、785 DSP、0 BRAM。相对 v6，LUT 增 7（约 0.011%），DSP 不变。vectorless 功耗为 4.670 W，较 v6 的 4.478 W 增加约 4.3%；没有 SAIF/VCD，不能把它当作能效实测。route 184,322/184,322 完成，DRC 821 项、0 Error；DPIP-2 仍为 34。

本轮新增性能页 `reports/2026-09-13_220048/2026-09-13_220048_TurboVLA_W8A16当前架构性能分析.html`。页面用结构图、频率图、关键路径延迟图和功耗图解释当前结果，并明确区分阵列峰值（250 MHz 下 192 GMAC/s）与尚未接入真实 TurboVLA 指令流的动态 PE 利用率。机器汇总位于 `data/v7_2026-09-13_220100_implementation/`。OOC 仍无板级 I/O、AXI/DDR 和时钟 buffer 约束，没有生成 bitstream；Icarus/UNISIM、板级功耗和端到端 LIBERO 未做。

## 2026-09-13 22:08:12 — 性能页复核

重新运行 `scripts/generate_performance_report.py`，并让脚本从 v5 的原始 DRC 报告补读 DPIP-2。新页面包含 v6→v7 的前后百分比表：Fmax 246.914→250.376 MHz（+1.402%），路径 3.946→3.889 ns（-1.445%），布线 3.645→3.417 ns（-6.255%），LUT 66,368→66,375（+0.011%），vectorless 功耗 4.478→4.670 W（+4.288%）。页面仍明确说明动态 PE 利用率和板上能效没有测量。

新页面：`reports/2026-09-13_220812/2026-09-13_220812_TurboVLA_W8A16当前架构性能分析.html`；机器汇总：同目录 `performance_summary.json`。

## 2026-09-13 22:11:29 — 性能页最终复核

修正了 v7 已通过 250 MHz 后仍出现的旧条件提示，并重新生成最终页面。页面和机器汇总位于 `reports/2026-09-13_221129/`。

## 2026-09-13 22:13:00 — 性能页文字复核

把下一步建议改成当前真实状态：v7 已过 OOC 250 MHz，所以先补板级约束和真实活动回放，不再提示“如果仍失败”。最终页面在 `reports/2026-09-13_221300/`。

## 2026-09-14 00:59:00 — 真实指令流接入 replay top

这轮先在服务器 GPU 3 上跑一次真实 TurboVLA forward。输入是 `libero_spatial` Spatial task 0，固定 seed=7、两路 256×256 图像、instruction 和 8 维状态。采集器记录了 408 个模块边界事件和 6,836 个 TorchDispatch 事件；其中 280 个 Linear 和 24 个动态 BMM 进入编译器覆盖。

编译器把模块事件变成 432 条 512-bit descriptor 和 433 条 64-bit 指令（含 END）。描述符保存 M/N/K、scale、依赖、tile、流量和周期，activation/weight payload 按 SHA256 去重保存。编译检查 module/BMM 覆盖、unknown=0 和父子事件不重复均通过。

新的 `tvla_replay_top` 使用 16×48、768-DSP W8A16 阵列、descriptor FIFO、activity counter 和行为级 AUX 事件。完整 replay 不跑 155.8M 个实际 RTL 时钟，而是每条 descriptor 在一个控制时钟内累加虚拟事件周期；代表性 2×3、K=5 tile 仍走真实阵列逐拍对拍。这样完整回放用微秒级仿真完成，且没有把 fallback 算子冒充阵列工作。

顶层计数器与软件摘要一致：总计 155,780,495 cycle、有效 MAC 49,584,342,528、输出 159,228,360 bytes、descriptor FIFO 最大占用 1。按 250 MHz 换算完整 replay 为 0.623 s；PE 时间利用率 41.445%，GEMM 映射段利用率 43.227%，有效吞吐 159.148 GOPS（峰值 384 GOPS）。这些是周期模型加 RTL counter replay，不是板上时延。

本机 Vivado 2021.2、`xczu7ev-ffvc1156-2-e`、4.000 ns 目标下三组 OOC synth 均通过。array on/trace on 为 60,364 LUT、116,980 FF、768 DSP、0 BRAM，WNS +2.051 ns；TRACE_ENABLE 当前没有增加资源。功耗为 vectorless、无 SAIF/VCD，不能换算 TOPS/W。新报告在 `reports/2026-09-13_231621/`。

## 2026-09-14 02:03:01 — 历史优化点接入和最终复核

我先把 `NAVIGATION.html` 中已经做过的优化按“能否作用于当前 W8A16、是否有历史证据、是否增加 DSP”筛了一遍，冻结十项清单。新轮只引用上一轮真实 TurboVLA task 0 trace，不重新采集大张量，也不改 v7/v8。

编译器 v6 将真实事件编成 432 个 descriptor、433 条命令。它修正了旧版 command word 中 descriptor ID 的编码位置，并把 24 个 BMM 的 batch tile 计入物理任务数。基线周期 155,780,495；全选条件模型 75,254,992，减少 51.692%。模型里的有效 GOPS 从 159.148 增到 329.442，PE 利用率从 41.445% 增到 85.792%；二者都不是板上测量。valid MAC 保持 49,584,342,528，没有把跳过的工作算作完成量。

本轮发现并修正一个顶层 bug：descriptor FIFO 在同一个时钟同时 push 和 pop 时，旧代码的两个非阻塞赋值会互相覆盖，导致入队项丢失。现在用 `{push,pop}` 单一分支更新计数，并保留 END 的 `cmd_fire` 路径。Verilator 完整回放、2×3 K=5 tile 和 FIFO overlap 回归都 PASS。

Vivado OOC 重新跑了 array off、array on/trace off、array on/trace on。三项均 PASS；array on 为 60,419 LUT、119,214 FF、768 DSP，WNS +1.884 ns，Fmax 472.6 MHz。活动监视器没有增加综合资源。当前没有 post-route、SAIF/VCD 和板级带宽证据。

报告生成于 2026-09-14 02:03:01，路径为 `reports/2026-09-14_010956/2026-09-14_010956_turbovla_history_optimization_report.html`。报告把历史继承项、条件周期模型和本轮实测回归分开写，并保留未完成项。

## 2026-09-14 02:15:24 — 报告最终复核

报告在 02:13:49 重新生成，并额外写出 `reports/2026-09-14_010956/round_summary.json`。阶段图改成按每行串行小计缩放；优化项的 121.92% 现在以右侧小计标签显示，不会把横条画出坐标范围。HTML 有 5 个 SVG、12 个数据表，无 `None`/`NaN`，结构检查通过。manifest 已包含最终报告和汇总文件的散列，并同步到服务器。
