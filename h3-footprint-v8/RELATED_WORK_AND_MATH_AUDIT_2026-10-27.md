# Related-work and concentration-metric audit

**Date:** 2026-10-27  
**Branch:** `review/h3-footprint-v8-postfreeze-audit-2026-10-27`  
**Status:** Research note only. The V1–V8 frozen artifacts and their tags are unchanged. This is not a new experiment protocol and authorizes no candidate execution.

## Executive result

The strongest current justification for the footprint pilot is a feasibility question, not a predictive claim: can the declared source population yield enough independent solver groups with the same total number of failed probes but different distributions of those failures across the six predefined probe families?

The literature offers relevant methods for studying algorithmic diversity and failure patterns, but does not validate this particular concentration statistic as a predictor of solver correctness. The old v0.2 result does not settle that question, because on its realized support the concentration measure was redundant with total failure count.

## 1. Exact mathematics of C

For family (j in \{1,\ldots,6\}), let (f_j\in\{0,1,2,3,4,5\}) be the number of failed probes among that family's five probes. Let

```text
k = sum_j f_j
C = max_j(f_j) / k, for k > 0.
```

Then:

- (C=5/k) **if and only if** at least one family is saturated, meaning (max_j f_j=5).
- This is not a universal algebraic identity. For example, a failure vector ((2,2,0,0,0,0)) gives (k=4), (C=2/4=0.5), not (5/4).
- For (k\geq25), a saturated family is mathematically forced: if all six families had at most four failures, the total could be at most (6\times4=24). Thus at those k values, (C=5/k) is forced by the instrument's capacity.
- At fixed (k\leq24), different family-level failure vectors can yield different values of (C). That same-k variation is the essential support requirement for a model to distinguish concentration from the total failure count.

Here (C) is most neutrally described as the **largest family share of all failures** (or maximum-category share). It is related to the broader idea of categorical concentration, but should not be described as a universally standardized software-reliability metric with an established predictive interpretation. Alternative dispersion summaries, such as Shannon entropy or the Herfindahl index, answer different questions and would be different predictors requiring a separately frozen design. Replacing (C) during the current pilot would change the protocol.

## 2. What the old v0.2 record does and does not establish

