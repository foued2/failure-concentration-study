def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = {s: 0}
    heap = [(0, s)]
    done = set()

    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue

        done.add(u)

        if u == t:
            return d

        for v, w in graph[u]:
            if v in done:
                continue
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))

    return -1
