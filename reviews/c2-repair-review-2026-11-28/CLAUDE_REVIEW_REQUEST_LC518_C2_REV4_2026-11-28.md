# Claude Follow-up Review Request: LC518 R2 C2 Revision 4

**Date:** 2026-11-28  
**Target branch:** review/lc518-c2-sequence-fixes-2026-11-28  
**Target document:** LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV4.md  
**Status:** Fresh technical review requested. No adoption, master merge, OAC, lock, drand query, or solver work is authorized.

Please review the exact Revision 4 composite and linked evidence. Revision 3 was NOT ADOPTABLE. Do not presume Revision 4 has closed the defects.

## Separate verdicts requested

1. Study-purpose OAC fork prevention: does the full adoptions/LC518-R2-C2/ subtree enforce exactly one root and a single non-branching successor chain?
2. Registry blocker: is a pre-existing canonical root ID and sequential successor ID required? Confirm no OAC can be created until the actual registry source and commit are identified.
3. Successor state: is a successor allowed only when the predecessor is conclusively NO_VALID_LOCK? Is an unknown/incomplete predecessor barred? Does any valid lock terminate the C2 chain, including a later NOT ASSESSABLE result?
4. Whole-lifetime ref scan: does the exact ref scan from the earliest available repository Activity record catch pre-OAC events?
5. Activity chronology: does ledger order plus non-decreasing timestamps replace strict timestamp inequality? Are equal-second timestamps handled without relying on commit timestamps or assumed event IDs?
6. Branch protection: confirm Revision 4 no longer relies on an unevidenced assertion that master is protected.
7. Actor identity: review numeric user ID plus login pinning, fail-closed until raw Activity actor schema is captured.
8. Timestamp parser and buffer: review exact RFC 3339 parsing, fractional precision, offset normalization, leap-second rejection, strict target boundary, and B_lock = 300 s as a policy margin only.
9. One attempt: does the first event on the canonical ref consume the only attempt, valid or invalid?
10. Literal v0.7 section 7: review LC518_C2_V07_SECTION_7_REPLACEMENT_REV4_2026-11-28.md. Confirm deletion of the old further-draw sentence.
11. Tampering/reconstructability: confirm reconstructable outcomes remain reportable with audit-breach flag and unreconstructable outcomes become permanently NOT ASSESSABLE, without replacement draw.
12. Activity evidence: raw bodies/headers and full-history evidence remain unavailable. Confirm this remains a hard blocker.
13. Verifier: review preserved Revision 2 verifier and new Revision 3 verifier. Confirm x = L − 1 acceptance, two consecutive rejection candidates, arithmetic-only labeling, hashes, and scope.
14. Preservation: review Git bundle inventory and raw corrupt ZIP report. Confirm no unsupported claim that the ZIP is usable.
15. Relay rule: confirm v0.7 two-relay requirement is unchanged and single-relay proposal remains separate.
16. 20-push study: confirm it remains unnecessary and NOT AUTHORIZED.

For every NOT PASS, identify exact heading or sentence, blocking reason, and minimum replacement text. Distinguish design-level PASS from evidence-level PASS. Do not infer raw Activity schema, actor ID availability, complete pagination, or registry content.

## Evidence boundary

- Uploaded Git bundle: 475,220 bytes; SHA-256 df16563f0244ba1e5231d0c40504a2dc2abefd397e455f99f01162819fc5665e; six refs; git bundle verify passed.
- ZIP-labelled upload: 13,698 bytes, corrupt, no central directory; quarantined as raw evidence only.
- New Revision 3 verifier: GPT-authored, 14 deterministic checks; no drand, BLS, HTTP-client, Activity API, or production-selection test.
- Experiment ID remains unresolved.
- Raw Activity ledger and headers remain outstanding.
- No OAC, lock, production selection, solver construction, or solver execution is authorized.

Please return explicit PASS / NOT PASS per item and a top-level adoptability verdict.