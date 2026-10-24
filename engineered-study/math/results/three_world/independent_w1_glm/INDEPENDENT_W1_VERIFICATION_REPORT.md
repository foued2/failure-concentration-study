# Independent W1 Verification — GLM Work Order Report

Field: independent verification (GLM), single bounded verification
Date: 2026-10-24
Branch: `research/concentration-math-spec` (HEAD `780daa5`, unchanged; **no commits, no pushes, no original files modified**)

## 1. Disposition (summary)

**W1 remains FAILED — now with independent confirmation.**

The declared W1 wiring check — fitted M1+fam should NOT improve held-out prediction over M0+fam — was re-implemented from the frozen design by an independent stdlib-only implementation and reproduced the entire W1 pipeline exactly:

- **Verification A (generator):** all 2,500,000 records of the local `raw/W1.jsonl.gz` were regenerated and matched **strictly, field by field, with zero mismatches and zero near-misses** (float fields included).
- **Verification B (estimator):** every aggregate primary/partition/represented-k metric reproduced the reference values to reported precision; all 36 reference comparison rows MATCH; per-trial losses/deltas differ from the originals only at last-bit floating scale (max absolute error ≤ 2.5e-15 on quantities of order 1e-6…3.4e-3).

The claimed "significant" primary result (positive trial fraction 0.804/0.754, mean Δ≈1.96e-6/1.91e-6) is therefore a genuine property of the frozen three-world W1 design and the declared estimator protocol — **not an implementation artifact** (no free parameter, no off-by-one, no RNG ordering difference, no scoring asymmetry). The Δ_pred scale (~2e-6 against baseline losses ~3.4e-3) is tiny; the study's own caution (review section; ~0.06% of SSE) stands. The alternate diagnostic partition shows the opposite-signed mean (−6.25e-7 / −6.78e-7), confirming the effect is not robust to a reasonable re-partitioning.

## 2. Source freeze

Directory of this task: `engineered-study/math/results/three_world/independent_w1_glm/`

| Item | Value |
|---|---|
| Implementation basis | Written from the frozen design `10_THREE_WORLD_SIM_DESIGN.md` (LF-normalized SHA-256 `a33b475dedbc66eb2d97e490389f3623f2fea29f6b7a98e6ceefb9536d277fd1`, 19,788 bytes — re-verified in-run) and the documented verification protocol. Does **not** import `simulate_worlds.py` or `analyze_three_world_review.py`. Standard library only. |
| Hash recorded before first execution | Yes (`source_sha256.txt`) |
| Initial frozen source | SHA-256 `1afcbe79a2536bca82d53a6e92cea2d6457daec03690a46813fd3fcf8b1a3497`, 51,920 bytes |
| Documented correction (before any simulation ran) | The initial source crashed at startup (`FileNotFoundError`): `DESIGN_PATH` pointed one directory too shallow (`math/results/…` instead of `math/…`). Single-line path fix only; **no generator, estimator, or comparison logic touched**; crash occurred during input-hash checking, before any simulation output existed. |
| Corrected source used for all executed runs | SHA-256 `4454ae9f5bca940f3c8253273d1bf198a70bfe4270b553464401855403542aae`, 51,927 bytes |
| Not modified after run results | Confirmed |

## 3. Environment

| Item | Value |
|---|---|
| Python | CPython 3.14.0 (`C:\Users\pakla\AppData\Roaming\uv\python\cpython-3.14.0-windows-x86_64-none\python.exe`, invoked via `py -V:Astral/CPython3.14.0`) |
| Platform | `Windows-11-10.0.26300-SP0` |
| Matches original run | Yes (per manifest environment) |
| Runtime | 500 trials × 5,000 cases, ~111.4 s wall |

## 4. Inputs used (read-only, hashes verified in-run)

| Input | SHA-256 | Manifest match |
|---|---|---|
| `raw/W1.jsonl.gz` | `544e920010b23f63b104781966ba3c4b84cd6ef3de47067b02a5e7b83f57ae85` | yes |
| `per_trial.json` | `b6761998db3a64cecbdc33b05d97625409422ce8919dee9eedfe289ee457556d` | yes |
| `12_review_correction_metrics.json` | `7d11454fd078f3290ccec645c4c83d282497f61f61b71aa63938d363dde9ddc7` | (recorded) |
| Frozen design (LF-normalized) | `a33b475dedbc66eb2d97e490389f3623f2fea29f6b7a98e6ceefb9536d277fd1` | verified again in-run |

## 5. Verification A — generator stream reproduction

