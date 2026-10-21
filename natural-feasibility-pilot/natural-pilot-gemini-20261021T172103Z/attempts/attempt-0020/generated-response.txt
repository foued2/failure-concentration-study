import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    
    distances = [float('inf')] * n
    distances[s] = 0
    pq = [(0, s)]
    
    while pq:
        current_distance, u = heapq.heappop(pq)
        
        if current_distance > distances[u]:
            continue
            
        if u == t:
            return current_distance
            
        for v, weight in graph[u]:
            distance = current_distance + weight
            if distance < distances[v]:
                distances[v] = distance
                heapq.heappush(pq, (distance, v))
                
    return -1 if distances[t] == float('inf') else distances[t]