# Three-world concentration simulation result

**Scope:** Synthetic-data simulation only. Results show implications of the declared assumptions; they are not evidence about real solvers.

**Frozen outcome: W1 FAILED.** The W1 wiring criterion did not pass. This report describes a weak positive estimate but does not claim that the frozen simulation demonstrated predictive value for `C`.

**Source review status: PENDING independent review.** The source notes below are author verification, not an independent GPT review or a certification of statistical correctness.

Trials per setting: 500; cases per trial: 5000; base seed: 20261024.
Frozen design SHA-256: `a33b475dedbc66eb2d97e490389f3623f2fea29f6b7a98e6ceefb9536d277fd1`; script SHA-256: `d19097434d999764fd913c514ff13344a2bd49b582f98de7bf8fcd02dd089c0a`.
Runtime: 1636.11 s; raw gzip bytes: 560553425.
World reaches: W1 diagnostic 0.80/0.05, evaluation 0.35/0.03; W2 1/0, 1/0; W3 diagnostic 0.80/0.05, evaluation 0.15/0.15 (home/other).

The intervals below are central 95% simulation-trial intervals, not confidence intervals about a real population.

## W1

| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| domain | 0.000002 | [-0.000001, 0.000008] | 0.804 | 0.000790 | [0.000692, 0.000886] | -0.000001 | [-0.000003, 0.000003] |
| equal | 0.000002 | [-0.000002, 0.000009] | 0.754 | -0.000006 | [-0.000016, 0.000002] | -0.000001 | [-0.000004, 0.000003] |

Eligible cases: 2499949; k=0 cases: 51 (W1=51); world cases: W1=2500000 (1.000).
Fixed-k carrier overlap: cases=2365022, strata=49834, pairs=24299794, residualized C variance=14737.3.
Overlap in W1: cases=2365022, strata=49834, residualized C variance=14737.3.

| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |
| --- | ---: | ---: | ---: | ---: |
| W1 | 2500000 | 51 | 0.808319 | 0.494205 |
Rank warnings (primary / alternate partition): M0=438, M0fam=438, M1=438, M1fam=438, MF=438 / M0fam=438, M1fam=438, MF=438.
Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.
Full-cohort M0 baseline (domain/equal): 0.004193 / 0.003338.

### Criteria

| Criterion | Domain | Equal | Outcome |
| --- | --- | --- | --- |
| Family-adjusted C gain positive with 95% interval above zero | FAIL | FAIL | FAIL |
| Alternate diagnostic-partition C gain positive | FAIL | FAIL | FAIL |
| Full vector beats C (95% interval above zero) | PASS | FAIL | FAIL |
| Usable fixed-k, different-C overlap | PASS | PASS | PASS |
| C survives under this simulation's criteria | FAIL | FAIL | DOES NOT SURVIVE |

W1/domain: full vector beats C under the finite-sample predictor.

## W2

| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| domain | 0.000000 | [0.000000, 0.000000] | 0.000 | 0.000000 | [0.000000, 0.000000] | 0.000000 | [0.000000, 0.000000] |
| equal | 0.000000 | [0.000000, 0.000000] | 0.000 | 0.000000 | [0.000000, 0.000000] | 0.000000 | [0.000000, 0.000000] |

Eligible cases: 2500000; k=0 cases: 0 (W2=0); world cases: W2=2500000 (1.000).
Fixed-k carrier overlap: cases=0, strata=0, pairs=0, residualized C variance=0.
Overlap in W2: cases=0, strata=0, residualized C variance=0.

| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |
| --- | ---: | ---: | ---: | ---: |
| W2 | 2500000 | 0 | 0.833310 | 1.000000 |
Rank warnings (primary / alternate partition): M0=0, M0fam=0, M1=2500, M1fam=2500, MF=2500 / M0fam=0, M1fam=2500, MF=2500.
Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.
Full-cohort M0 baseline (domain/equal): 0.010222 / 0.000000.

### Criteria

| Criterion | Domain | Equal | Outcome |
| --- | --- | --- | --- |
| Family-adjusted C gain positive with 95% interval above zero | FAIL | FAIL | FAIL |
| Alternate diagnostic-partition C gain positive | FAIL | FAIL | FAIL |
| Full vector beats C (95% interval above zero) | FAIL | FAIL | FAIL |
| Usable fixed-k, different-C overlap | ABSENT | ABSENT | ABSENT |
| C survives under this simulation's criteria | N/A | N/A | PASS (unidentifiable as expected) |


