# GLM Independent Review Brief — LC518-150 Analysis Revision 2.2

**Date:** 2026-11-02  
**Review target branch:** gpt/lc518-150-analysis-review-2026-11-02  
**Revision base:** 8fd82566bab0eac51456081b8d97e926ab878c1e (revision 2.1); review the subsequent revision 2.2 tree on this branch.  
**Requested review:** independent mathematical and specification review of revision 2.2 after GLM's revision 2.1 findings and Claude's disposition. Verify the new provenance, precedence, manifestation-taxonomy, reporting-protection and fold-support corrections. Continue to assess M1 and the extended sensitivity knots as proposals; do not treat either as owner-approved.

## 1. Scope and limits

Review the public design/review documents listed below. Do not edit, commit, push or merge repository files. Do not access or request the private mutation annex or sealed ground-truth manifest. Do not generate study banks or LC518 study records. Do not construct, import or execute candidate solver bodies. Do not fit predictive models or run power simulations.

The artificial-fixture scripts and results are only mechanical checks. They are not evidence about the actual generator, actual bank feasibility, solver behaviour, or predictive performance.

Under the owner's instruction, GPT is the only agent authorized to publish or modify repository contents. GLM and Claude are reviewers only.

## 2. Source files

Review these files on the target branch:

- lc518-150/review-v1.2/analysis-revision-2026-11-02/ANALYSIS_SPEC_REVIEW_DRAFT.md
- lc518-150/review-v1.2/analysis-revision-2026-11-02/WORK_ORDER_AMENDMENTS_REVIEW.md
- lc518-150/review-v1.2/analysis-revision-2026-11-02/MECHANICAL_DRY_RUN_REPORT.md
- lc518-150/review-v1.2/analysis-revision-2026-11-02/mechanical_dry_run.py
- lc518-150/review-v1.2/analysis-revision-2026-11-02/mechanical_dry_run_results.json
- lc518-150/review-v1.2/analysis-revision-2026-11-02/spline_basis_check.py
- lc518-150/review-v1.2/analysis-revision-2026-11-02/spline_basis_check_results.json
- lc518-150/review-v1.2/analysis-revision-2026-11-02/README.md

Compare with the unchanged design sources:

- lc518-150/LC518_TASK_CONTRACT.md
- lc518-150/glm-handoff/BANK_DESIGN.md
- lc518-150/glm-handoff/PARENT_DESIGN.md
- lc518-150/GLM_WORK_ORDER.md
- lc518-150/glm-handoff/ANALYSIS_SPEC.md (frozen v1.0)
- lc518-150/review-v1.2/CORRECTIONS_RECORD_v1.2.2-draft.md

The historical v1.0 work order and analysis specification must remain unchanged.

## 3. Prior findings and the revision's dispositions

### B1 — D6 order-invariance features

Revision 2 restores all three accepted C6 features to Model C:

- d_order_pairs_resolved;
- d_order_pairs_comparable; and
- d_order_inconsistent.

Both the inconsistency count and comparable-pair denominator enter Model C. The rate is descriptive only and null when the denominator is zero. Verify the definitions against BANK_DESIGN §6 and CORRECTIONS_RECORD C6.

### B2 — frozen feature inventory

Revision 2 restores d_unresolved_s, d_meandev_s_defined, d_maxdev_s_defined and the coverage_diag reporting obligation. It adds the accepted d_other_s feature and provides a row-by-row frozen-to-revised reconciliation table. Verify every row against frozen ANALYSIS_SPEC v1.0 and CORRECTIONS_RECORD C4, C5 and C7.

coverage_diag = resolved diagnostic records / 64 = 1 - k_unresolved/64. It is reported but excluded from the predictor matrix.

### B3 — future timeout/resource and other manifestations

Revision 2 restores d_timeout_s as a reserved per-stratum column. It is null and excluded from the design matrix until a separate execution protocol specifies runtime/memory budgets and timeout/resource classification, with the feature list frozen before any candidate runs. Null is not zero-filled. d_other_s is separate and counts another explicitly defined manifestation, excluding timeout/resource breach.

### M1 — concentration support

Revision 2.1 proposes, but does not adopt, a fixed operational minimum: at least three distinct parent groups must each contain at least one exact (k_fail, k_unresolved) cell among their five versions with k_fail >= 2 and at least two distinct C_D values. This is stricter than merely observing a same-k difference somewhere in a group. The numerical threshold and matching criterion are pending owner confirmation; do not describe them as pre-registered or owner-approved.

Independently assess whether this proposed rule is coherent with the stated estimand, whether matching on k_unresolved is appropriate, whether three groups is too weak or too strict, and whether the proposed below-threshold interpretation is correctly limited to INSUFFICIENT_WITHIN_PARENT_SUPPORT rather than a null-effect claim. Suggest any defect or unintended consequence, but do not use outcome data or invent a power claim.

### M2 — public IDs, fixed buckets and K5

Revision 2 uses numeric G01–G30 ordering and pins these buckets:

- Bucket 0: G05, G10, G15, G20, G25, G30
- Bucket 1: G01, G06, G11, G16, G21, G26
- Bucket 2: G02, G07, G12, G17, G22, G27
- Bucket 3: G03, G08, G13, G18, G23, G28
- Bucket 4: G04, G09, G14, G19, G24, G29

K5 comprises only G29 and G30. Verify that exactly two of the 150 inner split instances have no K5 group in inner training, and that the outer folds holding G29 or G30 train with only one K5 parent group. Assess the stated limitation on K5 family interpretation and common-alpha shrinkage.

