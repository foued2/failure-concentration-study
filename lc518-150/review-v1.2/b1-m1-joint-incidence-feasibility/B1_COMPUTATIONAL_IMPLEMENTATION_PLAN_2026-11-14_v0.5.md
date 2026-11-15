# B1 computational implementation plan — v0.5 design draft

**Date:** 2026-11-15  
**Status:** DESIGN DRAFT — NOT ACCEPTED, NOT FROZEN, NOT AN EXECUTION GO  
**Branch:** `gpt/b1-computational-plan-2026-11-14`  
**Binding statistical predecessor:** B1 analysis plan v1.7, accepted and frozen by the separate GPT acceptance record dated 2026-11-14.  
**Purpose:** specify the deterministic numerical implementation and the design-only feasibility checks required before any future execution GO. This document does not amend v1.7's estimand, null, target population, test, thresholds, or failure rules. v0.1 through v0.4 are retained unchanged. v0.4 blob: `4fbfb217b4adfac68a958e4f051ecd4b7f914f05` (commit `d18966f98becc3f9149ea5bfd662b8d5d38312de`). v0.3 blob: `de29d014840f6552c2193901cc728474337af05e` (commit `265dc3cef9f5825e3c4da86e6442ba7639dd554e`). v0.1 blob: `9379af0059c59a9910e5b42ced7814276029ad99` (commit `99fc5aeb47cdad2691c533c67123c47e7e060982`). v0.2 blob: `7e7954d613a08e77dbfeabe400ac34b2d859431c` (commit `6ed0e59034c9c4c6e7841b911f8c0919b0e423ac`).

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

## Revision log v0.3 → v0.4

Claude's independent review verified the v0.3 scalar likelihood-increment identities and the 1,075-halving binary64 bound. It identified (a) a mismatch between the ideal line-search point and the rounded parameter vector actually stored and (b) a remaining finite-precision resolution problem, including conditioning in the Firth determinant increment. GPT's dispositions are:

| # | Finding | Disposition in v0.4 |
|---|---|---|
| 1 | v0.3 evaluated the ideal displacement alpha*d but stored round_binary64(gamma + alpha*d), so the Armijo test could certify a different point. | The candidate is now generated first in binary64. Its actual stored displacement is defined as the exact real difference between the two stored binary64 vectors, represented as dyadic Arb inputs. Both the objective increment and directional derivative use this same displacement. |
| 2 | Direct binary64 row increments still accumulate rounding error that grows with row count and can dominate a small Armijo margin. | GPT rejects reducing the Armijo constant. Armijo acceptance is instead certified with Arb ball arithmetic at a deterministic precision ladder of 128, 256, 512, 1024, 2048 and 4096 bits. A candidate is accepted only when the lower bound on its objective increment is at least the upper bound on the unchanged v1.7-compatible Armijo requirement. If the intervals do not resolve the inequality at 4096 bits, that candidate is not accepted; the search proceeds to the next smaller representable candidate. |
| 3 | The binary64 Cholesky-diagonal log-determinant increment has a condition-dependent rounding error. | The Cholesky-diagonal difference is removed from the Armijo certification path. The current and candidate expected-information determinants are enclosed using Arb's verified ball-matrix determinant, and their positive determinant enclosures are logged and differenced as balls. The resulting interval radius is the certified absolute error bound for that specific matrix pair; it incorporates the actual conditioning and arithmetic enclosure. A condition-number estimate is recorded as a diagnostic and used to stratify tests, never as a substitute for the enclosure. |
| 4 | The row-count-dependent resolution limit was not stated. | Each fit records N = 78 times its number of training versions, the Arb precision used, the objective-increment interval, the directional-derivative interval, the resulting Armijo margin interval and, for Firth, both log-determinant intervals and a condition-number diagnostic. Before validation or GO, the exact frozen design inventory must establish the maximum N across real-data folds and all N4-a datasets. There is no fabricated universal N cap: the interval radius measures the actual N-dependent accumulation, and an unresolvable comparison is a stall. No execution GO is possible until N_max is known and the synthetic validation grid covers it. |
| 5 | The Firth directional derivative must be certified with the same stored displacement. | The Firth gradient used for the Armijo directional derivative is evaluated with Arb enclosures, including a verified interval inverse of the current expected information for its leverage terms. The derivative is U_star-transpose s, not alpha times a binary64 direction score. |
| 6 | An orthonormal Helmert matrix represented by binary64 entries does not preserve the exact sum-to-zero identity when those entries are treated as exact dyadic inputs for Arb. | Replace the floating Helmert design columns with the exact integer reference-contrast matrix B: B[r,j]=1 when r=j≤77, B[78,j]=-1, otherwise 0. Then omega=B theta enforces sum_r omega_r=0 algebraically. The basis is non-orthonormal but full rank. Since det(B-transpose B)=78, its Firth log-determinant differs from an orthonormal basis by the parameter-independent constant log(78); the Jeffreys penalty shifts by 0.5 log(78), identically for baseline and enriched models, without changing gradients, fitted values or objective increments. The convergence gradient is mapped back by B(B-transpose B)^-1, which is basis-invariant. |
| 7 | The v0.4 update initially specified Arb-certified Armijo comparisons but left the 10^-8 convergence decision as an unqualified numerical gradient evaluation. | The active objective gradient and the componentwise scaled convergence statistic are now enclosed with Arb at the same precision ladder. A convergence PASS is allowed only when every upper bound is at most 10^-8. An unresolved component at 4096 bits is not a PASS and is recorded explicitly. This preserves v1.7's threshold and prevents rounding uncertainty from being treated as convergence. |

**Binding v0.4 decisions:** retain the Armijo constant c = 10^-4; do not subtract an epsilon or weaken the inequality; certify the actual stored candidate using interval lower/upper bounds; certify convergence at the unchanged v1.7 threshold 10^-8 by requiring every scaled-gradient upper bound to be at or below that threshold; and classify an interval comparison unresolved at maximum precision as an unaccepted candidate. If no candidate is certified before the representability stop, the line search stalls and retains the v1.7 routing already specified in v0.3. This is a numerical safeguard, not a change to the estimand, convergence threshold, separation trigger, availability rule, or inferential procedure.

No change is made to v1.7's estimand, null, target population, fitting triggers, thresholds, test, availability rule, or execution boundary. v0.4 remains a design draft awaiting independent review.

## Revision log v0.4 → v0.5

Claude's independent review of v0.4 confirmed the reference-contrast algebra, the \(0.5\log(78)\) determinant shift, the stored-candidate Armijo construction, the interval-certification logic and the binary64 representability bound. It identified one decisive mismatch: the fitting predictor was still rounded to binary64 before the Arb calculations, so the certified optimizer was certifying a different model from v1.7's exact-rational \(C_D\). Claude also required a corrected coordinate-gradient statement, a runtime/workload model, and stronger precision-escalation and singular-matrix fixtures. GPT's v0.5 dispositions are:

