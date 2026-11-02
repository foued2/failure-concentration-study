from __future__ import annotations

import hashlib
import json
import random
import tempfile
import unittest
from pathlib import Path

import lc518_generator as g


class TraceRandom:
    """Synthetic trace RNG. It records calls and never seeds a study stream."""
    def __init__(self, overrides: dict[int, int] | None = None):
        self.calls = 0
        self.overrides = overrides or {}

    def randrange(self, start: int, stop: int | None = None) -> int:
        if stop is None:
            start, stop = 0, start
        idx = self.calls
        self.calls += 1
        value = self.overrides.get(idx, start + (idx % (stop - start)))
        if not start <= value < stop:
            raise AssertionError(f"synthetic value {value} outside [{start},{stop})")
        return value

    def shuffle(self, values: list[object]) -> None:
        values.reverse()


class ConstantRandom:
    def __init__(self, value: int):
        self.value = value
        self.calls = 0

    def randrange(self, start: int, stop: int | None = None) -> int:
        self.calls += 1
        if stop is None:
            start, stop = 0, start
        return self.value

    def shuffle(self, values: list[object]) -> None:
        values.reverse()


class DrawOrderTests(unittest.TestCase):
    def trace(self, stratum: str, k: int, overrides=None):
        calls: list[tuple[str, object]] = []
        candidate = g.draw_raw_candidate(stratum, k, TraceRandom(overrides), trace=calls)
        return candidate, [label for label, _ in calls]

    def expect(self, stratum, k, labels, overrides=None):
        _, observed = self.trace(stratum, k, overrides)
        self.assertEqual(observed, labels, f"draw-order mismatch for {stratum} record {k}")

    def test_every_stratum_and_pair_type_draw_order(self):
        # The fixtures record draw labels only. No bank rows are assembled or written.
        self.expect("D1", 1, ["n", "coins[1]"])
        self.expect("D2", 1, ["m", "c_star", "distractors[1]"])
        self.expect("D3", 1, ["n", "coins[1]", "coins[2]"])
        self.expect("D3", 1, ["n", "coins[1]", "coins[2]", "amount"], {1: 3, 2: 4})
        early, early_labels = self.trace("D3", 1, {1: 1})
        self.assertEqual(early_labels, ["n", "coins[1]", "coins[2]"])
        self.assertEqual(early.early_reject_reason, "MIN_COIN_ONE")
        self.expect("D3", 5, ["g", "n", "t[1]", "t[2]", "t[3]", "amount"])
        self.expect("D4", 1, ["n", "t[1]", "t[2]", "amount_half"])
        self.expect("D4", 3, ["n", "t[1]", "t[2]", "amount_half"])
        self.expect("D4", 5, ["n", "t[1]", "t[2]", "amount_half"])
        early, early_labels = self.trace("D4", 5, {1: 2, 2: 4})
        self.assertEqual(early_labels, ["n", "t[1]", "t[2]"])
        self.assertEqual(early.early_reject_reason, "D4_GCD_NOT_ONE")
        self.expect("D5", 1, [])
        self.expect("D5", 2, [])
        self.expect("D5", 3, ["n", "further_coins[1]", "further_coins[2]", "amount"])
        self.expect("D6", 1, ["amount", "n", "coins[1]", "coins[2]", "coins[3]", "coins[4]", "shuffle"])
        # Wide-n and many-coins counts are taken from the synthetic candidate,
        # then each slot must be drawn in monotonically increasing slot order.
        c, labels = self.trace("D7", 1)
        self.assertEqual(labels[:2], ["amount", "n"])
        self.assertEqual(labels[2:], [f"coins[{i}]" for i in range(1, len(c.records[0].coins) + 1)])
        c, labels = self.trace("D8", 1)
        self.assertEqual(labels[:2], ["amount", "n"])
        self.assertEqual(labels[2:], [f"coins[{i}]" for i in range(1, len(c.records[0].coins) + 1)])

        self.expect("H1", 1, ["amount", "n", "coins[1]", "coins[2]"])
        self.expect("H1", 4, [])
        self.expect("H1", 5, ["amount", "n", "coins[1]", "coins[2]"])
        self.expect("H2", 1, ["n", "remaining_coins[1]"])
        self.expect("H2", 2, ["n", "remaining_coins[1]", "amount"])
        self.expect("H2", 5, [])
        self.expect("H2", 6, ["n", "coins[1]", "coins[2]", "amount"])
        self.expect("H3", 1, [])
        self.expect("H3", 2, ["amount", "coin"])
        self.expect("H4", 1, ["coins[1]", "coins[2]"])
        self.expect("H4", 3, [])
        self.expect("H4", 4, ["amount", "coins[1]", "coins[2]"])
        c, labels = self.trace("H5", 1)
        self.assertEqual(labels[:2], ["amount", "n"])
        self.assertEqual(labels[2:], [f"coins[{i}]" for i in range(1, len(c.records[0].coins) + 1)])
        self.expect("H6", 1, ["amount", "n", "coins[1]", "coins[2]", "coins[3]", "coins[4]", "coins[5]", "coins[6]"])
        self.expect("H6", 7, ["amount", "n", "coins[1]", "coins[2]", "coins[3]", "coins[4]", "coins[5]", "coins[6]", "shuffle"])
        self.expect("H7", 1, ["n", "coins[1]", "coins[2]"])
        self.expect("H7", 1, ["n", "coins[1]", "coins[2]", "amount"], {1: 3, 2: 4})
        early, early_labels = self.trace("H7", 1, {1: 1})
        self.assertEqual(early_labels, ["n", "coins[1]", "coins[2]"])
        self.assertEqual(early.early_reject_reason, "MIN_COIN_ONE")
        self.expect("H7", 5, ["g", "n", "t[1]", "t[2]", "t[3]", "amount"])
        self.expect("H8", 1, ["n", "amount"])
        self.expect("H8", 7, [])
        self.expect("H8", 8, ["n", "amount"])

    def test_every_stratum_uses_its_pinned_inclusive_draw_ranges(self):
        cases = [
            ("D1", 1, {}, {"n": (1, 4), "coins": (1, 20)}),
            ("D2", 1, {}, {"m": (1, 4), "c_star": (1, 5000), "distractors": (1, 5000)}),
            ("D3", 1, {0: 2, 1: 3, 2: 4}, {"n": (2, 6), "coins": (1, 5000), "amount": (1, 2)}),
            ("D3", 5, {}, {"g": (2, 10), "n": (2, 6), "t": (1, 2500), "amount": (1, 5000)}),
            ("D4", 1, {}, {"n": (2, 6), "t": (1, 2500), "amount_half": (0, 2500)}),
            ("D4", 3, {}, {"n": (2, 6), "t": (1, 2500), "amount_half": (0, 2499)}),
            ("D4", 5, {}, {"n": (2, 6), "t": (1, 2500), "amount_half": (0, 2499)}),
            ("D5", 3, {}, {"n": (3, 5), "further_coins": (2, 9), "amount": (5, 30)}),
            ("D6", 1, {}, {"amount": (10, 200), "n": (3, 8), "coins": (1, 200)}),
            ("D7", 1, {}, {"amount": (50, 500), "n": (50, 300), "coins": (1, 5000)}),
            ("D8", 1, {}, {"amount": (2000, 5000), "n": (3, 30), "coins": (1, 5000)}),
            ("H1", 1, {}, {"amount": (0, 1), "n": (1, 4), "coins": (1, 20)}),
            ("H1", 5, {}, {"amount": (2, 12), "n": (1, 4), "coins": (1, 20)}),
            ("H2", 1, {}, {"n": (2, 6), "remaining_coins": (2, 60)}),
            ("H2", 2, {}, {"n": (2, 6), "remaining_coins": (2, 60), "amount": (13, 60)}),
            ("H2", 6, {}, {"n": (2, 6), "coins": (1, 60), "amount": (13, 60)}),
            ("H3", 2, {}, {"amount": (0, 5000), "coin": (1, 50)}),
            ("H4", 1, {}, {"coins": (1, 5000)}),
            ("H4", 4, {}, {"amount": (20, 5000), "coins": (1, 5000)}),
            ("H5", 1, {}, {"amount": (100, 2000), "n": (30, 120), "coins": (1, 5000)}),
            ("H6", 1, {}, {"amount": (3500, 5000), "n": (5, 40), "coins": (1, 5000)}),
            ("H6", 7, {}, {"amount": (3500, 5000), "n": (5, 40), "coins": (1, 5000)}),
            ("H7", 1, {0: 2, 1: 3, 2: 4}, {"n": (2, 6), "coins": (1, 5000), "amount": (1, 2)}),
            ("H7", 5, {}, {"g": (2, 10), "n": (2, 6), "t": (1, 2500), "amount": (1, 5000)}),
            ("H8", 1, {}, {"n": (3, 8), "amount": (6, 800)}),
            ("H8", 8, {}, {"n": (3, 8), "amount": (6, 800)}),
        ]
        for stratum, k, overrides, bounds in cases:
            trace = []
            g.draw_raw_candidate(stratum, k, TraceRandom(overrides), trace=trace)
            for label, observed_range in trace:
                if label == "shuffle":
                    self.assertEqual(observed_range, "permutation")
                    continue
                family = label.split("[", 1)[0]
                self.assertIn(family, bounds, f"unexpected draw {stratum}:{k} {label}")
                self.assertEqual(observed_range, bounds[family], f"range mismatch {stratum}:{k} {label}")

    def test_fixed_records_consume_no_random_draws(self):
        class NoDraw:
            def randrange(self, *args):
                raise AssertionError("fixed record consumed randrange")
            def shuffle(self, values):
                raise AssertionError("fixed record consumed shuffle")
        for stratum, k in [("D5", 1), ("D5", 2), ("H1", 4), ("H2", 5), ("H3", 1), ("H4", 3), ("H8", 7)]:
            candidate = g.draw_raw_candidate(stratum, k, NoDraw())
            self.assertEqual(len(candidate.records), 1)


