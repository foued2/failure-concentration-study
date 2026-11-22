# Gate 0 literature search — executed record

**Date:** 2026-11-22
**Status:** SEARCH EXECUTED AND LOGGED; NO DIRECT MATCH; `P` UNPROVEN; GATE 0 OPEN
**Scope:** Read-only bibliographic search. No solver construction, execution, fitting, sampling, or bank access.
**Supersedes:** nothing. Adds a dated search deliverable to register §9–§10.

---

## 1. What this record answers

The owner asked what the literature says about `P` and what the programme should do next. This record answers the first question with an executed, reproducible search and answers the second with a decision list (§10).

`P` is the register §1 proposition: within the observed parent set, does a version-level maximum share `C_D` of a prespecified 8-stratum diagnostic failure vector improve leave-one-parent-out prediction of record-level correctness on the fixed 78-record development bank, beyond the exact cell `(q, Z, k, ℓ)`?

The three discriminating features remain those of register §1: a **fixed prespecified partition**, the **maximum share**, and **parent-grouped evaluation**. A candidate that drops any one has not tested `P`.

---

## 2. Protocol as executed, and its deviations

The 12-query protocol was approved in principle but not executed verbatim. The deviations are recorded here rather than hidden, because a retrospective protocol is exactly the defect the 2026-11-22 review identified in the earlier three-query screening.

| Item | Planned | Executed | Reason |
|---|---|---|---|
| Search tool | Chat web search | OpenAlex API + Crossref | The web-search connector returned HTTP 402 (no credit) on every call |
| Query count | 12 | 18 informative + 2 discarded | The 12 approved strings collide badly in a Boolean index; four were split and two added to cover the same four themes |
| Query wording | Verbatim strings | Boolean/phrase expressions on `title_and_abstract.search` | Index syntax; mappings are listed in §3 |
| Date filter | 1990-01-01 → 2026-11-22 | None applied; retrieved records span 1958–2026 | No pre-1990 record was judged relevant; the filter would only have hidden the collision behaviour |
| Screening | Titles + abstracts | Title-level on 431 records; abstracts for 7 candidates | See §4; full text reachable for none of the closest four |
| Citation chasing | Backward + forward | Forward for 3 works; backward for 2 | §5 |
| Databases | Not specified | OpenAlex only (Crossref for DOI verification) | No Scopus, Web of Science, ACM DL, or IEEE Xplore subscription access |

**Consequence.** This is a documented scoping search with a real query log, not a systematic review. It is stronger than the earlier three-query screening and weaker than a PRISMA-style protocol. The limits in §9 are part of the result.

---

## 3. Query log

Source: `https://api.openalex.org/works`, `filter=title_and_abstract.search:…`, relevance order, 25 records per page. Retrieved 2026-11-22. Counts are OpenAlex's index counts for that expression and will drift.