| # | Finding | Disposition in v0.5 |
|---|---|---|
| 1 | The v0.4 predictor column was converted from \(m/k\) to binary64 before all certified objective and derivative calculations. | The exact fitting design is now \(X_{\mathbb Q}\), with every \(C_D\) stored as a reduced multiprecision rational \(m/k\) and converted directly from its rational representation to an Arb enclosure. No binary64 conversion enters the objective, gradient, Firth information, convergence, Wald-SE or Armijo certificate. |
| 2 | A binary64 predictor may still be useful for a practical Fisher-scoring proposal. | A separate \(X_{64}\) may be constructed only to propose binary64 update directions. It is explicitly an approximation to \(X_{\mathbb Q}\), and it has no authority over the fitted objective, accepted-step decision, convergence, trigger or inferential calculation. Every proposed displacement is independently checked against the exact-rational model before it can be accepted. |
| 3 | The basis-change wording incorrectly suggested that reduced-coordinate gradient components are unchanged. | The coordinate law is now explicit: if \(B=HR\) and \(\eta=R\theta\), then \(g_\theta=R^Tg_\eta\) and \(d_\theta=R^{-1}d_\eta\). The mapped tangent gradient, fitted linear predictor, Fisher-scoring displacement, objective increment and decision are the invariant objects. The fixed \(0.5\log(78)\) shift does not alter the gradient within a fixed parameterization. |
| 4 | The design-only cap assessment did not model the optimizer workload or escalation counts. | A symbolic workload model is added using the frozen inventory's assignment count, fold count, \(N_f\), and parameter dimension \(p_f\), plus per-fit iteration, line-search-candidate and Arb-precision counts. A synthetic benchmark supplies shape- and precision-specific timing and escalation diagnostics. These are explicitly not treated as estimates of the project's data-dependent trigger or escalation rates. |
| 5 | Fixtures did not require cases resolving only at 1024 or 2048 bits, or failure to resolve at 4096 bits. | The validation grid now has explicit first-resolution-at-1024, first-resolution-at-2048, first-resolution-at-4096 and never-resolves cases, together with singular and near-singular information matrices. An unresolved comparison or inverse remains a fail-closed stall/unavailability, never a pass. |
| 6 | The exact Python-FLINT rational-to-Arb conversion and API version needed to be grounded. | The candidate API is narrowed to Python-FLINT 0.9.0: the multiprecision rational constructor stores \(m/k\), and its canonical rational string is parsed by Arb as an enclosing ball without a binary64 intermediate. The API is still proposed and must be locked and tested; this text does not claim it is installed or validated. |
| 7 | The rank proof should state explicitly that the residual after cell-centering is orthogonal to the entire baseline span. | The proof now says that the cell-centered concentration residual is orthogonal to both cell indicators and all 77 reference-contrast columns; a positive exact squared norm therefore places the concentration column outside the baseline column span. |

**Binding v0.5 decisions:** v1.7's reduced-rational \(C_D\) is the predictor in the model. Binary64 \(C_D\) values may be used only to generate a proposal direction, never to evaluate or certify the model. The exact-rational model governs all Arb objective, gradient, information, convergence, Wald-SE and Armijo calculations. The Arb precision ladder remains 128, 256, 512, 1024, 2048 and 4096 bits, with no weakened inequality or midpoint fallback. Runtime estimates must separate deterministic design workload from data-dependent trigger/escalation behaviour. No project-data runtime pilot, solver fit, assignment sampling or feasibility run is permitted.

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

Use the fixed 78-by-77 integer reference-contrast matrix B in canonical record identifier order. For rows r=1,...,77 and columns j=1,...,77, set B[r,j]=1 when r=j and B[r,j]=0 otherwise. Set B[78,j]=-1 for every column j. Thus every column sums to zero, B has full column rank, and the constrained record-effect vector is omega = B theta, where omega_1,...,omega_77 equal theta_1,...,theta_77 and omega_78 equals minus their sum. The sum-to-zero constraint is exact in the parameterization; there is no redundant 78th coefficient and no floating-point square-root contrast is used.

This reference basis is not orthonormal: B-transpose B = I_77 + 11-transpose-ones, its inverse is I_77 - (1/78)11-transpose-ones, and det(B-transpose B) = 78. The constrained record-effect subspace is nevertheless the same as for any orthonormal Helmert basis H. If B=H R and eta=R theta, then det(R)^2=det(B-transpose B)=78, so the information determinant in B coordinates equals the determinant in orthonormal coordinates multiplied by 78. The Firth penalty therefore differs by the fixed additive constant 0.5 log(78), the same for baseline and enriched models.

The reduced-coordinate gradient components are **not** unchanged by this basis transformation: the chain rule gives g_theta = R-transpose g_eta, while a Fisher-scoring displacement transforms as d_theta = R-inverse d_eta. The invariant quantities are the represented constrained coefficient vector omega, the mapped tangent gradient, the fitted linear predictor, the Fisher-scoring displacement in the original model, the objective increment and the Armijo decision. The fixed 0.5 log(78) additive shift does not alter the objective gradient when expressed in any one fixed parameterization, and it does not alter the fitted parameters or objective differences.

The convergence test is not evaluated as a componentwise norm in theta coordinates. The operational definition in §3.1 maps the reduced-coordinate gradient back to the original 78-dimensional constrained omega representation. This makes the criterion a property of the constrained coefficient vector, not of the chosen full-rank coordinates.


### 2.2 Design matrices

For each LOPO fold, construct both models from the exact same training-row identifiers:
- baseline columns: one indicator per eligible exact cell and the 77 exact integer reference contrasts B;
- enriched columns: the baseline columns plus the raw C_D column.

The row order is a canonical sort by stable version identifier, then record identifier. The column order is fixed as cell indicators, the 77 columns of B, then C_D. Test rows are never used to fit parameters. The scoring rows and fold membership are those frozen by the v1.7 design-only audit.

The baseline design is full column rank under the declared complete crossing. Suppose a linear combination of the cell-indicator columns and B contrast columns is zero on every training row. Within any nonempty cell c, the cell coefficient a_c plus (B theta)_r must equal zero for every record r. Sum these 78 equalities over records. Because every column of B sums to zero, 78*a_c=0 and therefore a_c=0. It follows that B theta=0; because B has full column rank, theta=0. Thus the cell indicators and the 77 constrained record contrasts are linearly independent.

