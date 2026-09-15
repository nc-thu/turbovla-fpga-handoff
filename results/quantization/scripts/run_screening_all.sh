#!/usr/bin/env bash
set -u

source /home/nc23/experiments/sureflow_profile/2026-09-12_142640/venv/bin/activate
export PYTHONPATH=/home/nc23/experiments/turbovla_profile/2026-09-12_192541/source:/home/nc23/experiments/turbovla_profile/2026-09-12_192541/source/third_party/vla_adapter
export CUDA_VISIBLE_DEVICES=3
export MUJOCO_GL=egl
export PYOPENGL_PLATFORM=egl

ROOT=/home/nc23/experiments/turbovla_quant_2026-09-12_215112
SCRIPT="$ROOT/scripts/run_eval_quant.py"
SOURCE=/home/nc23/experiments/turbovla_profile/2026-09-12_192541/source
LIBERO=/home/nc23/workspace/LIBERO
CKPT=/home/nc23/experiments/turbovla_profile/2026-09-12_192541/pretrained/TurboVLA/checkpoints/libero/turbovla_libero.pth
DINO=/home/nc23/experiments/turbovla_profile/2026-09-12_192541/pretrained/assets/dinov3_local
BERT=/home/nc23/experiments/turbovla_profile/2026-09-12_192541/pretrained/assets/bert_local
STATS=/home/nc23/experiments/turbovla_profile/2026-09-12_192541/source/experiments/libero/configs/libero_all4_stats.json

mkdir -p "$ROOT/results" "$ROOT/logs" "$ROOT/videos"

for mode in fp32 w8a8 w8a16 w8afp16; do
  for suite in libero_spatial libero_object libero_goal libero_10; do
    out="$ROOT/results/screen_${mode}_${suite}.json"
    log="$ROOT/logs/screen_${mode}_${suite}.log"
    echo "START mode=$mode suite=$suite $(date -Is)" | tee "$log"
    python -u "$SCRIPT" \
      --source "$SOURCE" \
      --libero-root "$LIBERO" \
      --checkpoint "$CKPT" \
      --dino "$DINO" \
      --bert "$BERT" \
      --stats "$STATS" \
      --mode "$mode" \
      --suite "$suite" \
      --task-ids 0,1 \
      --episodes 3 \
      --seed 7 \
      --num-open-loop-steps 12 \
      --chunk-size 12 \
      --output "$out" \
      --log "$log" \
      --video-root "$ROOT/videos" \
      >> "$log" 2>&1
    rc=$?
    echo "DONE mode=$mode suite=$suite rc=$rc $(date -Is)" | tee -a "$log"
  done
done
