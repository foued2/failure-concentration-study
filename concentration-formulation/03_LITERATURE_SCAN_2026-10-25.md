# Literature scan: failure structure, failure counts, and prediction of held-out correctness

**Date:** 2026-10-25  
**Status:** stage 2 of the plan, a focused scan, not a systematic review (Claude Doc export, rev 1). No novelty claim is made. Nothing here authorizes a run, a generation step, or a repository change beyond this record.

**Bottom line.** Nothing found tests the specific claim that a max-share concentration statistic over predefined test families predicts held-out performance beyond failure count `k`. Neighboring work is substantial, and two findings bear directly on the primary question: failure-causing inputs usually form contiguous regions, which would make whole-family failure the common case, and the failure count is known not to equal the number of root causes. Both raise the risk that fixed-`k` variation in `C` is rare in natural candidates.

## 1. Scope and limits

- About ten targeted searches across the four areas GPT listed: failure distribution and correctness, failure clustering for ranking or repair, transfer to unfamiliar inputs, and when counts suffice versus patterns.
- Reading was at abstract and snippet level. No paper was read in full, so details below are what the abstracts state.
- Searches were deliberately aimed at counter-evidence as well as support.
- Absence of a direct study in these results is weak evidence of a gap. A fuller review could still find one.

## 2. What the literature establishes

