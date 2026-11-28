# LC518 R2 C2 Repair and Lock-Validity Proposal, Revision 4

**Date:** 2026-11-28  
**Status:** Consolidated candidate for independent Claude review. Not v0.11. Not adopted. Not a canonical composite. No production selection is authorized.  
**Predecessor:** Revision 3 at `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV3.md`. Revisions 2 and 3 are preserved unchanged.

## 1. Revision 4 purpose and decision

Revision 4 addresses Claude's latest review of Revision 3. Claude accepted the deterministic verifier and preservation disclosure, confirmed the experiment-registry blocker, and found Revision 3 NOT ADOPTABLE.

This revision corrects the remaining design defects: it requires one root OAC and one non-branching successor chain across the entire C2 study-purpose subtree; uses complete Activity-ledger order plus non-decreasing timestamps rather than strict timestamp inequality; scans the canonical ref's full lifetime, including before the OAC; makes successor eligibility depend on the predecessor's objectively established state; and supplies the complete replacement for v0.7 section 7, expressly deleting the further-draw sentence.

A separate GPT-authored verifier adds the x = L − 1 acceptance test and two consecutive rejected-candidate execution. The arithmetic-only check is distinguished from loop behavior.

Revision 4 does not resolve the experiment ID or missing raw Activity evidence. It is a corrected review candidate, not an adopted protocol or authorization.

## 2. One experiment charter precedes the lock

### 2.1 Pre-existing experiment identity

Before any lock-ref event, an immutable Owner Adoption Charter (OAC) must exist as a publicly recorded commit on master. Its one canonical path is:

adoptions/LC518-R2-C2/<experiment_id>/OWNER_ADOPTION.json

The experiment_id must match the pre-existing study-registry value and grammar [A-Z0-9][A-Z0-9._-]{0,63}. The OAC must cite the registry source path and commit that pre-register the ID. The current reviewed materials still do not identify the canonical C2 registry entry; no OAC can be created and no ID may be invented or selected by the operator.

The OAC fixes, in canonical machine-readable form: study-purpose key LC518-R2-C2; one registry-issued experiment_id; one exact adopted lock-protocol SHA-256; one canonical lock-ref path; one base-commit rule; one attempt; one allowed actor's stable GitHub numeric user ID and login snapshot; exact verifier/source hashes and algorithm identifier; and root/successor position with predecessor identity and terminal state when applicable.

The OAC is immutable. Its commit identity is the exact after SHA in the qualifying master Activity push event that first adds the charter file. It is never edited in place. Corrections are governed only by §2.2. The OAC must be an ancestor of the lock base commit and its exact push event must appear in the complete Activity ledger. This design does not rely on an unverified claim about branch-protection settings. Commit author/committer timestamps are not substitutes for Activity records.

### 2.2 One root and one non-branching successor chain

The entire reserved subtree adoptions/LC518-R2-C2/ represents one study purpose. It must contain exactly one root OAC, whose predecessor fields are null, followed only by zero or more successors that each name exactly one immediate predecessor. No second root, sibling successor, parallel branch, alternative charter, or competing protocol variant is permitted. The complete set of OACs must form one directed path. Every ID must be unique and registry-issued, and every successor must cite its predecessor OAC commit and mechanically determined terminal state.

A successor in this C2 chain is permitted only when the predecessor is conclusively NO_VALID_LOCK. That state requires complete Activity and Git evidence establishing that the predecessor's one attempt was consumed or closed without ever forming a valid lock. An invalid first attempt can qualify, but only after NO_VALID_LOCK is independently established and publicly recorded.

A successor is forbidden after any valid lock, whether or not the beacon was retrieved, whether or not the result is later NOT ASSESSABLE, and whether or not the ref is later deleted, rewritten, force-pushed, or recreated. It is also forbidden when the predecessor's evidence is incomplete and valid-lock presence cannot be determined. Unknown is not NO_VALID_LOCK.

A valid lock permanently ends the C2 successor chain. A later study motivated by a protocol deviation must be a distinct prospective study under a different study-purpose key, with separate review and explicit disclosure of the prior lock, result/status, and deviation rationale. It cannot be called a successor or replacement draw and cannot suppress or substitute for the earlier result.

The verifier must scan the complete master-tree history and repository-wide push ledger for every addition, edit, move, and deletion under this subtree. Any OAC outside the single root-to-successor path disqualifies the attempted adoption. This is a state-based rule, not an assessment of operator intent.

