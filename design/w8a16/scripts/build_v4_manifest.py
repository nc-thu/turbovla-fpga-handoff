"""Create the source/data manifest for the v4 timing-fixed archive."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "v4_2026-09-13_150700"
DATA = ROOT / "data" / VERSION


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def add_tree(files: list[Path], root: Path, *, exclude_runs: bool = False) -> None:
    if not root.exists():
        return
    for path in root.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if exclude_runs and "synth" in path.parts and "runs" in path.parts:
            # The selected system run is added explicitly below.  Old failed
            # attempts copied into the version directory are not part of v4.
            continue
        files.append(path)


def main() -> None:
    files: list[Path] = []
    add_tree(files, ROOT / "algo" / VERSION)
    add_tree(files, ROOT / "arch" / VERSION)
    add_tree(files, ROOT / "compiler" / VERSION)
    add_tree(files, ROOT / "hw" / VERSION, exclude_runs=True)
    add_tree(files, ROOT / "hw" / VERSION / "synth" / "runs" / "2026-09-13_150700_system_v14")
    add_tree(files, DATA)
    for name in ("collect_v4_rtl_results.py", "collect_v4_vivado_synth.py",
                 "generate_camera_ready_report_v4.py", "reproduce_v4_pipeline.ps1",
                 "build_v4_manifest.py"):
        p = ROOT / "scripts" / name
        if p.exists():
            files.append(p)
    # Do not hash the manifest being written.  Including its previous bytes
    # makes every rebuild report a stale self-hash and breaks reproducibility.
    out = (DATA / "file_manifest.json").resolve()
    unique = sorted({p.resolve() for p in files if p.resolve() != out})
    old_manifest = ROOT / "data" / "v3_2026-09-13_140118" / "file_manifest.json"
    old = json.loads(old_manifest.read_text(encoding="utf-8")) if old_manifest.exists() else {}
    data_hashes = {}
    for name in ("model_state_dict_shapes.json", "checkpoint_model_config.json", "quant_screening_summary.json"):
        p = DATA / name
        if p.exists():
            data_hashes[name] = sha256(p)
    manifest = {
        "schema_version": "tvla_w8a16.file_manifest.v4",
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "workspace": str(ROOT),
        "source_commit": old.get("source_commit", "not-recorded"),
        "checkpoint": old.get("checkpoint", {"status": "not-recorded"}),
        "version": VERSION,
        "metadata_hashes": data_hashes,
        "tracked_files": {str(p.relative_to(ROOT).as_posix()): sha256(p) for p in unique},
        "array_evidence": {
            "source_version": "v3_unchanged_array_top",
            "reason": "v4 vector_mul timing fix is not instantiated by top_w8a16_array",
            "records": [
                "2026-09-13_141621_array_1x1",
                "2026-09-13_141800_array_4x4",
                "2026-09-13_141900_array_16x48",
            ],
        },
        "notes": [
            "tracked_files 只覆盖 v4 源码、数据和当前 system_v14 原始综合报告；根级工作日志、旧版本和只读 references 不在本清单内。",
            "checkpoint hash 沿用 v3 归档的已记录值，没有重新下载 checkpoint。",
        ],
    }
    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / "file_manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "tracked_files": len(unique), "output": str(out)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
