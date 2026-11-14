# B1 computational implementation plan — v0.1 design draft

**Date:** 2026-11-14  
**Status:** DESIGN DRAFT — NOT ACCEPTED, NOT FROZEN, NOT AN EXECUTION GO  
**Branch:** `gpt/b1-computational-plan-2026-11-14`  
**Binding statistical predecessor:** B1 analysis plan v1.7, accepted and frozen by the separate GPT acceptance record dated 2026-11-14.  
**Purpose:** specify the deterministic numerical implementation and the design-only feasibility checks required before any future execution GO. This document does not amend v1.7's estimand, null, target population, test, thresholds, or failure rules.

## 0. Authorization boundary

This is a design-only artifact. No fitting, numerical probability evaluation, permutation, Monte Carlo, simulation, solver construction, mutation allocation, generator execution, or use of the 78-record bank is authorized or performed by this document.

The computational plan must be reviewed and accepted before an execution GO can be considered. Acceptance of this document would still not itself constitute an execution GO. The 78-record bank remains exposed development data, not sealed confirmatory data. No new-parent or new-record generalization is supported.

## 1. Frozen statistical contract

Implementation must reproduce B1 analysis plan v1.7 exactly:

- Primary statistic: equal-parent held-out log-loss gain under LOPO, with the baseline and enriched models refitted in every fold.
- Baseline: cell intercepts plus record effects. Enriched: the same terms plus the raw, uncentred (C_D) exposure and one common slope.
- Record effects obey the declared sum-to-zero constraint over the 78 records.
- The supplied exposure is permuted; raw failure/unresolved vectors, parent identity, cell membership, version identity and the full outcome vector remain attached.
- The admissible assignment set is defined by equality of the complete, declared design-only audit key.
- Exact enumeration is selected when |Ω| ≤ 10^6; otherwise use 9,999 accepted rejection-sampled assignments, with a hard cap of 10^8 design checks.
- The observed evaluation (T(b_{obs})) is computed once and reused exactly once as the observed member of the reference comparison set. It must not be fitted or counted twice.
- All applicable assignments must fit under the v1.7 availability rule. No failed assignment is dropped or replaced. Any applicable failure makes the test unavailable.
- The real-data inferential target is conditional on the realized parents, outcomes, cells and exposure multisets. No parent-population uncertainty or generalization claim is made.

Any implementation choice below is subordinate to these rules. A computational convenience must never alter the statistical contract.

## 2. Parameterization and design matrices

### 2.1 Record-effect constraint

Use a fixed, full-column-rank contrast basis for the 78 record effects. The recommended construction is an orthonormal Helmert contrast matrix H with 78 rows and 77 columns, fixed by record identifier order. Write omega = H eta. This enforces sum over r of omega_r = 0 by construction and avoids a redundant 78th record coefficient.

The canonical record order must be read from the frozen bank manifest and stored in the run manifest. No order may be inferred from incidental file-system order.

### 2.2 Design matrices

For each LOPO fold, construct the baseline and enriched matrices from the exact same training-row identifiers:
- baseline columns: one indicator per eligible exact cell and the 77 record contrasts;
- enriched columns: baseline columns plus the raw (C_D) column.

The row order is a canonical sort by stable version identifier, then record identifier. The column order is fixed as cell indicators, record contrasts, then (C_D). Test rows are never used to fit parameters. The scoring rows and fold membership are those frozen by the v1.7 design-only audit.

Before optimization, verify dimensions, finite inputs, binary outcomes, unique row identifiers, full-rank design matrices, and the declared sum-to-zero constraint. These are deterministic integrity checks, not grounds for changing the scored population. A failed integrity check makes the affected dataset unavailable and is reported.

### 2.3 Exact representation of concentration

Store each concentration as its exact rational definition (m/k), where (m=max_j f_j) and (k=k_{fail}), alongside its displayed decimal representation. Equality, distinct-value counts, multiplicities and permutation enumeration use the reduced integer numerator/denominator pair, never rounded floating-point values. Conversion to IEEE-754 binary64 occurs only when building the numerical predictor column for model fitting.

This preserves exact permutation combinatorics and prevents two distinct rational concentrations from being merged by display rounding.

## 3. Optimisation algorithm

### 3.1 Ordinary maximum-likelihood fits

Use deterministic Fisher-scoring / iteratively reweighted least squares (IRLS) for both models.

