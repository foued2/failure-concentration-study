from __future__ import annotations

import json
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import isolation_probe
import run_gate


class V7OutputBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.results = self.root / "results"
        self.results.mkdir()
        self.canary = self.results / "footprint.json"
        self.canary.write_text("trusted", encoding="utf-8")

    def tearDown(self):
        run_gate.unlock_output(self.root)
        self.tmp.cleanup()

    def test_lock_blocks_io_open_and_preserves_content(self):
        lock = run_gate.lock_output(self.root)
        self.assertTrue(lock["ok"], lock["errors"])
        try:
            self.assertEqual(self.canary.read_text(encoding="utf-8"), "trusted")
            with self.assertRaises(PermissionError):
                with self.canary.open("a", encoding="utf-8") as handle:
                    handle.write("tampered")
            row = isolation_probe._control_row(
                isolation_probe._io_open_source(self.canary), "io_open_output"
            )
            self.assertIsNone(row["excluded"])
            self.assertEqual(row["k"], 30)
            self.assertEqual(self.canary.read_text(encoding="utf-8"), "trusted")
        finally:
            unlock = run_gate.unlock_output(self.root)
            self.assertTrue(unlock["ok"], unlock["errors"])

    def test_preopened_handle_survives_lock(self):
        handle = self.canary.open("w", encoding="utf-8", newline="\n")
        lock = run_gate.lock_output(self.root)
        self.assertTrue(lock["ok"], lock["errors"])
        try:
            handle.write("trusted-result")
            handle.flush()
            handle.close()
            self.assertEqual(self.canary.read_text(encoding="utf-8"), "trusted-result")
        finally:
            if not handle.closed:
                handle.close()
            self.assertTrue(run_gate.unlock_output(self.root)["ok"])

    def test_unlock_restores_write(self):
        self.assertTrue(run_gate.lock_output(self.root)["ok"])
        self.assertTrue(run_gate.unlock_output(self.root)["ok"])
        with self.canary.open("a", encoding="utf-8") as handle:
            handle.write("-restored")
        self.assertEqual(self.canary.read_text(encoding="utf-8"), "trusted-restored")

    def test_isolation_report_must_be_outside_output_root(self):
        self.assertFalse(run_gate.isolation_report_outside_output(self.canary, self.root))
        outside = self.root.parent / (self.root.name + "-isolation.json")
        try:
            outside.write_text("{}", encoding="utf-8")
            self.assertTrue(run_gate.isolation_report_outside_output(outside, self.root))
        finally:
            outside.unlink(missing_ok=True)

    def test_writable_probe_returns_false_for_missing_file(self):
        self.assertFalse(run_gate.path_is_writable(self.results / "missing.json"))
        self.assertTrue(run_gate.path_is_writable(self.canary))

    def test_main_refuses_report_inside_output_root(self):
        argv = [
            "run_gate.py",
            "--results-dir", str(self.results),
            "--freeze-manifest", str(self.root / "FREEZE.json"),
            "--isolation-report", str(self.canary),
        ]
        with mock.patch.object(sys, "argv", argv):
            with self.assertRaises(SystemExit) as exc:
                run_gate.main()
        self.assertIn("outside the writable output root", str(exc.exception))

    def test_main_writes_under_lock_and_unlocks(self):
        with tempfile.TemporaryDirectory() as evidence:
            report = Path(evidence) / "isolation-report.json"
            report.write_text("{}", encoding="utf-8")
            report.chmod(stat.S_IREAD)
            argv = [
                "run_gate.py",
                "--results-dir", str(self.results),
                "--freeze-manifest", str(self.root / "FREEZE.json"),
                "--isolation-report", str(report),
            ]
            integrity = {"ok": True, "manifest": "fixture", "checked": {}}
            try:
                with mock.patch.object(sys, "argv", argv), \
                     mock.patch.object(run_gate, "verify_frozen", return_value=integrity), \
                     mock.patch.object(run_gate, "load_isolation_report",
                                       return_value={"ok": True, "failed_checks": [], "path": str(report)}), \
                     mock.patch.object(run_gate, "build", return_value={"verdict": "FAIL", "reason": "fixture"}), \
                     mock.patch.object(run_gate, "markdown", return_value="FIXTURE REPORT\n"), \
                     mock.patch("builtins.print"):
                    run_gate.main()
            finally:
                report.chmod(stat.S_IWRITE)
            written = json.loads((self.results / "footprint.json").read_text(encoding="utf-8"))
            self.assertTrue(written["output_boundary"]["locked_during_candidates"])
            self.assertEqual(written["verdict"], "FAIL")
            with (self.results / "footprint.json").open("a", encoding="utf-8") as handle:
                handle.write("")


if __name__ == "__main__":
    unittest.main()
