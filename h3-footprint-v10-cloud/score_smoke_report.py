"""Score only the hand-written executor-control fixture in a separate job.

This is a test of transport and scoring-job separation. It must never be
interpreted as a candidate result or an H3 scientific result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
V3 = ROOT / "h3-footprint-v3"
if str(V3) not in sys.path:
    sys.path.insert(0, str(V3))

import instrument



MAX_JSON_BYTES = 2 * 1024 * 1024
MAX_JSON_DEPTH = 64

def _check_json_depth(text: str, label: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char in "[{":
            depth += 1
            if depth > MAX_JSON_DEPTH:
                raise ValueError(f"{label} exceeds maximum JSON nesting depth {MAX_JSON_DEPTH}")
        elif char in "]}":
            depth -= 1
            if depth < 0:
                raise ValueError(f"{label} has unbalanced JSON nesting")
    if in_string or depth != 0:
        raise ValueError(f"{label} has incomplete JSON structure")

def _load_bounded_json(path: Path, label: str):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_JSON_BYTES + 1)
    if len(raw) > MAX_JSON_BYTES:
        raise ValueError(f"{label} exceeds {MAX_JSON_BYTES} byte limit")
    try:
        text = raw.decode("utf-8")
        _check_json_depth(text, label)
        return json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError):
        raise ValueError(f"{label} is not valid bounded UTF-8 JSON") from None

def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def score(report_path: Path, fixture_manifest_path: Path) -> dict:
    report = _load_bounded_json(report_path, "execution report")
    manifest = _load_bounded_json(fixture_manifest_path, "fixture manifest")
    if not isinstance(report, dict) or not isinstance(manifest, dict):
        raise ValueError("report and fixture manifest must be JSON objects")

    if manifest.get("kind") != "fixed_harness_control":
        raise ValueError("not a fixed harness-control fixture")
    if manifest.get("expected_answers_in_fixture") is not False:
        raise ValueError("fixture must not include expected answers")
    if manifest.get("model_generated") is not False:
        raise ValueError("this control cannot be model-generated")
    if report.get("candidate_sha256") != manifest.get("body_sha256"):
        raise ValueError("executed body hash does not match the fixture manifest")
    if report.get("probe_count") != 30 or len(report.get("results", [])) != 30:
        raise ValueError("expected exactly 30 prediction records")
    if report.get("isolation_harness_ok") is not True or report.get("all_trees_empty") is not True:
        raise ValueError("execution harness did not pass")
    if report.get("candidate_generation_performed") is not False:
        raise ValueError("unexpected candidate generation")
    if report.get("scoring_performed") is not False:
        raise ValueError("executor must not claim to score")
    if report.get("reference_answers_present") is not False:
        raise ValueError("executor report must attest that reference answers were absent")
    if report.get("host_repository_mounted") is not False:
        raise ValueError("repository was unexpectedly mounted in candidate container")
    if report.get("api_keys_passed_to_container") is not False:
        raise ValueError("API keys were unexpectedly passed to candidate container")
    if not all(report.get("container_config", {}).get("checks", {}).values()):
        raise ValueError("container configuration checks did not all pass")

    expected = instrument.expected_values()
    results = report["results"]
    for index, record in enumerate(results):
        if not isinstance(record, dict):
            raise ValueError(f"prediction record {index} is not an object")
        if record.get("status") != "ok":
            raise ValueError(f"prediction record {index} status is not ok")
        if record.get("tree_empty") is not True:
            raise ValueError(f"prediction record {index} does not attest an empty process tree")
        if record.get("processes_present_at_post_child_check") is not False:
            raise ValueError(f"prediction record {index} reports a process tree at the post-check")
        if record.get("tmp_cleanup_ok") is not True:
            raise ValueError(f"prediction record {index} scratch cleanup did not pass")
        if record.get("timed_out") is not False or record.get("output_overflow") is not False:
            raise ValueError(f"prediction record {index} timed out or overflowed output")
        if record.get("child_return_code") != 0:
            raise ValueError(f"prediction record {index} worker exit code was not zero")
    result_ids = [record.get("probe_id") for record in results]
    expected_ids = [probe["probe_id"] for probe in instrument.PROBES]
    if result_ids != expected_ids:
        raise ValueError("prediction records do not match the frozen V3 probe order")

    rows = []
    for record in results:
        probe_id = record["probe_id"]
        answer = record.get("answer")
        correct_type = record.get("status") == "ok" and record.get("answer_type") == "int" and type(answer) is int
        matches = correct_type and answer == expected[probe_id]
        rows.append({
            "probe_id": probe_id,
            "prediction_status": record.get("status"),
            "predicted_answer_type": record.get("answer_type"),
            "prediction_matches_reference": bool(matches),
        })

    correct = sum(1 for row in rows if row["prediction_matches_reference"])
    if correct != 30:
        raise ValueError(f"fixed harness control only matched {correct}/30 trusted answers")

    return {
        "version": 1,
        "status": "PASS",
        "scope": "fixed, hand-written control on V3 probe inputs; not model-generated candidates",
        "probe_count": 30,
        "correct_control_predictions": correct,
        "prediction_ids_match_frozen_order": True,
        "executor_was_reference_blind": True,
        "scoring_ran_in_separate_job": True,
        "candidate_generation_performed": False,
        "H3_candidate_evaluation_performed": False,
        "H3_scientific_result": False,
        "fixed_control_rows": rows,
        "execution_report_sha256": sha256(Path(report_path)),
        "fixture_manifest_sha256": sha256(Path(fixture_manifest_path)),
        "fixture_body_sha256": manifest["body_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--fixture-manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = score(Path(args.report), Path(args.fixture_manifest))
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "probe_count": result["probe_count"],
        "correct_control_predictions": result["correct_control_predictions"],
        "candidate_generation_performed": False,
        "H3_scientific_result": False,
        "report": str(output),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
