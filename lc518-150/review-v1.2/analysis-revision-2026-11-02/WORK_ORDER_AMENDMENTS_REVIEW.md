# Proposed Work-Order Amendments: LC518 150-Body Study

**Status:** Review-only addendum proposal. It does not modify or replace historical `GLM_WORK_ORDER.md` v1.0. This copy is published on a dedicated review branch solely for independent review.

This note identifies the edits needed to reconcile the existing `GLM_WORK_ORDER.md` v1.0 with the approved research direction and the revised analysis specification. It is not a replacement for the historical v1.0 work order and does not authorize implementation.

## 1. Authorization precedence addendum

Add an owner-authorized addendum stating:

- The broad construction permission in `GLM_WORK_ORDER.md` v1.0 is historical and is superseded for current operations by the owner's later, narrower instruction.
- Current permission covers drafting/review of the revised specification and the narrowly scoped artificial-fixture mechanical dry run only.
- Current permission does not cover generating either study bank, constructing any of the 150 solver bodies, accessing the private mutation annex, executing candidates, dynamically validating mutations, fitting predictive models, running a power study, or pushing/committing study artifacts.
- Each of those operations requires its own later explicit owner authorization.
- The v1.0 document itself remains preserved unchanged. The precedence note is a separate dated addendum; do not silently rewrite the historical authorization statement.

## 2. Replace Work Order §10 with the revised analysis specification

Use `ANALYSIS_SPEC_REVIEW_DRAFT.md` as the proposed replacement/referenced analysis specification. In particular, the revised §10 must contain:

- three arms A/B/C and the two separate comparisons A-vs-B and A-vs-C;
- the eight-stratum definition of `C_D`, including the no-observed-failures convention;
- the primary six-column `k_fail` basis with knots 1, 2, 3 and 4, distinguishing its pre-regularization rank/saturation property from the regularized fitted model; the standardized zero-failure indicator must be described as a standardized numeric feature;
- training-fold-only population standardization, zero-variance handling, the explicitly mean-normalized ridge objective (unpenalized intercept; all other coefficients penalized), the fixed alpha grid, and the fact that alpha is selected separately for A, B and C;
- the unseen-family all-zero encoding, including its penalized-intercept interpretation and training-mean limit as alpha tends to infinity;
- 30 outer parent-group folds and five deterministic inner group folds;
- pooled body-level MSE plus the equal-parent-group summary and the 30 paired group differences;
- the global, conditional, outer-fold and inner-fold concentration/support audit, including zero-variance validation differences and family-absence counts;
- a secondary A_sens-versus-B_sens sensitivity comparison using the proposed fixed extended knot set 1, 2, 3, 4, 8, 16, 32 and 48; and
- the distinction between raw oracle answer values (excluded predictors) and registered derived outcome features (permitted in Model C).

## 3. Correct the oracle wording

Replace any sentence saying that oracle evaluation is not used. The oracle is used to establish expected outputs, label PASS/FAIL, derive held-out correctness and compute the registered numerical-deviation summaries. Raw oracle answer values are not predictor columns.

## 4. Replace the unresolved-outcome decision

Record the strict C8/E3 rule: E3 is estimable only if every body has a resolved outcome on every held-out record. Otherwise, E3 is `NOT_ESTIMABLE`, with coverage and worst/best correctness bounds reported descriptively. Do not fit on a resolved-only subset. Preserve the primary matched analysis's separate unresolved-outcome rule.

## 5. Preserve the held-out-first disclosure

State that the held-out-first collision policy is the selected design direction, subject to review/freeze of the complete protocol. The accepted diagnostic bank is conditional on the frozen held-out bank. The two accepted banks are not statistically independent samples. Realized rejection counts must be reported for all D1–D8 and H1–H8 strata, including zeros, with sidecar reconciliation and a final canonical-disjointness check.

## 6. Keep all remaining gates explicit

No bank-generation or solver-construction authority follows from approval of the research question or analysis specification. The mechanical dry run is limited to disposable artificial fixtures outside the study package. No candidate solver source may be imported, constructed, or executed during that dry run. The owner separately authorized publication of this review package on a dedicated review branch only. That review-only publication does not authorize modification of design-of-record files, push of production/study artifacts, or merge to another branch.

## 7. Explicit interpretation language to add

- The low-count spline is saturated only as an unstandardized, unpenalized basis representation. The fitted regularized model is not saturated.
- Every numeric basis column, including the zero-failure indicator, is standardized from training-fold statistics. Family indicators remain unstandardized.
- The A-versus-B result compares separately tuned regularized procedures. It is not an unrestricted conditional effect of `C_D`, and the term "conservative" must not be used without a separate derivation.
- A-versus-C compares the full diagnostic profile with A. It does not test the incremental contribution of the profile after `C_D` has entered.
- The secondary extended-knot sensitivity is proposed with knots 8, 16, 32 and 48 added to the primary set. It must be fixed before any outcome is observed and reported separately.
