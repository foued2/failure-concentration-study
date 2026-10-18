# VDraft: Target Bridge and Research Decision Plan

**Date:** 2026-10-18  
**Status:** REVIEW DRAFT ONLY. Not frozen. No NC2 execution, Phase 1 simulation, solver generation, hidden-outcome collection, budget commitment, or protocol authorization is granted by this document.  
**Purpose:** Translate the Claude/GPT discussion into a reviewable next-step plan while keeping the original scientific question primary.

## 1. Recommendation in brief

Accept the goal framing, with two corrections to the proposed sequence.

The primary question remains:

> Does the concentration of a solver's diagnostic failures, `C`, predict correctness on unseen inputs beyond the total failure count, `k`, for naturally generated solver bodies?

The natural-solver predictive study should remain the primary route. An engineered mechanistic study is a possible alternative or validation route if the natural population cannot provide enough identifiable support at an acceptable cost. The two routes answer related but different questions; evidence for one must not be presented as evidence for the other.

Before choosing a route, create a target-translation report that relates the already chosen predictive-score target to the mechanistic signal parameter used by the `c*` heuristic. Treat the simple approximation in §4 as a sanity check, not as the final conversion.

Do **not** immediately redefine NC2 as the v0.3 Phase 1 power simulation. The existing `c*`-heuristic question and the v0.3 predictive-procedure validation are separate work products unless the owner explicitly merges them in a revised protocol. Phase 1 of v0.3 also remains blocked by unresolved design decisions in Revision F, including the §5A conditioning contradiction.

## 2. Terms that must not be conflated

| Symbol | Meaning in this plan | What it is not |
|---|---|---|
| `k` | Total number of diagnostic probe failures | A measure of where failures occur |
| `C` | Largest family’s share of failures; a concentration statistic | The mechanistic variance-like quantity `c` calculated in NC1 |
| `Δ` | Held-out predictive log-loss improvement: baseline (`k`) minus extended (`k, C`) | The mechanistic slope or a threshold-crossing probability |
| `δ*` | Existing proposed minimum meaningful predictive gain, `ln(1.5)/20 = 0.020273255405408218` nats per hidden input | A slope on the correctness-probability scale |
| `γ` | Coefficient on raw `C` in Revision F’s proposed logit outcome generator, `logit(p) = θ0 + θ1 log(1+k) + γC + u + v` | The same parameter as `β` without a specified transformation |
| `β` | The signal parameter used in the mechanistic `c*` heuristic. Working interpretation for this draft: probability-scale change in correctness rate per one reference SD of `C` | `Δ`, `δ*`, or the logit coefficient `γ` |
| `c*` | Mechanistic threshold `c* = (1.25/β)^2` under the M3 addendum’s stated construction | A directly measured estimate of predictive gain or statistical power |

**Required source reconciliation:** Revision F explicitly specifies `γ` for its logistic data-generating process, while NC1’s header uses `β` in `c* = (1.25/β)^2`. The exact unit definition of `β` and its relationship to `γ` must be checked against the controlling M3 addendum before the bridge calculation is frozen. Do not silently relabel `γ` as `β`.

## 3. What is already established, and what is not

### Established design target

The current v0.3-P Revision F draft records the owner’s earlier choice `r = 1.5`, operationalized as:

\[
\delta^* = \frac{\ln(1.5)}{20} \approx 0.0202733
\]

This is the proposed minimum meaningful *held-out log-loss gain* for prioritizing candidates for an expensive confirmation slot. Revision F also explicitly warns that `exp(20Δ)` is a multiplicative score contrast under the additive scoring interpretation, not a literal joint-vector likelihood ratio. This target is not a value of `β`.

### Established NC1 threshold mapping

Under the current heuristic, the values used in NC1 are:

| `β` supplied to heuristic | `c* = (1.25/β)^2` |
|---:|---:|
| 0.20 | 39.0625 |
| 0.10 | 156.25 |
| 0.05 | 625 |

NC1 has been technically validated and its validation loop is closed. Its threshold probabilities are conditional on the declared scenario distributions and gates. They do not establish the distribution of real natural solvers, nor do they constitute power estimates for the v0.3 predictive procedure.

### Still unknown

We have not yet established which `β` corresponds to `δ*` across the declared baseline probabilities and within-`k` spreads of `C`. A single approximate value cannot be assumed to apply across all scenario families.

## 4. Preliminary bridge: approximation only

For a probability-scale slope `β`, a centered predictor `z` with variance `Var(z)`, and a baseline correctness probability near `p`, a small-effect approximation for the population log-score gain is:

\[
\Delta_{\mathrm{oracle}} \approx
\frac{\beta^2\,\operatorname{Var}(z)}{2p(1-p)}.
\]

