import heapq


def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    distances = [None] * n
    distances[s] = 0
    queue = [(0, s)]

    while queue:
        distance, node = heapq.heappop(queue)
        if distance != distances[node]:
            continue
        if node == t:
            return distance
        for neighbor, weight in graph[node]:
            new_distance = distance + weight
            if distances[neighbor] is None or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(queue, (new_distance, neighbor))

    return -1