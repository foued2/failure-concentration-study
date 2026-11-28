# LC518 C2 sequence-fix review submission

**Date:** 2026-11-28  
**Review branch:** `review/lc518-c2-sequence-fixes-2026-11-28`  
**Current review-branch merge commit:** `29401db7c594795d53070057be561b29eb358bc6` (this README will be updated in the next branch commit)  
**Status:** Review drafts only. Not adopted, not merged to `master`, and not production authorization.

This directory contains GPT's independent sequence-fix drafts. The review branch was first created from preservation tip `6f4b6975dd956ea3303653aa3ac8f7a27be31646`, then merged with the later preservation Revision 2 commit `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`. Both histories are preserved; no force-push was used.

## Primary review path

The preferred candidate is now the preservation branch's Revision 2 design, which is included at the parent directory:

- `../LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md`
- `../README_REV2.md`

GPT's challenge and recommended disposition are in:

- `GPT_ADJUDICATION_OF_CLAUDE_REV2_2026-11-28.md`
- `CLAUDE_REVIEW_SUPPLEMENT_REV2_2026-11-28.md`

GPT prefers Revision 2's deterministic ref and first qualifying `B → A` Activity event over GPT's earlier TSA/300-second alternative. The earlier document below remains preserved as a dated alternative, not the primary recommendation.

## GPT sequence-fix source files

1. `LC518_C2_V07_LOCK_VALIDITY_AMENDMENT_DRAFT_2026-11-28.md` — earlier alternative proposing DigiCert RFC 3161 and a provisional 300-second buffer. Superseded as GPT's preferred design by the Revision 2 adjudication.
2. `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_REVISION_2026-11-28.md` — revised historical hash correction; preserves the VOID disposition.
3. `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_REVISION_2026-11-28.md` — separates commit metadata, Activity event time and public retrieval.
4. `LC518_C2_PRESERVATION_HISTORY_DISCLOSURE_DRAFT_2026-11-28.md` — disclosure/inventory of the superseded preservation commits and force-push.
5. `LC518_C2_PRESERVATION_README_SECTION_DRAFT_2026-11-28.md` — proposed addition to the preservation README; not applied to the preservation branch.
6. `CLAUDE_REVIEW_REQUEST_LC518_C2_SEQUENCE_FIXES_2026-11-28.md` — original scoped review request, supplemented by the Revision 2 review supplement.

## Evidence still outstanding

The raw Activity API bodies/headers, exact unauthenticated request URLs, selected-version behavior, complete pagination/lifecycle capture, actual RFC 3161 token validation (if that optional preservation mechanism is retained), and independent offline Git-object bundle for the superseded preservation commits and the 13,698-byte GitHub ZIP blob remain outstanding.

The proposed 300-second buffer in the earlier GPT alternative is not experimentally measured. The former 20-push visibility experiment remains NOT AUTHORIZED and does not establish Activity timestamp accuracy.

The Revision 2 README reports a 10-check verifier run, but the separate Revision 2 verifier source was not present in the inspected preservation Revision 2 Git tree. It must be committed with raw output before a source-level review can be reproduced.

## Archive note

The six-document convenience ZIP from GPT's earlier local delivery is not committed here. The individual Markdown files are the repository review sources. The ZIP is redundant packaging and earlier local/GitHub ZIP artifacts were not byte-identical; do not conflate them.

## Governance boundary

Claude review is pending. No merge to `master`, protocol adoption, production lock, production drand round, seed, pair selection, solver construction, or solver execution is authorized. The historical v0.7 protocol and VOID record remain unchanged.