# H3 Footprint Gate, Version 5 Harness

Status: engineering candidate awaiting pre-candidate freeze. No candidate generation or model calls have occurred in this version. Do not generate candidates until FREEZE.json, the annotated version-5 tag, and the execution-isolation check all pass.

## Purpose and version boundary

This version carries forward the version-2 extraction and outcome-classification repairs, the version-3 degeneracy and futility rules, and the version-4 structural classifier, and changes one further protocol element:

1. Primary degeneracy is the saturation rate, the fraction of eligible candidates with max_j f_j = 5. The version-2 per-family all-or-none rate is retained only as a secondary reported statistic. At low k the all-or-none rate treats a two-probe single-family failure, such as [2,0,0,0,0,0], as six all-or-none family counts and can exceed 0.80 without any fully failed family.
2. A predeclared futility rule stops generation when eligible provenance groups fall below a linear pace to the 40-group PASS target.
3. Algorithm classification for the supported-cell key is structural and conservative, rather than a raw substring search. Comments, docstrings, unused imports, and unused helpers cannot change a solver's cell; ambiguous or unrecognized structure is labelled other.
4. Candidates labelled other remain in overall counts, distributions, degeneracy rates, and futility, but cannot form a supported cell or contribute to the PASS group count. Pooling unidentified algorithms would otherwise create a false PASS from a mixture of distinct approaches. Supported cells and the PASS group count use identified algorithms only.

The six-family SSSP probes, expected values, family mapping, three generators, three prompt variants, batch schedule, and support thresholds remain unchanged.

Version 1 is marked INVALID_RUN. Its candidate outcomes and import-restoration diagnostic are not version-5 results. Versions 2, 3, and 4 are frozen but were not run. This version reuses the existing family partition after a prior invalid-run diagnostic, so it is a repaired feasibility run on an already-observed instrument, not a pristine first confirmatory test of that family definition.

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

Budget: up to 400 batches, eight requested candidates per batch, 3,200 requested candidates maximum. This is a fixed cap. The target of 150 distinct valid candidates with k greater than zero is reported; it is not a reason to alter prompts, widen the budget, or relax thresholds. The same full predeclared schedule is used for the run, subject only to the predeclared futility rule.

Generation is executed in predeclared segments of 100 batches (batch ranges 0-99, 100-199, 200-299, 300-399). After each completed segment, run_gate.py must be executed. If the futility rule has triggered, generation stops and the current data are evaluated. Segmenting does not change the model or prompt assigned to any batch.

The executable path is not hard-coded. Set OPENCODE_EXE to the intended opencode executable or ensure opencode is available on PATH.

## Futility rule

At batch checkpoints 100, 200, and 300, count distinct provenance groups that contributed at least one eligible candidate (2 <= k <= 24) from batches with batch_id below the checkpoint. Stop if the count is below 10, 20, or 30 respectively. These minima are a linear pace to the 40-group PASS requirement at batch 400. The rule is evaluated automatically by run_gate.py from attempts.jsonl and the evaluated bodies; it is not a discretionary judgment.

Futility is a stop rule for generation, not a claim about H3. A triggered checkpoint yields verdict FAIL with reason futility_checkpoint_batch_<n>. If no checkpoint triggers, the run continues to the 400-batch cap and the support thresholds decide the verdict.

## Provenance and duplicate handling

All candidate bodies extracted from one generation response (one batch ID) belong to the same solver-side dependence group. Different batches get different group labels, but generator or prompt labels are not themselves proof of statistical independence. A normalized body hash identifies a unique candidate. If an identical body appears again, keep its first observed batch as provenance and count it only once. attempts.jsonl records each extracted candidate hash, including duplicates, so this rule can be audited.

## Extraction and invalid candidates

A code fence is accepted only if it parses as a Python module containing exactly one top-level synchronous function named solve. The complete module is retained, including imports, constants, and helper functions that precede solve. Syntax-invalid or ambiguous multi-solve blocks are not silently rewritten or partially extracted.

Before assigning k, the gate checks forbidden constructs, statically referenced unresolved global names, provenance, and module import/load in a bounded preflight process. Syntax errors, missing solve, import errors, undefined names, runner errors, and preflight timeouts are invalid candidates. They are reported separately and receive no k.

If preflight passes, each of the 30 probes runs in a fresh isolated subprocess with a five-second timeout. A wrong result, bool, non-integer, runtime exception, or per-probe timeout counts as a failure for that probe. If a subsequent probe process cannot load the module or produces malformed harness output, the candidate is invalidated and receives no k rather than being assigned a partial or synthetic k. Each probe is called at most once for a candidate.

