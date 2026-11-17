# GPT Adjudication: GLM Follow-up on v0.21 and the Six-Point Review

**Date:** 2026-11-17  
**Artifact class:** GPT technical adjudication of GLM's follow-up verification and concurrence. This is not a new population specification, not a full independent review of v0.21, not a freeze record, and not an execution authorization.  
**Target specification:** `lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.21.md`  
**Target blob:** `8af908f6b0ad4cd060194a0a63f4914939f07756`  
**Working branch at verification:** `gpt/b1-computational-plan-2026-11-14`  
**Working-branch tip:** `cc20d02fa2f325295015723eff50fd88419709fc`  
**Master at verification:** `33dca9b61d95b9fb750f750919c32c2e08b2ee90`

## 1. Identity and provenance checks

GPT re-fetched the working branch, master, and v0.21 from GitHub on 2026-11-17.

- The working branch resolves to `cc20d02fa2f325295015723eff50fd88419709fc`, whose parent is `0a271ff48730664b63f708651be483e876e5bd80`.
- Master remains `33dca9b61d95b9fb750f750919c32c2e08b2ee90`.
- v0.21 remains blob `8af908f6b0ad4cd060194a0a63f4914939f07756`, 213,394 UTF-8 bytes, 1,294 newline-terminated lines, final newline present.

GLM's latest report independently confirms these identities using `ls-remote` and explicit-refspec fetches. GLM also corrected its earlier ref-reachability observation: its local clone had a single-branch fetch refspec tracking master only, so its earlier tracking-ref scan did not establish that the working branch was unanchored. The earlier warning is withdrawn. The working branch now demonstrably anchors the chain through `cc20d02`; no additional branch or tag repair is required.

GLM reports that it did not have Claude's original review document in its sandbox. Its current concurrence is based on GPT's written adjudication and GLM's own byte-level checks of the cited v0.21 sections. Therefore:
- GPT's assessment of the Claude-labelled review is grounded in the text pasted by the project owner in the conversation.
- GLM independently checked relevant v0.21 text and reached matching technical conclusions.
- GLM did not independently inspect or authenticate Claude's original review artifact, nor verify that GPT's précis reproduces every aspect of that artifact.
- This convergence is not a formal Claude-route review. The Claude route remains suspended under the owner decision in v0.21 §§0.23 and 8.

## 2. Adjudication of the six points

### 2.1 Option B and realization-setting proxy

**Disposition: CONCUR. No amendment to the primary estimand.**

v0.21 §5.7 explicitly chooses Option B. The primary target is incremental predictive information from \(C_D\) beyond the exact B1 cell \(c=(q,Z,k,\ell)\), while not conditioning on the realization-setting vector \(\mathbf a(v)\). The document also explicitly states that the predictive information may be carried through \(\mathbf a(v)\), and that the result is not a direct, causal, or realization-setting-independent effect.

M1-si requires within-parent variation in both realization settings and realized \(C_D\), but does not guarantee residual \(C_D\) variation at fixed \(\mathbf a(v)\). Accordingly:
- the adjusted sensitivity model is estimable only where the realized design has adequate residual \(C_D\) variation after conditioning on \(\mathbf a(v)\) and the exact cell;
- if that sensitivity is not estimable, the direct/parameter-independent question remains unanswered;
- failure of that sensitivity does not invalidate the broader proxy-inclusive Option B primary result.

Making the adjusted sensitivity a gate for the primary claim would silently replace Option B with the unadopted Option A. No such change is adopted.

### 2.2 Operating-count closure and authorization route

**Disposition: CONCUR. Material process gap remains open.**

v0.21 §2.5 requires a prospective operating-count justification but explicitly mentions separate authorization only for numerical simulation. It does not define an equally clear authorization route for outcome-free analytical operating-characteristic calculations. GLM correctly identifies that its symbolic scaffold inherited rather than closed this gap.

The required next design artifact is a named **Operating-Characteristic Evaluation Plan**. It may be drafted as a document-only, outcome-free proposal under the existing design-documentation scope. It must specify, at minimum:

1. the observed-parent-conditional estimand and fold scope, consistent with B1 v1.7 §5.7 V3;
2. the joint parent-cell-profile law as the primary support model, with any factorization explicitly flagged and justified;
3. the tiered attrition, score-coverage, LOPO, and fit-availability structure, without multiplying marginal attrition rates absent a justified factorization;
4. the frozen candidate-frame and selection-procedure requirements needed to make comparisons across candidate parent counts meaningful;
5. the source or elicitation basis for each assumed distribution, with every quantity labelled as assumed rather than empirical;
6. the owner-selected route and, if confirmatory, the prospective precision objective or minimum practically relevant predictive gain; otherwise, the explicit exploratory designation;
7. the outputs, sensitivity scenarios, limitations, and ratification sequence.

