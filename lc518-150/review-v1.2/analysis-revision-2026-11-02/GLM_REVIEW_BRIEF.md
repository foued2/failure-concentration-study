# GLM Independent Review Brief: LC518-150 Analysis Revision

**Review target branch:** `gpt/lc518-150-analysis-review-2026-11-02`  
**Scope:** independent scientific, mathematical and specification review only.  
**Status:** review material; not frozen and not authorization to modify the repository or generate study data.

## 1. Purpose

Independently challenge the revised LC518-150 analysis plan before it is treated as the design of record. Do not simply confirm GPT/Claude conclusions. Recalculate important claims, look for counterexamples, identify missing assumptions and report substantive disagreements.

The owner approved the research direction and analysis plan. The remaining task is to verify mathematical/statistical coherence and consistency with the frozen task, bank and parent designs.

## 2. Files to inspect

Review all files in this directory:

1. `ANALYSIS_SPEC_REVIEW_DRAFT.md` — primary review target.
2. `WORK_ORDER_AMENDMENTS_REVIEW.md` — proposed changes to the historical work order; no official work-order file is replaced here.
3. `MECHANICAL_DRY_RUN_REPORT.md` — scope and limits of the artificial mechanics test.
4. `mechanical_dry_run.py` and `mechanical_dry_run_results.json` — artificial fixture test and recorded output.
5. `spline_basis_check.py` and `spline_basis_check_results.json` — independent-style rank calculation for old, primary and proposed sensitivity count bases.
6. `README.md` and `SHA256SUMS` — package index and integrity digests.

Also inspect these unchanged public source documents on the same branch:

- `lc518-150/LC518_TASK_CONTRACT.md` (blob `5ca6fc69b9382300a93318bee853232a409c158f`).
- `lc518-150/glm-handoff/BANK_DESIGN.md` (blob `d91b8dcee05808926262c3636a891b776c03ab44`).
- `lc518-150/glm-handoff/PARENT_DESIGN.md` (blob `fd15338bd511ba479e62efa50ada9d2d233e143a`).
- `lc518-150/GLM_WORK_ORDER.md` v1.0 (blob `1322d82aeb8d4bd93b69cb01c43f728ae754f529`).

These four documents are context and constraints, not to be edited. The historical v1.0 work order contains a broad construction authorization in its header; the owner's later, narrower instruction supersedes that permission for current operations. The proposed amendments preserve the historical file and explain the intended authorization precedence.

Read-only repository context: `master` was at `b01b160e64190b27897e6461ed8226cafc3df67b` when checked. Its recursive tree did not contain an `lc518-150/` subtree. The LC518 v1.0 work order and frozen design documents are on the LC518 development/review branch, not at that path on master.

## 3. Source-design facts to verify

- `BANK_DESIGN.md` defines 64 diagnostic records, eight strata D1–D8 with eight records each. Hence the design-implied maximum is `k_fail=64`, because each record contributes at most one definite FAIL.
- D6 contains reorder pairs. Their records are separate rows but share the same canonical mathematical instance; dependence must be disclosed.
- `PARENT_DESIGN.md` defines 30 parent groups across five algorithm families: K1=7, K2=8, K3=8, K4=5, K5=2. K5 is sparse at the parent-group level.
- Each parent contributes five matched solver variants. The validation/interpretation grouping level is 30 parent groups, not 150 independent bodies.
- The held-out target is the declared 80-record bank. Strict E3 requires all 150 × 80 = 12,000 outcomes resolved.

Verify these facts directly against the source documents.

## 4. Required independent checks

### A. Concentration definition and support

Verify `f_j` as the number of definite FAIL outcomes in diagnostic stratum D_j, `k_fail=sum(f_j)`, and `C_D=max(f_j)/k_fail` for k_fail>0, with the labelled NO OBSERVED FAILURES convention at k_fail=0.

Check that unresolved records are excluded from f_j and k_fail and counted separately. Verify possible values at k=1,2,3. Assess how D6 pair dependence affects support and interpretation. Confirm that C_D is not the old six-family statistic.

### B. Primary spline and ridge

Independently derive the rank and coefficient mapping for:

`B(k)=(k,(k-1)+,(k-2)+,(k-3)+,(k-4)+,I[k=0])`.

Check:
- rank 5 for k=0,1,2,3,4;
- fitted-value mapping at those five levels and the extra tail-slope degree of freedom;
- rank 4 for the earlier {1,2,4} basis;
- why saturation applies only before standardization/regularization;
- why I[k=0] is standardized, no longer a raw 0/1 column;
- linear continuation above k=4 as a fixed assumption.

Check the objective: mean squared loss plus alpha times the sum of squares of every non-intercept coefficient. The intercept alone is unpenalized. Numeric predictors use training-only population means/SDs; family dummies remain binary and unstandardized. Alpha is separately selected for A, B and C from {0.1,1,10,100}. Assess whether the normalization and alpha scale are unambiguous and coherent with standardized features and Q in [0,1].

