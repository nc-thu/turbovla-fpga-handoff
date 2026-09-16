"""Small compiler-side contract test for the v6 DMA memory target field.

The test deliberately uses one synthetic DMA_READ rather than the full trace:
it checks the new descriptor field and its 512-bit sideband encoding without
rerunning the long model capture.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPILER = next((ROOT / "compiler").glob("v6_*/compile_complete_model.py"))


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="tvla_v6_dma_contract_") as td:
        capture = Path(td) / "capture"
        output = Path(td) / "output"
        capture.mkdir()
        event = {
            "seq": 0,
            "op_type": "dma_read",
            "module_path": "memory.ctx_loader",
            "input_shape": [1, 32],
            "output_shape": [1, 32],
            "bytes": 32,
            "base_addr": 0x1000,
            "memory_target": "ctx",
        }
        (capture / "operator_trace.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")
        (capture / "module_events.jsonl").write_text("", encoding="utf-8")
        subprocess.run([sys.executable, str(COMPILER), "--capture", str(capture),
                        "--output", str(output)], check=True,
                       stdout=subprocess.DEVNULL)
        record = json.loads((output / "descriptors.jsonl").read_text(encoding="utf-8").splitlines()[0])
        sideband = int(record["descriptor_sideband_hex"], 16)
        assert record["op"] == "DMA_READ", record
        assert record["memory_target"] == "ctx", record
        assert ((sideband >> 496) & 0x3) == 0, hex(sideband)
        assert ((sideband >> 320) & 0xFFFF_FFFF) == 32, hex(sideband)
        print("V6_DMA_DESCRIPTOR PASS op=DMA_READ target=ctx bytes=32 sideband_target=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
