from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
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

LIST_SCAN = """def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    inf = 10 ** 18
    dist = [inf] * n
    dist[s] = 0
    used = [False] * n
    for _ in range(n):
        u = -1
        for i in range(n):
            if not used[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if u == -1 or dist[u] == inf:
            break
        used[u] = True
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == inf else dist[t]
"""

BFS = """from collections import deque

def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            return dist[u]
        for v, w in adj[u]:
            nd = dist[u] + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                q.append(v)
    return -1
"""

BELLMAN = """def solve(n, edges, s, t):
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return -1 if dist[t] == inf else dist[t]
"""

FLOYD = """def solve(n, edges, s, t):
    inf = float("inf")
    dist = [[inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = w
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return -1 if dist[s][t] == inf else dist[s][t]
"""

DFS = """def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    best = [float("inf")]
    def dfs(u, d, seen):
        if u == t:
            best[0] = min(best[0], d)
            return
        for v, w in adj[u]:
            if v not in seen:
                dfs(v, d + w, seen | {v})
    dfs(s, 0, {s})
    return -1 if best[0] == float("inf") else best[0]
"""


class ConservativeClassifierTests(unittest.TestCase):
    def test_genuine_algorithms_are_recognized(self):
        self.assertEqual(run_gate.base_label(REFERENCE), "heap_dijkstra")
        self.assertEqual(run_gate.base_label(BFS), "bfs")
        self.assertEqual(run_gate.base_label(BELLMAN), "bellman_ford")
        self.assertEqual(run_gate.base_label(FLOYD), "floyd")
        self.assertEqual(run_gate.base_label(DFS), "dfs_bruteforce")

    def test_list_scan_dijkstra_is_not_forced_into_a_cell(self):
        self.assertEqual(run_gate.base_label(LIST_SCAN), "other")

    def test_comment_terms_cannot_change_the_label(self):
        source = "# heapq heappush heappop floyd bellman deque def dfs\n" + LIST_SCAN
        self.assertEqual(run_gate.base_label(source), "other")

    def test_docstring_terms_cannot_change_the_label(self):
        source = LIST_SCAN.replace(
            "def solve(n, edges, s, t):\n",
            'def solve(n, edges, s, t):\n    """heapq heappush floyd bellman deque dfs."""\n',
            1,
        )
        self.assertEqual(run_gate.base_label(source), "other")

    def test_unused_heap_import_does_not_create_a_heap_cell(self):
        self.assertEqual(run_gate.base_label("import heapq\n" + LIST_SCAN), "other")

    def test_unused_deque_import_does_not_create_a_bfs_cell(self):
        self.assertEqual(run_gate.base_label("from collections import deque\n" + REFERENCE), "heap_dijkstra")

    def test_unused_recursive_helper_does_not_create_a_dfs_cell(self):
        helper = "def dfs(u):\n    return dfs(u)\n"
        self.assertEqual(run_gate.base_label(helper + REFERENCE), "heap_dijkstra")

    def test_unused_floyd_shaped_helper_does_not_create_a_floyd_cell(self):
        helper = FLOYD.replace("def solve", "def floyd_unused")
        self.assertEqual(run_gate.base_label(helper + REFERENCE), "heap_dijkstra")

    def test_heap_used_only_in_an_unreached_helper_is_ignored(self):
        helper = "import heapq\ndef helper(pq):\n    heapq.heappush(pq, 1)\n"
        self.assertEqual(run_gate.base_label(helper + LIST_SCAN), "other")

    def test_import_aliases_are_resolved(self):
        aliased = REFERENCE.replace("import heapq", "import heapq as hq").replace("heapq.", "hq.")
        self.assertEqual(run_gate.base_label(aliased), "heap_dijkstra")
        from_import = REFERENCE.replace(
            "import heapq", "from heapq import heappush as push, heappop as pop"
        ).replace("heapq.heappush", "push").replace("heapq.heappop", "pop")
        self.assertEqual(run_gate.base_label(from_import), "heap_dijkstra")

    def test_multiple_structural_signals_fall_back_to_other(self):
        mixed = REFERENCE.replace(
            "    pq = [(0, s)]",
            "    def helper(x):\n        return helper(x - 1) if x else 0\n    helper(n)\n    pq = [(0, s)]",
        )
        self.assertEqual(run_gate.base_label(mixed), "other")


if __name__ == "__main__":
    unittest.main()
