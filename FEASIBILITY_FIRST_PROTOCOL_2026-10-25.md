# Feasibility-first protocol design: concentration beyond `k` and family

**Date:** 2026-10-25
**Status:** Authorized document-only protocol design. One bounded review round; corrected draft.
**Decision boundary:** No solver generation, model/API call, execution, simulation, bank change, frozen-result change, or experiment is authorized. Step 2 remains unauthorized.
**Scope:** Design a future study that could test whether adding `C = max(F)/k` improves held-out prediction beyond `k` and predeclared controls, without assuming that such a design is feasible.

This document is the corrected draft for the single authorized review round. The unchanged review snapshot is `2aa6faf`. This document is not a frozen protocol, a study result, or an authorization to generate anything.

---

## 1. Purpose and decision

The existing record does not establish whether concentration adds predictive value, and it does not establish that it lacks such value. The immediate question is:

> Can a credible study be specified, on paper, in which independent solver bodies have the same `k` but different family-count vectors and different `C`, while the competing explanations of family and defect identity remain visible?

The protocol is feasibility-first. It must decide whether that construction can be specified before any resources are spent producing or scoring solvers.

There are three possible outcomes of this review round:

1. **Accept the protocol design.** A future empirical construction audit and confirmatory study may then be proposed under separate authorization.
2. **Reject the constructability argument.** Record the study as infeasible under this design and close with a documented limitation.
3. **Request one bounded clarification.** The review round is single; a clarification is not a mandate to redesign the study.

No outcome authorizes execution.

---

## 2. Fixed question, target population, and estimand

### 2.1 Primary question

For solver bodies in a declared population, does adding `C` to a prediction procedure that already contains `k` and the predeclared controls improve prediction of a held-out evaluation score `S`?

This is a predictive question. It is not a causal question about changing `C`.

### 2.2 Definitions

For six diagnostic families,

\[
F=(f_1,\ldots,f_6),\qquad
k=\sum_{j=1}^{6}f_j,\qquad
C=\frac{\max_j f_j}{k}\quad(k>0).
\]

`C` is undefined at `k=0`. It is never imputed as zero.

The primary `k` levels are `k=5` and `k=10`. Within each level, the primary `C` contrast is:

| `k` | Low-`C` target | High-`C` target |
| ---: | ---: | ---: |
| 5 | 0.6 | 1.0 |
| 10 | 0.3 | 0.5 |

The high and low levels are fixed in advance. Other `k` or `C` levels are exploratory only and cannot rescue the primary comparison. At `k=10`, `C=1.0` is mathematically impossible because each family has only five probes; the protocol does not pretend otherwise.

### 2.3 Target population and score

The target population is **solver bodies from the declared task, with the same six diagnostic-family definitions and known mechanism families**, evaluated on a family-balanced held-out bank.

The primary score is:

\[
S_F=1-\frac{1}{6}\sum_{j=1}^{6}\frac{e_j}{N_j},
\]

where `e_j` is the number of held-out evaluation failures in family `j` and `N_j` is the number of held-out inputs in that family. This weights the six families equally.

The target is therefore **average correctness across the six structural families**, not a uniformly sampled input from the raw domain. This choice is deliberate: the raw-domain score

\[
S_D=1-\frac{\sum_j e_j}{\sum_j N_j}
\]

lets the largest family dominate merely because it has more inputs. `S_D` may be reported as a secondary score, but it cannot rescue a failed primary `S_F` comparison. The protocol does not claim that a family-balanced result transfers to a deployment distribution with different family frequencies.

The held-out score and the family weights must be frozen before any solver is generated. The protocol must not switch to a more favorable weighting after seeing results.

### 2.4 Primary estimand

Let `S0_hat` and `S1_hat` be predictions from two frozen procedures:

- baseline: `k` plus predeclared controls `Z`;
- augmented: `k`, `Z`, and `C`, including a prespecified `k`-by-`C` interaction.

Let

\[
\Delta_{\mathrm{pred}}
=\mathbb{E}\left[(S-\widehat S_0)^2-(S-\widehat S_1)^2\right],
\]

evaluated on held-out solver bodies. Positive `Delta_pred` means the augmented procedure predicts better.

`Z` may include task, generator protocol, carrier/anchor family, and mechanism-family indicators. The following are **not** allowed in `Z`:

- the full failure vector `F`;
- any family count vector that determines `F`;
- any transformation that determines `C` from the controls;
- any variable measured after the diagnostic outcomes that encodes the concentration contrast.

The full-vector comparison in Section 6 is a separate, prespecified check. It is not a baseline control.

### 2.5 What the estimand is not

It is not:

- the coefficient on `C` in a model fitted and evaluated on the same solvers;
- a test of whether `C` causes correctness;
- a claim that `C` contains more information than `F`;
- a comparison of high-`C` and low-`C` means without adjustment or common support;
- a test that can be rescued by changing the definition of `C`, the score, or the partition after seeing outcomes.

