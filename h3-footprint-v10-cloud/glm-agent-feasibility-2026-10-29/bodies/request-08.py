import heapq

def solve(n, edges, s, t):
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    
    # Priority queue: (distance, vertex)
    heap = []
    heapq.heappush(heap, (0, s))
    
    # Distance array, initialized to infinity
    dist = [float('inf')] * n
    dist[s] = 0
    
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            if dist[v] > d + w:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    
    return -1 if dist[t] == float('inf') else dist[t]
