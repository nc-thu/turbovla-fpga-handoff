# TurboVLA W8A16 v5：顶层实现后时序与功耗

生成时间：2026-09-13 16:36:09

这一轮使用 v4 timing-fixed RTL 的独立拷贝，只做系统 top 的 Vivado implementation：

```text
synth_design → opt_design → place_design → phys_opt_design
→ route_design → post-route phys_opt_design
```

目标器件为 `xczu7ev-ffvc1156-2-e`，目标时钟为 3.298 ns。实现后报告包括：

- `post_route_timing.rpt`：布线后的 WNS、TNS、关键路径和时钟信息；
- `post_route_utilization.rpt`：实现后的 LUT、FF、DSP、BRAM；
- `post_route_power.rpt`：Vivado 的 vectorless 功耗估计，不能替代板上电流测量；
- `post_route_drc.rpt`、`post_route_status.rpt`、`post_route_congestion.rpt`：实现完整性和布线状态；
- `post_route.dcp`：最终布线 checkpoint。

这是一个没有板级 pin、AXI/DDR 和时钟输入延迟约束的 OOC 系统壳。没有写 bitstream。功耗报告默认没有真实切换率，所以只能作为早期相对比较，不能写成芯片实测能效。

源代码来自：
`hw/v4_2026-09-13_150700_w8a16_timing_fixed_rtl/`。
本目录中的 `rtl/` 和 `synth/top_w8a16_system.sv` 是本轮独立拷贝，旧版本不修改。

## 2026-09-13 17:33:13 结果

- implementation 命令成功结束，route status 为 fully routed，184,104 条可路由网络全部完成，unrouted=0。
- 3.298 ns 目标没有达到：post-route WNS=-0.461 ns，按 WNS 推算最高频率约 266.0 MHz；最长数据路径为 3.740 ns（逻辑 2.056 ns、布线 1.684 ns）。
- 资源为 66,255 LUT、118,169 FF、785 DSP、0 BRAM。DSP 数量与 v4 相同，16×48 阵列仍为 768 DSP。
- `report_power` 给出 5.678 W（动态 5.058 W、静态 0.620 W），但这是没有 SAIF/VCD 的 vectorless 估算，不能当作板上实测功耗或能效。
- DRC 为 0 Error、4 Warning、1 Advisory；主要提示 DSP 输入／输出 pipeline 和 OOC 缺板级 I/O 约束。没有生成 bitstream。

机器可读归档在：
`data/v5_2026-09-13_173359_implementation/implementation_results.json`。
中文汇总页在：
`reports/2026-09-13_174037/2026-09-13_174037_turbovla_w8a16_post_route_impl.html`。