The enriched C_D column is independent of the baseline columns when the v1.7 within-cell variation gate holds. In each training cell c, let Cbar_c be the mean C_D over its training versions. Subtract Cbar_c from C_D(v) for every row belonging to version v in cell c. The resulting residual is orthogonal to the cell-indicator columns by within-cell centring. It is orthogonal to every B contrast column because each version contributes all 78 records and every column of B sums to zero. Thus this residual is orthogonal to the entire baseline column span, which is generated by the cell indicators and the 77 reference contrasts. Its squared norm is 78 times the sum, over training cells and versions, of (C_D(v) - Cbar_c)^2. A positive exact squared norm therefore proves that the C_D column is outside the baseline span. This is positive exactly when there is within-cell C_D variation; v1.7 requires the corresponding W_C,c_train positivity for every scored training fold-cell. The exact reduced-rational C_D values determine each positivity decision.

These structural arguments, together with the exact W_C,c_train checks, are the rank decision. A floating-point numerical-rank tolerance must not independently override that exact structural decision. A numerical condition/rank diagnostic may be recorded for transparency, but it is diagnostic only; it is not a new exclusion rule. If the actual model information matrix cannot be factorized under the pinned linear-algebra routine, the fitting failure is handled under §3.3 and v1.7. The implementation must never respond by dropping rows, cells, columns, or records.

### 2.3 Exact rational concentration and the model predictor

For each version, define \(C_D=m/k_{fail}\) when \(k_{fail}>0\), where \(m=\max_j f_j\). When \(k_{fail}=0\), define \(C_D=0\) exactly and retain the separate status label "NO OBSERVED FAILURES". The unresolved count \(k_{unresolved}\) is not included in either \(m\) or \(k_{fail}\). Store every value as its reduced exact rational pair (m,k) and as a multiprecision rational fmpq(m,k); zero is the exact rational 0/1. The reduced numerator/denominator pair remains the canonical representation for equality, distinct-value counts, multiplicities, exact within-cell variation, audit keys and permutation enumeration.

The statistical model's predictor matrix is the exact-rational matrix X_Q: cell-indicator entries and reference-contrast entries are exact integers, while the enriched C_D column contains the exact reduced rationals. The Arb path converts each rational directly from its canonical rational string to an Arb ball that encloses that exact value. No binary64 conversion is permitted on the objective, gradient, expected-information, determinant, inverse, convergence, Wald-SE, directional-derivative or Armijo-certification paths.

A separate binary64 proposal matrix X_64 may be formed by the fixed conversion routine of the pinned numerical stack, solely to generate approximate Fisher-scoring directions. It is not the model matrix and must never be substituted for X_Q in a fitted quantity or acceptance decision. The exact rational pair remains attached to each predictor value throughout. The proposal conversion is audited for deterministic reproducibility, but its rounding error is not treated as statistical approximation or as part of the model definition.

This preserves exact permutation combinatorics and prevents two distinct rational concentrations from being merged by display rounding. It also ensures that every certified numerical decision pertains to v1.7's exact C_D, rather than to a nearby binary64 surrogate.


## 3. Optimisation algorithm

### 3.1 Ordinary maximum-likelihood fits and the v1.7 convergence criterion

Use deterministic Fisher-scoring / iteratively reweighted least squares (IRLS) for both models, with a strict separation between the exact model and the binary64 proposal calculation. The model is defined by the exact-rational matrix X_Q from §2.3. At every accepted parameter vector, the objective, score, expected information, gradient, convergence statistic and all certified comparisons are evaluated from X_Q in Arb. For the purpose of proposing an update only, construct X_64 using the pinned deterministic conversion of each exact rational predictor to binary64; use X_64, binary64 logistic probabilities and binary64 Cholesky solves to obtain an approximate Fisher-scoring direction. This proposal direction is not itself a fitted quantity and is never accepted without the exact-rational Arb checks below. The ordinary proposal equations are I_64 = X_64-transpose W_64 X_64, U_64 = X_64-transpose(y-pi_64), and I_64 d = U_64. No binary64 inverse is formed. The exact model predictor is z_Q = X_Q gamma, not X_64 gamma.

The v1.7 convergence threshold is 10^-8 and its componentwise scaling is retained. To operationalise it without making the decision depend on the arbitrary full-rank coordinates, evaluate it in the original constrained coefficient representation:
- alpha components: use the ordinary gradient component g_alpha,c and denominator max(1, abs(alpha_c));
- record effects: let g_theta be the gradient component in the 77 reference-contrast coordinates for the active objective. Map it to the original sum-zero tangent space as g_omega_tan = B (B-transpose B)^-1 g_theta, a 78-component vector. Since (B-transpose B)^-1 = I_77 - (1/78)11-transpose-ones, this mapping is fully specified. Use g_omega_tan componentwise, with denominator max(1, abs(omega_r));
- enriched slope: use g_beta and denominator max(1, abs(beta_C)).

The fit is converged when the maximum of all applicable scaled component magnitudes is at most 10^-8. The mapping B(B-transpose B)^-1 g_theta is the orthogonal projection of any ambient record-effect gradient onto the sum-zero subspace. It is invariant under any invertible change of coordinates B-prime=BQ, because the reduced gradient transforms as Q-transpose g_theta and the mapped 78-vector remains unchanged. This is the declared operational interpretation of v1.7's constrained-parameter criterion; it does not use a coordinate-dependent componentwise norm in theta.

The convergence decision itself is certified with Arb balls, not a binary64 gradient comparison. At each iterate, compute the active objective gradient as an Arb vector from the exact dyadic stored coefficients and the exact-rational design matrix entries: for ordinary maximum likelihood, g = X-transpose(y-pi); for the Firth objective, g = U_star using the Arb inverse and leverage calculation specified in §3.2. Extract the alpha, theta and (where present) beta components. Compute g_omega_tan = B(B-transpose B)^-1 g_theta in Arb, using the exact rational entries of (B-transpose B)^-1 = I_77 - (1/78)11-transpose-ones. Compute each denominator max(1,abs(parameter)) from the exact stored parameter values; omega = B theta is an exact dyadic sum for the stored binary64 theta vector. Form Arb enclosures for every scaled absolute component and evaluate them at the same 128, 256, 512, 1024, 2048 and 4096-bit precision ladder.

A convergence PASS is allowed only when the upper bound of every scaled component is at most 10^-8. If any component's lower bound exceeds 10^-8, the iterate is definitely not converged and the Fisher-scoring update may proceed. If the intervals straddle the threshold, increase precision. If any component remains unresolved at 4096 bits, convergence is not certified: record the interval and continue as nonconverged, never as converged. If the current Firth gradient or inverse cannot be enclosed at the precision cap, the Firth fit is unavailable. This conservative certificate does not change v1.7's 10^-8 threshold; it prevents rounding uncertainty from being treated as evidence that the threshold has been met.

Check the Arb-certified convergence criterion at the initial point and immediately after each accepted update, before attempting another line search. If the criterion is certified, terminate successfully. Otherwise, compute the binary64 Fisher-scoring direction and proceed under the Armijo rule. A threshold-inconclusive gradient is recorded as 'convergence not certified at precision cap' and is not a convergence PASS. Initialization is the all-zero vector in the constrained parameterization. There is no random initialization, warm start, data-dependent alternative initialization, or parameter carry-over between folds or assignments.

