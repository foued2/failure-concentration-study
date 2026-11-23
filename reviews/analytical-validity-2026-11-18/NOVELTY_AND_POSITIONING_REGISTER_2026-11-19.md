# Novelty and positioning register — 2026-11-19

**Status:** record and positioning audit. Adds no hypothesis, authorizes nothing, executes nothing.
**Answers:** Gate 0 of the goal document — *has this proposition already been tested?*
**Does not answer:** whether the hypothesis is true, or whether it is worth funding.

---

## 1. The proposition, stated once

Everything below is about one sentence. If a paper tests this sentence, the programme stops.

> **P.** *Within the observed parent set*, for an engineered solver variant `v`, let
> `f(v) = (f_1,…,f_8)` count *definite* diagnostic failures across eight prespecified diagnostic input
> strata, `k(v) = Σ_j f_j`, and `C_D(v) = max_j f_j / k(v)`. Does `C_D(v)` improve leave-one-parent-out
> predictive log loss on the **fixed 78-record development bank**, beyond the exact-cell baseline
> `(q, Z, k, ℓ)` with record effects — keeping the parent as the independent unit, and making no claim
> about a new parent population?

Three features of `P` do the discriminating work, and each must be kept when searching:

1. **A fixed, prespecified 8-dimensional partition** of diagnostic inputs, not a learned representation.
2. **The maximum share**, not a general function of the failure vector.
3. **Parent-grouped evaluation**, not input-level or variant-level random splits.

A search that finds correctness prediction from execution but drops any of the three has not tested `P`.

**Scope, stated in the proposition itself.** `P` is a *conditional* claim. It concerns the observed parent
set, it is scored on a fixed development bank that the plan declares "publicly exposed, never sealed"
(B1 v1.7 §1, §12), and it makes no statement about a new parent population — B1 §5.7 V1/V4 refuses that
inference explicitly. Any version of `P` that is written as external generalisation to independently
developed parent implementations is a different and unsupported claim, and should not be attributed to
this programme.

---

## 2. The statistic is not new, and the protocol already says so

`LC518_A2_AUDIT_PROTOCOL_DRAFT_2026-11-06.md:218` names the statistic:

> "The concentration value is the Berger–Parker dominance index of the failure distribution:
> **`C_D = max_{j=1..8}(f_j / k_fail)`**"

The Berger–Parker index is from ecology: Berger & Parker 1970, *Science* 168(3937):1345–1347,
`10.1126/science.168.3937.1345` (verified, Crossref). It is one of the most widely used dominance
indices in community ecology, with a large methodological literature on its sampling properties.

**Consequence:** any claim that the programme *introduced* a concentration measure is false on its own
frozen record. The contribution, if any, is the **predictive use** of a 1970 index as a solver-level
covariate. That is a much smaller claim, and it should be stated that way everywhere.

The name "concentration theory" should not survive this. The defensible description is the one GPT
proposed and it is adopted here:

> *A proposed study of the incremental predictive value of diagnostic failure dominance in engineered
> solver implementations.*

---

## 3. One theorem, and what it does and does not settle

These matter because reviewers keep asking questions that have mathematical answers. They are stated
here once so they stop being re-litigated — but the scoping of the theorem matters as much as the
theorem, and an earlier version of this section overstated it.

### 3.1 The theorem: `C_D` cannot carry more *population* information than `F`

`C_D` is a deterministic function of `F = (f_1,…,f_8)`: it is `max(F)/ΣF`. Therefore
`σ(C_D) ⊆ σ(F)`, and by the data-processing inequality

```
I(Y ; C_D | X)  ≤  I(Y ; F | X)        for every joint distribution
```

and, conditioning further on `F`,

```
I(Y ; C_D | X, F)  =  0                exactly
```

Both hold for every joint distribution and every conditioning set `X`. `F` is an information ceiling
for `C_D` that no sample size can overturn.

**What this means:** a claim of *information superiority over the full failure vector* is false by
construction. `C_D` cannot be shown to carry more information about `Y` than `F` does. That is the whole
theorem, and it is all the theorem says.

### 3.2 What the theorem does **not** say

It is a statement about a bound at the population level, not a statement about the quantity B1
estimates. Four distinctions have to be kept apart:

| Claim | Mathematical status |
|---|---|
| `C_D` carries more population information about `Y` than the full `F` | **Impossible** — §3.1 |
| `C_D` carries **no** information beyond the baseline `X = (q, Z, k, ℓ)` | **Not implied.** `I(Y;C_D\|X) > 0` is entirely possible and is exactly the B1 question |
| A fitted `C_D` model improves held-out log loss over the exact-cell baseline | **Testable** — this is B1's estimand |
| A fitted `C_D` model beats a fitted full-vector model in finite samples | **Empirically testable**, and *not* excluded by §3.1: a lower-dimensional feature can generalise better through lower estimation variance, regularisation, or a restricted model class, without being more informative in the population |

**The correction this section carries:** an earlier draft of this register concluded from §3.1 that
"accuracy cannot be the claim". That does not follow, and it contradicted the register's own proposition
in §1, which asks precisely whether `C_D` adds information **beyond `X`**. The ceiling is against `F`,
not against `X`. Accuracy **is** a legitimate claim, but only as *incremental predictive performance
against the predeclared exact-cell baseline*. It may never be stated as information superiority over
`F`, and it may never be stated as a parent-population result.

### 3.3 What is testable, in order of strength

1. **Incremental value beyond the exact cell** — `I(Y;C_D|X) > 0`, evaluated as held-out log-loss
   improvement under B1's conditional LOPO procedure. This is the primary claim and it is non-vacuous.
2. **Finite-sample performance against the full-vector model** — a comparison of fitted models, where
   `C_D` may win on variance even though it cannot win on population information. Any such win must be
   reported as a finite-sample, model-class result, not as an information result.
3. **Compression ratio** — how much of `F`'s information the scalar retains, with the loss weighed
   against parsimony.
4. **Parsimony, stability, interpretability** — the secondary justifications, none measured anywhere in
   the corpus.

### 3.4 The W1 numbers, correctly scoped

The three-world W1 numbers are the only executed measurement of the compression ratio in the corpus:

| Quantity | W1 / domain score | Note |
|---|---|---|
| `F` gain | `+7.90×10⁻⁴` | `[+6.92×10⁻⁴, +8.86×10⁻⁴]`, excludes 0 |
| `C` gain | `+1.96×10⁻⁶` | `[−1.24×10⁻⁶, +7.58×10⁻⁶]`, includes 0 |
| Point-estimate ratio | `C/F ≈ 1/403` | `C` retains ≈0.25 % of `F`'s gain |

**Scope:** this is the result of **one fitted simulation**, not a consequence forced on every fitted
model by §3.1. The theorem fixes the *ordering of population information*; it does not fix the
magnitude of a fitted comparison, and it does not forbid `C` from beating `F` in a particular finite
sample. Here `C`'s interval spans zero and the second partition reverses the sign, so "0.25 %" is
illustrative only. The honest reading is: *in the one executed world, under one model class and one
partition, the scalar retained a fraction of a percent of the vector's gain, and the scalar's own
interval was indistinguishable from zero.* That is a poor compression result for that design. It is not
a refutation of `C_D`, and it is not evidence about B1's baseline comparison, which does not condition on
`F`.

### 3.5 A test that must not be run

Because `I(Y;C_D|X,F) = 0` exactly, a test of "incremental value of `C_D` **beyond the full failure
vector**" has a known answer. It must not be run, reported, or funded. This also corrects a recurring
misreading of condition 6: the `F`-versus-`C` comparison in the three-world simulation is a bound on
compression loss, not an incremental-value test. B1 correctly does not condition on `F`; conditioning on
`F` would make the estimand identically zero.

---

## 4. Prior work, verified

Every DOI below was resolved against Crossref on 2026-11-19. Where a venue differs from the review's
citation, the correction is in §6.

| # | Work | What it establishes | Pre-empts | Does **not** pre-empt |
|---|---|---|---|---|
| 1 | Berger & Parker 1970, *Science* 168:1345, `10.1126/science.168.3937.1345` | The dominance index itself; its sampling behaviour | Any claim of a novel concentration measure | Predictive use on software |
| 2 | Boland, Proschan & Tong 1987, *PEIS* 1(2):175, `10.1017/s0269964800000383` | Fault diversity in reliability models, multinomial structure | "Failure diversity matters for reliability" as an idea | Solver-level prediction under parent-grouped evaluation |
| 3 | Chen & May 2016, *IEEE TR* 65(3):1149, `10.1109/tr.2015.2503335` (conference predecessor SERE 2014, `10.1109/sere.2014.13`) | Diversity model from failure distributions; common-failure probability for safety cases | Distributional diversity as a quantitative safety input | The 8-stratum prespecified partition over diagnostic inputs |
| 4 | DiGiuseppe & Jones 2012, *ICST*, `10.1109/icst.2012.99` | Failure profiles do not map cleanly to individual fault causes, at scale | The **mechanism** reading of clustering (gate 2) | The predictive claim; this is about interpretation, not prediction |
| 5 | DiGiuseppe & Jones 2012, *FSE*, `10.1145/2393596.2393629` | Concept-based failure clustering | "Cluster failures by semantic signature" as novel | A fixed 8-cell input partition |
| 6 | Song et al. 2022, *JSS* 193:111452, `10.1016/j.jss.2022.111452` | Empirical evaluation of failure clustering, 1 060 faulty versions | "We empirically evaluate failure clustering" | Maximum-share as a predictor |
| 7 | Almaghairbe & Roper 2016, *ISSRE*, pp. 116–126, `10.1109/issre.2016.22` | Semi-supervised classification of passing and failing executions from dynamic execution data | "Separate pass from fail using execution traces" as novel | Anything about concentration or cluster failure share — not studied in this paper |
| 8 | Almaghairbe & Roper 2017, *Software Quality Journal* 25(3):803–840, `10.1007/s11219-016-9339-1` (online 2016) | Clustering anomalies to separate passing and failing executions; small clusters were sometimes composed of at least 60 % failures | **"Failure concentration is an established empirical observation"** | Predictive use of a maximum share, under parent-grouped evaluation, against an exact-cell baseline |
| 9 | Neural CodeRanker 2022, *NeurIPS* | Supervised correctness prediction from execution categories | Learning correctness from diagnostic failure information | Fixed interpretable scalar |
| 10 | CodeT 2023, *ICLR* | Generated tests + agreement for candidate selection | Test-based selection | — |
| 11 | LEVER 2023, *ICML* | Correctness prediction from task + code + execution; ablation shows execution helps | Execution outcomes add predictive information | The specific statistic or the grouped evaluation |
| 12 | AlphaCode 2022, *Science* 378(6624):1092, `10.1126/science.abq1158` | Filtering, clustering, reranking at scale | Clustering for selection | — |
| 13 | CodeScore 2025, *ACM TOSEM* 34(3):1–22, `10.1145/3695991` | Learns to estimate test PassRatio and executability | Broad "predict correctness from execution" | Incremental value of a maximum share |
| 14 | Sun et al. 2024, *ASE*, `10.1145/3691620.3695000` ("RankEF") | Execution feedback for ranking candidates | Same | Same |

