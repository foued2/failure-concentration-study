"""Mechanical intake checks for the proposed LC518 A2 C6 witness dossier.

PROPOSED COMPANION TOOL — NOT A FROZEN PROTOCOL CHANGE, NOT AN A2 VERDICT.

This tool:
- verifies byte bindings among the private annex, parent identity manifest,
  adopted family map, C4 report and C6 dossier;
- checks C6 witness arithmetic and parent/role/mechanism/family identity;
- verifies that cited text is literally present in the pinned mechanism definition;
- derives exact C_D values and detects a positive three-parent/cross-parent
  witness pattern within one exact cell.

It does NOT decide whether a quoted rule semantically establishes mechanism reach,
whether the complete vector is scientifically jointly attainable, whether a
structural absence is justified, or whether all cells in S_W x D are assessed.
Those remain independent human review obligations under A2 Rev 11. A mechanically
validated dossier is not a C6 verdict and never issues the aggregate A2 verdict.

The tool is deliberately positive-evidence-only. It can identify a candidate
positive witness pattern from admissible dossier entries. Lack of such a pattern
is NOT_SUPPORTED only after complete assessment; because this v1 dossier does
not encode exhaustive absence evidence, a no-pattern result is always
NOT_ASSESSABLE.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

TOOL_NAME = "lc518-c6-witness-dossier-checker"
TOOL_VERSION = "1.0.0"
LABEL = (
    "PROPOSED C6 DOSSIER MECHANICAL CHECK ONLY — NOT A2 VERDICT — "
    "SEMANTIC REACH AND JOINT ATTAINABILITY REQUIRE INDEPENDENT REVIEW"
)
SCHEMA_FILENAME = "C6_WITNESS_REVIEW_SCHEMA.json"
EXPECTED_SCHEMA_GIT_BLOB_SHA1 = "37d682d9228d7fab70963a4507488c1e4cf5ade5"
EXPECTED_BANK_DESIGN_SHA256 = "da7f8c1ae3c5e3a582c38d91be2463061bce2acb0a772fac72d34459f4b17843"
N_RECORDS = 64
STRATA = [f"D{i}" for i in range(1, 9)]
FAMILIES_IN_SCOPE = {"K1", "K2", "K3", "K4"}


class DossierError(ValueError):
    """Raised for a malformed, unbound or mechanically inadmissible dossier."""


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def _load_object(path: Path) -> tuple[dict, bytes]:
    raw = path.read_bytes()
    value = json.loads(raw.decode("utf-8"))
    if not isinstance(value, dict):
        raise DossierError(f"JSON_ROOT_NOT_OBJECT:{path.name}")
    return value, raw


def _load_pinned_dossier_schema(path: Path | None = None) -> dict:
    schema_path = path or (Path(__file__).resolve().parent / SCHEMA_FILENAME)
    raw = schema_path.read_bytes()
    actual = _git_blob_sha1(raw)
    if actual != EXPECTED_SCHEMA_GIT_BLOB_SHA1:
        raise DossierError(
            "C6_DOSSIER_SCHEMA_IDENTITY_MISMATCH:"
            f"expected={EXPECTED_SCHEMA_GIT_BLOB_SHA1}:actual={actual}"
        )
    schema = json.loads(raw.decode("utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def _parse_aware_timestamp(value: str, label: str) -> datetime:
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise DossierError(f"{label}_TIMESTAMP_INVALID") from exc
    if result.tzinfo is None or result.utcoffset() is None:
        raise DossierError(f"{label}_TIMESTAMP_MUST_INCLUDE_TIMEZONE")
    return result


def _validate_reviewer_attestation(dossier: dict) -> dict:
    attestation = dossier["reviewer_attestation"]
    recorded = _parse_aware_timestamp(
        attestation["attestation_recorded_at_utc"], "ATTESTATION_RECORDED"
    )
    first_access = _parse_aware_timestamp(
        attestation["first_annex_access_at_utc"], "FIRST_ANNEX_ACCESS"
    )
    completed = _parse_aware_timestamp(
        attestation["review_completed_at_utc"], "REVIEW_COMPLETED"
    )
    if not recorded < first_access:
        raise DossierError("C6_REVIEWER_ATTESTATION_NOT_RECORDED_BEFORE_ANNEX_ACCESS")
    if not first_access <= completed:
        raise DossierError("C6_REVIEW_COMPLETED_BEFORE_FIRST_ANNEX_ACCESS")
    return {
        "reviewer_id_present": bool(attestation["reviewer_id"].strip()),
        "attestation_precedes_first_access": True,
        "review_completed_after_access": True,
        "independence_fields_attested": True,
        "scope": "SELF_ATTESTED_NOT_EXTERNALLY_VERIFIED_BY_THIS_TOOL",
    }


def _validate_dossier_schema(dossier: dict, schema: dict) -> list[dict]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(
        validator.iter_errors(dossier),
        key=lambda error: (
            list(map(str, error.absolute_path)),
            error.validator or "",
        ),
    )
    return [
        {
            "instance_path": "/" + "/".join(str(part) for part in error.absolute_path),
            "keyword": error.validator,
            "message": error.message,
        }
        for error in errors
    ]


def _validate_bindings(
    *,
    dossier: dict,
    annex: dict,
    annex_raw: bytes,
    identity_manifest: dict,
    identity_raw: bytes,
    roster: dict,
    roster_raw: bytes,
    family_map: dict,
    family_map_raw: bytes,
    c4_report: dict,
    c4_raw: bytes,
) -> dict:
    expected = {
        "annex_sha256": _sha256(annex_raw),
        "parent_identity_manifest_sha256": _sha256(identity_raw),
        "parent_roster_sha256": _sha256(roster_raw),
        "family_map_sha256": _sha256(family_map_raw),
        "c4_report_sha256": _sha256(c4_raw),
    }
    for key, digest in expected.items():
        if dossier.get(key) != digest:
            raise DossierError(f"C6_DOSSIER_ARTIFACT_BINDING_MISMATCH:{key}")

    if roster.get("status") != "ADOPTED":
        raise DossierError("C6_PARENT_ROSTER_NOT_ADOPTED")
    if (
        not isinstance(roster.get("artifact_id"), str)
        or not isinstance(roster.get("version"), str)
    ):
        raise DossierError("C6_PARENT_ROSTER_IDENTITY_MISSING")
    if family_map.get("status") != "ADOPTED":
        raise DossierError("C6_FAMILY_MAP_NOT_ADOPTED")

    identity_roster_adoption = identity_manifest.get("parent_roster_adoption_ref")
    if (
        not isinstance(identity_roster_adoption, dict)
        or identity_roster_adoption.get("status") != "ADOPTED"
        or identity_roster_adoption.get("artifact_id") != roster.get("artifact_id")
        or identity_roster_adoption.get("version") != roster.get("version")
        or identity_roster_adoption.get("sha256") != expected["parent_roster_sha256"]
    ):
        raise DossierError("C6_IDENTITY_MANIFEST_PARENT_ROSTER_BINDING_INVALID")

    identity_adoption = identity_manifest.get("family_map_adoption_ref")
    c4 = c4_report.get("C4", {})
    c4_adoption = c4.get("family_map_adoption_ref", {})
    if (
        not isinstance(identity_adoption, dict)
        or identity_adoption.get("status") != "ADOPTED"
        or identity_adoption.get("artifact_id") != family_map.get("artifact_id")
        or identity_adoption.get("sha256") != expected["family_map_sha256"]
    ):
        raise DossierError("C6_IDENTITY_MANIFEST_FAMILY_BINDING_INVALID")
    if (
        c4_report.get("parent_identity_manifest_sha256") != expected["parent_identity_manifest_sha256"]
        or c4_report.get("parent_roster_sha256") != expected["parent_roster_sha256"]
        or c4.get("status") != "ASSESSED"
        or c4.get("parent_roster_sha256_verified") is not True
        or not isinstance(c4.get("parent_roster_adoption_ref"), dict)
        or c4.get("parent_roster_adoption_ref", {}).get("status") != "ADOPTED"
        or c4.get("parent_roster_adoption_ref", {}).get("artifact_id") != roster.get("artifact_id")
        or c4.get("parent_roster_adoption_ref", {}).get("version") != roster.get("version")
        or c4.get("parent_roster_adoption_ref", {}).get("sha256") != expected["parent_roster_sha256"]
        or c4.get("family_map_sha256_verified") is not True
        or c4.get("family_map_roster_partition_verified") is not True
        or c4.get("parent_source_hash_attestation_present") is not True
        or c4.get("parent_source_bundle_sha256_verified") is not True
        or not isinstance(c4_adoption, dict)
        or c4_adoption.get("status") != "ADOPTED"
        or c4_adoption.get("artifact_id") != family_map.get("artifact_id")
        or c4_adoption.get("sha256") != expected["family_map_sha256"]
    ):
        raise DossierError("C6_C4_REPORT_NOT_BOUND_TO_ADOPTED_IDENTITIES")

    if c4_report.get("audit_decision") != "STRUCTURAL_INTAKE_PASS_C6_ADEQUACY_NOT_ASSESSED":
        raise DossierError("C6_C4_STRUCTURAL_INTAKE_NOT_PASSED")

    design = dossier["design_basis"]
    if (
        design.get("N") != N_RECORDS
        or design.get("unit") != "diagnostic_bank_records_per_solver_body"
        or design.get("R") != [8] * 8
        or design.get("bank_design_sha256") != EXPECTED_BANK_DESIGN_SHA256
    ):
        raise DossierError("C6_FROZEN_DIAGNOSTIC_DOMAIN_BASIS_MISMATCH")

    return {
        "annex_sha256_verified": True,
        "parent_identity_manifest_sha256_verified": True,
        "parent_roster_sha256_verified": True,
        "parent_roster_adoption_verified": True,
        "family_map_sha256_verified": True,
        "c4_report_sha256_verified": True,
        "c4_status_assessed": True,
        "parent_roster_adopted": True,
        "family_map_adopted": True,
        "diagnostic_domain_N": N_RECORDS,
        "diagnostic_stratum_record_counts": [8] * 8,
        "all_bindings_match": True,
    }


def _build_role_mechanism_maps(annex: dict) -> tuple[dict, dict]:
    pair_by_parent: dict[str, dict] = {}
    for row in annex["pair_assignments"]:
        parent_id = row["parent_id"]
        if parent_id in pair_by_parent:
            raise DossierError(f"C6_ANNEX_PARENT_PAIR_ASSIGNMENT_AMBIGUOUS:{parent_id}")
        pair_by_parent[parent_id] = row

    extra_by_parent: dict[str, str] = {}
    for row in annex["s_extra_assignments"]:
        parent_id = row["parent_id"]
        if parent_id in extra_by_parent:
            raise DossierError(f"C6_ANNEX_S_EXTRA_ASSIGNMENT_AMBIGUOUS:{parent_id}")
        extra_by_parent[parent_id] = row["mechanism_id"]

    return pair_by_parent, extra_by_parent


def _expected_mechanism(
    parent_id: str,
    role: str,
    pair_by_parent: dict[str, dict],
    extra_by_parent: dict[str, str],
) -> str:
    if role == "SA":
        row = pair_by_parent.get(parent_id)
        return row["mechanism_a"] if row else ""
    if role == "SB":
        row = pair_by_parent.get(parent_id)
        return row["mechanism_b"] if row else ""
    if role == "S-EXTRA":
        return extra_by_parent.get(parent_id, "")
    return ""


def _c4_scope(c4_report: dict) -> set[tuple[str, str]]:
    cells = c4_report["C4"].get("qualifying_cells")
    if not isinstance(cells, list):
        raise DossierError("C6_C4_QUALIFYING_CELL_TABLE_MISSING")
    return {
        (row["mechanism_id"], row["Z_id"])
        for row in cells
        if row.get("Z_id") in FAMILIES_IN_SCOPE
    }


def _effective_parent_identities(
    roster: dict, identity_manifest: dict
) -> tuple[dict[str, dict], dict[str, dict]]:
    roster_rows = roster.get("parents")
    if (
        roster.get("status") != "ADOPTED"
        or not isinstance(roster.get("artifact_id"), str)
        or not isinstance(roster.get("version"), str)
    ):
        raise DossierError("C6_ROSTER_NOT_ADOPTED_OR_IDENTIFIED")
    if not isinstance(roster_rows, list) or len(roster_rows) != 30:
        raise DossierError("C6_ROSTER_NOT_EXACTLY_30_PARENTS")
    roster_by_id: dict[str, dict] = {}
    for row in roster_rows:
        if not isinstance(row, dict) or row.get("parent_id") in roster_by_id:
            raise DossierError("C6_ROSTER_PARENT_ID_DUPLICATE_OR_INVALID")
        roster_by_id[row["parent_id"]] = row

    identity_rows = identity_manifest.get("parents")
    if not isinstance(identity_rows, list) or len(identity_rows) != 30:
        raise DossierError("C6_PARENT_IDENTITY_MANIFEST_NOT_EXACTLY_30")
    identity_by_id: dict[str, dict] = {}
    hash_to_family: dict[str, str] = {}
    for row in identity_rows:
        if not isinstance(row, dict):
            raise DossierError("C6_PARENT_IDENTITY_ROW_NOT_OBJECT")
        parent_id = row.get("parent_id")
        digest = row.get("base_source_sha256")
        z_id = row.get("Z_id")
        if (
            not isinstance(parent_id, str)
            or parent_id not in roster_by_id
            or parent_id in identity_by_id
            or not isinstance(digest, str)
            or len(digest) != 64
            or any(ch not in "0123456789abcdef" for ch in digest)
            or z_id != roster_by_id[parent_id].get("Z_id")
        ):
            raise DossierError(f"C6_PARENT_IDENTITY_INVALID:{parent_id}")
        if digest in hash_to_family and hash_to_family[digest] != z_id:
            raise DossierError("C6_BASE_SOURCE_HASH_CROSSES_FAMILIES")
        hash_to_family[digest] = z_id
        identity_by_id[parent_id] = row

    if set(identity_by_id) != set(roster_by_id):
        raise DossierError("C6_PARENT_IDENTITY_ROSTER_COVERAGE_INCOMPLETE")
    return roster_by_id, identity_by_id


def _quote_in_definition(quote: str, definition: str, label: str) -> None:
    if not isinstance(quote, str) or not quote.strip() or quote not in definition:
        raise DossierError(f"{label}_QUOTE_NOT_FOUND_VERBATIM_IN_PINNED_DEFINITION")


def _check_vector(vector: Any, name: str) -> list[int]:
    if not isinstance(vector, list) or len(vector) != 8:
        raise DossierError(f"C6_{name}_VECTOR_MUST_HAVE_EIGHT_ENTRIES")
    values: list[int] = []
    for index, value in enumerate(vector):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise DossierError(f"C6_{name}_VECTOR_ENTRY_INVALID:{index + 1}")
        values.append(value)
    return values


def _validate_witness(
    witness: dict,
    *,
    definitions: dict[str, str],
    roster_by_id: dict[str, dict],
    identity_by_id: dict[str, dict],
    pair_by_parent: dict[str, dict],
    extra_by_parent: dict[str, str],
    R: list[int],
) -> tuple[dict, list[str]]:
    reasons: list[str] = []
    parent_id = witness["parent_id"]
    role = witness["version_role"]
    mechanism_id = witness["mechanism_id"]
    z_id = witness["Z_id"]

    roster_row = roster_by_id.get(parent_id)
    identity_row = identity_by_id.get(parent_id)
    if roster_row is None or identity_row is None:
        raise DossierError(f"C6_WITNESS_PARENT_NOT_IN_ROSTER_AND_IDENTITY:{parent_id}")
    if roster_row.get("Z_id") != z_id or identity_row.get("Z_id") != z_id:
        raise DossierError(f"C6_WITNESS_FAMILY_IDENTITY_MISMATCH:{witness['witness_id']}")

    expected_mechanism = _expected_mechanism(
        parent_id, role, pair_by_parent, extra_by_parent
    )
    if expected_mechanism != mechanism_id:
        raise DossierError(f"C6_WITNESS_ROLE_MECHANISM_MISMATCH:{witness['witness_id']}")

    expected_slot = f"{parent_id}:{role}"
    if witness.get("version_slot_id") != expected_slot:
        raise DossierError(f"C6_WITNESS_VERSION_SLOT_ID_MISMATCH:{witness['witness_id']}")

    definition = definitions.get(mechanism_id)
    if not isinstance(definition, str) or not definition.strip():
        raise DossierError(f"C6_MECHANISM_DEFINITION_MISSING:{mechanism_id}")

    f = _check_vector(witness["f"], "FAILURE")
    u = _check_vector(witness["u"], "UNRESOLVED")
    cell = witness["cell"]
    k_fail = cell["k_fail"]
    k_unresolved = cell["k_unresolved"]
    if sum(f) != k_fail:
        raise DossierError(f"C6_FAILURE_VECTOR_SUM_MISMATCH:{witness['witness_id']}")
    if sum(u) != k_unresolved:
        raise DossierError(f"C6_UNRESOLVED_VECTOR_SUM_MISMATCH:{witness['witness_id']}")
    if k_fail + k_unresolved > N_RECORDS:
        raise DossierError(f"C6_EXACT_CELL_OUT_OF_DOMAIN:{witness['witness_id']}")
    if any(f[j] + u[j] > R[j] for j in range(8)):
        raise DossierError(f"C6_PER_STRATUM_RECORD_BUDGET_EXCEEDED:{witness['witness_id']}")

    reach_rows = witness["reach_assessments"]
    reach_by_stratum: dict[str, dict] = {}
    for row in reach_rows:
        stratum = row["stratum_id"]
        if stratum in reach_by_stratum:
            raise DossierError(f"C6_DUPLICATE_REACH_ASSESSMENT:{witness['witness_id']}:{stratum}")
        reach_by_stratum[stratum] = row

    for index, count in enumerate(f):
        if count == 0:
            continue
        stratum = STRATA[index]
        assessment = reach_by_stratum.get(stratum)
        if assessment is None:
            raise DossierError(f"C6_NONZERO_FAILURE_REACH_NOT_ASSESSED:{witness['witness_id']}:{stratum}")
        if assessment["decision"] != "SUPPORTED":
            raise DossierError(f"C6_NONZERO_FAILURE_REACH_NOT_SUPPORTED:{witness['witness_id']}:{stratum}")
        _quote_in_definition(
            assessment["quoted_rule"], definition,
            f"C6_REACH:{witness['witness_id']}:{stratum}",
        )

    joint = witness["joint_attainability"]
    if joint["decision"] != "SUPPORTED":
        raise DossierError(f"C6_JOINT_ATTAINABILITY_NOT_SUPPORTED:{witness['witness_id']}")
    _quote_in_definition(
        joint["quoted_rule"], definition, f"C6_JOINT:{witness['witness_id']}"
    )

    unresolved_rows = witness["unresolved_provenance"]
    provenance_by_stratum: dict[str, dict] = {}
    for row in unresolved_rows:
        stratum = row["stratum_id"]
        if stratum in provenance_by_stratum:
            raise DossierError(f"C6_DUPLICATE_UNRESOLVED_PROVENANCE:{witness['witness_id']}:{stratum}")
        provenance_by_stratum[stratum] = row

    expected_unresolved_strata = {
        STRATA[index] for index, count in enumerate(u) if count > 0
    }
    if set(provenance_by_stratum) != expected_unresolved_strata:
        raise DossierError(f"C6_UNRESOLVED_PROVENANCE_COVERAGE_MISMATCH:{witness['witness_id']}")
    for stratum, provenance in provenance_by_stratum.items():
        if provenance["origin"] == "MECHANISM_ATTRIBUTED":
            _quote_in_definition(
                provenance["mechanism_rule_quote"],
                definition,
                f"C6_UNRESOLVED_MECHANISM:{witness['witness_id']}:{stratum}",
            )

    cd_value = Fraction(max(f), k_fail)
    identity_key = (z_id, identity_row["base_source_sha256"])
    cell_key = (mechanism_id, z_id, k_fail, k_unresolved)
    return {
        "witness_id": witness["witness_id"],
        "parent_id": parent_id,
        "version_role": role,
        "mechanism_id": mechanism_id,
        "Z_id": z_id,
        "cell_key": cell_key,
        "effective_parent_key": identity_key,
        "C_D": cd_value,
        "C_D_rational": f"{cd_value.numerator}/{cd_value.denominator}",
    }, reasons


def validate_c6_dossier(
    *,
    dossier: dict,
    dossier_schema: dict,
    annex: dict,
    annex_raw: bytes,
    identity_manifest: dict,
    identity_raw: bytes,
    roster: dict,
    roster_raw: bytes,
    family_map: dict,
    family_map_raw: bytes,
    c4_report: dict,
    c4_raw: bytes,
    roster: dict,
) -> dict:
    schema_errors = _validate_dossier_schema(dossier, dossier_schema)
    if schema_errors:
        return {
            "tool": TOOL_NAME,
            "tool_version": TOOL_VERSION,
            "label": LABEL,
            "dossier_decision": "REJECTED",
            "schema_errors": schema_errors,
            "audit_verdict": "NOT_ISSUED_COMPONENT_ONLY",
        }

    binding_report = _validate_bindings(
        dossier=dossier,
        annex=annex,
        annex_raw=annex_raw,
        identity_manifest=identity_manifest,
        identity_raw=identity_raw,
        roster=roster,
        roster_raw=roster_raw,
        family_map=family_map,
        family_map_raw=family_map_raw,
        c4_report=c4_report,
        c4_raw=c4_raw,
    )
    reviewer_report = _validate_reviewer_attestation(dossier)

    roster_by_id, identity_by_id = _effective_parent_identities(roster, identity_manifest)
    pair_by_parent, extra_by_parent = _build_role_mechanism_maps(annex)
    definitions = {
        row["mechanism_id"]: row["definition"]
        for row in annex["mechanisms"]
    }
    s_w = _c4_scope(c4_report)
    if not s_w:
        return {
            "tool": TOOL_NAME,
            "tool_version": TOOL_VERSION,
            "label": LABEL,
            "dossier_decision": "MECHANICALLY_VALIDATED_C4_SCOPE_EMPTY",
            "binding_checks": binding_report,
            "reviewer_attestation": reviewer_report,
            "S_W_pair_count": 0,
            "audit_verdict": "NOT_ISSUED_COMPONENT_ONLY",
            "C6_status": "NOT_ASSESSABLE_C4_SCOPE_EMPTY",
            "boundary": "C4 empty scope must be handled under Rev 11 §6; this tool does not issue that verdict.",
        }

    valid_witnesses: list[dict] = []
    inadmissible_witnesses: list[dict] = []
    out_of_scope_witnesses: list[dict] = []
    seen_witness_ids: set[str] = set()
    cell_groups: dict[tuple, dict[tuple[str, str], set[Fraction]]] = {}

    for witness in dossier["witnesses"]:
        witness_id = witness["witness_id"]
        if witness_id in seen_witness_ids:
            raise DossierError(f"C6_WITNESS_ID_DUPLICATE:{witness_id}")
        seen_witness_ids.add(witness_id)

        try:
            validated, _reasons = _validate_witness(
                witness,
                definitions=definitions,
                roster_by_id=roster_by_id,
                identity_by_id=identity_by_id,
                pair_by_parent=pair_by_parent,
                extra_by_parent=extra_by_parent,
                R=[8] * 8,
            )
        except DossierError as exc:
            inadmissible_witnesses.append({
                "witness_id": witness_id,
                "reason": str(exc),
                "disposition": "INADMISSIBLE_DISCARDED_NOT_STRUCTURAL_ABSENCE",
            })
            continue

        valid_witnesses.append(validated)
        mechanism_family = (validated["mechanism_id"], validated["Z_id"])
        if mechanism_family not in s_w or validated["Z_id"] not in FAMILIES_IN_SCOPE:
            out_of_scope_witnesses.append(witness_id)
            continue
        cell_key = validated["cell_key"]
        group_key = validated["effective_parent_key"]
        cell_groups.setdefault(cell_key, {}).setdefault(group_key, set()).add(validated["C_D"])

    cell_results: list[dict] = []
    positive_cell_count = 0
    for cell_key, groups in sorted(cell_groups.items()):
        mechanism_id, z_id, k_fail, k_unresolved = cell_key
        cross_parent_difference = False
        group_items = list(groups.items())
        for index, (left_key, left_values) in enumerate(group_items):
            for right_key, right_values in group_items[index + 1:]:
                if left_key == right_key:
                    continue
                if any(a != b for a in left_values for b in right_values):
                    cross_parent_difference = True
                    break
            if cross_parent_difference:
                break

        candidate = len(groups) >= 3 and cross_parent_difference
        if candidate:
            positive_cell_count += 1
        distinct_values = {
            value for values in groups.values() for value in values
        }
        cell_results.append({
            "mechanism_id": mechanism_id,
            "Z_id": z_id,
            "k_fail": k_fail,
            "k_unresolved": k_unresolved,
            "effective_parent_group_count_with_admissible_witnesses": len(groups),
            "distinct_C_D_value_count": len(distinct_values),
            "cross_parent_C_D_difference_found": cross_parent_difference,
            "status": (
                "POSITIVE_WITNESS_PATTERN_FOUND_PENDING_INDEPENDENT_SEMANTIC_REVIEW"
                if candidate
                else "NOT_ASSESSABLE_NO_POSITIVE_PATTERN_IN_SUBMITTED_DOSSIER"
            ),
        })

    overall = (
        "POSITIVE_WITNESS_PATTERN_FOUND_PENDING_INDEPENDENT_SEMANTIC_REVIEW"
        if positive_cell_count
        else "NO_POSITIVE_PATTERN_IN_SUBMITTED_DOSSIER_C6_NOT_ASSESSABLE"
    )
    return {
        "tool": TOOL_NAME,
        "tool_version": TOOL_VERSION,
        "label": LABEL,
        "dossier_decision": "MECHANICALLY_VALIDATED",
        "schema_sha256": _sha256(
            json.dumps(dossier_schema, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ),
        "binding_checks": binding_report,
        "reviewer_attestation": reviewer_report,
        "C4_scope": {
            "S_W_pair_count": len(s_w),
            "scope_rule": "C4 qualified pairs restricted to K1-K4",
        },
        "witness_counts": {
            "submitted": len(dossier["witnesses"]),
            "mechanically_admissible": len(valid_witnesses),
            "inadmissible": len(inadmissible_witnesses),
            "out_of_scope": len(out_of_scope_witnesses),
        },
        "inadmissible_witnesses": inadmissible_witnesses,
        "out_of_scope_witness_count": len(out_of_scope_witnesses),
        "cell_results": cell_results,
        "positive_witness_pattern_cell_count": positive_cell_count,
        "C6_status": overall,
        "domain_assessment_complete": False,
        "structural_absence_assessed": False,
        "audit_verdict": "NOT_ISSUED_COMPONENT_ONLY",
        "semantic_limit": (
            "Verbatim quote presence and reviewer-entered SUPPORTED decisions are "
            "mechanically checked only. This tool does not determine whether the rule "
            "semantically establishes mechanism reach or joint attainability. No "
            "structural absence or complete S_W x D assessment is represented."
        ),
        "boundary": (
            "This is a proposed companion dossier check only. It is not an A2 verdict, "
            "not an annex availability determination, not an owner authorization, and "
            "not a C6 semantic adjudication."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=LABEL)
    parser.add_argument("--dossier", required=True)
    parser.add_argument("--annex", required=True, help="private owner-supplied annex; keep local/private")
    parser.add_argument("--parent-identities", required=True)
    parser.add_argument("--family-map", required=True)
    parser.add_argument("--c4-report", required=True)
    parser.add_argument("--roster", required=True, help="exact adopted parent roster JSON whose bytes are pinned by C4")
    parser.add_argument("--report", required=True)
    args = parser.parse_args(argv)

    try:
        dossier, _dossier_raw = _load_object(Path(args.dossier))
        annex, annex_raw = _load_object(Path(args.annex))
        identities, identity_raw = _load_object(Path(args.parent_identities))
        family_map, family_map_raw = _load_object(Path(args.family_map))
        c4_report, c4_raw = _load_object(Path(args.c4_report))
        roster_path = Path(args.roster)
        roster, roster_raw = _load_object(roster_path)
        schema = _load_pinned_dossier_schema()
        annex_schema = (Path(__file__).resolve().parent / "ANNEX_INTAKE_FORM_SCHEMA.json")
        annex_schema_raw = annex_schema.read_bytes()
        from jsonschema import Draft202012Validator

        from validate_annex import load_and_verify_schema

        pinned_annex_schema = load_and_verify_schema(annex_schema)
        annex_errors = list(Draft202012Validator(
            pinned_annex_schema, format_checker=FormatChecker()
        ).iter_errors(annex))
        if annex_errors:
            raise DossierError("C6_OWNER_ANNEX_FAILS_PINNED_INTAKE_SCHEMA")
        _ = annex_schema_raw

        report = validate_c6_dossier(
            dossier=dossier,
            dossier_schema=schema,
            annex=annex,
            annex_raw=annex_raw,
            identity_manifest=identities,
            identity_raw=identity_raw,
            roster=roster,
            roster_raw=roster_raw,
            family_map=family_map,
            family_map_raw=family_map_raw,
            c4_report=c4_report,
            c4_raw=c4_raw,
            roster=roster,
        )
        report_raw = json.dumps(
            report, indent=2, sort_keys=True, ensure_ascii=False
        ) + "\n"
        Path(args.report).write_text(report_raw, encoding="utf-8", newline="\n")
        sys.stdout.write(json.dumps({
            "tool": TOOL_NAME,
            "status": report.get("dossier_decision"),
            "C6_status": report.get("C6_status"),
            "report_path": args.report,
            "audit_verdict": report.get("audit_verdict"),
            "semantic_limit": report.get("semantic_limit"),
        }, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        return 0 if report.get("dossier_decision") == "MECHANICALLY_VALIDATED" else 2
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, DossierError, ValueError) as exc:
        sys.stderr.write(f"C6_DOSSIER_CHECK_ERROR: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
