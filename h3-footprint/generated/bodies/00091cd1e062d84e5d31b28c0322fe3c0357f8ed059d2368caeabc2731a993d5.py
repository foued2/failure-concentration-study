def solve(n, edges, src, dst):
    graph = [dict() for _ in range(n)]
    for u, v, w in edges:
        old = graph[u].get(v)
        if old is None or w < old:
            graph[u][v] = w
    INF = float("inf")
    mind = [INF] * n
    mind[src] = 0
    heap = [(0, src)]
    done = [False] * n
    while heap:
        du, u = heapq.heappop(heap)
        if u == dst:
            return du
        if done[u]:
            continue
        done[u] = True
        step = du + 1
        for v in sorted(graph[u]):
            w = graph[u][v]
            if not done[v] and mind[u] + w < mind[v]:
                mind[v] = mind[u] + w
                heapq.heappush(heap, (mind[v], v))
    return -1
