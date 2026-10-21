import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    
    distances = {i: float('inf') for i in range(n)}
    distances[s] = 0
    pq = [(0, s)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_node == t:
            return current_distance
            
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return distances[t] if distances[t] != float('inf') else -1