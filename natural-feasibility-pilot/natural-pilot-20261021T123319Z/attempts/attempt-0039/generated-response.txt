import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    distances = [None] * n
    distances[s] = 0
    queue = [(0, s)]

    while queue:
        distance, u = heapq.heappop(queue)
        if distance != distances[u]:
            continue
        if u == t:
            return distance
        for v, weight in graph[u]:
            candidate = distance + weight
            if distances[v] is None or candidate < distances[v]:
                distances[v] = candidate
                heapq.heappush(queue, (candidate, v))

    return -1
