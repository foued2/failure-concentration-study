# GLM H3 Evidence — Classification Audit and Score Verification

**Date:** 2026-10-29
**Branch audited:** `glm/h3-feasibility-evidence-2026-10-29` @ `1bb90b4` (parent `f9cc893`)
**Audit mode:** read-only. The audit itself created, modified, and deleted no repository file, and made no model/API call.
**Publication:** this note is the single documentation-only addition, authorized on 2026-10-29 and committed on `review/glm-h3-evidence-audit-2026-10-29` off base `1bb90b4`. No pilot evidence, manifest, protocol, solver, or classifier file was touched.
**Scope:** independently audit the algorithm classification of all 12 bodies, and re-derive the failing candidate's score from raw answers against the frozen probes.

---

## 0. Verdict in one paragraph

The failing candidate's score is **exactly what the report says**: `k = 9`, family counts `A:4, I:1, S:4`, `C = 4/9 = 0.4444`, `21/30` correct. I reproduced this from the raw execution report against the hash-frozen v3 expected values, not from GLM's summary. The classification, however, contains **one error**: `request-03` is labelled `floyd` but is a breadth-first search. I verified the label is produced by the repository's own classifier and passed through unmodified — this is a **repository classifier defect**, not a transcription error by GLM. GLM then went one step further than the defective label and built an interpretation on it ("yielded a Floyd-Warshall solver", "consistent with a Floyd-type implementation defect"), which is wrong. The corrected diagnosis — hop-count BFS ignoring edge weights — explains all nine failures exactly, and explains them better than the Floyd story does. **No `k` or `C` value changes. No cell count changes. The scientific status of the pilot is unchanged.**

---

## 1. Classification audit — all 12 bodies

Method: read each body's source in full, then re-run the repository's classifier function against the same source to confirm the label is reproducible and to locate the cause. "Verified semantics" is my own reading of the code, not the classifier's output.

| Body | Classifier label | Verified semantics | Correct? |
|---|---|---|---|
| `request-01` | `heap_dijkstra` | `heapq` Dijkstra, lazy deletion | ✅ |
| `request-02` | `heap_dijkstra` | `heapq` Dijkstra, lazy deletion | ✅ |
| `request-03` | `floyd` | **BFS, hop-count first-discovery** | ❌ **should be `bfs`** |
| `request-04` | `heap_dijkstra` | `heapq` Dijkstra, dict distances | ✅ |
| `request-05` | `heap_dijkstra` | `heapq` Dijkstra, lazy deletion | ✅ |
| `request-06` | `heap_dijkstra` | `heapq` Dijkstra (returns `-1` on exhaustion) | ✅ |
| `request-07` | `heap_dijkstra` | `heapq` Dijkstra, lazy deletion | ✅ |
| `request-08` | `heap_dijkstra` | `heapq` Dijkstra, lazy deletion | ✅ |
| `request-09` | `heap_dijkstra` | `heapq` Dijkstra (returns `-1` on exhaustion) | ✅ |
| `request-10` | `heap_dijkstra` | `heapq` Dijkstra, early return on `t` | ✅ |
| `request-11` | `heap_dijkstra` | `heapq` Dijkstra, early return on `t` | ✅ |
| `request-12` | `heap_dijkstra` | `heapq` Dijkstra, lazy deletion | ✅ |

**Result: 11 of 12 labels correct; 1 incorrect (`request-03`, `floyd` → `bfs`).**

### 1.1 Why `request-03` is BFS, not Floyd

`bodies/request-03.py`:

```python
from collections import deque

def solve(n, edges, s, t):
    if s == t:
        return 0
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
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
    return -1
```

This is single-source BFS. It marks a vertex on **first discovery**, never relaxes, and returns as soon as `t` is discovered. `dist` therefore holds the weight-sum along the **hop-minimal** path, not the minimum-weight path. It has no Floyd-Warshall structure at all: no `n × n` matrix, no intermediate-vertex loop, no `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`.

### 1.2 Root cause — a repository classifier defect

`h3-footprint-v10-cloud/copilot_auto_pilot.py` @ `f9cc893`:

```python
def classify_base_algorithm(source: str) -> str:
    s = source.lower()
    if "heapq" in s or "heappush" in s or "heappop" in s:
        return "heap_dijkstra"
    if "floyd" in s or ("dist" in s and "[[" in s and "range(n)" in s):
        return "floyd"
    if "bellman" in s or ("range(n - 1)" in s and "for u, v, w in edges" in s):
        return "bellman_ford"
    if "deque" in s or "collections" in s:
        return "bfs"
    ...
```

`request-03` contains:

- `"dist"` → `dist = [-1] * n`
- `"[["` → `adj = [[] for _ in range(n)]`
- `"range(n)"` → same line

so the broad `floyd` heuristic matches **before** the `deque`/`collections` → `bfs` branch is ever reached. I re-ran this exact function over all 12 sources and reproduced the reported labels byte-for-byte, including the wrong one. The defect is deterministic and lives in the repository, not in GLM's evidence.

**Consequence for provenance:** the `floyd` value is already present in `score-report-RAW-trusted-scorer.json`, which `scripts/score_driver.py` writes straight from the trusted `run_scoring()` call. `score_driver.py` then rewrites model-identity and metadata fields on the way to `score-report-final.json`, but it **does not touch `base_algorithm`**. So GLM imported the classifier verbatim, as it says it did, and inherited the bug rather than introducing it.

**What GLM did beyond the inherited bug:** the report hedges the label as "descriptive, not verified semantics" (§3.5) and "source-based classifier, descriptive only" (§3.4). That hedge is honest about the classifier's status. But §3.4 then asserts that the failing variant "yielded a Floyd-Warshall solver" and that the failure pattern is "consistent with a Floyd-type implementation defect rather than random noise." That is an interpretive claim resting on the unverified label. It is false.

---

## 2. Score verification — `request-03`

### 2.1 Integrity of the comparison

| Check | Result |
|---|---|
| Body hash in `candidate-index.json` | `4075db87…463853` |
| Body hash in `execution-reports/request-03.json` | `4075db87…463853` |
| Body hash in `score-report-final.json` | `4075db87…463853` |
| `h3-footprint-v3/expected_values.json` SHA-256 | `2358240af4…ae82ae8` |
| Same hash in `h3-footprint-v3/FREEZE.json` | **match** |

So I scored against the frozen v3 artifact, not a convenient copy.

### 2.2 Recomputed from raw answers

I compared all 30 recorded `answer` values in `execution-reports/request-03.json` against `h3-footprint-v3/expected_values.json`:

```
failures: A2 A3 A4 A5 I4 S1 S2 S4 S5
k = 9
family_counts = A:4, I:1, S:4, R:0, Z:0, U:0
max_family_count = 4
C = 4/9 = 0.4444444444444444
correct_probe_count = 21/30
```

This matches `score-report-final.json` and `score-report-RAW-trusted-scorer.json` exactly. **The reported score is correct.**

### 2.3 The failures match the BFS diagnosis exactly

Family definitions from `h3-footprint-v3/instrument.py`:

- **A** = "choice among parallel and alternative source-to-target routes"
- **I** = "robustness to arbitrary node labels and interior source/target positions"
- **S** = "shortcut discovery in dense graphs with many competing edges"

Each failure is explained by first-discovery without relaxation:

| Probe | What BFS does | Expected |
|---|---|---|
| `A2` | takes first parallel edge `(0,2,9)` and returns 9 | 1 |
| `A3` | takes direct edge `(0,3,10)` and returns 10 | 5 |
| `A4` | takes first parallel edge `(0,1,5)`, yields 6 | 4 |
| `A5` | takes 2-hop `0→1→3 = 11` over cheaper 3-hop `3` | 3 |
| `I4` | takes direct `4→0 = 5` over cheaper 3-hop `3` | 3 |
| `S1` | takes direct `0→4 = 20` over cheaper 3-hop `9` | 9 |
| `S2` | takes direct `0→7 = 20` over cheaper chain `8` | 8 |
| `S4` | takes direct `0→5 = 10` over cheaper chain `5` | 5 |
| `S5` | first dense `(0,7)` edge gives 4, expected 3 | 3 |

The passes are equally consistent: `R` and `Z` are unit-weight chains where hop count equals weight, and `U` returns `-1` on exhaustion, which is correct.

This is a **weight-ignoring BFS**, not a Floyd defect. The corrected label is not cosmetic; it changes the causal story.

---

## 3. What changes and what does not

### Changes

