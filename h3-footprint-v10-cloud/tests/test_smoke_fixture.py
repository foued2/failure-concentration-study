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

    def test_profile_counts_timeouts_exceptions_overflow_and_wrong_answers_as_failures(self):
        expected = instrument.expected_values()
        expected_ids = [probe["probe_id"] for probe in instrument.PROBES]
        results = []
        for index, probe_id in enumerate(expected_ids):
            status = "ok"
            answer_type = "int"
            answer = expected[probe_id]
            timed_out = False
            overflow = False
            if index == 0:
                status = "timeout"
                answer_type = "none"
                answer = None
                timed_out = True
            elif index == 1:
                status = "exception"
                answer_type = "none"
                answer = None
            elif index == 2:
                status = "output_overflow"
                answer_type = "none"
                answer = None
                overflow = True
            elif index == 3:
                answer = answer + 1
            results.append({
                "probe_id": probe_id,
                "phase": "probe",
                "probe_index": index + 1,
                "sequence": index + 2,
                "status": status,
                "answer_type": answer_type,
                "answer": answer,
                "timed_out": timed_out,
                "solver_output_overflow": overflow,
                "tree_empty": True,
            })
        profile = score_smoke_report.derive_failure_profile(results, expected, expected_ids)
        self.assertEqual(profile["fails"][:5], [True, True, True, True, False])
        self.assertEqual(profile["k"], 4)
        self.assertEqual(profile["family_counts"]["R"], 4)
        self.assertEqual(profile["C"], 1.0)
        self.assertEqual(profile["max_f"], 4)
        self.assertEqual(profile["timeout_count"], 1)
        self.assertEqual(profile["runtime_exception_count"], 1)
        self.assertEqual(profile["output_overflow_count"], 1)

    def test_malformed_per_probe_protocol_is_rejected_not_counted_as_failure(self):
        expected = instrument.expected_values()
        expected_ids = [probe["probe_id"] for probe in instrument.PROBES]
        results = []
        for index, probe_id in enumerate(expected_ids):
            results.append({
                "probe_id": probe_id,
                "phase": "probe",
                "probe_index": index + 1,
                "sequence": index + 2,
                "status": "invalid_child_output" if index == 0 else "ok",
                "answer_type": "none" if index == 0 else "int",
                "answer": None if index == 0 else expected[probe_id],
                "tree_empty": True,
            })
        with self.assertRaisesRegex(ValueError, "candidate-invalid protocol status"):
            score_smoke_report.derive_failure_profile(results, expected, expected_ids)

    def test_success_status_with_overflow_flag_is_rejected(self):
        expected = instrument.expected_values()
        expected_ids = [probe["probe_id"] for probe in instrument.PROBES]
        results = []
        for index, probe_id in enumerate(expected_ids):
            results.append({
                "probe_id": probe_id,
                "phase": "probe",
                "probe_index": index + 1,
                "sequence": index + 2,
                "status": "ok",
                "answer_type": "int",
                "answer": expected[probe_id],
                "solver_output_overflow": index == 0,
                "tree_empty": True,
            })
        with self.assertRaisesRegex(ValueError, "contradicts output-overflow flag"):
            score_smoke_report.derive_failure_profile(results, expected, expected_ids)

    def test_response_order_and_sequence_are_bound(self):
        expected = instrument.expected_values()
        expected_ids = [probe["probe_id"] for probe in instrument.PROBES]
        results = []
        for index, probe_id in enumerate(expected_ids):
            results.append({
                "probe_id": probe_id,
                "phase": "probe",
                "probe_index": index + 1,
                "sequence": index + 2,
                "status": "ok",
                "answer_type": "int",
                "answer": expected[probe_id],
                "tree_empty": True,
            })
        results[0]["sequence"] = 99
        with self.assertRaisesRegex(ValueError, "response sequence mismatch"):
            score_smoke_report.derive_failure_profile(results, expected, expected_ids)

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