| # | Expression (as executed) | Count | Screened | What the first page was |
|---|---|---|---|---|
| Q01 | `"maximum category share"` | 2,274 | 25 | Network pricing, phylogenetics, retail; no software |
| Q02 | `"Berger-Parker"` | 811 | 25 | Ecology and parasitology only; no software-test use |
| Q03 | `"dominance index"` OR `"Simpson index"` OR `"Gini coefficient"`, full text `software` | 3,806 | 25 | Code-evolution Gini, ML out-of-distribution Gini, piracy economics |
| Q04 | `"failure concentration"` OR `"failure dominance"` OR `"concentrated failures"` | 112 | 25 | Structural reliability, medicine; one non-peer-reviewed Zenodo "failure dominance coefficient" |
| Q05 | `"failure diversity"` OR `"fault diversity"` | 67 | 25 | N-version programming, reliability diversity, RL fault diversity |
| Q06 | `"failure entropy"` OR `"test entropy"` OR `"entropy of failures"` | 95 | 25 | Reliability-theory entropy; mechanics; none predictive in SE |
| Q07 | `"per-input"` OR `"individual input"` OR `"individual test input"` | 3,521 | 25 | Control-flow integrity, control theory, economics |
| Q08 | `"item response theory"` | 19,240 | 25 | Psychometric handbooks; no SE application on page 1 |
| Q09 | `"test outcome prediction"` OR `"predicting test outcomes"` OR `"test verdict prediction"` | 43 | 25 | Two SE hits: BASHIRI (ASE 2025), LLM-trace study (2026) |
| Q10 | `"test failure prediction"` | 6 | 6 | One SE hit: *Striving for Failure* (ICSE 2015) |
| Q11 | `"failure proximity"` OR `"failure spectra"` OR `"test outcome pattern"` | 38 | 25 | Failure-proximity fault-localisation lineage (2006–2024) |
| Q12 | `"code generation"` AND `"correctness"` | 3,178 | 25 | LLM correctness evaluation, CodeT, uncertainty estimation |
| Q13 | `"predicting correctness"` OR `"correctness prediction"` | 20,362 | 25 | Dominated by predictor–corrector numerics; phrase collision |
| Q14 | `"pass rate"` OR `"pass@k"` OR `"test pass ratio"` | 14,484 | 25 | Education and medical licensing; phrase collision |
| Q15 | `"failure clustering"` | 255 | 25 | Six SE works: DiGiuseppe 2012, Song 2022, Hybiscus 2021, *Failure clustering without coverage* 2019, lexical-coverage 2021, behaviour-characterisation 2013 |
| Q16 | `"failure profile"` OR `"failure signature"` | 775 | 25 | Hardware and reliability signatures; no SE predictive use |
| Q17 | `"dominance"` AND `"software testing"` | 36 | 25 | Fault collapsing/domination in test-data generation; quantum output dominance |
| Q18 | `"failure distribution"` | 2,485 | 25 | Reliability theory and time-to-failure statistics |
| — | `"concentration index"` AND (`"software"` OR `"test"`) | 18,411,191 | 0 | **Discarded:** Boolean grouping error; the `OR "test"` term swallowed the query |
| — | `"execution outcomes"` OR (`"correctness"` AND `"execution results"` AND `"predict"`) | 247,339 | 0 | **Discarded:** over-broad; returned predictor–corrector numerics |

Approximately **431 titles** were screened. Abstracts were retrieved for seven candidates; the TSE record indexes none. No full text was read in this pass.

**Reproducibility.** Replace spaces with `%20` and quotes with `%22` in the `filter` value, e.g.
`https://api.openalex.org/works?filter=title_and_abstract.search:%22failure%20clustering%22&per-page=25`

---

## 4. Candidate decisions

Decision vocabulary: **DIRECT** = tests the full conjunction in `P`; **PARTIAL** = shares the target and at least one discriminating feature; **ADJACENT-CLOSE** = shares the prediction target or the concentration observation, but not both the prespecified partition and the parent-grouped design; **ADJACENT** = related object, different estimand; **EXCLUDED** = different domain or non-peer-reviewed.

**No DIRECT match was found. No PARTIAL match was found.**

