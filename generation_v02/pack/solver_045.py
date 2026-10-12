"""Submission 045 (base body 15, replica 2)."""

def solve(n, edges, s, t):
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for _ in range(n):
        changed = False
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i][j] > d[i][k] + d[k][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        changed = True
        if not changed:
            break
    return -1 if d[s][t] == INF else d[s][t]
