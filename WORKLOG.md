# TurboVLA 交接包工作记录

## 2026-09-15 19:39:43 — 建立交接包

把 TurboVLA 的 W8A8 Pack2 主线、W8A16 参考线、profiling、量化筛选、整数恢复、论文模板和 GEMM 利用率辅助资料复制到本目录。旧目录保持不动。模型权重、原始大张量、Vivado checkpoint 和服务器私有路径不进入仓库。

## 2026-09-15 19:44:48 — 包内复现检查

运行 `scripts/run_pack2_checks.ps1 -What all`。Pack2 黄金模型随机/极值共 100,343 组全部通过，K=1/32/256/3072/4096 的边界表也生成完成；RTL 冒烟的 `pack2_mult_padd`、`timing_array` 和 `timing_replay` 全部通过。`system_top_elab.vvp` 等临时仿真文件被 `.gitignore` 排除。

## 2026-09-15 19:46:29 — 推送 GitHub

创建私有仓库 `nc-thu/turbovla-fpga-handoff`，主分支为 `main`。初始提交为 `d31c8cde4c0b760f4113d93a4dcb45ad824080d1`。仓库只包含源码、脚本、报告和机器可读结果，不包含模型权重。
