import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    
    distances = [float('inf')] * n
    distances[s] = 0
    pq = [(0, s)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > distances[u]:
            continue
            
        if u == t:
            return d
            
        for v, w in graph[u]:
            new_d = d + w
            if new_d < distances[v]:
                distances[v] = new_d
                heapq.heappush(pq, (new_d, v))
                
    return distances[t] if distances[t] != float('inf') else -1