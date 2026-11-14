# B1 computational implementation plan — v0.3 design draft

**Date:** 2026-11-14  
**Status:** DESIGN DRAFT — NOT ACCEPTED, NOT FROZEN, NOT AN EXECUTION GO  
**Branch:** `gpt/b1-computational-plan-2026-11-14`  
**Binding statistical predecessor:** B1 analysis plan v1.7, accepted and frozen by the separate GPT acceptance record dated 2026-11-14.  
**Purpose:** specify the deterministic numerical implementation and the design-only feasibility checks required before any future execution GO. This document does not amend v1.7's estimand, null, target population, test, thresholds, or failure rules. v0.1 and v0.2 are retained unchanged. v0.1 blob: `9379af0059c59a9910e5b42ced7814276029ad99` (commit `99fc5aeb47cdad2691c533c67123c47e7e060982`). v0.2 blob: `7e7954d613a08e77dbfeabe400ac34b2d859431c` (commit `6ed0e59034c9c4c6e7841b911f8c0919b0e423ac`).

## Revision log v0.1 → v0.2

Claude's independent review of v0.1 identified four blocking implementation ambiguities and four required corrections. GPT's v0.2 dispositions are:

| # | Finding | Disposition in v0.2 |
|---|---|---|
| 1 | The componentwise convergence criterion was applied in Helmert coordinates, although v1.7 defines it on the constrained coefficient vector. The scaled sup-norm is not invariant to a change of coordinates. | The operational criterion is now evaluated in the original constrained coefficient representation: alpha components unchanged; the record-effect gradient is projected onto the sum-zero subspace by P = H H-transpose; denominators use the original omega coefficients; beta uses its original component. The reduced-coordinate gradient is mapped back by H. |
| 2 | The Firth section did not state which score drives the Fisher-scoring direction. | The expected information is I = X-transpose W X. The ordinary direction uses the ordinary score; the Firth direction uses the full Jeffreys-penalized adjusted score U-star. The adjusted-score formula and log-determinant derivative identity are given explicitly. |
| 3 | Objective non-decrease is not a sufficient deterministic line-search rule near convergence. | Both objectives use an Armijo sufficient-increase condition with c = 10^-4. Convergence is checked before attempting a line search. The candidate step sequence and failure rule are explicit. |
| 4 | The mapping from ordinary fit errors to the v1.7 separation trigger versus test unavailability was not defined. | A branch-specific outcome table distinguishes enriched-fit nonconvergence (trigger i, joint Firth refit), a valid beta/SE threshold (trigger ii/iii, joint Firth refit), an unevaluable SE after apparent convergence (unavailable, no invented trigger), ordinary baseline failure without an enriched trigger (unavailable), and any unresolved Firth failure (unavailable). |
| 5 | The rejection-sampling cap did not explicitly rule out a partial Monte Carlo reference. | Reaching 10^8 design checks before 9,999 accepted assignments makes the run unavailable. No partial reference, reduced sample size, or substitute is permitted. |
| 6 | RNG stream allocation offered alternatives rather than one deterministic schedule. | A single proposal stream is used per dataset; cells and versions are traversed in canonical order. N4-a data-generation and permutation streams are separate children in a fixed lambda-major, replication-minor order. |
| 7 | The Wald standard error was not fully defined. | It is computed from the inverse expected information at the final accepted ordinary enriched fit, using triangular solves. The beta variance component is invariant to the orthonormal nuisance-coordinate change. |
| 8 | The design-matrix rank check did not state why the concentration column is independent of baseline terms. | The plan now checks the full-rank baseline structure and the exact within-cell concentration variation. Under the complete 78-record crossing, positive within-cell variation makes the C_D column independent of cell indicators and record contrasts; a failed structural/rank check causes unavailability, never row or cell removal. |

## Revision log v0.2 → v0.3

Claude's independent review of v0.2 confirmed the Helmert construction, constrained-gradient mapping, Firth adjusted score and direction, full-rank argument, failure table, stream hierarchy, and uniform-proposal construction. It identified a numerical-stability concern in the absolute-objective Armijo comparison and requested several clarifications. GPT's dispositions are:

| # | Finding | Disposition in v0.3 |
|---|---|---|
| 1 | Near convergence, comparing two large absolute log-likelihood values can lose the small Armijo increase to floating-point rounding. | Armijo is now evaluated from a directly computed objective increment, not by subtracting two large objective totals. The logistic log-likelihood increment uses rowwise log1p/expm1 identities near zero and logaddexp identities outside that range, followed by fixed-order compensated summation. The Firth log-determinant increment is computed from the old and candidate Cholesky diagonals using log1p ratios. No epsilon is subtracted from the Armijo bound and no weaker acceptance inequality is introduced. |
| 2 | A numerical line-search stall needs an explicit outcome and route. | A line-search stall is recorded as a distinct diagnostic failure reason, not a new statistical outcome that overrides v1.7. If it occurs in the enriched ordinary fit, the fit is nonconverged and trigger (i) requires the joint Firth refit. If it occurs in either Firth refit, the applicable test is unavailable. If it occurs in the baseline ordinary fit without an enriched trigger, the test is unavailable. It is never silently relabelled as convergence. |
| 3 | The 50-halving limit was not justified. | The arbitrary limit is removed. Halving continues until a candidate is accepted, the step underflows to zero, or the candidate parameter vector is bitwise identical to the current vector. Under binary64, this is a finite sequence (at most 1,075 halvings from an initial step of 1). The representability stop is explicit and has the same line-search-stall routing in item 2. |
| 4 | The final expected-information factorization used for the Wald SE needs an exact iterate definition. | After enriched ordinary convergence, recompute and factorize expected information at the final accepted parameter vector. Use that one final-iterate Cholesky factorization for the Wald SE triangular solves. The factorization may fail: ordinary convergence checks the gradient before a new update factorization is needed, so the final-SE factorization is not guaranteed to have occurred already. The unavailable-SE row is therefore reachable and is retained. |
| 5 | The baseline-rank proof should state why a constant sum-zero record effect must vanish. | The proof now states explicitly that a vector in the sum-zero record subspace that is constant across all 78 records must be zero; full column rank of H then forces its coefficient vector to zero. |
| 6 | Near-optimum software tests are needed. | The validation gate now includes large-offset/small-increment likelihood fixtures, Firth log-determinant increment fixtures, near-optimum Armijo decisions, representability-stop cases, and the exact v1.7 failure routing for each stall location. |

**Binding v0.3 routing decision:** “numerical stall” is not an additional convergence state and does not create an escape from v1.7's trigger or availability rules. The v1.7 gradient threshold alone determines convergence. A failed line search means the fit did not reach that threshold by an accepted update; it is recorded as nonconvergence/fitting failure and routed according to the model and correction stage. The stable increment calculation is intended to prevent avoidable loss of precision; it cannot guarantee a representable improving step for every ill-conditioned dataset.

No change is made to v1.7's estimand, null, target population, fitting triggers, thresholds, test, availability rule, or execution boundary. v0.3 remains a design draft awaiting independent review.

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

Use the following fixed, full-column-rank orthonormal Helmert contrast matrix H with 78 rows and 77 columns, in canonical record identifier order. For column k = 1,...,77 (one-based), set H[r,k] = 1/sqrt(k(k+1)) for rows r = 1,...,k; set H[k+1,k] = -k/sqrt(k(k+1)); set all rows r > k+1 to zero. This fixes the column signs and order. The record-effect vector is omega = H eta. Thus H-transpose H is the 77-by-77 identity and H-transpose times the 78-vector of ones is zero. Consequently, the represented record effects satisfy sum_r omega_r = 0 exactly, without a redundant 78th coefficient.

The convergence test is not evaluated as a componentwise norm in eta coordinates. The operational definition in §3.1 maps the reduced-coordinate gradient back to the original 78-dimensional constrained omega representation. This distinction is necessary because a componentwise scaled sup-norm is not invariant under a change of basis.

Because H is orthonormal, the determinant of the information matrix on the constrained record-effect subspace is unchanged by expressing that subspace in Helmert coordinates. The beta_C component and its variance are also unchanged by this orthonormal re-expression of nuisance parameters.

### 2.2 Design matrices

For each LOPO fold, construct both models from the exact same training-row identifiers:
- baseline columns: one indicator per eligible exact cell and the 77 Helmert record contrasts;
- enriched columns: the baseline columns plus the raw C_D column.

The row order is a canonical sort by stable version identifier, then record identifier. The column order is fixed as cell indicators, record contrasts, then C_D. Test rows are never used to fit parameters. The scoring rows and fold membership are those frozen by the v1.7 design-only audit.

The baseline design is full column rank under the declared complete crossing. To see this, suppose a linear combination of the cell-indicator columns and the record-contrast columns is zero on every training row. Within any nonempty cell, the cell coefficient plus H gamma must equal zero for every record. Therefore H gamma is constant across the 78 records. But H gamma is in the sum-zero subspace, so a constant H gamma must be the zero vector. Since H has full column rank, gamma is zero; the cell coefficients must then also be zero. Thus neither the cell indicators nor the 77 record contrasts are aliased.

