"""Synthetic tests for the B1 v1.7 census intake validator v0.2.

No bank, solver, diagnostic-run or outcome data is used. All identifiers are invented.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FOLDER = ROOT / "census-intake"
sys.path.insert(0, str(FOLDER))

import validate_records as v  # noqa: E402

STRATA = [f"D{j}" for j in range(1, 9)]
F = [3, 1, 0, 2, 0, 0, 1, 0]
U = [1, 1, 2, 0, 1, 0, 0, 3]
DIGEST = "a" * 64
LABEL = "SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED"


def make_results(prefix: str = "v1", f=None, u=None):
    f = list(F if f is None else f)
    u = list(U if u is None else u)
    results = []
    for j, stratum in enumerate(STRATA):
        statuses = (
            ["DEFINITE_FAILURE"] * f[j]
            + ["UNRESOLVED"] * u[j]
            + ["DEFINITE_PASS"] * (8 - f[j] - u[j])
        )
        for i, status in enumerate(statuses):
            results.append(
                {
                    "diagnostic_record_id": f"{prefix}-{stratum}-r{i}",
                    "stratum_id": stratum,
                    "terminal_status": status,
                }
            )
    return results


def make_valid(variant_id="v1", parent_id="p1", prefix=None):
    return {
        "variant_id": variant_id,
        "parent_id": parent_id,
        "Z_id": "Z1",
        "q_id": "q1",
        "validity_status": "VALID",
        "diagnostic_record_results": make_results(prefix or variant_id),
        "semantic_source_digest": DIGEST,
        "runnable_artifact_digest": DIGEST,
        "diagnostic_evidence_ref": {"evidence_id": "ev-1", "sha256": DIGEST},
    }


def make_status_variant(status: str, results=None, **overrides):
    rec = {
        "variant_id": "sv-" + status.lower(),
        "parent_id": "p1",
        "Z_id": "Z1",
        "q_id": "q1",
        "validity_status": status,
        "diagnostic_record_results": [] if results is None else results,
        "status_reason": "audit reason",
        "status_decision": {
            "rule_ref": "rule-1",
            "decision_record_ref": {"evidence_id": "ev-d", "sha256": DIGEST},
            "decided_at_utc": "2026-11-22T00:00:00Z",
            "decision_basis": {
                "INVALID": "PREDIAGNOSTIC_OBJECTIVE_INVALIDITY",
                "EXCLUDED_BEFORE_DIAGNOSTICS": "PREDIAGNOSTIC_DESIGN_EXCLUSION",
                "INCOMPLETE": "POSTRUN_COMPLETENESS_AUDIT",
                "EXPECTED_NOT_RUN": "EXPECTED_NOT_RUN_INVENTORY_AUDIT",
            }[status],
            "diagnostic_terminal_values_consulted": False,
            "derived_failure_unresolved_counts_consulted": False,
            "record_presence_identity_metadata_consulted": status == "INCOMPLETE",
        },
    }
    if status == "INCOMPLETE":
        rec["diagnostic_evidence_ref"] = {"evidence_id": "ev-i", "sha256": DIGEST}
    rec.update(overrides)
    return rec


def make_manifest(variants=None, basis="record_level_64"):
    return {
        "schema_version": "0.6-draft",
        "study_id": "LC518",
        "measurement_basis": basis,
        "diagnostic_bank": {
            "stratum_ids": STRATA,
            "records_per_stratum": 8,
            "total_records": 64,
        },
        "parent_roster": [{"parent_id": "p1", "Z_id": "Z1"}],
        "variants": [make_valid()] if variants is None else variants,
        "outcome_exclusion_assertion": {
            "correctness_outcomes_included": False,
            "outcomes_consulted": False,
            "model_outputs_included": False,
        },
    }


def rep(manifest, digest="b" * 64):
    return v.validate_census_manifest(manifest, digest)


class IntakeV02Tests(unittest.TestCase):
    def test_valid_variant_admitted_and_derived(self):
        r = rep(make_manifest())
        self.assertEqual(r["rejected"], 0)
        d = r["records"][0]["derived"]
        self.assertEqual(d["f"], F)
        self.assertEqual(d["u"], U)
        self.assertEqual(sum(d["p"]), 64 - sum(F) - sum(U))
        self.assertEqual(d["k_fail"], sum(F))
        self.assertEqual(d["k_unresolved"], sum(U))
        self.assertEqual(d["c_d"], "3/7")
        self.assertEqual(d["cell"], ["q1", "Z1", sum(F), sum(U)])

    def test_empty_manifest_rejected(self):
        r = rep([])
        self.assertIn("EMPTY_MANIFEST", r["manifest_reason_codes"])

    def test_non_string_basis_all_types_controlled(self):
        for label, basis in [
            ("list", ["record_level_64"]),
            ("dict", {"x": 1}),
            ("number", 64),
            ("bool", True),
            ("null", None),
        ]:
            with self.subTest(label=label):
                r = rep(make_manifest(basis=basis))
                self.assertIn("NON_STRING_EXPOSURE_BASIS", r["manifest_reason_codes"])

    def test_unsupported_string_basis_rejected(self):
        for basis in ("canonical_60", "record", "canonical"):
            with self.subTest(basis=basis):
                r = rep(make_manifest(basis=basis))
                self.assertIn("UNSUPPORTED_EXPOSURE_BASIS", r["manifest_reason_codes"])

    def test_63_or_65_results_rejected(self):
        for n in (63, 65):
            with self.subTest(n=n):
                variant = make_valid()
                if n == 65:
                    results = make_results()
                    results.append(
                        {
                            "diagnostic_record_id": "v1-D1-extra",
                            "stratum_id": "D1",
                            "terminal_status": "DEFINITE_PASS",
                        }
                    )
                else:
                    results = make_results()[:n]
                variant["diagnostic_record_results"] = results
                r = rep(make_manifest([variant]))
                codes = r["records"][0]["reason_codes"]
                self.assertTrue({"VALID_RESULT_COUNT", "TOO_MANY_RESULTS"} & set(codes))

    def test_wrong_stratum_count_rejected(self):
        variant = make_valid()
        results = make_results()
        results[0]["stratum_id"] = "D2"
        variant["diagnostic_record_results"] = results
        r = rep(make_manifest([variant]))
        self.assertIn("STRATUM_RESULT_COUNT", r["records"][0]["reason_codes"])

    def test_invalid_terminal_status_rejected(self):
        variant = make_valid()
        variant["diagnostic_record_results"][0]["terminal_status"] = "TIMEOUT"
        r = rep(make_manifest([variant]))
        self.assertIn("INVALID_TERMINAL_STATUS", r["records"][0]["reason_codes"])

    def test_duplicate_record_id_within_variant_rejected(self):
        variant = make_valid()
        variant["diagnostic_record_results"][1]["diagnostic_record_id"] = (
            variant["diagnostic_record_results"][0]["diagnostic_record_id"]
        )
        r = rep(make_manifest([variant]))
        self.assertIn("DUPLICATE_RECORD_ID", r["records"][0]["reason_codes"])

    def test_same_id_set_reused_across_variants_accepted(self):
        v2 = make_valid("v2", prefix="v1")  # same frozen record IDs, different variant
        r = rep(make_manifest([make_valid(), v2]))
        self.assertEqual(r["rejected"], 0)

    def test_different_id_sets_rejected(self):
        r = rep(make_manifest([make_valid("v1"), make_valid("v2", prefix="v2")]))
        self.assertIn("CROSS_VARIANT_ID_SET_MISMATCH", r["manifest_reason_codes"])

    def test_absent_aggregates_derived(self):
        r = rep(make_manifest())
        self.assertEqual(r["records"][0]["aggregate_check"], "absent")
        self.assertEqual(r["records"][0]["derived"]["f"], F)

    def test_matching_aggregates_are_consistency_only(self):
        variant = make_valid()
        results = variant["diagnostic_record_results"]
        variant.update(
            {
                "f": [sum(1 for r in results if r["stratum_id"] == s and r["terminal_status"] == "DEFINITE_FAILURE") for s in STRATA],
                "u": [sum(1 for r in results if r["stratum_id"] == s and r["terminal_status"] == "UNRESOLVED") for s in STRATA],
                "p": [sum(1 for r in results if r["stratum_id"] == s and r["terminal_status"] == "DEFINITE_PASS") for s in STRATA],
            }
        )
        r = rep(make_manifest([variant]))
        self.assertEqual(r["rejected"], 0)
        self.assertEqual(r["records"][0]["aggregate_check"], "consistent")

    def test_conflicting_aggregate_rejected(self):
        variant = make_valid()
        variant["f"] = [8] * 8
        r = rep(make_manifest([variant]))
        self.assertIn("AGGREGATE_MISMATCH", r["records"][0]["reason_codes"])

    def test_malformed_aggregate_rejected(self):
        variant = make_valid()
        variant["u"] = [0] * 7
        r = rep(make_manifest([variant]))
        self.assertIn("MALFORMED_AGGREGATE", r["records"][0]["reason_codes"])

    def test_zero_failures_exact_label(self):
        variant = make_valid()
        variant["diagnostic_record_results"] = make_results(f=[0] * 8)
        r = rep(make_manifest([variant]))
        d = r["records"][0]["derived"]
        self.assertEqual(d["c_d"], "NO OBSERVED FAILURES")
        self.assertNotIn("c_d_numeric", d)

    def test_unresolved_does_not_enter_c_d(self):
        a = make_valid()
        b = make_valid()
        a["diagnostic_record_results"] = make_results(f=F, u=[0] * 8)
        b["diagnostic_record_results"] = make_results(f=F, u=U)
        da = rep(make_manifest([a]))["records"][0]["derived"]
        db = rep(make_manifest([b]))["records"][0]["derived"]
        self.assertEqual(da["c_d"], db["c_d"])

    def test_incomplete_status_rules(self):
        variant = make_status_variant("INCOMPLETE", results=make_results()[:10])
        r = rep(make_manifest([variant]))
        self.assertEqual(r["rejected"], 0)
        self.assertEqual(r["records"][0]["derived"]["c_d_status"], "NOT_APPLICABLE")

    def test_zero_result_statuses_admitted(self):
        for status in ("INVALID", "EXCLUDED_BEFORE_DIAGNOSTICS", "EXPECTED_NOT_RUN"):
            with self.subTest(status=status):
                r = rep(make_manifest([make_status_variant(status)]))
                self.assertEqual(r["rejected"], 0, r["records"][0]["reason_codes"])

    def test_zero_result_status_with_results_rejected(self):
        variant = make_status_variant("EXPECTED_NOT_RUN", results=make_results()[:1])
        r = rep(make_manifest([variant]))
        self.assertIn("NONZERO_RESULTS_FOR_STATUS", r["records"][0]["reason_codes"])

    def test_incomplete_without_decision_rejected(self):
        variant = make_status_variant("INCOMPLETE", results=make_results()[:2])
        del variant["status_decision"]
        r = rep(make_manifest([variant]))
        self.assertIn("INVALID_STATUS_DECISION", r["records"][0]["reason_codes"])

    def test_parent_z_mismatch_rejected(self):
        manifest = make_manifest()
        manifest["variants"][0]["Z_id"] = "Z9"
        r = rep(manifest)
        self.assertIn("PARENT_Z_MISMATCH", r["records"][0]["reason_codes"])

    def test_outcome_exclusion_assertion_enforced(self):
        manifest = make_manifest()
        manifest["outcome_exclusion_assertion"]["outcomes_consulted"] = True
        r = rep(manifest)
        self.assertIn("OUTCOME_EXCLUSION_ASSERTION_FAILED", r["manifest_reason_codes"])

    def test_report_label_determinism_and_no_census_verdict(self):
        manifest = make_manifest()
        first = rep(manifest, "c" * 64)
        second = rep(manifest, "c" * 64)
        self.assertEqual(first["intake_label"], LABEL)
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))
        self.assertEqual(first["manifest_sha256"], "c" * 64)
        text = json.dumps(first).lower()
        for token in ("eligible", "lopo", "gate 1 pass", "provenance verified"):
            self.assertNotIn(token, text)

    def test_schema_id_matches_version(self):
        schema = json.loads((FOLDER / "record_schema.json").read_text(encoding="utf-8"))
        self.assertTrue(schema["$id"].endswith(f"/v{schema['schema_version']}.json"))

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good.json"
            bad = Path(tmp) / "bad.json"
            empty = Path(tmp) / "empty.json"
            good.write_text(json.dumps(make_manifest()), encoding="utf-8")
            bad.write_text(json.dumps(make_manifest(basis=["record_level_64"])), encoding="utf-8")
            empty.write_text("[]", encoding="utf-8")
            for path, expected in ((good, 0), (bad, 2), (empty, 2)):
                result = subprocess.run(
                    [sys.executable, str(FOLDER / "validate_records.py"), "--manifest", str(path)],
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, expected, (path.name, result.stderr))


if __name__ == "__main__":
    unittest.main()