### 2.3 OAC publication order

The root OAC must be committed to master before any event on the canonical lock ref. A successor OAC may be added only after §2.2 permits it. A third party verifies that the OAC file is in the master tree; its exact commit SHA is identified by the master push event's after field; the complete Activity ledger orders that push before any canonical lock-ref event; the OAC is an ancestor of base B; all OAC fields match the lock manifest; and the OAC belongs to the one root-to-successor chain.

The event sequence is established by the complete, pinned Activity ledger and Git ancestry, not by requiring distinct whole-second timestamps. Event timestamps must be non-decreasing in ledger order, with equality allowed. A minimum gap may be required operationally but is not a validity condition.

If the OAC event cannot be identified, event order is ambiguous, the complete earlier ref history is missing, or the OAC is not an ancestor of B, no valid lock can be established.

## 3. Canonical lock ref and the single lock attempt

### 3.1 Ref identity and full-lifetime exclusion

The OAC fixes the canonical ref, derived from the pre-registered experiment ID and not from a protocol hash:

refs/heads/lc518-r2-c2-lock/<experiment_id>

No alternate ref qualifies. The exact canonical ref must have no event before the OAC push. The verifier scans that ref's entire lifetime from the earliest available repository Activity record, not only the OAC-to-lock interval. Any pre-OAC creation, push, deletion, recreation, or other event disqualifies it. If complete prior history cannot be established, absence of an earlier event is unproved and no lock is valid.

The complete repository-wide Activity ledger must also be scanned for all events in the reserved lc518-r2-c2-lock/ namespace and all additions, edits, moves, and deletions under adoptions/LC518-R2-C2/. It must prove one OAC chain, no alternate ref, no parallel charter, and no extra attempt. An incomplete page, inaccessible range, rate limit, or unverified pagination means absence of competing activity is not established. The ref must be absent immediately before the one attempt; a current branch lookup alone is insufficient.

### 3.2 Allowed actor

The OAC pins both the stable GitHub numeric user ID and the login snapshot of the one authorized actor. The repository owner currently resolves to numeric user ID `116307732` and login `foued2`; this observed identity may be used as the proposed OAC value, subject to owner confirmation in the actual charter.

The Activity actor on the OAC push, lock-ref creation, and qualifying lock push must expose and match the pinned numeric ID and login. The numeric ID is the identity key; the login is also checked against the OAC snapshot and preserved as a human-readable identifier. If the live Activity schema does not expose the required stable actor ID, or if identity cannot be reconciled, fail closed. Do not substitute commit author/committer strings for the Activity actor.

No bot, application, collaborator, alternate user, or second actor may create the OAC or perform the lock lifecycle unless the OAC explicitly authorizes that identity before any lock activity. This draft authorizes one actor only.

### 3.3 Required lifecycle and ledger ordering

Let B be the exact master tip selected under the OAC base-commit rule after the OAC push. The OAC commit must be an ancestor of B and the complete ledger must establish that the canonical ref had no prior event.

The qualifying lifecycle is:
1. OAC push: a master push event whose after field identifies the OAC commit and whose tree contains the immutable OAC and exact protocol hash.
2. Canonical ref creation: a branch-creation event on the exact ref with before = 0, or the exact null/zero representation established by raw schema evidence, and after = B.
3. Lock push: the first subsequent push on that same ref with before = B and after = A, where A has exactly one parent B.

The complete, pinned Activity ledger must place those events in that causal order. Use the fully paginated response sequence under a pinned request and schema. Do not reorder events using commit author/committer dates, local wall-clock observations, or guessed event IDs.

Their timestamps must be non-decreasing in ledger order:

t_OAC ≤ t_create ≤ t_lock

Equal whole-second values are permitted. Ledger sequence and Git ancestry establish the order when timestamp values are equal. A minimum gap may be an operating procedure, not a validity rule. Any extra event on the canonical ref between creation and first lock push disqualifies the lifecycle. If before = 0 is ambiguous, event order cannot be reconstructed, or timestamps decrease, this lifecycle cannot qualify.

Commit A contains a lock manifest pinning the OAC commit, study-purpose key, experiment ID, protocol hash, exact ref, base B, actor ID/login, verifier/source hashes, schema version, and selection algorithm. It must not contain t_lock or the target round, which are derived from the Activity lock-push event.

### 3.4 First attempt consumes the charter

