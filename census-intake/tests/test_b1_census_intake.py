"""Adversarial synthetic tests for the schema-exact B1 v1.7 intake validator.

Every fixture is invented. No bank, solver, diagnostic run, external evidence, or outcomes are read.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import validate_records as v  # noqa: E402

STRATA = [f"D{i}" for i in range(1, 9)]
DIGEST = "a" * 64
SHA1 = "b" * 40
FIRST_START = "2026-11-23T10:00:00Z"
SNAPSHOT = "2026-11-23T12:00:00Z"


def blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def artifact_ref(name="artifact"):
    return {"artifact_id": name, "version": "1", "git_blob_sha1": SHA1, "sha256": DIGEST}


def evidence_ref(name="evidence"):
    return {"evidence_id": name, "sha256": DIGEST}


def make_results(f=None, u=None, prefix="bank"):
    f = list(f if f is not None else [3, 1, 0, 2, 0, 0, 1, 0])
    u = list(u if u is not None else [1, 1, 2, 0, 1, 0, 0, 3])
    out = []
    for j, stratum in enumerate(STRATA):
        statuses = (["DEFINITE_FAILURE"] * f[j] + ["UNRESOLVED"] * u[j]
                    + ["DEFINITE_PASS"] * (8 - f[j] - u[j]))
        for i, terminal in enumerate(statuses):
            out.append({"diagnostic_record_id": f"{prefix}-{stratum}-{i}",
                        "stratum_id": stratum, "terminal_status": terminal})
    return out


def status_decision(status, decided_at=None, **overrides):
    basis = {
        "INVALID": "PREDIAGNOSTIC_OBJECTIVE_INVALIDITY",
        "EXCLUDED_BEFORE_DIAGNOSTICS": "PREDIAGNOSTIC_DESIGN_EXCLUSION",
        "INCOMPLETE": "POSTRUN_COMPLETENESS_AUDIT",
        "EXPECTED_NOT_RUN": "EXPECTED_NOT_RUN_INVENTORY_AUDIT",
    }[status]
    result = {
        "rule_ref": artifact_ref("status-rule"),
        "decision_record_ref": evidence_ref("decision-record"),
        "decided_at_utc": decided_at or ("2026-11-23T11:00:00Z" if status == "EXPECTED_NOT_RUN"
                                          else "2026-11-23T09:00:00Z" if status in {"INVALID", "EXCLUDED_BEFORE_DIAGNOSTICS"}
                                          else "2026-11-23T11:00:00Z"),
        "decision_basis": basis,
        "diagnostic_terminal_values_consulted": False,
        "derived_failure_unresolved_counts_consulted": False,
        "record_presence_identity_metadata_consulted": status == "INCOMPLETE",
    }
    result.update(overrides)
    return result


def make_variant(status="VALID", variant_id="v1", parent_id="p1", prefix="bank", **overrides):
    row = {
        "variant_id": variant_id,
        "parent_id": parent_id,
        "Z_id": "Z1",
        "q_id": "q1",
        "validity_status": status,
        "diagnostic_record_results": make_results(prefix=prefix) if status == "VALID" else [],
    }
    if status == "VALID":
        row.update({
            "semantic_source_digest": DIGEST,
            "runnable_artifact_digest": "c" * 64,
            "diagnostic_evidence_ref": evidence_ref("diagnostic-evidence"),
        })
    else:
        row["status_reason"] = "predeclared synthetic status reason"
        row["status_decision"] = status_decision(status)
        if status == "INCOMPLETE":
            row["diagnostic_record_results"] = make_results(prefix=prefix)[:13]
            row["diagnostic_evidence_ref"] = evidence_ref("incomplete-receipt")
    row.update(overrides)
    return row


def make_manifest(variants=None):
    return {
        "schema_version": "0.6-draft",
        "study_id": "LC518",
        "analysis_plan": {
            "name": "B1", "version": "1.7",
            "git_blob_sha1": "8c666e501a31726c728447d155045c0b20adc178",
            "sha256": "797bd9f72cf94fdc0eff4a03b1544823d4042f8e530b27f4fb70cbd7f2baca7c",
        },
        "measurement_spec": {
            "name": "C_D measurement specification and exposure register",
            "date": "2026-11-19",
            "git_blob_sha1": "923655f20337b99f11e400f3428d1d18ac34c96d",
        },
        "measurement_basis": "record_level_64",
        "evaluation_row_basis": {"row_count": 78, "source_ref": artifact_ref("evaluation-rows")},
        "diagnostic_bank": {
            "bank_id": "synthetic-bank", "version": "synthetic-v1",
            "sha256": DIGEST, "record_manifest_sha256": "d" * 64,
            "stratum_ids": STRATA, "records_per_stratum": 8, "total_records": 64,
        },
        "diagnostic_exposure_disclosure": {
            "historical_public_heldout_bank_status": "PUBLICLY_EXPOSED",
            "historical_used_for_candidate_filtering": True,
            "historical_selection_history_status": "NOT_RECONSTRUCTED",
            "historical_selection_description": "Synthetic fixture; historical evidence not accessed.",
            "future_bank_generation_selection_status": "NOT_YET_SPECIFIED",
            "independence_claim_permitted": False,
            "evidence_refs": [],
        },
        "parent_roster_ref": artifact_ref("parent-roster"),
        "q_registry_ref": artifact_ref("q-registry"),
        "family_map_ref": artifact_ref("family-map"),
        "variant_inventory_ref": artifact_ref("variant-inventory"),
        "diagnostic_run_start_ledger": {
            "ledger_ref": evidence_ref("run-start-ledger"),
            "first_diagnostic_execution_started_at_utc": FIRST_START,
            "snapshot_as_of_utc": SNAPSHOT,
        },
        "provenance": {
            "generation_record_ref": evidence_ref("generation-record"),
            "build_record_ref": evidence_ref("build-record"),
            "diagnostic_run_record_ref": evidence_ref("diagnostic-run-record"),
        },
        "parent_roster": [{"parent_id": "p1", "Z_id": "Z1"}],
        "variants": [make_variant()] if variants is None else variants,
        "outcome_exclusion_assertion": {
            "correctness_outcomes_included": False,
            "outcomes_consulted": False,
            "model_outputs_included": False,
        },
    }


def manifest_result(manifest):
    raw = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
    schema = v.load_and_verify_schema()
    return v.validate_manifest(manifest, hashlib.sha256(raw).hexdigest(), schema), raw


class B1IntakeV03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = v.load_and_verify_schema()
        Draft = __import__("jsonschema").Draft202012Validator
        Draft.check_schema(cls.schema)
        cls.sidecar_schema_raw = v._sidecar_schema_path().read_bytes()
        cls.sidecar_schema_sha = blob_sha1(cls.sidecar_schema_raw)

    def test_packaged_manifest_schema_exact_source_identity(self):
        raw = v._schema_path().read_bytes()
        self.assertEqual(v.SCHEMA_SOURCE_BLOB_SHA1, "0f2865e606fa61400184c09abd01601497637a6b")
        self.assertEqual(blob_sha1(raw), v.SCHEMA_SOURCE_BLOB_SHA1)
        self.assertEqual(self.schema["$id"], v.SCHEMA_ID)
        self.assertEqual(len(self.schema["required"]), 17)
        self.assertFalse(self.schema["additionalProperties"])

"def test_sidecar_schema_blob_is_pinned_in_validator(self):
        self.assertEqual(self.sidecar_schema_sha, v.SIDECAR_SCHEMA_BLOB_SHA1)

    def test_complete_17_field_manifest_passes_schema_and_local_checks(self):
        r, _ = manifest_result(make_manifest())
        self.assertTrue(r["manifest_schema_valid"], r["schema_issues"])
        self.assertEqual(r["manifest_decision"], "LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED")
        self.assertEqual(r["manifest_reason_codes"], [])

    def test_unknown_root_correctness_outcomes_rejected(self):
        manifest = make_manifest()
        manifest["correctness_outcomes"] = [True, False]
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")
        self.assertFalse(r["manifest_schema_valid"])
        self.assertTrue(any(x["schema_keyword"] == "additionalProperties" for x in r["schema_issues"]))

    def test_unknown_variant_outcome_field_rejected(self):
        manifest = make_manifest()
        manifest["variants"][0]["outcome_label"] = True
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")
        self.assertTrue(any(x["schema_keyword"] == "additionalProperties" for x in r["schema_issues"]))

    def test_unknown_diagnostic_result_outcome_field_rejected(self):
        manifest = make_manifest()
        manifest["variants"][0]["diagnostic_record_results"][0]["outcome_score"] = 0.9
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")
        self.assertTrue(any(x["schema_keyword"] == "additionalProperties" for x in r["schema_issues"]))

    def test_aggregate_fields_are_not_manifest_properties(self):
        manifest = make_manifest()
        manifest["variants"][0]["f"] = [0] * 8
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_unknown_nested_artifact_reference_field_rejected(self):
        manifest = make_manifest()
        manifest["parent_roster_ref"]["unchecked_url"] = "https://example.invalid"
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_status_decision_terminal_values_consulted_true_rejected(self):
        manifest = make_manifest([make_variant("INVALID")])
        manifest["variants"][0]["status_decision"]["diagnostic_terminal_values_consulted"] = True
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_status_decision_derived_counts_consulted_true_rejected(self):
        manifest = make_manifest([make_variant("INVALID")])
        manifest["variants"][0]["status_decision"]["derived_failure_unresolved_counts_consulted"] = True
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_status_decision_missing_required_field_rejected(self):
        manifest = make_manifest([make_variant("INVALID")])
        del manifest["variants"][0]["status_decision"]["rule_ref"]
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_status_decision_unknown_nested_field_rejected(self):
        manifest = make_manifest([make_variant("INVALID")])
        manifest["variants"][0]["status_decision"]["outcome_based_reason"] = "x"
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_null_semantic_source_digest_rejected(self):
        manifest = make_manifest()
        manifest["variants"][0]["semantic_source_digest"] = None
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_null_runnable_digest_rejected(self):
        manifest = make_manifest()
        manifest["variants"][0]["runnable_artifact_digest"] = None
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_null_diagnostic_evidence_ref_rejected(self):
        manifest = make_manifest()
        manifest["variants"][0]["diagnostic_evidence_ref"] = None
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_malformed_diagnostic_evidence_ref_rejected(self):
        manifest = make_manifest()
        manifest["variants"][0]["diagnostic_evidence_ref"] = {"evidence_id": "e1", "sha256": DIGEST, "unexpected": 1}
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_malformed_status_decision_refs_rejected(self):
        manifest = make_manifest([make_variant("INVALID")])
        manifest["variants"][0]["status_decision"]["rule_ref"] = {"artifact_id": "x"}
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_bad_digest_format_rejected(self):
"
        manifest = make_manifest()
        manifest["variants"][0]["semantic_source_digest"] = "not-a-digest"
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_datetime_format_enforced(self):
        manifest = make_manifest([make_variant("INVALID")])
        manifest["variants"][0]["status_decision"]["decided_at_utc"] = "yesterday"
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_pre_diagnostic_status_must_precede_campaign_start(self):
        manifest = make_manifest([make_variant("INVALID")])
        manifest["variants"][0]["status_decision"]["decided_at_utc"] = "2026-11-23T10:30:00Z"
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")
        self.assertIn("PREDIAGNOSTIC_DECISION_NOT_BEFORE_FIRST_RUN", r["manifest_reason_codes"])

    def test_expected_not_run_decision_cannot_follow_snapshot(self):
        manifest = make_manifest([make_variant("EXPECTED_NOT_RUN")])
        manifest["variants"][0]["status_decision"]["decided_at_utc"] = "2026-11-23T12:30:00Z"
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")
        self.assertIn("EXPECTED_NOT_RUN_DECISION_AFTER_LEDGER_SNAPSHOT", r["manifest_reason_codes"])

    def test_invalid_variant_emits_no_zero_counts_or_cell(self):
        r, _ = manifest_result(make_manifest([make_variant("INVALID")]))
        measurement = r["variants"][0]["measurement"]
        self.assertEqual(measurement, {"state": "NO_DIAGNOSTIC_MEASUREMENT"})
        for key in ("f", "u", "p", "k_fail", "k_unresolved", "cell", "c_d"):
            self.assertNotIn(key, measurement)

    def test_excluded_variant_emits_no_zero_counts_or_cell(self):
        r, _ = manifest_result(make_manifest([make_variant("EXCLUDED_BEFORE_DIAGNOSTICS")]))
        measurement = r["variants"][0]["measurement"]
        self.assertEqual(measurement, {"state": "NO_DIAGNOSTIC_MEASUREMENT"})

    def test_expected_not_run_emits_no_zero_counts_or_cell(self):
        r, _ = manifest_result(make_manifest([make_variant("EXPECTED_NOT_RUN")]))
        measurement = r["variants"][0]["measurement"]
        self.assertEqual(measurement, {"state": "NO_DIAGNOSTIC_MEASUREMENT"})

    def test_incomplete_has_provisional_vectors_but_no_cell_or_c_d(self):
        r, _ = manifest_result(make_manifest([make_variant("INCOMPLETE")]))
        measurement = r["variants"][0]["measurement"]
        self.assertEqual(measurement["state"], "PROVISIONAL_INCOMPLETE_MEASUREMENTS")
        self.assertEqual(measurement["label"], "PROVISIONAL — INCOMPLETE INVENTORY")
        self.assertIn("provisional_stratum_counts", measurement)
        for key in ("cell", "c_d", "k_fail", "k_unresolved"):
            self.assertNotIn(key, measurement)

    def test_incomplete_with_zero_received_records_has_no_vectors_or_cell(self):
        variant = make_variant("INCOMPLETE", diagnostic_record_results=[])
        r, _ = manifest_result(make_manifest([variant]))
        measurement = r["variants"][0]["measurement"]
        self.assertEqual(measurement["state"], "INCOMPLETE_ZERO_RECORD_RECEIPT")
        self.assertNotIn("provisional_stratum_counts", measurement)
        self.assertNotIn("cell", measurement)
        self.assertNotIn("c_d", measurement)

    def test_valid_zero_failure_uses_label_not_numeric_cd(self):
        f = [0] * 8
        u = [0] * 8
        variant = make_variant()
        variant["diagnostic_record_results"] = make_results(f=f, u=u)
        r, _ = manifest_result(make_manifest([variant]))
        measurement = r["variants"][0]["measurement"]
        self.assertEqual(measurement["c_d"], "NO OBSERVED FAILURES")
        self.assertNotIn("c_d_numerator", measurement)
        self.assertNotIn("c_d_denominator", measurement)
        self.assertEqual(measurement["cell"][2], 0)

"    def test_cd_formula_uses_failure_vector_only_and_is_cited(self):
        variant = make_variant()
        r, _ = manifest_result(make_manifest([variant]))
        measurement = r["variants"][0]["measurement"]
        self.assertEqual(measurement["c_d"], "3/7")
        self.assertIn("§1", measurement["c_d_formula_source"])
        self.assertEqual(sum(measurement["u"]), measurement["k_unresolved"])
        self.assertNotIn("k_unresolved", measurement["c_d_formula"])

    def test_unresolved_does_not_change_cd_when_failure_vector_is_fixed(self):
        a = make_variant(variant_id="a", prefix="bank")
        b = make_variant(variant_id="b", prefix="bank")
        a["diagnostic_record_results"] = make_results(f=[2, 0, 0, 0, 0, 0, 0, 0], u=[0]*8)
        b["diagnostic_record_results"] = make_results(f=[2, 0, 0, 0, 0, 0, 0, 0], u=[1, 0, 0, 0, 0, 0, 0, 0])
        b["semantic_source_digest"] = "e" * 64
        b["runnable_artifact_digest"] = "f" * 64
        ra, _ = manifest_result(make_manifest([a]))
        rb, _ = manifest_result(make_manifest([b]))
        self.assertEqual(ra["variants"][0]["measurement"]["c_d"], rb["variants"][0]["measurement"]["c_d"])

    def test_non_string_measurement_basis_rejected(self):
        for basis in (["record_level_64"], {"x": 1}, 64, True, None):
            with self.subTest(basis=type(basis).__name__):
                manifest = make_manifest()
                manifest["measurement_basis"] = basis
                r, _ = manifest_result(manifest)
                self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_unsupported_measurement_basis_rejected(self):
        manifest = make_manifest()
        manifest["measurement_basis"] = "canonical_60"
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_invalid_result_count_and_stratum_count_rejected(self):
        for n in (63, 65):
            with self.subTest(n=n):
                variant = make_variant()
                variant["diagnostic_record_results"] = make_results()[:n] if n == 63 else make_results() + [
                    {"diagnostic_record_id": "extra", "stratum_id": "D1", "terminal_status": "DEFINITE_PASS"}
                ]
                r, _ = manifest_result(make_manifest([variant]))
                self.assertEqual(r["manifest_decision"], "REJECTED")
        variant = make_variant()
        variant["diagnostic_record_results"][0]["stratum_id"] = "D2"
        r, _ = manifest_result(make_manifest([variant]))
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_invalid_terminal_status_rejected(self):
        variant = make_variant()
        variant["diagnostic_record_results"][0]["terminal_status"] = "TIMEOUT"
        r, _ = manifest_result(make_manifest([variant]))
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_duplicate_record_id_within_variant_rejected(self):
        variant = make_variant()
        variant["diagnostic_record_results"][1]["diagnostic_record_id"] = variant["diagnostic_record_results"][0]["diagnostic_record_id"]
        r, _ = manifest_result(make_manifest([variant]))
        self.assertIn("DUPLICATE_RECORD_ID_WITHIN_VARIANT", r["manifest_reason_codes"])
        self.assertEqual(r["variants"][0]["measurement"]["state"], "NOT_REPORTED_DUE_TO_LOCAL_VALIDATION_ERRORS")

    def test_same_id_set_reuse_across_valid_variants_is_allowed(self):
        a = make_variant(variant_id="a", prefix="bank")
        b = make_variant(variant_id="b", prefix="bank")
        b["semantic_source_digest"] = "e" * 64
        b["runnable_artifact_digest"] = "f" * 64
        r, _ = manifest_result(make_manifest([a, b]))
        self.assertEqual(r["manifest_decision"], "LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED")

"    def test_different_valid_id_sets_rejected(self):
        a = make_variant(variant_id="a", prefix="bank-a")
        b = make_variant(variant_id="b", prefix="bank-b")
        b["semantic_source_digest"] = "e" * 64
        b["runnable_artifact_digest"] = "f" * 64
        r, _ = manifest_result(make_manifest([a, b]))
        self.assertIn("CROSS_VARIANT_ID_SET_MISMATCH", r["manifest_reason_codes"])

    def test_identical_artifact_digests_flagged_for_adjudication(self):
        a = make_variant(variant_id="a", prefix="bank")
        b = make_variant(variant_id="b", prefix="bank")
        b["semantic_source_digest"] = "e" * 64
        b["runnable_artifact_digest"] = "f" * 64
        b["semantic_source_digest"] = a["semantic_source_digest"]
        r, _ = manifest_result(make_manifest([a, b]))
        self.assertIn("DUPLICATE_ARTIFACT_DIGEST_REQUIRES_ADJUDICATION", r["manifest_reason_codes"])

    def test_parent_roster_duplicate_rejected(self):
        manifest = make_manifest()
        manifest["parent_roster"].append(copy.deepcopy(manifest["parent_roster"][0]))
        r, _ = manifest_result(manifest)
        self.assertIn("DUPLICATE_PARENT_ID", r["manifest_reason_codes"])

    def test_parent_family_mapping_mismatch_rejected(self):
        manifest = make_manifest()
        manifest["variants"][0]["Z_id"] = "Z9"
        r, _ = manifest_result(manifest)
        self.assertIn("PARENT_FAMILY_MAPPING_MISMATCH", r["manifest_reason_codes"])

    def test_duplicate_variant_id_rejected(self):
        a = make_variant(variant_id="same", prefix="bank")
        b = make_variant(variant_id="same", prefix="bank")
        b["semantic_source_digest"] = "e" * 64
        b["runnable_artifact_digest"] = "f" * 64
        r, _ = manifest_result(make_manifest([a, b]))
        self.assertIn("DUPLICATE_VARIANT_ID", r["manifest_reason_codes"])

    def test_outcome_exclusion_assertion_true_rejected(self):
        manifest = make_manifest()
        manifest["outcome_exclusion_assertion"]["outcomes_consulted"] = True
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_fixed_exposure_facts_and_independence_prohibition_enforced(self):
        for field, value in (("historical_public_heldout_bank_status", "UNKNOWN"),
                             ("historical_used_for_candidate_filtering", False),
                             ("independence_claim_permitted", True)):
            manifest = make_manifest()
            manifest["diagnostic_exposure_disclosure"][field] = value
            r, _ = manifest_result(manifest)
            self.assertEqual(r["manifest_decision"], "REJECTED", field)

    def test_future_generation_selection_requires_protocol_ref(self):
        manifest = make_manifest()
        manifest["diagnostic_exposure_disclosure"]["future_bank_generation_selection_status"] = "DOES_NOT_USE_PUBLIC_HELDOUT_INFORMATION"
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_evaluation_row_count_must_be_78(self):
        manifest = make_manifest()
        manifest["evaluation_row_basis"]["row_count"] = 77
        r, _ = manifest_result(manifest)
        self.assertEqual(r["manifest_decision"], "REJECTED")

    def test_empty_manifest_rejected(self):
        raw = b"[]"
        r = v.validate_manifest([], hashlib.sha256(raw).hexdigest(), self.schema)
        self.assertIn("EMPTY_MANIFEST", r["manifest_reason_codes"])

    def test_external_checks_are_explicitly_not_performed(self):
        r, _ = manifest_result(make_manifest())
        self.assertIn("frozen bank record manifest", " ".join(r["external_checks_not_performed"]))
        self.assertIn("variant inventory", " ".join(r["external_checks_not_performed"]))
        self.assertIn("run-start ledger", " ".join(r["external_checks_not_performed"]))

    def _sidecar(self, raw, assertions):
        return {
            "schema_version": "0.1",
            "manifest_sha256": hashlib.sha256(raw).hexdigest(),
            "sidecar_schema_blob_sha1": self.sidecar_schema_sha,
            "aggregate_assertions": assertions,
        }

"    def test_sidecar_matching_vectors_are_consistency_only_and_do_not_change_manifest(self):
        manifest = make_manifest()
        manifest_report, raw = manifest_result(manifest)
        manifest_before = manifest_report["manifest_decision"]
        sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [3,1,0,2,0,0,1,0], "u": [1,1,2,0,1,0,0,3], "p": [4,6,6,6,7,8,7,5]}])
        sidecar_raw = json.dumps(sidecar, sort_keys=True).encode()
        report = v.validate_sidecar(sidecar, sidecar_raw, raw,
                                    {**manifest_report, "_validated_variants": manifest["variants"]})
        self.assertEqual(report["sidecar_decision"], "SIDECAR_CONSISTENCY_CHECKS_PASS")
        self.assertEqual(report["assertions"][0]["decision"], "CONSISTENT_NON_AUTHORITATIVE_ASSERTION")
        self.assertEqual(report["manifest_decision_unchanged"], manifest_before)
        self.assertEqual(manifest_report["manifest_decision"], manifest_before)

    def test_sidecar_boolean_aggregate_entry_is_malformed(self):
        manifest = make_manifest()
        report, raw = manifest_result(manifest)
        sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [True,1,0,2,0,0,1,0]}])
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("MALFORMED_AGGREGATE", sr["sidecar_reason_codes"])

    def test_sidecar_manifest_sha_mismatch_rejected(self):
        manifest = make_manifest()
        report, raw = manifest_result(manifest)
        sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [3,1,0,2,0,0,1,0]}])
        sidecar["manifest_sha256"] = "0" * 64
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("SIDECAR_MANIFEST_SHA256_MISMATCH", sr["sidecar_reason_codes"])
        self.assertEqual(sr["manifest_decision_unchanged"], report["manifest_decision"])

    def test_sidecar_schema_blob_sha_mismatch_rejected(self):
        manifest = make_manifest()
        report, raw = manifest_result(manifest)
        sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [3,1,0,2,0,0,1,0]}])
        sidecar["sidecar_schema_blob_sha1"] = "0" * 40
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("SIDECAR_SCHEMA_BLOB_SHA1_MISMATCH", sr["sidecar_reason_codes"])

    def test_sidecar_aggregate_mismatch_reason(self):
        manifest = make_manifest()
        report, raw = manifest_result(manifest)
        sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [8]*8}])
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("AGGREGATE_MISMATCH", sr["assertions"][0]["reason_codes"])

    def test_sidecar_malformed_aggregate_reason(self):
        manifest = make_manifest()
        report, raw = manifest_result(manifest)
        sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [1,2]}])
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("MALFORMED_AGGREGATE", sr["sidecar_reason_codes"])

    def test_sidecar_unknown_variant_rejected(self):
        manifest = make_manifest()
        report, raw = manifest_result(manifest)
        sidecar = self._sidecar(raw, [{"variant_id": "not-in-manifest", "f": [3,1,0,2,0,0,1,0]}])
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("SIDECAR_VARIANT_NOT_FOUND", sr["assertions"][0]["reason_codes"])

    def test_sidecar_unknown_field_rejected(self):
        manifest = make_manifest()
        report, raw = manifest_result(manifest)
        sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [3,1,0,2,0,0,1,0], "outcome": True}])
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("SIDECAR_SCHEMA_VALIDATION_FAILED", sr["sidecar_reason_codes"])

    def test_sidecar_duplicate_variant_assertion_rejected(self):
        manifest = make_manifest()
        report, raw = manifest_result(manifest)
        assertion = {"variant_id": "v1", "f": [3,1,0,2,0,0,1,0]}
        sidecar = self._sidecar(raw, [assertion, assertion])
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("SIDECAR_DUPLICATE_VARIANT_ASSERTION", sr["assertions"][1]["reason_codes"])

    def test_sidecar_for_rejected_manifest_is_rejected_and_cannot_override_it(self):
        manifest = make_manifest()
        manifest["correctness_outcomes"] = [1]
        report, raw = manifest_result(manifest)
        sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [3,1,0,2,0,0,1,0]}])
        sr = v.validate_sidecar(sidecar, json.dumps(sidecar).encode(), raw,
                                {**report, "_validated_variants": manifest["variants"]})
        self.assertIn("SIDECAR_MANIFEST_NOT_LOCALLY_VALID", sr["sidecar_reason_codes"])
        self.assertEqual(sr["manifest_decision_unchanged"], "REJECTED")


"    def test_cli_manifest_only_exit_code_and_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(json.dumps(make_manifest()), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "validate_records.py"),
                                     "--manifest", str(manifest_path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["manifest_report"]["manifest_decision"],
                             "LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED")

    def test_cli_rejects_root_outcome_field_with_exit_code_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = make_manifest()
            manifest["correctness_outcomes"] = [0, 1]
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "validate_records.py"),
                                     "--manifest", str(manifest_path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["manifest_report"]["manifest_decision"], "REJECTED")

    def test_cli_rejected_sidecar_does_not_change_manifest_decision(self):
        with tempfile.TemporaryDirectory() as tmp:
            manifest = make_manifest()
            manifest_path = Path(tmp) / "manifest.json"
            sidecar_path = Path(tmp) / "aggregates.json"
            raw = json.dumps(manifest).encode("utf-8")
            manifest_path.write_bytes(raw)
            sidecar = self._sidecar(raw, [{"variant_id": "v1", "f": [3,1,0,2,0,0,1,0]}])
            sidecar["manifest_sha256"] = "0" * 64
            sidecar_path.write_text(json.dumps(sidecar), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "validate_records.py"),
                                     "--manifest", str(manifest_path), "--sidecar", str(sidecar_path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["manifest_report"]["manifest_decision"],
                             "LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED")
            self.assertEqual(payload["sidecar_report"]["sidecar_decision"], "REJECTED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
