# Three-world concentration model: frozen simulation design

**Status:** Frozen design specification, written before the simulation script or any scenario run. This document fixes the generative worlds, estimands, trial plan, and interpretation rules. The seed is 20261024.

**Scope:** Offline synthetic-data simulation only. No real or model-generated solvers, model/API calls, changes to diagnostic/evaluation banks, or reopening of the closed Gate 1 study. Simulation results will show implications of declared assumptions only.

## 1. Research question

Does diagnostic failure concentration \(C\) improve held-out prediction of evaluation score \(S\), beyond total diagnostic failures \(k\) and prespecified family/carrier information? How does the answer depend on the assumed mapping from diagnostic defect reach to evaluation defect reach?

The three worlds are deliberately contrasting data-generating assumptions, not claims about real solvers:

- **W1: concentration is informative under the specified mechanism.**
- **W2: family/carrier identity explains the score pattern; \(C\) adds no value after family adjustment.**
- **W3: evaluation damage is generated independently of diagnostic concentration, conditional on declared baseline variables; \(C\) adds no population predictive value.**

A W1 positive result is a wiring check, not evidence for the real-world hypothesis. W2 and W3 are negative-control worlds. The mixture sweep probes how conclusions change between the W1 and W2 assumptions.

## 2. Fixed design quantities and definitions

There are six diagnostic families with five probes each. Evaluation-family sizes are

\[
N=(9,9,23,23,31,3),\qquad \sum_j N_j=98.
\]

For each synthetic case, generate diagnostic failure counts \(F=(f_1,\ldots,f_6)\), where \(f_j\in\{0,\ldots,5\}\), total \(k=\sum_j f_j\), and

\[
C=\begin{cases}\max_j f_j/k,& k>0,\\ \text{undefined},& k=0.\end{cases}
\]

Cases with \(k=0\) remain in the raw dataset and are summarized separately. They are excluded from models that use \(C\), and the number excluded must be reported by world and trial. No numeric value is imputed for undefined \(C\).

Evaluation failures are \(E=(e_1,\ldots,e_6)\), with \(e_j\in\{0,\ldots,N_j\}\). Scores are

\[
S_D=1-\frac{\sum_j e_j}{98},
\qquad
S_F=1-\frac{1}{6}\sum_{j=1}^6\frac{e_j}{N_j}.
\]

\(S_D\) is primary (domain-weighted); \(S_F\) is secondary (equal-family). Do not alter the score definitions after seeing results.

A **carrier family** is a generative latent label for the home family of a defect. It is available to the analyst only in models explicitly labelled family-adjusted. This is an intentionally strong diagnostic of confounding, not a claim that carrier family is always observable in natural solver data.

## 3. Generative construction

Each trial contains 5,000 synthetic cases. Each case has one to four latent defects, with defect count sampled uniformly from \(\{1,2,3,4\}\). For each defect, sample a home family uniformly from the six families. All randomness uses the frozen pseudorandom seed 20261024, with a deterministic, documented per-trial seed derivation (base seed plus trial index). Use only Python's standard library.

For family \(j\), combine independent defect reaches using a union probability:

\[
q^D_j=1-\prod_m(1-d_{mj}),\qquad
q^E_j=1-\prod_m(1-e_{mj}).
\]

Then draw \(f_j\sim\mathrm{Binomial}(5,q^D_j)\) and \(e_j\sim\mathrm{Binomial}(N_j,q^E_j)\), independently conditional on the defect reaches. This creates a deliberately simplified stochastic measurement model. It does not preserve input-level dependence or imply that real solver failures are independent Bernoulli trials. Those are limitations to state in the result.

### World W1: concentration-informative leakage

Each defect has a home family \(h\). Its diagnostic reach is \(d_h=0.8\), and \(d_j=0.05\) for \(j\ne h\). Evaluation reach is high in its home family and small elsewhere, but both the number of defects and their spillover determine damage: for each defect set \(e_h=0.35\) and \(e_j=0.03\) for \(j\ne h\). Since additional defects tend to spread diagnostic failures and expand evaluation damage, \(C\) can proxy the number/overlap of defects and may add predictive value at fixed \(k\).

These values are fixed assumptions, not fitted to any existing controls. Because W1's construction is intended to make \(C\) informative, a positive result is only a code-path check. If W1 does not show the expected direction under the frozen diagnostic checks, investigate implementation and report the failure; do not silently tune the parameters.

