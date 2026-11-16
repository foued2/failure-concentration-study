# Claude Review Handoff: LC518 Population and Experimental Design v0.17

**Date:** 2026-11-16  
**Status:** READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** gpt/b1-computational-plan-2026-11-14

## 1. Exact review target

Review the complete v0.17 specification, including every §0 historical/provenance subsection and the full §§1–9 body.

- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.17.md
- **Branch:** gpt/b1-computational-plan-2026-11-14
- **Predecessor:** v0.16, blob 21de8a7311e0fea2fa9ac94ffb3342494c9b7a9d, content-changing commit 26e70892688cb941512de66fa2e8e39488de67f0.
- **Current v0.17 blob:** f756e9923849072be5de3cd95677fe1bee36ad92
- **Content-changing commit:** ed4432e3df837aaf7569680a2ebc3615e9b86d80
- **Dimensions:** 1,190 newline-terminated lines; final newline present.

The accepted predecessor artifacts remain unchanged:
- Rev 1.4 Amendment E: blob 3728146356a74363a94fe75a87fd06c483954ee2.
- Rev 1.4 Amendment E acceptance record: blob 074b40980eb96d164cd8411c8995bb1db4af0d46.
- B1 v1.7: blob 8c666e501a31726c728447d155045c0b20adc178.
- B1 v1.7 acceptance record: blob ea51d72f4f85c5d832d72add561b4c93472c364a.

Neither accepted predecessor is an execution GO.

## 2. Review-source correction

The owner has clarified that the review response previously represented as Claude's review was produced by an independent GLM web chat. GLM was given the Claude review handoff as its task and presented its response as though it were Claude. That response is not Claude's work. Its technical findings are recorded as GLM findings in §0.19 and must not be attributed to Claude.

This request is addressed to Claude. Please identify your review as your own work and state exactly which sections and predecessor artifacts you personally inspected. Do not rely on GLM's self-reported coverage or findings as a substitute for your own review.

## 3. Required technical review

Read the complete v0.17 specification, including §0.1–0.20 and §§1–9. In particular:

1. Verify the corrected immediate predecessor and review-source provenance.
2. Independently assess the Option B exact-cell estimand, realization-setting proxy limitation, N5 interpretation, and the separation between B1, M1-si, LOPO and outcome-side informativeness.
3. Review the parent eligibility, pairwise lineage procedure, calibration/validation independence, and the requirement that verified lineage clusters, not repository names, determine parent counts.
4. Independently challenge the §0.20 assessment of the historical 30-parent × 5-variant = 150 scenario. Determine whether the stated conclusion follows from §§2.5, 3.1–3.2 and 6.1–6.5. Do not invent between-parent variance, precision targets, support rates, or power.
5. Verify the exact-cell and M1-si support conditions, including same-parent pairs, distinct realized C_D, no pooling, and non-adaptive shortfall rules.
6. Review the static-analysis contract, target-centred context-slice equivalence, canonicalization, abstract-domain adequacy, floating-point semantics, external-call summaries, control-flow completeness, deterministic work caps and uniform rerun protocol.
7. Review protected-set requirements, custodian independence, consent provenance, trigger-(i) ratification, B1 amendment dependency, computational-plan dependency, isolation and separate execution authorization.
8. Check all cross-references, current-version references, historical attributions, equations and the complete non-authorization section.

## 4. Parent-count decision boundary

The v0.17 decision is that 30 parents is a logistics scenario only, not an adopted confirmatory operating count. The operating count remains open because the record lacks the prospective precision objective and defensible between-parent/within-parent assumptions required by §2.5.

Do not turn 30 into a confirmatory sample-size recommendation merely because 30 × 5 equals 150. If you believe a different count can be justified from the existing evidence, show the exact assumptions and derivation. If the necessary assumptions are absent, say so.

No simulation, power calculation, parent selection, candidate-frame search, source acquisition, mutation allocation, variant construction, build, execution, diagnostic probing, bank access, protected-set access, fitting, sampling or scientific analysis is authorized.

## 5. Required deliverable

Return a finding table with:
- finding ID;
- severity: blocking, recommended, accepted or contradicted;
- exact section;
- technical reason;
- required correction;
- whether it blocks design freeze.

State explicitly which sections were read in full and which remain unread. Distinguish direct source findings from inference and from checks not performed. Do not give a whole-document verdict if any section remains unread.

## 6. Review boundary

This is a read-only review. Do not modify the repository. Any required substantive correction will be made by GPT as a new version after adjudication. This handoff is not a freeze record and grants no execution authorization.