#### Actual-candidate construction and certified Armijo evaluation

For a trial alpha, first construct the parameter candidate that will actually be stored, using two separate IEEE-754 binary64 round-to-nearest, ties-to-even operations componentwise: v = round64(alpha*d), then gamma_cand = round64(gamma + v). Fused multiply-add or compiler contraction is not permitted. If any component of v or gamma_cand is non-finite, reject that trial candidate and continue to the next smaller alpha; a non-finite direction d itself is a fitting failure. If gamma_cand is bitwise identical to gamma, stop backtracking: no representable parameter update remains at this alpha or any smaller one. When a candidate is certified and accepted, copy gamma_cand verbatim as the next iterate; do not recompute or reapply the update.

Define s = gamma_cand - gamma as the exact real difference of the two stored binary64 vectors. Do not round this subtraction back to binary64. Convert each finite binary64 current coefficient and candidate coefficient to its exact dyadic rational value (a*2^b), then to an Arb ball with zero input radius. Construct the design entries from X_Q: integer entries are inserted exactly, and each C_D=m/k entry is converted from its exact rational representation directly to an Arb enclosure, with no binary64 intermediate. Compute z_Q = X_Q gamma and t_Q = X_Q s in Arb ball arithmetic. The candidate linear predictor is therefore z_Q+t_Q = X_Q gamma_cand, and the point tested is exactly the point stored under the v1.7 rational predictor. The approximate X_64 used to obtain d has no role in this calculation.

Use the unchanged Armijo constant c = 10^-4. Compute the ordinary objective increment delta_ell and the directional derivative D = U_Q-transpose s as Arb balls enclosing their exact real values for the exact-rational design and stored binary64 parameters. For each trial candidate, evaluate at the fixed precision ladder 128, 256, 512, 1024, 2048 and 4096 bits. At each precision, construct the Arb enclosures afresh from the exact dyadic parameter inputs and exact-rational design entries.

For each row, obtain pi_i = 1/(1+exp(-z_i)) and q_i = 1/(1+exp(z_i)) in Arb. If the complete t_i ball lies in [-0.5, 0.5], use the stable small-step identities:
- if y_i = 0: delta_i = -log1p(pi_i * expm1(t_i));
- if y_i = 1: delta_i = -log1p(q_i * expm1(-t_i)).

Otherwise use the algebraically equivalent log-sum-exp identities, which are valid for all t_i:
- if y_i = 0: delta_i = -logaddexp(log(q_i), log(pi_i) + t_i);
- if y_i = 1: delta_i = -logaddexp(log(pi_i), log(q_i) - t_i).

Here log(pi_i) = -log1p(exp(-z_i)) and log(q_i) = -log1p(exp(z_i)). Implement logaddexp for Arb balls with the shift m equal to the larger of the two exact Arb upper endpoints, m = a.upper().max(b.upper()): m + log(exp(a-m) + exp(b-m)). Since m is at least each upper endpoint, both exponential arguments are bounded above by zero throughout their input balls. This is an exact identity and avoids positive exponential overflow. Sum the row increments in canonical row order using Arb ball addition; do not use a binary64 sum or fsum result to authorize a step. The Arb radius encloses row-operation, transcendental and accumulation error, including the dependence on the number of training rows.

Compute D = U_Q-transpose s from the same exact-rational Arb model at the current gamma, with the row and parameter reductions performed as Arb ball operations. A candidate is certified for acceptance only if lower(D) > 0 and lower(delta_ell) >= 10^-4 * upper(D). It is definitely rejected at a given precision if upper(delta_ell) < 10^-4 * lower(D) or upper(D) <= 0. If neither acceptance nor rejection is certified, increase precision and repeat. If the comparison remains unresolved at 4096 bits, mark that candidate 'Armijo interval inconclusive at precision cap', do not accept it, and continue to the next smaller representable candidate. Do not subtract an epsilon, lower c, or weaken the sufficient-increase inequality.

If no candidate is certified before alpha underflows to zero or gamma_cand becomes bitwise identical to gamma, the line search stalls. This is a fitting failure/nonconvergence routed by §3.3, never convergence. Record the precision used, N, both interval bounds, the resulting margin interval lower(delta_ell) - 10^-4*upper(D), number of inconclusive candidates and the termination reason for every line search.

Each fold has N = 78 times the number of training versions. The exact maximum N across the real-data LOPO folds and every N4-a dataset must be calculated from the frozen design inventory before software validation or an execution GO. Report this N_max. The Arb ball radius is the operational N-dependent error bound; no heuristic N-independent floating-point noise estimate is substituted. No execution GO is possible while N_max is unknown or while the synthetic fixture grid has not covered N_max.

The fit may take at most 200 accepted updates. After the 200th update, evaluate the convergence criterion once more; if it is not met, the fit is nonconverged. Any non-finite objective, score, information matrix, or update, or an information factorization failure needed to compute an update, is a numerical fitting failure. The enriched-fit and baseline-fit consequences are specified in §3.3.

### 3.2 Firth / Jeffreys-penalized refits

When the v1.7 enriched-model trigger fires, refit both models using the exact objective:
F(gamma) = ell(gamma) + 0.5 log det I(gamma),
where I(gamma) is the expected Fisher information X-transpose W X in the same constrained parameterization and W has entries pi_i(1-pi_i). Do not substitute the observed Hessian for expected information.

For the binary64 Firth proposal direction only, use the approximate matrix X_64 and its binary64 expected information I_64 = X_64-transpose W_64 X_64. Define its proposal leverage h_64,i = w_64,i times x_64,i-transpose I_64-inverse x_64,i. Compute it without forming the inverse: if I_64 = L L-transpose is the Cholesky factorization, solve L q_i = x_64,i and set h_64,i = w_64,i times q_i-transpose q_i. The binary64 proposal adjusted score is:
U_star,64 = X_64-transpose [ y - pi_64 + h_64 elementwise-multiplied by (1/2 - pi_64) ].

This binary64 score and its Fisher-scoring direction are proposal machinery only. The exact Firth objective and adjusted score are defined using X_Q, and the exact-rational Arb derivative U_star,Q-transpose s is the only directional derivative that can authorize a candidate. A proposal that is not an ascent direction for the exact model cannot pass the Arb Armijo test.


The derivative identity underlying this score is:
partial [0.5 log det I] / partial gamma_j = 0.5 trace( I-inverse times partial I / partial gamma_j ).

The Fisher-scoring direction for the Firth objective uses the full penalized adjusted score U_star, not the ordinary score U. Solve I d = U_star in binary64. At non-converged iterates, verify that the binary64 directional derivative is finite and strictly positive before forming candidates. The Arb-certified derivative used for candidate acceptance is independently computed as U_star-transpose s, as specified below.

