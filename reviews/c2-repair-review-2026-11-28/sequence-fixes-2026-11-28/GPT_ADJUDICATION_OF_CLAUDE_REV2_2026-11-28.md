# GPT Adjudication of LC518 C2 Repair Revision 2

**Date:** 2026-11-28  
**Repository:** `foued2/failure-concentration-study`  
**Preservation Revision 2 commit:** `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`  
**Review-branch merge commit:** `29401db7c594795d53070057be561b29eb358bc6`  
**Status:** Independent GPT challenge and recommendation. Not an adoption record, not a canonical protocol, and not production authorization.

## 1. Executive disposition

**Revision 2 is the better primary design than GPT's earlier lock-validity amendment draft.** It addresses the central abstention/re-roll defect more directly:

- the lock ref is deterministic from the adopted protocol identity;
- the qualifying lifecycle is explicit: branch creation `0 → B`, then the first lock push `B → A`;
- the first matching `B → A` event is binding;
- later deletion, force-push, rewrite, or recreation cannot erase that original event or create a replacement draw;
- non-retrieval does not fail or void the draw; the same public target round remains binding.

The earlier GPT amendment in this review branch proposed DigiCert RFC 3161 and a fixed five-minute buffer, with the TSA token required before the target. That was a candidate, not an adopted decision. **I do not recommend carrying that version forward unchanged.** It introduces a second timing gate and fixes a numeric buffer without an established bound. Keep the file as a dated alternative for audit, but use Revision 2 as the primary candidate for Claude's fresh review.

## 2. What GPT accepts from Revision 2

### 2.1 Deterministic ref and first qualifying event

Use exactly one ref deterministically derived from the full SHA-256 of the adopted lock-protocol artifact, for example:

`refs/heads/lc518-c2-lock-<full-lock-protocol-sha256>`

The branch-creation event must establish `0 → B`; the qualifying push must establish `B → A`; and commit `A` must have exactly one parent, `B`. The lock manifest in `A` pins the adopted protocol hash, verifier/source hashes, `B`, schema/version, and algorithm identifier. It must not include the event timestamp or target round, which are derived later.

There is no operator-selected alternative ref for the same authorization. If the deterministic ref has prior or ambiguous history, the authorization is consumed and no other ref may be substituted.

This is stronger than a generic “one never-deleted ref” rule. A ref can later be deleted or force-pushed, but that does not retroactively delete the already recorded first qualifying event.

### 2.2 Post-lock tampering

The first qualifying `B → A` push remains the lock event. Later pushes, force-pushes, deletion, recreation, or other ref changes are audit violations. They must be recorded, but must not void the original lock, move its target, or permit a replacement draw.

One important refinement is still required: **a post-lock violation must not become a convenient way to suppress an inconvenient outcome.** If the original lock and target round remain reconstructable from the archived commit/tree/manifest and the public beacon, the deterministic result remains reportable, with the tampering separately disclosed. If the evidence is genuinely insufficient to reconstruct the result, the status is permanently `NOT ASSESSABLE`, with no replacement lock or draw. Do not label post-lock tampering as an ordinary “failed draw” that can disappear from the record.

### 2.3 Non-retrieval

I agree with Revision 2 that non-retrieval is not a void, not a failed draw, and not permission to move to a later round. The correct intermediate statuses are `NOT_YET_RETRIEVED` and `NOT_YET_COMPUTED`. The public target round remains fixed and may be independently retrieved and verified by another party.

A retry horizon is an operational status boundary only. Expiration must not change the target or the binding commitment.

### 2.4 Activity API and cache semantics

The raw wire response at the actual unauthenticated endpoint and selected API version is the schema authority. The reported fields `timestamp`, `activity_type`, and `actor` must not be assumed until raw bodies and headers are preserved and checked. Capture the returned selected-version header, not merely the requested version header. Fail closed on schema drift or incomplete pagination.

`Cache-Control: max-age=60` is a freshness lifetime, not timestamp resolution. Preserve `Date`, `Age`, `ETag`, `Cache-Control`, `Vary`, `Link`, `Content-Type`, `X-GitHub-Api-Version-Selected`, rate-limit headers, and all other relevant response headers. A positive response containing the event is useful evidence; an absent event is not proof of non-occurrence. Absence claims require a demonstrably fresh response and complete pagination.

The record's event time is not commit committer time and must not be called the exact HTTP receipt instant or the first-public-visibility time.

## 3. Buffer: still unresolved, and the 20-push experiment does not settle it

Revision 2 correctly removes first-public-visibility latency as a lock-validity condition. Therefore the former 20-push experiment, whose purpose was to measure first retrieval latency, is not needed to define validity and remains **NOT AUTHORIZED**.

However, a numeric `B_lock` still must be frozen before adoption. It separates the Activity event-time from the scheduled drand round. The 20-push visibility test would not establish the Activity timestamp's clock accuracy, timestamp precision, or maximum event-time error. It cannot be used to justify `B_lock`.

I do not endorse simply copying `300 seconds` from the earlier GPT draft and calling it validated. A five-minute value can be proposed as a conservative engineering guard, but it is not an established error bound. Claude should either (a) identify reliable documentation or evidence that supports a bound and a chosen margin, or (b) state that a numeric buffer remains a freeze-blocker until the event-time semantics and required safety margin are justified. The 20-push experiment should not be used as a proxy for this.

