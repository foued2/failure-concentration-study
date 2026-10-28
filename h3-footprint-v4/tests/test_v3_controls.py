from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import run_gate


def profile(name, max_f, k, c, group_id, batch_id, counts=None):
    if counts is None:
        counts = {family: 0 for family in ("R", "Z", "A", "I", "S", "U")}
        counts["R"] = max_f
    return {
        "body_hash": name, "base_algorithm": "heap_dijkstra", "excluded": None,
        "k": k, "C": c, "max_f": max_f, "family_counts": counts,
        "eligible": 2 <= k <= 24, "group_id": group_id, "batch_id": batch_id,
        "generator": "fixture", "prompt_variant": "test",
    }


class SaturationMetricTests(unittest.TestCase):
    def test_low_k_single_family_two_probe_failure_is_not_saturated(self):
        rows = [profile("a", max_f=2, k=2, c=1.0, group_id="g", batch_id=0)]
        self.assertEqual(run_gate._saturation_rate(rows), 0.0)
        self.assertGreater(run_gate._all_or_none_fraction(rows), 0.80)

    def test_fully_failed_family_is_saturated(self):
        rows = [
            profile("a", max_f=5, k=5, c=1.0, group_id="g0", batch_id=0),
            profile("b", max_f=5, k=8, c=1.0, group_id="g1", batch_id=1),
        ]
        self.assertEqual(run_gate._saturation_rate(rows), 1.0)

    def test_empty_set_reports_none(self):
        self.assertIsNone(run_gate._saturation_rate([]))


class FutilityTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.gen = Path(self.tmp.name)
        self.old = run_gate.GEN
        run_gate.GEN = self.gen

    def tearDown(self):
        run_gate.GEN = self.old
        self.tmp.cleanup()

    def write_batches(self, count):
        with (self.gen / "attempts.jsonl").open("w", encoding="utf-8") as fh:
            for batch in range(count):
                fh.write(json.dumps({"batch_id": batch, "completed": True}) + "\n")

    def test_checkpoint_not_reached_before_100_batches(self):
        self.write_batches(99)
        eligible = [profile("a", 2, 2, 1.0, "g0", 0)]
        result = run_gate._futility(eligible)
        self.assertFalse(result["triggered"])
        self.assertEqual(result["completed_batches"], 99)
        self.assertIsNone(result["checkpoints"][0]["eligible_groups_at_checkpoint"])

    def test_below_pace_at_100_triggers(self):
        self.write_batches(100)
        eligible = [profile("a", 2, 2, 1.0, "g%d" % i, i) for i in range(9)]
        result = run_gate._futility(eligible)
        self.assertTrue(result["triggered"])
        self.assertEqual(result["first_triggered_batch"], 100)

    def test_at_pace_at_100_does_not_trigger(self):
        self.write_batches(100)
        eligible = [profile("a", 2, 2, 1.0, "g%d" % i, i) for i in range(10)]
        result = run_gate._futility(eligible)
        self.assertFalse(result["triggered"])

    def test_groups_from_batches_at_or_after_checkpoint_do_not_count(self):
        self.write_batches(100)
        eligible = [profile("a", 2, 2, 1.0, "g%d" % i, 100 + i) for i in range(30)]
        result = run_gate._futility(eligible)
        self.assertTrue(result["triggered"])


class VerdictTests(unittest.TestCase):
    def test_high_all_or_none_without_saturation_is_not_degeneracy_fail(self):
        rows = [profile("a%d" % i, 2, 2, 1.0, "g%d" % i, i) for i in range(6)]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bodies = root / "generated" / "bodies"
            bodies.mkdir(parents=True)
            for row in rows:
                (bodies / (row["body_hash"] + ".py")).write_text("fixture", encoding="utf-8")
            old = {
                "ROOT": run_gate.ROOT, "GEN": run_gate.GEN,
                "BODIES": run_gate.BODIES, "WORKER": run_gate.WORKER,
            }
            try:
                run_gate.ROOT = root
                run_gate.GEN = root / "generated"
                run_gate.BODIES = bodies
                run_gate.WORKER = root / "probe_worker.py"
                with mock.patch.object(run_gate, "body_meta", return_value={}), mock.patch.object(
                    run_gate, "evaluate_body", side_effect=lambda path, meta: rows[int(path.stem[1:])]
                ):
                    report = run_gate.build()
            finally:
                for key, value in old.items():
                    setattr(run_gate, key, value)
        self.assertGreater(report["all_or_none_fraction_eligible"], 0.80)
        self.assertEqual(report["saturation_rate_eligible"], 0.0)
        self.assertNotEqual(report["reason"], "degeneracy_saturation_among_eligible_k")


if __name__ == "__main__":
    unittest.main()
