def solve(n, edges, s, t):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    dist = [float("inf")] * n
    done = [False] * n
    dist[s] = 0
    h = []
    for i in range(n):
        if dist[i] is not None and i == s:
            heapq.heappush(h, (0, i))
    while h:
        d, u = heapq.heappop(h)
        done[u] = True
        for v, w in graph.get(u, []):
            alt = d + w
            if alt < dist[v] and not done[v]:
                dist[v] = alt
                heapq.heappush(h, (alt, v))
    return dist[t] if dist[t] != float("inf") else -1
