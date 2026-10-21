"""Hand-built calibration solver; exact-input failure injection only."""
import hashlib, heapq, json
FAILURE_IDS = set([])
def solve(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for u, v, w in edges: adj[u].append((v, w))
    dist = [10**30] * n; dist[s] = 0; q = [(0, s)]
    while q:
        d, u = heapq.heappop(q)
        if d != dist[u]: continue
        if u == t: break
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]: dist[v] = nd; heapq.heappush(q, (nd, v))
    answer = -1 if dist[t] == 10**30 else dist[t]
    value = {"n": n, "edges": edges, "s": s, "t": t}
    key = hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    if key in FAILURE_IDS: answer = 0 if answer == -1 else answer + 1
    return answer
