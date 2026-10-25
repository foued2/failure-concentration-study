# Construct-validity assessment: failure concentration beyond `k` and family

**Date:** 2026-10-25
**Branch:** `research/concentration-math-spec` (evidence base through `db00242`)
**Status:** Document-only synthesis. No experiment, solver, simulation, model fit, or model/API call is authorized by this document.
**Question:** Can diagnostic failure concentration `C` be interpreted as adding held-out predictive value beyond total diagnostic failures `k` and the declared family/defect information?

This assessment synthesizes the committed research record. It does not reopen v0.1, v0.2, Gate 1, or the three-world simulation, and it does not change any frozen result. In particular, **W1 remains FAILED**, the stratum contrasts remain descriptive, and the natural-solver inventory remains `INFEASIBLE_WITH_CURRENT_DATA`.

---

## 1. Estimand, stated before the history

### 1.1 Quantities

For a solver body with six diagnostic families, let

\[
F=(f_1,\ldots,f_6),\qquad
k=\sum_{j=1}^{6}f_j,\qquad
C=\frac{\max_j f_j}{k}\quad(k>0).
\]

`C` is undefined at `k=0`. It is not zero at `k=0`, and a stored zero there is a sentinel, not an observed concentration.

Let `S` be a solver's score on a predeclared held-out evaluation suite. Let `Z` denote predeclared context covariates such as task, generator protocol, carrier/family information, and defect mechanism, where those are available and estimable. `Z` must **not** contain the complete failure vector `F` for the primary comparison: if `F` is present, `C` is already determined by `F` and `k`, so `C` cannot add information conditional on those counts.

### 1.2 Target

The target is **incremental held-out predictive value**, not a causal effect of changing `C`.

Compare two frozen prediction procedures:

- baseline: predict `S` from `k` and `Z`;
- augmented: predict `S` from `k`, `Z`, and `C`.

With squared prediction error as a candidate primary metric, define

\[
\Delta_{\mathrm{pred}}
=\mathbb{E}\left[(S-\widehat S_0)^2-(S-\widehat S_1)^2\right],
\]

where `S0_hat` and `S1_hat` are generated without using the evaluation unit being predicted. Positive `Delta_pred` means the augmented procedure predicts better under the specified design. Zero means no improvement. Negative means it predicts worse.

The unit of held-out prediction must match the claim. A claim about new solvers requires held-out solver bodies, with replicas and near-duplicate mechanisms kept in the same fold. A claim about new instances under a fixed solver pack is a different, narrower claim and must be stated as such. The population, score definition, covariate set, model procedure, uncertainty method, and minimum meaningful effect must all be frozen before confirmatory evaluation.

### 1.3 Interpretation rule

A positive in-sample coefficient for `C` is not evidence for the target. Support requires all of the following in a future confirmatory design:

1. the prespecified overlap and identification checks pass;
2. `Delta_pred` is positive with its prespecified uncertainty interval above zero;
3. the fixed-`k` conditional direction is as predicted; and
4. the direction does not reverse or collapse under the prespecified scoring and partition checks.

The exact uncertainty procedure and minimum practically important `Delta_pred` are **not** set here. They must be set in a future protocol before any data are generated or examined. This assessment defines the target; it does not launch a study.

---

## 2. Three limits that must not be blurred

| Limit | What it means | What it does not mean |
| --- | --- | --- |
| **Mathematical possibility** | At fixed `k`, `C` can differ when failures are distributed differently across families. Example: at `k=4`, `(2,1,1,0,0,0)` gives `C=0.5`, while `(3,1,0,0,0,0)` gives `C=0.75`. | It does not show that independent solvers can realize those profiles without changing defect identity. |
| **Current data support** | The retained natural-solver archive contains no eligible same-`k`, different-`C` comparison. v0.1 and v0.2 sit on `C=5/k`; the later Codex and Gemini runs have only `k=0`; the expression `k>=2` bodies crash. | It is a limitation of the retained data, not a universal impossibility result and not evidence that `C` lacks predictive value. |
| **Scientific identification** | Even with variation, a `C` association can reflect family identity, family size, defect mechanism, or scoring weights. A useful claim must separate `C` from those alternatives, or explicitly narrow the claim to a setting where they are held fixed. | It does not imply that no possible design can identify a meaningful `C` question. |

