from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import isolation_probe
import run_gate


class V8LowIntegrityTests(unittest.TestCase):
    def test_required_checks_include_lock_removal(self):
        self.assertIn("output_lock_removal_blocked", run_gate.REQUIRED_ISOLATION_CHECKS)
        self.assertIn("candidate_output_lock_removal_blocked", run_gate.REQUIRED_ISOLATION_CHECKS)

    def test_lock_removal_candidate_cannot_change_canaries(self):
        with tempfile.TemporaryDirectory() as td:
            direct, candidate, removal, candidate_removal, detail = isolation_probe._output_lock_checks(
                Path(td)
            )
        self.assertTrue(direct, detail)
        self.assertTrue(candidate, detail)
        self.assertTrue(removal, detail)
        self.assertTrue(candidate_removal, detail)
        self.assertIsNone(detail["lock_removal_candidate_excluded"])
        self.assertEqual(detail["lock_removal_candidate_k"], 30)
        self.assertFalse(detail["report_canary_changed_after_attack"])
        self.assertFalse(detail["result_canary_changed_after_attack"])

    def test_attack_source_uses_loaded_os_without_importing_it(self):
        source = isolation_probe._lock_removal_source(Path("C:/out"), "user", Path("C:/out/a"))
        self.assertIn('sys.modules.get("os")', source)
        self.assertIn("icacls", source)
        self.assertIn("takeown", source)
        self.assertIn("io.open", source)
        self.assertNotIn("import os", source)
        self.assertNotIn("import ctypes", source)
        self.assertIsNone(run_gate.unsafe_reason(source))

    @unittest.skipUnless(sys.platform == "win32", "Windows integrity levels only")
    def test_worker_drops_to_low_integrity_before_writing(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "medium-target.txt"
            target.write_text("trusted", encoding="utf-8")
            script = Path(td) / "drop.py"
            script.write_text(
                "import sys\n"
                f"sys.path.insert(0, {str(HERE)!r})\n"
                "import probe_worker\n"
                "probe_worker._drop_to_low_integrity()\n"
                "path = sys.argv[1]\n"
                "try:\n"
                "    open(path, 'a').write('tampered')\n"
                "except PermissionError:\n"
                "    print('WRITE_BLOCKED')\n"
                "else:\n"
                "    print('WRITE_ALLOWED')\n"
                "print(open(path, 'r').read())\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                [sys.executable, str(script), str(target)],
                capture_output=True, text=True, timeout=30,
                encoding="utf-8", errors="replace",
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertIn("WRITE_BLOCKED", proc.stdout)
            self.assertIn("trusted", proc.stdout)
            self.assertEqual(target.read_text(encoding="utf-8"), "trusted")


if __name__ == "__main__":
    unittest.main()
