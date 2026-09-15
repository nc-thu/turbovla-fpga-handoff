# 2026-09-14 真实 TurboVLA trace 优化数据

生成时刻：2026-09-14 02:03:37。

本目录保存编译器 baseline/optimized、十项消融、RTL 回放日志、最终 Vivado OOC 报告和派生 CSV/JSON。源 trace 没有复制进来，仍在 `data/v8_2026-09-13_231621/raw_capture/`；两轮的文件散列写在 `trace_manifest.json`。

快速结果：baseline 为 155,780,495 cycles，优化条件模型为 75,254,992 cycles，周期下降 51.692%；valid MAC 保持 49,584,342,528，PE 时间利用率从 41.445% 提高到 85.792%，有效 GOPS 从 159.148 提高到 329.442。这里的优化数字来自周期模型和顶层 counter replay，不是板上时延。
