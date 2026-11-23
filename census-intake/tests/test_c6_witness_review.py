"""Synthetic tests for the proposed C6 witness-dossier checker.

All annex text, identities, hashes and witnesses are invented test fixtures.
They are not LC518 owner allocations, actual parent sources or scientific
findings. The tests verify mechanical handling only.
"""

from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path

CENSUS_INTAKE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CENSUS_INTAKE))
sys.path.insert(0, str(CENSUS_INTAKE / "tests"))

import validate_annex  # noqa: E402
import validate_c6_witness_review as c6_checker  # noqa: E402
from test_gate1_inputs import (  # noqa: E402
    ANNEX_SCHEMA,
    ROSTER,
    ROSTER_RAW,
    ROSTER_SHA256,
    synthetic_adopted_family_map,
    synthetic_parent_identities,
    synthetic_valid_annex,
)


def canonical_json_bytes(value: dict) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def prepare_inputs(duplicate_base_ids: bool = False) -> dict:
    annex = synthetic_valid_annex()
    annex_raw = canonical_json_bytes(annex)

    family_map, _ = synthetic_adopted_family_map()
    family_map_raw = canonical_json_bytes(family_map)
    family_map_sha = hashlib.sha256(family_map_raw).hexdigest()

    identities = synthetic_parent_identities(family_map, family_map_sha)
    if duplicate_base_ids:
        # Same-family duplicates are retained as separate IDs but represent one
        # effective base parent group under Rev 11 C4.
        for index in (1, 2):
            identities["parents"][index]["base_source_sha256"] = (
                identities["parents"][0]["base_source_sha256"]
            )
    bundle_rows = [
        {
            "parent_id": row["parent_id"],
            "base_source_path": row["base_source_path"],
            "base_source_sha256": row["base_source_sha256"],
        }
        for row in identities["parents"]
    ]
    identities["source_hash_attestation"]["source_bundle_sha256"] = hashlib.sha256(
        json.dumps(
            bundle_rows, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()
    identity_raw = canonical_json_bytes(identities)
    identity_sha = hashlib.sha256(identity_raw).hexdigest()

    family_map_sha = hashlib.sha256(family_map_raw).hexdigest()
    c4_report = validate_annex.audit_annex(
        annex,
        ROSTER,
        ANNEX_SCHEMA,
        identities,
        identity_sha,
        family_map,
        family_map_sha,
        ROSTER_SHA256,
    )
    if c4_report["audit_decision"] != "STRUCTURAL_INTAKE_PASS_C6_ADEQUACY_NOT_ASSESSED":
        raise AssertionError(c4_report["reason_codes"])
    c4_report["annex_sha256"] = hashlib.sha256(annex_raw).hexdigest()
    c4_raw = canonical_json_bytes(c4_report)

    return {
        "annex": annex,
        "annex_raw": annex_raw,
        "identity_manifest": identities,
        "identity_raw": identity_raw,
        "roster": ROSTER,
        "roster_raw": ROSTER_RAW,
        "family_map": family_map,
        "family_map_raw": family_map_raw,
        "c4_report": c4_report,
        "c4_raw": c4_raw,
        "dossier": None,
        "dossier_schema": c6_checker._load_pinned_dossier_schema(),
    }


def make_witness(parent_id: str, f: list[int], u: list[int] | None = None,
                 *, reach_decision: str = "SUPPORTED",
                 quote: str | None = None) -> dict:
    if u is None:
        u = [0] * 8
    role = "SA"
    mechanism_id = "M1"
    definition = f"SYNTHETIC definition 1 (invented for tests only)"
    use_quote = quote or definition
    reach_rows = [
        {
            "stratum_id": f"D{index + 1}",
            "decision": reach_decision,
            "quoted_rule": use_quote,
            "rationale": "SYNTHETIC reviewer rationale only",
        }
        for index, count in enumerate(f)
        if count > 0
    ]
    unresolved = [
        {
            "stratum_id": f"D{index + 1}",
            "origin": "PROCESS_ATTRIBUTED",
            "evidence_reference": "SYNTHETIC process evidence reference",
            "rationale": "SYNTHETIC unresolved provenance rationale",
        }
        for index, count in enumerate(u)
        if count > 0
    ]
    return {
        "witness_id": f"SYN-WITNESS-{parent_id}-{sum(f)}-{sum(u)}",
        "parent_id": parent_id,
        "version_slot_id": f"{parent_id}:{role}",
        "version_role": role,
        "mechanism_id": mechanism_id,
        "Z_id": "K1",
        "cell": {"k_fail": sum(f), "k_unresolved": sum(u)},
        "f": f,
        "u": u,
        "reach_assessments": reach_rows,
        "joint_attainability": {
            "decision": "SUPPORTED",
            "quoted_rule": use_quote,
            "rationale": "SYNTHETIC joint-attainability rationale only",
        },
        "unresolved_provenance": unresolved,
    }


def make_dossier(data: dict, witnesses: list[dict]) -> dict:
    return {
        "dossier_id": "SYNTHETIC-C6-DOSSIER",
        "version": "1.0",
        "annex_sha256": hashlib.sha256(data["annex_raw"]).hexdigest(),
        "parent_identity_manifest_sha256": hashlib.sha256(data["identity_raw"]).hexdigest(),
        "parent_roster_sha256": hashlib.sha256(data["roster_raw"]).hexdigest(),
        "family_map_sha256": hashlib.sha256(data["family_map_raw"]).hexdigest(),
        "c4_report_sha256": hashlib.sha256(data["c4_raw"]).hexdigest(),
        "design_basis": {
            "N": 64,
            "unit": "diagnostic_bank_records_per_solver_body",
            "R": [8] * 8,
            "bank_design_sha256": c6_checker.EXPECTED_BANK_DESIGN_SHA256,
        },
        "reviewer_attestation": {
            "reviewer_id": "SYNTHETIC TEST REVIEWER",
            "not_annex_author_or_coauthor": True,
            "no_role_in_taxonomy": True,
            "no_role_in_pair_assignments": True,
            "no_role_in_s_extra_design": True,
            "not_availability_investigator": True,
            "attestation_recorded_at_utc": "2026-11-23T00:00:00Z",
            "first_annex_access_at_utc": "2026-11-23T01:00:00Z",
            "review_completed_at_utc": "2026-11-23T02:00:00Z",
        },
        "witnesses": witnesses,
    }


def run_checker(data: dict, dossier: dict) -> dict:
    return c6_checker.validate_c6_dossier(
        dossier=dossier,
        dossier_schema=data["dossier_schema"],
        annex=data["annex"],
        annex_raw=data["annex_raw"],
        identity_manifest=data["identity_manifest"],
        identity_raw=data["identity_raw"],
        roster=data["roster"],
        roster_raw=data["roster_raw"],
        family_map=data["family_map"],
        family_map_raw=data["family_map_raw"],
        c4_report=data["c4_report"],
        c4_raw=data["c4_raw"],
        roster=ROSTER,
    )


class TestC6WitnessDossierMechanicalChecks(unittest.TestCase):
    def setUp(self):
        self.data = prepare_inputs()

    def test_three_parents_and_cross_parent_different_cd_flag_candidate_only(self):
        witnesses = [
            make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0]),
            make_witness("G02", [1, 1, 0, 0, 0, 0, 0, 0]),
            make_witness("G03", [2, 0, 0, 0, 0, 0, 0, 0]),
        ]
        result = run_checker(self.data, make_dossier(self.data, witnesses))
        self.assertEqual(result["dossier_decision"], "MECHANICALLY_VALIDATED")
        self.assertEqual(result["C6_status"],
                         "POSITIVE_WITNESS_PATTERN_FOUND_PENDING_INDEPENDENT_SEMANTIC_REVIEW")
        self.assertEqual(result["positive_witness_pattern_cell_count"], 1)
        self.assertEqual(result["audit_verdict"], "NOT_ISSUED_COMPONENT_ONLY")
        self.assertFalse(result["domain_assessment_complete"])

    def test_three_parents_with_same_cd_do_not_create_candidate(self):
        witnesses = [
            make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0]),
            make_witness("G02", [2, 0, 0, 0, 0, 0, 0, 0]),
            make_witness("G03", [2, 0, 0, 0, 0, 0, 0, 0]),
        ]
        result = run_checker(self.data, make_dossier(self.data, witnesses))
        self.assertEqual(
            result["C6_status"],
            "NO_POSITIVE_PATTERN_IN_SUBMITTED_DOSSIER_C6_NOT_ASSESSABLE",
        )
        self.assertEqual(result["positive_witness_pattern_cell_count"], 0)

    def test_multiple_parent_ids_with_same_base_hash_count_as_one_group(self):
        data = prepare_inputs(duplicate_base_ids=True)
        witnesses = [
            make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0]),
            make_witness("G02", [1, 1, 0, 0, 0, 0, 0, 0]),
            make_witness("G03", [2, 0, 0, 0, 0, 0, 0, 0]),
        ]
        result = run_checker(data, make_dossier(data, witnesses))
        self.assertEqual(result["positive_witness_pattern_cell_count"], 0)
        cell = result["cell_results"][0]
        self.assertEqual(
            cell["effective_parent_group_count_with_admissible_witnesses"], 1
        )

    def test_nonzero_unresolved_component_requires_provenance(self):
        witness = make_witness(
            "G01",
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
        )
        witness["unresolved_provenance"] = []
        result = run_checker(self.data, make_dossier(self.data, [witness]))
        self.assertEqual(result["witness_counts"]["inadmissible"], 1)
        self.assertIn(
            "C6_UNRESOLVED_PROVENANCE_COVERAGE_MISMATCH",
            result["inadmissible_witnesses"][0]["reason"],
        )

    def test_reach_quote_must_appear_verbatim_in_mechanism_definition(self):
        witness = make_witness(
            "G01",
            [2, 0, 0, 0, 0, 0, 0, 0],
            quote="plausible but invented quote not in source",
        )
        result = run_checker(self.data, make_dossier(self.data, [witness]))
        self.assertEqual(result["witness_counts"]["inadmissible"], 1)
        self.assertIn(
            "QUOTE_NOT_FOUND_VERBATIM_IN_PINNED_DEFINITION",
            result["inadmissible_witnesses"][0]["reason"],
        )

    def test_non_supported_reach_decision_discards_witness_not_as_absence(self):
        witness = make_witness(
            "G01",
            [2, 0, 0, 0, 0, 0, 0, 0],
            reach_decision="NOT_ESTABLISHED",
        )
        result = run_checker(self.data, make_dossier(self.data, [witness]))
        self.assertEqual(result["witness_counts"]["inadmissible"], 1)
        self.assertIn(
            "C6_NONZERO_FAILURE_REACH_NOT_SUPPORTED",
            result["inadmissible_witnesses"][0]["reason"],
        )
        self.assertIn(
            "NOT_STRUCTURAL_ABSENCE",
            result["inadmissible_witnesses"][0]["disposition"],
        )

    def test_wrong_role_to_mechanism_assignment_is_discarded(self):
        witness = make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0])
        witness["mechanism_id"] = "M8"
        result = run_checker(self.data, make_dossier(self.data, [witness]))
        self.assertEqual(result["witness_counts"]["inadmissible"], 1)
        self.assertIn(
            "C6_WITNESS_ROLE_MECHANISM_MISMATCH",
            result["inadmissible_witnesses"][0]["reason"],
        )

    def test_artifact_binding_mismatch_blocks_dossier(self):
        dossier = make_dossier(
            self.data,
            [make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0])],
        )
        dossier["annex_sha256"] = "0" * 64
        with self.assertRaisesRegex(c6_checker.DossierError,
                                    "C6_DOSSIER_ARTIFACT_BINDING_MISMATCH:annex_sha256"):
            run_checker(self.data, dossier)

    def test_dossier_is_bound_to_exact_roster_bytes(self):
        dossier = make_dossier(
            self.data,
            [make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0])],
        )
        dossier["parent_roster_sha256"] = "0" * 64
        with self.assertRaisesRegex(
            c6_checker.DossierError,
            "C6_DOSSIER_ARTIFACT_BINDING_MISMATCH:parent_roster_sha256",
        ):
            run_checker(self.data, dossier)

    def test_unadopted_roster_is_rejected_for_c6_review(self):
        data = dict(self.data)
        data["roster"] = dict(self.data["roster"])
        data["roster"]["status"] = "PENDING_ADOPTION"
        dossier = make_dossier(
            data,
            [make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0])],
        )
        with self.assertRaisesRegex(
            c6_checker.DossierError, "C6_PARENT_ROSTER_NOT_ADOPTED"
        ):
            run_checker(data, dossier)

    def test_incomplete_c4_incidence_table_is_rejected(self):
        data = dict(self.data)
        data["c4_report"] = json.loads(json.dumps(self.data["c4_report"]))
        data["c4_report"]["C4"]["n_m_z"].pop()
        data["c4_raw"] = canonical_json_bytes(data["c4_report"])
        dossier = make_dossier(
            data,
            [make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0])],
        )
        with self.assertRaisesRegex(
            c6_checker.DossierError,
            "C6_C4_INCIDENCE_TABLE_NOT_EXACTLY_40_CELLS",
        ):
            run_checker(data, dossier)

    def test_c4_report_annex_binding_must_match(self):
        data = dict(self.data)
        data["c4_report"] = json.loads(json.dumps(self.data["c4_report"]))
        data["c4_report"]["annex_sha256"] = "0" * 64
        data["c4_raw"] = canonical_json_bytes(data["c4_report"])
        dossier = make_dossier(
            data,
            [make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0])],
        )
        with self.assertRaisesRegex(
            c6_checker.DossierError, "C6_C4_REPORT_ANNEX_BINDING_INVALID"
        ):
            run_checker(data, dossier)

    def test_attestation_must_precede_first_annex_access(self):
        dossier = make_dossier(
            self.data,
            [make_witness("G01", [2, 0, 0, 0, 0, 0, 0, 0])],
        )
        dossier["reviewer_attestation"]["attestation_recorded_at_utc"] = (
            "2026-11-23T01:30:00Z"
        )
        with self.assertRaisesRegex(c6_checker.DossierError,
                                    "C6_REVIEWER_ATTESTATION_NOT_RECORDED_BEFORE_ANNEX_ACCESS"):
            run_checker(self.data, dossier)

    def test_c5_family_k5_witness_is_out_of_scope_for_inference(self):
        witness = make_witness("G29", [2, 0, 0, 0, 0, 0, 0, 0])
        witness["Z_id"] = "K5"
        # G29's SA role is M1, and its actual roster family is K5.
        result = run_checker(self.data, make_dossier(self.data, [witness]))
        self.assertEqual(result["positive_witness_pattern_cell_count"], 0)
        self.assertEqual(result["out_of_scope_witness_count"], 1)
        self.assertEqual(
            result["C6_status"],
            "NO_POSITIVE_PATTERN_IN_SUBMITTED_DOSSIER_C6_NOT_ASSESSABLE",
        )


if __name__ == "__main__":
    unittest.main()
