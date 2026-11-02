# Proposed Work-Order Amendments: LC518 150-Body Study

**Revision:** Consolidated review revision 2.1, 2026-11-02  
**Status:** Review-only addendum proposal. It does not modify or replace historical GLM_WORK_ORDER.md v1.0. This copy is published on a dedicated review-only branch for independent reconciliation.

This note identifies the amendments needed to reconcile the historical work order and frozen v1.0 analysis inventory with the revised research direction and ANALYSIS_SPEC_REVIEW_DRAFT.md revision 2.1. It does not itself authorize study implementation.

## 1. Authorization precedence and repository authorship

Add a dated owner-authorized addendum stating:

- The broad construction permissions in GLM_WORK_ORDER.md v1.0 are historical and are superseded for current operations by the owner's later, narrower instructions.
- Current permission includes drafting/review of the revised specification, the narrowly scoped artificial-fixture mechanical dry run, and publication of review artifacts on the designated review-only branch.
- GPT is the sole agent authorized by the owner to publish or otherwise modify repository contents under this delegation. Claude and GLM are reviewers; they may inspect and return findings but must not edit, commit, push or merge.
- Current permission does not cover generating either study bank, constructing any of the 150 solver bodies, accessing the private mutation annex, executing candidates, dynamically validating mutations, fitting predictive models, running a power study, or publishing study/production artifacts.
- The v1.0 document itself remains preserved unchanged. The precedence note is a separate dated addendum; do not silently rewrite the historical authorization statement.

## 2. Replace Work Order §10 with the revised analysis specification

Use ANALYSIS_SPEC_REVIEW_DRAFT.md revision 2.1 as the proposed replacement or referenced analysis specification. The revised §10 must include:

- three arms A/B/C and the two separate comparisons A-versus-B and A-versus-C;
- the eight-stratum definition of C_D, the NO OBSERVED FAILURES convention, and the general support bound;
- the primary six-column k_fail basis with knots 1, 2, 3 and 4, distinguishing its pre-regularization rank/saturation property from the regularized fitted model;
- the accepted per-stratum diagnostic feature inventory, including unresolved counts, deviation-defined indicators, other-manifestation counts, and D6 order-invariance features;
- the reserved timeout/resource count column, null and excluded from the design matrix until a separately authorized execution protocol and pre-run feature freeze exist;
- coverage_diag as a report-only aggregate, excluded from the design matrix because it is an affine function of k_unresolved;
- training-fold-only population standardization, zero-variance handling, the explicitly mean-normalized ridge objective, unpenalized intercept, fixed alpha grid and separate alpha selection for A/B/C;
- unseen-family all-zero encoding and the training-mean limit as alpha tends to infinity;
- the public numeric G01–G30 ordering, exact five inner buckets, the K5 sparse-support consequences, and the pooled 145-body inner alpha-selection rule;
- 30 outer leave-one-parent-group-out folds, pooled outer body-level MSE, equal parent-group summary and 30 paired group differences;
- global, conditional, parent-group, outer-fold and inner-fold concentration/support audits, including the proposed minimum of three distinct parent groups with within-parent variation at identical (k_fail, k_unresolved) and k_fail >= 2; this numerical threshold and matching criterion remain pending owner confirmation;
- the fixed secondary A_sens-versus-B_sens basis with knots 1, 2, 3, 4, 8, 16, 32 and 48, and fold-specific reporting of unsupported or zero-variance high-k hinges;
- the strict E3 all-12,000-resolved rule; and
- the distinction between raw oracle answer values (excluded predictors) and registered derived diagnostic features (permitted in Model C).

The B-versus-B+profile comparison is not part of this design. Do not call that hypothetical comparison B-versus-D.

## 3. Reconciliation of the frozen feature inventory

The following is the required frozen-to-revised mapping. It records the dispositions in ANALYSIS_SPEC_REVIEW_DRAFT.md revision 2.1 and prevents silent dropping or redefinition.

