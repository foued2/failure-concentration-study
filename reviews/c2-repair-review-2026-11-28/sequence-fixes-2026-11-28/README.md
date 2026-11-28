# LC518 C2 sequence fixes: review branch package

**Date:** 2026-11-28  
**Status:** Drafts for Claude review. Not adopted, not merged to master, and not production authorization.

This directory preserves the complete dated sequence-fix work as individually reviewable Markdown files. The branch was created from preservation commit `6f4b6975dd956ea3303653aa3ac8f7a27be31646`; the preservation branch and historical records are not modified.

## Review contents

1. `LC518_C2_V07_LOCK_VALIDITY_AMENDMENT_DRAFT_2026-11-28.md` — proposed replacement for v0.7 §7 and the paragraph currently at line 191.
2. `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_REVISION_2026-11-28.md` — revised historical hash correction, preserving the VOID disposition.
3. `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_REVISION_2026-11-28.md` — corrected separation of commit metadata, Activity event time and public retrieval.
4. `LC518_C2_PRESERVATION_HISTORY_DISCLOSURE_DRAFT_2026-11-28.md` — disclosure and inventory of the superseded preservation commits and force-push.
5. `LC518_C2_PRESERVATION_README_SECTION_DRAFT_2026-11-28.md` — proposed README insertion, not yet applied to the preservation branch.
6. `CLAUDE_REVIEW_REQUEST_LC518_C2_SEQUENCE_FIXES_2026-11-28.md` — scoped review instructions and unresolved technical questions.

The convenience archive `LC518_C2_SEQUENCE_REPAIR_REVIEW_PACKAGE_2026-11-28.zip` is supplied as a separate local delivery artifact, not committed as a GitHub binary. The source Markdown files are the review-of-record files in this directory.

## Important unresolved evidence

The raw Activity API body/headers, exact unauthenticated request capture, pinned wire schema, full pagination/lifecycle capture, actual DigiCert RFC 3161 token validation, and independent offline archival of superseded Git objects remain outstanding. These drafts do not represent those tasks as completed.

The proposed five-minute buffer is a fixed candidate protocol parameter, not an experimentally measured visibility bound. The former 20-push visibility experiment remains NOT AUTHORIZED and is not required by this draft's validity definition.

## Governance boundary

Claude's review is pending. No merge, adoption, production lock, production drand round, seed, pair selection, solver construction, or solver execution is authorized. The existing v0.7 protocol and VOID record remain unchanged.