---

## 3. Generalization target and cross-validation

### 3.1 Primary target

The primary target is **new solver bodies from the same task, same six diagnostic-family definitions, and same known mechanism families**, but new mechanism instances and new combinations of those mechanisms.

This is not a claim about generalization to entirely new families. Holding out entire families asks a different question: whether the fitted relationship transfers to a family never seen in training. That question is exploratory here.

### 3.2 Independent cluster

An **independent mechanism cluster** is a distinct mutation site and trigger condition with a distinct full-domain failure set.

- Variants that differ only by a constant, name, or equivalent predicate are one cluster.
- If two candidates have the same full-domain failure set, they are aliases and are collapsed.
- Replicas of one body are one cluster.
- Matched or dependent observations, including the low/high pair for one mechanism, stay in the same fold.

The cluster definition must be frozen before any outcome is examined. A cluster is not independent merely because its source text or filename differs.

### 3.3 Grouping rule

The primary cross-validation is grouped by **independent mechanism cluster**, not by family.

Folds are stratified so that every training fold and every held-out fold contains both primary `C` levels at each primary `k` level. If that stratification cannot be achieved, the design is infeasible.

Family identity remains a control. It is not a grouping factor in the primary analysis. A family-held-out analysis may be reported as exploratory, but it cannot replace or rescue the primary result.

### 3.4 Why this rule

Grouping by family would test generalization to new families. Grouping by mechanism cluster tests generalization to new defects within known families, which matches the stated target. The protocol must not silently substitute one target for the other.

---

## 4. Constructability gate

### 4.1 Gate A: paper construction

Gate A is satisfied only if the protocol can exhibit a concrete worked construction with all of the following:

1. at least two solver bodies at the same `k>0` with different family-count vectors and therefore different `C`;
2. a defensible account that the defects are distinct mechanisms, not aliases;
3. at least two `k` levels, each with at least two `C` levels;
4. at least two mechanism families, with at least one family represented at both `C` levels within each `k`;
5. a design that can meet the minimum support and precision rules in Sections 5 and 7.

The worked construction below is a **plausibility argument**. It is not empirical evidence that the mechanisms are independent or that the target profiles occur.

### 4.2 Worked construction: arithmetic expression evaluator

Task: evaluate integer arithmetic expressions with `+`, `-`, `*`, parentheses, unary minus, multi-digit integers, and arbitrary whitespace. The reference implementation is deterministic and modular: lexer, parser with a precedence table and reduction policy, and evaluator.

Six diagnostic families, five probes each:

| Family | Diagnostic property |
| --- | --- |
| F1 | operator precedence |
| F2 | left associativity |
| F3 | parentheses |
| F4 | unary minus |
| F5 | multi-digit tokenization |
| F6 | whitespace |

Candidate solvers are controlled mutations of the reference implementation, not model-generated samples.

**`k=5` construction.**

| Mechanism | Code location | Intended profile `F` | `k` | `C` | Secondary families |
| --- | --- | --- | ---: | ---: | --- |
| `P1`: precedence-table mutation | parser precedence table | `(5,0,0,0,0,0)` | 5 | 1.0 | none |
| `R1`: reduction-order mutation | parser reduction policy | `(3,1,1,0,0,0)` | 5 | 0.6 | F2, F3 |
| `T1`: digit-run termination mutation | lexer token boundary | `(0,0,0,0,5,0)` | 5 | 1.0 | none |
| `T2`: whitespace-boundary mutation | lexer token boundary | `(0,0,1,0,3,1)` | 5 | 0.6 | F3, F6 |

`P1` and `R1` are distinct code sites and distinct mechanisms. Both have the same leading family (F1), so the carrier family is held fixed. They have the same `k=5` but different `C`. The `R1` contrast is explicitly "one family fails alone" versus "the same dominant family plus two secondary families fail"; the secondary families are F2 and F3.

`T1` and `T2` are different tokenizer mutations but share a mechanism family. The tokenizer family is the sole failing family in `T1` and remains the dominant family in `T2`; the two secondary families for `T2` are F3 and F6. This provides within-family `C` variation, which is necessary to separate `C` from mechanism family.

**`k=10` construction.**

| Mechanism | Code location | Intended profile `F` | `k` | `C` | Secondary families |
| --- | --- | --- | ---: | ---: | --- |
| `T3`: digit-run termination mutation | lexer token boundary | `(0,0,0,0,5,5)` | 10 | 0.5 | F6 |
| `T4`: whitespace-boundary mutation | lexer token boundary | `(0,0,2,2,3,3)` | 10 | 0.3 | F3, F4, F6 |

