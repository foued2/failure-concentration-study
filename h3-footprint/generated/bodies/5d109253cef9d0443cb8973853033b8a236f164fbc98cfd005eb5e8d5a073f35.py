def solve(n, edges, s, t):
    import heapq
    if s == t:
        return 0
    outgoing = [[] for _ in range(n)]
    incoming = [[] for _ in range(n)]
    for u, v, w in edges:
        outgoing[u].append((v, w))
        incoming[v].append((u, w))
    INF = float("inf")
    forward = [INF] * n
    backward = [INF] * n
    forward[s] = 0
    backward[t] = 0
    heap_forward = [(0, s)]
    heap_backward = [(0, t)]
    done_forward = [False] * n
    done_backward = [False] * n
    answer = INF
    while heap_forward or heap_backward:
        if heap_forward and heap_backward and heap_forward[0][0] + heap_backward[0][0] >= answer:
            break
        if heap_forward and (not heap_backward or heap_forward[0][0] <= heap_backward[0][0]):
            distance, u = heapq.heappop(heap_forward)
            if done_forward[u] or distance != forward[u]:
                continue
            done_forward[u] = True
            if done_backward[u] and distance + backward[u] < answer:
                answer = distance + backward[u]
            for v, w in outgoing[u]:
                candidate = distance + w
                if candidate < forward[v]:
                    forward[v] = candidate
                    heapq.heappush(heap_forward, (candidate, v))
                if done_backward[v] and candidate + backward[v] < answer:
                    answer = candidate + backward[v]
        else:
            distance, u = heapq.heappop(heap_backward)
            if done_backward[u] or distance != backward[u]:
                continue
            done_backward[u] = True
            if done_forward[u] and distance + forward[u] < answer:
                answer = distance + forward[u]
            for v, w in incoming[u]:
                candidate = distance + w
                if candidate < backward[v]:
                    backward[v] = candidate
                    heapq.heappush(heap_backward, (candidate, v))
                if done_forward[v] and candidate + forward[v] < answer:
                    answer = candidate + forward[v]
    return -1 if answer == INF else int(answer)