| Work | Verification | Why it is not `P` | Decision |
|---|---|---|---|
| Almaghairbe & Roper 2017, *SQJ* 25(3):803–840, `10.1007/s11219-016-9339-1` | Full text read in earlier round (register §9.2) | Clusters are learned, not a prespecified 8-stratum partition; the finding is cluster *composition* (small clusters sometimes ≥60 % failures), not a maximum-share covariate; no held-out per-record correctness model; no parent grouping | ADJACENT-CLOSE |
| Almaghairbe & Roper 2019, AITest, `10.1109/aitest.2019.00009` | Abstract | States that failures "concentrate into smaller clusters" and uses cluster-size order to prioritise inspection; the concentration is a *diagnostic ordering device*, not a predictor in a correctness model; no baseline, no parent grouping | ADJACENT-CLOSE |
| *Can Open-Weight LLMs Predict Test Outcomes from Traces?* 2026, `10.1145/3843782.3844663` | Abstract | Predicts per-test pass/fail from execution traces across held-out subjects. Shares the per-input target, but the predictor is a fine-tuned LLM over trace chunks, not a concentration statistic; no failure-count/exact-cell baseline; not solver variants; no parent grouping | ADJACENT-CLOSE |
| BASHIRI 2025, ASE, `10.1109/ase63991.2025.00372` | Abstract | Learns an oracle from execution features to classify runs; 95 % accuracy claimed. Different target (oracle learning), no concentration statistic, no record-level bank, no LOPO | ADJACENT-CLOSE |
| *Striving for Failure* 2015, ICSE, `10.1109/icse.2015.134` | Abstract | Predicts which regression tests will fail before running them, at industrial scale (Microsoft Dynamics AX). File/test level, feature-based, not a failure-composition statistic, not per-record solver correctness | ADJACENT-CLOSE |
| Song et al. 2022, *JSS* 193:111452, `10.1016/j.jss.2022.111452` | Full text in earlier round | Evaluates what makes failure clustering effective. No predictive model of correctness; no concentration covariate; no LOPO. Its 98 references and 11 citing works contain no such model (§5) | ADJACENT |
| DiGiuseppe & Jones 2012, ICST `10.1109/icst.2012.99`; FSE `10.1145/2393596.2393629` | Abstract/record | Failure profiles do not map cleanly to faults; concept-based clustering. Interpretive, not predictive | ADJACENT |
| Hybiscus 2021, `10.48550/arxiv.2104.10360` | Abstract/record | Hypergraph test distance for failure clustering. Clustering only; 2 citing works, both clustering | ADJACENT |
| *Failure clustering without coverage* 2019, ISSTA, `10.1145/3293882.3330561` | Abstract | Groups failing hardware-in-the-loop tests by non-code features and selects representatives; 8,743 failing tests, 1,531 faults. Clustering for triage, no correctness model | ADJACENT |
| SURE 2024, `10.1145/3676958` | Record | Failure indexing by program memory spectrum; root-cause similarity. Not prediction of correctness | ADJACENT |
| ReClues 2024, `10.1145/3597503.3639098` | Record | Failure representation/indexing for parallel debugging | ADJACENT |
| Systemic Flakiness, EASE 2025 `10.1145/3756681.3756945`; IEEE TSE 2026 `10.1109/TSE.2026.3750452` | Crossref for both; abstract for EASE | Predicts *co-occurrence* of flaky failures using static test distance. Different response variable (pairwise co-occurrence, Jaccard), not individual input correctness; no concentration statistic | ADJACENT |
| Failure proximity: `10.1145/1181775.1181782` (2006); `10.1109/tse.2008.66` (2008); `10.1145/3551349.3556922` (2022) | Records | Proximity of failures for fault isolation. Response is fault ranking, not record correctness | ADJACENT |
| Boland, Proschan & Tong 1987, `10.1017/s0269964800000383`; Chen & May 2016, `10.1109/tr.2015.2503335` | Register rows 2–3 | Distributional/fault diversity as a reliability input. No prediction of per-record correctness, no prespecified diagnostic strata | ADJACENT |
| Gini/inequality indices in software | Q03 | Code-structure or model-uncertainty inequality. Different measured object | EXCLUDED |
| Berger–Parker ecology corpus | Q02 | The index itself, applied to species abundance. Domain transfer only; register row 1 already owns this | EXCLUDED |
| Zenodo "Failure Dominance Coefficient" 2025, `10.5281/zenodo.17723889` | Record | Non-peer-reviewed engineering artifact; "catastrophic failure" proof, not software-test prediction | EXCLUDED |

**Reading of the table.** The corpus contains (i) a mature concentration *observation* (Almaghairbe), (ii) a mature clustering-for-debugging literature (Song, DiGiuseppe, Hybiscus, ISSTA 2019), and (iii) a mature per-input outcome-prediction literature (BASHIRI, LLM traces, *Striving for Failure*). It does not contain the conjunction: a prespecified-partition maximum share used as a covariate against an exact-cell baseline under parent-held-out evaluation.

---

## 5. Citation chasing

| Direction | Seed | Records | Result |
|---|---|---|---|
| Forward | Almaghairbe & Roper 2017 (`W2529805005`) | 28 | Oracle learning, test classification, prioritisation. Closest: *Using ML to Classify Test Outcomes* (2019), *Supervised learning over test executions as a test oracle* (2021). Neither builds a concentration predictor |
| Forward | Song et al. 2022 (`W4288045708`) | 11 | Parallel fault localisation, multi-fault clustering, debugging surveys. None predictive of record correctness |
| Forward | Hybiscus 2021 (`W3152620067`) | 2 | Root-cause clustering (SAP HANA), multi-fault localisation |
| Backward | Song et al. 2022 (98 references) | 98 | Clustering, spectra-based localisation, mutation adequacy, failure proximity. No maximum-share predictor |
| Backward | Almaghairbe & Roper 2017 (26 references) | 26 | Cluster analysis of execution profiles, oracle construction, stratified sampling. No concentration covariate |
| Backward | Systemic Flakiness TSE 2026 | 0 | IEEE record deposits no references; backward chase not possible from the index |

Backward chasing surfaces *Finding failures by cluster analysis of execution profiles* (2001) and *Building Test Oracles by Clustering Failures* (2015, register row 8a). Both are clustering-for-detection; neither is `P`.