#### Certified Firth objective increment and directional derivative

For each actual stored binary64 candidate constructed under §3.1, use its exact displacement s and the same Arb precision ladder 128, 256, 512, 1024, 2048 and 4096 bits. Compute delta_ell from the same Arb rowwise method as §3.1. At the current and candidate coefficient vectors, construct the expected-information matrices I_current and I_candidate as Arb ball matrices from the exact-rational design entries and high-precision logistic probabilities.

Under §2.2's full-column-rank design proof and finite logits, every exact logistic weight pi_i(1-pi_i) is strictly positive, so the exact expected-information matrix X-transpose W X is positive definite. For each matrix, compute an Arb ball enclosure of its determinant with arb_mat.det(), then take the Arb logarithm only after the determinant enclosure has a strictly positive lower bound. Define delta_logdet = log(det(I_candidate)) - log(det(I_current)) as an Arb ball, and delta_F = delta_ell + 0.5*delta_logdet. Do not use the binary64 Cholesky-diagonal difference to authorize an Armijo step. The determinant enclosures and their logarithms provide a certified absolute error bound for this specific matrix pair. Their radii incorporate the effects of matrix conditioning and all enclosed arithmetic; a binary64 2-norm condition-number estimate may also be reported as a diagnostic, but it never replaces the ball enclosure or determines acceptance.

Compute the current Firth adjusted gradient in Arb for the Armijo directional derivative using X_Q. Form I_Q,current = X_Q-transpose W_Q X_Q and a verified Arb enclosure of its inverse using arb_mat.inv(). Compute the exact-rational Arb weights, h_i = w_i*x_Q,i-transpose*I_Q,current-inverse*x_Q,i, and U_star,Q = X_Q-transpose[y-pi_Q+h elementwise-multiplied by (1/2-pi_Q)]. If the inverse cannot be certified at a precision, increase precision. The directional derivative for the actual candidate is D = U_star,Q-transpose s, not alpha times a binary64 proposal score.

A Firth candidate is certified for acceptance only if the determinant enclosures for both matrices are positive, lower(D)>0, and lower(delta_F) >= 10^-4*upper(D). It is definitely rejected if upper(delta_F)<10^-4*lower(D) or upper(D)<=0. Otherwise increase precision. If the comparison or determinant sign remains unresolved at 4096 bits, do not accept that candidate; record it as interval-inconclusive and try the next smaller representable candidate. The same no-epsilon, no-weakened-inequality rule applies.

If the determinant or inverse enclosure for the current accepted Firth iterate cannot be certified after 4096 bits, the Firth fit is numerically unavailable. If a trial candidate cannot be certified, it is rejected as a candidate, not accepted as an iterate. If no candidate is certified before the representability stop, record a line-search stall. Every accepted Firth iterate must have finite binary64 proposal quantities, a useably positive-definite I_64 under the declared LAPACK factorization for the next proposal update, and a positive Arb determinant enclosure for the exact-rational I_Q. No jitter, pseudo-inverse, ridge fallback, alternate optimizer or silent model simplification is permitted.

The implementation must independently verify the adjusted-score formula against the analytic derivative of the stated penalized objective and against finite-difference gradients on fixed software fixtures. It must also verify Arb determinant/log enclosures against high-precision references and confirm enclosure containment for ill-conditioned fixtures. Fixture set, finite-difference scheme, precision ladder, tolerances and expected outputs must be frozen before any execution GO. This is software validation, not project-data analysis.

### 3.3 Standard error, separation trigger, and failure routing

The enriched ordinary model is fitted first. If it does not converge, trigger (i) in v1.7 fires and both models are refitted using the Firth objective. For this computational plan, enriched ordinary nonconvergence includes:
- reaching 200 accepted updates without satisfying the convergence criterion;
- failure to obtain a finite, strictly positive binary64 Fisher-scoring directional derivative;
- an Armijo line-search stall: no candidate is certified by the Arb interval comparison, including candidates that remain inconclusive at the 4096-bit precision cap, before alpha underflows to zero or the candidate vector becomes bitwise identical to the current vector;
- non-finite objective, score, information or parameter values before convergence;
- Cholesky failure when factorization is required to compute an ordinary enriched-model update.

If the enriched ordinary fit converges with finite parameters, first check whether abs(beta_C) > 50 using the stored binary64 coefficient (the threshold comparison is exact for this representable value). If so, trigger (ii) fires and both models are refitted with Firth. Otherwise, compute the final-iterate expected information from the exact-rational model:
I_Q = X_Q-transpose W_Q X_Q,
at the final accepted ordinary enriched-model parameter vector. Use Arb matrix inversion/solves to enclose the exact-model Wald variance
V_beta = e_beta-transpose I_Q-inverse e_beta
and its square root SE(beta_C). No binary64 predictor matrix may determine this standard error. If the information inverse or the variance cannot be certified at 4096 bits, or if the SE interval straddles 10^3 at the precision cap, the SE trigger cannot be evaluated and the fold/test is unavailable; this is not re-labelled as SE > 10^3. If the lower bound of the certified SE interval exceeds 10^3, trigger (iii) fires and both models are refitted with Firth. If its upper bound is at most 10^3, trigger (iii) does not fire. The exact reference-contrast reparameterization affects only nuisance coordinates and leaves this beta_C variance unchanged.

If the final-iterate exact-rational information inverse or Wald-SE interval is unavailable, this is not re-labelled as an SE exceeding 10^3 and does not create a new Firth trigger: the fold/test is unavailable under v1.7's no-silent-fallback rule.


If none of the three enriched-model triggers fires, fit the baseline ordinary model. Any unresolved baseline ordinary fitting failure makes the applicable test unavailable. Baseline failure alone does not create a new Firth trigger. If an enriched-model trigger has already fired, fit both models with Firth and do not run an unnecessary baseline ordinary fit first.

| Ordinary-fit outcome | Required action |
|---|---|
| Enriched ordinary fit does not converge, including an Arb interval-inconclusive Armijo stall or a representability-limited stall | Trigger (i); jointly Firth-refit baseline and enriched models |
| Enriched ordinary fit converges and abs(beta_C) > 50 | Trigger (ii); jointly Firth-refit both models |
| Enriched ordinary fit converges, abs(beta_C) <= 50, and the lower bound of the certified exact-rational Wald-SE interval exceeds 10^3 | Trigger (iii); jointly Firth-refit both models |
| Enriched ordinary fit converges but the exact-rational final-iterate information inverse/SE interval cannot be certified at 4096 bits, or the SE interval straddles 10^3 at the cap | Unavailable; do not invent an SE threshold or an extra trigger |
| Enriched ordinary fit converges with abs(beta_C) <= 50 and the upper bound of the certified exact-rational Wald-SE interval is at most 10^3; baseline ordinary fit succeeds | Use the ordinary fits; no Firth refit |
| No enriched trigger fires but baseline ordinary fitting fails, including an Arb interval-inconclusive Armijo stall | Unavailable; no baseline-only trigger exists |
| Either Firth refit fails to converge, including an Arb interval-inconclusive Armijo stall, or violates the declared information-matrix rules | Unavailable under v1.7 V5(b); no assignment is discarded or replaced |

