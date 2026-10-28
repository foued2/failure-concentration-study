from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import controller  # noqa: E402
from _support import fixture  # noqa: E402


class OracleControls(unittest.TestCase):
    """Known-good and known-bad fixtures must produce exact failure counts."""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._tmp.cleanup)
        cls.work = Path(cls._tmp.name) / "work"
        cls.ctl = controller.Controller(cls.work)

    def test_correct_solver_scores_zero_failures(self):
        row = self.ctl.evaluate(fixture("correct.py"), group_id="g-correct")
        self.assertIsNone(row["excluded"])
        self.assertEqual(row["probes_completed"], 30)
        self.assertEqual(row["k"], 0)
        self.assertEqual(row["C"], 0.0)
        self.assertFalse(row["eligible"])

    def test_constant_wrong_solver_fails_every_probe(self):
        row = self.ctl.evaluate(fixture("wrong_constant.py"), group_id="g-wrong")
        self.assertIsNone(row["excluded"])
        self.assertEqual(row["k"], 30)
        self.assertEqual(row["max_f"], 5)
        self.assertTrue(row["saturated"])
        self.assertFalse(row["eligible"])
        self.assertAlmostEqual(row["C"], 5 / 30, places=12)

    def test_sys_exit_counts_as_probe_failure(self):
        row = self.ctl.evaluate(fixture("sys_exit.py"), group_id="g-exit")
        self.assertIsNone(row["excluded"], "a raising solver is a failing solver, not an invalid one")
        self.assertEqual(row["k"], 30)

    def test_stdout_hijack_cannot_improve_score(self):
        row = self.ctl.evaluate(fixture("stdout_hijack.py"), group_id="g-hijack")
        self.assertIsNone(row["excluded"])
        # A fixed forged guess can collide with a genuine expected value (Z4 is
        # 0), so it may win a single probe. It can never produce a perfect score
        # or an eligible row, because the child has no reference data.
        self.assertNotEqual(row["k"], 0, "forged output produced a perfect score")
        self.assertFalse(row["eligible"])
        self.assertGreaterEqual(row["k"], 29)

    def test_compound_read_and_forge_attack_never_passes(self):
        row = self.ctl.evaluate(fixture("forgery.py"), group_id="g-forgery")
        self.assertIsNone(row["excluded"])
        self.assertNotEqual(row["k"], 0, "the compound attack achieved a perfect score")
        self.assertFalse(row["eligible"])

        report = (self.work / "case" / "scratch" / "probe_report.txt")
        self.assertTrue(report.exists())
        self.assertEqual(report.read_text(encoding="utf-8").strip(), "",
                         "candidate found reference material on a reachable path")


class JobOrdering(unittest.TestCase):
    def test_publish_refuses_after_untidy_tree(self):
        with tempfile.TemporaryDirectory() as td:
            ctl = controller.Controller(Path(td) / "work")
            ctl._last_tree_empty = False
            with self.assertRaises(controller.FatalBoundaryError):
                ctl._publish(Path(td) / "staging", b"def solve(*a):\n    return 0\n",
                             "probe", 0, {"n": 1, "edges": [], "s": 0, "t": 0})


if __name__ == "__main__":
    unittest.main()