The plan may leave route-dependent numerical criteria blank until the owner makes the confirmatory-versus-exploratory decision. It may not manufacture a precision target or count.

**Authorization clarification:** drafting and reviewing the plan does not authorize any operating-characteristic calculation. Analytical calculations and any synthetic simulation require a separate, explicit owner-issued authorization that states the permitted methods, assumptions, inputs, outputs, and boundaries. The plan can contain a record of that authorization, but it does not authorize itself. A GPT/GLM review, a draft signature, or a technical recommendation is not owner authorization. No calculation is authorized by this adjudication.

The operating count remains open. The 30-parent/150-variant configuration remains logistics only.

### 2.3 Lineage-calibration feasibility

**Disposition: CONCUR. Operational-feasibility gap remains open, with the existing fallback preserved.**

v0.21 §2.3 specifies a substantial reference-set and review procedure but does not establish whether the required independent positive and hard-negative lineage units, language-family coverage, blinded reviewers, adjudication capacity, and validation precision can realistically be assembled.

A lineage-feasibility assessment should therefore estimate the reference-set and reviewer workload before the procedure is treated as operationally ready. It must keep distinct:

- calibration/validation of similarity thresholds, which are triage tools; and
- the mandatory blinded pairwise dispositions and pairwise-coherent cluster decisions that determine whether candidate implementations can count as separate verified parents.

Failure to meet a threshold-validation floor makes similarity thresholds descriptive/triage-only. It does not, by itself, force the entire study to be exploratory, because the mandatory pairwise review rules remain. Conversely, unresolved candidate lineage cannot be counted toward eligible \(G_c\); a LINEAGE_UNRESOLVED component contributes zero to eligible parent support, and its members cannot be selected as parents until resolved.

The actual workload cannot be credibly quantified from the current record alone. It depends on the selected language families, candidate frame, category definitions, number of reference units, reviewer availability, and the number of candidate pairs requiring direct disposition. No candidate-frame work or parent sourcing is authorized. A framework or assessment plan can be developed without pretending those inputs are known.

### 2.4 Sentinel when \(k_{\mathrm{fail}}=0\)

**Disposition: CONCUR. Adopt a data-representation clarification; no change to the eligible population.**

v0.21 §1.3 currently documents zero as a sentinel labelled **NO OBSERVED FAILURES**, not as an ordinary observed concentration value. The ratio defining \(C_D\) is mathematically undefined when \(k_{\mathrm{fail}}=0\), and B1 excludes these rows from primary-cell eligibility.

The data dictionary and analytical representation should therefore:
- retain a distinct status such as `NO_OBSERVED_FAILURES`;
- represent analytical \(C_D\) as NA when \(k_{\mathrm{fail}}=0\);
- prohibit numerical analysis from treating a legacy zero sentinel as an observed \(C_D\) value;
- preserve the established \(C_D\) definition for \(k_{\mathrm{fail}}>0\).

This is prospective for the new population: no new-population variants or outcomes exist, so there is no migration task. The convention must be fixed in the data dictionary before diagnostic or analytical data are generated. This does not alter the B1 eligible population.

### 2.5 Attainable concentration-numerator interval

**Disposition: CONCUR. The general formula belongs in the operative design record, conditional on a future capacity binding.**

For eight strata with frozen nonnegative integer capacities \(c_1,\ldots,c_8\), an exact total of \(k\) definite failures is feasible only if \(k\le\sum_j c_j\). The attainable maximum numerator values are the integer interval

\[
M_{\min}(k)\le m\le M_{\max}(k).
\]

where

\[
M_{\min}(k)=\min\left\{t:\sum_{j=1}^{8}\min(c_j,t)\ge k\right\},
\qquad
M_{\max}(k)=\min\left(k,\max_j c_j\right).
\]

For a joint definite/unresolved count, the aggregate capacity condition is \(k+\ell\le\sum_j c_j\). The unresolved counts can occupy the remaining aggregate capacity after the definite-failure allocation.

