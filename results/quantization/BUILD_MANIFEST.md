# TurboVLA 量化筛选构建清单

- 生成时间：2026-09-12T22:51:38+08:00
- 实验目录：`E:\GPU ARCH\vector_core_sim\algo\turbovla_quant\2026-09-12_215112`
- 服务器：`nc23@101.6.64.77`，GPU 3 单进程共享
- 源码 commit：`b29ab1420baa5c663ec935df513f2012430beb67`
- checkpoint SHA256：`d031ad7be05a2f5d04afb3194ed26b0cb46083685edee7a5e145078a37d26bab`
- 筛选规模：4 suites × task 0/1 × 3 episodes × 4 modes = 96 episodes
- 汇总：`results/summary.json`
- 任务成功率 CSV：`results/task_rates.csv`
- suite 运行时 CSV：`results/suite_runtime.csv`
- HTML：`2026-09-12_225138_TurboVLA_quant_libero_screening.html`
- 原始结果：`remote_artifacts/screen_*.json`、`remote_artifacts/spot_*.json`
- 原始日志：`remote_artifacts/logs/screen_*.log`、`remote_artifacts/logs/spot_*.log`
- 量化边界：软件 fake quant；逻辑 INT8 存储统计不等于真实压缩显存或 INT8 kernel 延迟。
- 官方完整 benchmark 未做：本轮仅 task 0/1，每 task 3 回合，用于快速筛选。
