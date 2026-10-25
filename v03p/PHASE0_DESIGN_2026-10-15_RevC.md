# v0.3-P Phase 0 Design — Revision C

**Dates:** drafted 2026-10-14 (working session); circulated for review 2026-10-15 as Revision B; revised 2026-10-15 as Revision C after GPT's NOT-APPROVED review (four findings). Uncommitted — no git commit timestamp exists; the effective freeze date is unset until a freeze actually occurs. The Revision B draft is preserved as-reviewed.
**Status:** DRAFT for independent review (GPT, CLAUDE, GLM). Uncommitted; not frozen. This is a **new uncommitted document** superseding the Revision B draft (`v03p/PHASE0_DESIGN_2026-10-15.md`, uncommitted, preserved as-reviewed after GPT's NOT-APPROVED verdict with four findings), which itself superseded `v03p/PHASE0_DESIGN_2026-10-14.md` (commit `3cd62b8`, preserved unamended). It incorporates the committed review findings of `v03p/PHASE0_REVIEW_RESPONSE_2026-10-14.md` (commits `4018ebd`, `edae42c`) and the two owner decisions recorded 2026-10-14. Commit requires independent review sign-off plus explicit owner approval. **Design freeze occurs in two boundaries defined in §11–§12: the simulation-protocol freeze (before Phase 1) and the study freeze (after Phase 1 passes).** This document does not authorize Phase 1 simulation, solver generation, or hidden-outcome collection; each requires a separate owner authorization (§12). It is not an adequately identified evaluation and is not described as one. Revision C addresses GPT's four findings without freezing, authorizing, or deciding anything reserved to reviewers or the owner.

v0.3 is the first *proposed* design intended to test the predictive question in a new generation population, conditional on passing its design, simulation, and feasibility gates.

## 0. Corrections relative to the 2026-10-14 design (`3cd62b8`)

| Old design location | Correction in this revision |
|---|---|
| §6 "likelihood ratio" phrasing for δ* | Replaced by the multiplicative-contrast-under-additive-log-loss qualification (§3); e^(20Δ) is not a literal likelihood ratio for the joint 20-input vector and implies no input independence |
| §8 "[1, 24]" potentially identifiable range | Corrected to **2 ≤ k ≤ 24** (k=1 forces C=1; no within-k variation possible) |
| §9 line 83 body-only resampling | Replaced by the crossed two-way procedure over body and suite identities (§7) |
| no outcome-variation criterion | New outcome-variation feasibility gate (§6), aligned to the outcome-blind analysis support (§5) |
| no support-eligibility rule | New outcome-blind identifiability gate defining the analysis support (§5) |
| no duplicate/estimand-unit rule | Owner decision E adopted; full rule in §4 |
| no failure-disposition clause | Termination rule and timing discipline in §8 |

### 0.1 Change ledger (Revision B; each change cites the finding it repairs)

| Change | Source |
|---|---|
| Header chronology; freeze date unset | Final Work Order §9 |
| §0.1 ledger | Final Work Order §10 |
| §1 inference-target pointer (G6a/G6b open) | Final Work Order §7 |
| §3E normalization without whitespace stripping; cross-phase duplicate rule | GPT finding 7; CLAUDE suggestion (confirm at sign-off) |
| §4 interface/validity rewrite; versioned checker artifact | GPT finding 1; Final Work Order §2 |
| §5 exact design matrices; support-only fitting; rank-increase test; training-block rule | GPT finding 3; Final Work Order §3 |
| §6 tail-scale pointer | Final Work Order §4 (deterministic assessment) |
| §7 G6a/G6b options; training-support handling; three-site O2 note | Final Work Order §7 |
| §7.4 standard-library RNG + deterministic seed derivation | Final Work Order §3 |
| §9 2δ* claim mapping | Final Work Order §4 |
| §9.1 constrained DGP; uniformity 1/Z(k); C summaries; outcome tails; γ* distinction; misspecification statement | Final Work Order §4 |
| §9.2 corrected tables; block readings; O1–O5 table (none chosen) | Final Work Order §5; self-found §7 ambiguity |
| §9.3 sample-unit mapping | Final Work Order §6 |
| §10 recomputed budget arithmetic; scenario-(c) correction | Final Work Order §5 |
| §11–§12 two authorization boundaries | GPT finding 2; Final Work Order §9 |
| Appendices C–D (arithmetic provenance; decision register) | Final Work Order §10 |

### 0.2 Change ledger (Revision C; each change cites the GPT review finding it addresses)

| Change | Source |
|---|---|
| §5A matrix contradiction stated; M1/M2/M3 candidates with consequences; κ≤30 retained-but-flagged | GPT-R1; instruction 1 |
| "bucket-local" relabeled bucket-local throughout; complete-rule probability stated as 0 as-drafted; recalculation recipe deferred | GPT-R2; instruction 2 |
| Phase 1 grid/gate/power-cell incompatibility documented; grid reassessment deferred; tail expectations recomputed on bucket-local support with N_s sensitivity labels | GPT-R3; instruction 3 |
| "true effect" relabeled planted population-oracle contrast; G6-conditional calibration mapping; FPR/power non-claim | GPT-R4; instruction 4 |
| Verification: GPT provenance confirmation recorded; runtime report; feas_check.py + outcome_tails_c.py (additive; Rev-B scripts byte-unchanged) | instruction 5 |
| §11 +2 freeze items (matrix resolution; complete-rule recalculation); Appendix B/C/D updates | instructions 1, 5 |

## 1. Research question and estimand

**Question.** Does the failure-concentration statistic C carry predictive information about held-out per-input failure probability beyond the failure count k, in a newly generated population of solver bodies?

**Estimand (unchanged from `3cd62b8` §2; verified).** Δ = E[ L(baseline) − L(extended) ] over the **joint population of solver bodies and hidden suites**, where L is held-out log-loss **per hidden input** and positive Δ means C helps. The baseline model uses k only; the extended model uses (k, C). This is **not** a contrast between adjacent-k groups.

**Inference target (open owner decision; see §7).** The estimand above is stated in the conditional form (G6a: conditional on the realized training block). The unconditional full-procedure form (G6b), the implications of each, and their costs are presented in §7 without a choice; the choice is Foued's.

**Outcome.** The modeling outcome per (body, suite) pair is the **soft label s/20** (s = number of the 20 hidden inputs passed; `study/features.py:81-94`, `v02/models_v02.py:83`, `v02/run_pilot_v02.py:43-60`). The pass-all binary is **not** the outcome.

**Statistic definition (instrument; frozen).** C = max_j f_j / k for k ≥ 1, with f_j the number of failures in family j over 5 probes (`study/features.py:55-60`); 6 families × 5 probes = 30 probes (`study/families.py:35-44`, `study/probes.py:73-97`). k = 0 forces C = 0; k = 1 forces C = 1; k ≥ 25 forces C = 5/k. Family counts are discrete: at k = 24 the minimum attainable C is 4/24 and the maximum is 5/24; not every intermediate value is attainable.

## 2. Vocabulary (binding)

- **Potentially identifiable range:** 2 ≤ k ≤ 24 — the set of k where within-k variation in C is mathematically possible. Membership is maximum possible support only; it never establishes estimator eligibility.
- **Observed identifying support / analysis support:** the set of bodies that passes the preregistered outcome-blind identifiability gate of §5. The primary estimate and the feasibility gate both operate only on this support.
- Neither v0.1 nor v0.2 established observed identifying support (zero within-k C variation in both; response doc §1–§2).

## 3. Owner decisions (recorded 2026-10-14)

**C — minimum meaningful effect: ACCEPTED (r = 1.5).** Owner statement, adopted verbatim:

> I accept r = 1.5 as my chosen minimum meaningful separation for this study. This is an operational decision threshold for prioritizing candidates for an expensive confirmation slot, not a value derived from measured costs.

Operationalization: δ* = ln(1.5)/20 = 0.020273255405408218, a per-hidden-input log-loss threshold. **Statistical qualification (binding):** ln(1.5)/20 corresponds to a **1.5-fold multiplicative score contrast over 20 inputs under the additive log-loss scoring interpretation** — e^(20Δ) is a multiplicative contrast, **not a literal likelihood ratio for the joint 20-input outcome vector**, and nothing in this design implies the 20 inputs are independent replications. δ* is an operational decision threshold, not a value derived from measured costs; no measured cost ratio exists. v0.2's δ = 0.01 is not adopted.

**E — duplicate estimand unit: ADOPTED (Option 1, unique normalized bodies).** The estimand is over **unique normalized, valid solver bodies**. Each distinct body counts once toward support and scoring. Duplicate generation attempts remain in the provenance record but add no additional statistical weight. Normalization rule (frozen, deterministic, no semantic-equivalence detection): normalize line endings CRLF/CR to LF and ensure exactly one trailing newline; canonical identity = SHA-256 of the canonical bytes. Trailing-whitespace stripping is explicitly NOT performed: it can alter Python triple-quoted string contents. Consequence accepted: bodies differing only in trailing whitespace are distinct canonical identities. All occurrences of one canonical identity are assigned to the same fold; only one occurrence is scored. The duplicate rate (1 − unique/attempts) is reported as a generator property.

**Cross-phase duplicates (outcome-blind rule).** If one canonical body hash appears in both the feasibility and confirmatory attempt sets, the deterministic assignment is: the body belongs to FEASIBILITY and is removed from the confirmatory population; the confirmatory attempt remains in the provenance log with its hash, adds no statistical weight, and is counted in duplicate reporting. Assignment is decided by canonical-hash comparison before any hidden outcome of either phase is collected. Effect on targets: such bodies do not count toward the confirmatory unique-body target or effective sample count.

## 4. Generation procedure, validity, and budget

**Generator (when separately authorized; §12).** A single identical prompt for all bodies (no strategy directives — this is the deliberate contrast with v0.1's directed generation). Before generation: the exact model identifier, sampling parameters, prompt text, and session date are recorded and frozen; pack size and retention rules recorded. The population is the valid outputs of this specified procedure.

**Interface contract (existing; `specs/generator_spec.json:7,17`).** Language: Python. Entry point: `solve(n, edges, s, t) -> int`. Dependencies: Python standard library only. Return contract: the minimum total weight as an int, or `-1` if `t` is unreachable; the body must not read files or print. A `bool` return does not qualify as an integer result for this study.

**Validity check (frozen before generation).** Static validity only, on the frozen Python toolchain: the module parses and loads via `importlib` (`study/features.py:15-27`); exposes a module-level function with the exact frozen signature above; and passes an AST scan enforcing a frozen import allowlist and the absence of file-read/print statements (the frozen prompt contract, `specs/generator_spec.json:7`). Output conformance (int, non-bool, `-1` sentinel) is enforced at run time by the frozen harness (`study/features.py:38-44`) and is a behavioral matter, not a validity change. The checker is a versioned artifact (specification v0.3-P-1: mechanism, allowlist content, no-IO pattern list); its SHA-256 is recorded at the simulation-protocol freeze (§11). No manual review, no post-hoc edits.

**Retention and reporting.** Every generation attempt is retained in the provenance record with its canonical hash. Invalid-submission rate and valid-body count are reported; the invalid rate is itself a result about the generation process. Target population: valid outputs of the specified generator, conditional on the frozen validity criteria — not every attempted output, not LLM solvers generally.

**Budget (candidate; freeze-blocker §11).** Fixed attempt budgets, set before any generation: confirmatory N = 600 attempts; feasibility N = 150 attempts (separate draws, disjoint body and suite identities). The attempt/valid/unique/in-range/supported unit mapping for these budgets is in §9.3. No best-of selection, no silent replacement, no outcome-driven resubmission, no silent dedup. A valid-sample shortfall against preregistered support requirements within budget is feasibility failure (§8). Wrong answers, runtime exceptions, and timeouts after passing validity are behavioral failures, not grounds for exclusion.

## 5. Outcome-blind identifiability gate (defines analysis support)

**Purpose.** Decide which bodies enter the analysis support, using **no hidden outcomes of any kind** — neither feasibility nor confirmatory. Inputs to the rule: k, C, canonical body identity, suite identity only.

**Rule (candidate numbers; freeze-blocker §11).** A k-bucket (the set of canonical bodies sharing a k value) is **included in analysis support** iff all of:

1. 2 ≤ k ≤ 24 (potentially identifiable range);
2. ≥ B_min = 8 distinct canonical bodies in the bucket;
3. ≥ 2 distinct C values in the bucket (strict minimum for within-k variation);
4. both C extremes of the bucket are represented by ≥ 4 distinct bodies each.

**Design matrices (reference: `study/models.py`).** Baseline columns: [1, rcs_basis(log(1+k))] — five columns including the intercept, with rcs_basis the restricted-cubic-spline basis of x = log(1+k) at knots KNOTS = [1.0986122886681098, 1.6094379124341003, 2.302585092994046, 2.995732273553991, 3.4339872044851463] (log(1+k) at k ∈ {2, 4, 9, 19, 30}), as implemented in `study/models.py:17-34`. Extended columns: the baseline columns plus the scalar C column (six columns). Fixed ridge constant RIDGE = 1e-6; solver fallback pivot floor 1e-12 (`study/models.py:8-10,44-58`). With only three in-range k-values the baseline matrix cannot have full column rank; the ridge and pivot floor are recorded implementation facts and do not substitute for the identification check below.

**Fitting population (binding, consistent with §2).** Fitting uses only training-block bodies that belong to the analysis support; scoring uses eligible test-block cells. Out-of-support bodies enter neither fitting nor scoring.

**Rank/conditioning check.** On the realized analysis design matrix: rank(extended) − rank(baseline) must be ≥ 1 (C contributes an independent design-matrix dimension beyond the k-basis), computed on the column-standardized matrix (non-intercept columns centered to zero mean and scaled to unit SD over the in-support rows; intercept as-is) with the frozen analysis toolchain's matrix rank at its recorded tolerance; the condition number of the same standardized extended matrix must be ≤ κ_max = 30 (candidate). If the check cannot be evaluated, or if adding C contributes no independent dimension (rank increase 0), the run is INFEASIBLE (no estimation; §8). No threshold is relaxed post hoc.

**Training-block support rule (reuses the §5 numbers above; none new).** The primary training block must contain ≥ 2 included k-buckets and ≥ B_min in-support bodies; otherwise the primary split is INFEASIBLE (mirrors the §7 test-block rule).

**§5A. Known contradiction in the conditioning rule (GPT-R1; blocks freeze).** The baseline design matrix has five columns (intercept + four RCS columns), all deterministic functions of k (`study/models.py:17-34`). Fitted only on analysis-support bodies, whose in-range k values are {5, 10} under scenarios (a)/(c) and {5, 10, 20} under (b):

| Scenario | Distinct in-range k | Baseline rank (verified) | Extended rank (max) | Conventional κ |
|---|---|---|---|---|
| (a) | {5, 10} | exactly 2 | ≤ 3 | infinite |
| (b) | {5, 10, 20} | exactly 3 | ≤ 4 | infinite |
| (c) | {5, 10} | exactly 2 | ≤ 3 | infinite |
| (d) | none | no usable support | — | — |

Baseline rank is exactly #{distinct k}: at two k values the intercept and x = log(1+k) columns are independent (2×2 minor det = log(11/6) ≈ 0.606); at three k values all ten 3×3 minors are clearly nonzero (min |det| ≈ 7.0e-05 against a ~1e-14 noise floor; `feas_check.py` T4). The six-column extended matrix therefore has rank at most 4 < 6 in every scenario: its conventional condition number is infinite, never ≤ 30. The rank-increase test IS satisfiable — conditions 3–4 force within-k C variation in some included bucket, and a C vector varying within one k-slice is linearly independent of every k-function, so rank(extended) = rank(baseline) + 1 whenever the bucket rule passes. The κ ≤ 30 clause, as stated (conventional condition number), is the sole impossible conjunct; it is retained in the text above but flagged CONTRADICTED-PENDING, not deleted.

**Consequence.** Under the stated complete rule (conditions 1–4 AND rank-increase AND conventional κ ≤ 30), P(pass) = 0 in every scenario at every size — structural, not estimated. All bucket-local probabilities in §9.2/§10 (conditions 1–4 only) stand unchanged; they omit the rank-and-conditioning criterion.

**Candidate resolutions (none adopted; reviewers recommend, Foued decides per the routing below):**
- **M1 — lower-dimensional fixed baseline, e.g. [1, x] with x = log(1+k).** Exact columns: intercept, x; extended adds C (three columns). Rank: full (3) whenever conditions 3–4 pass (C varying within one k-slice is independent of {1, x}). Conventional κ finite and meaningful; κ_max = 30 preserved with no new threshold; the rank-increase test becomes implied-by-bucket-rule. Consequences: model-family change (abandons the RCS flexibility; at two k values [1, x] is saturated so "well-specified" holds trivially, at three it is restrictive); the κ ≤ 30 filter still binds probabilistically, so complete-rule probabilities must be recomputed post-decision (recipe: bucket-local sum ∧ κ(Z_pass) ≤ 30 over C-composition patterns). Requires explicit Foued approval (model change); reviewer re-verification of §9.1/Phase-1 artifacts under the new forms.
- **M2 — redefined conditioning diagnostic on the estimable subspace (κ_eff); models unchanged.** Exact definition: κ_eff = σ_1/σ_r on the column-standardized extended matrix (standardization as in the rank check), where r counts singular values above the rank tolerance τ; τ is a numerical parameter recorded at the simulation-protocol freeze, not a gate threshold; κ_max = 30 preserved (no replacement threshold). Relationship to the existing fit: the existing reference fit (`study/models.py:61-80`) is ridge-penalized IRLS logistic regression with λ = RIDGE = 1e-6 on all columns including the intercept, solved with a 1e-12-floored Gauss-Jordan — its operator (X'WX + λI) uses outcome-dependent weights and therefore cannot enter the outcome-blind §5 gate; κ_eff gates the unweighted proxy only, and unidentified directions remain silently ridge-regularized (the interval then covers estimable contrasts only — coherence with the G6 choice required). A regularized-matrix variant κ(Z'Z + λI) with the frozen λ = 1e-6 is NOT viable: κ ≈ λ_max/1e-6 ≫ 30 for any support size (λ_max ≥ trace/6), so it would need its own (λ, κ) pair — new numbers requiring owner approval. Consequences: no model change; gate controls estimable directions only; complete-rule probabilities recomputed post-decision (same recipe with κ_eff). Requires reviewer sign-off on the exact mathematics plus Foued's acceptance (gate-semantics change).
- **M3 — bucket fixed effects + C (the pre-Revision-B family).** Exact columns: q bucket dummies (q = 2 or 3; nonempty buckets guaranteed by condition 2) plus C. Rank: full (q+1) iff C varies within some bucket — implied by conditions 3–4; conventional κ finite and meaningful; κ_max = 30 preserved. Consequences: model-family change contradicting the `study/models.py` RCS implementation (implementation must be rewritten and re-verified; all §9.1/Phase-1 artifacts re-derived under the new forms); changes the meaning of "C beyond k" (beyond bucket means rather than beyond a smooth k function); complete-rule probabilities recomputed post-decision. Requires explicit Foued approval (model change); full reviewer re-verification.

The rank-increase ≥ 1 test is retained as stated (implied by the bucket rule under every candidate, hence never the binding conjunct). The conventional κ ≤ 30 clause is retained but flagged CONTRADICTED-PENDING until one candidate is adopted; it blocks the simulation-protocol freeze (§11).

**Separate application.** The same rule is applied **separately** to the feasibility population (§6) and the confirmatory population (§7), each computed from that population's own (k, C) values. Confirmatory outcomes are never used to select or revise the support; feasibility outcomes are never used to select or revise the confirmatory support. If the confirmatory support is inadequate after the rule (fewer than 2 included k-buckets, or fewer than B_min distinct bodies total), the confirmatory run is INFEASIBLE (§8).

## 6. Outcome-variation feasibility gate

**Purpose.** Establish, on separate feasibility material, that the modeling outcome (soft label s/20) exhibits usable variation on the analysis support, before any confirmatory estimation.

**Sample.** The predesignated feasibility sample (§4 budget): bodies and suites **distinct from all confirmatory material**. Confirmatory outcomes are never inspected to decide feasibility; feasibility outcomes never enter estimation.

**Statistic population (aligned to §5; binding).** Feasibility-sample (body, suite) pairs **whose body belongs to the feasibility-population analysis support defined by §5** — not range membership alone. Variation occurring only among out-of-support bodies cannot pass the gate.

**Binding criterion — tail counts (candidate numbers; freeze-blocker §11).** With θ_lo = 0.25 (≤ 5/20 successes) and θ_hi = 0.75 (≥ 15/20 successes):

- ≥ M = 30 pairs with s/20 ≤ θ_lo, and ≥ M = 30 pairs with s/20 ≥ θ_hi;
- within the lower tail: ≥ D = 10 distinct canonical bodies and ≥ S = 6 distinct suites;
- within the upper tail: ≥ D = 10 distinct canonical bodies and ≥ S = 6 distinct suites.

Variance of s/20 over the gate population is recorded with threshold v_min = 0.01 as a **secondary diagnostic only**; variance alone can be driven by outliers and is not the binding criterion. A pooled correct/incorrect rate over hidden inputs is **not** an acceptable gate statistic (it can pass while every pair has the same success fraction).

**Timing.** θ_lo, θ_hi, M, D, S, v_min, and the §5 numbers are fixed **before** any feasibility-sample hidden outcomes are collected (§8). Whether the proposed outcome-DGP parameters yield both gate tails at feasibility size is assessed deterministically in §9.1; the gate numbers here are candidates independent of that assessment.

**Precedent, not inheritance.** v0.2's pilot gate2 (≥ 10% correct and ≥ 10% incorrect among pairs' hidden inputs; `v02/run_pilot_v02.py:18-19,72-76`) pools inputs and ignores pair-level variation; it is not adopted.

**Disposition.** Gate failure **terminates v0.3** (§8).

## 7. Crossed evaluation procedure (confirmatory)

**Formation (both axes unseen).** Two-way holdout over canonical body identities and hidden-suite identities, from the master seed (§7.4). Per repetition: a held-out subset of body identities (25%) and of suite identities (25%); the remaining 75% on each axis is training. The **training block** = training bodies × training suites; the **test block** = held-out bodies × held-out suites; the **mixed (off-diagonal) blocks** are used for neither training nor scoring, so no test body or suite is seen in training in any form. The split-level minimum (O2) covers three sites — global (§5), training block, test block — as one coordinated resolution (§9.2); no site-specific minimum is adopted here.

**Primary split and robustness repetitions.** The **primary analysis uses one preregistered split** (drawn from the master seed, fixed before outcomes). Robustness: R = 50 additional seeded splits are scored and the distribution of per-split Δ̂ is **reported as a sensitivity diagnostic only**; it does not enter the point estimate or interval. This removes any aggregation ambiguity over overlapping test appearances.

**Scoring and aggregation.** Per eligible held-out (body, suite) cell in the test block: compute the per-hidden-input log-loss difference (extended − baseline, sign-flipped so Δ̂ is baseline − extended). Eligibility: the held-out body is in the confirmatory analysis support (§5 rule, computed outcome-blind on the full confirmatory population). Δ̂ = equal-weight mean over eligible test-block cells. Every held-out body is scored on every held-out suite, so equal weight per cell coincides with equal weight per body among eligible cells. Suite-level exclusions or incomplete cells must not be silently reweighted; discard/recompute rules are fixed in the analysis code before outcomes are collected and recorded here at freeze.

**Uncertainty.** *Primary:* two-way cluster bootstrap — resample eligible test-body identities with replacement and eligible test-suite identities with replacement, independently; score the intersection cells; B = 2000 resamples; percentile interval at nominal 95%. *Fallback:* crossed random-effects (variance-components) interval with body and suite as crossed factors. The procedure carried forward is the one that passes the Phase 1 coverage gate (§9); if neither passes, Phase 1 stops with an interval-procedure failure and the predictive question is not tested with intervals under v0.3. The v0.2 overlapping-fold bootstrap remains barred without a coverage test.

**Inference target (open owner decision; G6a vs G6b — neither adopted).**
- **G6a (conditional; minimal change).** The primary interval is conditional on the realized training block: it targets Δ(train), the expected loss difference over the §7 population given the observed 75% training identities. The R = 50 re-splits are a reported sensitivity diagnostic over training draws, not pooled into the estimate or interval. Cost: one fit per model plus the 50 diagnostic refits.
- **G6b (full pipeline).** Each of the B = 2000 replicates re-draws the 75/25 split and refits both models; the interval targets the unconditional Δ of the full split-fit-evaluate learning procedure; the R = 50 diagnostic is subsumed. Cost: 2000 × 2 fits per cell per replication — orders of magnitude above G6a.
- The current one-primary-split plus 50 sensitivity splits is not equivalent to full-pipeline inference: under G6a the 50 splits do not contribute to the estimate or interval. Reviewers recommend; Foued chooses.

**Inadequate support in the primary split.** If the primary test-block support has < 2 included k-buckets or < B_min distinct bodies, the confirmatory result is INFEASIBLE (no estimation; §8). Inadequate training support is handled the same way via the §5 training-block rule: no fitting on a deficient block, no silent fallback. No threshold is relaxed post hoc.

**7.4 Seeds.** Master seed **20261015**, fixed here before any data. All randomness (splits, bootstrap resamples, Phase 1 simulation) derives from the Python standard library: `random.Random` instances seeded by deterministic 32-bit child seeds, child_seed = int.from_bytes(SHA256("20261015/{stream}/{index}"), "big") mod 2^32 computed with `hashlib`, one stream per use (splits, bootstrap, Phase 1 draws); the pinned CPython version is recorded at the simulation-protocol freeze. NumPy is not required and not specified; adopting a pinned NumPy dependency would need an explicit decision. Seeds and spawned states are logged with results.

## 8. Threshold timing and failure disposition (binding)

- **Two threshold sets, each frozen before the data it judges is observed:** (i) diagnostic/range thresholds (§5 support rule); (ii) hidden-outcome thresholds (§6 gate; §9 coverage/power targets). Neither set may be chosen or adjusted after observing its data.
- **Order of operations.** Simulation-protocol freeze (§11 Stage 1) → (separate authorization) Phase 1 simulation → study freeze (§11 Stage 2) → (separate authorization) feasibility generation and gate → gate pass → (separate authorization) confirmatory generation → confirmatory estimation. Confirmatory hidden outcomes are never collected before the gate passes.
- **Failure disposition.** A feasibility-gate failure, an inadequate-support finding, or an invalid-sample shortfall within budget **terminates v0.3**. It is not followed by prompt tuning, switching to constructed solvers, probe-suite redesign, threshold relaxation, or resubmission. Any such pursuit is a separate owner decision after a deliberate pause, under a new charter.
- **No forecast.** The v0.1 and v0.2 populations create a **material feasibility risk** (dominant k=0 mass; zero within-k C variation in both) but do not establish the probability of gate failure under the single-prompt generator — the two generation procedures are different, and neither predicts the other (§10). Gate failure is a possible outcome; the disposition applies regardless of prior expectation.

## 9. Phase 1 — software simulation (separately authorized; §12)

**Nature.** Fully synthetic: bodies, suites, k, C, and soft labels are drawn from declared generative models. **No LLM calls, no real solver generation, no real hidden outcomes.** Purpose: validate the operating characteristics of §5–§7 (interval coverage; gate false-pass/false-fail; power/FPR) before any real data exists.

**Grid (candidate; freeze-blocker §11).** Full crossing: bodies N_b ∈ {60, 120}; suites N_s ∈ {20, 40}; support scenario ∈ {a, b, c, d} (§10); planted population-oracle contrast Δ_oracle ∈ {0, δ*, 2δ*} (NOT the procedure's predictive gain — see the calibration note below); duplicate rate ∈ {0%, 25%}. 96 cells. Re-anchoring the grid to the attempt/budget scale is open under O1 (§9.2); the grid above is unchanged pending that decision. Grid reassessment as a whole is deferred until the §5A resolution.

**Replications and Monte Carlo uncertainty.** 2000 replications per cell (binomial SE on coverage ≈ 0.006 at p = 0.925). Coverage decision rule: for each cell, the one-sided 95% Clopper–Pearson lower bound of estimated coverage must be ≥ 92.5% (candidate number; freeze-blocker §11). This accounts for Monte Carlo error explicitly rather than comparing a point estimate to the threshold.

**Targets (fixed now; evidence produced by Phase 1).**

- *Coverage:* passes as above, in **every** cell, including thin-support cells. Known caveat (recorded): the two-way bootstrap undercovers with few bodies and few suites; those cells exist precisely to expose this.
- *FPR:* at Δ = 0, two-sided interval excludes 0 in ≤ 5% of replications (per cell).
- *Power:* at Δ = 2δ*, interval excludes 0 in the direction of the extended model in ≥ 80% of replications under scenario (a) at N_b = 120, N_s = 40; power under thinner scenarios is reported, not gated.
- *Gate characteristics:* false-pass and false-fail rates of §6 under each scenario are reported; the gate's thresholds are not adjusted in response.

**Claim mapping (binding).** FPR = 5% at Δ = 0 controls false claims of ANY predictive gain. The 80% power gate applies at 2δ*: the design reliably detects gains of at least twice the owner's minimum meaningful effect. Power AT δ* is reported, not gated — δ* is the owner's decision threshold (decision C) and the design claims no reliable detection exactly at it. Detection of any positive gain is not a gated claim. The 80% target at 2δ* tests power to have the interval exclude zero under the larger effect; it is not an 80% power guarantee at δ*. Recorded explicitly as a limitation.

**Effect calibration (binding interpretation; GPT-R4).** "True effect" in the grid means the planted population-oracle contrast: the §1 estimand evaluated on DGP truth at the planted γ* (γ* from bisection, tolerance 1e-4 on Δ). It is NOT the finite-sample fitting procedure's expected loss difference: at γ = 0 the oracle benefit of C can be zero while a fitted extended model differs by estimation noise and regularization, and at γ* > 0 the procedure-level gain differs from Δ_oracle by bias and noise. The 5% FPR and 80% power claims are claims about the procedure's interval behavior at the planted oracle values — they do not validate the intended predictive estimand. The mapping to the selected inference target is conditional and deferred: under G6a the relevant procedure target would be Δ(train) at the realized training block; under G6b the unconditional full-procedure Δ; the current oracle γ* coincides with neither in finite samples. After the G6 choice and the §5A model resolution, γ* is recalibrated to the selected target, or the targets are restated. Until then, no FPR/power result may be read as validating the predictive estimand.

**Failure.** Any coverage, FPR, or interval-procedure failure stops Phase 1; the predictive question is not tested under v0.3 until a redesigned procedure passes its own preregistered simulation (new authorization).

## 9.1 Data-generating processes (candidate; freeze-blocker §11)

**Simulation altitude.** Phase 1 operates at the count/label level: no graphs, probes, or solvers are generated. Each replication draws body-level (k, C), body and suite latents, and per-(body, suite) soft labels from the declared models below; the unmodified analysis code path of §5–§7 runs on the simulated data.

**Body-level k draw (per scenario), k ~ categorical:**
- (a) {0: .80, 5: .10, 10: .05, 25: .05} — in-range mass .15 (historical v0.1 shape)
- (b) {0: .75, 5: .075, 10: .025, 20: .025, 25: .125} — .125 (historical v0.2 shape)
- (c) {0: .94, 5: .03, 10: .02, 25: .01} — .05
- (d) {0: .90, 25: .10} — 0
Within-range splits for (a)/(b) are the historical-conditional shapes; alternative within-range mixes are an open option (§9.2, O4). The historical samples behind the within-range splits (3 in-range bodies for v0.1, 15 for v0.2) are weak estimates of their within-range distributions, not reliable forecasts.

**Family composition → C (body-level; suite-independent).** p ~ Dirichlet(1,1,1,1,1,1); f ~ Multinomial(k, p) over the 6 families, **conditional on the feasibility constraints** sum(f_j) = k and 0 ≤ f_j ≤ 5 (five probes per family); C = max_j f_j / k (k = 0 → C = 0). With the symmetric parameterization the conditional distribution is **uniform over feasible count vectors for fixed k**, with probability 1/Z(k) per feasible vector (Z(5) = 252, Z(10) = 2247, Z(20) = 2247, Z(24) = 456; verified by exact enumeration in `dgp_counts_v2.py`). Only attainable C values are generated and within-k variation exists for every k in 2..24. Deterministic C summaries: k = 5: C ∈ {0.2, 0.4, 0.6, 0.8, 1.0}, E[C] = 0.528571, P(C = 0.2) = P(C = 1.0) = 0.023810; k = 10: four attainable values in [0.2, 0.5], E[C] = 0.407744; k = 20: C ∈ {0.2, 0.25}, P(C = 0.25) = 0.943925, P(C = 0.2) = 0.056075.

**Duplicates.** ρ ∈ {0, .25}: slots drawn in order; each slot after the first copies an earlier slot with probability ρ (byte-identical body → same k, C, and body latent), else fresh draw. §3E applies (one occurrence scored, same fold).

**Outcomes (PROPOSED parameters; not validated).** Per (body, suite): logit(p) = m(x) + γ·C + u + v, x = log(1+k), m(x) = θ0 + θ1·x, u ~ N(0, σ_b²) (body), v ~ N(0, σ_s²) (suite), s ~ Binomial(20, p); soft label = s/20. Proposed: θ0 = 0, θ1 = −1, σ_b = σ_s = 1. Baseline is well-specified (linear in x; the RCS basis spans it); extended adds γ·C only. Deterministic tail-scale assessment at γ = 0 (per-pair fractions from `dgp_outcome_tails.py` — Simpson quadrature, 81- vs 161-node grids agree to 6e-12 — crossed with bucket-local support expectations in `outcome_tails_c.py`): per-pair P(s/20 ≤ 0.25) ≈ 0.75 and P(s/20 ≥ 0.75) ≈ 0.026 under the scenario-(a) mix (0.775/0.023 under (b), 0.757/0.024 under (c)). Expected tail pairs = E[bucket-local-support bodies] × N_s × per-pair fraction (pair-exchangeability assumed; N_s ∈ {20, 40} are sensitivity cases S20/S40 — the real-study suite count is owner-open, not adopted). The lower tail passes in expectation at most sizes; the upper tail does NOT: best case (a) @ N_b = 600 / S40 gives ≈ 26.5 expected upper-tail pairs vs M = 30 required, and at feasibility size (N_b = 150) the expectation is ≈ 2.2 with E[bucket-local support] ≈ 2.1 bodies — the per-tail diversity floors (D ≥ 10 bodies, S ≥ 6 suites) are unreachable in expectation under every scenario. (The Revision B assessment used count-rule support and overstated the upper tail by ~9×.) Any "spans both gate tails" characterization is therefore dropped; θ0, θ1, σ remain PROPOSED values pending reviewer sign-off and owner acceptance (§11).

**Planted effect.** γ = 0 for Δ = 0. For Δ ∈ {δ*, 2δ*}: γ* by bisection (tolerance 1e-4 on Δ) so the DGP population value of §1's estimand equals the target, using a fixed calibration seed and large Monte Carlo size from DGP truth (simulation-internal; never from real data). **γ* calibrates the population-oracle contrast** (the estimand evaluated on DGP truth), **not finite-sample learning-procedure performance**; the latter is what Phase 1 measures and reports (coverage, FPR, power of the procedure). Relation to the G6a/G6b inference targets: see the §9 calibration note (recalibration deferred until the G6 choice and the §5A resolution).

**Baseline misspecification.** Phase 1 does not assess robustness to baseline misspecification: the simulated baseline is well-specified by construction. No robustness is implied. (A misspecification sensitivity scenario would be new procedure and is not added here.)

**Explicitly not modeled in Phase 1 (open option §9.2/O1):** invalid-submission rate, prompt/generation mechanics, probe-suite graph structure — Phase 1 is conditional on valid unique bodies unless a declared p_valid parameter is added.

## 9.2 Feasibility of the drafted rules under the drafted DGP (disclosed before freeze; decision required)

Exact deterministic arithmetic (log-space; `feas_prob.py`, `feas_prob_test.py`; provenance in Appendix C). Two results are kept separate: (1) the exact count-only support bound, ignoring §5 conditions 3–4; (2) the bucket-local support-feasibility calculation accounting for C variation and the extreme-representation conditions (observed-extremes reading), with remaining omissions stated below. "Bucket-local" means conditions 1–4 only: the rank-and-conditioning criterion is omitted, and the complete-rule probability is 0 as-drafted (§5A). Complete-rule probabilities will be recalculated after the §5A resolution (recipe: bucket-local sum ∧ conditioning pass over C-composition patterns). The split uses the exact fixed-size hypergeometric holdout (T = round-half-up(0.25·N) body identities); no binomial thinning. N below denotes unique valid bodies; the attempt-budget mapping is in §9.3. No count-only probability is the probability that the full study passes all gates.

**Full-population probabilities** — count-only P(≥2 in-range buckets, each ≥ B_min = 8 bodies) | bucket-local P(≥2 buckets pass the full §5 rule):

| N_b | (a) cnt | (a) bl | (b) cnt | (b) bl | (c) cnt | (c) bl | (d) |
|---|---|---|---|---|---|---|---|
| 60 | 0.001679 | 6.0e-06 | 1.1e-05 | 1.6e-08 | 4.4e-09 | 1.1e-11 | 0* |
| 113 | 0.177632 | 0.001117 | 0.008590 | 1.8e-05 | 3.1e-05 | 9.6e-08 | 0* |
| 120 | 0.229011 | 0.001546 | 0.013708 | 3.0e-05 | 6.5e-05 | 2.0e-07 | 0* |
| 150 | 0.469554 | 0.004279 | 0.060517 | 0.000157 | 0.000778 | 2.7e-06 | 0* |
| 240 | 0.915980 | 0.021882 | 0.445824 | 0.001939 | 0.045907 | 0.000226 | 0* |
| 300 | 0.984032 | 0.039534 | 0.729808 | 0.004937 | 0.170091 | 0.001075 | 0* |
| 400 | 0.999380 | 0.060552 | 0.955021 | 0.013897 | 0.499715 | 0.004845 | 0* |
| 450 | 0.999896 | 0.063514 | 0.985419 | 0.019730 | 0.651113 | 0.007832 | 0* |
| 600 | 1.000000 | 0.056830 | 0.999747 | 0.037421 | 0.910291 | 0.020446 | 0* |

(0* = structural zero: scenario (d) has no in-range mass. Scenario-(b) count-only figures supersede the prior table's three-bucket branch, which required all three buckets ≥ 8; scenarios (a)/(c) reproduce the verified figures exactly. The bucket-local column is non-monotone in N — e.g. (a) 0.0635 at 450 → 0.0568 at 600: at moderate bucket sizes, rare extreme C values are drawn but lack ≥ 4 copies. This is verified exact arithmetic, not error; see Appendix C.)

**Block readings at the budget-mapped sizes** (T = test bodies; CONS = test re-applies the count rule; LIB = liberal test support; TRN = training+test; bucket-local LIB/TRN use the bucket-local (conditions 1–4) support definition at population level):

| scenario @ N_b (T) | F_cnt | CONS | LIB_c | TRN_c | F_bl | LIB_bl | TRN_bl |
|---|---|---|---|---|---|---|---|
| (a) @ 113 (28) | 0.177632 | 2.8e-08 | 0.019603 | 0.019545 | 0.001117 | 0.000153 | 0.000153 |
| (a) @ 150 (38) | 0.469554 | 5.0e-06 | 0.127005 | 0.126965 | 0.004279 | 0.001381 | 0.001381 |
| (a) @ 450 (113) | 0.999896 | 0.177632 | 0.993802 | 0.993802 | 0.063514 | 0.063204 | 0.063204 |
| (a) @ 600 (150) | 1.000000 | 0.469554 | 0.999493 | 0.999493 | 0.056830 | 0.056805 | 0.056805 |
| (b) @ 113 (28) | 0.008590 | 3.9e-11 | 0.000454 | 0.000445 | 1.8e-05 | 1.1e-06 | 1.1e-06 |
| (b) @ 150 (38) | 0.060517 | 1.2e-08 | 0.007170 | 0.007130 | 0.000157 | 2.1e-05 | 2.1e-05 |
| (b) @ 450 (113) | 0.985419 | 0.008590 | 0.945538 | 0.945538 | 0.019730 | 0.017659 | 0.017659 |
| (b) @ 600 (150) | 0.999747 | 0.060517 | 0.997541 | 0.997541 | 0.037421 | 0.035749 | 0.035749 |
| (c) @ 113 (28) | 3.1e-05 | 3.8e-15 | 7.9e-07 | 7.2e-07 | 9.6e-08 | 2.8e-09 | 2.6e-09 |
| (c) @ 150 (38) | 0.000778 | 1.8e-12 | 3.0e-05 | 2.8e-05 | 2.7e-06 | 1.3e-07 | 1.2e-07 |
| (c) @ 450 (113) | 0.651113 | 3.1e-05 | 0.167638 | 0.167528 | 0.007832 | 0.002568 | 0.002567 |
| (c) @ 600 (150) | 0.910291 | 0.000778 | 0.451088 | 0.451077 | 0.020446 | 0.011857 | 0.011857 |

(P(no usable support in test | bucket-local support exists) ≤ 0.006 in every cell with support; the binding constraint is support itself, not the split. The conservative reading with conditions 3–4 re-applied at test level is statedly not computed.)

**O4 within-range-mix sensitivity** (historical splits as in §9.1; 50:50 two-bucket alternatives for (a)/(c); equal-thirds alternative for (b)):

| mix @ N_b | F_cnt | CONS | LIB_c | F_bl | LIB_bl |
|---|---|---|---|---|---|
| a-hist @ 150 | 0.469554 | 5.0e-06 | 0.127005 | 0.004279 | 0.001381 |
| a-50:50 @ 150 | 0.774938 | 1.3e-05 | 0.184835 | 0.013341 | 0.004305 |
| a-hist @ 600 | 1.000000 | 0.469554 | 0.999493 | 0.056830 | 0.056805 |
| a-50:50 @ 600 | 1.000000 | 0.774938 | 0.999930 | 0.070041 | 0.070035 |
| b-hist @ 150 | 0.060517 | 1.2e-08 | 0.007170 | 0.000157 | 2.1e-05 |
| b-thirds @ 150 | 0.194770 | 1.3e-08 | 0.019123 | 0.000450 | 4.2e-05 |
| b-hist @ 600 | 0.999747 | 0.060517 | 0.997541 | 0.037421 | 0.035749 |
| b-thirds @ 600 | 1.000000 | 0.194770 | 0.998947 | 0.111332 | 0.106044 |
| c-hist @ 150 | 0.000778 | 1.8e-12 | 3.0e-05 | 2.7e-06 | 1.3e-07 |
| c-50:50 @ 150 | 0.001071 | 2.5e-12 | 4.1e-05 | 3.8e-06 | 1.8e-07 |
| c-hist @ 600 | 0.910291 | 0.000778 | 0.451088 | 0.020446 | 0.011857 |
| c-50:50 @ 600 | 0.966303 | 0.001071 | 0.469952 | 0.033809 | 0.019136 |

**Expected support bodies** (E[in-range] = N·M exact; E[count-support], E[bl-support] exact sums):

| scenario @ N_b | E[in-range] | E[cnt-support] | E[bl-support] |
|---|---|---|---|
| (a) @ 150 | 22.5 | 19.56 | 2.09 |
| (a) @ 600 | 90.0 | 90.00 | 25.66 |
| (b) @ 150 | 18.8 | 11.14 | 1.13 |
| (b) @ 600 | 75.0 | 74.78 | 10.30 |
| (c) @ 150 | 7.5 | 0.82 | 0.06 |
| (c) @ 600 | 30.0 | 29.45 | 4.71 |

**Findings (the drafted artifacts are jointly unsatisfiable as written):**
1. §9's grid sizes {60, 120} do not bracket the budget-implied populations (113–150 feasibility, 450–600 confirmatory bodies): the bucket-local rule is passed with probability ≤ 0.0016 at N_b = 120 in every scenario, and the count-only bound overstates feasibility by one to two orders of magnitude at every size.
2. The bucket-local §5 rule (conditions 1–4) is the binding filter at every size and scenario: even scenario (a) at N_b = 600 reaches only F_bl = 0.057 (complete-rule probability: 0 as-drafted, §5A).
3. The conservative test-block reading is harsh at small N by construction (CONS ≤ 0.00001 at N_b = 150 in all historical scenarios); the liberal and training+test readings differ negligibly (the train block holds 3× the bodies).
4. §7's three support sites — global (§5), training block, test block — need one coordinated split-level-minimum resolution (O2); none is adopted here.
5. §10's verbal scenario assessments are replaced by the computed table in §10.
6. The gated power cell (scenario (a), N_b = 120, N_s = 40) cannot establish estimator performance: bucket-local support probability there is 0.0016 and the complete rule is impossible as-drafted (§5A). The power target is retained as a candidate; its evaluation — and any grid/gate reassessment — is deferred until the §5A resolution (O1/O3 may move the cell).

**Decision options (NO option adopted; reviewers recommend, owner decides):**

| option | change | P(feasible) side | cost / identification side |
|---|---|---|---|
| O1 grid re-anchor | attempt axis {150, 600} with validity/dedup modeled, or valid-unique-body axis at budget scale | computed above at 113/150/450/600 under both ρ mappings | Phase 1 compute scales with N_b × N_s × replications; validity/dedup modeling is new procedure |
| O2 split-level minimum | replace §7's reuse of B_min with declared B_split (or ≥1 body per included bucket + ≥ B_split total), coordinated over all three sites | not computed (new number) | relaxes CONS/LIB/TRN; identification consequences must be restated |
| O3 target scoping | coverage/FPR/power conditional on feasible replications, P(feasible) reported per cell with a floor; (c)/(d) gated on correct-infeasible-decision rates instead | P(feasible) per cell computed above | changes what Phase 1 gates; no new data needed |
| O4 within-range k-mix | historical-conditional vs 50:50 / equal-thirds | computed above (mix moves F_bl by ~2–3×) | no design change; acknowledges the historical mixes are weak estimates |
| O5 B_min re-fixing | 8 → smaller, with identification consequences restated | not computed (new number) | weakens the per-bucket minimum; rank/conditioning impact must be restated |

The five interact; resolution must be one coordinated set, recorded in §11. The O4 rows use the labeled alternative mixes; the historical within-range splits rest on 3 (v0.1) and 15 (v0.2) in-range bodies.

## 9.3 Sample-unit mapping (binding vocabulary for N_b, N_s, attempts, bodies, suites)

| row | attempt budget | expected valid submissions | expected unique canonical bodies | expected in-range bodies | expected bucket-local-support bodies (complete rule: 0 as-drafted) | hidden suites × inputs |
|---|---|---|---|---|---|---|
| Phase 1 simulation | — (no generation) | N_b simulated valid unique bodies by construction | N_b | N_b × M (scenario) | N_b-scaled E[bl-support] (§9.2) | N_s simulated suites × 20 labels |
| feasibility | 150 attempts | 150 × p_valid (p_valid not declared — O1) | 150 (ρ=0) / 112.75 (ρ=0.25) | × M | §9.2 E[bl-support] at 113–150 | owner slot; precedents: 3 pilot suites (`v02/run_pilot_v02.py:16`), 20 inputs/suite |
| confirmatory | 600 attempts | 600 × p_valid (not declared — O1) | 600 (ρ=0) / 450.25 (ρ=0.25) | × M | §9.2 E[bl-support] at 450–600 | owner slot; precedents: 40 confirmatory suites (`v02/run_confirmatory_v02.py:24`), 20 inputs/suite |

The simulation grid's N_b is simulated valid unique bodies; N_s is simulated suites with 20 soft-label inputs each. Attempts, valid bodies, unique bodies, in-range bodies, supported bodies, and suite identities are distinct units and are never interchanged. The hidden-suite count per real-study phase is an owner decision slot (cited precedents are not adoptions); validity-rate and duplicate-rate modeling at the attempt axis is O1. Suite facts (supporting the crossed design): hidden suite M = 20 inputs (15 random + 5 templates), identity = instance seed (`specs/instrument_spec.json:23-27`, `study/instances.py:23-46`); k/C are body-level (probes ignore instance_seed; 0/120 v0.2 bodies change k across suites).

## 10. Historical support rates as stress-test scenarios (not forecasts)

**Non-equivalence clause (binding).** v0.1's directed-prompt generation and v0.3's single-prompt generation are different sampling procedures; **neither predicts the other**. The historical shapes are recorded as a warning pattern, not a forecast. The two historical populations must **not** be pooled into an estimate of v0.3's generator population.

**Scenarios (separate; never pooled).** (a) in-range mass 15.0% — historical v0.1 (3/20); (b) in-range mass 12.5% — historical v0.2 (15/120); (c) lower support, 5% — below both historical figures; (d) no usable support, 0% — zero bodies in 2 ≤ k ≤ 24.

**Budget arithmetic at the candidate budgets (stated plainly, before any spend).** Attempts → E[unique canonical bodies] = 1 + (A−1)(1−ρ), fresh-draw uniqueness assumed, validity not modeled (O1): 600 attempts → 600 (ρ=0) / 450.25 (ρ=0.25); 150 attempts → 150 / 112.75. Full-population probabilities from §9.2 (count-only bound | bucket-local pass probability; complete-rule probability 0 as-drafted):

| Scenario | E[in-range] at 600 att. (ρ=0 / 0.25) | count-only F | bucket-local F | Plain statement |
|---|---|---|---|---|
| (a) 15.0% | 90.0 / 67.5 | 1.000 | 0.057 | Passes the count rule almost surely but the bucket-local rule with probability ≈ 0.06; E[bl-support] ≈ 26 bodies (complete rule: 0 as-drafted, §5A) |
| (b) 12.5% | 75.0 / 56.2 | 1.000 | 0.037 | Same pattern; E[bl-support] ≈ 10 bodies |
| (c) 5% | 30.0 / 22.5 | 0.910 | 0.020 | Prior "likely inadequate" verdict corrected and reinstated on the right ground: the count-only bound (0.910) looks adequate, but under the bucket-local rule the probability is 0.020 with E[bl-support] ≈ 5 bodies — likely inadequate (complete-rule probability 0 as-drafted, §5A) |
| (d) 0% | 0 / 0 | 0* | 0* | v0.3 cannot estimate; terminates at the gate |

At 150 feasibility attempts: (a) count-only 0.470 / bucket-local 0.004 with E[bl-support] ≈ 2 bodies; (b) 0.061 / 0.0002; (c) 0.0008 / 0.000003. The §6 gate additionally requires the outcome tails; §9.1 records that the upper tail is not supported at feasibility size under the proposed parameters.

If the owner judges any scenario's implied spend unrealistic, the budget is an owner decision at freeze (§11) — stated now, not after money is spent.

## 11. Freeze-blocker register and authorization boundaries

**STAGE 1 — SIMULATION-PROTOCOL FREEZE (before any Phase 1 run).** Freezes the simulation DGP, analysis procedure, thresholds, seeds, dependencies, and acceptance criteria. Pre-freeze items (all must close before the simulation-protocol freeze):

1. §5 support-rule numbers: B_min, per-extreme minimum (4), κ_max — reviewer sign-off.
2. §6 gate numbers: θ_lo, θ_hi, M, D, S, v_min — reviewer sign-off.
3. §7 split fractions (75/25), R = 50, B = 2000, split-level minimum per §9.2/O2 resolution (covering all three sites: global, training, test), incomplete-cell handling text — reviewer sign-off after analysis-code spec.
4. §9 grid + targets as revised per §9.2 (incl. the §9 claim mapping), 2000 replications, Clopper–Pearson decision rule — reviewer sign-off (document side only; evidence is post-freeze).
5. §9.1 DGP specification (k-draws incl. O4 choice, Dirichlet/θ/σ values, duplicate mechanism, γ-calibration, population-oracle vs finite-sample statement) — reviewer sign-off + owner acceptance.
6. §4 validity-check specification (signature, AST allowlist content, no-IO pattern list) and the versioned checker artifact with recorded SHA-256 — reviewer sign-off.
7. §9.2 option resolution (O1–O5) — reviewers recommend, owner decides.
8. G6a/G6b inference-target choice — reviewers recommend, owner decides.
9. §10 scenarios and recomputed budget arithmetic (per §9.2) — owner acceptance.
10. Normalization rule (§3 E, without trailing-whitespace stripping; cross-phase duplicate rule) — reviewer sign-off that the byte-level rule is adequate for the unique-body estimand.
11. Master seed 20261015 and the §7.4 standard-library seed-derivation scheme + pinned CPython version — reviewer sign-off.
12. Hidden-suite counts per real-study phase — owner decision (precedents cited, not adopted).
13. §5A matrix-contradiction resolution (M1/M2/M3 — reviewers recommend; M1/M3 require explicit owner approval as model changes, M2 requires reviewer sign-off on the exact mathematics plus owner acceptance as a gate-semantics change) — owner decision with reviewer recommendation.
14. Complete-rule probability recalculation against the adopted §5A resolution — reviewer verification (computable only after item 13).

**STAGE 2 — STUDY FREEZE (after Phase 1 evidence passes; before feasibility).** Locks validated numbers, generation spec (model id, sampling params, prompt per §4), budgets N = 600/150 (owner spend approval), suite-count numbers if not fixed earlier, final normalization sign-off.

**Not freeze blockers (sequenced in §12; closable only by evidence):** Phase 1's pass against the §9 targets as revised (incl. interval-procedure selection), and the §6 feasibility-gate pass. Neither closes by document revision; both must pass before confirmatory generation. No pre-freeze item above requires post-freeze output.

Already closed by owner decision (2026-10-14) and not reopenable by document iteration: C (r = 1.5 affirmation, §3) and E (Option 1, §3); D-style timing/disposition is fixed in §8.

## 12. Phase authorization boundaries

- **This document:** drafting authorized by the owner's 2026-10-14 plan approval; commit requires review sign-off + explicit owner approval.
- **Simulation-protocol freeze:** closes all §11 Stage-1 items; freezes the simulation DGP, analysis procedure, thresholds, seeds, dependencies, and acceptance criteria.
- **Phase 1 (software simulation):** requires a **separate explicit owner authorization** after the simulation-protocol freeze. Passing Phase 1 does **not** authorize anything else automatically.
- **Study freeze:** only after Phase 1 evidence passes and the required review and decisions (§11 Stage 2) are complete may the full study protocol be frozen.
- **Feasibility generation and gate:** separate authorization after the study freeze.
- **Confirmatory generation and estimation:** separate authorization after the feasibility gate passes.
- **Hidden-outcome collection** beyond what each authorized phase requires: never implicit.

## Appendix A — verified counts carried forward

```text
v0.1 (pilot/pilot_report.json, 20 LLM-directed bodies):
  k_hist: {0: 16, 5: 2, 10: 1, 25: 1}   potentially_identifiable_range(2..24): 3/20 (15.0%)
  distinct C per k: 0->0.0  5->1.0  10->0.5  25->0.2   observed_identifying_support: none
  old_gate_eligible (k>=2): 4 bodies, all Y=0; INFEASIBLE under the old gate

v0.2 (v02/pilot_v02/pilot_v02_report.json, 120 code-constructed bodies):
  k_hist per body: {0: 90, 5: 9, 10: 3, 20: 3, 25: 15}
  potentially_identifiable_range(2..24): 15/120 (12.5%)   k=0: 90/120 (75.0%)
  within-k C variation in the realized pack: none (C=5/k forced only for k>=25;
    at k=24: min C 4/24, max C 5/24). observed_identifying_support: none.

v0.3-P: untested; single identical prompt; not an identified evaluation
```

## Appendix B — relation to prior records

- `v03p/PHASE0_DESIGN_2026-10-14.md` (`3cd62b8`): superseded by this draft, preserved unamended.
- `v03p/PHASE0_REVIEW_RESPONSE_2026-10-14.md` (`4018ebd`, erratum `edae42c`): terminal review response; its OPEN items A/B close only with §5–§9 evidence, C/E closed by the owner decisions recorded in §3.
- `v03p/PHASE0_DESIGN_2026-10-15.md` (Revision B draft): reviewed by GPT 2026-10-15 with verdict NOT APPROVED (four findings: §5 matrix contradiction; bucket-local labeling; Phase-1/support incompatibility; calibration/estimand mismatch). Preserved as-reviewed, uncommitted; superseded by Revision C.
- v0.1/v0.2 records, audit series (`da4030d`, `c75fb43`, `11d86b9`), rlc0 series: untouched.

## Appendix C — design-arithmetic provenance (deterministic; no simulation)

| artifact | bytes | SHA-256 |
|---|---|---|
| `feas_prob.py` (corrected full-population arithmetic) | 11930 | 262E0DBFE6C08A97084C3AF82BBC1D7B16C9ED97EC7DE57BB1DC80FFE |
| `feas_prob_test.py` (corrected exact fixed-size block readings) | 16326 | 6DFC54C86C4E923C4EC8EB5875FFBC95815EF0AE92BDDBCC8F40086E3DBC0668 |
| `dgp_counts_v2.py` (§9.1 conditioned-DM enumeration) | 4603 | 8D07376BA46A956E6B140144A95E1BFD0C1C3EE8004CF27F01C6B0E2F076C216 |
| `dgp_outcome_tails.py` (§9.1 deterministic tail-scale assessment) | 5940 | F530EC74F6EF5550692A8FF0AE6EB44B7C70ADC58BF334AE0736243F2890CF0E |
| `g_check.py` (g_k brute-force cross-check) | 1695 | 12A650D0AB7CD489DBABAB50E284BF0C44CEF8EFA7E7D5E55758AD7236532510 |
| `feas_prob.out.txt` (deterministic output) | 12330 | 3CD0ABD28EB7962756DDD3E540DA3F1F8817BA0CC6E187D343F4D28C60EDA4BB |
| `feas_prob_test.out.txt` (deterministic output) | 32442 | DB5E250C02A86BBD3D02EC93E1FD488766F87A646E4F66663E4B99780BEA27F8 |
| `dgp_outcome_tails.out.txt` (deterministic output) | 7688 | 8DC11E64B77541051423AACAE2C25304521EA970C32A774081B04E56CEB82DD9 |

All scripts use only the Python standard library. Methods: exact multinomial/hypergeometric enumeration in log space (summation-term cutoff 1e-20, omitted mass bounded by 1e-13); Simpson quadrature over latents (`dgp_outcome_tails.py`, 81- vs 161-node grids agree to 6e-12); exact composition enumeration (`dgp_counts_v2.py`; `g_check.py` brute-force cross-check of the pair-sum g_k formula 12/12 to 1e-9); regression of the corrected count-only figures against the verified (a)/(c) values (11/11 to 5e-7) with the corrected (b) values verified as supersets of the superseded branch. Structural zeros (0*) vs log-space underflow (0-dag) are distinguished in every output. The conservative reading with §5 conditions 3–4 re-applied at test level is statedly not computed; validity rate and duplicate-attempt mechanics are not modeled (N denotes unique valid bodies). Script fate (commit under v03p/ vs inline numbers) is an open reviewer/owner decision (Appendix D).

**Revision C additions (additive only; every Revision B script above is byte-unchanged, hashes stand):**

| artifact | bytes | SHA-256 |
|---|---|---|
| `feas_check.py` (fast exact reference tests: hypergeometric closed forms vs explicit sums; end-to-end brute force vs readings() at N=32; RCS rank minors; tail convergence; bucket-local wiring) | 9702 | F5DAFD13EDBC4E0F4E4E024A4D9AF906BB79797F7A6304A6CF68F6D775B8BEE5 |
| `outcome_tails_c.py` (gate-tail expectations on bucket-local support; S20/S40 sensitivity labels) | 2597 | 4CC5D4E82B8E9F7620AD87238ED2A86D010542F6992C70A410344F7F61B1CADF |
| `feas_check.out.txt` (deterministic output: 26/26 PASS) | 3376 | 32BCC2B2DB0B8299D411393719A20F354FC33150AB6598E5082869D79A218F20 |
| `outcome_tails_c.out.txt` (deterministic output) | 6104 | 9805ED4CEF98F221D696DCABD3830D15B2CB9510351FC932BA82C18D46F00F0C |

**GPT verification record (2026-10-15 review).** GPT extracted the three Revision B scripts: source byte counts and SHA-256 match Appendix C; `feas_prob.py` reproduces the count-only and bucket-local figures; `dgp_outcome_tails.py` reproduces the upper-tail fractions (≈ 2.59%, 2.28%, 2.45% for the historical mixes); `feas_prob_test.py` exceeded GPT's 200-second review timeout (its block-level tables were unverified by GPT, not disproven).

**Local runtime report (CPython 3.14.0, Win32).** `feas_prob.py` 5715 ms; `feas_prob_test.py` 34013 ms; `dgp_outcome_tails.py` 7687 ms. Deterministic re-runs reproduce the recorded outputs exactly (normalized-content MATCH on all three). The full block script runs in ~34 s in this environment; review-environment timing varies — `feas_check.py` covers the same algebra (closed forms, end-to-end brute force at N=32, wiring) in seconds.

## Appendix D — decision register (resolved / outstanding evidence / owner decisions)

**Resolved in Revision B (each repair cites its finding):** header chronology with unset freeze date; §4 interface/validity rewrite (GPT finding 1); two-boundary §11–§12 (GPT finding 2); §5 rank-increase test replacing the cross-k requirement (GPT finding 3); §5 exact design matrices, support-only fitting, training-block rule; §7.4 standard-library RNG; §9.1 feasibility-constrained DGP with uniformity 1/Z(k) and deterministic C summaries; scenario-(b) three-bucket event correction with regression; exact fixed-size hypergeometric split replacing binomial thinning; §10 scenario-(c) correction on recomputed grounds; normalization without whitespace stripping (GPT finding 7) with cross-phase duplicate rule; 2δ* claim mapping recorded as limitation; γ* population-oracle vs finite-sample distinction; explicit baseline-misspecification non-assessment; §9.2 O1–O5 table with none chosen; §9.3 sample-unit mapping.

**Resolved in Revision C:** §5A contradiction stated with the verified rank table and the M1/M2/M3 candidates (exact definitions, consequences, approval routing — no selection; κ≤30 retained-but-flagged); bucket-local relabeling throughout with the complete-rule probability stated as 0 as-drafted and the recalculation recipe deferred; Phase-1 incompatibility documented (grid/gate/power-cell evaluation deferred until the §5A resolution); gate-tail expectations recomputed on bucket-local support with N_s sensitivity labels; planted-oracle calibration meaning fixed with the G6-conditional mapping and the FPR/power non-claim; verification package (GPT record, runtime report, reference tests) delivered.

**Outstanding evidence (closable only post-freeze, never by document revision):** Phase 1 coverage/FPR/power evidence and interval-procedure selection; the §6 feasibility-gate pass; checker artifact SHA-256 (recorded at simulation-protocol freeze); pinned CPython version (recorded at freeze); γ* calibration values (Phase-1 simulation-internal); §5A resolution adoption (§11.13); complete-rule recalculation against the adopted resolution (§11.14); γ* recalibration to the selected G6 target.

**Foued's owner decisions (none chosen here):** §5A M1/M2/M3 choice (M1/M3 explicit approval as model changes; M2 acceptance as gate-semantics change); O1–O5 coordinated resolution; G6a vs G6b; hidden-suite counts per real-study phase; generation-budget spend approval; §10 acceptance; §9.1 DGP parameter acceptance (θ/σ, with the recorded upper-tail shortfall); policy for permitted pre-freeze computation (plus GPT deviation classification — see the process-deviation record); script fate (commit vs inline).

**Settled (not reopened):** C (ACCEPT, r = 1.5); E (Option 1, unique normalized valid bodies).
