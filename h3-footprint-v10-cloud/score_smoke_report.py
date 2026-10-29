"""Score only the hand-written executor-control fixture in a separate job.

This is a test of transport and scoring-job separation. It never imports or
executes candidate code. It must never be interpreted as an H3 scientific result.
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
import run_gate


FROZEN_REQUIRED = ("GATE.md", "expected_values.json", "instrument.py", "probe_worker.py", "run_gate.py")
FROZEN_V3_FREEZE_GIT_BLOB_SHA1 = "d112abbdabe904c4f8f29463f018a04e7ab92eea"
KNOWN_OK_ANSWER_TYPES = {"none", "bool", "int", "int_out_of_range", "str", "float", "other"}
PROBE_FAILURE_STATUSES = {"timeout", "exception", "output_overflow"}
CANDIDATE_INVALID_STATUSES = {
    "invalid_child_output", "invalid_input", "load_error", "supervisor_error",
    "boundary_error", "tree_cleanup_failed", "process_tree_leak", "tmp_cleanup_failed",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(Path(path).read_bytes())


def git_blob_sha1(path: Path) -> str:
    """Hash canonical LF bytes as a Git blob, independent of checkout line endings."""
    raw = Path(path).read_bytes().replace(b"\r\n", b"\n")
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def canonical_probe_payloads() -> list[dict]:
    return [
        {
            "probe_id": probe["probe_id"],
            "n": probe["n"],
            "edges": [list(edge) for edge in probe["edges"]],
            "s": probe["s"],
            "t": probe["t"],
        }
        for probe in instrument.PROBES
    ]


def canonical_probe_payload_sha256() -> str:
    payload = json.dumps(canonical_probe_payloads(), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(payload)


def verify_frozen_v3() -> dict:
    freeze_path = V3 / "FREEZE.json"
    if git_blob_sha1(freeze_path) != FROZEN_V3_FREEZE_GIT_BLOB_SHA1:
        raise ValueError("V3 FREEZE.json does not match the pinned frozen manifest blob")
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    if freeze.get("tag") != "h3-footprint-v3-freeze-2026-10-27":
        raise ValueError("unexpected V3 freeze tag")
    if freeze.get("status") != "PRE_CANDIDATE_HARNESS_FREEZE":
        raise ValueError("V3 freeze is not in the expected pre-candidate state")
    artifact_hashes = freeze.get("artifact_hashes_sha256")
    if not isinstance(artifact_hashes, dict):
        raise ValueError("V3 freeze has no artifact hash table")
    checked = {}
    for name in FROZEN_REQUIRED:
        expected = artifact_hashes.get(name)
        if not isinstance(expected, str):
            raise ValueError(f"V3 freeze omits required file: {name}")
        actual = sha256(V3 / name)
        if actual != expected:
            raise ValueError(f"frozen V3 hash mismatch: {name}")
        checked[name] = actual

    frozen_expected = json.loads((V3 / "expected_values.json").read_text(encoding="utf-8"))
    recomputed_expected = instrument.expected_values()
    if frozen_expected != recomputed_expected:
        raise ValueError("current V3 oracle implementation disagrees with frozen expected values")
    if len(instrument.PROBES) != 30 or len(frozen_expected) != 30:
        raise ValueError("expected exactly 30 frozen V3 probes")
    return {
        "tag": freeze["tag"],
        "status": freeze["status"],
        "checked_artifact_sha256": checked,
        "probe_count": len(instrument.PROBES),
        "expected_values_recomputed_and_equal": True,
    }


def validate_probe_binding(report: dict, manifest: dict) -> None:
    if report.get("probe_payload_sha256") != manifest.get("probe_payload_sha256"):
        raise ValueError("executed probe payload hash does not match the fixture manifest")
    if report.get("probe_ids") != manifest.get("probe_ids"):
        raise ValueError("executed probe IDs do not match the fixture manifest")
    if report.get("probe_payload_sha256") != canonical_probe_payload_sha256():
        raise ValueError("fixture probe payload hash does not match frozen V3 inputs")
    expected_ids = [probe["probe_id"] for probe in instrument.PROBES]
    if report.get("probe_ids") != expected_ids:
        raise ValueError("probe order does not match frozen V3 inputs")


def derive_failure_profile(results: list[dict], expected: dict[str, int], expected_ids: list[str]) -> dict:
    """Apply the probe-level failure semantics without running candidate code."""
    if len(results) != len(expected_ids):
        raise ValueError("candidate response count differs from frozen probe count")
    fails: list[bool] = []
    rows: list[dict] = []
    output_overflow_count = 0
    timeout_count = 0
    exception_count = 0

    for index, (record, expected_id) in enumerate(zip(results, expected_ids)):
        if record.get("probe_id") != expected_id:
            raise ValueError(f"probe response order mismatch at index {index}")
        if record.get("phase") != "probe":
            raise ValueError(f"unexpected response phase at probe {index + 1}")
        if record.get("probe_index") != index + 1 or record.get("sequence") != index + 2:
            raise ValueError(f"response sequence mismatch at probe {index + 1}")
        if record.get("tree_empty") is not True or record.get("fatal"):
            raise ValueError(f"process cleanup not verified at probe {index + 1}")

        status = record.get("status")
        reason = None
        if status in CANDIDATE_INVALID_STATUSES:
            raise ValueError(f"candidate-invalid protocol status at probe {index + 1}: {status}")
        if status == "timeout":
            if record.get("timed_out") is not True:
                raise ValueError(f"timeout status is not backed by timeout evidence at probe {index + 1}")
            timeout_count += 1
            failed = True
            reason = "timeout"
        elif status == "exception":
            failed = True
            exception_count += 1
            reason = "runtime_exception"
        elif status == "output_overflow":
            if record.get("solver_output_overflow") is not True:
                raise ValueError(f"overflow status lacks bounded-output evidence at probe {index + 1}")
            failed = True
            output_overflow_count += 1
            reason = "output_overflow_v10_policy"
        elif status == "ok":
            if record.get("solver_output_overflow") is True:
                raise ValueError(f"success status contradicts output-overflow flag at probe {index + 1}")
            answer_type = record.get("answer_type")
            if answer_type not in KNOWN_OK_ANSWER_TYPES:
                raise ValueError(f"unknown answer type at probe {index + 1}")
            if answer_type == "int":
                answer = record.get("answer")
                if type(answer) is not int:
                    raise ValueError(f"integer answer type lacks an exact int at probe {index + 1}")
                failed = answer != expected[expected_id]
                reason = "wrong_answer" if failed else None
            else:
                # V3 marks bool, None, strings, floats, and other non-int returns
                # as probe failures. Oversized integers are necessarily wrong
                # for this frozen tiny-graph instrument.
                failed = True
                reason = "wrong_output_type"
        else:
            raise ValueError(f"unrecognized probe status at probe {index + 1}: {status}")

        fails.append(bool(failed))
        rows.append({
            "probe_index": index + 1,
            "probe_id": expected_id,
            "status": status,
            "failed": bool(failed),
            "failure_reason": reason,
        })

    family_counts = instrument.family_counts(fails)
    k, concentration = instrument.concentration(fails)
    return {
        "fails": fails,
        "family_counts": family_counts,
        "k": k,
        "C": concentration,
        "max_f": max(family_counts.values()) if family_counts else 0,
        "eligible": 2 <= k <= 24,
        "probe_count": len(fails),
        "timeout_count": timeout_count,
        "runtime_exception_count": exception_count,
        "output_overflow_count": output_overflow_count,
        "rows": rows,
        "output_overflow_policy": (
            "V10-specific: bounded stdout/stderr overflow counts as a failed probe; "
            "this differs from frozen V3's unbounded StringIO capture and requires "
            "an explicit V10 protocol amendment before candidate data collection."
        ),
    }


def score(report_path: Path, fixture_manifest_path: Path, body_path: Path) -> dict:
    """Validate and score only the fixed, hand-written smoke control."""
    report = json.loads(Path(report_path).read_text(encoding="utf-8"))
    manifest = json.loads(Path(fixture_manifest_path).read_text(encoding="utf-8"))
    freeze_info = verify_frozen_v3()

    if manifest.get("kind") != "fixed_harness_control":
        raise ValueError("this scorer is limited to the fixed harness-control fixture")
    if manifest.get("expected_answers_in_fixture") is not False:
        raise ValueError("fixture must not include expected answers")
    if manifest.get("model_generated") is not False:
        raise ValueError("this control cannot be model-generated")
    if manifest.get("candidate_generation_performed") is not False:
        raise ValueError("fixture manifest reports candidate generation")
    body = Path(body_path)
    if body.is_symlink() or not body.is_file():
        raise ValueError("control body must be a regular non-symlink file")
    if body.stat().st_size > 1_000_000:
        raise ValueError("control body exceeds the fixed-control byte limit")
    body_hash = sha256(body)
    if body_hash != manifest.get("body_sha256"):
        raise ValueError("actual control body hash does not match fixture manifest")
    if report.get("candidate_sha256") != body_hash:
        raise ValueError("executed body hash does not match the actual control body")
    validate_probe_binding(report, manifest)

    if report.get("probe_count") != 30 or report.get("expected_probe_count") != 30:
        raise ValueError("expected exactly 30 executed predictions")
    if len(report.get("results", [])) != 30:
        raise ValueError("expected exactly 30 prediction records")
    if report.get("isolation_harness_ok") is not True or report.get("all_trees_empty") is not True:
        raise ValueError("execution harness did not pass")
    if report.get("candidate_valid") is not True or report.get("candidate_status") != "valid":
        raise ValueError("fixed control was not classified as a valid candidate")
    if report.get("execution_performed") is not True:
        raise ValueError("fixed control was not executed")
    if report.get("static_checks_enforced") is not True:
        raise ValueError("the fixed-control report must use the frozen V3 static checks")
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
    preflight = report.get("preflight")
    if not isinstance(preflight, dict):
        raise ValueError("preflight record is missing")
    if (
        preflight.get("phase") != "preflight"
        or preflight.get("probe_id") != "__h3_preflight__"
        or preflight.get("sequence") != 1
        or preflight.get("status") != "ok"
        or preflight.get("answer_type") != "callable"
        or preflight.get("answer") is not None
        or preflight.get("solver_output_overflow") is True
    ):
        raise ValueError("fixed control module preflight did not pass its full schema")
    if preflight.get("tree_empty") is not True:
        raise ValueError("process cleanup was not verified after preflight")
    if not report.get("container_config", {}).get("verified"):
        raise ValueError("container configuration was not verified")
    if not all(report.get("container_config", {}).get("checks", {}).values()):
        raise ValueError("container configuration checks did not all pass")

    source = body.read_text(encoding="utf-8")
    if run_gate.unsafe_reason(source) is not None:
        raise ValueError("fixed control violates the frozen V3 static import/call policy")
    missing = run_gate.undefined_global_names(source)
    if missing:
        raise ValueError("fixed control contains undefined globals: " + ",".join(missing))

    expected = instrument.expected_values()
    expected_ids = [probe["probe_id"] for probe in instrument.PROBES]
    profile = derive_failure_profile(report["results"], expected, expected_ids)
    if profile["k"] != 0 or profile["C"] != 0.0 or profile["max_f"] != 0:
        raise ValueError("hand-written fixed control is not expected to pass every diagnostic probe")
    rows = profile["rows"]
    correct = sum(1 for row in rows if not row["failed"])
    if correct != 30:
        raise ValueError(f"fixed harness control only matched {correct}/30 trusted answers")

    return {
        "version": 1,
        "status": "PASS",
        "scope": "fixed, hand-written control on V3 probe inputs; not model-generated candidates",
        "probe_count": 30,
        "correct_control_predictions": correct,
        "k": profile["k"],
        "C": profile["C"],
        "max_f": profile["max_f"],
        "family_counts": profile["family_counts"],
        "eligible": profile["eligible"],
        "timeout_count": profile["timeout_count"],
        "runtime_exception_count": profile["runtime_exception_count"],
        "output_overflow_count": profile["output_overflow_count"],
        "output_overflow_policy": profile["output_overflow_policy"],
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
        "frozen_v3_contract": freeze_info,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True)
    parser.add_argument("--fixture-manifest", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    result = score(Path(args.report), Path(args.fixture_manifest), Path(args.body))
    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "probe_count": result["probe_count"],
        "correct_control_predictions": result["correct_control_predictions"],
        "k": result["k"],
        "C": result["C"],
        "eligible": result["eligible"],
        "H3_scientific_result": False,
        "report": str(output),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
