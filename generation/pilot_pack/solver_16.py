"""Directive: DFS with memoization on nodes."""


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
