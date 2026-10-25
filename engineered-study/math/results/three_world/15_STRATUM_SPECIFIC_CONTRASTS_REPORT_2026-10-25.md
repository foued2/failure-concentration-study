# Saved-record-only stratum-specific concentration contrasts

**Report date:** 2026-10-25  
**Status:** Descriptive overlap analysis completed. The frozen scientific disposition remains **W1 FAILED**.  
**Branch:** `research/concentration-math-spec`

## Purpose

This report records the descriptive fixed-k, within-carrier score contrasts computed from the existing three-world synthetic simulation archive. It closes the previously outstanding descriptive reporting item without rerunning the simulation, changing the frozen design, or revising the original scientific result.

The research question is whether diagnostic concentration, defined as `C = max(F) / k` for `k > 0`, carries information about held-out evaluation score beyond total diagnostic failures `k`. Concentration is undefined when `k = 0`.

## Input provenance and integrity

The saved-record analysis used the eight existing compressed JSONL files listed in `manifest.json`, with 2,500,000 records per setting and 20,000,000 records in total. The analysis script checked each consumed archive's byte count and SHA-256 against the manifest before reading; verified the record counts; checked the recorded setting and world, the six-element diagnostic and evaluation vectors, `k = sum(F)`, the defined/undefined status and value of `C`, and both score calculations from the evaluation vector; and rechecked each archive's SHA-256 after reading.

Before the analysis, all nine payload files in the local archive copy (the eight compressed JSONL files plus `per_trial.json`) were also reported as verified against the manifest. `per_trial.json` was not consumed by this descriptive contrast script.

The manifest byte hash printed by the local run was `16af20b8b92856f8a5336737039da43609128caa5eb188ef40e7f3181dca7575`. That hash describes the local working-copy bytes with Windows line endings, not the GitHub blob representation. The repository-stored manifest uses different line endings. The eight compressed payload files were checked against the asset sizes and hashes declared in the manifest; the line-ending difference in the manifest representation is not a claim that the payload files differ.

The raw archive remains local-only and is deliberately not included in this commit.

## Method

Each stratum was defined by **setting × realized world × carrier family × fixed `k`**. At fixed `k`, the observed concentration levels correspond to the observed values of `max(F) / k`.

For every stratum with at least two distinct observed `C` values, the script calculated the unadjusted difference between:
- the mean evaluation score among cases at the highest observed `C`, and
- the mean evaluation score among cases at the lowest observed (C).

The sign is therefore **high-`C` mean score minus low-`C` mean score**. A positive value means that the high-(C) cases in that stratum had a higher average score. The summaries below report the mean and median of the stratum-level differences, weighting each stratum equally, as well as the number of positive, negative, and numerically zero contrasts.

These are descriptive extreme-level comparisons. They are not adjusted effects, causal effects, estimates of cross-validated predictive gain, or statistical inference. No p-values, confidence intervals, model fits, or hypothesis tests were produced by this analysis.

## Overall counts

| Quantity | Result |
|---|---:|
| Raw records read | 20,000,000 |
| Eligible records with `k > 0` | 19,999,737 |
| Records with (k=0), where (C) is undefined | 263 |
| Carrier-family-by-`k` strata across settings/worlds | 973 |
| Strata with at least two observed (C) values | 756 |

### Counts by setting and realized world

“Cases in multi-`C` strata” counts all eligible cases belonging to strata with at least two observed (C) levels, not only cases at the high and low endpoints.

| Setting | Realized world | Cases | Eligible (k>0) | Multi-(C) strata | Eligible cases in multi-(C) strata | Fraction of eligible cases |
|---|---|---:|---:|---:|---:|---:|
| MIX_0_0 | W2 | 2,500,000 | 2,500,000 | 0 | 0 | 0.0000 |
| MIX_0_25 | W1 | 624,238 | 624,218 | 123 | 621,980 | 0.9964 |
| MIX_0_25 | W2 | 1,875,762 | 1,875,762 | 0 | 0 | 0.0000 |
| MIX_0_5 | W1 | 1,250,445 | 1,250,411 | 127 | 1,248,040 | 0.9981 |
| MIX_0_5 | W2 | 1,249,555 | 1,249,555 | 0 | 0 | 0.0000 |
| MIX_0_75 | W1 | 1,874,354 | 1,874,306 | 126 | 1,870,597 | 0.9980 |
| MIX_0_75 | W2 | 625,646 | 625,646 | 0 | 0 | 0.0000 |
| MIX_1_0 | W1 | 2,500,000 | 2,499,947 | 126 | 2,494,881 | 0.9980 |
| W1 | W1 | 2,500,000 | 2,499,949 | 128 | 2,495,826 | 0.9984 |
| W2 | W2 | 2,500,000 | 2,500,000 | 0 | 0 | 0.0000 |
| W3 | W3 | 2,500,000 | 2,499,943 | 126 | 2,494,928 | 0.9980 |

The mixture rows are stratified by the realized W1/W2 label. W2 contributes no within-stratum concentration contrast because its construction makes `C = 1` for all eligible cases. The mixture settings are synthetic stress tests, not estimates of real-world mechanism prevalence.

