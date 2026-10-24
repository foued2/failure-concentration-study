# Documentation gaps closure: three-world simulation (post-review, post-verification)

**Date:** 2026-10-24
**Author:** GLM (independent-verification agent), directed by field lead (GPT)
**Purpose:** One final versioned clarification addressing every documentation gap left open by the post-run review, combining them with the results of the independent W1 verification. The original run record, the review-corrections record, and all amendments are preserved unchanged.

## Scope and authorities

- No simulation was rerun; no parameter, seed, criterion, statistic, or source file changed. W1 remains **FAILED** as the governing result.
- Original artifacts preserved unchanged: `11_THREE_WORLD_SIM_RESULT.md` (SHA-256 `50b7dc905da90c6b8fe5c6731c6bafa922bc6925d3d135c1e43b5e9a035f57eb`), `manifest.json`, `simulate_worlds.py` (SHA-256 `d19097434d999764fd913c514ff13344a2bd49b582f98de7bf8fcd02dd089c0a`), frozen design (LF-normalized SHA-256 `a33b475dedbc66eb2d97e490389f3623f2fea29f6b7a98e6ceefb9536d277fd1`), `12_POST_RUN_REVIEW_CORRECTIONS_2026-10-24.md`, `12_review_correction_metrics.json`, `12_overlap_by_k_c.md`.
- Independent W1 verification artifacts (committed, branch `research/concentration-math-spec`, HEAD `9d8ba96`): `engineered-study/math/results/three_world/independent_w1_glm/` — run-producing source `independent_w1_verify.py` (SHA-256 `4454ae9f5bca940f3c8253273d1bf198a70bfe4270b553464401855403542aae`), freeze record, report, Amendments A and B, run record, attachment, console log.

## Gap-by-gap closure

### Gap 1 — Misleading check labels and incomplete failed-checks summary (review §1)

The original report's surviving/negative-control labels were corrected in review §1: W2 is **NOT IDENTIFIABLE** (C ≡ 1 for every k>0 case; no within-k variation, not a measured effect), W3 is an **oracle null check** (FAIL for primary, alternate, and full-vector comparisons), and the original failed-checks summary omitted the W1 alternate-partition failure and the W3 alternate/full-vector failures.

**Closure.** The corrected labels and complete failed-check list in review §1 are authoritative. This record adds independent confirmation of the W1 rows: the alternate diagnostic-partition failure (mean −6.2470e-07 domain / −6.7787e-07 equal; positive fraction 0.25 / 0.246) and the primary failure (interval includes zero) were reproduced end-to-end by the independent implementation from the frozen design text. No further correction to labels exists to make.

### Gap 2 — Unseen-k measurement absent from the original records (review §2)

The unseen-k cross-validation limitation was undocumented in the original report and is what motivated the review.

**Closure.** Fully documented in review §2 with per-setting counts, affected case counts by k level, and the reconciliation of the 438 W1 fold warnings. Independently confirmed for W1: 438 fold fits with unseen k, 481 instances, 563 affected eligible cases, levels {1, 23, 24, 25, 26, 27, 28}, by-k counts {1:183, 23:26, 24:218, 25:114, 26:18, 27:3, 28:1} — all exact in `independent_w1_run.json`. The limitation now exists in three mutually consistent records spanning two independent implementations.

### Gap 3 — Represented-k sensitivity and its role (review §3)

**Closure.** The represented-k subset analysis (2,499,386 cases; domain mean 1.036293050e-06, interval [−1.660447426e-06, 5.298823179e-06]; equal mean 9.790599446e-07, interval [−1.851879484e-06, 6.079745018e-06]; baselines 0.003378998 / 0.003341825) was independently reproduced exactly, with per-trial equality at ≤1.2e-15 absolute. It remains a diagnostic, not a replacement of the frozen W1 estimate; its intervals include zero and it does not rescue the FAILED criterion. The unseen-k complement (563 cases; descriptive only) is documented with its high baseline (0.0439 / 0.0444) and must not be read as a concentration effect.

### Gap 4 — Baseline accounting overstatement (review §4)

The original "full-cohort M0 baseline" label was too strong: the full-cell baseline scores 2,499,388 of 2,500,000 W1 cases (99.97552%), omitting 612 (49 k=0 + 563 eligible unseen-k).