class PipelineTests(unittest.TestCase):
    def test_fixed_key_preflight_and_d5_exclusion(self):
        fixed_d, fixed_h = g.fixed_key_preflight()
        self.assertEqual(len(fixed_d), 2)
        self.assertEqual(len(fixed_h), 5)
        self.assertFalse(fixed_d & fixed_h)
        result = g.validate_d5_structural_exclusion()
        self.assertEqual(set(result), {f"H{i}" for i in range(1, 9)})
        self.assertTrue(all(result.values()))

    def test_record_ids_and_pair_ids_follow_bank_generation_order(self):
        self.assertEqual(g.planned_input_id("diagnostic", "D6", 1), "D041")
        self.assertEqual(g.planned_input_id("diagnostic", "D6", 8), "D048")
        self.assertEqual(g.planned_input_id("heldout", "H6", 7), "H057")
        self.assertEqual(g.planned_input_id("heldout", "H8", 12), "H080")
        self.assertEqual(g.planned_candidate_id("diagnostic", "D6", (1, 2)), "D6-P01")
        self.assertEqual(g.planned_candidate_id("diagnostic", "D6", (7, 8)), "D6-P04")
        self.assertEqual(g.planned_candidate_id("heldout", "H6", (7, 8)), "H6-P01")
        self.assertEqual(g.planned_candidate_id("heldout", "H6", (9, 10)), "H6-P02")
        self.assertEqual(sum(g.QUOTAS[f"D{i}"] for i in range(1, 9)), 64)
        self.assertEqual(sum(g.QUOTAS[f"H{i}"] for i in range(1, 9)), 80)

    def test_fixed_repeated_use_witnesses_satisfy_exact_dp_predicate(self):
        _, fixed_h = g.fixed_candidates()
        expected = {
            "H1:4": (12, (2, 3), 3, 0),
            "H2:5": (60, (2, 58), 2, 1),
            "H3:1": (100, (50,), 1, 0),
            "H4:3": (100, (4, 96), 2, 1),
        }
        for key, (amount, coins, answer, n0) in expected.items():
            raw = fixed_h[key].records[0]
            self.assertEqual((raw.amount, raw.coins), (amount, coins))
            self.assertEqual(g.combinations_count(amount, coins), answer)
            self.assertEqual(g.no_reuse_subset_count(amount, coins), n0)
            self.assertGreater(answer, n0)

    def test_predicate_log_is_emitted_once_after_accepted_h1_record_is_appended(self):
        from unittest.mock import patch
        generator = g.ProductionGenerator()
        order = []
        emitted = []
        original_append = generator._append_accepted

        def append_spy(*args, **kwargs):
            result = original_append(*args, **kwargs)
            order.append(("accepted", len(generator.heldout)))
            return result

        def emit_spy(tag, payload):
            emitted.append((tag, payload))
            order.append(("emitted", len(generator.heldout)))

        class NoDraw:
            def randrange(self, *args):
                raise AssertionError("fixed witness consumed RNG")
            def shuffle(self, values):
                raise AssertionError("fixed witness consumed shuffle")

        with patch.object(generator, "_append_accepted", side_effect=append_spy), \
             patch.object(g, "emit_structured_stderr", side_effect=emit_spy):
            generator._accept_one_slot("heldout", "H1", (4,), NoDraw())

        self.assertEqual(order[0], ("accepted", 1))
        self.assertEqual(order[1], ("emitted", 1))
        self.assertEqual(len(emitted), 1)
        tag, event = emitted[0]
        self.assertEqual(tag, "PREDICATE_LOG")
        self.assertEqual(set(event), {
            "input_id", "stratum", "amount", "coins", "oracle_answer", "N0", "repeated_use_predicate"
        })
        self.assertEqual((event["input_id"], event["amount"], event["coins"]), ("H004", 12, [2, 3]))
        self.assertEqual((event["oracle_answer"], event["N0"], event["repeated_use_predicate"]), (3, 0, True))

    def test_fatal_heldout_fixed_key_collision_streams_c9_reason_before_abort(self):
        from unittest.mock import patch
        generator = g.ProductionGenerator()
        candidate = g.Candidate(
            (g.RawRecord(1, (2, 3), "H1", {"edge": True, "repeated_use_witness": False}),),
            "H001", "H1",
        )
        emitted = []
        with patch.object(g, "draw_raw_candidate", return_value=candidate), \
             patch.object(g, "classify_collision", return_value=("CROSS_BANK_COLLISION", True)), \
             patch.object(g, "emit_structured_stderr", side_effect=lambda tag, payload: emitted.append((tag, payload))):
            with self.assertRaisesRegex(g.GeneratorDefect, "CROSS_BANK_COLLISION"):
                generator._accept_one_slot("heldout", "H1", (1,), TraceRandom())
        self.assertEqual(len(emitted), 1)
        self.assertEqual(emitted[0][0], "REJECTION_EVENT")
        self.assertEqual(emitted[0][1]["reason"], "CROSS_BANK_COLLISION")
        self.assertEqual(generator.events_h, [emitted[0][1]])
        self.assertEqual(generator.repeated_use_log, [])

    def test_rejected_h2_candidate_emits_rejection_but_never_predicate(self):
        from unittest.mock import patch
        generator = g.ProductionGenerator()
        rejected = g.Candidate(
            (g.RawRecord(13, (7, 8), "H2", {
                "forced_coin_1": False, "match_amount": False, "repeated_use_witness": False
            }),),
            "H013", "H2",
        )
        emitted = []
        with patch.object(g, "draw_raw_candidate", return_value=rejected), \
             patch.object(g, "MAX_WHOLE_CANDIDATE_ATTEMPTS", 1), \
             patch.object(g, "emit_structured_stderr", side_effect=lambda tag, payload: emitted.append((tag, payload))):
            with self.assertRaises(g.GeneratorDefect):
                generator._accept_one_slot("heldout", "H2", (1,), TraceRandom())
        self.assertEqual([tag for tag, _ in emitted], ["REJECTION_EVENT"])
        self.assertEqual(generator.repeated_use_log, [])

    def test_rejection_stream_event_uses_exact_sidecar_fields_and_prefix(self):
        from unittest.mock import patch
        generator = g.ProductionGenerator()
        event = g.make_sidecar_row(1, "diagnostic", "D001", "INT32_OVERFLOW", "D1")
        seen = []
        with patch.object(g, "emit_structured_stderr", side_effect=lambda tag, payload: seen.append((tag, payload))):
            generator._stream_rejection("diagnostic", event)
        self.assertEqual(generator.events_d, [event])
        self.assertEqual(seen, [("REJECTION_EVENT", event)])
        self.assertEqual(set(event), {"attempt", "bank", "candidate_id", "reason", "stratum"})

    def test_generator_source_has_no_environment_or_command_line_configuration_reads(self):
        import inspect
        source = inspect.getsource(g)
        self.assertNotIn("os.environ", source)
        self.assertNotIn("sys.argv", source)
        self.assertNotIn("argparse", source)

    def test_reorder_pair_rejects_identity_permutation(self):
        rec1 = g.RawRecord(20, (1, 4, 7), "D6", {"pair_id": "D6-P01", "ordering": "original"})
        rec2 = g.RawRecord(20, (1, 4, 7), "D6", {"pair_id": "D6-P01", "ordering": "permutation"})
        _, reason = g.evaluate_candidate(g.Candidate((rec1, rec2), "D6-P01", "D6"))
        self.assertEqual(reason, "IDENTITY_PERMUTATION")

    @staticmethod
    def _schema_test_bank(prefix: str) -> list[dict]:
        quotas = g.QUOTAS
        rows = []
        ordinal = 1
        for stratum_number in range(1, 9):
            stratum = f"{prefix}{stratum_number}"
            for slot in range(1, quotas[stratum]):
                pass
            if stratum == f"{prefix}6":
                if prefix == "D":
                    for pair_no in range(1, 5):
                        amount = 100 + pair_no
                        original = [1, pair_no + 1, pair_no + 5]
                        permutation = [original[1], original[2], original[0]]
                        pair_id = f"D6-P{pair_no:02d}"
                        for ordering, coins in (("original", original), ("permutation", permutation)):
                            rows.append({
                                "input_id": f"D{ordinal:03d}", "amount": amount, "coins": coins,
                                "canonical_id": g.canonical_id(amount, coins), "stratum": stratum,
                                "rule_id": stratum,
                                "rule_params": {"pair_id": pair_id, "ordering": ordering},
                                "int32_guard": {"status": "accepted", "redraws": 0},
                                "oracle_output_file_sha256": "a" * 64,
                            })
                            ordinal += 1
                else:
                    for singleton in range(6):
                        amount = 200 + singleton
                        coins = [2, 11 + singleton]
                        rows.append({
                            "input_id": f"H{ordinal:03d}", "amount": amount, "coins": coins,
                            "canonical_id": g.canonical_id(amount, coins), "stratum": stratum,
                            "rule_id": stratum, "rule_params": {"singleton": True},
                            "int32_guard": {"status": "accepted", "redraws": 0},
                            "oracle_output_file_sha256": "a" * 64,
                        })
                        ordinal += 1
                    for pair_no in range(1, 3):
                        amount = 300 + pair_no
                        original = [3, pair_no + 11, pair_no + 15]
                        permutation = [original[1], original[2], original[0]]
                        pair_id = f"H6-P{pair_no:02d}"
                        for ordering, coins in (("original", original), ("permutation", permutation)):
                            rows.append({
                                "input_id": f"H{ordinal:03d}", "amount": amount, "coins": coins,
                                "canonical_id": g.canonical_id(amount, coins), "stratum": stratum,
                                "rule_id": stratum,
                                "rule_params": {"pair_id": pair_id, "ordering": ordering},
                                "int32_guard": {"status": "accepted", "redraws": 0},
                                "oracle_output_file_sha256": "a" * 64,
                            })
                            ordinal += 1
                continue
            for slot in range(quotas[stratum]):
                amount = ordinal + 10_000
                coins = [1, ordinal + 1]
                rows.append({
                    "input_id": f"{prefix}{ordinal:03d}", "amount": amount, "coins": coins,
                    "canonical_id": g.canonical_id(amount, coins), "stratum": stratum,
                    "rule_id": stratum,
                    "rule_params": {"singleton": True} if stratum == "H6" else {},
                    "int32_guard": {"status": "accepted", "redraws": 0},
                    "oracle_output_file_sha256": "a" * 64,
                })
                ordinal += 1
        return rows

    def test_serialized_pair_schema_is_rule_params_only_for_d6_and_h6(self):
        diagnostic = self._schema_test_bank("D")
        heldout = self._schema_test_bank("H")
        g.validate_serialized_records(diagnostic, "D")
        g.validate_serialized_records(heldout, "H")
        for record in diagnostic + heldout:
            self.assertNotIn("pair_id", record)
            self.assertNotIn("ordering", record)

    def test_pair_validator_checks_each_written_record_hash(self):
        records = self._schema_test_bank("D")
        g.attach_record_hashes(records)
        g.validate_serialized_records(records, "D")
        records[40]["record_sha256"] = "0" * 64
        with self.assertRaisesRegex(g.GeneratorDefect, "record_sha256 mismatch"):
            g.validate_serialized_records(records, "D")

    def test_pair_validator_rejects_top_level_pair_fields(self):
        records = self._schema_test_bank("D")
        records[40]["pair_id"] = "D6-P01"
        with self.assertRaises(g.GeneratorDefect):
            g.validate_serialized_records(records, "D")

    def test_pair_validator_rejects_mismatched_rule_params_and_order(self):
        for mutation in ("pair_id", "ordering", "canonical_id", "guard", "amount", "coin_set", "identity"):
            records = self._schema_test_bank("D")
            if mutation == "pair_id":
                records[41]["rule_params"]["pair_id"] = "D6-P02"
            elif mutation == "ordering":
                records[41]["rule_params"]["ordering"] = "original"
            elif mutation == "canonical_id":
                records[41]["canonical_id"] = "C-" + "0" * 64
            elif mutation == "guard":
                records[41]["int32_guard"] = {"status": "redrawn", "redraws": 1}
            elif mutation == "amount":
                records[41]["amount"] += 1
                records[41]["canonical_id"] = g.canonical_id(records[41]["amount"], records[41]["coins"])
            elif mutation == "coin_set":
                records[41]["coins"] = [1, 7, 9]
                records[41]["canonical_id"] = g.canonical_id(records[41]["amount"], records[41]["coins"])
            elif mutation == "identity":
                records[41]["coins"] = list(records[40]["coins"])
                records[41]["canonical_id"] = records[40]["canonical_id"]
            with self.subTest(mutation=mutation), self.assertRaises(g.GeneratorDefect):
                g.validate_serialized_records(records, "D")

    def test_pair_validator_rejects_pair_id_order_drift(self):
        records = self._schema_test_bank("D")
        for row in records[40:42]:
            row["rule_params"]["pair_id"] = "D6-P02"
        for row in records[42:44]:
            row["rule_params"]["pair_id"] = "D6-P01"
        with self.assertRaisesRegex(g.GeneratorDefect, "pair IDs/order mismatch"):
            g.validate_serialized_records(records, "D")

    def test_pair_validator_rejects_nonadjacent_pair_rows(self):
        records = self._schema_test_bank("H")
        records[56], records[57] = records[57], records[56]
        with self.assertRaises(g.GeneratorDefect):
            g.validate_serialized_records(records, "H")

    def test_all_closed_sidecar_reason_codes_are_accepted_and_no_other_code_is(self):
        self.assertEqual(len(g.REJECTION_REASONS), 12)
        for reason in sorted(g.REJECTION_REASONS):
            row = g.make_sidecar_row(1, "diagnostic", "D001", reason, "D1")
            self.assertEqual(row["reason"], reason)
            self.assertEqual(set(row), {"attempt", "bank", "candidate_id", "reason", "stratum"})
        with self.assertRaises(g.GeneratorDefect):
            g.make_sidecar_row(1, "diagnostic", "D001", "UNDECLARED_REASON", "D1")

    def test_h2_h4_h8_threshold_and_answer_rejections_map_exactly(self):
        cases = [
            (g.RawRecord(2, (1, 2), "H2", {"match_amount": True}), "H2_MATCH_AMOUNT_BELOW_13"),
            (g.RawRecord(13, (7, 8), "H2", {"match_amount": False}), "H2_ORACLE_BELOW_TWO"),
            (g.RawRecord(3, (2, 3), "H4", {"match_amount": True}), "H4_MATCH_AMOUNT_BELOW_20"),
            (g.RawRecord(6, (100, 101), "H8", {"anchor": "1-2-3", "anchor_fixed": True}), "H8_ORACLE_BELOW_TWO"),
        ]
        for raw, expected in cases:
            _, reason = g.evaluate_candidate(g.Candidate((raw,), "fixture", raw.stratum))
            self.assertEqual(reason, expected)

    def test_int32_overflow_is_one_closed_reason(self):
        candidate = g.Candidate(
            (g.RawRecord(5000, tuple(range(1, 31)), "D8", {}),), "D008", "D8"
        )
        answer, reason = g.evaluate_candidate(candidate)
        self.assertGreater(answer, g.MAX_INT32)
        self.assertEqual(reason, "INT32_OVERFLOW")
        row = g.make_sidecar_row(1, "diagnostic", "D008", reason, "D8")
        self.assertEqual(set(row), {"attempt", "bank", "candidate_id", "reason", "stratum"})
        self.assertEqual(reason, "INT32_OVERFLOW")

    def test_gcd_divides_amount_is_rejected_even_if_answer_positive(self):
        candidate = g.Candidate(
            (g.RawRecord(4, (2, 4), "D3", {"mechanism": "gcd", "g": 2}),), "D005", "D3"
        )
        answer, reason = g.evaluate_candidate(candidate)
        self.assertGreater(answer, 0)
        self.assertEqual(reason, "GCD_DIVIDES_AMOUNT")

    def test_d4_gcd_t_set_rejection(self):
        candidate = g.Candidate(
            (g.RawRecord(7, (4, 8), "D4", {"mechanism": "gcd2"}),), "D005", "D4"
        )
        _, reason = g.evaluate_candidate(candidate)
        self.assertEqual(reason, "D4_GCD_NOT_ONE")

    def test_d5_greedy_minimum_rejection(self):
        candidate = g.Candidate(
            (g.RawRecord(6, (1, 2, 5), "D5", {"coin_1_fixed": True}),), "D007", "D5"
        )
        _, reason = g.evaluate_candidate(candidate)
        self.assertEqual(reason, "D5_GREEDY_EQUALS_MINIMUM")

    def test_h1_zero_amount_is_assertion_not_rejection(self):
        candidate = g.Candidate(
            (g.RawRecord(0, (1, 2), "H1", {"edge": True, "repeated_use_witness": False}),), "H001", "H1"
        )
        answer, reason = g.evaluate_candidate(candidate)
        self.assertEqual(answer, 1)
        self.assertIsNone(reason)

    def test_collision_paths_and_fatal_heldout_fixed_key_hit(self):
        fixed_d, fixed_h = g.fixed_key_preflight()
        d_key = next(iter(fixed_d))
        h_key = next(iter(fixed_h))
        reason, fatal = g.classify_collision("heldout", d_key, set(fixed_h), set(fixed_h), fixed_d)
        self.assertEqual((reason, fatal), ("CROSS_BANK_COLLISION", True))
        reason, fatal = g.classify_collision("diagnostic", h_key, set(fixed_d), set(fixed_h), fixed_d)
        self.assertEqual((reason, fatal), ("CROSS_BANK_COLLISION", False))
        reason, fatal = g.classify_collision("diagnostic", d_key, set(fixed_d), set(fixed_h), fixed_d)
        self.assertEqual((reason, fatal), ("WITHIN_BANK_CANONICAL_COLLISION", False))
        fresh = (999, (1, 2, 3))
        reason, fatal = g.classify_collision("diagnostic", fresh, set(fixed_d), set(fixed_h), fixed_d)
        self.assertEqual((reason, fatal), (None, False))

    def test_coin_slot_cap_is_1000_per_candidate_attempt(self):
        rng = ConstantRandom(5)
        with self.assertRaises(g.CoinSlotBudgetExhausted):
            g.draw_unique(rng, 1, 1, 10, already=(5,), label="fixture")
        self.assertEqual(rng.calls, 1000)
        # A new candidate attempt gets a fresh per-slot budget.
        result = g.draw_unique(rng, 1, 1, 10, label="fixture")
        self.assertEqual(result, [5])
        self.assertEqual(rng.calls, 1001)
        self.assertEqual(g.MAX_WHOLE_CANDIDATE_ATTEMPTS, 1000)

    def test_whole_record_candidate_cap_is_cumulative_for_the_slot(self):
        generator = g.ProductionGenerator()
        overflowing = g.Candidate(
            (g.RawRecord(5000, tuple(range(1, 31)), "D8", {}),), "", "D8"
        )
        from unittest.mock import patch
        from contextlib import redirect_stderr
        import io
        captured = io.StringIO()
        with patch.object(g, "draw_raw_candidate", return_value=overflowing), redirect_stderr(captured):
            with self.assertRaises(g.GeneratorDefect):
                generator._accept_one_slot("diagnostic", "D8", (1,), TraceRandom())
        self.assertEqual(len(captured.getvalue().splitlines()), 1000)
        self.assertTrue(all(line.startswith("REJECTION_EVENT ") for line in captured.getvalue().splitlines()))
        self.assertEqual(len(generator.events_d), 1000)
        self.assertEqual([row["attempt"] for row in generator.events_d], list(range(1, 1001)))
        self.assertTrue(all(row["reason"] == "INT32_OVERFLOW" for row in generator.events_d))

    def test_whole_pair_candidate_cap_is_cumulative_for_the_pair_slot(self):
        generator = g.ProductionGenerator()
        original = g.RawRecord(5000, tuple(range(1, 31)), "D6", {"pair_id": "D6-P01", "ordering": "original"})
        permutation = g.RawRecord(5000, tuple(reversed(range(1, 31))), "D6", {"pair_id": "D6-P01", "ordering": "permutation"})
        overflowing_pair = g.Candidate((original, permutation), "D6-P01", "D6")
        from unittest.mock import patch
        from contextlib import redirect_stderr
        import io
        captured = io.StringIO()
        with patch.object(g, "draw_raw_candidate", return_value=overflowing_pair), redirect_stderr(captured):
            with self.assertRaises(g.GeneratorDefect):
                generator._accept_one_slot("diagnostic", "D6", (1, 2), TraceRandom())
        self.assertEqual(len(captured.getvalue().splitlines()), 1000)
        self.assertTrue(all(line.startswith("REJECTION_EVENT ") for line in captured.getvalue().splitlines()))
        self.assertEqual(len(generator.events_d), 1000)
        self.assertEqual([row["attempt"] for row in generator.events_d], list(range(1, 1001)))
        self.assertTrue(all(row["candidate_id"] == "D6-P01" for row in generator.events_d))
        self.assertTrue(all(row["reason"] == "INT32_OVERFLOW" for row in generator.events_d))

    def test_pair_pairlevel_guard_and_hash_payload_follow_closed_text(self):
        pair = g.draw_raw_candidate("D6", 1, TraceRandom())
        guard = {"status": "redrawn", "redraws": 3}
        a = g._record_to_dict(pair.records[0], "D025", guard, "a" * 64)
        b = g._record_to_dict(pair.records[1], "D026", guard, "a" * 64)
        self.assertEqual(a["int32_guard"], b["int32_guard"])
        self.assertEqual(a["canonical_id"], b["canonical_id"])
        self.assertNotEqual(a["coins"], b["coins"])
        payload = g.record_hash_payload(a)
        self.assertNotIn("pair_id", a)
        self.assertNotIn("ordering", a)
        self.assertEqual(a["rule_params"]["pair_id"], b["rule_params"]["pair_id"])
        self.assertEqual(set(payload), {
            "input_id", "amount", "coins", "canonical_id", "stratum", "rule_id",
            "rule_params", "int32_guard", "oracle_output_file_sha256",
        })
        self.assertNotIn("pair_id", payload)
        self.assertNotIn("ordering", payload)

    def test_oracle_outputs_deduplicate_pair_identity(self):
        pair = g.draw_raw_candidate("D6", 1, TraceRandom())
        guard = {"status": "accepted", "redraws": 0}
        rows = [g._record_to_dict(pair.records[i], f"D{25+i:03d}", guard, "b" * 64) for i in (0, 1)]
        output = g.oracle_output_rows(rows)
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["canonical_id"], rows[0]["canonical_id"])

    def test_cached_oracle_answer_is_reused_without_recomputation(self):
        pair = g.draw_raw_candidate("D6", 1, TraceRandom())
        guard = {"status": "accepted", "redraws": 0}
        rows = [g._record_to_dict(pair.records[i], f"D{25+i:03d}", guard, "b" * 64) for i in (0, 1)]
        cid = rows[0]["canonical_id"]
        from unittest.mock import patch
        key = g.canonical_key(rows[0]["amount"], rows[0]["coins"])
        with patch.object(g, "combinations_count", side_effect=AssertionError("oracle recomputed")):
            output = g.oracle_output_rows(rows, {key: 7})
        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["oracle_answer"], 7)

    def test_production_entry_point_fails_closed_without_execution_protocol(self):
        from unittest.mock import patch
        with patch.object(g, "OUTPUT_DIR", None), patch.object(g, "BANK_GENERATION_AUTHORIZED", False):
            with self.assertRaises(SystemExit) as caught:
                g.main()
        self.assertIn("execution protocol has not pinned", str(caught.exception))


