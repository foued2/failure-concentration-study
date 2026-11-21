# Gate 0 preliminary literature and citation sweep

**Record ID:** LC518-G0-LITERATURE-SWEEP-2026-11-21  
**Search date:** 2026-11-21  
**Status:** PRELIMINARY SOURCE-VERIFIED SCAN; NOT AN EXHAUSTIVE SYSTEMATIC REVIEW; NO NOVELTY VERDICT

## 1. Scope and question

This initial scan addresses the closest software-testing literature on:
- clustering failures or failed test executions;
- execution-profile / program-behaviour clustering;
- stratified sampling and reliability estimation from execution profiles;
- clustering-based test-oracle construction; and
- fault-focused clustering in multi-fault debugging.

The Gate 0 question is narrower and different: whether a solver-version-level, record-weighted Berger–Parker maximum-share summary (C_D), calculated from definite failures assigned to eight predeclared input-property diagnostic strata, carries information about correctness on a separate declared evaluation distribution beyond the frozen B1 conditioning variables. The review must also examine how much predictive performance the scalar retains relative to the full eight-component failure vector.

The scan does **not** treat the Berger–Parker formula as novel. It does not assume that related work establishes or refutes the LC518 question.

## 2. Search procedure and reproducibility

The following exact-query families were run in web search on 2026-11-21. Queries were sent in English; results were opened where an authoritative publisher, author, or repository source was available.

1. `Dickinson Leon Podgurski 2001 software failure clustering execution profiles paper`
2. `Almaghairbe Roper 2017 failure clustering execution profiles software testing paper`
3. `DiGiuseppe Jones 2012 execution profile clusters faults software testing paper`
4. `software testing failure clustering execution profiles failure density test cases related work`
5. `"Separating passing and failing test executions by clustering anomalies" citations related work`
6. `"Concept-based failure clustering" PDF DOI 2012 full text`
7. `"Software Behavior and Failure Clustering: An Empirical Study of Fault Causality" PDF`
8. `"Estimation of software reliability by stratified sampling" Podgurski 1999 PDF`
9. `"Pursuing failure: the distribution of program failures in a profile space" 2001`
10. `"Building Test Oracles by Clustering Failures" authors proceedings`
11. `failure clustering software testing execution profiles fault localization software testing survey`
12. `"A comprehensive empirical investigation on failure clustering in parallel debugging"`
13. `"Evolving Ranking-Based Failure Proximities for Better Clustering in Fault Isolation" 2022 ASE`
14. `"failure clustering" "program version" predictive correctness concentration index software testing`

Search included publisher/author pages, repository records, conference pages, proceedings records and accessible full-text pages. It was not restricted to one database and no complete search export, deduplication ledger, protocol, or formal inclusion/exclusion coding was created. This is therefore a reproducible **initial scan**, not a systematic review.

## 3. Primary and near-primary sources reviewed

