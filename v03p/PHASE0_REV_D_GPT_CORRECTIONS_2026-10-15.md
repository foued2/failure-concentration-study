# GPT correction record for Revision D

**Date:** 2026-10-15  
**Status:** Technical correction patch for independent review. Not a protocol freeze, owner decision, or phase authorization.  
**Scope:** This record addresses GPT findings D1–D6 against the Revision D text supplied for review. The GitHub default branch currently contains the committed 2026-10-14 baseline and review response, but not the uncommitted Revision C/D files or `v03p/scripts/` package described in the review message. This file therefore records the exact corrections needed without altering the preserved committed baseline or claiming that untracked bytes were verified.

## Disposition

Revision D remains **NOT APPROVED for simulation-protocol freeze**. The mathematical support rule, Phase 1 feasibility policy, inference target, and fitted-model definition must be made mutually consistent before freeze. Findings D1–D4 are blockers; D5–D6 are additional specification blockers. The new package must not imply Phase 1 authorization.

## D1. Distinguish bucket-local support from the complete support event

For each in-range bucket (k), define (I_k=1) when that bucket passes the within-bucket conditions (minimum body count, at least two C values, and the two extreme values each represented by at least four bodies). Define the global event

[
G=I\left(\sum_k I_k\ge 2\right).
]

The per-bucket calculations reported in Revision D use (E[n_k I_k]), where (n_k) is the number of bodies in bucket (k). These are valid bucket-local expectations, but the complete analysis support also requires (G=1). The corresponding count for an analysis population satisfying the global support rule is (n_k I_k G); its expectation is (E[n_k I_k G]). An expectation conditional on global support would additionally divide by (P(G=1)), when that probability is positive.

**Required change to §9.1 and §9.2:** Keep the existing table labelled as *bucket-local support-proxy expectations*, and explicitly say it does not report the tail expectations conditional on the complete two-bucket support event. Do not use the table alone to assert the probability that the actual study's outcome gate passes or fails. Recompute the complete-rule quantities after the support/model rule is resolved, or clearly mark them as not calculated and leave the full gate result to the prespecified Phase 1 procedure. The support event is outcome-blind, but that does not make the bucket-local and globally supported populations interchangeable.

Suggested replacement paragraph:

> The following expectations are calculated under the bucket-local support proxy: each bucket is assessed against conditions 1–4 independently. The global analysis-support rule additionally requires at least two buckets to pass. Accordingly, these values are not expectations conditional on the global support event and do not estimate the probability that the complete support and outcome gate passes. The complete-rule distribution must be evaluated under the adopted model/support specification; until then, the table is descriptive only.

## D2. Correct the claims that contradict the displayed table

Two statements in the Revision D text are too strong:

1. “The upper tail fails on pairs, bodies, and suites in every computed cell” is contradicted by row **a50 @ (N_b=600), S40**, which reports (E[\text{suites}]=6.55), greater than (S=6). The pair and body expectations in that row remain below their minima.
2. “At feasibility size the per-tail diversity floors are unreachable in expectation under every scenario and mix” is contradicted by row **a50 @ (N_b=150), S40**, which reports lower-tail (E[\text{suites}]=9.04), greater than six.

Replace these claims with:

> In the computed bucket-local table, the upper-tail pair and body expectations are below their gate thresholds in every listed cell. The lower-tail distinct-body expectation is below (D=10) in every listed feasibility-size cell. Some suite expectations exceed (S=6); therefore, it is not correct to say that every diversity expectation misses its threshold. These are marginal expectations, not gate-pass probabilities: neither an expectation below a threshold nor one above it determines the probability that the joint gate passes.

Do not describe an expectation below a threshold as deterministic impossibility. Keep three concepts separate: an expected count, a probability of meeting a count threshold, and a structural zero.

## D3. Repair the Phase 1 grid/gate incompatibility before simulation-protocol freeze

The current proposal requires coverage to pass in every grid cell, including thin-support cells, while the reported bucket-local support probability for scenario (a), (N_b=120), is (0.001546). At 2,000 unconditional replications, this corresponds to only 3.092 expected bucket-local support-feasible replications; the complete rule is at least as restrictive as the bucket-local rule when it adds further conditions. Such a cell cannot meaningfully evaluate the proposed interval-coverage criterion on the stated replication budget.

**Required change:** Split Phase 1 outputs into (a) feasibility/gate-classification operating characteristics and (b) interval performance conditional on a replication being estimable under the frozen procedure. The protocol must state in advance the minimum number of feasible replications needed for coverage/FPR/power assessment and what happens if a cell cannot reach it. Either re-anchor the grid/sample size, or mark such cells *not evaluable for interval performance* and do not let them pass the interval gate by default. Report (P(\text{feasible})) separately. Rejection/conditioning used to obtain feasible simulation replicates must be disclosed, seeded and distinguished from unconditional feasibility-probability estimation.

O3 remains an owner/reviewer decision until the exact policy and grid are specified. No simulation should run while this item and the §5A matrix contradiction remain unresolved.

