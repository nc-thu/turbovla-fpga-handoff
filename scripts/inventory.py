#!/usr/bin/env python3
"""Write a small, deterministic inventory for a cloned handoff package."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    rows = []
    for p in sorted(root.rglob('*')):
        if not p.is_file() or '.git' in p.parts:
            continue
        rel = p.relative_to(root).as_posix()
        # The inventory is generated after the source tree is assembled.  Do
        # not recursively hash the previous inventory itself; this keeps the
        # manifest deterministic when it is regenerated.
        # Simulation binaries/logs are deliberately ignored by .gitignore and
        # are not part of the handoff manifest either.
        if rel == 'package_inventory.json' or p.suffix.lower() in {'.vvp'} or p.name == 'system_top_elaboration.log':
            continue
        rows.append({'path': rel, 'bytes': p.stat().st_size, 'sha256': sha256(p)})
    out = root / 'package_inventory.json'
    out.write_text(json.dumps({'root': str(root), 'files': rows}, indent=2), encoding='utf-8')
    print(out)
    print(f'files={len(rows)} bytes={sum(x["bytes"] for x in rows)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
