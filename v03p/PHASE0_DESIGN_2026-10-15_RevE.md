# v0.3-P Phase 0 Design — Revision E

**Dates:** drafted 2026-10-14 (working session); circulated 2026-10-15 as Revision B; revised 2026-10-15 as Revision C after GPT's NOT-APPROVED review (four findings); re-revised 2026-10-15 as Revision D after the joint GPT/CLAUDE review (GPT A/B/C, CLAUDE N1–N8); re-revised 2026-10-15 as Revision E (five textual fixes per PR #2 review; no reruns, no owner decisions). Uncommitted — no git commit timestamp exists for this file; the effective freeze date is unset until a freeze actually occurs. The Revision C draft is preserved as-reviewed.
**Status:** DRAFT for independent review (GPT, CLAUDE, GLM). Uncommitted; not frozen. This is a **new uncommitted document** superseding the Revision D draft (published for independent review on `review/revd-package` at `eb46a2c`, preserved byte-identical and unmerged; this file is a separate successor draft), which superseded the Revision C draft (`v03p/PHASE0_DESIGN_2026-10-15_RevC.md`, uncommitted, preserved as-reviewed after the joint GPT/CLAUDE NOT-APPROVED review), which superseded the Revision B draft (`v03p/PHASE0_DESIGN_2026-10-15.md`, preserved as-reviewed), which itself superseded `v03p/PHASE0_DESIGN_2026-10-14.md` (commit `3cd62b8`, preserved unamended). It incorporates the committed review findings of `v03p/PHASE0_REVIEW_RESPONSE_2026-10-14.md` (commits `4018ebd`, `edae42c`) and the two owner decisions recorded 2026-10-14. Commit requires independent review sign-off plus explicit owner approval. **Design freeze occurs in two boundaries defined in §11–§12: the simulation-protocol freeze (before Phase 1) and the study freeze (after Phase 1 passes).** This document does not authorize Phase 1 simulation, solver generation, or hidden-outcome collection; each requires a separate owner authorization (§12). It is not an adequately identified evaluation and is not described as one. Revision C addresses GPT's four findings without freezing, authorizing, or deciding anything reserved to reviewers or the owner. Revision D addresses the joint GPT/CLAUDE review (GPT A/B/C, CLAUDE N1–N8) on the same terms: no freeze, no authorization, no owner decisions taken. Revision D is committed for independent review on `review/revd-package` at `eb46a2c`, not merged to `master`, not frozen, and not phase-authorized; this Revision E file is a separate uncommitted successor draft applying the five textual fixes from the PR #2 independent review.

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

### 0.3 Change ledger (Revision D; cites the joint GPT/CLAUDE review)

| Change | Source |
|---|---|
| §5B training-block specification: per-split checks on the realized matrix with INFEASIBLE disposition and failure counting; N1 readings distinguished (computed tables assume global-membership; selection tied to O2); N2 eligibility per M-option with policy options open; same-cases requirement | GPT-A; CLAUDE N1/N2; work order 1 |
| §1 estimand conditioned on the globally-supported population; test-eligibility per split; G6 layering; owner-acceptance flag for the narrowed claim | CLAUDE N4 |
| Per-M matrix + standardization definitions (§5A extended; fit-vs-diagnostic split in D5) with the ridge-on-dummies sub-decision left open | CLAUDE N3 |
| Suite-count derived constraints (feasibility ≥6; conditional test-block minima 24/48; precedents incompatible); shared-vs-disjoint left open | CLAUDE N5 |
| Directional FPR/power (gain = lower bound above 0; harm reported separately); per-replication coverage target specified for post-selection use | CLAUDE N6 |
| §9.1 per-bucket tail table (exact E[B_k], q_k, bodies, suites); 26.5 headline superseded (corrected value below it); joint-P omission; γ≠0 requirement | GPT-B; CLAUDE N8; work order 2 |
| Calibration: conditional two-path procedure (recalibrate-to-target vs oracle-stress-test restatement); calibration-freeze item; no validation claims | GPT-C; work order 3 |
| Provenance: N7 correction by mechanical full-hash regeneration; portable v03p/scripts/ + RUN.txt; new hashes for path-fixed scripts; historical lineage kept | CLAUDE N7; work order 4 |
| §11 +4 freeze items; Appendix B/C/D updates; feasibility-warning scope caveat | work order 5 |

### 0.4 Change ledger (Revision D integration of GPT-PR #1; branch unmerged, nothing committed)

| Change | Source |
|---|---|
| §9.1/§9.2 proxy labeling with I_k/G formalism; complete-rule quantities marked not calculated | GPT-PR D1 |
| D2 replacement paragraph; three-concept separation; no determinism claims from expectations | GPT-PR D2 |
| Phase-1 evaluability policy (output split, floor open, not-evaluable disposition, P(feasible), rejection disclosure); (a)@120 arithmetic | GPT-PR D3 |
| G6a-fix/G6a-id/G6b explicit targets with matched procedures; coverage-truth mapping | GPT-PR D4 |
| Per-M fit-vs-diagnostic six-point specification; M2 raw-fit preservation; M3 ridge sub-decision open | GPT-PR D5 |
| Baseline claim narrowed to latent fixed-effect component (adopted suggested text) | GPT-PR D6 |

### 0.5 Change ledger (Revision E; five textual fixes from PR #2 review, no reruns)

| Change | Source |
|---|---|
| Coverage rule conditional on interval-evaluable cells; NOT EVALUABLE disposition; O3 still open | PR #2 finding 1 |
| §9.2 header renamed to conditions 1–4; rank/conditioning exclusion stated | PR #2 finding 2 |
| M2 stale interval sentence replaced; predictive-loss target retained | PR #2 finding 3 |
| M2 standardization stated as diagnostic-only; raw-RCS fitting | PR #2 finding 4 |
| Publication metadata distinguishes review-committed package from frozen/authorized protocol | PR #2 finding 5 |

## 1. Research question and estimand

**Question.** Does the failure-concentration statistic C carry predictive information about held-out per-input failure probability beyond the failure count k, in a newly generated population of solver bodies?

**Estimand (conditioned on the analysis support; owner acceptance required — narrows the prior joint-population wording).** Δ = E[ L(baseline) − L(extended) ] over the **globally-supported population** (bodies in globally-included buckets × hidden suites), equal weight per eligible test cell; under G6a-fix additionally conditional on the realized training data (G6a-id conditions on training identities only; §7). Bodies outside globally-included buckets enter neither fitting nor scoring. The conclusion applies to supported-bucket bodies, not to the generator's output in general: outcome-blind selection still changes the analysis population's composition. Which globally-supported bodies are scored in each split (test eligibility) is defined in §5B/§7; the G6a/G6b choice (§7, Foued) selects the conditional vs unconditional form. The baseline model uses k only; the extended model uses (k, C). This is **not** a contrast between adjacent-k groups.

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

