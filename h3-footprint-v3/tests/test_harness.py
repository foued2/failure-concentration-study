from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import generate
import instrument
import run_gate


REFERENCE = '''import heapq

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
'''

BUG_SENTINEL = REFERENCE.replace(
    'return -1 if dist[t] == inf else int(dist[t])',
    'return 0 if dist[t] == inf else int(dist[t])'
)
CONST_ZERO = 'def solve(n, edges, s, t):\n    return 0\n'
CONST_MINUS_ONE = 'def solve(n, edges, s, t):\n    return -1\n'
PLUS_ONE = REFERENCE.replace(
    'return -1 if dist[t] == inf else int(dist[t])',
    'return -1 if dist[t] == inf else int(dist[t]) + 1'
)
ONE_PROBE_R1_BUG = REFERENCE.replace(
    'return -1 if dist[t] == inf else int(dist[t])',
    'return (int(dist[t]) + 1) if n == 10 and len(edges) == 9 and s == 0 and t == 9 else (-1 if dist[t] == inf else int(dist[t]))'
)
ONE_PROBE_Z4_BUG = REFERENCE.replace(
    'return -1 if dist[t] == inf else int(dist[t])',
    'return 1 if n == 4 and s == 0 and t == 3 and edges == [(0, 1, 0), (1, 2, 0), (2, 3, 0)] else (-1 if dist[t] == inf else int(dist[t]))'
)
RUNTIME_CRASH = 'def solve(n, edges, s, t):\n    raise RuntimeError("planted runtime failure")\n'
MISSING_IMPORT = 'import definitely_missing_h3_v2_dependency\ndef solve(n, edges, s, t):\n    return 0\n'
UNDEFINED_GLOBAL = 'def solve(n, edges, s, t):\n    return missing_h3_v2_name\n'
NO_SOLVE = 'import heapq\ndef helper():\n    return 0\n'
SYNTAX_ERROR = 'def solve(:\n    return 0\n'


class ExtractTests(unittest.TestCase):
    def test_top_level_import_is_preserved(self):
        fence = chr(96) * 3
        text = fence + 'python\nimport heapq\ndef solve(n, edges, s, t):\n    return 0\n' + fence
        got = generate.extract(text)
        self.assertEqual(len(got), 1)
        self.assertIn('import heapq', got[0])
        self.assertEqual(got[0].splitlines()[0], 'import heapq')

    def test_function_local_import_is_preserved(self):
        fence = chr(96) * 3
        text = fence + 'python\ndef solve(n, edges, s, t):\n    import heapq\n    return 0\n' + fence
        got = generate.extract(text)
        self.assertEqual(len(got), 1)
        self.assertIn('import heapq', got[0])

    def test_multiple_fences_yield_multiple_complete_modules(self):
        fence = chr(96) * 3
        text = (
            fence + 'python\nimport heapq\ndef solve(n, edges, s, t):\n    return 0\n' + fence
            + '\n' +
            fence + 'python\nfrom collections import deque\ndef solve(n, edges, s, t):\n    return 0\n' + fence
        )
        got = generate.extract(text)
        self.assertEqual(len(got), 2)
        self.assertIn('import heapq', got[0])
        self.assertIn('from collections import deque', got[1])

    def test_ambiguous_multi_solve_block_is_rejected(self):
        fence = chr(96) * 3
        text = fence + 'python\ndef solve(n, edges, s, t):\n    return 0\ndef solve(n, edges, s, t):\n    return -1\n' + fence
        self.assertEqual(generate.extract(text), [])

    def test_malformed_block_is_rejected(self):
        fence = chr(96) * 3
        text = fence + 'python\ndef solve(:\n    return 0\n' + fence
        self.assertEqual(generate.extract(text), [])


