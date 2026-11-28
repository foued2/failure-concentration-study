# LC518 R2 C2 v0.7 Lock-Validity Amendment Draft

**Date:** 2026-11-28  
**Status:** New dated review draft. Not adopted, not a replacement protocol, and not production authorization.  
**Scope:** Proposed replacement text for v0.7 §7 and its production-selection paragraph (the paragraph currently at line 191). Historical v0.7, its hash, the attempted owner lock, and the VOID disposition remain unchanged.

## 1. Decision and scope

The current v0.7 timing rule is not retained. It makes validity depend on an operator or observer retrieving an Activity API record before the target round, and treats a missed retrieval window as failure of the draw. This creates an observation-dependent failure path and an avoidable opportunity to abstain and try again.

This draft separates four things:

1. **Lock identity and lifecycle:** established by one canonical Git ref, its initial push transition, and the corresponding GitHub Repository Activity record.
2. **Preservation of the captured evidence:** provided by a canonical evidence manifest and an independently issued RFC 3161 timestamp token.
3. **Target-round derivation:** deterministic from the verified timestamp token, with a fixed buffer.
4. **Failure disposition:** non-retrieval never changes the outcome; post-lock tampering or loss of auditable history never creates a replacement draw.

The GitHub Activity API is not described here as an immutable or permanently retained ledger. Its records are primary evidence while available; the captured bundle and timestamp token preserve a point-in-time copy. Neither mechanism alone proves the authenticity of a past TLS session. That limitation remains explicit.

This amendment does **not** change the pair universe, hash framing, rejection sampling, labels, drand chain identity, or pair-selection mathematics in v0.7. It does not adopt R2 or authorize a draw.

## 2. Timestamp witness selection

**Selected witness:** an RFC 3161 Time-Stamp Authority (TSA), using DigiCert's published RFC 3161 endpoint `http://timestamp.digicert.com`.

The GitHub Activity record remains the primary lock-time and lifecycle evidence. The RFC 3161 token is a second, independent timestamp witness for the SHA-256 digest of the captured evidence manifest; it is a preservation fallback, not the source of the target-round timestamp. DigiCert currently documents that endpoint and lists its active timestamp responder/intermediate/root certificate chain. The chain and relevant certificate identities must be preserved with each evidence package because TSA certificates are rotated. RFC 3161 binds a message imprint (hash algorithm and digest) to a TSA-signed token containing `genTime`; the request nonce, imprint, token signature, signer certificate, certificate path, and certificate status must all be checked. The token proves that the submitted digest existed no later than the TSA's stated time, subject to the TSA's trust and accuracy policy. It does **not** prove that the bytes submitted to the TSA were genuinely returned by GitHub.

References:

- IETF RFC 3161: https://www.rfc-editor.org/rfc/rfc3161.html
- DigiCert RFC 3161 TSA endpoint and current certificate-chain information: https://knowledge.digicert.com/general-information/rfc3161-compliant-time-stamp-authority-server
- DigiCert timestamping troubleshooting / endpoint confirmation: https://knowledge.digicert.com/solution/troubleshooting-timestamping-problems

Open adoption condition: the exact DigiCert certificate chain, TSA policy identifier, published time-accuracy bound, and verification procedure must be pinned in the implementation evidence. If no defensible maximum time uncertainty can be established from the token's `accuracy` field or the provider's applicable published policy, the token cannot be relied upon as a preservation-time witness. The TSA time does not set or move the target round.

Open provenance limitation: a later reviewer cannot cryptographically reconstruct the TLS authentication of a historical HTTP response from the raw response bytes alone. The package therefore requires a contemporaneous raw capture, later live unauthenticated re-query, and exact content comparison. If the live GitHub record is unavailable or conflicts with the capture, the result is `NOT ASSESSABLE` and the slot halts. The TSA token is an independent time-and-integrity witness for the captured bytes, not a substitute for authenticating the source response.

## 3. Proposed definitions

### 3.1 Slot and canonical ref

