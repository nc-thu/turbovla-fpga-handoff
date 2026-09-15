"""Generate a self-contained Chinese TurboVLA deployment/profile report."""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "remote_artifacts"


def read_json(name: str):
    return json.loads((ART / name).read_text(encoding="utf-8"))


def esc(value) -> str:
    return html.escape(str(value), quote=True)


def fmt_ms(v: float) -> str:
    return f"{v:.2f} ms"


def fmt_mib(v: int | float) -> str:
    return f"{float(v) / 1024 / 1024:.1f} MiB"


def link(rel: str, label: str | None = None) -> str:
    return f'<a href="{esc(rel)}">{esc(label or rel)}</a>'


def runtime_svg(fp: dict, bf: dict) -> str:
    vals = [fp["wall_ms_median"], bf["wall_ms_median"]]
    vmax = max(vals) * 1.35
    bars = []
    colors = ["#34495e", "#1f8a70"]
    names = ["FP32", "BF16"]
    for i, (name, val, color) in enumerate(zip(names, vals, colors)):
        x = 180 + i * 250
        h = 150 * val / vmax
        y = 205 - h
        bars.append(
            f'<rect x="{x}" y="{y:.1f}" width="120" height="{h:.1f}" fill="{color}"/>'
            f'<text x="{x+60}" y="{y-8:.1f}" text-anchor="middle">{val:.2f}</text>'
            f'<text x="{x+60}" y="230" text-anchor="middle">{name}</text>'
        )
    return (
        '<svg class="chart" viewBox="0 0 700 260" role="img" aria-label="V100稳定单次推理耗时">'
        '<line x1="100" y1="205" x2="620" y2="205" stroke="#333" stroke-width="1.5"/>'
        '<line x1="100" y1="45" x2="100" y2="205" stroke="#333" stroke-width="1.5"/>'
        '<text x="24" y="42">稳定单次推理耗时（ms）</text>'
        + "".join(bars)
        + '<text x="350" y="258" text-anchor="middle">精度配置（5 次预热，10 次同步测量）</text></svg>'
    )