At each iteration:
1. Compute the linear predictor, probabilities using a numerically stable logistic function, log-likelihood, score vector and expected Fisher information.
2. Solve the Fisher-scoring system for the parameter increment using the Cholesky factorization specified in §4. Do not form an explicit matrix inverse.
3. Apply deterministic step halving: start at step length 1 and halve until the candidate objective is finite and does not decrease. The maximum number of halvings is 50. If no acceptable step is found, the fit fails.
4. Evaluate the v1.7 componentwise relative-gradient convergence criterion after the accepted update. Stop when it is ≤ 10^-8 or when 200 iterations have been used.

Initialization is the all-zero coefficient vector in the constrained parameterization. There is no random initialization, warm start, data-dependent alternative initialization, or parameter carry-over between folds or assignments. Both models use the same stopping and step-acceptance rules.

### 3.2 Firth / Jeffreys-penalized refits

When the v1.7 enriched-model trigger fires, refit both models using the exact objective
[
ell^F(gamma)=ell(gamma)+\tfrac12\log\det I(\gamma).
]

Use the standard adjusted-score representation of the Jeffreys-penalized logistic likelihood. At each iteration compute the penalized objective, its analytic adjusted score, and the expected information matrix. Solve the Fisher-scoring system using the same Cholesky routine as §4, then apply the same deterministic step-halving rule, with acceptance based on non-decrease of the penalized objective. Use the same zero initialization, 200-iteration maximum and v1.7 relative-gradient criterion, where the gradient is that of the penalized objective.

The implementation must independently verify that the adjusted score equals the gradient of the stated penalized objective to a predeclared floating-point tolerance in a separate software-validation test suite. This is a software correctness test, not a data analysis. The tolerance and test vectors must be frozen before any execution GO.

If either penalized refit fails, if the information matrix cannot be Cholesky-factorized, if its log-determinant is non-finite, or if no step is accepted within 50 halvings, apply the v1.7 unavailable rule. No diagonal jitter, pseudo-inverse, ridge fallback, alternate optimizer, or silent model simplification is allowed.

### 3.3 Standard error and separation trigger

The enriched model is fitted first. Apply the v1.7 trigger exactly: nonconvergence, |β̂_C| > 50, or Wald standard error > 10^3. The Wald standard error is computed from the inverse-information diagonal using triangular solves, not an explicitly formed inverse. If the ordinary enriched fit cannot provide a valid standard error because the information factorization fails, that is a fitting failure and invokes the declared trigger only insofar as the v1.7 rule says nonconvergence; it must not be silently reinterpreted as a finite standard error.

If the trigger fires, refit both models with the Firth objective. If the baseline fit fails without the enriched trigger having activated a joint Firth refit, the test is unavailable, as required by the v1.7 acceptance record.

## 4. Linear algebra

**Candidate routine:** IEEE-754 binary64 arithmetic with the LAPACK symmetric positive-definite Cholesky factorization (lower-triangular form, corresponding to `DPOTRF`), called through the pinned numerical-library interface selected in the environment lock.

- Solve systems by forward/back substitution using the Cholesky factor. Never compute the inverse of the information matrix explicitly.
- Compute the log determinant as twice the sum of the natural logarithms of the Cholesky diagonal entries.
- A non-positive-definite matrix, factorization error, non-finite factor, or non-finite log-determinant is a hard fit failure under v1.7.
- No diagonal perturbation, eigenvalue clipping, pseudo-determinant, generalized inverse, or fallback factorization is permitted.
- Record the library name/version, linked LAPACK implementation, binary64 platform details, factorization status and any reported numerical error code.

The exact numerical-library version and platform build are not frozen in v0.1 because the repository contains no root-level `pyproject.toml`, `requirements.txt`, `environment.yml` or `setup.cfg` at the inspected review-branch root. The implementation environment must first be inventoried and then pinned in a lock artifact before software validation. No dependency is to be installed into the user's working environment as part of this design step.

## 5. Random-number generation and assignment sampling

### 5.1 Generator proposal

Candidate generator: NumPy `PCG64DXSM`, initialized from the v1.7 root seed 20261114 through NumPy `SeedSequence`. The exact NumPy version and bit-generator implementation must be pinned before execution.

Use spawned, non-overlapping child streams with stable identifiers:
- one stream per synthetic replication;
- within each replication, one substream per λ value;
- one substream for that dataset's assignment proposals.

