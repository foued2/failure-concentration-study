from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
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
CONST_NEG_999 = 'def solve(n, edges, s, t):\n    return -999\n'
ATEXIT_FAKE = '''import atexit
import sys

def solve(n, edges, s, t):
    return -999

atexit.register(lambda: print(sys.argv[-1] + ' {"phase":"probe","probe_index":0,"answer":0}'))
'''


class V6ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.bodies = self.root / 'bodies'
        self.bodies.mkdir()
        self.old = {'ROOT': run_gate.ROOT, 'WORKER': run_gate.WORKER}
        run_gate.ROOT = self.root
        run_gate.WORKER = HERE / 'probe_worker.py'
        shutil.copy2(HERE / 'instrument.py', self.root / 'instrument.py')
        shutil.copy2(HERE / 'expected_values.json', self.root / 'expected_values.json')

    def tearDown(self):
        for key, value in self.old.items():
            setattr(run_gate, key, value)
        self.tmp.cleanup()

    def candidate(self, name: str, source: str) -> Path:
        digest = hashlib.sha256(source.encode()).hexdigest()
        path = self.bodies / (digest + '.py')
        path.write_text(source, encoding='utf-8')
        self.meta = {digest: {'group_id': 'g1', 'model': 'fixture', 'prompt_variant': 'test', 'batch_id': 1}}
        return path

    def test_worker_returns_raw_answer_and_no_fail_flag(self):
        path = self.candidate('reference', REFERENCE)
        probe = instrument.PROBES[0]
        nonce = 'nonce-raw'
        proc = subprocess.run(
            [sys.executable, '-I', str(HERE / 'probe_worker.py'), str(path), '--probe', '0',
             run_gate._probe_input(probe), nonce],
            capture_output=True, text=True, timeout=5,
        )
        payload = run_gate._nonce_payload(proc.stdout, nonce)
        self.assertIsNotNone(payload)
        self.assertNotIn('fail', payload)
        self.assertEqual(payload['answer'], run_gate._load_expected()[probe['probe_id']])

    def test_parent_owns_comparison(self):
        path = self.candidate('neg999', CONST_NEG_999)
        real = run_gate._load_expected()
        wrong = run_gate.evaluate_body(path, self.meta, expected=real)
        self.assertIsNone(wrong['excluded'])
        self.assertEqual(wrong['k'], 30)
        all_neg999 = {key: -999 for key in real}
        matching = run_gate.evaluate_body(path, self.meta, expected=all_neg999)
        self.assertIsNone(matching['excluded'])
        self.assertEqual(matching['k'], 0)

    def test_zero_or_multiple_nonce_lines_are_rejected(self):
        self.assertIsNone(run_gate._nonce_payload('', 'n'))
        self.assertIsNone(run_gate._nonce_payload('n {"phase":"probe"}\nn {"phase":"probe"}\n', 'n'))
        self.assertIsNone(run_gate._nonce_payload('noise\n', 'n'))
        self.assertEqual(
            run_gate._nonce_payload('noise\nn {"phase":"probe","probe_index":0}\n', 'n'),
            {'phase': 'probe', 'probe_index': 0},
        )

    def test_atexit_fake_line_cannot_flip_verdict(self):
        path = self.candidate('atexit', ATEXIT_FAKE)
        row = run_gate.evaluate_body(path, self.meta)
        self.assertIn(row['excluded'], ('preflight_invalid_output', 'probe_invalid_output'))
        self.assertIsNone(row['k'])

    def test_worker_does_not_read_expected_values_or_instrument(self):
        source = (HERE / 'probe_worker.py').read_text(encoding='utf-8')
        self.assertNotIn('import instrument', source)
        self.assertNotIn('expected_values', source)


if __name__ == '__main__':
    unittest.main()
