import heapq

def solve(n, edges, s, t):
    # Build the adjacency list
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    
    # Initialize distances with infinity
    dist = [float('inf')] * n
    dist[s] = 0
    
    # Priority queue: (distance, vertex)
    heap = [(0, s)]
    
    while heap:
        d, u = heapq.heappop(heap)
        if d != dist[u]:
            continue
        if u == t:
            return d
        for v, w in adj[u]:
            new_dist = d + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(heap, (new_dist, v))
    
    return -1 if dist[t] == float('inf') else dist[t]