Each selection attempt has one `slot_id`, fixed in the reviewed protocol and owner adoption record before any lock operation. The canonical lock ref is derived deterministically from it:

`refs/heads/lc518-r2-c2-lock/<slot_id>`

No operator-selected alternative ref is permitted for the same slot. The slot's attempt count is one. The ref must not exist before the attempt; its creation and subsequent single lock push must be visible in the Activity history.

For the proposed one-push construction:

- `B` is the exact, pre-existing base commit SHA recorded in the lock manifest and owner record.
- The canonical ref is created at `B`.
- Exactly one subsequent normal push changes the ref from `B` to lock commit `A`.
- The qualifying Activity event must identify the exact canonical ref, `before = B`, and `after = A`, with the raw activity type and timestamp fields recorded as returned by the live endpoint.
- Commit `A` must contain a lock manifest that pins the exact protocol SHA-256, `slot_id`, base SHA `B`, verifier/evidence artifact hashes, and the fixed selection constants. It must not contain the Activity timestamp, TSA timestamp, or target round, which are not known when `A` is created.

The preceding branch-creation event must identify the same canonical ref and show that it was created at `B`. The exact live field values for both lifecycle events must be tested and pinned before adoption. A branch-creation event, later push, deletion, same-name recreation, force-push, or other update must not be mistaken for the single qualifying transition.

### 3.2 Evidence bundle and canonical manifest

Immediately after obtaining a positive unauthenticated Activity API response for the qualifying push, capture and preserve:

- the exact request URL, query parameters, request headers, API version requested, and redirect chain;
- the raw HTTP status and complete raw response headers, including `Date`, `Age` when present, `ETag`, `Cache-Control`, `Vary`, `Link`, `Content-Type`, rate-limit headers, and all `X-GitHub-*` headers;
- the exact raw response body for every page, with every `Link: rel="next"` URL and page order;
- raw GitHub ref/commit lookups proving the canonical ref, base `B`, lock commit `A`, and manifest bytes;
- a verifier report recording exact checks, their inputs, and outcomes;
- the pinned protocol, verifier, lock-manifest, and relevant source-artifact hashes.

Construct a canonical UTF-8 evidence index. The index format, filename grammar, LF line endings, byte lengths, path ordering, and hash algorithm must be fixed before implementation. Each entry must contain the relative path, exact byte length, and SHA-256 of one payload file. Sort entries lexicographically by ASCII relative path. The index must not include the TSA token or TSA response, avoiding self-reference. The TSA request must use SHA-256 over the exact index bytes as its `messageImprint` and must include a fresh unique nonce with certificate request enabled.

Preserve the raw TSA request and response, the full token, signer certificate, certificate chain, policy identifier, serial number, `genTime`, `accuracy` (if present), nonce, and independent token-verification output alongside the evidence bundle. These post-index timestamp files are retained as companion evidence; do not alter the already timestamped index to add them.

### 3.3 Cache semantics and absence

`Cache-Control: max-age=60` is a cache freshness lifetime. It is **not** a statement that the Activity timestamp has 60-second resolution, and it is not a validity cutoff. Record `Date`, `Age`, `ETag`, `Cache-Control`, and any cache-related headers exactly as received.

A positive Activity response containing the exact qualifying event is evidence that the response data existed by the time represented by that response/cache chain. A response that omits the event does not prove that the event did not occur; it may be stale, incomplete, paginated, or delayed. Absence must never be used as proof of non-occurrence. If a positive complete response cannot be obtained, do not issue a valid lock timestamp and do not proceed to target derivation.

The raw live response at the exact pinned endpoint is the schema authority for the implementation. Do not infer the wire schema from docs, mirrors, SDK normalization, or connector-normalized output. The current GitHub documentation example exposes `pushed_at`, `push_type`, and `pusher`; Claude's reported live response uses `timestamp`, `activity_type`, and `actor`. That discrepancy is unresolved. Before adoption, capture raw request/response bytes from the unauthenticated endpoint with the selected API version, determine the exact live schema, and fail closed if the response does not match the pinned schema. Preserve the requested and returned API-version headers and all response headers.

