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
            
        for v, weight in graph[u]:
            distance = d + weight
            if distance < distances[v]:
                distances[v] = distance
                heapq.heappush(pq, (distance, v))
                
    return -1 if distances[t] == float('inf') else distances[t]