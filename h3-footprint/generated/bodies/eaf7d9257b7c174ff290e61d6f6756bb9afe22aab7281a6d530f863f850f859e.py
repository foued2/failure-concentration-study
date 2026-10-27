def solve(n, edges, s, t):
    graph = {}
    for u, v, w in edges:
        graph.setdefault(u, []).append((v, w))
    best = {s: 0}
    pq = [(0, s)]
    done = set()
    while pq:
        d, cur = heappop(pq)
        if cur in done:
            continue
        done.add(cur)
        if cur == t:
            return int(d)
        for nxt, wt in graph.get(cur, []):
            nd = d + wt
            if nd < best.get(nxt, float('inf')):
                best[nxt] = nd
                heappush(pq, (nd, nxt))
    return -1
