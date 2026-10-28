from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

import backend  # noqa: E402
import controller  # noqa: E402
from _support import fixture, seed_targets  # noqa: E402

V9 = HERE.parent


def host_controller(root: Path, case_paths=None) -> controller.Controller:
    return controller.Controller(
        root / "work",
        transport=backend.HostLocalTransport(root / "rt"),
        case_paths=case_paths,
    )


def case_dirs(root: Path):
    paths = tuple(root / name for name in ("staging", "response", "scratch"))
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
    return paths


def reference_targets() -> dict[str, str]:
    return {
        "oracle": str(V9 / "oracle.py"),
        "expected_values": str(V9.parent / "h3-footprint-v8" / "expected_values.json"),
        "controller": str(V9 / "controller.py"),
    }


class HostBoundaryExposure(unittest.TestCase):
    """The host-local transport is not an isolation boundary.

    These tests intentionally assert the exposure. The previous revision
    asserted that the attack found nothing, but its fixture only walked its own
    scratch directory, so a green result measured the fixture's search depth
    rather than the boundary.
    """

    def test_host_backend_exposes_the_reference_data(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = host_controller(root, case_paths=case_dirs(root))
            seed_targets(root, **reference_targets())
            row = ctl.evaluate(fixture("oracle_hunt.py"), group_id="g-exposure")
            self.assertIsNone(row["excluded"])

            report = json.loads((root / "scratch" / "oracle_hunt.json").read_text(encoding="utf-8"))
            status = {entry["label"]: entry["status"] for entry in report}
            self.assertEqual(
                status.get("oracle"), "READ",
                "expected the host backend to expose oracle.py; if this ever fails, "
                "the host transport has gained a real barrier and the docs must change",
            )
            self.assertEqual(status.get("expected_values"), "READ")
            self.assertFalse(row["isolation_verified"])
            self.assertFalse(row["authorized"])

    def test_host_backend_lets_an_attack_score_perfectly(self):
        """Keys + channel control = fabricated correct answers, exactly the V8 finding."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = host_controller(root, case_paths=case_dirs(root))
            seed_targets(root, **reference_targets())
            row = ctl.evaluate(fixture("key_reader.py"), group_id="g-perfect")
            self.assertIsNone(row["excluded"])
            self.assertEqual(row["k"], 0, "the key-reading fixture failed to reach the oracle")
            self.assertFalse(row["isolation_verified"])
            self.assertFalse(row["authorized"])

    def test_attack_without_the_host_path_falls_back_to_guessing(self):
        """Without a usable path the same attack cannot answer the probes."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = host_controller(root, case_paths=case_dirs(root))
            row = ctl.evaluate(fixture("key_reader.py"), group_id="g-guess")
            self.assertIsNone(row["excluded"])
            self.assertEqual(row["k"], 30)

    def test_authorized_evaluation_refuses_the_host_transport(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = host_controller(root)
            with self.assertRaises(controller.BoundaryNotEstablished):
                ctl.evaluate_authorized(fixture("correct.py"), group_id="g-refused")


class ScoringLogicOnHostBackend(unittest.TestCase):
    """Oracle-control tests. These are scoring-logic tests, not isolation evidence.

    They run on the host transport because the Sandbox is unavailable here; every
    row they produce is marked ``authorized: false``.
    """

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls._tmp.cleanup)
        cls.root = Path(cls._tmp.name)
        cls.ctl = host_controller(cls.root)

    def test_correct_solver_scores_zero_failures(self):
        row = self.ctl.evaluate(fixture("correct.py"), group_id="g-correct")
        self.assertIsNone(row["excluded"])
        self.assertEqual(row["probes_completed"], 30)
        self.assertEqual(row["k"], 0)
        self.assertEqual(row["C"], 0.0)
        self.assertFalse(row["eligible"])
        self.assertFalse(row["authorized"])

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
        # 0), so it may win a single probe. It cannot win without the key.
        self.assertNotEqual(row["k"], 0, "forged output produced a perfect score")
        self.assertFalse(row["eligible"])
        self.assertGreaterEqual(row["k"], 29)


class JobOrdering(unittest.TestCase):
    def test_publish_refuses_after_untidy_tree(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ctl = host_controller(root)
            ctl._last_tree_empty = False
            with self.assertRaises(controller.FatalBoundaryError):
                ctl._publish(root / "staging", b"def solve(*a):\n    return 0\n",
                             "probe", 0, {"n": 1, "edges": [], "s": 0, "t": 0})


if __name__ == "__main__":
    unittest.main()
