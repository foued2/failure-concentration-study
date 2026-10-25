# Next-Study Design Amendment

Status: **`DESIGN_AMENDMENT_PREPARATION_ONLY_NO_AUTHORIZATION`**

> **NOT APPROVED FOR LAUNCH — PRESERVED FOR REUSE.** The companion power grid
> used infeasible `C = 1.0` cells at `k = 6, 12, 24` under the five-probe family
> structure, so its numerical estimates are invalid for operational planning.
> This amendment is not a launch design; its continuous score, execution
> eligibility, and structural criteria remain reusable. See
> `next-task/11_CLOSURE_RECORD_2026-10-22.md`.

Date: 2026-10-22

Baseline commit: `766b3788d22b8591b24020753f71fd9a17875d7a`

This amendment is additive to
`next-task/08_RESEARCH_DECISION_MEMO_2026-10-22.md`. It resolves only the
run-count ambiguity left open in that memo and specifies the design that a later
preregistration must use. It does not modify the memo, the expression
preregistration, the expression result, the banks, or the expression verdict. It
selects no task, authorizes no generation, and makes no model calls.

## 1. Scope and authority

Foued's 2026-10-22 clarification governs the study count:

- Completed natural-solver feasibility runs: **3** — Codex SSSP, Gemini SSSP, and
  Gemini expression.
- The next study would be the **fourth provider run** and the **third task-level
  study**.
- At most **one** new task-level study may be prepared. It is final for this
  route.
- The conditional sentence in memo `08` about an alternative provider-run count is
  resolved by this clarification. The memo itself remains unchanged.

This document records preparation requirements only. It is not a task-selection
decision, a task preregistration, a calibration result, or a launch
authorization. No task is selected or generated here.

If the next task does not produce a qualifying fixed-`k`, different-`C`
comparison with evaluation separation, the natural-solver route ends. There is no
fourth task, no fallback task, no search across tasks, and no outcome-dependent
retry.

## 2. Frozen metric definitions

The existing expression metric definitions remain the reference definitions:

- `k` is the total number of failed diagnostic probes.
- For `k > 0`, `C = max_f(family_failure_count[f]) / k`, where the maximum is over
  the task's frozen semantic families.
- For `k = 0`, `C = 0`.

The next study must freeze its own family list, probe assignment, and `C`
definition before generation. It must not reuse expression bank inputs. If the
task uses a different concentration definition, that definition must be frozen in
the task preregistration and must not be selected from preliminary outcomes; this
amendment assumes the existing `C` definition unless a later preregistration
explicitly replaces it.

## 3. Primary outcome: evaluation score

Replace the binary all-or-nothing evaluation outcome with a continuous score on a
larger, independent evaluation sample.

### 3.1 Evaluation sample

- The evaluation bank is separate from the diagnostic bank, with disjoint inputs.
- The task must expose at least **six** independently specifiable semantic
  families or clauses. Each family must have:
  - a separately described defect mechanism;
  - at least five diagnostic probes;
  - a disjoint evaluation block;
  - a deterministic host-side expected value and an independent oracle check.
- The evaluation sample is family-balanced. For `F` frozen families, allocate
  `N_eval / F` inputs per family, with family sizes differing by at most one when
  `N_eval` is not an exact multiple of `F`.
- `N_eval = 200` is the reference design; for `F = 6`, the family sizes are
  `34, 33, 33, 33, 33, 34`. If exact equal blocks are preferred, use
  `N_eval = 240` (40 per family) and rerun the power calculation at that value
  before authorization. The planning simulation uses `N_eval = 200`.
- The evaluation inputs, family labels, expected values, seed, generator code,
  output contract, and bank hashes are frozen before generation.

### 3.2 Score

For an execution-eligible body `i`:

```text
S_i = (number of correct evaluation inputs) / N_eval
```

`S_i` is a proportion in `[0, 1]`. The primary descriptive summaries are the
per-body score, the per-`(k, C)` mean and distribution, and the number of
evaluation-correct bodies. An all-correct indicator may be retained only as a
secondary descriptive field; it is not the primary outcome.

### 3.3 Primary analysis

The planned analysis is a stratified within-`k` test of the association between
`C` and `S`:

- include only execution-eligible bodies;
- for each `k` with at least two observed `C` levels and at least two bodies per
  level, center `C` and `S` within that `k`;
- define the statistic as the sum over eligible `k` of the within-`k` centered
  `C`-`S` cross-product;
- obtain a two-sided p-value by permuting `S` within `k`, preserving the observed
  `C` and `k` marginals;
- use at least 999 permutations for the final study unless a larger frozen count
  is specified. The planning simulation used 99 permutations for power and 199
  for null calibration; those counts are not sufficient for a final p-value.
