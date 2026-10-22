"""Freeze the validated expression banks before the calibration run."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BANKS = ROOT / "banks"
MANIFEST = BANKS / "BUILD_MANIFEST.json"
FREEZE = BANKS / "FREEZE.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    if FREEZE.exists():
        raise FileExistsError(FREEZE)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("status") != "BUILT_NOT_FROZEN":
        raise RuntimeError("bank manifest is not in the expected pre-freeze state")
    for name, expected in (
        ("diagnostic", manifest["diagnostic"]),
        ("evaluation", manifest["evaluation"]),
    ):
        actual = sha256_file(BANKS / expected["path"])
        if actual != expected["sha256"]:
            raise RuntimeError(f"{name} bank hash mismatch")
        if expected["records"] != 30:
            raise RuntimeError(f"{name} bank does not contain 30 records")
        if set(expected["family_counts"].values()) != {5}:
            raise RuntimeError(f"{name} bank is not five per family")
    freeze = {
        "schema": 1,
        "task_id": manifest["task_id"],
        "status": "FROZEN_FOR_CALIBRATION",
        "frozen_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "no_model_calls": True,
        "diagnostic": {
            "path": "diagnostic.json",
            "sha256": manifest["diagnostic"]["sha256"],
            "records": 30,
        },
        "evaluation": {
            "path": "evaluation.json",
            "sha256": manifest["evaluation"]["sha256"],
            "records": 30,
        },
        "manifest_sha256": sha256_file(MANIFEST),
        "post_freeze_rule": (
            "Do not edit either bank or this freeze record. If calibration fails, "
            "report the gaps and stop; create a new task version rather than tuning "
            "the observed banks."
        ),
    }
    FREEZE.write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(freeze, indent=2), flush=True)


if __name__ == "__main__":
    main()
