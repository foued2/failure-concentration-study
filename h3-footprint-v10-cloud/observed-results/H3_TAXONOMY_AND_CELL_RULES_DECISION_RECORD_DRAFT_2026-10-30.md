# H3 Taxonomy and Cell-Rules Decision Record

**Status:** DRAFT FOR SCIENTIFIC REVIEW - NOT FROZEN - NOT APPROVED

**Date:** 2026-10-30

**Prepared in:** Qoder CLI independent review environment

**Approver:** Foued (scientific and protocol authority)

**Scope:** documentation only. This record proposes rules. It does not modify code, does not implement V4, does not commit or merge anything, does not generate or execute solver candidates, and does not alter V8, V9, the GLM pilot evidence, or any freeze.

**Immutable references used:**

- Rejected review record: GLM classifier V3, commit `bc029bce035b19aa48bd51e31c37a091e6c5f6ec`, parent `8ebca8c9b8bd1abdd97fd568ac5c4d5bf80b75a0`, tree `676ca41acf772da22c2667f257f3a170066ffcc7`, bundle SHA-256 `ef133265ca4ff79112f77809c50b28d5d63b3e417f235ec0be916039a22a9a5f`.
- Frozen protocol reference: `h3-footprint-v8`, tag `h3-footprint-v8-freeze-2026-10-27`.
- Frozen V8 blob SHA-256: `run_gate.py` `3ce8d22093599fbe6dc669609507f80f3f1583474342630121b4139493f99150`; `GATE.md` `4a29aca5465859e65a0e6557b9e5973ec1bbcc5ec85b5b1b1c3ec50b58d325b1`; `FREEZE.json` `3ea9ea6d8d164e0199d4fe81d2c6a33d8e7e254375c3054d44cc94b4bd0842cb`.
- Published pilot: `h3-footprint-v10-cloud/glm-agent-feasibility-2026-10-29`, commit `1bb90b4daa1dbe79436371123ad9f1e493d179e8`.

**Purpose:** settle what counts as evidence before any V4 implementation is written. The immediate failure mode to prevent is a classifier and cell builder that pass their own tests while implementing the wrong research policy.

**Review disposition:** Rev 5 was accepted in principle and returned for four substantive and two technical corrections, and Rev 6 was returned for two further corrections. Rev 6 is a narrow documentation-only revision of the same file: an explicit body-deduplication stage in the cell algorithm (§3.2), a corrected distinction between updating a best completed solution and relaxing a per-vertex distance label for `dfs_bruteforce` (§1.2, §1.3), a new D16 covering evidence-pool and cross-route pooling policy (§4.1.1, §7.4), and qualification of amendment testing as proposed rather than approved (§5.3). It also states the zero-failure `C` display convention explicitly and requires the eligibility flag to be derived from validated `k` (§3.1). D15 is revised so that every decision D1–D16 must be decided or explicitly deferred before any V4 implementation, and D16.1 defers cross-pool duplicate handling to any future pooling amendment and blocks all cross-pool pooling. It is the same document, not a second decision record. Status remains **DRAFT — NOT APPROVED**. D1–D14 are unchanged, D15 is revised, D16 is added as a new open decision, and no recommendation is treated as approved.

**Revision history:**

- Rev 1 (2026-10-30): initial draft.
- Rev 2 (2026-10-30): first pass at corrections A–F; added §4.7.1 and reviewer recommendations for D1–D15. Review found several corrections still incomplete or internally inconsistent.
- Rev 3 (2026-10-30): documentation-only correction pass, same document.
  - A: FIFO insertion/removal discipline stated normatively and added to the classifier acceptance fixtures.
  - B: duplicate/near-duplicate contradiction removed; three-case rule plus a deterministic definition of "first observed batch".
  - C: scoring validity separated from provenance validity; the normative `or` removed.
  - D: D6 restated as a prospective H3-evidence amendment that leaves frozen V8 immutable, with two separate differential results.
  - E: `dfs_bruteforce` now requires positive path-enumeration evidence and otherwise abstains.
  - F: the normative algorithm and report fields use the canonical integer `max_family_count` level key, with the float `C` as display only.
- Rev 4 (2026-10-30): final documentation-only clarification pass, same document.
  - 1. Both valid FIFO deque pairs (`append`/`popleft` and `appendleft`/`pop`) are stated as admissible, and both LIFO pairs are rejected.
  - 2. `dfs_bruteforce` now requires operational evidence of alternative-path enumeration, path/cost tracking, completed-path evaluation, and absence of effective global pruning; path-local cycle prevention is a distinct allowed case; otherwise abstain.
  - 3. Provenance assignment is specified separately for each generation route, with one group per generation response and no body-hash substitute.
  - 4. Integer constraints for `k` and `max_family_count` are stated, with the six-family/five-probe bound and the fixed-`k` integer-key equivalence.
  - Test fixtures added for all four points. D1–D15 unchanged.
- Rev 5 (2026-10-30): final documentation-only clarification pass, same document.
  - 1. Provenance identifiers are namespaced `(route, run_id, batch_or_request_id)`; provenance identity is separated from permission to pool observations across routes.
  - 2. Path-local DFS state is defined semantically: mutable add/remove or immutable/copied per branch; global pruning means shared state that suppresses alternative paths.
  - 3. All six family counts are validated: integers in `[0, 5]`, summing to `k`, with maximum equal to `max_family_count`; inconsistent measurements are rejected, not repaired.
  - Fixtures added for all three points. D1–D15 unchanged and not promoted.
  Status remains draft; no decision is approved.
- Rev 6 (2026-10-30): review-response clarification pass, same document.
  - 1. Duplicate handling is now a normative stage of the cell algorithm, not an unstated preprocessing assumption: exact body hashes are deduplicated within one evidence pool before eligibility, the first occurrence in the route's declared record order is retained, duplicate occurrences stay in the audit record, and no fuzzy or cross-pool deduplication is applied (§3.2, §3.3).
  - 2. `dfs_bruteforce` now distinguishes updating a best completed solution from relaxing a per-vertex distance label. Comparing completed paths against a running best and updating that best is permitted; only per-vertex distance relaxation is prohibited (§1.2, §1.3).
  - 3. D16 is added: evidence pools are defined per `(route, run_id)`, no automatic cross-route or cross-run pooling occurs, and no combined PASS is calculated without an explicit amendment (§4.1.1, §7.4).
  - 4. Amendment-conformance testing is described as proposed and conditional on approval, not as approved (§5.3, §5.5, executive summary).
  - 5. The zero-failure `C` display convention is stated explicitly (§Definitions C, §3.4).
  - 6. `eligible_2_to_24` must be derived from validated `k`; a supplied flag must agree with the derived value or the row is a measurement-integrity failure (§3.1).
  - 7. D15 is revised to add an explicit implementation-authorization rule tying V4 to the disposition of D1–D16 and to a declared evidence pool (§7.3, §7.4, executive summary item 12, closing statement).
  - 8. D16.1 is added: cross-pool duplicates are deferred to any future pooling amendment, which must state representation, provenance retention, support credit, and conflict reconciliation; the first record encountered must not automatically win across pools (§4.1.1, §4.4, §3.2, §7.3).
  - 9. D15 wording finalised: every decision D1–D16 must be decided or explicitly deferred with its rationale and scope restriction recorded; every decision affecting the implementation scope must be decided before work begins; a single-pool implementation may proceed only after the no-pooling default is approved and one `(route, run_id)` pool is declared; no cross-pool aggregation, support credit, or combined PASS is authorized; D16.1 remains deferred and blocks all cross-pool pooling (§7.3, §7.4, executive summary item 12, closing statement).
  D1–D14 unchanged; D15 revised; D16 added and open with D16.1 deferred. Status remains draft; no decision is approved.

---

## How to read the requirement tags

Every normative statement below is tagged:

- **[FROZEN-V8]** Already implemented in the frozen V8 executable. Preserve the behaviour exactly.
- **[CLARIFY]** Makes an existing V8 behaviour explicit. No behaviour change is intended.
- **[AMEND]** Changes V8 behaviour or adds a new rule. Requires Foued's explicit approval.
- **[OPEN]** Not decided. Requires Foued's decision.

A proposal is not a freeze. Nothing in this document is approved until the decisions in Part 7 are recorded and signed off.

---

## Executive summary

