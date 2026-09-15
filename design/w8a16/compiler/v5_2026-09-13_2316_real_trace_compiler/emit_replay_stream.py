"""Emit the descriptor sideband consumed by tvla_replay_top."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

OPCODE = {"GEMM_W8A16": 0x10, "BMM_W8A16": 0x11, "LAYER_NORM": 0x30, "SOFTMAX": 0x31, "GELU": 0x33, "AUX_EVENT": 0x50, "END": 0xFF}


def u32(value) -> int:
    return max(0, min(int(value or 0), 0xFFFFFFFF))


def pack_descriptor(d: dict) -> int:
    c = d.get("cycle_cost", {})
    words = [
        u32(c.get("total_cycles")), u32(c.get("valid_mac_count")), u32(c.get("valid_mac_count")),
        u32(c.get("activation_read_cycles")), u32(c.get("write_cycles")),
        u32(c.get("vector_cycles", c.get("fallback_cycles", 0))), u32(c.get("snapshot_cycles")),
        u32(c.get("requant_cycles")), u32(c.get("activation_bytes")), u32(c.get("weight_bytes")),
        u32(c.get("output_bytes")), u32(d.get("m")), u32(d.get("n")), u32(d.get("k")),
    ]
    value = 0
    for w in words:
        value = (value << 32) | w
    # Fourteen 32-bit words occupy [511:64]; the low 64 bits are reserved for
    # the compact operation code and tile count consumed by the RTL top.
    value <<= 64
    op = OPCODE.get(d.get("op", "AUX_EVENT"), 0x50)
    tile = u32(c.get("tile_count")) & 0xFFFF
    # The top decodes op at [63:56] and tile count at [31:16].
    value &= ~(((0xFF) << 56) | (0xFFFF << 16))
    value |= (op & 0xFF) << 56
    value |= tile << 16
    return value & ((1 << 512) - 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--compiled", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    descs = [json.loads(x) for x in (args.compiled / "descriptors.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    insts = [json.loads(x) for x in (args.compiled / "instructions.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    # Descriptor ids are contiguous by construction; use them as command ids.
    sideband = []
    for d in descs:
        raw = pack_descriptor(d)
        sideband.append({"descriptor_id": d["descriptor_id"], "word_hex": f"0x{raw:0128x}", "op": d["op"], "source_seq": d["source_seq"]})
    (out / "descriptor_words.hex").write_text("\n".join(x["word_hex"] for x in sideband) + "\n", encoding="utf-8")
    (out / "descriptors.jsonl").write_text("\n".join(json.dumps(d, sort_keys=True) for d in descs) + "\n", encoding="utf-8")
    words = []
    for i in insts:
        op = i["op"]
        if op == "END":
            words.append(f"0xFF00000000000000")
        else:
            words.append(f"0x{((OPCODE.get(op, 0x50) << 56) | ((int(i['descriptor_id']) & 0xFFFF) << 32) | (int(i['pc']) & 0xFFFF)):016x}")
    (out / "instructions.hex").write_text("\n".join(words) + "\n", encoding="utf-8")
    (out / "descriptor_words.json").write_text(json.dumps(sideband, indent=2), encoding="utf-8")
    shutil.copy2(args.compiled / "replay_summary.json", out / "replay_summary.json")
    print(json.dumps({"descriptors": len(descs), "instructions": len(insts), "output": str(out)}, indent=2))


if __name__ == "__main__":
    main()
