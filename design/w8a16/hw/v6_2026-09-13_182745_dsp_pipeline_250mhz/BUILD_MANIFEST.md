# v6 构建清单

生成时间：2026-09-13 19:33:56

| 项目 | 内容 |
|---|---|
| RTL 来源 | v4/v5 工作区的 W8A16 RTL；v6 只改 w8a16_mult.sv、w8a16_pe.sv、w8a16_action_path.sv |
| 器件 | xczu7ev-ffvc1156-2-e |
| 时钟 | clk，4.000 ns，250 MHz |
| Vivado 流程 | synth_design → opt_design → place_design → phys_opt_design → route_design → post-route phys_opt_design |
| 阵列 | 16×48，768 DSP，单时钟 |
| Verilator | 11/11 PASS，153 s；日志位于 sim/logs/verilator_run.json |
| UNISIM | 未完成；服务器无 xvlog |
| route | 184306/184306 fully routed，routing errors=0 |
| timing | WNS -0.050 ns，TNS -4.464 ns，246.9 MHz 估算；250 MHz 未过 |
| resources | 66368 LUT，117105 FF，785 DSP，0 BRAM |
| power | 4.478 W vectorless estimate，Medium confidence |
| DRC | 821 violations，0 Error；DPIP-2 从 v5 的 1,571 降到 34（约减少 97.8%），仍有其他 DSP pipeline warning 与 OOC advisory |
| bitstream | 未生成 |

## 原始文件

- impl/runs/2026-09-13_182745_system_250mhz/post_route_timing.rpt
- impl/runs/2026-09-13_182745_system_250mhz/post_route_critical_paths.rpt
- impl/runs/2026-09-13_182745_system_250mhz/post_route_utilization.rpt
- impl/runs/2026-09-13_182745_system_250mhz/post_route_power.rpt
- impl/runs/2026-09-13_182745_system_250mhz/post_route_drc.rpt
- impl/runs/2026-09-13_182745_system_250mhz/post_route.dcp

机器可读汇总：../../data/v6_2026-09-13_193556_implementation/implementation_results.json。
结果页：../../reports/2026-09-13_193800/2026-09-13_193800_turbovla_w8a16_v6_250mhz_implementation.html。

## 边界

post-route 是真实实现结果；功耗没有真实切换活动；OOC 没有板级 I/O 和时钟约束。v5 与 v6 的资源／频率对照只能用于方向判断，因为目标周期和 RTL 同时变化。
