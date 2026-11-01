# ANALYSIS_SPEC.md — LC518 150-Body Construction Study

**Study package:** lc518-150
**Version:** 1.0 (FROZEN)
**Frozen by:** GLM
**Freeze date:** 2026-11-01
**Authorization:** GLM_WORK_ORDER.md v1.0 (commit `4608922`), §5 item 2, §9, §10.
**Freeze attestation:** This document is frozen before any solver source exists and before
any candidate outcome is observed. No fitting, prediction, or dynamic evaluation is
authorized in the construction phase (work order §13); everything below is a
preregistered plan for a later, separately authorized analysis phase. Nothing in this
document upgrades design intentions into findings.

---

## 1. Status labels that govern all reporting

- Every candidate body: `GENERATED_NOT_EXECUTED`.
- Every intended mutation: `DESIGNED_NOT_VERIFIED`.
- Static inspection cannot establish that a mutant is semantically different from S0,
  that a defect is triggered, that two defects interact, or that an intended-correct
  parent is correct over the full domain (work order line 202). The phrase "mutation
  isolation verified" is prohibited for static evidence.

## 2. Definitions

- **Correctness** of one solver/input execution follows LC518_TASK_CONTRACT.md §5:
  the call completes under the pinned execution conditions, the returned object has
  exact type `int`, and its value equals the reference count. `bool` is not accepted.
- **Statuses (work order §8):** `PASS`, `FAIL`, `UNRESOLVED`.
  `UNRESOLVED` is neither PASS nor FAIL and is counted separately, always.
- **Failure manifestations (typed, never collapsed in the retained record):**
  wrong answer, invalid return type, exception, timeout/resource breach, other
  explicitly defined status. Binary summaries may be derived later; the typed record
  remains authoritative. Timeout/resource classification is impossible until a separate
  execution protocol declares runtime, memory budget, and timeout rule (contract §5;
  work order §8) — no such budget exists in this phase and none is invented here.
- **Resolved record:** a record with status PASS or FAIL. **Coverage** of a set =
  resolved records / total records in the set.
- **Observed failure vs. injected defect:** outcomes are observations; mutation labels
  are construction intents. A mutation's intended label is never evidence that the
  resulting solver exhibits any behaviour (work order §8).

## 3. Estimand E1 — matched within-parent correctness contrasts (primary)

For parent group g ∈ {1..30} and version v ∈ {S0, SA, SB, SAB, S-extra}:

    L(g, v) = mean over the 80 frozen held-out records of 1[status(record) = FAIL]

All five versions of a parent use identical held-out records, identical oracle outputs,
and identical execution conditions (work order §9). Because unresolved records are
neither pass nor fail, L is reported on the resolved subset with coverage, together with
worst/best bounds over unresolved records (worst: all unresolved are FAIL; best: all are
PASS). No unresolved record is silently counted either way.

Reported per parent group:

- A-only contrast: `L(g, SA) − L(g, S0)`
- B-only contrast: `L(g, SB) − L(g, S0)`
- S-extra contrast: `L(g, S-extra) − L(g, S0)`
- Pair contrast: `I(g, A, B) = L(g, SAB) − L(g, SA) − L(g, SB) + L(g, S0)`

Per-input interaction contrast, preserved in full (never summarized away):

    i(g, A, B, x) = loss(g, SAB, x) − loss(g, SA, x) − loss(g, SB, x) + loss(g, S0, x)

where `loss(g, v, x) = 1[status(g, v, x) = FAIL]` for resolved x (undefined for
unresolved x, reported as such).

**Cancellation rule:** aggregate I = 0 does not mean "no interaction"; positive and
negative per-input interactions can cancel. Both the aggregate and the full per-input
distribution are reported (work order §9).

**Status of E1:** defect interactions are UNKNOWN until all four matched versions have
been dynamically evaluated under the same declared conditions. Before that point the
formulas are planned estimands, not measured results. Because most mechanism pairs occur
on only one parent, the 28-pair screen is exploratory with only limited replication (two
preselected pairs); nothing in this design estimates general interaction laws across
solver implementations.

## 4. Feature definitions (frozen before any mutation; work order §10)

For each solver and each diagnostic stratum D1–D8 (BANK_DESIGN.md §6), computed only from
diagnostic-bank records:

| Column | Definition |
|---|---|
| `d_pass_s` | count of PASS records in stratum s |
| `d_wrong_answer_s` | count of FAIL records whose manifestation is wrong answer, in s |
| `d_invalid_return_s` | count of FAIL records whose manifestation is invalid return type, in s |
| `d_exception_s` | count of FAIL records whose manifestation is exception, in s |
| `d_unresolved_s` | count of UNRESOLVED records in s (coverage variable, never a failure count) |
| `d_meandev_s` | mean of |returned − expected| over wrong integer outputs in s; `NaN` + `defined=False` when undefined |
| `d_maxdev_s` | max of |returned − expected| over wrong integer outputs in s; `NaN` + `defined=False` when undefined |

Aggregate baseline columns: `k_fail` (total diagnostic FAIL count), `k_unresolved`
(total diagnostic UNRESOLVED count), `family` (parent algorithm family Z from
PARENT_DESIGN.md §4 — prespecified context variable), `coverage_diag`.

Reserved (null in this phase, populated only after an execution protocol fixes budgets):
timeout/resource counts per stratum. The column list is frozen; a reserved column that
stays null is reported as null, not dropped silently.

**Prohibited as predictive features, without exception:** raw input IDs, raw output text,
source code, mutation labels, version-role labels, sealed-manifest fields, solver IDs as
features. The parent-group identifier may be used **only** to form validation folds and
cluster summaries. Raw outputs and traces are preserved separately as evidence
(work order §10).

