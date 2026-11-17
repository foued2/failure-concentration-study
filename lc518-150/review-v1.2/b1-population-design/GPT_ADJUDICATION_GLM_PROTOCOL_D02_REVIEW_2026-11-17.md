# GPT Adjudication: GLM Bounded Review of LC518 Exploratory Feasibility Protocol Draft 0.2

**Date:** 2026-11-17  
**Artifact class:** GPT technical adjudication of GLM's bounded analytical review of protocol draft 0.2, with a corresponding document-only revision to draft 0.3. This is not protocol adoption, not a freeze, not a v0.21 amendment, not an owner GO, and not an execution authorization.  
**Review route:** GLM remains the active formal independent-review route under v0.21 §0.23. Claude's prior assignment was one-time and is complete; it does not reinstate the Claude route.  
**Target:** `LC518_EXPLORATORY_FEASIBILITY_PROTOCOL_DRAFT_0.2.md`, Git blob `e4cf431fe72826711ef5f2660119a19a443a87b3`, SHA-256 `fe8883fc95303158797e4c12634330d518030a23335d3b220d349487e7a01858`, 241 LF-terminated lines.  
**Population-specification basis:** `POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.21.md`, blob `8af908f6b0ad4cd060194a0a63f4914939f07756`; v0.21 and `master` are not edited by this adjudication.  
**GLM review identity as reported by GLM:** `GLM_PROTOCOL_D02_BOUNDED_REVIEW_2026-11-17.md`; SHA-256 `e681b2b05500244d8b9ce951954b51806b33f9e56d8031b993ff0e8c2a9795a1`; Git blob SHA-1 `df79d59f208bbf2718f5818d4acdc6907b61f7e8`; 27,079 bytes; 107 LF-terminated lines; final newline. The complete review text was supplied inline in the conversation. The standalone file itself was not present in this session's mounted files or conversation attachment listing when this adjudication was prepared; therefore GPT has not independently recomputed the GLM file's SHA-256, Git blob SHA-1, byte count or line count. The reported identity is retained as GLM/user-attested provenance, not GPT-verified byte identity.

## 1. Overall disposition

**ACCEPT GLM's central verdict and all nine findings.** Draft 0.2 has a coherent gate architecture and can be developed into an executable Stage A protocol without silently authorizing later stages, but the identified sequencing and precision defects must be corrected before adoption. GLM-B1 is a true predecessor-condition omission, not an editorial issue. GLM-A1–A4 are adoption-blocking clarifications. GLM-N1–N4 are accepted completeness improvements and are incorporated in the same revision.

Draft 0.3 is the current GPT working revision. Draft 0.2 remains preserved unchanged. Draft 0.3 remains document-only, inactive, unfrozen and not execution-ready until GLM completes the bounded delta review and the owner separately decides whether to adopt the exploratory route.

## 2. Finding-by-finding adjudication