Stream identifiers are derived from fixed integer indices, never from execution order, wall-clock time, process ID or worker scheduling. The manifest records the root seed, bit-generator name/version, child-stream index mapping, and every proposal/acceptance counter.

The statistical guarantee remains the v1.7 sampling-model guarantee, not a claim conditional on one deterministic seed. The implementation must not reuse a stream across independent replication/λ tasks.

### 5.2 Uniform proposals on Ω

For each cell, randomly permute the cell's version positions with an unbiased Fisher–Yates shuffle driven by the designated generator stream, then assign the observed multiset of rational C_D values to those positions. Because every distinct arrangement has the same number of underlying position permutations, the induced proposal is uniform over that cell's distinct assignments. Independent cell streams or a fixed sequential stream consumption rule produce the product-uniform proposal on Ω.

For every proposal, compute the complete audit-equality key and accept if and only if it exactly equals the observed key. Rejected proposals consume one design check and no model fit. Continue until 9,999 accepted assignments or the hard 10^8 design-check cap is reached. Never change the cap or accepted-sample target after observing the acceptance rate.

### 5.3 Independent accepted draws and accounting

Each proposal uses fresh generator output. Sampling is with replacement: repeated accepted assignments are allowed and counted as separate Monte Carlo draws, as required by v1.7. Record:
- total proposals/design checks;
- accepted and rejected counts;
- acceptance rate;
- accepted assignment identifiers and canonical hashes;
- repeated-assignment count;
- stream state identifiers or reproducibility metadata sufficient to regenerate the sequence.

The observed statistic is evaluated once before the sampled comparison set and reused once. The 9,999 accepted assignments are additional evaluations; no observed assignment is added a second time by the sampler.

### 5.4 Exact enumeration

When |Ω| ≤ 10^6, enumerate each distinct multiset arrangement exactly once in deterministic lexicographic order of reduced rational concentration values and canonical version identifiers. Apply the audit-equality key before fitting. The observed assignment is included exactly once; reuse its already-computed (T(b_{obs})), rather than fitting it again. Exact p-value denominators are |Ω_adm|, with no +1.

The enumerator must be checked on small, hand-constructed fixtures where cell multiplicities are known. These are software unit tests and must not use the project bank.

## 6. Design-only feasibility of the 10^8 cap

The rejection-sampling acceptance probability is
[
a=|\Omega_{adm}|/|\Omega|.
]
A design-only feasibility assessment must be completed before any Monte Carlo sampling. It must use only the frozen design structure, rational concentration multiplicities, and the declared audit-equality key. It must not inspect outcomes, fit models, scores, convergence, separation, or any other outcome-dependent quantity.

The report must include:
1. per-cell (n_c), distinct concentration multiplicities, and exact (|\Omega_c|);
2. exact or bounded (|\Omega|), with arbitrary-precision integer arithmetic;
3. the audit-key components that can vary under assignments and the reason each component is invariant or assignment-sensitive;
4. an exact count of (|\Omega_{adm}|) only if it can be obtained by design-only combinatorial enumeration within the declared cap; otherwise a mathematically justified bound or a clearly labelled unknown;
5. the implied expected proposal count (9,999 divided by a) only when a is known, plus a conservative cap-attainment assessment;
6. a predeclared feasibility decision: exact enumeration, Monte Carlo potentially feasible, or computationally infeasible/unresolved.

Do not substitute an estimated acceptance rate based on outcome-dependent trial runs. Do not run a pilot sampler against the project bank. If the audit-key selectivity cannot be bounded adequately without inspecting or reusing protected project data, mark the feasibility assessment unresolved and stop. The 10^8 cap is binding; no relaxation is permitted.

**Current status:** not assessed. The required exact design inventory and approved bank-use scope have not been supplied by this design-only step. No acceptance-rate number is claimed.

## 7. Determinism, parallelism and evaluation accounting

For the first implementation, use single-process, deterministic execution. Parallel fitting or parallel random streams are not introduced until a separate reproducibility audit establishes that worker scheduling cannot alter stream assignment or reduction order.

Canonical ordering is required for cells, parents, versions, records, design columns, rational concentrations, enumerated assignments and report rows. Floating-point reductions use a fixed order. Any platform-dependent numerical difference that changes convergence, trigger status, admissibility, availability or a reported decision is a reproducibility failure requiring investigation before results are interpreted.

