from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import lc518_generator as g
import lc518_launcher as launcher


class LauncherAuditTests(unittest.TestCase):
    def predicate_events(self):
        events = []
        ranges = [("H1", 1, 12), ("H2", 13, 24), ("H3", 25, 32), ("H4", 33, 40)]
        for stratum, lo, hi in ranges:
            for ordinal in range(lo, hi + 1):
                events.append({
                    "input_id": f"H{ordinal:03d}",
                    "stratum": stratum,
                    "amount": ordinal,
                    "coins": [1, ordinal + 1],
                    "oracle_answer": ordinal + 1,
                    "N0": 1,
                    "repeated_use_predicate": True,
                })
        return events

    def test_parse_structured_stderr_tags(self):
        event = g.make_sidecar_row(2, "diagnostic", "D009", "INT32_OVERFLOW", "D2")
        pred = self.predicate_events()[0]
        raw = "ordinary diagnostic\n" + "REJECTION_EVENT " + json.dumps(event) + "\n" + "PREDICATE_LOG " + json.dumps(pred)
        parsed = launcher.parse_structured_lines(raw)
        self.assertEqual(parsed["REJECTION_EVENT"], [event])
        self.assertEqual(parsed["PREDICATE_LOG"], [pred])

    def test_malformed_tagged_json_fails_closed(self):
        with self.assertRaises(ValueError):
            launcher.parse_structured_lines("PREDICATE_LOG {broken\n")

    def test_predicate_count_and_stratum_allocation_exact_40(self):
        events = self.predicate_events()
        counts = launcher.validate_predicate_events(events, require_complete=True)
        self.assertEqual(counts, {"H1": 12, "H2": 12, "H3": 8, "H4": 8})
        self.assertEqual(len(events), 40)

    def test_partial_predicate_count_is_preserved_but_not_accepted(self):
        events = self.predicate_events()[:19]
        counts = launcher.validate_predicate_events(events, require_complete=False)
        self.assertEqual(sum(counts.values()), 19)
        with self.assertRaises(ValueError):
            launcher.validate_predicate_events(events, require_complete=True)

    def test_duplicate_or_misallocated_predicate_id_is_rejected(self):
        events = self.predicate_events()
        events[12]["input_id"] = "H001"
        with self.assertRaises(ValueError):
            launcher.validate_predicate_events(events, require_complete=False)

    def test_predicate_crosswalk_matches_heldout_rows_and_oracle_attachment(self):
        events = self.predicate_events()
        heldout_rows = []
        oracle_rows = []
        for event in events:
            key = g.canonical_key(event["amount"], event["coins"])
            cid = g.canonical_id(*key)
            heldout_rows.append({
                "input_id": event["input_id"], "amount": event["amount"],
                "coins": event["coins"], "stratum": event["stratum"], "canonical_id": cid,
            })
            if all(row["canonical_id"] != cid for row in oracle_rows):
                oracle_rows.append({"canonical_id": cid, "oracle_answer": event["oracle_answer"]})
        launcher.validate_predicate_crosswalk(events, heldout_rows, oracle_rows)
        heldout_rows[0]["coins"] = [999]
        with self.assertRaises(ValueError):
            launcher.validate_predicate_crosswalk(events, heldout_rows, oracle_rows)

    def test_rejection_events_reconcile_exactly_with_both_sidecars(self):
        events = [
            g.make_sidecar_row(1, "heldout", "H013", "H2_ORACLE_BELOW_TWO", "H2"),
            g.make_sidecar_row(2, "diagnostic", "D041", "CROSS_BANK_COLLISION", "D6"),
        ]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / "diagnostic_bank.rejections.jsonl").write_bytes(g.sidecar_bytes([events[1]]))
            (out / "heldout_bank.rejections.jsonl").write_bytes(g.sidecar_bytes([events[0]]))
            launcher.reconcile_rejections(events, out)
            (out / "heldout_bank.rejections.jsonl").write_bytes(b"")
            with self.assertRaises(ValueError):
                launcher.reconcile_rejections(events, out)

    def test_item8_report_and_artifacts_pass_hash_verification(self):
        d = [{"input_id": "D001", "amount": 2, "coins": [1], "canonical_id": g.canonical_id(2, [1]), "stratum": "D1"}]
        h = [{"input_id": "H001", "amount": 2, "coins": [2], "canonical_id": g.canonical_id(2, [2]), "stratum": "H1"}]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            report = g.atomic_publish_fixture_or_bank_package(
                out, b"[]\n", b"[]\n", b"[]\n", b"[]\n", b"", b"", d, h, [], []
            )
            self.assertEqual(report["status"], "PASS")
            status, report_hash, artifacts = launcher.verify_item8_package(out)
            self.assertEqual(status, "PASS")
            self.assertEqual(report_hash, launcher.sha256_file(out / "canonical_disjointness_report.json"))
            self.assertEqual(set(artifacts), launcher.PASS_ARTIFACTS)

    def test_item8_fail_artifacts_are_rejection_sidecars_only(self):
        d = [{"input_id": "D001", "amount": 2, "coins": [1], "canonical_id": g.canonical_id(2, [1]), "stratum": "D1"}]
        h = [{"input_id": "H001", "amount": 2, "coins": [1], "canonical_id": g.canonical_id(2, [1]), "stratum": "H1"}]
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            report = g.atomic_publish_fixture_or_bank_package(
                out, b"[]\n", b"[]\n", b"[]\n", b"[]\n", b"", b"", d, h, [], []
            )
            self.assertEqual(report["status"], "FAIL")
            status, _, artifacts = launcher.verify_item8_package(out)
            self.assertEqual(status, "FAIL")
            self.assertEqual(set(artifacts), launcher.FAIL_ARTIFACTS)
            self.assertFalse((out / "diagnostic_bank.json").exists())



    def test_published_generator_module_loader_handles_dataclasses(self):
        module = launcher._load_generator_module(Path(g.__file__).resolve())
        self.assertEqual(module.EXPECTED_PYTHON_VERSION, (3, 13, 5))
        self.assertIsNone(module.OUTPUT_DIR)
        self.assertFalse(module.BANK_GENERATION_AUTHORIZED)

    def test_setup_abort_preserves_manifest_and_empty_capture_logs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "run"
            source = Path(td) / "source"
            source.mkdir()
            launcher_path = source / "launcher.py"
            generator_path = source / "generator.py"
            generator_tests = source / "test_generator.py"
            launcher_tests = source / "test_launcher.py"
            protocol_path = source / "protocol.json"
            for path in (launcher_path, generator_path, generator_tests, launcher_tests, protocol_path):
                path.write_text("fixture\n", encoding="utf-8")
            output = root / "bank"
            fake_cfg = {
                "run_root": root, "output_dir": output, "launcher_path": launcher_path,
                "generator_path": generator_path,
                "suite_paths": {"generator": generator_tests, "launcher": launcher_tests},
                "protocol_path": protocol_path,
            }
            with mock.patch.object(launcher, "validate_static_configuration", return_value=fake_cfg), \
                 mock.patch.object(launcher, "_copy_exclusive", side_effect=RuntimeError("synthetic setup stop")), \
                 mock.patch.object(launcher, "EXPECTED_GENERATOR_SHA256", hashlib.sha256(generator_path.read_bytes()).hexdigest()), \
                 mock.patch.object(launcher, "EXPECTED_TEST_SUITE_SHA256S", {
                     "generator": hashlib.sha256(generator_tests.read_bytes()).hexdigest(),
                     "launcher": hashlib.sha256(launcher_tests.read_bytes()).hexdigest(),
                 }), \
                 mock.patch.object(launcher, "PROTOCOL_SHA256", hashlib.sha256(protocol_path.read_bytes()).hexdigest()):
                manifest = launcher.run()
            logs = root / "logs"
            self.assertTrue((logs / "stdout.log").is_file())
            self.assertTrue((logs / "stderr.log").is_file())
            self.assertEqual((logs / "stdout.log").read_bytes(), b"")
            self.assertEqual((logs / "stderr.log").read_bytes(), b"")
            self.assertEqual(manifest["overall_acceptance_status"], "NOT_ACCEPTED")
            self.assertIn("synthetic setup stop", manifest["post_run_audit_error"])
            self.assertTrue((logs / "run_manifest.json").is_file())

    def test_launcher_refuses_without_owner_go_before_creating_a_run_root(self):
        with self.assertRaisesRegex(RuntimeError, "separate owner GO for bank generation is absent"):
            launcher.validate_static_configuration()

    def test_runner_image_identity_is_pinned(self):
        with mock.patch.dict("os.environ", {
            "ImageOS": launcher.EXPECTED_RUNNER_IMAGE_OS,
            "ImageVersion": "deliberately-wrong-image-version",
        }):
            with self.assertRaisesRegex(RuntimeError, "runner image identity"):
                launcher.validate_static_configuration()


if __name__ == "__main__":
    unittest.main(verbosity=2)
