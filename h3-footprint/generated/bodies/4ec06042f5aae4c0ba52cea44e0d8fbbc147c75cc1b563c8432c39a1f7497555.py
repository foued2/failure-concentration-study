def solve(n, edges, s, t):
    import heapq

    if n <= 0 or s < 0 or t < 0 or s >= n or t >= n:
        return -1
    if s == t:
        return 0

    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        if 0 <= u < n and 0 <= v < n and w >= 0:
            graph[u].append((v, w))

    infinity = float("inf")
    distance = [infinity] * n
    distance[s] = 0
    finished = [False] * n
    buckets = {0: [s]}
    active = [0]

    while active:
        level = heapq.heappop(active)
        if level not in buckets:
            continue
        layer = buckets.pop(level)
        for node in layer:
            if finished[node] or distance[node] != level:
                continue
            if node == t:
                return level
            finished[node] = True
            for neighbor, weight in graph[node]:
                candidate = level + weight
                if candidate < distance[neighbor]:
                    distance[neighbor] = candidate
                    if candidate not in buckets:
                        buckets[candidate] = []
                        heapq.heappush(active, candidate)
                    buckets[candidate].append(neighbor)

    return -1