**§5B. Training-block checks and test eligibility (per-split; no fallback).** Rank and conditioning are evaluated on the realized TRAINING design matrix after each split — never on the global matrix, and test-block eligibility is a separate rule from training identifiability.
- **Per-split training checks.** On the realized training matrix: (i) the training-block count rule above; (ii) rank-increase ≥ 1; (iii) the adopted conditioning criterion (post-§5A-resolution; until then the rank/increase checks apply and the conditioning conjunct is pending as globally). Additionally the realized training block must retain ≥ 2 distinct C values in at least one included bucket (reuses condition 3's number; applied per-split) — otherwise C is unidentified in training under every M-option.
- **Disposition.** Any failed training-matrix check makes that split INFEASIBLE: no fitting on a deficient block, no silent fallback, no refit. Phase 1 counts infeasible splits by cause (support/rank/conditioning × train/test blocks) and reports the counts; they enter the procedure's operating characteristics.
- **N1 — two readings of "included" inside a block.** (R-a) global-membership: a bucket counts as included iff globally included, with the block counting its members; (R-b) re-application: the block's counts are re-checked against B_min = 8 (a bucket with 8–10 global bodies holds only ~6–7 training bodies, so R-b fails it). The computed TRN_bl tables assume R-a (stated provenance). Selection between R-a and R-b is tied to the O2 coordinated resolution (owner) — no selection here.
- **N2 — test eligibility (bucket present in training).** A test cell is eligible iff (i) its body is in a globally-included bucket AND (ii) its bucket is training-represented under the adopted model: under M3 (bucket dummies) a bucket with zero training bodies has an unestimable dummy, so scoring such a cell is undefined; under M1/M2 (global bases) scoring at an untrained k is extrapolation. Policy options, left open (owner, tied to M-selection and O2): (P-i) split INFEASIBLE if any (i)-eligible test body is untrained, or (P-ii) a narrower evaluation population scoring only training-represented buckets (the estimand conditions further). The same evaluation cases are required across M1/M2/M3 whenever models are compared — scores over different test sets must not be compared as though they measured the same quantity. No silent extrapolation under one model alongside undefined scoring under another.

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
- **M1 — lower-dimensional fixed baseline, e.g. [1, x] with x = log(1+k).** Exact columns: intercept, x; extended adds C (three columns). Rank: full (3) whenever conditions 3–4 pass (C varying within one k-slice is independent of {1, x}). Conventional κ finite and meaningful; κ_max = 30 preserved with no new threshold; the rank-increase test becomes implied-by-bucket-rule. Consequences: model-family change (abandons the RCS flexibility; at two k values [1, x] is saturated so the fixed-effect component is trivially covered, at three it is restrictive); the κ ≤ 30 filter still binds probabilistically, so complete-rule probabilities must be recomputed post-decision (recipe: bucket-local sum ∧ κ(Z_pass) ≤ 30 over C-composition patterns). Requires explicit Foued approval (model change); reviewer re-verification of §9.1/Phase-1 artifacts under the new forms.
- **M2 — redefined conditioning diagnostic on the estimable subspace (κ_eff); models unchanged.** Exact definition: κ_eff = σ_1/σ_r on the column-standardized extended matrix (standardization as in the rank check), where r counts singular values above the rank tolerance τ; τ is a numerical parameter recorded at the simulation-protocol freeze, not a gate threshold; κ_max = 30 preserved (no replacement threshold). Relationship to the existing fit: the existing reference fit (`study/models.py:61-80`) is ridge-penalized IRLS logistic regression with λ = RIDGE = 1e-6 on all columns including the intercept, solved with a 1e-12-floored Gauss-Jordan — its operator (X'WX + λI) uses outcome-dependent weights and therefore cannot enter the outcome-blind §5 gate; κ_eff gates the unweighted proxy only, and unidentified directions remain silently ridge-regularized. κ_eff is a conditioning diagnostic on the nonzero-singular-value subspace; it does not redefine the predictive-loss estimand as a coefficient-contrast estimand. The selected G6 target and its uncertainty procedure must remain aligned. A regularized-matrix variant κ(Z'Z + λI) with the frozen λ = 1e-6 is NOT viable: κ ≈ λ_max/1e-6 ≫ 30 for any support size (λ_max ≥ trace/6), so it would need its own (λ, κ) pair — new numbers requiring owner approval. Consequences: no model change; gate controls estimable directions only; complete-rule probabilities recomputed post-decision (same recipe with κ_eff). Requires reviewer sign-off on the exact mathematics plus Foued's acceptance (gate-semantics change).
- **M3 — bucket fixed effects + C (the pre-Revision-B family).** Exact columns: q bucket dummies (q = 2 or 3; nonempty buckets guaranteed by condition 2) plus C. Rank: full (q+1) iff C varies within some bucket — implied by conditions 3–4; conventional κ finite and meaningful; κ_max = 30 preserved. Consequences: model-family change contradicting the `study/models.py` RCS implementation (implementation must be rewritten and re-verified; all §9.1/Phase-1 artifacts re-derived under the new forms); changes the meaning of "C beyond k" (beyond bucket means rather than beyond a smooth k function); complete-rule probabilities recomputed post-decision. Requires explicit Foued approval (model change); full reviewer re-verification.

**Matrix and standardization definitions per candidate (N3; each option needs its own before κ comparisons are meaningful).**
- **M1:** raw X = [1, x, C] with x = log(1+k); fitting uses the raw matrix. Diagnostics use the standardized form (intercept as-is; x and C centered to zero mean and scaled to unit SD on the training rows; test rows transformed with the training moments; authoritative fit-vs-diagnostic split in D5 below). Regularization follows the reference behavior (all columns including the intercept penalized at λ = RIDGE).
- **M2:** X = the current RCS forms ([1, rcs_basis(log(1+k))] baseline, plus C extended). The standardized extended matrix is used for rank/conditioning diagnostics only; fitting remains on the raw committed RCS matrix as specified in D5, unless a fit change is explicitly approved.
- **M3:** raw X_M3 = [D_1, …, D_q, C] with D_1…D_q the bucket indicators; fitting uses the raw matrix. Diagnostics use [D_1…D_q uncentered, z_C] with z_C the standardized C (training mean/SD; test transformed with training moments; authoritative fit-vs-diagnostic split in D5 below). No separate intercept (the dummies span constants); dummies are NOT centered (centering creates collinearity). Ridge treatment of the dummies is an OPEN sub-decision (penalize bucket means toward zero per the reference all-columns behavior, or leave the intercept-equivalent terms unpenalized) — owner/reviewer call; until fixed, κ comparisons involving M3 are not meaningful. With only 2–3 buckets M3 is nearly saturated, and conditions 3–4 carry the entire identification burden.

**Fitting vs diagnostic matrices per option (D5).** For every M-option the three matrices are identified separately (standardization is diagnostic-only throughout: with a fixed ridge penalty, rescaling predictors changes the estimator, and no fit-standardization change is proposed):
1. raw design matrix;
2. diagnostic-only matrix (rank/conditioning);
3. fitting/prediction matrix;
4. centering/scaling moments and their estimation population;
5. ridge-penalized columns and penalty value;
6. rank/condition formula and tolerance.
- **M1:** (1) [1, x, C], x = log(1+k); (2) column-standardized [1, x, C] (intercept as-is; training moments); (3) raw [1, x, C]; (4) training rows only, applied to test rows; (5) all columns including the intercept at λ = RIDGE = 1e-6 (reference behavior); (6) rank-increase + conventional κ ≤ 30 on the diagnostic matrix.
- **M2:** (1) current RCS forms [1, rcs_basis(log(1+k))] + C; (2) column-standardized forms (standardization as in the rank check); (3) the RAW matrix exactly as committed in `study/models.py` (no training-mean/SD transformation anywhere in the displayed source: `design_row` returns raw values and `logistic_fit` consumes them directly) — the standardized matrix is diagnostic-only unless a fit change is explicitly adopted and approved; (4) training rows only; (5) all columns including the intercept at λ = RIDGE = 1e-6 each IRLS iteration, 1e-12 pivot floor (`study/models.py:61-80`); (6) rank-increase + κ_eff ≤ 30 on the diagnostic matrix. A condition gate on the unweighted standardized proxy must not be conflated with the outcome-weighted penalized fitting operator; κ_eff does not turn the predictive-loss estimand into a coefficient-contrast estimand.
- **M3:** (1) [D_1…D_q, C] raw; (2) [D_1…D_q uncentered, z_C] with training moments; (3) raw [D_1…D_q, C] (reference pattern; no fit-standardization change proposed); (4) training rows only; (5) ridge columns OPEN sub-decision (reference all-columns behavior would shrink bucket means toward zero; alternative leaves intercept-equivalent terms unpenalized) — owner/reviewer call; (6) rank-increase + conventional κ ≤ 30 on the diagnostic matrix.

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

**Suite-count constraint.** Each tail needs ≥ 6 distinct suites; §9.3 gives the derived minima (the 3-suite precedent does not satisfy this requirement).

Variance of s/20 over the gate population is recorded with threshold v_min = 0.01 as a **secondary diagnostic only**; variance alone can be driven by outliers and is not the binding criterion. A pooled correct/incorrect rate over hidden inputs is **not** an acceptable gate statistic (it can pass while every pair has the same success fraction).

**Timing.** θ_lo, θ_hi, M, D, S, v_min, and the §5 numbers are fixed **before** any feasibility-sample hidden outcomes are collected (§8). Whether the proposed outcome-DGP parameters yield both gate tails at feasibility size is assessed deterministically in §9.1; the gate numbers here are candidates independent of that assessment.

**Precedent, not inheritance.** v0.2's pilot gate2 (≥ 10% correct and ≥ 10% incorrect among pairs' hidden inputs; `v02/run_pilot_v02.py:18-19,72-76`) pools inputs and ignores pair-level variation; it is not adopted.

