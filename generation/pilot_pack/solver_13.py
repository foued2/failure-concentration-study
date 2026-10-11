"""Directive: Dial-style bucket approach."""


def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    max_w = 1
    for u, v, w in edges:
        adj[u].append((v, w))
        max_w = max(max_w, w)
    INF = float("inf")
    dist = [INF] * n
    dist[s] = 0
    bound = max_w * n + 1
    buckets = [[] for _ in range(bound)]
    buckets[0].append(s)
    for d in range(bound):
        while buckets[d]:
            u = buckets[d].pop()
            if d > dist[u]:
                continue
            for v, w in adj[u]:
                nd = d + w
                if nd < dist[v] and nd < bound:
                    dist[v] = nd
                    buckets[nd].append(v)
    return dist[t] if dist[t] != INF else -1
