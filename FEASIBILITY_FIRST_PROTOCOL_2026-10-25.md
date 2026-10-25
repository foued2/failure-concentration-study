# Feasibility-first protocol design: concentration beyond `k` and family

**Date:** 2026-10-25
**Status:** Authorized document-only protocol design. One bounded review round.
**Decision boundary:** No solver generation, model/API call, execution, simulation, bank change, frozen-result change, or experiment is authorized. Step 2 remains unauthorized.
**Scope:** Design a future study that could test whether adding `C = max(F)/k` improves held-out prediction beyond `k` and predeclared controls, without assuming that such a design is feasible.

This document is the single draft for the authorized review round. It is not a frozen protocol, a study result, or an authorization to generate anything.

---

## 1. Purpose and decision

The existing record does not establish whether concentration adds predictive value, and it does not establish that it lacks such value. The immediate question is therefore narrower:

> Can a credible study be specified, on paper, in which independent solver bodies have the same `k` but different family-count vectors and different `C`, while the competing explanations of family and defect identity remain visible?

The protocol is feasibility-first. It must decide whether that construction can be specified before any resources are spent producing or scoring solvers.

There are three possible outcomes of this review round:

1. **Accept the protocol design.** A future empirical construction audit and confirmatory study may then be proposed under separate authorization.
2. **Reject the constructability argument.** Record the study as infeasible under this design and close with a documented limitation.
3. **Request one bounded clarification.** The review round is single; a clarification is not a mandate to redesign the study.

No outcome authorizes execution.

---

## 2. Fixed question and estimand

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

The primary fixed-`k` stratum is `k=5`. The primary `C` levels are `C=1.0` and `C=0.6`. Other levels are exploratory only and cannot rescue the primary comparison.

The primary score is a predeclared held-out score. The exact score must be frozen before any solver is generated. The domain-weighted and equal-family variants may both be reported, but the primary must be named in advance.

### 2.3 Primary estimand

Let `S0_hat` and `S1_hat` be predictions from two frozen procedures:

- baseline: `k` plus predeclared controls `Z`;
- augmented: `k`, `Z`, and `C`.

Let

\[
\Delta_{\mathrm{pred}}
=\mathbb{E}\left[(S-\widehat S_0)^2-(S-\widehat S_1)^2\right],
\]

evaluated on held-out solver bodies. Positive `Delta_pred` means the augmented procedure predicts better.

`Z` may include task, generator protocol, carrier/anchor family, and mechanism-family indicators. `Z` must not include the complete failure vector `F`; if it did, `C` would be redundant by construction. The full-vector comparison in Section 6 is a separate, prespecified check.

### 2.4 What the estimand is not

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

### 3.2 Grouping rule

The primary cross-validation is grouped by **independent mechanism cluster**, not by family.

- Each distinct mutation site and trigger condition is a mechanism cluster.
- Variants that differ only by a constant, name, or equivalent predicate are the same cluster.
- A cluster must have a distinct full-domain failure set; otherwise it is an alias and is collapsed.
- Replicas and mechanically equivalent predicates stay in the same fold.

Folds are stratified so that every training fold and every held-out fold contains both primary `C` levels and both mechanism families required by the design. If that stratification cannot be achieved, the design is infeasible.

Family identity remains a control. It is not a grouping factor in the primary analysis. A family-held-out analysis may be reported as exploratory, but it cannot replace or rescue the primary result.

### 3.3 Why this rule

Grouping by family would test generalization to new families. Grouping by mechanism cluster tests generalization to new defects within known families, which matches the stated target. The protocol must not silently substitute one target for the other.

---

## 4. Constructability gate

### 4.1 Gate A: paper construction

Gate A is satisfied only if the protocol can exhibit a concrete worked construction with all of the following:

1. at least two solver bodies with the same `k>0`;
2. different family-count vectors and therefore different `C`;
3. a defensible account that the defects are distinct mechanisms, not aliases;
4. a design that includes at least two mechanism families and at least two `C` levels with common support;
5. at least one mechanism family that produces both primary `C` levels, so `C` is not perfectly determined by mechanism family.

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

**Minimal distinct-mechanism pair.**

| Mechanism | Code location | Intended diagnostic profile | `k` | `C` |
| --- | --- | --- | ---: | ---: |
| `P1`: precedence-table mutation | parser precedence table | `(5,0,0,0,0,0)` | 5 | 1.0 |
| `R1`: reduction-order mutation | parser reduction policy | `(3,2,0,0,0,0)` | 5 | 0.6 |

`P1` and `R1` are distinct code sites and distinct mechanisms. Both have the same leading family (F1), so the carrier family is held fixed. They have the same `k=5` but different `C`.

**Within-family crossing example.**

| Mechanism | Code location | Intended diagnostic profile | `k` | `C` |
| --- | --- | --- | ---: | ---: |
| `T1`: digit-run termination mutation | lexer token boundary | `(0,0,0,0,5,0)` | 5 | 1.0 |
| `T2`: whitespace-boundary mutation | lexer token boundary | `(0,0,0,0,3,2)` | 5 | 0.6 |

`T1` and `T2` are different tokenizer mutations but share a mechanism family. They provide within-family `C` variation, which is necessary to separate `C` from mechanism family.

The profiles above are **targets for a future construction audit**, not observed results. The audit must verify the exact family counts, the full-domain failure sets, and the absence of aliases. If the mutations do not produce the target profiles, the design is infeasible; the profiles must not be adjusted after measurement.

### 4.3 Gate A result

**Conditional pass for the minimal construction argument.** The arithmetic and code-location argument is concrete and plausible. The full crossed design is not established: the document specifies the required structure, but it does not prove that two independent mechanism families can each realize both primary `C` levels with the required cluster counts.

