from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import build_smoke_fixture
import score_smoke_report
import instrument


class FixedFixtureTests(unittest.TestCase):
    def test_payload_has_all_30_public_inputs_and_no_answer_fields(self):
        payloads = build_smoke_fixture.build_probe_payloads()
        self.assertEqual(len(payloads), 30)
        self.assertEqual(len({p["probe_id"] for p in payloads}), 30)
        self.assertTrue(all(set(p) == {"probe_id", "n", "edges", "s", "t"} for p in payloads))

    def test_written_fixture_has_hash_manifest_and_no_expected_answers(self):
        with tempfile.TemporaryDirectory() as td:
            manifest = build_smoke_fixture.write_fixture(Path(td))
            self.assertEqual(manifest["probe_count"], 30)
            self.assertFalse(manifest["expected_answers_in_fixture"])
            sums = (Path(td) / "SHA256SUMS").read_text()
            self.assertIn("smoke-body.py", sums)
            self.assertIn("probes.json", sums)
            self.assertIn("fixture-manifest.json", sums)
            payload = json.loads((Path(td) / "probes.json").read_text())
            self.assertEqual(len(payload), 30)
            self.assertNotIn("expected_values", json.dumps(payload))

    def test_scorer_pins_the_exact_frozen_manifest_blob(self):
        self.assertEqual(
            score_smoke_report.git_blob_sha1(score_smoke_report.V3 / "FREEZE.json"),
            score_smoke_report.FROZEN_V3_FREEZE_GIT_BLOB_SHA1,
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "FREEZE.json").write_text(
                json.dumps({
                    "tag": "h3-footprint-v3-freeze-2026-10-27",
                    "status": "PRE_CANDIDATE_HARNESS_FREEZE",
                    "artifact_hashes_sha256": {},
                }),
                encoding="utf-8",
            )
            original_v3 = score_smoke_report.V3
            score_smoke_report.V3 = root
            try:
                with self.assertRaisesRegex(ValueError, "pinned frozen manifest blob"):
                    score_smoke_report.verify_frozen_v3()
            finally:
                score_smoke_report.V3 = original_v3

    def test_scorer_checks_probe_payload_hash_and_ids(self):
        expected_ids = [probe["probe_id"] for probe in instrument.PROBES]
        manifest = {
            "probe_payload_sha256": score_smoke_report.canonical_probe_payload_sha256(),
            "probe_ids": expected_ids,
        }
        good = dict(manifest)
        score_smoke_report.validate_probe_binding(good, manifest)
        bad_hash = {**manifest, "probe_payload_sha256": "tampered"}
        with self.assertRaises(ValueError):
            score_smoke_report.validate_probe_binding(bad_hash, manifest)
        bad_ids = {**manifest, "probe_ids": ["TAMPERED", *expected_ids[1:]]}
        with self.assertRaises(ValueError):
            score_smoke_report.validate_probe_binding(bad_ids, manifest)

    def test_scorer_rejects_a_non_fixture_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            report = root / "report.json"
            manifest = root / "manifest.json"
            report.write_text("{}")
            manifest.write_text(json.dumps({"kind": "candidate_pack"}))
            with self.assertRaises(ValueError):
                score_smoke_report.score(report, manifest, root / "body.py")


if __name__ == "__main__":
    unittest.main()