## 4. TSA selection: DigiCert RFC 3161 is optional evidence preservation, not the lock clock

For the separate question of an independent timestamp witness for the evidence-manifest hash, GPT's candidate is DigiCert RFC 3161 at:

`http://timestamp.digicert.com`

Use this only as an **additional evidence-preservation witness**, not as the source of `t_event`, not as a substitute for the Activity API, and not as a new validity cutoff. An RFC 3161 token binds a digest to a TSA-signed `genTime`, subject to the TSA's published accuracy and trust policy. It does not prove that the timestamped bytes were genuinely returned by GitHub or authenticate a historical TLS session.

The actual DigiCert TSA policy identifier, current certificate chain, signer identity, nonce, message imprint, token signature, certificate status, revocation, and time-accuracy bound must be validated in a local conformance test before relying on it. If the token is not obtained, that should not change the already established Activity event or permit a replacement lock. If used, preserve the exact manifest bytes and TSA request/response/token as companion evidence. Do not require the TSA token's arrival before the target unless Claude can justify why that additional gate cannot reintroduce an operator-controlled failure path.

References:
- RFC 3161: https://www.rfc-editor.org/rfc/rfc3161.html
- DigiCert RFC 3161 TSA endpoint and chain information: https://knowledge.digicert.com/general-information/rfc3161-compliant-time-stamp-authority-server

## 5. Additional defects or unresolved points for Claude

1. **Exact lifecycle fields:** The proposed branch-creation value `before=0, after=B` must be verified against raw live responses. Confirm the exact representation of a null/zero before SHA and whether every branch creation is represented as `branch_creation`.
2. **Actor identity:** Pin the allowed actor by stable account/user ID as well as login. “Actor preserved” is not a full acceptance rule. Decide whether a human owner or a named automation identity is permitted.
3. **No intervening lifecycle events:** State exactly which order is allowed between the `0 → B` branch creation and the `B → A` lock push. Any unexpected event consumes the one authorization; it cannot be bypassed by deleting/recreating the ref.
4. **First-event stability:** Prove the Activity endpoint returns stable IDs and the relevant complete lifecycle for the canonical ref. If the record disappears, pagination is incomplete, or the live query conflicts with the preserved raw bundle, mark `NOT ASSESSABLE`; never infer no tampering and never create a replacement.
5. **No-second-lock rule:** Deterministic ref identity is the primary control. An alternate ref is never a qualifying lock for the same authorization. If a repository-wide scan is used as corroboration, specify the precise scope, pagination, and fail-closed behavior; a partial feed cannot prove absence.
6. **Commit identity:** Confirm commit `A` has exactly one parent `B`, its tree and lock manifest are archived, and the manifest hash is computed over a canonical, non-self-referential representation.
7. **Target formula:** Preserve all timestamp precision in the raw event field. Specify the timestamp parser, UTC normalization, target round formula, and the exact rule for a round whose scheduled time equals the boundary.
8. **Post-lock tampering outcome:** A post-lock mutation must not permit an operator to censor the outcome by asking for a halt after observing the beacon. The original selection remains binding and reportable if it can be reconstructed; otherwise permanent `NOT ASSESSABLE`, no replacement.
9. **Vector Revision 2 source:** The preservation branch's Revision 2 README says the verifier was corrected and reports 10 passing checks, but the recursive Git tree at commit `4ab5ce1...` did not contain a separately named `verify_lc518_c2_v07_vectors_REV2.py`. The README says that script is in the session ZIP. Until the script and raw output are committed as source/evidence, the 10-check claim is reported, not independently rerunnable from the branch.
10. **Relay proposal is separate:** Revision 2's proposed single-valid-relay rule changes v0.7 §4/§7. It must receive a separate cryptographic review of canonical BLS encoding, subgroup membership, pinned key, message/domain, and the uniqueness assumption. Do not mix it into the lock-validity amendment or treat it as adopted. Until then, the two-relay v0.7 rule remains in force.

## 6. Recommended review sequence

1. Treat Revision 2's deterministic-ref / first-qualifying-event design as the primary candidate.
2. Keep the older GPT TSA/300-second draft as a superseded alternative, not an adopted competing rule.
3. Resolve the Activity schema and branch lifecycle values from raw wire responses.
4. Decide and freeze `B_lock` based on event-time semantics, not a visibility-latency experiment.
5. Complete local/mock conformance tests for the exact fixed-round retry and no-reroll behavior; no remote 20-push experiment is authorized.
6. Resolve whether an RFC 3161 token is a useful optional evidence seal, without making it a new outcome-dependent validity gate.
7. Submit the exact final candidate text, source verifier, and raw conformance evidence to Claude for separate PASS/NOT PASS verdicts.

## 7. Current status

- Revision 2 is the preferred candidate design, not adopted.
- GPT's earlier TSA/300-second amendment is an alternative draft, not adopted.
- The historical hash addendum and timing clarification remain review drafts.
- The original attempted v0.7 lock remains VOID FOR PRODUCTION USE.
- The 20-push experiment remains NOT AUTHORIZED.
- No production round, seed, or pair has been selected.
- No solver construction or execution is authorized.
