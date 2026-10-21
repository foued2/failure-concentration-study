"""Record and validate feasibility-pilot evidence; never execute solver source here."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from study.features import concentration, family_counts
from study.families import FAMILY_ORDER

VALID_STATUSES = {"pass", "wrong", "invalid", "error", "timeout", "not_run"}
FAIL_STATUSES = {"wrong", "invalid", "error", "timeout"}
EVALUATION_STATUSES = {"complete", "error", "timeout", "not_run"}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def input_id(instance: dict) -> str:
    value = {k: instance[k] for k in ("n", "edges", "s", "t")}
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def body_id(source: str) -> str:
    normalized = source.replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def attempt_id(order: int) -> str:
    if order < 1:
        raise ValueError("generation order must be positive")
    return f"attempt-{order:04d}"


def make_attempt_record(order: int, raw_output: str | None, provider_metadata: dict,
                        prompt_config_ref: str | None = None,
                        known_bodies: dict[str, str] | None = None) -> dict:
    """Represent every attempt, including failed/duplicate attempts, without selecting."""
    bid = body_id(raw_output) if raw_output is not None else None
    known_bodies = known_bodies or {}
    return {
        "attempt_id": attempt_id(order),
        "generation_order": order,
        "provider_metadata": provider_metadata,
        "prompt_config_ref": prompt_config_ref,
        "raw_output": raw_output,
        "body_id": bid,
        "duplicate_of_attempt_id": known_bodies.get(bid) if bid else None,
        "parsing_status": "not_assessed",
        "execution_status": "not_run",
        "failure_reason": None,
    }


def jsonl_text(records: list[dict]) -> str:
    """Serialize all supplied records in order; no filtering or deduplication."""
    return "".join(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n" for row in records)


def derive_features(probe_rows: list[dict]) -> dict:
    """Map complete probe records through the existing six-family definitions."""
    if len(probe_rows) != 30:
        raise ValueError("exactly 30 diagnostic probe rows are required")
    expected = [(family, variant) for family in FAMILY_ORDER for variant in range(5)]
    observed = [(r["family"], r["variant"]) for r in probe_rows]
    if observed != expected:
        raise ValueError("probe rows must be in the existing family-major order")
    for row in probe_rows:
        if row.get("status") not in VALID_STATUSES:
            raise ValueError(f"invalid probe status: {row.get('status')!r}")
        if row["status"] == "not_run":
            raise ValueError("incomplete probe battery cannot produce k or C")
    fails = [row["status"] in FAIL_STATUSES for row in probe_rows]
    counts = family_counts(fails)
    k, c = concentration(fails)
    if k != sum(counts.values()):
        raise AssertionError("feature arithmetic is inconsistent")
    return {"family_counts": counts, "k": k, "C": c, "eligible": k >= 2}


def check_input_separation(diagnostic_inputs: list[dict], evaluation_inputs: list[dict]) -> dict:
    diagnostic_ids = [input_id(x) for x in diagnostic_inputs]
    evaluation_ids = [input_id(x) for x in evaluation_inputs]
    duplicates = sorted({x for x in evaluation_ids if evaluation_ids.count(x) > 1})
    overlap = sorted(set(diagnostic_ids) & set(evaluation_ids))
    return {
        "diagnostic_count": len(diagnostic_ids),
        "evaluation_count": len(evaluation_ids),
        "diagnostic_duplicates": sorted({x for x in diagnostic_ids if diagnostic_ids.count(x) > 1}),
        "evaluation_duplicates": duplicates,
        "diagnostic_evaluation_overlap": overlap,
        "passed": not duplicates and not overlap and len(evaluation_ids) <= 100,
    }


def check_edge_fixtures(evaluation_records: list[dict]) -> dict:
    """Verify e0-e4 are present at most once and no other fixture IDs are duplicated."""
    fixture_ids = [r.get("hid") for r in evaluation_records if str(r.get("hid", "")).startswith("e")]
    expected = {f"e{i}" for i in range(5)}
    counts = {fixture: fixture_ids.count(fixture) for fixture in sorted(expected)}
    unknown = sorted(set(fixture_ids) - expected)
    duplicates = sorted({fixture for fixture in fixture_ids if fixture_ids.count(fixture) > 1})
    return {"counts": counts, "unknown_fixture_ids": unknown, "duplicates": duplicates,
            "all_expected_present": set(fixture_ids) == expected,
            "passed": all(n <= 1 for n in counts.values()) and not unknown and not duplicates}


def validate_trace(attempts: list[dict], diagnostic_rows: list[dict], evaluation_rows: list[dict]) -> list[str]:
    """Check references across retained row-level records; return all integrity errors."""
    errors: list[str] = []
    attempt_ids = [a.get("attempt_id") for a in attempts]
    if len(set(attempt_ids)) != len(attempt_ids):
        errors.append("duplicate attempt identifiers")
    attempt_body = {a.get("attempt_id"): a.get("body_id") for a in attempts}
    body_ids = {a.get("body_id") for a in attempts if a.get("body_id")}
    for row in diagnostic_rows:
        if row.get("body_id") not in body_ids:
            errors.append(f"diagnostic row has unknown body: {row.get('body_id')}")
        if row.get("attempt_id") not in attempt_body or attempt_body.get(row.get("attempt_id")) != row.get("body_id"):
            errors.append("diagnostic row attempt/body reference mismatch")
    for row in evaluation_rows:
        if row.get("body_id") not in body_ids:
            errors.append(f"evaluation row has unknown body: {row.get('body_id')}")
        if row.get("attempt_id") not in attempt_body or attempt_body.get(row.get("attempt_id")) != row.get("body_id"):
            errors.append("evaluation row attempt/body reference mismatch")
        if not row.get("input_id"):
            errors.append("evaluation row lacks input identity")
        if row.get("status") == "complete" and "solver_output" not in row:
            errors.append("completed evaluation row lacks solver output")
        if row.get("status") == "complete" and "oracle_output" not in row:
            errors.append("completed evaluation row lacks oracle output")
        if row.get("status") not in EVALUATION_STATUSES:
            errors.append(f"invalid evaluation status: {row.get('status')!r}")
        if row.get("status") == "complete" and not isinstance(row.get("correct"), bool):
            errors.append("completed evaluation row lacks boolean correctness")
    for row in diagnostic_rows:
        if row.get("status") not in VALID_STATUSES:
            errors.append(f"invalid diagnostic status: {row.get('status')!r}")
        if not row.get("probe_id") or not row.get("input_id"):
            errors.append("diagnostic row lacks probe or input identity")
    return errors


def validate_records(attempts: list[dict], diagnostic_rows: list[dict], evaluation_rows: list[dict],
                     feature_rows: list[dict], allowed_input_ids: set[str]) -> list[str]:
    """Validate required schema fields, references, uniqueness, and feature arithmetic."""
    errors = validate_trace(attempts, diagnostic_rows, evaluation_rows)
    required_attempt = {
        "attempt_id", "generation_order", "provider_metadata", "prompt_config_ref", "raw_output",
        "body_id", "duplicate_of_attempt_id", "parsing_status", "execution_status", "failure_reason",
    }
    for attempt in attempts:
        missing = required_attempt - attempt.keys()
        if missing:
            errors.append(f"attempt {attempt.get('attempt_id')} missing fields: {sorted(missing)}")
        if attempt.get("parsing_status") not in {"not_assessed", "parsed", "parse_failed"}:
            errors.append(f"attempt {attempt.get('attempt_id')} has invalid parse status")
        if attempt.get("execution_status") not in {"not_run", "executable", "execution_failed"}:
            errors.append(f"attempt {attempt.get('attempt_id')} has invalid execution status")

    required_diagnostic = {
        "attempt_id", "body_id", "probe_id", "family", "variant", "input_id", "status",
        "solver_output", "oracle_output", "error", "timeout_seconds",
    }
    for row in diagnostic_rows:
        missing = required_diagnostic - row.keys()
        if missing:
            errors.append(f"diagnostic row {row.get('probe_id')} missing fields: {sorted(missing)}")

    required_evaluation = {
        "attempt_id", "body_id", "input_id", "status", "solver_output", "oracle_output",
        "correct", "error", "timeout_seconds",
    }
    for row in evaluation_rows:
        missing = required_evaluation - row.keys()
        if missing:
            errors.append(f"evaluation row {row.get('input_id')} missing fields: {sorted(missing)}")

    seen_eval_pairs: set[tuple[str, str]] = set()
    for row in evaluation_rows:
        pair = (row.get("body_id"), row.get("input_id"))
        if pair in seen_eval_pairs:
            errors.append(f"duplicate body/input evaluation row: {pair}")
        seen_eval_pairs.add(pair)
        if row.get("input_id") not in allowed_input_ids:
            errors.append(f"evaluation row input is not in the frozen bank: {row.get('input_id')}")

    diagnostics_by_body: dict[str, list[dict]] = {}
    for row in diagnostic_rows:
        diagnostics_by_body.setdefault(row.get("body_id"), []).append(row)
    for bid, rows in diagnostics_by_body.items():
        if len(rows) != 30:
            errors.append(f"body {bid} has {len(rows)} diagnostic rows, expected 30")
        identities = [(r.get("family"), r.get("variant")) for r in rows]
        if len(set(identities)) != len(identities):
            errors.append(f"body {bid} has duplicate diagnostic probe identity")

    feature_by_body = {row.get("body_id"): row for row in feature_rows}
    for row in feature_rows:
        missing = {"attempt_id", "body_id", "family_counts", "k", "C", "eligible"} - row.keys()
        if missing:
            errors.append(f"feature row {row.get('body_id')} missing fields: {sorted(missing)}")
    for bid, rows in diagnostics_by_body.items():
        if len(rows) == 30 and bid in feature_by_body and all(r.get("status") != "not_run" for r in rows):
            try:
                computed = derive_features(sorted(rows, key=lambda r: (FAMILY_ORDER.index(r["family"]), r["variant"])))
                stored = feature_by_body[bid]
                if stored.get("k") != computed["k"] or stored.get("C") != computed["C"]:
                    errors.append(f"body {bid} feature values disagree with diagnostic rows")
                if stored.get("family_counts") != computed["family_counts"]:
                    errors.append(f"body {bid} family counts disagree with diagnostic rows")
            except (KeyError, ValueError, IndexError) as exc:
                errors.append(f"body {bid} feature validation failed: {exc}")
    return errors


def decision_summary(attempts: list[dict], feature_rows: list[dict], evaluation_rows: list[dict], integrity_passed: bool) -> dict:
    """Descriptive feasibility counts only; deliberately does not fit predictive models."""
    distinct_bodies = {a["body_id"] for a in attempts if a.get("body_id")}
    support: dict[int, dict[float, set[str]]] = {}
    for row in feature_rows:
        if row.get("eligible") and row.get("body_id"):
            support.setdefault(row["k"], {}).setdefault(row["C"], set()).add(row["body_id"])
    contrasts = [
        {"k": k, "C_body_counts": {c: len(bodies) for c, bodies in by_c.items()}}
        for k, by_c in sorted(support.items()) if len(by_c) > 1
    ]
    outcome_by_body: dict[str, list[bool]] = {}
    for row in evaluation_rows:
        if row.get("status") == "complete" and isinstance(row.get("correct"), bool):
            outcome_by_body.setdefault(row["body_id"], []).append(row["correct"])
    outcome_varies = False
    for k, by_c in support.items():
        if len(by_c) < 2:
            continue
        fractions = []
        for bodies in by_c.values():
            for bid in bodies:
                values = outcome_by_body.get(bid, [])
                if values:
                    fractions.append(sum(values) / len(values))
        if len(set(fractions)) > 1:
            outcome_varies = True
            break
    qualifying = any(all(n >= 2 for n in c["C_body_counts"].values()) for c in contrasts)
    return {
        "generation_attempts": len(attempts),
        "distinct_canonical_bodies": len(distinct_bodies),
        "fixed_k_contrasts": contrasts,
        "correctness_varies_in_fixed_k_contrast": outcome_varies,
        "integrity_passed": integrity_passed,
        "feasibility_demonstrated": bool(qualifying and outcome_varies and integrity_passed),
        "predictive_effect_tested": False,
    }
