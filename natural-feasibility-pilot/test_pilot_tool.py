"""Bounded software checks; fixtures are synthetic and are not solver observations."""
from __future__ import annotations

import unittest
import json

from study.families import FAMILY_ORDER
from study.instances import make_hidden_suite
from study.probes import make_probe_suite
from study.sssp import dijkstra_ref
from pilot_tool import (
    attempt_id, body_id, check_edge_fixtures, check_input_separation, derive_features, input_id,
    jsonl_text, make_attempt_record, validate_records, validate_trace,
)


def rows_with_failed_slots(slots: set[int]) -> list[dict]:
    rows = []
    for i in range(30):
        rows.append({
            "family": FAMILY_ORDER[i // 5], "variant": i % 5,
            "status": "wrong" if i in slots else "pass",
        })
    return rows


class PilotToolTests(unittest.TestCase):
    def test_four_failures_one_family(self):
        got = derive_features(rows_with_failed_slots({0, 1, 2, 3}))
        self.assertEqual((got["k"], got["C"]), (4, 1.0))

    def test_two_failures_in_each_of_two_families(self):
        got = derive_features(rows_with_failed_slots({0, 1, 5, 6}))
        self.assertEqual((got["k"], got["C"]), (4, 0.5))

    def test_one_failure_in_each_of_four_families(self):
        got = derive_features(rows_with_failed_slots({0, 5, 10, 15}))
        self.assertEqual((got["k"], got["C"]), (4, 0.25))

    def test_counts_sum_to_k_and_zero_convention(self):
        got = derive_features(rows_with_failed_slots(set()))
        self.assertEqual(got["k"], sum(got["family_counts"].values()))
        self.assertEqual((got["k"], got["C"]), (0, 0.0))

    def test_timeout_and_invalid_remain_failure_statuses(self):
        rows = rows_with_failed_slots(set())
        rows[0]["status"] = "timeout"
        rows[5]["status"] = "invalid"
        got = derive_features(rows)
        self.assertEqual((got["k"], got["C"]), (2, 0.5))
        records = [json.loads(line) for line in jsonl_text([
            {"probe_index": 1, "status": "timeout"},
            {"probe_index": 2, "status": "invalid"},
        ]).splitlines()]
        self.assertEqual([r["status"] for r in records], ["timeout", "invalid"])
        rows[6]["status"] = "not_run"
        with self.assertRaises(ValueError):
            derive_features(rows)

    def test_duplicate_attempts_are_preserved_but_body_identity_matches(self):
        source = "def solve():\r\n    return 1\r\n"
        self.assertEqual(body_id(source), body_id(source.replace("\r\n", "\n")))
        self.assertNotEqual(attempt_id(1), attempt_id(2))
        first = make_attempt_record(1, source, {"model": "test"})
        second = make_attempt_record(2, source, {"model": "test"}, known_bodies={first["body_id"]: first["attempt_id"]})
        decoded = [json.loads(line) for line in jsonl_text([first, second]).splitlines()]
        self.assertEqual(len(decoded), 2)
        self.assertEqual(decoded[1]["duplicate_of_attempt_id"], first["attempt_id"])

    def test_input_duplicates_and_overlap_detected(self):
        x = {"n": 2, "edges": [(0, 1, 2)], "s": 0, "t": 1}
        y = {"n": 2, "edges": [(0, 1, 3)], "s": 0, "t": 1}
        got = check_input_separation([x], [y, y])
        self.assertFalse(got["passed"])
        self.assertEqual(len(got["evaluation_duplicates"]), 1)
        self.assertEqual(input_id(x), input_id(dict(x)))
        overlap = check_input_separation([x], [x])
        self.assertEqual(len(overlap["diagnostic_evaluation_overlap"]), 1)

    def test_frozen_generator_bank_is_unique_and_probe_disjoint(self):
        diagnostic = make_probe_suite(20261020)
        evaluation = make_hidden_suite(20261020, m_count=20)
        got = check_input_separation(diagnostic, evaluation)
        self.assertEqual(got["evaluation_count"], 20)
        self.assertTrue(got["passed"], got)
        fixtures = check_edge_fixtures(evaluation)
        self.assertTrue(fixtures["passed"], fixtures)
        self.assertTrue(fixtures["all_expected_present"], fixtures)
        self.assertEqual(fixtures["counts"], {f"e{i}": 1 for i in range(5)})

    def test_reference_oracle_known_bounded_cases(self):
        self.assertEqual(dijkstra_ref(3, [(0, 1, 4), (1, 2, 2)], 0, 2), 6)
        self.assertIsNone(dijkstra_ref(3, [(0, 1, 4)], 0, 2))

    def test_trace_integrity_links_body_and_input(self):
        bid = body_id("def solve(): pass\n")
        attempts = [{"attempt_id": attempt_id(1), "body_id": bid}]
        diagnostics = [{"attempt_id": attempt_id(1), "body_id": bid, "probe_id": "F1_0", "input_id": "probe1", "status": "pass"}]
        evaluations = [{"attempt_id": attempt_id(1), "body_id": bid, "input_id": "abc", "status": "complete", "solver_output": 2, "oracle_output": 2, "correct": True}]
        self.assertEqual(validate_trace(attempts, diagnostics, evaluations), [])
        self.assertTrue(validate_trace(attempts, [], [{"body_id": "missing", "status": "complete", "input_id": "x"}]))

    def test_record_schema_and_feature_reconstruction(self):
        source = "def solve(): pass\n"
        attempt = make_attempt_record(1, source, {"model": "synthetic-test"}, "synthetic-config")
        bid = attempt["body_id"]
        diag = []
        for row in rows_with_failed_slots({0, 1, 5}):
            diag.append({**row, "attempt_id": attempt["attempt_id"], "body_id": bid,
                         "probe_id": f"{row['family']}_{row['variant']}", "input_id": f"p{len(diag)}",
                         "solver_output": 1, "oracle_output": 1, "error": None, "timeout_seconds": None})
        feature = {"attempt_id": attempt["attempt_id"], "body_id": bid, **derive_features(diag)}
        evaluation = [{"attempt_id": attempt["attempt_id"], "body_id": bid, "input_id": "eval1",
                       "status": "complete", "solver_output": 4, "oracle_output": 4, "correct": True,
                       "error": None, "timeout_seconds": None}]
        self.assertEqual(validate_records([attempt], diag, evaluation, [feature], {"eval1"}), [])
        feature["k"] = 99
        self.assertTrue(validate_records([attempt], diag, evaluation, [feature], {"eval1"}))


if __name__ == "__main__":
    unittest.main()
