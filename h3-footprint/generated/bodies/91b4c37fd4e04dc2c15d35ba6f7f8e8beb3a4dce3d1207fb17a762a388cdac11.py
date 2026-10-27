def solve(n, edges, s, t):
    E = [e for e in edges if 0 <= e[0] < n and 0 <= e[1] < n]
    best = [1 << 60] * n
    best[s] = 0
    heap = [(0, s)]
    seen = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u == t:
            return d
        if u in seen:
            continue
        seen.add(u)
        for v, w in E and [(v, w) for (uu, v, w) in E if uu == u]:
            nd = d + w
            if nd < best[v]:
                best[v] = nd
                heapq.heappush(heap, (nd, v))
    return -1
