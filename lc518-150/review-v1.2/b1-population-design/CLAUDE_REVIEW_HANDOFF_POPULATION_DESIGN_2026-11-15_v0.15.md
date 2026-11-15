# Claude Review Handoff: LC518 Population and Experimental Design v0.15

**Date:** 2026-11-15  
**Status:** READ-ONLY INDEPENDENT REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** gpt/b1-computational-plan-2026-11-14

## 1. Exact review target

Please review the complete v0.15 specification, including every §0 historical/provenance subsection and the full §§1–9 body:

- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.15.md
- **Branch:** gpt/b1-computational-plan-2026-11-14
- **Git blob SHA-1:** 65d64f639231434acf74db7c3fcdf841b1561baa
- **Content-changing commit:** bf378ee9d49a5a17c8177a4cea430e596c13b013
- **Dimensions:** 4 lines; final newline present.

The immediate predecessor v0.14 remains unchanged:
- **Path:** lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.14.md
- **Blob:** 5d91df2ebf84da28ab559630883702b1ecf44a01
- **Content-changing commit:** 4c40f30c91591a49869d051b6ac33334d3046c18

The v0.13 predecessor remains unchanged with blob b15c44549abaea52dc35941fd8f8e181e8f82684. The accepted predecessor artifacts remain unchanged:
- **Rev 1.4 Amendment E:** blob 3728146356a74363a94fe75a87fd06c483954ee2.
- **Rev 1.4 Amendment E acceptance record:** blob 074b40980eb96d164cd8411c8995bb1db4af0d46.
- **B1 v1.7:** blob 8c666e501a31726c728447d155045c0b20adc178.
- **B1 v1.7 acceptance record:** blob ea51d72f4f85c5d832d72add561b4c93472c364a.

Neither accepted predecessor is an execution GO.

## 2. Review history and limits of the v0.14 review

Claude's v0.14 body review covered §§1–9 in full but did not read all of the §0 history and did not independently verify repository blob identities. GPT checked the exact v0.14 blob, the v0.13 predecessor blob, the v0.14 handoff, and the v0.14 content-changing commit. GPT also found that the v0.14 history displayed §0.16 before §0.15, despite §0.15 describing the earlier v0.11→v0.12 revision.

v0.15 corrects the three Claude findings and reorders those history blocks:
- Y1: Option B is attributed to GPT's selection; Claude's earlier recommendation of Option A is retained explicitly.
- Y2: the minimum attempt-budget formula is correctly rendered as \\(A_{\max}\ge3\\).
- Y3: the §3.1 proposal wording refers to “this specification,” not to v0.5 as a current proposal.
- §0.15 and §0.16 now appear in chronological order.
- §0.13 repository provenance records the exact v0.14 blob and content-changing commit.

Do not rely on this summary in place of reading the actual v0.15 source. Check the exact identities and verify the current document's predecessor pointers, §0.1–0.18 numbering/order, decision attributions, current-version references and history consistency.

The v0.15 specification remains an **UNREVIEWED DESIGN-ONLY DRAFT**. This is a read-only review request. Do not modify the repository, generate sources or variants, allocate mutations, access diagnostic or protected banks, execute solvers, fit models, simulate, or perform scientific analysis.

## 3. Targeted recheck of Claude Y1–Y3

### Y1: Option B attribution (§5.7, first paragraph; §0.4 item 4)

v0.15 now states that excluding \\(\mathbf a(v)\\) from the primary exact-cell baseline is GPT's selection of Option B, with the realization-proxy limitation stated. It explicitly records that Claude's earlier recommendation was Option A and points to §0.4 item 4.

Review whether the corrected wording accurately represents the recorded sequence and does not imply a joint decision or consensus.

### Y2: mathematical rendering (§8 item 13)

v0.15 renders the condition as \\(A_{\max}\ge3\\). Verify that it displays correctly and matches the minimum-attempt rule in §4.1.1b and §0.17.

### Y3: historical proposal wording (§3.1)

v0.15 says “this specification proposes to operationalize” (q) as a stable mutation-operator class. Verify that this is consistent with the separate requirement for a future B1 amendment to adopt or reject that coding and does not imply that B1 v1.7 was retroactively changed.

## 4. History ordering and provenance

Please read all of §§0.1–0.18, not just the newest adjudication.

