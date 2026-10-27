def solve(n, edges, s, t):
    import heapq

    if n <= 0 or s < 0 or t < 0 or s >= n or t >= n:
        return -1
    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        if 0 <= u < n and 0 <= v < n:
            graph[u].append((v, w))

    infinity = float("inf")
    distance = [infinity] * n
    distance[s] = 0
    queue = [(0, s)]

    while queue:
        current, node = heapq.heappop(queue)
        if current != distance[node]:
            continue
        if node == t:
            return current
        for neighbor, weight in graph[node]:
            candidate = current + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                heapq.heappush(queue, (candidate, neighbor))

    return -1
