"""B1 census intake validator (step-1 infrastructure).

Admits per-variant diagnostic records to the Gate 1 outcome-free support census.
No bank access, no solver execution, no outcomes, no census decisions.

Standard library only. See README.md for the record contract and scope.
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
TOOL_VERSION = "0.1"
SCHEMA_VERSION = "0.1"

STRATA = tuple(f"D{j}" for j in range(1, 9))
CAPACITY = {
    "record": (8, 8, 8, 8, 8, 8, 8, 8),
    "canonical": (8, 8, 8, 8, 8, 4, 8, 8),
}
REQUIRED_FIELDS = frozenset(
    {
        "variant_id",
        "parent_id",
        "parent_family",
        "mutation_id",
        "exposure_basis",
        "f",
        "u",
        "strata_record_ids",
        "source_digest",
    }
)
ALLOWED_FIELDS = REQUIRED_FIELDS | {"notes"}
STRING_FIELDS = ("variant_id", "parent_id", "parent_family", "mutation_id")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")

OUTCOME_NAMES = frozenset(
    {
        "correctness",
        "y",
        "outcome",
        "pass",
        "fail",
        "passed",
        "failed",
        "evaluation_outcome",
        "heldout_correctness",
    }
)
OUTCOME_PREFIXES = ("y_", "outcome_", "correctness_", "heldout_")


def _is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _outcome_fields(record: dict) -> list[str]:
    found = []
    for key in record:
        name = str(key)
        lowered = name.lower()
        if (
            lowered in OUTCOME_NAMES
            or lowered.startswith(OUTCOME_PREFIXES)
            or lowered.endswith("_correctness")
        ):
            found.append(name)
    return found


def _validate_vector(value: object, label: str, errors: list[str]) -> list[int] | None:
    if not isinstance(value, list):
        errors.append(f"{label}_NOT_ARRAY")
        return None
    if len(value) != 8:
        errors.append(f"{label}_VECTOR_LENGTH")
    good = True
    for item in value:
        if not _is_int(item):
            errors.append(f"{label}_NOT_INTEGER")
            good = False
        elif item < 0:
            errors.append(f"{label}_NEGATIVE")
            good = False
    if not good or len(value) != 8:
        return None
    return list(value)


def validate_record(
    record: object,
    index: int,
    seen_variant_ids: set[str],
    seen_record_ids: set[str],
) -> tuple[dict, bool]:
    """Validate one record. Mutates the two seen-id sets. Returns (entry, admitted)."""

    entry: dict = {
        "index": index,
        "variant_id": None,
        "exposure_basis": None,
        "decision": "REJECTED",
        "reason_codes": [],
    }

    if not isinstance(record, dict):
        entry["reason_codes"] = ["RECORD_NOT_OBJECT"]
        return entry, False

    vid = record.get("variant_id")
    if isinstance(vid, str) and vid:
        entry["variant_id"] = vid

    errors: list[str] = []

    outcome_fields = _outcome_fields(record)
    if outcome_fields:
        errors.append("OUTCOME_FIELD_PRESENT")

    unknown = sorted(str(k) for k in record if str(k) not in ALLOWED_FIELDS)
    if unknown:
        errors.append("UNKNOWN_FIELD")

    missing = sorted(ALLOWED_FIELDS - {"notes"} - set(record))
    if missing:
        errors.append("MISSING_FIELD")
    if "u" not in record:
        errors.append("MISSING_UNRESOLVED_VECTOR")

    if not missing:
        for field in STRING_FIELDS:
            value = record[field]
            if not isinstance(value, str) or not value:
                errors.append("EMPTY_STRING_FIELD")
                break

        basis = record["exposure_basis"]
        if basis not in CAPACITY:
            errors.append("INVALID_EXPOSURE_BASIS")
        entry["exposure_basis"] = basis if isinstance(basis, str) else None

        digest = record["source_digest"]
        if not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest):
            errors.append("INVALID_SOURCE_DIGEST")

        f = _validate_vector(record["f"], "F", errors)
        u = _validate_vector(record["u"], "U", errors)

        strata_ids = record["strata_record_ids"]
        if not isinstance(strata_ids, dict):
            errors.append("STRATA_NOT_OBJECT")
        else:
            if set(strata_ids) != set(STRATA):
                errors.append("STRATA_KEYS")
            else:
                local_ids: set[str] = set()
                for pos, stratum in enumerate(STRATA):
                    ids = strata_ids[stratum]
                    expected = CAPACITY[basis][pos] if basis in CAPACITY else None
                    if not isinstance(ids, list):
                        errors.append("STRATUM_IDS_NOT_ARRAY")
                        continue
                    if expected is not None and len(ids) != expected:
                        errors.append("STRATUM_ID_COUNT")
                    for item in ids:
                        if not isinstance(item, str) or not item:
                            errors.append("STRATUM_ID_TYPE")
                            continue
                        if item in local_ids:
                            errors.append("DUPLICATE_RECORD_ID")
                        if item in seen_record_ids:
                            errors.append("RECORD_ID_REUSED_ACROSS_RECORDS")
                        local_ids.add(item)
                seen_record_ids.update(local_ids)

        if f is not None and u is not None and basis in CAPACITY:
            for pos, capacity in enumerate(CAPACITY[basis]):
                if f[pos] + u[pos] > capacity:
                    errors.append("STRATUM_CAPACITY_EXCEEDED")
                    break

        if f is not None and u is not None:
            k_fail = sum(f)
            k_unresolved = sum(u)
            if k_fail == 0:
                c_d = "0"
                cd_status = "NO_OBSERVED_FAILURES"
            else:
                ratio = Fraction(max(f), k_fail)
                c_d = str(ratio)
                cd_status = "DEFINED"

            entry["derived"] = {
                "k_fail": k_fail,
                "k_unresolved": k_unresolved,
                "c_d_exact": c_d,
                "c_d_status": cd_status,
                "cell": [record["mutation_id"], record["parent_family"], k_fail, k_unresolved],
            }

    if isinstance(vid, str) and vid:
        if vid in seen_variant_ids:
            errors.append("DUPLICATE_VARIANT_ID")
        seen_variant_ids.add(vid)

    # Stable, de-duplicated ordering of reason codes.
    codes = sorted(set(errors))
    entry["reason_codes"] = codes
    if not codes:
        entry["decision"] = "ADMITTED"
    return entry, not codes


def validate_manifest(data: object, manifest_sha256: str | None = None) -> dict:
    """Validate a manifest (list of records) and return a deterministic report."""

    if not isinstance(data, list):
        raise ValueError("manifest root must be a JSON array")

    seen_variants: set[str] = set()
    seen_record_ids: set[str] = set()
    entries = []
    for index, record in enumerate(data):
        entry, _ = validate_record(record, index, seen_variants, seen_record_ids)
        entries.append(entry)

    admitted = sum(1 for e in entries if e["decision"] == "ADMITTED")
    basis_counts = {"record": 0, "canonical": 0}
    for entry in entries:
        basis = entry.get("exposure_basis")
        if entry["decision"] == "ADMITTED" and basis in basis_counts:
            basis_counts[basis] += 1

    report = {
        "tool": TOOL_NAME,
        "tool_version": TOOL_VERSION,
        "schema_version": SCHEMA_VERSION,
        "manifest_sha256": manifest_sha256,
        "scope": "intake only: no census, no outcomes, no gate verdict",
        "count": len(entries),
        "admitted": admitted,
        "rejected": len(entries) - admitted,
        "admitted_by_basis": basis_counts,
        "records": entries,
    }
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="path to a JSON manifest array")
    parser.add_argument("--report", help="write the JSON report to this path (default: stdout)")
    args = parser.parse_args(argv)

    path = Path(args.manifest)
    try:
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        data = json.loads(raw.decode("utf-8"))
        report = validate_manifest(data, digest)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"INTAKE_INPUT_ERROR: {exc}", file=sys.stderr)
        return 3

    text = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8", newline="\n")
    else:
        sys.stdout.write(text)
    return 0 if report["rejected"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
