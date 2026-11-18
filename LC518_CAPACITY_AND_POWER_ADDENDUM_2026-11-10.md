# LC518/150 — Capacity envelope and finite-sample power addendum

**Date:** 2026-11-10
**Status:** record-keeper arithmetic and power-planning record. Not a feasibility finding, not a GO, not a ratification of B1.
**Relation to other records:** two additions to GPT's revision 2 review points, as agreed in chat. Supplies §3 A1a of `LC518_CONCENTRATION_ESTIMAND_REVIEW_2026-11-05.md` and the open power rule in `engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md:228`. It does **not** answer GPT revision 2's parent-by-concentration incidence request (§5).

## 0. Non-claims

- Capacity is a property of the bank layout. It is not feasibility. The mutation system may force every realized failure vector into a single stratum (`LC518_CONCENTRATION_ESTIMAND_REVIEW_2026-11-05.md` §3, degenerate counterexample).
- The envelope bounds the static support of `C_D` at a given `k_fail`. It does not predict how many parents land at a given `k_fail`, which is the population model's job.
- No empirical residual variance exists. The power numbers below are planning multipliers, not validation.

## 1. Notation

`C_D = max_j f_j / k_fail` for `k_fail > 0`, per `.qoder_reviewdraft.md:44`. Strata `D1–D7` hold 8 records each; `D6` holds 4 canonical instances × 2 orderings (`.qoder_reviewdraft.md:23`; `engineered-study/banks` frozen bank). "Contrast holds at `k`" means the attainable set of `C_D` at total failures `k` contains at least two values, i.e. `min over feasible allocations of max_j f_j < k`. The forcing condition is `min over feasible allocations of max_j f_j = k`.

## 2. Addition 1 — two capacity envelopes, not one

Checked by exhaustive enumeration of feasible integer allocations (`f_j ≤ stratum capacity`, `Σ f_j = k`), all `k` from 2 to the bank total.

| Counting basis | Capacities | Total | Contrast holds | Maximum forced | Allocation vectors ≤ last contrast `k` |
|---|---|---|---|---|---|
| Record-level | 8×8 | 64 | 2 ≤ k ≤ 56 | k ≥ 57 | 43,040,286 (k ≤ 56) |
| Canonical | 8×7, 4×1 | 60 | 2 ≤ k ≤ 53 | k ≥ 54 | 23,911,851 (k ≤ 53) |

Record-level frontier facts (confirmed against GPT): at `k = 57` the maximum is forced to 8, and at `k = 56` the only feasible shape has the maximum at 7. At `k = 57` the forced-8 allocations number `C(8,7) = 8`; the remaining 96 allocations have maximum 6 and sit outside the capacity bound. At `k = 64` exactly one allocation is feasible.

Canonical frontier facts: `k = 53` (the last contrast `k`) admits only 3,396 allocations, of which 8 are distinct stratum-level partitions, all with the maximum in `D6`'s single occupied canonical (`29/53`). At `k = 54` the slack-relaxed frontier admits 1,708 allocations / 784 partitions, all with the maximum equal to `k`. The sliver closes abruptly.

**Basis recommendation.** Use the canonical count, `2 ≤ k ≤ 53`, as the capacity basis. The two records of a `D6` ordering pair are the same canonical input reordered; under the frozen layout their outcomes are dependent, so counting them as two independent measurements inflates the apparent variation. Already required by `.qoder_reviewdraft.md:62,116`. Report the record-level envelope, `2 ≤ k ≤ 56`, only as an upper bound.

**Caveat on the sliver.** The A1a witness (`k = 2`) and the last-contrast `k` are both inside the envelope, but what actually matters is where the parent population puts its mass on `k_fail` (§5). A contrast at `k = 53` exists in principle and is practically irrelevant. The envelope is a necessary bound, not a design point.

## 3. Addition 2 — finite-sample multiplier for the power rule

The large-sample multiplier `z_{0.975} + z_{0.80} = 2.8016` is replaced by the exact **paired** multiplier `t(0.975, df) + t(0.80, df)` with `df = n − 1`, where `n` is the number of parents and the statistic is the per-parent paired ΔLL on identical grouped folds. (Correction 2026-11-10, second pass: an earlier revision called this a "two-group multiplier"; that label was wrong — a two-independent-group design would use `df = 2n − 2`. The `df = n − 1` values are correct for the paired per-parent statistic, which is the agreed estimand.) Computed from the incomplete-beta CDF (`t(0.975, 9) = 2.262`, `t(0.80, 9) = 0.883`, consistent with standard tables).

