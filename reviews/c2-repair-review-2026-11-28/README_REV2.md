# LC518 C2 repair packet, Revision 2

**Branch:** `preserve/lc518-c2-repair-packet-2026-11-28`  
**Base commit:** `6f4b6975dd956ea3303653aa3ac8f7a27be31646`  
**Status:** Review draft only. Not adopted, not canonical, and not production authorization.

## Revision 2 review artifact

- [Repair and Claude follow-up proposal](./LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md)
- The complete Revision 2 delivery archive is also preserved as a session artifact and is available by download from the current conversation. Its SHA-256 is `8004777f1abc5cb7391ccdadb89ddf1c93167f2213424e85b753cd8b1dbcba9b`. It contains the revised hash addendum, timing clarification, repair proposal, preservation-history note, Claude follow-up request, and corrected vector verifier. This ZIP is not represented as a GitHub blob in this branch.

## Revision 2 local artifact hashes

| File | SHA-256 |
|---|---|
| `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28_REV2.md` | `695e6020848367b20010a3b795584997b2d8069d2da48eb27f1ed070aff12e02` |
| `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28_REV2.md` | `8350c927c996fc9da166cfc4d1912d1b21b042dd26780d576f9985f280c95812` |
| `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md` | `a9e1c98b6ebbfd3bbaff305a6703ce971e9262d4dcf75ef8877c60c150b798a8` |
| `LC518_C2_PRESERVATION_BRANCH_HISTORY_NOTE_2026-11-28.md` | `1db3a8c40b884874df0b4bbc439f1222839b7696e8cb84aff702d6f96fbbcd7b` |
| `CLAUDE_FOLLOWUP_REVIEW_REQUEST_LC518_C2_REV2_2026-11-28.md` | `3baca0bc05cdb3f131e305bd7e725e714a9ac8f45692635d32e4ad521ecbf680` |
| `verify_lc518_c2_v07_vectors_REV2.py` | `491984d98c0cf5d5a3df6cf620e1f5814eaa5e3a84d29973073100fba7390bb7` |

The corrected verifier was executed on 2026-11-28: **10 checks passed**. It verifies deterministic vectors, both actual rejection/counter-advance paths using injected rejected values, and counter overflow. It does not query drand or perform a production selection.

## Revision 1 branch-history disclosure

The initial preservation branch received three pushes and then a force-push to the current Revision 1 tip. The event sequence and replaced commit IDs are documented in `LC518_C2_PRESERVATION_BRANCH_HISTORY_NOTE_2026-11-28.md` inside the Revision 2 archive. Revision 2 is being appended by ordinary fast-forward commit; no further force-push is intended.

The local PyCharm checkout remains untouched. `master` is not modified.