| Frozen v1.0 item | Revision 2 disposition | Required treatment |
|---|---|---|
| d_pass_s | Retained | Model C predictor for each D1–D8 stratum. |
| d_wrong_answer_s | Retained | Model C predictor for each stratum. |
| d_invalid_return_s | Retained | Model C predictor for each stratum. |
| d_exception_s | Retained | Model C predictor for each stratum. |
| d_unresolved_s | Restored | Per-stratum unresolved/coverage count; included in Model C, never in k_fail. |
| d_meandev_s | Retained with C4 convention | Zero when undefined, accompanied by d_meandev_s_defined. |
| d_meandev_s_defined | Restored | Model C predictor indicating that a wrong exact-int output exists in the stratum. |
| d_maxdev_s | Retained with C4 convention | Zero when undefined, accompanied by d_maxdev_s_defined. |
| d_maxdev_s_defined | Restored | Model C predictor indicating that a wrong exact-int output exists in the stratum. |
| d_other_s | Added under accepted C5 | Other explicitly defined FAIL manifestations, excluding timeout/resource breach. |
| d_timeout_s | Restored as reserved | Null and excluded from the matrix until a separately authorized protocol defines runtime/memory limits and timeout/resource classification, with the feature list frozen before candidate runs. |
| d_order_pairs_resolved | Restored under accepted C6 | D6 pair count; both orderings resolved PASS/FAIL, any manifestation. |
| d_order_pairs_comparable | Restored under accepted C6 | D6 pair count with both outcomes resolved and both returned values exact-int; denominator for descriptive rate. |
| d_order_inconsistent | Restored under accepted C6 | D6 comparable-pair count whose returned integers differ; included with its denominator. |
| k_fail | Retained | Total definite diagnostic FAIL count across all registered manifestations. |
| k_unresolved | Retained | Total diagnostic UNRESOLVED count. |
| family Z | Retained | Prespecified parent algorithm family context. |
| coverage_diag | Restored as report-only | Resolved diagnostic records / 64 = 1 - k_unresolved/64; exclude from predictors. |
| Reserved timeout/resource per-stratum count obligation | Restored explicitly as d_timeout_s | Null now; never zero-filled while reserved. |

For a null reserved column, exclusion from the current design matrix is mandatory; null must not be converted to zero. A zero-variance numeric column that is actually present is different: after training-only preprocessing it maps to zero in both training and validation rows and remains in the declared feature schema and support audit.

The accepted C4, C5, C6 and C7 corrections are represented. The D6 order-pair rate is descriptive only and is null when its denominator is zero; it is never imputed as zero. coverage_diag is reported but excluded from every predictive design matrix because it duplicates k_unresolved affinely.

## 4. Oracle and manifestation wording

No oracle prohibition is being replaced. Preserve the v1.0 distinction: oracle implementations may be used to establish expected outputs; candidate solvers remain outside oracle-only checks; raw expected-answer values and raw oracle outputs are not predictive columns. The registered derived outcomes and deviation summaries may be used exactly as predeclared.

The typed manifestation record remains authoritative. Current registered manifestations include wrong answer, invalid return type, exception, and other explicitly defined status. Timeout/resource breach cannot be classified until a separate execution protocol fixes budgets and rules. The reserved d_timeout_s column remains null and outside the matrix until that gate is satisfied. All definite FAIL manifestations must contribute to k_fail and the corresponding stratum f_j.

A wrong numerical answer eligible for deviation summaries must have exact Python type int and differ from the expected value. bool does not qualify. Its absolute deviation is at least 1, making the accepted zero sentinel for undefined mean/max deviation unambiguous when accompanied by the defined indicators.

## 5. Unresolved held-out outcomes

Record the strict C8/E3 rule: E3 is estimable only if every body has a resolved outcome on every held-out record. If any of the 12,000 body-by-held-out-record outcomes is unresolved, E3 is NOT_ESTIMABLE, with coverage and worst/best correctness bounds reported descriptively. Do not fit on a resolved-only subset. Preserve the primary matched analysis's separate unresolved-outcome rule.

## 6. Held-out-first disclosure

State that the held-out-first collision policy is the selected design direction, subject to review/freeze of the complete protocol. The accepted diagnostic bank is conditional on the frozen held-out bank. The two accepted banks are not statistically independent samples. Realized rejection counts must be reported for all D1–D8 and H1–H8 strata, including zeros, with sidecar reconciliation and a final canonical-disjointness check.

## 7. Fold, support and scoring clarifications

