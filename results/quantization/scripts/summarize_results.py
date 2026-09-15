#!/usr/bin/env python3
"""Build a machine-readable summary and a small, self-contained HTML report."""

from __future__ import annotations

import hashlib
import html
import json
import csv
import statistics
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "remote_artifacts"
RESULT_DIR = ROOT / "results"
RESULT_DIR.mkdir(exist_ok=True)

MODE_ORDER = ["fp32", "w8a8", "w8a16", "w8afp16"]
MODE_LABEL = {
    "fp32": "FP32",
    "w8a8": "W8A8",
    "w8a16": "W8A16",
    "w8afp16": "W8A(FP16)",
}
SUITE_ORDER = ["libero_spatial", "libero_object", "libero_goal", "libero_10"]
SUITE_LABEL = {
    "libero_spatial": "Spatial",
    "libero_object": "Object",
    "libero_goal": "Goal",
    "libero_10": "LIBERO-10",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def pct(num: int, den: int) -> float:
    return 100.0 * num / den if den else 0.0


records = []
for path in sorted(ART.glob("screen_*.json")):
    data = json.loads(path.read_text(encoding="utf-8"))
    mode = data.get("quantization_mode", "fp32")
    suite = data["task_suite_name"]
    timing = data.get("policy_call_timing_ms", {})
    records.append(
        {
            "file": path.name,
            "sha256": sha256_file(path),
            "mode": mode,
            "suite": suite,
            "requested_task_ids": data.get("requested_task_ids", []),
            "num_trials_per_task": data.get("num_trials_per_task"),
            "tasks": data.get("tasks", []),
            "total_episodes": data.get("total_episodes", 0),
            "total_successes": data.get("total_successes", 0),
            "overall_success_rate": data.get("overall_success_rate", 0.0),
            "elapsed_seconds": data.get("experiment_elapsed_seconds"),
            "policy_timing_ms": {
                "count": timing.get("count"),
                "median": timing.get("median"),
                "p90": timing.get("p90"),
                "min": timing.get("min"),
                "max": timing.get("max"),
            },
            "quantization": data.get("quantization", {}),
            "experiment_started": data.get("experiment_started"),
            "experiment_finished": data.get("experiment_finished"),
        }
    )

by_mode = {mode: [r for r in records if r["mode"] == mode] for mode in MODE_ORDER}
aggregate = {}
for mode, rows in by_mode.items():
    successes = sum(r["total_successes"] for r in rows)
    episodes = sum(r["total_episodes"] for r in rows)
    medians = [r["policy_timing_ms"]["median"] for r in rows if r["policy_timing_ms"]["median"] is not None]
    p90s = [r["policy_timing_ms"]["p90"] for r in rows if r["policy_timing_ms"]["p90"] is not None]
    aggregate[mode] = {
        "successes": successes,
        "episodes": episodes,
        "success_rate_percent": pct(successes, episodes),
        "suite_median_of_medians_ms": statistics.median(medians) if medians else None,
        "suite_median_of_p90_ms": statistics.median(p90s) if p90s else None,
        "sum_process_elapsed_seconds": sum(r["elapsed_seconds"] or 0 for r in rows),
    }

spot = None
spot_path = ART / "quant_smoke.json"
if spot_path.exists():
    raw_spot = json.loads(spot_path.read_text(encoding="utf-8"))
    spot = {
        "file": spot_path.name,
        "sha256": sha256_file(spot_path),
        "status": raw_spot.get("status"),
        "suite": raw_spot.get("suite"),
        "task_id": raw_spot.get("task_id"),
        "seed": raw_spot.get("seed"),
        "modes": {},
    }
    for mode, row in raw_spot.get("modes", {}).items():
        spot["modes"][mode] = {
            "status": row.get("status"),
            "elapsed_s": row.get("elapsed_s"),
            "output_dtype": row.get("output_dtype"),
            "max_abs_vs_fp32": row.get("max_abs_vs_fp32", 0.0),
            "mean_abs_vs_fp32": row.get("mean_abs_vs_fp32", 0.0),
            "quantization": row.get("quantization", {}),
        }

checks = {
    "screening_files": len(records),
    "expected_screening_files": 16,
    "all_screening_files_present": len(records) == 16,
    "each_file_has_tasks_0_1": all(sorted(r["requested_task_ids"]) == [0, 1] for r in records),
    "each_task_has_three_episodes": all(
        all(t.get("episodes") == 3 for t in r["tasks"]) for r in records
    ),
    "quant_smoke_passed": bool(spot and spot.get("status") == "passed"),
    "screening_processes_completed": all(r["elapsed_seconds"] is not None for r in records),
}

generated = datetime.now().astimezone().replace(microsecond=0).isoformat()
summary = {
    "generated_at": generated,
    "experiment_directory": str(ROOT),
    "server": "nc23@101.6.64.77",
    "gpu_policy": "CUDA_VISIBLE_DEVICES=3; one process at a time; existing services were not stopped",
    "source_commit": "b29ab1420baa5c663ec935df513f2012430beb67",
    "checkpoint": {
        "path": "/home/nc23/experiments/turbovla_profile/2026-09-12_192541/pretrained/TurboVLA/checkpoints/libero/turbovla_libero.pth",
        "sha256": "d031ad7be05a2f5d04afb3194ed26b0cb46083685edee7a5e145078a37d26bab",
    },
    "environment": {"python": "3.10.20", "torch": "2.6.0+cu124", "gpu": "Tesla V100-SXM2-32GB"},
    "screening": {
        "suites": SUITE_ORDER,
        "task_ids": [0, 1],
        "episodes_per_task": 3,
        "seed": 7,
        "num_open_loop_steps": 12,
        "chunk_size": 12,
        "total_episodes_per_mode": 24,
        "total_episodes_all_modes": 96,
        "note": "This is a screening sample, not the official 50-episode-per-task benchmark.",
    },
    "quantization_definitions": {
        "fp32": "Released FP32 policy path; official DINO autocast setting retained.",
        "w8a8": "Per-output-channel symmetric INT8 weight fake quant + dynamic per-tensor INT8 activation fake quant; FP32 bias/norm.",
        "w8a16": "Per-output-channel symmetric INT8 weight fake quant + dynamic per-tensor INT16 activation fake quant; FP32 bias/norm.",
        "w8afp16": "Logical INT8 weight fake quant with FP16 model/activation execution; no INT8 CUDA kernel.",
        "common_boundary": "Software reference fake quantization. Dequantized weights are used for GPU execution; logical INT8 bytes are accounting only and are not FPGA latency evidence.",
    },
    "records": records,
    "aggregate": aggregate,
    "spot": spot,
    "checks": checks,
}

summary_path = RESULT_DIR / "summary.json"
summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

with (RESULT_DIR / "task_rates.csv").open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["mode", "suite", "task_id", "successes", "episodes", "success_rate"])
    for r in records:
        for task in r["tasks"]:
            writer.writerow([
                r["mode"], r["suite"], task.get("task_id"), task.get("successes"),
                task.get("episodes"), task.get("success_rate"),
            ])