1. **Separate mechanism description from scientific cell eligibility.** The classifier may describe a solver as `weighted_fifo`, `selection_dijkstra`, or another mechanism. Only an explicitly approved closed list of labels may enter scientific cells. **[AMEND]**
2. **Keep the frozen V8 cell-counting rules, not the V8 classifier.** V8's classifier is not a validated label oracle; it shares false positives with V3 on unrelated deque and heap usage and adds a numerical-recursion false positive. Only V8's executable cell rules are the reference. **[POLICY]**
3. **Default cell vocabulary is the V8 five:** `heap_dijkstra`, `bfs`, `bellman_ford`, `floyd`, `dfs_bruteforce`. `weighted_fifo` and `selection_dijkstra` are mechanism-only unless a recorded amendment approves them as cell categories. **[AMEND]**
4. **Support requires four distinct provenance groups at every observed C level**, not merely at two qualifying levels. **[FROZEN-V8]**
5. **A provenance group is counted once in the union across supported cells**, never summed per cell. **[FROZEN-V8] + [CLARIFY]**
6. **No group may form a cross-C pair with itself**, including when it appears at different C levels. **[FROZEN-V8] + [CLARIFY]**
7. **Cross-C pairs are restricted to supported cells and deduplicated.** **[FROZEN-V8] + [CLARIFY]**
8. **Scoring validity and provenance validity are separate, and missing or invalid provenance is not an independent group.** A body with no valid score is unscored; a body with a valid score but invalid provenance keeps its measured `k` for audit only. Invalid provenance never contributes to a cell, support count, cross-C pair, or PASS total, and no group identifier is ever synthesized from a body hash. This is a prospective amendment to the H3 evidence protocol that departs from V8's `untracked:<body_hash>` synthesis path; frozen V8 itself is unchanged. **[AMEND]**
9. **V4 requires a differential test against a faithful V8 reference on the domain where V8 is defined**, plus separate tests for proposed amendments, once those amendments are explicitly approved. **[PROCESS]**
10. **Classifier acceptance prioritises avoiding false positives over avoiding false negatives.** Abstention is preferred to a confident wrong label. **[POLICY]**
11. **V3 `bc029bc` remains an immutable rejected review record.** It is not merged, its cell summaries are not used, and its new labels do not enter H3 evidence. **[POLICY]**
12. **No V4 implementation starts until D1–D16 have each been decided or explicitly deferred, with the rationale and scope restriction recorded.** Every decision affecting the proposed implementation scope must be decided before work begins. A single-pool implementation may proceed only after the no-pooling default is approved and one `(route, run_id)` evidence pool is explicitly declared; no cross-pool aggregation, support credit, or combined PASS is authorized, and D16.1 remains deferred and blocks all cross-pool pooling. **[PROCESS]**
13. **Classification and cell counting are two independent gates.** Passing the classifier acceptance suite does not establish V8 cell-rule equality; passing the cell differential does not establish label correctness. Both must pass. **[PROCESS]**
14. **Provenance identifiers are namespaced by route and run, and namespacing is not permission to pool.** Identifiers take the form `(route, run_id, batch_or_request_id)`. Bodies from different routes or runs are not automatically exchangeable independent observations; pooling them into one cell table or PASS total requires an explicit approved protocol decision; the default position and the open decision are recorded as D16. **[AMEND; pooling → D16]**

---

## Definitions

- **Candidate body:** A generated `solve(n, edges, s, t)` implementation that passed extraction and preflight.
- **k:** Number of failed frozen probes out of 30 (six families × five probes). Integer in `0..30`. Eligible range for cells is `2 <= k <= 24`. **[FROZEN-V8]**
- **family_counts:** The six per-family failure counts `(f_R, f_Z, f_A, f_I, f_S, f_U)`. Each is an integer in `0..5`; `sum(f_j) = k`; `max_j(f_j) = max_family_count`. These identities are validated, not assumed. **[FROZEN-V8]**
- **max_family_count:** The largest per-family failure count across the six probe families. Integer; `1..min(k, 5)` when `k >= 1`, and `0` when `k = 0`. It is the canonical C-level key (see **C**). **[FROZEN-V8]**
- **C:** `max_family_count / k`, the displayed rational concentration. Within a fixed-`k` cell the **canonical C-level key is the integer `max_family_count`**. All level grouping, `m_min` checks, and cross-C comparisons use that integer; the quotient is display only and is never compared as a float. Because `k <= 24` inside a cell, distinct integers map to distinct quotients, so integer keying is exactly equivalent to V8's float `C` grouping (`run_gate.py:550`). The equivalence is a required differential assertion (Part 5). For `k = 0` the quotient is undefined. The frozen V8 convention is `concentration()` returning `(0, 0.0)`, so a zero-failure row displays `max_family_count = 0` and `C_display = 0.000`. A `k = 0` row is never a cell row (eligibility begins at `k = 2`), so this convention is display-only and is never used for grouping, comparison, pairing, or support. **[FROZEN-V8 value; CLARIFY canonical key]**
- **Mechanism label:** A descriptive classification of solver structure. It may be fine-grained and may abstain. It does not by itself enter a scientific cell.
- **Cell label:** A scientific category admitted to `(cell_label, k)` cells. The list is closed and explicitly approved.
- **Uncertain mechanism label:** `other`, `ambiguous`, or any mechanism label that has no approved cell mapping. Uncertain rows remain in audit totals but never form or support a cell. **[FROZEN-V8 for `other`; AMEND for `ambiguous` and mechanism-only labels]**
- **Provenance group:** The independent generation unit that produced a candidate, defined per route in §4.1 (a batch, or a request only where the protocol defines the request as the unit). All bodies from one generation response share one group. It is assigned before scoring and is not derived from the body hash, body text, or any per-body value.
- **Supported cell:** A `(cell_label, k)` cell with at least two observed C levels, each represented by at least `m_min` distinct provenance groups. **[FROZEN-V8]**
- **Supported group:** A provenance group that appears in at least one supported cell.
- **m_min:** `4` distinct provenance groups per C level. **[FROZEN-V8]**

---

## Part 1 - Descriptive mechanism vocabulary

### 1.1 Principles

- Evidence must be structurally connected to the operation it claims. Co-occurrence is not evidence.
- Names, comments, docstrings, and imports never produce a confident label.
- Analysis is restricted to `solve` and the helpers that `solve` actually calls. Uncalled nested definitions are excluded, not merely uncalled top-level functions. **[FROZEN-V8 intent; V3 failed this for nested definitions]**
- If evidence is insufficient or conflicting, abstain (`other` or `ambiguous`). A confident wrong label is worse than an abstention.
- A mechanism label is descriptive only. The cell builder decides eligibility in a separate layer.

### 1.2 Proposed mechanism labels

| Label | Required connected evidence | Explicit abstention conditions | Status |
|---|---|---|---|
| `floyd` | An assignment to `M[a][b]` whose value reads the same matrix at `M[a][k]` and `M[k][b]`; `k` bound by an enclosing loop; `a`, `b`, `k` pairwise structurally distinct; `a` and `b` each bound by enclosing loops, not fixed constants; target not diagonal; at least one genuine relaxation (min-form or ordering-form). | Fixed row/column indices; reused or degenerate indices; reads not through the same matrix; unreachable helper; disconnected loops. | Mechanism label; cell label approved by V8 vocabulary. |
| `bellman_ford` | An outer rounds loop containing a loop that unpacks a 3-name edge tuple; update target indexed by the destination; the same distance container read at the source; the weight name present; source and destination distinct; at least one relaxation. | A repeated tuple loop whose update touches only one unpacked variable; a container read only at the destination; a temp-form update that the detector cannot connect; no edge relaxation. | Mechanism label; cell label approved by V8 vocabulary. |
| `heap_dijkstra` | `heappop` result bound to an extracted vertex (and distance); a neighbour loop over the extracted vertex's adjacency; a neighbour-indexed distance update; a weight-derived candidate with the extracted distance flowing in directly or through a candidate temporary; an ordering or min-form relaxation. | Unrelated heap extraction; update indexed only by the extracted vertex; adjacency not indexed by the extracted vertex; no weight flow; no relaxation test; a distance update that merely references the extracted distance without a weight or relaxation. | Mechanism label; cell label approved by V8 vocabulary. |
| `selection_dijkstra` | The same Dijkstra chain with `min(..., key=...)` extract-min instead of a heap. | Same abstention conditions as `heap_dijkstra`; no genuine selection extract-min. | Mechanism-only by default. Not a cell label unless amended. |
| `bfs` | FIFO `deque` on a single queue object, using one of the two valid FIFO pairs: **insert `append`, remove `popleft`**, or **insert `appendleft`, remove `pop`**. The classifier must confirm that insertion and removal use opposite ends of the same deque. The queued elements are graph vertices; the dequeued vertex is expanded through its adjacency. Distance updates, if present, are hop count (`dist[v] = dist[u] + 1`) or absent; no weight-derived distance is connected to the traversal; no relaxation. | Either LIFO pair — `append` with `pop`, or `appendleft` with `popleft`; insertion and removal on the same end; opposite ends that cannot be confirmed on the same deque (for example, two different deque objects); queue not connected to graph traversal; queue used for unrelated ordering; weight flows into the traversal's distances; relaxation present. | Mechanism label; cell label approved by V8 vocabulary. |
| `weighted_fifo` | FIFO `deque` connected to graph traversal, using either valid FIFO pair defined for `bfs` (`append`/`popleft` or `appendleft`/`pop`, verified on the same deque); distances set from the edge weight on first discovery, directly or through a candidate temporary; no relaxation of an already-discovered vertex; no ordering/min relaxation. | Either LIFO pair; weight bookkeeping unrelated to the traversal; later relaxation of discovered vertices; no FIFO traversal of graph vertices. | Mechanism-only by default. Not a cell label unless amended. |
| `dfs_bruteforce` | An actual recursive call cycle reachable from `solve`, where a cycle member calls a cycle member from inside a loop that iterates graph adjacency or successors. Brute-force status requires **all four** properties below, each connected to that cycle: (i) **alternative-path enumeration** — the recursion explores alternatives: after returning from one successor branch, siblings or further successors are still explored, and branch fan-out is not reduced to a single-path walk; (ii) **path or accumulated-cost tracking** — a path container/stack, or an accumulated cost carried into and out of the recursive call; (iii) **completed-path evaluation** — at a terminal/base case the completed path or accumulated cost is compared against the target or a running best-distance/best-path value, and may update it. Updating a best completed solution is permitted and is **not** relaxation: relaxation means revising a per-vertex distance or cost label so that vertex is re-expanded. The prohibition is on relaxation, not on best-solution updates; (iv) **no effective global pruning** — no state shared across alternative branches that suppresses alternative paths (a global/reachable visited or settled set, or a memo table, is the typical case). Path-local cycle prevention is allowed and is a distinct case in either form: (a) **mutable add/remove** — a set or stack scoped to the current path, added before the recursive call and removed after return; or (b) **immutable/copied state** — a new path value or accumulator constructed for each recursive branch (for example `dfs(v, path + (v,))`, or a fresh accumulator passed down), so each branch receives its own copy and no branch mutates state seen by a sibling. An explicit undo is therefore not required. The test is semantic: state is global pruning only if it is shared across alternative branches in a way that suppresses paths. Recursion inside a loop is evidence of recursive traversal, not of exhaustive search, and is insufficient on its own. No FIFO queue; no per-vertex distance-label relaxation (a best-complete-solution update is not relaxation). | Recursion without loop fan-out; numerical recursion; a loop that does not iterate graph successors; an ordinary DFS with an effective global visited/settled set; recursion inside a loop with no path or cost tracking; tracking without completed-path evaluation; a global memo that suppresses alternatives; mutable path state that is shared across branches and never undone (equivalent to global pruning); visited/settled or sharing behaviour that cannot be established statically; any FIFO queue; any per-vertex distance relaxation. If the classifier cannot reliably establish all four properties, it must abstain with `other` rather than emit `dfs_bruteforce`. | Mechanism label; cell label approved by V8 vocabulary. |
| `other` | No connected structural evidence, syntax error, missing `solve`, or analysis unavailable. | This is an abstention, not a positive label. | Uncertain; never a cell label. |
| `ambiguous` | Two or more genuine, connected signals; or a FIFO queue with weight relaxation (SPFA-like); or otherwise conflicting evidence. | This is an abstention, not a positive label. | Uncertain; never a cell label. |

