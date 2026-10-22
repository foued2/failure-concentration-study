"""Prespecified hand-built SSSP variants for bank-coverage calibration."""
from __future__ import annotations

VARIANTS = {
    "reference_dijkstra": {
        "defect": "none; correct reference control",
        "source": r'''import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        if u == t:
            return du
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
''',
    },
    "unreachable_wrong_sentinel": {
        "defect": "returns 0 instead of -1 for an unreachable target",
        "source": r'''import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        if u == t:
            return du
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return 0
''',
    },
    "skip_zero_weight_edges": {
        "defect": "omits zero-weight edges from the graph",
        "source": r'''import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        if w != 0:
            graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        if u == t:
            return du
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
''',
    },
    "last_parallel_edge": {
        "defect": "keeps only the last parallel edge for each node pair",
        "source": r'''import heapq

def solve(n, edges, s, t):
    graph = [{} for _ in range(n)]
    for u, v, w in edges:
        graph[u][v] = w
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        if u == t:
            return du
        for v, w in graph[u].items():
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
''',
    },
    "reject_self_loops": {
        "defect": "raises on a valid graph containing a self-loop",
        "source": r'''import heapq

def solve(n, edges, s, t):
    for u, v, w in edges:
        if u == v:
            raise ValueError("self-loop")
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        if u == t:
            return du
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
''',
    },
    "bfs_unweighted": {
        "defect": "ignores edge weights and returns unweighted hop count",
        "source": r'''from collections import deque

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append(v)
    dist = [-1] * n
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            return dist[u]
        for v in graph[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)
    return -1
''',
    },
    "early_return_on_target_push": {
        "defect": "returns when the target is first discovered, before later relaxation",
        "source": r'''import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        if u == t:
            return du
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if v == t:
                    return nd
                heapq.heappush(pq, (nd, v))
    return -1
''',
    },
    "directed_as_undirected": {
        "defect": "adds reverse edges to a directed graph",
        "source": r'''import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        if u == t:
            return du
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return -1
''',
    },
}

VARIANT_ORDER = [
    "reference_dijkstra",
    "unreachable_wrong_sentinel",
    "skip_zero_weight_edges",
    "last_parallel_edge",
    "reject_self_loops",
    "bfs_unweighted",
    "early_return_on_target_push",
    "directed_as_undirected",
]
