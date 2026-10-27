def solve(n, edges, s, t):
    import heapq
    INF = float("inf")
    matrix = [[INF] * n for _ in range(n)]
    for u, v, w in edges:
        if w < matrix[u][v]:
            matrix[u][v] = w
    dist = [INF] * n
    dist[s] = 0
    visited = [False] * n
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if visited[u] or d != dist[u]:
            continue
        visited[u] = True
        if u == t:
            return d
        for v in range(n):
            w = matrix[u][v]
            if w != INF and not visited[v] and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    return -1
