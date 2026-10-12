"""Submission 090 (base body 30, replica 2)."""

def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    total, seen, u = 0, set(), s
    while u != t:
        if u in seen or not g[u]:
            return -1
        seen.add(u)
        v, w = max(g[u], key=lambda e: e[1])
        total += w
        u = v
    return total