- Sort the published IDs numerically as G01–G30 and use the exact five buckets in ANALYSIS_SPEC_REVIEW_DRAFT.md revision 2.1. The IDs are public, not opaque.
- K5 comprises only G29 and G30. In exactly two of the 150 inner split instances, K5 is absent from the inner-training partition; in outer refits holding G29 or G30, only one K5 parent group remains in training. Do not claim a generalizable K5 family effect. Record the sparse-group and fixed-penalty shrinkage limitations.
- Inner alpha selection pools all 145 inner-validation body predictions across the 29 outer-training groups and computes one body-level MSE. Because every parent contributes five bodies, this equals the unweighted mean of the 29 group MSEs. Do not average the five fold-level MSEs.
- The proposed three-parent minimum support rule is an operational support floor, not a power or precision guarantee, and is pending owner confirmation. A parent qualifies only if its five versions contain at least two distinct C_D values in an exact (k_fail, k_unresolved) cell with k_fail >= 2. If the owner confirms this rule and fewer than three parent groups qualify, report Delta_AB descriptively and label concentration-specific interpretation INSUFFICIENT_WITHIN_PARENT_SUPPORT. If the owner chooses another threshold or matching criterion, update this rule before outcomes are observed.
- The two outer deltas share Model A and are correlated comparisons, not independent replications.

## 8. Interpretation language

- The primary low-count spline is saturated only as an unstandardized, unpenalized basis representation. The fitted regularized model is not saturated.
- Every numeric predictor, including the zero-failure indicator and defined flags, is standardized from training-partition statistics. Family indicators remain unstandardized.
- Zero-variance numeric columns map to zero in both training and validation rows and remain reported. Reserved null columns are excluded, not zero-filled.
- A-versus-B compares separately tuned regularized procedures. It is not an unrestricted conditional effect of C_D, and "conservative" must not be used without a separate derivation.
- A-versus-C compares the full diagnostic profile with A. It does not test the incremental contribution of the profile after C_D.
- The extended-knot sensitivity with knots {1,2,3,4,8,16,32,48} remains a proposal pending owner confirmation. If confirmed before outcomes are observed, it is a fixed pre-outcome sensitivity. Its additional high-k hinges may have zero variance in many folds; this must be reported and must not prompt post-hoc knot changes.
- Model C count columns have exact collinearities with k_fail and k_unresolved. Ridge predictions remain uniquely defined under the specified penalty, but individual coefficients are not independently interpretable. Report predictions and deltas, not coefficient narratives.
- The 150 body predictions are clustered within 30 parent groups. Do not treat them as 150 independent observations.

## 9. Mechanical dry-run report row mapping

The mechanical dry-run report has 13 human-readable check rows, while the machine-readable result records seven top-level test groups. The report must explicitly map them as follows:

| Human-readable report row | JSON top-level test group |
|---|---|
| C_D calculation | cd_and_spline_math |
| k_fail basis | cd_and_spline_math |
| Training-only standardization | training_only_standardization |
| Unseen-family encoding | unknown_family_encoding |
| MSE weighting | mse_weighting |
| Canonical identity | canonical_collision_and_rejection_accounting |
| Whole-candidate collision rejection | canonical_collision_and_rejection_accounting |
| Within-bank permutation pair | canonical_collision_and_rejection_accounting |
| Cross-bank disjointness | canonical_collision_and_rejection_accounting |
| Fixed D5 exclusion preflight | canonical_collision_and_rejection_accounting |
| Rejection counts / sidecar | canonical_collision_and_rejection_accounting |
| Separate PRNG streams | separate_rng_streams |
| Atomic PASS/FAIL publication | atomic_pass_fail_publication |

This is a presentation mapping only. It does not change the test script or turn artificial-fixture results into evidence about the actual study generator.

## 10. Repository divergence record

The prior GLM review brief stated that master had no LC518 subtree. That statement was incorrect. At master HEAD b01b160, the file lc518-150/review-v1.2/c9-dryrun/REPORT_C9_DRYRUN.md exists with blob SHA 3ff9bf170bae0d28f3a74f30bc172ef6e996df32. The review-branch copy of that path has blob SHA e7228c89e4b9fd7f7aa4ac9fa11e140fdd5b9711 and includes a process note about the earlier accidental master write. The master copy is intentionally left untouched in this revision; no revert or deletion is performed.

## 11. Remaining gates

No bank-generation or solver-construction authority follows from approval of the research question or analysis specification. The artificial mechanical dry run is limited to disposable fixtures outside the study package. No candidate solver source may be imported, constructed or executed during that dry run. Review-only publication does not authorize modification of design-of-record files, study/production artifact publication, private-annex access, candidate execution, predictive fitting, a power study or merge to another branch.

The historical GLM_WORK_ORDER.md v1.0, ANALYSIS_SPEC.md v1.0, BANK_DESIGN.md and PARENT_DESIGN.md remain unchanged. This revision is for Claude/GLM reconciliation only; it is not a freeze record or implementation authorization.
