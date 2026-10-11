"""Directive: A*-style search with zero heuristic."""
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
