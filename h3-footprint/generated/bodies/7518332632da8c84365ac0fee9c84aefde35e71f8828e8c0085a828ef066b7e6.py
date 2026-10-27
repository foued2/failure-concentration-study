def solve(n, edges, s, t):
    adj = defaultdict(list)
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    best = defaultdict(lambda: INF)
    best[s] = 0
    done = set()
    heap = [(0, s)]
    while heap:
        cost, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        if u == t:
            return cost
        for v, w in adj[u]:
            if cost + w < best[v]:
                best[v] = cost + w
                heapq.heappush(heap, (best[v], v))
    return -1