## W3

| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| domain | -0.000001 | [-0.000005, 0.000005] | 0.262 | -0.000006 | [-0.000019, 0.000007] | -0.000001 | [-0.000006, 0.000004] |
| equal | -0.000001 | [-0.000007, 0.000006] | 0.238 | -0.000008 | [-0.000024, 0.000008] | -0.000002 | [-0.000008, 0.000004] |

Eligible cases: 2499943; k=0 cases: 57 (W3=57); world cases: W3=2500000 (1.000).
Fixed-k carrier overlap: cases=2367488, strata=49901, pairs=24332103, residualized C variance=14740.3.
Overlap in W3: cases=2367488, strata=49901, residualized C variance=14740.3.

| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |
| --- | ---: | ---: | ---: | ---: |
| W3 | 2500000 | 57 | 0.677143 | 0.494209 |
Rank warnings (primary / alternate partition): M0=453, M0fam=453, M1=453, M1fam=453, MF=453, ORACLE=453, ORACLE_NOC=453 / M0fam=453, M1fam=453, MF=453.
Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.
Full-cohort M0 baseline (domain/equal): 0.005021 / 0.006768.

W3 oracle C-after-defects domain: mean=-0.000000, 95%=[-0.000002, 0.000002], positive=0.284. W3 primary C gain domain: mean=-0.000001, 95%=[-0.000005, 0.000005].
W3 oracle C-after-defects equal: mean=-0.000001, 95%=[-0.000003, 0.000003], positive=0.238. W3 primary C gain equal: mean=-0.000001, 95%=[-0.000007, 0.000006].

### Criteria

| Criterion | Domain | Equal | Outcome |
| --- | --- | --- | --- |
| Family-adjusted C gain positive with 95% interval above zero | FAIL | FAIL | FAIL |
| Alternate diagnostic-partition C gain positive | FAIL | FAIL | FAIL |
| Full vector beats C (95% interval above zero) | FAIL | FAIL | FAIL |
| Usable fixed-k, different-C overlap | PASS | PASS | PASS |
| C survives under this simulation's criteria | N/A | N/A | PASS |


## MIX_0_0

| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| domain | 0.000000 | [0.000000, 0.000000] | 0.000 | 0.000000 | [0.000000, 0.000000] | 0.000000 | [0.000000, 0.000000] |
| equal | 0.000000 | [0.000000, 0.000000] | 0.000 | 0.000000 | [0.000000, 0.000000] | 0.000000 | [0.000000, 0.000000] |

Eligible cases: 2500000; k=0 cases: 0 (W2=0); world cases: W2=2500000 (1.000).
Fixed-k carrier overlap: cases=0, strata=0, pairs=0, residualized C variance=0.
Overlap in W2: cases=0, strata=0, residualized C variance=0.

| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |
| --- | ---: | ---: | ---: | ---: |
| W2 | 2500000 | 0 | 0.833328 | 1.000000 |
Rank warnings (primary / alternate partition): M0=0, M0fam=0, M1=2500, M1fam=2500, MF=2500 / M0fam=0, M1fam=2500, MF=2500.
Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.
Full-cohort M0 baseline (domain/equal): 0.010223 / 0.000000.

### Criteria

| Criterion | Domain | Equal | Outcome |
| --- | --- | --- | --- |
| Family-adjusted C gain positive with 95% interval above zero | FAIL | FAIL | FAIL |
| Alternate diagnostic-partition C gain positive | FAIL | FAIL | FAIL |
| Full vector beats C (95% interval above zero) | FAIL | FAIL | FAIL |
| Usable fixed-k, different-C overlap | ABSENT | ABSENT | ABSENT |
| C survives under this simulation's criteria | N/A | N/A | DESCRIPTIVE |


## MIX_0_25

| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| domain | 0.000014 | [-0.000014, 0.000042] | 0.870 | 0.000705 | [0.000597, 0.000828] | 0.000005 | [-0.000006, 0.000021] |
| equal | 0.000015 | [-0.000011, 0.000039] | 0.902 | -0.000020 | [-0.000046, 0.000010] | 0.000006 | [-0.000003, 0.000020] |