Gate A therefore permits a future empirical construction audit, not a confirmatory study. The audit is a separate authorization and is not part of this document.

### 4.4 Gate B: empirical construction audit, not authorized

A future Gate B would build the frozen candidate mutations and verify:

- the intended diagnostic profiles, including exact family counts;
- distinct full-domain failure sets for every claimed independent cluster;
- no aliases, replicas, or mechanism variants mislabeled as independent;
- common support for `C` within at least one mechanism family, and sufficient crossing for the primary model;
- at least the minimum number of independent clusters per `C x mechanism family` cell.

A failure at Gate B is recorded as **infeasible under this design**, not as evidence that `C` lacks predictive value.

### 4.5 Gate C: precision, not authorized

A future Gate C would use the observed between-cluster variance from the construction audit to check whether the design can distinguish zero gain from the practical threshold. If the required precision cannot be reached with the available number of independent clusters, the design is infeasible.

No power simulation, model fit, or outcome analysis is authorized here.

---

## 5. Design structure and minimum support

The primary design must contain:

- one fixed `k` stratum (`k=5`);
- two primary `C` levels (`1.0` and `0.6`);
- at least two mechanism families;
- at least one mechanism family represented at both `C` levels;
- at least three independent mechanism clusters per occupied `C x mechanism family` cell;
- at least three independent clusters at each `C` level within every mechanism family that crosses `C`;
- unbalanced mechanism families may be included only if `C` is not perfectly determined by mechanism family;
- a stratified grouped fold assignment that preserves both `C` levels in every fold.

The worked example suggests how the cells could be populated. The exact task and mutation set must be frozen only after Gate B.

Replicas of the same body do not contribute independent support. Multiple names for the same full-domain predicate do not contribute independent support. More copies of a profile cannot create missing `C` variation.

---

## 6. Models, controls, and comparisons

### 6.1 Primary models

Use prespecified ordinary least squares with an intercept and categorical `k` (a single fixed level here), estimated on training folds and evaluated on held-out solver bodies.

- `M0`: `k` + carrier/anchor family indicators + mechanism-family indicators.
- `M1`: `M0` + `C`.

The primary comparison is `Delta_pred = L(M0) - L(M1)` on the same held-out bodies and folds. Positive means `C` improved prediction.

No nonlinear terms, interactions, or alternative `C` definitions are added after seeing results.

### 6.2 Full-vector check

The full-vector model `MF` uses `k`, the same family and mechanism-family controls, and five of the six family counts. It is compared with `M1` on the same folds.

This check is required because `C` is a summary of `F`. A claim that `C` is a useful summary cannot be converted into a claim that it contains more information than `F`. If `MF` predicts better, that is the result.

### 6.3 Rank and support

Before fitting, check the design matrix for full column rank within every fold. If a fold is rank deficient and cannot be resolved by a prespecified, non-outcome-dependent rule, the design is infeasible for that fold. Do not report a coefficient or effect from a rank-deficient fit as identified.

### 6.4 `k=0`

Bodies with `k=0` are excluded from the primary analysis. Their count is reported. `C` is undefined for them and is never set to zero.

### 6.5 Exploratory analyses

Alternative `C` definitions, alternative partitions, family-held-out generalization, and nonlinear models may be listed as exploratory before the study. They cannot be used to rescue a failed primary comparison. Exploratory results are labelled as such.

---

## 7. Evidential standards

### 7.1 Uncertainty

The primary uncertainty procedure is a paired cluster bootstrap over independent mechanism clusters, stratified by `C x mechanism family`, with 10,000 resamples and a percentile 95% interval. The unit of resampling is the mechanism cluster, not the individual solver row. Replicas remain attached to their cluster.

The interval is for `Delta_pred` on the held-out bodies. It is not a confidence interval about a real-world population unless the sampling design supports that interpretation.

### 7.2 Two thresholds

Two standards are frozen separately.

**Any positive gain.** The lower bound of the 95% interval for `Delta_pred` is above zero.

**Practically meaningful gain.** The lower bound of the 95% interval is above a prespecified minimum:

\[
\Delta_{\min}=0.05\,L(M0),
\]

a 5% relative reduction in baseline held-out MSE. This is a planning value, not an empirical estimate. It must be justified in the review round as a meaningful improvement for the intended decision.

A result can satisfy the first standard without satisfying the second. That outcome is reported as a statistically detectable but not practically meaningful gain, not as support for the stronger claim.

### 7.3 Precision and interpretation

If the interval is too wide to distinguish zero from `Delta_min`, the result is **inconclusive**, not negative. If the interval excludes `Delta_min` on the low side but lies above zero, the result supports a positive but not practically meaningful gain. If the interval lies entirely below `Delta_min`, that is evidence against a practically meaningful gain under the design; it is not evidence that `C` is universally useless.

No threshold or uncertainty method may be changed after seeing outcomes.

---

## 8. Stop rule and bounded review

### 8.1 Stop rule

The study is **infeasible under this design** if any of the following occurs:

- Gate A cannot exhibit a credible distinct-mechanism construction;
- Gate B cannot produce the required profiles or independent clusters;
- Gate C cannot reach the precision needed to distinguish zero from `Delta_min`;
- the required stratified grouped folds cannot be formed;
- the design matrix is rank deficient in a way the prespecified rule cannot resolve;
- the minimum support in Section 5 is not met.

Infeasibility is a legitimate terminal outcome. It is not a negative result about concentration and does not authorize a replacement design.

### 8.2 One bounded review round

This document is the single draft for the authorized review round. Review may:

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
**Paper constructability status:** conditional pass for the minimal distinct-mechanism construction; full crossed design remains unverified and requires a separately authorized Gate B audit.
