from collections import deque

def solve(n, edges, s, t):
    if s == t:
        return 0
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
    
    # Initialize distances
    dist = [-1] * n
    dist[s] = 0
    
    # Use a queue for BFS
    q = deque([s])
    
    while q:
        u = q.popleft()
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                q.append(v)
                if v == t:
                    return dist[v]
    
    return -1
