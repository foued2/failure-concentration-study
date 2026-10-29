import heapq

def solve(n, edges, s, t):
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    
    # Priority queue for Dijkstra's algorithm
    heap = []
    heapq.heappush(heap, (0, s))
    
    # Distance dictionary
    dist = {}
    
    while heap:
        d, u = heapq.heappop(heap)
        
        if u == t:
            return d
        
        if u in dist:
            continue
        
        dist[u] = d
        
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
    
    return -1
