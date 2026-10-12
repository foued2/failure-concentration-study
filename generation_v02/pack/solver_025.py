"""Submission 025 (base body 9, replica 0)."""

def solve(n, edges, s, t):
    d = [10**18] * n
    d[s] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if d[u] + w < d[v]:
                d[v] = d[u] + w
    return -1 if d[t] >= 10**18 else d[t]