Check:
1. the headings progress consecutively and chronologically from §0.1 through §0.18;
2. §0.15 (v0.11→v0.12) precedes §0.16 (v0.12→v0.13), followed by §0.17 (v0.13→v0.14) and §0.18 (v0.14→v0.15);
3. the history preserves earlier disagreements and does not recast Claude's Option A recommendation as Option B;
4. November 6 allocation provenance remains evidence-bounded: existence and contents of a standalone artifact are unproven; allocation is not established; no statement claims it never existed; no recovery/reconstruction is claimed;
5. each predecessor blob and content-changing commit cited in the latest provenance section matches the repository;
6. the v0.14 identity is blob 5d91df2ebf84da28ab559630883702b1ecf44a01, commit 4c40f30c91591a49869d051b6ac33334d3046c18;
7. v0.15's own blob/commit identity matches GitHub and the paired review handoff;
8. accepted B1 v1.7, Rev 1.4 Amendment E and their acceptance-record identities remain unchanged.

## 5. Retry/reproducibility rule retained from v0.14

Recheck §§4.1.1b, 4.1.5(B), 4.1.6 and §8 item 13:
- (A_{\max}\ge3) is frozen in the Stage 2 profile before enumeration;
- the same attempt protocol applies uniformly to every syntactically enumerated candidate;
- each attempt uses a fresh process, the same immutable source/profile/input and exact execution environment;
- two independently initiated complete attempts must produce byte-identical canonical semantic-result envelopes;
- all attempts are logged;
- deterministic work-cap exhaustion is terminal under that profile;
- operational interruptions may be retried only within the uniform attempt budget and same environment;
- fewer than two complete results within the cap remain unresolved;
- differing completed envelopes remain UNRESOLVED / NONDETERMINISTIC ANALYSIS OUTPUT;
- no majority vote, preferred-result selection, selective retry or budget reset is allowed.

Review whether the attempt protocol remains internally consistent and whether v0.15 has introduced any drift.

## 6. Other findings accepted in v0.14

Reconfirm the following substantive findings remain correct and unchanged:

- **Lineage:** every within-cluster pair has its own direct disposition; no transitive-closure shortcut; unresolved components count zero toward verified (G_c) and cannot supply selected parents.
- **Calibration:** independent lineage units, no pair-row pseudoreplication, separate calibration/validation identities, per-category floors and predeclared confidence-interval precision requirements.
- **Serial static analysis:** one worker for semantic phases; counter totals are only comparable within the same pinned implementation/profile.
- **Floating point and external calls:** sound-model requirement, precedence of float-sensitive exclusion, conservative havoc for unknown external effects, fail-closed site-context decisions.
- **Runtime frequency:** static context equivalence is not equality of dynamic frequency or hot-path exposure.
- **Discrete concentration:** for eight strata and fixed integer (k\), (C_D=m/k\); at (k=2\), only (1/2\) and (1\) are possible before capacity restrictions.
- **Output/outcome concordance:** descriptive only; not a selection, admissibility or support gate.
- **Scientific boundary:** Option B exact-cell predictive target, realization-proxy limitation, N5 operating-characteristic interpretation, M1-si as a separate design choice, and rank-increment/shortfall protections.
- **Governance:** custodian, joint-consent, trigger-(i), isolation, new B1 amendment and separate execution GO remain open.

## 7. Full v0.15 body review required

Please re-read §§1–9 in full rather than assuming the v0.14 coverage is enough. Recheck all cross-references and current-version self-references, and pay particular attention to the corrected passages in §§3.1, 5.7 and 8. Confirm no other current/historical attribution error remains.

## 8. Required deliverable

Return a review table with:
- finding ID;
- severity: blocking, recommended, accepted or contradicted;
- exact v0.15 section;
- technical reason;
- required correction, if any;
- whether it blocks design freeze.

State explicitly which sections were read in full and which remain unread. Distinguish source findings from any inference. Do not give a whole-document verdict if any section remains unread.

## 9. Boundary

This is a read-only review. v0.15 authorizes no solver-source acquisition, parent selection, mutation allocation, mutation/source generation, compilation, execution, diagnostic probing, bank access, protected-set access, model fitting, sampling, simulation or scientific analysis.

Passing review would concern only the population/design specification. Separate statistical, computational, consent/provenance, custodian, isolation, data-access and execution gates remain in force. GPT will adjudicate the complete review. Any substantive correction after v0.15 must be a new version with its own identity and review.
