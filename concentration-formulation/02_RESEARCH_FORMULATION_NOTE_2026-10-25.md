# Research-formulation note: does failure concentration carry information beyond failure count?

**Date:** 2026-10-25  
**Status:** formulation only (Claude Doc export, rev 3). Every hypothesis below is **proposed, not demonstrated**. This note is not an implementation plan and authorizes no solver generation, execution, simulation, model calls, data collection, or repository change beyond this record. The failure-concentration project remains closed under its existing authorization.

## 1. Purpose

Two claims have been mixed together in this project. This note separates them, states what is settled, and formulates what is not, with the assumptions named.

## 2. Setting and definitions

- A diagnostic instrument has six families with `p` probes each (`p = 5` in the natural-solver runs). `f_j` is the number of failed probes in family `j`, and `F = (f_1, ..., f_6)`.
- `k = sum_j f_j` is the failure count.
- `C = max_j f_j / k`, defined only for `k > 0`.
- **B1** is the strict decision rule: accept if `k = 0`, reject if `k > 0`.
- `C` depends on `F` only through its largest entry and the total. It does not depend on which family fails.

## 3. What is settled: universal correctness

Assume the tests are valid, their expected results are correct, and execution is reliable. Then:

- A failing test is a counterexample, so a solver with `k > 0` is not universally correct, whatever its failure pattern. `C` cannot overturn that.
- Passing a finite test set does not prove universal correctness, so B1 can accept wrong solvers. `C` is undefined at `k = 0`, so it cannot help there either.
- The EvalPlus study (Liu et al., NeurIPS 2023) is practical evidence that small test sets pass wrong programs. Its reported size of the effect differs between summaries of the paper, so no figure is relied on here.

**Consequence.** Concentration cannot improve B1's binary decision about universal correctness. This part is not a hypothesis. The question that remains is empirical and about held-out performance, not universal correctness.

## 4. Two research questions

They have different practical meanings and are not to be conflated.

- **Q1 (prediction).** Does `C` improve prediction of held-out average performance beyond `k`?
- **Q2 (ranking).** Among rejected candidates with the same `k`, does `C` rank them by held-out performance better than an arbitrary order?

A variant of Q1 concerns spread and tail events, treated in Section 6.

## 5. When `k` alone is enough for the original six-family target

The original target was a family-balanced score on held-out inputs from the same six families. The precise statement is as follows.

The observed family-balanced failure rate is `R_hat = (1/6) sum_j f_j / p = k / (6p)`, which is `k / 30` for `p = 5`. Hence `C` adds nothing to the observed average failure rate once `k` is known. (An earlier draft called `k` "close to a sufficient statistic". That wording was imprecise. The statement above is the correct one.)

This does not show that `C` cannot help predict future outcomes. It shows that any help has to come from how the observed average relates to the future average, which depends on the sampling model.

**A reference model.** Suppose that, within family `j`, probes are independent samples from inputs with true held-out failure rate `theta_j`, so `f_j ~ Binomial(p, theta_j)`. Suppose the six `theta_j` have independent, identical `Beta(a, b)` priors. Then the posterior for `theta_j` is `Beta(a + f_j, b + p - f_j)`, and for the family-balanced target `R = (1/6) sum_j theta_j`:

- The posterior mean is `(6a + k) / (6(a + b + p))`, which depends on `F` only through `k`.
- The posterior variance of `R` is `(1/36) sum_j (a + f_j)(b + p - f_j) / ((a + b + p)^2 (a + b + p + 1))`. The numerator sum equals `6(ab + ap) + k(b + p - a) - sum_j f_j^2`. At fixed `k`, it depends on `F` through `sum_j f_j^2`.

Two observations follow, both conditional on this model:

1. Under the specified independent, identical Beta-prior reference model, the posterior mean depends only on `k`. This result should not be generalized to arbitrary exchangeable models: with correlated family rates, the posterior mean of the overall average can depend on how `F` is distributed, not just on its total.
2. The posterior **variance** changes when a fixed number of failures is redistributed among families, through `sum_j f_j^2`, which is related to `C` but not identical to it. The posterior mean is unchanged by redistribution, but the full predictive distribution can depend on more of `F` than either `k` or `C` captures. So `C` is a candidate predictor of uncertainty, not a proven sufficient summary of it. This is a remark about the reference model and does not change the primary feature, which stays `C`.

**What Q1 tests.** Q1 tests whether `C` adds out-of-sample predictive value for the specified mean-performance target, conditional on `k`. A positive result would establish incremental predictive value in that target population. It would not identify the mechanism responsible.

**Known violation in the saved data.** The v0.2 probes within a family are variations of one property, so within-family outcomes are not independent: every eligible row has `f_j` equal to 0 or `p`. The binomial assumption fails there. The model is a reference for what "no extra information in `C`" looks like, not a description of the data.

**Mean versus uncertainty.** A concentration measure could help predict extreme outcomes or threshold decisions without improving prediction of the mean. The research must state which of the two it targets.

## 6. Variant: spread and threshold events

Q1b: does `C` improve prediction of the **distribution** of future family-balanced performance, such as the probability of exceeding a stated failure rate, beyond `k`? It requires a predictive distribution and a proper scoring rule for it, and a pre-declared threshold. It is listed separately because the reference model in Section 5 suggests that if `C` carries information, it is more likely to concern spread than the mean.

## 7. The out-of-instrument target

"Unseen input types" is not a target. A target for transfer must be:

- a **pre-specified input domain**, defined by a stated construction rule before any outcome is seen;
- **independently evaluated**, disjoint from the diagnostic bank and from any in-instrument held-out bank;
- **bounded**, so the domain can be described exactly and failure sets compared;
- stated together with its scoring rule (family-balanced or pooled), chosen to match the population the claim is about.

A transfer claim applies only to that domain. A high `C` does not show that a weakness is narrow or that it stays narrow on unfamiliar inputs. Both concentrated and dispersed failures can arise from different mechanisms.

## 8. Proposed hypotheses (not demonstrated)

The motivating direction is that higher `C` at fixed `k` means a narrower weakness and better held-out performance. Tests are two-sided, and each hypothesis has three distinct outcomes: evidence for the proposed direction, evidence for the opposite direction, and insufficient evidence of a meaningful association. A reversed association contradicts the proposed direction even if `C` still carries predictive information, and it would not support a rule that prefers higher `C`.

| Hypothesis | Statement | Baseline | Contribution attributed to `C` |
| --- | --- | --- | --- |
| H1 (Q1, in-instrument) | At fixed `k`, `C` predicts held-out average performance on the same six families | `k` only | Reduction in held-out loss on new defect groups |
| H2 (Q1, transfer) | Same, on the pre-specified out-of-instrument domain | `k` only | Reduction in held-out loss on that domain |
| H3 (Q2, ranking) | Among rejected candidates with equal `k`, higher `C` ranks better on held-out performance | Arbitrary order within `k` | Rank agreement within each `k` stratum |
| H4 (Q1b, spread) | `C` improves prediction of the spread or threshold-event probability | `k` only | Improvement in a proper scoring rule for the predictive distribution |

At fixed `k` a `k`-only baseline gives equal predictions, so for H3 the comparison is against arbitrary ordering, not against a fitted model.

**Evidence that would count against a hypothesis.**

- An interval for the gain that is precise and centered near zero, so any gain is below a practically meaningful size. A wide interval is inconclusive, not evidence against.
- A reversed sign of the effect.
- A gain that disappears when whole defect groups are held out.
- A gain fully explained by family identity or by the number of defects.

The smallest practically meaningful gain and the uncertainty procedure must be fixed before any data exist.

**Units of independence (to be defined before any study).** Two kinds of independence are handled separately: independent solvers do not give independent inputs, and the reverse.

- **Solver unit.** The independent unit is the defect group, not the generated body. Replicas of one generated solver body, and closely related outputs from the same generation process or mutation site, count as one unit. In the saved v0.2 data, 90 rows come from ten base bodies, so the body is the most that could count.
- **Defect group.** A set of solvers that share at least one mutation site or code component. It is different from a probe family (a set of diagnostic probes), from an input (one test case), and from a solver (one program). Held-out folds are formed by defect group, so no site appears in both training and test data.
- **Input cluster.** Test inputs derived from the same underlying defect mechanism or construction template form one cluster. A cluster is assigned whole to the diagnostic bank, the in-instrument held-out bank, or the out-of-instrument domain, so related inputs cannot leak across banks and make transfer look stronger than it is.

**Feasible support.** With six families of `p = 5` probes, some strata allow no variation in `C`: `k = 1` forces `C = 1`, and `k = 29` forces `C = 5/29`. For `k > 5`, `C <= 5/k`. How many values of `C` are attainable at each `k` is a property of the instrument. Variation in `C` at fixed `k` must be demonstrated for the particular strata a study would use, because a larger sample cannot create it.

## 9. Identification requirements carried forward

These are lessons from the earlier work, not a design.

- The comparison must hold `k` fixed. The saved v0.2 data cannot provide this, because `C = 5/k` throughout, and the natural inventory found no same-`k`, different-`C` pairs.
- The v0.2 instrument builds defects that fail all of a family or none of it, so partial-family variation may need a different kind of defect or a different instrument.
- Independent units must be defined (site groups, not sampled solvers), with leakage control between training and test.
- `C` has tracked a hidden variable in each earlier setting: algorithm type in the old Doctor project, failure count in v0.2, and family size and defect identity in the engineered Gate 1 work.

## 10. Literature status

- **Verified in this thread (abstracts):** EvalPlus on test inadequacy; failure clustering and failure indexing for debugging (Hybiscus, GREClue); the similarity of failing tests for patch correctness (BATS, Tian et al., ACM TOSEM 2022).
- **Reported by GPT, titles not independently checked by me:** SimSCOOD (NAACL Findings 2024) on out-of-distribution generalization of code models, Fault-Aware Neural Code Rankers (NeurIPS 2022), and Uncovering Weaknesses in Neural Code Generation (2024).
- None of these tests `C` against `k`. This is an adjacent literature and not a validation. No claim of novelty or duplication is made, and a systematic review is needed before either.

## 11. What this note does not do

- It does not provide a design, a sample size, a model class, or any run.
- It does not claim that `C` has predictive value, or that it lacks it.
- It does not reopen the closed study.

## 12. Open items

- The out-of-instrument domain, its scoring rule, and its bound.
- The smallest practically meaningful gain, and the uncertainty procedure.
- Whether Q1b is worth a separate treatment.
- A systematic literature review before any novelty claim.

*Revised 2026-10-25 after review: the reference-model claim is narrowed to the stated Beta-Binomial model, direction is separated from the two-sided test, and units of independence and feasible support are added.*
