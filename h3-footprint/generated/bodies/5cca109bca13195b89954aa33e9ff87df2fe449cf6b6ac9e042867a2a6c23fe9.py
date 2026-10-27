def solve(n, edges, s, t):
    from collections import deque
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    queue = deque([s])
    in_queue = [False] * n
    in_queue[s] = True
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        du = dist[u]
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    in_queue[v] = True
                    queue.append(v)
    return int(dist[t]) if dist[t] != INF else -1