The tokenizer family is tied for dominant in both `k=10` profiles. The same mechanism family therefore supplies both primary `C` levels at both `k` levels. The exact family counts are **targets for a future construction audit**, not observed results. The audit must verify the counts, the full-domain failure sets, and the absence of aliases. If the mutations do not produce the target profiles, the design is infeasible; the profiles must not be adjusted after measurement.

### 4.3 Gate A result

**Conditional pass for the minimum construction argument.** The arithmetic, family-count, and code-location arguments are concrete and plausible. The full multi-`k`, multi-mechanism design is not established: the document specifies the required structure, but it does not prove that the independent clusters can be produced in the required numbers with the required profiles.

Gate A permits a future empirical construction audit, not a confirmatory study. The audit is a separate authorization and is not part of this document.

### 4.4 Gate B: empirical construction audit, not authorized

A future Gate B would build the frozen candidate mutations and verify:

- the intended diagnostic profiles at both `k` levels, including exact family counts;
- distinct full-domain failure sets for every claimed independent cluster;
- no aliases, replicas, or mechanism variants mislabeled as independent;
- common support for `C` within at least one mechanism family at each `k`;
- at least the minimum number of independent clusters per `k x C` cell;
- the secondary families for each mixed profile are fixed across all instances of that profile.

A failure at Gate B is recorded as **infeasible under this design**, not as evidence that `C` lacks predictive value.

### 4.5 Gate C: precision, not authorized

A future Gate C would use the observed between-cluster variance from the construction audit to check whether the design can distinguish zero gain from the practical threshold. If the required precision cannot be reached with the available number of independent clusters, the design is infeasible.

No power simulation, model fit, or outcome analysis is authorized here.

---

## 5. Design structure and minimum support

The primary design must contain:

- two fixed `k` strata (`5` and `10`);
- two primary `C` levels within each `k` (Table in Section 2.2);
- at least two mechanism families at each `k`;
- at least one mechanism family represented at both `C` levels within each `k`;
- at least **6 independent mechanism clusters per `k x C` cell**;
- at least **3 independent clusters per mechanism family within each `k x C` cell**;
- balanced secondary-family composition across the low/high `C` instances of a given mechanism family, or an explicit secondary-family control;
- a stratified grouped fold assignment that preserves both `C` levels at each `k` in every fold.

With two `k` levels and two `C` levels, the floor is **24 independent clusters** (2 x 2 x 6). This is a floor, not a convenience. The actual number must also satisfy the precision rule in Section 7; if 24 is insufficient, the design must increase the number or stop.

The worked example suggests how the cells could be populated. The exact task and mutation set must be frozen only after Gate B.

Replicas of the same body do not contribute independent support. Multiple names for the same full-domain predicate do not contribute independent support. More copies of a profile cannot create missing `C` variation.

---

## 6. Models, controls, and comparisons

### 6.1 Primary models

Use prespecified ordinary least squares with an intercept and categorical `k`, estimated on training folds and evaluated on held-out solver bodies.

- `M0`: categorical `k` + carrier/anchor family indicators + mechanism-family indicators.
- `M1`: `M0` + `C` + the prespecified categorical-`k` by `C` interaction.

The primary comparison is `Delta_pred = L(M0) - L(M1)` on the same held-out bodies and folds. Positive means the joint addition of `C` and its `k` interaction improved prediction.

The interaction is included because a single `C` coefficient would force one slope across `k=5` and `k=10`, where the attainable `C` ranges differ. If the interaction is not estimable in a fold, the design is infeasible for that fold.

No nonlinear terms, family interactions, or alternative `C` definitions are added after seeing results.

### 6.2 Full-vector check

The full-vector model `MF` uses categorical `k`, the same family and mechanism-family controls, and five of the six family counts. It is compared with `M1` on the same folds.

This check is required because `C` is a summary of `F`. A claim that `C` is a useful summary cannot be converted into a claim that it contains more information than `F`. If `MF` predicts better, that is the result.

### 6.3 Rank and support

Before fitting, check the design matrix for full column rank within every fold. If a fold is rank deficient and cannot be resolved by a prespecified, non-outcome-dependent rule, the design is infeasible for that fold. Do not report a coefficient or effect from a rank-deficient fit as identified.

### 6.4 `k=0`

Bodies with `k=0` are excluded from the primary analysis. Their count is reported. `C` is undefined for them and is never set to zero.

### 6.5 Exploratory analyses

Alternative `C` definitions, alternative partitions, family-held-out generalization, and nonlinear models may be listed as exploratory before the study. They cannot be used to rescue a failed primary comparison. Exploratory results are labelled as such.

---

## 7. Evidential standards

### 7.1 Loss and relative gain

The loss is squared prediction error on `S_F`. Let `L0` and `L1` be the mean squared errors of the baseline and augmented procedures on the same held-out bodies. The relative gain is

