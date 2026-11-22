"""B1 v1.7 census intake validator — v0.2 successor.

SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED

Validates the per-variant diagnostic_record_results structure of a B1 v1.7
outcome-blind census manifest. The individual terminal records are the source of
truth; supplied aggregate f/u/p vectors are non-authoritative consistency checks.
No bank access, no solvers, no diagnostics, no census decision, no outcomes.

Standard library only. See README.md for the scope and the reviewed correction brief.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

TOOL_NAME = "b1-census-intake"
TOOL_VERSION = "0.2"
SCHEMA_VERSION = "0.6-draft"
INTAKE_LABEL = "SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED"

STRATA = tuple(f"D{j}" for j in range(1, 9))
RECORDS_PER_STRATUM = 8
EXPECTED_RESULTS = 64
MEASUREMENT_BASIS = "record_level_64"
TERMINAL_STATUSES = ("DEFINITE_PASS", "DEFINITE_FAILURE", "UNRESOLVED")

VALIDITY_STATUSES = (
    "VALID",
    "INVALID",
    "EXCLUDED_BEFORE_DIAGNOSTICS",
    "INCOMPLETE",
    "EXPECTED_NOT_RUN",
)
DECISION_BASIS = {
    "INVALID": "PREDIAGNOSTIC_OBJECTIVE_INVALIDITY",
    "EXCLUDED_BEFORE_DIAGNOSTICS": "PREDIAGNOSTIC_DESIGN_EXCLUSION",
    "INCOMPLETE": "POSTRUN_COMPLETENESS_AUDIT",
    "EXPECTED_NOT_RUN": "EXPECTED_NOT_RUN_INVENTORY_AUDIT",
}
ZERO_RESULT_STATUSES = ("INVALID", "EXCLUDED_BEFORE_DIAGNOSTICS", "EXPECTED_NOT_RUN")

VARIANT_REQUIRED = (
    "variant_id",
    "parent_id",
    "Z_id",
    "q_id",
    "validity_status",
    "diagnostic_record_results",
)
VARIANT_ALLOWED = frozenset(VARIANT_REQUIRED) | frozenset(
    {
        "semantic_source_digest",
        "runnable_artifact_digest",
        "status_reason",
        "status_decision",
        "diagnostic_evidence_ref",
        "f",
        "u",
        "p",
    }
)
AGGREGATES = ("f", "u", "p")
DIGEST_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _nonempty_str(value: object) -> bool:
    return isinstance(value, str) and bool(value)


def _status_decision_ok(variant: dict, status: str) -> bool:
    sd = variant.get("status_decision")
    if not isinstance(sd, dict):
        return False
    if sd.get("decision_basis") != DECISION_BASIS[status]:
        return False
    consulted = sd.get("record_presence_identity_metadata_consulted")
    if not isinstance(consulted, bool):
        return False
    if status == "INCOMPLETE":
        return consulted is True
    return consulted is False


def _vector_ok(value: object) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 8
        and all(_is_int(v) and v >= 0 for v in value)
    )


def _empty_counts() -> list[int]:
    return [0] * 8


def _derive_from_results(results: list[dict]) -> tuple[list[int], list[int], list[int]]:
    f = [0] * 8
    u = [0] * 8
    p = [0] * 8
    for result in results:
        stratum = STRATA.index(result["stratum_id"])
        status = result["terminal_status"]
        if status == "DEFINITE_FAILURE":
            f[stratum] += 1
        elif status == "UNRESOLVED":
            u[stratum] += 1
        else:
            p[stratum] += 1
    return f, u, p


def validate_variant(
    variant: object,
    index: int,
    parent_ids: set[str],
    parent_z: dict[str, str],
    seen_variant_ids: set[str],
) -> tuple[dict, set[str] | None]:
    """Return (entry, id_set_for_valid_complete_variant_or_None)."""

    entry: dict = {
        "index": index,
        "variant_id": None,
        "validity_status": None,
        "decision": "REJECTED",
        "reason_codes": [],
        "aggregate_check": None,
    }
    codes: list[str] = []
    id_set_for_consistency: set[str] | None = None

    try:
        if not isinstance(variant, dict):
            codes.append("VARIANT_NOT_OBJECT")
            entry["reason_codes"] = codes
            return entry, None

        vid = variant.get("variant_id")
        if _nonempty_str(vid):
            entry["variant_id"] = vid
        status = variant.get("validity_status")
        entry["validity_status"] = status if isinstance(status, str) else None

        unknown = sorted(k for k in variant if k not in VARIANT_ALLOWED)
        if unknown:
            codes.append("UNKNOWN_VARIANT_FIELD")
        missing = [k for k in VARIANT_REQUIRED if k not in variant]
        if missing:
            codes.append("MISSING_VARIANT_FIELD")
            entry["reason_codes"] = sorted(set(codes))
            return entry, None

        for field in ("variant_id", "parent_id", "Z_id", "q_id"):
            if not _nonempty_str(variant[field]):
                codes.append("EMPTY_IDENTIFIER")
                break

        if _nonempty_str(vid):
            if vid in seen_variant_ids:
                codes.append("DUPLICATE_VARIANT_ID")
            seen_variant_ids.add(vid)

        if not isinstance(status, str) or status not in VALIDITY_STATUSES:
            codes.append("INVALID_VALIDITY_STATUS")
            entry["reason_codes"] = sorted(set(codes))
            return entry, None

        if variant["parent_id"] not in parent_ids:
            codes.append("UNKNOWN_PARENT_ID")
        elif parent_z.get(variant["parent_id"]) != variant["Z_id"]:
            codes.append("PARENT_Z_MISMATCH")

        results = variant["diagnostic_record_results"]
        if not isinstance(results, list):
            codes.append("RESULTS_NOT_ARRAY")
            entry["reason_codes"] = sorted(set(codes))
            return entry, None
        if len(results) > EXPECTED_RESULTS:
            codes.append("TOO_MANY_RESULTS")

        if status == "VALID":
            if len(results) != EXPECTED_RESULTS:
                codes.append("VALID_RESULT_COUNT")
            for field in (
                "diagnostic_evidence_ref",
                "semantic_source_digest",
                "runnable_artifact_digest",
            ):
                if field not in variant:
                    codes.append("MISSING_VALID_FIELD")
                    break
            for digest_field in ("semantic_source_digest", "runnable_artifact_digest"):
                value = variant.get(digest_field)
                if value is not None and not (
                    isinstance(value, str) and DIGEST_RE.fullmatch(value)
                ):
                    codes.append("INVALID_DIGEST_FORMAT")
                    break
        else:
            if "status_reason" not in variant or not _nonempty_str(variant.get("status_reason")):
                codes.append("MISSING_STATUS_REASON")
            if status == "INCOMPLETE":
                if len(results) > 63:
                    codes.append("INCOMPLETE_RESULT_COUNT")
                if "diagnostic_evidence_ref" not in variant:
                    codes.append("MISSING_DIAGNOSTIC_EVIDENCE_REF")
            elif results:
                codes.append("NONZERO_RESULTS_FOR_STATUS")
            if not _status_decision_ok(variant, status):
                codes.append("INVALID_STATUS_DECISION")

        id_set: set[str] = set()
        for result in results:
            if not isinstance(result, dict):
                codes.append("RESULT_NOT_OBJECT")
                continue
            rid = result.get("diagnostic_record_id")
            stratum = result.get("stratum_id")
            terminal = result.get("terminal_status")
            if not _nonempty_str(rid):
                codes.append("INVALID_RECORD_ID")
            elif rid in id_set:
                codes.append("DUPLICATE_RECORD_ID")
            else:
                id_set.add(rid)
            if stratum not in STRATA:
                codes.append("INVALID_STRATUM_ID")
            if terminal not in TERMINAL_STATUSES:
                codes.append("INVALID_TERMINAL_STATUS")

        if status == "VALID":
            counts = [0] * 8
            for result in results:
                if isinstance(result, dict) and result.get("stratum_id") in STRATA:
                    counts[STRATA.index(result["stratum_id"])] += 1
            if any(c != RECORDS_PER_STRATUM for c in counts):
                codes.append("STRATUM_RESULT_COUNT")

        derived_f, derived_u, derived_p = (
            _derive_from_results(results)
            if all(
                isinstance(r, dict)
                and r.get("stratum_id") in STRATA
                and r.get("terminal_status") in TERMINAL_STATUSES
                for r in results
            )
            else (_empty_counts(), _empty_counts(), _empty_counts())
        )

        aggregate_status = "absent"
        for name, derived in zip(AGGREGATES, (derived_f, derived_u, derived_p)):
            if name not in variant:
                continue
            supplied = variant[name]
            if not _vector_ok(supplied):
                codes.append("MALFORMED_AGGREGATE")
                aggregate_status = "malformed"
                break
            if supplied != derived:
                codes.append("AGGREGATE_MISMATCH")
                aggregate_status = "mismatch"
                break
            aggregate_status = "consistent"
        entry["aggregate_check"] = aggregate_status

        id_set_for_consistency = id_set if status == "VALID" and len(results) == EXPECTED_RESULTS else None

        if not codes:
            k_fail = sum(derived_f)
            k_unresolved = sum(derived_u)
            entry["derived"] = {
                "f": derived_f,
                "u": derived_u,
                "p": derived_p,
                "k_fail": k_fail,
                "k_unresolved": k_unresolved,
                "cell": [variant["q_id"], variant["Z_id"], k_fail, k_unresolved],
            }
            if status != "VALID":
                entry["derived"]["c_d_status"] = "NOT_APPLICABLE"
            elif k_fail == 0:
                entry["derived"]["c_d"] = "NO OBSERVED FAILURES"
                entry["derived"]["c_d_status"] = "NO OBSERVED FAILURES"
            else:
                ratio = str(Fraction(max(derived_f), k_fail))
                entry["derived"]["c_d"] = ratio
                entry["derived"]["c_d_numeric"] = ratio
                entry["derived"]["c_d_status"] = "DEFINED"
            entry["decision"] = "ADMITTED"

    except Exception:
        # No uncaught exception may escape on malformed input.
        codes.append("VALIDATION_EXCEPTION")

    entry["reason_codes"] = sorted(set(codes))
    if codes:
        entry["decision"] = "REJECTED"
        entry.pop("derived", None)
    return entry, id_set_for_consistency if not codes else None


def validate_census_manifest(data: object, manifest_sha256: str | None = None) -> dict:
    """Validate the full B1 v1.7 outcome-blind census manifest object."""

    if not isinstance(data, dict):
        if isinstance(data, list) and not data:
            return {
                "intake_label": INTAKE_LABEL,
                "tool": TOOL_NAME,
                "tool_version": TOOL_VERSION,
                "schema_version": SCHEMA_VERSION,
                "manifest_sha256": manifest_sha256,
                "count": 0,
                "admitted": 0,
                "rejected": 0,
                "manifest_reason_codes": ["EMPTY_MANIFEST"],
                "records": [],
            }
        raise ValueError("manifest root must be a JSON object")

    codes: list[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        codes.append("UNSUPPORTED_SCHEMA_VERSION")
    if data.get("study_id") != "LC518":
        codes.append("INVALID_STUDY_ID")

    basis = data.get("measurement_basis")
    if not isinstance(basis, str):
        codes.append("NON_STRING_EXPOSURE_BASIS")
    elif basis != MEASUREMENT_BASIS:
        codes.append("UNSUPPORTED_EXPOSURE_BASIS")

    bank = data.get("diagnostic_bank")
    if not isinstance(bank, dict):
        codes.append("INVALID_DIAGNOSTIC_BANK")
    else:
        if bank.get("stratum_ids") != list(STRATA):
            codes.append("INVALID_STRATUM_IDS")
        if bank.get("records_per_stratum") != RECORDS_PER_STRATUM:
            codes.append("INVALID_RECORDS_PER_STRATUM")
        if bank.get("total_records") != EXPECTED_RESULTS:
            codes.append("INVALID_TOTAL_RECORDS")

    assertion = data.get("outcome_exclusion_assertion")
    if not isinstance(assertion, dict) or any(
        assertion.get(k) is not False
        for k in (
            "correctness_outcomes_included",
            "outcomes_consulted",
            "model_outputs_included",
        )
    ):
        codes.append("OUTCOME_EXCLUSION_ASSERTION_FAILED")

    roster = data.get("parent_roster")
    parent_ids: set[str] = set()
    parent_z: dict[str, str] = {}
    if not isinstance(roster, list) or not roster:
        codes.append("INVALID_PARENT_ROSTER")
    else:
        for parent in roster:
            if not isinstance(parent, dict):
                codes.append("INVALID_PARENT_ENTRY")
                continue
            pid, zid = parent.get("parent_id"), parent.get("Z_id")
            if not _nonempty_str(pid) or not _nonempty_str(zid):
                codes.append("INVALID_PARENT_ENTRY")
            elif pid in parent_ids:
                codes.append("DUPLICATE_PARENT_ID")
            else:
                parent_ids.add(pid)
                parent_z[pid] = zid

    variants = data.get("variants")
    if not isinstance(variants, list):
        codes.append("VARIANTS_NOT_ARRAY")
        variants = []
    elif not variants:
        codes.append("EMPTY_VARIANT_LIST")

    entries = []
    id_sets: list[tuple[int, set[str]]] = []
    seen_variant_ids: set[str] = set()
    for index, variant in enumerate(variants):
        entry, id_set = validate_variant(
            variant, index, parent_ids, parent_z, seen_variant_ids
        )
        entries.append(entry)
        if id_set is not None:
            id_sets.append((index, id_set))

    if id_sets:
        reference_index, reference_set = id_sets[0]
        for index, id_set in id_sets[1:]:
            if id_set != reference_set:
                codes.append("CROSS_VARIANT_ID_SET_MISMATCH")
                for entry in entries:
                    if entry["index"] in (index, reference_index):
                        entry.setdefault("reason_codes", []).append(
                            "CROSS_VARIANT_ID_SET_MISMATCH"
                        )
                        entry["reason_codes"] = sorted(set(entry["reason_codes"]))
                        entry["decision"] = "REJECTED"
                        entry.pop("derived", None)

    for entry in entries:
        for code in set(codes):
            entry.setdefault("manifest_reason_codes", []).append(code)
        entry["manifest_reason_codes"] = sorted(set(entry.get("manifest_reason_codes", [])))
        if entry["manifest_reason_codes"]:
            entry["decision"] = "REJECTED"
            entry.pop("derived", None)

    admitted = sum(1 for e in entries if e["decision"] == "ADMITTED")
    report = {
        "intake_label": INTAKE_LABEL,
        "tool": TOOL_NAME,
        "tool_version": TOOL_VERSION,
        "schema_version": SCHEMA_VERSION,
        "manifest_sha256": manifest_sha256,
        "scope": "syntactic intake only; no bank membership, provenance, census decision or outcomes",
        "count": len(entries),
        "admitted": admitted,
        "rejected": len(entries) - admitted,
        "manifest_reason_codes": sorted(set(codes)),
        "records": entries,
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=INTAKE_LABEL)
    parser.add_argument("--manifest", required=True, help="path to a B1 v1.7 census manifest JSON object")
    parser.add_argument("--report", help="write report JSON here (default: stdout)")
    args = parser.parse_args(argv)

    try:
        raw = Path(args.manifest).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw.decode("utf-8"))
        report = validate_census_manifest(data, digest)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"INTAKE_INPUT_ERROR: {exc}", file=sys.stderr)
        return 3

    text = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0 if report["rejected"] == 0 and not report["manifest_reason_codes"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