The enriched C_D column is independent of the baseline columns when the v1.7 within-cell variation gate holds. In each training cell c, let Cbar_c be the mean C_D over its training versions. Subtract Cbar_c from C_D(v) for every row belonging to version v in cell c. The resulting residual is orthogonal to the cell indicators by within-cell centring. It is orthogonal to every record-contrast column because each version contributes all 78 records and each Helmert contrast sums to zero over those records. Its squared norm is 78 times the sum, over training cells and versions, of (C_D(v) - Cbar_c)^2. This is positive exactly when there is within-cell C_D variation; v1.7 requires the corresponding W_C,c_train positivity for every scored training fold-cell. The exact reduced-rational C_D values determine each positivity decision.

These structural arguments, together with the exact W_C,c_train checks, are the rank decision. A floating-point numerical-rank tolerance must not independently override that exact structural decision. A numerical condition/rank diagnostic may be recorded for transparency, but it is diagnostic only; it is not a new exclusion rule. If the actual model information matrix cannot be factorized under the pinned linear-algebra routine, the fitting failure is handled under §3.3 and v1.7. The implementation must never respond by dropping rows, cells, columns, or records.

### 2.3 Exact representation of concentration

Store each concentration as its exact reduced rational pair (m,k), where m = max_j f_j and k = k_fail, alongside its displayed decimal representation. Equality, distinct-value counts, multiplicities and permutation enumeration use the reduced integer numerator/denominator pair, never rounded floating-point values. Conversion to IEEE-754 binary64 occurs only when building the numerical predictor column for model fitting.

This preserves exact permutation combinatorics and prevents two distinct rational concentrations from being merged by display rounding.

## 3. Optimisation algorithm

### 3.1 Ordinary maximum-likelihood fits and the v1.7 convergence criterion

Use deterministic Fisher-scoring / iteratively reweighted least squares (IRLS) for both models. Compute the linear predictor z = X gamma, probabilities with a numerically stable logistic function, and the log-likelihood as the sum over rows of y_i z_i minus logaddexp(0,z_i), avoiding direct evaluation of log(pi_i) or log(1-pi_i). For the current design matrix X, fitted probabilities pi, and diagonal weight matrix W with entries w_i = pi_i(1-pi_i), define the expected Fisher information I = X-transpose W X and the ordinary score U = X-transpose(y-pi). The ordinary Fisher-scoring direction d solves I d = U. No explicit matrix inverse is formed.

The v1.7 convergence threshold is 10^-8 and its componentwise scaling is retained. To operationalise it without making the decision depend on the arbitrary Helmert coordinate basis, evaluate it in the original constrained coefficient representation:
- alpha components: use the ordinary gradient component g_alpha,c and denominator max(1, abs(alpha_c));
- record effects: let g_eta be the gradient component in the 77 Helmert coordinates for the active objective. Map it back to the sum-zero tangent space as g_omega_tan = H g_eta, a 78-component vector. Use g_omega_tan componentwise, with denominator max(1, abs(omega_r)). Equivalently, for an objective with a chosen smooth ambient extension, this is the projection P g_omega with P = H H-transpose; the primary definition is H g_eta and does not require an unconstrained extension of the Firth log-determinant objective;
- enriched slope: use g_beta and denominator max(1, abs(beta_C)).

The fit is converged when the maximum of all applicable scaled component magnitudes is at most 10^-8. In reduced coordinates, the record-effect part of this tangent gradient is H times the eta-gradient. If another orthonormal basis H-prime = H Q is used, with Q orthogonal, the mapped tangent gradient is unchanged because H Q Q-transpose g_eta = H g_eta. Thus the 78-component convergence vector is independent of the arbitrary orthonormal basis choice. This is the declared operational interpretation of v1.7's constrained-parameter criterion; it does not use the non-invariant componentwise norm of the eta-gradient.

Check convergence at the initial point and immediately after each accepted update, before attempting another line search. If the criterion is met, terminate successfully. Otherwise, compute the Fisher-scoring direction. Initialization is the all-zero vector in the constrained parameterization. There is no random initialization, warm start, data-dependent alternative initialization, or parameter carry-over between folds or assignments.

Use the Armijo sufficient-increase rule for the ordinary log-likelihood, but evaluate the objective increment directly rather than subtracting two absolute log-likelihood totals. At the current iterate let z = X gamma, let t = alpha X d for a trial step, let pi_i = logistic(z_i), and let q_i = logistic(-z_i), with pi_i and q_i evaluated separately by a numerically stable logistic routine. The rowwise log-likelihood increment is:

- if y_i = 0: delta_i = -log1p(pi_i * expm1(t_i));
- if y_i = 1: delta_i = -log1p(q_i * expm1(-t_i)).

These identities are used when abs(t_i) <= 0.5. For abs(t_i) > 0.5, evaluate the algebraically equivalent forms without exponentiating a potentially large t_i:
- if y_i = 0: delta_i = -logaddexp(log(q_i), log(pi_i) + t_i);
- if y_i = 1: delta_i = -logaddexp(log(pi_i), log(q_i) - t_i).

