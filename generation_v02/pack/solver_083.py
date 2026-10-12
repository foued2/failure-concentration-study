"""Submission 083 (base body 28, replica 1)."""

def solve(n, edges, s, t):
    # natural defect: memo keyed only by node, ignores cycle stack (can loop-wrong)
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    memo = {t: 0}
    def best(u, depth):
        if u in memo:
            return memo[u]
        if depth > n:
            return float("inf")
        m = float("inf")
        for v, w in g[u]:
            sub = best(v, depth + 1)
            if sub != float("inf"):
                m = min(m, w + sub)
        memo[u] = m
        return m
    r = best(s, 0)
    return -1 if r == float("inf") else r
