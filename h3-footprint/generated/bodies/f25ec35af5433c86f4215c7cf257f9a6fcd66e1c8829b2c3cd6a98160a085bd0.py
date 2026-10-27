def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    INF = float("inf")
    dist = [INF] * n
    queued = [False] * n
    dist[s] = 0

    queue = deque([s])
    queued[s] = True

    while queue:
        u = queue.popleft()
        queued[u] = False

        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if not queued[v]:
                    queued[v] = True
                    queue.append(v)

    return -1 if dist[t] == INF else dist[t]