For every fold, record the enriched ordinary-fit status, all triggers that could be evaluated, whether the baseline ordinary fit was attempted, whether the Firth pair was attempted, both final model statuses, and the reason for any unavailability. Also record accepted updates, backtracking halvings, the Arb convergence-gradient enclosures at each checked iterate, the Armijo termination reason, and interval-inconclusive, precision-cap and representability stalls. If abs(beta_C) > 50 already triggers Firth, a Wald SE is not needed to establish the trigger and may be marked not evaluated. A certified SE interval is recorded with its precision and lower/upper bounds whenever trigger (ii) has not already fired. The v1.7 rule is otherwise unchanged.

## 4. Linear algebra and exact-rational interval arithmetic

**Binary64 proposal path:** IEEE-754 binary64 arithmetic with the pinned LAPACK symmetric positive-definite Cholesky factorization, lower-triangular form (DPOTRF), applied to X_64-transpose W_64 X_64.

- X_64 is formed only to propose approximate Fisher-scoring directions. Solve proposal systems by forward/back substitution using the Cholesky factor. Never form the binary64 information-matrix inverse.
- The binary64 Cholesky log determinant may be calculated for proposal diagnostics only. It must not determine the objective, convergence, Wald-SE trigger, Armijo comparison, or any fitting/availability classification.
- No diagonal perturbation, eigenvalue clipping, pseudo-determinant, generalized inverse, or fallback factorization is permitted.
- Record the library name/version, linked LAPACK implementation, binary64 platform details, factorization status and any reported numerical error code.

**Exact rational input and certified path:** candidate library python-flint 0.9.0, using fmpq, Arb real balls and Arb ball matrices. This is a proposed dependency, not installed or locked. Python-FLINT's documented fmpq(m,k) constructor stores a multiprecision rational. Its canonical rational string is accepted by the Arb constructor as a rational input and converted to an enclosing real ball. Construct C_D as fmpq(m,k) and pass its canonical rational string directly to Arb; do not call float, create a decimal approximation, or pass through binary64 first. The enclosure must contain the exact rational input. This exact-rational conversion and containment check is mandatory in the synthetic unit fixtures.

- Convert every finite binary64 parameter x exactly using its exact x.as_integer_ratio() = (p,2^k) representation. The stored parameter and candidate values are dyadic rationals and are inserted into Arb with zero input radius. Integer and reference-contrast entries are inserted exactly. The rational C_D entries are separately enclosed from their exact rational strings.
- Use Arb balls for the exact-rational rowwise log-likelihood increment, exact-model directional derivative, exact-model convergence gradient, exact-model expected information, Firth determinant/inverse calculations and Wald-SE certification. Use arb_mat.det() to enclose determinants and arb_mat.inv() to enclose the inverse required for the Firth leverage and exact-model Wald variance. Increase context precision only along the fixed ladder in §§3.1–3.2.
- A determinant may be logged only when its Arb enclosure has a strictly positive lower bound. If the sign, inverse, SE threshold, or Armijo comparison cannot be certified at 4096 bits, follow the candidate/current-iterate failure rules in §§3.1–3.3; never substitute a midpoint or a binary64 estimate.
- Arb real balls enclose rounding and propagated error for the exact-rational model. Record the radius of every objective, derivative, gradient, determinant/log-determinant, inverse-dependent SE and Armijo-margin interval, plus a binary64 2-norm condition-number diagnostic for information matrices. The condition estimate is diagnostic only; it is not used to accept/reject a step or trigger separation handling.

References for the proposed API and its guarantees: https://python-flint.readthedocs.io/en/latest/fmpq.html (fmpq(m,k) exact rational construction and canonical numerator/denominator access); https://python-flint.readthedocs.io/en/stable/arb.html (Arb balls and rational-string input); https://python-flint.readthedocs.io/en/latest/arb_mat.html (arb_mat.det() and arb_mat.inv()).

The exact numerical-library versions and platform build are not frozen in v0.5. The implementation environment must first be inventoried and then pinned in a lock artifact before software validation. Do not install dependencies into the user's working environment as part of this design step. Pin the exact Python-FLINT, FLINT, Python, platform and wheel/build identities before relying on the proposed APIs.


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


### 6.2 Optimizer and assignment workload model

The design inventory must supply, for every dataset d and LOPO fold f:

- V_df: number of training versions and N_df = 78 V_df training rows;
- C_df: number of eligible exact cell-intercept columns;
- pB_df = C_df + 77 baseline parameters and pE_df = C_df + 78 enriched parameters;
- G_d: number of held-out parent folds;
- A_d: number of assignment evaluations, counting the observed assignment once. For exact enumeration, A_d = |Omega_adm|. For the Monte Carlo branch, A_d = 1 + 9,999 = 10,000. The 300 N4-a datasets are indexed in the frozen lambda-major/replication-minor order.

These counts are design-inventory quantities; they do not require fitting. Derive N_max = max(N_df) and p_max = max(pE_df) over the real-data design and all 300 specified N4-a datasets before software validation. No substitute count based on a proposed or remembered variant inventory is allowed.

For each assignment evaluation and fold, the path is deterministic conditional on the fit outcomes:

- one enriched ordinary fit is attempted;
- if no enriched trigger fires, one baseline ordinary fit is attempted;
- if any enriched trigger fires, the baseline ordinary fit is not run as an ordinary fit and the two joint Firth refits are attempted.

Thus, for each dataset, the total ordinary-fit count is
\[
F_{ord,d}=\sum_{a=1}^{A_d}\sum_{f=1}^{G_d}\left(1+\mathbf{1}\{\text{no enriched trigger}_{daf}\}\right),
\]
and the total Firth-fit count is
\[
F_{Firth,d}=2\sum_{a=1}^{A_d}\sum_{f=1}^{G_d}\mathbf{1}\{\text{an enriched trigger}_{daf}\}.
\]
The no-trigger path uses two ordinary fits per fold; the triggered path uses one enriched ordinary fit plus two Firth fits. A conservative path bound is therefore at most three fit calls per fold per assignment. These formulas count the observed evaluation once and do not repeat T(b_obs).

