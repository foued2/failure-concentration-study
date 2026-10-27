def solve(n, edges, s, t):
    import heapq
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = [float('inf')] * n
    dist[s] = 0
    settled = set()
    pq = [(0, s)]
    while pq:
        cost, u = heapq.heappop(pq)
        if u in settled:
            continue
        settled.add(u)
        if u == t:
            break
        for v, w in adj[u]:
            if v not in settled:
                alt = cost + w
                if alt < dist[v]:
                    dist[v] = alt
                    heapq.heappush(pq, (alt, v))
    return -1 if dist[t] == float('inf') else dist[t]