The first event that creates or mutates the canonical lock ref after the OAC starts and consumes the one permitted attempt, valid or invalid. This includes an existing ref or any pre-OAC event; wrong before/after; wrong actor; wrong parent or manifest; an intervening/extra event; or inability to establish schema, event order, or complete ref history.

There is no second ref, replacement push, second OAC under the same ID, parallel root, or alternate protocol hash under the same study-purpose key. An invalid attempt consumes the charter. A successor is allowed only when complete evidence establishes NO_VALID_LOCK. An incomplete ledger cannot establish NO_VALID_LOCK. Once any valid lock forms, no successor in the LC518-R2-C2 chain is permitted, even if later evidence is unavailable and the result becomes NOT ASSESSABLE.

## 4. Activity API evidence, schema, and absence

The raw wire response from the exact unauthenticated GitHub endpoint and server-selected API version is the schema authority. Reported fields id, node_id, before, after, ref, timestamp, activity_type, and actor are not pinned until raw body bytes and complete headers are captured and checked.

Before adoption preserve: exact request URL/query and request headers; requested and selected API versions; redirects and response URL; raw body bytes and all headers for every page; Date, Age, Cache-Control, ETag, Vary, Link, Content-Type, Retry-After and rate-limit headers; every pagination page and server-provided next URL while HTTPS on api.github.com; the complete repository-wide feed for the canonical ref's whole lifetime including before the OAC; every push touching the reserved OAC subtree; the raw actor object and stable numeric ID; response SHA-256 values and canonical evidence manifest.

Set time_period, direction, and per_page explicitly. Pin the request order and preserve every page as returned. The required history must extend to the earliest relevant Activity record. If API retention cannot cover that lifetime, or the complete scan cannot be obtained, the protocol cannot prove the absence of pre-OAC or competing events. The attempt is NOT ASSESSABLE and no successor may proceed.

A 403/429, rate-limit response, missing page, partial response, inaccessible page, or truncated feed is not an empty result. The verifier must fail closed.

Cache-Control: max-age=60 is a freshness lifetime, not timestamp resolution. Record Age and cache headers. A positive response containing an exact event proves that it was represented in that response/cache chain. An absent event proves nothing unless the retrieval is demonstrably fresh, unfiltered as required, covers the entire history, and is completely paginated. The Activity timestamp is an event-time field, not commit time, HTTP Date, or first-public-visibility time.

## 5. Timestamp parser and target-round rule

### 5.1 Timestamp parsing

Parse the exact raw event timestamp field pinned by the live-schema qualification. The accepted grammar is RFC 3339 date-time with an explicit timezone (`Z` or numeric offset) and optional decimal fractional seconds. Preserve all fractional digits from the raw value; normalize offsets to UTC using exact integer/decimal arithmetic, never binary floating point. Reject a missing timezone, malformed date/time, unsupported precision, leap-second notation unless separately specified and tested, or a value that cannot be parsed losslessly.

Store both:
- the exact raw timestamp string and source field name; and
- its exact normalized UTC value used in the calculation.

A Unix-second conversion may be stored as a derived integer/decimal representation, but must not truncate fractional seconds or round down.

### 5.2 Fixed policy buffer

Set:

`B_lock = 300 seconds`.

This is a fixed **policy margin**, not a measured visibility percentile and not a documented upper bound on GitHub's event-clock error. The 20-push first-visibility experiment is not needed to define this rule and remains **NOT AUTHORIZED**. It would measure observation latency, not the maximum lag or clock accuracy of the Activity event timestamp.

The use of a five-minute margin expresses the study's chosen separation from the server-recorded event time. It does not establish a cryptographic or contractual guarantee that GitHub's event clock can never lag true UTC by more than five minutes. The protocol must state this as a trust assumption/limitation. If the study requires a formally bounded server-clock error rather than a disclosed policy margin, the Activity API cannot be adopted as the sole time source without additional authoritative evidence.

### 5.3 Target formula and equality boundary

For the pinned Quicknet schedule:

`T_r = genesisTime + period × (r − 1)`.

Let `t_lock` be the exact UTC normalized Activity event timestamp for the first qualifying `B → A` push. The target round is the smallest integer `r ≥ 1` satisfying:

`T_r > t_lock + 300 seconds`.

The comparison is strictly greater. If a round's scheduled time equals the cutoff exactly, that round is not the target; use the next round. The parser must use the full precision preserved under §5.1. The OAC protocol hash and experiment ID are fixed before the event; the target is mechanically determined by the event timestamp and chain constants.