The first limit is an arithmetic fact. The second is an inventory fact. The third is the construct-validity problem that any future design must solve.

---

## 3. What the research record shows

### 3.1 RLC-0: adjacent formal-localization feasibility, not a concentration test

RLC-0 is a separate feasibility track for formal behavioral localization on six LeetCode 704 seeds. Its contract and freeze record describe a **freeze candidate**, not a completed frozen study. The recorded C2 audit found that full-domain CBMC certification was not demonstrated under the pinned toolchain and budget: the canary runs ended in out-of-memory/incomplete states, and the canary-FAIL half of the requirement was not observed. No seed was compiled or executed, and the `rlc0-freeze` tag was not created.

RLC-0 therefore contributes **no concentration evidence** and no `C`-`S` comparison. Its relevance to this assessment is limited to the general lesson that a feasibility gate can close without answering the scientific question.

Sources: `rlc0/CONTRACT.md`, `rlc0/FREEZE.md`, `rlc0/evidence/C2/RESULTS.md`.

### 3.2 v0.1: natural SSSP pilot, terminal infeasible

The v0.1 pilot used one generator and 20 single-shot SSSP submissions. It terminated at its frozen yield gate. The retained support contains four eligible bodies with `k>=2` (two at `k=5`, one at `k=10`, one at `k=25`), contributing 12 eligible body-instance rows.

All eligible support has `C=5/k` exactly. There are **zero** same-`k`, different-`C` pairs. The infeasibility finding is about the yield and support of this pilot, not a test of the concentration hypothesis.

Sources: `pilot/`, `natural-feasibility-pilot/offline-inventory-2026-10-25/INVENTORY_REPORT_2026-10-25.md`.

### 3.3 v0.2: natural SSSP pack, terminal negative but not an independent-`C` test

The v0.2 pack contains 120 files, but only **40 unique base bodies replicated three times**. The audited pilot support has 90 eligible rows at four `(k,C)` cells:

| `k` | `C` | Rows | Base bodies |
| ---: | ---: | ---: | ---: |
| 5 | 1.0 | 27 | 3 |
| 10 | 0.5 | 9 | 1 |
| 20 | 0.25 | 9 | 1 |
| 25 | 0.2 | 45 | 5 |

Every row satisfies `C=5/k`; within each `k` there is exactly one `C` level and zero within-`k` variance. The persisted confirmatory report does not expose body-level rows; the offline inventory therefore did not use its 1,200 aggregate eligible pairs to create a qualifying contrast.

The frozen decision is **NEGATIVE** under its prespecified rule. The interpretability audit narrows what that means: because `C` is deterministic given `k` on the eligible support, the near-zero confirmatory estimate is uninformative about independently varying concentration. It is consistent with the structural degeneracy and does not test whether `C` predicts correctness when it varies at fixed `k`. The broader hypothesis is neither supported nor refuted.

Sources: `v02/REPORT_V02.md`, `v02/INTERPRETABILITY_AUDIT_2026-10-14.md`, `v02/FINDINGS_LEDGER_2026-10-19.md`.

### 3.4 Later natural runs and the expression pilot: no eligible fixed-`k` contrast

The Codex and Gemini SSSP runs produced no eligible `k>=2` bodies; every complete body had `k=0`, where `C` is undefined. Those outcomes are infrastructure and feasibility observations, not scientific negatives.

The expression pilot has 30 attempt directories. Nineteen passed fail-closed source and host-record validation, but all 13 of its `k>=2` bodies crash on the diagnostic and evaluation suites and are ineligible under the frozen protocol. The six `k=0` bodies are valid but cannot support a fixed-`k` concentration contrast. The pilot therefore contributes zero eligible `k>=2` bodies.

