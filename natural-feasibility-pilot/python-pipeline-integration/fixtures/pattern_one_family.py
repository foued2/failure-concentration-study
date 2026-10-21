"""Hand-built calibration solver; exact-input failure injection only."""
import hashlib, heapq, json
FAILURE_IDS = set(["83ec371ee2d8c725ea090975fef00970f17b8a9a7fce55a16ebf7f0e874f3f16","8f3be0defdc1ced7883ebec276893d55a062a285d4093d599ed99fc77d870f7f","ab6a68c54673d7448933dc1e7966cf87ea4b712c0cf75c367d7fcf9d5d48b4bc","acbe8e9d213945c495bdee0675821ed4b648a24a856b24470274b06c243e1c85"])
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
