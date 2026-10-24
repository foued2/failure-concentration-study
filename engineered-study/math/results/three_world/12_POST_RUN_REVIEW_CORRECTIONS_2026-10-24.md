# Post-run review corrections: three-world simulation

**Status: reviewed, corrections pending.** This is the current review record. The original
report and manifest are preserved unchanged as the original run record; their historical
`source_review_status` is not the current status.

**Scope:** Post-run analysis of the saved synthetic records only. No simulation was rerun, no
parameter or criterion was changed, and no result was tuned. W1 remains **FAILED** and remains
the governing result.

**Original artifacts preserved:**

- Report: `11_THREE_WORLD_SIM_RESULT.md` (23,632 bytes; SHA-256 `50b7dc905da90c6b8fe5c6731c6bafa922bc6925d3d135c1e43b5e9a035f57eb`)
- Manifest: `manifest.json` (6,243 bytes; original `source_review_status` remains the historical pending value)
- Simulation: `engineered-study/math/simulate_worlds.py` (unchanged; SHA-256 `d19097434d999764fd913c514ff13344a2bd49b582f98de7bf8fcd02dd089c0a`)
- Frozen design: SHA-256 `a33b475dedbc66eb2d97e490389f3623f2fea29f6b7a98e6ceefb9536d277fd1`

**Correction inputs and outputs:**

- Correction script: `engineered-study/math/analyze_three_world_review.py`
- Metrics: `12_review_correction_metrics.json`
- Full per-k, per-C case-count appendix: `12_overlap_by_k_c.md`
- Raw records: local-only under `engineered-study/math/results/three_world/raw/`; the script verified all eight raw SHA-256 values before analysis.

The correction script reconstructs the original eligible cases from the saved raw JSONL,
reproduces each original W1 per-trial `Delta_pred` exactly (`max abs error = 0.0`), and then
computes the diagnostics below. It does not regenerate cases or alter the frozen model.

## 1. Corrected labels

The original report's "C survives" row is misleading for the negative controls. The corrected
reading is:

| Check | W1 | W2 | W3 |
| --- | --- | --- | --- |
| Primary family-adjusted C gain positive, 95% interval above zero | FAIL | NOT IDENTIFIABLE | FAIL (oracle-null check) |
| Alternate diagnostic-partition C gain positive | FAIL | NOT APPLICABLE | FAIL |
| Full vector beats C | domain PASS; equal FAIL; overall FAIL | NOT IDENTIFIABLE | FAIL |
| Usable fixed-k, different-C overlap | PASS | ABSENT as designed; pipeline PASS | PASS |
| C survives under this simulation's criteria | FAIL | NOT IDENTIFIABLE | N/A; oracle null check PASS |

W2 is **unidentifiable**, not a measured negative effect and not a successful concentration
result: `C=1` for every case with `k>0`, so there is no within-k C variation. W3 is an oracle
null check; its `C survives` row is not a positive result. W1 is the failed wiring check.

### All failed checks

- W1 primary family-adjusted C gain: domain FAIL; equal FAIL.
- W1 alternate diagnostic-partition C gain: domain FAIL (`mean=-6.2470e-07`, 95% `[-3.4517e-06, 3.1384e-06]`); equal FAIL (`mean=-6.7787e-07`, 95% `[-3.8943e-06, 2.6534e-06]`).
- W1 full vector beats C: domain PASS; equal FAIL (`mean=-6.4299e-06`, 95% `[-1.6384e-05, 2.1034e-06]`); overall FAIL.
- W1 `C survives`: FAIL.
- W3 primary C gain: domain FAIL; equal FAIL.
- W3 alternate diagnostic-partition C gain: domain FAIL (`mean=-1.2237e-06`); equal FAIL (`mean=-1.6349e-06`).
- W3 full vector beats C: domain FAIL; equal FAIL.

The original failed-checks summary omitted the W1 alternate-partition failure and the W3
alternate-partition/full-vector failures. They are included above. W2's zero/undefined C
contrast is not listed as a measured failure.

## 2. Unseen-k measurement

For every setting, trial, and fold, the correction counted held-out eligible cases (`k>0`) whose
`k` value did not occur in that fold's training data. These cases receive no k-specific term
because the training design has no active column for that k level. Counts are across all 500
trials; a "fold fit" is one trial-fold pair.

| Setting | Fold fits with unseen k | Affected eligible cases | Fraction of eligible | Unseen-k fold instances | Global unseen k levels |
| --- | ---: | ---: | ---: | ---: | --- |
| W1 | 438 / 2500 | 563 | 0.0225% | 481 | 1, 23, 24, 25, 26, 27, 28 |
| W2 | 0 / 2500 | 0 | 0.0000% | 0 | none |
| W3 | 453 / 2500 | 575 | 0.0230% | 490 | 1, 23, 24, 25, 26, 27 |
| MIX_0_0 | 0 / 2500 | 0 | 0.0000% | 0 | none |
| MIX_0_25 | 583 / 2500 | 732 | 0.0293% | 644 | 1, 2, 22, 23, 24, 25, 26, 28 |
| MIX_0_5 | 545 / 2500 | 673 | 0.0269% | 592 | 1, 2, 23, 24, 25, 26, 27 |
| MIX_0_75 | 504 / 2500 | 626 | 0.0250% | 545 | 1, 23, 24, 25, 26, 27 |
| MIX_1_0 | 477 / 2500 | 591 | 0.0236% | 513 | 1, 23, 24, 25, 26, 27 |

For W1, the 438 fold fits with unseen k exactly match the 438 M0/M0fam/M1/M1fam/MF rank-warning
fits. The affected W1 cases by unseen k are:

| Unseen k | Affected eligible cases |
| ---: | ---: |
| 1 | 183 |
| 23 | 26 |
| 24 | 218 |
| 25 | 114 |
| 26 | 18 |
| 27 | 3 |
| 28 | 1 |

W2's 2,500 M1/M1fam/MF rank warnings are not unseen-k warnings; they arise because C is constant
for all eligible W2 cases. W3's 453 rank warnings match its 453 unseen-k fold fits. The unseen-k
problem is therefore frequent at the fold level but affects only 0.0225% of W1 eligible cases.

## 3. W1 sensitivity without unseen-k cases

The original estimate is preserved exactly. The sensitivity refits the same M0fam and M1fam
models on the same original training folds, then scores only held-out eligible cases whose `k`
occurs in that fold's training data. Both models are scored on exactly the same subset. The
complement (unseen-k cases) is reported separately for description only.

| Subset | Trials | Cases | Score | Mean Delta_pred | Central 95% trial interval | Positive trials | Mean L(M0fam) |
| --- | ---: | ---: | --- | ---: | --- | ---: | ---: |
| all eligible (original) | 500 | 2,499,949 | domain | 1.961346752e-06 | [-1.242089975e-06, 7.581285807e-06] | 0.804 | 0.003387840 |
| all eligible (original) | 500 | 2,499,949 | equal | 1.914362824e-06 | [-1.833270363e-06, 8.988738209e-06] | 0.754 | 0.003350860 |
| represented-k sensitivity | 500 | 2,499,386 | domain | 1.036293050e-06 | [-1.660447426e-06, 5.298823179e-06] | 0.716 | 0.003378998 |
| represented-k sensitivity | 500 | 2,499,386 | equal | 9.790599446e-07 | [-1.851879484e-06, 6.079745018e-06] | 0.642 | 0.003341825 |
| unseen-k complement (descriptive) | 328 | 563 | domain | 4.302023599e-03 | [-1.013030504e-04, 1.017680314e-02] | 0.970 | 0.043868614 |
| unseen-k complement (descriptive) | 328 | 563 | equal | 4.288053415e-03 | [-8.418119868e-04, 1.115650276e-02] | 0.951 | 0.044445288 |

The represented-k estimate is smaller than the original but still positive: `1.04e-6` domain and
`9.79e-7` equal, or `0.0307%` and `0.0293%` of their respective baselines. Both intervals still
include zero. The W1 criterion therefore remains **FAILED**; the sensitivity does not rescue it
and does not replace it. The unseen-k complement has a much higher baseline loss (`0.0439` /
`0.0444`) and only 563 cases; it is not comparable to the full eligible population and must not
be read as a concentration effect.

## 4. Corrected baseline accounting

The original label "full-cohort M0 baseline" is too strong. The full-cell baseline omits test
cases whose `k` is absent from the other folds. For W1 it scores 2,499,388 cases and omits 612:
49 k=0 cases plus 563 eligible unseen-k cases. The scored fraction is 99.97552%, not 100%.

| Setting | Total cases | Full baseline scored | Omitted | Omitted k=0 | Omitted eligible unseen-k | Scored fraction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| W1 | 2,500,000 | 2,499,388 | 612 | 49 | 563 | 99.97552% |
| W2 | 2,500,000 | 2,500,000 | 0 | 0 | 0 | 100.00000% |
| W3 | 2,500,000 | 2,499,374 | 626 | 51 | 575 | 99.97496% |
| MIX_0_0 | 2,500,000 | 2,500,000 | 0 | 0 | 0 | 100.00000% |
| MIX_0_25 | 2,500,000 | 2,499,253 | 747 | 15 | 732 | 99.97012% |
| MIX_0_5 | 2,500,000 | 2,499,295 | 705 | 32 | 673 | 99.97180% |
| MIX_0_75 | 2,500,000 | 2,499,326 | 674 | 48 | 626 | 99.97304% |
| MIX_1_0 | 2,500,000 | 2,499,362 | 638 | 47 | 591 | 99.97448% |

The correct label is **M0 baseline on k-represented cases**, not full-cohort performance. The
eligible model comparison separately uses the common eligible subset (`k>0`) and reports
`L(M0fam)` on that subset; the two baselines are not interchangeable.

## 5. Overlap completeness

The missing per-k, per-C case counts are in `12_overlap_by_k_c.md`. It lists every observed
`(world, k, C)` pair and its pooled eligible-case count for all settings. C is recorded as the
exact fraction `max(F)/k`; the decimal is display only. W1 has 74 observed `(k,C)` pairs, W2 has
one (`k=5`, `C=1`), W3 has 73, and the mixtures have 72-74. Counts are synthetic cases pooled
over 500 trials, not estimates of real-solver prevalence.

This appendix supplies the detail omitted from the original report; it does not change the
original overlap summary.

## 6. Archive status

The 592,020,294-byte raw/per-trial archive remains local-only. The correction used those local
files and verified their manifest hashes. No GitHub Release was recreated and no upload was
retried. A hash records integrity but cannot recover the data if the sole copy is lost; a
second verified copy is still advisable.

## Reproduction

```text
python engineered-study/math/analyze_three_world_review.py --verify-hashes
```

This writes `12_review_correction_metrics.json` and `12_overlap_by_k_c.md`. It reads the
original raw records and does not call the simulation generator. The original report,
manifest, and `simulate_worlds.py` remain unchanged.

## Limits

This is a post-run correction record, not a new pre-registered analysis or a new simulation.
The represented-k sensitivity is a diagnostic of the cross-validation limitation; it does not
replace the frozen W1 estimate. The unseen-k complement is descriptive and is not a like-for-like
estimate of a C effect. W2 remains unidentifiable; W3's oracle check remains a null check. None
of these results is evidence about real solvers.
