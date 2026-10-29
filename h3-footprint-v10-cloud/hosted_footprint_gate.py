"""Run the frozen V3 footprint gate through the V10 isolated Docker executor.

This adapter never generates candidates and never executes candidate source on
the host. V3 supplies the exact static checks, failure-profile semantics,
support-cell logic, saturation rule, and futility rule. V10 supplies the
isolated preflight/probe execution and a separate trusted scoring function.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
V3_DIR = ROOT / "h3-footprint-v3"
if str(V3_DIR) not in sys.path:
    sys.path.insert(0, str(V3_DIR))

import generation_plan_draft
import run_container_candidate as executor
import score_smoke_report

V3_GATE = score_smoke_report.run_gate
PROBES = score_smoke_report.canonical_probe_payloads()
EXPECTED = score_smoke_report.instrument.expected_values()
EXPECTED_IDS = [probe["probe_id"] for probe in score_smoke_report.instrument.PROBES]
V3_GATE_TAG = generation_plan_draft.V3_FROZEN_TAG
V3_GENERATOR_SHA256 = generation_plan_draft.V3_GENERATOR_SOURCE_SHA256


class HostedGateError(RuntimeError):
    """Execution or provenance failure that must not be assigned a candidate k."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_body_hash(source: str) -> str:
    return generation_plan_draft._V3.digest(source)


def _candidate_hash_from_record(item: Any) -> str | None:
    if isinstance(item, str):
        return item
    if not isinstance(item, dict):
        return None
    first = item.get("body_hash")
    second = item.get("body_sha256")
    if first is not None and second is not None and first != second:
        raise HostedGateError("conflicting body_hash and body_sha256 in candidate provenance")
    value = first if first is not None else second
    return value if isinstance(value, str) else None


