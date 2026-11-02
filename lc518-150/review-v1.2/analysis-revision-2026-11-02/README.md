# LC518-150 analysis review package (2026-11-02)

**Status:** Review-only revision 2.1, published on the dedicated analysis-review branch. This is not the frozen design of record and does not authorize study generation or execution.

**Repository authorship:** Under the owner's 2026-11-02 instruction, GPT is the sole agent authorized to publish or otherwise modify repository contents under this delegation. Claude and GLM are reviewers only.

## Current contents

- ANALYSIS_SPEC_REVIEW_DRAFT.md: consolidated analysis specification, including the restored C6/C7 features, the complete frozen-to-revised feature reconciliation, proposed concentration-support floor and sensitivity knots pending owner confirmation, fixed folds, pooled inner alpha selection and K5 caveats.
- WORK_ORDER_AMENDMENTS_REVIEW.md: corresponding authorization, feature-inventory, oracle, unresolved-outcome, fold/scoring and interpretation amendments.
- MECHANICAL_DRY_RUN_REPORT.md: artificial-fixture test scope, results, limitations and an explicit mapping from its 13 report rows to seven JSON test groups.
- mechanical_dry_run.py and mechanical_dry_run_results.json: reproducible standard-library-only artificial-fixture checks. They are not the production/study generator.
- spline_basis_check.py and spline_basis_check_results.json: artificial-only rank checks for the old, primary and proposed sensitivity count bases.
- GLM_REVIEW_BRIEF.md: updated independent-review request for the consolidated revision.
- SHA256SUMS: SHA-256 content digests for the nine package files other than the checksum file itself.

## Revision 2.1 status: settled corrections and open proposals

The revision restores the three D6 C6 order features; restores per-stratum unresolved counts, the deviation-defined indicators and coverage_diag reporting; restores d_other_s and the reserved d_timeout_s field; and specifies that a null reserved field is excluded from the matrix rather than zero-filled. These corrections are incorporated in the review draft.

Two design choices remain open pending owner confirmation. First, the proposed concentration interpretation support floor is three distinct parent groups. A group qualifies only when at least two of its five versions differ in C_D within the same exact (k_fail, k_unresolved) cell with k_fail >= 2. This tests variation beyond both aggregate baseline counts. Three groups is proposed as a minimum support safeguard, not a power or precision guarantee. Second, the proposed sensitivity knots are {1,2,3,4,8,16,32,48}; they are not frozen. Both choices must be confirmed or changed before any outcomes are observed.

Parent IDs are public. The numeric G01–G30 order and exact five inner buckets are pinned in the analysis specification. The alpha-tuning criterion is one pooled MSE over the 145 inner-validation bodies, not an average of five fold means. K5's two-parent support limitation is explicitly documented.

## Master/review-branch divergence

The earlier review brief incorrectly stated that master had no LC518 subtree. Master HEAD b01b160 contains lc518-150/review-v1.2/c9-dryrun/REPORT_C9_DRYRUN.md with blob SHA 3ff9bf170bae0d28f3a74f30bc172ef6e996df32. The copy on this review branch has blob SHA e7228c89e4b9fd7f7aa4ac9fa11e140fdd5b9711 and includes the process note. The master copy is left untouched; this revision does not revert or delete it.

## Limits

The dry run uses only out-of-contract synthetic sentinel fixtures and disposable seeds. It does not validate the actual repository generator. The basis checks use integer feature values only, not solver outcomes or study records. No LC518 diagnostic or held-out bank was generated; no candidate body was constructed, imported or executed; no private mutation annex was accessed; no predictive model was fitted; no power study was run.

This branch does not freeze the analysis specification, modify the official work order, authorize bank generation, authorize construction/execution of the 150 solver bodies, authorize private-annex access or predictive fitting, or authorize a merge to master. The original v1.0 source documents remain unchanged.