### 1.3 Mandatory abstention rules

- If a queue, heap, or recursive helper is not tied to graph traversal, abstain. **[Closes the unrelated-queue and unrelated-heap cases]**
- If a weight assignment is not connected to the distance container used by the traversal, do not treat it as weight flow. **[Closes the unit-BFS-plus-bookkeeping case]**
- If a distance update references the extracted distance but performs no weight flow and no relaxation, abstain. **[Closes the unrelated-update case]**
- If a Floyd-shaped update uses fixed row or column indices, abstain. **[Closes the fixed-index case]**
- If a nested helper is defined but never called, ignore its body entirely when computing labels and reachability. **[Closes the uncalled-nested-helper case]**
- If recursion occurs only inside a numerical helper's own loop and has no graph-successor fan-out, abstain. **[Closes the numerical-recursion case]**
- Deque end discipline: `append` + `popleft` and `appendleft` + `pop` are the only valid FIFO pairs; `append` + `pop` and `appendleft` + `popleft` are LIFO and are not FIFO. Do not emit `bfs` or `weighted_fifo` for a LIFO pair, for insertion and removal on the same end, or when the two operations cannot be confirmed on the same deque object; abstain. **[Closes the LIFO-deque and same-end cases]**
- Recursion over graph successors is not brute force by itself. Emit `dfs_bruteforce` only with connected evidence of alternative-path enumeration, path or accumulated-cost tracking, completed-path evaluation, and absence of effective global pruning. Path-local cycle prevention is allowed whether it is mutable (added before the call, removed after) or immutable/copied per branch (for example `dfs(v, path + (v,))`). Global pruning is state shared across alternative branches that suppresses paths; a mutable set shared across branches and never undone is one form. If any property cannot be established statically, abstain with `other`. **[Closes the ordinary-DFS case]**
- For `dfs_bruteforce`, a completed-path or best-cost comparison may update a running best solution. That is a solution update, not relaxation, and must not trigger abstention. Abstention on relaxation grounds applies only when the code revises a per-vertex distance or cost label in order to re-expand that vertex — a shortest-path relaxation mechanism that conflicts with brute-force enumeration. **[Closes the best-path-update ambiguity]**
- If any required evidence is missing or disconnected, prefer `other` over a confident label.

### 1.4 Non-signals

The following never contribute to a label: identifier names, function names, comments, docstrings, unused imports, unused top-level helpers, uncalled nested helpers, and values recorded in an unrelated container.

---

## Part 2 - Closed list of approved scientific cell labels

### 2.1 Approved cell labels (default)

The approved scientific cell vocabulary is the frozen V8 vocabulary:

- `heap_dijkstra`
- `bfs`
- `bellman_ford`
- `floyd`
- `dfs_bruteforce`

**[FROZEN-V8 vocabulary]**

### 2.2 Mechanism-only labels (default, not cell labels)

- `weighted_fifo`
- `selection_dijkstra`

These may be emitted by the mechanism classifier and reported as descriptive labels. They do not enter scientific cells unless a recorded amendment explicitly approves them. **[AMEND - default position]**

### 2.3 Abstention labels (never cell labels)

- `other`
- `ambiguous`

**[FROZEN-V8 for `other`; AMEND for `ambiguous`]**

### 2.4 Explicit mapping table

| Mechanism label | Cell label |
|---|---|
| `heap_dijkstra` | `heap_dijkstra` |
| `bfs` | `bfs` |
| `bellman_ford` | `bellman_ford` |
| `floyd` | `floyd` |
| `dfs_bruteforce` | `dfs_bruteforce` |
| `selection_dijkstra` | none by default |
| `weighted_fifo` | none by default |
| `other` | none |
| `ambiguous` | none |
| any unrecognised label | none |

There is no implicit mapping. A label not listed in the left column, or any label whose mapping is `none`, is excluded from cells.

### 2.5 No implicit admission

A cell builder must not admit "every label except `other` and `ambiguous`." That is the V3 failure mode. Admission requires an explicit entry in the approved mapping table. **[AMEND relative to V3; [CLARIFY] relative to V8, whose classifier vocabulary is closed by construction]**

### 2.6 Audit visibility

Uncertain and mechanism-only rows remain visible in overall audit totals: candidate counts, k distribution, family counts, saturation rates, and exclusion reason. They are excluded only from cells, supported cells, cross-C pairs, and PASS group counts. **[FROZEN-V8]**

---

## Part 3 - Cell-eligibility algorithm

### 3.1 Inputs

Every scored row must provide the following (an unscored row supplies only its invalidity reason):

- `provenance_group`: a valid, non-empty, namespaced group identifier, or a recorded invalidity reason (Part 4). This is one validity dimension.
- `cell_label`: the approved cell label, or a non-cell label.
- `family_counts`: the six per-family failure counts `(f_R, f_Z, f_A, f_I, f_S, f_U)` for the frozen 30-probe instrument. Each is an integer in `[0, 5]`; `sum(f_j) = k`; and `max_j(f_j) = max_family_count`.
- `k`: integer failure count in `0..30` (30 probes = six families × five probes). Cells use the eligible subrange `2..24`. `k` is absent when the candidate is unscored. A boolean or non-integer is rejected.
- `max_family_count`: integer, the largest per-family failure count. For `k >= 1`, `1 <= max_family_count <= min(k, 5)`; for `k = 0`, `max_family_count = 0`. A boolean or non-integer is rejected. Present whenever `k` is present. The upper bound of `5` follows from the six-family probe structure: the 30 probes are six families of five probes each, so no single family count can exceed five.
- `eligible_2_to_24`: **derived** from the validated integer `k` as `2 <= k <= 24`. It is not an independent input and never overrides `k`. If a producer also supplies a boolean flag, the supplied value must equal the derived value; a disagreement is a measurement-integrity failure — for example `k = 25` with `eligible_2_to_24 = true`, or `k = 9` with `eligible_2_to_24 = false` — and the row is rejected rather than resolved in favour of either input.
- `body_sha256`: exact body hash, for duplicate handling.

The recorded `k` and `max_family_count` must agree with the six underlying family counts; they are not independent values to be trusted on their own. A row is a **measurement-integrity failure** if any of the following holds:

- any `f_j` is not an integer, is a boolean, or lies outside `[0, 5]`;
- `sum_j(f_j) != k`;
- `max_j(f_j) != max_family_count`;
- `k` or `max_family_count` itself is outside the domains above;
- `eligible_2_to_24`, if supplied as a boolean, disagrees with the value derived from `k`.

A row with a measurement-integrity failure is marked invalid for audit and excluded from every cell, supported-cell count, cross-C pair, and PASS total. It is reported with its inconsistency; it is never silently corrected, recomputed, or clamped to fit.

Scoring validity and provenance validity are independent:

| State | Enters the cell algorithm? | Visible in audit totals? |
|---|---|---|
| Valid score, valid provenance | Yes | Yes |
| Valid score, invalid provenance | No | Yes |
| Valid score but invalid `k`/`max_family_count`/`family_counts` consistency | No | Yes, as a measurement-integrity failure |
| No valid score (unscored) | No | Yes, as an invalid candidate |

A row with a valid score but invalid provenance keeps its measured `k` for audit and distributional reporting, but it is excluded from every cell, supported-cell count, cross-C pair, and PASS group total. An unscored row never enters the algorithm at all.

### 3.2 Normative algorithm

The following reproduces frozen V8 cell construction (`h3-footprint-v8/run_gate.py:541-588`) with the approved exclusions made explicit.

