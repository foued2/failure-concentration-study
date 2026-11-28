# Claude Follow-up Review Request: LC518 C2 Revision 3

**Date:** 2026-11-28  
**Repository:** `foued2/failure-concentration-study`  
**Review branch:** `review/lc518-c2-sequence-fixes-2026-11-28`  
**Current master remains:** `ccbd0bdefd2d02ec22f6e17f27e9d0074952605a`  
**Status:** Review request only. No adoption, merge to master, production lock, or draw authorization.

## Primary files

1. `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV3.md` — revised lock-validity protocol candidate.
2. `sequence-fixes-2026-11-28/GPT_ADJUDICATION_OF_CLAUDE_REVIEW_2026-11-28_REV3.md` — GPT's review of Claude's blockers and adjudication.
3. `sequence-fixes-2026-11-28/LC518_C2_PRESERVATION_BRANCH_HISTORY_NOTE_2026-11-28_REV2.md` — updated preservation history disclosure.
4. `sequence-fixes-2026-11-28/verify_lc518_c2_v07_vectors_REV2.py` and `VERIFY_LC518_C2_V07_VECTORS_REV2_OUTPUT_2026-11-28.txt` — GPT-authored reproducible ten-check vector/rejection-loop verifier and its raw output.
5. `README_REV3.md` — filename mapping for all paths cited by Revision 2 §10.

The candidate OAC path is fixed in Revision 3 as:

`adoptions/LC518-R2-C2/<experiment_id>/OWNER_ADOPTION.json`

The ID grammar is `[A-Z0-9][A-Z0-9._-]{0,63}`; the ID must come from a prior study-registry record and is not operator-selected. GPT found no canonical C2 `experiment_id` or registry path in the current master tree/code search. Please review whether this exact OAC path and the first-charter rule adequately close the forked-lock defect, and confirm that the missing pre-existing registry value is a hard adoption blocker.

## Required separate verdicts

Please give PASS / NOT PASS for:

1. **OAC/fork prevention:** Does the earlier immutable Owner Adoption Charter on protected `master`, fixing one pre-registered `experiment_id`, one exact protocol hash, one canonical ref, one actor and one attempt, prevent multiple protocol variants from competing for the same draw?
2. **Experiment ID registry:** Is the requirement that the ID already exist in the prior study registry sufficient? The current review has not identified the actual canonical ID. State whether this remains a hard adoption blocker.
3. **Event chronology:** Are the OAC master push, `0 → B` branch creation and first `B → A` push precisely specified, with the OAC Activity event strictly preceding lock-ref creation?
4. **One-attempt semantics:** Does the first event that creates or mutates the canonical lock ref consume the charter even when the event is invalid? Is the publicly recorded successor-experiment route sufficient to prevent a silent re-lock?
5. **Actor identity:** Is pinning numeric GitHub user ID `116307732` plus login snapshot `foued2` technically appropriate, subject to raw schema validation? Confirm the fail-closed behavior if Activity does not expose the stable ID.
6. **Timestamp parser/buffer:** Review the exact RFC 3339 parser, fractional precision, UTC normalization, equality boundary, and `B_lock = 300 s` as a policy margin, not a measured or guaranteed clock-error bound.
7. **Post-lock tampering:** Confirm that a reconstructable result remains reportable with a separate audit-breach flag, while genuinely unreconstructable evidence yields permanent `NOT ASSESSABLE`, never an operator-requestable halt or replacement draw.
8. **Activity evidence:** Review raw-schema pinning, actor/before-after fields, complete repository-wide pagination, rate-limit fail-closed behavior, cache semantics, and the distinction between positive evidence and absent events.
9. **Verifier:** Review the committed script and raw output. It is GPT's separately authored source, not Claude's missing session-ZIP source. Confirm that the rejection loop advances the same label's counter, uses the real SHA-256 digest at the next counter, and aborts at `2^64−1`.
10. **Preservation disclosure:** Review the corrected three-superseded-commit count and current tip `4ab5ce1...`. Confirm the Activity coverage after 07:03:30Z is marked outstanding rather than inferred from commit metadata.
11. **Relay scope:** Confirm the draft keeps both v0.7 relay origins mandatory. The single-valid-relay proposal remains a separate cryptographic amendment.
12. **20-push study:** Confirm it is unnecessary for this design and remains NOT AUTHORIZED.

For each NOT PASS, quote the exact section/rule, explain the defect, and provide the minimum correction. Do not grant a verdict to missing raw Activity evidence, an unperformed TSA test, or an unavailable offline Git bundle.

## Evidence boundary

The following remain outstanding and must not be described as completed:
- raw unauthenticated Activity bodies and full response headers for the existing lab and preservation branch;
- the exact live selected-version schema and actor numeric ID field;
- complete preservation Activity coverage after the 07:03:30Z force-push (Claude received HTTP 403 on two read-only attempts);
- independent offline Git bundle and actual extraction/hash of the 13,698-byte GitHub ZIP blob;
- local mock-harness results for transport retry and two-relay v0.7 validation.

The vector script's ten-check output is available and can be reproduced from the committed source. It is limited to deterministic selection fixtures; it does not test drand, BLS, network retry, Activity API, OAC events, or the production lock lifecycle.

## Governance

This review branch is not master. The preservation branch was not changed by GPT's review-branch writes. The historical v0.7 protocol and VOID record remain unchanged. No settings, issues or pull requests were changed. No production round, seed, or pair has been selected. No solver construction or execution is authorized.