def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    removed = object()
    ticket = count()
    heap = []
    live = {}
    dist = {s: 0}

    def offer(node, d):
        if node in live:
            live[node][2] = removed
        entry = [d, next(ticket), node]
        live[node] = entry
        heapq.heappush(heap, entry)

    offer(s, 0)
    while heap:
        d, _, node = heapq.heappop(heap)
        if node is removed:
            continue
        if node == t:
            return d
        for v, w in adj[node]:
            nd = d + w
            if nd < dist.get(v, INF):
                dist[v] = nd
                offer(v, nd)
    return -1