**Disposition.** Gate failure **terminates v0.3** (§8).

## 7. Crossed evaluation procedure (confirmatory)

**Formation (both axes unseen).** Two-way holdout over canonical body identities and hidden-suite identities, from the master seed (§7.4). Per repetition: a held-out subset of body identities (25%) and of suite identities (25%); the remaining 75% on each axis is training. The **training block** = training bodies × training suites; the **test block** = held-out bodies × held-out suites; the **mixed (off-diagonal) blocks** are used for neither training nor scoring, so no test body or suite is seen in training in any form. The split-level minimum (O2) covers three sites — global (§5), training block, test block — as one coordinated resolution (§9.2); no site-specific minimum is adopted here.

**Primary split and robustness repetitions.** The **primary analysis uses one preregistered split** (drawn from the master seed, fixed before outcomes). Robustness: R = 50 additional seeded splits are scored and the distribution of per-split Δ̂ is **reported as a sensitivity diagnostic only**; it does not enter the point estimate or interval. This removes any aggregation ambiguity over overlapping test appearances.

**Scoring and aggregation.** Per eligible held-out (body, suite) cell in the test block: compute the per-hidden-input log-loss difference (extended − baseline, sign-flipped so Δ̂ is baseline − extended). Eligibility: the held-out body is in the confirmatory analysis support (§5 rule, computed outcome-blind on the full confirmatory population). Δ̂ = equal-weight mean over eligible test-block cells. Every held-out body is scored on every held-out suite, so equal weight per cell coincides with equal weight per body among eligible cells. Suite-level exclusions or incomplete cells must not be silently reweighted; discard/recompute rules are fixed in the analysis code before outcomes are collected and recorded here at freeze.

**Uncertainty.** *Primary:* two-way cluster bootstrap — resample eligible test-body identities with replacement and eligible test-suite identities with replacement, independently; score the intersection cells; B = 2000 resamples; percentile interval at nominal 95%. *Fallback:* crossed random-effects (variance-components) interval with body and suite as crossed factors. The procedure carried forward is the one that passes the Phase 1 coverage gate (§9); if neither passes, Phase 1 stops with an interval-procedure failure and the predictive question is not tested with intervals under v0.3. The v0.2 overlapping-fold bootstrap remains barred without a coverage test.

**Inference target (open owner decision; none adopted).**
- **G6a-fix (conditional on realized training data).** Let D_train denote the realized training data, including outcomes, with fitted predictors f_0(D_train), f_1(D_train). The target is the expected held-out loss difference over new eligible test body/suite cells conditional on this realized training data. Coverage truth and the test-resampling procedure target this same quantity; the current test-only bootstrap holds fits fixed and is aligned with this target. Cost: one fit per model plus the 50 diagnostic refits (the R = 50 re-splits remain a reported sensitivity diagnostic over training draws, not pooled).
- **G6a-id (conditional on training identities only).** The target conditions only on the training identities and averages over possible training outcomes and refits. This needs a simulation/uncertainty procedure that accounts for training-outcome variability; the fixed-fit test bootstrap does not automatically cover it.
- **G6b (full pipeline).** The unconditional full-procedure target: each of the B = 2000 replicates re-draws the 75/25 split and refits both models; the R = 50 diagnostic is subsumed. Cost: 2000 × 2 fits per cell per replication — orders of magnitude above the fixed-fit options.
- The current one-primary-split plus 50 sensitivity splits is not equivalent to full-pipeline inference. Reviewers recommend; Foued chooses.

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

**Replications and Monte Carlo uncertainty.** 2000 replications per cell (binomial SE on coverage ≈ 0.006 at p = 0.925). Coverage decision rule: For each cell designated before simulation for interval-performance assessment that reaches the prespecified feasible-replication floor, the one-sided 95% Clopper–Pearson lower bound of estimated coverage must be ≥ 92.5% (candidate number; freeze-blocker). This criterion applies only to interval-evaluable cells. A cell below the floor is NOT EVALUABLE and does not pass by default. O3 must specify before freeze how such cells affect the overall Phase 1 decision; a required interval-performance cell may not silently be converted to a gate-characterization-only cell after results are seen.

**Targets (fixed now; evidence produced by Phase 1).**

- *Coverage:* passes as above, in every interval-evaluable cell — i.e., every cell designated before simulation for interval-performance assessment that reaches the prespecified feasible-replication floor. Known caveat (recorded): the two-way bootstrap undercovers with few bodies and few suites; those cells exist precisely to expose this. Coverage is against the per-replication conditional target computed from DGP truth: under G6a-fix, the realized-training-data conditional target; under G6a-id, Δ(train-identities) averaging over training outcomes; under G6b the corresponding unconditional target (computable by quadrature or large Monte Carlo; exact method frozen before Phase 1). Target computation is specified fully after the G6 choice and the §5A resolution.
- *FPR (directional, for gain):* at planted Δ_oracle = 0, the interval lies entirely above 0 (lower bound above 0) in ≤ 5% of replications (per cell). An interval entirely below 0 is evidence of harm, reported separately — it is not counted as a false positive for the claim of gain; any other outcome is inconclusive.
- *Power (directional, for gain):* at planted Δ_oracle = 2δ*, the interval lies entirely above 0 in ≥ 80% of replications under scenario (a) at N_b = 120, N_s = 40; power under thinner scenarios is reported, not gated.
- *Gate characteristics:* false-pass and false-fail rates of §6 under each scenario are reported; the gate's thresholds are not adjusted in response. Phase 1 reports per-split infeasibility counts by cause (support/rank/conditioning × train/test blocks) and estimates the joint §6 gate-pass probability P(≥ M pairs ∧ ≥ D bodies ∧ ≥ S suites per tail), which is not pre-freeze calculable.

**Claim mapping (binding).** FPR = 5% at Δ = 0 controls false claims of ANY predictive gain. The 80% power gate applies at 2δ*: the design reliably detects gains of at least twice the owner's minimum meaningful effect. Power AT δ* is reported, not gated — δ* is the owner's decision threshold (decision C) and the design claims no reliable detection exactly at it. Detection of any positive gain is not a gated claim. The 80% target at 2δ* tests power to have the interval exclude zero under the larger effect; it is not an 80% power guarantee at δ*. Recorded explicitly as a limitation.

