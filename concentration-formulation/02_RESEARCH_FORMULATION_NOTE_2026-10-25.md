# Research-formulation note: does failure concentration carry information beyond failure count?

**Date:** 2026-10-25  
**Status:** reconciled research-formulation candidate, revision 5, recorded on the review branch. Every hypothesis below is **proposed, not demonstrated**. This is a research record, not an implementation plan or authorization to generate or execute solvers, simulate, call models, collect data, or change other repository files. The failure-concentration project remains closed under existing authorization. This file is the active formulation candidate for this repository branch; a separately reported local copy was not available for byte-for-byte comparison, so identity with that copy is not claimed.

## 1. Purpose

Two claims have been mixed together in this project. This note separates them, states what is settled, and formulates what is not, with the assumptions named.

## 2. Setting and definitions

- A diagnostic instrument has six families with `p` probes each (`p = 5` in the natural-solver runs). `f_j` is the number of failed probes in family `j`, and `F = (f_1, ..., f_6)`.
- `k = sum_j f_j` is the failure count.
- `C = max_j f_j / k`, defined only for `k > 0`.
- **B1** is the strict decision rule: accept if `k = 0`, reject if `k > 0`.
- `C` depends on `F` only through its largest entry and the total. It does not depend on which family fails.
- **Historical exposure of the legacy partition:** the six-family, `p = 5` instrument has already been used in v0.2 and Gate 1, where failures were observed. The record here does not establish that the family partition itself was frozen before those historical outcomes, so its status is conservatively **outcome-exposed**. Freezing it now would not erase that history.
- **If the legacy partition is reused:** freeze its exact mapping and all weights before any new candidate is generated, but describe the study as a prospective replication using a previously outcome-exposed feature definition, not as a clean first confirmatory test of a pre-specified partition. Its result is conditional on the legacy taxonomy and retains possible design-selection optimism.
- **If a cleaner confirmatory test is required:** define a genuinely new partition from documented task semantics and measurement criteria before the new candidate sample exists, with partition authors blinded to prior failure-profile tables where feasible. This changes the operational definition of `C`, so it is a new operationalization of the max-family-count hypothesis, not an exact replication of legacy `C`. The choice and rationale must be documented before examining outcomes from the new sample.
- **Eventual protocol freeze record:** a later authorized protocol must be frozen before candidate generation and before held-out scores are accessible. Record the repository, an annotated tag and its full target commit SHA, UTC timestamp, and hashes of the partition specification, generator/sampling frame, diagnostic and evaluation input manifests, scoring rules, and analysis code. Do not move the tag or amend the frozen version after outcomes are seen; any outcome-informed change requires a new version and a new confirmatory sample. This note is not itself a protocol freeze and authorizes no experiment.

## 3. What is settled: universal correctness

Assume the tests are valid, their expected results are correct, and execution is reliable. Then:

- A failing test is a counterexample, so a solver with `k > 0` is not universally correct, whatever its failure pattern. `C` cannot overturn that.
- Passing a finite test set does not prove universal correctness, so B1 can accept wrong solvers. `C` is undefined at `k = 0`, so it cannot help there either.
- The EvalPlus study (Liu et al., NeurIPS 2023) is practical evidence that small test sets pass wrong programs. Its reported size of the effect differs between summaries of the paper, so no figure is relied on here.

**Consequence.** Concentration cannot improve B1's binary decision about universal correctness. This part is not a hypothesis. The question that remains is empirical and about held-out performance, not universal correctness.

## 4. Research questions and working primary hypothesis

The questions have different practical meanings and must not be conflated.

**Working primary question: H3 (ranking B1-rejected candidates).** The target population is naturally generated candidates in a pre-specified sampling frame that are rejected by B1, meaning `k > 0`. B1's rejection rule depends only on `k`, not on the family profile. H3 asks whether, among independent solver-side dependence groups with the same `k` **and the same pre-specified task/base-algorithm stratum**, the ordering induced by `max_j f_j` predicts performance on a separately constructed, held-out input domain. The proposed direction is that higher `C` predicts better held-out performance. This is a hypothesis, not a result. The claim applies only to the stated B1-rejected population and does not generalize automatically to candidates with `k = 0`, other tasks/base algorithms outside the sampling frame, or another selection rule. No additional inclusion or exclusion criterion may use the family failure profile unless it is pre-specified.

**What is actually being compared.** At a fixed `k > 0`, `C = max_j f_j / k`; therefore ranking by `C` is exactly the same ordering as ranking by `max_j f_j`. The proposed study would test whether the largest family-specific failure count adds information conditional on total failures. It would not establish a special property of the ratio itself.