### M3 — inner alpha tuning

Revision 2 pools the validation predictions for all 145 bodies in the 29 outer-training parent groups and computes one body-level MSE for each alpha/model. Since each group contributes five bodies, this equals the equally weighted mean of the 29 group MSEs. It expressly prohibits averaging the five fold-level MSEs. Verify this is unambiguous and consistent with the fixed buckets.

### E1–E8 — corrections

- E1: the brief now records the master/review-branch divergence. Master HEAD b01b160 contains lc518-150/review-v1.2/c9-dryrun/REPORT_C9_DRYRUN.md with blob 3ff9bf170bae0d28f3a74f30bc172ef6e996df32; the review-branch copy has blob e7228c89e4b9fd7f7aa4ac9fa11e140fdd5b9711 and includes the process note. The master copy is left untouched.
- E2: the report now maps all 13 human-readable rows to seven JSON top-level test groups.
- E3: the hypothetical incremental comparison is called B-versus-B+profile, not B-versus-D.
- E4: G01–G30 are described as public IDs and numeric order is pinned.
- E5: the general C_D support bound is stated.
- E6: wrong integer outputs require exact Python type int; bool is excluded. Their absolute deviation is at least 1.
- E7: no oracle-wording replacement is proposed because the cited sentence did not exist. The existing correct oracle distinction is restated.
- E8: count-column collinearities and coefficient-interpretation limits are disclosed.

## 4. Additional independent checks for revision 2.2

Do not treat the M1 threshold or extended sensitivity-knot set as owner-approved. Report whether each is mathematically coherent and what trade-offs it creates. The owner retains the decision on whether to approve, revise or reject these two proposals.

Also specifically attack the following revision 2.2 changes:

- C8 provenance: verify that the wording says only that the strict all-12,000-resolved rule was owner-confirmed in chat on 2026-11-02. It must not imply that the whole specification was frozen or that execution was authorized.
- C9 status: verify the distinction between held-out-first as the selected design direction and the detailed C9 correction remaining pending independent review, not accepted or frozen.
- MC2 carry-over: verify the one-pass stop, all-identical-Q ZERO_VARIANCE rule, coverage/unresolved reporting in every table, and preservation of successful executions. Check that the conditional precedence clause does not supersede E1 or unaffected v1.0 provisions and has no present effect before formal ratification.
- MC3 taxonomy: verify that the pre-run other allowlist is closed and may be empty, that unmatched FAIL manifestations cause protocol abort, bool/non-exact-int returns are invalid-return-type, and timeout/resource remains outside other while its reserved column is null.
- ME2 K5: verify that the two inner splits with no K5 in training score the five validation bodies from the other K5 parent under the all-zero unseen-family representation.
- MC5 support: verify the requested fold-level rank, distinct-count, zero-count and knot-side coverage diagnostics. Check that the prose does not confuse rank-deficient support with an undefined ridge solution.
- Ridge implementation hazard: verify the stated alpha_sklearn = n_train * alpha_spec scaling under the corresponding sum-loss versus mean-loss conventions, and the requirement for a future synthetic numerical-equivalence test. Do not implement or fit a model.
- ME1–ME4: verify the deduplicated six-column basis description, K5 pooled-validation note, procedure-level reconciliation and per-stratum partition identity.

1. Re-derive the C_D bound ceil(k/8)/k <= C_D <= 1 for positive k, and check the k=1,2,3 cases.
2. Re-derive the primary six-column spline rank and coefficient mapping; check the former {1,2,4} basis rank 4; verify the candidate sensitivity basis with knots {1,2,3,4,8,16,32,48} over k=0..64. Assess its usefulness and limitations as a proposal; it is pending owner confirmation, not a frozen choice.
3. Check the mean-squared-loss plus ridge objective, unpenalized intercept, training-only population standardization, zero-variance mapping and distinction between a zero-variance column and a reserved null column.
4. Check that all three predictive arms use the same target and group folds, that alpha is separately tuned, and that the 145-body pooled inner criterion is explicit.
5. Check that the 30 outer body-level prediction scores are summarized at the 30-parent level, that Delta_AB and Delta_AC share Model A and are correlated, and that neither is a causal contrast.
6. Check strict E3: any unresolved one of 12,000 held-out outcomes makes E3 NOT_ESTIMABLE; no resolved-only subset fit is permitted.
7. Check that Model C's full profile remains pre-registered and that the D6 features, unresolved counts, defined flags, other-status count and reserved timeout field reconcile to the frozen feature inventory.
8. Inspect wording for any silent expansion of authorization. Review-only publication must not be read as authority for bank generation, solver construction, private-annex access, candidate execution, predictive fitting, power simulation or master merge.

## 5. Master/review divergence

The previous brief incorrectly stated that master had no LC518 subtree. That was wrong. The only divergence addressed here is the C9 report at the path and blob hashes above. No deletion or revert is requested. Do not modify master.

## 6. Required response format

Return a written review with five headings:

1. **BLOCKERS**
2. **MAJOR CONCERNS**
3. **MINOR/EDITORIAL**
4. **CONFIRMED**
5. **UNTESTED / NOT IDENTIFIABLE FROM DESIGN**

For each finding identify the exact file/section, explain why it matters, provide the calculation or counterexample, and propose a correction where possible. State what was actually checked and what remains untested.

Do not edit the repository. Do not infer actual support, bank feasibility, solver behaviour, alpha choice or predictive performance from the artificial fixtures.