1. **A counterexample refutes correctness, and passing tests does not prove it.** EvalPlus ([Liu et al., NeurIPS 2023](https://arxiv.org/pdf/2305.01210)) shows that small benchmark test sets pass flawed programs and distort rankings. Work on coincidental correctness ([arXiv 1808.09233](https://arxiv.org/pdf/1808.09233v3)) shows passing tests can hide defects through masked error propagation. This supports the accept-side limit of the strict rule, which `C` cannot reach.
2. **The failure count is not the number of root causes.** The Hybiscus authors ([arXiv 2104.10360](https://arxiv.org/pdf/2104.10360)) state that one fault can fail many tests, so the number of failing tests may not indicate the number of root causes. Failure indexing methods (Hybiscus, [GREClue](https://doi.org/10.1145/3808118)) group failing tests by root cause and estimate fault counts. Hybiscus reports perfect clustering for 418 of 605 multi-failure runs.
3. **Faults usually act independently.** A fault-injection study on the Siemens suite reports under 1% interference between two faults ([Li et al., ICRSE 2017](https://research.buaa.edu.cn/en/publications/an-insight-of-double-faults-interactions-in-program-an-empirical-/)). Another empirical study finds failure behavior mostly accounted for by dominant faults ([Yan et al., QRS-C 2017](https://research.buaa.edu.cn/en/publications/the-failure-behaviors-of-multi-faults-programs-an-empirical-study/)). Composite-fault theory ([ICST 2017](https://www.cefns.nau.edu/~adg326/icst17.pdf)) says masking is rare but strong interactions can produce semantically new faults.
4. **Failure-causing inputs cluster in contiguous regions.** The adaptive random testing literature ([survey](https://arxiv.org/pdf/2007.03885), [taxonomic review](https://arxiv.org/pdf/1909.10879)) reports block, strip and point failure patterns, with block and strip patterns more common than point patterns.
5. **How failure rates distribute over partitions of the input domain matters for detection.** Partition-versus-random testing theory finds partition testing can be better, equal, or worse than random testing depending on how failures fall across subdomains, with proportional allocation the one scheme that never loses ([Chen and Yu](https://i.cs.hku.hk/~tse/Papers/2000s/typssTR.pdf)). Majorization and Schur-function methods give general conditions for this (Singh, Boland and Cukic, IEEE TSE 2003). The outcome studied is the probability that a test strategy detects a failure, not the held-out performance of a solver.
6. **Evaluation on tests independent of those used for repair is established method, and overfitting is common.** Smith et al. ([FSE 2015](https://www.cs.washington.edu/homes/brun/pubs/pubs/Smith15fse.pdf)) and Motwani et al. ([TSE 2022](https://people.cs.umass.edu/~brun/pubs/pubs/Motwani22tse.pdf)) evaluate repair patches on independent suites and find many pass the repair tests but fail the held-out ones. A 2025 study finds the problem persists with LLM-based repair ([arXiv 2511.16858](https://arxiv.org/pdf/2511.16858v1)).
7. **Ranking or selecting among candidates by execution behavior is established.** AlphaCode ([arXiv 2203.07814](https://arxiv.org/pdf/2203.07814)) clusters candidates that pass the example tests by their outputs on generated inputs. Trustworthy neural program synthesis ([arXiv 2210.00848](https://arxiv.org/pdf/2210.00848)) combines input-output pass rate and cluster size to estimate correctness. BATS ([arXiv 2107.13296](https://arxiv.org/abs/2107.13296)) uses the similarity of failing tests to predict patch correctness.

## 3. Matrix

| Area | Source | What it shows | Bearing on our question | Status |
| --- | --- | --- | --- | --- |
| Test adequacy | EvalPlus | Weak test sets pass wrong code | Accept side of B1, outside `C` | Established |
| Test adequacy | Coincidental correctness | Passing tests can hide defects | Same | Established |
| Failure vs fault | Hybiscus, GREClue | `k` is not root-cause count; clustering recovers it | `C` would compete with clustering, not only with `k` | Established (debugging use) |
| Fault independence | Li 2017, Yan 2017, ICST 2017 | Interference rare; dominant faults explain behavior | Supports a union-of-footprints assumption, with limits | Adjacent |
| Failure geometry | ART survey and review | Failures form contiguous block and strip regions | Whole-family failure may be the typical case | Established (numeric domains) |
| Partition theory | Chen and Yu; Singh et al. | Failure-rate spread over partitions drives detection | Same mathematics as concentration, different outcome | Adjacent |
| Held-out evaluation | Smith 2015; Motwani 2022; 2025 | Independent suites expose overfitting | Supports the held-out design | Established |
| Candidate selection | AlphaCode; trustworthy synthesis | Behavior clusters and pass rate rank candidates that pass examples | Different population: candidates that already pass | Adjacent |
| Patch correctness | BATS | Similar failing tests predict patch correctness | Different object: repair patches | Adjacent |
| Concentration beyond `k` | none found | None | The specific claim | **Not found** |

## 4. Evidence against, or complicating, the hypothesis

- **Contiguous regions suggest all-or-none.** If most real faults fail a contiguous region, and a diagnostic family is a region of the input space, whole-family failure is expected. That would give `C = p/k` throughout, which is what the saved v0.2 data show. A second cause is the instrument: the v0.2 families are built so that a defect on a property fails all of its probes. The ART evidence concerns numeric input domains and does not address constructed test categories. I did not find a source that does.
- **`k` may be a poor baseline in either direction.** One RL study argues test-case pass rate is a miscalibrated surrogate for proximity to full correctness ([arXiv 2605.02944](https://arxiv.org/pdf/2605.02944)). That is a different setting from ranking, but it warns against assuming that `k` is a strong, well-behaved baseline.
- **A max-share statistic is crude beside existing methods.** If the purpose is to estimate the number of root causes, failure clustering with richer test distances is better established. `C` would have to add value over those methods, not only over `k`.
- **Results in the partition-testing literature are assumption-dependent.** Conclusions flip with the failure-rate distribution and allocation scheme, which argues against expecting a single clean effect.

## 5. What the scan did not find

- No study of failure concentration across predefined test categories as an incremental predictor beyond failure count.
- No study of ranking rejected candidates (those failing tests) by held-out performance. Most selection work concerns candidates that pass example tests.
- No treatment of constructed test families whose probes are parameter variations of one property.

## 6. Corrections to earlier descriptions

- **Fault-Aware Neural Code Rankers** ([Inala et al., NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/hash/5762c579d09811b7639be2389b3d07be-Abstract.html)) does not use observed failures of a candidate. It trains a model to predict correctness and execution outcomes from the code without running it.
- **SimSCOOD** ([Hajipour et al., NAACL Findings 2024](https://arxiv.org/pdf/2210.04802)) studies out-of-distribution behavior of fine-tuned code models across data properties, not transfer of a solver's test failures. Its relevance to our held-out domain is weak.
- **Uncovering Weaknesses in Neural Code Generation** ([arXiv 2407.09793](https://arxiv.org/pdf/2407.09793)) builds a taxonomy of weaknesses by thematic analysis. It is not a statistical study of failure distributions.

## 7. Implications for the primary question

The proposed primary question asks whether `C` improves the ranking of same-`k` rejected candidates on independently constructed held-out inputs.

- **Support is the main risk, and the literature raises it.** Contiguous failure regions plus family-aligned probes predict few partial-family footprints. The ART sources describe region shapes but not their size relative to a test family, so partial failures remain plausible for threshold-type defects. This is a hypothesis to test in the feasibility stage, not a result.
- **A mathematical link exists.** At fixed `k`, `max_j f_j` is a Schur-convex function of `F`, so `C` is monotone in the majorization order. This is my observation, not from a source. It connects `C` to the majorization approach used in partition-testing theory, where the outcome is detection probability.
- **Same-`k` ranking against a constant baseline is a low bar.** At fixed `k` a `k`-only model ranks nothing, so any real rank agreement counts. That makes uncertainty control and the practical-significance threshold important.
- **A source of ground-truth root-cause structure may exist.** The Hybiscus authors report public multi-fault datasets built on Defects4J and SIR. They carry known root causes for failing tests but are real-world programs with no predefined families, so they would test a different question. This is a lead, not a proposal.
- **Independent-suite evaluation has precedent.** The repair literature's practice of an evaluation suite independent of the repair tests matches the held-out domain requirement in the formulation note.

## 8. Neighboring areas not yet searched

- Slice-based and worst-group evaluation in machine learning and NLP behavioral testing, where the worst-performing subgroup is analogous to `max_j f_j`.
- Defect prediction and software reliability estimation from failure counts.
- Automated grading with partial credit.
- Capture-recapture methods for estimating the number of faults.

## 9. Next steps within current authorization

- GPT challenges the interpretation above, in particular the reading of the ART evidence and the claim that nothing direct exists.
- Search the four neighboring areas in Section 8, again looking for counter-evidence.
- Then produce the short research brief GPT described, with the recommended primary estimand and a proposed bounded held-out domain.
- No execution, generation, simulation, or repository change is needed for any of these.
