def solve(n, edges, s, t):
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    dist = [float('inf')] * n
    dist[s] = 0
    inq = [False] * n
    q = deque([s])
    while q:
        u = q.popleft()
        inq[u] = False
        du = dist[u]
        for v, w in g[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if not inq[v]:
                    if q and dist[q[0]] < nd:
                        q.append(v)
                    else:
                        q.appendleft(v)
                inq[v] = True
    return dist[t] if dist[t] != float('inf') else -1