| GLM finding | GPT disposition | Treatment in draft 0.3 |
|---|---|---|
| **B1: v0.21 §4.1.3 two-reviewer approval is not explicitly placed before enumeration** | **ACCEPT; blocking before GO-4 and before adoption.** The required review of the exact Stage 2 profile and manifest digest must occur before any candidate-site enumeration. The later G9 identity review cannot substitute for it. | Added G6b: after the pinned tooling and reference enumerator are materialized and hashed, two reviewers approve the exact profile manifest against the frozen Stage 1 contract before GO-3 analyser execution and before GO-4 enumeration. GO-TOOL is explicitly limited to tool acquisition/installation and reference-enumerator implementation/build; it cannot execute the analyser or inspect parent/solver source. This placement is a deliberate implementation of GLM-B1 and is submitted for GLM delta review. |
| **A1: G4/G5 catalog-schema sequence is inverted** | **ACCEPT; resolve before adoption.** Select GLM's option (a): Stage 1 schema-level requirements precede actual per-`q` catalogs. | G4 now freezes the Stage 1 contract, catalog schema/selection procedure, status taxonomy, graph model, normalization and abstract-domain adequacy criteria. G5 then defines actual per-parent/per-`q` catalogs in that already frozen schema. Any schema correction requires Stage 1 re-review and regeneration/re-freeze of affected catalogs before Stage 2. |
| **A2: assurance-adequacy conjunct is unoperationalized** | **ACCEPT; resolve before adoption.** A binary hash proves artifact identity, not static-analysis soundness. | G6 now specifies a predeclared assurance rubric covering abstract-domain invariants and transfer functions, external-summary soundness scope, binary/release identity and provenance, the frozen input contract/supported scope, and residual limitations. Named independent reviewer(s) record `ADEQUATE` or `INADEQUATE`; the latter rejects the profile. Fixture conformance and assurance adequacy are separate acceptance decisions. |
| **A3: battery is not bound to T1–T12 and misses fixture classes** | **ACCEPT; resolve before adoption.** A generic battery requirement could omit the actual adjudicated family set. | G6 explicitly binds the battery to T1–T12, each with stable ID, property, fixture source/hash, pre-fixed expected results, positive/negative cases, pass/fail rule, reviewer and report. It adds full status coverage with downstream-admission assertions; a q-invariant protection fixture producing `FAIL_Q_CONFORMANCE`; and a prehashed seeded fault set with class-coverage rationale. T11 requires every seeded defect in that declared set to be detected by at least one preassigned test. |
| **A4: three operations lack explicit authorization** | **ACCEPT; resolve before the relevant GOs.** | Split fixture-only work into GO-TOOL (pinned-tool acquisition/installation and reference-enumerator implementation/build) and GO-3 (T1–T12 and reference-enumerator comparison on prehashed synthetic/reference materials only). Neither authorizes parent-source or candidate-site analysis. GO-8 now names the post-diagnostic audit register, exact-cell membership table, derived `k_fail`, `k_unresolved`, `C_D` table, and B1/M1-si/LOPO/shortfall outputs. |
| **N1: G0 completeness ledger** | **ACCEPT.** | G0 must cross-reference every §5 criterion and §8 owner-set/UNKNOWN field, with value, evidence, responsible owner and required-before gate. No gate may pass while a value due at or before it remains UNKNOWN. |
| **N2: fixture/fault-set author independence disposition** | **ACCEPT.** | G6 records fixture and fault-set authors, profile implementer, roles/relationships, independence disposition, and any mitigation where independence is not practicable. |
| **N3: derive attainable maximum interval from actual capacities** | **ACCEPT.** | G10 records `M_min(k) = min{t ∈ Z_≥0 : Σ_j min(c_j,t) ≥ k}` and `M_max(k) = min(k, max_j c_j)` for feasible `k`, calculated from the frozen eight-stratum capacity vector. No uniform 8-by-8 or other historical capacity assumption is introduced. |
| **N4: closeout reporting home** | **ACCEPT.** | G16 explicitly requires unresolved-rate and excluded-site-class reporting and separately named static-analysis epistemic claims/non-claims. |

## 3. B1 sequencing decision and authorization interpretation

v0.21 §4.1.3 requires two reviewers to independently approve the Stage 2 profile and its manifest digest against the frozen Stage 1 contract before any candidate-site enumeration. Draft 0.2 did not schedule that approval before G8/GO-4; its G9 review occurs too late.

Draft 0.3 deliberately materializes the pinned tooling and independent reference enumerator under GO-TOOL, records their actual hashes, then finalizes the Stage 2 profile manifest. Two reviewers approve that exact digest at G6b before GO-3 executes the analyser and reference enumerator on synthetic materials and before GO-4 enumerates parent sources. GO-TOOL may not execute the analyser or reference enumerator, inspect parent or solver source, or enumerate candidate sites. This separates artifact acquisition/build from analysis execution and ensures the reviewed digest is the one actually tested. Any profile-manifest change invalidates the approval.

The later G9 two-reviewer review remains distinct: it concerns the completed candidate inventory, q identity, site signatures, source diffs and variant schedule before construction or diagnostics. The pre-enumeration profile approval and post-inventory identity review are both required.

## 4. T1–T12 and the epistemic boundary

GLM's paper assessment of all twelve test families is accepted. Draft 0.3 binds those families directly into G6 and strengthens their fixtures as recommended: automorphism-heavy canonical graphs; deterministic unordered-set serialization; normalization hazards; per-edge and unsupported-flow coverage; escape/global/callback effects; every catalog partition; strict floating-point/build-mode cases; external-summary and concurrency cases; complete status/retry evidence; search misses/extras/order; seeded analyser faults; and fresh-process/profile-separation checks.

Three epistemic limits are mandatory:

1. **Expected unresolved is not a failure** when the construct is explicitly outside the supported scope and the expected fail-closed status is returned. An unexpected unresolved result for a construct claimed as supported rejects the profile.
2. **T11 is bounded by the declared fault set.** Detection of every seeded defect in the prehashed set does not establish detection of undeclared defects or universal defect detection.
3. **Fixture conformance is not static-analysis soundness.** The battery can reveal defects and measure detection within the declared fault set. It cannot prove soundness for all programs. A separate assurance argument is required for the declared supported scope and frozen input contract. The assurance argument itself does not license soundness beyond that scope, correctness on untested constructs, or concrete program/observational equivalence.

G16 must report the positive, bounded claims separately from the non-claims: expected fixture assertions; seeded-defect detection within the hashed fault set; assurance applicability only to the declared supported scope/input contract/toolchain; and no inference beyond those limits.

## 5. Gate-order map adopted for the delta review

Draft 0.3 adopts this order:

G0 route decision/adoption and completeness ledger → G1 solver input contract → G2 source-frame freeze and GO-1 source acquisition → G3 lineage procedure and GO-2 outcome-blind parent selection → G4 Stage 1 design contract/schema/status taxonomy and independent review → G5 per-parent/per-`q` operator contract and actual catalogs → G6 provisional Stage 2 profile, normative search-predicate specification, assurance rubric and T1–T12 battery design → GO-TOOL pinned-tool acquisition/installation and reference-enumerator implementation/build on frozen specifications and synthetic/reference materials → G6b materialized profile-manifest hash and two-reviewer approval → GO-3 fixture-only T1–T12 and reference-enumerator validation execution → G7 separate fixture-conformance and assurance-adequacy acceptance → G8 parent-specific source-frame freeze and validation-record check → GO-4 parent-source candidate-site enumeration → G9 complete variant schedule/source-diff freeze and diagnostic-blind identity review → G10 diagnostic instrument/probe/input/capacity freeze → GO-5 isolation probe → GO-6 mutation generation → GO-7 solver build/run → GO-8 diagnostic execution and named audit outputs → GO-9 correctness-oracle execution/validation → GO-10 correctness evaluation → G16 closeout.

The normative candidate predicate and synthetic known-answer corpus are now frozen at G6 so the reference enumerator can be implemented and validated against the exact predicate. G8 subsequently freezes the parent-specific source frame and verifies that its predicate digest matches the G6 digest. This resolves the otherwise circular ordering between reference-enumerator validation and predicate freeze.

## 6. No authorization and no route change

This adjudication and draft 0.3 authorize no route adoption; source acquisition; parent selection; tool acquisition/installation; reference-enumerator implementation/build; fixture or enumerator execution; candidate-site enumeration; mutation allocation/generation; source modification; solver construction/build/run; isolation probe; diagnostic execution; oracle creation/validation; correctness evaluation; model fitting; simulation; or protected/development-bank access. GO-1 and GO-2, GO-TOOL, GO-3, and GO-4 through GO-10 all remain NOT AUTHORIZED.

No owner-set values have been supplied by this revision. The route remains OPEN, draft 0.3 remains inactive, and all unresolved §8 fields remain UNKNOWN until supplied and verified at their required-before gates. v0.21 and `master` remain unchanged. No source, candidate site, mutation or solver was accessed or evaluated in preparing this revision.

## 7. GLM review artifact provenance qualification

GLM reports that its canonical standalone review file is 27,079 bytes, 107 LF-terminated lines with final newline, SHA-256 `e681b2b05500244d8b9ce951954b51806b33f9e56d8031b993ff0e8c2a9795a1`, Git blob `df79d59f208bbf2718f5818d4acdc6907b61f7e8`, and that two local GLM-side copies are byte-identical. GLM further reports that the blob has never entered the published work-branch tree and that publication is by the owner, not by GLM.

The owner supplied the review text inline, including the reported identity values. The standalone file was not exposed as a mounted/current-conversation attachment to GPT in this session. GPT therefore does not claim to have independently recomputed those file-level hashes or dimensions, and this commit does not contain a reconstructed substitute. The exact GLM artifact should be added byte-for-byte from the original file when that file is actually attached to the GPT working session; do not regenerate it from the formatted inline rendering.

**Disposition:** GPT accepts GLM-B1, GLM-A1–A4 and GLM-N1–N4; draft 0.3 implements the accepted corrections and is submitted to GLM for bounded delta review. No Stage 2 profile is approved, no protocol is adopted, and no execution authorization is issued.