This target derivation does not depend on when the operator or any independent observer first retrieves the Activity record. Visibility delay is operational, not a validity criterion.

## 6. Post-lock ref mutation and reconstructability

### 6.1 Later mutations never erase the lock

After the first qualifying `B → A` event, later ref deletion, force-push, rewrite, same-name recreation, or additional push is a post-lock audit violation. It cannot retroactively erase the original Activity event, void the lock, move the target round, or permit a replacement draw.

The protocol must not use an operator-requested `FORFEIT / HALT` as a way to suppress an inconvenient result after the beacon is known. A post-lock mutation is recorded alongside the selection status.

### 6.2 Result remains reportable when reconstructable

If a third party can reconstruct all of the following:
- the prior OAC and exact adopted protocol hash;
- the first qualifying Activity `B → A` lock event;
- commit `A`, its tree, the lock manifest and all pinned source bytes;
- the exact target round under §5;
- the target beacon response(s) and the required v0.7 cryptographic validation;
- the deterministic seed and pair-selection calculation;

then the deterministic pair result remains reportable even if later ref tampering occurred. Report the result together with a separate `POST-LOCK AUDIT BREACH` flag and the full tampering chronology. Do not suppress a reconstructable outcome because the operator, owner, or reviewer requests a halt after seeing it.

### 6.3 Permanent NOT ASSESSABLE when reconstruction is impossible

If required evidence is genuinely unavailable, incomplete, inconsistent, or cannot be independently validated, mark the selection permanently `NOT ASSESSABLE`. This status is evidence-determined, not operator-discretionary. It never grants a new lock, a replacement round, or a new draw under the same experiment ID. Any successor experiment must follow §2.2 and be separately reported.

Non-retrieval alone is not invalidity. Until a party retrieves and validates the target beacon, status is `NOT_YET_RETRIEVED` or `NOT_YET_COMPUTED`. Any party may retrieve and independently compute the same fixed target round. A client timeout, missed local retry horizon, or failure to run code cannot change the target or make the original charter available again.

## 7. Proposed complete replacement for v0.7 section 7

The following is the complete proposed replacement for the current v0.7 section 7. The current v0.7 file is not modified by this review draft.

### 7.1 Prospective target and one-selection authorization

This draft is not draw authorization. Only after Claude gives a scoped technical PASS on the exact final protocol and its evidence may the owner adopt it and create the one OAC authorized by the pre-existing registry. Under the owner's previously stated process decision, that adopted OAC and its one valid lock authorize exactly one production selection. A reviewer PASS or this draft does not itself authorize a selection.

For pinned Quicknet, round r is scheduled at T_r = genesisTime + period × (r − 1). Let t_lock be the exact, losslessly parsed UTC Activity timestamp of the first qualifying B → A lock-push event. Let B_lock = 300 seconds, the policy margin in §5. The target is the smallest integer r ≥ 1 satisfying T_r > t_lock + B_lock. The comparison is strictly greater; a round exactly at the cutoff is excluded. No person selects a round after seeing a beacon. Do not use round 1, stopped round 34323983, a fixture, or a previously observed round as the production target.

One valid lock fixes one target round and one selection attempt. It does not authorize a second round, replacement lock, seed, or pair. Never substitute /latest, a later round, another chain, or a manually selected round.

### 7.2 Two-relay retrieval and same-round retries only

Query exactly the derived target round from both pinned relay origins. Apply the full v0.7 identity, encoding, BLS, randomness-consistency, and relay-agreement checks independently to both responses. Both pinned relays must return the exact round and pass all prescribed checks before computing the seed or pair. The two-relay rule is unchanged; the single-valid-relay proposal remains separate and unadopted.

Every permitted transport retry requests the same pinned chain and exact same target round. Retry classes, schedule, timeout, and terminal horizon must be frozen before OAC/lock and tested against the actual client in separate local mock-conformance work. No post-lock discretion may extend the target, substitute a relay, use a later round, alter labels or universe, reroll a pair, or replace a result.

One valid relay is insufficient. A transport failure, invalid response, signature failure, or disagreement yields no pair selection unless the fixed same-round retry policy obtains two valid agreeing responses. Exhausting that policy does not authorize another draw. The lock and target remain unchanged.

### 7.3 Terminal statuses and no replacement draw