### World W2: family identity, not concentration

Each case has one home family \(h\). Diagnostic reach is \(d_h=1\), \(d_j=0\) otherwise. Evaluation reach is \(e_h=1\), \(e_j=0\) otherwise. Thus the score is determined by home-family size, while \(C=1\) for all cases with \(k>0\). This is a deliberately clear family-confounding control: it does not supply within-world variation in \(C\), so the concentration effect is **unidentifiable** in W2, rather than empirically shown to be zero by a coefficient test.

Because this world cannot estimate a concentration contrast at fixed \(k\), do not use W2 alone to validate the family-adjusted estimator. It tests whether the pipeline correctly flags absent overlap.

### World W3: concentration-independent evaluation damage

Generate the diagnostic reaches as in W1. Generate evaluation reaches independently of the diagnostic reach pattern and independently of the resulting \(C\): each defect's evaluation reach is \(e_j=0.15\) for every family, regardless of home family. Thus, conditional on defect count and the model's declared baseline, evaluation damage does not depend on diagnostic concentration or carrier family. \(C\) may still correlate with defect count through the diagnostic mechanism, so the baseline includes the number of latent defects **only as an oracle diagnostic check**, never as an observable predictor in the primary comparison. Report both:
- the primary practical comparison using \(k\) and carrier family, where any residual relationship caused by imperfect proxying is measured; and
- the oracle comparison adding latent defect count, which should show no incremental population value for \(C\) under W3.

This distinction prevents a false assertion that W3 has no \(C\) association when \(C\) indirectly proxies an omitted latent count. If the primary model finds gain in W3 but the oracle model does not, interpret it as proxy information about latent defect count, not a direct concentration mechanism.

## 4. W1/W2 mixture sweep

Run mixture weights \(\lambda\in\{0,0.25,0.5,0.75,1\}\). At each \(\lambda\), draw the world label per case: W1 with probability \(\lambda\), W2 with probability \(1-\lambda\), using the same underlying trial procedure and reporting results separately by mixture. The mixture is a synthetic stress test, not an estimated prevalence of mechanisms in real solvers.

Report whether \(C\)'s incremental predictive gain shrinks, changes sign, or becomes unidentified as W2 cases dominate. Because W2 has no within-world concentration variation, report the fraction of cases and fixed-\(k\) strata with usable overlap at each mixture. Do not interpret a smooth curve as a universal threshold.

## 5. Models and estimands

Use five-fold cross-validation, with cases randomly assigned to folds using the fixed seed. Since these are synthetic independent cases, no duplicate solver replicas are intentionally introduced. If implementation creates repeated latent templates, cluster by template and keep each cluster in one fold.

Compare these feature sets:

- **M0:** \(k\) only.
- **M0+fam:** \(k\) plus carrier-family indicators.
- **M1:** \(k\) plus \(C\).
- **M1+fam:** \(k\), \(C\), and carrier-family indicators.
- **MF:** the full vector \(F\), with the same family indicators as M1+fam in the adjusted comparison.
- **Oracle W3 check:** M1+fam plus latent defect count, used only to diagnose the W3 mechanism.

For numerical stability and fair comparisons, use a prespecified ordinary least-squares model with intercept; use the same folds for all compared models and do not tune features per trial. Do not add nonlinear terms after inspecting results. If a fold has rank deficiency, record it and use a prespecified Moore-Penrose least-squares solution consistently, while flagging that parameter interpretation is unavailable.

For each held-out case, calculate squared error. Average over cases to obtain cross-validated MSE \(L(M)\). The primary incremental gain is

\[
\Delta_{\mathrm{pred}}=L(M0+\mathrm{fam})-L(M1+\mathrm{fam}).
\]

Positive values mean adding \(C\) improved prediction. Also report \(L(M1+\mathrm{fam})-L(MF+\mathrm{fam})\); positive values mean the full vector improved over \(C\) under this finite-sample modelling procedure.

For each world and score, summarize the mean \(\Delta_{\mathrm{pred}}\) across 500 independent trials and a 95% trial-level interval (2.5th and 97.5th percentiles of the 500 trial estimates). This interval describes variation across the specified simulation trials, not a confidence interval about real solvers. Report the fraction of trials with positive gain as well. Report W3's oracle comparison separately.

## 6. Frozen run plan and output

