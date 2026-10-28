from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import protocol  # noqa: E402
from _support import fixture, run_direct  # noqa: E402


class OutputBoundaryTests(unittest.TestCase):
    def test_candidate_cannot_tamper_with_job_or_response(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            record = run_direct(fixture("boundary_probe.py"), work, timeout=25.0)
            self.assertIn(record["status"], {"ok", "error"})

            report = json.loads((work / "scratch" / "boundary_report.json").read_text(encoding="utf-8"))

            # The SID must be resolved, not interpolated as a literal that the
            # restricted environment cannot expand.
            self.assertTrue(str(report["sid"]).startswith("S-1-5-"),
                            f"account SID was not resolved: {report['sid_probe']}")
            for attempt in report["attempts"]:
                self.assertNotIn("%USERNAME%", attempt["command"])
                self.assertNotEqual(attempt["rc"], 0,
                                    f"escape command unexpectedly succeeded: {attempt}")
                # A usage/syntax error is not an attempted escape.
                self.assertNotIn("/?", attempt["output"],
                                 f"command was rejected before doing anything: {attempt}")
                if not attempt["name"].startswith("takeown"):
                    self.assertEqual(attempt["rc"], 5,
                                     f"expected ERROR_ACCESS_DENIED, got {attempt}")

            wrote = [w for w in report["writes"] if w["status"] == "WROTE"]
            self.assertEqual(wrote, [], f"candidate wrote a boundary record: {wrote}")
            self.assertEqual(len(report["writes"]), 4)
            self.assertTrue(all(w["error"] == "PermissionError" for w in report["writes"]),
                            report["writes"])

            # The active job is readable (it is not secret), and even knowing the
            # job id the candidate cannot plant the matching response.
            self.assertTrue(report["job_id_visible"])
            self.assertIn(f"response-{report['job_id_visible']}.json",
                          [w["file"] for w in report["writes"]])

            # The deny ACE survived every correction attempt, or could not be read.
            for label, snapshot in report["acl_after"].items():
                self.assertTrue(snapshot["rc"] != 0 or "(DENY)" in snapshot["output"],
                                f"{label} lost its deny ACE: {snapshot}")

            self.assertFalse((work / "response" / "evil.json").exists())
            self.assertEqual(
                protocol.sha256_file(work / "staging" / "body.py"), record["body_sha256"],
                "the active body was modified during the probe",
            )
            self.assertEqual(protocol.read_job(work / "staging")["job_id"], record["job_id"])

    def test_output_flood_is_bounded_and_contained(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            record = run_direct(fixture("big_output.py"), work, timeout=2.0)
            self.assertIn(record["status"], {"timeout", "output_limit"})
            self.assertTrue(record["tree_empty"])
            self.assertLessEqual(len(record["raw_stdout"]), 2048)


if __name__ == "__main__":
    unittest.main()