Here log(pi_i) and log(q_i) are evaluated as -logaddexp(0, -z_i) and -logaddexp(0, z_i), respectively. Sum the rowwise increments in the canonical row order using fixed-order compensated summation (Python math.fsum, with the Python version pinned before GO). This gives delta_ell = ell(gamma + alpha d) - ell(gamma) without subtracting two large, nearly equal absolute log-likelihood totals.

Compute U-transpose d with the same fixed-order compensated summation in canonical parameter order. Require it to be finite and strictly positive, and require:

delta_ell >= 10^-4 * alpha * (U-transpose d).

Do not subtract an estimated epsilon/noise floor from the right-hand side and do not accept a weaker inequality. If the direct objective increment and positive Armijo bound are not numerically distinguishable because one or both underflow to zero, record an Armijo line-search stall; do not call it convergence.

Try alpha = 1 first and halve successively. There is no arbitrary fixed 50-halving limit. After each halving, form the candidate parameter vector in binary64. Stop the search if alpha underflows to zero or if every candidate parameter is bitwise identical to the current parameter vector; reducing alpha further cannot produce a representable update. Otherwise evaluate the candidate and accept the first satisfying the direct-increment Armijo inequality and all finite-value checks. A line-search stall is a fitting failure/nonconvergence, routed by §3.3. No objective-decrease-only acceptance rule is used.

The fit may take at most 200 accepted updates. After the 200th update, evaluate the convergence criterion once more; if it is not met, the fit is nonconverged. Any non-finite objective, score, information matrix, or update, or an information factorization failure needed to compute an update, is a numerical fitting failure. The enriched-fit and baseline-fit consequences are specified in §3.3.

### 3.2 Firth / Jeffreys-penalized refits

When the v1.7 enriched-model trigger fires, refit both models using the exact objective:
F(gamma) = ell(gamma) + 0.5 log det I(gamma),
where I(gamma) is the expected Fisher information X-transpose W X in the same constrained parameterization and W has entries pi_i(1-pi_i). Do not substitute the observed Hessian for expected information.

For the current design matrix X, define the leverage h_i = w_i times x_i-transpose I-inverse x_i. Compute it without forming I-inverse: if I = L L-transpose is the Cholesky factorization, solve L q_i = x_i and set h_i = w_i times q_i-transpose q_i. The Firth adjusted score, which is the gradient of the full penalized objective, is:
U_star = X-transpose [ y - pi + h elementwise-multiplied by (1/2 - pi) ].

The derivative identity underlying this score is:
partial [0.5 log det I] / partial gamma_j = 0.5 trace( I-inverse times partial I / partial gamma_j ).

The Fisher-scoring direction for the Firth objective must use the full penalized gradient U_star, not the ordinary score U. Solve I d = U_star. If I is positive definite, then U_star-transpose d = U_star-transpose I-inverse U_star is strictly positive whenever U_star is nonzero; this is the ascent direction for the penalized objective. The implementation must verify this positivity numerically at every non-converged iterate.

Apply Armijo to the penalized objective using a directly evaluated increment:

delta_F = delta_ell + 0.5 * delta_logdet_I,

where delta_ell is computed by the stable rowwise method in §3.1. Let L be the Cholesky factor of the current expected information and L_new the Cholesky factor at a positive-definite trial point. Since logdet(I) = 2 times the sum of log diagonal entries of L, compute the log-determinant increment as:

delta_logdet_I = 2 * sum_j r_j, where d_j = L_new[j,j] - L[j,j], r_j = log1p(d_j / L[j,j]) when abs(d_j) <= 0.5 * L[j,j], and r_j = log(L_new[j,j]) - log(L[j,j]) otherwise.

Use fixed-order compensated summation for the diagonal terms and for the combined delta_F. This avoids subtracting two large absolute log determinants. Compute U_star-transpose d with fixed-order compensated summation. Require a finite, strictly positive directional derivative and:

delta_F >= 10^-4 * alpha * (U_star-transpose d).

Use the same unbounded-by-arbitrary-cap halving schedule as §3.1: begin at alpha = 1 and halve until a candidate is accepted, alpha underflows to zero, or the candidate parameter vector is bitwise identical to the current vector. A trial candidate whose information cannot be factorized or whose log determinant is non-finite is rejected, and a shorter representable candidate may be tried. If no candidate satisfies the direct-increment Armijo inequality, record a line-search stall. Check the convergence criterion before each line search. The criterion uses the gradient of the active penalized objective, mapped to the original constrained omega representation as specified in §3.1. At every accepted iterate, the expected information must be useably positive definite and its log determinant finite.