- Trials per world: 500.
- Cases per trial: 5,000.
- Base seed: 20261024; trial seed = base seed + trial index, with index starting at 0.
- Worlds: W1, W2, W3, plus the five W1/W2 mixture weights.
- Scores: primary domain-weighted, secondary equal-family.
- Save per-trial outputs as JSON, including each world/mixture, trial seed, model losses, \(\Delta_{\mathrm{pred}}\), fold-rank warnings, \(k=0\) counts, fixed-\(k\) overlap summaries, and the frozen scenario parameters.
- Save compact failure-set records in JSON: each case's diagnostic vector \(F\), evaluation vector \(E\), \(k\), defined/undefined \(C\), carrier-family label, defect count, and world label. To keep the file practical, use a documented JSON Lines format compressed with gzip; include a checksum and record count. These are synthetic records only.
- The report must include a table per world and mixture, both scores, all criteria outcomes, overlap and rank diagnostics, and every failed check. No failed check may be omitted from the summary.

## 7. Frozen interpretation and failure criteria

### A. Overlap / identifiability

Do **not** define identifiability as “carrier family explains more than 90% of the variance in \(C\).” That threshold is not a general identification criterion. Instead, report these observable design diagnostics:

1. For each \(k>0\), number of distinct \(C\) values and number of independent cases at each value.
2. Whether the design matrix for the adjusted model has full column rank.
3. Whether the residualized \(C\) (after projecting on \(k\) and carrier-family indicators) has nonzero variance.
4. The number of usable fixed-\(k\), different-\(C\) comparisons within carrier family.

If no such comparison exists, or residualized \(C\) has zero variance, label the family-adjusted concentration effect **unidentifiable**. Small but nonzero variation is weak overlap, not automatically adequate identification; report it quantitatively.

### B. Expected outcome checks

- **W1 wiring check:** expected direction is positive under the declared W1 mechanism. If it fails, mark the simulation check **FAILED** and investigate code/model mismatch. Do not change leakage parameters after seeing the result without a new versioned design and rationale.
- **W2 overlap check:** must be flagged unidentifiable for concentration because \(C=1\) whenever \(k>0\). A reported estimable C effect in W2 is a pipeline failure.
- **W3 oracle check:** after adding latent defect count, \(C\) should have no population predictive contribution by construction. Sampling estimates may be nonzero; report their trial interval and positive fraction. If the interval systematically excludes zero, investigate implementation and leakage.
- **W3 primary check:** do not require the primary \(k\)+family comparison to be exactly zero, because \(k\) may not fully capture latent defect count and \(C\) may proxy that omitted count. Any primary gain must be interpreted as indirect proxy information unless the oracle comparison contradicts the declared mechanism.

### C. “C survives” criterion for this simulation

A world is labelled **simulation-supportive under its assumptions** only if:
1. the family-adjusted \(\Delta_{\mathrm{pred}}\) is positive and the 95% trial-level interval excludes zero;
2. the expected sign is positive for both domain-weighted and equal-family scores;
3. usable fixed-\(k\), different-\(C\) overlap exists after family adjustment; and
4. the direction is not reversed by the predeclared partition sensitivity analysis.

This is a statement about the simulation world only. It is not evidence that real solvers follow the world.

### D. “F beats C” criterion

The full vector is labelled better for the specified finite-sample predictor only if the trial-level 95% interval for \(L(M1+\mathrm{fam})-L(MF+\mathrm{fam})\) lies above zero on the same held-out folds. This is an empirical predictive result for the chosen estimator/sample size, not an information-theoretic result. The full vector cannot contain less information than its deterministic summary in principle.

### E. Partition sensitivity

A valid partition sensitivity test must recompute the diagnostic vector and \(C\) from the same input-level failure outcomes under an alternative **diagnostic** partition. Repartitioning only evaluation families cannot change diagnostic \(C\) and is not a test of \(C\)'s partition dependence.

The current generative specification creates family-level Bernoulli reach rather than a fixed set of input-level outcomes that can be reclassified under arbitrary partitions. Therefore, before claiming partition robustness, the implementation must generate and retain input-level diagnostic outcomes, define at least one alternative partition of the 30 diagnostic inputs, recompute \(F\), \(k\), and \(C\) under that partition, and apply the same predictive comparison. If this input-level representation and alternate partition cannot be specified without inventing an unsupported taxonomy, report partition sensitivity as **NOT TESTED**, not passed.