**Read as a set:** rows 9–14 establish that execution-derived signals predict correctness. Rows 1–8
establish that failure diversity, failure clustering, and failure concentration are mature ideas. Neither
set tests `P`.

**Row 8 is the closest single result in the corpus**, and it is why the two Almaghairbe papers must stay
separate: the clustering paper reports high failure share in small clusters, which is the *observational*
form of the programme's premise. It does not predict held-out correctness from that share. That distance
is the whole of `P`.

**But the margin is narrow.** `P` survives on the conjunction of an old index, a fixed partition, and a
grouped evaluation. Remove any one and the claim is already covered. A reviewer is entitled to ask
whether that conjunction is a scientific contribution or a well-specified ablation. The register
records the question rather than answering it.

---

## 5. The nearest genuine threat

The strongest competitor is not any single paper above; it is the **learned-representation family**
(rows 9–14). Given the same `(f, q, Z, k, ℓ, Y)` data, a flexible model over `F` has a higher population
ceiling than `C_D` (§3.1). That does **not** settle the B1 question, because B1 does not compare `C_D`
against `F`. It compares `C_D` against the exact cell.

Two different threats must therefore be separated:

**Threat A — to the B1 estimand.** Does the exact cell `(q, Z, k, ℓ)` plus record effects already absorb
the composition information that `C_D` carries? If it does, the incremental term is zero *in this
baseline*, and the study returns a negative result on a well-posed question. That is a legitimate
outcome and B1 is designed to detect it. It is not a literature threat; no prior work computes this
baseline.

**Threat B — to the contribution.** If the baseline is beaten, is a one-parameter improvement worth
reporting? A flexible model over `F` would likely beat it further in population terms. The remaining
justifications are parsimony, finite-sample stability, interpretability, and pre-registration — and none
of the four is measured anywhere in the corpus. This is the question a reviewer is entitled to press, and
the register does not answer it.

A narrower version of Threat B is now specified separately: whether the *maximum share* is doing the work,
rather than any other shape summary of the same failure vector. That comparison is well posed within an
exact cell, and its identifying variation is *equal competitor value with differing `C_D`* — which is
competitor-specific and begins as early as `k = 3` for the second-largest share, but is almost absent for
Shannon entropy. See `DOMINANCE_SPECIFICITY_AND_PARTITION_SENSITIVITY_2026-11-19.md` §4.1.

The earlier draft of this section said `P` "cannot be won on accuracy". That was wrong for the same reason
as §3.2: accuracy against `X` is testable, and `C_D` may well win it. What `C_D` cannot win is accuracy
**against `F` in population information**. Those are different contests, and only the first is the study.

---

## 6. Citation corrections

| Review claim | Verified position | Correction |
|---|---|---|
| AlphaCode "(2023)" | *Science* **2022**, 378(6624):1092–1097 | Year corrected; Claude's recollection was right |
| CodeScore "ACM TOSEM, 2024" | TOSEM 34(3):1–22, Crossref year **2025** | Online-first 2024, issue 2025; cite the DOI, not the year |
| "RankEF (ASE 2024)" | Actual title: *Sifting through the Chaff: On Utilizing Execution Feedback for Ranking the Generated Code Candidates*, ASE 2024, pp. 229–241 | "RankEF" is the system name; cite the title |
| "Almaghairbe & Roper (published online 2016; journal issue 2017)" | Two distinct papers, both verified: *Automatically Classifying Test Results by Semi-Supervised Learning*, ISSRE **2016**, pp. 116–126, `10.1109/issre.2016.22`; and *Separating Passing and Failing Test Executions by Clustering Anomalies*, *Software Quality Journal* **25**(3):803–840, `10.1007/s11219-016-9339-1`, online 2016, issue 2017 | Both records stand. The "no 2017 journal issue" statement applied only to the ISSRE paper and was over-generalised in the previous draft |
| Small-cluster high-failure-share finding attributed to the ISSRE paper | It belongs to the **Software Quality Journal** paper (row 8), which reports small clusters sometimes composed of at least 60 % failures | Wrong-paper attribution, corrected. This one matters: the finding is the closest prior result to the programme's premise |
| "average precision 0.79 across unseen protocol implementations" attributed to Almaghairbe & Roper | Not located in either Almaghairbe paper during this round; provenance **unverified** | The figure must not be cited until the paper it appears in is identified and read |
| "Learning to Encode and Classify Test Executions" | No DOI resolved; treat as arXiv-only until a venue record is produced | Status: **unverified**, do not cite as peer-reviewed |

The Almaghairbe rows matter beyond bookkeeping: a finding from the clustering paper was attached to the
semi-supervised classification paper, and a numeric figure was cited with no paper identified for it.
Any figure carried into a future record must be re-checked against the paper it actually appears in.

---

## 7. Search limits and stopping rule

**Limits, stated so the register cannot be read as a systematic review:**

- The Elicit connector returned `api_access_denied` for both reviewers; no Elicit search was performed.
  An Elicit result remains **pending** and is not implied by anything here.
- Full text was read for Boland et al. and Song et al. only. Chen & May, both DiGiuseppe papers, and
  Almaghairbe & Roper are represented by abstracts and records.
- No systematic protocol: no database list, date range, query strings, or screening criteria.
- Coverage is biased toward what the reviewers already knew to look for. Absence of a hit is weak
  evidence of absence, and is not novelty.

**Stopping rule, pre-registered before the next search:**

> If any work is found that tests `P` — a prespecified dominance share over a fixed diagnostic partition,
> evaluated for incremental held-out correctness beyond the exact-cell baseline, with parents held out —
> the programme stops at Gate 0 and does not proceed to gate 1. A close result that differs on exactly
> one of the three discriminating features in §1 must be recorded and adjudicated, not waved past.

---

## 8. Gate 0 verdict

| Question | Answer |
|---|---|
| Is the index novel? | **No** — Berger–Parker 1970, and the protocol already names it |
| Is "failures concentrate" novel? | **No** — rows 4–8; row 8 reports it empirically |
| Is "execution predicts correctness" novel? | **No** — rows 9–14 |
| Is `P` as stated already tested? | **Not found**, on a non-systematic search |
| Is `P` novel? | **Unproven.** Not the same as novel. |
| Is accuracy against the exact-cell baseline a legitimate claim? | **Yes.** `I(Y;C_D\|X) > 0` is possible and is B1's estimand |
| Is accuracy against the full failure vector a legitimate claim? | **No.** `I(Y;C_D\|X) ≤ I(Y;F\|X)`; this is a theorem, not a finding |
| Does `P` have a defensible contribution? | Incremental value beyond the baseline is testable and sufficient for B1. Whether a one-parameter gain is *scientifically interesting* beyond parsimony, stability, and interpretability is open, and no record measures it |

**Gate 0 status: OPEN, with the burden shifted.** The programme may proceed to measurement work. It may
not describe its contribution as novel, and it may not describe `C_D` as more informative than the full
failure vector. Accuracy **against the predeclared exact-cell baseline** remains available as a claim,
because that comparison is against `X`, not against `F`.

---

## 9. Dated amendment — 2026-11-20 (Gate 0 scoping round)

**Trigger:** GPT's Gate 0 memo and Claude's review of it. This section adds one prior work, closes one
provenance item, and pre-registers one design-only census. It changes no verdict: Gate 0 remains **OPEN**
and `P` remains **unproven**. The §4 table above is retained unamended, so the dated record keeps its own
text; the addition and the corrections are recorded here.

### 9.1 Row 8a — the 2015 precursor is real and belongs in §4

| # | Work | What it establishes | Pre-empts | Does **not** pre-empt |
|---|---|---|---|---|
| 8a | Almaghairbe & Roper 2015, *AST* — 2015 IEEE/ACM 10th International Workshop on Automation of Software Test (ICSE), pp. 3–7, `10.1109/ast.2015.8` | Preliminary study: cluster-based anomaly detection builds an oracle from input/output pairs; failures "tend to group into small clusters"; two systems; order-of-magnitude reduction in outputs needing manual examination | "Cluster failures to detect bugs / build an oracle" as novel, and the priority of the small-cluster observation (2015, before the SQJ paper) | Maximum-share scalar, held-out correctness prediction, exact-cell baseline, parent-grouped evaluation |

Crossref record: IEEE, published print 2015-05, pp. 3–7. The venue string is the workshop's full name, not
a journal.

**Disposition of Claude's "closer than the SQJ paper".** Not accepted as stated. The 2015 paper is the
*earlier* statement of the same hypothesis on two systems; the 2017 *Software Quality Journal* paper is
the fuller evaluation on three systems with the quantified finding. So 2015 takes priority for the
observation and the SQJ paper remains the closest *evidence*. Neither tests `P`, and adding row 8a does not
change §8.

### 9.2 The ≥60 % finding: publisher abstract and full-text qualification

