def solve(n, edges, s, t):
    out = [[] for _ in range(n)]
    for u, v, w in edges:
        out[u].append((v, w))
    unseen = set(range(n))
    dist = {s: 0}
    queue = [(0, s)]
    while queue:
        d, u = heapq.heappop(queue)
        if u not in unseen:
            continue
        unseen.discard(u)
        if u == t:
            return d
        for v, w in out[u]:
            if v in unseen and d + w < dist.get(v, float('inf')):
                dist[v] = d + w
                heapq.heappush(queue, (d + w, v))
    return -1
