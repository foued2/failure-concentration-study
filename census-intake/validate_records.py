"""LC518 B1 v1.7 census-manifest structural and local-semantic intake checks.

SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED

This tool validates against the exact reviewed B1 v1.7 manifest schema draft 0.6
and applies only manifest-local semantic checks that do not require external files.
It does not establish full census admissibility, bank membership, source provenance,
run-ledger reconciliation, registry membership, or scientific support.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

TOOL_NAME = "lc518-b1-census-intake"
TOOL_VERSION = "0.3.0"
INTAKE_LABEL = "SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED"

SCHEMA_FILENAME = "B1_V1_7_CENSUS_MANIFEST_SCHEMA_DRAFT_0_6.json"
SCHEMA_ID = "urn:lc518:b1-v1.7:census-manifest:0.6-draft"
SCHEMA_SOURCE_COMMIT = "f19e2a0ba09f2161f290558da5f61abc9d3ab52a"
SCHEMA_SOURCE_PATH = (
    "reviews/analytical-validity-2026-11-18/"
    "b1-v17-census-review-2026-11-22/"
    "B1_V1_7_CENSUS_MANIFEST_SCHEMA_DRAFT_0_6.json"
)
SCHEMA_SOURCE_BLOB_SHA1 = "0f2865e606fa61400184c09abd01601497637a6b"

MEASUREMENT_SPEC_COMMIT = "ccd95e4c125d081abca95153f9af9c9a28d65b9a"
MEASUREMENT_SPEC_PATH = "reviews/analytical-validity-2026-11-18/CD_MEASUREMENT_SPEC_2026-11-19.md"
MEASUREMENT_SPEC_BLOB_SHA1 = "923655f20337b99f11e400f3428d1d18ac34c96d"
MEASUREMENT_FORMULA_CITATION = (
    "C_D measurement specification and exposure register (2026-11-19), §1, "
    "which quotes LC518 Rev 11 lines 216–221; see also §5."
)
SIDECAR_SCHEMA_BLOB_SHA1 = "72fc746c3d6129534aeb2fdbcd866842865f98c7"

MEASUREMENT_ZERO_CITATION = (
    "C_D measurement specification and exposure register (2026-11-19), §§1 and 4; "
    "Rev 11 convention is C_D=0 when k_fail=0, labelled NO OBSERVED FAILURES. "
    "The intake report emits the label as a categorical display state, not a numeric predictor."
)

STRATA = tuple(f"D{i}" for i in range(1, 9))
TERMINAL_STATUSES = frozenset({"DEFINITE_PASS", "DEFINITE_FAILURE", "UNRESOLVED"})
VALIDITY_STATUSES = frozenset({
    "VALID", "INVALID", "EXCLUDED_BEFORE_DIAGNOSTICS", "INCOMPLETE", "EXPECTED_NOT_RUN"
})
DECISION_BASIS = {
    "INVALID": "PREDIAGNOSTIC_OBJECTIVE_INVALIDITY",
    "EXCLUDED_BEFORE_DIAGNOSTICS": "PREDIAGNOSTIC_DESIGN_EXCLUSION",
    "INCOMPLETE": "POSTRUN_COMPLETENESS_AUDIT",
    "EXPECTED_NOT_RUN": "EXPECTED_NOT_RUN_INVENTORY_AUDIT",
}

EXTERNAL_CHECKS_NOT_PERFORMED = [
    "diagnostic record IDs and stratum assignments against the frozen bank record manifest",
    "bank hash/source-artifact identity against the referenced bank artifact",
    "exact one-to-one variant coverage against the referenced frozen variant inventory",
    "q_id membership against the referenced q registry",
    "Z_id membership against the referenced family map",
    "per-variant execution-state rows, start times, and status reconciliation in the referenced run-start ledger",
    "cross-file identity consistency among referenced roster, registry, inventory, bank, build, and run artifacts",
    "historical exposure evidence and future bank-generation protocol contents",
    "external evidence retrieval, source provenance, or artifact integrity",
]


def _git_blob_sha1(raw: bytes) -> str:
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def _parse_utc(value: str) -> datetime:
    # JSON Schema FormatChecker validates RFC3339 syntax; normalize trailing Z for Python.
    return datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)


def _schema_path() -> Path:
    return Path(__file__).resolve().parent / SCHEMA_FILENAME


def load_and_verify_schema(schema_path: Path | None = None) -> dict:
    path = schema_path or _schema_path()
    raw = path.read_bytes()
    actual_blob = _git_blob_sha1(raw)
    if actual_blob != SCHEMA_SOURCE_BLOB_SHA1:
        raise RuntimeError(
            "PACKAGED_B1_SCHEMA_IDENTITY_MISMATCH: packaged schema bytes do not match "
            f"the reviewed source blob {SCHEMA_SOURCE_BLOB_SHA1}; found {actual_blob}"
        )
    schema = json.loads(raw.decode("utf-8"))
    if schema.get("$id") != SCHEMA_ID:
        raise RuntimeError("PACKAGED_B1_SCHEMA_ID_MISMATCH")
    Draft202012Validator.check_schema(schema)
    return schema


def _schema_issues(data: object, schema: dict) -> list[dict]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    issues = []
    for error in sorted(validator.iter_errors(data), key=lambda e: (list(map(str, e.absolute_path)), e.validator or "")):
        issues.append({
            "instance_path": "/" + "/".join(str(p) for p in error.absolute_path),
            "schema_keyword": error.validator,
            "message": "value violates the reviewed B1 v1.7 schema draft 0.6 constraint",
        })
    return issues

def _derive_vectors(results: list[dict]) -> tuple[list[int], list[int], list[int]]:
    f = [0] * 8
    u = [0] * 8
    p = [0] * 8
    for result in results:
        j = STRATA.index(result["stratum_id"])
        terminal = result["terminal_status"]
        if terminal == "DEFINITE_FAILURE":
            f[j] += 1
        elif terminal == "UNRESOLVED":
            u[j] += 1
        else:
            p[j] += 1
    return f, u, p


def _variant_entry(variant: dict, index: int) -> dict:
    status = variant["validity_status"]
    result = {
        "index": index,
        "variant_id": variant["variant_id"],
        "validity_status": status,
        "local_semantic_decision": "LOCAL_CHECKS_PASS",
        "reason_codes": [],
        "measurement": {"state": "NO_DIAGNOSTIC_MEASUREMENT"},
    }
    errors = result["reason_codes"]
    results = variant["diagnostic_record_results"]

    # These checks are local; referenced external artifacts are deliberately not opened.
    decision = variant.get("status_decision")
    if status != "VALID":
        if not isinstance(decision, dict):
            errors.append("STATUS_DECISION_MISSING_OR_NOT_OBJECT")
        else:
            if decision.get("decision_basis") != DECISION_BASIS[status]:
                errors.append("STATUS_DECISION_BASIS_MISMATCH")
            if decision.get("diagnostic_terminal_values_consulted") is not False:
                errors.append("DIAGNOSTIC_TERMINAL_VALUES_CONSULTATION_NOT_FALSE")
            if decision.get("derived_failure_unresolved_counts_consulted") is not False:
                errors.append("DERIVED_FAILURE_COUNTS_CONSULTATION_NOT_FALSE")
            expected_identity = status == "INCOMPLETE"
            if decision.get("record_presence_identity_metadata_consulted") is not expected_identity:
                errors.append("RECORD_IDENTITY_CONSULTATION_STATUS_MISMATCH")
            try:
                decided = _parse_utc(decision["decided_at_utc"])
                ledger = None
                # The ledger's external rows cannot be checked here. Only campaign-level
                # ordering for the pre-diagnostic classifications is locally testable.
                first = variant.get("__campaign_first_start")
                if first is not None:
                    ledger = _parse_utc(first)
                snapshot = variant.get("__ledger_snapshot")
                if status in {"INVALID", "EXCLUDED_BEFORE_DIAGNOSTICS"}:
                    if ledger is not None and not decided < ledger:
                        errors.append("PREDIAGNOSTIC_DECISION_NOT_BEFORE_FIRST_RUN")
                    elif ledger is None and snapshot is not None and decided > _parse_utc(snapshot):
                        errors.append("PREDIAGNOSTIC_DECISION_AFTER_LEDGER_SNAPSHOT")
                elif status == "EXPECTED_NOT_RUN" and snapshot is not None and decided > _parse_utc(snapshot):
                    errors.append("EXPECTED_NOT_RUN_DECISION_AFTER_LEDGER_SNAPSHOT")
            except (KeyError, TypeError, ValueError, OverflowError):
                errors.append("STATUS_DECISION_TIMESTAMP_INVALID")

    # Identity checks within a variant are local and do not assert bank membership.
    ids = [row["diagnostic_record_id"] for row in results]
    if len(ids) != len(set(ids)):
        errors.append("DUPLICATE_RECORD_ID_WITHIN_VARIANT")

    if errors:
        result["local_semantic_decision"] = "REJECTED"
        result["reason_codes"] = sorted(set(errors))
        result["measurement"] = {"state": "NOT_REPORTED_DUE_TO_LOCAL_VALIDATION_ERRORS"}
        return result

    if status == "VALID":
        f, u, p = _derive_vectors(results)
        k_fail = sum(f)
        k_unresolved = sum(u)
        measurement = {
            "state": "COMPLETE_VALID_MEASUREMENT",
            "f": f,
            "u": u,
            "p": p,
            "k_fail": k_fail,
            "k_unresolved": k_unresolved,
            "cell": [variant["q_id"], variant["Z_id"], k_fail, k_unresolved],
            "c_d_formula": "max_{j=1..8}(f_j / k_fail); k_fail = sum_{j=1..8}(f_j)",
            "c_d_formula_source": MEASUREMENT_FORMULA_CITATION,
        }
        if k_fail == 0:
            measurement["c_d"] = "NO OBSERVED FAILURES"
            measurement["c_d_status"] = "NO OBSERVED FAILURES"
            measurement["c_d_zero_convention_source"] = MEASUREMENT_ZERO_CITATION
        else:
            rational = Fraction(max(f), k_fail)
            measurement["c_d"] = f"{rational.numerator}/{rational.denominator}"
            measurement["c_d_numerator"] = rational.numerator
            measurement["c_d_denominator"] = rational.denominator
            measurement["c_d_status"] = "DEFINED"
        result["measurement"] = measurement

    elif status == "INCOMPLETE":
        if results:
            f, u, p = _derive_vectors(results)
            result["measurement"] = {
                "state": "PROVISIONAL_INCOMPLETE_MEASUREMENTS",
                "label": "PROVISIONAL — INCOMPLETE INVENTORY",
                "received_record_count": len(results),
                "provisional_stratum_counts": {"f": f, "u": u, "p": p},
            }
        else:
            result["measurement"] = {
                "state": "INCOMPLETE_ZERO_RECORD_RECEIPT",
                "label": "PROVISIONAL — INCOMPLETE INVENTORY",
                "received_record_count": 0,
            }

    elif status in {"INVALID", "EXCLUDED_BEFORE_DIAGNOSTICS", "EXPECTED_NOT_RUN"}:
        # No measurement exists. Do not generate zero-valued vectors or exact cells.
        result["measurement"] = {
            "state": "NO_DIAGNOSTIC_MEASUREMENT",
        }

    return result

def validate_manifest(data: object, manifest_sha256: str, schema: dict | None = None) -> dict:
    schema = schema or load_and_verify_schema()
    base = {
        "intake_label": INTAKE_LABEL,
        "tool": TOOL_NAME,
        "tool_version": TOOL_VERSION,
        "manifest_schema": {
            "schema_id": SCHEMA_ID,
            "source_commit": SCHEMA_SOURCE_COMMIT,
            "source_path": SCHEMA_SOURCE_PATH,
            "source_blob_sha1": SCHEMA_SOURCE_BLOB_SHA1,
        },
        "measurement_definition": {
            "formula": "C_D = max_{j=1..8}(f_j / k_fail), where k_fail = sum_j f_j",
            "source_path": MEASUREMENT_SPEC_PATH,
            "source_commit": MEASUREMENT_SPEC_COMMIT,
            "source_blob_sha1": MEASUREMENT_SPEC_BLOB_SHA1,
            "source_section": "§1 (quotes Rev 11 lines 216–221); §5 reporting definition",
            "unresolved_rule": "k_unresolved does not enter C_D; it remains part of the exact cell identity",
        },
        "manifest_sha256": manifest_sha256,
        "manifest_schema_valid": False,
        "manifest_decision": "REJECTED",
        "manifest_reason_codes": [],
        "schema_issues": [],
        "variants": [],
        "external_checks_not_performed": EXTERNAL_CHECKS_NOT_PERFORMED,
        "scope_warning": (
            "A local schema/semantic pass is not full census-input admissibility and is not a census decision."
        ),
    }

    if isinstance(data, list) and not data:
        base["manifest_reason_codes"] = ["EMPTY_MANIFEST"]
        return base
    if not isinstance(data, dict):
        base["manifest_reason_codes"] = ["MANIFEST_ROOT_NOT_OBJECT"]
        return base

    if not isinstance(data.get("measurement_basis"), str):
        base["manifest_reason_codes"].append("NON_STRING_MEASUREMENT_BASIS")
    elif data.get("measurement_basis") != "record_level_64":
        base["manifest_reason_codes"].append("UNSUPPORTED_MEASUREMENT_BASIS")

    schema_issues = _schema_issues(data, schema)
    base["schema_issues"] = schema_issues
    if schema_issues:
        base["manifest_reason_codes"].append("B1_SCHEMA_VALIDATION_FAILED")
    else:
        base["manifest_schema_valid"] = True

    # Stop semantic processing when the structural contract failed. Never let a partial parse
    # turn an invalid manifest into a locally accepted one.
    if schema_issues:
        base["manifest_reason_codes"] = sorted(set(base["manifest_reason_codes"]))
        return base

    parent_z: dict[str, str] = {}
    for parent in data["parent_roster"]:
        pid, zid = parent["parent_id"], parent["Z_id"]
        if pid in parent_z:
            base["manifest_reason_codes"].append("DUPLICATE_PARENT_ID")
        else:
            parent_z[pid] = zid

    variant_ids: set[str] = set()
    valid_sets: list[tuple[str, set[str]]] = []
    digest_owners: dict[tuple[str, str], str] = {}
    ledger = data["diagnostic_run_start_ledger"]
    first_start = ledger["first_diagnostic_execution_started_at_utc"]
    snapshot = ledger["snapshot_as_of_utc"]

    for index, variant in enumerate(data["variants"]):
        vid = variant["variant_id"]
        if vid in variant_ids:
            base["manifest_reason_codes"].append("DUPLICATE_VARIANT_ID")
        variant_ids.add(vid)
        if parent_z.get(variant["parent_id"]) != variant["Z_id"]:
            base["manifest_reason_codes"].append("PARENT_FAMILY_MAPPING_MISMATCH")

        # Add the envelope ledger timestamps only for local temporal checks. These are not
        # inserted into or represented as original manifest fields.
        copy_variant = dict(variant)
        copy_variant["__campaign_first_start"] = first_start
        copy_variant["__ledger_snapshot"] = snapshot
        entry = _variant_entry(copy_variant, index)
        base["variants"].append(entry)
        if entry["local_semantic_decision"] == "REJECTED":
            base["manifest_reason_codes"].extend(entry["reason_codes"])

        if variant["validity_status"] == "VALID":
            ids = {r["diagnostic_record_id"] for r in variant["diagnostic_record_results"]}
            valid_sets.append((vid, ids))
            for field in ("semantic_source_digest", "runnable_artifact_digest"):
                key = (field, variant[field].lower())
                if key in digest_owners and digest_owners[key] != vid:
                    base["manifest_reason_codes"].append("DUPLICATE_ARTIFACT_DIGEST_REQUIRES_ADJUDICATION")
                else:
                    digest_owners[key] = vid

    if len(valid_sets) > 1:
        reference_vid, reference_ids = valid_sets[0]
        for other_vid, other_ids in valid_sets[1:]:
            if other_ids != reference_ids:
                base["manifest_reason_codes"].append("CROSS_VARIANT_ID_SET_MISMATCH")
                for entry in base["variants"]:
                    if entry["variant_id"] in {reference_vid, other_vid}:
                        entry["reason_codes"] = sorted(set(entry["reason_codes"] + ["CROSS_VARIANT_ID_SET_MISMATCH"]))
                        entry["local_semantic_decision"] = "REJECTED"

    base["manifest_reason_codes"] = sorted(set(base["manifest_reason_codes"]))
    if not base["manifest_reason_codes"]:
        base["manifest_decision"] = "LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED"
    return base

def _sidecar_schema_path() -> Path:
    return Path(__file__).resolve().parent / "aggregate_assertions.schema.json"


def validate_sidecar(
    sidecar: object,
    sidecar_raw: bytes,
    manifest_raw: bytes,
    manifest_report: dict,
    sidecar_schema_path: Path | None = None,
) -> dict:
    path = sidecar_schema_path or _sidecar_schema_path()
    schema_raw = path.read_bytes()
    actual_schema_blob_sha1 = _git_blob_sha1(schema_raw)
    if actual_schema_blob_sha1 != SIDECAR_SCHEMA_BLOB_SHA1:
        raise RuntimeError(
            "PACKAGED_SIDECAR_SCHEMA_IDENTITY_MISMATCH: expected "
            f"{SIDECAR_SCHEMA_BLOB_SHA1}, found {actual_schema_blob_sha1}"
        )
    schema = json.loads(schema_raw.decode("utf-8"))
    Draft202012Validator.check_schema(schema)
    report = {
        "intake_label": INTAKE_LABEL,
        "sidecar_sha256": hashlib.sha256(sidecar_raw).hexdigest(),
        "sidecar_schema_blob_sha1_actual": actual_schema_blob_sha1,
        "sidecar_decision": "REJECTED",
        "sidecar_reason_codes": [],
        "assertions": [],
        "manifest_decision_unchanged": manifest_report["manifest_decision"],
        "note": "Sidecar results never modify the manifest's independent local validation decision.",
    }

    if not isinstance(sidecar, dict):
        report["sidecar_reason_codes"].append("SIDECAR_ROOT_NOT_OBJECT")
        return report

    if manifest_report.get("manifest_decision") == "REJECTED":
        report["sidecar_reason_codes"].append("SIDECAR_MANIFEST_NOT_LOCALLY_VALID")
        return report

    for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(sidecar):
        report["sidecar_reason_codes"].append("SIDECAR_SCHEMA_VALIDATION_FAILED")
        if any(str(part) in {"f", "u", "p"} for part in error.absolute_path):
            report["sidecar_reason_codes"].append("MALFORMED_AGGREGATE")
        report.setdefault("schema_issues", []).append({
            "instance_path": "/" + "/".join(str(p) for p in error.absolute_path),
            "schema_keyword": error.validator,
            "message": "value violates the aggregate-sidecar schema constraint",
        })

    expected_manifest_sha = hashlib.sha256(manifest_raw).hexdigest()
    if report.get("sidecar_reason_codes"):
        report["sidecar_reason_codes"] = sorted(set(report["sidecar_reason_codes"]))
        return report
    if sidecar.get("manifest_sha256") != expected_manifest_sha:
        report["sidecar_reason_codes"].append("SIDECAR_MANIFEST_SHA256_MISMATCH")
    if sidecar.get("sidecar_schema_blob_sha1") != actual_schema_blob_sha1:
        report["sidecar_reason_codes"].append("SIDECAR_SCHEMA_BLOB_SHA1_MISMATCH")
    if report["sidecar_reason_codes"]:
        report["sidecar_reason_codes"] = sorted(set(report["sidecar_reason_codes"]))
        return report

    variants_by_id = {v.get("variant_id"): v for v in manifest_report.get("_validated_variants", [])}
    seen = set()
    for assertion in sidecar.get("aggregate_assertions", []) if isinstance(sidecar.get("aggregate_assertions"), list) else []:
        vid = assertion.get("variant_id") if isinstance(assertion, dict) else None
        row = {"variant_id": vid, "decision": "REJECTED", "reason_codes": []}
        if not isinstance(vid, str) or vid not in variants_by_id:
            row["reason_codes"].append("SIDECAR_VARIANT_NOT_FOUND")
        elif vid in seen:
            row["reason_codes"].append("SIDECAR_DUPLICATE_VARIANT_ASSERTION")
        else:
            seen.add(vid)
            variant = variants_by_id[vid]
            if variant.get("validity_status") != "VALID":
                row["reason_codes"].append("SIDECAR_ASSERTION_REQUIRES_VALID_VARIANT")
            else:
                derived_f, derived_u, derived_p = _derive_vectors(variant["diagnostic_record_results"])
                for field, derived in (("f", derived_f), ("u", derived_u), ("p", derived_p)):
                    if field not in assertion:
                        continue
                    supplied = assertion[field]
                    if (not isinstance(supplied, list) or len(supplied) != 8
                            or any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in supplied)):
                        row["reason_codes"].append("MALFORMED_AGGREGATE")
                    elif supplied != derived:
                        row["reason_codes"].append("AGGREGATE_MISMATCH")
            if not row["reason_codes"]:
                row["decision"] = "CONSISTENT_NON_AUTHORITATIVE_ASSERTION"
        row["reason_codes"] = sorted(set(row["reason_codes"]))
        report["assertions"].append(row)

    report["sidecar_reason_codes"] = sorted(set(report["sidecar_reason_codes"]))
    if not report["sidecar_reason_codes"] and all(a["decision"] != "REJECTED" for a in report["assertions"]):
        report["sidecar_decision"] = "SIDECAR_CONSISTENCY_CHECKS_PASS"
    report["manifest_decision_unchanged"] = manifest_report["manifest_decision"]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=INTAKE_LABEL)
    parser.add_argument("--manifest", required=True, help="B1 v1.7 manifest JSON")
    parser.add_argument("--sidecar", help="optional aggregate-assertion sidecar JSON")
    parser.add_argument("--report", help="combined report JSON path; defaults to stdout")
    args = parser.parse_args(argv)

    try:
        manifest_raw = Path(args.manifest).read_bytes()
        manifest_sha = hashlib.sha256(manifest_raw).hexdigest()
        manifest_data = json.loads(manifest_raw.decode("utf-8"))
        schema = load_and_verify_schema()
        manifest_report = validate_manifest(manifest_data, manifest_sha, schema)
        combined: dict[str, Any] = {"manifest_report": manifest_report, "sidecar_report": None}
        exit_code = 0 if manifest_report["manifest_decision"] != "REJECTED" else 2
        if args.sidecar:
            sidecar_raw = Path(args.sidecar).read_bytes()
            sidecar_data = json.loads(sidecar_raw.decode("utf-8"))
            # Internal lookup is not exposed in the public report.
            manifest_report_for_sidecar = dict(manifest_report)
            manifest_report_for_sidecar["_validated_variants"] = manifest_data.get("variants", []) if isinstance(manifest_data, dict) else []
            sidecar_report = validate_sidecar(sidecar_data, sidecar_raw, manifest_raw, manifest_report_for_sidecar)
            combined["sidecar_report"] = sidecar_report
            if sidecar_report["sidecar_decision"] == "REJECTED":
                exit_code = 2
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, RuntimeError) as exc:
        print(f"INTAKE_INPUT_ERROR: {exc}", file=sys.stderr)
        return 3

    output = json.dumps(combined, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.report:
        Path(args.report).write_text(output, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(output)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