**Effect calibration (binding interpretation; GPT-R4).** "True effect" in the grid means the planted population-oracle contrast: the §1 estimand evaluated on DGP truth at the planted γ* (γ* from bisection, tolerance 1e-4 on Δ). It is NOT the finite-sample fitting procedure's expected loss difference: at γ = 0 the oracle benefit of C can be zero while a fitted extended model differs by estimation noise and regularization, and at γ* > 0 the procedure-level gain differs from Δ_oracle by bias and noise. The 5% FPR and 80% power claims are claims about the procedure's interval behavior at the planted oracle values — they do not validate the intended predictive estimand. The mapping to the selected inference target is conditional and deferred: under G6a-fix the relevant procedure target conditions on the realized training data; under G6a-id it conditions on training identities and averages over training outcomes; under G6b it is the unconditional full-procedure Δ; the current oracle γ* coincides with none of them in finite samples. After the G6 choice and the §5A model resolution, γ* is recalibrated to the selected target, or the targets are restated. Until then, no FPR/power result may be read as validating the predictive estimand. Two paths after selection (deferred): (i) recalibrate γ* to the selected finite-sample procedure target and freeze the calibration procedure (bisection tolerance, seed, Monte Carlo size) before Phase 1; or (ii) restate the simulation as an oracle-effect stress test and remove all claims that its FPR/power results validate the predictive estimand. Either path is recorded at the simulation-protocol freeze (§11).

**Phase-1 evaluability policy (O3 refinement; floor number open).** Phase 1 outputs split into (a) feasibility/gate-classification operating characteristics (always reported) and (b) interval performance (coverage/FPR/power) conditional on a replication being estimable under the frozen procedure. The protocol prespecifies the minimum number of feasible replications required for interval assessment and the disposition when a cell cannot reach it: such cells are marked NOT EVALUABLE for interval performance and never pass the interval gate by default. P(feasible) is reported separately per cell. Any rejection/conditioning used to obtain feasible simulation replicates is disclosed, seeded, and distinguished from unconditional feasibility-probability estimation. The floor number and any grid/sample-size re-anchoring are O3 (owner) — no simulation runs while this item and the §5A contradiction remain unresolved. Illustrating the need: at bucket-local F_bl = 0.001546 ((a) @ N_b = 120), 2000 unconditional replications yield ≈ 3.1 expected feasible replications — such a cell cannot meaningfully evaluate interval coverage on the stated budget, and the complete rule is stricter still.

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

**Outcomes (PROPOSED parameters; not validated).** Per (body, suite): logit(p) = m(x) + γ·C + u + v, x = log(1+k), m(x) = θ0 + θ1·x, u ~ N(0, σ_b²) (body), v ~ N(0, σ_s²) (suite), s ~ Binomial(20, p); soft label = s/20. Proposed: θ0 = 0, θ1 = −1, σ_b = σ_s = 1. The latent structural fixed-effect component (m(x)=θ0+θ1x) lies in the baseline RCS span. Body and suite random effects are present in the outcome-generating process but omitted from the stated fitted model; therefore, correct specification of this latent fixed-effect component does not establish that the fitted likelihood is correctly specified for the marginal observed outcomes. Phase 1 assesses performance under this declared random-effects environment and does not establish robustness to alternative baseline/marginal-model misspecification. Extended adds γ·C only. Deterministic tail-scale assessment at γ = 0 (per-pair fractions from `dgp_outcome_tails.py` — Simpson quadrature, 81- vs 161-node grids agree to 6e-12 — crossed with exact per-bucket support expectations in `tail_support_d.py`): the supported population does not retain the original in-range k-mix (support selection thins buckets unevenly), so the expectation is N_s·Σ_k E[B_{k,support}]·q_{tail,k} with per-bucket quantities, not the mix-averaged rate. Formally, with I_k = 1{bucket k passes conditions 1–4} and G = 1{Σ_k I_k ≥ 2}, the tables use E[n_k·I_k] (bucket-marginal expectations); the complete-population count for a globally-supported analysis population is n_k·I_k·G, and an expectation conditional on global support would additionally divide by P(G = 1). The following expectations are calculated under the bucket-local support proxy: each bucket is assessed against conditions 1–4 independently. The global analysis-support rule additionally requires at least two buckets to pass. Accordingly, these values are not expectations conditional on the global support event and do not estimate the probability that the complete support and outcome gate passes. The complete-rule distribution must be evaluated under the adopted model/support specification; until then, the table is descriptive only. The support event is outcome-blind, but that does not make the bucket-local and globally supported populations interchangeable. N_s ∈ {20, 40} are sensitivity cases S20/S40 — the real-study suite count is owner-open, not adopted. The Revision B headline (≈ 26.5 upper-tail pairs at (a) @ N_b = 600 / S40) used the mix-averaged rate and is SUPERSEDED (the corrected value is below it: support tilts toward k = 10, the lower-rate bucket — contrary to the conjectured direction; the computation decides). In the computed bucket-local table, the upper-tail pair and body expectations are below their gate thresholds in every listed cell. The lower-tail distinct-body expectation is below D=10 in every listed feasibility-size cell. Some suite expectations exceed S=6; therefore, it is not correct to say that every diversity expectation misses its threshold. These are marginal expectations, not gate-pass probabilities: neither an expectation below a threshold nor one above it determines the probability that the joint gate passes. Three concepts stay separate throughout: an expected count, a probability of meeting a count threshold, and a structural zero. At γ ≠ 0 the tail rate additionally needs the supported C-distribution (requirement stated, not computed here). The joint gate-pass probability P(≥ M pairs ∧ ≥ D bodies ∧ ≥ S suites per tail) needs latent-scale joint integration = Phase-1 simulation scope (see §9 reporting), not pre-freeze arithmetic.

<!-- TAIL-A-BEGIN -->
**Per-bucket support and per-k tail rates (bucket-local support, γ=0; `tail_support_d.py`):**
Per-k tail fractions: k=5: P(s≤5)=0.708871, P(s≥15)=0.032657; k=10: P(s≤5)=0.829803, P(s≥15)=0.012253; k=20: P(s≤5)=0.916672, P(s≥15)=0.003653.
| cell | E[B_5] | E[B_10] | E[B_20] |
|---|---|---|---|
| a-hist @ 113 | 1.12 | 0.12 | — |
| a-hist @ 150 | 1.66 | 0.44 | — |
| a-hist @ 450 | 4.75 | 13.82 | — |
| a-hist @ 600 | 4.89 | 20.78 | — |
| b-hist @ 113 | 0.61 | 0.00 | 0.00 |
| b-hist @ 150 | 1.11 | 0.02 | 0.00 |
| b-hist @ 450 | 4.19 | 2.11 | 0.06 |
| b-hist @ 600 | 4.75 | 5.36 | 0.20 |
| c-hist @ 113 | 0.01 | 0.00 | — |
| c-hist @ 150 | 0.06 | 0.00 | — |
| c-hist @ 450 | 1.45 | 0.93 | — |
| c-hist @ 600 | 2.07 | 2.65 | — |
| a50 @ 150 | 1.11 | 2.08 | — |
| a50 @ 600 | 4.75 | 29.17 | — |
| b3 @ 150 | 0.23 | 0.20 | 0.00 |
| b3 @ 600 | 3.10 | 16.40 | 1.49 |
| c50 @ 150 | 0.02 | 0.02 | — |
| c50 @ 600 | 1.66 | 5.36 | — |
(Σ_k E[B_k] cross-checks against the feas totals: max diff 7.11e-15.)
<!-- TAIL-A-END -->

