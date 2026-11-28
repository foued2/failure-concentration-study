# LC518 Gemini findings and instrument-qualification register

**Record ID:** LC518-GEMINI-INSTRUMENT-QUALIFICATION-REGISTER-2026-11-28  
**Prepared:** 2026-11-28  
**Status:** INVESTIGATION REGISTER / DRAFT / NOT AN ADOPTED PROTOCOL  
**Base snapshot:** `master` at `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a`  
**Branch:** `gpt/lc518-instrument-qualification-register-2026-11-28`

This file preserves the Gemini findings, GPT adjudications and unresolved work items for subsequent investigation. It is a tracking record, not a scientific decision, implementation, design freeze, execution authorization, or claim that any unperformed experiment has been completed. No change to the B1 estimand or accepted v0.21 taxonomy is made here.

## 1. Findings and adjudication status

Status meanings:

- **Resolved analytically:** the logical or mathematical issue is settled, without requiring a new experiment.
- **Source-reviewed:** repository or preserved-package source was inspected; execution/reproduction may remain outstanding.
- **Partially verified:** some underlying facts were checked, but the full reported result was not independently reproduced.
- **Confirmed weakness, not repaired:** the defect or limitation is established, but no corrective implementation has been made.
- **Open:** requires additional evidence, a decision, or an experiment.

| # | Gemini issue / finding | GPT adjudication and evidence | Status | Remaining work |
|---:|---|---|---|---|
| 1 | Hurdle 2 demanded that scalar concentration carry information beyond the full eight-stratum failure vector. | Mathematically impossible: for nonzero failure count, (C_D = \max_j(f_j)/\sum_j f_j) is a deterministic function of (F=(f_1,\ldots,f_8)). Therefore (I(Y;C_D\mid F)=0). This cannot be a B1 hurdle. | **Resolved analytically** | Preserve the corrected distinction: B1 tests (C_D) added to the coarse baseline; vector/locus comparisons are separate representation diagnostics. |
| 2 | Reframing into Question A and Question B. | Question A is the adopted B1 comparison: does (C_D) improve held-out prediction beyond (k_{fail}, k_{unresolved}, q, Z), under parent-grouped validation? Question B compares the scalar summary against richer vector or stratum-identity representations as a practical finite-sample comparison, not as extra information beyond the vector. | **Resolved conceptually** | Analysis specification and scoring/validation procedure still need to be predeclared before relevant outcomes. |
| 3 | Old C9 D4 and D8 weaknesses may undermine v0.21. | The accepted v0.21 v0.4 taxonomy changes D4 to all-even denominations with gcd 2 and an odd target at/above the minimum denomination; D8 is large-target reachable input, with the signed-int32 cap a global contract condition rather than an overflow-selection rule. Old C9 criticisms must not be transferred automatically. Owner acceptance is limited to the exact taxonomy document; it did not freeze a generator or authorize generation. | **Resolved as a version distinction** | Build and independently validate the new v0.21 bank. Do not treat taxonomy acceptance as evidence that the generated instrument works. |
| 4 | Finite-sample capacity of (C_D) may make within-cell variation impossible or narrow. | With eight strata of capacity eight, (\lceil k/8\rceil\le M\le\min(k,8)). At (k=1), (C_D=1); at (k=64), (C_D=1/8); for (57\le k\le64), (M=8) is forced. For (49\le k\le56), only (M=7) or (8) is possible. A specific mechanism may attain a much narrower subset than this combinatorial envelope. | **Resolved mathematically; realized support open** | Measure achieved (C_D) variation in real mutation realizations within exact ((q,Z,k,\ell)) cells. Capacity bounds are not evidence of achieved support. |
| 5 | v0.2 SSSP probes failed to expose several annotated algorithmic defects. | Source inspection of `study/probes.py` confirms fixed probe graphs across instance seeds and limited structures: chain/path cases, parallel edges with the shorter edge first, equal-cost two-path tie, and a self-loop. No (s=t) probes. These structures plausibly fail to expose the reported Bellman-Ford iteration, weighted-BFS, Floyd-Warshall diagonal, memoization/cycle, and early-target-return defects. The reported exact 0/30 outcomes were not rerun in this audit. Qualification: S[12]'s missing INF guard is not necessarily a genuine defect because it uses floating-point `inf`; adding a finite integer to infinity remains infinity. | **Source-reviewed; partly verified** | Re-run each relevant solver against the frozen v0.2 probes, then construct adversarial witnesses proving the intended defects. Reclassify S[12] separately rather than counting it as a confirmed defect. |
| 6 | v0.1 pilot hardcodes chi-square df=2 although the code permits only two finite LOIO fold estimates; LOIO fold estimates are dependent. | Source inspection of `scripts/run_pilot.py` confirms the hardcoded `CHI2_UB80_DF2` and `len(finite) >= 2` condition. With two finite estimates the sample variance has one degree of freedom, not two. The LOIO training sets overlap and the folds are not independent replicates; the same solver bodies recur across folds. | **Source-reviewed; statistical validity concern established** | Treat the reported variance-based sample-size estimate as unreliable. Any replacement needs an appropriate independent sampling unit and a justified variance method; do not repair only the df constant and call the design valid. |
| 7 | C9 launcher may trust its own generator's oracle and schema validator. | In the preserved GLM scratch review package, the launcher dynamically loads the published generator to run its serialized-record validator. The predicate crosswalk checks generator-produced logged oracle values against the saved held-out oracle output. This checks internal consistency but does not independently recompute the mathematical coin-change answer. This does not establish that historical answers were wrong. | **Confirmed integrity weakness, not repaired** | Independently recompute (W) and (N_0) using a separately implemented oracle and compare every generated record. Separate the validator from the generator implementation and document oracle provenance. |
| 8 | Historical C9 D/H banks have weak outcome composition and diagnostic-signature aliasing. | The preserved C9 run artifact was inspected: D has 64 raw records with 32 oracle-zero answers; H has 80 raw records with 37 zero answers. D3 and D4 are all zero; D2 puts the matching denomination first in all eight records. D1 and D6 have no answers >=2 in their 16 records. The reported four-bug profiles (D failures 18–23/64 and H failures 36–37/80) were supplied by Gemini and were not independently rerun in this audit. The always-zero solver therefore gets 50% on D and 46.25% on H by raw-record weighting. | **Bank composition verified; four-bug profiles partially verified** | Treat historical C9 H80 as exposed development data, not sealed confirmation. Run a predeclared challenge panel on the new v0.21 bank and report per-stratum failures, missed defects, and signature collisions. Do not transfer C9 composition counts to v0.21. |
| 9 | C9 D5 structural-exclusion preflight checked only two fixed exemplars, not all random draws. | The inspected preflight function checks the two fixed D5 exemplars. The final process also includes runtime collision checks and a final bank-disjointness check; the preserved run's final disjointness report passed. Therefore this establishes an incomplete static preflight proof, not a demonstrated collision in the published run. | **Scope weakness confirmed; collision not established** | For any future generator, run the complete structural-exclusion predicate on every candidate before acceptance, in addition to the final whole-bank collision audit. |
| 10 | RLC-0 classifier does not enforce the cross-seed gate. | Current `rlc0/classifier.py` implements `classify_all()` as independent per-seed classification. The RLC-0 contract says seed 1 = UNKNOWN voids certification claims for seeds 2 and 3. No such gate is implemented in that function. | **Confirmed contract-enforcement weakness, not repaired** | Add and test a study-level aggregation/gate before any authorized RLC-0 run. Preserve per-seed raw classifications separately from contract-level dispositions. |
| 11 | RLC-0 CBMC harness may be a scalability bottleneck. | Current `rlc0/harness/proof_harness.h` has a symbolic `int buf[10000]` and a 10,000-iteration loop with adjacent strict-increase constraints. `rlc0/FREEZE.md` records six baseline OOM/incomplete invocations and an authorized retry ending in wall timeout. This supports a major scalability concern, but does not isolate the loop as the sole cause. RLC-0 remains draft/unfrozen; Phase C is unauthorized. | **Concern confirmed; causal decomposition open** | No seed execution or unapproved resource/tool change. Any redesign requires a separate decision and must preserve full-domain semantics. |
| 12 | Current master workflow refers to missing C9 package chunks. | The current master workflow references `lc518-150/c9-github-generation-package-parts/part-00.b64` through `part-04.b64`, which are absent at those master paths. This snapshot is not self-contained for reproducing the package build. The historical Actions run and preserved run artifact are real and must not be erased by this snapshot observation. | **Snapshot reproducibility gap confirmed** | Preserve the historical artifact and its provenance. Any restoration/repackaging must be tied to exact hashes and history; do not imply the historical run did not occur. |