Eligible cases: 2499980; k=0 cases: 20 (W1=20, W2=0); world cases: W1=624238 (0.250), W2=1875762 (0.750).
Fixed-k carrier overlap: cases=2402910, strata=40946, pairs=22267398, residualized C variance=4889.86.
Overlap in W1: cases=527148, strata=40946, residualized C variance=3370.96.
Overlap in W2: cases=0, strata=0, residualized C variance=0.

| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |
| --- | ---: | ---: | ---: | ---: |
| W1 | 624238 | 20 | 0.808114 | 0.493482 |
| W2 | 1875762 | 0 | 0.833268 | 1.000000 |
Rank warnings (primary / alternate partition): M0=583, M0fam=583, M1=583, M1fam=583, MF=583 / M0fam=583, M1fam=583, MF=583.
Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.
Full-cohort M0 baseline (domain/equal): 0.008859 / 0.000966.

### Criteria

| Criterion | Domain | Equal | Outcome |
| --- | --- | --- | --- |
| Family-adjusted C gain positive with 95% interval above zero | FAIL | FAIL | FAIL |
| Alternate diagnostic-partition C gain positive | FAIL | FAIL | FAIL |
| Full vector beats C (95% interval above zero) | PASS | FAIL | FAIL |
| Usable fixed-k, different-C overlap | PASS | PASS | PASS |
| C survives under this simulation's criteria | N/A | N/A | DESCRIPTIVE |

MIX_0_25/domain: full vector beats C under the finite-sample predictor.

## MIX_0_5

| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| domain | 0.000039 | [0.000010, 0.000074] | 0.998 | 0.000995 | [0.000878, 0.001119] | 0.000015 | [-0.000000, 0.000035] |
| equal | 0.000039 | [0.000013, 0.000069] | 0.998 | -0.000044 | [-0.000073, -0.000016] | 0.000015 | [0.000002, 0.000032] |

Eligible cases: 2499966; k=0 cases: 34 (W1=34, W2=0); world cases: W1=1250445 (0.500), W2=1249555 (0.500).
Fixed-k carrier overlap: cases=2388663, strata=46148, pairs=33703037, residualized C variance=9995.94.
Overlap in W1: cases=1139108, strata=46148, residualized C variance=7174.55.
Overlap in W2: cases=0, strata=0, residualized C variance=0.

| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |
| --- | ---: | ---: | ---: | ---: |
| W1 | 1250445 | 34 | 0.808357 | 0.494343 |
| W2 | 1249555 | 0 | 0.833464 | 1.000000 |
Rank warnings (primary / alternate partition): M0=545, M0fam=545, M1=545, M1fam=545, MF=545 / M0fam=545, M1fam=545, MF=545.
Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.
Full-cohort M0 baseline (domain/equal): 0.007448 / 0.001904.

### Criteria

| Criterion | Domain | Equal | Outcome |
| --- | --- | --- | --- |
| Family-adjusted C gain positive with 95% interval above zero | PASS | PASS | PASS |
| Alternate diagnostic-partition C gain positive | FAIL | PASS | FAIL |
| Full vector beats C (95% interval above zero) | PASS | FAIL | FAIL |
| Usable fixed-k, different-C overlap | PASS | PASS | PASS |
| C survives under this simulation's criteria | N/A | N/A | DESCRIPTIVE |

MIX_0_5/domain: full vector beats C under the finite-sample predictor.

## MIX_0_75

| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| domain | 0.000048 | [0.000024, 0.000076] | 1.000 | 0.000981 | [0.000877, 0.001096] | 0.000019 | [0.000004, 0.000037] |
| equal | 0.000048 | [0.000025, 0.000072] | 1.000 | -0.000053 | [-0.000080, -0.000026] | 0.000019 | [0.000006, 0.000036] |

Eligible cases: 2499952; k=0 cases: 48 (W1=48, W2=0); world cases: W1=1874354 (0.750), W2=625646 (0.250).
Fixed-k carrier overlap: cases=2376707, strata=48426, pairs=34456237, residualized C variance=14599.8.
Overlap in W1: cases=1751061, strata=48426, residualized C variance=10941.8.
Overlap in W2: cases=0, strata=0, residualized C variance=0.

| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |
| --- | ---: | ---: | ---: | ---: |
| W1 | 1874354 | 48 | 0.808437 | 0.494536 |
| W2 | 625646 | 0 | 0.833414 | 1.000000 |
Rank warnings (primary / alternate partition): M0=504, M0fam=504, M1=504, M1fam=504, MF=504 / M0fam=504, M1fam=504, MF=504.
Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.
Full-cohort M0 baseline (domain/equal): 0.006010 / 0.002808.

### Criteria

| Criterion | Domain | Equal | Outcome |
| --- | --- | --- | --- |
| Family-adjusted C gain positive with 95% interval above zero | PASS | PASS | PASS |
| Alternate diagnostic-partition C gain positive | PASS | PASS | PASS |
| Full vector beats C (95% interval above zero) | PASS | FAIL | FAIL |
| Usable fixed-k, different-C overlap | PASS | PASS | PASS |
| C survives under this simulation's criteria | N/A | N/A | DESCRIPTIVE |

MIX_0_75/domain: full vector beats C under the finite-sample predictor.

## MIX_1_0

| Score | C gain mean | C gain 95% interval | Positive trials | F-vs-C mean | F-vs-C 95% interval | Partition C gain mean | Partition 95% interval |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| domain | 0.000002 | [-0.000001, 0.000007] | 0.822 | 0.000790 | [0.000702, 0.000879] | -0.000001 | [-0.000004, 0.000003] |
| equal | 0.000002 | [-0.000002, 0.000008] | 0.758 | -0.000007 | [-0.000015, 0.000003] | -0.000001 | [-0.000004, 0.000003] |

Eligible cases: 2499947; k=0 cases: 53 (W1=53); world cases: W1=2500000 (1.000).
Fixed-k carrier overlap: cases=2367821, strata=49978, pairs=24291662, residualized C variance=14753.4.
Overlap in W1: cases=2367821, strata=49978, residualized C variance=14753.4.

| World | Cases | k=0 | Mean S_domain | Mean C (k>0) |
| --- | ---: | ---: | ---: | ---: |
| W1 | 2500000 | 53 | 0.808338 | 0.494413 |
Rank warnings (primary / alternate partition): M0=477, M0fam=477, M1=477, M1fam=477, MF=477 / M0fam=477, M1fam=477, MF=477.
Rank warnings mean a fold-level parameterization is not identified; parameter interpretation is unavailable for those fits.
Full-cohort M0 baseline (domain/equal): 0.004192 / 0.003340.

### Criteria

| Criterion | Domain | Equal | Outcome |
| --- | --- | --- | --- |
| Family-adjusted C gain positive with 95% interval above zero | FAIL | FAIL | FAIL |
| Alternate diagnostic-partition C gain positive | FAIL | FAIL | FAIL |
| Full vector beats C (95% interval above zero) | PASS | FAIL | FAIL |
| Usable fixed-k, different-C overlap | PASS | PASS | PASS |
| C survives under this simulation's criteria | N/A | N/A | DESCRIPTIVE |

MIX_1_0/domain: full vector beats C under the finite-sample predictor.

## Failed checks

- W1: W1 wiring / positive-direction interval criterion failed
- W1/domain: family-adjusted C gain not positive with interval above zero
- W1/equal: family-adjusted C gain not positive with interval above zero

## Limits

W1 is constructed to make concentration informative; its positive result is a wiring check, not evidence for the real-world hypothesis. W2 is an overlap negative control. W3 separates direct concentration effects from proxy information about latent defect count. The mixture sweep is a stress test, not an estimate of real-world prevalence. The generative model treats diagnostic and evaluation failures as independent Bernoulli draws and does not preserve input-level dependence. The 20 million raw records and validated hashes establish output accounting and integrity, not statistical correctness. Model definitions, matched folds, rank handling, and comparisons require source-level review.

## Post-run source verification and effect sizes

This section was added after the run from the existing outputs; it did not rerun the simulation or change any model, parameter, fold, or criterion.

### Source-level checks