<!-- TAIL-B-BEGIN -->
**Gate-tail expectations vs M=30 / D=10 / S=6 (✓/✗ marks whether the expectation meets the threshold; descriptive, not a pass verdict):**
| cell | N_s | E[pairs] lo | E[pairs] hi | E[bodies] lo | E[bodies] hi | E[suites] lo | E[suites] hi |
|---|---|---|---|---|---|---|---|
| a-hist @ 113 | S20 | 17.96 ✗ | 0.76 ✗ | 1.24 ✗ | 0.33 ✗ | 2.05 ✗ | 0.41 ✗ |
| a-hist @ 113 | S40 | 35.93 ✓ | 1.53 ✗ | 1.24 ✗ | 0.44 ✗ | 4.09 ✗ | 0.81 ✗ |
| a-hist @ 150 | S20 | 30.75 ✓ | 1.19 ✗ | 2.09 ✗ | 0.51 ✗ | 2.86 ✗ | 0.58 ✗ |
| a-hist @ 150 | S40 | 61.49 ✓ | 2.38 ✗ | 2.09 ✗ | 0.70 ✗ | 5.72 ✗ | 1.16 ✗ |
| a-hist @ 450 | S20 | 296.66 ✓ | 6.49 ✗ | 18.53 ✓ | 3.14 ✗ | 12.68 ✓ | 2.38 ✗ |
| a-hist @ 450 | S40 | 593.32 ✓ | 12.98 ✗ | 18.56 ✓ | 4.48 ✗ | 25.37 ✓ | 4.75 ✗ |
| a-hist @ 600 | S20 | 414.11 ✓ | 8.28 ✗ | 25.62 ✓ | 4.10 ✗ | 14.28 ✓ | 2.84 ✗ |
| a-hist @ 600 | S40 | 828.22 ✓ | 16.57 ✗ | 25.65 ✓ | 5.89 ✗ | 28.55 ✓ | 5.69 ✗ |
| b-hist @ 113 | S20 | 8.72 ✗ | 0.40 ✗ | 0.61 ✗ | 0.17 ✗ | 1.15 ✗ | 0.23 ✗ |
| b-hist @ 113 | S40 | 17.44 ✗ | 0.80 ✗ | 0.61 ✗ | 0.23 ✗ | 2.31 ✗ | 0.45 ✗ |
| b-hist @ 150 | S20 | 16.03 ✗ | 0.73 ✗ | 1.12 ✗ | 0.31 ✗ | 1.83 ✗ | 0.39 ✗ |
| b-hist @ 150 | S40 | 32.06 ✓ | 1.46 ✗ | 1.13 ✗ | 0.42 ✗ | 3.67 ✗ | 0.77 ✗ |
| b-hist @ 450 | S20 | 95.48 ✓ | 3.26 ✗ | 6.33 ✗ | 1.44 ✗ | 5.18 ✗ | 1.15 ✗ |
| b-hist @ 450 | S40 | 190.95 ✓ | 6.51 ✗ | 6.35 ✗ | 1.98 ✗ | 10.35 ✓ | 2.29 ✗ |
| b-hist @ 600 | S20 | 159.86 ✓ | 4.43 ✗ | 10.27 ✓ | 2.03 ✗ | 7.85 ✓ | 1.51 ✗ |
| b-hist @ 600 | S40 | 319.73 ✓ | 8.86 ✗ | 10.29 ✓ | 2.84 ✗ | 15.71 ✓ | 3.02 ✗ |
| c-hist @ 113 | S20 | 0.20 ✗ | 0.01 ✗ | 0.01 ✗ | 0.00 ✗ | 0.03 ✗ | 0.01 ✗ |
| c-hist @ 113 | S40 | 0.39 ✗ | 0.02 ✗ | 0.01 ✗ | 0.01 ✗ | 0.06 ✗ | 0.01 ✗ |
| c-hist @ 150 | S20 | 0.89 ✗ | 0.04 ✗ | 0.06 ✗ | 0.02 ✗ | 0.14 ✗ | 0.02 ✗ |
| c-hist @ 150 | S40 | 1.78 ✗ | 0.08 ✗ | 0.06 ✗ | 0.02 ✗ | 0.27 ✗ | 0.05 ✗ |
| c-hist @ 450 | S20 | 35.93 ✓ | 1.17 ✗ | 2.37 ✗ | 0.52 ✗ | 3.41 ✗ | 0.60 ✗ |
| c-hist @ 450 | S40 | 71.86 ✓ | 2.35 ✗ | 2.37 ✗ | 0.72 ✗ | 6.82 ✓ | 1.21 ✗ |
| c-hist @ 600 | S20 | 73.25 ✓ | 2.00 ✗ | 4.70 ✗ | 0.92 ✗ | 5.45 ✗ | 0.95 ✗ |
| c-hist @ 600 | S40 | 146.50 ✓ | 4.00 ✗ | 4.71 ✗ | 1.29 ✗ | 10.90 ✓ | 1.89 ✗ |
| a50 @ 150 | S20 | 50.28 ✓ | 1.24 ✗ | 3.18 ✗ | 0.58 ✗ | 4.52 ✗ | 0.68 ✗ |
| a50 @ 150 | S40 | 100.55 ✓ | 2.47 ✗ | 3.19 ✗ | 0.82 ✗ | 9.04 ✓ | 1.35 ✗ |
| a50 @ 600 | S20 | 551.40 ✓ | 10.25 ✗ | 33.86 ✓ | 5.18 ✗ | 13.80 ✓ | 3.27 ✗ |
| a50 @ 600 | S40 | 1102.80 ✓ | 20.50 ✗ | 33.90 ✓ | 7.48 ✗ | 27.60 ✓ | 6.55 ✓ |
| b3 @ 150 | S20 | 6.70 ✗ | 0.20 ✗ | 0.44 ✗ | 0.09 ✗ | 0.87 ✗ | 0.12 ✗ |
| b3 @ 150 | S40 | 13.40 ✗ | 0.40 ✗ | 0.44 ✗ | 0.13 ✗ | 1.74 ✗ | 0.25 ✗ |
| b3 @ 600 | S20 | 343.59 ✓ | 6.16 ✗ | 20.97 ✓ | 3.11 ✗ | 14.03 ✓ | 2.55 ✗ |
| b3 @ 600 | S40 | 687.17 ✓ | 12.31 ✗ | 20.99 ✓ | 4.49 ✗ | 28.05 ✓ | 5.09 ✗ |
| c50 @ 150 | S20 | 0.59 ✗ | 0.02 ✗ | 0.04 ✗ | 0.01 ✗ | 0.09 ✗ | 0.01 ✗ |
| c50 @ 150 | S40 | 1.18 ✗ | 0.04 ✗ | 0.04 ✗ | 0.01 ✗ | 0.17 ✗ | 0.02 ✗ |
| c50 @ 600 | S20 | 112.45 ✓ | 2.40 ✗ | 7.00 ✗ | 1.17 ✗ | 7.72 ✓ | 1.20 ✗ |
| c50 @ 600 | S40 | 224.90 ✓ | 4.79 ✗ | 7.01 ✗ | 1.67 ✗ | 15.45 ✓ | 2.41 ✗ |
Suite quadrature 31 vs 61 nodes: maxdiff 1.60e-06.
<!-- TAIL-B-END -->

Any "spans both gate tails" characterization is therefore dropped; θ0, θ1, σ remain PROPOSED values pending reviewer sign-off and owner acceptance (§11).

**Planted effect.** γ = 0 for Δ = 0. For Δ ∈ {δ*, 2δ*}: γ* by bisection (tolerance 1e-4 on Δ) so the DGP population value of §1's estimand equals the target, using a fixed calibration seed and large Monte Carlo size from DGP truth (simulation-internal; never from real data). **γ* calibrates the population-oracle contrast** (the estimand evaluated on DGP truth), **not finite-sample learning-procedure performance**; the latter is what Phase 1 measures and reports (coverage, FPR, power of the procedure). Relation to the G6a/G6b inference targets: see the §9 calibration note (recalibration deferred until the G6 choice and the §5A resolution).

