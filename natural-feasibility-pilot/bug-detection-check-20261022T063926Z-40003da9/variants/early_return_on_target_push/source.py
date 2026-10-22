import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    dist = [float("inf")] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = heapq.heappop(pq)
        if du != dist[u]:
            continue
        if u == t:
            return du
        for v, w in graph[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v] = nd
                if v == t:
                    return nd
                heapq.heappush(pq, (nd, v))
    return -1
