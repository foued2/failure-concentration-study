# H3 Footprint Gate

**Status:** pre-candidate freeze candidate. This branch is not a protocol freeze until the annotated tag is created.

**Question:** does one newly defined six-family SSSP instrument produce enough same-`k`, different-`C` variation across independent, naturally generated solver groups to make H3 structurally estimable?

**Out of scope:** held-out inputs, held-out scoring, effect estimation, power, and any change to `review/concentration-formulation-2026-10-25` or `review/feasibility-protocol-2026-10-25`.

## Task

Directed SSSP with non-negative integer weights. `solve(n, edges, s, t)` returns the minimum total weight of a directed path from `s` to `t`, or `-1` if `t` is unreachable. Nodes are `0..n-1`; `edges` contains `(u,v,w)` tuples; parallel edges and self-loops may occur.

## Instrument

Six families, five probes per family, 30 probes total. Family order is `R,Z,A,I,S,U`.

| Family | Construct |
|---|---|
| R | Depth of relaxation required along a long chain of dependencies. |
| Z | Termination and distance correctness around zero-weight reachability and zero cycles. |
| A | Choice among parallel and alternative source-to-target routes. |
| I | Robustness to arbitrary node labels and interior source/target positions. |
| S | Shortcut discovery in dense graphs with many competing edges. |
| U | Correct unreachable-target sentinel behavior. |

Each probe is assigned to one family by construction. The five probes in a family exercise different manifestations of that construct. Probe definitions and both oracles are frozen in `instrument.py`. All 30 probes passed agreement between Dijkstra, Bellman-Ford, and exhaustive simple-path enumeration before this gate was frozen.

## Candidate population

Three generators:

- `opencode/deepseek-v4.1-flash-free`
- `opencode/glm-5.3-flash-free`
- `opencode/mimo-v2.6-flash-free`

Each request asks for eight independent first-attempt implementations. Three predeclared prompt variants are used: direct, algorithmic-menu, and minimal. The schedule is fixed by batch number and does not depend on outcomes.

**Provenance group:** one distinct normalized source body. No repairs or revisions are generated. Fresh bodies are separate groups. Identical body hashes collapse to one candidate and one group. Generator and prompt labels are sensitivity metadata, not evidence of statistical independence.

**Budget:** at most 72 generation batches, eight requested bodies per batch, 576 requested bodies. Target: 150 distinct `k>0` bodies, or the budget cap. No replacement sampling and no prompt tuning after outcomes.

## Labels and features

**Base-algorithm label:** assigned from source text before any probe outcome is observed. Rubric: `heap_dijkstra`, `bellman_ford`, `bfs`, `floyd`, `dfs_bruteforce`, `other`.

**Failure rules:** crash, timeout, wrong integer, `bool`, non-integer, or missing `solve` counts as a failed probe. Each candidate is executed once in an isolated subprocess with a hard timeout. Probes are never added, removed, or swapped after candidate generation.

**Eligible range:** `k = 2..24`. `k=0` is excluded; `k=1` and `k=25..30` cannot vary `C` in this instrument.

## Structural thresholds

These are predeclared engineering rules, not statistical power requirements.

- `m_min = 4` distinct provenance groups per `C` level.
- **Supported cell:** one `(base algorithm, k)` cell with at least two distinct `C` levels, each represented by at least four groups.
- **PASS:** at least three supported cells across at least two distinct `k` values, with at least 40 unique provenance groups across those cells.
- **WEAK:** one or two supported cells. Only the predeclared one-task expansion is allowed, with no threshold changes.
- **FAIL:** all other cases, or failure of the degeneracy rule.

**Degeneracy rule:** across all candidate-family rows, report the fraction with family count `0` or `5`. If that fraction exceeds `0.80`, the instrument fails regardless of other counts.

## Required output

1. Distribution of `k` and `max_j f_j`.
2. All-or-none fraction.
3. `(base algorithm, k)` table with `C` levels and group counts.
4. Number of unique provenance groups in supported cells and number of distinct cross-group pairs with same `k` and different `C`.
5. Verdict under these frozen thresholds.

A PASS does not show that `C` predicts held-out performance. A FAIL is a finding about this instrument.

## Freeze

The annotated tag must point to the commit containing this file, `instrument.py`, `generate.py`, `run_gate.py`, `expected_values.json`, and `coherence_review.json`. The tag record must include the full target SHA, a UTC timestamp, and SHA-256 hashes of those artifacts. No candidate exists at freeze time.

## Authorization boundary

This gate is footprint-only. It does not authorize held-out inputs, held-out scoring, effect estimation, power calculation, a PR, a merge, or edits to the existing review branches.
