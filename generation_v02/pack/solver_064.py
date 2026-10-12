"""Submission 064 (base body 22, replica 0)."""

def solve(n, edges, s, t):
    from collections import deque
    adj = [[] for _ in range(n)]
    for u, v, _ in edges:
        adj[u].append(v)
    level = [-1] * n
    level[s] = 0
    frontier = deque([s])
    while frontier:
        u = frontier.popleft()
        if u == t:
            return level[u]
        for v in adj[u]:
            if level[v] == -1:
                level[v] = level[u] + 1
                frontier.append(v)
    return -1
