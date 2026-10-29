from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

import hosted_footprint_gate as hosted
import generation_plan_draft as draft
import score_smoke_report


class HostedFootprintGateTests(unittest.TestCase):
    def _write_body(self, root: Path, source: str) -> Path:
        normalized = draft.normalize_source(source)
        body_hash = draft._V3.digest(normalized)
        path = root / f"{body_hash}.py"
        path.write_text(normalized, encoding="utf-8", newline="\n")
        return path

    def _valid_mock_report(self, body_path: Path) -> dict:
        source_bytes = body_path.read_bytes()
        results = []
        expected = score_smoke_report.instrument.expected_values()
        for index, probe in enumerate(score_smoke_report.instrument.PROBES, start=1):
            results.append({
                "v": 1,
                "sequence": index + 1,
                "probe_index": index,
                "probe_id": probe["probe_id"],
                "phase": "probe",
                "status": "ok",
                "answer_type": "int",
                "answer": expected[probe["probe_id"]],
                "tree_empty": True,
                "timed_out": False,
                "output_overflow": False,
                "solver_output_overflow": False,
                "solver_stdout_characters": 0,
                "solver_stderr_characters": 0,
            })
        return {
            "candidate_sha256": hashlib.sha256(source_bytes).hexdigest(),
            "probe_payload_sha256": score_smoke_report.canonical_probe_payload_sha256(),
            "probe_ids": [p["probe_id"] for p in score_smoke_report.instrument.PROBES],
            "probe_count": 30,
            "expected_probe_count": 30,
            "candidate_valid": True,
            "candidate_status": "valid",
            "isolation_harness_ok": True,
            "all_trees_empty": True,
            "candidate_generation_performed": False,
            "scoring_performed": False,
            "reference_answers_present": False,
            "host_repository_mounted": False,
            "api_keys_passed_to_container": False,
            "container_config": {"checks": {"network_none": True, "read_only_root": True, "candidate_readonly": True}},
            "results": results,
        }

    def test_attempt_normalization_preserves_batch_and_hash_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "attempts-input.jsonl"
            target = root / "attempts.jsonl"
            body_hash = "a" * 64
            source.write_text(
                json.dumps({
                    "batch_id": 0,
                    "original_route_alias": "opencode/deepseek-v4.1-flash-free",
                    "prompt_variant": "direct",
                    "candidate_records": [{"body_sha256": body_hash}],
                }) + "\n",
                encoding="utf-8",
            )
            summary = hosted.normalize_attempts(source, target)
            normalized = json.loads(target.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(summary["attempt_count"], 1)
            self.assertEqual(normalized["candidate_records"][0]["body_hash"], body_hash)
            self.assertEqual(normalized["batch_id"], 0)

    def test_attempt_normalization_rejects_gaps_and_duplicate_batches(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "attempts.jsonl"
            target = root / "out" / "attempts.jsonl"
            rows = [
                {"batch_id": 0, "model": "m0", "prompt_variant": "direct", "candidate_records": []},
                {"batch_id": 2, "model": "m2", "prompt_variant": "simple", "candidate_records": []},
            ]
            source.write_text("".join(json.dumps(x) + "\n" for x in rows), encoding="utf-8")
            with self.assertRaisesRegex(hosted.HostedGateError, "complete zero-based batch prefix"):
                hosted.normalize_attempts(source, target)

    def test_invalid_static_candidate_is_excluded_without_container_execution(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = self._write_body(root, "import os\n\ndef solve(n, edges, s, t):\n    return -1\n")
            info = {body.stem: {"group_id": "batch-000", "model": "model", "prompt_variant": "direct", "batch_id": 0}}
            with mock.patch.object(hosted.executor, "run_candidate", side_effect=AssertionError("must not execute")):
                row = hosted.evaluate_body_hosted(
                    body, info,
                    trusted_dir=root,
                    report_dir=root / "reports",
                )
            self.assertEqual(row["excluded"], "import:os")
            self.assertIsNone(row["k"])
            self.assertIsNone(row["C"])

    def test_container_prediction_profile_matches_frozen_v3_profile_contract(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = self._write_body(
                root,
                "def solve(n, edges, s, t):\n    return 0\n",
            )
            info = {body.stem: {"group_id": "batch-000", "model": "model", "prompt_variant": "direct", "batch_id": 0}}
            report = self._valid_mock_report(body)
            with mock.patch.object(hosted.executor, "run_candidate", return_value=report):
                row = hosted.evaluate_body_hosted(body, info, trusted_dir=root, report_dir=root / "reports")
            self.assertIsNone(row["excluded"])
            self.assertEqual(row["k"], 0)
            self.assertEqual(row["C"], 0.0)
            self.assertEqual(row["max_f"], 0)
            self.assertEqual(row["eligible"], False)
            saved = json.loads((root / "reports" / f"{body.stem}.json").read_text(encoding="utf-8"))
            self.assertFalse(saved["candidate_generation_performed"])
            self.assertFalse(saved["scoring_performed"])
            self.assertFalse(saved["reference_answers_present"])
            self.assertFalse(saved["host_repository_mounted"])
            self.assertFalse(saved["api_keys_passed_to_container"])

    def test_full_gate_uses_frozen_aggregation_without_generating_candidates(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body_dir = root / "bodies"
            body_dir.mkdir()
            body = self._write_body(
                body_dir,
                "def solve(n, edges, s, t):\n    return 0\n",
            )
            attempts = root / "attempts-v10.jsonl"
            attempts.write_text(
                json.dumps({
                    "batch_id": 0,
                    "original_route_alias": "opencode/deepseek-v4.1-flash-free",
                    "prompt_variant": "direct",
                    "requested_bodies": 8,
                    "extracted_bodies": 1,
                    "candidate_records": [{"body_sha256": body.stem}],
                }) + "\n",
                encoding="utf-8",
            )
            output_dir = root / "gate-output"
            trusted_dir = root / "trusted"
            trusted_dir.mkdir()
            mocked_execution = self._valid_mock_report(body)
            with mock.patch.object(hosted.executor, "run_candidate", return_value=mocked_execution) as execute:
                summary = hosted.build_hosted_report(
                    body_dir=body_dir,
                    attempts_path=attempts,
                    trusted_dir=trusted_dir,
                    output_dir=output_dir,
                )
            execute.assert_called_once()
            self.assertEqual(summary["protocol_status"], "V10_DRAFT_NOT_FROZEN")
            self.assertEqual(summary["candidate_bodies"], 1)
            self.assertEqual(summary["valid_bodies"], 1)
            self.assertEqual(summary["eligible_bodies"], 0)
            self.assertEqual(summary["verdict"], "FAIL")
            self.assertEqual(summary["reason"], "insufficient_support")
            self.assertFalse(summary["candidate_generation_performed_by_this_gate"])
            self.assertEqual(summary["model_calls_performed_by_this_gate"], 0)
            self.assertFalse(summary["held_out_work_performed"])
            report = json.loads((output_dir / "footprint.json").read_text(encoding="utf-8"))
            self.assertEqual(report["rows"][0]["k"], 0)
            self.assertEqual(report["rows"][0]["C"], 0.0)
            manifest = json.loads((output_dir / "V10_EXECUTION_MANIFEST.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["h3_scientific_result"])
            self.assertFalse(manifest["candidate_generation_performed_by_this_gate"])
            self.assertTrue((output_dir / "REPORT.md").is_file())
            self.assertTrue((output_dir / "runner-reports" / f"{body.stem}.json").is_file())

    def test_missing_provenance_is_excluded_before_docker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = self._write_body(root, "def solve(n, edges, s, t):\n    return 0\n")
            with mock.patch.object(hosted.executor, "run_candidate", side_effect=AssertionError("must not execute")):
                row = hosted.evaluate_body_hosted(body, {}, trusted_dir=root, report_dir=root / "reports")
            self.assertEqual(row["excluded"], "missing_provenance")
            self.assertIsNone(row["k"])


if __name__ == "__main__":
    unittest.main()
