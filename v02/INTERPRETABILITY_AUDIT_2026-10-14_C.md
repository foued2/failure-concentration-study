# v0.2 Interpretability Audit — Addendum C: Ratio Correction and Narrowed Interval Wording

**Date:** 2026-10-14
**Status:** append-only correction to `v02/INTERPRETABILITY_AUDIT_2026-10-14_B.md` (commit `c75fb43`, preserved unamended; note A at `da4030d` likewise preserved). Issued per GPT's adjudication of addendum B and CLAUDE's instruction. No frozen file was edited, no pipeline stage re-executed, and no outcome regenerated.

## 1. Ratio correction (explicit values)

Addendum B §2 (check 3) archived the spread figures as: population std of the 40 `delta_i` values `5.008826427687712e-06`, persisted CI width `3.1013670966861807e-06`, range `2.5133693763890186e-05`, and the phrase "range/width ratio 8.10". On inspection, that archived label is correct — 8.104… is the range divided by the CI width. The mislabeling occurred in the session summary accompanying the publication, which juxtaposed the population standard deviation against the CI width and then quoted 8.1, implying a std/width ratio. For the record, both ratios with explicit inputs (arithmetic in the Appendix):

| Quantity | Value |
|---|---|
| population std / CI width | `5.008826427687712e-06 / 3.1013670966861807e-06 = 1.6150382304112456` |
| range / CI width | `2.5133693763890186e-05 / 3.1013670966861807e-06 = 8.104069263759717` |

No underlying value in addendum B is changed; only the labeling ambiguity is resolved here. Neither ratio is used as a premise anywhere in the audit; both are descriptive spread summaries of the 40 archived `delta_i` values.

## 2. Narrowed interval wording (supersedes "calibrated" in addendum B §4)

Addendum B §4 described the interval as "a calibrated uncertainty interval for the mean score difference over the hidden-suite generator's draws". That wording is **withdrawn** and replaced by:

> The interval reproduces the preregistered bootstrap procedure applied to 40 distinct hidden-suite instances. It describes uncertainty under that procedure and the frozen generator, subject to the validity of the resampling assumptions. It does not establish generalization to unseen diagnostic probe suites or unseen solvers.

Supporting record, checked against the frozen files:

- The frozen protocol prespecified the procedure — `PROTOCOL_V02.md` §3: "Uncertainty resamples instances, never inputs or solvers"; §4 table: "10 000 instance bootstrap resamples, 95 % CI"; `spec_v02.json`: `n_boot=10000, seed=99, ci=0.95`. It did **not** establish the statistical coverage of that procedure: nothing in the frozen protocol or the supporting analyses justifies exchangeability of the 40 contributions.
- The 40 resampled contributions are leave-one-instance-out score differences computed through **overlapping training folds** (each fold omits a different instance out of 40); they are therefore dependent, while the percentile bootstrap resamples them as exchangeable units.
- Addendum B's bitwise reproduction of the published interval from the persisted `delta_i` establishes **computational reproducibility only** — not coverage.

This is a limitation on the interpretation of the interval, not grounds to change the formal result.

## 3. Persistence gap (restated)

Per-solver outcome vectors were not persisted in the confirmatory report (addendum B check 2: NOT PERFORMABLE). The 40 distinct `delta_i` values evidence variation in the aggregate instance-level contributions but are not a substitute for the missing outcome vectors.

## 4. Disposition (four conclusions, kept distinct)

1. **Formal result:** v0.2 remains NEGATIVE under its frozen decision rule (CI upper bound 1.583 × 10⁻⁶ < δ = 0.01); unchanged by this audit series.
2. **Identifiability:** the realized design cannot distinguish the incremental contribution of concentration from information already encoded by failure count — C = 5/k on 90/90 eligible pilot rows, constant per solver across all 40 instances (shared probe suite), and the augmented design matrix gains no rank.
3. **Predictive hypothesis:** unresolved — neither established nor refuted that independently varying family concentration improves prediction of correctness.
4. **Generalization:** the result concerns hidden-suite variation conditional on the shared diagnostic-probe construction and the fixed solver pack; it does not establish robustness to new diagnostic probes or new solvers.

The experiment did not fail because its hidden instances were duplicated — they were not (40/40 distinct hidden-suite hashes, addendum B check 1). The central predictor-comparison question remained unanswerable because the concentration feature was aliased with failure count. These two statements remain separate in the archive.

## 5. Closure

The v0.2 interpretability audit (note A and addenda B and C) is **closed with limitations recorded**. Nothing further is authorized by this audit. A successor design with equal-k, different-C submissions is the repository owner's decision; the record does not settle it.

## Appendix — ratio arithmetic (explicit values)

```python
pop_std = 5.008826427687712e-06
ci_width = 3.1013670966861807e-06
rng = 2.5133693763890186e-05
print(f"pop_std            = {pop_std!r}")
print(f"ci_width           = {ci_width!r}")
print(f"range              = {rng!r}")
print(f"pop_std / ci_width = {pop_std / ci_width!r}")
print(f"range / ci_width   = {rng / ci_width!r}")
```

```text
pop_std            = 5.008826427687712e-06
ci_width           = 3.1013670966861807e-06
range              = 2.5133693763890186e-05
pop_std / ci_width = 1.6150382304112456
range / ci_width   = 8.104069263759717
```
