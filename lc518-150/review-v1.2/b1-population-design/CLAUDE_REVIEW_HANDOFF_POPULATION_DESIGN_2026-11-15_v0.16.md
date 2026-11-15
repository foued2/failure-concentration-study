# Claude Review Handoff: LC518 Population and Experimental Design v0.16

Date: 2026-11-15
Status: READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD
Repository branch: gpt/b1-computational-plan-2026-11-14

## 1. Exact review target

Please review the complete v0.16 specification, including every §0 historical/provenance subsection and the full §§1–9 body:

Path: lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.16.md
Branch: gpt/b1-computational-plan-2026-11-14
Git blob SHA-1: 21de8a7311e0fea2fa9ac94ffb3342494c9b7a9d
Content-changing commit: 26e70892688cb941512de66fa2e8e39488de67f0
Dimensions: 1179 lines; final newline present.

The immediate predecessor v0.15 remains unchanged:

Path: lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.15.md
Blob: 65d64f639231434acf74db7c3fcdf841b1561baa
Content-changing commit: bf378ee9d49a5a17c8177a4cea430e596c13b013
Dimensions: 1,157 lines; final newline present.

The v0.14 predecessor remains unchanged with blob 5d91df2ebf84da28ab559630883702b1ecf44a01 and content-changing commit 4c40f30c91591a49869d051b6ac33334d3046c18. The v0.13 predecessor remains unchanged with blob b15c44549abaea52dc35941fd8f8e181e8f82684.

The accepted predecessor artifacts remain unchanged:

- Rev 1.4 Amendment E: blob 3728146356a74363a94fe75a87fd06c483954ee2.
- Rev 1.4 Amendment E acceptance record: blob 074b40980eb96d164cd8411c8995bb1db4af0d46.
- B1 v1.7: blob 8c666e501a31726c728447d155045c0b20adc178.
- B1 v1.7 acceptance record: blob ea51d72f4f85c5d832d72add561b4c93472c364a.

Neither accepted predecessor is an execution GO.

## 2. v0.15 review and v0.16 correction history

The supplied Claude independent review of v0.15 reports complete reading of §0.1–0.18 and §§1–9 and identifies no blocking scientific or computational defect. GPT independently fetched the v0.15 specification and paired handoff and verified their blob identities, the 1,157-line specification length, and the two-file addition-only branch delta. GPT confirmed the targeted Z1 and Z2 source defects.

v0.16 makes only these document-level corrections:

1. Z1: the two Option A/Option B decision-history pointers now reference §0.5 item 4, which contains the explicit record of Claude's Option A recommendation and GPT's independent Option B selection. §0.4 item 4 concerns the q/a operator-class fingerprint boundary.
2. Z2: all five un-delimited A_max expressions and both doubled-backslash inline-math spans identified in v0.15 have been normalized to the single-backslash \(...\) convention. The attempt rule itself is unchanged.
3. Active current-version references have been updated from v0.15 to v0.16. Historical references remain historical.
4. §0.19 records the review findings, handoff-only observations, the bounded provenance statements and the unresolved review-date metadata discrepancy.

The v0.15 handoff's incorrect '4 lines' metadata and its malformed math are not edited. v0.15 and its handoff remain immutable predecessors; the v0.16 handoff gives the verified line count and uses normalized math.

## 3. Targeted recheck requested

Please independently verify:

- The Option B wording remains accurate and non-consensual: Claude recommended Option A; GPT selected Option B; the realization-proxy limitation remains explicit.
- Both decision-history pointers now lead to §0.5 item 4, not §0.4 item 4.
- Every inline mathematical expression in the complete specification is rendered consistently with single-backslash \(...\) delimiters; identify any remaining malformed or un-delimited expressions.
- The A_max minimum remains at least three, frozen before enumeration, applied uniformly, with two independent complete byte-identical canonical semantic-result envelopes, complete attempt logging, terminal deterministic-cap treatment, bounded retries only for operational interruptions, and unresolved status when fewer than two complete results or differing complete results remain.
- §3.1 still requires a separate future B1 amendment to adopt or reject the q/operator-class coding and does not retroactively amend B1 v1.7.
- The v0.15 handoff dimensions are correctly described as a historical metadata error; do not claim that file was edited.
- §0.1–0.19 headings, chronology, predecessor pointers, all current-version references and all § cross-references are correct.
- November 6 allocation provenance remains bounded: existence and contents of a standalone artifact are unproven; allocation is not established; no claim says it never existed; no recovery or reconstruction is claimed.

## 4. Full specification review required

Read all of §0.1–0.19 and §§1–9 in full. Recheck the scientific estimand, support rules, lineage and calibration requirements, static-analysis soundness and determinism, floating-point and external-call safeguards, runtime-frequency limitation, discrete C_D arithmetic, output/outcome concordance boundary, parent-count justification, rank-increment and shortfall protections, compatibility requirements, governance gates and the complete non-authorization section.

Do not give a whole-document verdict if any section remains unread. Distinguish direct source findings from inferences and from checks you could not reproduce.

## 5. Required deliverable

Return a review table with finding ID, severity (blocking, recommended, accepted or contradicted), exact v0.16 section, technical reason, required correction and whether it blocks design freeze. State explicitly which sections were read in full and which remain unread. Verify the exact v0.16 blob and commit and the v0.15 predecessor identity. Do not modify the repository.

## 6. Review-date metadata note

The supplied v0.15 review artifact labels itself 2026-11-16, while this v0.16 handoff is dated 2026-11-15. The date discrepancy is recorded in §0.19 and is not silently resolved. Please state the source of the review artifact's date or provide verifiable timestamp context; do not alter the original review artifact.

## 7. Boundary

This is a read-only review request. Do not modify the repository, generate sources or variants, allocate mutations, acquire or modify solver source, compile or execute solvers, probe diagnostics, access banks or protected sets, fit models, sample, simulate, or perform scientific analysis.

v0.16 authorizes no such activity. Passing review would concern only the population/design specification. Separate statistical, computational, consent/provenance, custodian, isolation, data-access and execution gates remain in force. Any substantive correction after v0.16 must be a new version with its own identity and review.