Every accepted Firth iterate must have finite objective, useably positive-definite expected information and finite log determinant. If any of these conditions fails at an accepted iterate, the Firth fit fails immediately. This does not authorize jitter, pseudo-inverse, ridge fallback, alternate optimizer, or silent model simplification.

The implementation must independently verify the adjusted-score formula against the analytic derivative of the stated penalized objective and against a finite-difference gradient on fixed software fixtures. The fixture set, finite-difference scheme, tolerance and expected outputs must be frozen before any execution GO. This is software validation, not project-data analysis.

### 3.3 Standard error, separation trigger, and failure routing

The enriched ordinary model is fitted first. If it does not converge, trigger (i) in v1.7 fires and both models are refitted using the Firth objective. For this computational plan, enriched ordinary nonconvergence includes:
- reaching 200 accepted updates without satisfying the convergence criterion;
- failure to obtain a finite, strictly positive numerically representable Fisher directional derivative;
- an Armijo line-search stall: no candidate satisfies the direct-increment inequality, the direct comparison becomes unresolved through underflow, or alpha underflows to zero or the candidate vector becomes identical to the current vector;
- non-finite objective, score, information or parameter values before convergence;
- Cholesky failure when factorization is required to compute an ordinary enriched-model update.

If the enriched ordinary fit converges with finite parameters, first check whether abs(beta_C) > 50. If so, trigger (ii) fires and both models are refitted with Firth. Otherwise, at the final accepted ordinary enriched-model parameter vector, recompute the expected information from that vector's fitted probabilities and weights and factorize this final-iterate matrix once. Use this same final-iterate Cholesky factorization for the Wald standard error:
SE(beta_C) = square root of e_beta-transpose I-inverse e_beta,
where e_beta selects the beta_C coordinate in the enriched parameter vector. Compute the selected inverse-information quadratic form by triangular solves; do not explicitly form I-inverse. Do not reuse an information factorization from the preceding iterate. The orthonormal Helmert transformation affects only nuisance coordinates and leaves this beta_C variance unchanged. If the final-iterate factorization fails or the resulting SE is non-finite, the SE trigger cannot be evaluated and the fold/test is unavailable; this is not re-labelled as SE > 10^3. If the finite SE exceeds 10^3, trigger (iii) fires and both models are refitted with Firth.

If the final-iterate information factorization or Wald SE is unavailable, this is not re-labelled as an SE exceeding 10^3 and does not create a new Firth trigger: the fold/test is unavailable under v1.7's no-silent-fallback rule.

If none of the three enriched-model triggers fires, fit the baseline ordinary model. Any unresolved baseline ordinary fitting failure makes the applicable test unavailable. Baseline failure alone does not create a new Firth trigger. If an enriched-model trigger has already fired, fit both models with Firth and do not run an unnecessary baseline ordinary fit first.

| Ordinary-fit outcome | Required action |
|---|---|
| Enriched ordinary fit does not converge, including an Armijo line-search stall or a representability-limited stall | Trigger (i); jointly Firth-refit baseline and enriched models |
| Enriched ordinary fit converges and abs(beta_C) > 50 | Trigger (ii); jointly Firth-refit both models |
| Enriched ordinary fit converges, abs(beta_C) <= 50, final-iterate expected information is factorable, and Wald SE > 10^3 | Trigger (iii); jointly Firth-refit both models |
| Enriched ordinary fit converges but the separately computed final-iterate information cannot be factorized for SE, or SE is non-finite | Unavailable; do not invent an SE threshold or an extra trigger |
| Enriched ordinary fit converges with abs(beta_C) <= 50 and finite Wald SE <= 10^3; baseline ordinary fit succeeds | Use the ordinary fits; no Firth refit |
| No enriched trigger fires but baseline ordinary fitting fails, including an Armijo line-search stall | Unavailable; no baseline-only trigger exists |
| Either Firth refit fails to converge, including an Armijo line-search stall, or violates the declared information-matrix rules | Unavailable under v1.7 V5(b); no assignment is discarded or replaced |

For every fold, record the enriched ordinary-fit status, all triggers that could be evaluated, whether the baseline ordinary fit was attempted, whether the Firth pair was attempted, both final model statuses, and the reason for any unavailability. Also record accepted updates, backtracking halvings and the Armijo termination reason, including precision/representability stalls. If abs(beta_C) > 50 already triggers Firth, a Wald SE is not needed to establish the trigger and may be marked not evaluated. The v1.7 rule is otherwise unchanged.

## 4. Linear algebra

**Candidate routine:** IEEE-754 binary64 arithmetic with the LAPACK symmetric positive-definite Cholesky factorization, lower-triangular form (DPOTRF), through the numerical-library interface fixed in the environment lock.

