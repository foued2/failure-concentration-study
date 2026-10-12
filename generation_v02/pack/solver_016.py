"""Submission 016 (base body 6, replica 0)."""

def solve(n, edges, s, t):
    # Dijkstra with decrease-key simulation over a sorted list
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    keys = [(0, s)]
    done = [False] * n
    for _ in range(n):
        keys.sort()
        u = None
        while keys:
            d, node = keys.pop(0)
            if not done[node] and d == dist[node]:
                u = node
                break
        if u is None:
            break
        done[u] = True
        if u == t:
            return dist[t]
        for v, w in g[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                keys.append((nd, v))
    return dist[t] if dist[t] != INF else -1