class StaticCheckTests(unittest.TestCase):
    def test_undefined_global_is_detected_but_import_and_helpers_are_not(self):
        self.assertEqual(run_gate.undefined_global_names(REFERENCE), [])
        self.assertEqual(run_gate.undefined_global_names(UNDEFINED_GLOBAL), ['missing_h3_v2_name'])
        self.assertEqual(run_gate.undefined_global_names(MISSING_IMPORT), [])

    def test_preflight_rejects_missing_solve_and_import_error(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for name in ('instrument.py', 'probe_worker.py', 'expected_values.json'):
                shutil.copy2(HERE / name, root / name)
            for label, source in (('missing_solve', NO_SOLVE), ('missing_import', MISSING_IMPORT), ('syntax', SYNTAX_ERROR)):
                target = root / (label + '.py')
                target.write_text(source, encoding='utf-8')
                import subprocess
                proc = subprocess.run(
                    [sys.executable, '-I', str(root / 'probe_worker.py'), str(target), '--preflight'],
                    capture_output=True, text=True, timeout=5
                )
                payload = json.loads(proc.stdout.strip().splitlines()[-1])
                self.assertFalse(payload.get('valid', False), label)
                self.assertEqual(payload.get('phase'), 'load', label)


class EndToEndControlTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.gen = self.root / 'generated'
        self.bodies = self.gen / 'bodies'
        self.bodies.mkdir(parents=True)
        self.gen.mkdir(exist_ok=True)
        for name in ('instrument.py', 'probe_worker.py', 'expected_values.json'):
            shutil.copy2(HERE / name, self.root / name)
        self.old = {
            'ROOT': run_gate.ROOT, 'GEN': run_gate.GEN,
            'BODIES': run_gate.BODIES, 'WORKER': run_gate.WORKER,
        }
        run_gate.ROOT = self.root
        run_gate.GEN = self.gen
        run_gate.BODIES = self.bodies
        run_gate.WORKER = self.root / 'probe_worker.py'

    def tearDown(self):
        for key, value in self.old.items():
            setattr(run_gate, key, value)
        self.tmp.cleanup()

    def write_candidate(self, name, source, batch):
        normalized = generate.normalize(source)
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        (self.bodies / (digest + '.py')).write_text(normalized, encoding='utf-8')
        rec = {
            'batch_id': batch,
            'model': 'control-fixture',
            'prompt_variant': 'test',
            'candidate_records': [{'candidate_index': 0, 'body_hash': digest, 'stored_new': True}],
            'body_hashes': [digest],
        }
        attempts = self.gen / 'attempts.jsonl'
        with attempts.open('a', encoding='utf-8') as fh:
            fh.write(json.dumps(rec) + '\n')
        meta = run_gate.body_meta()
        return run_gate.evaluate_body(self.bodies / (digest + '.py'), meta)

    def test_reference_has_k_zero(self):
        row = self.write_candidate('reference', REFERENCE, 1)
        self.assertIsNone(row['excluded'])
        self.assertEqual(row['k'], 0)
        self.assertEqual(row['probes_completed'], 30)

    def test_five_probe_sentinel_bug_has_exact_known_k(self):
        row = self.write_candidate('sentinel_bug', BUG_SENTINEL, 2)
        self.assertIsNone(row['excluded'])
        self.assertEqual(row['k'], 5)
        self.assertEqual(row['family_counts']['U'], 5)
        self.assertEqual(row['C'], 1.0)

    def test_constant_zero_has_known_k_29(self):
        row = self.write_candidate('zero', CONST_ZERO, 3)
        self.assertIsNone(row['excluded'])
        self.assertEqual(row['k'], 29)

    def test_constant_minus_one_has_known_k_25(self):
        row = self.write_candidate('minus_one', CONST_MINUS_ONE, 4)
        self.assertIsNone(row['excluded'])
        self.assertEqual(row['k'], 25)

    def test_plus_one_distance_bug_has_known_k_25(self):
        row = self.write_candidate('plus_one', PLUS_ONE, 5)
        self.assertIsNone(row['excluded'])
        self.assertEqual(row['k'], 25)

    def test_single_R1_bug_has_k_one(self):
        row = self.write_candidate('r1_bug', ONE_PROBE_R1_BUG, 6)
        self.assertIsNone(row['excluded'])
        self.assertEqual(row['k'], 1)

    def test_single_Z4_bug_has_k_one(self):
        row = self.write_candidate('z4_bug', ONE_PROBE_Z4_BUG, 7)
        self.assertIsNone(row['excluded'])
        self.assertEqual(row['k'], 1)

    def test_runtime_exception_is_probe_failure_not_load_error(self):
        row = self.write_candidate('runtime_crash', RUNTIME_CRASH, 8)
        self.assertIsNone(row['excluded'])
        self.assertEqual(row['k'], 30)
        self.assertTrue(all(row['fails']))

    def test_import_error_and_undefined_name_receive_no_k(self):
        missing_import = self.write_candidate('missing_import', MISSING_IMPORT, 9)
        undefined = self.write_candidate('undefined', UNDEFINED_GLOBAL, 10)
        no_solve = self.write_candidate('no_solve', NO_SOLVE, 13)
        syntax = self.write_candidate('syntax', SYNTAX_ERROR, 14)
        for row in (missing_import, undefined, no_solve, syntax):
            self.assertIsNotNone(row['excluded'])
            self.assertIsNone(row['k'])
            self.assertIsNone(row['fails'])

    def test_duplicate_body_hash_keeps_first_provenance_group(self):
        normalized = generate.normalize(REFERENCE)
        digest = hashlib.sha256(normalized.encode()).hexdigest()
        attempts = self.gen / 'attempts.jsonl'
        for batch in (11, 12):
            rec = {'batch_id': batch, 'model': 'test', 'prompt_variant': 'test',
                   'candidate_records': [{'body_hash': digest, 'stored_new': batch == 11}]}
            with attempts.open('a', encoding='utf-8') as fh:
                fh.write(json.dumps(rec) + '\n')
        self.assertEqual(run_gate.body_meta()[digest]['group_id'], 'batch-011')


if __name__ == '__main__':
    unittest.main()