Before target retrieval and validation, report NOT_YET_RETRIEVED or NOT_YET_COMPUTED. These are work states, not failed draws.

If all evidence permits independent reconstruction of OAC, valid lock, target, both relay responses, cryptographic validation, seed, and calculation, report the result. If required evidence is genuinely incomplete, unavailable, inconsistent, or cannot be independently validated, report permanently NOT ASSESSABLE. Failed or interrupted retrieval never permits a replacement target or second lock.

**The following sentence in the current v0.7 section 7 is deleted and must not remain in the operative protocol:**

> A failed or interrupted draw does not yield a pair selection; a further draw requires a new owner adoption/lock event under an appropriately reviewed protocol version.

The replacement rule is: one valid lock fixes one target and one selection only. Failure or non-assessability never restores the attempt or authorizes a replacement draw. A C2 successor is possible only where the predecessor never formed a valid lock under §2.2, and is not a reroll of an existing valid lock.

Retain lock event, target, both relay requests/responses, validation results, seed, digest/counter path, indices, selected pairs if any, statuses, and hashes.

A successful pair selection authorizes no R2 adoption, allocation acceptance, parent-source construction, solver construction/evaluation, Rev11 amendment, publication, or scientific claim. Those decisions remain separate.

## 8. Evidence preservation and optional timestamp sealing

At lock time, archive the raw Activity request/response capture, all pages and headers, matching ref/commit objects, OAC, lock manifest, commit/tree/blob bytes, parsed validation report, and SHA-256 hashes.

An RFC 3161 TSA token (DigiCert may be used) is optional additional preservation evidence for the SHA-256 hash of the canonical evidence manifest. It is not the source of `t_lock`, not a validity condition, not a replacement for the Activity API, and not proof that the timestamped bytes were returned by GitHub. Failure to obtain a TSA token does not void an otherwise valid lock or authorize a replacement. If used, preserve the manifest bytes, exact TSA request/response/token, nonce, message imprint, signer certificate, chain, policy and validation output. Do not require token arrival before the target.

GitHub's Activity API is not assumed immutable or permanently retained. The capture is a contemporaneous preservation copy; later public re-query provides corroboration. If the API record is no longer available and the captured source cannot be independently trusted or reconciled, apply §6.3. Never assert that a local archive alone authenticates a historical TLS response.

## 9. Branch-history, archive, and document corrections

The preservation branch points to 4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21, a normal child of 6f4b6975dd956ea3303653aa3ac8f7a27be31646. The three superseded commits are a0f1ba90b92457bfaa43c3ec68c754578243cb0e, 0e6c47b26959019cafc6e11eb04e5f7e19a037dd, and e0cddeacc7ea3ff17477708ec3470f71c8ee476b. Base 24e973f... and retained force-pushed tip 6f4b697... are not superseded.

The uploaded Git bundle is 475,220 bytes, SHA-256 df16563f0244ba1e5231d0c40504a2dc2abefd397e455f99f01162819fc5665e, Git blob SHA-1 570dbd11f4ebb1591d855b8c27505e59118efc33. git bundle verify passed and reports six refs. This preserves Git objects/refs, not missing GitHub Activity records.

The uploaded 13,698-byte ZIP-labelled file has SHA-256 52792b86a7b8f7e656302db477a09ffbb915d3d42f2a38341d1c818c96443189 and Git blob SHA-1 b5998912ff9fcee8584ada76ebd370128ba8f6b2. It is corrupt: standard ZIP readers report the end-of-central-directory record is absent and no central-directory records can be enumerated. Preserve it only as quarantined raw input, not a usable archive. The earlier claim that members of this exact upload were decompressed is withdrawn because it could not be reproduced. Claude independently classified the extracted blob as corrupt.

Activity coverage after the reported 07:03:30Z force-push remains outstanding. The 07:54:01Z value in 4ab5ce1 commit metadata is a Git commit timestamp, not an Activity push-event time. The raw Activity feed and its completeness remain unresolved.

The parent README.md is the single entry point for current material. Revisions 2 and 3 remain unchanged. README_REV3.md retains historical filename mappings.

## 10. Former 20-push visibility experiment and local verifier

The 20-push Activity visibility experiment is unnecessary for this candidate validity rule and remains NOT AUTHORIZED. The target is derived from t_lock + B_lock; the experiment would not establish the Activity timestamp's maximum clock lag.

