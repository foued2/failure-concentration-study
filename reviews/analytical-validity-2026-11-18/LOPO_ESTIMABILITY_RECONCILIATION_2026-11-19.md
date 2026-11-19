# LOPO estimability reconciliation — 2026-11-19

**Status:** reconciliation record. Design only. No execution, no fitting, no frozen document altered.
**Question:** the review asks for a fold-level estimability rule, coverage reporting, and parent-level
uncertainty. How much of that already exists in the frozen B1 plan, and what is genuinely missing?

**Short answer:** the estimability rule and the coverage reporting already exist, with three explicit
conditions and a no-silent-drop rule. The genuinely missing piece is a **pre-declared minimum-coverage
gate** — a threshold below which the verdict is *not assessable* rather than positive or negative.

---

## 1. Clause-by-clause map

Source: `B1_ANALYSIS_PLAN_2026-11-14_v1.7.md` on `origin/gpt/lc518-m1si-audit-2026-11-17`.

| Review request | Frozen clause | Status |
|---|---|---|
| Fold-level estimability rule | §3 item 3: a cell contributes within-cell information only when `G_c^train ≥ 2`, `D_c^train ≥ 2`, and `W_{C,c}^train = Σ(C_D − C̄_D)² > 0` | **Already specified** |
| Non-estimable cell must not be silently dropped | §3 item 3: excluded cells are "not scored, and its exclusion reason is listed"; no fold "silently scored with a zeroed slope, a reduced baseline, or a changed test population"; no excluded fold silently added | **Already specified** |
| Support checked on training portion only | §3 item 3: conditions are computed from the training folds (`^train` superscript throughout) | **Already specified** |
| Do not pool unsupported cells to make them estimable | §5.7 V2 and §3 item 3: admissibility requires reproducing the observed selection key; a previously excluded cell that *becomes* estimable makes the assignment inadmissible | **Already specified, and stronger than requested** |
| Report coverage | §3 item 4(c): "reports include per-fold and per-dataset coverage tables"; §11(e): "coverage diagnostics" | **Already specified** |
| Do not treat 150 predictions as 150 independent observations | §3 item 4(a): statistic uses each dataset's own scored-parent set "with **equal weight per scored parent**"; §11(a): per-parent paired differences | **Already specified** |
| Parent-level uncertainty | §5.7 V1: the test "does **not establish the parent-population target**"; §12: no claim that the gain generalises to independently developed parents | **Explicitly refused, not omitted** |
| Extrapolation must not change the scored population | §3 item 2: flags are "diagnostic only — they never drop or add scored rows" | **Already specified** |
| Minimum coverage threshold for a valid verdict | — | **MISSING** |

Nine of ten are already frozen. The review's point 3 is largely a rediscovery, and one clause (§5.7 V2)
is stricter than the review asked for.

---

## 2. Why "one parent per fold" is not the problem it looks like

The review's stated worry: a held-out fold contains one parent, so its `C_D` and correctness estimate are
noisy, and the effective sample is 30, not 150.

Two corrections, in order:

1. **The fold's test set is not five observations.** B1 scores the held-out parent's variants on **all 78
   records** (§3 item 2). The scored rows per fold are `variants × 78`, not `5`. Precision per fold is
   therefore much better than "five points".
2. **The number of independent units is still the parent.** B1 already concedes exactly this: the
   statistic averages with equal weight per scored parent (§3 item 4a), and §5.7 V1 states that the
   test does not establish the parent-population target. The consequence is not a defect to be repaired
   by pretending otherwise; it is a **declared scope limit**: LOPO yields a cross-validated
   held-out-parent performance, and a parent-population interval requires a separate procedure that the
   plan does not claim (a parent-level resampling of exposures, or a hierarchical superpopulation model,
   both removed from the plan in v1.2 precisely because they were not specified).

So the review is right about the arithmetic and wrong that the plan ignores it. The plan names the limit
and forbids advertising the conditional result as population inference.

---

## 3. The genuine gap: a coverage gate

B1 v1.7 requires coverage to be **reported**. It does not require any minimum coverage for a verdict to
be issued. That leaves a real failure mode: a run in which only a small minority of parents are scored
could still produce a `ΔLL` and a p-value, and the p-value would be computed on a population that is
almost empty — validly, but not usefully.

**Proposed structure** (numbers are owner/adjudicator decisions, not findings):

For each target — conditional-on-realized-parents, or parent-population — declare in advance:

| Element | Requirement |
|---|---|
| Scored-parent fraction `|G_score| / J` | reported; a pre-declared floor `ρ_min` below which the verdict is `NOT ASSESSABLE` |
| Scored-cell fraction | reported per fold; floor `ρ_cell` |
| Records scored per fold | reported; floor `ρ_rec` |
| Exclusion reasons | enumerated with counts, design-based only |
| Verdict vocabulary | `SUPPORTED` / `NOT SUPPORTED` / `NOT ASSESSABLE` — the third is a first-class outcome |

**Why the third verdict matters:** without it, a run with 3 scored parents out of 30 reports either a
"positive" or a "negative" result on a sample that cannot support either. The audit's own pattern —
refusing to report a pass or a fail when the evidence is absent — requires the third category here too.

**Why no numbers are proposed:** `ρ_min` depends on the estimand and on between-parent variation, neither
of which is estimated anywhere. Inventing a threshold would be the same error as inventing a power
calculation, which the record has already refused twice. The correct state is: **gate specified, threshold
open, owner decision.**

---

## 4. What this changes in the record

Nothing frozen. The addition is a reporting and verdict rule for future runs:

1. Every B1 evaluation reports the three coverage fractions of §3 alongside §11's existing coverage
   diagnostics.
2. `NOT ASSESSABLE` becomes an available **final** verdict, not an intermediate state to be resolved by
   relaxing a gate.
3. The threshold values are declared before evaluation and may not be revised after outcomes are seen.

---

## 5. What remains unresolved

| Item | Why it is open |
|---|---|
| `ρ_min`, `ρ_cell`, `ρ_rec` | no between-parent variance or precision target exists |
| Whether a parent-population claim is intended at all | owner route decision |
| Whether a hierarchical model is required | would need to be predeclared through review before any evaluation |
| Whether 30 parents is enough for any of the above | not adopted as an operating count; no justification exists |

**Gate 3 status:** the fold machinery is specified and stricter than the review assumed; the coverage
gate is specified here for the first time; the operating count and the precision objective remain open.
No identifiability evidence exists, and none can exist until solvers are built and evaluated.