## 5. Estimand E2 — held-out correctness score Q

Target: the solver's mean correctness score on the fixed 80-record held-out bank,

    Q = (1/80) · Σ_records 1[correct per contract §5]

If any held-out outcome is unresolved, the analysis reports: Q_resolved (over resolved
records only), coverage, and the worst/best possible score bounds implied by the
unresolved records. Unresolved outcomes are never silently counted as wrong, and never
silently discarded without reporting coverage (work order §10).

## 6. Estimand E3 — exploratory baseline-vs-enriched prediction (secondary)

**Question:** does diagnostic failure information predict held-out correctness Q better
than the total diagnostic failure count and declared context? This is a prediction
question about correctness, distinct from E1's mutation contrasts; the two are never
merged, and a predictive gain is never described as a causal effect of a mutation.

**Arms (frozen):**

- **Baseline arm:** ridge regression on `k_fail`, `k_unresolved`, `family`.
- **Enriched arm:** ridge regression on all baseline columns plus the per-stratum
  columns of §4 (`d_pass_s`, `d_wrong_answer_s`, `d_invalid_return_s`, `d_exception_s`,
  `d_unresolved_s`, `d_meandev_s` + `d_meandev_s_defined`, `d_maxdev_s` +
  `d_maxdev_s_defined`, for s = D1..D8).

**Procedure (frozen; work order §10 verbatim constraints):**

1. Model class: ridge linear regression with an intercept; candidate penalties
   alpha ∈ {0.1, 1, 10, 100}.
2. Numeric feature standardization and categorical encoding are fitted on training data
   only, inside every fold.
3. Outer validation: leave one complete parent group out per fold → 30 outer folds; all
   five bodies of a parent remain together in the held-out fold.
4. Inner tuning: five-fold group-wise cross-validation over the remaining parent groups;
   alpha chosen by lowest inner-fold mean squared prediction error, separately inside
   each arm's training data. Both arms use the same fold definitions and the same alpha
   grid.
5. No post-hoc feature selection, model switching, fold changes, or feature engineering
   after outcomes are inspected.
6. Loss: squared prediction error for Q. Overall result: first average squared
   prediction error within each held-out parent group, then average equally across the
   30 parent groups. All 30 group-level paired differences are also reported.
7. The paired group-level difference is baseline MSE − enriched MSE; positive values
   favour the enriched arm.
8. **Exploratory only.** With 30 parent groups, no power calculation and no
   meaningful-effect threshold are authorized (work order line 66). No invented delta,
   lower-confidence-bound rule, or p-value decision rule is applied; no confirmatory
   support is claimed. The report presents the 30 group-level results and the
   descriptive overall difference, with all coverage figures.
9. **One frozen analysis pass.** Stop after it. If data, coverage, or unresolved
   outcomes make a fold or arm not estimable under the frozen procedure, report
   `NOT_ESTIMABLE` with the precise reason. Do not collect more data, change features,
   or rerun with a replacement model automatically.
10. Sanity constraint inherited from the earlier study's frozen feasibility criterion:
    the comparison is meaningful only where the held-out outcomes vary within parent
    groups; if every body of every group scores identically, the correct report is
    zero-variance, not a prediction result.

## 7. Reporting rules

1. Every table reports coverage and unresolved counts alongside failure counts.
2. Successful executions are preserved, not just failures (work order §8).
3. Typed manifestation records remain available; binary summaries are derived views.
4. Observed outcomes are kept separate from injected defect labels and cause hypotheses.
5. E1 and E3 are reported separately, never merged; no estimate migrates between them.
6. All limitations below accompany every release of results.

## 8. Limitations (binding language for any results release)

1. This is a deliberately constructed LC518 population — not a sample of arbitrary
   programs, naturally occurring submissions, or every possible solver (work order §1).
2. Results apply only to the declared construction process, task contract, execution
   protocol, and the 80-record held-out distribution of BANK_DESIGN.md; they do not
   automatically generalize to all LeetCode submissions or all LC518 inputs
   (contract §7).
3. The 28-pair screen is exploratory; the two preselected replications provide limited
   replication; no universal taxonomy of failure, no universal law of solver
   correctness, and no transport to other tasks or populations is claimable
   (work order §16).
4. The eight owner-supplied mechanisms do not cover every possible program failure;
   concurrency, external I/O, and unrelated systems issues are out of scope unless
   separately defined (work order §11).
5. No power or minimum-detectable-effect claim is made anywhere in this study
   (work order line 66).
6. The legacy concentration statistic of the earlier study is not an estimand here; any
   descriptive reuse must respect the typed-record and unresolved-handling rules above.

## 9. Pending external inputs (slots, not content)

| Slot | Owner | Gates |
|---|---|---|
| Eight-mechanism taxonomy | owner's private annex | mutation assignment; §11 compatibility report |
| Pair-allocation schedule: all 28 unordered pairs once + two preselected replications + S-extra balancing | owner's private annex | all source construction (replications must be preselected before source construction, work order line 47) |
| Execution protocol: interpreter pin, runtime/memory budgets, timeout rule | owner, separate authorization | any solver execution; timeout/resource classification; reserved feature columns |
| Blind predictive analyst appointment | owner | any E3 fitting (analyst must not have seen the sealed manifest, mutation assignments, or solver source; work order §4) |

## 10. Freeze record

- Frozen content: §1–§9.
- The feature columns (§4), strata (BANK_DESIGN.md §6), fold definitions, alpha grid,
  loss, and aggregation (§6) are frozen before any source mutation is constructed, as
  required by work order §10.
- Any change requires a new version header and a stated reason; silent edits are
  prohibited. No content of the owner's annex is anticipated, invented, or pre-filled
  here.