## D4. Make G6a and its coverage truth refer to the same target

The current G6a prose mixes two targets:

- conditioning on the realized training data, including its outcomes and the fitted models; and
- conditioning only on the training identities while averaging over possible training outcomes and refitting.

These are not the same estimand. A test-only bootstrap with the trained models held fixed is aligned more directly with the first target. It does not, by itself, account for training-outcome variability required by the second.

**Required change:** Preserve G6a/G6b as an owner decision, but make both candidates mathematically explicit.

- **G6a-compatible target:** Let (D_{\mathrm{train}}) denote the realized training data, including outcomes, and let (f_0(D_{\mathrm{train}})) and (f_1(D_{\mathrm{train}})) be the fitted predictors. Define the conditional target as the expected held-out loss difference over new eligible test body/suite cells conditional on this realized training data. Coverage truth and the test-resampling procedure must target this same quantity.
- **Training-identities-conditional alternative:** If the target conditions only on training identities and averages over possible training outcomes/refits, state that separate target and use a simulation/uncertainty procedure that accounts for training-outcome variability. Do not describe the current fixed-fit test bootstrap as automatically covering it.
- **G6b:** Retain the full-pipeline target as the alternative that resamples the split and refits in the inference procedure.

After the owner chooses the target and the model is resolved, freeze the per-replication truth-calculation algorithm, numerical tolerance, seeds and simulation size before Phase 1. Until that point, no FPR/power/coverage result can be claimed to validate the predictive estimand.

## D5. Separate diagnostic standardization from model-fitting standardization

The committed `study/models.py` constructs the current RCS design as `[1, rcs_basis(log(1+k)), C]` and feeds it to the fitting implementation; the displayed source does not apply the proposed training-mean/SD transformation. Revision D's M1/M2 table, by contrast, describes standardization “as in the rank check.” If this standardization is used for fitting, it changes the fitted matrix. With a fixed ridge penalty, rescaling predictors can change the estimator, so it is not merely a numerical housekeeping detail.

**Required change:** For every M-option, identify separately:
1. the raw design matrix;
2. the matrix used only for rank/conditioning diagnostics;
3. the transformed matrix actually used for fitting and prediction;
4. the centering/scaling moments and whether they are estimated on training rows only;
5. the columns penalized by ridge and the fixed penalty value;
6. the condition-number/rank formula and tolerance.

If M2 is meant to preserve the committed model implementation, specify its existing fitting matrix and penalty exactly and describe the standardized matrix only as a separate diagnostic unless a fit change is explicitly adopted and approved. M1 and M3 require their own complete fitting definitions. A condition gate on an unweighted, standardized proxy must not be conflated with the outcome-weighted, penalized fitting operator.

The M2 κ_eff proposal also requires a clear statement about what it does and does not identify. A diagnostic condition number does not change a predictive loss estimand into a coefficient-contrast estimand.

## D6. Narrow the “well-specified baseline” statement

The DGP's latent fixed-effect component (m(x)=\theta_0+\theta_1x) is represented in the baseline RCS basis because (x=\log(1+k)) is itself a basis column. However, the DGP also adds body and suite random effects (u_i+v_j), while the fitted model described in the document does not include those effects. Integrating over the random effects generally does not preserve an ordinary logistic model with the same linear predictor.

**Required change to §9.1:** Replace the broad claim “Baseline is well-specified” with:

> The latent structural fixed-effect component (m(x)=\theta_0+\theta_1x) lies in the baseline RCS span. Body and suite random effects are present in the outcome-generating process but omitted from the stated fitted model; therefore, correct specification of this latent fixed-effect component does not establish that the fitted likelihood is correctly specified for the marginal observed outcomes. Phase 1 assesses performance under this declared random-effects environment and does not establish robustness to alternative baseline/marginal-model misspecification.

Retain the no-robustness-claim limitation unless an additional misspecification scenario is deliberately designed and approved before freeze.

## Verification and release conditions

Before Revision D can be presented for freeze review:

- [ ] Apply D1 and label the per-bucket table as a proxy unless the global-event calculations are added.
- [ ] Apply D2 using wording that agrees with every table row.
- [ ] Resolve O3 and define evaluability of Phase 1 cells before running simulations.
- [ ] Make G6a/G6b and their coverage-truth definitions internally consistent.
- [ ] Specify diagnostic vs fitted matrices and penalty behavior per M-option.
- [ ] Narrow the baseline specification claim.
- [ ] Re-run document-level arithmetic/table checks and the portable script/test suite from the exact staged tree; record full SHA-256 digests.
- [ ] Preserve the no-freeze/no-authorization posture. Do not infer approval from this correction record.

## Repository handling

This is an additive reviewer record on a separate branch. It does not amend the committed 2026-10-14 baseline design, resolve Foued's owner decisions, modify any prior audit, or authorize computation or data collection. The supplied Revision D draft and its script package were not found in the published GitHub branches at review time, so their claimed hashes and local test results remain unverified here.
