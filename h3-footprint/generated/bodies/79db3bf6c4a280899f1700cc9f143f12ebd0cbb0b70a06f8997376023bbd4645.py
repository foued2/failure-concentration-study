def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    cap = 0
    for _, _, w in edges:
        cap += w
    layers = {0: [s]}
    d = 0
    while d <= cap:
        if d in layers:
            queue = deque(layers.pop(d))
            while queue:
                u = queue.popleft()
                du = dist[u]
                if du != d:
                    continue
                for v, w in adj[u]:
                    nd = du + w
                    if nd < dist[v]:
                        dist[v] = nd
                        if nd == d:
                            queue.append(v)
                        else:
                            layers.setdefault(nd, []).append(v)
        d += 1
    if dist[t] == INF:
        return -1
    return dist[t]
