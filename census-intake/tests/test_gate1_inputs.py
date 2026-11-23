"""Tests for the Gate 1 inputs machinery (GLM 2026-11-23).

Covers: parent roster/family map integrity; the mutation-design annex
auditor's frozen-protocol rule checks (C1, C2, C3, C5) with synthetic
adversarial mutations; and end-to-end pre-registration manifest construction
in demo-synthetic mode, verified against the reviewed B1 v1.7 intake checker.
All identifiers, digests and timestamps in this file are invented; no real
allocation content exists anywhere in these tests (no-reconstruction rule).
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from itertools import combinations
from pathlib import Path

CENSUS_INTAKE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CENSUS_INTAKE))

import build_preregistration_manifest as builder  # noqa: E402
import validate_annex  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402


def _load(path: Path):
    return json.loads(path.read_bytes().decode("utf-8"))


ROSTER = _load(CENSUS_INTAKE / "gate1-inputs" / "PARENT_ROSTER_G01_G30.json")
FAMILY_MAP = _load(CENSUS_INTAKE / "gate1-inputs" / "FAMILY_MAP.json")
ANNEX_SCHEMA = validate_annex.load_and_verify_schema()


def synthetic_valid_annex() -> dict:
    mechs = [{"mechanism_id": f"M{i}", "name": f"SYNTHETIC mechanism {i}",
              "definition": f"SYNTHETIC definition {i} (invented for tests only)"}
             for i in range(1, 9)]
    parents = [p["parent_id"] for p in ROSTER["parents"]]
    pairs = list(combinations([f"M{i}" for i in range(1, 9)], 2))[:28]
    assignments = [
        {"parent_id": parents[i], "mechanism_a": pairs[i][0], "mechanism_b": pairs[i][1],
         "is_replication": False}
        for i in range(28)
    ] + [
        {"parent_id": parents[28], "mechanism_a": pairs[0][0], "mechanism_b": pairs[0][1],
         "is_replication": True, "preselection_evidence": "invented synthetic preselection note"},
        {"parent_id": parents[29], "mechanism_a": pairs[1][0], "mechanism_b": pairs[1][1],
         "is_replication": True, "preselection_evidence": "invented synthetic preselection note"},
    ]
    s_extra_mechs = [f"M{(i % 8) + 1}" for i in range(30)]
    return {
        "annex_id": "SYNTHETIC-ANNEX-001",
        "submitted_by": "SYNTHETIC",
        "submitted_at_utc": "2026-11-23T00:00:00Z",
        "provenance_statement": "SYNTHETIC provenance statement (invented).",
        "mechanisms": mechs,
        "pair_assignments": assignments,
        "replication_preselection": {
            "replicated_pair_1": {"mechanism_a": pairs[0][0], "mechanism_b": pairs[0][1]},
            "replicated_pair_2": {"mechanism_a": pairs[1][0], "mechanism_b": pairs[1][1]},
            "declared_before_construction": True,
        },
        "s_extra_assignments": [
            {"parent_id": parents[i], "mechanism_id": s_extra_mechs[i]} for i in range(30)
        ],
        "witness_declarations": {
            "cd_feasibility_witnesses_documented": True,
            "witness_notes": "SYNTHETIC witness notes (invented).",
        },
    }


class TestRosterAndFamilyMap(unittest.TestCase):
    def test_roster_has_30_unique_parents(self):
        ids = [p["parent_id"] for p in ROSTER["parents"]]
        self.assertEqual(len(ids), 30)
        self.assertEqual(len(set(ids)), 30)
        self.assertEqual(ids, [f"G{i:02d}" for i in range(1, 31)])

    def test_family_counts_match_frozen_design(self):
        counts = {"K1": 7, "K2": 8, "K3": 8, "K4": 5, "K5": 2}
        observed: dict[str, int] = {}
        for p in ROSTER["parents"]:
            observed[p["Z_id"]] = observed.get(p["Z_id"], 0) + 1
        self.assertEqual(observed, counts)
        self.assertEqual(ROSTER["family_counts"], counts)
        self.assertEqual(ROSTER["population_total"]["bodies"], 150)

    def test_family_map_partitions_match_roster(self):
        for zid, fam in FAMILY_MAP["families"].items():
            roster_members = sorted(p["parent_id"] for p in ROSTER["parents"] if p["Z_id"] == zid)
            self.assertEqual(sorted(fam["parents"]), roster_members)


class TestAnnexAuditor(unittest.TestCase):
    def setUp(self):
        self.valid = synthetic_valid_annex()
        report = validate_annex.audit_annex(self.valid, ROSTER, ANNEX_SCHEMA)
        self.assertEqual(report["audit_decision"], "ALL_LOCAL_RULES_PASS", report["reason_codes"])

    def audit(self, annex):
        return validate_annex.audit_annex(annex, ROSTER, ANNEX_SCHEMA)

    def test_missing_mechanism_fails_schema(self):
        annex = synthetic_valid_annex()
        annex["mechanisms"] = annex["mechanisms"][:7]
        report = self.audit(annex)
        self.assertIn("ANNEX_SCHEMA_VALIDATION_FAILED", report["reason_codes"])
        self.assertEqual(report["audit_decision"], "AUDIT_FAILED")
        self.assertEqual(report["schema_decision"], "REJECTED")

    def test_undefined_mechanism_fails_c1(self):
        annex = synthetic_valid_annex()
        annex["mechanisms"][3]["definition"] = "   "
        # minLength 1 still holds for whitespace; C1 requires non-blank content.
        schema_ok = Draft202012Validator(ANNEX_SCHEMA).is_valid(annex)
        self.assertTrue(schema_ok)
        report = self.audit(annex)
        self.assertIn("C1_MECHANISM_TAXONOMY_FAIL", report["reason_codes"])

    def test_missing_pair_fails_c2(self):
        annex = synthetic_valid_annex()
        annex["pair_assignments"][4] = dict(annex["pair_assignments"][0],
                                            parent_id="G05")
        report = self.audit(annex)
        self.assertTrue(
            any(c.startswith("C2_PAIR_MISSING") for c in report["reason_codes"]),
            report["reason_codes"],
        )

    def test_parent_assigned_twice_fails_c3(self):
        annex = synthetic_valid_annex()
        annex["pair_assignments"][4] = dict(annex["pair_assignments"][0])
        report = self.audit(annex)
        self.assertIn("C3_PARENT_ASSIGNED_MORE_THAN_ONCE: G01", report["reason_codes"])

    def test_orientation_inconsistency_fails_c3(self):
        annex = synthetic_valid_annex()
        rep = annex["pair_assignments"][28]
        rep["mechanism_a"], rep["mechanism_b"] = rep["mechanism_b"], rep["mechanism_a"]
        report = self.audit(annex)
        self.assertTrue(
            any(c.startswith("C3_ORIENTATION_INCONSISTENT") for c in report["reason_codes"]),
            report["reason_codes"],
        )

    def test_replication_without_preselection_evidence_fails_c2(self):
        annex = synthetic_valid_annex()
        annex["pair_assignments"][28].pop("preselection_evidence", None)
        report = self.audit(annex)
        self.assertIn(
            "C2_REPLICATION_PRESELECTION_EVIDENCE_MISSING: G29",
            report["reason_codes"],
        )

    def test_s_extra_imbalance_reported_and_fails_c5(self):
        annex = synthetic_valid_annex()
        first = annex["s_extra_assignments"][0]
        target = annex["s_extra_assignments"][7]
        target["mechanism_id"] = first["mechanism_id"]
        report = self.audit(annex)
        self.assertTrue(
            any(c.startswith("C5_BALANCE_DEVIATES") for c in report["reason_codes"]),
            report["reason_codes"],
        )

    def test_c7_reported_not_enforced(self):
        report = self.audit(synthetic_valid_annex())
        self.assertEqual(report["rules"]["C7_K5_scope_exclusion_notice"], "REPORTED")


class TestPreregistrationBuilderDemo(unittest.TestCase):
    def test_demo_manifest_passes_intake_checker(self):
        import validate_records

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "demo"
            argv = ["--demo-synthetic", "--out-dir", str(out)]
            rc = builder.main(argv)
            self.assertEqual(rc, 0)

            report = _load(out / "build_report.json")
            self.assertTrue(report["label"].startswith("SYNTHETIC DEMO"))
            self.assertEqual(report["variant_count"], 150)
            self.assertTrue(report["all_rows_not_started"])
            self.assertIsNone(report["first_diagnostic_execution_started_at_utc"])

            manifest_raw = (out / "preregistration_manifest.json").read_bytes()
            manifest = json.loads(manifest_raw.decode("utf-8"))
            schema = validate_records.load_and_verify_schema()
            sha = validate_records.hashlib.sha256(manifest_raw).hexdigest()
            result = validate_records.validate_manifest(manifest, sha, schema)
            self.assertEqual(
                result["manifest_decision"],
                "LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED",
                result["manifest_reason_codes"],
            )
            self.assertTrue(result["manifest_schema_valid"])
            self.assertEqual(len(result["variants"]), 150)
            self.assertTrue(
                all(v["validity_status"] == "EXPECTED_NOT_RUN" for v in manifest["variants"])
            )
            self.assertTrue(
                all(v["measurement"]["state"] == "NO_DIAGNOSTIC_MEASUREMENT"
                    for v in result["variants"])
            )
            self.assertIsNone(
                manifest["diagnostic_run_start_ledger"]["first_diagnostic_execution_started_at_utc"]
            )
            self.assertEqual(
                manifest["outcome_exclusion_assertion"],
                {"correctness_outcomes_included": False,
                 "outcomes_consulted": False,
                 "model_outputs_included": False},
            )

    def test_real_mode_requires_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                builder.main(["--out-dir", tmp])


if __name__ == "__main__":
    unittest.main()
