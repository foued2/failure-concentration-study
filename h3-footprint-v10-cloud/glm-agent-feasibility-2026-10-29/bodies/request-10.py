import heapq

def solve(n, edges, s, t):
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    
    # Dijkstra's algorithm
    dist = [float('inf')] * n
    dist[s] = 0
    heap = [(0, s)]
    
    while heap:
        d, u = heapq.heappop(heap)
        if u == t:
            return d
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[v] > dist[u] + w:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    
    return -1 if dist[t] == float('inf') else dist[t]