The offline inventory concludes that the total protocol-eligible `k>=2` support across the retained natural datasets is 14 bodies (4 from v0.1, 10 base bodies from v0.2), with **zero** same-`k`, different-`C` pairs in every dataset. This is criterion `INFEASIBLE_WITH_CURRENT_DATA`, not a demonstrated zero effect.

Sources: `natural-feasibility-pilot/offline-inventory-2026-10-25/INVENTORY_REPORT_2026-10-25.md`, `next-task/06_EXPRESSION_PILOT_RESULT_2026-10-22.md`, `next-task/07_EXPRESSION_PILOT_AUDIT_2026-10-22.md`.

### 3.5 Engineered Gate 1: bounded construction failure in the parenthesis task

The engineered `paren7_min_insertions` study asked whether, at fixed `k=5`, higher `C` predicts higher held-out score after accounting for generator identity and carrier family. Gate 1 closed before generating any study solvers.

The target design had six `C=1` profiles, each localizing the five failures in a different family, and one `C=0.2` spread profile. This did not identify `C` separately from carrier family or defect identity: there was no within-carrier high/low contrast, and the evaluation bank is unbalanced across families.

The calibration controls showed that score varies at fixed `k` and fixed `C=1` (0.683673 to 0.969388), which is a carrier/defect effect, not a concentration effect. The high-`C` control mean (0.833333) was actually lower than the low-`C` control score (0.887755).

The bounded Option B construction audit evaluated 257 hand-built mechanism instances. Fourteen produced `k=5`, but no mechanism family produced more than one distinct `k=5` concentration profile. Eight cross-mechanism profile matches were found, and all had identical full-domain failure sets; there were zero matches between genuinely different mechanisms. The stop rule was met, Gate 1 closed, and no solvers were generated.

This is a bounded negative construction result, not proof that no possible mechanism exists and not evidence that H1a is false.

Sources: `engineered-study/00_CLAIM.md`, `engineered-study/GATE1_REPORT.md`, `engineered-study/08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`, `engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md`.

### 3.6 Three-world simulation and stratum contrasts: synthetic assumptions, not real-solver evidence

The three-world simulation was constructed to show the implications of declared assumptions, not to estimate what real solvers do.

- **W1** was designed to make concentration informative. Its frozen wiring check **FAILED**: the family-adjusted domain gain was `1.961346752e-6` with central 95% trial interval `[-1.242089975e-6, 7.581285807e-6]`; the equal-family estimate was similarly small with an interval including zero. The alternate-partition check also failed. W1 remains the governing result.
- **W2** sets `C=1` for every eligible case, so there is no within-`k` concentration variation. It is **unidentifiable**, not a measured zero and not a positive result.
- **W3** makes evaluation damage independent of diagnostic concentration conditional on the declared baseline and latent defect count. Its primary `C` gain failed; its oracle comparison is a null check, not a positive result.

The later saved-record stratum analysis is descriptive only. Across 973 carrier-by-`k` strata, 756 contain at least two observed `C` levels. In W1, the unadjusted high-minus-low score difference is positive on average (`+0.0083141` for the domain-weighted score; 92 positive, 36 negative strata). W3 also shows positive descriptive contrasts on average even though its oracle construction makes `C` non-causal. W2 contributes zero. These summaries involve no adjustment, no model fit, no confidence interval, and no inference. They do not rescue the W1 failure.

This is exactly the distinction the construct-validity assessment must preserve: a positive descriptive contrast can arise because `C` proxies latent structure. It is not an incremental held-out predictive gain.

Sources: `engineered-study/math/10_THREE_WORLD_SIM_DESIGN.md`, `engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md`, `engineered-study/math/results/three_world/12_POST_RUN_REVIEW_CORRECTIONS_2026-10-24.md`, `engineered-study/math/results/three_world/15_STRATUM_SPECIFIC_CONTRASTS_REPORT_2026-10-25.md`.

