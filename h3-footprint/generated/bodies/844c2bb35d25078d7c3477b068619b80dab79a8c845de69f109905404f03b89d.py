def solve(n, edges, s, t):
    graph = {}
    for u, v, w in edges:
        if u not in graph:
            graph[u] = {}
        old = graph[u].get(v)
        if old is None or w < old:
            graph[u][v] = w

    dist = [None] * n
    dist[s] = 0
    heap = [(0, s)]

    while heap:
        d, u = heapq.heappop(heap)
        if dist[u] is not None and d > dist[u]:
            continue
        if u == t:
            break
        for v, w in graph.get(u, {}).items():
            nd = d + w
            if dist[v] is None or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return -1 if dist[t] is None else dist[t]
