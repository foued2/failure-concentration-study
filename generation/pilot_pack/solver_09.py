"""Directive: Floyd-Warshall all-pairs."""


def solve(n, edges, s, t):
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        for i in range(n):
            if d[i][k] == INF:
                continue
            for j in range(n):
                if d[k][j] == INF:
                    continue
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return d[s][t] if d[s][t] != INF else -1