## 2. Operative B1 framing retained

The B1 target remains the accepted question: among singly mutated versions, does (C_D) carry incremental predictive information about held-out correctness beyond total definite failures and unresolved diagnostic outcomes, conditional on individual mutation-mechanism identity (q) and parent family (Z)?

The exact support cell remains ((q,Z,k_{fail},k_{unresolved})). The minimum support screen remains:

- (k_{fail}\ge2);
- at least three distinct parent groups contributing to the exact cell; and
- at least two distinct observed (C_D) values among those parent groups.

No pooling across mechanisms, families, or exact ((k,\ell)) cells. Parent-group IDs are for grouped validation, not predictive covariates. Failure of support is non-identification/insufficient support, not a null effect and not permission to switch to Claim A.

This register does not amend the adopted B1 decision record or authorize construction, execution, outcome collection, fitting, or confirmatory evaluation.

## 3. Proposed next scientific milestone: v0.21 instrument qualification

The immediate goal is to establish whether the accepted input taxonomy can yield a trustworthy and meaningfully discriminating diagnostic instrument. This must precede construction of the B1 mutation population.

### IQ-1. Independent answer verification

1. Implement two independent exact-answer oracles for the unbounded coin-change combination count (W(a,C)).
2. Independently implement the bounded 0/1 count (N_0(a,C)).
3. Cross-check both oracles on exhaustive small domains and predeclared edge cases before using either to validate a bank.
4. For every future bank candidate and accepted record, recompute (W), (N_0), the canonical input identity, and all required derived predicates in code that does not import the generator's oracle.
5. Check invariants: denomination-order invariance; irrelevant denominations greater than the target do not change (W); (W(0,C)=1); D4 has (W=0); D2/D3 have (W=1); D5 has (W\ge2) and (W>N_0); D6 paired rows agree on (W,N_0).

