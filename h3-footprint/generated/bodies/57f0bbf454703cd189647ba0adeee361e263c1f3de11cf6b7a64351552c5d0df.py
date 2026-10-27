def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        if u != v:
            graph[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    settled = [False] * n
    heap = [(0, s)]
    remaining = n
    while heap and remaining:
        d, u = heapq.heappop(heap)
        if settled[u]:
            continue
        settled[u] = True
        remaining -= 1
        for v, w in graph[u]:
            if not settled[v] and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return dist[t] if dist[t] != INF else -1
