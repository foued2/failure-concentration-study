"""Directive: matrix-style repeated relaxation."""


def solve(n, edges, s, t):
    d = [[float("inf")] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        d[u][v] = min(d[u][v], w)
    for _ in range(n):
        changed = False
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
                        changed = True
        if not changed:
            break
    return d[s][t] if d[s][t] != float("inf") else -1
