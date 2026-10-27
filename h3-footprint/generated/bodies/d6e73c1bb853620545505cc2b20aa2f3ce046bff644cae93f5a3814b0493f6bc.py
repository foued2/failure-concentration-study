def solve(n, edges, s, t):
    INF = 1 << 62
    cur = [INF] * n
    cur[s] = 0
    for _ in range(n - 1):
        nxt = cur[:]
        for u, v, w in edges:
            if cur[u] + w < nxt[v]:
                nxt[v] = cur[u] + w
        cur = nxt
    return cur[t] if cur[t] < INF else -1