**Primary estimand and weighting rule.** Work within each pre-specified task × base-algorithm × `k` cell. For every unordered pair of distinct solver-side dependence groups, form all cross-group candidate pairs that share the same task/base-algorithm and `k` but have different `C`. Score each candidate pair as `1` when the higher-`C` candidate has the better held-out score, `0` when it has the worse score, and `0.5` when the held-out scores tie. Average these values within each eligible dependence-group pair to make one value per group pair, then average those group-pair values equally within the cell. This is the chosen rule: do not switch to selecting one candidate per group after seeing the data. Thus candidates from larger groups do not dominate merely because a group contains more variants. Group pairs with no shared eligible `k`, or no same-`k` cross-group candidate pairs with different `C`, contribute no value to that cell and must be counted and reported; do not compare across `k` or across task/base-algorithm strata to fill the gap. Combine the cell estimates using weights declared before held-out scores are available; absent a target-population weighting justified and specified in advance, use equal weights across the pre-declared eligible task × base-algorithm × `k` cells. Ties in held-out score receive half credit. The chance-ordering reference is `0.5` under this convention.

**Task/base-algorithm control.** The older Doctor work reported that `C` tracked algorithm type, so a pooled cross-task result could reflect task composition rather than within-task ranking value. If more than one task or base algorithm is in the target frame, task identifier and base implementation/version are mandatory strata: compute concordance only within each task/base-algorithm/`k` cell, report every pre-specified task/base-algorithm result, and report the pre-weighted aggregate as a companion result. Cross-task candidate pairs are never part of H3. If the sampling frame fixes one task and one base algorithm by design, state that explicitly. A cell with inadequate support is not rescued by pooling candidates across tasks; its exclusion is determined by the outcome-blind support rule below, not by held-out scores.

**Dependence and uncertainty.** Pairwise comparisons are a dependent U-statistic, not independent observations. The proposed primary interval is a two-way cluster bootstrap with 5,000 replicates: independently resample whole solver-side dependence groups and held-out input-construction clusters within each pre-specified task stratum, keep all candidate variants in a sampled solver group and all inputs in a sampled input cluster together, recompute candidate held-out scores and the complete group-pair statistic, and form a 95% percentile interval for concordance and its gain over `0.5`. Never bootstrap pair rows as if independent. Report the fraction of resamples in which a target cell or the aggregate is undefined because support disappears; the protocol must set an acceptable invalid-replicate limit in advance, and exceeding it makes the interval non-confirmatory. A delete-one-solver-group jackknife is a pre-specified sensitivity analysis. The numerical practical-gain threshold and the invalid-replicate limit still require rationale before any held-out scores are inspected. If the target is explicitly an exhaustively enumerated finite evaluation domain, no input-population uncertainty is claimed and the input-cluster resampling component should be omitted by definition; this target choice must be fixed in advance.

**Population qualification.** The intended primary population is naturally generated solver candidates, but the generation mechanism, sampling frame, task/base-algorithm strata, and solver-side dependence groups are not yet operationally specified. The mutation-site combinations discussed in the separate Idea 1 feasibility note are a different population and cannot establish the primary claim about naturally generated candidates. Conditioning on `k > 0` is explicit selection under B1; the result is a conditional ranking claim, not a population-wide claim about all generated candidates.

**Secondary questions.**
- **Q1 (mean prediction):** Does `C` improve out-of-sample prediction of held-out average performance beyond `k`?
- **Q1b (spread and threshold events):** Does `C` improve prediction of the distribution of future performance or a pre-declared threshold event beyond `k`?
- Other ranking settings are secondary and must not be used to replace a failed primary result after outcomes are seen.

H1 to H4 below remain proposed hypotheses. A two-sided analysis distinguishes evidence for the proposed direction, the opposite direction, and insufficient evidence of a practically meaningful association. A reversed effect would contradict the rule that higher `C` is better even if the feature carried predictive information.

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

"Unseen input types" is not a target. The held-out score must measure performance on input clusters independently constructed from, and disjoint from, the diagnostic clusters. A target for transfer must be:

- a **pre-specified input domain**, defined by a construction rule before any candidate outcomes are seen;
- **input-cluster disjoint**, with related inputs kept together and no diagnostic input cluster reused for held-out evaluation;
- **not defined or weighted by the six diagnostic families**. If evaluation strata are needed, their construction rules and weights must be fixed independently of the diagnostic family partition and before any candidate outcomes are seen. This avoids a transfer result arising solely because the scoring target reuses the diagnostic partition by design; it does not rule out real correlations between diagnostic failures and held-out performance;
- **bounded**, so the target domain and score are precisely specified;
- paired with a pre-specified score (for example, a pooled failure rate or a balanced rate over independently defined evaluation strata) matching the target population.

A transfer claim applies only to that domain. A high `C` does not show that a weakness is narrow or that it stays narrow on unfamiliar inputs. Both concentrated and dispersed failures can arise from different mechanisms.

## 8. Proposed hypotheses (not demonstrated)