### IQ-2. Independent structural validation

Validate each candidate against all eight accepted v0.4 stratum rules, not just the assigned rule. Verify exact-one assignment, task-contract bounds, canonical identities, 64 raw rows, 60 distinct canonical identities, and exactly four permitted D6 duplicate pairs. Reject invalid candidates; do not relabel or silently replace them after outcomes are known.

### IQ-3. Predeclared diagnostic challenge panel

Before looking at bank outcomes, specify a compact suite of independently verified solver implementations representing the intended semantic defect classes. Each defective implementation must have at least one independently checked witness showing that it actually violates the task contract.

Run the correct reference and the challenge panel on the diagnostic bank. Record per-solver ((f_1,\ldots,f_8)), (k_{fail}), (k_{unresolved}), (C_D) where defined, defect detection/miss, and identical or near-identical failure signatures. The panel is an instrument-qualification set, not the B1 mutation population and not part of B1 fitting.

The qualification criteria and required defect classes must be specified before this run. Do not choose a favourable panel or alter thresholds after inspecting results.

### IQ-4. Protected evaluation identity and custody

Resolve the exact evaluation-bank identity and its relationship to the B1 population. Verify independent oracle provenance, canonical identity, manifest hashes, and custody. The exposed historical C9 H80 bank cannot be described as sealed confirmatory data. No protected evaluation inputs or outcomes should be visible to parent/mutation constructors or the analyst before the prescribed access point.

### IQ-5. Qualification verdict

Report one of:

- **PASS:** independent answer and structural checks pass, and the predeclared challenge panel meets the predeclared discriminatory-coverage criteria; protected evaluation identity/custody is separately established.
- **FAIL:** wrong answers, invalid structure, or failure to meet a predeclared essential discriminatory criterion.
- **NOT ASSESSABLE:** required provenance, source, records, custody, or evidence is missing.

Do not turn NOT ASSESSABLE into PASS. Do not revise the bank repeatedly until desired mutants fail. A failed instrument should trigger a versioned redesign and fresh review, not a post hoc patch to the same qualification run.

## 4. After instrument qualification: realized B1 support

Only after the instrument is qualified and the relevant authorizations are separately satisfied:

1. Establish real parent solver identities, source hashes, family assignments, build provenance, and custody.
2. Define each semantic mutation mechanism (q) and the legitimate realization variable (a). Distinguish a new realization of the same mechanism from a different mechanism.
3. Generate provenance-tracked runnable versions; record parent, (q), (a), source transformation, artifact hash, build and execution identity.
4. Run the diagnostic bank and compute the actual failure vector and (C_D).
5. Audit realized support within every exact ((q,Z,k_{fail},k_{unresolved})) cell under the adopted minimum rule.
6. If support exists, proceed only with the predeclared B1 comparison and grouped validation. If it does not, report non-identification/insufficient support. Do not pool cells or switch estimands after seeing results.

## 5. Evidence boundaries and source anchors

Repository sources inspected on the 2026-11-28 master snapshot:

- `study/probes.py`: v0.2 probe builders and seed-insensitive probe construction.
- `study/features.py`: feature, failure-count, and concentration calculation.
- `study/models.py`: LOIO training/test split and fold-delta calculation.
- `scripts/run_pilot.py`: hardcoded chi-square constant and variance calculation.
- `rlc0/classifier.py`: independent per-seed classifier.
- `rlc0/CONTRACT.md`, `rlc0/spec.json`: contract-level gate and status rules.
- `rlc0/harness/proof_harness.h`, `rlc0/FREEZE.md`: symbolic array, harness loop, and recorded OOM/timeout status.
- `.github/workflows/lc518-github-generation.yml`, `execution_protocol_v1.md`: current-master package references and historical protocol record.

Other evidence used in the preceding audit:

- Preserved historical C9 Actions artifact run `41591572358`, including its actual D/H banks and oracle outputs.
- Preserved GLM scratch review package `lc518_generator_scratch_GLM_review_v1.2.zip` for the launcher/generator implementation discussion. These package sources are not present at the current master paths; do not describe them as files fetched from current master.
- Accepted v0.21 v0.4 taxonomy and owner acceptance record on branch `gpt/lc518-v021-operational-strata-spec-2026-11-21`.
- Accepted B1 decision record on branch `gpt/lc518-claim-b1-primary-2026-11-05`.

Important limitations:

- Source inspection is not an execution reproduction.
- The exact four-mutant historical C9 failure profiles supplied by Gemini were not independently rerun in this audit.
- The exact v0.2 S[1..40] zero-failure claims were not independently rerun in this audit.
- No v0.21 bank was generated or run as part of this register.
- No B1 parent/mutation population was generated or evaluated.
- No B1 fitting, power analysis, or confirmatory evaluation was performed.
- This register does not constitute Claude review or agreement.
