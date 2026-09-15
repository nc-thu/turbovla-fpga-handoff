# v7 构建清单

生成时间：2026-09-13 22:00:24

| 项目 | 内容 |
|---|---|
| 独立目录 | `hw/v7_2026-09-13_195800_clr_partition_250mhz/` |
| RTL 改动 | `rtl/w8a16_sysarr.sv`；`clr` 按每 8 列分组，共 16×6 个控制组网 |
| 继承内容 | v6 的 DSP AREG/BREG/MREG/PREG、PE product register、action-path product/drain |
| 器件 | `xczu7ev-ffvc1156-2-e` |
| 时钟 | `clk`，4.000 ns，250 MHz |
| Vivado 流程 | synth_design → opt_design → place_design → phys_opt_design → route_design → post-route phys_opt_design |
| 时序 | WNS +0.006 ns，TNS 0，0 个 setup 失败端点，Fmax 250.38 MHz，**250 MHz 通过** |
| 关键路径 | runtime `word_r_reg[58]` → array PE `acc_r_reg[15]/CE`；3.889 ns，route 87.863% |
| 资源 | 66,375 LUT、117,104 FF、785 DSP、0 BRAM |
| 功耗 | 4.670 W vectorless，动态 4.056 W，静态 0.614 W，Medium |
| 布线 | 184,322/184,322 fully routed；unrouted=0；routing errors=0 |
| DRC | 821 violations，0 Error；DPIP-2 34、DPOP-3 1、DPOP-4 17、RTSTAT-10 1、AVAL-155 768 |
| Verilator | 11/11 PASS，159 s；完整阵列 768 DSP |
| UNISIM | 未完成；服务器无 `xvlog` |
| 机器汇总 | `data/v7_2026-09-13_220100_implementation/implementation_results.json` |
| 性能页 | `reports/2026-09-13_221300/2026-09-13_221300_TurboVLA_W8A16当前架构性能分析.html` |
| 原始报告 | `impl/runs/2026-09-13_195800_system_250mhz/` |
| bitstream | 未生成 |

## 复现

```text
服务器 Verilator：cd sim && PATH=/home/nc23/.conda/envs/vsim/bin:$PATH bash run_verilator.sh
Vivado：D:\software\Vivado\2021.2\bin\vivado.bat -mode batch -source impl\impl_top_250mhz.tcl -tclargs w8a16_system_top <output_dir> 16 48
收集：python scripts/collect_v7_implementation.py <output_dir> --output-dir data/v7_<timestamp>_implementation
生成性能页：python scripts/generate_performance_report.py --v5 data/v5_2026-09-13_173359_implementation/implementation_results.json --v6 data/v6_2026-09-13_193556_implementation/implementation_results.json --v7 data/v7_<timestamp>_implementation/implementation_results.json --output reports/<timestamp>/<timestamp>_TurboVLA_W8A16当前架构性能分析.html
```
