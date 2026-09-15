"""Create a reproducibility manifest for the captured TurboVLA replay round."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()
    data = args.data
    cap = json.loads((data / "capture_result.json").read_text(encoding="utf-8"))
    files = {}
    for p in sorted(data.rglob("*")):
        if p.is_file() and p.name not in {"trace_manifest.json"}:
            rel = p.relative_to(data).as_posix()
            files[rel] = {"bytes": p.stat().st_size, "sha256": digest(p)}
    manifest = {
        "schema_version": "tvla_w8a16.trace_manifest.v1",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "round": "2026-09-13_231621",
        "capture_status": cap.get("status"),
        "source": {
            "suite": cap.get("suite"),
            "task_id": cap.get("task_id"),
            "instruction": cap.get("instruction"),
            "device_requested": cap.get("device_requested", cap.get("device")),
            "seed": cap.get("seed"),
            "parameter_count": cap.get("parameter_count", cap.get("parameters")),
            "module_events": cap.get("module_events", cap.get("module_event_count")),
            "dispatch_events": cap.get("dispatch_events", cap.get("dispatch_event_count")),
            "linear_events": cap.get("linear_events", cap.get("linear_event_count")),
            "unique_weights": cap.get("unique_weights", cap.get("weight_unique_count")),
        },
        "quantization": {"activation_bits": 16, "weight_bits": 8, "accumulator_bits": 40, "output_bits": 16, "scale_source": "capture-generated per-event calibration metadata"},
        "hardware_replay": {"rows": 16, "physical_cols": 48, "dsp": 768, "clock_mhz": 250.0, "command_bits": 64, "descriptor_bits": 512, "array_cycle_replay": "representative tile", "full_trace_replay": "virtual event counters"},
        "host": {"platform": platform.platform(), "python": platform.python_version()},
        "files": files,
    }
    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "file_count": len(files), "capture_status": cap.get("status")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
