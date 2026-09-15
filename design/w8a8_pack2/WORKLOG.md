# TurboVLA W8A8 Pack2 工作记录

## 2026-09-14 11:52:30 — 建立独立版本

这轮工作的目的，是把 HB 最新的 Pack2 INT8 数据通路接到 TurboVLA 的实际算子记录上。工作区独立保存，旧 HB 和 W8A16 结果只读引用。

### 已完成

1. 从 TurboVLA 真实 trace 枚举 408 个模块事件和 6836 个 dispatch 事件。编译器产生 432 个 descriptor，304 个可映射 GEMM/BMM descriptor，128 个行为级辅助 descriptor，未知事件为 0。
2. 将 16×48 物理阵列映射为 96 个逻辑输出列。每个 DSP 使用 HB Pack2 的两个 INT8×INT8 乘积，累加器为 INT32。
3. 生成四种周期模型。current 为 86,410,126 cycles；双缓冲为 41,949,544 cycles；兼容任务队列为 41,947,112 cycles。双缓冲相对 current 减少 51.45% 周期；队列在这条 trace 上只再减少约 0.006%。
4. Pack2 黄金模型完成 100,343 个随机和边界样本，失败数为 0。K=4096 时 27-bit snapshot 不够，需要由编译器标记保护；K≤3072 的代表边界通过。
5. Vivado OOC 综合 1×1、4×4 和 16×48 阵列，DSP 数分别为 1、16、768。16×48 OOC 使用 78,249 LUT、148,168 FF，目标 3.298 ns 下 WNS 为 +1.433 ns。

### 证据边界

- 周期、PE 利用率和有效 GOPS 来自 trace 驱动的 Python 周期模型，不是整机 FPGA 实测。
- Vivado 结果是综合 OOC，不是 place/route 后结果。功耗是 vectorless 估计，没有 SAIF/VCD，因此不报告 TOPS/W。
- 现有 W8A8 文件来自软件假量化筛选；静态 scale、Pack2 部署误差和新的 LIBERO 成功率本轮没有重新验证。
- `unknown=0` 只表示编译器已经给每个 trace 事件分配了 `rtl_gemm`、`rtl_bmm` 或 `aux_behavior` 类别，不表示 LayerNorm、GELU、DINO 等辅助算子已经有完整 RTL。

## 2026-09-14 12:35:11 — 报告和服务器镜像

- 生成 `reports/2026-09-14_123511/2026-09-14_123511_turbovla_w8a8_pack2_arch_report.html`。HTML 自带 6 个 SVG，扫描没有发现 `None`、`NaN` 或未闭合标签。
- 报告已经用 `open_in_codex` 打开，并保存到服务器 `/home/nc23/experiments/turbovla_w8a8_pack2_2026-09-14_123511/`。
- 本地和服务器 HTML SHA256 相同：`1260a4378873899737a955ef155c461bf1cfbd97857061a47860e8166b993b35`。

## 2026-09-14 12:36:48 — 补充双频率吞吐表

- 报告补充 250 MHz 和 303.215 MHz 两个频率下的有效 GOPS 对照，重新生成 `reports/2026-09-14_123648/2026-09-14_123648_turbovla_w8a8_pack2_arch_report.html`。
- 最新 HTML 本地/服务器 SHA256：`12ef1086ab9e31d850b0a0d65e695a7cfed6fbb5cee1e9219f6e81f367be49d3`。

## 2026-09-15 16:18:22 — 建立时序版 RTL，完成本地可展开检查