**Baseline misspecification.** Phase 1 does not assess robustness to baseline misspecification: the simulated latent fixed-effect component is correctly represented by construction. No robustness is implied. (A misspecification sensitivity scenario would be new procedure and is not added here.)

**Explicitly not modeled in Phase 1 (open option §9.2/O1):** invalid-submission rate, prompt/generation mechanics, probe-suite graph structure — Phase 1 is conditional on valid unique bodies unless a declared p_valid parameter is added.

## 9.2 Feasibility of the drafted rules under the drafted DGP (disclosed before freeze; decision required)

Exact deterministic arithmetic (log-space; `feas_prob.py`, `feas_prob_test.py`; provenance in Appendix C). Two results are kept separate: (1) the exact count-only support bound, ignoring §5 conditions 3–4; (2) the bucket-local support-feasibility calculation accounting for C variation and the extreme-representation conditions (observed-extremes reading), with remaining omissions stated below. "Bucket-local" means conditions 1–4 only: the rank-and-conditioning criterion is omitted, and the complete-rule probability is 0 as-drafted (§5A). Within the bucket-local family the tables differ in which conjuncts they include: F_bl = P(≥2 buckets pass conditions 1–4) includes the ≥2-bucket conjunct G; the expected-support figures E[B_k] = E[n_k·I_k] and every tail expectation built on them are bucket-marginal (no G conjunct) — a support proxy, not the globally-supported population. Neither estimates the complete-rule probability. Complete-rule probabilities will be recalculated after the §5A resolution (recipe: bucket-local sum ∧ conditioning pass over C-composition patterns). The split uses the exact fixed-size hypergeometric holdout (T = round-half-up(0.25·N) body identities); no binomial thinning. N below denotes unique valid bodies; the attempt-budget mapping is in §9.3. No count-only probability is the probability that the full study passes all gates.

**Full-population probabilities** — count-only P(≥2 in-range buckets, each ≥ B_min = 8 bodies) | bucket-local P(≥2 buckets pass conditions 1–4) (rank/conditioning conjunct excluded):

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

The simulation grid's N_b is simulated valid unique bodies; N_s is simulated suites with 20 soft-label inputs each. Attempts, valid bodies, unique bodies, in-range bodies, supported bodies, and suite identities are distinct units and are never interchanged. The hidden-suite count per real-study phase is an owner decision slot (cited precedents are not adoptions); validity-rate and duplicate-rate modeling at the attempt axis is O1. **Suite-count constraints (derived minima, not adopted counts).** The gate needs ≥ 6 distinct suites per tail (S ≥ 6): the feasibility sample needs ≥ 6 suites under the shared-tail interpretation (same suites may serve both tails), ≥ 12 under the disjoint interpretation (left open — owner, tied to the count decision). Any test-block suite-diversity rule of ≥ 6 suites at a 25% holdout implies ≥ 24 total suites (≥ 48 if disjoint), before integer rounding. Consequences: the 3-suite pilot precedent cannot satisfy the gate's S requirement; a 20-suite design yields 5 test suites, satisfying no ≥ 6 test-block need under either interpretation. The count remains an owner decision subject to these minima. Suite facts (supporting the crossed design): hidden suite M = 20 inputs (15 random + 5 templates), identity = instance seed (`specs/instrument_spec.json:23-27`, `study/instances.py:23-46`); k/C are body-level (probes ignore instance_seed; 0/120 v0.2 bodies change k across suites).

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

If the owner judges any scenario's implied spend unrealistic, the budget is an owner decision at freeze (§11) — stated now, not after money is spent. The tabulated probabilities are per-attempt under the stated protocol (single feasibility attempt; no repeated-attempt policy is specified); they are stress-scenario calculations, not forecasts, and are neither hidden nor presented as independently verified predictions.

## 11. Freeze-blocker register and authorization boundaries

**STAGE 1 — SIMULATION-PROTOCOL FREEZE (before any Phase 1 run).** Freezes the simulation DGP, analysis procedure, thresholds, seeds, dependencies, and acceptance criteria. Pre-freeze items (all must close before the simulation-protocol freeze):

1. §5 support-rule numbers: B_min, per-extreme minimum (4), κ_max — reviewer sign-off.
2. §6 gate numbers: θ_lo, θ_hi, M, D, S, v_min — reviewer sign-off.
3. §7 split fractions (75/25), R = 50, B = 2000, split-level minimum per §9.2/O2 resolution (covering all three sites: global, training, test), incomplete-cell handling text — reviewer sign-off after analysis-code spec.
4. §9 grid + targets as revised per §9.2 (incl. the §9 claim mapping), 2000 replications, Clopper–Pearson decision rule — reviewer sign-off (document side only; evidence is post-freeze).
5. §9.1 DGP specification (k-draws incl. O4 choice, Dirichlet/θ/σ values, duplicate mechanism, γ-calibration, population-oracle vs finite-sample statement) — reviewer sign-off + owner acceptance.
6. §4 validity-check specification (signature, AST allowlist content, no-IO pattern list) and the versioned checker artifact with recorded SHA-256 — reviewer sign-off.
7. §9.2 option resolution (O1–O5), including the D3 evaluability policy (output split, minimum-feasible-replications floor, not-evaluable disposition, P(feasible) reporting, rejection disclosure) — reviewers recommend, owner decides.
8. G6a-fix vs G6a-id vs G6b inference-target choice — reviewers recommend, owner decides.
9. §10 scenarios and recomputed budget arithmetic (per §9.2) — owner acceptance.
10. Normalization rule (§3 E, without trailing-whitespace stripping; cross-phase duplicate rule) — reviewer sign-off that the byte-level rule is adequate for the unique-body estimand.
11. Master seed 20261015 and the §7.4 standard-library seed-derivation scheme + pinned CPython version — reviewer sign-off.
12. Hidden-suite counts per real-study phase — owner decision (precedents cited, not adopted).
13. §5A matrix-contradiction resolution (M1/M2/M3 — reviewers recommend; M1/M3 require explicit owner approval as model changes, M2 requires reviewer sign-off on the exact mathematics plus owner acceptance as a gate-semantics change) — owner decision with reviewer recommendation.
14. Complete-rule probability recalculation against the adopted §5A resolution — reviewer verification (computable only after item 13).
15. Training-block specification (N1 reading selection tied to O2; N2 eligibility rule per adopted M with P-i/P-ii policy; per-split checks with INFEASIBLE disposition; same-cases requirement) — owner decision with reviewer recommendation (blocked on M-selection + O2).
16. Estimand conditioning on the globally-supported population (N4) — owner acceptance (narrows the claim).
17. Calibration procedure freeze (G6-conditional mapping; directional FPR/power definitions; per-replication coverage-truth method) — reviewer sign-off + owner acceptance (blocked on M + G6).
18. Suite-count selection subject to the §9.3 derived minima (shared-vs-disjoint interpretation + count) — owner decision.

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
- `v03p/PHASE0_DESIGN_2026-10-15_RevC.md` (Revision C draft): joint GPT/CLAUDE review 2026-10-15 with verdict NOT APPROVED (GPT A/B/C, CLAUDE N1–N8, hash/portability release blockers). Preserved as-reviewed, uncommitted; superseded by Revision D.
- GPT draft PR #1 (`gpt/rev-d-review-corrections`, commit `e4bb6ee009dd57d38c7a3b5f6694d81043918f21`, correction record `v03p/PHASE0_REV_D_GPT_CORRECTIONS_2026-10-15.md`): six corrections D1–D6 against Revision D, branch deliberately separate from `master`, NOT merged; protocol remains unapproved for freeze. Integrated below (uncommitted); the branch was not fetched or merged locally and no local bytes were verified by GPT.
- Draft PR #2 (independent review of the published `review/revd-package` at `eb46a2c9fe165b7f19f8c88f1e932f9e8df5a430`): byte-integrity PASS on all 19 files (scripts not executed); verdict REQUEST CHANGES with five textual findings (coverage/evaluable cells, §9.2 header, M2 estimand wording, M2 standardization wording, publication metadata); unmerged; no freeze/authorization. Addressed below in this Revision E draft; the published RevD bytes are unchanged.
- v0.1/v0.2 records, audit series (`da4030d`, `c75fb43`, `11d86b9`), rlc0 series: untouched.