with (RESULT_DIR / "suite_runtime.csv").open("w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["mode", "suite", "policy_calls", "median_ms", "p90_ms", "process_elapsed_s"])
    for r in records:
        t = r["policy_timing_ms"]
        writer.writerow([
            r["mode"], r["suite"], t.get("count"), t.get("median"), t.get("p90"),
            r.get("elapsed_seconds"),
        ])


def fmt_rate(row: dict) -> str:
    return f"{row['total_successes']}/{row['total_episodes']} ({row['overall_success_rate'] * 100:.1f}%)"


def fmt_num(value, digits=1):
    return "—" if value is None else f"{value:.{digits}f}"


def rec(mode: str, suite: str):
    return next((r for r in records if r["mode"] == mode and r["suite"] == suite), None)


def task_rows_html(mode: str) -> str:
    out = []
    for suite in SUITE_ORDER:
        row = rec(mode, suite)
        if not row:
            continue
        for task in row["tasks"]:
            out.append(
                f"<tr><td>{html.escape(MODE_LABEL[mode])}</td><td>{html.escape(SUITE_LABEL[suite])}</td>"
                f"<td>{task.get('task_id')}</td><td>{task.get('successes')}/{task.get('episodes')} "
                f"({task.get('success_rate', 0) * 100:.1f}%)</td><td>{html.escape(task.get('task_description', ''))}</td></tr>"
            )
    return "\n".join(out)


rate_colors = {"fp32": "#333333", "w8a8": "#b44d4d", "w8a16": "#3f6f9f", "w8afp16": "#8b6a32"}
bar_svg = []
bar_w, left, top, row_h = 112, 110, 28, 34
height = top + len(SUITE_ORDER) * len(MODE_ORDER) * row_h + 24
for i, suite in enumerate(SUITE_ORDER):
    y0 = top + i * len(MODE_ORDER) * row_h
    bar_svg.append(f'<text x="8" y="{y0 + 17}" class="axis">{html.escape(SUITE_LABEL[suite])}</text>')
    for j, mode in enumerate(MODE_ORDER):
        row = rec(mode, suite)
        rate = (row["overall_success_rate"] * 100) if row else 0
        y = y0 + j * row_h
        bar_svg.append(f'<text x="{left - 8}" y="{y + 15}" text-anchor="end" class="small">{html.escape(MODE_LABEL[mode])}</text>')
        bar_svg.append(f'<rect x="{left}" y="{y + 4}" width="{bar_w}" height="18" fill="#eeeeee" stroke="#bbbbbb"/>')
        bar_svg.append(f'<rect x="{left}" y="{y + 4}" width="{bar_w * rate / 100:.1f}" height="18" fill="{rate_colors[mode]}"/>')
        bar_svg.append(f'<text x="{left + bar_w + 7}" y="{y + 17}" class="small">{rate:.1f}%</text>')

spot_rows = []
if spot:
    for mode in MODE_ORDER:
        s = spot["modes"].get(mode, {})
        spot_rows.append(
            f"<tr><td>{html.escape(MODE_LABEL[mode])}</td><td>{s.get('output_dtype', '—')}</td>"
            f"<td>{fmt_num(s.get('max_abs_vs_fp32'), 5)}</td><td>{fmt_num(s.get('mean_abs_vs_fp32'), 5)}</td>"
            f"<td>{fmt_num(s.get('elapsed_s'), 2)}</td></tr>"
        )

suite_rows = []
for suite in SUITE_ORDER:
    cells = []
    for mode in MODE_ORDER:
        row = rec(mode, suite)
        cells.append(f"<td>{fmt_rate(row) if row else '—'}</td>")
    suite_rows.append(f"<tr><td>{html.escape(SUITE_LABEL[suite])}</td>{''.join(cells)}</tr>")

runtime_rows = []
for suite in SUITE_ORDER:
    cells = []
    for mode in MODE_ORDER:
        row = rec(mode, suite)
        if row:
            t = row["policy_timing_ms"]
            cells.append(f"<td>{fmt_num(t.get('median'), 1)} / {fmt_num(t.get('p90'), 1)}<br><span class='muted'>{fmt_num(row.get('elapsed_seconds'), 1)} s process</span></td>")
        else:
            cells.append("<td>—</td>")
    runtime_rows.append(f"<tr><td>{html.escape(SUITE_LABEL[suite])}</td>{''.join(cells)}</tr>")

fp = aggregate["fp32"]


def conclusion_line(mode: str) -> str:
    a = aggregate[mode]
    delta_pp = a["success_rate_percent"] - fp["success_rate_percent"]
    speedup = fp["suite_median_of_medians_ms"] / a["suite_median_of_medians_ms"]
    return f"{MODE_LABEL[mode]}：{a['successes']}/{a['episodes']}（{a['success_rate_percent']:.1f}%），相对 FP32 {delta_pp:+.1f} 个百分点；四个 suite 的 policy 调用中位数的中位数为 {a['suite_median_of_medians_ms']:.1f} ms（相对 FP32 {speedup:.2f}×）。"


html_text = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TurboVLA 量化 LIBERO 快速筛选</title>
<style>
body{{font-family:Arial,"Microsoft YaHei",sans-serif;color:#222;max-width:1180px;margin:28px auto;padding:0 22px;line-height:1.55}}
h1{{font-size:25px;margin-bottom:4px}} h2{{font-size:18px;border-bottom:1px solid #bbb;padding-bottom:4px;margin-top:28px}}
.meta,.muted{{color:#666;font-size:13px}} table{{border-collapse:collapse;width:100%;font-size:13px;margin:10px 0 18px}}
th,td{{border:1px solid #bbb;padding:6px 8px;text-align:left;vertical-align:top}} th{{background:#f1f1f1}}
.note{{border-left:4px solid #555;padding:8px 12px;background:#f6f6f6;margin:12px 0}}
svg{{width:100%;max-width:620px;height:auto;border:1px solid #bbb;background:#fff}} .axis{{font-size:12px;font-weight:bold}} .small{{font-size:11px}}
code{{font-size:12px;background:#f2f2f2;padding:1px 3px}} ul{{margin-top:6px}}
</style></head><body>
<h1>TurboVLA W8A8 / W8A16 / W8A(FP16) LIBERO 快速筛选</h1>
<div class="meta">生成时间：{html.escape(generated)}　|　服务器：nc23@101.6.64.77　|　GPU：V100-SXM2-32GB（CUDA_VISIBLE_DEVICES=3，单进程）</div>
<div class="note"><b>这轮结果的边界：</b>四个 suite、task 0/1、每 task 3 回合，共 24 回合/模式、96 回合总计。这是筛选样本，不是官方每 task 50 回合的论文 benchmark。量化是软件 fake-quant 参考执行：逻辑上统计 INT8 权重，但 GPU 仍使用反量化权重，不能把本页运行时间当作 FPGA 或 INT8 CUDA kernel 延迟。</div>
<h2>先看结论</h2>
<ul>
<li>{conclusion_line('w8a8')} 这是明显的精度风险：Spatial 为 1/6、Goal 为 0/6，不进入后续候选。</li>
<li>{conclusion_line('w8a16')} 成功率总数与 FP32 相同，但 policy 调用比 FP32 慢；它更像数值保守基线，不是当前速度方案。</li>
<li>{conclusion_line('w8afp16')} 速度最快，但总成功率比 FP32 低 4.2 个百分点（21/24 对 22/24）。这个差异来自小样本筛选，不能直接宣称模型质量下降，也不能据此换算正式成功率。</li>
<li>GPU 3 同时有其他服务，计时受共享负载影响。要做论文 runtime 或确定性比较，应在空闲卡上重复预热和多次同步计时。</li>
</ul>
<h2>为什么 W8A16 比 W8A(FP16) 慢</h2>
<p>这两个名字都含有“16”，但执行路径不是一回事。当前 W8A16 把每层输入做动态 INT16 假量化（计算 absmax、round、clamp，再反量化），随后仍以 FP32 权重和 FP32 <code>F.linear</code> 完成矩阵乘。它没有调用 INT16 CUDA GEMM。W8A(FP16) 则把模型和输入转为 FP16，直接使用 FP16 矩阵乘；V100 的 Tensor Core 可以加速这一条路径。因此 W8A16 的软件时间不能代表未来 INT8×INT16 PE 的硬件吞吐。</p>
<p>换句话说，W8A16 是数值保守基线（成功率与 FP32 持平），W8A(FP16) 是软件速度候选（约 1.61× 相对 FP32），二者不能只按“位宽更小”比较快慢。若要比较 W8A16 的硬件速度，需要真正的 INT8×INT16 kernel 或 FPGA 周期模型。</p>
<h2>每个 suite 的 task 0/1 成功率</h2>
<table><thead><tr><th>Suite</th><th>FP32</th><th>W8A8</th><th>W8A16</th><th>W8A(FP16)</th></tr></thead><tbody>{''.join(suite_rows)}</tbody></table>
<p class="muted">每个单元格是 successes/episodes；一个回合占 16.7 个百分点。任务描述和逐 task 记录见下表及 <code>results/summary.json</code>。</p>
<h2>成功率图</h2>
<svg viewBox="0 0 360 {height}" role="img" aria-label="每个 suite 的成功率"><style>.axis{{font:700 12px Arial}}.small{{font:11px Arial}}</style>{''.join(bar_svg)}</svg>
<h2>逐 task 记录</h2>
<table><thead><tr><th>模式</th><th>Suite</th><th>Task</th><th>成功率</th><th>任务描述</th></tr></thead><tbody>{task_rows_html('fp32')}{task_rows_html('w8a8')}{task_rows_html('w8a16')}{task_rows_html('w8afp16')}</tbody></table>
<h2>policy 调用和进程耗时</h2>
<table><thead><tr><th>Suite</th><th>FP32<br>median / P90 (ms)</th><th>W8A8<br>median / P90 (ms)</th><th>W8A16<br>median / P90 (ms)</th><th>W8A(FP16)<br>median / P90 (ms)</th></tr></thead><tbody>{''.join(runtime_rows)}</tbody></table>
<p class="muted">表中第一行是每个 suite 内 policy 调用的 median/P90；下一行是该 JSON 进程从加载到结束的时间。加载和环境初始化不要与单次 policy 延迟混为一谈。</p>
<h2>单观测数值自检</h2>
<table><thead><tr><th>模式</th><th>输出 dtype</th><th>相对 FP32 最大绝对差</th><th>相对 FP32 平均绝对差</th><th>加载+一次观测耗时 (s)</th></tr></thead><tbody>{''.join(spot_rows)}</tbody></table>
<p class="muted">Spatial task 0、seed 7、初始状态 0、256×256 RGB 观测。W8A8 的单观测误差较大，与其回合成功率下降方向一致；W8A16 和 W8A(FP16) 的单观测误差较小。</p>
<h2>量化口径和可追溯信息</h2>
<table><tr><th>项目</th><th>记录</th></tr>
<tr><td>FP32</td><td>官方 FP32 policy 路径；DINO 的 released autocast 设置保留。</td></tr>
<tr><td>W8A8</td><td>权重 per-output-channel 对称 INT8 fake quant；激活动态 per-tensor INT8；bias/norm FP32。</td></tr>
<tr><td>W8A16</td><td>权重 per-output-channel 对称 INT8 fake quant；激活动态 per-tensor INT16；bias/norm FP32。</td></tr>
<tr><td>W8A(FP16)</td><td>逻辑 INT8 权重 fake quant，模型和激活以 FP16 参考执行；不是 INT8 CUDA kernel。</td></tr>
<tr><td>源代码 commit</td><td><code>b29ab1420baa5c663ec935df513f2012430beb67</code></td></tr>
<tr><td>checkpoint SHA256</td><td><code>d031ad7be05a2f5d04afb3194ed26b0cb46083685edee7a5e145078a37d26bab</code></td></tr>
</table>
<h2>复现</h2>
<p>服务器脚本：<code>/home/nc23/experiments/turbovla_quant_2026-09-12_215112/scripts/run_screening_all.sh</code>。本地原始 JSON、日志和脚本位于本目录；汇总文件为 <code>results/summary.json</code>。关闭复用、未改任务、未改 seed；没有进行成功后重试。</p>
<p class="meta">生成脚本：<code>scripts/summarize_results.py</code>。本页数字从 JSON 自动读取；HTML 不手抄评测结果。</p>
</body></html>"""

report_path = RESULT_DIR / f"{datetime.now().strftime('%Y-%m-%d_%H%M%S')}_TurboVLA_quant_libero_screening.html"
report_path.write_text(html_text, encoding="utf-8")

manifest = f"""# TurboVLA 量化筛选构建清单

- 生成时间：{generated}
- 实验目录：`{ROOT}`
- 服务器：`nc23@101.6.64.77`，GPU 3 单进程共享
- 源码 commit：`b29ab1420baa5c663ec935df513f2012430beb67`
- checkpoint SHA256：`d031ad7be05a2f5d04afb3194ed26b0cb46083685edee7a5e145078a37d26bab`
- 筛选规模：4 suites × task 0/1 × 3 episodes × 4 modes = 96 episodes
- 汇总：`results/summary.json`
- 任务成功率 CSV：`results/task_rates.csv`
- suite 运行时 CSV：`results/suite_runtime.csv`
- HTML：`{report_path.name}`
- 原始结果：`remote_artifacts/screen_*.json`、`remote_artifacts/spot_*.json`
- 原始日志：`remote_artifacts/logs/screen_*.log`、`remote_artifacts/logs/spot_*.log`
- 量化边界：软件 fake quant；逻辑 INT8 存储统计不等于真实压缩显存或 INT8 kernel 延迟。
- 官方完整 benchmark 未做：本轮仅 task 0/1，每 task 3 回合，用于快速筛选。
"""
(ROOT / "BUILD_MANIFEST.md").write_text(manifest, encoding="utf-8")
print(report_path)
print(summary_path)
