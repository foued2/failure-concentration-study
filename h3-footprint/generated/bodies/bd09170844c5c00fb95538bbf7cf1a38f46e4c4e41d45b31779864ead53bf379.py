def solve(n, edges, s, t):
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    for _ in range(n - 1):
        nxt = dist[:]
        for u, v, w in edges:
            if dist[u] != inf:
                candidate = dist[u] + w
                if candidate < nxt[v]:
                    nxt[v] = candidate
        dist = nxt
    return -1 if dist[t] == inf else dist[t]