class PublicationGateTests(unittest.TestCase):
    def record(self, input_id: str, amount: int, coins: list[int], stratum: str) -> dict:
        return {
            "input_id": input_id,
            "amount": amount,
            "coins": coins,
            "canonical_id": g.canonical_id(amount, coins),
            "stratum": stratum,
        }

    def fixture_call(self, out: Path, collision: bool, fixture_prefix: str = "fixture_"):
        d = self.record("D001", 2, [1], "D1")
        h = self.record("H001", 2, [1] if collision else [2], "H1")
        evd = [g.make_sidecar_row(1, "diagnostic", "D002", "CROSS_BANK_COLLISION", "D1")]
        evh: list[dict] = []
        return g.atomic_publish_fixture_or_bank_package(
            out,
            g.compact_json_bytes([{"fixture": "diagnostic"}]),
            g.compact_json_bytes([{"fixture": "heldout"}]),
            g.compact_json_bytes([{"fixture": "diagnostic-oracle"}]),
            g.compact_json_bytes([{"fixture": "heldout-oracle"}]),
            g.sidecar_bytes(evd),
            g.sidecar_bytes(evh),
            [d], [h], evd, evh,
            fixture_prefix=fixture_prefix,
        )

    def test_item8_collision_failure_writes_no_bank_or_oracle_artifacts(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "fixture-output"
            report = self.fixture_call(out, collision=True)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual({x["filename"] for x in report["artifacts"]}, {
                "fixture_diagnostic_bank.rejections.jsonl", "fixture_heldout_bank.rejections.jsonl"
            })
            files = {p.name for p in out.iterdir()}
            self.assertEqual(files, {
                "fixture_diagnostic_bank.rejections.jsonl",
                "fixture_heldout_bank.rejections.jsonl",
                "canonical_disjointness_report.json",
            })
            self.assertFalse((out / "fixture_diagnostic_bank.json").exists())
            self.assertFalse((out / "fixture_heldout_bank.json").exists())
            self.assertFalse((out / "fixture_diagnostic_oracle_outputs.json").exists())
            self.assertFalse((out / "fixture_heldout_oracle_outputs.json").exists())

    def test_item8_pass_fixture_is_atomic_and_all_digests_verify(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "fixture-output"
            report = self.fixture_call(out, collision=False)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(len(report["artifacts"]), 6)
            for item in report["artifacts"]:
                data = (out / item["filename"]).read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), item["sha256"])

    def test_same_synthetic_fixture_reproduces_identical_output_digests(self):
        reports = []
        dirs = []
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for i in (1, 2):
                out = root / f"run{i}"
                report = self.fixture_call(out, collision=False)
                reports.append(report)
                dirs.append(out)
            self.assertEqual(reports[0], reports[1])
            names = sorted(p.name for p in dirs[0].iterdir())
            self.assertEqual(names, sorted(p.name for p in dirs[1].iterdir()))
            for name in names:
                self.assertEqual((dirs[0] / name).read_bytes(), (dirs[1] / name).read_bytes())

    def test_logged_heldout_fixed_key_collision_blocks_item8_publication(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "fixture-output"
            evh = [g.make_sidecar_row(1, "heldout", "H008", "CROSS_BANK_COLLISION", "H1")]
            with self.assertRaises(g.GeneratorDefect):
                g.atomic_publish_fixture_or_bank_package(
                    out, b"[]\n", b"[]\n", b"[]\n", b"[]\n", b"", g.sidecar_bytes(evh),
                    [], [], [], evh, fixture_prefix="fixture_",
                )
            self.assertFalse(out.exists())
            self.assertFalse(Path(str(out) + ".staging").exists())

    def test_preflight_refuses_existing_final_or_staging_directory(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "fixture-output"
            out.mkdir()
            with self.assertRaises(g.GeneratorDefect):
                self.fixture_call(out, collision=False)
            out.rmdir()
            staging = Path(str(out) + ".staging")
            staging.mkdir()
            with self.assertRaises(g.GeneratorDefect):
                self.fixture_call(out, collision=False)


    def test_preflight_refuses_dangling_symlink_paths(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "fixture-output"
            target = Path(td) / "missing-target"
            try:
                out.symlink_to(target, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is unavailable in this environment")
            with self.assertRaises(g.GeneratorDefect):
                g.preflight_output_directory(out)



if __name__ == "__main__":
    unittest.main(verbosity=2)
