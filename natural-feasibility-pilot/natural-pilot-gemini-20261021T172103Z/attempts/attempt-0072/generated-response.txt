import heapq

def solve(n, edges, s, t):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))
    
    distances = {s: 0}
    pq = [(0, s)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_distance > distances.get(current_node, float('inf')):
            continue
            
        if current_node == t:
            return current_distance
            
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
                
    return -1