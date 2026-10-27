# H3 Footprint Gate, Version 2 Harness

Status: engineering candidate awaiting pre-candidate freeze. No candidate generation or model calls have occurred in this version. Do not generate candidates until FREEZE.json and the annotated version-2 tag exist.

## Purpose and version boundary

This version repairs the version-1 extraction and outcome-classification defects. The six-family SSSP probes, expected values, family mapping, three generators, and three prompt variants remain unchanged so that this engineering revision does not also change the sampling population.

Version 1 is marked INVALID_RUN. Its candidate outcomes and its import-restoration diagnostic are not version-2 results. This version reuses the existing family partition after a prior invalid-run diagnostic, so it is a repaired feasibility run on an already-observed instrument, not a pristine first confirmatory test of that family definition.

Out of scope: held-out inputs, held-out scoring, effect estimation, power analysis, prompt tuning after outcomes, and edits to research formulation branches.

## Task and instrument

Task: directed single-source/single-target shortest path with non-negative integer edge weights. The candidate interface is solve(n, edges, s, t), returning the minimum path distance as an integer or -1 if unreachable.

The instrument has 30 probes, six families in fixed order R, Z, A, I, S, U, and five probes per family. The unchanged definitions and expected values are in instrument.py and expected_values.json. Oracle agreement is checked by validate_controls.py before freezing.

## Candidate generation frame and budget

The generator models are unchanged:
- opencode/deepseek-v4.1-flash-free
- opencode/glm-5.3-flash-free
- opencode/mimo-v2.6-flash-free

The prompt variants remain direct, menu, and simple, on the original batch-number schedule. No generator or prompt variant is selected based on outcomes.

Budget: up to 400 batches, eight requested candidates per batch, 3,200 requested candidates maximum. This is a fixed cap. The target of 150 distinct valid candidates with k greater than zero is reported; it is not a reason to alter prompts, widen the budget, or relax thresholds. There is no early stop based on observed concentration support. The same full predeclared schedule is used for the run.

The executable path is not hard-coded. Set OPENCODE_EXE to the intended opencode executable or ensure opencode is available on PATH.

## Provenance and duplicate handling

All candidate bodies extracted from one generation response (one batch ID) belong to the same solver-side dependence group. Different batches get different group labels, but generator or prompt labels are not themselves proof of statistical independence. A normalized body hash identifies a unique candidate. If an identical body appears again, keep its first observed batch as provenance and count it only once. attempts.jsonl records each extracted candidate hash, including duplicates, so this rule can be audited.

## Extraction and invalid candidates

A code fence is accepted only if it parses as a Python module containing exactly one top-level synchronous function named solve. The complete module is retained, including imports, constants, and helper functions that precede solve. Syntax-invalid or ambiguous multi-solve blocks are not silently rewritten or partially extracted.

Before assigning k, the gate checks forbidden constructs, statically referenced unresolved global names, provenance, and module import/load in a bounded preflight process. Syntax errors, missing solve, import errors, undefined names, runner errors, and preflight timeouts are invalid candidates. They are reported separately and receive no k.

If preflight passes, each of the 30 probes runs in a fresh isolated subprocess with a five-second timeout. A wrong result, bool, non-integer, runtime exception, or per-probe timeout counts as a failure for that probe. If a subsequent probe process cannot load the module or produces malformed harness output, the candidate is invalidated and receives no k rather than being assigned a partial or synthetic k. Each probe is called at most once for a candidate.

## Support thresholds

These are engineering thresholds for structural feasibility, not power or effect-size claims. They are carried forward numerically from version 1:
- m_min = 4 distinct provenance groups per C level.
- Eligible range: 2 <= k <= 24. At k=1 and k=25..30, C cannot vary for this instrument.
- A supported cell is a (base algorithm, k) cell with at least two C levels, each represented by at least four distinct provenance groups.
- PASS: at least three supported cells across at least two distinct k values and at least 40 unique provenance groups across those supported cells.
- WEAK: one or two supported cells.
- FAIL: all other cases or the degeneracy rule below.

Degeneracy is reported three ways: among all valid candidates, among B1-rejected valid candidates (k>0), and among eligible valid candidates (2<=k<=24). The primary degeneracy rule applies the unchanged 0.80 cutoff to eligible candidates only. Including k=0 candidates in the primary denominator would let six zero family counts per passing candidate trivially inflate the statistic. If the eligible set is empty, report its primary degeneracy rate as null and fail for insufficient support, not for a statistic calculated on an empty set.

Group-pair counts are distinct pairs of provenance groups that share a base-algorithm/k cell and have at least one different-C cross-group comparison. Candidate rows are not independent groups. The output must report unique group counts, not just body counts.

## Required outputs

The result report and JSON must include:
1. Distribution of k and max_j f_j over valid candidates only.
2. Valid and invalid candidate counts and invalidity reasons; invalid candidates never receive k.
3. All-or-none rates for all valid, B1-rejected, and eligible candidates.
4. The complete base-algorithm/k cell table with candidate-body counts and distinct-group counts per C level.
5. Unique provenance groups in supported cells and distinct cross-group different-C group pairs.
6. The verdict under the thresholds above.

A PASS does not show that C predicts held-out performance. A FAIL means this sampling frame and instrument did not furnish the predeclared structural support. Neither verdict estimates power or effect size.
