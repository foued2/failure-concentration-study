from __future__ import annotations

import itertools
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import constants  # noqa: E402
import oracle  # noqa: E402


class InstrumentTests(unittest.TestCase):
    def test_probe_count_and_families(self):
        self.assertEqual(len(oracle.PROBES), 30)
        self.assertEqual(
            [p["family"] for p in oracle.PROBES],
            [f for f in constants.FAMILY_ORDER for _ in range(constants.PROBES_PER_FAMILY)],
        )

    def test_expected_matches_frozen_v8(self):
        frozen = HERE.parent.parent / "h3-footprint-v8" / "expected_values.json"
        self.assertTrue(frozen.exists(), f"frozen V8 expected values missing at {frozen}")
        recorded = json.loads(frozen.read_text(encoding="utf-8"))
        self.assertEqual(recorded, oracle.EXPECTED)

    def test_probe_input_hides_identity(self):
        payload = oracle.probe_input(oracle.PROBES[0])
        self.assertEqual(set(payload), {"n", "edges", "s", "t"})

    def test_answer_type_is_strict(self):
        self.assertTrue(oracle.answer_is_correct(9, 0))          # R1 -> 9
        self.assertFalse(oracle.answer_is_correct(True, 0))
        self.assertFalse(oracle.answer_is_correct(9.0, 0))
        self.assertFalse(oracle.answer_is_correct("9", 0))


class ConcentrationMathTests(unittest.TestCase):
    def _profiles(self, k: int):
        for parts in itertools.product(range(6), repeat=6):
            if sum(parts) == k:
                yield parts

    def test_saturation_forced_at_k_ge_25(self):
        """Six families x five probes: k >= 25 forces a fully failed family."""
        for k in range(25, 31):
            for parts in self._profiles(k):
                self.assertEqual(max(parts), 5, f"k={k} profile={parts}")

    def test_saturation_implies_c_equals_five_over_k(self):
        for k in range(1, 31):
            for parts in self._profiles(k):
                if max(parts) == 5:
                    rows = []
                    for family_index, count in enumerate(parts):
                        rows.extend([True] * count + [False] * (5 - count))
                    _, c = oracle.concentration(rows)
                    self.assertAlmostEqual(c, 5 / k, places=12)

    def test_c_can_vary_at_fixed_k_below_25(self):
        saturated = [True] * 5 + [True] * 5 + [True] * 5 + [True] * 5 + [True] * 4 + [False] * 6
        spread = ([True] * 4 + [False]) * 6
        self.assertEqual(sum(saturated), 24)
        self.assertEqual(sum(spread), 24)
        _, c_sat = oracle.concentration(saturated)
        _, c_spread = oracle.concentration(spread)
        self.assertAlmostEqual(c_sat, 5 / 24, places=12)
        self.assertAlmostEqual(c_spread, 4 / 24, places=12)
        self.assertNotEqual(c_sat, c_spread)


if __name__ == "__main__":
    unittest.main()
