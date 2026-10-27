def solve(n, edges, s, t):
    from collections import deque
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    queue = deque([s])
    queued = [False] * n
    queued[s] = True
    while queue:
        u = queue.popleft()
        queued[u] = False
        current = dist[u]
        for v, w in graph[u]:
            candidate = current + w
            if dist[v] is None or candidate < dist[v]:
                dist[v] = candidate
                if not queued[v]:
                    queued[v] = True
                    queue.append(v)
    if dist[t] is None:
        return -1
    return dist[t]
