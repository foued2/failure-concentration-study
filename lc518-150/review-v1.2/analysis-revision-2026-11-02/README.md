# LC518-150 analysis review package (2026-11-02)

**Status:** Review-only revision 2.5, published on the dedicated analysis-review branch. It is not frozen or the design of record and does not authorize study generation or execution.

**Repository authorship:** Under the owner's 2026-11-02 instruction, GPT is the sole agent authorized to publish or otherwise modify repository contents under this delegation. Claude and GLM are reviewers only.

## Current contents

- ANALYSIS_SPEC_REVIEW_DRAFT.md: consolidated analysis specification, including the restored C6/C7 features, closed pre-run manifestation taxonomy, owner-confirmed C8 provenance, fixed three-parent exact-cell support rule, fixed sensitivity knots, fold-level support diagnostics, C9 status, four carried-forward v1.0 analysis/reporting protections, fixed folds, pooled inner alpha selection and K5 caveats.
- WORK_ORDER_AMENDMENTS_REVIEW.md: corresponding conditional-precedence, authorization, feature-inventory, closed-manifestation, oracle, unresolved-outcome, fold/scoring, future ridge-equivalence and interpretation amendments.
- MECHANICAL_DRY_RUN_REPORT.md: artificial-fixture test scope, results, limitations and an explicit mapping from its 13 report rows to seven JSON test groups.
- mechanical_dry_run.py and mechanical_dry_run_results.json: reproducible standard-library-only artificial-fixture checks. They are not the production/study generator.
- spline_basis_check.py and spline_basis_check_results.json: artificial-only rank checks for the old, primary and fixed extended-sensitivity count bases.
- C9_GENERATION_SPEC_REVIEW.md: complete, corrected and renumbered C9 held-out-first protocol, including GLM findings ME-1 to ME-6 from its revision 2.4 review; GLM found no blockers or major concerns in revision 2.4. The revision 2.5 wording remains pending owner ratification; the historical corrections record and frozen v1.0 BANK_DESIGN.md remain unchanged.
- GLM_REVIEW_BRIEF.md: focused read-only follow-up request for the six revision 2.5 C9 clarifications; M1 and the sensitivity knots remain fixed and are not reopened.
- SHA256SUMS: SHA-256 content digests for the ten package files other than the checksum file itself.

## Revision 2.5 status: fixed design choices and remaining ratification gate

The revision restores the three D6 C6 order features; restores per-stratum unresolved counts, the deviation-defined indicators and coverage_diag reporting; restores d_other_s and the reserved d_timeout_s field; and specifies that a null reserved field is excluded from the matrix rather than zero-filled. These corrections are incorporated in the review draft.

M1 and sensitivity are fixed pre-outcome design choices. For M1, a particular exact (k_fail, k_unresolved) cell with k_fail >= 2 is supported only if at least three distinct parent groups each contribute within-parent C_D variation in that same cell. A parent contributes only if at least two of its five versions fall in that cell with different C_D values; contributions across different cells cannot be pooled. The less restrictive same-k variation count remains reported alongside exact-cell support. Below the floor, the label is INSUFFICIENT_WITHIN_PARENT_SUPPORT, not a null effect. This three-parent floor is an operational support convention, not a power or precision claim. The sensitivity knots are fixed at {1,2,3,4,8,16,32,48}. Fold-level basis rank, distinct-k support, k=0 presence and hinge-side coverage remain mandatory. The report must identify which knots are STRADDLED in each fold. The set mainly tests low-count functional form; it does not guarantee evidence about high-count curvature. Neither choice may be retuned after outcomes are observed.

The strict C8/E3 all-12,000-resolved gate is recorded as confirmed by the owner in chat on 2026-11-02. The C8 status statements in `lc518-150/review-v1.2/CORRECTIONS_RECORD_v1.2.2-draft.md` (dated 2026-11-01) predate that confirmation and are superseded for C8/E3 status only by revision 2.5; the historical corrections record remains unchanged. This provenance record does not freeze the whole specification or authorize execution. For C9, GLM's focused review of revision 2.4 found no blockers or major concerns; its six minor findings are incorporated into C9_GENERATION_SPEC_REVIEW.md revision 2.5. The revision 2.5 text remains pending owner ratification and does not freeze BANK_DESIGN.md or authorize generation.

The v1.0 protections are carried forward: one frozen analysis pass only; an all-identical-Q ZERO_VARIANCE report rather than a prediction result; coverage and unresolved counts alongside failures in every results table; and preservation of successful executions as well as failures. The typed manifestation taxonomy is newly closed before any run. The other allowlist may be empty; any non-exact-int return, including bool, is invalid-return-type; and any unmatched FAIL manifestation is a protocol error, not an implicit other.

Parent IDs are public. The numeric G01–G30 order and exact five inner buckets are pinned in the analysis specification. The alpha-tuning criterion is one pooled MSE over the 145 inner-validation bodies, not an average of five fold means. In two outer-by-inner splits, the five validation bodies from the other K5 parent are scored with all-zero family indicators because K5 is unseen in inner training; include these bodies in the training-unseen-family validation count. K5's two-parent support limitation is explicitly documented.

## Master/review-branch divergence

The earlier review brief incorrectly stated that master had no LC518 subtree. Master HEAD b01b160 contains lc518-150/review-v1.2/c9-dryrun/REPORT_C9_DRYRUN.md with blob SHA 3ff9bf170bae0d28f3a74f30bc172ef6e996df32. The copy on this review branch has blob SHA e7228c89e4b9fd7f7aa4ac9fa11e140fdd5b9711 and includes the process note. The master copy is left untouched; this revision does not revert or delete it.

## Limits

The dry run uses only out-of-contract synthetic sentinel fixtures and disposable seeds. It does not validate the actual repository generator. The basis checks use integer feature values only, not solver outcomes or study records. No LC518 diagnostic or held-out bank was generated; no candidate body was constructed, imported or executed; no private mutation annex was accessed; no predictive model was fitted; no power study was run.

This branch does not freeze the analysis specification, modify the official work order, authorize bank generation, authorize construction/execution of the 150 solver bodies, authorize private-annex access or predictive fitting, or authorize a merge to master. The original v1.0 source documents remain unchanged.
