"""Submission 076 (base body 26, replica 0)."""

def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    best = [float("inf")]
    def dfs(u, cost, visited):
        if cost >= best[0]:
            return
        if u == t:
            best[0] = cost
            return
        for v, w in g[u]:
            if v not in visited:
                dfs(v, cost + w, visited | {v})
    dfs(s, 0, {s})
    return -1 if best[0] == float("inf") else best[0]
