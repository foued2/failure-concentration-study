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

### 9.2 The ≥60 % figure is now verified at the publisher abstract

The earlier round had not verified it. It is verified as of 2026-11-20 against the publisher abstract
(Crossref record `10.1007/s11219-016-9339-1`, CC-BY, issue 25(3):803–840, online 2016-10-03):

> "Evaluation on three systems with a range of faults demonstrates this hypothesis to be valid — in many
> cases small clusters were composed of at least 60 % failures (and often more)."

Row 8's wording therefore stands, with one qualifier: the figure is a cluster-composition observation
("in many cases"), not a distributional estimate and not a predictor. It does not license "failures are
usually concentrated", and it says nothing about held-out correctness. The other figures Claude lists
(Wu 2004, Herzig 2014, Anand 2015, Sundell, Xiong 56.3 %, Tian AUC 0.557–0.718) remain abstract-level; this
amendment does not promote them to verified findings.

### 9.3 Challenge 1 — within-cell support: accepted, with one correction and one ceiling

Claude's statement: the exact cell already fixes the failure total and the unresolved count, so the only
information `C_D` can add is the ordering of the within-cell configuration.

- **Correction.** `C_D` is invariant to permuting stratum labels (dominance document §2). It does not see
  the ordering at all. Within a fixed-`k` cell, `C_D = M/k` with `M = max_j f_j`, so the only thing that can
  vary is the *size of the largest part*. The added information is "how large is the largest part", never
  "which stratum holds it". A claim that `C_D` localises failures to a stratum is a different claim and
  would require reallocating inputs, not permuting labels.
- **Ceiling.** With eight strata of capacity eight, `M ∈ {⌈k/8⌉, …, min(8,k)}`, so any cell admits at most
  eight distinct `M`, hence at most eight distinct `C_D`. The distinct-`C_D` column of the §4.1 table is
  that ceiling (seven values for `9 ≤ k ≤ 16`). The realized count can only be lower. That is the
  resolution of the exposure B1 tests: a one-parameter feature with at most eight levels.
- **Already frozen as a design condition.** B1 v1.7 §3 item 3 makes a cell contribute only when
  `G_c^train ≥ 2`, `D_c^train ≥ 2`, and `W_{C,c}^train = Σ_v (C_D(v) − C̄_D,c)^2 > 0`; §3 item 4 requires
  coverage tables, exclusion reasons, and per-parent reporting. `W > 0` *is* "at least two distinct `C_D`
  in the cell". Claude's requirement is therefore not a missing design element; it is a census that has
  not been run.
- **Not computed here.** The census needs the LC518 diagnostic tables, which are not in this tree, and the
  pause forbids bank access. It is computable from the design and the `C_D` configuration alone: no
  outcome, no fit, no solver.

**Pre-registered census (first Gate 1 action, on reopening).** Group versions by exact cell `(q, Z, k, ℓ)`.
Per cell report: version count, parent count, `G_c`, `D_c`, distinct `M`, distinct `C_D`, and
`W_{C,c}`. Then report (a) the cells with ≥2 distinct `C_D`; (b) the versions and parents they cover;
(c) the cells where every version shares `M`; (d) the fraction of the 78-record estimand carried by (b).
**Stop rule:** if no cell has ≥2 distinct `C_D` with ≥2 parents, the within-cell permutation is degenerate
and Gate 1 fails before fitting. That outcome is reported as a design failure, never as a negative result
about concentration.

### 9.4 Challenge 2 — power and MDE: the gap is real but not empty

GPT's memo carries no MDE, and Claude is right that this matters before a parent count is argued. Three
facts, kept separate:

1. The record already contains illustrative MDE arithmetic (`claude-keys-verification-2026-11-18.md` §3):
   `MDE₈₀ ≈ 2.802 · σ_u / (sd(C) · √J)`. At `J = 30` it gives 0.10–0.41 nats on the two larger assumed
   `σ_u` rows (0.04 nats on the smallest), and the favourable row needs ≈150 units. **Both inputs are
   assumed; neither `σ_u` nor `sd(C)` is estimated anywhere.** The table shows the size of the hole, not a
   design input.
2. The LC518 bank disclaims power explicitly: its sizes are for structural coverage, not statistical
   power, and "previous power figures remain invalidated".
3. No empirically grounded MDE therefore exists. GPT's rejection of the 150-variant programme is correct
   on Gate 0 and on measurement, but incomplete as written: the statistical reason is the missing variance
   source, not a computed power figure for B1.

Adopted as a Gate 0 exit condition: before any parent count is argued, state the target effect, the
variance source, and the resulting `J`. No such `J` is currently justified anywhere in the record, and the
`J` grid in the S1 specification is a calibration dimension only.

### 9.5 Challenge 3 — "no exact match" is not closure: already the record's position

§7 states that the search is non-systematic and that absence of a hit is weak evidence of absence; §8 says
`P` is **unproven, not novel**. This amendment makes the acceptance sentence explicit:

> Gate 0 closes only when the contribution is stated in one precise paragraph, its difference from the
> closest prior work is shown, its inferential scope is fixed, and **no priority or novelty claim rests on
> the absence of a search hit**. A completed scoping review carrying the §7 evidence-matrix fields is the
> minimum. A failed search is not a result.

### 9.6 Citation hygiene

The favicon links and the stray "ES" in GPT's message are chat-interface artifacts, not record content;
§4 and §6 carry DOI-verified citations only. Claude's venue and year checks agree with Crossref on both
Almaghairbe papers. No row of §4 is corrected by this amendment other than the addition of row 8a.
