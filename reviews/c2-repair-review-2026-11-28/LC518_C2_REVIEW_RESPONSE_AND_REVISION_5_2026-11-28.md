# LC518 C2 Review Response and Revision 5 Consolidation

**Date:** 2026-11-28  
**Branch:** review/lc518-c2-sequence-fixes-2026-11-28  
**Status:** Candidate for fresh Claude review. NOT ADOPTED. NOT LOCKED. NO DRAW AUTHORIZED.

## 1. Response to Claude's Revision 4 review

GPT accepts Claude's NOT ADOPTABLE verdict and the two identified design defects.

### 1.1 Post-lock sibling-OAC reroll lever: corrected

Revision 4 scanned the adoption subtree for competing OACs but did not define when the scan ended. That left a post-outcome sibling OAC capable of being treated as a pre-lock disqualifier and manufacturing NO_VALID_LOCK.

The consolidated composite now defines a hard temporal cutoff. All OAC-chain, canonical-ref, actor, and event-validity conditions are evaluated only on the complete Activity-ledger prefix ending at the first qualifying B-to-A lock push and on immutable Git objects reachable from the OAC, B, and A. Anything first appearing after that push is an audit flag only. It cannot void the lock, alter valid-lock status, or enable a successor. A valid lock permanently terminates the C2 successor chain.

The composite also fixes B as the exact OAC commit itself, whose direct master push publishes the OAC and exact adopted protocol bytes. This removes the ambiguity of selecting a later master tip.

### 1.2 Operator retry exhaustion: corrected

Revision 4's §7.2 treated a transport failure as yielding no pair selection unless the operator's retry policy succeeded. That contradicted §6.3, which allowed any party to retrieve the same round later.

The composite now says that retry policy governs only the operator's execution run. Exhausting it leaves study status NOT_YET_COMPUTED. It neither selects nor forfeits a pair and creates no right to a second draw. Any party may later retrieve the same target round from both pinned relays. The first complete, validated two-relay retrieval defines the outcome, and later complete retrievals must match exactly.

### 1.3 Permanent and run-level failure: separated

Activity API 403/429, incomplete pagination, timeouts, missing pages, and drand retrieval failures are run-level incomplete events. They do not prove absence, invalidate a lock, forfeit a result, or establish permanent NOT ASSESSABLE. Permanent NOT ASSESSABLE requires an independently reviewed, irrecoverable evidence defect and must identify the missing or contradictory objects and recovery checks.

## 2. Full replacement map for v0.7

The composite file is a complete review target. It retains v0.7 §§1–6 with the historical corrections listed below, replaces §§7–8 in full, and adds §§9–11. The original v0.7 file remains unchanged as a historical source.

| Previous v0.7 location or phrase | Revision 5 treatment |
|---|---|
| Header status line: DRAFT / NOT ADOPTED / NOT LOCKED / NO DRAW | Retained in updated form as REVIEW COMPOSITE, DRAFT, NOT ADOPTED, NOT LOCKED, NO DRAW AUTHORIZED. |
| Header owner-workflow line stating no separate per-draw preregistration/authorization | Replaced by the one immutable OAC and one valid lock authorizing one selection. The registry ID is mandatory and unresolved. |
| §1.2 final bullet stating only the prior v0.6 PASS and a final narrow v0.7 review | Replaced with the historical note that Revision 4 was NOT ADOPTABLE and this composite requires fresh review. |
| §6 paragraph saying v0.7 was submitted for a final narrow review | Replaced with the same historical correction; the exact composite hash is the only current review target. |
| §7 in its entirety | Replaced by §7.1 target derivation, §7.2 run-level retries and later-party retrieval, and §7.3 study-level states. |
| Old §7 sentence authorizing a further draw after a failed/interrupted draw | Explicitly absent from the composite. One valid lock fixes one target and one selection; failure never restores the attempt. |
| §8 in its entirety, including old items 1–5 | Replaced by exact canonical composite identity, Claude review, owner adoption via OAC, and change-control rules. |
| Old §8 item 4 requiring a whole-second UTC timestamp from a trusted clock in the owner adoption/lock record | Removed. The OAC commit fixes B; the qualifying Activity lock-push event supplies t_lock using the observed whole-second UTC grammar. |
| Old §8 item 5 asserting adoption/lock authorizes one production selection | Replaced by the more precise OAC, branch-creation, first B-to-A push, and target-round procedure in §§8–9. |
| Old final current-disposition line | Replaced by new §11, which states registry, raw Activity, drand-client, and solver limitations. |