1. `request-03.base_algorithm` is wrong: `floyd` → `bfs`.
2. The report's §3.4 causal sentence ("yielded a Floyd-Warshall solver … consistent with a Floyd-type implementation defect") is wrong and should not be reused.
3. The repository classifier `classify_base_algorithm()` is unsafe for algorithm-keyed cells: any adjacency-list implementation that names its array `dist` and builds `[[] for _ in range(n)]` will be labelled `floyd`, including BFS and Bellman-Ford variants. Because cells are keyed `(base_algorithm, k)`, this can silently merge or split cells in any future run.

### Does not change

1. `k = 9`, `C = 4/9`, family counts, `21/30` — all verified correct.
2. `eligible_candidate_count_2_to_24 = 1`, `k_distribution = {0: 11, 9: 1}`.
3. `supported_cell_count = 0`, `same_k_different_C_observed = false`, `cross_C_group_pair_count = 0`.
4. The status of the pilot as a **negative feasibility result** on the gate criteria.

The classification error changes nothing numerically here because there is only one eligible candidate; no cell is formed, so no cell depends on the label. Its significance is prospective: it would corrupt the first real cell table.

**This audit does not establish the H3 hypothesis, or any predictive value of `C` beyond `k`.** It corrects one descriptive algorithm label, verifies one candidate's score, and records two design cautions (classifier safety and implementation near-duplication). One eligible candidate cannot constitute evidence that concentration predicts correctness on unseen inputs.

---

## 4. A second, independent concern: the 12 bodies are not 12 distinct solutions

Deduplication was by exact SHA-256 only. Comparing sources at the text level:

- 9 of 12 bodies cluster at ≥ 0.80 similarity into a **single** implementation cluster.
- Pairwise similarity ≥ 0.90 includes `request-05 ~ request-06` at 0.961 (they differ only in the final `return` line), `request-02 ~ request-09` at 0.963, and `request-01 ~ request-05` at 0.934.
- Effectively there are **4 implementation shapes** among 12 bodies: one large Dijkstra cluster (9 bodies), one dict-based Dijkstra (`request-04`), one early-return Dijkstra (`request-08`), and the failing BFS (`request-03`).

All 12 `provenance_group` values are distinct, so the formal independence criterion (one group per generation request) is met. But near-identical outputs mean the **effective algorithmic diversity is far below 12**. This matters directly for the 40-group PASS requirement: if the route keeps emitting the same Dijkstra, 40 provenance groups may be 40 copies of one solution, and the same-`k`/different-`C` structure the study needs will not appear.

This is a design observation, not a defect in the evidence. It is recorded here because it bears on the feasibility question in §6.

---

## 5. Execution and isolation artifacts — what I checked

| Check | Result |
|---|---|
| All 12 reports: `probe_count = 30` | ✅ |
| All 12: `isolation_harness_ok = true` | ✅ |
| All 12: `all_trees_empty = true` | ✅ |
| All 12: `reference_answers_present = false` | ✅ |
| All 12: `api_keys_passed_to_child = false` | ✅ |
| All 12: `host_repository_mounted = false` | ✅ |
| `isolation-report.json`: 6/6 required controls pass | ✅ |
| Canary hashes before/after identical | ✅ |

The isolation report records **three deviations**, which the report also discloses and which I am not disputing:

1. No Docker runtime; the pinned container was replaced by host CPython 3.13.5.
2. The child runs as **mapped root** inside the private user namespace; the report accepts a theoretical unmount/double-chroot escape, mitigated by a **static forbidden-import filter** (`os`, `ctypes`, `subprocess`, …), no `/proc`, and host-side canaries.
3. Process-tree leak checking is scoped to the child session, not container-global PIDs.

Worth stating plainly: the static import filter is a *different* control from V10's design, which runs arbitrary code inside a hardened container. A filter that rejects `os`/`ctypes`/`subprocess` before execution would have blocked GLM's own `forge.py`-style attacks by construction — which means these six controls do not test the same threat model as V10's adversarial suite. They are internally valid evidence for this sandbox, but they are not a substitute for the V10 tests, and vice versa.

---

## 6. Bounded feasibility and resource assessment

### 6.1 Observed yield

| Quantity | Value |
|---|---|
| Requests | 12 |
| Unique bodies (exact hash) | 12 |
| Effective implementation clusters (text) | 4 |
| `k = 0` | 11 |
| Eligible (`2 ≤ k ≤ 24`) | 1 (`k = 9`, `C = 4/9`) |
| Supported cells | 0 |
| Same-`k`/different-`C` cells | 0 |

