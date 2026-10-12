"""Submission 046 (base body 16, replica 0)."""

def solve(n, edges, s, t):
    # natural defect: skips self-initialization for unreachable pairs handled oddly
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return -1 if d[s][t] == INF else d[s][t] + (0 if s == t else 0)
