def solve(n, edges, s, t):
    import math
    if s == t:
        return 0
    d = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for u, v, w in edges:
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            a = d[i][k]
            if a == math.inf:
                continue
            di = d[i]
            for j in range(n):
                b = dk[j]
                if b == math.inf:
                    continue
                nd = a + b
                if nd < di[j]:
                    di[j] = nd
    ans = d[s][t]
    return -1 if ans == math.inf else ans
