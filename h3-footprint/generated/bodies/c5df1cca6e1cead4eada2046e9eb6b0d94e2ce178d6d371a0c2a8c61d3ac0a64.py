def solve(n, edges, s, t):
    if n <= 0:
        return -1
    if s == t:
        return 0
    INF = float("inf")
    mat = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if w < mat[u][v]:
            mat[u][v] = w
    dist = [INF] * n
    settled = [False] * n
    dist[s] = 0
    for _ in range(n):
        u = -1
        cur = INF
        for i in range(n):
            if not settled[i] and dist[i] < cur:
                cur = dist[i]
                u = i
        if u == -1:
            break
        if u == t:
            return cur
        settled[u] = True
        row = mat[u]
        for v in range(n):
            if not settled[v] and row[v] < INF:
                cand = cur + row[v]
                if cand < dist[v]:
                    dist[v] = cand
    return -1