- Solve systems by forward/back substitution using the Cholesky factor. Never form the information-matrix inverse.
- Compute log det I as twice the sum of the natural logarithms of the Cholesky diagonal entries.
- A non-positive-definite matrix, factorization error, non-finite factor, or non-finite log determinant at an accepted Firth iterate is a hard fitting failure under v1.7.
- No diagonal perturbation, eigenvalue clipping, pseudo-determinant, generalized inverse, or fallback factorization is permitted.
- Record the library name/version, linked LAPACK implementation, binary64 platform details, factorization status and any reported numerical error code.

The exact numerical-library version and platform build are not frozen in v0.2 because no root-level pyproject.toml, requirements.txt, environment.yml or setup.cfg was found at the inspected review-branch root. The implementation environment must first be inventoried and then pinned in a lock artifact before software validation. No dependency is to be installed into the user's working environment as part of this design step.

## 5. Random-number generation and assignment sampling

### 5.1 Generator and fixed stream hierarchy

Candidate generator: NumPy PCG64DXSM, initialized from the v1.7 root seed 20261114 through NumPy SeedSequence. The generator is instantiated explicitly as Generator(PCG64DXSM(child_seed_sequence)); do not use default_rng or rely on its default bit generator. The exact NumPy version and bit-generator implementation must be pinned before software validation. NumPy documents PCG64DXSM as an upgraded PCG64 generator and documents SeedSequence spawning as producing independent and very probably non-overlapping initial states; this is an engineering stream-construction guarantee, not a proof of mathematical independence. References: https://numpy.org/doc/stable/reference/random/bit_generators/ and https://numpy.org/doc/stable/reference/random/parallel.html. The inferential guarantee remains the v1.7 guarantee with respect to the ideal independent-uniform sampling model, not conditional on a deterministic seed.

Use exactly one proposal stream per dataset. Do not create per-cell streams and do not offer alternative stream-allocation schemes. Within each dataset, visit eligible cells in lexicographic order of the exact cell key (q, Z, k, ell), and versions within a cell in ascending stable version-identifier order. Use the dataset's single proposal stream sequentially for the within-cell Fisher-Yates shuffles. Every proposal consumes the stream in this canonical traversal order.

For N4-a, establish the fixed task order as lambda-major then replication-minor: lambda values 0.5, 1.0, 2.0; within each lambda, replication indices 1 through 100. Construct root SeedSequence(20261114), spawn two children in this fixed order: real-data assignment stream, N4-a task master. From the N4-a task master, spawn exactly 300 dataset children in the task order above. Each dataset child spawns exactly two children: first the data-generation stream, second the assignment-proposal stream. The real-data child is used only for the real-data assignment-proposal stream. No stream is reused; worker order or run order must not alter the mapping. Execution remains single-process in the first implementation.

### 5.2 Uniform proposals on Omega

For each cell, use an unbiased Fisher-Yates shuffle of its version positions. At current upper index i, draw j using Generator.integers(low=0, high=i+1), whose half-open range is exactly the integers 0 through i, then swap positions i and j. Assign the observed multiset of reduced-rational C_D values to the shuffled positions. Each distinct arrangement has the same number of raw permutations, so a uniform position shuffle induces the uniform proposal over that cell's distinct arrangements. Canonical cell traversal with one dataset stream yields the product-uniform proposal over Omega under the stated sampling model.

For every proposal, compute the complete audit-equality key and accept if and only if it exactly equals the observed key. Rejected proposals consume one design check and no model fit. Continue until 9,999 accepted assignments or the hard 10^8 design-check cap is reached.

**Binding cap outcome:** if the 10^8th design check is reached before 9,999 assignments have been accepted, declare the Monte Carlo test run unavailable under v1.7 V5(c). Do not compute a p-value from a partial sample. Do not lower the accepted-assignment target, relax the cap, substitute an approximate reference, or replace any failed assignment.

### 5.3 Independent accepted draws and accounting

Each proposal uses fresh generator output. Sampling is with replacement: repeated accepted assignments are allowed and counted as separate Monte Carlo draws, as required by v1.7. Record:
- total proposals/design checks;
- accepted and rejected counts;
- acceptance rate;
- accepted assignment identifiers and canonical hashes;
- repeated-assignment count;
- stream identifiers, generator state metadata and sufficient draw accounting to regenerate the sequence.

The observed statistic is evaluated once before the sampled comparison set and reused once. The 9,999 accepted assignments are additional evaluations; no observed assignment is added a second time by the sampler.

### 5.4 Exact enumeration

