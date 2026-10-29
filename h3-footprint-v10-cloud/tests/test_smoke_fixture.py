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

    def test_scorer_checks_probe_payload_hash_and_ids(self):
        manifest = {"probe_payload_sha256": "abc", "probe_ids": ["R1", "R2"]}
        good = {"probe_payload_sha256": "abc", "probe_ids": ["R1", "R2"]}
        score_smoke_report.validate_probe_binding(good, manifest)
        bad_hash = {"probe_payload_sha256": "tampered", "probe_ids": ["R1", "R2"]}
        with self.assertRaises(ValueError):
            score_smoke_report.validate_probe_binding(bad_hash, manifest)
        bad_ids = {"probe_payload_sha256": "abc", "probe_ids": ["R1", "Z2"]}
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
                score_smoke_report.score(report, manifest)


if __name__ == "__main__":
    unittest.main()
