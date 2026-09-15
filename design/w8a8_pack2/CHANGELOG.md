# TurboVLA W8A8 Pack2 变更记录

## 2026-09-14 11:52:30

- 新建独立工作区 `turbovla_w8a8_pack2`，不改动 HB、TurboVLA W8A16 和历史目录。
- 复制 HB v10 Pack2 预加器、PE、阵列、GEMM、snapshot/readout 和 requant RTL 作为只读参考。
- 新增 TurboVLA W8A8 专用描述符与 64-bit command + 512-bit sideband 编译器。
- 对一个已有 TurboVLA forward trace 生成 current、double-buffer、queue、R5 conditional 四种周期模型。
- 新增 Pack2 黄金模型、Verilator/ Icarus smoke、16×48 参数化 Vivado OOC 综合壳。
- 本轮没有重跑 LIBERO 成功率，没有做 post-route、板级 DDR 或真实 TOPS/W 测量。

## 2026-09-15 16:18:22

- 新增 `hw/v2_2026-09-15_155202_timing_pipeline/` 时序版 RTL：DSP P 输出寄存、阵列输入寄存和输出寄存。
- 本地 Icarus 4/4 冒烟及 system_top 展开通过；新增两个单独的 Vivado 实现配置（250 MHz、303.215 MHz）。
- Vivado 实现尚未执行，原因是本机缺少 Vivado 且 C 集群 SSH 超时；本轮不写入新的实现数字。
- 生成时序和架构说明页 `reports/2026-09-15_161822/2026-09-15_161822_timing_pipeline_report.html`。

## 2026-09-15 19:17:06

- 修正 Vivado 定位：使用本机 `D:/software/Vivado/2021.2/bin/vivado.bat`，在独立 `hw/v3_2026-09-15_174639_vivado_impl/` 重跑两个频率点。
- 250 MHz 和 303.215 MHz 均完成综合、布局和布线，保留 768 DSP；新增报告使用真实 post-route 资源、时序、routing 和 vectorless power 结果。
- 新报告：`reports/2026-09-15_192300/2026-09-15_192200_TurboVLA时序实现与架构分析.html`。旧的未执行报告保持不变。

## 2026-09-15 19:25:12

- 修正最终 HTML 的时序字段与结论措辞，区分 setup slack、pulse-width slack 和 Vivado 中显示为 NA 的 hold 项。
- 最终 HTML：`reports/2026-09-15_192512/2026-09-15_192512_TurboVLA时序实现与架构分析.html`，机器可读结果：同目录 `vivado_real_results.json`。
