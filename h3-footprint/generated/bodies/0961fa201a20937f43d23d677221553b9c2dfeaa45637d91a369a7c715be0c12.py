def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    heap = [(0, s)]
    seen = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in seen:
            continue
        seen.add(u)
        if u == t:
            return d
        for v, w in adj[u]:
            if v not in seen:
                heapq.heappush(heap, (d + w, v))
    return -1