The motivating direction is that higher `C` at fixed `k` means a narrower weakness and better held-out performance. Tests are two-sided, and each hypothesis has three distinct outcomes: evidence for the proposed direction, evidence for the opposite direction, and insufficient evidence of a meaningful association. A reversed association contradicts the proposed direction even if `C` still carries predictive information, and it would not support a rule that prefers higher `C`.

| Hypothesis | Statement | Baseline | Contribution attributed to `C` |
| --- | --- | --- | --- |
| H1 (Q1, in-instrument) | At fixed `k`, `C` predicts held-out average performance on the same six families | `k` only | Reduction in held-out loss on new defect groups |
| H2 (Q1, transfer) | Same, on the pre-specified out-of-instrument domain | `k` only | Reduction in held-out loss on that domain |
| **H3 (working primary; ranking)** | Among independent solver-side groups with equal `k`, the ordering induced by `C` predicts held-out performance; proposed direction: higher `C` means better performance | Chance ordering (0.5 pairwise concordance) within `k` strata | Incremental, pre-specified rank concordance over chance, combined across eligible `k` strata |
| H4 (Q1b, spread) | `C` improves prediction of the spread or threshold-event probability | `k` only | Improvement in a proper scoring rule for the predictive distribution |

At fixed `k` and within a fixed task/base-algorithm stratum, a model using only `k` makes tied predictions. Therefore H3 compares the ordering induced by `C` with chance ordering within eligible cells; its metric, tie rule, group-pair weighting, cell weights, support gate, and meaningful-gain threshold must be frozen before evaluation.

**Evidence that would count against a hypothesis.**

- An interval for the gain that is precise and centered near zero, so any gain is below a practically meaningful size. A wide interval is inconclusive, not evidence against.
- A reversed sign of the effect.
- A gain that disappears when whole defect groups are held out.
- A gain fully explained by family identity, by the number of defects, or by task/base-algorithm composition that disappears in within-task/base-algorithm comparisons.

The smallest practically meaningful gain and the uncertainty procedure must be fixed before any data exist.

**Units and dependence (distinct concepts; operational rules are still required).**

- **Solver instance:** one generated candidate program body. Repeated execution or replica rows for the identical body are repeated measurements, not new independent solver candidates.
- **Defect group:** a mutation mechanism or identity class used to describe the underlying defect source. It is not itself automatically the statistical inference unit.
- **Solver-side dependence group:** a pre-defined group of solver instances linked by shared generation lineage, a common mutation site, shared code components, or another known source of dependence. This is the inference and validation cluster. Related candidates must be kept together across training and held-out folds.
- **Input cluster:** related test inputs derived from one construction template or underlying mechanism. Related inputs must be allocated together to one diagnostic or evaluation bank; the out-of-instrument bank must use pre-specified construction rules and be separate at the input-cluster level.
- **Probe family:** a designed category of diagnostic probes from which the family counts `f_j` are calculated. A probe family is not equivalent to a defect group or an input cluster.

Neither distinct program text nor different observed failure sets by itself proves statistical independence. Dependence groups must be justified from provenance and construction, with behavioral-alias checks treated as supporting evidence rather than proof of independence. The archived v0.2 data contain 40 solver bodies with three replicas each; the 120 solver-body/replica records are not 120 independent solver candidates.

**Feasible support gate and the low-`k` issue.** With six families of `p = 5` probes, the feasible maximum family count at total `k` lies between `ceil(k/6)` and `min(5,k)`. Therefore, `C` has no variation at `k = 1` and at every `k` from 25 through 30; at `k = 0`, `C` is undefined and B1 accepts the candidate. At `k = 2`, two levels are possible (`C = 1/2` or `C = 1`), so variation is possible but sparse. Before any held-out score is accessed, apply this gate using diagnostic footprints only: within every pre-declared task/base-algorithm/`k` cell that is to contribute to H3, `C` must take at least two distinct levels, and each of at least two levels must be represented by at least `m_min` distinct solver-side dependence groups. Count a group at most once per level; candidates and replicas within one group do not increase the independent-group count. Fix `m_min`, the eligible cells, and the rule for combining cells in the protocol before measuring footprints. Justify `m_min` from an explicit precision or decision rationale, not from the resulting held-out association. A footprint-only feasibility pilot can determine whether the support exists without opening held-out scores, but by itself cannot estimate outcome variance or establish adequate power. If no defensible group minimum and precision plan can be justified, stop at feasibility rather than proceed to a confirmatory test. More generally, low and high `k` strata may have only a few feasible levels. A larger sample cannot create variation where the instrument's feasible support is a single value.

## 9. Identification requirements carried forward

These are lessons from the earlier work, not a design.