A-versus-B compares separately tuned regularized procedures. Shared baseline coefficients can receive different shrinkage in A and B. It is not an unrestricted conditional effect of C_D. Do not call it categorically conservative without proof.

### C. Proposed sensitivity basis

The proposal adds knots {8,16,32,48} to {1,2,3,4}. This is a 10-column basis over the design-implied range k=0..64. The rationale is fixed before outcomes: 8,16,32 are doubling landmarks, and 48 is three-quarters of the upper bound, leaving 48..64 as the final segment. A knot at 64 adds no variation because (k-64)+ is zero over the whole allowed range.

Assess whether this set is defensible, full-column-rank over integer k=0..64, and useful as a secondary A_sens-versus-B_sens check. Check that it remains secondary, separately reported, and cannot replace the primary result after seeing outcomes. The knot set is proposed for review, not frozen.

### D. Fold-specific support audit and preprocessing

Check the training-only standardization and zero-variance rule. For every outer and inner training split, the specification requires:
- observed k_fail values and range;
- training variance, mean and scale for every spline column and numeric feature;
- exact unseen/out-of-range validation k_fail and C_D values;
- zero-variance columns whose held-out original values differ from the training constant;
- affected body counts and distinct parent groups;
- training-unseen families and all-zero UNKNOWN encoding.

Assess whether this audit is operational and sufficiently precise. A held-out value that differs from a training constant mapped to zero is unsupported by the fitted representation, not successfully adjusted.

### E. Parent-family encoding and nested folds

Check the all-training-family one-hot encoding with an intercept, unstandardized and penalized family indicators, and all-zero encoding for absent families. At finite alpha, an unseen family's prediction is intercept plus other predictor contributions. As alpha tends to infinity, all slopes tend to zero and the intercept tends to the training outcome mean.

Inspect K1–K5 group counts and round-robin buckets. Determine exactly when K5 can be absent from an inner-training split because it has only two groups. Verify that such folds are reported and no K5 effect is claimed as learned without K5 training support.

### F. Features, outcomes and leakage

Check:
- A = flexible k_fail basis + k_unresolved + Z;
- B = A + C_D;
- C = A + the pre-registered per-stratum outcome profile;
- A-vs-B tests concentration relative to A;
- A-vs-C tests the full profile relative to A, **not** incremental profile value beyond C_D;
- sealed mutation identity, mutation details and version roles are excluded as predictors;
- raw oracle answers are excluded, while oracle labels and registered derived diagnostic deviations are permitted.

Challenge whether Model C categories PASS, wrong answer, invalid return type and exception are mutually exclusive and exhaustive of all possible definite FAIL manifestations in the work-order schema. If not, identify the missing category. Also assess whether a zero deviation-summary convention can be confused with a measured zero.

### G. Scoring and estimability

Check the 30 outer leave-one-parent-group-out folds and five inner group-wise folds, deterministic assignment, no parent leakage, tuning and preprocessing boundaries. Confirm pooled body-level MSE equals the equally weighted mean of group MSEs because each group contributes five bodies. Ensure no inference treats 150 bodies as independent; the grouping level is 30 parents.

Check strict E3: if any of 12,000 held-out outcomes is unresolved, E3 is NOT_ESTIMABLE, with coverage/bounds descriptive and no resolved-only model fit. The primary matched analysis retains its own separate unresolved rule.

### H. Authorization and document consistency

Compare the proposed amendments against v1.0. The old document must remain unchanged; later owner instruction narrows current permission to specification review and artificial-fixture testing. Production bank generation, solver construction, private-annex access, candidate execution and predictive fitting remain separately unauthorized. Review-only branch publication does not authorize production artifacts or merge.

Check consistency with the task contract, BANK_DESIGN and PARENT_DESIGN.

## 5. Required response format

Return a written review with five headings:
1. **BLOCKERS**
2. **MAJOR CONCERNS**
3. **MINOR/EDITORIAL**
4. **CONFIRMED**
5. **UNTESTED / NOT IDENTIFIABLE FROM DESIGN**

For every finding, identify the exact file/section, explain why it matters, show the independent calculation or counterexample, and propose a correction where possible. Do not edit the repository.

## 6. Review boundaries

- Inspect only the public specifications, source design documents and artificial fixture files listed above.
- Do not access or request the private mutation annex or sealed ground-truth manifest.
- Do not generate study banks or any LC518 study records.
- Do not construct, import or execute any candidate solver body.
- Do not fit predictive models or run power simulations.
- Do not treat a synthetic basis check or the 7/7 artificial mechanics pass as evidence about actual generator correctness, bank feasibility, solver behaviour or predictive performance.
- Do not commit, push, merge or edit repository files.
