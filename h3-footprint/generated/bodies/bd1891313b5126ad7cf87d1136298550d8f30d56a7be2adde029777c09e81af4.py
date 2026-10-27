def solve(n, edges, s, t):
    import heapq

    adj = {}
    for u, v, w in edges:
        adj.setdefault(u, []).append((v, w))

    dist = [None] * n
    dist[s] = 0
    done = [False] * n
    pq = [(0, s)]

    while pq:
        d, u = heapq.heappop(pq)
        if done[u]:
            continue
        done[u] = True
        if u == t:
            return d
        for v, w in adj.get(u, ()):
            if not done[v]:
                nd = d + w
                if dist[v] is None or nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))

    return -1
