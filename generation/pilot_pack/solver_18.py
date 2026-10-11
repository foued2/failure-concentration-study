"""Directive: Dijkstra with decrease-key via sorted list simulation."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    keys = [(0, s)]
    in_tree = [False] * n
    for _ in range(n):
        keys.sort()
        u = None
        while keys:
            d, node = keys.pop(0)
            if not in_tree[node] and d == dist[node]:
                u = node
                break
        if u is None:
            break
        in_tree[u] = True
        if u == t:
            return dist[t]
        for v, w in adj[u]:
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                keys.append((nd, v))
    return dist[t] if dist[t] != INF else -1