When |Omega| <= 10^6, enumerate each distinct multiset arrangement exactly once in deterministic lexicographic order of reduced rational concentration values and canonical version identifiers. Apply the audit-equality key before fitting. The observed assignment is included exactly once; reuse its already-computed T(b_obs), rather than fitting it again. Exact p-value denominators are |Omega_adm|, with no +1.

The enumerator must be checked on small, hand-constructed fixtures where cell multiplicities are known. These are software unit tests and must not use the project bank.

## 6. Design-only feasibility of the 10^8 cap

The rejection-sampling acceptance probability is a = |Omega_adm| / |Omega|. A design-only feasibility assessment must be completed before any Monte Carlo sampling. It must use only the frozen design structure, rational concentration multiplicities, and the declared audit-equality key. It must not inspect outcomes, fit models, scores, convergence, separation, or any other outcome-dependent quantity.

The report must include:
1. per-cell n_c, distinct concentration multiplicities, and exact |Omega_c|;
2. exact or bounded |Omega|, with arbitrary-precision integer arithmetic;
3. the audit-key components that can vary under assignments and the reason each component is invariant or assignment-sensitive;
4. an exact count of |Omega_adm| only if it can be obtained by design-only combinatorial enumeration within the declared cap; otherwise a mathematically justified bound or a clearly labelled unknown;
5. the implied expected proposal count 9,999/a only when a is known, plus a conservative cap-attainment assessment;
6. a predeclared feasibility decision: exact enumeration, Monte Carlo potentially feasible, or computationally infeasible/unresolved.

Do not substitute an estimated acceptance rate based on outcome-dependent trial runs. Do not run a pilot sampler against the project bank. If the audit-key selectivity cannot be bounded adequately without inspecting or reusing protected project data, mark the feasibility assessment unresolved and stop. The 10^8 cap is binding; no relaxation is permitted. If the cap cannot be demonstrated feasible by design-only analysis, mark the Monte Carlo branch unresolved or unavailable; no outcome-dependent pilot may be used to rescue it.

**Current status:** not assessed. The required exact design inventory and approved bank-use scope have not been supplied by this design-only step. No acceptance-rate number is claimed.

## 7. Determinism, parallelism and evaluation accounting

For the first implementation, use single-process, deterministic execution. Parallel fitting or parallel random streams are not introduced until a separate reproducibility audit establishes that worker scheduling cannot alter stream assignment or reduction order.

Canonical ordering is required for cells, parents, versions, records, design columns, rational concentrations, enumerated assignments and report rows. Floating-point reductions use a fixed order. Any platform-dependent numerical difference that changes convergence, trigger status, admissibility, availability or a reported decision is a reproducibility failure requiring investigation before results are interpreted.

Per dataset, count:
- one observed pipeline evaluation, computed once;
- exact branch: |Omega_adm| total assignment evaluations, with the observed evaluation reused and not repeated;
- Monte Carlo branch: 1 + 9,999 comparison-set members, with the observed evaluation reused and not repeated;
- per assignment: two model fits per LOPO fold, plus both Firth refits on folds where the trigger fires.

The implementation must reconcile these counts against v1.7 §8(iii) and the binding v1.7 acceptance-record note before any run. Report, per evaluated assignment, the enriched ordinary-fit outcome, trigger status, baseline ordinary-fit status when applicable, Firth-refit status, accepted updates, line-search halvings, Armijo termination reason (including precision/representability stall), and final availability classification. This allows the v1.7 evaluated-assignment accounting to be audited without using fit status to filter assignments.

## 8. Software validation required before execution GO

Validation must use synthetic fixtures authored solely for software testing, not the LC518 bank or real solver outcomes. No statistical power, null calibration, simulation study or numerical probability evaluation is part of this validation phase.

