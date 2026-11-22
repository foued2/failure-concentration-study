"""Synthetic software tests for the B1 census intake validator.

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

import validate_records as validator  # noqa: E402

CAPACITY = {"record": [8] * 8, "canonical": [8, 8, 8, 8, 8, 4, 8, 8]}
STRATA = [f"D{j}" for j in range(1, 9)]
DIGEST = "a" * 64


def make_record(variant: str = "v-1", basis: str = "record", f=None, u=None) -> dict:
    f = list(f) if f is not None else [1, 1, 0, 0, 0, 0, 0, 0]
    u = list(u) if u is not None else [0] * 8
    ids = {}
    for pos, stratum in enumerate(STRATA):
        ids[stratum] = [f"{variant}-{stratum}-r{i}" for i in range(CAPACITY[basis][pos])]
    return {
        "variant_id": variant,
        "parent_id": "parent-1",
        "parent_family": "family-A",
        "mutation_id": "mut-1",
        "exposure_basis": basis,
        "f": f,
        "u": u,
        "strata_record_ids": ids,
        "source_digest": DIGEST,
    }


def report_for(records: list[dict]) -> dict:
    return validator.validate_manifest(records, "b" * 64)


class IntakeTests(unittest.TestCase):
    def test_valid_record_basis_admitted(self):
        rep = report_for([make_record()])
        self.assertEqual(rep["rejected"], 0)
        self.assertEqual(rep["admitted"], 1)
        self.assertEqual(rep["admitted_by_basis"]["record"], 1)
        entry = rep["records"][0]
        self.assertEqual(entry["derived"]["k_fail"], 2)
        self.assertEqual(entry["derived"]["c_d_exact"], "1/2")
        self.assertEqual(entry["derived"]["cell"], ["mut-1", "family-A", 2, 0])

    def test_valid_canonical_basis_admitted(self):
        rep = report_for([make_record("v-c", "canonical")])
        self.assertEqual(rep["rejected"], 0)
        self.assertEqual(rep["admitted_by_basis"]["canonical"], 1)
        self.assertEqual(len(rep["records"][0]["derived"]["cell"]), 4)

    def test_missing_unresolved_vector_rejected(self):
        rec = make_record()
        del rec["u"]
        rep = report_for([rec])
        self.assertIn("MISSING_UNRESOLVED_VECTOR", rep["records"][0]["reason_codes"])
        self.assertIn("MISSING_FIELD", rep["records"][0]["reason_codes"])

    def test_unresolved_vector_length_rejected(self):
        rec = make_record(u=[0] * 7)
        rep = report_for([rec])
        self.assertIn("U_VECTOR_LENGTH", rep["records"][0]["reason_codes"])

    def test_negative_f_rejected(self):
        rec = make_record(f=[-1, 1, 0, 0, 0, 0, 0, 0])
        rep = report_for([rec])
        self.assertIn("F_NEGATIVE", rep["records"][0]["reason_codes"])

    def test_capacity_exceeded_rejected(self):
        rec = make_record("v-cap", "canonical", f=[8, 8, 8, 8, 8, 8, 0, 0])
        rep = report_for([rec])
        self.assertIn("STRATUM_CAPACITY_EXCEEDED", rep["records"][0]["reason_codes"])

    def test_duplicate_record_id_within_stratum_rejected(self):
        rec = make_record("v-dup")
        rec["strata_record_ids"]["D1"][1] = rec["strata_record_ids"]["D1"][0]
        rep = report_for([rec])
        self.assertIn("DUPLICATE_RECORD_ID", rep["records"][0]["reason_codes"])

    def test_record_id_reused_within_one_record_rejected(self):
        rec = make_record("v-cross")
        rec["strata_record_ids"]["D2"][0] = rec["strata_record_ids"]["D1"][0]
        rep = report_for([rec])
        self.assertIn("DUPLICATE_RECORD_ID", rep["records"][0]["reason_codes"])

    def test_record_id_reused_across_records_rejected(self):
        first = make_record("v-first")
        second = make_record("v-second")
        second["strata_record_ids"]["D1"][0] = first["strata_record_ids"]["D1"][0]
        rep = report_for([first, second])
        self.assertIn("RECORD_ID_REUSED_ACROSS_RECORDS", rep["records"][1]["reason_codes"])

    def test_unknown_stratum_rejected(self):
        rec = make_record()
        rec["strata_record_ids"]["D9"] = ["x"]
        rep = report_for([rec])
        self.assertIn("STRATA_KEYS", rep["records"][0]["reason_codes"])

    def test_outcome_field_rejected(self):
        for field in ("correctness", "Y", "y_heldout", "outcome", "diagnostic_correctness"):
            with self.subTest(field=field):
                rec = make_record()
                rec[field] = 1
                rep = report_for([rec])
                self.assertIn("OUTCOME_FIELD_PRESENT", rep["records"][0]["reason_codes"])

    def test_unknown_field_rejected(self):
        rec = make_record()
        rec["surprise"] = 1
        rep = report_for([rec])
        self.assertIn("UNKNOWN_FIELD", rep["records"][0]["reason_codes"])

    def test_zero_failures_convention(self):
        rec = make_record("v-zero", f=[0] * 8, u=[1, 1, 0, 0, 0, 0, 0, 0])
        rep = report_for([rec])
        self.assertEqual(rep["rejected"], 0)
        derived = rep["records"][0]["derived"]
        self.assertEqual(derived["k_fail"], 0)
        self.assertEqual(derived["k_unresolved"], 2)
        self.assertEqual(derived["c_d_exact"], "0")
        self.assertEqual(derived["c_d_status"], "NO_OBSERVED_FAILURES")

    def test_duplicate_variant_rejected(self):
        rep = report_for([make_record("v-same"), make_record("v-same")])
        self.assertIn("DUPLICATE_VARIANT_ID", rep["records"][1]["reason_codes"])
        self.assertEqual(rep["rejected"], 1)

    def test_report_deterministic_and_hashed(self):
        payload = [make_record("v-a"), make_record("v-b")]
        raw = json.dumps(payload, sort_keys=True).encode("utf-8")
        digest = hashlib.sha256(raw).hexdigest()
        first = validator.validate_manifest(payload, digest)
        second = validator.validate_manifest(payload, digest)
        self.assertEqual(
            json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True)
        )
        self.assertEqual(first["manifest_sha256"], digest)

    def test_report_contains_no_census_verdict(self):
        rep = report_for([make_record()])
        text = json.dumps(rep).lower()
        for token in ("eligible", "lopo", "pass", "gate 1 pass"):
            self.assertNotIn(token, text)

    def test_schema_id_matches_schema_version(self):
        schema = json.loads((FOLDER / "record_schema.json").read_text(encoding="utf-8"))
        self.assertTrue(
            schema["$id"].endswith(f"/v{schema['schema_version']}.json"),
            "schema $id must carry its revision identifier",
        )

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            good = Path(tmp) / "good.json"
            bad = Path(tmp) / "bad.json"
            good.write_text(json.dumps([make_record("v-cli-good")]), encoding="utf-8")
            bad.write_text(json.dumps([make_record("v-cli-bad", u=[0] * 7)]), encoding="utf-8")
            ok = subprocess.run(
                [sys.executable, str(FOLDER / "validate_records.py"), "--manifest", str(good)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(ok.returncode, 0, ok.stderr)
            rejected = subprocess.run(
                [sys.executable, str(FOLDER / "validate_records.py"), "--manifest", str(bad)],
                capture_output=True,
                text=True,
            )
            self.assertEqual(rejected.returncode, 2, rejected.stderr)


if __name__ == "__main__":
    unittest.main()
