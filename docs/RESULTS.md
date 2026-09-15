# 已验证结果和下一步

更新时间：2026-09-16 03:33:14

## 已验证

- Pack2 乘法器、时序阵列、回放顶层和 system_top 展开检查：4/4 通过。
- Vivado 2021.2 在 `xczu7ev-ffvc1156-2-e` 上完成 250 MHz 和 303.215 MHz 两档综合、布局和布线。
- 两档都保留 768 DSP，routing error 为 0；post-route setup WNS 为 +0.241 ns 和 +0.103 ns。
- 250 MHz 实现的 LUT/FF/DSP/BRAM 为 77,770/179,363/768/0；303.215 MHz 实现为 77,860/179,320/768/0。

## 仍需补齐

- generic top 的板级 LOC、IOSTANDARD 和真实 DDR 约束；当前 DRC 的 NSTD-1/UCIO-1 是接口约束缺失，不是内部逻辑时序错误。
- DSP 输入侧 AREG/BREG 等寄存器的架构取舍。当前实现时序已过，但 Vivado 对 768 个 DSP 给出输入未寄存 warning。
- SAIF/VCD 活动文件和板级功耗；当前 5.310 W/6.924 W 只是 vectorless 估算。
- TurboVLA 全模型的真实 W8A8 整数 trace、完整 fallback 复放和 LIBERO 正式成功率。

## 2026-09-16 全模型 generic top

- 最终实现目录：`design/w8a8_pack2/full_model_v2/`，Vivado run `vivado_runs_20260916_0248`。
- 资源：89,795 LUT、193,533 FF、784 DSP、25.5 BRAM；vectorless power 5.733 W（Low confidence）。
- route 完成、failed nets=0、DRC Error=0，但 setup WNS=-0.303 ns（TNS=-20.580 ns），因此 4 ns/250 MHz 约束未通过。
- 全模型 trace 周期为 565,587,640 cycles，PE 时间利用率 1.794%，GEMM 利用率 61.13%，有效吞吐 13.78 GOPS@250 MHz。周期结果来自 Python 模型，不能当作板上运行速度。
- XSim 宽接口 smoke 通过；尚未完成板级 I/O/DDR、bitstream、真实整模型 FPGA 回放和新的 LIBERO 成功率。

## 如何读这些数字

WNS 是目标周期减去最坏路径延迟，正数表示目标时钟还有余量。推导 Fmax 用 `1000/(目标周期-WNS)` 计算，所以它比请求频率略高。它不是另一次综合，也不是芯片在所有条件下的保证频率。

历史 trace 模型的双缓冲结果（591.0 GOPS @250 MHz）仍是条件估算。它说明读、算、写重叠的方向，不能替代本次 Vivado 实现或真实 TurboVLA 端到端延迟。
