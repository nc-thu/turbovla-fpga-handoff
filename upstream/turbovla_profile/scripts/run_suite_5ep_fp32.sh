#!/usr/bin/env bash
set -u
ROOT=/home/nc23/experiments/turbovla_profile/2026-09-12_192541
source /home/nc23/experiments/sureflow_profile/2026-09-12_142640/venv/bin/activate
export PYTHONPATH="$ROOT/source:$ROOT/source/third_party/vla_adapter"
export CUDA_VISIBLE_DEVICES=3
export MUJOCO_GL=egl
export PYOPENGL_PLATFORM=egl
for suite in libero_spatial libero_object libero_goal libero_10; do
  echo "[suite-5ep-fp32] $suite start $(date -Is)"
  python "$ROOT/scripts/run_eval_patched.py" \
    --libero_root /home/nc23/workspace/LIBERO \
    --ckpt_path "$ROOT/pretrained/TurboVLA/checkpoints/libero/turbovla_libero.pth" \
    --dinov3_path "$ROOT/pretrained/assets/dinov3_local" \
    --bert_path "$ROOT/pretrained/assets/bert_local" \
    --stats_path "$ROOT/source/experiments/libero/configs/libero_all4_stats.json" \
    --stats_key libero_all4_no_noops \
    --task_suite_name "$suite" \
    --task_ids 0 --num_trials_per_task 5 \
    --num_open_loop_steps 12 --chunk_size 12 --seed 7 --precision fp32 \
    --result_json_path "$ROOT/eval_${suite}_fp32_5ep.json" \
    --log_path "$ROOT/eval_${suite}_fp32_5ep.log"
  rc=$?
  echo "[suite-5ep-fp32] $suite end $(date -Is) rc=$rc"
done