---

## 6. Bibliographic corrections

**6.1 The disputed Systemic Flakiness DOI is real.** GPT's `10.1109/TSE.2026.3750452` resolves in both Crossref and OpenAlex to:

> Parry, Kapfhammer, Hilton & McMinn, "Systemic Flakiness: A Study of Flaky Test Failure Co-Occurrence Using Java and Python Projects," *IEEE Transactions on Software Engineering*, pp. 1–21, Crossref record created 2026-11-03; IEEE Xplore document 11773385.

The EASE 2025 paper (`10.1145/3756681.3756945`, pp. 476–487, "An Empirical Analysis of Co-Occurring Flaky Test Failures") is a **separate, earlier publication** of the same research line, not a preprint of the TSE article. Claude's statement that no TSE 2026 version exists is **wrong**; its recommendation not to cite the DOI until a publisher record is checked is satisfied here. Both records should now be cited separately.

**6.2 Two register additions.** Rows 20 and 21 are recorded in register §11: the EASE 2025 and TSE 2026 Systemic Flakiness records, with the TSE version flagged as record-level only (no indexed abstract; no open full text).

**6.3 No change to the Wu et al. resolution.** Register §10.2 stands.

---

## 7. What the search supports

1. **The phenomenon is not new.** Failure concentration in small clusters is reported empirically from 2015 onward, and the Berger–Parker index dates from 1970.
2. **Per-input correctness prediction is an active line.** BASHIRI (2025) and the LLM-trace study (2026) predict test outcomes directly.
3. **The conjunction is not in the corpus.** No retrieved work uses a prespecified-partition maximum share as a covariate against a failure-count/exact-cell baseline with parents held out.
4. **The margin is narrow and defined by design, not by statistic.** Remove the prespecified partition, the maximum share, or the grouped evaluation and the claim is already covered.

## 8. What the search does not support

- It does **not** establish novelty. A documented non-finding on one index with stated limits is a scoping result, not a priority claim.
- It does **not** establish that `P` is untested outside OpenAlex's coverage: no Scopus, Web of Science, IEEE Xplore, or ACM DL; English-language bias; abstract-level for four closest candidates; no full text for any.
- It does **not** decide the contribution question. Whether a one-parameter incremental gain is worth reporting is a positioning and design judgement, not a literature fact.
- It does **not** touch any measurement decision: H6 aggregation, unresolved handling, and outcome coding remain open.

---

## 9. Verdict

| Question | Answer |
|---|---|
| Is there a direct match to `P`? | **No**, on this search |
| Is there a partial match? | **No**; four adjacent-close works share either the target or the observation, not both |
| Is `P` novel? | **Unproven.** Unchanged from register §8 |
| Is Gate 0 closed? | **No.** The search deliverable is now documented; the contribution decision is not made |
| Did this change any register §8 verdict? | **No** |

---

## 10. What we need to do

The literature is no longer the binding constraint. Four decisions and one prohibition remain, in order.

**10.1 Accept or reject this search as the Gate 0 scoping deliverable.** It has a query log, counts, candidate decisions, forward and backward chasing, and explicit limits. If accepted, record it as such; if not, name the missing element. Do not describe it as a systematic review.

**10.2 Fix the contribution object.** The defensible contribution is **the design**, not the statistic and not the phenomenon: a prespecified-partition dominance covariate evaluated against an exact-cell, failure-count-conditioned baseline under parent-held-out evaluation, with a pre-registered null-capable outcome. Register §9.8 already moves in this direction; it should say plainly that the index is borrowed, the phenomenon is known, and the test is the contribution.

**10.3 Decide whether to authorize the design-only support census.** This is the only remaining Gate 1 prerequisite and it needs the LC518 diagnostic tables, which the pause currently forbids. The census is cheap, uses no outcomes, and answers whether B1 has any eligible cell and any scoreable LOPO fold at all. It should precede any solver budget.

**10.4 Do not fund 150 solvers before 10.3.** The one executed world retained ≈0.25 % of the full vector's gain, with an interval spanning zero. That does not refute `C_D`, but it sets the prior: the most likely B1 outcome is a well-identified null. Fund the census and, if it passes, a minimal pre-registered run; not a 150-solver programme on the strength of an old index.

**10.5 What not to do.** Do not run further keyword searches with the same object and call the result novelty. Do not reopen the identity documentation. Do not treat this record as an execution GO.

---

**End of record.**