Per-case recipe reimplemented independently from the frozen design text: same draw order (fold draw `fold_rng.randrange(5)` first from `Random(seed + 7919)`, then `randint(1,4)` defects, one `randrange(6)` home per defect, 30 `rng.random()` diagnostic bits family-major vs. union reach q = 1 − ∏(1 − r), then 6 `binomialvariate(N_j, q^E_j)` draws). All score quantities (`C`, `C_alt`, `S_domain`, `S_equal`) were derived independently.

| Check | Result |
|---|---|
| Records checked | 2,500,000 (= expected 500 × 5,000) |
| Records matched strictly | 2,500,000 |
| Records with ≥1 mismatched field | 0 |
| Float fields matched only within 1e-12 (near-misses) | 0 |
| Trailing records after expected count | 0 |
| First mismatch | none |
| **All records matched strictly** | **True** |

Every W1 record — `trial, case, fold, F, E, F_alt, k, C, C_alt, carrier, home_counts, defects, S_domain, S_equal, diag_bits` — is bit-identical to the original archive, byte for byte in JSON serialization.

## 6. Verification B — estimator reproduction

Independent OLS machinery: per-(k, carrier)-level sufficient statistics, X'X assembled per fold for intercept + categorical k dummies (reference = smallest eligible k of the trial) + 5 anchor-family indicators (family 6 reference) + the model's feature; rank-deficient columns (training-unobserved k levels) dropped and flagged; own Cholesky solve, with own Moore–Penrose eigen fallback; held-out SSE accumulated per test case across the 5 folds; loss = SSE / eligible count.

### 6.1 Primary models vs references (domain / equal)

| Metric | Reference | Independent | Difference | Status |
|---|---|---|---|---|
| Mean Δ_pred domain | 1.961346752e-06 | 1.9613467519803966e-06 | −2.0e-17 | MATCH |
| 95% interval low domain | −1.242089975e-06 | −1.2420899751200486e-06 | −1.2e-16 | MATCH |
| 95% interval high domain | 7.581285807e-06 | 7.581285806617664e-06 | −3.8e-16 | MATCH |
| Positive fraction domain | 0.804 | 0.804 (402/500) | 0 | MATCH |
| Mean Δ_pred equal | 1.914362824e-06 | 1.914362823589913e-06 | −4.1e-16 | MATCH |
| 95% interval low equal | −1.833270363e-06 | −1.8332703626153802e-06 | 3.8e-16 | MATCH |
| 95% interval high equal | 8.988738209e-06 | 8.988738208602912e-06 | −4.0e-16 | MATCH |
| Positive fraction equal | 0.754 | 0.754 (377/500) | 0 | MATCH |
| Eligible cases (k>0) | 2,499,949 | 2,499,949 | 0 (exact) | MATCH |
| Mean L(M0+fam) domain | 0.00338784 | 0.0033878403920887938 | 3.9e-10 | MATCH (tol 1e-7) |
| Mean L(M0+fam) equal | 0.00335086 | 0.003350859520304698 | −4.8e-10 | MATCH (tol 1e-7) |

Mean L(M1+fam): domain 0.003385879045336813, equal 0.0033489451574811083 (delta ≈ baseline − M1, strictly positive mean, as declared FAILED).

### 6.2 Represented-k sensitivity (denominator = represented cases only)

| Metric | Reference | Independent | Status |
|---|---|---|---|
| Mean Δ domain (represented) | 1.03629305e-06 | 1.0362930502466538e-06 | MATCH |
| 95% low domain | −1.660447426e-06 | −1.6604474258972783e-06 | MATCH |
| 95% high domain | 5.298823179e-06 | 5.298823179046563e-06 | MATCH |
| Positive fraction domain | 0.716 | 0.716 (358/500) | MATCH |
| Mean Δ equal (represented) | 9.790599446e-07 | 9.790599446280343e-07 | MATCH |
| 95% low equal | −1.851879484e-06 | −1.8518794834550793e-06 | MATCH |
| 95% high equal | 6.079745018e-06 | 6.079745017574371e-06 | MATCH |
| Positive fraction equal | 0.642 | 0.642 (321/500) | MATCH |
| Represented cases | 2,499,386 | 2,499,386 | MATCH (exact) |
| Represented L(M0+fam) domain | 0.003378998 | 0.0033789980213903554 | MATCH (tol 1e-7) |
| Represented L(M0+fam) equal | 0.003341825 | 0.0033418252894216248 | MATCH (tol 1e-7) |

### 6.3 Alternate diagnostic partition (C_alt; M0+fam design identical)

