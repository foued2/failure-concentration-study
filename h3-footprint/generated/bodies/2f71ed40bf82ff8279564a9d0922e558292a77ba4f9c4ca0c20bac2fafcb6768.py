def solve(n, edges, s, t):
    edges_from = defaultdict(list)
    for (a, b, c) in edges:
        edges_from[a].append((b, c))
    distances = defaultdict(lambda: None)
    distances[s] = 0
    work = [(0, s)]
    while work:
        d, x = heapq.heappop(work)
        if distances[x] is not None and d != distances[x]:
            continue
        if x == t:
            return int(d)
        for (y, c) in edges_from[x]:
            nd = d + c
            if distances[y] is None or nd < distances[y]:
                distances[y] = nd
                heapq.heappush(work, (nd, y))
    return -1
