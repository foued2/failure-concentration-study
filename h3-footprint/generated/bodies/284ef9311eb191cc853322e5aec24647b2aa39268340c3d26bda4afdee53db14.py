def solve(n, edges, s, t):
    INF = float('inf')
    cur = [[INF] * n for _ in range(n)]
    for i in range(n):
        cur[i][i] = 0
    for u, v, w in edges:
        if w < cur[u][v]:
            cur[u][v] = w

    def compose(a, b):
        res = [[INF] * n for _ in range(n)]
        for i in range(n):
            ai = a[i]
            ri = res[i]
            for k in range(n):
                aik = ai[k]
                if aik == INF:
                    continue
                bk = b[k]
                for j in range(n):
                    bkj = bk[j]
                    if bkj == INF:
                        continue
                    cand = aik + bkj
                    if cand < ri[j]:
                        ri[j] = cand
        return res

    limit = n - 1
    rounds = 0 if limit <= 1 else (limit - 1).bit_length()
    for _ in range(rounds):
        cur = compose(cur, cur)
    ans = cur[s][t]
    if ans == INF:
        return -1
    return int(ans)
