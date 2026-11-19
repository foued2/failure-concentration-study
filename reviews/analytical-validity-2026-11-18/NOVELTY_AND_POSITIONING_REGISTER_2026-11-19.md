# Novelty and positioning register — 2026-11-19

**Status:** record and positioning audit. Adds no hypothesis, authorizes nothing, executes nothing.
**Answers:** Gate 0 of the goal document — *has this proposition already been tested?*
**Does not answer:** whether the hypothesis is true, or whether it is worth funding.

---

## 1. The proposition, stated once

Everything below is about one sentence. If a paper tests this sentence, the programme stops.

> **P.** For an engineered solver variant `v`, let `f(v) = (f_1,…,f_8)` count *definite* diagnostic
> failures across eight prespecified diagnostic input strata, `k(v) = Σ_j f_j`, and
> `C_D(v) = max_j f_j / k(v)`. Does `C_D(v)` carry incremental information about the variant's
> correctness on a fixed held-out input bank, beyond `(q, Z, k, ℓ)` — mutation mechanism `q`, parent
> algorithm family `Z`, definite-failure count `k`, unresolved count `ℓ` — when whole parent
> implementations are held out of evaluation?

Three features of `P` do the discriminating work, and each must be kept when searching:

1. **A fixed, prespecified 8-dimensional partition** of diagnostic inputs, not a learned representation.
2. **The maximum share**, not a general function of the failure vector.
3. **Parent-grouped evaluation**, not input-level or variant-level random splits.

A search that finds correctness prediction from execution but drops any of the three has not tested `P`.

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

## 3. Two claims that are theorems, not tests

These matter because reviewers keep asking questions that have mathematical answers. They are stated
here once so they stop being re-litigated.

### 3.1 `C_D` cannot out-predict `F`

`C_D` is a deterministic function of `F = (f_1,…,f_8)`: it is `max(F)/ΣF`. Therefore
`σ(C_D) ⊆ σ(F)`, and by the data-processing inequality

```
I(Y ; C_D | X)  ≤  I(Y ; F | X)        for every joint distribution
```

So **no experiment can show that `C_D` carries more information than the full failure vector.** The
population ceiling is fixed by mathematics. `F` is an upper bound that no sample size can overturn.

What *is* testable is the **compression ratio**: how much of `F`'s information a single scalar retains,
and whether the loss is worth the parsimony.

The three-world W1 numbers, which are the only executed measurement of this ratio in the corpus:

| Quantity | W1 / domain score | Note |
|---|---|---|
| `F` gain | `+7.90×10⁻⁴` | `[+6.92×10⁻⁴, +8.86×10⁻⁴]`, excludes 0 |
| `C` gain | `+1.96×10⁻⁶` | `[−1.24×10⁻⁶, +7.58×10⁻⁶]`, includes 0 |
| Point-estimate ratio | `C/F ≈ 1/403` | `C` retains ≈0.25 % of `F`'s gain |

**How strongly this may be stated:** the *ordering* is a theorem; the *magnitude* is one simulation's
point estimates, and the `C` interval spans zero, so "0.25 %" is illustrative, not an estimate. The
honest version is: *in the one executed world, the scalar retained a fraction of a percent of the
vector's gain, and the scalar's own interval was indistinguishable from zero under a second partition.*
That is a bad compression result, not a disproof of dominance.

### 3.2 "Does `C_D` add beyond `F`?" is identically zero

Because `C_D` is `F`-measurable, `I(Y ; C_D | X, F) = 0` exactly. A test of "incremental value beyond
the full failure vector" has a known answer and must not be run, reported, or funded.

This also corrects a recurring misreading of the repo's condition 6. The `F`-versus-`C` comparison in
the three-world simulation is a **bound on compression loss**, not an incremental-value test. B1
correctly does not condition on `F`; conditioning on `F` would make the estimand identically zero.

