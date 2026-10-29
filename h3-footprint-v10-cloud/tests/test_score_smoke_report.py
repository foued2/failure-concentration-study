from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "h3-footprint-v3"))
import instrument
import score_smoke_report as scorer


class ScorerBoundaryTests(unittest.TestCase):
    def test_bounded_json_reader_rejects_large_report_before_parsing(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "oversize.json"
            path.write_bytes(b"{" + b" " * scorer.MAX_JSON_BYTES)
            with self.assertRaisesRegex(ValueError, "byte limit"):
                scorer._load_bounded_json(path, "execution report")

    def _valid_report_and_manifest(self, root):
        expected = instrument.expected_values()
        manifest = {"kind":"fixed_harness_control", "expected_answers_in_fixture":False, "model_generated":False, "body_sha256":"abc"}
        results = []
        for probe in instrument.PROBES:
            results.append({"probe_id":probe["probe_id"], "status":"ok", "answer_type":"int", "answer":expected[probe["probe_id"]], "tree_empty":True, "processes_present_at_post_child_check":False, "tmp_cleanup_ok":True, "timed_out":False, "output_overflow":False, "child_return_code":0})
        report = {"candidate_sha256":"abc", "probe_count":30, "results":results, "isolation_harness_ok":True, "all_trees_empty":True, "candidate_generation_performed":False, "scoring_performed":False, "reference_answers_present":False, "host_repository_mounted":False, "api_keys_passed_to_container":False, "container_config":{"checks":{"network_none":True,"read_only_root":True}}}
        rp, mp = root / "report.json", root / "manifest.json"
        rp.write_text(json.dumps(report), encoding="utf-8")
        mp.write_text(json.dumps(manifest), encoding="utf-8")
        return rp, mp, report

    def test_bounded_json_reader_rejects_excessive_nesting(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "deep.json"
            path.write_text("[" * 100 + "0" + "]" * 100, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "nesting depth"):
                scorer._load_bounded_json(path, "execution report")

    def test_scorer_rejects_record_level_cleanup_failure_even_if_top_level_is_true(self):
        with tempfile.TemporaryDirectory() as td:
            rp, mp, report = self._valid_report_and_manifest(Path(td))
            report["results"][0]["tree_empty"] = False
            rp.write_text(json.dumps(report), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "record 0"):
                scorer.score(rp, mp)

    def test_scorer_accepts_consistent_control_report(self):
        with tempfile.TemporaryDirectory() as td:
            rp, mp, _ = self._valid_report_and_manifest(Path(td))
            out = scorer.score(rp, mp)
            self.assertEqual(out["status"], "PASS")
            self.assertEqual(out["correct_control_predictions"], 30)


if __name__ == "__main__":
    unittest.main()