At `p ≈ 0.5` and `Var(z) = 1`, this becomes `Δ ≈ 2β²`. Substituting the existing `δ*` gives:

\[
\beta \approx \sqrt{\delta^*/2} \approx 0.1007.
\]

This explains why the `β = 0.10` row was proposed as a boundary scenario. It does **not** prove that `β = 0.10` is the right row for the study. The approximation can move with baseline probability, the reference-scale spread of `C`, the distribution of `k`, the support gate, and the nonlinear/random-effects outcome model. It is also a population-oracle approximation, not finite-sample power of the fitted procedure.

## 5. Proposed work item A: target-translation report

**Purpose:** Replace an arbitrary choice among `β = 0.05, 0.10, 0.20` with a transparent mapping from the existing predictive target to the signal scale used by NC1.

### A1. Lock the definitions before calculating

1. Inspect the controlling M3 addendum and the NC1 specification to pin down the units, sign, and reference scale of `β`.
2. Keep `δ*`, the logit coefficient `γ`, probability-scale `β`, and mechanistic threshold `c*` as four distinct quantities.
3. Because the scientific claim is *incremental prediction beyond `k`*, define the reference spread of `C` from its variation **within `k`**, among supported bodies, rather than from marginal variation in `C` that can be explained by differences in `k`. If the M3 addendum prescribes a different reference scale, document the difference and obtain reviewer/owner acceptance before adopting it.
4. Separate the population-oracle log-score contrast from the finite-sample score gain of the fitted analysis procedure. Revision F itself says its proposed `γ*` calibration targets the former; Phase 1 would assess the latter.

### A2. Calculate the bridge under declared cases

For each declared outcome baseline and support/composition scenario, including the documented within-range alternatives where relevant:

1. Use the declared Revision F outcome model as specified: `logit(p) = θ0 + θ1 log(1+k) + γ C + u + v`, with proposed `θ0 = 0`, `θ1 = -1`, `σ_b = σ_s = 1` unless a reviewed change is made.
2. Calibrate `γ` to the population-oracle target `Δ = δ*` (and optionally `2δ*` as a sensitivity case), using the predeclared numerical method and convergence checks.
3. Compute the corresponding probability-scale `β` under the locked reference definition. Report `γ`, `β`, the supported-population `C` spread, baseline probability range, and numerical error/tolerance together.
4. Map the resulting `β` values to `c* = (1.25/β)^2` and show where they fall relative to NC1’s evaluated threshold grid.
5. Report a range/sensitivity across scenarios, not a single pooled value that conceals differences between a-, b-, and c-type populations.

**Precision language:** discrete NC1 probability calculations may be exact under their specified enumerations, but the target bridge involves a nonlinear random-effects outcome model and numerical calibration. Unless the calculation actually proves a closed form, describe this bridge as a *numerically calibrated mapping with convergence checks*, not simply as “exact.”

### A3. Required output

One table with at least these columns:

| Scenario/support definition | Within-`k` reference SD of `C` | Baseline correctness range | Target `Δ` | Calibrated `γ` | Implied probability-scale `β` | Implied `c*` | NC1 quantity at that threshold | Numerical tolerance/status |
|---|---:|---:|---:|---:|---:|---:|---:|---|

If the current support rule cannot be defined because an unresolved protocol contradiction makes the complete analysis support empty, the report must say so and label affected rows **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE**. It must not present bucket-local proxy results as the probability that the full study passes.

## 6. Proposed work item B: decide what “NC2” is meant to test

Two questions are being bundled in the discussion. Keep them distinct in the draft and in any work order.

**Question B1: Is the `c*` heuristic calibrated to the signal scale that matters?**

This is the mechanistic bridge/NC2 question. It asks whether the threshold mapping is too pessimistic or optimistic under defined signal models, and what the corresponding `c*`-crossing probabilities are under the declared distributions. It does not, by itself, estimate the predictive gain from natural solvers.

**Question B2: Can the proposed `k` versus `k+C` estimator detect `Δ = δ*` with controlled error?**

This is the v0.3 Phase 1 software-simulation question. It requires a frozen simulation DGP, analysis procedure, inference target, support/gate rules, interval procedure, Type I error criterion, power criterion, and explicit owner authorization after protocol freeze. Revision F §5A currently records a structural problem: the conventional condition-number requirement makes the full support rule impossible as drafted. The selected M1/M2/M3 resolution and recalculation of complete-rule probabilities must precede a meaningful Phase 1 power result.

