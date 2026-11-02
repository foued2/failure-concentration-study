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
- the corrected `k_fail` basis with knots 1, 2, 3 and 4, not the earlier incomplete 1, 2, 4 proposal;
- training-fold-only population standardization, zero-variance handling, the explicitly mean-normalized ridge objective (unpenalized intercept; all other coefficients penalized), and the fixed alpha grid;
- explicit unknown-family all-zero encoding for a family absent from training, with no family-specific adjustment and no averaging over known families;
- 30 outer parent-group folds and five deterministic inner group folds;
- pooled body-level MSE plus the equal-parent-group summary and the 30 paired group differences;
- the concentration-support audit; and
- the distinction between raw oracle answer values (excluded predictors) and registered derived outcome features (permitted in Model C).

## 3. Correct the oracle wording

Replace any sentence saying that oracle evaluation is not used. The oracle is used to establish expected outputs, label PASS/FAIL, derive held-out correctness and compute the registered numerical-deviation summaries. Raw oracle answer values are not predictor columns.

## 4. Replace the unresolved-outcome decision

Record the strict C8/E3 rule: E3 is estimable only if every body has a resolved outcome on every held-out record. Otherwise, E3 is `NOT_ESTIMABLE`, with coverage and worst/best correctness bounds reported descriptively. Do not fit on a resolved-only subset. Preserve the primary matched analysis's separate unresolved-outcome rule.

## 5. Preserve the held-out-first disclosure

State that the held-out-first collision policy is the selected design direction, subject to review/freeze of the complete protocol. The accepted diagnostic bank is conditional on the frozen held-out bank. The two accepted banks are not statistically independent samples. Realized rejection counts must be reported for all D1–D8 and H1–H8 strata, including zeros, with sidecar reconciliation and a final canonical-disjointness check.

## 6. Keep all remaining gates explicit

No bank-generation or solver-construction authority follows from approval of the research question or analysis specification. The mechanical dry run is limited to disposable artificial fixtures outside the study package. No candidate solver source may be imported, constructed, or executed during that dry run. The owner separately authorized publication of this review package on a dedicated review branch only; this does not authorize modification of the design-of-record files, push of study artifacts, or merge to another branch.