The canonical composite SHA-256 is recorded in the external sidecar. No hash is embedded in the composite itself. A byte change requires a new sidecar digest and a fresh Claude verdict.

## 3. Other Claude corrections incorporated

- **Direct OAC publication:** the qualifying master event must be a direct push, not pr_merge or merge-queue.
- **Base commit:** B is the OAC commit identified by the direct master push event's after field; its tree contains the exact canonical composite and sidecar.
- **Actor:** pin numeric ID 116307732, login foued2, and type User. Each relevant raw Activity actor object must match.
- **Two ordering keys:** response order and strictly ascending numeric event IDs must agree; timestamps must be non-decreasing. A disagreement fails closed for that retrieval run.
- **Timestamp grammar:** accept only YYYY-MM-DDTHH:MM:SSZ. Reject offsets, fractions, invalid calendar values, and leap seconds. This is limited to the observed field format, not general RFC 3339.
- **OAC chain:** exactly one root and one non-branching successor chain. No successor after a valid lock, including a later NOT ASSESSABLE outcome.
- **Post-lock cutoff:** later events cannot invalidate the already established lock.

## 4. Activity evidence: what is and is not preserved

Claude reports observing 944 records across ten ascending pages, from 2026-10-14T09:37:43Z through 2026-11-28T10:34:48Z. It reports strictly ascending IDs, non-decreasing timestamps, no repeated second, and the actor object including numeric ID, login, and type. The repository creation time was 2026-10-14T09:37:17Z, 26 seconds before the first observed Activity record.

GPT independently retrieved the first parsed page through the connected GitHub Activity reader: 100 records, first event ID 46450944076 at 09:37:43Z, last event ID 47789198475 at 2026-10-26T06:31:00Z. The first event is master branch_creation with before represented as forty zeroes. Its actor object has id 116307732, login foued2, type User.

The normalized projection of those 100 parsed records is committed at:

evidence/ACTIVITY_PAGE1_NORMALIZED_EXTRACT_2026-11-28.json

Its SHA-256 is 14fa57a6a80515bce494178bc35a2955e5cea5f86a23074e63c86ebd94fec1e2. It is a normalized projection, not raw HTTP body bytes. It has no HTTP status line, headers, Link header, or pagination cursor. It cannot establish full-ledger completeness.

Claude reports the raw page 1 response digest 5e79ffa8661a43ebf9db80c4129be72ac8197b60b2640db5f9c6c2ce5bbfbf6e, but the raw bytes are not preserved in this repository, so that digest is not independently authenticated here. The remaining nine pages and all page headers also remain unpreserved. API retention is undocumented. The full 944-record ledger is therefore an observed result, not yet an archival evidence package.

## 5. Verifier and preservation status

The hardened Revision 3 verifier remains a GPT-authored deterministic model of the selection/rejection loop. It passed 14 checks and includes x=L−1 acceptance and two consecutive injected rejections. It is not the pinned production verifier and does not test drand, BLS, the actual HTTP client, GitHub Activity, OAC/ledger logic, or production selection.

The 475,220-byte Git bundle was locally verified and its commit lineages are reachable through the archive and preservation branches. The original bundle container is not duplicated in the repo. The 13,698-byte ZIP-labelled file remains committed only as corrupt quarantined evidence.

## 6. Current disposition

- Revision 5 composite: created, exact hash sidecar created, awaiting Claude review.
- Revision 4: preserved unchanged as the prior NOT ADOPTABLE review target.
- Registry experiment ID: unresolved; no OAC may be created.
- Raw Activity: first 100 parsed records normalized and preserved; raw bodies/headers and remaining pages outstanding.
- Actor ID and actor fields: observed in the parsed reader; raw evidence still required.
- Full 944-record chronology: reported by Claude but not preserved as raw records.
- Two-relay rule: unchanged.
- 20-push visibility study: NOT AUTHORIZED.
- No production round, seed, or pair selected.
- R2 C2 remains NOT ESTABLISHED.
- No solver construction or execution authorized.
