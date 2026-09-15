# TurboVLA W8A16 v5 implementation 构建清单

生成时间：2026-09-13 17:40:37

## 本轮输入

| 内容 | 路径 | 说明 |
|---|---|---|
| v4 RTL 拷贝 | `rtl/` | 本轮只读使用，不修改 v4 |
| 系统 top | `synth/top_w8a16_system.sv` | `w8a16_system_top` |
| Vivado Tcl | `impl/impl_top.tcl` | non-project implementation 流程 |
| launcher | `run_impl.ps1` | 记录完整墙钟耗时 |
| 器件 | `xczu7ev-ffvc1156-2-e` | Vivado 2021.2 |
| 时钟约束 | `3.298 ns` | 303.214 MHz 目标 |

## 结果

| 项目 | 值 |
|---|---:|
| implementation 状态 | passed；route fully routed |
| 墙钟耗时 | 3274.176 s |
| post-route WNS | -0.461 ns |
| 按 WNS 推算 Fmax | 266.028 MHz |
| LUT / FF / DSP / BRAM | 66,255 / 118,169 / 785 / 0 |
| route 可路由网络 | 184,104 / 184,104 |
| vectorless 总片上功耗 | 5.678 W |
| 动态 / 静态 | 5.058 W / 0.620 W |
| DRC | 0 Error，4 Warning，1 Advisory |

## 原始结果

完整文件在 `impl/runs/2026-09-13_163609_system_impl/system_top/`，包括 timing、critical paths、utilization、power、route status、congestion、DRC、methodology、qor、最终 DCP 和 Vivado log。

功耗没有使用 SAIF/VCD，属于 vectorless 估算。OOC wrapper 没有板级 pin、AXI/DDR 和时钟 buffer 约束，因此本轮不能生成 bitstream，也不能代替板上功耗和系统时序测试。