### F. Limits

The simulation does not validate the assumed defect types, reach probabilities, or relation between diagnostic and evaluation inputs. A positive W1 result is expected because the world is constructed to make concentration informative. A negative W2 result reflects missing overlap. W3 separates direct concentration effects from concentration acting as a proxy for an omitted latent property. None of these establishes what real solvers do.

## 8. Change control

This design is frozen before the simulation script is created or any world is run. If an implementation defect requires a change, document the bug, preserve the original design and outputs, version the correction, and report both the original failed check and corrected result. Do not silently revise parameters or criteria to obtain expected outcomes.


## 9. Pre-run clarification amendment (committed before implementation)

This amendment resolves implementation ambiguities found during review. It is part of the frozen design and must be read together with Sections 1-8.

1. **Carrier-family coding:** every case has one to four defects in W1, so it does not have one uniquely defined carrier family. Define the carrier family used in the primary family-adjusted models as the home family of the first sampled defect (the anchor family). This label is generated before diagnostic/evaluation outcomes. In W2 it is also the sole defect's home family. Report the number of defects and their full home-family counts in the synthetic records, but do not add those counts to the primary family-adjusted model. W3's oracle check adds defect count, as already specified.
2. **Input-level diagnostic outcomes and alternate partition:** the implementation must generate a Bernoulli outcome for each of the 30 diagnostic probes, using each probe's original family's combined reach \(q^D_j\), and then aggregate those outcomes into \(F\). Retain the 30 binary outcomes. The alternate diagnostic partition merges original families (1,2), (3,4), and (5,6), yielding three groups of ten probes. Recompute \(F\), \(k\), and \(C\) under this partition from the retained outcomes. Keep the evaluation score definitions fixed at their original six-family/domain definitions, so this sensitivity changes the diagnostic summary, not the target outcome.
3. **Mixture model labels:** W1/W2 mixture cases use the W1 or W2 generative recipe, and the recorded world label is retained. The primary mixture analysis fits the declared models to the combined mixture. Report the fraction of cases from each world, overlap diagnostics by world and overall, and both the pooled result and within-world descriptive results. Do not imply that a mixture estimate identifies real-world prevalence.
4. **Meaning of the interval:** the 2.5th and 97.5th percentiles across 500 independently seeded trial-level estimates describe Monte Carlo design variability under the fixed generator. They are not conventional confidence intervals for a single population parameter. Label them “central 95% simulation-trial interval” in all outputs.
5. **W1 sign check:** the mechanism makes higher defect count tend to broaden diagnostic failures and increase evaluation damage, so the hypothesized direction is that higher \(C\) predicts a higher score. This is an expectation, not a mathematical guarantee under the finite stochastic design. If the interval does not support the positive direction, report the frozen W1 criterion as failed; do not tune the parameters to force it.
6. **Undefined \(C\) and model fitting:** use one common eligible subset with \(k>0\) for every model comparison involving \(C\), and score all compared models on exactly the same held-out eligible cases. Separately report full-cohort baseline performance, but do not compare MSEs calculated on different populations.
7. **No evaluation-family-only partition claim:** the only planned partition sensitivity is the alternative diagnostic partition in item 2. Repartitioning evaluation labels alone is not a test of concentration's partition sensitivity.

This clarification was committed before creation of the simulation script or any scenario run. It does not change the trial count, seed, score definitions, model families, or interpretation thresholds.


## 10. Final estimand clarification (before implementation)

The primary claim is explicitly **conditional on the same total failure count**. Therefore, represent \(k\) as a categorical fixed effect in M0, M0+fam, M1, and M1+fam, not as one numeric linear term. This allows the baseline score relationship to differ at each observed \(k\), and makes the incremental \(C\) comparison consistent with the fixed-\(k\) claim. Report stratum-specific contrasts as descriptive overlap checks.

For the full-vector model \(MF\), use categorical \(k\) plus five of the six family counts (for example \(f_1,\ldots,f_5\)); \(f_6=k-\sum_{j=1}^5 f_j\) is then recovered exactly. This represents the full vector without adding an exactly redundant linear column. Include the same anchor-family indicators and use the same eligible cases and held-out folds as M1+fam. The oracle W3 model uses categorical \(k\), anchor-family indicators, \(C\), and latent defect count.

This is a clarification of the estimator, not a post-result change. It is committed before the simulation script exists and before any world is run.
