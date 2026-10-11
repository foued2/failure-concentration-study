"""Emit the pilot solver pack exactly once per specs/generator_spec.json.

Generation session: executor (MIMO, opencode/mimo-v2.6-flash-free), 2026-10-11.
Each submission is a single-shot LLM generation following its approach directive:
first solution produced, no self-review, no fixing, retained in order.
Run once; files must not be regenerated or edited.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "generation" / "pilot_pack"

SOLVERS: dict[str, str] = {}

SOLVERS["solver_01"] = '''"""Directive: Dijkstra with heapq."""
import heapq


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
'''

SOLVERS["solver_02"] = '''"""Directive: Bellman-Ford relaxation."""


def solve(n, edges, s, t):
    dist = [float("inf")] * n
    dist[s] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    return dist[t] if dist[t] != float("inf") else -1
'''

SOLVERS["solver_03"] = '''"""Directive: Dijkstra with dict distances."""
import heapq


def solve(n, edges, s, t):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    best = {s: 0}
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > best.get(u, float("inf")):
            continue
        if u == t:
            return d
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < best.get(v, float("inf")):
                best[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
'''

SOLVERS["solver_04"] = '''"""Directive: BFS assuming unit weights."""
from collections import deque


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, _ in edges:
        adj[u].append(v)
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist[t]
'''

SOLVERS["solver_05"] = '''"""Directive: DP over topological order."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for u, v, w in edges:
        adj[u].append((v, w))
        indeg[v] += 1
    from collections import deque

    q = deque([i for i in range(n) if indeg[i] == 0])
    order = []
    indeg_copy = indeg[:]
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in adj[u]:
            indeg_copy[v] -= 1
            if indeg_copy[v] == 0:
                q.append(v)
    if len(order) != n:
        return -1
    dist = [float("inf")] * n
    dist[s] = 0
    for u in order:
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] != float("inf") else -1
'''

SOLVERS["solver_06"] = '''"""Directive: brute-force path enumeration."""


def solve(n, edges, s, t):
    best = [float("inf")]

    def dfs(u, cost, visited, used):
        if u == t:
            if cost < best[0]:
                best[0] = cost
            return
        for i, (a, b, w) in enumerate(edges):
            if i in used or a != u or b in visited:
                continue
            dfs(b, cost + w, visited | {b}, used | {i})

    dfs(s, 0, {s}, set())
    return -1 if best[0] == float("inf") else best[0]
'''

SOLVERS["solver_07"] = '''"""Directive: Dijkstra with greedy visited-on-push shortcut."""
import heapq


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    visited = set()
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist[t] if dist[t] != float("inf") else -1
'''

SOLVERS["solver_08"] = '''"""Directive: A*-style search with zero heuristic."""
import heapq


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    def h(node):
        return 0

    g = {s: 0}
    pq = [(h(s), 0, s)]
    closed = set()
    while pq:
        _, cost, u = heapq.heappop(pq)
        if u in closed:
            continue
        closed.add(u)
        if u == t:
            return cost
        for v, w in adj[u]:
            ng = cost + w
            if ng < g.get(v, float("inf")):
                g[v] = ng
                heapq.heappush(pq, (ng + h(v), ng, v))
    return -1
'''

SOLVERS["solver_09"] = '''"""Directive: Floyd-Warshall all-pairs."""


def solve(n, edges, s, t):
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        for i in range(n):
            if d[i][k] == INF:
                continue
            for j in range(n):
                if d[k][j] == INF:
                    continue
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d[s][t] if d[s][t] != INF else -1
'''

SOLVERS["solver_10"] = '''"""Directive: Dijkstra with early exit when t first seen (not popped)."""
import heapq


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
                if v == t:
                    return nd
    return -1
'''

SOLVERS["solver_11"] = '''"""Directive: BFS counting edge weight as hop count."""
from collections import deque


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                q.append(v)
    return dist[t]
'''

SOLVERS["solver_12"] = '''"""Directive: Bellman-Ford with reduced iteration count."""


def solve(n, edges, s, t):
    dist = [float("inf")] * n
    dist[s] = 0
    for _ in range(n - 2):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] != float("inf") else -1
'''

SOLVERS["solver_13"] = '''"""Directive: Dial-style bucket approach."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    max_w = 1
    for u, v, w in edges:
        adj[u].append((v, w))
        max_w = max(max_w, w)
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    bound = max_w * n + 1
    buckets = [[] for _ in range(bound)]
    buckets[0].append(s)
    for d in range(bound):
        while buckets[d]:
            u = buckets[d].pop()
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v] and nd < bound:
                    dist[v] = nd
                    buckets[nd].append(v)
    return dist[t] if dist[t] != INF else -1
'''

SOLVERS["solver_14"] = '''"""Directive: Dijkstra with plain list scan."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    used = [False] * n
    for _ in range(n):
        u = -1
        best = INF
        for i in range(n):
            if not used[i] and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1:
            break
        used[u] = True
        if u == t:
            return dist[t]
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist[t] if dist[t] != INF else -1
'''

SOLVERS["solver_15"] = '''"""Directive: SPFA / queue-based relaxation."""
from collections import deque


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    inq = [False] * n
    dist[s] = 0
    q = deque([s])
    inq[s] = True
    while q:
        u = q.popleft()
        inq[u] = False
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                if not inq[v]:
                    q.append(v)
                    inq[v] = True
    return dist[t] if dist[t] != INF else -1
'''

SOLVERS["solver_16"] = '''"""Directive: DFS with memoization on nodes."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    memo = {}

    def best(u, stack):
        if u == t:
            return 0
        if u in memo:
            return memo[u]
        if u in stack:
            return float("inf")
        m = float("inf")
        for v, w in adj[u]:
            sub = best(v, stack | {u})
            if sub != float("inf"):
                m = min(m, w + sub)
        memo[u] = m
        return m

    r = best(s, set())
    return -1 if r == float("inf") else r
'''

SOLVERS["solver_17"] = '''"""Directive: matrix-style repeated relaxation."""


def solve(n, edges, s, t):
    d = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for _ in range(n):
        changed = False
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        changed = True
        if not changed:
            break
    return d[s][t] if d[s][t] != float("inf") else -1
'''

SOLVERS["solver_18"] = '''"""Directive: Dijkstra with decrease-key via sorted list simulation."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    keys = [(0, s)]
    in_tree = [False] * n
    for _ in range(n):
        keys.sort()
        u = None
        while keys:
            d, node = keys.pop(0)
            if not in_tree[node] and d == dist[node]:
                u = node
                break
        if u is None:
            break
        in_tree[u] = True
        if u == t:
            return dist[t]
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                keys.append((nd, v))
    return dist[t] if dist[t] != INF else -1
'''

SOLVERS["solver_19"] = '''"""Directive: greedy walk always taking the largest outgoing edge."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    total = 0
    seen = set()
    u = s
    while u != t:
        if u in seen:
            return -1
        seen.add(u)
        if not adj[u]:
            return -1
        v, w = max(adj[u], key=lambda e: e[1])
        total += w
        u = v
    return total
'''

SOLVERS["solver_20"] = '''"""Directive: relaxation loop with parent tracking; returns 0 on unreachable."""


def solve(n, edges, s, t):
    dist = [float("inf")] * n
    parent = [-1] * n
    dist[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    if dist[t] == float("inf"):
        return 0
    return dist[t]
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, src in SOLVERS.items():
        (OUT / f"{name}.py").write_text(src, encoding="utf-8")
    print(f"emitted {len(SOLVERS)} submissions to {OUT}")


if __name__ == "__main__":
    main()
