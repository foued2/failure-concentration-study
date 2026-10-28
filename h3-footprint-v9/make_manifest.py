"""Record and verify hashes of the V9 executable surface.

Docs and status files are intentionally excluded: a manifest that changes when
prose changes cannot protect the code. Freeze-time run:
`python make_manifest.py` then commit `MANIFEST.json`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INCLUDE = (
    "constants.py",
    "oracle.py",
    "controller.py",
    "backend.py",
    "supervisor.py",
    "child_runner.py",
    "sandbox_agent.py",
    "winjob.py",
    "protocol.py",
    "gates.py",
    "generation/generate_v9.py",
    "generation/agent/h3-generator.md",
)


def canonical(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def build() -> dict:
    return {
        "version": 9,
        "note": "Executable surface only. Regenerate at freeze time.",
        "artifact_hashes_sha256": {name: canonical(HERE / name) for name in INCLUDE},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    path = HERE / "MANIFEST.json"
    current = build()
    if args.check:
        if not path.exists():
            raise SystemExit("MANIFEST.json missing")
        recorded = json.loads(path.read_text(encoding="utf-8"))
        if recorded.get("artifact_hashes_sha256") != current["artifact_hashes_sha256"]:
            raise SystemExit("MANIFEST.json does not match the working tree")
        print("manifest OK")
        return
    path.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