- The comparison must hold `k` and task/base-algorithm stratum fixed and use independent solver-side dependence groups. The archived v0.2 confirmatory table reports `C = 5/k` throughout and therefore has no within-`k` concentration variation. A separate natural-candidate inventory was reported as 90 eligible rows from ten base bodies, also without same-`k`, different-`C` support. These are different records and must not be conflated.
- The legacy six-family partition has already been exposed to observed failures in v0.2 and Gate 1, and this record does not prove the partition was frozen before those outcomes. Reuse is therefore a prospective replication on an outcome-exposed definition unless contemporaneous records establish an earlier freeze; a cleaner confirmatory test requires a task-semantics partition selected without access to prior failure profiles, with the changed operationalization declared explicitly.
- The primary target is explicitly conditional on B1 rejection (`k > 0`). Because B1 uses only `k`, it does not select among family profiles within a fixed-`k` stratum; however, the claim does not apply to accepted candidates or to another rejection rule.
- The v0.2 instrument used five probes per family that varied one underlying property; its all-or-none family counts are at least partly instrument-induced. They do not establish that naturally generated solvers have family-aligned failure patterns.
- Independence and leakage control must be defined separately for solver-side dependence groups and input-construction clusters. A difference in observed failure sets does not by itself prove independence.
- `C` has tracked a hidden variable in each earlier setting: algorithm type in the old Doctor project, failure count in v0.2, and family size and defect identity in the engineered Gate 1 work. Accordingly, task/base-algorithm composition is controlled by within-stratum comparisons, not by pooling and hoping the task effect averages out.

## 10. Literature status

The focused scan and its exploratory follow-up covered failure clustering and root-cause indexing, held-out repair evaluation, out-of-distribution code evaluation, slice/worst-group evaluation, software reliability and capture-recapture, and automated grading/test-suite properties. The reading remains at abstract/snippet level for several sources; this is not a systematic review.

- **Direct result:** no directly matching study was identified in these limited searches that tests whether `max_j f_j` (equivalently `C` at fixed `k`) adds predictive ranking value for rejected solver candidates on held-out inputs. This is not evidence of novelty.
- **Adjacent evidence:** EvalPlus addresses test inadequacy; Hybiscus/GREClue address clustering failures to infer root causes; BATS studies similarity of failing tests for patch correctness; DEIm studies automated identification of underperforming data slices; Clegg et al. study how test-suite properties affect automated grading; capture-recapture work estimates fault counts/reliability from overlapping detections. These are different targets and do not directly validate H3.
- **Corrected descriptions:** Fault-Aware Neural Code Rankers predicts code correctness and execution information from code rather than using a candidate's own observed failure pattern. SimSCOOD studies OOD behavior of fine-tuned code models, not transfer of a candidate's diagnostic failure profile. Uncovering Weaknesses in Neural Code Generation is a thematic taxonomy, not a statistical test of concentration.
- **Limitation:** the scan has not read every relevant paper in full and has not established the absence of a direct precedent. No novelty or duplication claim is made. A systematic review is needed before such a claim.

## 11. What this note does not do

- It does not provide a design, a sample size, a model class, or any run.
- It does not claim that `C` has predictive value, or that it lacks it.
- It does not reopen the closed study.

## 12. Open items

- Define and justify the natural solver-generation mechanism and target population.
- Establish whether the existing six-family partition was frozen before the historical v0.2/Gate 1 outcomes. Unless documented evidence establishes that, treat it as outcome-exposed. Decide between a prospective replication on the fixed legacy definition and a new, task-semantics partition selected blind to prior failure profiles; do not describe the legacy reuse as a clean first confirmatory partition.
- Freeze the diagnostic probe-to-family partition, labels, counts, and weights before the new candidate sample is generated.
- Specify the bounded held-out input domain and its construction independently of diagnostic family labels; freeze its score orientation and any evaluation strata/weights.
- Set the B1-rejected target population (`k > 0`), task/base-algorithm strata, eligible `k` cells, group-pair estimand and tie rule, cell weights, minimum practically meaningful ranking improvement, `m_min` support threshold, bootstrap-invalid-replicate limit, and group/input-cluster uncertainty procedure before any held-out score is inspected. A footprint-only pilot can test support but cannot by itself justify power or precision.
- Establish sufficient fixed-`k`, varying-`C` comparisons across independent solver-side dependence groups. For `p = 5` and six families, `k = 1` and `k = 25..30` have no variation in `C`; `k = 2` has only two feasible levels.
- Resolve input-cluster separation and the limits of behavioral-alias checks.
- Record the eventual protocol freeze by annotated Git tag and full commit SHA, plus UTC timestamp and hashes of the partition, candidate-generation/sampling frame, diagnostic/evaluation input manifests, score rules, and analysis code. This is a future protocol requirement, not a freeze of the present research note.
- Complete a systematic literature review before making any novelty claim.

No item in this note authorizes data collection, generation, execution, or an experiment.