For a fit of dimension p and N rows, record separately: accepted IRLS updates (at most 200); line-search candidate attempts per update (bounded by the binary64 representability rule); the number of candidate comparisons reaching each Arb precision b in {128, 256, 512, 1024, 2048, 4096}; ordinary/Firth model class; and determinant/inverse/SE calls. The principal binary64 proposal-update workload scales as O(N p^2 + p^3). An ordinary Arb candidate certificate scales at least with its O(N p) rowwise likelihood and gradient operations. A Firth certificate additionally constructs O(N p^2) expected-information terms and performs dimension-p determinant/inverse operations, whose practical cost depends strongly on p, precision and conditioning. Actual measured timings, rather than asymptotic notation, control the runtime report.

The runtime benchmark is software-only and uses synthetic matrices/fixtures at the design-derived (N,p) grid, including (N_max,p_max), the required condition-number strata and every precision level. It records wall-clock time, peak memory, fit class, iteration count, candidate count, and escalation counts E_b, where E_b is the number of candidate certificates that required precision b or higher. Report the benchmark mean, median, 95th percentile and maximum by workload class. Include synthetic cases first resolving at 1024, 2048 and 4096 bits, and cases unresolved at 4096 bits. A separate scenario table reports estimated runtime under (i) no precision escalation, (ii) the synthetic benchmark's observed escalation profile, and (iii) the all-candidates-to-4096-bit conservative scenario.

The synthetic benchmark's E_b profile is a software workload diagnostic only. It is not an estimate of the project's data-dependent escalation distribution, trigger frequency, or total runtime. Those quantities cannot be known from design inventory alone. Therefore, no single expected project runtime or execution-feasibility claim may be reported until the exact inventory, design-only assignment counts, isolated benchmark results and a transparent conservative workload bound are available. No timing pilot, candidate-fit experiment, or benchmark against the LC518 bank is allowed in this phase.

## 7. Determinism, parallelism and evaluation accounting

For the first implementation, use single-process, deterministic execution. Parallel fitting or parallel random streams are not introduced until a separate reproducibility audit establishes that worker scheduling cannot alter stream assignment or reduction order.

Canonical ordering is required for cells, parents, versions, records, design columns, rational concentrations, enumerated assignments and report rows. Floating-point reductions use a fixed order. Any platform-dependent numerical difference that changes convergence, trigger status, admissibility, availability or a reported decision is a reproducibility failure requiring investigation before results are interpreted.

Per dataset, count:
- one observed pipeline evaluation, computed once;
- exact branch: |Omega_adm| total assignment evaluations, with the observed evaluation reused and not repeated;
- Monte Carlo branch: 1 + 9,999 comparison-set members, with the observed evaluation reused and not repeated;
- per assignment: two model fits per LOPO fold, plus both Firth refits on folds where the trigger fires.

The implementation must reconcile these counts against v1.7 §8(iii) and the binding v1.7 acceptance-record note before any run. Report, per evaluated assignment, the enriched ordinary-fit outcome, trigger status, baseline ordinary-fit status when applicable, Firth-refit status, accepted updates, line-search halvings, Armijo termination reason (including interval-inconclusive and precision/representability stall), and final availability classification. Retain each checked iterate's convergence-gradient intervals and PASS/non-PASS decision. For each accepted or rejected line-search candidate, retain N, precision used, objective-increment interval, directional-derivative interval, Armijo margin interval, and Firth determinant/log-determinant interval radii and condition diagnostics when applicable. This allows the v1.7 evaluated-assignment accounting to be audited without using fit status to filter assignments.

## 8. Software validation required before execution GO

Validation must use synthetic fixtures authored solely for software testing, not the LC518 bank or real solver outcomes. No statistical power, null calibration, simulation study or numerical probability evaluation is part of this validation phase.

Required tests:
1. constrained contrast basis: exact column sums zero, full column rank of B, B-transpose B = I + 11-transpose-ones, determinant 78, exact sum-to-zero parameterization, and invariance of the mapped tangent-gradient criterion under invertible basis changes;
2. design matrix: deterministic row/column ordering and correct fold separation;
3. exact rational concentration: reduced fractions, equality, multiplicities and distinct arrangements; confirm the fmpq constructor and Arb rational-string conversion enclose the exact rational without a binary64 intermediate, including non-dyadic cases such as 1/3 and close distinct fractions;
4. enumerator: exact unique arrangement count and deterministic order on hand-checkable fixtures;
5. sampler: Fisher–Yates implementation and uniformity proof at the algorithm level; any empirical frequency experiment is deferred until a separate execution GO;
6. audit key: exact equality, all scored and excluded fold-cell decisions, and no outcome/fit/score fields;
7. exact-candidate displacement: prove that the Arb displacement s is the exact difference of the current and candidate binary64 vectors; verify t = X_Q s matches the exact-rational evaluated stored candidate, including halfway rounding, cancellation and sub-ULP candidate cases; separately verify that X_64 is used only for proposal directions and never enters a certified quantity;
8. likelihood increment: verify the Arb log1p/expm1 and logaddexp identities against exact/high-precision references; confirm interval containment for large absolute likelihoods with tiny increments and for rowwise sums at increasing N;
9. directional derivative: verify Arb enclosures of U-transpose s for ordinary fits and U_star-transpose s for Firth, including positivity, inconclusive and non-ascent cases;
10. Firth: adjusted-score formula, expected-information identity, analytic adjusted score against an independently differentiated objective and finite-difference gradient; verify the binary64 Fisher direction uses U-star;
11. Arb determinant/inverse: verify arb_mat.det() and arb_mat.inv() enclosures against known matrices and high-precision references; include matrices with controlled condition numbers, positive-definite near-singular matrices, exactly singular matrices, non-positive-definite matrices, and cases where 4096-bit certification correctly fails closed;
12. Firth objective increment: verify Arb log(det(I_candidate))-log(det(I_current)) interval containment against independent high-precision references; record determinant and log-determinant radii and condition diagnostics;
13. Cholesky: SPD success, singular/non-SPD failure, and triangular-solve correctness for the binary64 update path;
14. convergence certificate: verify Arb enclosures of ordinary and Firth gradients, the B(B-transpose B)^-1 tangent projection, exact parameter denominators, and PASS only when every upper bound is <= 10^-8; include threshold-straddling and 4096-bit inconclusive fixtures;
15. optimizer: convergence, certified Armijo lower/upper-bound comparison, initial-point convergence check, dynamic halving, actual stored-candidate evaluation, 4096-bit interval-inconclusive handling, binary64 representability stop, iteration-limit and deterministic failure-routing; include candidates whose first certified decision occurs only at 1024, 2048 and 4096 bits, plus a candidate that remains unresolved at 4096 bits and must never be accepted;
16. resolution grid: synthetic software-only fixtures over gradient magnitudes 10^-4, 10^-6, 10^-8 and 10^-10; row counts 78, 780, 7,800 and the exact design-derived N_max (remove duplicate sizes); and controlled information condition-number strata 10^2, 10^6, 10^10 and 10^14 where constructible. Record certified decisions, inconclusive candidate counts, interval radii, and stall rates. The N_max fixture is mandatory; the numerical design gate remains blocked until N_max is established from the frozen exact inventory;
17. stall routing: an enriched ordinary stall triggers joint Firth; a Firth stall makes the test unavailable; a baseline-only ordinary stall makes the test unavailable; none is called convergence;
18. assignment accounting: observed statistic reused exactly once; no duplicate observed fit;
19. availability: any unresolved fit failure invalidates the applicable test; no silent filtering or replacement;
20. RNG: deterministic regeneration from the root seed and stable stream identifiers;
21. cap: synthetic acceptance-rate fixtures verify stop-at-cap behavior and unavailable-on-partial-sample rule without touching project data;
22. failure routing: enriched ordinary nonconvergence triggers joint Firth; converged-fit unavailable SE does not invent a trigger; baseline-only ordinary failure is unavailable; any unresolved Firth failure is unavailable;
23. rank: full baseline rank and C_D independence from all baseline columns under the complete 78-record crossing; verify the algebraic proof and exact W_C,c gate, and confirm that no floating-point rank tolerance silently changes eligibility;
24. exact-model Wald SE: compare the Arb variance/SE enclosure based on X_Q with independent high-precision references; test intervals wholly below, wholly above and straddling 10^3 at the 4096-bit cap, with the straddling case routed unavailable and never reclassified as a trigger;
25. proposal/model separation: deliberately perturb the binary64 X_64 predictor column while holding X_Q fixed; confirm that the exact objective, gradients, convergence, SE, determinants, Armijo decision and final fit classification remain unchanged whenever the same stored candidate is supplied;
26. runtime model: verify assignment/fold/fit-call accounting, N_f and p_f derivations, per-precision escalation counters, and runtime scenario calculations on synthetic workloads; ensure no benchmark reads project records, outcomes, bank files or protected data.

