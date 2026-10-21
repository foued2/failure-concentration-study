"""Synthetic controlled calibration checks; not evidence about generated solvers."""
from __future__ import annotations

import unittest

from calibration import CASES, SEED, run_case
from study.probes import make_probe_suite


class DiagnosticCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.probes = make_probe_suite(SEED)

    def test_all_pass_reference_solver_path(self):
        result = run_case(self.probes, CASES[0])
        self.assertEqual((result["k"], result["C"]), (0, 0.0))
        self.assertEqual(sum(row["failed"] for row in result["probe_records"]), 0)

    def test_k4_concentrated_in_one_family(self):
        result = run_case(self.probes, CASES[1])
        self.assertEqual(result["family_counts"], {"F1": 4, "F2": 0, "F3": 0, "F4": 0, "F5": 0, "F6": 0})
        self.assertEqual((result["k"], result["C"]), (4, 1.0))

    def test_k4_split_across_two_families(self):
        result = run_case(self.probes, CASES[2])
        self.assertEqual(result["family_counts"], {"F1": 2, "F2": 2, "F3": 0, "F4": 0, "F5": 0, "F6": 0})
        self.assertEqual((result["k"], result["C"]), (4, 0.5))

    def test_k4_split_across_four_families(self):
        result = run_case(self.probes, CASES[3])
        self.assertEqual(result["family_counts"], {"F1": 1, "F2": 1, "F3": 1, "F4": 1, "F5": 0, "F6": 0})
        self.assertEqual((result["k"], result["C"]), (4, 0.25))

    def test_every_case_runs_all_probes_and_matches_targeted_failures(self):
        for case in CASES:
            with self.subTest(case=case["case_id"]):
                result = run_case(self.probes, case)
                self.assertEqual(len(result["probe_records"]), 30)
                self.assertTrue(result["matches_expected"])


if __name__ == "__main__":
    unittest.main()
