def solve(n, edges, s, t):
    import heapq

    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))

    dist = {s: 0}
    pq = [(0, s)]
    done = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in done:
            continue
        done.add(u)

        if u == t:
            return d

        for v, w in adj.get(u, []):
            nd = d + w
            if v not in dist or nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    return -1