**Recommendation:** Run the target-translation report first. Then decide, on its results, whether a mechanistic NC2 calculation is still needed. Do not start the v0.3 Phase 1 simulation by calling it “NC2”; resolve its separate freeze blockers and authorization boundary first. No solver generation or hidden-outcome collection is part of either work item.

## 7. Decision sheet to prepare before simulation results

The report should end with a decision table whose criteria are agreed before any Phase 1 outputs are examined.

| Outcome | Proposed meaning | Required conditions |
|---|---|---|
| **GO: natural-solver predictive study** | Proceed to the next separately authorized phase aimed at the primary theory question | Complete-rule support is nonzero and adequate under the adopted protocol; the design is evaluable at the approved budget; Phase 1 controls Type I error and meets the owner-approved power/coverage criteria at `δ*`; projected cost is within the owner-approved ceiling |
| **ALTERNATIVE: engineered mechanistic study** | Do not spend the natural-solver budget under the current design; consider a separately chartered controlled-mechanism study | Natural-solver support/power is inadequate at the affordable budget, but the controlled design has a clear, separately stated estimand and can test the mechanism without being misrepresented as evidence about natural solvers |
| **STOP / redesign decision** | Neither route currently justifies the planned cost, or neither has a valid, evaluable design | State the failed gate and what it implies for feasibility; do not claim that a failed feasibility gate falsifies the scientific theory |

The following are **owner decisions still required before a protocol freeze**, not numbers for reviewers or agents to guess:

- Maximum affordable budget, expressed as attempts, hidden suites, and/or a monetary ceiling.
- Minimum acceptable Phase 1 power at `δ*` and the Type I error ceiling.
- The final suite-count choice, consistent with Revision F’s derived minimum constraints.
- Whether an ALTERNATIVE mechanistic study is an acceptable fallback and what result it must deliver to be useful.

Existing Revision F candidate budgets (`150` feasibility attempts and `600` confirmatory attempts) are not treated as final spend approval. The design itself says they require owner approval.

## 8. Required protocol blockers and authorization boundaries

Before the v0.3 predictive procedure can be simulated, the review must close the relevant Revision F items, at minimum:

1. §5A’s M1/M2/M3 matrix/conditioning resolution and recalculation of complete-rule support probabilities.
2. Coordinated O1–O5 resolution, including attempt-versus-valid/unique-body budgeting and the support/replication-grid mapping.
3. G6 inference-target choice and the calibration/coverage-truth method.
4. Support and split eligibility rules, including training-block/test-block behavior.
5. Predeclared FPR, power, coverage, and “not evaluable” criteria.
6. Owner approval of the estimand narrowing, DGP parameters, suite counts, budget, and proposed decision rule.

Authorization sequence remains:

1. Review and revise this VDraft.
2. Owner approves the target-translation computation and the precise work order.
3. Review the bridge report; decide whether NC2 is justified.
4. Resolve and review the v0.3 simulation-protocol blockers; freeze only after sign-off and owner approval.
5. Obtain separate explicit owner authorization before Phase 1 simulation.
6. Obtain separate authorization for each later study phase. Passing a gate never authorizes the next phase automatically.

NC1 remains closed. Its source artifacts and results are not reopened by this plan. NC2 remains held until explicitly authorized. Phase 1 remains unauthorized until its protocol freeze and separate authorization. Solver generation and hidden-outcome collection remain unauthorized.

## 9. Review questions

Reviewers should respond to these specific questions rather than reopening unrelated provenance checks:

1. Does the proposed within-`k` reference scale for `β` match the controlling M3 definition? If not, state the exact controlling definition and required conversion.
2. Is the target bridge’s population-oracle estimand correctly aligned with Revision F, and are its numerical method and tolerances adequate?
3. Is the distinction between the mechanistic NC2 question and v0.3 Phase 1 power/Type I error validation correctly stated?
4. Are the GO / ALTERNATIVE / STOP conditions logically complete without claiming that a feasibility failure falsifies the theory?
5. Are there any scientific blockers to the *bridge calculation itself*, as distinct from blockers to Phase 1 or real data collection?

## 10. Source anchors

- v0.3-P Phase 0 Design, Revision F, especially §§1–3, 5A–5B, 7, 9–12, on branch snapshot `4551cac`: `v03p/PHASE0_DESIGN_2026-10-15_RevF.md`.
- NC1 rev-3 report on branch snapshot `4551cac`: `v03p/nc1/nc1_report.md`.
- NC1 engine definition of `c* = (1.25/β)^2` and scenario threshold set: `v03p/nc1/nc1_calc.py`.
- NC1 RUN record through M1b: `v03p/nc1/RUN.txt`, commit `4551cac`.

**Status line:** This VDraft is a proposal for review only. No new computation or study phase is authorized by its creation.
