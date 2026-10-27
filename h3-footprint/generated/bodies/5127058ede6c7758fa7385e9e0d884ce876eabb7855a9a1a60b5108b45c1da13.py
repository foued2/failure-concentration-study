def solve(n, edges, s, t):
    from collections import deque

    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    inf = float("inf")
    dist = [inf] * n
    queued = [False] * n
    dist[s] = 0
    queue = deque([s])
    queued[s] = True

    while queue:
        u = queue.popleft()
        queued[u] = False
        base = dist[u]

        for v, w in graph[u]:
            candidate = base + w
            if candidate < dist[v]:
                dist[v] = candidate
                if not queued[v]:
                    queued[v] = True
                    queue.append(v)

    if dist[t] == inf:
        return -1
    return int(dist[t])
