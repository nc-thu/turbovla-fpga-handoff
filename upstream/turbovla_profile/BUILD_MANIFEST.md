# TurboVLA V100 部署与 profiling 清单

生成时间：2026-09-12 20:05:36（报告文件名中的时间戳为最终生成时刻）

## 目录与来源

- 服务器实验目录：`/home/nc23/experiments/turbovla_profile/2026-09-12_192541/`
- 本地实验目录：`E:\GPU ARCH\vector_core_sim\algo\turbovla_profile\2026-09-12_192541\`
- 官方 TurboVLA 源码 commit：`b29ab1420baa5c663ec935df513f2012430beb67`
- 发布 checkpoint：`H-EmbodVis/TurboVLA/checkpoints/libero/turbovla_libero.pth`
- checkpoint SHA-256：`d031ad7be05a2f5d04afb3194ed26b0cb46083685edee7a5e145078a37d26bab`
- checkpoint 顶层字段：`model_state_dict`、`model_config`；没有 `ema_model_state_dict`

## 运行环境

- GPU：Tesla V100-SXM2-32GB，GPU 3，CUDA 12.4，驱动 550.54.15
- Python 3.10.21，PyTorch 2.6.0+cu124，Transformers 4.57.6
- LIBERO：`/home/nc23/workspace/LIBERO`
- 渲染：`MUJOCO_GL=egl`，`PYOPENGL_PLATFORM=egl`
- 运行策略：GPU 3 单进程；没有停止其他进程，也没有切换 GPU

## 运行命令

```bash
python scripts/model_load_smoke.py ... --precision fp32
python scripts/model_load_smoke.py ... --precision bf16
python scripts/runtime_profile.py ... --precision fp32 --warmup 5 --repeat 10
python scripts/runtime_profile.py ... --precision bf16 --warmup 5 --repeat 10
python scripts/run_eval_patched.py ... --task_suite_name libero_spatial --task_ids 0 --num_trials_per_task 5 --precision bf16
python scripts/run_eval_patched.py ... --task_suite_name libero_object --task_ids 0 --num_trials_per_task 5 --precision bf16
```

完整的四 suite BF16/FP32 5 回合命令保存在 `scripts/run_suite_5ep.sh` 和
`scripts/run_suite_5ep_fp32.sh`。这些命令中的 `...` 是清单中记录的绝对路径，
没有改变模型、LIBERO 或公共接口。

## 重要实验边界

1. DINOv3 HF 仓库在服务器上是 gated。checkpoint 已经包含 DINOv3 ViT-B/16 的 211 个张量；实验从 checkpoint 抽出这些权重，并用 Transformers 的同结构 `DINOv3ViTModel` 保存为本地模型。预处理使用 DINOv3 官方 LVD-1689M 的 ImageNet mean/std，输入保持 256×256。
2. `scripts/run_eval_patched.py` 只在进程内兼容 `model_state_dict`；任务循环、LIBERO 环境、归一化统计和动作转换仍来自官方评测入口。
3. 20 回合是每套 task 0 的初始状态 0–4 spot check，不是官方完整的 50 trials/task benchmark。
4. 本轮没有做 W8A16、FPGA 周期映射或成功率正式复现。