- **Like-for-like full-vector comparison:** `M1fam` is `C_INDEX + FAM_INDICES`, while `MF` is `F_INDICES + FAM_INDICES` (`simulate_worlds.py:506-507`). Both are assembled from the same `categories`, the same `eligible_by_fold` data, and the same five folds (`simulate_worlds.py:515-521`). The reported quantity is exactly `L(M1+fam) - L(MF+fam)` (`simulate_worlds.py:751-753`); the table label "F-vs-C" is shorthand for that like-for-like comparison, not a model without anchor-family indicators.
- **Oracle check:** `ORACLE` is `k + anchor-family indicators + C + latent defect count`; `ORACLE_NOC` is `k + anchor-family indicators + latent defect count` (`simulate_worlds.py:509-511`). Both use the same folds, categories, and eligible cases.
- **Fold matching and rank handling:** each case is assigned to one fold once, and all compared models use the same fold assignment (`simulate_worlds.py:515-521`, `simulate_worlds.py:696-706`). `subset_sse` drops zero-diagonal active columns before solving and uses Cholesky with a Moore-Penrose-style cyclic-Jacobi fallback for rank deficiency (`simulate_worlds.py:473-492`). A fold is counted as a rank warning when either score has deficient rank; parameter interpretation is unavailable for those fits.
- **W1 construction:** `C = max(F)/k` for `k>0`; the alternate partition recomputes `F`, `k`, and `C` from the retained 30 diagnostic bits (`simulate_worlds.py:99-141`). No post-result changes were made.
- **Investigation result:** the W1 partial residual correlation is positive but small (about 0.021 in a 200,000-case diagnostic), with a fitted C coefficient of about 0.015. No obvious code-path mismatch was found. The most parsimonious reading is that `C` is a weak summary at this sample size under the stipulated W1 reaches; this review does not prove that the estimator is optimal or that the generator is substantively correct.

### Baseline-relative scale

`L(M0+fam)` is the mean held-out loss of the family-adjusted baseline on the common eligible subset. `Delta_pred` is `L(M0+fam) - L(M1+fam)`; `Delta_f` is `L(M1+fam) - L(MF+fam)`. Ratios use the corresponding baseline loss; `n/a` means the baseline is zero.

| Setting | Score | Mean L(M0+fam) | Delta_pred mean | Delta_pred 95% | Delta_pred / baseline | Delta_f mean | Delta_f 95% | Delta_f / baseline |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| W1 | domain | 0.003387840 | 1.96134675e-06 | [-1.24208998e-06, 7.58128581e-06] | 0.0579% | 0.00078998261 | [0.000691849522, 0.00088594136] | 23.3182% |
| W1 | equal | 0.003350860 | 1.91436282e-06 | [-1.83327036e-06, 8.98873821e-06] | 0.0571% | -6.42986985e-06 | [-1.63841259e-05, 2.10343462e-06] | -0.1919% |
| W2 | domain | 0.000000000 | 0 | [0, 0] | n/a | 0 | [0, 0] | n/a |
| W2 | equal | 0.000000000 | 0 | [0, 0] | n/a | 0 | [0, 0] | n/a |
| W3 | domain | 0.005047055 | -8.20078659e-07 | [-5.46801819e-06, 4.51635324e-06] | -0.0162% | -6.12110944e-06 | [-1.86224686e-05, 6.79662498e-06] | -0.1213% |
| W3 | equal | 0.006795518 | -1.13985233e-06 | [-7.1490007e-06, 5.84236217e-06] | -0.0168% | -8.34588431e-06 | [-2.40678826e-05, 7.55777727e-06] | -0.1228% |
| MIX_0_25 | domain | 0.001997736 | 1.4164428e-05 | [-1.3668591e-05, 4.19779089e-05] | 0.7090% | 0.000704551307 | [0.000597029461, 0.000827637969] | 35.2675% |
| MIX_0_25 | equal | 0.000979102 | 1.47620552e-05 | [-1.08020082e-05, 3.86983285e-05] | 1.5077% | -1.98699093e-05 | [-4.60302167e-05, 9.89582313e-06] | -2.0294% |
| MIX_0_5 | domain | 0.003265374 | 3.85820666e-05 | [1.0067364e-05, 7.43425279e-05] | 1.1816% | 0.000995015837 | [0.000877587415, 0.00111913512] | 30.4717% |
| MIX_0_5 | equal | 0.001917616 | 3.89425683e-05 | [1.26034817e-05, 6.85803982e-05] | 2.0308% | -4.36148798e-05 | [-7.33246757e-05, -1.56160805e-05] | -2.2744% |
| MIX_0_75 | domain | 0.003841324 | 4.82190744e-05 | [2.44906528e-05, 7.64985372e-05] | 1.2553% | 0.000981166326 | [0.00087720012, 0.00109570853] | 25.5424% |
| MIX_0_75 | equal | 0.002822071 | 4.84296073e-05 | [2.48628031e-05, 7.20521556e-05] | 1.7161% | -5.30462997e-05 | [-7.96141848e-05, -2.57507777e-05] | -1.8797% |
| MIX_1_0 | domain | 0.003386827 | 1.94465333e-06 | [-1.26163766e-06, 7.47186043e-06] | 0.0574% | 0.000789561552 | [0.000701804176, 0.000878522681] | 23.3127% |
| MIX_1_0 | equal | 0.003353506 | 1.78691273e-06 | [-2.06461606e-06, 7.93888351e-06] | 0.0533% | -6.56392543e-06 | [-1.53783688e-05, 3.13022175e-06] | -0.1957% |

