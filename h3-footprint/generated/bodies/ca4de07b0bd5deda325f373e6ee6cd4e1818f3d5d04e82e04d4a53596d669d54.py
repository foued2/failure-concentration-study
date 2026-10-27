def solve(n, edges, s, t):
    if s == t:
        return 0
    radj = [[] for _ in range(n)]
    for u, v, w in edges:
        radj[v].append((u, w))
    seen = {}
    pq = [(0, t)]
    while pq:
        d, x = heapq.heappop(pq)
        if x in seen:
            continue
        seen[x] = d
        if x == s:
            return d
        for u, w in radj[x]:
            if u not in seen:
                heapq.heappush(pq, (d + w, u))
    return -1
