#!/usr/bin/env python3
"""Hash the timing version's source and generated evidence files."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    wanted = []
    for sub in ("rtl", "sim", "vivado", "data"):
        base = root / sub
        if base.exists():
            wanted.extend(p for p in base.rglob("*") if p.is_file() and p.name != "version_hashes.json")
    result = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "root": str(root),
        "files": {},
    }
    for path in sorted(wanted):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        result["files"][str(path.relative_to(root)).replace("\\", "/")] = digest
    out = root / "data" / "version_hashes.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