## Appendix C — design-arithmetic provenance (deterministic; no simulation)

**N7 erratum (mechanical correction).** The Revision C table contained a transcription error in the `feas_prob.py` row (57 characters instead of the full 64-character digest); the other eleven Revision B/C entries verified byte-exact against disk. Short-form (ellipsized) hash citations in chat messages are not authoritative — only the full table values below, mechanically verified from disk, are. Both tables below are generated mechanically (no hand transcription of hashes).

**Staged portable evidence (`v03p/scripts/` as committed for review on `review/revd-package`; local staging is not committing).** Same-directory imports only; run from `v03p/scripts/` per `RUN.txt` (pinned layout: repository `.venv`, CPython 3.14.0, stdlib only). Four scripts are byte-identical to the verified Revision B/C files (hashes preserved); three had machine-specific path lines removed (new hashes); one script is new. Publication of this package is for independent review only — not frozen, not phase-authorized.

<!-- PROV-STAGED-BEGIN -->
| artifact | bytes | SHA-256 |
|---|---|---|
| `feas_prob.py` (corrected full-population arithmetic (Rev B)) | 11930 | 262E0DBFE6C08A97084C3AF82BBC1D7B5E1AD7B16C9ED97EC7DE57BB1DC80FFE |
| `feas_prob_test.py` (corrected exact fixed-size block readings (Rev B)) | 16326 | 6DFC54C86C4E923C4EC8EB5875FFBC95815EF0AE92BDDBCC8F40086E3DBC0668 |
| `dgp_counts_v2.py` (conditioned-DM enumeration (Rev B)) | 4603 | 8D07376BA46A956E6B140144A95E1BFD0C1C3EE8004CF27F01C6B0E2F076C216 |
| `dgp_outcome_tails.py` (deterministic tail-scale assessment (Rev B)) | 5940 | F530EC74F6EF5550692A8FF0AE6EB44B7C70ADC58BF334AE0736243F2890CF0E |
| `g_check.py` (g_k brute-force cross-check (Rev B; path-fix Rev D)) | 1613 | 8ED928BA507F86828802703037DF5C5DDF9E22D0BDA95FA5C2FEA7A100EF27E0 |
| `feas_check.py` (fast exact reference tests (Rev C; path-fix Rev D)) | 9615 | AD82BF75E753CB4103C6A2F1DDF73688BA791343CD23FD1DAF91E35E24811DCC |
| `outcome_tails_c.py` (gate-tail expectations on bucket-local support (Rev C; path-fix Rev D)) | 2509 | D00E09265323C078FB77A110BA8F7B8C9F8D925FED8526E66448E44C97CC62E7 |
| `tail_support_d.py` (per-bucket gate-tail expectations (Rev D)) | 8859 | 9E67FE25DB98B75895FEFB31C61177238F45340A29189D1DAA4D9B37A42C84B0 |
| `RUN.txt` (pinned run record (Rev D)) | 1486 | B39052057D42AC672F31C7C9919EE15C19B1B1EF259D0BB086499C584879AE0D |
| `feas_prob.out.txt` (deterministic output) | 12330 | 3CD0ABD28EB7962756DDD3E540DA3F1F8817BA0CC6E187D343F4D28C60EDA4BB |
| `feas_prob_test.out.txt` (deterministic output) | 32442 | DB5E250C02A86BBD3D02EC93E1FD488766F87A646E4F66663E4B99780BEA27F8 |
| `dgp_counts_v2.out.txt` (deterministic output) | 3574 | 74A5C96C55C040D6655959EFC8AF96F8692774B3C6600B6CE54072C4FDFB90C5 |
| `dgp_outcome_tails.out.txt` (deterministic output) | 7688 | 8DC11E64B77541051423AACAE2C25304521EA970C32A774081B04E56CEB82DD9 |
| `g_check.out.txt` (deterministic output) | 4516 | 6EFB2F5CC7B4954253CE2CFC9E0D5C0D285FC7706DF4F93E1453C7D767F104A5 |
| `feas_check.out.txt` (deterministic output) | 3376 | 32BCC2B2DB0B8299D411393719A20F354FC33150AB6598E5082869D79A218F20 |
| `outcome_tails_c.out.txt` (deterministic output) | 6104 | 9805ED4CEF98F221D696DCABD3830D15B2CB9510351FC932BA82C18D46F00F0C |
| `tail_support_d.out.txt` (deterministic output) | 13170 | 6ABC0867FCC3A72D0DADAECB09DC84EB8EE637CECF5FC57F6AF13FCE186CEFE6 |
<!-- PROV-STAGED-END -->

**Historical lineage (temporary working directory; superseded as the canonical record by the staged copies; byte-identical files share hashes).**

<!-- PROV-HIST-BEGIN -->
| artifact | bytes | SHA-256 |
|---|---|---|
| `feas_prob.py` (corrected full-population arithmetic (Rev B)) | 11930 | 262E0DBFE6C08A97084C3AF82BBC1D7B5E1AD7B16C9ED97EC7DE57BB1DC80FFE |
| `feas_prob_test.py` (corrected exact fixed-size block readings (Rev B)) | 16326 | 6DFC54C86C4E923C4EC8EB5875FFBC95815EF0AE92BDDBCC8F40086E3DBC0668 |
| `dgp_counts_v2.py` (conditioned-DM enumeration (Rev B)) | 4603 | 8D07376BA46A956E6B140144A95E1BFD0C1C3EE8004CF27F01C6B0E2F076C216 |
| `dgp_outcome_tails.py` (deterministic tail-scale assessment (Rev B)) | 5940 | F530EC74F6EF5550692A8FF0AE6EB44B7C70ADC58BF334AE0736243F2890CF0E |
| `g_check.py` (g_k brute-force cross-check (Rev B; path-fix Rev D)) | 1695 | 12A650D0AB7CD489DBABAB50E284BF0C44CEF8EFA7E7D5E55758AD7236532510 |
| `feas_check.py` (fast exact reference tests (Rev C; path-fix Rev D)) | 9702 | F5DAFD13EDBC4E0F4E4E024A4D9AF906BB79797F7A6304A6CF68F6D775B8BEE5 |
| `outcome_tails_c.py` (gate-tail expectations on bucket-local support (Rev C; path-fix Rev D)) | 2597 | 4CC5D4E82B8E9F7620AD87238ED2A86D010542F6992C70A410344F7F61B1CADF |
| `feas_prob.out.txt` (deterministic output) | 12330 | 3CD0ABD28EB7962756DDD3E540DA3F1F8817BA0CC6E187D343F4D28C60EDA4BB |
| `feas_prob_test.out.txt` (deterministic output) | 32442 | DB5E250C02A86BBD3D02EC93E1FD488766F87A646E4F66663E4B99780BEA27F8 |
| `dgp_outcome_tails.out.txt` (deterministic output) | 7688 | 8DC11E64B77541051423AACAE2C25304521EA970C32A774081B04E56CEB82DD9 |
| `feas_check.out.txt` (deterministic output) | 3376 | 32BCC2B2DB0B8299D411393719A20F354FC33150AB6598E5082869D79A218F20 |
| `outcome_tails_c.out.txt` (deterministic output) | 6104 | 9805ED4CEF98F221D696DCABD3830D15B2CB9510351FC932BA82C18D46F00F0C |
<!-- PROV-HIST-END -->

