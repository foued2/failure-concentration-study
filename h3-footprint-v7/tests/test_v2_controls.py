from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import instrument
import run_gate


REFERENCE = """import heapq

def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        if u == t:
            break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1 if dist[t] == inf else int(dist[t])
"""

SPREAD_BUG = REFERENCE.replace(
    "return -1 if dist[t] == inf else int(dist[t])",
    """return (int(dist[t]) + 1) if (
        (n == 10 and len(edges) == 9 and s == 0 and t == 9) or
        (n == 20 and len(edges) == 19 and s == 0 and t == 19) or
        (n == 3 and edges == [(0, 1, 0), (1, 2, 1)] and s == 0 and t == 2) or
        (n == 4 and edges == [(0, 1, 1), (1, 2, 0), (2, 1, 0), (1, 3, 1)] and s == 0 and t == 3) or
        (n == 4 and edges == [(0, 1, 0), (0, 2, 3), (1, 3, 2), (2, 3, 0)] and s == 0 and t == 3)
    ) else (-1 if dist[t] == inf else int(dist[t]))"""
)


class OracleIntegrityTests(unittest.TestCase):
    def test_three_oracles_match_frozen_expected_values(self):
        expected = json.loads((HERE / "expected_values.json").read_text(encoding="utf-8"))
        values = instrument.oracle_values()
        self.assertEqual(len(instrument.PROBES), 30)
        self.assertEqual(len({p["probe_id"] for p in instrument.PROBES}), 30)
        self.assertEqual(len(expected), 30)
        for probe_id, oracle_row in values.items():
            self.assertEqual(len(set(oracle_row.values())), 1, (probe_id, oracle_row))
            raw = next(iter(oracle_row.values()))
            normalized = -1 if raw is None else raw
            self.assertEqual(expected[probe_id], normalized, probe_id)
        counts = {
            family: sum(p["family"] == family for p in instrument.PROBES)
            for family in instrument.FAMILY_ORDER
        }
        self.assertEqual(counts, {family: 5 for family in instrument.FAMILY_ORDER})
        review = json.loads((HERE / "coherence_review.json").read_text(encoding="utf-8"))
        self.assertEqual(len(review), 30)
        self.assertTrue(all(item["belongs"] is True for item in review))


class GroupCountingTests(unittest.TestCase):
    def test_body_variants_do_not_inflate_distinct_group_count(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            bodies = root / "generated" / "bodies"
            bodies.mkdir(parents=True)
            profiles = {}
            for i in range(4):
                name = "a" + str(i)
                profiles[name] = {
                    "body_hash": name, "base_algorithm": "heap_dijkstra", "excluded": None,
                    "k": 5, "C": 1.0, "max_f": 5,
                    "family_counts": {"R": 5, "Z": 0, "A": 0, "I": 0, "S": 0, "U": 0},
                    "eligible": True, "group_id": "g" + str(i), "generator": "fixture",
                }
            for i, gid in enumerate(("g4", "g5", "g6", "g7", "g4")):
                name = "b" + str(i)
                profiles[name] = {
                    "body_hash": name, "base_algorithm": "heap_dijkstra", "excluded": None,
                    "k": 5, "C": 0.6, "max_f": 3,
                    "family_counts": {"R": 2, "Z": 3, "A": 0, "I": 0, "S": 0, "U": 0},
                    "eligible": True, "group_id": gid, "generator": "fixture",
                }
            for name in profiles:
                (bodies / (name + ".py")).write_text("fixture", encoding="utf-8")
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
                    run_gate, "evaluate_body", side_effect=lambda path, meta, *args, **kwargs: profiles[path.stem]
                ):
                    report = run_gate.build()
            finally:
                for key, value in old.items():
                    setattr(run_gate, key, value)
            self.assertEqual(report["candidate_bodies"], 9)
            self.assertEqual(report["supported_cell_count"], 1)
            cell = report["supported_cells"][0]
            self.assertEqual(cell["candidate_bodies"], 9)
            self.assertEqual(sorted(level["groups"] for level in cell["levels"]), [4, 4])
            self.assertEqual(report["unique_groups_in_supported_cells"], 8)
            self.assertEqual(report["cross_group_pairs_different_C"], 16)


class SpreadControlTests(unittest.TestCase):
    def test_five_known_failures_spanning_two_families_have_expected_k_and_c(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "generated" / "bodies").mkdir(parents=True)
            for name in ("instrument.py", "probe_worker.py", "expected_values.json"):
                shutil.copy2(HERE / name, root / name)
            body_dir = root / "generated" / "bodies"
            candidate = body_dir / "spread.py"
            candidate.write_text(SPREAD_BUG, encoding="utf-8")
            digest = candidate.stem
            rec = {
                "batch_id": 50,
                "model": "control-fixture",
                "prompt_variant": "test",
                "candidate_records": [{"body_hash": digest, "stored_new": True}],
            }
            (root / "generated" / "attempts.jsonl").write_text(json.dumps(rec) + chr(10), encoding="utf-8")
            old = {
                "ROOT": run_gate.ROOT, "GEN": run_gate.GEN,
                "BODIES": run_gate.BODIES, "WORKER": run_gate.WORKER,
            }
            try:
                run_gate.ROOT = root
                run_gate.GEN = root / "generated"
                run_gate.BODIES = body_dir
                run_gate.WORKER = root / "probe_worker.py"
                row = run_gate.evaluate_body(candidate, run_gate.body_meta())
            finally:
                for key, value in old.items():
                    setattr(run_gate, key, value)
            self.assertIsNone(row["excluded"])
            self.assertEqual(row["k"], 5)
            self.assertEqual(row["family_counts"]["R"], 2)
            self.assertEqual(row["family_counts"]["Z"], 3)
            self.assertAlmostEqual(row["C"], 0.6)


if __name__ == "__main__":
    unittest.main()
