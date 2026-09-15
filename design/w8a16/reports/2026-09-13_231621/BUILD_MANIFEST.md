# 真实 TurboVLA 指令流活动回放交付清单

生成时刻：2026-09-14 00:59:00。

| 交付物 | 路径 | 状态 |
|---|---|---|
| 中文报告 | `2026-09-13_231621_TurboVLA_activity_replay.html` | 已生成，数字由 JSON/CSV 读取 |
| 机器摘要 | `report_summary.json` | 已生成 |
| 真实采集 | `../data/v8_2026-09-13_231621/raw_capture/` | GPU3，Spatial task 0，seed 7 |
| 编译结果 | `../data/v8_2026-09-13_231621/compiled/` | 432 descriptors，433 instructions |
| RTL 对拍 | `../data/v8_2026-09-13_231621/rtl_logs/` | full replay 与代表 tile PASS |
| Vivado | `../hw/v8_2026-09-13_2316_integrated_replay_top/synth/runs/2026-09-14_0039/` | 3 组 OOC synth PASS |

关键口径：768 DSP、250 MHz、单 MAC/DSP 的物理峰值为 384 GOPS；本次完整 forward 周期模型为 155,780,495 cycles，PE 时间利用率 41.445%，有效吞吐 159.148 GOPS。full replay 是虚拟事件周期，代表 tile 才是逐拍 RTL 算术验证；vectorless power 没有 SAIF/VCD，不能写成 TOPS/W。
