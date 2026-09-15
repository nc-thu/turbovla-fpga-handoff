# 工作记录

## 2026-09-15 13:47:42 — 生成芯片架构说明报告

读取 TurboVLA W8A8 Pack2 的编译器、描述符、周期汇总、Pack2 RTL 和 Vivado OOC 报告，生成单文件 HTML。没有修改旧代码和历史报告。

- 432 个 descriptor、433 条 command（含 END）。
- current：86,410,126 cycles；双缓冲：41,949,544 cycles。
- 16×48 OOC：78249 LUT、148168 FF、768 DSP、0 BRAM。
