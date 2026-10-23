from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.model import (  # noqa: E402
    FAMILY_COUNT,
    FAMILY_ORDER,
    PROBES_PER_FAMILY,
    attainable_vectors,
    concentration,
)

OUT = ROOT / "profiles"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    vectors = list(attainable_vectors())
    if len(vectors) != (PROBES_PER_FAMILY + 1) ** FAMILY_COUNT:
        raise AssertionError("profile enumeration size mismatch")
    cells: dict[tuple[int, float | None], dict[str, object]] = {}
    for vector in vectors:
        k, c = concentration(vector)
        key = (k, c)
        cell = cells.setdefault(key, {"count": 0, "example": vector})
        cell["count"] = int(cell["count"]) + 1
    with (OUT / "attainable_profiles.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow([*[f"f{index}" for index in range(FAMILY_COUNT)], "k", "C"])
        for vector in vectors:
            k, c = concentration(vector)
            writer.writerow([*vector, k, "" if c is None else f"{c:.12f}"])
    with (OUT / "attainable_cells.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["k", "C", "vector_count", "example_vector"])
        for (k, c), cell in sorted(cells.items(), key=lambda item: (item[0][0], -1 if item[0][1] is None else item[0][1])):
            writer.writerow([k, "" if c is None else f"{c:.12f}", cell["count"], json.dumps(cell["example"], separators=(",", ":"))])

    targets = []
    for index in range(FAMILY_COUNT):
        profile = [0] * FAMILY_COUNT
        profile[index] = PROBES_PER_FAMILY
        k, c = concentration(profile)
        targets.append({
            "target_id": f"T{index}_{FAMILY_ORDER[index]}",
            "profile": profile,
            "k": k,
            "C": c,
            "assigned_slots": 20,
            "carrier_family": FAMILY_ORDER[index],
            "reason": "fixed k=5, maximum attainable concentration; carrier family rotated",
        })
    spread_profile = [1, 1, 1, 1, 1, 0]
    k, c = concentration(spread_profile)
    targets.append({
        "target_id": "T6_SPREAD",
        "profile": spread_profile,
        "k": k,
        "C": c,
        "assigned_slots": 30,
        "carrier_family": None,
        "reason": "fixed k=5, low concentration; one failure in each of five families",
    })
    total = sum(int(target["assigned_slots"]) for target in targets)
    if total != 150:
        raise AssertionError("target allocation does not sum to 150")
    if any(tuple(target["profile"]) not in vectors for target in targets):
        raise AssertionError("selected target is not attainable")
    selected = {
        "schema": 1,
        "status": "TARGETS_SELECTED_FROM_FEASIBLE_SET_BEFORE_GENERATION",
        "selection_basis": (
            "All nonnegative integer vectors with each family count in 0..5 were enumerated first. "
            "Targets use k=5, where C=1 and C=0.2 are both attainable, and rotate the carrier "
            "family across all six families. No solver result was used."
        ),
        "family_order": list(FAMILY_ORDER),
        "probe_count_per_family": PROBES_PER_FAMILY,
        "total_feasible_vectors": len(vectors),
        "total_allocated_slots": total,
        "targets": targets,
        "files": {
            "attainable_profiles.csv": sha256_file(OUT / "attainable_profiles.csv"),
            "attainable_cells.csv": sha256_file(OUT / "attainable_cells.csv"),
            "build_profiles.py": sha256_file(Path(__file__).resolve()),
        },
    }
    write_json(OUT / "selected_profiles.json", selected)
    print(json.dumps({
        "vectors": len(vectors),
        "cells": len(cells),
        "targets": [{"id": target["target_id"], "k": target["k"], "C": target["C"]} for target in targets],
        "allocated": total,
        "selected_sha256": sha256_file(OUT / "selected_profiles.json"),
    }, indent=2))


if __name__ == "__main__":
    main()
