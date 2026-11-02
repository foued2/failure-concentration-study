# LC518-150 review package (2026-11-02)

**Status:** Published on a dedicated review-only branch at the owner's request so Claude can review it. These files are proposals and test evidence, not the frozen design of record.

Contents:

- `ANALYSIS_SPEC_REVIEW_DRAFT.md`: revised analysis specification, including separate A-vs-B concentration and A-vs-C enriched-profile comparisons.
- `WORK_ORDER_AMENDMENTS_REVIEW.md`: proposed authorization-precedence and work-order amendments. The historical v1.0 work order is not modified.
- `MECHANICAL_DRY_RUN_REPORT.md`: scope, results, correction and limits of the artificial-fixture test.
- `mechanical_dry_run.py`: reproducible standard-library-only artificial-fixture test harness. It is not the production/study generator.
- `mechanical_dry_run_results.json`: machine-readable output from the 7/7 artificial mechanics run.
- `spline_basis_check.py` and `spline_basis_check_results.json`: separate artificial-only rank checks for the old, primary and proposed sensitivity count bases.
- `GLM_REVIEW_BRIEF.md`: exact independent-review scope, source documents, mathematical checks and required GLM response format.
- `SHA256SUMS`: SHA-256 integrity digests for the review materials (excluding the checksum file itself and any convenience ZIP archive).

The dry run uses only out-of-contract synthetic sentinel inputs and disposable seeds. It does not validate the actual repository generator. The basis-check script uses integer feature values only, not solver outcomes or study records. No LC518 diagnostic or held-out bank was generated; no candidate body was constructed, imported or executed; no private mutation annex was accessed; and no predictive model was fitted.

The ZIP archive is retained as a convenience download in the conversation, not versioned in this review branch. This branch does not freeze the analysis specification, modify the official work order, authorize study-bank generation or authorize construction/execution of the 150 solver bodies.
The extended count-basis sensitivity (additional knots 8, 16, 32 and 48) is a proposal for GLM review, not a frozen owner-approved analysis choice. The fold-specific support audit is specified but cannot be populated before the 150-body diagnostic outcomes exist.