- 新版本：`hw/v2_2026-09-15_155202_timing_pipeline/`。旧 v1 RTL 和 OOC 结果保持不动。
- 在 DSP P 输出与 Pack2 字段校正之间加入 `P_pipe_r`；在阵列边界加入输入寄存和读出寄存。阵列仍为 16×48、768 DSP、每颗 DSP 两个 INT8×INT8 产品。
- Icarus 冒烟通过 4/4：Pack2 乘法器、2×3 timing array、回放顶层、`tvla_w8a8_pack2_system_top` 展开。四项合计约 1.6 s，日志在 `hw/v2_2026-09-15_155202_timing_pipeline/data/functional/`。
- 已准备 250 MHz（4.000 ns）和 303.215 MHz（3.298 ns）两个独立 Vivado 工程入口，并写入结果收集器。当前本机没有 Vivado，连接 `192.168.2.5` 和 `101.6.64.77` 均超时，所以两个实现状态仍是“未执行”，没有虚构 WNS/Fmax/功耗。
- 生成说明页：`reports/2026-09-15_161822/2026-09-15_161822_timing_pipeline_report.html`。页面把历史 v1 OOC、Python 周期模型、本地 RTL 冒烟和待执行 Vivado 结果分开说明。

## 2026-09-15 16:21:42 — 说明页最终检查

- 最终页面：`reports/2026-09-15_162142/2026-09-15_162142_timing_pipeline_report.html`。
- HTML 解析通过，未发现 `None`、`NaN`、`undefined` 或 `not_available`；页面内联架构图和三张数据图，两个 Vivado 频率点明确显示为“未执行”。

## 2026-09-15 16:28:42 — 记录两个频率点的尝试结果

- 用本地包装器实际尝试 250 MHz（4.000 ns）和 303.215 MHz（3.298 ns）；两个单元均在约 0.05 s 内记录为“未执行”，原因是本机没有 Vivado。
- `data/vivado_results.json` 已收录每个频率的开始、结束、耗时和原因。最新说明页为 `reports/2026-09-15_163224/2026-09-15_163224_timing_pipeline_report.html`。

## 2026-09-15 19:17:06 — 使用本机 Vivado 完成两个频率的实现

- 复查后确认本机 Vivado 位于 `D:/software/Vivado/2021.2/bin/vivado.bat`。前一条“本机没有 Vivado”只是当时 shell PATH 检查失败，保留作历史记录，不再作为当前结论。
- 新版本 `hw/v3_2026-09-15_174639_vivado_impl/` 在 `tvla_w8a8_pack2_impl_top` 上完成综合、布局、物理优化和布线。250 MHz（4.000 ns）和 303.215 MHz（3.298 ns）两档均生成 routed checkpoint。
- 250 MHz：post-route WNS +0.241 ns、推导 Fmax 266.0 MHz、77,770 LUT、179,363 FF、768 DSP、0 BRAM、vectorless 5.310 W；实现耗时 1,497 s。
- 303.215 MHz：post-route WNS +0.103 ns、推导 Fmax 313.0 MHz、77,860 LUT、179,320 FF、768 DSP、0 BRAM、vectorless 6.924 W；实现耗时 2,022 s。
- 两档 routing errors 均为 0。DRC 没有 Error，但存在 2 项顶层 I/O critical warning（未给 LOC/IOSTANDARD）和 768 项 DSP 输入未寄存的 warning；因此这是可布局布线的 generic top，不是已绑定开发板引脚的 bitstream。
- 新报告：`reports/2026-09-15_192300/2026-09-15_192200_TurboVLA时序实现与架构分析.html`；机器可读结果在同目录 `vivado_real_results.json`。

## 2026-09-15 19:25:12 — 重新生成最终说明页

- 修正报告中的时序字段，把 Vivado 的 pulse-width slack 标成 `WPWS`，不再把 hold 的 `NA` 误写成 hold 数字。
- 最终页面：`reports/2026-09-15_192512/2026-09-15_192512_TurboVLA时序实现与架构分析.html`。同目录保留 `vivado_real_results.json`，数字直接从两个 post-route 报告解析。
- 页面自检通过：没有 `None`、`NaN`、`undefined` 或未解析字段；旧页面和旧 Vivado 输出均未覆盖。
