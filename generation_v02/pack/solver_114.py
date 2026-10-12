"""Submission 114 (base body 38, replica 2)."""

def solve(n, edges, s, t):
    INF = float("inf")
    dm = {}
    for i in range(n):
        dm[(i, i)] = 0
    for u, v, w in edges:
        key = (u, v)
        if key in dm:
            dm[key] = min(dm[key], w)
        else:
            dm[key] = w
    for k in range(n):
        for i in range(n):
            a = dm.get((i, k), INF)
            if a == INF:
                continue
            for j in range(n):
                b = dm.get((k, j), INF)
                if b == INF:
                    continue
                cur = dm.get((i, j), INF)
                if a + b < cur:
                    dm[(i, j)] = a + b
    r = dm.get((s, t), INF)
    return -1 if r == INF else r
