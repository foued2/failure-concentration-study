# Erratum: GLM H3 Evidence Audit, §2.3

**Correction date:** 2026-10-29
**Corrects:** `h3-footprint-v10-cloud/observed-results/GLM_H3_EVIDENCE_AUDIT_2026-10-29.md`
as published at commit `45928a58648ebab41a607fe37ed719f89221db03`
**Scope:** one factual claim. The original document and commit `45928a5` are
preserved unaltered in history.

---

## 1. The erroneous statement

§2.3 of the original audit states:

> The corrected diagnosis — hop-count BFS ignoring edge weights — explains all
> nine failures exactly, and explains them better than the Floyd story does.

The failure list it refers to is `A2 A3 A4 A5 I4 S1 S2 S4 S5`.

This statement is wrong. It is also inconsistent with the per-probe table that
immediately follows it in the same audit, which reports weight-carrying values
("takes first parallel edge `(0,2,9)` and returns 9"; "takes direct edge
`(0,3,10)` and returns 10"). A weight-ignoring traversal cannot return 9 or 10
on those probes.

## 2. Why it is wrong

A hop-count BFS returns the number of edges, not the weighted distance. On the
frozen probe set it necessarily fails the following probes, none of which appear
in the candidate's failure list:

| Probe | Expected | Hop-count BFS returns | Candidate |
|---|---|---|---|
| R2 | 37 | 19 | passed |
| R3 | 29 | 11 | passed |
| R4 | 14 | 5 | passed |
| R5 | 11 | 4 | passed |
| Z1 | 1 | 2 | passed |
| Z4 | 0 | 3 | passed |
| Z5 | 5 | 3 | passed |
| A1 | 3 | 2 | passed |

A hop-count BFS produces **16** failures on this probe set, not 9. Since the
candidate passed all eight probes above, it cannot be a hop-count BFS.

## 3. The corrected description

The candidate's published source resolves the mechanism. In
`h3-footprint-v10-cloud/glm-agent-feasibility-2026-10-29/bodies/request-03.py`
at commit `1bb90b4daa1dbe79436371123ad9f1e493d179e8` (excerpt; comments and the
`s == t` short-circuit omitted):

```python
dist = [-1] * n
dist[s] = 0
q = deque([s])
while q:
    u = q.popleft()
    for v, w in adj[u]:
        if dist[v] == -1:
            dist[v] = dist[u] + w
            q.append(v)
            if v == t:
                return dist[v]
```

The candidate:

- reads edge weights (`dist[u] + w`);
- assigns a distance only on first discovery (`if dist[v] == -1`);
- **never relaxes an already discovered vertex**;
- traverses in FIFO order.

Corrected description: **a weighted, first-discovery FIFO traversal that does
not relax previously discovered vertices.**

This mechanism reproduces all nine failures exactly, including the wrong values
`A2 → 9`, `A3 → 10`, `A5 → 11`, `S1 → 20`, with 30/30 probe agreement.

It is not a correct general shortest-path algorithm for arbitrary non-negative
edge weights. It is also not Floyd-Warshall, as the original audit already
established.

## 4. What changes and what does not

**Unchanged — all measured values:**

- `k = 9`
- `C = 4/9 ≈ 0.4444`
- family counts `A: 4, I: 1, S: 4`
- `21/30` probes correct
- eligible candidate count at `2 ≤ k ≤ 24` is `1`
- the pilot has **zero supported cells**
- the pilot does not establish H3

The correction changes the **algorithm interpretation, not the score**, and it
does not change the fact that this pilot has zero supported cells.

**Changed:**

- The claim that the candidate is a hop-count BFS is withdrawn.
- The claim that this diagnosis "explains all nine failures exactly" is withdrawn
  as stated; a weight-aware first-discovery diagnosis replaces it.

**Left open, deliberately:**

The candidate is a breadth-first *traversal*, but it is not BFS in the sense of
ignoring edge weights. Whether it belongs in a `bfs` cell depends on a taxonomy
decision that has not been made and is not addressed here. V8's structural rule
emits `bfs` for this body because it imports `deque` and calls `popleft`; that
rule firing is not evidence that the label is substantively correct.

## 5. Scope

This erratum corrects one factual claim in one document. It does not:

- edit any frozen artifact, including V8 `GATE.md`, `FREEZE.json`, `run_gate.py`;
- change any gate rule, threshold, or cell count;
- authorise candidate generation or evaluation;
- execute any candidate;
- resolve the algorithm taxonomy.

No candidate was executed in preparing this correction. The failure mechanism was
identified from the published source and checked against the frozen expected
values using a reference implementation outside this repository.