The corrected [v0.2 findings ledger](https://github.com/foued2/failure-concentration-study/blob/master/v02/FINDINGS_LEDGER_2026-10-19.md) reports a direct read-only recount of 1,200 solver-instance rows: all 1,200 had at least one family with all five probes failing, so (C=5/k) exactly on that realized support (maximum absolute residual zero). Its realized k values were 5, 10, 20 and 25.

The ledger explicitly scopes that statement to the observed failure patterns. For k=25, saturation is forced by the instrument; for k=5, 10 and 20, saturation was an empirical feature of this generated solver pack, not an algebraic requirement.

The [v0.2 terminal report](https://github.com/foued2/failure-concentration-study/blob/master/v02/REPORT_V02.md) classified the frozen predictive comparison NEGATIVE under its prespecified threshold. The [interpretability addendum C](https://github.com/foued2/failure-concentration-study/blob/master/v02/INTERPRETABILITY_AUDIT_2026-10-14_C.md) says the predictor comparison was unanswerable about independent concentration value because C was aliased with k on the observed support. These records support a narrow conclusion: **that v0.2 pack and instrument could not identify incremental predictive value from C beyond k.** They do not prove that C can never be predictive when the same k has different C values, nor do they establish that concentration is useful in that setting.

There is also a unit-of-analysis warning in the ledger: the 120 solver files were 40 distinct base bodies each emitted in three byte-identical replicas; only 10 base bodies were eligible under the v0.2 criterion. Treating replicated body-instance outcomes as independent solver submissions would overstate solver-population evidence. The current footprint gate's use of provenance groups is important for that reason.

## 3. Relevant literature

These references inform how to frame and test the question; none independently validates (C).

| Reference | Useful finding | Relevance and limit for this project |
|---|---|---|
| Jangra & Muresan, [*DivAlgo: A systematic evaluation of algorithmic diversity for code generation models*](https://arxiv.org/html/2610.19157) (13 Oct 2026, preprint) | Across 24 code-generation models, uncontrolled generated solutions captured about 31% of human algorithmic diversity in the benchmark; the best studied diversity-oriented strategy reached about 70.5%. The paper measures algorithmic overlap across generated and human solutions. | Strong reason not to assume repeated generations will yield enough algorithm-family diversity. It is about algorithmic diversity over a broad programming benchmark, not SSSP probe failures, within-k variation, or the predictive value of (C). |
| Lee et al., [*How Diversely Can Language Models Solve Problems?*](https://arxiv.org/html/2503.00691v2) (2025) | Studies generated-code diversity against human-written solutions and examines model, temperature, instruction-tuning, and problem-complexity effects. | Supports recording model and prompt provenance and not treating pooled generations as automatically diverse. Does not justify substituting different models into the frozen frame. |
| Schneckenburger & Mayer, [*Towards the determination of typical failure patterns*](https://dlnext.acm.org/doi/10.1145/1295074.1295091) (2007) | Notes that the assumption that failure-inducing inputs are spatially clustered had not been empirically quantified; proposes metrics for the location and shape of failure regions. | Methodological precedent for treating concentration/cluster claims as something to measure rather than assume. Their object is geometry of failure-inducing input regions, not a solver's distribution of failed probe families. |
| Guo, Qiu & Siy, [*Locating Fault-Inducing Patterns from Structural Inputs*](https://dl.acm.org/doi/pdf/10.1145/2554850.2554938) | Uses grammar-generated structured inputs and structural features to discover common fine-grained patterns associated with failures. | Relevant to engineering meaningful, well-defined probe families and auditing their coverage. It is a fault-localization technique; it does not establish a universal concentration predictor. |
| DiGiuseppe & Jones, [*Software Behavior and Failure Clustering: An Empirical Study of Fault Causality*](https://doi.org/10.1109/icst.2012.99) (2012) | Analyses more than four billion test outputs and execution profiles across more than 9,000 program versions; finds that common simplifying assumptions in failure clustering can be unsuitable, particularly with multiple faults and imperfect profile/output correlation. | Warns against equating concentration with one common underlying cause. A high maximum-family share is a descriptive pattern, not proof that one mechanism caused the failures. |
| Song et al., [*A comprehensive empirical investigation on failure clustering in parallel debugging*](https://doi.org/10.1016/j.jss.2022.111452) (2022) | Controlled studies across 1,060 faulty versions, including simulated and real faults, report that clustering effectiveness changes with fault count and fault type. | Reinforces that failure distribution depends on the studied population and fault structure; no universal benefit follows from concentration alone. |
| Ploski et al., [*Research issues in software fault categorization*](https://doi.org/10.1145/1317471.1317478) (2007) | Surveys quantitative fault-category distributions and discusses whether such distributions transfer to fault-injection studies. | Relevant caution: the frequency distribution over declared categories depends on the classification scheme and whether the studied population matches the intended population. |

## 4. Implications for the current footprint gate

1. **The immediate outcome is feasibility, not efficacy.** PASS means the fixed generation frame and this instrument furnish the prespecified number of supported same-k/different-C cells with independent provenance groups. It is not evidence that C improves predictive performance.
2. **Do not confuse a code-algorithm label with a failure mechanism.** The conservative AST classifier assigns structural algorithm labels; it cannot establish why a particular family fails. Reports should not overstate these labels as causal findings.
3. **Preserve provenance and clustering.** Multiple bodies from one generation batch are not independent merely because their text differs. Keep the provenance-group accounting and report model/prompt/batch, exact duplicates, invalid bodies, and “other” labels.
4. **Do not prompt toward the desired result mid-run.** The question is about natural variation under the frozen schedule. Explicitly instructing the model to use a chosen algorithm or making outcome-guided prompt changes would study a different population and could manufacture apparent support.
5. **Probe-family design is a separate validity layer.** Six fixed family names do not guarantee that all families represent distinct mechanisms, or that their five probes are comparable. The current bounded gate can check variation under the instrument; it cannot, by itself, validate the construct or establish generalization to unseen probe families.
6. **A failure verdict must remain scoped.** If the frame does not supply enough same-k, different-C groups, the result is “this frame/instrument failed the predeclared feasibility gate,” not “concentration has no value.”
7. **Generation access must be diagnosed, not worked around silently.** The official OpenCode catalog still lists the three model IDs named in the frozen V8 schedule, but catalog presence does not prove account-level usability. Record the installed CLI version, whether those IDs appear in its actual model selector, the free-model environment setting, and the exact error/retry state. Keep the frozen frame unchanged unless a new protocol is explicitly versioned.

## 5. Execution-security status

The separate [post-freeze V8 audit](POSTFREEZE_AUDIT_2026-10-27.md) records an evaluator trust-boundary flaw and open read-access checks. A further concrete consequence is worth emphasizing: V8's read-only host mapping makes the mapped harness files readable, and read-only does not mean secret. Since candidate code shares the worker interpreter and can traverse Python module state, staged expected values and probe definitions must be treated as potentially exposed to candidate code. The next revision must not merely add another static import rule. It must keep confidential evaluator state outside the candidate-visible file/process boundary and define results as externally observed solver outputs, with the evaluator comparing against expected answers in a trusted process.

No candidate execution is authorized until the trust boundary and read-access issue are resolved and the actual Windows Sandbox isolation probe passes. This research note does not change the frozen protocol, model schedule, thresholds, or scientific status.