- report the per-`k` slopes, the pooled statistic, the number of contributing
  `k` levels, and the score difference between the highest and lowest
  prespecified `C` levels.

The test is exploratory. It does not authorize a confirmatory, population,
prevalence, or causal claim. A p-value is reported as part of the feasibility
evidence and is not a substitute for the fixed-`k`, behavioral-diversity
qualification rule.

### 3.4 Qualification

A statistically detectable association is not by itself a qualifying comparison.
The fixed-`k` group must contain at least two `C` levels, each supported by at
least two **behavior-distinct** bodies under the prospective diagnostic behavior
profile. Source-distinct but behaviorally identical bodies do not satisfy the
behavioral requirement. Report source-distinct and behavior-distinct counts
separately, along with per-`C` score distributions and the high-low score
difference. The expression pilot's identity rule and verdict remain unchanged.

## 4. Execution eligibility

The next study must distinguish semantic failure from infrastructure failure
before scoring.

### 4.1 Execution-eligible body

A body is execution-eligible only if:

1. its source passes the frozen static screen;
2. it produces a valid host-authoritative outcome for every diagnostic probe;
3. it produces a host-authoritative outcome for every evaluation input; an
   input-specific exception raised by the body is recorded as an incorrect
   outcome, not as missing data;
4. every row is tree-terminated, and no suite-level runner timeout, transport
   failure, or runtime/API incompatibility prevents the suite from completing;
5. bank hashes, raw captures, row identities, and source screens validate against
   the freeze record.

### 4.2 Classification rules

- **Execution-ineligible:** no valid diagnostic outputs, or no valid evaluation
  outcomes because a whole evaluation suite crashes, the runtime is incompatible,
  the sandbox or runner fails, or a host-side transport/contract error prevents
  valid rows. No `S_i` is assigned. The record remains in the manifest and is
  excluded from the primary semantic contrast.
- **Semantic failure:** a validly executed body returns a wrong value, wrong type,
  invalid output, or raises an input-specific exception. The affected evaluation
  input is scored incorrect. It is not missing data and is not an execution
  exclusion.
- **Runner-versus-body adjudication:** if only part of a suite is missing, the
  adjudicator must record whether the missingness is attributable to the runner
  or to the body. Ambiguous cases are execution-ineligible and cannot be used to
  support a qualifying contrast. The adjudication log is part of the raw record.
- **Duplicate bodies:** retained and reported. They are not replacement samples.
  Determine behavioral identity from the prospectively frozen diagnostic
  behavior profile, not from source hashes alone.
- **Provider outage or API interruption:** an operational interruption, not a
  scientific negative. It must be reported as such. It does not authorize endless
  retries or a new task.

The three expression `k=30` crash bodies demonstrate why this distinction is
mandatory: a whole-suite crash is not a semantic failure count and must not be
treated as six defect families or as `C` evidence.

## 5. Structural task-selection criteria

A candidate task is eligible only if it satisfies all of the following before any
model call:

1. **Independent semantic clauses.** At least six clauses, families, or
   mechanisms that can be specified separately and tested separately.
2. **Separately testable defects.** For each clause, at least five diagnostic
   probes that isolate that clause and a disjoint evaluation block.
3. **Plausible partial implementations.** A documented space of at least three
   non-catastrophic partial implementations that pass some clauses and fail
   others. These are hand-built for calibration and are not model-generated.
4. **Deterministic oracle.** A host-side expected value for every input, plus an
   independent oracle implementation that agrees on the full bank.
5. **Exact output contract.** No tolerance, no hidden normalization, no
   post-hoc coercion. The contract states types, serialization, and error
   behavior.
6. **Bounded execution.** Each probe has a fixed worker timeout, memory cap, and
   no network. The suite is cheap enough for the declared budget.
7. **Pinned runtime and API.** The Python version, sandbox image, and required
   standard-library API surface are pinned in the task specification and freeze
   record. The expression `ast.Num` failure must not recur silently.
8. **Claim separation.** The task is structurally distinct from SSSP and from the
   expression task; it is not a surface-difficulty variant.

Tasks are selected by the frozen rubric, not by preliminary model failure rates,
per-body outcomes, or a search for a favorable contrast. If no candidate
satisfies all criteria, stop; do not weaken the rubric.

## 6. Calibration gate

Before generation, a no-model calibration must pass:

- reference implementation: all diagnostic probes and all evaluation inputs
  correct;
- six prespecified faulty implementations: every target-family diagnostic probe
  and every target-family evaluation input fails, with no non-target family
  failures;