The W1 domain estimate is `1.96e-6` against a baseline loss of `3.39e-3`, or about `0.058%` of baseline; its interval includes zero. It is not a practically meaningful improvement. The W1 equal-score estimate is similarly tiny. W3's oracle C-after-defects estimates are about `-2.8e-7` (domain) and `-6.0e-7` (equal), both negligible relative to their baselines and with intervals including zero.

Mixture gains are between-world composition effects: they are not evidence of a general within-world concentration contribution, because W2 has no usable within-world variation in `C`. The W1 wiring failure remains the governing result; no parameter change or rerun was made to rescue it.

## Local archive

The complete per-trial JSON and raw JSONL gzip files remain on the machine that produced the run, under `engineered-study/math/results/three_world/`. They are not in ordinary Git history and were not uploaded to GitHub. The small script, report, and manifest are committed; the checksums below record integrity but do not preserve the data if these local files are lost.

| Local artifact | Path | Bytes | Records | SHA-256 |
| --- | --- | ---: | ---: | --- |
| `per_trial.json` | `per_trial.json` | 31466869 | 4000 | `b6761998db3a64cecbdc33b05d97625409422ce8919dee9eedfe289ee457556d` |
| `W1.jsonl.gz` | `raw/W1.jsonl.gz` | 108575908 | 2500000 | `544e920010b23f63b104781966ba3c4b84cd6ef3de47067b02a5e7b83f57ae85` |
| `W2.jsonl.gz` | `raw/W2.jsonl.gz` | 14044132 | 2500000 | `3bbd492660073f03d3fd0fbd35daf7a95747481abd2e1adc2313d19d0a9d992a` |
| `W3.jsonl.gz` | `raw/W3.jsonl.gz` | 110740371 | 2500000 | `464796e595565b7bd23232a6402df388658352147e3ef68b46db5ee4e8e63820` |
| `MIX_0_0.jsonl.gz` | `raw/MIX_0_0.jsonl.gz` | 14380075 | 2500000 | `e08265f97e54e5244c0d5b2925dbaf228bbe8d707e0cd1adae0318c681965b5c` |
| `MIX_0_25.jsonl.gz` | `raw/MIX_0_25.jsonl.gz` | 45765444 | 2500000 | `3a3858bff4e687a070d59451ce64f0984cda9f32f6688390ba65f7eb101bf3d7` |
| `MIX_0_5.jsonl.gz` | `raw/MIX_0_5.jsonl.gz` | 68733468 | 2500000 | `8016aaf8977c47a8ccc6b981a0cda17bd89040a96d627b60a37d7e025e2ccc35` |
| `MIX_0_75.jsonl.gz` | `raw/MIX_0_75.jsonl.gz` | 89522944 | 2500000 | `e3059e0622dd9fcfbd8e70a015e2907bf43448d1bec545c492e61ce98eaf95ce` |
| `MIX_1_0.jsonl.gz` | `raw/MIX_1_0.jsonl.gz` | 108791083 | 2500000 | `1207480625efac2acb1007c3fc924b042fe28cea1d4369e75025bcbcffba6f05` |

Local results total about 592 MB. The raw compressed JSONL files account for 560.5 MB and the per-trial JSON for 31.5 MB. The report, manifest, and script are committed; the data files are local-only until a separate archival decision is made.
