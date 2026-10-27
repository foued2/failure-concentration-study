def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    buckets = {0: [s]}

    while buckets:
        current = min(buckets)
        nodes = buckets.pop(current)
        for u in nodes:
            if dist[u] != current:
                continue
            if u == t:
                return current
            for v, w in graph[u]:
                nd = current + w
                if nd < dist[v]:
                    dist[v] = nd
                    buckets.setdefault(nd, []).append(v)

    return -1 if dist[t] == inf else dist[t]
