from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import run_gate


def make_row(name, label, k, max_f, group_id, batch_id):
    counts = {family: 0 for family in ("R", "Z", "A", "I", "S", "U")}
    counts["R"] = max_f
    counts["Z"] = k - max_f
    return {
        "body_hash": name, "base_algorithm": label, "excluded": None,
        "k": k, "C": max_f / k, "max_f": max_f, "family_counts": counts,
        "eligible": 2 <= k <= 24, "group_id": group_id, "batch_id": batch_id,
        "generator": "fixture", "prompt_variant": "test",
    }


def build_with(rows):
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
                return run_gate.build()
        finally:
            for key, value in old.items():
                setattr(run_gate, key, value)


def other_threshold_rows():
    """42 other-labelled bodies that meet the numerical cell thresholds."""
    specs = [(4, 2), (4, 3), (5, 3), (5, 4), (6, 3), (6, 4)]
    rows = []
    index = 0
    for k, max_f in specs:
        for group_index in range(7):
            name = f"r{index:02d}"
            rows.append(make_row(
                name, "other", k, max_f,
                f"g-{k}-{max_f}-{group_index}", index,
            ))
            index += 1
    return rows


class OtherCategoryTests(unittest.TestCase):
    def test_other_cannot_create_a_supported_cell_even_when_thresholds_are_met(self):
        rows = other_threshold_rows()
        self.assertEqual(len(rows), 42)
        report = build_with(rows)
        self.assertEqual(report["other_eligible_bodies"], 42)
        self.assertEqual(report["other_eligible_groups"], 42)
        self.assertEqual(report["support_eligible_bodies"], 0)
        self.assertEqual(report["support_eligible_groups"], 0)
        self.assertEqual(report["supported_cell_count"], 0)
        self.assertEqual(report["unique_groups_in_supported_cells"], 0)
        self.assertEqual(report["cell_table"], [])
        self.assertEqual(report["saturation_rate_eligible"], 0.0)
        self.assertEqual(report["verdict"], "FAIL")
        self.assertEqual(report["reason"], "insufficient_support")

    def test_identified_algorithms_still_form_cells(self):
        rows = []
        index = 0
        for max_f in (2, 3):
            for group_index in range(4):
                rows.append(make_row(
                    f"i{index:02d}", "heap_dijkstra", 4, max_f,
                    f"g-heap-{max_f}-{group_index}", index,
                ))
                index += 1
        for max_f in (2, 3):
            for group_index in range(7):
                rows.append(make_row(
                    f"o{index:02d}", "other", 4, max_f,
                    f"g-other-{max_f}-{group_index}", index,
                ))
                index += 1
        report = build_with(rows)
        self.assertEqual(report["supported_cell_count"], 1)
        self.assertEqual(report["supported_cells"][0]["base_algorithm"], "heap_dijkstra")
        self.assertEqual(report["support_eligible_groups"], 8)
        self.assertEqual(report["other_eligible_bodies"], 14)
        self.assertTrue(all(cell["base_algorithm"] != "other" for cell in report["cell_table"]))
        self.assertEqual(report["verdict"], "WEAK")


if __name__ == "__main__":
    unittest.main()