## 4. Proposed target-time rule

Let `t_event` be the server-assigned event-time value in the exact qualifying Activity record, parsed from the raw field name and format established by the live-schema qualification test. Preserve the raw value and its source field. Do not substitute a Git commit timestamp, author/committer date, local clock, HTTP `Date`, or the TSA `genTime`. `t_event` is the Activity event timestamp used by this protocol; it must not be described as the exact instant GitHub received the HTTP push.

Proposed fixed buffer:

`b = 300 seconds` (five minutes).

This is a proposed protocol constant, not a measured visibility-latency percentile and not an inference from the unrun 20-trial lab test. It is a fixed separation between the server-assigned push-event time and the scheduled target, intended to leave operational time to capture and timestamp the raw evidence. Claude must review the value and its adequacy before adoption. A missed evidence-capture deadline consumes the slot; it never grants a replacement draw.

For the pinned Quicknet schedule, round `r` is scheduled at:

`T_r = genesisTime + period × (r − 1)`

The production target is the smallest integer `r ≥ 1` for which:

`T_r > t_event + b`

Use the full timestamp precision present in the raw Activity event field. Do not truncate fractional seconds or round the timestamp down. The target is derived mechanically from the server-assigned Activity event timestamp and the pinned chain constants; no operator chooses a round after seeing a beacon. The timestamp token over the evidence manifest is a separate preservation witness and is not used to move the target. Its verified `genTime` plus its uncertainty bound must precede the scheduled target time; otherwise, the slot halts and no pair is selected.

This rule removes local NTP as a validity condition and removes the independent-observer first-visibility cutoff. Local clock readings may be retained as diagnostics only. It does not remove the need to validate the exact raw Activity response, verify the TSA token, or reconcile the public record after the target.

## 5. Proposed replacement for v0.7 §7

