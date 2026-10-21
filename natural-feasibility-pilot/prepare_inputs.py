"""Prepare only the unique diagnostic and evaluation input records; run no solvers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

REPOSITORY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY))

from study.instances import make_hidden_suite
from study.probes import make_probe_suite
from pilot_tool import check_edge_fixtures, check_input_separation, input_id

ROOT = Path(__file__).resolve().parent
SEED = 20261020


def main() -> None:
    diagnostic = make_probe_suite(SEED)
    evaluation = make_hidden_suite(SEED, m_count=20)
    check = check_input_separation(diagnostic, evaluation)
    fixture_check = check_edge_fixtures(evaluation)
    if not check["passed"] or not fixture_check["passed"]:
        raise SystemExit(f"input integrity failed: overlap={check}, fixtures={fixture_check}")

    diagnostic_records = [
        {"probe_id": p["probe_id"], "family": p["family"], "input_id": input_id(p),
         "input": {k: p[k] for k in ("n", "edges", "s", "t")}}
        for p in diagnostic
    ]
    evaluation_records = [
        {"input_id": input_id(h), "hid": h["hid"],
         "input": {k: h[k] for k in ("n", "edges", "s", "t")}}
        for h in evaluation
    ]
    payloads = {
        "diagnostic_battery.json": diagnostic_records,
        "evaluation_bank.json": evaluation_records,
        "input_integrity.json": check,
        "edge_fixture_integrity.json": fixture_check,
    }
    hashes = {}
    for name, value in payloads.items():
        data = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")
        (ROOT / name).write_bytes(data)
        hashes[name] = hashlib.sha256(data).hexdigest()

    manifest = {
        "status": "INPUTS_PREPARED_NO_SOLVER_EXECUTION",
        "seed": SEED,
        "diagnostic_generator": "study.probes.make_probe_suite",
        "evaluation_generator": "study.instances.make_hidden_suite(seed, m_count=20)",
        "evaluation_distribution": "15 random graphs plus 5 existing edge templates",
        "evaluation_count": len(evaluation),
        "records": hashes,
        "integrity": check,
        "edge_fixture_integrity": fixture_check,
    }
    (ROOT / "input_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