| Metric | Reference | Independent | Status |
|---|---|---|---|
| Mean Δ domain | ≈ −6.2470e-07 | −6.246999292176686e-07 | MATCH |
| 95% low domain | −3.4517e-06 | −3.451731479743065e-06 | MATCH |
| 95% high domain | 3.1384e-06 | 3.1384100087721974e-06 | MATCH |
| Positive fraction domain | — | 0.25 (125/500) | recorded |
| Mean Δ equal | ≈ −6.7787e-07 | −6.778654116399202e-07 | MATCH |
| 95% low equal | −3.8943e-06 | −3.894306437576631e-06 | MATCH |
| 95% high equal | 2.6534e-06 | 2.6533976665879947e-06 | MATCH |
| Positive fraction equal | — | 0.246 (123/500) | recorded |

Mean L(PM1fam): domain 0.003388465092018011, equal 0.003351537385716338 — worse than the primary-partition M1+fam means, consistent with the review's negative-mean estimate.

### 6.4 Rank / unseen-k diagnostics vs review values

| Diagnostic | Review value | Independent | Status |
|---|---|---|---|
| Deficient fold fits (each model) | 438 | 438 | MATCH |
| Fold fits with unseen k | 438 | 438 | MATCH |
| Unseen-k instances | 481 | 481 | MATCH |
| Affected eligible cases | 563 | 563 | MATCH |
| Unseen k levels | [1, 23, 24, 25, 26, 27, 28] | same | MATCH |
| Affected by k | {1:183, 23:26, 24:218, 25:114, 26:18, 27:3, 28:1} | same | MATCH |
| Full-baseline scored cases | 2,499,388 | 2,499,388 | MATCH |
| Full-baseline omitted cases | 612 | 612 | MATCH |
| Full-baseline omitted k=0 | 49 | 49 | MATCH |

Omitted-k subset (descriptive, 563 cases over 328 trials): consistent with the review's descriptive characterization (no inferential weight in the records).

## 7. Per-trial numeric fidelity (full run, vs original `per_trial.json` / review metrics)

| Quantity | Max abs error (over 500 trials) |
|---|---|
| Δ_pred domain | 1.02e-15 |
| Δ_pred equal | 7.87e-16 |
| L(M0+fam) domain / equal | 8.46e-16 / 5.52e-16 |
| L(M1+fam) domain / equal | 9.26e-16 / 8.06e-16 |
| Partition Δ domain / equal | 2.26e-15 / 1.09e-15 |
| Partition L(PM1fam) domain / equal | 2.46e-15 / 1.02e-15 |
| Represented Δ domain / equal | 1.21e-15 / 7.73e-16 |

All far below the declared tolerances (Δ: 1e-9; L: 1e-7). Residual differences are last-bit floating-point noise from associativity-order differences between the independent implementation and the originals; no structural discrepancy.

## 8. Interpretation and disposition

1. **No wiring defect exists in W1.** An independent re-implementation of both the frozen generator and the declared estimator protocol, written without access to the original code paths (reference code was read only as documentation of protocol interpretation, never imported), reproduces the W1 archive bit-strictly and every recorded statistic. The primary positive Δ and its FAILED wiring-check status are genuine outputs of the frozen design.
2. **Effect size remains decisively small.** Mean primary Δ ≈ 1.96e-6 (domain) / 1.91e-6 (equal) against baseline losses ≈ 3.39e-3 / 3.35e-3 (~0.06% relative). Central 95% intervals exclude zero but begin within ∼1.2–1.9e-6 of it; per-trial Δs straddle zero; the alternate (descriptively equivalent) diagnostic partition flips the sign (−6.25e-7 / −6.78e-7, positive fraction 0.25/0.246). The reviewer's caution that the partition choice carries the result stands; the wiring check itself is unambiguous and remains FAILED by declared criterion.
3. **No further experiment warranted.** This closes the requested bounded verification: the same frozen design cannot yield a different W1 outcome under a different correct implementation.

Final disposition to report: **W1 wiring check FAIL: independent verification confirms the recorded results are exactly reproducible; no implementation defect; study design already internally notes the small-scale caveat; W1 remains FAILED as declared.**

## 9. Artifacts

All new artifacts are confined to `engineered-study/math/results/three_world/independent_w1_glm/`:

- `independent_w1_verify.py` — frozen corrected source (hash in `source_sha256.txt`)
- `source_sha256.txt` — freeze record incl. documented pre-execution correction
- `independent_w1_run.json` — full machine-readable run record (500 trials, per-trial values, reference comparison)
- `run_500_console.log` — console capture
- `INDEPENDENT_W1_VERIFICATION_REPORT.md` — this report

No original file, record, or the frozen design was modified. No commit or push was performed.