The Revision 2 verifier and its output remain unchanged. A separately authored Revision 3 verifier adds Claude's hardening suggestions: x = L − 1 acceptance for both universe sizes; two consecutive injected rejection candidates followed by the real SHA-256 candidate at counter 2; and an explicit arithmetic-only label for the threshold calculation.

The new verifier covers deterministic vector/rejection-sampling behavior only. It does not query drand, verify BLS, exercise the actual HTTP client, inspect Activity records, create refs, or perform a production selection. Its source and raw output are separately identified in the packet index.

Remaining work before adoption: identify the pre-existing C2 registry ID; capture raw Activity request/response bytes and headers; verify selected version, actor, before/after schema, filtering and full pagination; implement locally reproducible OAC/chain/ref/chronology checks; test the actual pinned drand client with local mocks; and complete read-only preservation-branch Activity coverage after 07:03:30Z. A disconnected mock imitation is not a test of the actual client.

## 11. Freeze blockers and required Claude verdicts

This design remains NOT ADOPTABLE until:

1. the exact pre-existing canonical root experiment_id is identified in the study registry;
2. the complete adoptions/LC518-R2-C2/ subtree is shown to contain exactly one root and only one state-eligible non-branching successor chain;
3. raw unauthenticated Activity response bodies/headers establish selected API version, actor object, and before/after fields;
4. complete repository-wide pagination covers the canonical ref's entire lifetime, including pre-OAC events and all OAC/lock namespace changes, failing closed on 403/429, missing pages, or incomplete history;
5. ledger record order establishes OAC → ref creation → first B→A push, with non-decreasing timestamps and equality allowed;
6. the actual Activity actor object exposes the pinned stable numeric ID and login;
7. B_lock = 300 s is reviewed as a policy margin, not a measured bound or clock guarantee;
8. exact RFC 3339 parsing, fractional precision, timezone normalization, leap-second rejection, and strict target equality are approved;
9. invalid attempts consume their OAC; a successor is possible only after proven NO_VALID_LOCK; any valid lock terminates the C2 chain even if the result later becomes NOT ASSESSABLE;
10. the full v0.7 section 7 replacement in LC518_C2_V07_SECTION_7_REPLACEMENT_REV4_2026-11-28.md is reviewed, including deletion of the further-draw sentence;
11. reconstructable outcomes remain reportable after tampering, while genuinely unreconstructable outcomes become permanently NOT ASSESSABLE without a reroll;
12. both the preserved Revision 2 verifier and the new Revision 3 verifier/output are reviewed with distinct scopes;
13. the verified Git bundle and quarantined corrupt-ZIP report are accepted, and later Activity coverage after 07:03:30Z is completed;
14. the two-relay v0.7 rule remains unchanged; any single-relay proposal receives separate cryptographic review.

Claude must issue separate PASS / NOT PASS verdicts for the study-purpose OAC chain, registry identity, chronology and whole-lifetime scan, one-attempt/successor rule, actor identity, Activity schema/ledger, timestamp parser and buffer, literal v0.7 section 7 replacement, reconstructability, preservation disclosure, and each verifier. For each NOT PASS identify the exact text and minimum correction.

## 12. Current disposition

- Revision 2: preserved unchanged.
- Revision 3: preserved unchanged; Claude's latest review found it NOT ADOPTABLE.
- Revision 4: consolidated candidate for fresh Claude review; not adopted.
- OAC and experiment ID: not created; registry blocker remains.
- Activity API raw wire evidence and full-lifetime ledger: not established.
- Root/successor-chain rule and equal-timestamp chronology: proposed, pending Claude review and schema evidence.
- B_lock = 300 s: policy margin, not a measured or guaranteed bound.
- v0.7 section 7 replacement: supplied in full; current v0.7 file remains unchanged.
- Uploaded Git bundle: verified and inventoried.
- Uploaded ZIP-labelled blob: quarantined as corrupt evidence, not a usable archive.
- Two-relay v0.7 validation: unchanged.
- Revision 2 verifier: preserved with its original output.
- Revision 3 verifier: GPT-authored; 14 deterministic checks; no drand, BLS, HTTP-client, Activity, or production-selection testing.
- 20-push visibility test: NOT AUTHORIZED and not required.
- Original attempted v0.7 lock: VOID FOR PRODUCTION USE.
- Production round, seed, or pair: none selected.
- R2 C2: NOT ESTABLISHED.
- No solver construction or execution authorized.