- at least three partial implementations that pass some families and fail others;
- every row tree-terminated and not timed out;
- strict output adapter, frozen source and bank hashes, and the pinned runtime;
- zero model calls and zero generation attempts.

Because the new evaluation block is larger than five inputs per family, the
requirement is "all target-family inputs fail," not the old five-input wording.
The expression calibration and its five-input-per-family records remain
unchanged. The calibration panel is separate from the evaluation bank and does
not contribute to any body's `S_i`. Calibration proves bank discrimination. It
does not prove that natural solvers will produce the calibrated defect
mechanisms.

## 7. Generation conditions and cap

The generation design must be frozen before the first request:

- At most **two** generator/prompt conditions. Each condition fixes the provider,
  model identifier, backend settings, prompt, output contract, seed where
  available, and request cap.
- Exactly **100 one-shot requests per condition** is the planning ceiling under
  review. It is not an invitation to increase the cap after seeing results.
- No retries, no replacement sampling, no prompt tuning, no body selection, no
  outcome-dependent stopping.
- Conditions are reported and analyzed separately. Do not pool conditions unless
  a pooling rule is registered before generation.
- A provider outage is an operational interruption. The preregistration must
  state whether an interrupted condition may be resumed and how; it may not be
  used to justify an unlimited retry loop.
- The task, prompt, condition list, cap, banks, runtime, scoring code, and
  analysis code are frozen before generation.

If the power report shows that 100 requests per condition cannot support the
smallest effect of interest at the declared error rate, the natural route should
stop. The cap is not to be raised quietly.

## 8. Power and feasibility requirements

Before any generation authorization, the following must be reported:

- false-positive rate under the conditional-independence null
  `S ⟂ C | k`;
- power for each prespecified alternative, including a linear `C` effect and
  score overdispersion;
- required bodies per `(k, C)` cell and total bodies;
- sensitivity to duplicate bodies, execution-ineligible bodies, and partial-suite
  loss;
- the planned decision rule and its operating characteristics at the declared
  cap;
- an explicit statement that the analysis is conditional on the generator
  producing populated cells.

The power calculation is planning evidence, not evidence that a generator will
produce the required cells or effect. A null simulation result cannot be used as
a substitute for a natural run or as evidence about natural solvers.

## 9. Stop and terminal rules

The next task is the third and final task-level natural-solver feasibility study.
The route ends if any of the following occurs:

- no task satisfies the frozen structural rubric;
- calibration fails;
- the fixed cap cannot support adequate power for the smallest effect of
  interest;
- the run produces no qualifying fixed-`k`, different-`C` comparison with
  behavioral diversity and evaluation separation;
- the run is dominated by execution-ineligible bodies or duplicate behavior
  profiles such that the planned contrast cannot be estimated.

A provider outage is not a scientific negative, but it does not create another
task-level study. A failed next task does not authorize a fourth task, a fallback
task, or a post-result task search.

## 10. Claims and preservation

A qualifying result would support only a procedure-specific statement: under the
declared task, conditions, banks, prompt, runtime, and execution procedure, the
procedure produced a fixed-`k` comparison with differing `C` and differing
evaluation score. It would not establish a general concentration-correctness
relation, a prevalence estimate, a causal effect, or a result about natural
solvers in general.

A null result would support only: this procedure did not produce the required
comparison within the declared cap. It would not establish that concentration is
unrelated to correctness.

Preserved without modification:

- the frozen expression result and `REPEATED_K_BUT_NO_C_SEPARATION` verdict;
- `next-task/03_PILOT_PREREGISTRATION_2026-10-22.md`,
  `next-task/03A_PREREGISTRATION_AMENDMENT_2026-10-22.md`,
  `next-task/03B_OUTPUT_CONTRACT_AMENDMENT_2026-10-22.md`, and
  `next-task/03C_PILOT_LAUNCH_PRECONDITIONS_2026-10-22.md`;
- `next-task/04_READINESS_REPORT_2026-10-22.md`,
  `next-task/05_EXPRESSION_RUNNER_READINESS_2026-10-22.md`, and
  `next-task/06_EXPRESSION_PILOT_RESULT_2026-10-22.md`;
- the expression run directory, attempts, raw captures, and `PILOT_RESULTS.json`;
- `next-task/banks/diagnostic.json`, `next-task/banks/evaluation.json`, and
  `next-task/banks/FREEZE.json`;
- `next-task/07_EXPRESSION_PILOT_AUDIT_2026-10-22.md` and
  `next-task/08_RESEARCH_DECISION_MEMO_2026-10-22.md`;
- `README.md` and all closed SSSP runs.

No generation, bank change, task selection, or launch is authorized by this
amendment.
