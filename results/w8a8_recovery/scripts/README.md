# TurboVLA 全矩阵乘 W8A8 实验

记录时间：2026-09-14 11:46:00。评测正在运行，最终数字以生成后的 HTML 和 `validation.json` 为准。

## 这轮改变了什么

进入 Linear、Conv、QK 和 AV 的两个乘法操作数均使用 INT8 数值网格。分组方案沿 K 维切分，每组独立量化，再按各组 scale 合并部分和。GPU 使用 FP32 核计算整数值，不是 INT8 CUDA 性能测试。

Embedding 查表、归一化、非线性、bias 和残差保留浮点。主成功率版本的跨组尺度合并也保留浮点。`fixed` 是独立的后处理检查，不沿用主版本的成功率。

## 数据不能混用

- 开发：四套 suite、task 0/1、初始状态 0～2。24 条 FP32 轨迹均匀抽取 144 次规划输入。
- 留出：四套 suite、task 0/1、初始状态 3～22，共 160 对回合。候选已于 2026-09-14 11:34:34 固定为 `group_32`。
- 12×7 是完整预测动作；MAE 在归一化动作空间计算，不是弧度或米。
- 成功由 LIBERO 环境判断。失败不换种子，不重试刷成绩。

## 文件位置

- `episodes/`：逐回合动作、成功判定、实际初始状态散列和耗时。
- `observations/`：开发用真实规划输入，仅用于开发与回放。
- `replay/`：逐输入误差和全部矩阵乘覆盖记录。
- `integer_fixtures/`、`integer_audit.json`：实际输入切片与 INT64 核对。
- `hardware_cost.csv`：逻辑访问、scale、部分和及条件周期；不是实测 FPGA 性能。
- `provenance.json`：代码、模型、输入及标定文件散列。
- `stage_events.jsonl`：每个实验单元的开始、结束和耗时。
- `frozen_candidate.json`：留出测试之前确定的候选。
- `validation.json`：数据划分、覆盖和配对核对。

## 服务器复现

服务器：`nc23@101.6.64.77`。脚本依赖已有 LIBERO 与官方 TurboVLA 源码，具体路径见 `scripts/run_recovery.py` 和构建清单。不要把这套脚本当成可直接在 Windows 上启动的模型环境。

```bash
PY=/home/nc23/experiments/sureflow_profile/2026-09-12_142640/venv/bin/python
ROUND=/home/nc23/experiments/turbovla_w8a8_recovery_2026-09-14_104416

# 只重新生成统计，不运行机器人，不改变评测结果。
$PY "$ROUND/scripts/hardware_cost.py" --root "$ROUND"
$PY "$ROUND/scripts/validate.py" --root "$ROUND" --complete
$PY "$ROUND/scripts/report.py" --root "$ROUND"
```

完整重跑请创建新的秒级目录，把 `scripts/` 复制到新目录，并先检查空闲 GPU。依次执行：

```bash
# NEW_ROUND 指向新目录；不要使用旧结果目录。
NEW_ROUND=/home/nc23/experiments/turbovla_w8a8_recovery_$(date +%Y-%m-%d_%H%M%S)
mkdir -p "$NEW_ROUND/scripts" "$NEW_ROUND/logs"
cp "$ROUND/scripts/"*.py "$NEW_ROUND/scripts/"
CUDA_VISIBLE_DEVICES=1 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  $PY "$NEW_ROUND/scripts/run_recovery.py" --root "$NEW_ROUND" --mode fp32 --capture
CUDA_VISIBLE_DEVICES=1 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  $PY "$NEW_ROUND/scripts/pipeline.py" --root "$NEW_ROUND"
CUDA_VISIBLE_DEVICES=1 MUJOCO_GL=egl PYOPENGL_PLATFORM=egl OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=1 \
  $PY "$NEW_ROUND/scripts/postflight.py" --root "$NEW_ROUND"
```

上面的 GPU 1 是本轮启动时选中的空闲设备；重跑前重新检查，不停止他人服务。`pipeline.py` 是初始实验入口，完整完成后的目录不能拿来再次执行它；它要求最初只有 24 个严格 FP32 开发回合。