```
# Stage 0 - duplicate handling is part of the algorithm, not a preprocessing step (§4.4).
# Scope is one evidence pool (route, run_id) at a time. Identical body hashes are
# collapsed to a single row, retaining the first occurrence in the route's declared
# record order. Every occurrence remains in the audit record. No fuzzy or
# near-duplicate merge. No deduplication across evidence pools.
pool_rows = [row for row in rows if row.pool_id == active_pool_id]
dedup = first row per distinct row.body_sha256, in declared record order, over pool_rows

eligible = [row for row in dedup if 2 <= row.k <= 24 and row.valid_for_k]
support_eligible = [row for row in eligible
                    if row.cell_label in APPROVED_CELL_LABELS
                    and row.provenance_valid         # Part 4: invalid provenance never joins a cell
                    and row.measurement_valid]       # §3.1 domain: invalid k/m never joins a cell

cells = group support_eligible by (row.cell_label, row.k)
for each cell (label, k):
    # Canonical level key is the integer max_family_count. The float C = max_f/k
    # is display only and is never used for grouping or comparison.
    levels = group cell rows by row.max_family_count
    level_groups[level] = set of valid provenance_group values at that level

    supported = (len(levels) >= 2)
    for each level in levels:
        if len(level_groups[level]) < 4:
            supported = False

    cell_unique_groups = union of level_groups over all levels
    cell_candidate_bodies = number of deduplicated rows in the cell   # §4.4; duplicates do not inflate this

    if supported:
        add cell to supported_cells with:
            label, k, levels, candidate_bodies,
            level_group_counts, cell_unique_groups

supported_group_union = union of cell_unique_groups over supported cells
distinct_supported_k = set of k over supported cells

cross_pairs = empty set
for each supported cell (label, k):
    group_to_level[group] = set of canonical level keys at which that group appears
    for each unordered pair of distinct groups (gA, gB) in group_to_level:
        if any level key of gA differs from any level key of gB:
            add (label, k, gA, gB) to cross_pairs
```

Deduplication is a required stage, not an implicit assumption. It runs before eligibility and before any count, because `candidate_bodies` is defined over deduplicated rows. Omitting it inflates `candidate_bodies` and makes the gate's output depend on an unstated preprocessing step. It does not change group counts, because a duplicate keeps the provenance of its first record (§4.4), but it does make reports non-reproducible between implementations. Deduplication never crosses evidence-pool boundaries (§4.1.1, D16). A body that appears in two pools is handled by D16.1 and is not resolved by this stage: it is reported per pool until a pooling amendment specifies representation, provenance retention, support credit, and conflict reconciliation.

#### 3.2.1 Why the integer key preserves V8's grouping

Within a fixed-`k` cell, `C = m / k` where `m = max_family_count` is an integer and `k` is constant. Distinct integers `m` therefore produce distinct quotients: with `k <= 30`, two distinct values differ by at least `1/k >= 1/30`, which is far above binary floating-point resolution for these values. Grouping by the integer `m` consequently yields exactly the same levels as grouping by the exact rational `m/k`, and the same levels as V8's float `C` (`run_gate.py:550`), for every input this instrument can produce. The integer key removes float equality entirely without changing the intended grouping. The equivalence is still asserted by test (§5.1–§5.2), not assumed.

### 3.3 Normative requirements

| Requirement | Tag |
|---|---|
| Eligible range is `2 <= k <= 24`. | [FROZEN-V8] |
| Exact body hashes are deduplicated once per evidence pool before eligibility, retaining the first occurrence in the route's declared record order. | [FROZEN-V8; CLARIFY stage] |
| Duplicate occurrences remain in the audit record but do not inflate `candidate_bodies`. | [FROZEN-V8; CLARIFY] |
| No fuzzy, semantic, or similarity deduplication; no deduplication across evidence pools. | [FROZEN-V8; CLARIFY] |
| `k` is an integer in `0..30`; cells use `2..24`. Booleans and non-integers are rejected. | [FROZEN-V8; CLARIFY validation] |
| `eligible_2_to_24` is derived from validated `k`; a supplied boolean must agree, or the row is a measurement-integrity failure. | [CLARIFY validation] |
| `max_family_count` is an integer; for `k >= 1` it lies in `1..min(k, 5)`; for `k = 0` it is `0`. Booleans and non-integers are rejected. | [FROZEN-V8; CLARIFY validation] |
| The six family counts are integers in `[0, 5]`; their sum equals `k` and their maximum equals `max_family_count`. Inconsistent measurements are rejected, never repaired. | [FROZEN-V8; CLARIFY validation] |
| Cells are keyed by `(cell_label, k)`. | [FROZEN-V8] |
| C levels are keyed by the integer `max_family_count`, never by the float quotient `max_family_count / k`. | [FROZEN-V8 value; CLARIFY canonical key] |
| Only rows with valid provenance join a cell. Invalid provenance is excluded from cells, support, cross-C pairs, and PASS totals, and keeps its `k` only for audit. | [AMEND] |
| A cell is supported only if it has at least two observed C levels. | [FROZEN-V8] |
| Every observed C level in a supported cell must have at least `m_min = 4` distinct provenance groups. A third or later sparse level disqualifies the cell. | [FROZEN-V8] |
| The distinct-group count per level uses the set of valid provenance groups, not the candidate-body count. | [FROZEN-V8] |
| A cell's unique-group count is the union of its per-level group sets, not the sum of per-level counts. | [FROZEN-V8] + [CLARIFY] |
| The supported-group total is the union of group identifiers across all supported cells, not the sum of each cell's group count. | [FROZEN-V8] + [CLARIFY] |
| Cross-C pairs are considered only within supported cells. | [FROZEN-V8] |
| Cross-C pairs use unordered pairs of distinct provenance groups. A group cannot pair with itself, including when it appears at different C levels. | [FROZEN-V8] + [CLARIFY] |
| Cross-C pair sets are deduplicated; a pair is recorded as `(cell_label, k, group_a, group_b)` with `group_a != group_b`. Counting scope: one pair per supported cell, not one per C-level contrast and not collapsed across different supported cells. | [FROZEN-V8] + [CLARIFY] |
| `other`, `ambiguous`, and any mechanism-only label are excluded from all cell construction, supported-cell counts, cross-C pairs, and PASS group counts. They remain in audit totals. | [FROZEN-V8 for `other`; AMEND for `ambiguous` and mechanism-only labels] |
| PASS requires at least three supported cells, at least two distinct supported k values, and at least 40 unique provenance groups in the union of supported cells. | [FROZEN-V8] |
| WEAK means one or two supported cells. | [FROZEN-V8] |
| FAIL covers all other cases, plus the frozen futility and saturation rules. | [FROZEN-V8] |

### 3.4 Required report fields

For each cell:

- `cell_label`
- `k`
- `candidate_bodies`
- per C level: `max_family_count` (canonical key), `C_display` (`max_family_count / k`), `candidate_bodies`, `groups` (distinct valid provenance groups), `group_ids`
- `cell_unique_groups`
- `supported` (boolean)

For the run:

- `support_eligible_bodies`
- `support_eligible_groups` (union)
- `uncertain_or_mechanism_only_eligible_bodies`
- `uncertain_or_mechanism_only_eligible_groups` (union)
- `supported_cell_count`
- `distinct_supported_k`
- `unique_groups_in_supported_cells` (union)
- `cross_C_group_pair_count` (size of deduplicated supported-cell pair set)
- the complete cell table, including unsupported cells
- the exclusion reason for every non-cell label

Rows with `k = 0` appear only in audit and distributional reporting, never in a cell. For those rows `max_family_count = 0` and `C_display = 0.000` by the frozen V8 convention; the quotient `C` is undefined and is never compared or used as a grouping key.

### 3.5 Worked examples

These are the cases that separate the frozen V8 rules plus the proposed amendments from the V3 failure mode.

| Synthetic rows | Correct result |
|---|---|
| 3 C levels: 4 groups, 4 groups, 1 group | **Unsupported**; every observed level must have at least 4 groups. |
| Same 4 provenance groups at 2 C levels | **Supported**; `cell_unique_groups = 4`; cross-C pairs = 6 unique pairs, not 16; no self-pairs. |
| Same group pair across several C-level contrasts | **One** pair for that cell, not one per contrast. |
| 1 group at each of 2 levels | **Unsupported**; cross-C pairs = 0 because unsupported cells do not contribute. |
| 4+4 groups labelled `other` or `ambiguous` | **No cells**; uncertain labels never enter cells. |
| 4+4 groups labelled `weighted_fifo` | **No cells** by default; mechanism-only unless amended. |
| Two different bodies from the same group | One group; candidate bodies may be two, groups is one. |
| Same body duplicated | One body after hash deduplication; one group; provenance is the first record, in the route's file order, that contains it (for V8, `attempts.jsonl`). |
| Two near-identical bodies from different batches | Two groups under the frozen batch rule; no fuzzy merge. |
| Valid `k` but invalid provenance | `k` retained for audit; no group; excluded from cells, support, pairs, and PASS totals. |
| Levels `4/9` and `5/9` in one `k=9` cell | Two levels keyed by `max_family_count` 4 and 5; the float quotients are display only. |
| A group present in two supported cells | Counted once in the supported-group union; no self-pair; may contribute to each cell's own level counts. |

### 3.6 Out of scope for this record

The following remain frozen and unchanged:

- Futility checkpoints at batches 100/200/300 with minima 10/20/30. [FROZEN-V8]
- Eligible saturation rate and the 0.80 degeneracy cutoff. [FROZEN-V8]
- Generation budget, batch schedule, prompt variants, and model set. [FROZEN-V8]
- Extraction and preflight rules. [FROZEN-V8]

This record concerns only mechanism labels, cell eligibility, provenance, and the tests that enforce them.

---

## Part 4 - Provenance independence and duplicate handling

### 4.1 Definition

A provenance group is the independent generation unit that produced a candidate. Its identifier is a **namespaced triple `(route, run_id, batch_or_request_id)`**, rendered as one opaque string. Group identity is assigned before scoring, from the generation record, and is never derived from a body. Multiple bodies produced by one generation response belong to one group.

- `route` names the generation route (for example `v8-gate`, `glm-cloud`, `copilot-auto`).
- `run_id` identifies the generation run whose record file contains the unit. It must be stable and declared in that run's protocol; for a published artifact it is the run or commit identifier.
- `batch_or_request_id` identifies the independent generation unit within that run.

A bare `batch-001` or `request-001` is **not** a valid identifier: it can collide across runs and routes, and it hides which route's independence definition applies.

The independent unit is defined per generation route. A route must not adopt another route's definition of independence.

| Route | Independent generation unit | Identifier form | Bodies per group |
|---|---|---|---|
| H3 gate, frozen V8 (`run_gate.py`) | one generation batch | `v8-gate:<run_id>:batch-<batch_id>`, from the integer `batch_id` in `attempts.jsonl` | every body extracted from that batch response |
| GLM cloud pilot (`glm-agent-feasibility-2026-10-29`) | one generation request, because that protocol defines the request as the independent unit | `glm-cloud:<run_id>:request-<request_id>` | every body extracted from that request |
| Copilot-Auto screen (`copilot-auto-screen-2026-10-29`) | one generation request, because that protocol defines the request as the independent unit | `copilot-auto:<run_id>:request-<request_id>` | every body extracted from that request |

Rules:

- **One response, one group.** All bodies from one generation response share exactly one group identifier. If a batch or request produces eight candidate bodies, all eight carry the same group and count as one group; they do not become eight groups. [FROZEN-V8]
- **A request identifier is route-conditional.** It is a valid group only where the protocol defines the request as the independent generation unit (as in the pilot and screen above). Where the batch is the unit, as in the V8 gate, a request id must not be substituted for `v8-gate:<run_id>:batch-<batch_id>`. [CLARIFY]
- **Namespaced and unique.** Every identifier includes `route` and `run_id`. The same `batch_or_request_id` in two different runs yields two distinct groups; the same logical unit must not be re-identified under a second `run_id`, and identifiers must not be truncated to bare numbers. [AMEND]
- **Never a body hash.** A body hash, body text, or any per-body value is never a group identifier, and no hash-derived surrogate may be created. [FROZEN-V8 intent; AMEND for the synthetic `untracked:<hash>` path]
- **Assigned before scoring and before duplicate handling.** Duplicate bodies keep the group of their first record in the route's declared record file (§4.4). [FROZEN-V8]

#### 4.1.1 Provenance identity is not permission to pool

Namespacing guarantees that identifiers do not collide. It does **not** by itself authorise treating bodies from different routes or runs as exchangeable, independent observations.

- Within one approved evidence pool, every supported cell, `m_min` check, cross-C pair, and PASS group count uses only provenance groups from that pool.
- Bodies from different generation routes must not be pooled automatically, because their independence definitions differ. The GLM cloud pilot already differs from the V8 gate: a batch and a request are not the same unit, and the pilot's outputs are near-identical (GLM evidence audit, 2026-10-29).
- Combining routes or runs into one cell table, and counting their groups toward the same PASS total, requires an **explicit approved protocol decision** that states which unit is independent and how runs are combined. Until such a decision is recorded, cross-route bodies are reported separately and do not share a cell or a group total.

This is recorded as **D16**. The default position is one evidence pool per `(route, run_id)`, no automatic cross-route or cross-run pooling, and no combined PASS total unless a further explicit amendment defines how pools are combined and which unit is independent. Cross-pool duplicates are not resolved here; D16.1 requires any future pooling amendment to state representation, provenance retention, support credit, and conflict reconciliation, and forbids first-encountered-record precedence across pools. D16 is not approved by this record. Under D15 it must be decided or explicitly deferred before any V4 implementation; approving the no-pooling default decides it for work confined to one declared pool, and D16.1 remains deferred and blocks all cross-pool pooling. [OPEN; D16, D16.1]

### 4.2 Validity

A provenance identifier is valid only if it is:

- present,
- a non-empty string,
- a namespaced triple `(route, run_id, batch_or_request_id)` as defined in §4.1, not a bare batch or request number and not truncated,
- assigned from the route's independent generation unit (the batch for the V8 gate; the request only where the protocol defines the request as the unit),
- shared by all bodies from the same generation response,
- drawn from one approved evidence pool; cross-route or cross-run pooling requires the decision described in §4.1.1,
- not synthesized from a body hash, body text, or any per-body value,
- not the literal form `untracked:<body_hash>`.

### 4.3 Missing or invalid provenance

Scoring validity and provenance validity are independent, and neither implies the other.

| Situation | Normative treatment |
|---|---|
| No valid score (`k` absent) | Unscored. Receives no `k`; never enters eligibility, cells, or support. |
| Valid score, invalid provenance | Retains its measured `k` for audit and distributional reporting only. Never enters a cell, supported-cell count, cross-C pair, or PASS group total. |

A provenance identifier is invalid if it is missing, empty, non-string, not namespaced by route and run, drawn from a different evidence pool than the cell being built, synthesized from a body hash / body text / any per-body value, or of the literal form `untracked:<body_hash>`. For a body with a valid score and invalid provenance:

- the `k` value is kept, labelled as audit-only, and may appear in `k` and `max_family_count` distributions;
- the body is excluded from every cell, supported-cell count, cross-C pair, and PASS group total;
- the body remains visible in overall audit totals and in the invalidity/exclusion reason table;
- the body is **never** assigned a synthetic group identifier derived from its hash or text, and is never treated as a new independent group.

**[AMEND]** This explicitly overrides V8's `body_meta()` path, which synthesises `untracked:<body_hash>` when `batch_id` is absent (`run_gate.py:255`). Under this record that synthesis is prohibited for evidence, and no substitute hash-derived identifier may be created. V8's other path, where a body has no `attempts.jsonl` record at all and `group_id` is `None` (`run_gate.py:364-365`), already invalidates the candidate; this record makes that behaviour explicit and extends it to the synthetic-identifier path.

### 4.4 Duplicates and replicas

Duplicate handling follows the frozen per-response provenance rule (one generation response, one group). There are three distinct cases, and they must not be conflated.

| Situation | Required treatment |
|---|---|
| **Exact duplicate body** (identical bytes, identical hash) | Deduplicate by exact hash. Count the body once, with the provenance of its first observed generation record for that route. |
| **Different bodies from one generation batch/request** | One provenance group. The group is the batch/request, not the body. |
| **Near-duplicate bodies from different batches/requests** | Separate provenance groups under the frozen per-response rule. No fuzzy, semantic, or similarity clustering is applied implicitly; adding one would be a separate protocol amendment. |

- A candidate body is identified by its exact body hash. [FROZEN-V8]
- An identical body is counted once; the route's declared record file still records every occurrence, including duplicates (for V8, `attempts.jsonl`), so the choice is auditable. [FROZEN-V8]
- Multiple distinct bodies from one generation response remain one group. [FROZEN-V8]
- Exact-hash deduplication is **within one evidence pool only**. If an identical body appears in two pools, this section does not decide whether it is one observation or two: D16.1 requires the eventual pooling amendment to specify representation, provenance retention, support credit, and conflict reconciliation. Across pools, file order confers no precedence. [OPEN; D16.1]

**"First observed" is a deterministic record-selection order, not a chronological one.** For the V8 gate, frozen V8 assigns each distinct body to the first batch that emitted it via `meta.setdefault` while iterating `attempts.jsonl` in file order (`run_gate.py:236-260`): the provenance of a duplicate body is the group of the earliest record, in `attempts.jsonl` line order, that contains that body hash. A request-based route must apply the same rule to its own generation-request record, and that record file must be declared in the route's protocol. In every route the rule does not read timestamps, does not select the smallest identifier, and does not depend on any ordering outside the declared record file. V4 must use the route's declared file-order rule. [FROZEN-V8; CLARIFY generalisation]

### 4.5 A group at multiple C levels

- The group counts at each C level for that level's `m_min` check, because the threshold is per level. [FROZEN-V8]
- The group counts once in the cell's unique-group union. [FROZEN-V8] + [CLARIFY]
- The group cannot form a cross-C pair with itself, even across different C levels. [FROZEN-V8] + [CLARIFY]

### 4.6 Union across supported cells

The supported-group total is:

```
unique_supported_groups = union over supported cells of cell_unique_groups
```

It is not the sum of `cell_unique_groups` across cells. A group that appears in three supported cells counts once. [FROZEN-V8] + [CLARIFY]

### 4.7 Cross-C pairs

A cross-C pair exists only when two distinct provenance groups appear in the same supported cell and have at least one different canonical C level (`max_family_count`). Comparisons use that integer key, never the float quotient.

