def solve(n, edges, s, t):
    if s == t:
        return 0
    INF = 10**30

    def mul(a, b):
        c = [[INF] * n for _ in range(n)]
        for i in range(n):
            ai = a[i]
            ci = c[i]
            for k in range(n):
                aik = ai[k]
                if aik >= INF:
                    continue
                bk = b[k]
                for j in range(n):
                    val = aik + bk[j]
                    if val < ci[j]:
                        ci[j] = val
        return c

    cur = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if w < cur[u][v]:
            cur[u][v] = w
    res = [[INF] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 0
    hops = n - 1
    while hops:
        if hops & 1:
            res = mul(res, cur)
        hops >>= 1
        if hops:
            cur = mul(cur, cur)
    ans = res[s][t]
    return -1 if ans >= INF else ans
