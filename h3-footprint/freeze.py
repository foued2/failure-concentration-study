from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTIFACTS = [
    "GATE.md",
    "instrument.py",
    "generate.py",
    "run_gate.py",
    "probe_worker.py",
    "expected_values.json",
    "coherence_review.json",
    "freeze.py",
]
TAG = "h3-footprint-freeze-2026-10-26"


def main() -> None:
    hashes = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in ARTIFACTS
    }
    record = {
        "tag": TAG,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "artifact_hashes_sha256": hashes,
        "candidate_count_at_freeze": 0,
        "budget_batches": 72,
        "bodies_per_batch": 8,
        "target_rejected_bodies": 150,
        "thresholds": {"m_min": 4, "pass_cells": 3, "pass_k": 2, "pass_groups": 40, "weak_cells_max": 2, "degeneracy_max": 0.80},
    }
    out = ROOT / "FREEZE.json"
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