This formula is conditional on the frozen capacity vector. It does not bind the new population to eight slots per stratum, nor does it establish that Rev 1.4's 8-by-8 composition applies. Until the diagnostic-composition binding is separately authorized and frozen, v0.21's strata-only outer envelope remains the only unconditionally applicable bound. GLM's symbolic scaffold already contains the general formula; the remaining documentation task is to place it in, or directly reference it from, the v0.21 support rule without implying a capacity choice.

### 2.6 Historical reviewer attribution wording

**Disposition: No substantive finding. Optional wording improvement.**

v0.21 §0.21 already defines “GLM-authenticated” as GLM reviewer self-attestation, not a cryptographic identity claim. The unrelated counting error identified in GLM's earlier work does not logically invalidate that self-attestation.

For clarity, a future record may use “GLM self-attested” in place of “GLM-authenticated”. This is an editorial preference, not a scientific, methodological, or freeze blocker. No historical artifact should be silently rewritten.

## 3. §4.1: technical feasibility remains unreviewed

The latest GLM reply confirms that it checked the structure of §4.1 but expressly did not conduct a technical review of that section. Its check confirms that the document has the required staged architecture and fail-closed clauses; it does not establish that a concrete language-specific toolchain can satisfy them.

The outstanding issue is substantive implementation feasibility. Before any site enumeration, a concrete Stage 2 profile must be tested against a predeclared battery covering at least:
- canonical-labelling invariance under node renumbering, insertion-order changes, and other declared irrelevant representation changes;
- completeness of the selected language's relevant control-flow, exception, cleanup, and non-local-transfer model;
- sound treatment of external calls, unresolved effects, aliases, and unsupported constructs;
- resolution of the frozen operator-specific predicates/effect catalogue by the selected abstract domain;
- deterministic repeated-run byte identity and the uniform attempt/interruption protocol.

The test battery, fixtures, pass criteria, failure dispositions, and profile-hash discipline can be designed and reviewed before a concrete toolchain is selected. Toolchain selection, test execution, candidate-site enumeration, and any source-level work remain outside this document's authorization. If a later authorized Stage 2 test fails, the existing fail-closed disposition stands. Fixed-site parameter variation is not automatically admissible; it must independently satisfy the declared operator semantics and effect requirements.

A focused GLM technical review of §4.1 and of the proposed test-battery design remains outstanding. GLM's v0.20-to-v0.21 delta handoff did not request this full-depth review, and GLM confirms that the thirteen broader §8 questions were not reviewed in its latest reply.

## 4. Governance and review-route status

The owner decision recorded in v0.21 §§0.23 and 8 leaves GLM as the active independent-review route and suspends Claude. GPT's earlier request to Claude did not reinstate that route. The supplied Claude-labelled text remains usable as analytical input considered by GPT, but it is not counted as a formal review-route deliverable.

GLM's present response is a follow-up verification and technical concurrence with GPT's six-point adjudication. It is not a complete v0.21 review, not a review of the original Claude artifact, and not a technical review of §4.1. The active GLM route remains the formal route for the outstanding bounded reviews, with GPT providing separate adjudication.

## 5. Next sequence and current status

1. The owner decides whether the study is intended to be confirmatory or exploratory. This decision controls whether a prospective precision objective must be supplied.
2. Prepare the document-only Operating-Characteristic Evaluation Plan. Keep numerical calculations and simulation disabled pending explicit owner authorization.
3. Prepare a lineage-feasibility assessment framework. Actual workload estimates require declared language families, candidate-frame assumptions, reference-set categories, and reviewer-capacity inputs; none are to be invented.
4. Prepare the Stage 2 test-battery design and obtain a focused GLM review of §4.1 and that battery. Do not run tests or enumerate sites under this document.
5. Only after the relevant upstream decisions and reviews should the diagnostic-composition binding be drafted and independently reviewed.

Current project state remains:
- v0.21 is a design-only draft and is not frozen;
- operating parent count is open;
- the diagnostic-composition capacity vector is not bound;
- the protected-set custodian, consent/trigger ratifications, B1 analysis-plan amendment, computational-plan validation, isolation approval, and separate execution GO remain outstanding;
- mutation allocation is not established;
- no new-population solver variants or outcomes exist;
- no analytical evaluation, simulation, candidate-frame work, parent selection, source acquisition, solver construction, diagnostic execution, bank access, protected-set access, fitting, sampling, or outcome analysis is authorized by this artifact.

**Disposition:** GPT concurs with GLM's six-point technical concurrence, subject to the explicit authorization clarification in §2.2 and the scope limitations in §§1, 3, and 4. No v0.22 is created or proposed by this adjudication. The v0.21 specification itself is unchanged.