- Restrict to supported cells. [FROZEN-V8]
- Use unordered pairs of distinct groups. [FROZEN-V8]
- No self-pairs, including a group at two C levels. [FROZEN-V8] + [CLARIFY]
- Deduplicate; record `(cell_label, k, group_a, group_b)` with a canonical order. [FROZEN-V8]
- Do not count pairs from unsupported variation cells. [FROZEN-V8]
- Do not count a pair twice because the groups span multiple C-level combinations. [FROZEN-V8]

#### 4.7.1 Counting scope

A pair of groups is counted **once per supported cell `(cell_label, k)`**, regardless of how many C-level contrasts exist between them.

- If group A appears at levels `max_family_count = 4` and `5` (displayed `C=4/9`, `C=5/9` for `k=9`) and group B appears at the same two levels, the pair `(A, B)` is **one** cross-C pair, not four.
- If the same group pair appears in two different supported cells with different `k` or different `cell_label`, it contributes one pair to each cell, because each is a distinct cell-specific comparison.
- The global `cross_C_group_pair_count` is the size of the union of per-cell keys `(cell_label, k, min(group_a, group_b), max(group_a, group_b))`.

This matches V8's `group_pairs` set keyed by `(label, k, group_a, group_b)` (`run_gate.py:575-588`). It is neither a count per C-level transition nor a single global pair collapsed across all cells.

### 4.8 PASS group count

The PASS group count is `len(unique_supported_groups)`, not the sum of per-cell group counts and not a candidate-body count. [FROZEN-V8] + [CLARIFY]

### 4.9 Audit visibility

The report must show, separately:

- eligible candidates and groups with approved cell labels;
- eligible candidates and groups labelled `other`, `ambiguous`, or mechanism-only;
- invalid candidates by reason, including missing/invalid provenance;
- the full cell table, including unsupported cells.

This makes the exclusion auditable. [FROZEN-V8 requirement, extended]

---

## Part 5 - Required differential tests

### 5.1 Reference implementation

V4's cell builder must be compared against a faithful reference implementation transcribed from frozen V8 cell construction (`h3-footprint-v8/run_gate.py:541-588`). The reference must:

- be a standalone function taking synthetic scored rows with explicit `provenance_group`, `cell_label`, `k`, `max_family_count`, and validity;
- implement the exact V8 semantics: eligible range, `other` exclusion, `(label, k)` keying, per-C-level distinct group sets, every-level `m_min`, unique-group union, and deduplicated supported-cell cross-C pairs;
- implement those semantics with V8's level key (`C = max_family_count / k`, `run_gate.py:550`) **and** assert that it produces exactly the same levels, counts, and pairs as the canonical integer `max_family_count` key for every fixture with fixed `k`; the two keyings are equivalent because `k <= 24`, but the equivalence must be proven by test, not assumed;
- be frozen with a SHA-256 and a provenance note stating the V8 source lines and blob hash;
- not import or execute any generated solver body.

### 5.2 Exact-V8 differential layer

On inputs where V8's domain is defined, V4 must produce exactly the same results as the reference:

- valid namespaced, route-conformant provenance (the batch is the unit for the V8 gate);
- labels restricted to the V8 cell vocabulary;
- no `ambiguous`;
- eligible `k` in `2..24`;
- explicit canonical C levels (`max_family_count`).

