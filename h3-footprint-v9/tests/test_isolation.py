from __future__ import annotations

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
            record = run_direct(fixture("boundary_probe.py"), work, timeout=2.0)
            self.assertIn(record["status"], {"ok", "error"})

            report = (work / "scratch" / "boundary_report.txt").read_text(encoding="utf-8")
            self.assertTrue(report.strip())
            self.assertFalse(any(line.startswith("WROTE") for line in report.splitlines()), report)
            self.assertTrue(any(line.startswith("BLOCKED") for line in report.splitlines()), report)

            self.assertFalse((work / "response" / "evil.json").exists())
            self.assertFalse((work / "response" / "response-forged.json").exists())
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
