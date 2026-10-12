"""Submission 079 (base body 27, replica 0)."""

def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    memo = {}
    def best(u, stack):
        if u == t:
            return 0
        if u in memo:
            return memo[u]
        if u in stack:
            return float("inf")
        m = float("inf")
        for v, w in g[u]:
            sub = best(v, stack | {u})
            if sub != float("inf"):
                m = min(m, w + sub)
        memo[u] = m
        return m
    r = best(s, frozenset())
    return -1 if r == float("inf") else r