def success_svg(records: list[dict]) -> str:
    suites = ["libero_spatial", "libero_object", "libero_goal", "libero_10"]
    lookup = {(r["precision"], r["suite"]): r for r in records}
    bars = []
    for i, suite in enumerate(suites):
        x0 = 85 + i * 150
        for j, precision in enumerate(["fp32", "bf16"]):
            r = lookup[(precision, suite)]
            val = 100 * r["success_rate"]
            h = 135 * val / 100
            x = x0 + j * 38
            y = 190 - h
            color = "#34495e" if precision == "fp32" else "#1f8a70"
            bars.append(
                f'<rect x="{x}" y="{y:.1f}" width="28" height="{h:.1f}" fill="{color}"/>'
                f'<text x="{x+14}" y="{y-5:.1f}" text-anchor="middle">{val:.0f}</text>'
            )
        label = suite.replace("libero_", "").upper()
        bars.append(f'<text x="{x0+33}" y="215" text-anchor="middle">{label}</text>')
    return (
        '<svg class="chart" viewBox="0 0 700 250" role="img" aria-label="LIBERO task 0 五回合成功率">'
        '<line x1="65" y1="190" x2="660" y2="190" stroke="#333" stroke-width="1.5"/>'
        '<line x1="65" y1="55" x2="65" y2="190" stroke="#333" stroke-width="1.5"/>'
        '<text x="9" y="52">成功率（%）</text><text x="65" y="205">0</text><text x="48" y="122">50</text><text x="48" y="57">100</text>'
        + "".join(bars)
        + '<rect x="535" y="35" width="13" height="13" fill="#34495e"/><text x="554" y="46">FP32</text>'
        + '<rect x="600" y="35" width="13" height="13" fill="#1f8a70"/><text x="619" y="46">BF16</text></svg>'
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--timestamp", default=dt.datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    args = ap.parse_args()
    ts_parts = args.timestamp.split("_")
    if len(ts_parts) == 2 and len(ts_parts[1]) == 6:
        display_timestamp = f"{ts_parts[0]} {ts_parts[1][0:2]}:{ts_parts[1][2:4]}:{ts_parts[1][4:6]}"
    else:
        display_timestamp = args.timestamp
    fp_rt = read_json("runtime_fp32.json")
    bf_rt = read_json("runtime_bf16.json")
    fp_smoke = read_json("model_smoke_fp32.json")
    bf_smoke = read_json("model_smoke_bf16.json")
    eval_records: list[dict] = []
    for precision in ["fp32", "bf16"]:
        for suite in ["libero_spatial", "libero_object", "libero_goal", "libero_10"]:
            name = f"eval_{suite}_{precision}_5ep.json"
            data = read_json(name)
            row = data["tasks"][0]
            eval_records.append(
                {
                    "precision": precision,
                    "suite": suite,
                    "description": row["task_description"],
                    "episodes": row["episodes"],
                    "successes": row["successes"],
                    "success_rate": row["success_rate"],
                }
            )
    total = {
        p: {
            "episodes": sum(r["episodes"] for r in eval_records if r["precision"] == p),
            "successes": sum(r["successes"] for r in eval_records if r["precision"] == p),
        }
        for p in ["fp32", "bf16"]
    }
    for p in total:
        total[p]["rate"] = total[p]["successes"] / total[p]["episodes"]
    source_commit = subprocess.check_output(
        ["git", "-C", str(ROOT / "source"), "rev-parse", "HEAD"], text=True
    ).strip()
    source_date = subprocess.check_output(
        ["git", "-C", str(ROOT / "source"), "show", "-s", "--format=%cI", source_commit], text=True
    ).strip()
    checksum_lines = (ART / "checksums.txt").read_text(encoding="utf-8").splitlines()
    ckpt_sha = checksum_lines[0].split()[0]
    model_params = fp_smoke["parameters"]
    mem_reduction = 1.0 - bf_rt["peak_cuda_allocated_bytes"] / fp_rt["peak_cuda_allocated_bytes"]
    runtime_delta = bf_rt["wall_ms_median"] / fp_rt["wall_ms_median"] - 1.0

    summary = {
        "generated_at": args.timestamp,
        "experiment_root": str(ROOT),
        "source_commit": source_commit,
        "source_commit_time": source_date,
        "checkpoint_sha256": ckpt_sha,
        "checkpoint_top_level": ["model_state_dict", "model_config"],
        "parameters": model_params,
        "runtime": {"fp32": fp_rt, "bf16": bf_rt, "bf16_vs_fp32_median_delta": runtime_delta},
        "memory_reduction_fraction": mem_reduction,
        "spot_check": {"fp32": total["fp32"], "bf16": total["bf16"], "records": eval_records},
        "official_reference": {
            "reported_libero_avg": 0.977,
            "reported_runtime_ms": 31.2,
            "reported_vram_gb": 0.9,
            "hardware": "RTX 4090",
        },
        "not_run": ["完整四套 50 trials/task 正式 benchmark", "W8A16 量化", "FPGA 周期映射"],
    }
    (ROOT / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    rows = []
    for r in eval_records:
        rows.append(
            f'<tr><td>{esc(r["precision"].upper())}</td><td>{esc(r["suite"])}</td>'
            f'<td>{esc(r["description"])}</td><td>{r["successes"]}/{r["episodes"]}</td>'
            f'<td>{100*r["success_rate"]:.0f}%</td></tr>'
        )
    runtime_table = (
        f'<tr><td>FP32</td><td>{fmt_ms(fp_rt["wall_ms_median"])}</td><td>{fmt_ms(fp_rt["wall_ms_p90"])}</td>'
        f'<td>{fmt_mib(fp_rt["peak_cuda_allocated_bytes"])}</td><td>{fmt_mib(fp_rt["peak_cuda_reserved_bytes"])}</td></tr>'
        f'<tr><td>BF16</td><td>{fmt_ms(bf_rt["wall_ms_median"])}</td><td>{fmt_ms(bf_rt["wall_ms_p90"])}</td>'
        f'<td>{fmt_mib(bf_rt["peak_cuda_allocated_bytes"])}</td><td>{fmt_mib(bf_rt["peak_cuda_reserved_bytes"])}</td></tr>'
    )
    output = ROOT / f"{args.timestamp}_TurboVLA服务器部署与profiling.html"
    html_text = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>TurboVLA 服务器部署与 profiling</title>
<style>
body{{margin:0;background:#f5f6f7;color:#20252b;font-family:"Microsoft YaHei",Arial,sans-serif;line-height:1.65}}
main{{max-width:1120px;margin:0 auto;padding:28px 34px 56px;background:#fff;min-height:100vh}}
h1{{font-size:28px;margin:0 0 5px}} h2{{font-size:20px;border-bottom:1px solid #d9dde2;padding-bottom:6px;margin-top:30px}}
h3{{font-size:16px;margin-bottom:5px}} .meta{{color:#66717c;font-size:13px}} .lead{{font-size:16px;background:#eef6f3;border-left:4px solid #1f8a70;padding:12px 16px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}} .kpi{{border:1px solid #d8dde3;padding:12px;background:#fafbfc}} .kpi b{{font-size:22px;display:block;color:#1d5f50}}
table{{width:100%;border-collapse:collapse;font-size:13px;margin:10px 0 18px}} th,td{{border:1px solid #d8dde3;padding:7px 8px;text-align:left;vertical-align:top}} th{{background:#eef1f3}}
.figure{{border:1px solid #d8dde3;padding:10px;margin:14px 0}} .caption{{font-size:13px;color:#4d5964;margin-top:5px}} .chart{{width:100%;max-height:300px}} .note{{color:#5a6570;font-size:13px}}
code{{background:#f0f2f4;padding:1px 4px}} a{{color:#195f8d}} ul{{margin-top:6px}}
@media(max-width:720px){{main{{padding:18px 14px}}h1{{font-size:23px}}.grid{{grid-template-columns:repeat(2,1fr)}}table{{font-size:12px;display:block;overflow-x:auto;white-space:nowrap}}.chart{{min-width:620px}}}}
</style></head><body><main>
<div class="meta">生成时间：{esc(display_timestamp)}　|　实验目录：{esc(ROOT)}</div>
<h1>TurboVLA 在 V100 上的部署与 runtime profiling</h1>
<p class="lead">结论：发布的 TurboVLA LIBERO checkpoint 已在 V100 上完成严格加载、真实 LIBERO 闭环和稳定单次推理测量。当前 V100 的稳定单次调用约 <b>{fp_rt['wall_ms_median']:.1f} ms（FP32）</b> / <b>{bf_rt['wall_ms_median']:.1f} ms（BF16）</b>；BF16 相比 FP32 的中位数变化为 <b>{runtime_delta*100:+.2f}%</b>，主要收益是显存从 {fmt_mib(fp_rt['peak_cuda_allocated_bytes'])} 降到 {fmt_mib(bf_rt['peak_cuda_allocated_bytes'])}（减少 {mem_reduction*100:.1f}%）。</p>
<div class="grid"><div class="kpi"><b>{model_params/1e6:.1f}M</b>严格加载参数</div><div class="kpi"><b>672</b>checkpoint 张量</div><div class="kpi"><b>{total['fp32']['successes']}/{total['fp32']['episodes']}</b>FP32 spot check</div><div class="kpi"><b>{total['bf16']['successes']}/{total['bf16']['episodes']}</b>BF16 spot check</div></div>

<h2>1. 这次实际跑了什么</h2>
<p>代码来自 TurboVLA 官方仓库 commit <code>{esc(source_commit)}</code>（{esc(source_date)}）。服务器使用 GPU 3 单进程共享；启动时记录到 GPU 3 仍有约 25.8 GiB 空闲，没有停止其他进程。模型 checkpoint 的 SHA-256 为 <code>{esc(ckpt_sha)}</code>。</p>
<p>发布文件的顶层字段是 <code>model_state_dict</code> 和 <code>model_config</code>，没有官方评测代码当前要求的 <code>ema_model_state_dict</code>。因此实验包装器只在本进程把回退顺序设为 EMA（若有）→ model_state_dict；任务、环境、动作协议和统计文件仍使用官方入口。</p>
<p>DINOv3 官方 HF 权重仓库在服务器上需要权限。checkpoint 本身包含完整 DINOv3 ViT-B/16 的 211 个张量，所以我们用 Transformers 的 <code>DINOv3ViTModel</code> 实例化同一结构，并从 checkpoint 抽出权重保存成本地目录；BERT 也从 checkpoint 抽出。图像归一化采用 DINOv3 官方 LVD-1689M 推荐的 ImageNet mean/std，输入保持 256×256，不做额外裁剪。</p>

<h2>2. V100 runtime</h2>
<div class="figure">{runtime_svg(fp_rt,bf_rt)}<div class="caption">这张图看稳定调用，不看第一次加载。每种精度先预热 5 次，再做 10 次 CUDA 同步测量；FP32 和 BF16 的 GPU event 时间与 wall time 基本一致。</div></div>
<table><thead><tr><th>配置</th><th>中位数</th><th>P90</th><th>峰值已分配显存</th><th>峰值保留显存</th></tr></thead><tbody>{runtime_table}</tbody></table>
<p>这里的 67 ms 是“当前 V100、两路 256×256 图像、在线 BERT、一次 12 动作 chunk”的单次规划推理，不是整回合耗时。它比官方在 RTX 4090 上报告的 31.2 ms 慢约 {((fp_rt['wall_ms_median']/31.2)-1)*100:.0f}%；两者 GPU 型号和软件环境不同，不能直接当作架构加速倍数。</p>
<p class="note">首次加载和第一次前向包含磁盘读取、CUDA kernel 初始化，FP32 smoke 约 {fp_smoke['elapsed_seconds']:.1f} s，BF16 smoke 约 {bf_smoke['elapsed_seconds']:.1f} s；这两个冷启动数不用于精度排名。重复调用输出最大绝对差为 0，输出形状为 12×7 且全部有限。</p>

<h2>3. LIBERO 闭环 spot check</h2>
<div class="figure">{success_svg(eval_records)}<div class="caption">每套只跑 task 0 的初始状态 0–4，共 5 回合；四套合计 20 回合。成功由 LIBERO 环境 done 判定，程序异常和初始化失败没有混入成功率。</div></div>
<table><thead><tr><th>精度</th><th>Suite</th><th>Task 0</th><th>成功/回合</th><th>成功率</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
<p>在这组固定 task 0 的小样本中，FP32 为 <b>{total['fp32']['successes']}/{total['fp32']['episodes']}（{total['fp32']['rate']*100:.0f}%）</b>，BF16 为 <b>{total['bf16']['successes']}/{total['bf16']['episodes']}（{total['bf16']['rate']*100:.0f}%）</b>。Goal 的两种精度都为 4/5；BF16 的 LIBERO-10 为 4/5，FP32 为 5/5。这个差异只有 1 个回合，不能据此推断精度导致策略退化。</p>
<p>Spatial task 0 的 FP32/BF16 录像各保留 1 段，已检查可解码：FP32 3.90 s，BF16 4.05 s。录像播放时间是仿真帧时间，不是推理速度。</p>

<h2>4. 官方数字与本次实测要分开</h2>
<table><thead><tr><th>口径</th><th>数字</th><th>怎么理解</th></tr></thead><tbody>
<tr><td>官方模型卡</td><td>LIBERO 平均 97.7%</td><td>官方完整 benchmark 报告；本次没有重跑 50 trials/task 的完整协议。</td></tr>
<tr><td>官方模型卡</td><td>31.2 ms、0.9 GB</td><td>RTX 4090 上的报告值；不能替代 V100 实测。</td></tr>
<tr><td>本次 V100</td><td>{fp_rt['wall_ms_median']:.2f} ms FP32 / {bf_rt['wall_ms_median']:.2f} ms BF16</td><td>稳定单次规划调用，真实 LIBERO 初始观测。</td></tr>
<tr><td>本次闭环</td><td>19/20 FP32、18/20 BF16</td><td>四套 task 0 各 5 回合的快速 spot check，不是论文成功率。</td></tr>
</tbody></table>
<p>官方参考：{link('https://github.com/H-EmbodVis/TurboVLA','TurboVLA 官方仓库')}、{link('https://huggingface.co/H-EmbodVis/TurboVLA','TurboVLA checkpoint/model card')}、{link('https://github.com/H-EmbodVis/TurboVLA/blob/main/experiments/libero/README.md','官方 LIBERO 评测说明')}、{link('https://github.com/facebookresearch/dinov3','DINOv3 官方预处理说明')}。</p>

<h2>5. 目前能下的结论</h2>
<ul><li><b>部署可行：</b>checkpoint、DINOv3、BERT、策略头和 LIBERO 环境已在 V100 上接通；严格加载的实际参数量是 {model_params/1e6:.1f}M，不是只看 action policy 的 40M。</li><li><b>V100 的瓶颈：</b>稳定调用约 67 ms，FP32 与 BF16 几乎同速；BF16 的确定收益是显存减少约 {mem_reduction*100:.1f}%，不是当前 V100 上的端到端加速。</li><li><b>策略行为：</b>task 0 spot check 合计 FP32 95%、BF16 90%，两种精度在 Goal 都各失败 1/5。样本太小，不能把 95%/90% 写成 TurboVLA 的正式成绩。</li><li><b>下一步：</b>如果要做正式对照，优先修正官方 evaluator 对 checkpoint 字段的兼容并固定 DINOv3 processor 文件，然后按官方四套、每任务 50 回合跑完整 benchmark；若目标是硬件映射，再以 trace 中 GEMM、BMM、softmax 和 DINO backbone 的算子形状建立周期表。</li></ul>

<h2>6. 交付文件</h2>
<ul><li>{link('summary.json','机器可读汇总')}</li><li>{link('remote_artifacts/runtime_fp32.json','FP32 runtime JSON')}、{link('remote_artifacts/runtime_bf16.json','BF16 runtime JSON')}</li><li>{link('remote_artifacts/trace_fp32.json.txt','FP32 算子统计')}、{link('remote_artifacts/trace_bf16.json.txt','BF16 算子统计')}、{link('remote_artifacts/trace_fp32.json','FP32 Chrome trace')}、{link('remote_artifacts/trace_bf16.json','BF16 Chrome trace')}</li><li>{link('remote_artifacts/eval_libero_spatial_fp32_5ep.json','FP32 Spatial 5 回合')}、{link('remote_artifacts/eval_libero_spatial_bf16_5ep.json','BF16 Spatial 5 回合')} 等四套 JSON 与原始日志</li><li>{link('remote_artifacts/spatial_task0_fp32.mp4','FP32 Spatial task 0 录像')}、{link('remote_artifacts/spatial_task0_bf16.mp4','BF16 Spatial task 0 录像')}</li><li>复现脚本位于 {link('scripts/runtime_profile.py','runtime_profile.py')}、{link('scripts/run_eval_patched.py','run_eval_patched.py')}、{link('scripts/prepare_local_backbones.py','prepare_local_backbones.py')}。</li></ul>
<p class="meta">未做：完整四套正式 50 trials/task benchmark、W8A16 量化、FPGA 周期映射。原因是本轮目标先确认服务器部署和稳定 runtime，避免把小样本或条件估计当成正式结果。</p>
</main></body></html>"""
    output.write_text(html_text, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
