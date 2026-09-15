# TurboVLA W8A8 Pack2 时序版 RTL

版本开始时间：2026-09-15 15:52:02  
本轮报告：`../../reports/2026-09-15_163224/2026-09-15_163224_timing_pipeline_report.html`

这是一份独立的时序优化候选。它不修改 v1，也不改变 Pack2 的数据格式和阵列规模。改动集中在三个寄存器边界：

1. 阵列输入端捕获 CTX activation、WRAM weight、valid 和 pulse；
2. DSP48E2 的 P 输出先进入 `P_pipe_r`，再做高场借位校正；
3. 阵列读出端增加输出寄存器，隔离行选择 mux。

这样做的目的，是把 DSP 输出、校正和读出之间的长组合路径切短。代价是固定流水延迟增加，必须由时序和协议测试一起确认。

## 本地检查

```text
powershell -ExecutionPolicy Bypass -File sim/run_timing_smoke.ps1 \
  -OutDir data/functional
```

当前记录为 4/4 通过：Pack2 乘法器、2×3 timing array、回放顶层和 system_top 展开。

## Vivado 两个频率点

```bash
bash vivado/run_two_freqs.sh
python vivado/collect_vivado_results.py data/vivado_results.json
```

- 250 MHz：4.000 ns；
- 303.215 MHz：3.298 ns。

每个频率独立建工程和写报告。当前本机没有 Vivado，远端 SSH 也暂时不可达，所以 `data/vivado_results.json` 中的状态为 `not_run`，不代表时序失败或通过。
