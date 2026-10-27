def solve(n, edges, s, t):
    from collections import deque

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
    queue = deque([s])
    queued = [False] * n
    queued[s] = True

    while queue:
        node = queue.popleft()
        queued[node] = False
        current = distance[node]
        for neighbor, weight in graph[node]:
            candidate = current + weight
            if candidate < distance[neighbor]:
                distance[neighbor] = candidate
                if not queued[neighbor]:
                    queued[neighbor] = True
                    queue.append(neighbor)

    return distance[t] if distance[t] != infinity else -1