## Stratum-level high-(C) minus low-(C) score differences

The reported mean and median are over strata, not over individual cases. The last columns count the direction of the stratum-level contrasts.

| Setting | Realized world | Strata | Mean \(\Delta S_D\) | Median \(\Delta S_D\) | Positive / negative / zero \(S_D\) | Mean \(\Delta S_F\) | Median \(\Delta S_F\) | Positive / negative / zero \(S_F\) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| MIX_0_25 | W1 | 123 | +0.0109708 | +0.0080803 | 95 / 28 / 0 | +0.0085523 | +0.0100222 | 86 / 37 / 0 |
| MIX_0_5 | W1 | 127 | +0.0113341 | +0.0094822 | 96 / 31 / 0 | +0.0121300 | +0.0103310 | 96 / 31 / 0 |
| MIX_0_75 | W1 | 126 | +0.0079683 | +0.0065713 | 88 / 38 / 0 | +0.0094239 | +0.0115631 | 92 / 34 / 0 |
| MIX_1_0 | W1 | 126 | +0.0106781 | +0.0088527 | 91 / 35 / 0 | +0.0090743 | +0.0085116 | 93 / 33 / 0 |
| W1 | W1 | 128 | +0.0083141 | +0.0071520 | 92 / 36 / 0 | +0.0074300 | +0.0092900 | 93 / 35 / 0 |
| W3 | W3 | 126 | +0.0021625 | +0.0045178 | 81 / 45 / 0 | +0.0012967 | +0.0045965 | 81 / 45 / 0 |

Here `S_D` is the frozen domain-weighted score and `S_F` is the frozen equal-family score. Scores range from zero to one, so a difference of (+0.01) corresponds to one percentage point.

Across the displayed strata, the mean and median extreme-level differences are positive for both score definitions. This is a description of the saved synthetic records, not evidence that (C) improves out-of-sample prediction once the full frozen comparison is applied.

## Interpretation and relation to the frozen result

### W1 remains FAILED

The frozen primary estimand compares cross-validated prediction loss with and without `C`, using the same eligible cases, folds, categorical `k` effects, and family adjustment. That is different from comparing the highest and lowest observed (C) levels within a stratum.

In the frozen simulation report, W1's mean incremental predictive gain from adding `C` was approximately (1.96\times10^{-6}) for `S_D`, with central 95% simulation-trial interval ([-1.24\times10^{-6},\,7.58\times10^{-6}]). For `S_F`, the mean was approximately (1.91\times10^{-6}), with interval ([-1.83\times10^{-6},\,8.99\times10^{-6}]). Both intervals include zero, and the frozen alternate-partition check did not establish the required positive gain. **The W1 wiring criterion therefore remains FAILED.** These new descriptive contrasts do not change that finding.

### W3 shows why descriptive contrasts are not a direct-effect test

The W3 data-generating process makes evaluation reach independent of diagnostic concentration conditional on the latent defect count and declared construction. Nevertheless, the high-(C) versus low-(C) contrasts are positive on average. In this simulation, (C) can act as a proxy for latent defect structure, so fixing `k` and the anchor/carrier label does not fix latent defect count. The original W3 oracle comparison, which also includes latent defect count, remains the relevant diagnostic for the distinction in the frozen design.

### W2 has no concentration overlap

W2's `C` does not vary among eligible cases. It cannot identify a within-W2 concentration contrast; its absence of contrast is expected, not evidence of a precisely estimated zero concentration effect.

## Limits

- All observations analyzed here are synthetic, generated under the frozen assumptions. They are not naturally generated solver observations.
- The high-versus-low comparison uses the extreme observed (C) levels within each stratum and does not estimate a causal or independent effect of `C`.
- The summaries are equally weighted over strata. They are not case-weighted pooled effects.
- A positive contrast can occur because (C) carries proxy information about latent variables. The W3 result illustrates this limitation.
- The mixture sweep is a designed sensitivity exercise, not a prevalence estimate.
- This report does not add a model, perform inference, or justify another simulation. The raw per-trial archive remains local-only.
- The frozen design, original simulation result, and closure amendment remain unchanged.

## Reproduction

From the repository root, after placing the verified local-only raw archive at the path expected by the script, run the saved-record-only analysis with the pinned interpreter:

```powershell
py -V:Astral/CPython3.14.0 engineered-study/math/analyze_stratum_specific_contrasts.py
```

The script's detailed Markdown and JSON outputs are local run artifacts under `engineered-study/math/results/three_world/stratum_specific_analysis/`. This committed report is a portable summary of the console results and contains no machine-specific paths or raw records.

## Related frozen materials

- [Frozen simulation design](../10_THREE_WORLD_SIM_DESIGN.md)
- [Original three-world simulation results](11_THREE_WORLD_SIM_RESULT.md)
- [Correction and closure amendment: W3 oracle distinction and contrast-reporting status](13_DOCUMENTATION_GAPS_CLOSURE_AMENDMENT_1_2026-10-24.md)
- [Saved-record contrast analysis script](../../analyze_stratum_specific_contrasts.py)