| Work | Source-verified bibliographic details | What the work studies | Relation to LC518 |
|---|---|---|---|
| Podgurski et al. (1999), “Estimation of Software Reliability by Stratified Sampling” | *ACM Transactions on Software Engineering and Methodology*, 8(3), 263–283. DOI: [10.1145/310663.310667](https://doi.org/10.1145/310663.310667). | Automatic clustering of captured operational execution profiles to create strata for sampling, reducing the number of executions requiring manual conformance checks and estimating software reliability. | Close precedent for execution-profile stratification and failure concentration, but its unit is an execution population and its estimand is operational software reliability, not a solver-version scalar predicting held-out correctness beyond version/family variables. |
| Dickinson, Leon & Podgurski (2001), “Finding Failures by Cluster Analysis of Execution Profiles” | Proceedings of ICSE 2001, pp. 339–348. DOI: [10.1109/ICSE.2001.919107](https://doi.org/10.1109/ICSE.2001.919107). | Uses cluster analysis of execution profiles to select executions for conformance checking; compares clustering-based filtering and sampling strategies with random selection. | Establishes that failures can be structured in execution-profile space and that clustering can help find them. It does not define a version-level maximum-share predictor or evaluate held-out correctness of solver versions. |
| Almaghairbe & Roper (2015), “Building Test Oracles by Clustering Failures” | *2015 IEEE/ACM 10th International Workshop on Automation of Software Test*, pp. 3–7. DOI: [10.1109/AST.2015.8](https://doi.org/10.1109/AST.2015.8). | Preliminary anomaly-detection study using input/output pairs to identify failure-enriched small clusters; evaluated on two systems. | Close to the idea that failures may cluster in a representation of input/output behaviour, but the objective is automated oracle support and reducing manual output inspection. |
| Almaghairbe & Roper (2017), “Separating Passing and Failing Test Executions by Clustering Anomalies” | *Software Quality Journal*, 25, 803–840 (2017; published online 3 October 2016). DOI: [10.1007/s11219-016-9339-1](https://doi.org/10.1007/s11219-016-9339-1). | Cluster-based anomaly detection using input/output pairs, and input/output pairs combined with execution traces, to identify passing/failing executions; evaluates three systems with multiple versions/faults. | Extends the clustering/oracle line. It concerns classifying executions and oracle assistance, not the LC518 solver-version-level (C_D) estimand or incremental prediction of separate evaluation correctness. |
| DiGiuseppe & Jones (2012), “Software Behavior and Failure Clustering: An Empirical Study of Fault Causality” | Proceedings of the Fifth IEEE International Conference on Software Testing, Verification and Validation (ICST 2012), pp. 191–200. DOI: [10.1109/ICST.2012.99](https://doi.org/10.1109/ICST.2012.99). | Studies the relation between execution profiles and output behaviour across multiple programs and more than 9,000 versions; examines assumptions that profile clusters correspond to uniform fault behaviour and the impact of multiple faults. | A relevant warning against equating clusters with one fault or a simple causal construct. It is not a held-out correctness prediction study using an aggregate failure-share index. |
| DiGiuseppe & Jones (2012), “Concept-Based Failure Clustering” | Proceedings of ACM SIGSOFT 20th Symposium on the Foundations of Software Engineering (FSE 2012). DOI: [10.1145/2393596.2393629](https://doi.org/10.1145/2393596.2393629). | Uses latent semantic analysis over concepts in executed source code to cluster failures, compared with traditional control-flow-based clustering. | Shows that the representation used for failure clustering matters. The unit remains an execution/failure cluster and the target is fault isolation, not the LC518 predictive estimand. |
| Song et al. (2022), “A Comprehensive Empirical Investigation on Failure Clustering in Parallel Debugging” | *Journal of Systems and Software*, 193, 111452. DOI: [10.1016/j.jss.2022.111452](https://doi.org/10.1016/j.jss.2022.111452). | Examines failure clustering for parallel debugging in multi-fault scenarios; controlled experiments span 1,060 faulty versions, 228 simulated faults and 141 real faults. Studies effects of risk-evaluation formula, number/type of faults, and pairing successful tests. | A contemporary adjacent line. It clusters failed test cases for fault isolation and parallel debugging, not diagnostic input strata into a version-level maximum-share predictor of separate correctness outcomes. |
| Song et al. (2022), “Evolving Ranking-Based Failure Proximities for Better Clustering in Fault Isolation” | Proceedings of ASE 2022. DOI: [10.1145/3551349.3556922](https://doi.org/10.1145/3551349.3556922). | Evolves suspiciousness-ranking representations of failed tests to improve clustering/fault isolation in multi-fault scenarios. | Further evidence that failure representation and clustering effectiveness are established topics. Its object and objective differ from LC518's aggregate predictor and evaluation target. |

## 4. Important distinctions supported by the inspected sources

The closest lines are related to LC518, but they generally operate at a different level:

1. **Execution/test-case unit versus solver-version unit.** The clustering studies group or classify executions/test cases. LC518 aggregates one solver version's failure counts over a fixed diagnostic suite.
2. **Fault isolation/oracle assistance versus correctness prediction.** The closest papers seek failure discovery, output checking, or grouping failures by likely fault. LC518 asks whether the diagnostic distribution predicts a separate correctness outcome.
3. **Representation versus scalar summary.** Existing work often clusters execution profiles, input/output representations, statement spectra, or suspiciousness rankings. LC518's proposed primary predictor is the maximum share of definite record-level failures across predefined input-property strata.
4. **Within-population concentration versus transfer to a separate target.** A cluster being failure-enriched does not establish that a solver version's diagnostic concentration predicts performance on another input distribution.
5. **Causation is not implied.** DiGiuseppe and Jones specifically examine limitations of assumptions linking profile similarity and uniform fault causality. LC518 must not describe stratum labels or (C_D) as causal fault identities.

These differences define a candidate comparison framework, not a novelty conclusion.

## 5. Citation-chase leads and unresolved bibliography

The inspected Dickinson/Leon/Podgurski and Almaghairbe/Roper papers cite earlier work on stratified sampling, execution profiles and test-oracle construction. The 2022 Song et al. work points to a broader multi-fault clustering and fault-isolation literature, including related DiGiuseppe/Jones studies and R-proximity work.

Additional leads identified but not fully examined in this pass include:
- Dickinson, Leon & Podgurski, “Pursuing Failure: The Distribution of Program Failures in a Profile Space” (2001). Search results returned inconsistent DOI strings; do not pin a DOI until checked against the publisher/ACM record.
- Francis, Leon, Minch & Podgurski, “Tree-Based Methods for Classifying Software Failures” (ISSRE 2004), cited by the related execution-classification literature.
- Liu et al. work on trace proximity / ranking proximity, and subsequent studies using statement-ranking representations.
- Later studies on program spectra, failure proximity, fault localization, anomaly-based oracles, and software product-line / multi-fault failure clustering.

The scan did not complete:
- full backward-reference extraction for every primary work;
- complete forward-citation enumeration from a stable citation index;
- full-text review of every lead;
- a deduplicated database export; or
- functional-equivalence searches across all terms for input strata, diagnostic feature composition, program/solver-version prediction, reliability indicators and out-of-sample correctness.

A bibliographic ambiguity also needs attention: search aggregation for “Pursuing Failure” returned more than one DOI string. That reference must be reconciled against the original proceedings before inclusion in the final claim register.

## 6. Preliminary synthesis, not a Gate 0 novelty verdict

The preliminary scan supports the following limited statements:

- Failure concentration and failure clustering are established ideas in software-testing research; LC518 must not claim novelty for the general observation that failures can cluster or for the Berger–Parker formula.
- Existing work provides relevant methods and warnings about the interpretation of failure groups, execution profiles and fault causality.
- The inspected studies do not, on the evidence reviewed in this scan, establish the exact LC518 conjunction: fixed diagnostic input-property strata, solver-version-level record-weighted (C_D), prediction of a separate evaluation correctness outcome beyond the frozen B1 baseline, and comparison to the full failure vector.
- The absence of an exact match in this initial scan is **not evidence that no functional equivalent exists** and is not enough to authorize a novelty claim.

## 7. Required next literature work

Before any Gate 0 novelty disposition:
1. Complete backward citation review of the seven core works in §3.
2. Run and save a forward-citation search for each core work in at least two stable indexes, with dates, result counts, exports and deduplication.
3. Examine the full texts of the 1999, 2001, 2012 and 2022 works and inspect their reference lists.
4. Review the 2004 classification study, 2001 “Pursuing Failure” record, later R-proximity work and oracle-clustering follow-ups.
5. Search for functional equivalents using alternate names: failure profile, test-family composition, diagnostic signature, fault/error distribution, version-level robustness profile, failure concentration, failure diversity, input-property partition and held-out correctness.
6. Build the source-verified comparison matrix required by Gate 0 §9.2, including analysis unit, predictor, outcome, baseline, validation split and limitations.
7. Record every excluded source with a reason. Do not declare novelty until the matrix and citation sweep are reproducible and independently reviewed.

**Disposition: PRELIMINARY LITERATURE SCAN COMPLETE; SYSTEMATIC BACKWARD/FORWARD CITATION SWEEP OPEN; NOVELTY DECISION OPEN.**