---

## 4. What the chain establishes

| Question | Current answer |
| --- | --- |
| Can `C` differ at fixed `k` mathematically? | **Yes.** Different family-count vectors can give different `C` at the same `k`. |
| Does the retained natural archive contain an eligible same-`k`, different-`C` contrast? | **No.** v0.1 and v0.2 have only `C=5/k`; later SSSP bodies are `k=0`; expression `k>=2` bodies crash. |
| Did v0.1 or v0.2 test independent `C` variation? | **No.** v0.1 was infeasible; v0.2 was negative under a support where `C` is deterministic in `k`. |
| Did engineered Gate 1 demonstrate a constructible within-carrier contrast? | **No.** The bounded audit found no genuinely different mechanism family with multiple `k=5` concentration profiles. |
| Did the three-world simulation demonstrate real predictive value? | **No.** W1 failed its wiring check; W2 is unidentifiable; W3 is a null check. |
| Are the stratum contrasts evidence for `C`? | **No.** They are descriptive extreme-level comparisons, with no adjustment or inference. |
| Did RLC-0 test concentration? | **No.** It is an adjacent formal-localization feasibility track with no executed seeds and no completed freeze. |

The defensible synthesis is:

> The existing work has not demonstrated the proposed predictive gain, but it has not established that concentration lacks predictive value. The natural data are infeasible for the target contrast; the engineered design failed a bounded constructibility audit; and the simulation’s informative world failed its own wiring check. These are findings about the existing designs and evidence, not a universal negative about `C`.

---

## 5. Construct-validity finding

`C = max(F)/k` is a deterministic summary of the entire family-count vector `F`. It cannot be varied while holding `F` fixed, because `C` is a function of `F`. The scientifically relevant question is therefore not whether `C` can be changed “independently” of the distribution it summarizes. It is whether, at fixed `k`, the **distribution** of failures across families carries held-out predictive information beyond `k` and beyond the family/defect information already available.

That question is legitimate, but it has three construct threats:

1. **Family identity.** A high-`C` profile may fail because one family is especially difficult or because its defect mechanism is different, not because concentration itself carries information.
2. **Family size and scoring.** The domain-weighted score depends on which evaluation family receives the damage. Equal-family weighting removes one size effect but does not make different mechanisms comparable.
3. **Mechanism identity and latent structure.** Different profiles can be different defects. A `C` association can be a proxy for defect count, defect type, or overlap, as W3 illustrates.

The existing natural-support degeneracy is a concrete example: when the eligible runs fully fail one diagnostic family, `C=5/k`. This is not a law about all solvers. It is a property of the retained instrument, generator behavior, and eligibility rule. A future design would have to produce independent units at the same `k` with different failure distributions while keeping the relevant family/mechanism alternatives visible.

The engineered Gate 1 attempted exactly that and failed its bounded construction audit. The three-world simulation attempted to model the mapping and found that the informative world did not pass its own predictive criterion. Neither result proves the construct is universally invalid. Together they show that the construct has not yet been operationalized in a way that supports the estimand in Section 1.

---

## 6. Conditions a future design must satisfy

These are conditions for review, not an authorization. Any future study requires a separate, explicitly scoped decision and a new frozen protocol.