Per dataset, count:
- one observed pipeline evaluation, computed once;
- exact branch: |Ω_adm| total assignment evaluations, with the observed evaluation reused and not repeated;
- Monte Carlo branch: 1 + 9,999 comparison-set members, with the observed evaluation reused and not repeated;
- per assignment: two model fits per LOPO fold, plus both Firth refits on folds where the trigger fires.

The implementation must reconcile these counts against the v1.7 §8(iii) formula and the binding v1.7 acceptance-record note before any run.

## 8. Software validation required before execution GO

Validation must use synthetic fixtures authored solely for software testing, not the LC518 bank or real solver outcomes. No statistical power, null calibration, simulation study or numerical probability evaluation is part of this validation phase.

Required tests:
1. contrast basis: full column rank and sum-to-zero record effects;
2. design matrix: deterministic row/column ordering and correct fold separation;
3. exact rational concentration: reduced fractions, equality, multiplicities and distinct arrangements;
4. enumerator: exact unique arrangement count and deterministic order on hand-checkable fixtures;
5. sampler: Fisher–Yates implementation and uniformity proof at the algorithm level; any empirical frequency experiment is deferred until a separate execution GO;
6. audit key: exact equality, all scored and excluded fold-cell decisions, and no outcome/fit/score fields;
7. likelihood: stable probability/log-likelihood/score calculations on hand-computable fixtures;
8. Firth: analytic adjusted score against an independently differentiated objective on fixed software fixtures;
9. Cholesky: SPD success, singular/non-SPD failure, log-determinant identity and triangular-solve correctness;
10. optimizer: convergence, step-halving, iteration-limit and deterministic failure behavior on fixed fixtures;
11. assignment accounting: observed statistic reused exactly once; no duplicate observed fit;
12. availability: any unresolved fit failure invalidates the applicable test; no silent filtering or replacement;
13. RNG: deterministic regeneration from the root seed and stable stream identifiers;
14. cap: synthetic acceptance-rate fixtures verify stop-at-cap behavior without touching project data.

The test suite, expected outputs, tolerances, software versions and hashes must be frozen before any project-data evaluation. Passing software tests demonstrates implementation consistency, not scientific validity, exchangeability, consent, bank integrity or predictive evidence.

## 9. Unresolved decisions and blockers

| Item | Current disposition | Required closure |
|---|---|---|
| Numerical stack and pinned versions | Open; no root dependency manifest found | Inspect the intended isolated environment; pin Python, NumPy, SciPy and linked LAPACK before software validation |
| IRLS and Firth update details | Proposed above; not independently validated | Independent mathematical/code review of adjusted-score implementation and deterministic line search |
| Linear algebra | Candidate LAPACK Cholesky / DPOTRF | Pin actual implementation and record binary64/platform details |
| PRNG | Candidate PCG64DXSM + SeedSequence | Pin NumPy version and verify stream mapping; no project sampling |
| Exact rational encoding | Proposed and required for combinatorics | Review canonical serialization and equality implementation |
| Audit-key feasibility | Not assessed | Requires approved design inventory; no bank reuse or outcome access in this phase |
| 10^8 cap feasibility | Unknown | Derive design-only bound or mark Monte Carlo unavailable |
| Consent provenance | Open | Must be resolved separately; computational readiness does not cure it |
| Parent-population uncertainty | Not provided by v1.7 | No parent-population claim; any change requires a new statistical plan |
| Execution authorization | Not granted | Separate explicit GO after computational plan, software validation, isolation and data-access scope are accepted |

## 10. Phase gate

This v0.1 document is a proposal for review, not a final implementation contract. The next review must challenge, at minimum:
- whether the reduced Helmert parameterization exactly preserves the v1.7 coefficient interpretation and gradient criterion;
- whether the proposed adjusted-score/Fisher-scoring method plus deterministic step halving is a complete implementation of the stated Jeffreys objective;
- whether the 50-halving rule and zero initialization are acceptable deterministic implementation choices;
- whether PCG64DXSM and the proposed stream hierarchy satisfy the required independent-uniform sampling model;
- whether the exact-enumeration and Monte Carlo accounting correctly reuses (T(b_{obs})) once;
- whether any proposed feasibility calculation would improperly reuse the exposed bank or inspect outcomes.

No item in this document is approved merely by appearing here. No code is implemented against project data, no project-data feasibility computation is performed, and no execution is authorized.

---

**End of B1 computational implementation plan v0.1 — design draft only.**
