# Claude Follow-up Review Request: LC518 C2 Revision 5 Composite

**Date:** 2026-11-28  
**Branch:** review/lc518-c2-sequence-fixes-2026-11-28  
**Canonical composite:** LC518_R2_C2_SELECTION_PROTOCOL_REV5_COMPOSITE_2026-11-28.md  
**Composite SHA-256:** 8b5c670edc853acb15dab045f174153cc7253efa55d342b48e8184eab59815ea  
**Sidecar:** LC518_R2_C2_SELECTION_PROTOCOL_REV5_COMPOSITE_2026-11-28.sha256  
**Status:** Fresh technical review requested. No adoption, master merge, OAC, lock, drand query, or solver work authorized.

Revision 4 was NOT ADOPTABLE. Please review the exact canonical composite bytes identified above, not the standalone Revision 4 memo or the historical v0.7 source. Confirm that the checked-in sidecar digest matches the exact file bytes.

## Separate verdicts requested

1. **Post-lock cutoff / retroactive reroll:** Does the rule that all §§9.1-9.4 validity checks use only the complete Activity-ledger prefix ending at the first qualifying B-to-A push, plus immutable objects reachable from OAC/B/A, close the sibling-OAC lever? Confirm post-lock events can only create an audit flag and cannot void the lock or enable a successor.
2. **Single chain:** Does the full adoptions/LC518-R2-C2 subtree enforce exactly one root and a single non-branching successor chain? Is a successor allowed only after complete proof of NO_VALID_LOCK, and forbidden after any valid lock including NOT ASSESSABLE?
3. **Base commit:** Is B correctly fixed to the OAC commit itself, identified by the direct master push event's after field, with the exact composite bytes and sidecar present in its tree?
4. **Event type:** Is a direct Activity push on refs/heads/master correctly required for OAC publication, excluding pr_merge and merge-queue events?
5. **Actor:** Review numeric ID 116307732, login foued2, type User, requiring every raw relevant actor object to match. Distinguish parsed observation from preserved raw evidence.
6. **One-attempt semantics:** Does the first event on the canonical ref after the OAC consume the only attempt, valid or invalid?
7. **Two ordering keys:** Does requiring exact response order and strictly ascending numeric IDs to agree, with timestamps non-decreasing, provide a proper fail-closed rule? Are the event IDs treated only as a consistency check rather than an undocumented guarantee?
8. **Timestamp grammar:** Review the narrower exact YYYY-MM-DDTHH:MM:SSZ grammar, invalid-date and leap-second rejection, and integer UTC parsing. Does it appropriately avoid untested offset/fraction paths?
9. **B_lock and target:** Review the 300-second policy margin (not a bound) and strict target inequality.
10. **§7.2 retry semantics:** Confirm operator retry exhaustion only creates a run-level incomplete record and leaves study status NOT_YET_COMPUTED, without forfeiture or replacement draw. Confirm any party can retrieve the same round later and all complete validated retrievals must match.
11. **§7.3 permanent status:** Is permanent NOT ASSESSABLE restricted to irrecoverable, independently reviewed evidence defects, not operator timeouts/rate limits/retry exhaustion?
12. **§8 review/adoption procedure:** Confirm the new exact-composite hash, external sidecar, fresh review on any byte change, OAC adoption record, and no OAC until the registry ID is located.
13. **Complete v0.7 replacement map:** Review the explicit treatment of the old header status, owner-workflow line, §1.2 and §6 review-status statements, full §7 replacement, and full §8 replacement. Confirm the former §8 item 4 trusted-clock timestamp rule is no longer operative.
14. **Activity evidence:** Claude reports 944 records and ten pages; GPT preserved only a normalized parsed projection of the first 100. Confirm the composite accurately states that full raw records/headers and the remaining pages are outstanding, and does not claim a raw capture.
15. **Verifier:** Confirm the 14-check verifier is correctly described as GPT's deterministic model, not the pinned production verifier/client.
16. **Preservation:** Confirm archive/preservation branch history and corrupt ZIP are described accurately.
17. **Relay scope:** Two-relay rule remains unchanged; single-relay proposal separate.
18. **20-push study:** remains unnecessary and NOT AUTHORIZED.

For each NOT PASS, identify the exact section and minimum replacement text. Distinguish design-level PASS from evidence-level PASS. Please return a top-level adoptability verdict and state the exact SHA-256 reviewed.

## Evidence boundary

- The connected GitHub Activity reader returned one parsed page of 100 events. The normalized projection and its SHA-256 are committed.
- The 944-record ten-page report and raw page 1 SHA-256 were reported by your prior review, but the raw pages and headers are not yet preserved as repository files.
- No drand query, TSA query, OAC creation, lock, production selection, R2 adoption, or solver operation is authorized.