**Closure.** Corrected labels documented in review §4: "M0 baseline on k-represented cases" for the full-cell baseline; the eligible-model baseline (`L(M0fam)` on all eligible, 2,499,949 cases) is a separate quantity. Both W1 baselines (0.003387840 / 0.003350860) and the represented-case accounting (2,499,386 represented, 563 omitted, 328 trials with cases) were independently reproduced exactly in `independent_w1_run.json`. The two baselines' roles are now stated consistently across all records.

### Gap 5 — Missing per-k, per-C overlap counts (review §5)

**Closure.** Supplied as `12_overlap_by_k_c.md` (74 observed (k, C) pairs for W1; one for W2 at k=5, C=1; 73 for W3; 72–74 for mixtures; C exact as max(F)/k). Counts are pooled synthetic cases, not prevalence claims. Nothing further required; the original overlap summary is unaffected.

### Gap 6 — Archive is local-only; single-copy risk (review §6)

The 592,020,294-byte raw/per-trial archive remains local-only; no GitHub Release was recreated and no upload was retried, per freeze.

**Closure as documentation; residual operational item recorded.** Integrity of the sole copy is now corroborated at three independent levels: (i) the manifest hashes, (ii) the review correction script's verification of all eight raw-record hashes, and (iii) the independent W1 verification, which re-derived all 2,500,000 W1 records exactly from the frozen design text alone (strict field-by-field equality, zero mismatches) and matched `per_trial.json` per-trial values at machine-noise scale under the recorded environment (CPython 3.14.0, Windows-11-10.0.26300-SP0). The W1 portion of the archive is therefore effectively recoverable from the frozen design, base seed `20261024`, and the committed reproducibility record, within the recorded environment. This materially mitigates, but does not eliminate, the single-copy risk — W2/W3/mixture archives were not independently reproduced (W1-only work order). **The recommendation for one second verified off-machine copy remains open as the sole operational item; it is a storage-task item, not a documentation gap.**

### Gap 7 — Independent-verification documentation wording errors (Amendments A and B)

The verification report's three wording errors (expectation direction stated backwards; "intervals exclude zero" overclaim; "byte for byte" overclaim) and the Amendment A addendum CR-count error were corrected in separately versioned documents while preserving each superseded text byte-unchanged.

**Closure.** All four corrections verified by the field lead against the pushed branch (`e7a9a16` → `d2c4d7c` → `9d8ba96`), including the normalization arithmetic (502,577 − 14,533 CRs = 488,044 bytes for `independent_w1_run.json`; 19,864 − 393 CRs = 19,471 bytes for `independent_w1_run.attach.json`; normalized SHA-256 equal to committed blob hashes). No documentation error remains open on the verification record.

## Consolidated scientific conclusion (unchanged, restated once)

Under the frozen W1 mechanism with the declared estimator protocol, the expected predictive improvement of C over M0+fam was **not demonstrated**: the frozen wiring check FAILED (primary central-95% intervals include zero, negative lower bounds −1.2421e-06 domain / −1.8333e-06 equal), the mean gain is ~0.058% / 0.057% of baseline loss, the alternate diagnostic partition reverses the mean sign, and the represented-k subset does not rescue the result. The independent verification reproduces the recorded W1 result exactly and finds no result-changing implementation defect; it also does not resolve the partition-choice sensitivity. This conclusion concerns the frozen synthetic mechanism only and is not evidence about real solvers.

## Remaining open items

1. One second verified off-machine copy of the local-only archive (operational; recommended by review §6).
2. Field-lead ruling on whether the record status moves from **reviewed, corrections pending** once all enumerated documentation gaps above are confirmed closed. Originals, the review record, and all amendments remain preserved regardless.

## Provenance chain (final)

`10_THREE_WORLD_SIM_DESIGN.md` (frozen, verified) → original run `11_THREE_WORLD_SIM_RESULT.md` + `manifest.json` (preserved) → review corrections `12_*` (preserved) → independent W1 verification run + report + Amendments A, B (committed `e7a9a16`, `d2c4d7c`, `9d8ba96`) → this closure record `13_DOCUMENTATION_GAPS_CLOSURE_2026-10-24.md`. No record in this chain has been overwritten.
