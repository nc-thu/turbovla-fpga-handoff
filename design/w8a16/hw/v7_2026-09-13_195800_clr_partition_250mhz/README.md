# v7：`clr` 扇出分区与 250 MHz 实现

生成时间：2026-09-13 22:00:24（结果收集时间）

这一轮从 v6 独立复制出来，只改 `w8a16_sysarr.sv`。原来一条 `clr` 控制线直接连接整个 16×48 阵列的 PE 累加器，布线负担很重。v7 保持控制时序和 PE 算法不变，把它拆成每 8 列一组的保留网络，再连接到各组 PE。

## 改动

- `rtl/w8a16_sysarr.sv`：增加 `clr_group[16][6]`，每组最多连接 8 个 PE 列；使用 `keep/dont_touch/max_fanout` 保留分区。
- 未修改 `w8a16_mult.sv`、`w8a16_pe.sv`、`w8a16_gemm.sv` 和动作路径协议。
- 这是物理扇出修正，不增加时钟周期，不增加 DSP。

## 验证

- 服务器 Verilator：11/11 测试通过，耗时 159 s；完整阵列仍为 768 DSP。
- 包含 PE、2×3 阵列、完整 16×48 阵列、GEMM、激活、向量、DMA、ISA、runtime 和 system smoke。
- Icarus/UNISIM 仍未完成，服务器环境没有 `xvlog`。

## Vivado post-route

- 工具：Vivado 2021.2；器件：`xczu7ev-ffvc1156-2-e`；目标周期：4.000 ns（250 MHz）。
- 综合、opt、place、phys_opt、route 和 post-route phys_opt 全部完成，184,322 条可路由网络全部完成，未布线为 0，routing errors 为 0。
- **WNS +0.006 ns，TNS 0，setup 失败端点 0；按 WNS 推算 Fmax 250.38 MHz，因此本轮 post-route 通过 250 MHz。**
- 关键路径从 `u_runtime/u_ctrl/word_r_reg[58]/C` 到 `u_gemm/u_arr/g_row[9].g_col[47].u_pe/acc_r_reg[15]/CE`，数据路径 3.889 ns；逻辑 0.472 ns（12.137%），布线 3.417 ns（87.863%）。路径仍是控制到 PE CE，但分区后布线延迟下降。
- 资源：66,375 LUT、117,104 FF、785 DSP、0 BRAM。相比 v6，LUT 增 7（约 0.011%），FF 减 1，DSP 不变。
- vectorless 功耗：4.670 W（动态 4.056 W、静态 0.614 W，Medium）；没有 SAIF/VCD，不是上板实测能耗。
- DRC：821 项，0 Error；DPIP-2 34、DPOP-3 1、DPOP-4 17、RTSTAT-10 1、AVAL-155 advisory 768。

机器汇总在 `../../data/v7_2026-09-13_220100_implementation/`。当前架构性能页在 `../../reports/2026-09-13_221300/`；该页重新从 v5/v6/v7 JSON 生成，并补充了 v6→v7 的前后百分比。Vivado 原始报告和 DCP 在 `impl/runs/2026-09-13_195800_system_250mhz/`。

## 边界

这仍是 OOC wrapper，没有板级 pin、时钟 buffer、AXI/DDR 和 I/O delay 约束；没有生成 bitstream。250 MHz 结论只适用于本轮 4.000 ns OOC post-route 约束。功耗是 vectorless 估算。完整 TurboVLA 视觉／语言／采样和 LIBERO 端到端运行没有在本轮完成。
