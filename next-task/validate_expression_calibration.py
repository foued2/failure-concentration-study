"""Independently validate the expression calibration run and raw captures."""
from __future__ import annotations

import base64
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PILOT = REPO / "natural-feasibility-pilot"
PIPELINE = PILOT / "python-pipeline-integration"
EXPRESSION_PIPELINE = ROOT / "pipeline_expression"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(PILOT))
sys.path.insert(0, str(PIPELINE))

from integration_runner import validate_capture_directory
from expression_task import FAMILY_ORDER

BANKS = ROOT / "banks"
RUN = ROOT / "calibration-20261022T084750Z-288f2ac1"

SOURCE_PATHS = {
    "run_expression_calibration.py": ROOT / "run_expression_calibration.py",
    "expression_mutants.py": ROOT / "expression_mutants.py",
    "expression_task.py": ROOT / "expression_task.py",
    "build_expression_banks.py": ROOT / "build_expression_banks.py",
    "freeze_expression_banks.py": ROOT / "freeze_expression_banks.py",
    "calibration_protocol": ROOT / "CALIBRATION_PROTOCOL_2026-10-22.md",
    "banks/FREEZE.json": BANKS / "FREEZE.json",
    "banks/diagnostic.json": BANKS / "diagnostic.json",
    "banks/evaluation.json": BANKS / "evaluation.json",
    "run_generated_smoke.py": PILOT / "run_generated_smoke.py",
    "source_policy.py": PILOT / "source_policy.py",
    "integration_runner.py": PILOT / "integration_runner.py",
    "python-pipeline-integration/python_adapter.py": PIPELINE / "python_adapter.py",
    "python-pipeline-integration/sandbox_suite_supervisor.ps1": PIPELINE / "sandbox_suite_supervisor.ps1",
    "pipeline_expression/python_adapter.py": EXPRESSION_PIPELINE / "python_adapter.py",
    "pipeline_expression/sandbox_suite_supervisor.ps1": EXPRESSION_PIPELINE / "sandbox_suite_supervisor.ps1",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def parse_output(stdout_b64: str):
    raw = base64.b64decode(stdout_b64, validate=True)
    text = raw.decode("utf-8", errors="strict").strip()
    if not text:
        raise ValueError("empty stdout")
    return int(text)


def independent_outcome(row: dict, expected: int) -> dict:
    parsed = None
    error = None
    correct = False
    if row["status"] == "complete" and row["exit_code"] == 0 and not row["timed_out"]:
        try:
            parsed = parse_output(row["stdout_b64"])
            correct = type(parsed) is int and parsed == expected
        except (ValueError, UnicodeDecodeError) as exc:
            error = str(exc)
    else:
        error = row["status"]
    status = "pass" if correct else "wrong" if parsed is not None else "invalid" if row["status"] == "complete" else row["status"]
    return {
        "probe_id": row["probe_id"],
        "solver_output": parsed,
        "expected": expected,
        "correct": correct,
        "status": status,
        "error": error,
        "tree_terminated": row["tree_terminated"],
        "timed_out": row["timed_out"],
    }


def check(condition: bool, message: str, checks: list[str]) -> None:
    if not condition:
        raise AssertionError(message)
    checks.append(message)


def main() -> None:
    checks: list[str] = []
    result = load(RUN / "CALIBRATION_RESULT.json")
    protocol = load(RUN / "PROTOCOL.json")
    panel = load(RUN / "PANEL.json")
    freeze = load(BANKS / "FREEZE.json")
    diagnostic_doc = load(BANKS / "diagnostic.json")
    evaluation_doc = load(BANKS / "evaluation.json")

    check(result["status"] == "PASS", "calibration result is PASS", checks)
    check(result["gate_pass"] is True, "calibration gate flag is true", checks)
    check(result["no_model_calls"] is True and result["model_calls"] == 0, "zero model calls recorded", checks)
    check(result["generation_attempts"] == 0, "zero generation attempts recorded", checks)
    check(result["protocol"] == protocol, "embedded protocol matches PROTOCOL.json", checks)
    check(result["gaps"] == [], "no calibration gaps", checks)
    check(freeze["status"] == "FROZEN_FOR_CALIBRATION", "banks are frozen for calibration", checks)
    check(protocol["input_hashes"]["diagnostic.json"] == freeze["diagnostic"]["sha256"], "diagnostic freeze hash matches protocol", checks)
    check(protocol["input_hashes"]["evaluation.json"] == freeze["evaluation"]["sha256"], "evaluation freeze hash matches protocol", checks)

    for key, expected in protocol["source_hashes"].items():
        check(key in SOURCE_PATHS, f"source hash key is recognized: {key}", checks)
        check(SOURCE_PATHS[key].is_file(), f"source file exists: {key}", checks)
        check(sha256_file(SOURCE_PATHS[key]) == expected, f"source hash matches: {key}", checks)
    check(sha256_file(BANKS / "diagnostic.json") == freeze["diagnostic"]["sha256"], "diagnostic bank hash unchanged", checks)
    check(sha256_file(BANKS / "evaluation.json") == freeze["evaluation"]["sha256"], "evaluation bank hash unchanged", checks)
    check(sha256_file(BANKS / "BUILD_MANIFEST.json") == freeze["manifest_sha256"], "bank manifest hash unchanged", checks)
    check(canonical_hash(panel) == protocol["panel_sha256"], "calibration panel hash matches protocol", checks)

    diagnostic = diagnostic_doc["records"]
    evaluation = evaluation_doc["records"]
    check(len(diagnostic) == 30 and len(evaluation) == 30, "both banks have 30 records", checks)
    check(len({record["probe_id"] for record in diagnostic}) == 30, "diagnostic IDs are unique", checks)
    check(len({record["hid"] for record in evaluation}) == 30, "evaluation IDs are unique", checks)
    check({record["expr"] for record in diagnostic} & {record["expr"] for record in evaluation} == set(), "bank expressions are disjoint", checks)
    check(
        all(Counter(record["family"] for record in diagnostic)[family] == 5 for family in FAMILY_ORDER),
        "diagnostic bank is five per family",
        checks,
    )
    check(
        all(Counter(record["family"] for record in evaluation)[family] == 5 for family in FAMILY_ORDER),
        "evaluation bank is five per family",
        checks,
    )

    variants = result["variants"]
    check(len(variants) == 7, "one reference and six faulty variants recorded", checks)
    check(variants[0]["variant"] == "reference_parser", "reference variant is first", checks)
    check([record["variant"] for record in variants] == panel["order"], "variant order matches panel", checks)
    reference = variants[0]
    check(reference["status"] == "executed", "reference executed", checks)
    check(reference["diagnostic"]["failed"] == 0, "reference has zero diagnostic failures", checks)
    check(reference["evaluation"]["correct"] == 30, "reference has 30/30 evaluation correct", checks)
    check(reference["all_tree_terminated"] is True, "reference transport tree-terminated", checks)

    captures: list[dict] = []
    for name in panel["order"]:
        variant_dir = RUN / "variants" / name
        summary = load(variant_dir / "variant-summary.json")
        result_record = next(record for record in variants if record["variant"] == name)
        check(summary["screen"]["accepted"] is True, f"{name}: source accepted", checks)
        check(
            summary["screen"]["source_sha256"] == sha256_text((variant_dir / "source.py").read_text(encoding="utf-8")),
            f"{name}: source hash matches retained source file",
            checks,
        )
        is_reference = name == "reference_parser"
        target = None if is_reference else panel["targets"][name]
        if not is_reference:
            check(summary["status"] == "executed", f"{name}: executed", checks)
            check(summary["gate_pass"] is True, f"{name}: variant gate pass", checks)
            check(summary["target_family"] == target, f"{name}: target family retained", checks)
            check(summary["target_diagnostic_failures"] == 5, f"{name}: five diagnostic target failures", checks)
            check(summary["target_evaluation_failures"] == 5, f"{name}: five evaluation target failures", checks)
            check(summary["cross_family_diagnostic"] == {}, f"{name}: no diagnostic cross-family failures", checks)
            check(summary["cross_family_evaluation"] == {}, f"{name}: no evaluation cross-family failures", checks)
            check(result_record["gate_pass"] is True, f"{name}: result gate pass", checks)

        for phase, bank, id_key, suite_prefix, case_prefix in (
            ("diagnostic", diagnostic, "probe_id", "diagnostic-", "diagnostic_"),
            ("evaluation", evaluation, "hid", "evaluation-", "holdout_"),
        ):
            capture_dir = RUN / "guest-captures" / f"{suite_prefix}{name}"
            capture_path = capture_dir / "capture.json"
            check(capture_path.is_file(), f"{name}/{phase}: capture exists", checks)
            capture_doc = load(capture_path)
            case_id = f"{case_prefix}{name}"
            check(capture_doc["case_id"] == case_id, f"{name}/{phase}: case id matches", checks)
            transport = validate_capture_directory(capture_dir, capture_doc["nonce"], case_id)
            check(len(transport["probe_rows"]) == 30, f"{name}/{phase}: 30 raw rows", checks)
            expected_ids = [record[id_key] for record in bank]
            check([row["probe_id"] for row in transport["probe_rows"]] == expected_ids, f"{name}/{phase}: raw row order matches bank", checks)
            expected_by_id = {record[id_key]: record["expected"] for record in bank}
            family_by_id = {record[id_key]: record["family"] for record in bank}
            recomputed = [independent_outcome(row, expected_by_id[row["probe_id"]]) for row in transport["probe_rows"]]
            for row, expected_row in zip(recomputed, summary[phase]["probe_rows"], strict=True):
                check(row["probe_id"] == expected_row["probe_id"], f"{name}/{phase}: retained row id matches", checks)
                check(row["status"] == expected_row["status"], f"{name}/{phase}: retained status recomputes", checks)
                check(row["correct"] == expected_row["correct"], f"{name}/{phase}: retained correctness recomputes", checks)
                check(row["solver_output"] == expected_row["solver_output"], f"{name}/{phase}: retained output recomputes", checks)
                check(row["tree_terminated"] is True, f"{name}/{phase}: row tree terminated", checks)
            if not is_reference:
                fail_counts = Counter(
                    family_by_id[row["probe_id"]] for row in recomputed if row["status"] != "pass"
                )
                check(fail_counts[target] == 5, f"{name}/{phase}: target family failures recompute", checks)
                check(
                    all(fail_counts[family] == 0 for family in FAMILY_ORDER if family != target),
                    f"{name}/{phase}: no cross-family failures recompute",
                    checks,
                )
            captures.append({
                "variant": name,
                "phase": phase,
                "case_id": case_id,
                "path": str(capture_path.relative_to(RUN)),
                "sha256": sha256_file(capture_path),
                "rows": len(transport["probe_rows"]),
            })

    check(len(captures) == 14, "14 raw capture files validated", checks)
    integrity = {
        "schema": 1,
        "run_id": RUN.name,
        "status": "PASS",
        "checks": checks,
        "capture_count": len(captures),
        "captures": captures,
        "bank_hashes": {
            "diagnostic": freeze["diagnostic"]["sha256"],
            "evaluation": freeze["evaluation"]["sha256"],
            "freeze": sha256_file(BANKS / "FREEZE.json"),
        },
    }
    (RUN / "INTEGRITY.json").write_text(json.dumps(integrity, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "PASS",
        "run_id": RUN.name,
        "checks": len(checks),
        "captures": len(captures),
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