\[
R=\frac{L_0-L_1}{L_0}.
\]

The practical threshold is

\[
\Delta_{\min}=\max\left(0.05\,L_0,\;0.0005\right).
\]

The 5% relative value and the 0.0005 absolute floor are **policy choices**, written before data exist. The absolute floor prevents a near-zero `L0` from making the relative criterion arbitrarily small. If `L0` is so small that a 0.0005 MSE difference is not meaningful for the intended decision, the score is unsuitable and the design is infeasible; the protocol must not divide by a near-zero baseline to manufacture a favorable relative gain.

### 7.2 Uncertainty

The primary uncertainty procedure is a paired cluster bootstrap over independent mechanism clusters, stratified by `k x C x mechanism family`, with 10,000 resamples and a percentile 95% interval.

The cluster bootstrap is required because the independent unit is the mechanism cluster, not the individual solver body. Resampling solver bodies would treat aliases, replicas, and matched low/high pairs as independent and would understate uncertainty.

The entire fold construction, model fitting, and held-out scoring must be repeated inside every bootstrap replicate. The protocol does not bootstrap residuals from a single cross-validation run. Ordinary cross-validation intervals can undercover, and repeating only the scoring step is not sufficient.

Matched or dependent observations, including the low/high pair for one mechanism, remain in the same fold and are resampled together as a cluster.

### 7.3 Two thresholds

**Any positive gain.** The lower bound of the 95% interval for `Delta_pred` is above zero.

**Practically meaningful gain.** The lower bound of the 95% interval for `Delta_pred` is above `Delta_min`.

A result can satisfy the first standard without satisfying the second. That outcome is reported as a statistically detectable but not practically meaningful gain, not as support for the stronger claim.

### 7.4 Precision requirement

The design is adequate only if, under the Gate C variance estimate, the expected 95% interval half-width for each within-`k` contrast is at most `0.5 * Delta_min`. Equivalently, the interval must be narrow enough that a planning effect at `Delta_min` would be distinguishable from zero with the prespecified procedure.

If the required half-width cannot be achieved with the available independent clusters, the design is infeasible. The protocol must not relax the half-width after seeing results.

### 7.5 Interpretation

If the interval is too wide to distinguish zero from `Delta_min`, the result is **inconclusive**, not negative. If the interval excludes `Delta_min` on the low side but lies above zero, the result supports a positive but not practically meaningful gain. If the interval lies entirely below `Delta_min`, that is evidence against a practically meaningful gain under the design; it is not evidence that `C` is universally useless.

No threshold, weighting, or uncertainty method may be changed after seeing outcomes.

---

## 8. Stop rule and bounded review

### 8.1 Stop rule

The study is **infeasible under this design** if any of the following occurs:

- Gate A cannot exhibit a credible multi-`k`, distinct-mechanism construction;
- Gate B cannot produce the required profiles or independent clusters;
- Gate C cannot reach the precision needed to distinguish zero from `Delta_min`;
- fewer than 24 independent clusters are available, or the precision rule requires more than the construction can supply;
- the required stratified grouped folds cannot be formed;
- the design matrix is rank deficient in a way the prespecified rule cannot resolve;
- the family-balanced score cannot be defined or is unsuitable because `L0` is too near zero.

Infeasibility is a legitimate terminal outcome. It is not a negative result about concentration and does not authorize a replacement design.

### 8.2 One bounded review round

This document is the corrected draft for the single authorized review round. Review may:

- accept the protocol as a basis for a future authorization request;
- reject the constructability argument and close the project with a documented limitation;
- request one clarification within the existing design.

Review may not expand the design, add an experiment, or authorize generation. If the protocol does not clear the gate after this round, closure is the outcome.

---

## 9. Preservation obligation

The three-world raw/per-trial archive is about 592 MB and remains local-only. It should be copied to storage independent of the C: drive and verified against its manifest when the other machine becomes accessible. This is a separate preservation obligation, not a dependency for protocol design and not an authorization to rerun anything.

---

## 10. What is not authorized

This document does not authorize:

- solver generation, mutation execution, or bank construction;
- model or API calls;
- simulations or power analyses;
- predictive model fitting;
- changing the frozen banks, scores, protocols, or prior results;
- changing `README.md`;
- Step 2 or any confirmatory study;
- treating the worked construction as empirical evidence of mechanism independence.

---

## 11. Decision record

**Authorized:** document-only, feasibility-first protocol design; one bounded review round.
**Not authorized:** Step 2, solver generation, model calls, execution, simulation, or repository changes to existing artifacts.
**Current scientific status:** the project has not established that `C` adds predictive value, and it has not established that `C` lacks such value.
**Paper constructability status:** conditional pass for the minimum multi-`k` construction; full crossed design and minimum support remain unverified and require a separately authorized Gate B audit.
