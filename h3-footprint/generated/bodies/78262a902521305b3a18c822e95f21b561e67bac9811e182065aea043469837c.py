def solve(n, edges, s, t):
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
    tentative = {s: 0}
    settled = {}
    heap = [(0, s)]
    while heap and t not in settled:
        d, u = heapq.heappop(heap)
        if u in settled:
            continue
        settled[u] = d
        for v, w in g[u]:
            nd = d + w
            if nd < tentative.get(v, float('inf')):
                tentative[v] = nd
                heapq.heappush(heap, (nd, v))
    return settled.get(t, -1)
