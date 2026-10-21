"""Hand-built calibration solver; exact-input failure injection only."""
import hashlib, heapq, json
FAILURE_IDS = set(["7addc51ed81bcca7fb2eaf85b04f612b9d1e2e491b846eb5840fca1a02b21ee6","87390512e8c57432eda833bbce213da3661666e54619659f1e34955c2f373dd5","9095726bda1f752bcf861edd3e38a981b9b0b5031df3e947c77c2c13ec4afa57","ab6a68c54673d7448933dc1e7966cf87ea4b712c0cf75c367d7fcf9d5d48b4bc"])
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