## Execution isolation

Candidate bodies are untrusted generated code. They must not execute on the development host.

Execution is separated into two stages, specified in RUNBOOK.md:

1. Generation stage: OpenCode runs where it has the network access it needs. generate.py only parses returned text and writes bodies; it does not import or execute candidate code.
2. Evaluation stage: run_gate.py, probe_worker.py, instrument.py, expected values, and the generated bodies are staged into a sandbox with networking disabled and no host repository, credential directory, or development checkout exposed. run_gate.py must be started inside that environment, not on the host. The ordinary host shell does not move subprocesses into Windows Sandbox by itself.

Before any candidate is evaluated, the operator must record an execution-isolation check in isolation-report.json and confirm that the actual evaluation ran inside the sandbox. A static import/call denylist alone is not an isolation boundary. If no such environment is available, the run must not start.

The isolation check must include a harmless probe showing that a candidate cannot write outside its scratch directory and cannot reach the network, the mechanism used (for example Windows Sandbox with networking and clipboard disabled, a restricted container, or a dedicated VM), and evidence that run_gate.py itself executed inside that environment (sandbox hostname or marker, staged paths, and the network-blocked probe result). The check is recorded before generation and is part of the freeze evidence.

## Algorithm classification

Each valid candidate is assigned a base-algorithm label used only to form (base algorithm, k) cells. Classification is structural and conservative. The gate parses the module and restricts analysis to solve and the helpers actually reachable from solve. It requires an imported and actually called heappush/heappop for heap_dijkstra; an imported deque called with popleft or appendleft for bfs; an edges loop nested inside a range loop for bellman_ford; three nested loops with 2D subscripting for floyd; and a recursive reachable function for dfs_bruteforce. If zero or more than one signal is present, the label is other. Comments, docstrings, unused imports, and unused helpers cannot affect the label. Labelling other is conservative: it can only make support harder to obtain, not easier.

## Support thresholds

These are engineering thresholds for structural feasibility, not power or effect-size claims. They are carried forward numerically from versions 1 and 2:
- m_min = 4 distinct provenance groups per C level.
- Eligible range: 2 <= k <= 24. At k=1 and k=25..30, C cannot vary for this instrument.
- A supported cell is a (base algorithm, k) cell with at least two C levels, each represented by at least four distinct provenance groups.
- PASS: at least three supported cells across at least two distinct k values and at least 40 unique provenance groups across those supported cells.
- WEAK: one or two supported cells.
- FAIL: all other cases, the futility rule above, or the degeneracy rule below.

Degeneracy is reported as the saturation rate (fraction with max_j f_j = 5) among all valid candidates, among B1-rejected valid candidates (k>0), and among eligible valid candidates (2<=k<=24). The primary rule applies the unchanged 0.80 cutoff to the eligible saturation rate. The version-2 per-family all-or-none rates are reported for continuity but do not determine the verdict. If the eligible set is empty, report its primary degeneracy rate as null and fail for insufficient support, not for a statistic calculated on an empty set.

Only eligible candidates with an identified base algorithm form cells. Candidates labelled other are excluded from the cell table, the supported-cell count, the distinct supported-k set, and the unique PASS group count. They remain in eligible-body and eligible-group totals, the k and max_j f_j distributions, the saturation rates, and the futility pace. The report must show both the support-eligible and other-labelled totals so the exclusion is auditable.

Group-pair counts are distinct pairs of provenance groups that share a base-algorithm/k cell and have at least one different-C cross-group comparison. Candidate rows are not independent groups. The output must report unique group counts, not just body counts.

## Required outputs

The result report and JSON must include:
1. Distribution of k and max_j f_j over valid candidates only.
2. Valid and invalid candidate counts and invalidity reasons; invalid candidates never receive k.
3. Saturation rates for all valid, B1-rejected, and eligible candidates, plus the secondary all-or-none rates.
4. Futility checkpoints, completed batch count, and whether a stop was triggered.
5. Support-eligible and other-labelled eligible body and group totals.
6. The complete base-algorithm/k cell table (identified algorithms only) with candidate-body counts and distinct-group counts per C level.
7. Unique provenance groups in supported cells and distinct cross-group different-C group pairs.
8. The verdict under the thresholds above.

A PASS does not show that C predicts held-out performance. A FAIL means this sampling frame and instrument did not furnish the predeclared structural support. Neither verdict estimates power or effect size.
