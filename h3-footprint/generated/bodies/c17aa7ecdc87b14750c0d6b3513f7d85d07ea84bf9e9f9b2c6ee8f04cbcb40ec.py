def solve(n, edges, s, t):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    best = {s: 0}
    heap = [(0, s)]

    while heap:
        d, u = heapq.heappop(heap)
        if best.get(u) != d:
            continue
        if u == t:
            return d

        for v, w in graph.get(u, ()):
            nd = d + w
            old = best.get(v)
            if old is None or nd < old:
                best[v] = nd
                heapq.heappush(heap, (nd, v))

    return -1
