# LC518-150 Artificial Mechanical Dry-Run Report

**Date:** 2026-11-02  
**Status:** Completed; artificial-fixture test only.  
**Location:** disposable temporary directory under the runtime's temporary filesystem; it was automatically deleted. The script and report are retained separately under `/mnt/data/lc518_150_review_work/`, outside the repository and study package.

## Scope

The owner authorized a mechanical dry run using disposable artificial fixtures only. This run tested a fresh, small reimplementation of selected mechanics. It did **not** execute or validate the actual study generator. The fixtures deliberately use amounts and denominations outside the LC518 contract (greater than 5,000), so they cannot be mistaken for study-bank records. Only disposable test seeds were used.

No diagnostic or held-out study bank was generated. No study records, oracle outputs, solver bodies, mutation assignments, or candidate execution results were created. No candidate code was imported or executed. The private mutation annex was not accessed. No predictive model was fitted. The dry-run process itself changed no GitHub files and performed no commit, push or merge. The report and review materials were subsequently published by a separate owner-authorized action on the dedicated review-only branch; that later publication did not change the dry-run scope.

## Results

<summary>All artificial-fixture checks passed.</summary>

| Check | Result | What was checked |
|---|---|---|
| `C_D` calculation | PASS | No-failure convention; one, two and three failures; values 1, 1/2, 2/3 and 1/3 as appropriate. |
| `k_fail` basis | PASS after correction | Six-column basis has full row rank over k=0..4 and a one-to-one mapping to five low-count fitted values plus the linear tail slope. |
| Training-only standardization | PASS | Training means/scales are used for validation values; a zero-variance training column maps to zero in both training and held-out data. |
| Unseen-family encoding | PASS | A family absent from training, including a singleton family when its parent is held out, receives all-zero family indicators and no family-specific adjustment. |
| MSE weighting | PASS | Pooled 150-body MSE equals the unweighted mean of the 30 parent-group MSEs because each group contains exactly five bodies. |
| Canonical identity | PASS | Coin-order permutations map to the same `(amount, sorted coins)` key. |
| Whole-candidate collision rejection | PASS | One colliding record rejects its entire multi-record diagnostic candidate, including its otherwise non-colliding companion. |
| Within-bank permutation pair | PASS | A permutation pair with one canonical identity is allowed within a bank. |
| Cross-bank disjointness | PASS | Accepted artificial diagnostic keys have no intersection with the frozen artificial held-out key set. |
| Fixed D5 exclusion preflight | PASS | An artificial held-out collision with a fixed D5 key is treated as a fatal contradiction, not as a routine held-out redraw. |
| Rejection counts / sidecar | PASS | Counts reconcile to sidecar rows for all 16 D1–D8 and H1–H8 stratum slots, including zeros. |
| Separate PRNG streams | PASS | Variable diagnostic-side retries do not consume or alter the independent held-out RNG stream. |
| Atomic PASS/FAIL publication | PASS | Failed validation creates no authoritative PASS file; successful validation publishes only after the predicate passes, via same-filesystem atomic replace. |

## Important mathematical correction found during testing

The earlier proposed basis with hinge terms only at 1, 2 and 4,

\[
(k, (k-1)_+, (k-2)_+, (k-4)_+, \mathbf{1}[k=0]),
\]

does **not** allow arbitrary fitted values at k=0,1,2,3,4. The term `(k-4)_+` is zero at k=4, so it cannot independently control the fitted value at k=4. A direct rank check of the 5-by-5 low-count design matrix for that earlier basis returns rank 4, not the required rank 5; the reproducible harness now checks and records that deficiency.

The review draft therefore uses knots at **1, 2, 3 and 4**:

\[
(k, (k-1)_+, (k-2)_+, (k-3)_+, (k-4)_+, \mathbf{1}[k=0]).
\]

This provides arbitrary fitted values at k=0..4 and a linear continuation for k>4. The corrected mapping from the six coefficients to the five low-count fitted values plus the tail slope has rank six. The final artificial test passed and records both the old-basis rank deficiency and the corrected-basis full-rank transformation.

This is a correction to the earlier GPT/Claude proposal and must be shown to Claude as a substantive math correction before anyone labels the specification frozen.

## Limitations

1. The actual generator source was not available to this run. The collision, RNG, accounting and publication checks test the artificial reimplementation only. They do not establish that any repository generator implements these rules correctly.
2. No production seeds, production bank candidates, fixed study records, oracle outputs, or private annex content were used.
3. This was not a bank-generation dry run and gives no evidence about expected rejection rates, quotas, realized support, or whether the real bank can be generated within its attempt caps.
4. No statistical model was fitted. The script checks the primary spline feature basis, standardization convention and weighting identities; it does not fit or validate the ridge objective or any alpha choice. It does not run the proposed fold-specific support audit or the A_sens-versus-B_sens comparison. A separate artificial-only rank-check script and JSON result are included for the proposed extended spline basis; they do not use study data.
5. No test was made of real source-body construction, mutation validity, solver correctness, runtime limits, or candidate isolation.

## Overall disposition

**Artificial mechanics: PASS (7/7 tests in the recorded run). Primary and extended basis algebra: separately checked on integer k values only. Actual generator: NOT TESTED. Ridge fitting, fold-specific support audit and predictive sensitivity fitting: NOT TESTED. Study generation and solver construction: NOT PERFORMED and remain unauthorized.**