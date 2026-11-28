# LC518 R2 C2 Repair Review and Claude Follow-up Packet, Revision 2

**Date:** 2026-11-28  
**Status:** Revised candidate design for independent Claude review. Not v0.11. Not adopted. Not a canonical composite. No production selection is authorized.

## 1. Adjudication of Claude's first review

Claude's first review issued:

- Historical hash correction addendum: **PASS**, with two non-blocking text fixes.
- Timing evidence clarification: **PASS**, with one recommended upgrade.
- Repair packet: **NOT PASS**, because its visibility criterion and retrieval-window failure semantics allowed operator discretion.

This revision implements those corrections. It does not claim Claude has reviewed or agreed with this revision.

## 2. Selection mathematics remain unchanged

The v0.7 two-stage selection algorithm remains unchanged. The independent verifier checks the 28-pair universe, four SHA-256 vectors, normal two-pair fixture and rejection boundary. The prior run returned seven passes.

A code gap was identified in that verifier: it checked the rejection threshold arithmetically but did not execute a counter-advance path after an injected rejected digest. Revision 2 adds that execution to the script. It does not change the v0.7 algorithm or any production mapping.

## 3. Activity API findings and request contract

### 3.1 Lifecycle evidence

The disposable repository is `foued2/lc518-activity-api-lab-20261127`. Claude reports seven ledger records: one `main` branch creation and six test-ref lifecycle records covering branch creation, push, deletion, same-name recreation, identical-commit re-push, and force-push. The `ref=` filter returned the six test-ref records in order.

The Activity timestamps for the three push cases differed from commit committer dates by +6, +59 and +13 seconds. In particular, the identical-commit re-push generated a new Activity timestamp despite unchanged commit metadata. This supports use of the Activity timestamp as a server-recorded event-time field, not as a copied commit timestamp.

### 3.2 Live schema and API-version behavior

Claude's unauthenticated requests with both `X-GitHub-Api-Version: 2026-03-10` and `X-GitHub-Api-Version: 2022-11-28` returned `X-GitHub-Api-Version-Selected: 2026-03-10`. Therefore the request header did not force the older version. The selected-version response header must be captured and treated as authoritative for the observed response. A production protocol must pin the expected selected version and fail closed if the server-selected version differs.

The live response schema reported by Claude is:

- common fields: `id`, `node_id`, `before`, `after`, `ref`;
- event fields: `timestamp`, `activity_type`, `actor`.

This differs from the field names in the current documentation example (`pushed_at`, `push_type`, `pusher`). Treat the live response as the observed schema, but archive raw unauthenticated bodies and headers and reconcile them against the official OpenAPI definition before final schema pinning. Third-party OpenAPI mirrors are supplementary, not the sole authority.

### 3.3 Query, pagination, cache, and rate limits

Always specify `ref`, `time_period`, `direction`, and `per_page`; never rely on endpoint defaults. Use `time_period=year`, `direction=asc`, and `per_page=100` for the audit query, then follow every server-provided `Link: rel="next"` URL. Validate that each next URL remains HTTPS on `api.github.com`; do not require the pagination URL path to equal the original request path, because Claude observed cursor URLs using `/repositories/{repository_id}/activity` rather than `/repos/{owner}/{repo}/activity`.

Claude observed `Cache-Control: public, max-age=60`. Preserve `Age` and all cache headers. Any visibility-latency measurement claiming finer than 60-second resolution is invalid unless it demonstrates from fresh, uncached responses that the cache did not constrain that measurement. The `Age` value must be recorded for every poll.

One Claude query with `ref=` and no `time_period` returned five records; an unfiltered query returned 100 records across roughly five days. Luna earlier reported nine records from the main repository, but the exact query URL was not preserved. Stage A must record the exact URL and query parameters used in any count claim.

Respect primary and secondary rate limits. Record `Retry-After`, `X-RateLimit-*`, 403 and 429 responses. Do not accelerate polling after a rate-limit response or silently discard rate-limited trials.

### 3.4 Raw evidence preservation

At lock time, archive immediately:

