"""Submission 085 (base body 29, replica 0)."""

def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    total, seen, u = 0, set(), s
    while u != t:
        if u in seen or not g[u]:
            return -1
        seen.add(u)
        v, w = min(g[u], key=lambda e: e[1])
        total += w
        u = v
    return total