> ## 7. Prospective production target and lock validity
>
> This draft is not a draw authorization. No production selection is authorized until this amendment has received a scoped Claude technical PASS, the owner has adopted an exact successor protocol hash, and the single lock procedure below has completed successfully.
>
> **7.1 One slot, one canonical ref, one attempt.** The owner adoption record fixes one `slot_id`, one canonical lock ref derived from that ID, the exact base commit `B`, and the exact protocol SHA-256. The canonical ref must be absent before the attempt. It is created at `B` and receives exactly one normal push from `B` to lock commit `A`. No alternate ref, concurrent lock, second attempt, or operator-selected replacement is allowed for that slot. `A` must contain the lock manifest specified in §3.1 of the dated lock-validity amendment. The qualifying Activity record must identify the exact ref and the transition `before = B`, `after = A`. The preceding branch-creation record must identify the same ref at `B`.
>
> **7.2 Evidence capture and timestamp witness.** Obtain the complete raw unauthenticated Activity API response, all pages, request URL, request and response headers, redirect history, and matching Git ref/commit evidence. Capture the exact wire schema from the live endpoint; fail closed on schema drift, missing required fields, incomplete pagination, or a mismatch of ref, base, lock commit, or activity type. Build the canonical evidence index and obtain a valid RFC 3161 token from the selected TSA over SHA-256 of the exact index bytes. Verify the token's imprint, nonce, signature, signer certificate, chain, certificate status, policy, serial, `genTime`, and accuracy bound. The token timestamps the captured evidence manifest; it does not determine the target round or authenticate the historical TLS response. The token's `genTime` plus its pinned uncertainty bound must precede the scheduled target time. `Cache-Control: max-age=60` is a cache lifetime, not timestamp precision. A positive response is retained as evidence; an absent event is not proof that no event occurred.
>
> **7.3 Target.** Let `t_event` be the server-assigned event-time field in the exact qualifying Activity record. Use the proposed fixed buffer `b = 300 seconds`, unless a reviewed successor specifies another fixed value. The target is the smallest Quicknet round `r ≥ 1` for which `genesisTime + period × (r − 1) > t_event + b`. Preserve the full precision of the raw Activity event field. The target is not selected manually and cannot be replaced by a later round.
>
> **7.4 Validity and failure before a valid lock.** A ledger lock is valid only if the canonical ref and the single qualifying `B → A` Activity transition satisfy §7.1, the Activity event timestamp is the pinned server-assigned field, the event is not later than the fixed target cutoff, and no other lock exists for the slot. A late event, pre-existing ref, wrong `before`/`after`, wrong ref, extra or concurrent lock, incomplete or schema-incompatible Activity response, or mismatch between the captured and live record means no valid lock exists. For this one-attempt slot, that failure consumes the slot: it does not authorize another ref or replacement lock. A missing, invalid, or late TSA token does not change the ledger event timestamp or create a new target; it makes the evidence package incomplete and the selection `NOT ASSESSABLE / HALT`. In neither case is a replacement draw allowed. This is intentionally stricter than allowing an operator to declare a prior attempt void and re-lock; a replacement policy would require its own predeclared, independently auditable attempt schedule and must not be inferred here.
>
> **7.5 Post-lock tampering and retention failure.** After the qualifying lock transition, any deletion, force-push, rewrite, same-name recreation, additional push, or other mutation of the canonical ref is a `FORFEIT / HALT`, not a void that permits a new draw. The same applies if the record needed to determine the ref's lifecycle is no longer available or the preserved bundle conflicts with the live public record: mark `NOT ASSESSABLE / HALT`. Never convert a post-lock violation into permission to create a replacement lock. A post-lock violation is an adverse protocol disposition; it is not automatically a solver-correctness failure or a numeric outcome unless a separate, pre-adopted statistical rule defines such a mapping.
>
> **7.6 Retrieval and outcome.** The lock and the single public target round define the selection. Operator non-retrieval of the target beacon, a client timeout, or failure to run the local draw code does not void the lock and does not permit a later round. Any permitted transport retries must request the exact same target round and chain path. If the target beacon cannot be retrieved or cryptographically validated within a separately fixed retry policy, the slot halts without a pair selection; no later round or replacement draw is allowed. A reviewer may independently retrieve and validate the same public round.
>
> **7.7 Evidence retention.** Preserve the lock commit and ref, the complete Activity API capture, all pagination and headers, the canonical evidence index, raw TSA request/response and token, certificate chain and validation output, target calculation, drand request/response evidence, signature verification, derived seed, digest/counter path, indices, selected pairs (if any), and all hashes. The GitHub Activity API is not assumed to provide permanent retention or cryptographic append-only guarantees. Re-query it after the target and compare the full relevant lifecycle. If the lifecycle cannot be reconstructed, halt; do not infer that no tampering occurred.
>
> A successful pair selection authorizes no R2 adoption, allocation acceptance, parent-source construction, solver construction/evaluation, Rev11 amendment, publication, or scientific claim. Those decisions remain separate.

## 6. Proposed replacement for current v0.7 line 191

Replace the current paragraph beginning “For the authorized production selection…” with:

> For the authorized production selection, query only the exact derived target round and pinned chain path. Preserve the complete request/response evidence and apply the full validation order in §4. Any permitted transport retry must use that same round and path; do not use `/latest`, substitute another round, change labels, alter the universe, reroll a selected pair, or manually replace a result. Both pinned relay origins remain required under the current v0.7 relay rule unless a separately reviewed cryptographic amendment changes that requirement. A valid lock remains binding even if the operator does not retrieve or process the target beacon. A target-round retrieval or validation failure ends the slot without a pair selection; it does not authorize a later round. Any post-lock deletion, force-push, rewrite, recreation, additional push, loss of required lifecycle evidence, or mismatch between the preserved bundle and the live record is `FORFEIT / HALT`, never a void permitting a replacement draw. Retain the lock ref and commit, raw Activity API responses and headers, complete pagination, canonical evidence index, TSA request/response/token and certificate chain, target calculation, all drand responses and verification results, seed, digest/counter path, indices, pair values, and hashes.

## 7. Corrections to the existing repair notes and review packet