- the exact request URL and query parameters;
- raw response body bytes for every page;
- raw response headers, especially `Date`, `Age`, `Cache-Control`, `ETag`, `Vary`, `Link`, `Content-Type`, `Retry-After`, `X-RateLimit-*`, and `X-GitHub-Api-Version-Selected`;
- redirect status and Location, if any;
- local send/receive monotonic times;
- parsed Activity records and validation results;
- SHA-256 hashes for every raw body and the complete evidence manifest.

The current packet does not yet contain the raw adoption-push response or raw lab responses. Claude confirms the adoption event is publicly retrievable now; therefore this is a preservation gap, not an unresolved existence question.

## 4. Revised lock-validity design

This is a candidate amendment for Claude review, not an adopted v0.7 rule.

### 4.1 Immutable lock object

Before publication, prepare one lock commit `A` whose tree contains a lock manifest naming:

- the exact protocol SHA-256;
- the exact verifier/source SHA-256 values;
- the base commit `B` from which the lock branch is created;
- the lock-manifest schema/version;
- the selection algorithm identifier.

The manifest must not contain the Activity timestamp or target round, because those values are derived from the server event and including them would create circularity.

Use exactly one deterministic ref name derived from the full SHA-256 of the final adopted lock-protocol artifact, for example `refs/heads/lc518-c2-lock-<full-lock-protocol-sha256>`. This namespace is fixed before publication. No alternate ref name may be substituted under the same owner authorization. Any pre-existing Activity history on the deterministic ref other than the required `0 -> B` branch-creation event is disqualifying; it must not be bypassed by choosing a different ref.

Create that ref at base commit `B`, then make exactly one lock push from `B` to `A`. The required ordered lifecycle is: one `branch_creation` event showing `before=0` and `after=B`, followed by the first `push` event showing `before=B` and `after=A`. There must be no intervening push, deletion, or recreation. The branch-creation event is not the lock timestamp; the matching `B -> A` push event is the lock event. The commit `A` must have exactly one parent, `B`. Preserve and validate the actor identity. Archive `A`'s commit, tree, and content bytes at lock time so later branch deletion or garbage collection cannot remove the evidence.

The first matching `B -> A` push event in that exact lifecycle is the one binding lock event. Later pushes, force-pushes, deletion or recreation are audit violations and must be recorded, but must not retroactively erase the already recorded lock or grant a replacement draw. This avoids turning a post-outcome ref deletion into an operator-controlled void lever. The deterministic ref name and first matching event prevent a second lock from being substituted under the same authorization.

### 4.2 Server-event timestamp and target derivation

Let `t_event` be the server-recorded `timestamp` on the exact matching Activity `push` record. It is an event-time field, not the commit's committer date and not the first-public-visibility time. Do not claim it is the exact HTTP receipt instant to sub-second precision.

Let `B_lock` be a fixed safety buffer, selected and frozen in the adopted protocol before the lock is published. Its numeric value remains unresolved pending controlled timing evidence and review. The target round is the smallest Quicknet round `r` satisfying:

`genesisTime + period × (r − 1) > t_event + B_lock`.

The buffer separates the server-recorded lock event from the target round. It is not a public-observer visibility deadline. The Activity record can be retrieved and independently checked later; first retrieval time is not a lock-validity condition.

### 4.3 Objective verification

A third party verifies the lock by independently retrieving the Activity ledger and checking the complete ordered lifecycle and the immutable lock commit:

1. exactly the deterministic ref is used;
2. the branch-creation record is `0 -> B`;
3. the qualifying push record is `B -> A`;
4. `A` names the exact protocol and verifier hashes in its immutable manifest;
5. actor, event type, ref, before, after and timestamp fields match the lock specification;
6. the selected API version, schema, all pagination pages, and raw-response hashes match the frozen request contract;
7. the server event timestamp plus the fixed buffer precedes the scheduled target round under the formula in §4.2.

A later deletion or force-push is a recorded breach but cannot erase or replace the original qualifying event. There is no second ref or second lock under the same authorization.

### 4.4 Visibility latency is operational, not validity

The requirement that an independent observer must retrieve the event before the target is removed. This was the central defect in Revision 1.

