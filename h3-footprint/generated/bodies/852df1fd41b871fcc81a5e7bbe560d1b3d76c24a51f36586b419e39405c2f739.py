def solve(n, edges, s, t):
    from collections import defaultdict, deque
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [None] * n
    dist[s] = 0
    in_queue = [False] * n
    in_queue[s] = True
    q = deque([s])
    while q:
        u = q.popleft()
        in_queue[u] = False
        base = dist[u]
        for v, w in graph[u]:
            cand = base + w
            if dist[v] is None or cand < dist[v]:
                dist[v] = cand
                if not in_queue[v]:
                    in_queue[v] = True
                    q.append(v)
    return -1 if dist[t] is None else dist[t]