Required tests:
1. contrast basis: full column rank, H-transpose H equals identity, and sum-to-zero record effects; projected-gradient criterion invariance across orthonormal bases spanning the same sum-zero subspace;
2. design matrix: deterministic row/column ordering and correct fold separation;
3. exact rational concentration: reduced fractions, equality, multiplicities and distinct arrangements;
4. enumerator: exact unique arrangement count and deterministic order on hand-checkable fixtures;
5. sampler: Fisher–Yates implementation and uniformity proof at the algorithm level; any empirical frequency experiment is deferred until a separate execution GO;
6. audit key: exact equality, all scored and excluded fold-cell decisions, and no outcome/fit/score fields;
7. likelihood increments: verify the rowwise log1p/expm1 and logaddexp identities against high-precision references on hand-computable fixtures; include large absolute log-likelihoods with tiny trial increments and confirm no subtraction of large objective totals;
8. Firth: adjusted-score formula, expected-information identity, analytic adjusted score against an independently differentiated objective and finite-difference gradient on fixed software fixtures; verify that the Fisher direction uses U-star and has positive penalized directional derivative;
9. Firth objective increment: verify the Cholesky-diagonal log-determinant increment against a high-precision log-determinant difference on fixed software fixtures;
10. Cholesky: SPD success, singular/non-SPD failure, log-determinant identity and triangular-solve correctness;
11. optimizer: convergence, direct-increment Armijo sufficient-increase, initial-point convergence check, dynamic halving and binary64 representability stop, iteration-limit and deterministic failure-routing behavior on fixed fixtures; include near-optimum cases whose absolute objective is large but whose predicted increment is small;
12. stall routing: an enriched ordinary stall triggers joint Firth; a Firth stall makes the test unavailable; a baseline-only ordinary stall makes the test unavailable; none is called convergence;
13. assignment accounting: observed statistic reused exactly once; no duplicate observed fit;
14. availability: any unresolved fit failure invalidates the applicable test; no silent filtering or replacement;
15. RNG: deterministic regeneration from the root seed and stable stream identifiers;
16. cap: synthetic acceptance-rate fixtures verify stop-at-cap behavior and unavailable-on-partial-sample rule without touching project data;
17. failure routing: enriched ordinary nonconvergence triggers joint Firth; converged-fit unavailable SE does not invent a trigger; baseline-only ordinary failure is unavailable; any unresolved Firth failure is unavailable;
18. rank: full baseline rank and C_D independence from all baseline columns under the complete 78-record crossing; verify the algebraic proof and exact W_C,c gate, and confirm that no floating-point rank tolerance silently changes eligibility.

The test suite, expected outputs, tolerances, software versions and hashes must be frozen before any project-data evaluation. Passing software tests demonstrates implementation consistency, not scientific validity, exchangeability, consent, bank integrity or predictive evidence.

## 9. Unresolved decisions and blockers

| Item | Current disposition | Required closure |
|---|---|---|
| Numerical stack and pinned versions | Open; no root dependency manifest found | Inspect the intended isolated environment; pin Python, NumPy, SciPy and linked LAPACK before software validation |
| IRLS and Firth update details | Proposed above; not independently validated | Independent mathematical/code review of adjusted-score implementation, direct objective-increment evaluation and deterministic line search |
| Linear algebra and objective-increment arithmetic | Candidate LAPACK Cholesky / DPOTRF; fixed-order compensated summation via Python math.fsum; binary64 halving/representability stop | Pin Python, NumPy, SciPy, linked LAPACK, binary64 platform details and summation implementation before software validation |
| PRNG | Candidate PCG64DXSM + SeedSequence | Pin NumPy version and verify stream mapping; no project sampling |
| Exact rational encoding | Proposed and required for combinatorics | Review canonical serialization and equality implementation |
| Audit-key feasibility | Not assessed | Requires approved design inventory; no bank reuse or outcome access in this phase |
| 10^8 cap feasibility | Unknown | Derive design-only bound or mark Monte Carlo unavailable |
| Consent provenance | Open | Must be resolved separately; computational readiness does not cure it |
| Parent-population uncertainty | Not provided by v1.7 | No parent-population claim; any change requires a new statistical plan |
| Execution authorization | Not granted | Separate explicit GO after computational plan, software validation, isolation and data-access scope are accepted |

## 10. Phase gate

This v0.3 document is a proposal for review, not a final implementation contract. The next review must challenge, at minimum:
- whether the orthonormal Helmert parameterization and projected original-coordinate gradient criterion are a faithful operationalization of v1.7's constrained componentwise gradient rule;
- whether the explicit Firth adjusted score, expected-information Fisher direction, Armijo sufficient-increase rule and derivative identity implement the stated Jeffreys objective correctly;
- whether the direct-increment Armijo evaluator is algebraically correct and numerically stable, including the Firth Cholesky-diagonal log-determinant increment, and whether the representability-based stopping rule is deterministic and adequate;
- whether PCG64DXSM and the fixed SeedSequence stream hierarchy adequately implement the independent-uniform sampling model, with the limits of pseudorandom independence stated honestly;
- whether a line-search stall has been routed consistently with v1.7 in all three positions (enriched ordinary, baseline ordinary, Firth refit);
- whether the final-iterate information factorization for the Wald SE is specified without reusing a preceding-iterate factorization;
- whether the exact structural-rank argument, rather than an unspecified floating-point rank tolerance, is the appropriate design gate;
- whether the exact-enumeration and Monte Carlo accounting correctly reuses (T(b_{obs})) once;
- whether any proposed feasibility calculation would improperly reuse the exposed bank or inspect outcomes.

No item in this document is approved merely by appearing here. No code is implemented against project data, no project-data feasibility computation is performed, and no execution is authorized.

---

**End of B1 computational implementation plan v0.3 — design draft only.**