Public retrieval is required for later auditability. First-public-visibility latency is measured only to plan when and how an operator archives the evidence. A poll that does not yet see the event does not void the lock. An event first retrieved after the target can still be checked retrospectively using its server event timestamp, provided the event remains publicly retrievable and its identity is unambiguous.

## 5. No-abstention and no-reroll semantics

The lock and target round determine one selection outcome whether or not the operator runs the client, retrieves the beacon promptly, or agrees with the resulting pairs.

The retry deadline is a liveness and operational deadline only. If the operator cannot retrieve a valid beacon by that deadline, the status is `NOT_YET_RETRIEVED` or `NOT_YET_COMPUTED`; it is not a failed draw, a void, or permission to create another lock. The exact same predetermined round remains the only round that may be used. Any party may later retrieve and verify that round and reproduce the deterministic pair calculation.

No new lock, round, seed or pair may replace the one defined by a valid lock event because of a missed retrieval window, inconvenient result, unavailable operator, relay outage, or failure to run the script. A protocol change or new owner authorization cannot be used to replace this already binding selection. Only objective invalidity of the lock event itself, established from the ledger and immutable commit, can show that no valid lock was formed; such invalidity does not authorize a replacement draw under the same authorization.

## 6. drand retrieval and relay rule, candidate amendment

V0.7 currently requires both relays to pass all checks. That creates an availability veto. The proposed rule below changes v0.7 §4 and §7 and therefore requires a fresh Claude review.

### 6.1 Per-relay verification

Each relay response is independently checked against the pinned chain identity and exact target round. A single response with a canonical, correctly encoded signature, valid subgroup membership, and successful BLS verification against the pinned public key and correct round message is sufficient to establish the beacon value.

The second relay is corroborative, not a mandatory availability quorum. An unavailable or invalid second relay must not erase a valid beacon from the first relay. The verifier must not accept a relay's claimed `randomness` without locally deriving and checking it from the signature according to the pinned protocol.

If two responses both pass independent verification but contain different signature bytes for the same pinned key and message, stop with `VERIFIER_INCONSISTENCY_HALT`; this indicates a cryptographic or implementation inconsistency requiring investigation, not a reason to select a different round. The validator must enforce canonical encoding and subgroup membership.

### 6.2 Retryable outcomes

All retries use the same chain identity, exact target round and exact round endpoint. Never use `/latest`, never substitute another round, and never reroll.

Candidate retry classes:

- no HTTP response: DNS failure, connection failure/reset, TLS transport failure, timeout, or incomplete/truncated response;
- HTTP 404, 408, 429, and 5xx from the **round endpoint only**;
- respect valid `Retry-After` subject to a separately frozen maximum elapsed retry horizon.

A persistent 404 from the chain-info endpoint is a configuration/identity error, not a retryable “round not published” condition. Other non-retryable 4xx responses, unexpected redirects, malformed successful JSON, wrong chain identity, wrong round, malformed/non-canonical signature encoding, subgroup failure, or failed BLS verification are not retried as ordinary availability failures. Preserve each relay's failure evidence; a failure from one relay does not veto a valid response from the other.

Finite retry timestamps, per-attempt timeouts, `Retry-After` handling, and the maximum elapsed horizon remain unset until testnet and local mock evidence is collected. The retry horizon affects operational status only. Expiry does not invalidate the lock or allow another round.

### 6.3 Required local mock tests

The existing injected exception before a request is too weak. The local mock suite must exercise:

- 404 for the first N round-endpoint attempts, then a valid same-round response;
- persistent chain-info 404 as terminal configuration failure;
- 408, 429 with valid/invalid `Retry-After`, and 500/502/503;
- DNS failure, connection refused/reset, timeout before response, timeout after headers, and truncated body;
- 200 malformed JSON, wrong chain, wrong round, malformed/non-canonical signature, wrong length, subgroup failure, and well-formed invalid BLS signature;
- first relay invalid/unavailable while second provides a valid beacon;
- first relay valid while second is unavailable/invalid;
- both relays returning the same valid beacon;
- conflicting injected validation results, which must halt as verifier inconsistency;
- retry-horizon expiry resulting in `NOT_YET_RETRIEVED`, with no new round and no new lock.