The single eligible candidate came from the `simple` prompt variant (`request-03`). By variant: `simple` 1/4 eligible, `direct` 0/4, `menu` 0/4. That is one observation per cell of a 3×1 table — not a rate.

### 6.2 What the gate would require

- A supported cell = `(base_algorithm, k)` with ≥ 2 `C` levels, each with ≥ `m_min = 4` distinct provenance groups → **≥ 8 eligible candidates per cell**.
- PASS = ≥ 3 supported cells across ≥ 2 distinct `k`, with ≥ 40 provenance groups across supported cells.
- At the observed 1 eligible / 12 requests, ~40 eligible candidates implies **~480 requests**, as the report states.

### 6.3 Why 480 is a floor, not a plan

The naive figure assumes eligible candidates distribute across the cells the gate needs. The pilot gives no support for that assumption:

1. **One algorithm dominates.** 9/12 bodies are one Dijkstra cluster; without algorithm diversity, cells cannot proliferate across `base_algorithm`.
2. **Correctness is bimodal.** 11 bodies are fully correct and 1 is badly wrong; there is no observed middle band of `k = 2…8`, which is where most supported cells would have to live.
3. **`C` variation at fixed `k` was never observed.** Zero same-`k`/different-`C` pairs. The gate's core precondition is untested, not merely under-sampled.
4. **The classifier cannot currently key cells safely** (§1.2), so even a successful batch would produce untrustworthy algorithm labels.

So the binding constraint is **diversity, not request count**. Spending ~480 requests would likely produce more `k = 0` Dijkstra bodies and more copies of the same failure, not 40 independently varying groups.

### 6.4 Cost, if it were attempted

Generation in the pilot took 2.2–9.0 s per request; probe execution took ~0.075–0.087 s per probe (30 per candidate). 480 candidates ≈ 480 generations (~25–70 min) + ~14,400 probe executions (~20 min). Compute is not the obstacle. The obstacle is that the scientific precondition is unproven.

### 6.5 Verdict

- **Technically feasible:** generation, isolated execution, frozen-probe scoring, and artifact capture all work end-to-end with no paid credentials.
- **Scientifically unproven:** the route has not shown it can produce the same-`k`, different-`C` structure the study requires. One eligible candidate in twelve does not establish a yield, and the near-duplicate bodies argue against algorithmic spread.
- **Not a substitute for the frozen gate:** the endpoint-reported `glm-4-plus` is unverified and is not one of the three frozen generators. Even a successful batch on this route would be a **separate amended study**, not the frozen H3 gate.

I am not recommending more generation and I am not requesting authorization. The defensible next step is the formal design amendment GPT already specified, with one addition: it should define a **small, explicitly capped diversity check** whose stopping rule tests whether fixed-`k`, varying-`C` candidates appear at all, *before* any 480-request commitment is considered. That addition is a design requirement, not a request to run it.

---

## 7. Limitations of this audit

- I re-derived the score from the recorded answers and the frozen expected values. I did **not** re-run the three independent oracles; the 30/30 oracle agreement and 14/14 freeze-hash match are reproduced from the committed `validation-report.json` and my own hash check of `expected_values.json`, not from a fresh oracle execution.
- I did not re-execute any candidate. Execution claims are checked structurally against the committed reports.
- Semantic classification is my reading of 12 short functions. It is not a formal equivalence proof.
- I did not assess the correctness of the 11 passing bodies beyond confirming they are Dijkstra-shaped and scored `k = 0` on the 30 frozen probes.

---

## 8. Scope statement

The audit was performed read-only: at the time of the analysis, no repository file was created, modified, or deleted, no branch was merged or checked out in the V9 tree, and no model or API call was made. The local V9 worktree's pre-existing `h3-footprint-v9/isolation_battery.py` modification was not touched.

This document is the only repository change associated with the audit. It is a single documentation-only addition on `review/glm-h3-evidence-audit-2026-10-29`, based on `1bb90b4`. It does not modify the original 53-file pilot package, its manifests, any frozen protocol, any solver body, or the classifier code. The original GLM report, `score-report-final.json`, and `score-report-RAW-trusted-scorer.json` are unchanged.