**Methods.** All scripts use only the Python standard library. Exact multinomial/hypergeometric enumeration in log space (summation-term cutoff 1e-20, omitted mass bounded by 1e-13); Simpson quadrature over latents (outcome-tail grids agree to 6e-12; suite quadrature 31 vs 61 nodes agree to 1.60e-06); exact composition enumeration (`dgp_counts_v2.py`; `g_check.py` brute-force cross-check of the pair-sum g_k formula 12/12 to 1e-9); `feas_check.py` reference tests 26/26 PASS (closed forms vs explicit sums, end-to-end brute force at N=32, RCS rank minors, tail convergence, wiring); regression of the corrected count-only figures against the verified (a)/(c) values (11/11 to 5e-7) with the corrected (b) values verified as supersets of the superseded branch; `tail_support_d.py` exact per-bucket expectations with cross-checks against the feas totals (all ≤ 4e-15). Structural zeros (0*) vs log-space underflow (0-dag) are distinguished in every output. The conservative reading with §5 conditions 3–4 re-applied at test level is statedly not computed; validity rate and duplicate-attempt mechanics are not modeled (N denotes unique valid bodies). Script fate (commit under v03p/ vs inline numbers) is an open reviewer/owner decision (Appendix D).


**GPT verification record (2026-10-15 review).** GPT extracted the three Revision B scripts: source byte counts and SHA-256 match the recorded values; `feas_prob.py` reproduces the count-only and bucket-local figures; `dgp_outcome_tails.py` reproduces the upper-tail fractions (≈ 2.59%, 2.28%, 2.45% for the historical mixes); `feas_prob_test.py` exceeded GPT's 200-second review timeout (its block-level tables were unverified by GPT, not disproven). "Match" here means agreement with the mechanically verified full digests in the tables above (prefix comparison is not sufficient).

**Local runtime report (CPython 3.14.0, Win32; portable runs from `v03p/scripts/`).** feas_prob.py 5826 ms; feas_prob_test.py 35662 ms; dgp_counts_v2.py 1720 ms; dgp_outcome_tails.py 7667 ms; g_check.py 463 ms; feas_check.py 1356 ms; outcome_tails_c.py 3224 ms; tail_support_d.py 27911 ms. Portable re-runs reproduce the recorded outputs (normalized-content MATCH on all carried outputs). The full block script runs in ~35 s in this environment; review-environment timing varies — `feas_check.py` covers the same algebra (closed forms, end-to-end brute force at N=32, wiring) in ~1 s.

## Appendix D — decision register (resolved / outstanding evidence / owner decisions)

**Resolved in Revision B (each repair cites its finding):** header chronology with unset freeze date; §4 interface/validity rewrite (GPT finding 1); two-boundary §11–§12 (GPT finding 2); §5 rank-increase test replacing the cross-k requirement (GPT finding 3); §5 exact design matrices, support-only fitting, training-block rule; §7.4 standard-library RNG; §9.1 feasibility-constrained DGP with uniformity 1/Z(k) and deterministic C summaries; scenario-(b) three-bucket event correction with regression; exact fixed-size hypergeometric split replacing binomial thinning; §10 scenario-(c) correction on recomputed grounds; normalization without whitespace stripping (GPT finding 7) with cross-phase duplicate rule; 2δ* claim mapping recorded as limitation; γ* population-oracle vs finite-sample distinction; explicit baseline-misspecification non-assessment; §9.2 O1–O5 table with none chosen; §9.3 sample-unit mapping.

**Resolved in Revision C:** §5A contradiction stated with the verified rank table and the M1/M2/M3 candidates (exact definitions, consequences, approval routing — no selection; κ≤30 retained-but-flagged); bucket-local relabeling throughout with the complete-rule probability stated as 0 as-drafted and the recalculation recipe deferred; Phase-1 incompatibility documented (grid/gate/power-cell evaluation deferred until the §5A resolution); gate-tail expectations recomputed on bucket-local support with N_s sensitivity labels; planted-oracle calibration meaning fixed with the G6-conditional mapping and the FPR/power non-claim; verification package (GPT record, runtime report, reference tests) delivered.

**Resolved in Revision D:** §5B training-block specification (per-split checks on the realized matrix with INFEASIBLE disposition and failure counting; N1 readings distinguished with tables tied to global-membership; N2 eligibility per M-option with policy options open; same-cases requirement); §1 estimand conditioned on the globally-supported population (owner acceptance required for the narrowed claim); per-M matrix and standardization definitions (M3 ridge-on-dummies sub-decision left open); suite-count derived constraints with precedents marked incompatible (shared-vs-disjoint left open); directional FPR/power with harm reported separately and per-replication coverage targets specified for post-selection use; per-bucket tail expectations replacing the mix-averaged headline (26.5 superseded); N7 provenance correction with mechanical hashes and portable scripts; joint gate-pass probability assigned to Phase-1 estimation (not pre-freeze calculable); GPT-PR D1–D6 integration (§0.4): proxy labeling with I_k/G formalism, D2 wording, evaluability policy structure, G6a-fix/G6a-id/G6b explicitness, per-M fit-vs-diagnostic specification, narrowed baseline claim.

**Resolved in Revision E:** five textual fixes from the PR #2 independent review with no reruns and no owner decisions: coverage rule conditional on interval-evaluable cells with NOT EVALUABLE disposition (O3 still open); §9.2 header renamed to conditions 1–4 with rank/conditioning exclusion stated; M2 stale interval sentence replaced (predictive-loss target retained); M2 standardization stated as diagnostic-only with raw-RCS fitting; publication metadata distinguishes review-committed package from frozen/authorized protocol.

**Outstanding evidence (closable only post-freeze, never by document revision):** Phase 1 coverage/FPR/power evidence and interval-procedure selection; the §6 feasibility-gate pass; checker artifact SHA-256 (recorded at simulation-protocol freeze); pinned CPython version (recorded at freeze); γ* calibration values (Phase-1 simulation-internal); §5A resolution adoption (§11.13); complete-rule recalculation against the adopted resolution (§11.14); training-block specification adoption (§11.15); estimand-acceptance (§11.16); calibration-procedure freeze (§11.17); suite-count selection (§11.18); γ* recalibration to the selected G6 target; D3 floor number + grid re-anchoring (O3).

**Foued's owner decisions (none chosen here):** §5A M1/M2/M3 choice (reviewer lean recorded: M3 with the scope qualification, CLAUDE concurring it is Foued's call; M1/M3 explicit approval as model changes; M2 acceptance as gate-semantics change); training-block reading and eligibility policy (N1/N2, tied to O2 and M); estimand conditioning acceptance (N4); M3 ridge-on-dummies sub-decision (N3); suite count with derived minima and shared-vs-disjoint interpretation (N5); directional FPR/power and coverage-truth method acceptance (N6); O1–O5 coordinated resolution (incl. D3 evaluability floor + grid); G6a-fix vs G6a-id vs G6b; calibration path (i) recalibrate vs (ii) oracle-stress-test restatement; generation-budget spend approval; §10 acceptance; §9.1 DGP parameter acceptance (θ/σ, with the recorded upper-tail shortfall); policy for permitted pre-freeze computation (plus GPT deviation classification — see the process-deviation record); script fate (commit vs inline).

**Settled (not reopened):** C (ACCEPT, r = 1.5); E (Option 1, unique normalized valid bodies).
