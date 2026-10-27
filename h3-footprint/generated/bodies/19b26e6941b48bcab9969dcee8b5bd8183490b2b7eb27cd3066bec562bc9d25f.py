def solve(n, edges, s, t):
    inf = float("inf")
    cur = [inf] * n
    cur[s] = 0

    for _ in range(n - 1):
        nxt = cur[:]
        for u, v, w in edges:
            if cur[u] != inf and cur[u] + w < nxt[v]:
                nxt[v] = cur[u] + w
        if nxt == cur:
            break
        cur = nxt

    return -1 if cur[t] == inf else cur[t]
