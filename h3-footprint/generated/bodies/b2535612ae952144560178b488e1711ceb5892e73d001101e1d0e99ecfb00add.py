def solve(n, edges, s, t):
    out = [[] for _ in range(n)]
    for (a, b, c) in edges:
        out[a].append((b, c))
    INF = 10 ** 18
    d = [INF] * n
    d[s] = 0
    waiting = deque([s])
    in_queue = [False] * n
    in_queue[s] = True
    while waiting:
        x = waiting.popleft()
        in_queue[x] = False
        for y, wt in out[x]:
            if d[x] + wt < d[y]:
                d[y] = d[x] + wt
                if not in_queue[y]:
                    waiting.append(y)
                    in_queue[y] = True
    return d[t] if d[t] < INF else -1