**What remains coherent:** `C_D` against the **exact cell** `(q, Z, k, ℓ)`. The cell fixes volume and
identity but not composition, so `C_D` still varies within it. That is the only non-vacuous contrast,
and it is the one B1 specifies.

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
| 7 | Almaghairbe & Roper 2016, *ISSRE*, `10.1109/issre.2016.22` | Classifying test results by semi-supervised learning; small clusters with high failure share | "Learn from test outcomes / failures concentrate" | Held-out correctness from a prespecified partition |
| 8 | Neural CodeRanker 2022, *NeurIPS* | Supervised correctness prediction from execution categories | Learning correctness from diagnostic failure information | Fixed interpretable scalar |
| 9 | CodeT 2023, *ICLR* | Generated tests + agreement for candidate selection | Test-based selection | — |
| 10 | LEVER 2023, *ICML* | Correctness prediction from task + code + execution; ablation shows execution helps | Execution outcomes add predictive information | The specific statistic or the grouped evaluation |
| 11 | AlphaCode 2022, *Science* 378(6624):1092, `10.1126/science.abq1158` | Filtering, clustering, reranking at scale | Clustering for selection | — |
| 12 | CodeScore 2025, *ACM TOSEM* 34(3):1–22, `10.1145/3695991` | Learns to estimate test PassRatio and executability | Broad "predict correctness from execution" | Incremental value of a maximum share |
| 13 | Sun et al. 2024, *ASE*, `10.1145/3691620.3695000` ("RankEF") | Execution feedback for ranking candidates | Same | Same |

**Read as a set:** rows 8–13 establish that execution-derived signals predict correctness. Rows 1–7
establish that failure diversity and failure clustering are mature ideas. Neither set tests `P`.

**But the margin is narrow.** `P` survives on the conjunction of an old index, a fixed partition, and a
grouped evaluation. Remove any one and the claim is already covered. A reviewer is entitled to ask
whether that conjunction is a scientific contribution or a well-specified ablation. The register
records the question rather than answering it.

---

## 5. The nearest genuine threat

The strongest competitor is not any single paper above; it is the **learned-representation family**
(rows 8–13). Given the same `(f, q, Z, k, ℓ, Y)` data, a flexible model over `F` will match or beat
`C_D` by §3.1. So `P` cannot be won on accuracy. It can only be won on:

- **parsimony** — one parameter instead of eight;
- **finite-sample stability** — fewer parameters at `J` parents;
- **interpretability** — "failures are concentrated" is a sentence a practitioner can act on;
- **pre-registration** — the partition is fixed before outcomes, so the comparison is not a search.

If the programme's justification is accuracy, the theorem in §3.1 already refutes the premise. If the
justification is parsimony or interpretability, then those are the quantities that must be measured,
and no record in the corpus measures them.

**This is the most important open question in this register**, and it is not a literature question. It
is a question about what the programme is claiming.

---

## 6. Citation corrections

| Review claim | Verified position | Correction |
|---|---|---|
| AlphaCode "(2023)" | *Science* **2022**, 378(6624):1092–1097 | Year corrected; Claude's recollection was right |
| CodeScore "ACM TOSEM, 2024" | TOSEM 34(3):1–22, Crossref year **2025** | Online-first 2024, issue 2025; cite the DOI, not the year |
| "RankEF (ASE 2024)" | Actual title: *Sifting through the Chaff: On Utilizing Execution Feedback for Ranking the Generated Code Candidates*, ASE 2024, pp. 229–241 | "RankEF" is the system name; cite the title |
| "Almaghairbe & Roper (published online 2016; journal issue 2017)" | ISSRE **2016**, pp. 116–126, `10.1109/issre.2016.22` — a conference paper | No 2017 journal issue exists for this title |
| "average precision 0.79 across unseen protocol implementations" attributed to Almaghairbe & Roper | That figure belongs to *Learning to Encode and Classify Test Executions*, a separate work | Two references were conflated; the figure must not be attached to the ISSRE paper |
| "Learning to Encode and Classify Test Executions" | No DOI resolved; treat as arXiv-only until a venue record is produced | Status: **unverified**, do not cite as peer-reviewed |

The last two rows matter beyond bookkeeping: a numeric claim from one paper was attached to another.
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
> evaluated for incremental held-out correctness beyond volume and identity, with parents held out —
> the programme stops at Gate 0 and does not proceed to gate 1. A close result that differs on exactly
> one of the three discriminating features in §1 must be recorded and adjudicated, not waved past.

---

## 8. Gate 0 verdict

| Question | Answer |
|---|---|
| Is the index novel? | **No** — Berger–Parker 1970, and the protocol already names it |
| Is "failures concentrate" novel? | **No** — rows 4–7 |
| Is "execution predicts correctness" novel? | **No** — rows 8–13 |
| Is `P` as stated already tested? | **Not found**, on a non-systematic search |
| Is `P` novel? | **Unproven.** Not the same as novel. |
| Does `P` have a defensible contribution? | Only if the claim is parsimony/interpretability, not accuracy — and no record measures either |

**Gate 0 status: OPEN, with the burden shifted.** The programme may proceed to measurement work, but it
may not describe its contribution as novel, and it may not describe accuracy as the motivation. Both
would be contradicted by §3.1 and §4.