The test suite, expected outputs, tolerances, software versions and hashes must be frozen before any project-data evaluation. Passing software tests demonstrates implementation consistency, not scientific validity, exchangeability, consent, bank integrity or predictive evidence.

## 9. Unresolved decisions and blockers

| Item | Current disposition | Required closure |
|---|---|---|
| Numerical stack and pinned versions | Open | Inventory the intended isolated environment; pin Python, NumPy, SciPy, LAPACK, python-flint and FLINT build/version before software validation |
| Arb interval implementation | Proposed; not implemented or validated | Independently review exact dyadic parameter conversion, exact-rational C_D conversion, interval row increments, convergence-gradient certification, exact-model determinant/inverse/SE certification, precision ladder and interval-bound comparisons |
| Convergence decision | Arb certificate specified; not yet tested | Validate the B(B-transpose B)^-1 projection and every scaled-component interval; an unresolved component cannot pass; test against independent high-precision references |
| Maximum training-row count N_max and parameter count p_max | Unknown; exact frozen version/cell inventory has not been established in this computational step | Derive N_max = 78 × max training versions and p_max = max(C_f+78) across real-data folds and all 300 N4-a datasets; validate the optimizer, interval and runtime grids at (N_max,p_max) before GO |
| Armijo/SE resolution under conditioning | Conservative exact-rational certification rule specified; not tested | Record interval radii and diagnostic condition numbers; exercise first resolution at 1024/2048/4096-bit levels, unresolved-at-4096 cases, and singular/near-singular information matrices; confirm every unresolved case fails closed |
| IRLS and Firth update details | Proposed above; not independently validated | Independent mathematical/code review of adjusted-score implementation, actual-candidate displacement and certified Armijo logic |
| Linear algebra | Candidate LAPACK Cholesky / DPOTRF for binary64 proposal directions; Arb verified determinant/inverse/SE enclosures for the exact-rational model | Pin actual library implementations and record binary64/Arb precision and platform details |
| PRNG | Candidate PCG64DXSM + SeedSequence | Pin NumPy version and verify stream mapping; no project sampling |
| Exact rational encoding/model predictor | Proposed and required for the fitting model as well as combinatorics | Review canonical rational construction, exact rational-string to Arb enclosure, deterministic X_64 proposal conversion, and proof that no rounded predictor enters any certified quantity |
| Audit-key feasibility | Not assessed | Requires approved design inventory; no bank reuse or outcome access in this phase |
| 10^8 cap feasibility | Unknown | Derive design-only bound or mark Monte Carlo unavailable |
| Consent provenance | Open | Must be resolved separately; computational readiness does not cure it |
| Parent-population uncertainty | Not provided by v1.7 | No parent-population claim; any change requires a new statistical plan |
| Runtime model and benchmark | Symbolic workload model specified; no design inventory or benchmark available | Establish assignment/fold/fit counts and (N_max,p_max); benchmark only synthetic fixtures in the isolated pinned environment; report zero-, observed-synthetic- and worst-case-escalation scenarios without presenting them as a project runtime forecast |
| Execution authorization | Not granted | Separate explicit GO after computational plan, software validation, isolation and data-access scope are accepted |

This v0.4 document is a proposal for review, not a final implementation contract. The next review must challenge, at minimum:
- whether the exact integer reference-contrast matrix B enforces the v1.7 sum-to-zero constraint and whether its fixed logdet shift and mapped tangent-gradient formula are correct;
- whether the explicit Firth adjusted score, expected-information Fisher direction, Armijo sufficient-increase rule and derivative identity implement the stated Jeffreys objective correctly;
- whether the actual stored-candidate displacement and Arb ball enclosure fully certify ordinary and Firth Armijo inequalities and the 10^-8 convergence test, including exact dyadic conversion and the 4096-bit precision cap;
- whether the Arb determinant/inverse/SE enclosures adequately capture the exact-rational model and conditioning, and whether the N_max/p_max resolution and escalation fixtures are sufficient;
- whether the exact-rational rational-to-Arb conversion avoids every binary64 intermediate in all certified quantities, while X_64 is confined to proposal-direction generation;
- whether the symbolic runtime model and synthetic escalation profile are auditable without presenting them as data-dependent project estimates;
- whether PCG64DXSM and the fixed SeedSequence stream hierarchy adequately implement the independent-uniform sampling model, with the limits of pseudorandom independence stated honestly;
- whether a line-search stall has been routed consistently with v1.7 in all three positions (enriched ordinary, baseline ordinary, Firth refit);
- whether the final-iterate information factorization for the Wald SE is specified without reusing a preceding-iterate factorization;
- whether the exact structural-rank argument, rather than an unspecified floating-point rank tolerance, is the appropriate design gate;
- whether the exact-enumeration and Monte Carlo accounting correctly reuses (T(b_{obs})) once;
- whether any proposed feasibility calculation would improperly reuse the exposed bank or inspect outcomes.

No item in this document is approved merely by appearing here. No code is implemented against project data, no project-data feasibility computation is performed, and no execution is authorized.

---

**End of B1 computational implementation plan v0.5 — design draft only.**
