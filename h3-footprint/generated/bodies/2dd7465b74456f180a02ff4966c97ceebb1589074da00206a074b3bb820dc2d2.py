def solve(n, edges, s, t):
    nbrs = [[] for _ in range(n)]
    for u, v, w in edges:
        nbrs[u].append((v, w))
    UNSEEN, DONE = 0, 1
    INF = float("inf")
    dist = [INF] * n
    state = [UNSEEN] * n
    dist[s] = 0
    while True:
        u = -1
        best = INF
        for i in range(n):
            if state[i] == UNSEEN and dist[i] < best:
                best = dist[i]
                u = i
        if u == -1 or best == INF:
            break
        state[u] = DONE
        if u == t:
            return dist[u]
        for v, w in nbrs[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
    return -1
