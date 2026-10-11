"""Directive: greedy walk always taking the largest outgoing edge."""


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