**Sidedness must be pinned.** This section and the chat discussion use a two-sided critical value, but `engineered-study/power/simulate.py:18` uses one-sided `z_{0.95} = 1.6449`, whose large-sample multiplier is `1.6449 + 0.8416 = 2.4865`, about 13% below 2.80. The directional alternative (ΔLL > 0) makes one-sided defensible; the frozen analysis plan must declare the convention before any MDE is reported.

**Exact noncentral-t reference (added 2026-11-10, second pass).** The t-sum multiplier is an approximation; the exact paired-t MDE solves `P(t'_{df, δ} > t_crit) = 0.80` for the noncentrality `δ`, computed by numerical integration over the χ² mixing distribution (sanity check: df = 1000 reproduces the t-sum to four decimals). Exact values, two-sided convention: df 2 → 5.74, df 4 → 3.76, df 11 → 3.08, df 17 → 2.97, df 23 → 2.93, df 29 → 2.90, df 39 → 2.87, df 49 → 2.86, df 59 → 2.85. The t-sum understates the exact MDE by 7.0% at df 2 and 1.2% at df 4, and by at most 0.1% for df ≥ 9 — so at the proposed parent grid (12–60 parents, df 11–59) the correction is negligible, and the simulation's necessity comes from the grouped-CV and support-cell structure, not from the noncentral refinement.

| Parents/group `n` | df | Exact multiplier | Inflation vs 2.80 | Note |
|---|---|---|---|---|
| 3 | 2 | 5.36 | +91% | test nearly uninformative |
| 5 | 4 | 3.72 | +33% | |
| 10 | 9 | 3.15 | +12% | matches chat figure (≈3.15) |
| 20 | 19 | 2.95 | +5% | matches chat figure (≈2.95) |
| 30 | 29 | 2.90 | +3.5% | |
| 100 | 99 | 2.83 | +1% | |

Chat's "`n = 3` → 6.19" (corrected 2026-11-10, second pass) reads the df-2 two-sided-80% column entry — 1.886 is `t(0.90, 2)`, the one-sided-90% quantile — instead of the one-sided-80% quantile `t(0.80, 2) = 1.061`. The correct t-sum is `4.303 + 1.061 = 5.36`; the exact noncentral value is 5.74. Both are below 6.19, so the chat figure was conservative but derived incorrectly.

Consequences for the plan:

1. The existing analytic MDE in `engineered-study/power/simulate.py:48` uses `(z_{0.975}+z_{0.80})·σ·√(1/n_h+1/n_l)`. It is replaced by the `t`-based multiplier at the realized parent count, and the final power table is produced by simulation over the actual support-cell procedure, not by the two-group formula.
2. The unit of `n` is parents, not observation slots. The present `simulate.py` pools 150 slots (`HIGH_SLOTS = 120`, `LOW_SLOTS = 30`) and must not be reused for the new estimand.
3. Grouped parent resampling (leave-parents-out folds, test on unseen parents) replaces the single split.

## 4. Agreed statistic

Per-parent mean log-loss improvement, equal parent weighting, expressed in nats per held-out observation. Parents are the sampling unit; no variant-level standard deviation is reported or used. Training and test partitions are both split by parent, so every held-out observation comes from parents absent from training.

## 5. What is still blocked

GPT revision 2 asks for parent-by-concentration incidence per cell, parent counts, and alternative population sizes. Each of those is a functional of the population model: the distribution of `k_fail` across parents and the conditional distribution of failure vectors given `k_fail`. The capacity envelope in §2 bounds the second only. Without the model, the incidence table and the power simulation cannot be computed, and I cannot draft the model without making design choices that belong to the owner and GPT.

**Proposed division:** GPT drafts the population model (generation of parents, failure-vector distribution); I audit its implied incidence against the canonical support rule `⌈k/8⌉/k ≤ C_D ≤ 1` (`PROTOCOL.md` / `.qoder_reviewdraft.md:56`), against the canonical envelope `2 ≤ k ≤ 53`, and against the three-parent same-cell floor (`LC518_CONCENTRATION_ESTIMAND_REVIEW_2026-11-05.md` §3, rev 2.6 §5). I then compute per-candidate support incidence and run the simulation with the §3 `t`-based multiplier and §4 grouped-parent procedure.

**Open status:** B1 eight-stratum feasibility stays open. Verified static bound: canonical envelope `2 ≤ k ≤ 53`; record-level envelope `2 ≤ k ≤ 56` as upper bound only.