These are prospective text corrections for a reviewed copy; do not rewrite the original v0.7 lock attempt or the current preservation-branch snapshot.

1. **Historical hash addendum, §5:** quote the VOID record's wording exactly as “GitHub's server-side creation time” when describing what that record says. Do not paraphrase it as a demonstrated receipt timestamp. The separate Activity record `52144406651` is reported as a push event at `2026-11-27T16:41:59Z`; cite it as the distinct event-time evidence, and disclose that the raw response was not included in the original packet.
2. **Timing clarification, §§3–6:** use Activity push record `52144406651` and its reported `2026-11-27T16:41:59Z` timestamp as the stronger, separate observation. Do not claim the commit committer timestamp proves exact receipt time. Keep the target round/time at `34331448` / `16:41:48Z`, making the reported Activity event 11 seconds later. Explicitly state that raw body/headers and exact request URL remain unpreserved unless separately captured.
3. **README status lines:** the source notes are now committed to the preservation branch at `6f4b6975dd956ea3303653aa3ac8f7a27be31646`. Therefore, “Not committed” is stale if read as repository state. The accurate status is “committed to the preservation branch; not merged to `master`; not adopted; no production authority.”
4. **Force-push:** add the disclosure in the companion README section supplied with this draft. Preserve the old commit identities and the fact that the branch history was force-replaced.
5. **Cache wording:** remove the proposed rule “invalid below 60 s resolution.” `max-age=60` is not timestamp resolution. Preserve Date/Age/ETag/Cache-Control and do not use an absent result as proof of absence.

## 8. Disposition of the 20-trial test

The 20-trial visibility experiment was proposed to measure first-public-observer latency and establish an operational visibility cutoff. This draft removes first-visibility time as a validity condition. The target is derived from the server-assigned Activity push-event timestamp plus the fixed buffer; the RFC 3161 token timestamps the captured evidence manifest as a preservation fallback. Therefore, the 20-trial run is **not required to define the proposed validity rule** and remains **NOT AUTHORIZED**. Do not execute it or create lab refs under this draft.

Before adoption, the minimum evidence work is narrower and deterministic: (a) capture and pin one raw unauthenticated Activity API response and its exact schema/API-version behavior; (b) test pagination, ref filtering, branch-creation/push/deletion/force-push lifecycle representation; (c) verify an RFC 3161 token end-to-end, including nonce, imprint, signer, chain, revocation, and accuracy; and (d) verify the same-round retry/halt behavior in a local mock harness. These are conformance tests, not permission for production pushes or a production draw.

## 9. Explicit unresolved items for Claude

Claude's fresh review must decide, at minimum:

1. Whether the Activity API response fields reported in the prior review are actually present in the raw wire response at the pinned endpoint and API version, and whether the GitHub documentation discrepancy has been resolved.
2. Whether the one canonical ref and single-attempt slot construction can distinguish branch creation, the single `B → A` push, later push, deletion, recreation, and force-push with no lifecycle ambiguity.
3. Whether a DigiCert RFC 3161 token is an adequate independent time witness for this use, including the actual policy, accuracy bound, certificate validation, and long-term verification plan.
4. Whether `b = 300 seconds` is acceptable or must be changed; it is a proposed fixed constant, not a measured latency claim.
5. Whether the stated limitations around historical TLS authenticity, GitHub retention, and post-target re-query are adequate. No claim of immutable GitHub history is made.
6. Whether the one-attempt/no-replacement rule is sufficiently strict and operationally acceptable. This draft intentionally rejects automatic re-locking for the same slot because that would reopen the abstention surface.
7. Whether the retained two-relay requirement and transport rules remain unchanged. This draft does not adopt Claude's candidate single-relay sufficiency proposal or an untested retry schedule.

**Current disposition:** proposed ledger/TSA-based lock design only; not adopted; no lock valid; original attempted lock remains VOID FOR PRODUCTION USE; no production round, seed, or pair selected; 20-trial run not authorized; no R2 C2 compliance claim.
