def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    heap = [(0, s)]
    settled = [False] * n

    while heap:
        d, u = heapq.heappop(heap)
        if settled[u]:
            continue

        settled[u] = True
        if u == t:
            return d

        for v, w in graph[u]:
            if not settled[v]:
                heapq.heappush(heap, (d + w, v))

    return -1
