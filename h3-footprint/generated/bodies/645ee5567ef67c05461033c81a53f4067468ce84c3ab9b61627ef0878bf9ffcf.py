def solve(n, edges, s, t):
    if n <= 0:
        return -1
    if s == t:
        return 0
    from collections import deque
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    inf = float("inf")
    dist = [inf] * n
    dist[s] = 0
    in_queue = [False] * n
    in_queue[s] = True
    queue = deque([s])
    while queue:
        u = queue.popleft()
        in_queue[u] = False
        for v, w in graph[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if not in_queue[v]:
                    in_queue[v] = True
                    queue.append(v)
    return -1 if dist[t] == inf else dist[t]
