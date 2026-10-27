def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    in_queue = [False] * n
    queue = deque([s])
    in_queue[s] = True

    while queue:
        u = queue.popleft()
        in_queue[u] = False
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True

    return -1 if dist[t] == inf else dist[t]