Use testnet `quicknet-t` for real publication-behavior observations only. No production mainnet target may be queried during these tests.

## 7. Vector verifier correction

Revision 1's script checks that `L = 2^256 − 16` and contains counter-1 digest vectors, but does not execute the rejection-and-counter-advance path. Revision 2 must execute it.

For each label (`repeat-1`, `repeat-2`), inject the first rejected integer `2^256 − 16` at counter 0, verify it is rejected because `x >= L`, increment the same label's counter to 1, compute the real SHA-256 digest for counter 1, and verify the accepted index is 23 for `repeat-1` and 13 for `repeat-2`. Include a counter-overflow test proving that rejection at `2^64−1` aborts rather than wrapping. The synthetic injected digest is a test harness value, not claimed to be a real SHA-256 output.

## 8. Branch-history disclosure

The preservation branch was created from the VOID-record commit `24e973fc8517d5467807446f915841896b65f8a4`. Claude's read-only Activity inspection reports the following branch sequence:

- branch created at `06:56:54Z`;
- pushes at `06:59:56Z`, `07:02:04Z`, and `07:02:39Z`;
- force-push at `07:03:30Z`, replacing prior tip `e0cddeacc7ea3ff17477708ec3470f71c8ee476b` with final tip `6f4b6975dd956ea3303653aa3ac8f7a27be31646`.

The intermediate commits included the first packet commit `a0f1ba90b92457bfaa43c3ec68c754578243cb0e` and the intermediate cleanup/manifest commit `0e6c47b26959019cafc6e11eb04e5f7e19a037dd`. The final force-pushed commit is a single commit directly on base `24e973f`. The README and follow-up review must disclose this history. No force-push is to be used for Revision 2; append commits normally.

## 9. Authorization boundary

The proposed 20-push Activity API timing experiment was not authorized and has not been run. Do not create refs or pushes in the lab until the owner explicitly authorizes it. The read-only ledger observations and the local vector/mock tests are separate from that external-write test.

No LC518 master changes, production drand query, production seed, pair selection, solver construction, or solver execution are authorized by this packet.

## 10. Claude follow-up review request

Please review the exact Revision 2 files and issue explicit verdicts:

1. `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28_REV2.md` — re-check the exact VOID-record quotation, corrected hash, and current preservation status.
2. `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28_REV2.md` — verify use of Activity record `52144406651`, the late-event conclusion, and separation of event timestamp from first visibility.
3. `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md` — especially challenge the deterministic one-ref/one-lock-event mechanics, whether later ref mutation can or cannot void the original event, the anti-abstention rule, timestamp-plus-buffer validity, and the revised single-valid-relay rule.
4. `verify_lc518_c2_v07_vectors_REV2.py` — confirm the rejection path actually executes, including same-label counter increment and counter overflow.
5. `LC518_C2_PRESERVATION_BRANCH_HISTORY_NOTE_2026-11-28.md` — confirm the force-push disclosure against the Activity ledger.

For every NOT PASS, identify exact sections/lines, explain the defect, and give the minimum correction. Do not claim tests have run unless their raw output is supplied. Do not treat review of these candidates as adoption of an amended protocol. V0.10 remains NOT PASS; no v0.11 or canonical composite exists.

## 11. Current disposition

- v0.7 selection mathematics: unchanged; prior vectors independently reproduced.
- Historical hash addendum: PASS from Claude, with the two text corrections implemented in Revision 2.
- Timing clarification: PASS from Claude, with the event-time and preservation corrections implemented in Revision 2.
- Repair proposal Revision 1: NOT PASS; revised in Revision 2.
- Activity API: promising candidate; no 20-push write test authorized or run.
- Events API: unsuitable as a timing gate.
- drand retry and relay availability amendments: proposals only, requiring fresh review and tests.
- Vector rejection-loop correction: implemented in Revision 2 and requires execution review.
- V0.10: NOT PASS.
- V0.11/canonical composite: not produced.
- Production target, seed, and pair selection: none queried or selected.
- Original R2 C2: NOT ESTABLISHED.