def normalize_attempts(source_path: Path, destination_path: Path) -> dict:
    """Normalize V10/V3 attempt metadata to the frozen V3 body_meta() schema."""
    source_path = Path(source_path)
    destination_path = Path(destination_path)
    if not source_path.is_file() or source_path.is_symlink():
        raise HostedGateError("attempts metadata must be a regular non-symlink file")

    records = []
    seen: set[int] = set()
    for line_no, line in enumerate(source_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            raise HostedGateError(f"invalid attempts JSON at line {line_no}") from None
        if not isinstance(record, dict):
            raise HostedGateError(f"attempts row at line {line_no} is not an object")
        batch_id = record.get("batch_id")
        if type(batch_id) is not int or not 0 <= batch_id < 400:
            raise HostedGateError(f"invalid batch_id at attempts line {line_no}")
        if batch_id in seen:
            raise HostedGateError(f"duplicate attempt record for batch {batch_id}")
        seen.add(batch_id)

        candidates = record.get("candidate_records")
        if candidates is None:
            candidates = record.get("body_hashes_in_response_order")
        if candidates is None:
            candidates = record.get("body_hashes", [])
        if not isinstance(candidates, list):
            raise HostedGateError(f"candidate record list malformed at attempts line {line_no}")
        normalized_candidates = []
        for item in candidates:
            body_hash = _candidate_hash_from_record(item)
            if body_hash is None or len(body_hash) != 64 or any(c not in "0123456789abcdef" for c in body_hash.lower()):
                raise HostedGateError(f"invalid candidate hash at attempts line {line_no}")
            normalized_candidates.append({"body_hash": body_hash.lower()})

        model = record.get("model") or record.get("original_route_alias")
        variant = record.get("prompt_variant")
        if not isinstance(model, str) or not model:
            raise HostedGateError(f"missing generator/model provenance for batch {batch_id}")
        if variant not in {"direct", "menu", "simple"}:
            raise HostedGateError(f"missing or invalid prompt variant for batch {batch_id}")

        records.append({
            "batch_id": batch_id,
            "model": model,
            "prompt_variant": variant,
            "requested": record.get("requested", record.get("requested_bodies", 8)),
            "extracted": record.get("extracted", record.get("extracted_bodies", len(normalized_candidates))),
            "returncode": record.get("returncode", record.get("http_status")),
            "error": record.get("error") or record.get("error_category"),
            "candidate_records": normalized_candidates,
            "body_hashes": [item["body_hash"] for item in normalized_candidates],
        })

    if not records:
        raise HostedGateError("no completed generation attempts were supplied")
    records.sort(key=lambda x: x["batch_id"])
    batch_ids = [row["batch_id"] for row in records]
    if batch_ids != list(range(len(batch_ids))):
        raise HostedGateError("generation attempts must contain a complete zero-based batch prefix")
    # The V3 futility rule is evaluated at 100/200/300 only once each prefix
    # is complete. The V10 controller must not infer a checkpoint from a
    # scattered set of 100 records.
    for checkpoint in (100, 200, 300):
        if len(records) >= checkpoint and batch_ids[:checkpoint] != list(range(checkpoint)):
            raise HostedGateError(f"generation prefix incomplete at futility checkpoint {checkpoint}")

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(
        "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in records),
        encoding="utf-8",
        newline="\n",
    )
    return {
        "attempt_count": len(records),
        "complete_batch_prefix": len(records),
        "attempts_sha256": sha256_bytes(destination_path.read_bytes()),
        "batches": batch_ids,
    }


def _invalid_candidate(row: dict, reason: str) -> dict:
    return V3_GATE._invalid_candidate(row, reason)


def evaluate_body_hosted(
    body_path: Path,
    meta: dict[str, dict],
    *,
    trusted_dir: Path,
    report_dir: Path,
    expected: dict[str, int] | None = None,
) -> dict:
    """Evaluate one body only in the isolated executor; derive no k on invalid input."""
    body_path = Path(body_path)
    if body_path.is_symlink() or not body_path.is_file() or body_path.suffix != ".py":
        raise HostedGateError("candidate path must be a regular .py file")
    source_bytes = body_path.read_bytes()
    try:
        source = source_bytes.decode("utf-8")
    except UnicodeDecodeError:
        source = ""
        decode_error = True
    else:
        decode_error = False

    body_hash = body_path.stem
    info = meta.get(body_hash) or {}
    row = {
        "body_hash": body_hash,
        "base_algorithm": V3_GATE.base_label(source),
        "source_chars": len(source),
        "excluded": None,
        "timeout": False,
        "fails": None,
        "k": None,
        "C": None,
        "group_id": info.get("group_id"),
        "generator": info.get("model"),
        "prompt_variant": info.get("prompt_variant"),
        "batch_id": info.get("batch_id"),
        "execution_runtime": "V10 pinned Docker container",
    }

    if decode_error:
        return _invalid_candidate(row, "encoding:invalid_utf8")
    if canonical_body_hash(source) != body_hash:
        return _invalid_candidate(row, "body_hash_mismatch")
    if sha256_bytes(source_bytes) == "":
        raise HostedGateError("unreachable SHA-256 calculation failure")
    static_reason = V3_GATE.unsafe_reason(source)
    if static_reason:
        return _invalid_candidate(row, static_reason)
    missing = V3_GATE.undefined_global_names(source)
    if missing:
        return _invalid_candidate(row, "undefined_name:" + ",".join(missing))
    if not isinstance(row["group_id"], str) or not row["group_id"]:
        return _invalid_candidate(row, "missing_provenance")
    if type(row["batch_id"]) is not int or not 0 <= row["batch_id"] < 400:
        return _invalid_candidate(row, "missing_or_invalid_batch_id")

    out_dir = Path(report_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / f"{body_hash}.json"
    try:
        report = executor.run_candidate(
            body_path,
            Path(trusted_dir),
            PROBES,
            enforce_static=False,
        )
    except Exception as exc:
        # A Docker failure is infrastructure failure, not a solver failure.
        raise HostedGateError(f"isolated execution failed for {body_hash}: {type(exc).__name__}") from None

    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report.get("candidate_sha256") != sha256_bytes(source_bytes):
        raise HostedGateError(f"body hash changed across isolated execution for {body_hash}")
    if report.get("probe_payload_sha256") != score_smoke_report.canonical_probe_payload_sha256():
        raise HostedGateError(f"probe payload hash mismatch for {body_hash}")
    if report.get("probe_ids") != EXPECTED_IDS or report.get("expected_probe_count") != 30:
        raise HostedGateError(f"probe sequence mismatch for {body_hash}")
    if report.get("isolation_harness_ok") is not True:
        raise HostedGateError(f"isolation harness did not pass for {body_hash}")
    if report.get("all_trees_empty") is not True:
        raise HostedGateError(f"process tree cleanup not verified for {body_hash}")
    if report.get("reference_answers_present") is not False or report.get("api_keys_passed_to_container") is not False:
        raise HostedGateError(f"candidate container isolation disclosure failed for {body_hash}")
    checks = (report.get("container_config") or {}).get("checks") or {}
    if not checks or not all(value is True for value in checks.values()):
        raise HostedGateError(f"container configuration checks did not all pass for {body_hash}")

    if report.get("candidate_valid") is not True:
        candidate_status = str(report.get("candidate_status") or "invalid_candidate")
        reason = report.get("candidate_exclusion_reason")
        return _invalid_candidate(row, f"hosted_{candidate_status}" + (f":{reason}" if reason else ""))

    profile = score_smoke_report.derive_failure_profile(
        report["results"],
        expected if expected is not None else EXPECTED,
        EXPECTED_IDS,
    )
    row.update({
        "excluded": None,
        "load_error": None,
        "fails": profile["fails"],
        "family_counts": profile["family_counts"],
        "k": profile["k"],
        "C": profile["C"],
        "max_f": profile["max_f"],
        "eligible": profile["eligible"],
        "probes_completed": profile["probe_count"],
        "timeout": profile["timeout_count"] > 0,
        "runtime_exception_count": profile["runtime_exception_count"],
        "output_overflow_count": profile["output_overflow_count"],
    })
    return row


def build_hosted_report(
    body_dir: Path,
    attempts_path: Path,
    trusted_dir: Path,
    output_dir: Path,
) -> dict:
    """Run V3's frozen aggregation/verdict logic over V10-isolated probe profiles."""
    score_smoke_report.verify_frozen_v3()
    if generation_plan_draft.V3_GENERATOR_SOURCE_SHA256 != "ff5b638455f16a3033168b02929e4d7bb63b72a5b486b72930b119b69b3e3456":
        raise HostedGateError("frozen V3 generator hash changed")

    body_dir = Path(body_dir).resolve(strict=True)
    attempts_path = Path(attempts_path).resolve(strict=True)
    output_dir = Path(output_dir).resolve()
    trusted_dir = Path(trusted_dir).resolve(strict=True)
    if not body_dir.is_dir() or body_dir.is_symlink():
        raise HostedGateError("body_dir must be a directory")
    if not attempts_path.is_file() or attempts_path.is_symlink():
        raise HostedGateError("attempts_path must be a regular file")
    if body_dir == ROOT or body_dir == V3_DIR or body_dir in V3_DIR.parents:
        raise HostedGateError("candidate body directory must be outside the trusted source tree")

    workspace = output_dir / "gate-workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    normalized_attempts = workspace / "attempts.jsonl"
    attempt_summary = normalize_attempts(attempts_path, normalized_attempts)

    gate = V3_GATE
    old_gen, old_bodies, old_results = gate.GEN, gate.BODIES, gate.RESULTS
    old_eval = gate.evaluate_body
    try:
        gate.GEN = workspace
        gate.BODIES = body_dir
        gate.RESULTS = output_dir

        def evaluator(path: Path, meta: dict[str, dict]) -> dict:
            return evaluate_body_hosted(
                path, meta,
                trusted_dir=trusted_dir,
                report_dir=output_dir / "runner-reports",
                expected=EXPECTED,
            )

        gate.evaluate_body = evaluator
        report = gate.build()
    finally:
        gate.GEN, gate.BODIES, gate.RESULTS = old_gen, old_bodies, old_results
        gate.evaluate_body = old_eval

    summary = {
        "status": "PASS" if report["verdict"] in {"PASS", "WEAK", "FAIL"} else "ERROR",
        "protocol_status": "V10_DRAFT_NOT_FROZEN",
        "verdict": report["verdict"],
        "reason": report["reason"],
        "candidate_bodies": report["candidate_bodies"],
        "valid_bodies": report["valid_bodies"],
        "invalid_candidates": report["invalid_candidates"],
        "eligible_bodies": report["eligible_bodies"],
        "eligible_groups": report["eligible_groups"],
        "supported_cell_count": report["supported_cell_count"],
        "distinct_supported_k": report["distinct_supported_k"],
        "unique_groups_in_supported_cells": report["unique_groups_in_supported_cells"],
        "saturation_rate_eligible": report["saturation_rate_eligible"],
        "saturation_max": report["saturation_max"],
        "futility": report["futility"],
        "attempts": attempt_summary,
        "v3_freeze_tag": V3_GATE_TAG,
        "v3_generator_sha256": V3_GENERATOR_SHA256,
        "v10_execution_runtime": "GitHub-hosted Ubuntu plus pinned Docker image",
        "candidate_generation_performed_by_this_gate": False,
        "model_calls_performed_by_this_gate": 0,
        "held_out_work_performed": False,
        "h3_scientific_result": False,
        "candidate_evaluation_performed": True,
        "candidate_sources_executed_on_host": False,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "footprint.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown = gate.markdown(report).rstrip()
    markdown += (
        "\n\n## V10 execution amendment\n\n"
        "- Candidate bodies were executed only by the V10 isolated-container executor; no candidate source was imported or called on the host.\n"
        "- Output overflow over the bounded stdout/stderr capture is counted as a failed probe under the draft V10 rule.\n"
        "- This run is footprint feasibility only. V10 remains DRAFT_NOT_FROZEN; this report is not an H3 scientific result.\n"
    )
    (output_dir / "REPORT.md").write_text(markdown + "\n", encoding="utf-8")
    (output_dir / "V10_EXECUTION_MANIFEST.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--body-dir", required=True)
    parser.add_argument("--attempts", required=True)
    parser.add_argument("--trusted-dir", default=str(Path(__file__).resolve().parent))
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()
    try:
        report = build_hosted_report(
            Path(args.body_dir), Path(args.attempts), Path(args.trusted_dir), Path(args.out_dir)
        )
    except (HostedGateError, ValueError, OSError) as exc:
        print(json.dumps({"status": "ERROR", "error_type": type(exc).__name__, "error": str(exc)}, sort_keys=True))
        return 2
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
