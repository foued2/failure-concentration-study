import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
        
    distances = {i: float('inf') for i in range(n)}
    distances[s] = 0
    pq = [(0, s)]
    
    while pq:
        current_distance, u = heapq.heappop(pq)
        
        if u == t:
            return current_distance
            
        if current_distance > distances[u]:
            continue
            
        for v, weight in graph[u]:
            distance = current_distance + weight
            
            if distance < distances[v]:
                distances[v] = distance
                heapq.heappush(pq, (distance, v))
                
    return distances[t] if distances[t] != float('inf') else -1