Equality must cover: supported/unsupported decisions, level identity (canonical integer key mapped one-to-one to V8's float `C`), per-level group counts, cell unique-group counts, supported-cell count, distinct supported k, supported-group union, and cross-C pair set.

The differential report must present **two independent results**: the exact-V8 result on the domain where V8 is defined, and the amendment-conformance result on amendment inputs. They are reported and must pass separately; neither substitutes for the other.

### 5.3 Amendment layer

Proposed amendments, once explicitly approved, are tested separately against their approved requirements, not against V8 equality. This layer is the second of the two required differential results; it does not modify the frozen V8 comparison in §5.2. Until an amendment is approved, its cases remain proposals and cannot be used to claim conformance.

- missing/invalid provenance (V8 would synthesize `untracked:<hash>`; V4 excludes);
- `ambiguous` label (V8 has no such label);
- mechanism-only labels `weighted_fifo` and `selection_dijkstra` (V8's classifier would not emit them; V4 excludes by default).

For these cases, once the amendment is approved, the test asserts the approved behaviour and documents the intentional difference from V8. Before approval, the expectation is a proposal and is reported without being treated as accepted policy.

### 5.4 Minimum fixture table

| Fixture | Expected |
|---|---|
| No rows | No cells; zero supported; zero pairs. |
| One eligible row | No variation; no supported cell. |
| Two C levels, 3 groups each | Unsupported; zero pairs. |
| Two C levels, 4 groups each | One supported cell; 4 unique groups; 6 cross-C pairs. |
| Three C levels, 4/4/1 | Unsupported; zero pairs. |
| Same 4 groups at two C levels | Supported; 4 unique groups; 6 pairs; no self-pairs. |
| Same two groups at `C=4/9` and `C=5/9`, plus other groups | The pair counts once for the cell, not four times. |
| Levels `max_family_count=4` and `5` at `k=9` | Two canonical levels; V8's float `C` grouping yields the same two levels. |
| Same group pair in two supported cells with different `k` | One cell-specific pair per cell; two keys. |
| Two bodies, same group, same level | One group; no support inflation. |
| Duplicate body hash in two batches | One body; one group; provenance from the first `attempts.jsonl` record. |
| Same body hash recorded twice in one pool | One row after deduplication; `candidate_bodies` counts once; both occurrences remain auditable. |
| Same body re-recorded in a later batch | Still the first-record group; one body. |
| Near-identical bodies in two batches | Two groups; no fuzzy merge. |
| Two distinct bodies in one batch | One group. |
| One request producing eight bodies | One group; eight candidate bodies. |
| Two requests, one body each | Two groups. |
| `request_id` used where the batch is the unit | Invalid provenance; not the route's independent unit. |
| Body hash used as `provenance_group` | Invalid; hash substitutes are prohibited. |
| Same `batch_id` in two different runs | Two distinct groups; identifiers differ by `run_id`. |
| Same `batch_id`/`request_id` in two routes | Two distinct groups; never merged. |
| Bare `batch-001` without route/run | Invalid identifier; not namespaced. |
| Cross-route bodies placed in one cell without an approved pooling decision | Rejected for that cell; reported separately, not pooled. |
| Valid `k`, missing provenance | `k` retained for audit; no group; excluded from cells/support/pairs/PASS. |
| Valid `k`, empty-string provenance | Same as missing: `k` audit-only, no group. |
| Valid `k`, `untracked:<hash>` provenance | Same as missing; synthesis prohibited; no surrogate group. |
| `other` with 4+4 groups | No cells. |
| `ambiguous` with 4+4 groups | No cells. |
| `weighted_fifo` with 4+4 groups | No cells by default. |
| `selection_dijkstra` with 4+4 groups | No cells by default. |
| Pair only in an unsupported variation cell | Zero cross-C pairs. |
| Same group in two supported cells | Counted once in the supported-group union. |
| `k = 1`, `k = 25` | Not eligible; no cells. |
| `k = 0` | Not eligible; `max_family_count = 0`, `C_display = 0.000`; no cell. |
| `eligible_2_to_24 = true` with `k = 25` | Measurement-integrity failure; excluded. |
| `eligible_2_to_24 = false` with `k = 9` | Measurement-integrity failure; excluded. |
| `k = 7.5` (float) | Invalid measurement; no cell. |
| `k = true` (bool) | Invalid measurement; no cell. |
| `k = 31` | Invalid; outside `0..30`. |
| `max_family_count = 6` | Invalid; exceeds the five-probe per-family bound. |
| `max_family_count = 5`, `k = 3` | Invalid; `max_family_count` exceeds `k`. |
| `max_family_count = 0`, `k = 5` | Invalid; a scored cell row must have `max_family_count >= 1`. |
| `family_counts` sum differs from `k` | Measurement-integrity failure; excluded. |
| `family_counts` maximum differs from `max_family_count` | Measurement-integrity failure; excluded. |
| Any `f_j = 6`, `f_j = -1`, or `f_j = 1.5` | Measurement-integrity failure; excluded. |
| `family_counts` integers in `[0,5]`, sum `k`, max `max_family_count` | Valid measurement. |
| Three supported cells, two k, 39 unique groups | FAIL (insufficient groups). |
| Three supported cells, two k, 40 unique groups | PASS. |
| 40 groups by sum but 39 by union | FAIL; union is authoritative. |

### 5.5 Acceptance criteria

- Exact equality with the reference on every exact-V8 fixture.
- Expected behaviour on every approved-amendment fixture; proposed fixtures are reported and remain non-blocking until the amendment is approved.
- The exact-V8 result and the amendment result are reported and pass separately; a pass on one is not accepted for the other.
- The canonical integer level key is asserted equivalent to V8's float `C` grouping on every fixed-`k` fixture.
- No test may generate candidates, call model APIs, or execute generated solver bodies.
- Synthetic rows only; no frozen pilot evidence rewritten.
- The differential suite must run before any V4 cell-summary result is used.

### 5.6 Non-goals

The differential test does not validate the classifier and does not validate V8's mechanism labels. It validates only cell counting and provenance handling.

---

## Part 6 - Classifier acceptance cases

This suite is independent of the cell differential in Part 5, and it must be satisfied in addition to it. The five approved cell labels are a closed admission list, not a guarantee that a candidate carrying one of them was classified correctly: V8's classifier has known false positives. Passing the cell differential does not establish label correctness, and passing this suite does not establish V8 cell-rule equality. Both gates must pass. **[PROCESS]**

### 6.1 Hard requirements (false positives are merge-blocking)

These cases must abstain or produce the correct mechanism label. A confident wrong label blocks acceptance.

| Case | Input shape | Required outcome | Current V3 outcome | Current V8 outcome |
|---|---|---|---|---|
| A | Floyd-shaped update with fixed row and column indices | `other` | `floyd` (wrong) | `other` |
| B | Deque operations unrelated to graph traversal | `other` | `bfs` (wrong) | `bfs` (wrong) |
| C | Unit-weight FIFO plus unrelated weight bookkeeping | `bfs` | `weighted_fifo` (wrong) | `bfs` |
| D | Heap extract-min plus unrelated adjacency/distance update | `other` | `heap_dijkstra` (wrong) | `heap_dijkstra` (wrong) |
| E1 | Numerical recursive helper called from a loop, no graph DFS | `other` | `other` (correct) | `dfs_bruteforce` (wrong) |
| E2 | Numerical recursion with the recursive call inside its own loop | `other` | `dfs_bruteforce` (wrong) | `dfs_bruteforce` (wrong) |
| F | Uncalled nested helper that references another function, or contains a strong structure | `other` | `floyd` (wrong) | `other` |

#### 6.1.1 Queue-discipline and path-enumeration fixtures

These fixtures enforce the queue-discipline and brute-force requirements above. They are not exercised by the audited V3 or V8 suites, so no current outcome is recorded; the required outcome is normative.

| Case | Input shape | Required outcome |
|---|---|---|
| Q1 | `deque` insert `append`, remove `popleft`, graph vertices, hop-count distances | `bfs` |
| Q2 | `deque` insert `appendleft`, remove `pop`, graph vertices, hop-count distances | `bfs` |
| Q3 | `deque` insert `append`, remove `pop` (LIFO) connected to graph traversal | `other` |
| Q4 | `deque` insert `appendleft`, remove `popleft` (LIFO) connected to graph traversal | `other` |
| Q5 | Opposite-end operations that cannot be confirmed on the same deque object | `other` |
| P1 | Recursive cycle over graph successors, effective global visited set, no path or cost tracking | `other` |
| P2 | Recursive cycle over graph successors, accumulated path cost, completed-path evaluation, path-local visited set undone on return | `dfs_bruteforce` |
| P3 | Recursive cycle over graph successors; visited/path behaviour not statically determinable | `other` (abstain; never a confident `dfs_bruteforce`) |
| P4 | Recursive cycle over graph successors, explicit path container, completed-path evaluation, no visited set at all | `dfs_bruteforce` |
| P5 | Recursive cycle over graph successors, path tracking, but no evaluation of completed paths against target or best | `other` |
| P6 | Recursive cycle over graph successors, path cost tracked, mutable path-local set shared across branches and never removed (acts as global pruning) | `other` |
| P7 | Recursive cycle over graph successors, immutable path value copied per branch (`dfs(v, path + (v,))`), completed-path evaluation, no shared visited state | `dfs_bruteforce` |
| P8 | Recursive cycle over graph successors with a copied path but a global visited set shared across branches | `other` |

### 6.2 Target requirements (false negatives are documented, not merge-blocking)

| Case | Input shape | Target outcome | Current V3 outcome |
|---|---|---|---|
| request-04 | Genuine heap Dijkstra with a finality check and no neighbour-indexed `dist[v]` assignment | `heap_dijkstra`, or a documented abstention | `other` |
| Temp-form weighted FIFO | Weighted first-discovery FIFO using `nd = dist[u] + w; dist[v] = nd` | `weighted_fifo`, or at least not `bfs` | `bfs` |
| Temp-form Bellman-Ford | Bellman-Ford using a candidate temporary | `bellman_ford`, or a documented abstention | `other` |

The priority is explicit: a false negative is acceptable if documented; a false positive that enters a cell is not.

### 6.3 True-positive fixtures

The acceptance suite must also include genuine examples of:

- `floyd`
- `heap_dijkstra`
- `selection_dijkstra` (mechanism label)
- `bellman_ford`
- `bfs` (unit-weight via `append`/`popleft`)
- `bfs` (unit-weight via `appendleft`/`pop`)
- `weighted_fifo`
- `dfs_bruteforce` with mutable path-local state added/removed
- `dfs_bruteforce` with immutable path state copied per branch
- SPFA-like FIFO with relaxation (`ambiguous`)

### 6.4 Test method

- Static classification of test-owned fixtures; no generated bodies.
- Behavioural cross-checks may run test-owned fixtures in bounded subprocesses, as the V3 suite does, but must never execute generated candidates.
- Names, comments, docstrings, and imports must be shown not to affect labels.
- Unreachable top-level and nested helpers must be shown not to affect labels.
- Conflicting genuine signals must produce `ambiguous`.

### 6.5 A–G, Q, and P interpretation

The A–G, Q, and P expectations above are **proposals**, not approved policy. The structural definitions in Part 1 are the normative basis. If Foued prefers a different label for a case (for example, treating a fixed-pair intermediate relaxation as a distinct mechanism), that decision must be recorded before it is encoded in tests.

---

## Part 7 - Frozen requirements, clarifications, amendments, and blocking decisions

### 7.1 Frozen V8 requirements to preserve exactly

| Requirement | Source |
|---|---|
| Eligible range `2 <= k <= 24`. | `GATE.md:85`; `run_gate.py:541` |
| `m_min = 4` distinct provenance groups per C level. | `GATE.md:84`; `run_gate.py:563` |
| Supported cell requires at least two C levels and at least four groups at **every** observed level. | `run_gate.py:554-564` |
| `other` excluded from supported cells and PASS group count, retained in audit totals. | `GATE.md:93`; `run_gate.py:546-547` |
| Supported-group total is the union across supported cells. | `run_gate.py:575` |
| Cross-C pairs are unique pairs of distinct groups, differing C, supported cells only. | `run_gate.py:575-588` |
| PASS: >=3 supported cells, >=2 distinct k, >=40 unique groups. | `GATE.md:87`; `run_gate.py:606-611` |
| WEAK: 1-2 supported cells. | `GATE.md:88` |
| Duplicate bodies identified by hash; first batch retained; counted once. | `GATE.md:50-56` |
| Futility and saturation rules unchanged. | `GATE.md:44-48, 90-91` |

### 7.2 Clarifications (no behaviour change intended)

- Count a group once in the cell union, not once per level.
- Count a group once in the supported-group union, not once per cell.
- No self-pairs across different C levels.
- Cross-C pairs only in supported cells and deduplicated.
- A cross-C pair is counted once per supported cell, not once per C-level contrast and not collapsed across different supported cells.
- Every observed level must meet `m_min`, including a third or later level.
- C levels are identified canonically by the integer `max_family_count`; the float quotient is display only.
- A duplicate body's provenance is the earliest record containing its hash in the route's declared record file (for V8, `attempts.jsonl` file order), not the chronologically earliest batch.
- Provenance is assigned per route (§4.1); all bodies from one generation response share one group, and a request identifier is used only where the protocol defines the request as the unit.
- Provenance identifiers are namespaced `(route, run_id, batch_or_request_id)`; identity does not authorise cross-route pooling (§4.1.1).
- Path-local DFS state may be mutable (add/remove) or immutable/copied per branch; global pruning is shared state that suppresses alternative paths.
- Scoring validity and provenance validity are independent; an invalid-provenance body keeps `k` only for audit.
- `k`, `max_family_count`, and the six `family_counts` are validated integers with the identities in §3.1; invalid measurements are excluded rather than coerced or repaired.
- The report must expose support-eligible and uncertain/mechanism-only totals separately.

### 7.3 Proposed amendments (require approval)

- Two-layer separation of mechanism classification and cell eligibility.
- Closed cell vocabulary with explicit mapping; no "all labels except other/ambiguous" admission.
- `weighted_fifo` and `selection_dijkstra` are mechanism-only by default.
- `ambiguous` is an explicit abstention label, never a cell label.
- Missing/invalid provenance is not an independent group; `untracked:<hash>` synthesis is prohibited for evidence.
- Provenance identifiers are namespaced `(route, run_id, batch_or_request_id)`; identity is not permission to pool across routes or runs (§4.1.1).
- Scoring validity and provenance validity are independent: an invalid-provenance body keeps `k` for audit only.
- False-positive avoidance takes priority over false-negative avoidance.
- V8's classifier is not a label oracle; only its cell rules are reference.
- Evidence pools are defined per `(route, run_id)`; no automatic cross-route or cross-run pooling, and no combined PASS total without an explicit amendment (D16).

### 7.4 Decisions requiring Foued's approval (blocking)

The following table records the reviewer's **recommended** dispositions. They are recommendations for the scientific decision record, not approvals: every decision below remains open until Foued signs it.

| Decision | Reviewer recommendation |
|---|---|
| D1 | Approve |
| D2 | Approve as the default preserved protocol |
| D3 | Mechanism-only |
| D4 | Mechanism-only |
| D5 | Approve as non-cell abstention |
| D6 | Approve the prospective amendment; never modify frozen V8 |
| D7 | Preserve the V8 executable behaviour |
| D8 | Preserve the V8 executable behaviour |
| D9 | Approve as a mandatory gate |
| D10 | Approve as a mandatory gate |
| D11 | Record as an established limitation |
| D12 | Confirm |
| D13 | Confirm |
| D14 | Decide after review |
| D15 | Approve the revised rule: every D1–D16 decision decided or explicitly deferred with rationale and scope; single-pool work only after the no-pooling default is approved and one pool is declared |
| D16 | Approve the default: one evidence pool per `(route, run_id)`; no automatic cross-route or cross-run pooling; any future pooling amendment must also satisfy D16.1 |
| D16.1 | Deferred under D15: blocks all cross-pool pooling; decide before approving any pooling amendment |

**D1.** Approve the two-layer architecture: mechanism classification separate from cell eligibility.

**D2.** Approve the closed cell vocabulary: `heap_dijkstra`, `bfs`, `bellman_ford`, `floyd`, `dfs_bruteforce`.

**D3.** Decide the status of `selection_dijkstra`: exclude from cells (default), merge into `heap_dijkstra`, or approve as a new cell category. The descriptive accuracy of the label does not by itself authorise a cell category. *Reviewer recommendation: mechanism-only; do not merge `selection_dijkstra` into `heap_dijkstra`, because a selection-based extract-min is not a heap-based implementation. A broader `dijkstra` category could be considered only through an explicit taxonomy amendment.*

**D4.** Decide the status of `weighted_fifo`: exclude from cells (default), map to `bfs`, or approve as a new cell category. The descriptive accuracy of the label does not by itself authorise a cell category. *Reviewer recommendation: mechanism-only; do not map `weighted_fifo` to `bfs`, because their distance-update mechanisms differ.*

**D5.** Approve `ambiguous` as a non-cell abstention label.

**D6.** Approve or reject a prospective amendment to the **subsequent H3 evidence protocol** that (i) forbids `untracked:<hash>` and any hash-derived provenance synthesis, and (ii) separates scoring validity from provenance validity as in §4.3. Frozen V8 remains the immutable historical comparison baseline: its source, hashes, tag, and behaviour are not modified, and the amendment is not recorded as a change to V8. The differential test must report two separate results — exact V8 behaviour on the domain where V8 is defined, and conformance to this approved amendment on amendment inputs — and both must pass independently.

**D7.** Confirm the union/no-self-pair/supported-only/deduplicated cross-C rules as normative (these are already V8 behaviour).

**D8.** Confirm that `m_min = 4` applies to every observed C level, rejecting the V3 two-level relaxation.

**D9.** Approve the differential test and the minimum fixture table as a merge gate for V4.

**D10.** Approve the classifier acceptance suite and the false-positive-over-false-negative priority.

**D11.** Confirm that V8's classifier is not a label oracle; only its cell rules are reference.

**D12.** Confirm V3 `bc029bc` remains an immutable rejected review record: not merged, its cell summaries not used, its new labels not admitted to H3 evidence.

**D13.** Confirm the published GLM pilot evidence is not reclassified or rewritten; it remains a frozen negative feasibility result for that sample.

**D14.** Decide where the approved record will live and how it will be frozen (hash/tag) after review.

**D15.** No V4 implementation starts until D1-D16 have each been decided or explicitly deferred, with the rationale and scope restriction recorded. Every decision affecting the proposed implementation scope must be decided before work begins. A single-pool implementation may proceed only after the no-pooling default is approved and one `(route, run_id)` evidence pool is explicitly declared. No cross-pool aggregation, support credit, or combined PASS is authorized. D16.1 remains deferred and blocks all cross-pool pooling.

**D16.** Approve the evidence-pool and cross-route pooling policy. Default: each `(route, run_id)` pair is a separate evidence pool; every supported cell, `m_min` check, cross-C pair, and PASS group total is computed within one pool; no cross-route or cross-run pooling occurs, and no combined PASS is calculated, unless a further explicit amendment authorizes it and defines which unit is independent and how runs combine. A `run_id` must be a stable generation-run identifier declared in that run's protocol (a run manifest or run identifier). A later documentation or audit commit hash may be recorded as supplementary provenance, but it must not redefine the generation run. V4 may be developed for one explicitly declared pool once D16 has been explicitly decided, normally by approving this default, under the D15 rule; any combination of pools requires a further explicit amendment.

**D16.1** Cross-pool duplicates are deferred to that amendment, not resolved by the per-pool rule. D16.1 is deferred under D15 and blocks all cross-pool pooling: it must be decided before any pooling amendment is approved. If pooling is later approved and the same exact body appears in more than one pool, the pooling amendment must state all four of the following before any combined cell table or PASS total is produced:

- (a) **Representation.** Whether that body appears once or more than once in the pooled dataset, and the unit that repetition would represent.
- (b) **Provenance retention.** How every original provenance record for the body is retained in the audit record, without collapsing distinct route, run, or batch history into a single synthesized group.
- (c) **Support credit.** Whether either provenance group, both, or neither receives support credit, and the independence argument for that choice. Default, pending the amendment: no support credit is assigned across pools and no combined PASS is computed.
- (d) **Conflict reconciliation.** How conflicting records for the same body — differing `k`, family counts, or measurement-integrity status across routes — are reconciled or reported.

The first record encountered must **not** automatically win across different pools. File-order precedence is a within-pool rule (§4.4); across pools it would let one route silently take ownership of another route's body, which is the outcome D16 exists to prevent. Until an amendment specifies (a)-(d), such a body is reported per pool and never deduplicated or merged across them.

---

## Part 8 - Disposition of V3 and preservation

- V3 commit `bc029bc` is an immutable review record. It is not merged.
- V3's cell summaries are not used for any scientific claim.
- V3's new labels (`weighted_fifo`, `selection_dijkstra`) may be cited as descriptive findings but do not enter H3 cells without approval.
- The GLM pilot's numerical result is unchanged: 12 bodies, 11 with `k = 0`, one eligible body (`request-03`, `k = 9`, `C = 4/9`, 21/30 correct), zero supported cells. The `weighted_fifo` description is more accurate for `request-03`, but it is not an approved cell category.
- The pilot remains a negative feasibility result for that sample. It does not establish that H3 is false.
- No frozen V8/V9 artifact, pilot evidence, manifest, protocol, or freeze is modified by this record.

---

## Appendix A - V8 executable references

- `base_label`: `h3-footprint-v8/run_gate.py:173-233`.
- `body_meta`: `h3-footprint-v8/run_gate.py:236-260`.
- `evaluate_body` provenance check: `h3-footprint-v8/run_gate.py:342-365`.
- Cell construction: `h3-footprint-v8/run_gate.py:541-588`.
- PASS/WEAK/FAIL: `h3-footprint-v8/run_gate.py:606-611`.
- GATE provenance and thresholds: `h3-footprint-v8/GATE.md:50-56, 77-95`.
- V8 freeze hashes: `h3-footprint-v8/FREEZE.json`.

## Appendix B - V8 provenance conflict detail

V8 has two missing-provenance paths:

1. No `attempts.jsonl` record for the body: `meta.get(h)` returns `{}`, `group_id` is `None`, and `evaluate_body` returns `_invalid_candidate(row, "missing_provenance")` (`run_gate.py:364-365`). This already prevents support.
2. `attempts.jsonl` record with no integer `batch_id`: `body_meta()` assigns `group_id = f"untracked:{h}"` (`run_gate.py:255`). This synthetic identifier would count as an independent group in V8's cell logic.

The proposed rule prohibits path 2 for evidence. This is an amendment, not a clarification, and it leaves frozen V8 unchanged. The exact-V8 differential must either exclude path-2 rows from the V8-domain comparison or record them as a documented amended difference in the amendment result; the two results are reported and pass separately (Part 5; D6).

## Appendix C - V3 review findings (condensed)

The independent review of `bc029bc` established:

- Bundle, commit, parent, tree, and three-file scope are authentic.
- 78 tests ran: 77 passed, 1 skipped (`symlink creation unavailable`).
- A: fixed-index Floyd -> `floyd` (false positive).
- B: unrelated deque -> `bfs` (false positive).
- C: unit BFS + weight bookkeeping -> `weighted_fifo` (false positive; regression vs V2).
- D: heap extract + unrelated update -> `heap_dijkstra` (false positive; regression vs V2).
- E1: numerical recursion called from a loop -> `other` (correct).
- E2: numerical recursion inside its own loop -> `dfs_bruteforce` (false positive).
- F: uncalled nested helper -> contributes a label (false positive).
- False negatives: `request-04` -> `other`; temp-form weighted FIFO -> `bfs`.
- Cell policy: open vocabulary, two-level `m_min`, per-level group summing, inflated cross-C pairs.

The 78-test pass does not cover the exact A-G shapes, which is why the suite passes despite these defects.

## Appendix D - Non-goals and prohibitions

This record does not:

- authorise V4 implementation;
- authorise candidate generation, model calls, or solver execution;
- modify V8, V9, the GLM pilot, any manifest, protocol, or freeze;
- merge or rebase V3;
- introduce fuzzy, semantic, or similarity-based deduplication of candidate bodies;
- declare any label, rule, or document frozen or approved.

The only valid next step after review is a recorded disposition of D1-D16 - each decision decided or explicitly deferred with its rationale and scope restriction recorded - followed by a V4 implementation that satisfies the differential and acceptance suites. V4 may be built for one explicitly declared evidence pool only after the no-pooling default is approved; D16.1 remains deferred and blocks all cross-pool pooling, so any cross-route or cross-run aggregation requires a further explicit amendment under D16 and D16.1.
