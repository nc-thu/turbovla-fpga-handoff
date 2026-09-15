# v6：DSP 输入／输出 pipeline 与 250 MHz 实现

生成时间：2026-09-13 19:33:56（Vivado 结束时间）

这一轮从 v5 独立复制，目标是给 W8A16 乘法阵列补 DSP 输入寄存器，并把动作路径的乘积和 INT40 累加反馈拆开。没有修改旧版本目录。

## 改动

- rtl/w8a16_mult.sv：DSP A/B 输入使用 AREG=1/BREG=1，乘法和输出保留 MREG=1/PREG=1。
- rtl/w8a16_pe.sv：保留乘积寄存器和 valid 对齐，保证输入 pipeline 不改变 PE 接口协议。
- rtl/w8a16_action_path.sv：增加 MAC 操作数／乘积寄存器，末尾累加 drain 分为两拍。

## 验证结果

- 服务器 Verilator：11 个测试全部通过，耗时 153 s；完整 16×48 阵列为 768 DSP。
- Icarus/UNISIM：服务器日志记录 xvlog 不存在，本轮未完成该冒烟。
- Vivado 2021.2：xczu7ev-ffvc1156-2-e，4.000 ns（250 MHz）目标；综合、布局、布线和 post-route phys-opt 均完成。

## 实现结果

- route：184,306 / 184,306 条可路由网络完成，unrouted=0，routing errors=0。
- post-route WNS：-0.050 ns，TNS -4.464 ns，192 个 setup 失败端点；按 1000/(4.000-0.050) 推算约 246.9 MHz，因此 250 MHz 仍未通过。
- 资源：66,368 LUT、117,105 FF、785 DSP、0 BRAM。
- vectorless 功耗：4.478 W（动态 3.865 W、静态 0.613 W，Medium confidence）；没有 SAIF/VCD，不是板上实测。
- DRC：821 项（0 Error；DPIP-2 34、DPOP-3 1、DPOP-4 17、RTSTAT-10 1、AVAL-155 advisory 768）。v5 的 DPIP-2 为 1,571 项，v6 降到 34 项，减少约 97.8%；剩余主要在 runtime 的其他 DSP 路径。

机器汇总在 ../../data/v6_2026-09-13_193556_implementation/，HTML 在 ../../reports/2026-09-13_193800/。Vivado 原始报告和 DCP 在 impl/runs/2026-09-13_182745_system_250mhz/。

本轮是 OOC wrapper，没有板级 pin、AXI/DDR、时钟 buffer 和 I/O delay 约束；没有生成 bitstream，也没有做板上 TurboVLA 端到端运行。
