def solve(n, edges, s, t):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    best = [None] * n
    best[s] = 0
    pq = [(0, s)]
    while pq:
        d, node = heapq.heappop(pq)
        if d > best[node]:
            continue
        if node == t:
            return d
        for nxt, wt in graph.get(node, []):
            cand = d + wt
            if best[nxt] is None or cand < best[nxt]:
                best[nxt] = cand
                heapq.heappush(pq, (cand, nxt))
    return -1
