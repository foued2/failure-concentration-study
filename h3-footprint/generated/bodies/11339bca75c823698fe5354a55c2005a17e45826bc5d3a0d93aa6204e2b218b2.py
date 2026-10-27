def solve(n, edges, s, t):
    g = {i: [] for i in range(n)}
    for u, v, w in edges:
        g[u].append((v, w))
    INF = float('inf')
    dist = [INF] * n
    dist[s] = 0
    done = [False] * n
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v, w in g[u]:
            if not done[v] and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (d + w, v))
    return dist[t] if dist[t] < INF else -1
