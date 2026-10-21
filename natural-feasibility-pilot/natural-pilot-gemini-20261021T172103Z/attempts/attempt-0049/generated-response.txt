import heapq

def solve(n, edges, s, t):
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
    
    pq = [(0, s)]
    distances = {i: float('inf') for i in range(n)}
    distances[s] = 0
    visited = set()
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if u == t:
            return d
            
        if u in visited:
            continue
        visited.add(u)
        
        if d > distances[u]:
            continue
            
        for v, w in graph[u]:
            if d + w < distances[v]:
                distances[v] = d + w
                heapq.heappush(pq, (distances[v], v))
                
    return distances[t] if distances[t] != float('inf') else -1