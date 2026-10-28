from __future__ import annotations

import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import protocol  # noqa: E402
import winjob  # noqa: E402
from _support import fixture, run_direct  # noqa: E402


@unittest.skipUnless(winjob.IS_WINDOWS, "Job Objects require Windows")
class ProcessTreeTests(unittest.TestCase):
    def test_timeout_kills_descendants(self):
        with tempfile.TemporaryDirectory() as td:
            work = Path(td)
            record = run_direct(fixture("spawn_child.py"), work, timeout=0.8)
            self.assertEqual(record["status"], "timeout")
            self.assertTrue(record["timed_out"])
            self.assertTrue(record["tree_empty"], "job object still reports live processes")

            pid_file = work / "scratch" / "grandchild.pid"
            self.assertTrue(protocol.wait_for(pid_file.exists, 3.0))
            pid = int(pid_file.read_text(encoding="utf-8").strip())
            self.assertTrue(
                protocol.wait_for(lambda: not winjob.is_process_alive(pid), 5.0),
                f"grandchild {pid} survived the probe timeout",
            )


if __name__ == "__main__":
    unittest.main()