The publisher abstract for Almaghairbe & Roper's *Software Quality Journal* paper
(DOI [10.1007/s11219-016-9339-1](https://doi.org/10.1007/s11219-016-9339-1), issue 25(3):803–840;
published online 2016-10-03) states that, **in many cases**, small clusters were composed of at least
60 % failures, and often more. That wording is essential. It is a cluster-composition observation for
some system/configuration combinations, not a universal rate, not a population estimate, and not a
prediction of held-out correctness.

The full text was also checked from the authors' institutional repository copy ([Strathprints full-text PDF](https://strathprints.strath.ac.uk/58621/1/Almaghairbe_Roper_SQJ_2016_Separating_passing_and_failing_test_executions.pdf)). It documents substantial
heterogeneity across systems, program versions, and clustering configurations:

- In §6.2, the **agglomerative hierarchical-clustering** results for Sed show small-cluster
  failure density below 50 %, peaking just above 40 % under complete linkage at an average cluster
  size of about three. This statement is specific to that method and analysis.
- The same section reports a markedly different Sed result under **DBSCAN**. Table 7's Sed V5
  row reports cluster count 48.23 % of the test-set count, average cluster size 1 % of the test set,
  failure density 83.3 %, and F-measure 0.3091 (the table's DBSCAN setting for Sed is
  epsilon = 1.5, MinPoints = 1). The authors describe the smallest-cluster density as very high and
  the F-score as reasonable.
- This is not a clean counterexample to the agglomerative result. The DBSCAN configuration generated
  a very large number of very small clusters, almost twice the number explored in the agglomerative
  analysis. The density therefore comes with substantial fragmentation and should not be read as
  evidence of broad failure capture or robust performance. EM, by contrast, performed very poorly on
  Sed. These are method-dependent results, not contradictory estimates of one universal Sed rate.
- NanoXML version 3 is a direct counterexample to a universal small-cluster claim: the paper reports
  that its largest clusters contained most of the failures.
- Other sections report different quantities, including the proportion of all failures captured by
  small clusters (for example, three of four Sed failures in a particular analysis, and a later
  statement that 75 % of Sed failures lay in about 16 % of results). Those are *failure-capture* or
  concentration measures, not the same denominator as the percentage of failures **within** small
  clusters. They must not be merged into the ≥60 % cluster-density result.

Accordingly, row 8 remains a real and close precedent, but its result must be described as
configuration-dependent and heterogeneous. The paper supports the proposition that failure
concentrations can occur in clusters; it does not support "failures are usually concentrated in small
clusters", much less the B1 predictive proposition P. The separate ISSRE 2016 semi-supervised
classification paper remains a different work and is not the source of the ≥60 % result.

The 2015 AST precursor in row 8a remains the earlier preliminary observation on two systems. The 2017
SQJ article is the fuller three-system evaluation. Neither tests P.

### 9.3 Challenge 1 — within-cell support and exposure-basis arithmetic

Claude's underlying concern is accepted: the exact cell fixes total definite failures and unresolved
counts, so the possible within-cell contribution of C_D must be described accurately and its realised
support audited before any predictive fit.

**What varies.** Within a fixed-k cell, let M = max_j f_j. Then C_D = M/k. C_D is invariant to
permuting stratum labels. It records only the *size* of the largest failure count, not which diagnostic
stratum contains that count. It therefore cannot identify a named failure mechanism or localise failures
to a semantic stratum. Such a claim would require a different analysis of the stratum-labelled vector.

**Record-level support bound.** On the record-level exposure basis, R = (8,8,8,8,8,8,8,8). Therefore
M is in {ceil(k/8), …, min(8,k)}. There are at most eight attainable M values, hence at most eight
distinct C_D values at any fixed k. For 9 ≤ k ≤ 16, the record-level upper bound is seven distinct
values. This is a record-level result only.

**Canonical-level support is not identical.** On the canonical basis, R = (8,8,8,8,8,4,8,8): the
sixth stratum has capacity four. M is still at most eight, so the ceiling of at most eight distinct
C_D values survives. But the exact attainable set is not given by the record-level formula above.
For a concrete distinction at k = 54:

- With record-level capacities, M = 7 is feasible, for example
  (7,7,7,7,7,7,7,5), whose entries sum to 54.
- With canonical capacities, if M were at most 7, the total could be no larger than
  4 + 7×7 = 53. Therefore M = 7 is impossible at k = 54; the canonical vector must have M = 8.

This is not a relabelling of one vector. The two exposure bases define different failure-count vectors
and different C_D measurements. Canonical C_D must be recomputed from the canonical failure vector;
it must never be obtained by averaging or selecting paired record-level values. The ≤8 distinct-value
ceiling holds for both bases, but the record-level attainable-set formula must not be presented as the
canonical attainable set.

**What B1 v1.7 actually requires.** The full-population B1 cell eligibility rule is
B1(c)=1 only when k ≥ 2, G_c ≥ 3 distinct parents, and D_c ≥ 2 distinct C_D values. This is distinct
from the LOPO training-fold estimability rule: in each fold-cell, G_c^train ≥ 2,
D_c^train ≥ 2, and W_C,c^train > 0. The earlier stop rule in this amendment, which used only
two parents, was too weak: two parents do not satisfy the full-population eligibility rule. Nor is
checking only that some cell has two C_D values enough. B1 requires the complete design-only audit,
including all eligible and excluded cells, scored and excluded fold-cells, scored parents, and exact
test-row sets per fold.

**Pre-registered design-only support census (first Gate 1 action, only after explicit reopening).**
For each exposure basis separately, recompute from its own diagnostic failure vectors:

1. Full-population cell counts and decisions for every exact B1 cell (q, Z, k, ℓ): version count,
   distinct-parent count G_c, distinct-C_D count D_c, distinct M and C_D values, and W_C.
   Explicitly record eligible cells (k ≥ 2, G_c ≥ 3, D_c ≥ 2) and every excluded cell with its reason.
2. For every LOPO fold and every cell, G_c^train, D_c^train, W_C,c^train, and the scored/excluded
   decision with its reason.
3. The scored-parent membership, the exact scored test-row identifiers per fold, total scored rows,
   and parent/row coverage. Report all exclusions; do not silently pool cells or drop parents.
4. The record-level and canonical-level audits side by side, without averaging their C_D values or
   treating one basis's support decisions as the other's.

**Stop/interpretation rule.** If no full-population cell satisfies k ≥ 2, G_c ≥ 3, and D_c ≥ 2,
there is no B1 primary sample with the required cell support and no model fitting is permitted.
If eligible cells exist but no LOPO fold supplies the required training support or no parent/test rows
remain scoreable, report the exact support failure and stop before fitting. If some parents are scoreable,
report the complete coverage and exclusions. B1 does not currently specify a minimum acceptable
overall |G_score| threshold; this audit must not invent one. Coverage adequacy therefore remains an
explicit unresolved design decision, not an automatic PASS from finding one eligible cell.

This census is design-only: it uses diagnostic/design quantities, never outcomes or fitted models. It
has not been run because it requires the LC518 diagnostic tables and the pause prohibits bank access.
No result is implied.

### 9.4 Challenge 2 — power and MDE belong to Gate 4, not Gate 0

The earlier amendment correctly noted that no empirically grounded MDE exists, but incorrectly made
that absence a Gate 0 exit condition. This is corrected.

The repository's illustrative expression
MDE_80 ≈ 2.802 · σ_u / (sd(C) · sqrt(J))
and its numerical examples are an approximation for a simplified cluster-level covariate setting.
The displayed inputs were assumed, not estimated. The calculation is not an MDE for B1 v1.7.

B1 is structurally different: C_D is a version-level exposure nested within parent groups; multiple
variants belong to each parent; the outcome is record-level Y_{v,r} across 78 bank records per version;
evaluation is leave-one-parent-out; and the test conditions on exact cells and design-only fold-support
decisions. Its operating characteristics depend on within- and between-parent exposure variation,
parent and record dependence, cell support, fold-level estimability, the scored-parent set, and the
frozen conditional-randomization/fitting pipeline. The simple expression above does not represent
those dependencies.

Consequently, the illustrative numbers must not be used to claim that 30 parents are inadequate, that
150 variants are required, or that 150 would be adequate. No such conclusion follows from that formula.
The 30-parent × 5-variant arrangement remains a logistics scenario, not an accepted operating sample
size or execution GO. The LC518 bank's statement that structural coverage is not a power calculation
also remains binding.

A defensible power/MDE or operating-characteristic assessment belongs to Gate 4. It would have to
simulate the actual frozen B1 pipeline under declared null and non-null data-generating processes,
including parent nesting, record outcomes, the actual within-cell C_D variation, full-population
eligibility, each LOPO fold's support rule, and the full scored-parent coverage. No such assessment has
been run or validated. S1 known-gain calibration is also a Gate 4 validation task, not literature evidence
for Gate 0.

**Gate 0 does not require an MDE or a chosen parent count.** Gate 0 closes on the scoping-review
deliverable: a sufficiently documented evidence matrix and citation process, a precise candidate
contribution statement, comparison with the closest prior work, and a fixed inferential scope. It
cannot close by treating a failed search as evidence of novelty.

### 9.5 Challenge 3 — "no exact match" is not closure: already the record's position

§7 states that the search is non-systematic and that absence of a hit is weak evidence of absence; §8 says
`P` is **unproven, not novel**. This amendment makes the acceptance sentence explicit:

> Gate 0 closes only when the contribution is stated in one precise paragraph, its difference from the
> closest prior work is shown, its inferential scope is fixed, and **no priority or novelty claim rests on
> the absence of a search hit**. A completed scoping review carrying the §7 evidence-matrix fields is the
> minimum. A failed search is not a result.

### 9.6 Citation hygiene

The favicon links and the stray "ES" in GPT's message are chat-interface artifacts, not record content.
Bibliographic identifiers are separated from content-verification level in §9.7. DOI resolution or a
publisher record verifies identity and metadata; it does not mean that the full paper was read. The new
entries below preserve that distinction.

### 9.7 Evidence-matrix additions and verification levels

These are dated additions to the review matrix, not retroactive renumbering of the §4 table. They broaden
the set of relevant precedents and make the verification boundary explicit. A bibliographic record or
abstract is not silently promoted to a full-text review.

| Register ID | Work and DOI | What it establishes | What it pre-empts | What it does not pre-empt | Verification level |
|---|---|---|---|---|---|
| 8b | Dickinson, Leon & Podgurski (2001), “Pursuing Failure: The Distribution of Program Failures in a Profile Space,” ESEC/FSE-9, pp. 246–255. [10.1145/503209.503243](https://doi.org/10.1145/503209.503243) | Failure executions can occupy unusual/sparse regions of an execution-profile space; the paper motivates failure-pursuit sampling from profile-space structure. | Clustering and geometric/profile-space structure of program failures as a new general idea. | A prespecified diagnostic-input partition, a maximum-share scalar, exact-cell incremental prediction, or parent-grouped evaluation. | Bibliographic record and abstract-level description checked; full text not reviewed in this pass. |
| 8c | Wu et al. (2004), “A Statistical Model to Locate Faults at Input Level,” ASE 2004, pp. 274–277. DOI withheld pending publisher-level resolution. | Uses success/failure patterns to locate faults at input level; the abstract reports five programs and 17 experiments, with mean precision 0.803 and recall 0.697. | Statistical use of input-level failure patterns for fault localisation. | Prediction of held-out solver-version record correctness, C_D, or incremental value beyond the B1 exact-cell baseline. | Title, authors, venue, pages and abstract-level result corroborated; third-party DOI records conflict; full text not reviewed in this pass. |
| 15 | Herzig (2014), “Using Pre-Release Test Failures to Build Early Post-Release Defect Prediction Models,” ISSRE 2014, pp. 300–311. [10.1109/ISSRE.2014.21](https://doi.org/10.1109/ISSRE.2014.21) | Test-execution metrics, including sequences/bursts of quality-gate failures, are used to predict pre- and post-release defect counts for code artifacts in the Windows 8 development setting. The study is explicitly exploratory. | Use of development-time test-failure metrics as predictors of later software defect outcomes. | Record-level correctness prediction for solver variants, the eight fixed diagnostic strata, maximum-share dominance, or B1's parent-held-out conditional estimand. | Full text reviewed; single-product setting and stated scope limitations retained. |
| 16 | Wu et al. (2004), “Application of Maximum Entropy Principle to Software Failure Prediction,” COMPSAC 2004, pp. 180–185. [10.1109/CMPSAC.2004.1342825](https://doi.org/10.1109/CMPSAC.2004.1342825) | Two maximum-entropy models use input/failure co-occurrence and fault/failure relationships; the abstract reports five programs and 17 experiments, with average precision 0.876 and 0.858. | Predictive/statistical modelling of software failure from input and fault relationships. | C_D, an eight-stratum prespecified failure-dominance summary, exact-cell incremental prediction, or parent-grouped solver-version evaluation. | Bibliographic record and abstract checked; full text not reviewed in this pass. |
| 17 | Chen et al. (2017), “An Empirical Study on the Effect of Testing on Code Quality Using Topic Models: A Case Study on Software Development Systems,” *IEEE Transactions on Reliability* 66(3):806–824. [10.1109/TR.2017.2699938](https://doi.org/10.1109/TR.2017.2699938) | LDA-derived topics represent higher-level themes across source and test files; topic testedness and topic defect density are used to predict defect-prone and under-tested topics in Mylyn, Eclipse, and NetBeans. The paper reports average precision 0.75 and recall 0.77 for that topic-level task. | Semantic/topic-level testing and defect-proneness analysis, including prediction using test information. | Fixed diagnostic *input* strata, a maximum share of definite failures, or per-record correctness of held-out solver variants. | Full text reviewed. |
| 18 | Xiong et al. (2018), “Identifying Patch Correctness in Test-Based Program Repair,” ICSE 2018, pp. 789–799. [10.1145/3180155.3180182](https://doi.org/10.1145/3180155.3180182) | Uses execution-behaviour similarity of passing/failing tests to assess generated patch correctness. Its 139-patch study reports preventing 56.3 % of incorrect generated patches without blocking correct patches in that dataset. | Correctness assessment from behaviour of failing and passing tests in automated program repair. | Solver-variant record-level correctness, a fixed eight-stratum dominance statistic, or B1's exact-cell/LOPO estimand. | Full text reviewed; the 139-patch dataset and study-specific result are not generalised beyond the paper. |
| 19 | Tian et al. (2022), “Predicting Patch Correctness Based on the Similarity of Failing Test Cases,” *ACM Transactions on Software Engineering and Methodology* 31(4), Article 77. [10.1145/3511096](https://doi.org/10.1145/3511096) | BATS uses representations and similarity of failing test specifications/cases to historical patches to predict patch correctness; results vary with similarity thresholds and the availability of comparable historical tests. | Prediction of patch correctness from failing-test similarity and historical patch behaviour. | A fixed input-stratum maximum-share statistic, incremental prediction beyond `(q,Z,k,ℓ)`, or parent-held-out solver-variant record correctness. | Full paper/publisher postprint reviewed; dataset and threshold dependence retained as limitations. |

**Metadata corrections and open identifier.**
- Dickinson, Leon & Podgurski's DOI remains `10.1145/503209.503243`. The SQJ paper's own reference list
  and DBLP proceedings record support that identifier. A conflicting `503241.503243` string appears
  in a secondary ResearchGate record and is not adopted.
- The DOI for Wu et al.'s ASE 2004 input-level fault-localisation paper is **not settled in this pass**.
  Third-party records return incompatible strings, including `10.1109/ASE.2004.10008`,
  `10.1109/ASE.2004.1342745`, `10.1109/ASE.2004.1342763`, and `10.1109/ASE.2004.7`.
  The official ASE 2004 programme confirms the paper's title, authors and venue, and DBLP confirms
  pages 274–277, but the primary IEEE/Crossref DOI record has not been resolved here. No candidate DOI
  is printed in row 8c or used as a citation until that conflict is settled.
- Chen et al.'s issue is `66(3)`, not `66(4)`; the page range remains 806–824.

**Interpretation.** These additions close neither Gate 0 nor the novelty question. They show that the
surrounding territory is broader than failure clustering alone: input-level fault localisation,
test-metric defect prediction, semantic topic-level quality prediction, and patch correctness from test
behaviour all predate or parallel parts of P. None of the works listed above, as checked here, tests the
full conjunction in P. That remains “not found” on a scoping review, not proof of novelty.

### 9.8 Candidate contribution statement, with outcome level made explicit

The following is a precise *candidate research/contribution statement*, not an accepted novelty claim:

> Within the observed parent set, this study tests whether a version-level maximum-share summary of a
> prespecified diagnostic failure profile improves prediction of record-level correctness for engineered
> solver variants on the fixed 78-record development bank, beyond the B1 exact-cell baseline
> `(q, Z, k, ℓ)`, using leave-one-parent-out evaluation.

The outcome is `Y_{v,r}`, a record-level binary correctness observation for version `v` on bank record
`r`; `C_D(v)` is a version-level predictor. “Held out” means the parent group is held out in a LOPO fold.
It does **not** mean the 78-record bank is sealed, independently held out, or external confirmation, and
it does not mean the response is a single version-level correctness score. B1 v1.7 expressly describes
the 78-record bank as publicly exposed development data and makes no new-parent population claim.

This wording does not resolve the record-level versus canonical-level measurement alignment described
in `CD_MEASUREMENT_SPEC_2026-11-19.md` §2. The primary exposure basis still needs explicit
reconciliation with the B1 outcome rows before Gate 1. It also does not claim that C_D identifies which
stratum dominates, that the index is new, or that a positive B1 result would establish a mechanism.

**Gate 0 status remains OPEN; P remains UNPROVEN.** The statement fixes the target and inferential
scope, but the broader citation-search protocol and backward/forward citation checks are not yet complete.

### 9.9 Claude follow-up review — additional full-text and identifier adjudication (2026-11-20)

Claude's follow-up review is accepted on the need to state both Sed clustering outcomes. The full text
supports the following narrower account: under agglomerative hierarchical clustering, Sed's §6.2
small-cluster failure density peaks just above 40 % and remains below 50 %; under DBSCAN, Table 7's
Sed V5 row reports 48.23 % cluster count, 1 % average cluster size, 83.3 % failure density, and
F-measure 0.3091. DBSCAN generated almost twice the number of small clusters explored in the
agglomerative analysis. This is a high-density but heavily fragmented result, not evidence that DBSCAN
captures most failures with a small inspection burden. The DBSCAN result is not an exception to the
agglomerative figure; it is a different algorithm and clustering configuration. The NanoXML version 3
case remains a separate exception in which the largest clusters contained most failures. Section 9.2
now records all three facts.

The additional literature checks also distinguish “not checked by Claude in that round” from “not
verified by any reviewer”:

- **Chen et al. (2017):** the article full text is available and was reviewed; the journal issue is
  66(3), pages 806–824. The DOI and article identity are corroborated; the earlier 66(4) issue number
  is corrected.
- **Xiong et al. (2018):** the authors' full paper is available; its first-page ACM reference gives
  DOI `10.1145/3180155.3180182`. The 139-patch result remains study-specific.
- **Tian et al. (2022):** the University of Luxembourg repository provides the publisher postprint and
  bibliographic record for DOI `10.1145/3511096`; the full paper was reviewed. Its similarity-threshold
  and historical-test availability limits remain part of the interpretation.
- **Wu et al. (2004), maximum entropy:** the title, COMPSAC venue, pages and abstract-level result are
  corroborated. Full text was not reviewed in this pass; the entry remains abstract-level.
- **Wu et al. (2004), input-level fault localisation:** the paper identity, title, authors, venue,
  pages and abstract-level result are corroborated, but the DOI strings in third-party records conflict.
  Row 8c therefore withholds the DOI rather than choosing one by plausibility. Publisher/Crossref
  resolution is still required.
- **Dickinson et al. (2001):** the paper and proceedings entry are confirmed. The `503209.503243`
  DOI is supported by the SQJ paper's bibliography and DBLP; the conflicting `503241.503243` secondary
  record is not used.

These checks improve metadata accuracy but do not complete the Gate 0 search protocol. The evidence
matrix still lacks a complete, reproducible database/query/screening log and systematic backward- and
forward-citation checks. **Gate 0 remains OPEN; P remains UNPROVEN.** No Gate 1 freeze is declared by
this amendment.

---

## 10. Dated amendment — 2026-11-21 (B1 identity source; Wu ASE DOI resolved)

**Trigger:** the owner's direct question whether any file identifies B1 v1.7's actual 78
development-bank rows, and the open identifier recorded in §9.7 row 8c and §9.9. Section 9 already
records the round-2 literature additions, the record/canonical exposure arithmetic, the
full-population and fold-level B1 eligibility rules, the Gate 4 relocation of power/MDE, and the
candidate contribution statement. This section does not restate those items. It adds the
identity-source recovery and resolves one DOI. It changes no verdict: Gate 0 remains **OPEN** and
`P` remains **unproven**.

### 10.1 B1's 78 rows: the identity source is recoverable

The owner asked whether any file identifies B1 v1.7's actual 78 development-bank rows. The full record is
`B1_78_ROW_IDENTITY_RECOVERY_2026-11-21.md`; the result is:

- B1 v1.7 itself gives only the symbolic index `r = 1,…,78`; it does not enumerate keys or cite a bank
  path or hash.
- Rev 1.1 §1.4, inherited by Rev 1.4 §1 and carried into B1 v1.7 §1 item 1, defines the outcome
  population as **"78 unique canonical records of the fixed, publicly exposed held-out bank."**
- The B1 decision reconciliation §6.1 pins the artifact (`lc518-bank-run-41591572358-1.zip`, 75,523 B,
  SHA-256 `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`, equal to GitHub artifact
  `13210063805`, run `41591572358`), and §6.5 records that this artifact, containing
  `bank/heldout_bank.json` and its oracle answers, was publicly downloadable. The erratum §3 pins the
  same hash to the same artifact ID.
- The artifact contains 80 raw held-out records, 78 unique canonical identities, and 78 oracle objects
  with an equal key set. The two-row reduction is exactly the two H6 reorder pairs `H057`/`H058`
  (`H6-P01`) and `H059`/`H060` (`H6-P02`). The 78 B1 rows are the **78 canonical identities**, not the
  80 raw rows. Review record §27.2 already records the 80/78 design fact.
- The sorted canonical-ID set hashes to
  `01bb0e4c8edb2c4a0678d1b6c65c4295bdaf59c9baf2436d793f25c740c3cccd`; the sorted
  `(amount, sorted(coins))` payload set hashes to
  `8b67d1f0193d85838a98486ae4fbf7ef17d948b1cca4abdfc4c0180ae61e48fa`. The authoritative list is the
  pinned JSON, not a new manifest.

**What this is.** A definitional chain, not a `78 = 78` cardinality inference. The evidence is B1's own
definition of its outcome population plus the contemporaneous identification of the bank; the matching
count is a consequence.

**What this is not.** It is not a B1 v1.7 citation: v1.7's change table item 7 deliberately removed the
138/144/6 erratum counts, so the chain runs through Rev 1.1 §1.4 and the separate B1 decision record. It
is not a historical enumeration order: B1 fixes no order, and the likelihood's `ω_r` is a free record
effect, so any order is a reporting convention. It is not a confirmatory target: the bank remains
development data, publicly exposed, never sealed, and the consent/custody gates are untouched. It also
does not adopt a raw-pair-to-canonical outcome aggregation rule: the artifact supplies one oracle answer
per `canonical_id`, but B1 v1.7 does not fix how two raw execution statuses collapse to one `Y`, which
review record §27.3–§27.4 already records as an open Gate 1 measurement gap.

**Disposition.** The identity source is **RECOVERED**; the B1 identity gate moves from
**source-missing** to **source-recovered / adjudication pending**. The warning against substituting H80
by cardinality stands, and this record does not close the gate unilaterally. The two lawful paths are:
(a) the owner/GPT accepts the documentary chain and records the path/hash in a dated B1 addendum; or
(b) a contemporaneous B1-issued manifest is supplied, or B1 design is reopened. No third path infers
identity from equal counts.

### 10.2 Wu et al. (2004), ASE: the withheld DOI is resolved

Section 9.7 row 8c and §9.9 withhold the DOI for "A Statistical Model to Locate Faults at Input Level"
(ASE 2004, pp. 274–277) because third-party records disagreed. The primary registration record resolves
it:

- Crossref `10.1109/ASE.2004.1342745` returns the matching title, authors (Wu Ji, Jia Xiao-xia, Liu
  Chang, Yang Hai-yan, Liu Chao, Jin Mao-zhong), proceedings, pages 274–277, publisher IEEE.
- The DOI handle resolves to `http://ieeexplore.ieee.org/document/1342745/`.
- The competing strings do not identify this paper: `10.1109/ASE.2004.1342763` is a different ASE 2004
  paper (Choi & Heimdahl, "Combination model checking", pp. 354–357); `10.1109/ASE.2004.10008` and
  `10.1109/ASE.2004.7` do not resolve.

Row 8c therefore carries `10.1109/ASE.2004.1342745`. Section 9.7 is not rewritten; this section is the
controlling resolution. The verification level remains a bibliographic record plus DOI handle; the full
text was not reviewed in this pass, and the paper is still not evidence for `P`.

### 10.3 Effect on the record

- **Added:** `B1_78_ROW_IDENTITY_RECOVERY_2026-11-21.md`, the standalone provenance record.
- **Resolved:** the Wu et al. (2004) ASE DOI withheld in §9.7/§9.9.
- **Unchanged:** §1–§9, including the exposure-basis arithmetic, the two-level B1 eligibility rule, the
  Gate 4 relocation of power/MDE, and the candidate contribution statement.
- **Gate 0 remains OPEN. `P` remains unproven.** No novelty claim is licensed.
- **B1 v1.7 is unchanged and is not amended.** The identity gate is source-recovered, not closed.
  *(Superseded for current status by §10.4; retained as the 2026-11-21 position.)*
- **Not done:** no solver construction, execution, fitting, sampling, calibration, or outcome model. The
  only bank access was read-only identity inspection of the held-out artifact; the project pause remains
  in force.


### 10.4 Subsequent owner adjudication (2026-11-22)

On 2026-11-22, the repository owner accepted the B1 78-record documentary identity chain. The dated decision is recorded in `B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md`; the detailed source reconstruction is `B1_78_ROW_IDENTITY_RECOVERY_2026-11-21.md`, with its byte-level v3 audit and derived manifests listed in the review-bundle README.

Accordingly, §10.1's **source recovered / adjudication pending** disposition is a historical snapshot as of 2026-11-21 and is superseded for current identity status by **source-recovered / owner-accepted**. This acceptance is limited to identity and documentary attribution. Historical row numbering, H6 primary-outcome aggregation, unresolved-status handling, and outcome coding remain undecided. B1 execution remains unauthorized; Gate 0 remains OPEN; (P) remains unproven; no novelty or predictive claim is licensed. B1 v1.7 remains unchanged.

---

## 11. Dated amendment — 2026-11-22 (Gate 0 search executed)

**Trigger:** the owner's instruction to run the literature search rather than request another approval cycle. The full log, counts, query expressions, candidate decisions, citation chasing, and limits are in `GATE0_LITERATURE_SEARCH_2026-11-22.md`. This section records only the result and the two bibliographic additions. It changes no verdict: Gate 0 remains **OPEN** and `P` remains **unproven**.

### 11.1 Executed search

Eighteen informative OpenAlex queries and two discarded queries were run on 2026-11-22, with three forward and two backward citation chases; approximately 431 titles were screened and abstracts were read for seven candidates. Deviations from the planned twelve-query protocol — chat web search unavailable, index syntax, no date filter, no full text — are recorded in the search record §2.

**Result:** no direct match and no partial match to `P`. Four adjacent-close works share either the prediction target or the concentration observation, never the conjunction: Almaghairbe & Roper (2017, 2019), the 2026 LLM trace-outcome study, BASHIRI (2025), and *Striving for Failure* (2015). The corpus contains a mature concentration observation, a mature clustering-for-debugging literature, and a mature per-input outcome-prediction literature; it does not contain a prespecified-partition maximum share evaluated against an exact-cell baseline with parents held out.

### 11.2 Rows 20–21 — Systemic Flakiness, two distinct records

| Register ID | Work and DOI | What it establishes | What it pre-empts | What it does not pre-empt | Verification level |
|---|---|---|---|---|---|
| 20 | Parry, Kapfhammer, Hilton & McMinn (2025), “Systemic Flakiness: An Empirical Analysis of Co-Occurring Flaky Test Failures,” EASE 2025, pp. 476–487. [10.1145/3756681.3756945](https://doi.org/10.1145/3756681.3756945) | Flaky tests occur in clusters with co-occurring failures sharing root causes ("systemic flakiness"); 10,000 runs, 24 Java projects, 810 flaky tests | Failure co-occurrence as an object of study; clustering of failures by shared cause | A concentration statistic, per-record correctness prediction, an exact-cell baseline, or parent-grouped evaluation | Abstract read; full text not read |
| 21 | Parry, Kapfhammer, Hilton & McMinn (2026), “Systemic Flakiness: A Study of Flaky Test Failure Co-Occurrence Using Java and Python Projects,” *IEEE Transactions on Software Engineering*, pp. 1–21. [10.1109/TSE.2026.3750452](https://doi.org/10.1109/TSE.2026.3750452) | Extended study of flaky-test failure co-occurrence; the title extends the scope from the EASE record's Java-only corpus to Java and Python projects | Failure co-occurrence as an object of study, extended beyond the EASE corpus | The response appears to be co-occurrence structure, not individual input correctness; no concentration covariate; no parent grouping. **Method and results unverified** — Crossref deposits no abstract and the full text is inaccessible, so only title, authorship, venue and early-access status are citable | Crossref record only (created 2026-11-03; early access, pp. 1–21, no volume or issue assigned; Xplore 11773385); abstract unavailable; full text not read |

These are two publications of one research line, not a preprint and its version of record. Both should be cited separately where the line matters.

**Correction.** The 2026-11-22 statement that no TSE 2026 version exists is wrong. `10.1109/TSE.2026.3750452` resolves in Crossref and OpenAlex to the IEEE TSE article above. The caution that generated the statement — do not cite an unverified DOI — was right in principle and is now satisfied by the publisher record.

### 11.3 Effect on the record

- **Added:** `GATE0_LITERATURE_SEARCH_2026-11-22.md`; rows 20–21 above.
- **Unchanged:** §8 verdict table, the exposure-basis arithmetic, the two-level B1 eligibility rule, the Gate 4 relocation of power/MDE, and the candidate contribution statement.
- **Gate 0 remains OPEN; `P` remains unproven.** The search is a scoping deliverable with stated limits, not a systematic review and not a novelty finding.
- **Not done:** no solver construction, execution, fitting, sampling, or bank access.

### 11.4 Consequence for the programme

The literature is no longer the binding constraint. The defensible contribution object is the **design** — a prespecified-partition dominance covariate tested against an exact-cell, failure-count-conditioned baseline under parent-held-out evaluation — not the index (Berger–Parker 1970) and not the phenomenon (Almaghairbe 2015/2017). The next decisions are, in order: accept or reject the search record; state that contribution explicitly; authorize the design-only support census before any solver budget; and treat a null B1 result as the prior-consistent outcome rather than a failure of execution.

---

## 12. Dated amendment — 2026-11-22 (search record accepted; pause retained)

### 12.1 The decision

On 2026-11-22 the owner accepted `GATE0_LITERATURE_SEARCH_2026-11-22.md` **as the Gate 0 scoping deliverable**, and declined, at this point, to authorise anything beyond that acceptance. The recorded decision is in reviewer-ledger §30.

The decision is an owner-authored conversational instruction in the project session on 2026-11-22. Like the identity acceptance in §10.4 and its addendum, it is not a repository artifact, and a reviewer reading only this repository cannot independently authenticate it from the repository alone. It is recorded, not presented as corroboration.

### 12.2 What acceptance covers

- The query log in search record §3, including the two discarded expressions and the reason each was discarded.
- The protocol deviations in §2 — substituted instrument, 18 expressions instead of 12, no date filter, title-level screening, no full text, single database.
- The candidate decisions in §4, including the distinction between adjacent-close and adjacent, and the exclusions with their reasons.
- The citation-chasing results in §5, including the failure to chase the IEEE TSE record backward.
- The limits in §8 and the verdict in §9.

Acceptance means these are now the repository's account of the Gate 0 search. It does not mean the search is complete, exhaustive, or a systematic review, and §8's limits stand unmodified.

### 12.3 What acceptance does not cover, and does not authorise

1. **It is not a novelty finding.** `P` remains unproven. A documented non-finding on one index is not a priority claim, and §8's verdict table is unchanged.
2. **It is not Gate 0 closure.** Gate 0 closes when a documented scoping review supports closure *and* the contribution decision is made. The first condition is now recorded; the second is not. Gate 0 remains **OPEN**.
3. **It does not authorise the support census.** The design-only census on the LC518 diagnostic tables remains unrequested and forbidden. The project pause remains in force in full.
4. **It does not authorise anything downstream.** No solver construction, execution, diagnostic collection, outcome labelling, `Y` matrix, sampling, fitting, or predictive analysis. Were the census later authorised, it would use no outcomes and would still not be an execution GO.
5. **It does not decide the contribution object.** §11.4 states the design as the defensible object; that statement is a recommendation, not an adopted position, until it is separately decided.
6. **It does not touch measurement.** H6 primary aggregation, unresolved-status handling, outcome coding, and historical row numbering remain open exactly as §10.4 left them.

### 12.4 Effect on the record

- **Added:** this section; reviewer-ledger §30.
- **Changed:** none of §1–§11. The search record and its index entry are unchanged.
- **Unchanged:** Gate 0 **OPEN**; `P` **unproven**; B1 execution **not authorised**; B1 v1.7 **unchanged**; pause **in force**.

### 12.5 Consequence

No action beyond this acceptance is authorised. The next step, whenever the owner chooses to take it, is the contribution decision in §11.4 — whether the programme adopts the design as the contribution object. That is the second condition for Gate 0 closure and the only remaining item that requires no data access. The census remains the first Gate 1 action and remains blocked until separately authorised.

---

## 13. Dated amendment — 2026-11-22 (review round: GPT and Claude)

**Trigger:** GPT's Gate 0 review and Claude's response to it, both dated 2026-11-22. They converge on four corrections and divide on one question of gate structure. This section applies the corrections, resolves the structural question against the repository's own frozen gate definitions, and reduces the open work to one decision. It changes no verdict: Gate 0 remains **OPEN**, `P` remains **unproven**, nothing is authorised.

### 13.1 Corrections both reviews are right about, now applied

**a. The screening count.** GPT is correct and exact: 431 is the sum of the per-query first pages (17 × 25 + 6), not a deduplicated count. The search record's §2, §3 and §8 now say so, and §3 states the arithmetic explicitly. The unique union across the 18 result pages was never computed or stored and is not claimed. Claude's accompanying point also stands and is now stated: only the first page of each expression was screened, so counts of 3,178, 14,484 and 20,362 were examined to 25 records each. The supported sentence is unchanged but now bounded in the record itself:

> No direct or partial match was identified among the records screened in this OpenAlex pass.

**b. The TSE record's scope.** Claude is right that the indexed content describing 24 Java projects cannot be the TSE article's scope. Crossref resolves the two records separately: the EASE 2025 paper (`10.1145/3756681.3756945`, pp. 476–487, published 2025-06-17) is the Java-only study, and the TSE title explicitly extends to "Java and Python Projects" (`10.1109/TSE.2026.3750452`, early access, pp. 1–21, Crossref record created 2026-11-03, no volume or issue assigned). The apparent mismatch is therefore between two publications, not inside one. But Claude's underlying caution is accepted and now governs the record: the TSE article's method, results, and project count are **unverified**, because Crossref deposits no abstract and the full text is inaccessible. Only its title, authorship, venue and early-access status are citable, and register row 21 now says so.

**c. The acceptance's authentication limit.** Claude cannot find the owner's acceptance in the transcript it holds. The decision was made through an explicit owner selection among stated options in the project session on 2026-11-22, and §§12.1 and 30.1 already record it as conversational rather than documentary. That limit is now stated in the stronger form Claude asks for: a reader who does not hold that session cannot authenticate the act, and nothing in this repository supplies an independent record of it. If the owner wants the acceptance to be citable without that caveat, a one-line confirmation in the owner's own words, added as a dated note to `B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md` or a new file, would do it. This register does not manufacture one.

**d. Disclosure is not endorsement of the deviation.** Both reviewers accept the search with its deviations disclosed. That is the correct disposition and it is already §12.2. Disclosure does not upgrade a scoping pass into a systematic review.

### 13.2 The structural question: does Gate 0 need splitting?

GPT proposes two decisions — **A**, close Gate 0 on scoping plus contribution; **B**, a new feasibility gate holding support, estimability, MDE and power. Claude proposes that the census precede any adoption, on the ground that a null is uninformative without established power.

The repository already contains the separation GPT is proposing, and it is worth naming precisely because both reviews write as though it does not.

| Function | Where it already sits | Source |
|---|---|---|
| Is the proposition already tested? | Gate 0 | `FUNDAMENTAL_GOAL` §3 |
| Is the statistic presented as novel? | Gate 0 | `FUNDAMENTAL_GOAL` §3 |
| Is there a precise contribution paragraph, a shown difference from the closest prior work, and a fixed inferential scope? | Gate 0 | §9.5, §9.8 |
| Can the frozen support conditions be satisfied, and is there a scoreable LOPO fold? | Gate 1, first action: the design-only support census | §9.3 |
| MDE, power, operating characteristics of the frozen pipeline | Gate 4 | §9.4 |

So GPT's Decision B is **Gate 1 plus Gate 4**, not a missing gate. Creating a third gate to hold them would duplicate the structure and leave the frozen goal document contradicted. No such amendment is made here, and none should be made without the owner explicitly changing `FUNDAMENTAL_GOAL` §3.

What GPT is right about is narrower and more useful: **Gate 0 is being asked to wait for feasibility, which is not its question.** Under §9.5 and §9.8, Gate 0 needs the contribution paragraph adopted; it does not need the census. Claude's objection does not overturn that, because Claude is making a claim about *interpretation of a future null*, not about *whether to ask the question*. Those are separable, and the separation is the substance of the resolution below.

### 13.3 Claude's constraint, kept

Claude's power argument is accepted as a constraint on what a null would mean, and it is not softened:

- The bank's diagnostic exposure is 64 records on the record basis and 60 on the canonical basis, with per-stratum capacity `R = (8,8,8,8,8,4,8,8)` canonically. At most eight distinct `C_D` values exist at any fixed `k` (§9.3), so the covariate is coarse by construction, and Claude's "8 strata of 8 records" is the record-basis reading of the same fact.
- The one executed world retained about 0.25 % of the full vector's gain with an interval spanning zero (§3.4). That is a warning about the likely result, not a refutation.
- Therefore a null is **not automatically informative**. It is informative only if the design could have detected a stated effect. Establishing that is Gate 1 (support) and Gate 4 (power), in that order.

The consequence for the contribution decision is a reporting rule, not a delay: the adopted statement must pre-commit that an observed null will be reported as **inconclusive** unless the feasibility work establishes an MDE and the design's power against it. A null obtained without that is a support failure, not a scientific finding. This is how GPT's "a null is not automatically informative" and Claude's "a null is only legitimate with power" become the same sentence instead of two positions.

### 13.4 The one remaining Gate 0 item

Under §9.5, Gate 0 closes when the contribution is stated in one precise paragraph, its difference from the closest prior work is shown, its inferential scope is fixed, and no priority claim rests on the absence of a search hit. Four of the five are done. The missing item is adoption of the paragraph. The exact text proposed for adoption, with the reporting rule of §13.3 attached, is:

> This study tests whether a version-level maximum-share summary of a prespecified eight-stratum diagnostic failure profile adds incremental predictive information about record-level correctness for engineered solver variants on the fixed, publicly exposed 78-record B1 development bank, beyond the exact-cell baseline `(q, Z, k, ℓ)`, under leave-one-parent-out evaluation with the parent as the independent unit.
>
> The index is Berger–Parker dominance (1970) and is not claimed as new. Failure concentration as a phenomenon is established (Almaghairbe & Roper 2015, 2017) and is not claimed as new. Execution-derived signals predicting correctness are established (register §4 rows 9–14) and are not claimed as new. The contribution claimed is the controlled, null-capable test of incremental value in this design.
>
> No claim is made about a new parent population, about information superiority over the full failure vector, or about identifying which stratum dominates. A null result will be reported as inconclusive unless Gate 1 support and Gate 4 power establish that the design could have detected a stated effect; a null obtained without that is a support failure.

Adoption of this paragraph would satisfy the last Gate 0 condition. It would not authorise the census, any measurement work, or any solver activity.

### 13.5 Status

- **Gate 0: OPEN.** One item remains, and it needs no data access.
- **`P`: unproven.** No novelty claim. The supported sentence remains "no direct or partial match among the records screened in this OpenAlex pass".
- **Census: not authorised.** Pause in force.
- **Operational items: open.** H6 presentation and aggregation, unresolved-status handling, outcome coding, historical row numbering. None can be settled by adopting a contribution statement, and none is settled here.
- **Records corrected:** search record §§2, 3, 4, 8; register row 21.

---

## 14. Owner adopts the contribution statement; Gate 0 closed (2026-11-22)

### 14.1 The decision and its provenance

On 2026-11-22, the owner explicitly confirmed adoption of the exact contribution paragraph in §13.4 as written. The confirmation was given directly in this project conversation in response to the two decisions presented: adopt §13.4, and leave the separate search-record acceptance authentication caveat unchanged.

This is a direct owner decision in the current conversation. It is not inferred from DeepSeek's report, and it does not authenticate the earlier search-record acceptance beyond the caveat already stated in §§12.1 and 13.1(c).

### 14.2 Adopted contribution statement

The owner adopts the complete three-paragraph statement in §13.4 without textual modification, including its null-interpretation rule:

> This study tests whether a version-level maximum-share summary of a prespecified eight-stratum diagnostic failure profile adds incremental predictive information about record-level correctness for engineered solver variants on the fixed, publicly exposed 78-record B1 development bank, beyond the exact-cell baseline `(q, Z, k, ℓ)`, under leave-one-parent-out evaluation with the parent as the independent unit.
>
> The index is Berger–Parker dominance (1970) and is not claimed as new. Failure concentration as a phenomenon is established (Almaghairbe & Roper 2015, 2017) and is not claimed as new. Execution-derived signals predicting correctness are established (register §4 rows 9–14) and are not claimed as new. The contribution claimed is the controlled, null-capable test of incremental value in this design.
>
> No claim is made about a new parent population, about information superiority over the full failure vector, or about identifying which stratum dominates. A null result will be reported as inconclusive unless Gate 1 support and Gate 4 power establish that the design could have detected a stated effect; a null obtained without that is a support failure.

### 14.3 Gate 0 disposition

**Gate 0: CLOSED, for position and contribution definition only.**

The documented scoping review was accepted in §12, the closest-work comparison and bounded search result are recorded in §§11–13, the inferential scope is fixed in the adopted statement, and the owner has now adopted that statement. The closure does not rely on absence of a search hit as proof of novelty.

The scientific proposition `P` remains **UNPROVEN**. The supported literature statement remains: *no direct or partial match was identified among the records screened in this OpenAlex pass.* This is not a novelty finding, a priority claim, or evidence that the proposed effect exists.

### 14.4 Scope and non-authorisations

This decision adopts the research question as the programme's intended contribution. It does not make the statement operationally executable and does not alter any frozen protocol.

- Gate 1 remains **NOT STARTED**. Its first action, the design-only support census, remains unauthorised and blocked by the project pause.
- Gate 4 remains **NOT STARTED**. MDE, power, and operating characteristics remain unestablished.
- A null without Gate 1 support and Gate 4 power remains **inconclusive**, not evidence against the hypothesis.
- H6 presentation/aggregation, unresolved-status handling, outcome coding, and historical row numbering remain open.
- B1 v1.7 is unchanged. No solver construction, execution, diagnostic collection, outcome labelling, `Y` matrix construction, sampling, fitting, or predictive analysis is authorised.
- The project pause remains in force. Any Gate 1 work requires a separate explicit reopening and authorization.

### 14.5 Record effect

This section supersedes only the **OPEN** status in §13.5 and the earlier statements that contribution adoption remained outstanding. Those statements are retained as dated history. The search limits, literature verdict, and all scientific non-claims remain unchanged.

---

## 15. Owner clarifies the engineered-solver study population (2026-11-22)

### 15.1 Owner decision

The owner has now explicitly settled the population terminology and intended study direction: the research is to be framed as a study of **engineered solvers**. The owner rejects “natural solver” as a distinct or useful population category for this project: every solver has an authoring, design, construction, or transformation history, including human-authored implementations.

This is a direct owner clarification in the 2026-11-22 project conversation. It resolves the earlier disagreement about whether the current research target should be described as “naturally generated” or “engineered.” It does not rely on a reviewer’s recollection of the 2026-10-31 discussion.

### 15.2 Operational meaning and inferential scope

For the current B1 study, “engineered solvers” means **solver variants deliberately constructed, modified, parameterized, or otherwise produced under a declared study process, nested within selected real parent solver implementations**. Parent implementations are the source and grouping units; the tested study units are the engineered variants.

The adopted contribution in §14.2 already names engineered solver variants. This section clarifies that wording; it does not replace the adopted contribution or change its estimand.

The inferential scope remains conditional on the selected and observed parent implementations and their engineered variants. It does not establish a result for all solvers, all human-authored implementations, all model-produced implementations, or a superpopulation of newly developed parents. It does not establish generalization to an independently sampled parent population.

“Natural solver” and “natural solver population” must not be used as the current target-population label in new scientific claims or plans. Earlier documents using that terminology remain part of the historical record. The earlier feasibility exercises remain evidence about the particular sampling and generation procedures they tested; they are not retroactively reclassified as tests of an ontologically distinct “natural” class. The 2026-10-30/31 doctoral blueprint was explicitly an unapproved reconstructed draft, not an owner-approved replacement target.

### 15.3 Parent origin, lineage, and provenance

Rejecting a natural/engineered dichotomy does **not** remove the need to document parent provenance. Before any future parent acquisition or selection, the record must identify, as applicable:

- source or repository and immutable source identity;
- authorship or originating process, including any human, model-assisted, model-generated, or other contribution that is known;
- lineage, edits, repairs, transformations, and derivation relationships;
- the outcome-blind selection procedure and exclusions;
- parent-family assignment, source hashes, and reproducible identity mapping; and
- relevant permission, license, and custody/consent status.

If a parent is specifically represented as an output of a model-generation event, the six-point model-generation provenance gate in reviews/CLAUDE_FULL_REPO_CHALLENGE_ADJUDICATION_2026-11-21.md §6 applies before that origin claim is used: independently verifiable session/request evidence; exact model/version and generation settings; retained raw outputs in generation order; body/file hashes and mappings; an independently recomputable event-to-file manifest; and a pre-freeze gate that fails closed when evidence is missing. Hashes establish byte identity, not model origin.

These are documentation and eligibility prerequisites for any future parent-acquisition decision. They do not authorize acquisition, selection, generation, mutation, or solver execution.

### 15.4 Exact-cell notation clarification

In the adopted expression (q, Z, k, ℓ), the symbols are aliases for the frozen Rev 11 support-cell coordinates:

- q ≡ m: mutation-mechanism / mutation-operator identity;
- Z ≡ z: parent algorithm family;
- k ≡ k_fail: number of definite diagnostic failures; and
- ℓ ≡ k_unresolved: number of unresolved diagnostic outcomes.

The underlying frozen cell remains (m, z, k_fail, k_unresolved) (Rev 11, line 226). This is a notation clarification only; it does not alter the cell, the conditioning variables, or B1 v1.7.

### 15.5 Measurement and execution boundaries retained

This population decision does not settle the remaining measurement details:

1. **Diagnostic exposure.** Rev 11 defines the diagnostic counting unit as a bank record, not a unique mathematical input, and specifies eight records per stratum (N = 64, R_j = 8). That remains the protocol-prescribed record-level C_D unless changed by an explicit protocol amendment. A canonical-level calculation (N = 60, with four canonical records in stratum 6) is a different statistic and, if reported, must be recomputed from canonical failure counts and labelled as a sensitivity. It must not be averaged with, or silently substituted for, the record-level statistic. The separate measurement audit's warning about alignment between diagnostic exposure and canonical outcome rows remains a documentation reconciliation item; it does not authorize changing the frozen Rev 11 counting unit.
2. **H6 outcomes.** The two H6 raw reorder pairs among the 80 held-out presentations, which collapse to two canonical identities within the 78-record bank, still lack an adopted raw-pair-to-canonical correctness rule. No aggregation rule is selected here. This is required before constructing or interpreting the canonical Y_{v,r} outcome matrix.
3. **Census distinction.** A strictly design-only support census uses diagnostic predictors and exact-cell structure, not the held-out correctness outcomes. Therefore the unresolved H6 outcome rule is a blocker for the outcome matrix and predictive analysis, but is not itself an input to an outcome-free support census. The census remains blocked by the project pause and requires its own explicit authorization.
4. **Other open measurement matters.** Unresolved-status handling, the final outcome coding rule, and historical B1 row numbering remain open as recorded in the identity and measurement records.

### 15.6 Current gate status and non-authorisations

- **Gate 0 remains CLOSED for position and contribution definition only.** This owner clarification resolves the current population terminology; it does not establish novelty, priority, predictive value, or operational readiness. P remains **UNPROVEN**.
- **Gate 1 remains NOT STARTED.** The design-only support census remains unauthorised. The project pause remains in force.
- **Gate 4 remains NOT STARTED.** MDE, power, and operating characteristics remain unestablished.
- B1 v1.7 and the frozen Rev 11 definitions are unchanged. No parent acquisition, solver construction, generation, mutation allocation, solver execution, diagnostic collection, outcome labelling, Y-matrix construction, fitting, or predictive analysis is authorised by this clarification.

This section supersedes only the disputed current use of “natural solver population” as the research target. It preserves the earlier documents as historical records and does not silently rewrite or retroactively reinterpret their results.

---

## 16. Dated amendment — 2026-11-22 (strategic reset: the blueprint is not the experiment)

**Provenance.** This records a strategic message forwarded from the owner, written by GPT. It is reported, not verified from this branch: PR #9 and revision 0.6 live on other lines of work, and this branch contains no artifact against which their state could be checked.

### 16.1 The distinction accepted

- **PR #9 is a GitHub review workspace. Revision 0.6 is a draft specification** for counting diagnostic support in a future dataset; its JSON Schema describes the structure of records a census would inspect.
- **A PASS on that specification means the agreed blueprint corrections are sound.** It is not a scientific result, not a census result, and not evidence about `P`.
- The programme has been checking the blueprint rather than building the machine, and review has become the dominant activity rather than a means to an experiment.

This register's §§11–15 and the ledger's §§29–33 belong to that paperwork layer. They settled positioning, identity, population scope and gate status; they did not advance any scientific milestone.

### 16.2 Where the scientific presentation already lives

This section deliberately does **not** duplicate the status tables. The scientific question, why it is difficult, population/measurement boundaries, gate status, Gate 1 preflight and the null rule are already presented in the repository root `README.md` ("LC518: Diagnostic failure concentration and solver correctness", 2026-11-22), with the decisions in register §§14–15, ledger §§32–33 and goal §§18–19. That README records Gate 1 preflight as **BLOCKED / NOT ASSESSABLE** until a per-variant eight-stratum diagnostic manifest exists, and limits the owner's instruction to a design-only census once that manifest exists.

### 16.3 Working-approach decisions recorded from the message

1. **Stop expanding review paperwork.** Keep revision 0.6 as reviewed; no further cosmetic revisions from this line of work.
2. **Make implementation serve the experiment.** A semantic validator is justified only insofar as it gets real diagnostic records safely and reproducibly into the census; engineering detached from that objective is not.
3. **Measure progress in scientific outputs.** The milestones are, in order: parent roster; runnable variants; diagnostic bank; diagnostic measurements; validated manifest; census results; held-out predictive results. PRs, review comments, schema revisions and this register's sections are supporting evidence only, not milestones.

This amendment is itself paperwork and claims no scientific progress.

### 16.4 Authorisation boundary

This section creates **no** authorisation. It neither grants nor narrows the limited Gate 1 preflight/census scope recorded in the root README. Parent acquisition, mutation allocation, solver construction, diagnostic execution to create the missing manifest, outcome collection and predictive analysis still require their own explicit GO. `P` remains unproven; B1 v1.7 unchanged; the pause remains in force outside the recorded preflight scope.

### 16.5 Effect

No verdict in §§1–15 changes. Gate 0 remains CLOSED for position and contribution only; Gate 1 not started; `P` unproven. No bank access, solver work, diagnostics, census, fitting or scientific output was produced in this round.

---

## 17. Dated amendment — 2026-11-22 (intake prototype held for independent review)

**Trigger.** GPT's review of commit `0060e7b413b709f7ff66f7d9f89780fa2b1a1703` on branch
`work/b1-census-intake-validator-2026-11-22`, and its instruction to preserve the work but not merge
it, not run it on real records, and not implement a correction before Claude's independent agreement.

### 17.1 What was reviewed

The commit adds `census-intake/` (validator, descriptive JSON Schema, 18 synthetic tests,
documentation) and one root `README.md` index entry. It is separate from PR #9 and revision 0.6 and
has not been merged. The reported 18/18 synthetic result is evidence about constructed fixtures only;
GPT did not reproduce it, and a local re-run during review preparation observed 18/18 passing.

### 17.2 Four findings, independently checked

All four were confirmed against the artifact by local fact-check:

1. **Prohibited basis admitted as primary.** The validator accepts `canonical` (60 records, four in
   D6) as well as `record`, with a passing test for canonical admission. §15.5 fixes record-level as
   the protocol-prescribed primary statistic and canonical as a recomputed sensitivity, never a
   silent substitute.
2. **Aggregates validated, individual results not.** The tool checks supplied `f`/`u` vectors and ID
   arrays, not 64 per-result terminal statuses (`DEFINITE_PASS` / `DEFINITE_FAILURE` / `UNRESOLVED`).
   It cannot establish that the counts were derived from the records.
3. **Provenance is syntactic.** `source_digest` is checked as a hex string only; no bank or artifact
   is read, and record-ID membership in the frozen diagnostic bank is not established.
4. **Two input-handling defects.** An empty JSON array is admitted with CLI exit 0; a non-string
   `exposure_basis` (array/object) raises an uncaught `TypeError` at `validate_records.py:146`.

### 17.3 Disposition

The artifact is described accurately as a **synthetic-tested summary-record intake prototype**, not
the B1 semantic validator specified in revision 0.6. The review packet at
`census-intake/REVIEW_PACKET_FOR_CLAUDE_2026-11-22.md` (on the work branch) puts the four findings,
reproductions and a required PASS / NOT PASS to Claude. **Claude's verdict is outstanding.**

Until that verdict: preserve the branch; do not merge; do not run on real records; implement no
correction. The local agent complied: no validator code was changed after the findings arrived; only
the review packet and a review-status note were added in commit `639ee3f`.

### 17.4 Scientific status unchanged

No LC518 diagnostic measurement was produced. Gate 1 preflight remains **BLOCKED / NOT ASSESSABLE**
for want of a per-variant eight-stratum diagnostic manifest. No parent roster, variants, bank, runs,
manifest, census or predictive result exists. `P` remains unproven; Gate 0 closed for position and
contribution only; B1 v1.7 unchanged; pause in force outside the recorded preflight scope. No
verdict in §§1–16 changes.

---

## 18. Dated amendment — 2026-11-22 (v0.2 intake successor implemented; review pending)

**Trigger.** GPT accepted Claude's NOT PASS on prototype `0060e7b` and the two-reviewer correction
scope, and authorized implementation of that scope within Step 1.

### 18.1 What was done

A successor was implemented on the separate, unmerged branch
`work/b1-census-intake-validator-v02-2026-11-22` (commit `fd0b34b`). Prototype `0060e7b` is unchanged
in history; no history was rewritten and nothing was merged into master. The v0.2 validator validates
individual `diagnostic_record_results` under `measurement_basis = record_level_64`, derives f/u/p and
`C_D` from terminal statuses, treats supplied aggregates as non-authoritative consistency checks,
enforces identical record-ID sets across complete `VALID` variants, and emits the exact label
`SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED`. The zero-failure state is `NO OBSERVED FAILURES`,
never a numeric zero. Twenty-five synthetic tests pass. The earlier review packet's 4(b) reproduction
was corrected by an **appendix** (§6), leaving the original review intact.

Details and hashes: `census-intake/CORRECTION_RECORD_2026-11-22.md`.

### 18.2 Boundaries explicitly not decided

Claude's independent review of the successor has **not** been rendered; the synthetic suite is not that
review. No bank membership, artifact provenance or source integrity was verified. No real manifest was
validated. No parents, solvers, diagnostics, census, fitting or predictive analysis occurred.

The question whether an earlier conditional census authorization remains operative, or was intended to
be revoked, is **left unanswered** by this amendment and by the correction scope. Neither interpretation
is written into this record.

### 18.3 Effect

No verdict in §§1–17 changes. Gate 0 closed for position and contribution only; Gate 1 preflight
remains **BLOCKED / NOT ASSESSABLE**; `P` unproven; B1 v1.7 unchanged; pause in force outside the
recorded preflight scope. No scientific output was produced.


---

## 19. Dated amendment — 2026-11-23 (GPT-owned v0.3 B1 intake rewrite; Claude review pending)

### 19.1 Trigger and authorship

Following the v0.2 review, GPT's static inspection and Claude's independent probes identified further defects. Claude gave written agreement to GPT's proposed repair sequence and six conditions before implementation on 2026-11-23. That agreement covered the implementation approach only; it was not a code review or PASS.

HY4 authored the historical prototype commit `0060e7b` and v0.2 successor commit `fd0b34b`. Both commits remain unchanged. GPT inspected and rewrote the implementation on the separate branch `gpt/b1-v06-intake-repair-2026-11-23`. The correction record explicitly attributes previous work to HY4 and the v0.3 rewrite to GPT. No GitHub action is attributed to Claude.

### 19.2 Additional defects found in v0.2

The v0.2 validator did not enforce the full revision 0.6 manifest envelope or nested unknown-property rules. It could admit an unknown root field such as `correctness_outcomes`, ignore prohibited consultation flags set to true, and admit present-but-null digest/evidence fields. It also generated a `[q,Z,0,0]` cell for non-measured statuses including INVALID, EXCLUDED_BEFORE_DIAGNOSTICS and EXPECTED_NOT_RUN. Those statuses do not have diagnostic measurements; treating an empty result set as zero failures creates false measurements.

### 19.3 GPT v0.3 implementation

The v0.3 successor is on branch `gpt/b1-v06-intake-repair-2026-11-23`, whose code work is three commits ahead of the HY4 v0.2 parent:

- `da1f41fc8a902be01b42257e028f8ad974952905`: GPT v0.3 schema-exact rewrite.
- `9caf82819887975e2f03951af58e87f256a369a6`: explicit source-schema identity assertion in the tests and a corrected local-test limitation record.
- `b31c14c4b6f3e99fffc3a72f2609e6bda53927f1`: successor-specific Claude review packet.

Draft PR #10 is open at https://github.com/foued2/failure-concentration-study/pull/10. Its base is the HY4 v0.2 predecessor branch so that the review diff is limited to the GPT successor commits. It is not a merge to that branch or to master; no merge has occurred. Master remains unchanged.

The implementation packages the exact reviewed B1 schema draft 0.6 from commit `f19e2a0ba09f2161f290558da5f61abc9d3ab52a`, source path `reviews/analytical-validity-2026-11-18/b1-v17-census-review-2026-11-22/B1_V1_7_CENSUS_MANIFEST_SCHEMA_DRAFT_0_6.json`, Git blob SHA-1 `0f2865e606fa61400184c09abd01601497637a6b`. It pins this source blob in the code and rejects a different packaged schema. The schema requires 17 top-level fields, prohibits additional properties at the root and variant level, and does not define `f`, `u` or `p` as manifest fields. Those optional assertions have therefore been moved to a separate sidecar.

The aggregate sidecar schema is separately pinned by Git blob SHA-1 `72fc746c3d6129534aeb2fdbcd866842865f98c7`. Sidecar inputs bind to the SHA-256 of the exact manifest bytes and to the sidecar schema blob identity. Mismatches are rejected with `AGGREGATE_MISMATCH`; malformed vectors with `MALFORMED_AGGREGATE`. The sidecar cannot alter the manifest's independent validation decision.

The implemented C_D formula is sourced from `CD_MEASUREMENT_SPEC_2026-11-19.md` §1, which quotes Rev 11 lines 216–221, and the reporting definition in §5. It is not inferred from the predecessor's code. Unresolved outcomes are excluded from the C_D numerator and denominator.

For VALID variants, the tool derives the complete f/u/p vectors, k values, exact cell and rational C_D from the 64 individual result records. A valid zero-failure variant is labelled `NO OBSERVED FAILURES`. INCOMPLETE variants can report provisional stratum counts only, labelled `PROVISIONAL — INCOMPLETE INVENTORY`, with no full cell or C_D. INVALID, EXCLUDED_BEFORE_DIAGNOSTICS and EXPECTED_NOT_RUN produce no measurement vectors, k values, cell or C_D. The tool labels its output `SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED` and lists external checks not performed.

### 19.4 Testing and limits

The synthetic suite contains 59 test methods covering the complete 17-field manifest fixture; unknown root and nested fields; both prohibited status-decision consultation flags; null/malformed digests and evidence references; status-specific measurement output; the no-false-zero correction; formula/source citation; record-ID and family checks; sidecar binding, schema identity and mismatch codes; and CLI outcomes.

A local run reported 59 tests passing after the validator and test's expected schema hash were temporarily adjusted to a locally reconstructed schema copy. That copy was 7 bytes shorter than the reviewed source; equivalence was not established. Therefore the local 59/59 result is not a test against the exact committed schema and does not prove that all fixtures pass against the exact source bytes. The committed branch packages the exact reviewed schema blob and pins its hash; the test now asserts the literal expected source hash. Claude's independent run against the exact committed bytes remains required. This limitation is recorded in `census-intake/CORRECTION_RECORD_2026-11-23.md` and the successor-specific review packet.

No bank membership, source-artifact provenance, exact variant-inventory coverage, q-registry membership, family-map membership, per-variant run-ledger reconciliation, historical exposure evidence or other external artifact checks were performed. No real manifest was read or validated.

### 19.5 Effect

The v0.3 successor remains unmerged and held pending Claude's independent code review. Claude's prior agreement is agreement to the repair approach, not a PASS. No master merge, owner freeze, production GO, real-manifest admission, census execution or downstream analysis is authorized by this amendment.

No bank access, parent acquisition, mutation allocation, solver construction or execution, diagnostic run, outcome collection, fitting or predictive analysis occurred. Gate 1 preflight remains **BLOCKED / NOT ASSESSABLE**; `P` remains **UNPROVEN**. The question whether the earlier conditional census authorization remains operative or was revoked remains unanswered.


---

## 20. Claude v0.3 review response and remaining test gate (2026-11-23)

Claude reviewed v0.3 and returned NOT PASS, identifying three remaining items. The two documentary/identity items have been addressed in successor commit `a48cc9dfdc5af87661762f6be9b98e11030ce9b8`:

1. The validator and README now describe `NO OBSERVED FAILURES` as this implementation's categorical reporting choice. The measurement specification §1 transcribes Rev 11's labelled zero convention, but §4 records that the convention is inconsistent across instruments. The code no longer describes the zero convention as universally settled.
2. The sidecar schema's Git blob SHA-1 was independently recomputed from the exact committed file bytes. At 1,268 bytes, its Git blob SHA-1 is `72fc746c3d6129534aeb2fdbcd866842865f98c7`, matching the GitHub-reported blob and validator pin. The 24,279-byte B1 schema was also recomputed as `0f2865e606fa61400184c09abd01601497637a6b`, matching the reviewed source.

The remaining gate is the complete 59-test suite executed against the exact committed branch bytes, with no schema-hash substitution. The prior local 59/59 run used a reconstructed schema and does not satisfy this requirement. No one has yet run the exact committed suite. Claude's NOT PASS remains operative pending that run. PR #10 remains draft and unmerged; no master merge is authorized.

No real manifest or external research inputs were used. Gate 1 remains BLOCKED / NOT ASSESSABLE and the scientific proposition remains UNPROVEN.