1. **Declare the unit and population.** State whether the claim is about held-out solver bodies or held-out instances under a fixed pack. Do not mix the two.
2. **Fix the score before generation.** Freeze the primary held-out score, the secondary score, the diagnostic/evaluation split, and the family definitions.
3. **Produce independent same-`k` units.** At a prespecified `k>0`, realize at least two `C` levels with independent solver bodies. Replicas and mechanically equivalent predicates do not count as independent units.
4. **Hold the competing explanations visible.** Demonstrate that the contrast survives the declared carrier/family and defect-mechanism controls, or narrow the claim to a setting where those are fixed. Report loss of common support as non-identification.
5. **Demonstrate `C` is not deterministic given `k` and controls.** Report the number of distinct `C` values per `k`, the number of independent units at each value, the design rank, and the residualized variance of `C` after the declared controls.
6. **Compare `C` with the full vector `F`.** Because `C` is a summary of `F`, a claim that `C` is the better representation is not available in principle. The empirical question is whether the summary is useful under a fair, finite-sample predictive comparison.
7. **Use held-out prediction, not an in-sample coefficient.** Tune and select within training folds only; use the same held-out units and folds for baseline and augmented procedures; cluster duplicates and near-duplicates in the same fold.
8. **Prespecify a minimum meaningful `Delta_pred` and a stop rule.** State in advance what improvement is practically important and what sample size or overlap is required. If fewer than the required independent same-`k` pairs exist, report infeasible and stop.
9. **Keep outcome separation.** Do not construct candidates, choose thresholds, or select the analysis after seeing evaluation outcomes. Record any exposure.
10. **Do not treat infeasibility as a negative result.** If the design cannot identify the estimand, report that. Do not report “no effect” from a support with no contrast.

A future design that cannot satisfy conditions 3-5 should not be run. More replicas of the same profile cannot create missing variation; renaming mechanisms cannot create independent mechanisms; rotating carrier families without a within-carrier contrast cannot identify `C` separately from family.

---

## 7. What would not count as evidence

- A positive in-sample coefficient for `C`.
- A high-`C` versus low-`C` mean difference without adjustment, common support, or uncertainty.
- More copies of a profile already represented by a single mechanism.
- A family rotation that changes `C` only by changing which family carries the defect.
- A simulation in which `C` is wired to the outcome, such as W1, presented as real-world evidence.
- A negative result from a support where `C` is deterministic given `k`, such as v0.2, presented as evidence that `C` is useless.
- A natural-solver infeasibility finding presented as a universal impossibility result.
- A post-hoc partition or score chosen because it produces a preferred sign.

---

## 8. Outstanding preservation item

The three-world raw/per-trial archive totals about 592 MB and remains local-only. The committed report and manifest record its hashes, but hashes do not preserve the data if the sole copy is lost. A second verified copy on storage independent of the C: drive remains an owed operational item.

This is not a dependency for the construct-validity assessment and does not authorize a rerun. It is recorded so it does not drop silently.

---

## 9. Evidence base

Primary sources used for this assessment:

- `README.md` (read only; unchanged)
- `engineered-study/00_CLAIM.md`
- `engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md`
- `engineered-study/GATE1_REPORT.md`
- `engineered-study/08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`
- `engineered-study/math/10_THREE_WORLD_SIM_DESIGN.md`
- `engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md`
- `engineered-study/math/results/three_world/12_POST_RUN_REVIEW_CORRECTIONS_2026-10-24.md`
- `engineered-study/math/results/three_world/15_STRATUM_SPECIFIC_CONTRASTS_REPORT_2026-10-25.md`
- `engineered-study/math/15_NATURAL_SOLVER_FEASIBILITY_PROTOCOL_2026-10-24.md`
- `natural-feasibility-pilot/offline-inventory-2026-10-25/INVENTORY_REPORT_2026-10-25.md`
- `v02/REPORT_V02.md`
- `v02/INTERPRETABILITY_AUDIT_2026-10-14.md`
- `v02/FINDINGS_LEDGER_2026-10-19.md`
- `next-task/06_EXPRESSION_PILOT_RESULT_2026-10-22.md`
- `next-task/07_EXPRESSION_PILOT_AUDIT_2026-10-22.md`
- `rlc0/CONTRACT.md`
- `rlc0/FREEZE.md`
- `rlc0/evidence/C2/RESULTS.md`

This document is the only new artifact. It imports no solver code, reads no local-only raw archive, runs no simulation, performs no model fit, and makes no model/API call. It does not modify `README.md` or any frozen result.
