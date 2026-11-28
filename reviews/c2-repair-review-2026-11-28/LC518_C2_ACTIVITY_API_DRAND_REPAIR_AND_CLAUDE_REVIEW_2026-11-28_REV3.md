# LC518 R2 C2 Repair and Lock-Validity Proposal, Revision 3

**Date:** 2026-11-28  
**Status:** Candidate for independent Claude review. Not v0.11. Not adopted. Not a canonical composite. No production selection is authorized.  
**Predecessor:** Revision 2 at `LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV2.md`. Revision 2 is preserved unchanged.

## 1. Revision 3 purpose and decision

Revision 3 addresses Claude's three blockers to adopting the Revision 2 lock direction:

1. **Forked locks:** a protocol-hash-derived ref alone allows multiple protocol variants and therefore does not identify one unique experiment commitment.
2. **Invalid-attempt handling:** the protocol must state that one attempted lock consumes the slot, even when the attempted lifecycle is invalid. A new attempt must be a separately registered successor, never a quiet replacement.
3. **Post-lock reconstructability:** later ref mutation cannot void the original lock or create an operator-controlled halt. The original deterministic result remains reportable if it can be reconstructed; otherwise its status is permanently `NOT ASSESSABLE`, with no replacement draw.

Revision 3 prefers Revision 2's deterministic-ref / first-`B → A`-event architecture. It rejects GPT's earlier DigiCert-plus-300-second design as a mandatory validity gate. The previous alternative remains preserved for audit only.

This proposal does not change the v0.7 pair universe, hash framing, rejection sampling, Quicknet identity, target-round mathematics apart from the reviewed event-time buffer, or current two-relay retrieval requirement. The candidate single-valid-relay amendment remains separate and is not adopted.

## 2. One experiment charter precedes the lock

### 2.1 Pre-existing experiment identity

A lock is not authorized by a protocol hash alone. Before any lock-ref creation, a single **Owner Adoption Charter (OAC)** must exist as an immutable, publicly recorded commit on the repository's protected `master` branch.

The OAC must fix, in canonical machine-readable form:

- one `experiment_id`, obtained from the pre-existing LC518 study/experiment registry, not invented or chosen by the operator at lock time;
- one exact adopted lock-protocol SHA-256;
- one exact canonical lock-ref path;
- one base-commit rule;
- one attempt only;
- one allowed actor's stable GitHub numeric user ID and login snapshot;
- the exact verifier/source SHA-256 values and algorithm identifier;
- the status of any predecessor experiment/charter, if this is a formally registered successor.

The OAC must be a dedicated, immutable charter record. Its commit identity is the exact `after` SHA in the qualifying master-branch Activity push event that first adds the charter file. The OAC commit/tree/file bytes are preserved. The charter file is never edited in place; corrections require a new, separately registered successor experiment and explicit public supersession record.

**The `experiment_id` must already exist in the study registry before the OAC is prepared.** The current reviewed materials do not establish a single canonical registry value for this C2 draw. That value is therefore an explicit adoption blocker; this draft does not invent one. No placeholder or operator-selected ID is acceptable in an adopted protocol.

### 2.2 Exactly one OAC for one experiment ID

The canonical `experiment_id` is fixed by the prior study registry and is not derived from the chosen protocol hash. The first OAC for that exact ID, recorded on protected `master`, is the only charter that can authorize a lock.

A second OAC, a different protocol hash, or a different charter file for the same ID cannot replace, supersede, or compete with the first. The first OAC remains binding, including if its attempt is later consumed or invalid. A later protocol variant under the same ID is non-qualifying.

A new attempt after a consumed or failed charter must be registered as a **new successor experiment**, with a new pre-registered sequential ID and an immutable public record that:
- identifies the predecessor ID and OAC commit;
- records the predecessor's final status and why it was consumed;
- states that the successor is a distinct prospective experiment, not a replacement result;
- fixes the successor's one protocol hash, one actor, one lock ref, and one attempt.

The old selection/result, if any, remains independently reportable and cannot be withdrawn or replaced by the successor. A successor cannot be created merely to suppress an inconvenient but reconstructable result.

### 2.3 OAC publication order

The OAC must be committed to protected `master` before any event on the canonical lock ref. A third party verifies:

1. the OAC file is present in the protected-master commit tree;
2. the exact OAC commit SHA is identified by the master Activity push event's `after` field;
3. that push event is earlier than the canonical lock-ref branch-creation event;
4. the OAC commit is an ancestor of the lock base commit `B`;
5. the OAC's experiment ID, protocol hash, lock-ref path, allowed actor, and attempt number match the later lock manifest.

If the OAC push event cannot be distinguished from commit metadata, if its exact Activity record is unavailable, or if its timestamp does not strictly precede the lock-ref creation event, no valid lock can be established. A commit author/committer date is not a substitute for the Activity event time.

## 3. Canonical lock ref and the single lock attempt

### 3.1 Ref identity

The canonical ref is fixed by the OAC and derived from the pre-registered experiment ID, **not** from a protocol hash:

`refs/heads/lc518-r2-c2-lock/<experiment_id>`

The exact allowed string and ID grammar must be frozen in the OAC. No alternative ref name may be selected for the same experiment ID. A different ref, even if it contains an identical manifest or a different protocol hash, is not a qualifying lock.

The repository-wide Activity feed must be captured from the OAC event through the lock event. Any other event in the reserved `lc518-r2-c2-lock/` namespace during that interval is an authorization violation; it cannot be used as a candidate lock or as a substitute. A partial feed, inaccessible page, rate-limit response, or unavailable history means the absence of competing lock activity is not established and the attempt cannot proceed.

### 3.2 Allowed actor

The OAC pins both the stable GitHub numeric user ID and the login snapshot of the one authorized actor. The repository owner currently resolves to numeric user ID `116307732` and login `foued2`; this observed identity may be used as the proposed OAC value, subject to owner confirmation in the actual charter.

The Activity actor on the OAC push, lock-ref creation, and qualifying lock push must expose and match the pinned numeric ID and login. The numeric ID is the identity key; the login is also checked against the OAC snapshot and preserved as a human-readable identifier. If the live Activity schema does not expose the required stable actor ID, or if identity cannot be reconciled, fail closed. Do not substitute commit author/committer strings for the Activity actor.

No bot, application, collaborator, alternate user, or second actor may create the OAC or perform the lock lifecycle unless the OAC explicitly authorizes that identity before any lock activity. This draft authorizes one actor only.

### 3.3 Required lifecycle and ordering

Let `B` be the exact `master` tip SHA after the OAC has been recorded. The canonical lock ref must be absent before the attempt.

The only qualifying lifecycle is:

1. **OAC push:** one Activity push event on `refs/heads/master` whose `after` identifies the OAC commit, with the charter file and exact protocol hash in its tree.
2. **Lock-ref creation:** one Activity branch-creation event on the exact canonical lock ref with `before = 0` (or the exact null/zero representation established by the raw live schema) and `after = B).
3. **Lock push:** the first subsequent Activity push event on that same ref with `before = B` and `after = A`, where commit `A` has exactly one parent `B`.

The event times must be strictly ordered:

`t_OAC < t_create < t_lock`.

The branch-creation event is not the lock timestamp. The first matching `B → A` push is the binding lock event. No additional push, deletion, recreation, or other event may occur between branch creation and that first lock push. If the actual API does not expose an unambiguous representation of `before = 0`, this lifecycle cannot be adopted as written; do not silently substitute a different interpretation.

Commit `A` contains a lock manifest that pins the OAC commit SHA, experiment ID, protocol SHA-256, exact ref, base SHA `B`, actor ID/login, verifier/source hashes, manifest schema version, and selection algorithm identifier. The manifest must not contain `t_lock` or the target round, because those are derived from the Activity event. Archive `A`, its tree, every manifest/source blob, and their SHA-256 hashes at lock time.

### 3.4 First attempt consumes the charter

The first event that creates or mutates the canonical lock ref after the OAC is the start of the one permitted attempt. It consumes the charter whether it is valid or invalid.

Examples that consume the attempt without creating a valid lock include:
- the ref already exists;
- the branch-creation event has the wrong `before` or `after`;
- the wrong actor creates the ref or pushes the lock commit;
- the lock push has a wrong `before`, `after`, parent, manifest, experiment ID, or protocol hash;
- an intervening or extra event occurs;
- the live schema or complete lifecycle cannot be established.

There is no second ref, replacement push, second OAC, or alternate protocol hash under the same experiment ID. An invalid attempt is permanently recorded as `CHARTER CONSUMED / NO VALID LOCK`. A later attempt is permissible only as a separately registered successor experiment under §2.2, not as a correction or replacement under the same authorization.

This is intentionally strict. It avoids the ambiguity in which an operator can decide after observing events that an earlier attempt was merely an invalid candidate and should be rerun.

## 4. Activity API evidence, schema, and absence

The raw wire response from the exact unauthenticated GitHub endpoint and the server-selected API version is the schema authority. The prior review reports fields `id`, `node_id`, `before`, `after`, `ref`, `timestamp`, `activity_type`, and `actor`; GitHub's documentation example uses different event-field names. These reported fields must not be treated as pinned until raw body bytes and complete headers are captured and checked.

Before adoption, preserve and validate:
- exact request URL/query, request headers, API-version requested, redirects and response URL;
- raw response body bytes and all response headers for every page;
- `Date`, `Age`, `Cache-Control`, `ETag`, `Vary`, `Link`, `Content-Type`, `Retry-After`, rate-limit headers and `X-GitHub-Api-Version-Selected`;
- all pagination pages, following the server-provided `Link: rel="next"` URL if it remains HTTPS on `api.github.com); do not require its path to remain identical to the original request path;
- the complete repository-wide feed covering the OAC-to-lock interval, plus the exact ref-specific lifecycle;
- the raw actor object and the stable numeric actor ID;
- raw-response SHA-256 values and the canonical evidence manifest.

Always set `time_period`, `direction`, and `per_page`; use a one-year history window covering the entire OAC-to-lock interval and preserve all pages. The raw request URL must be recorded exactly. A 403/429 or rate-limit response is not an empty result. Do not claim that no other lock exists when any page is missing or inaccessible.

`Cache-Control: max-age=60` is a freshness lifetime, not timestamp resolution. Record `Age` and all cache headers. A positive response containing the exact event is evidence that the event was represented in that response/cache chain. An absent event proves nothing unless the retrieval is demonstrably fresh, unfiltered as required, and completely paginated. Absence is never converted into proof of non-occurrence merely because one query returned no record.

The Activity event timestamp is an event-time field, not commit committer time, not the HTTP `Date` header, and not first-public-visibility time. Do not describe it as the exact HTTP receipt instant.

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

## 7. Drand retrieval remains under current v0.7 rule

This revision does not adopt the proposed single-valid-relay sufficiency change. The current v0.7 two-relay rule remains in force: both pinned relay origins must return the exact target round and independently pass the prescribed identity, encoding, BLS, randomness-consistency, and agreement checks.

Any retry must request the same chain and exact target round; never use `/latest`, substitute a later round, alter the selection algorithm, or reroll. Transport retry classes, retry schedule, timeout and horizon remain subject to the separate local/mock conformance test and scoped Claude review. Expiry of an operational retry window does not void the lock or authorize a new draw.

The proposed single-valid-relay rule remains a separate, unadopted cryptographic amendment. It requires separate Claude review of canonical encoding, subgroup membership, pinned key/message, and the uniqueness assumption for the pinned BLS scheme.

## 8. Evidence preservation and optional timestamp sealing

At lock time, archive the raw Activity request/response capture, all pages and headers, matching ref/commit objects, OAC, lock manifest, commit/tree/blob bytes, parsed validation report, and SHA-256 hashes.

An RFC 3161 TSA token (DigiCert may be used) is optional additional preservation evidence for the SHA-256 hash of the canonical evidence manifest. It is not the source of `t_lock`, not a validity condition, not a replacement for the Activity API, and not proof that the timestamped bytes were returned by GitHub. Failure to obtain a TSA token does not void an otherwise valid lock or authorize a replacement. If used, preserve the manifest bytes, exact TSA request/response/token, nonce, message imprint, signer certificate, chain, policy and validation output. Do not require token arrival before the target.

GitHub's Activity API is not assumed immutable or permanently retained. The capture is a contemporaneous preservation copy; later public re-query provides corroboration. If the API record is no longer available and the captured source cannot be independently trusted or reconciled, apply §6.3. Never assert that a local archive alone authenticates a historical TLS response.

## 9. Branch-history and document corrections

The preservation branch currently points to `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`, a normal commit on top of `6f4b6975dd956ea3303653aa3ac8f7a27be31646`. The three superseded preservation commits are `a0f1ba90b92457bfaa43c3ec68c754578243cb0e`, `0e6c47b26959019cafc6e11eb04e5f7e19a037dd`, and `e0cddeacc7ea3ff17477708ec3470f71c8ee476b`. The base `24e973f...` and force-pushed tip `6f4b697...` are not counted as superseded commits.

Claude's latest Activity read of the preservation ref returned HTTP 403 rate-limit responses for both attempts, so activity coverage after the reported 07:03:30Z force-push is outstanding. The later Revision 2 commit metadata reports `2026-11-28T07:54:01Z` for commit `4ab5ce199a80dc6a2e8c6f382bcb6eeb3fa41b21`; this Git commit timestamp is not asserted to be the corresponding Activity push-event time. The preservation-history note must state this evidence boundary.

The earlier README's Revision 2 request paths do not match the actual filenames in the GPT sequence-fix directory. The companion `README_REV3.md` supplies an explicit mapping. No historical protocol, adoption record, VOID record, or preservation-branch README is rewritten by this review draft.

## 10. Former 20-push visibility experiment

The 20-push Activity visibility experiment is unnecessary for this candidate validity rule and remains **NOT AUTHORIZED**. The validity rule no longer depends on an independent observer retrieving the event before the target; the target is derived from `t_lock + B_lock`. The experiment would not establish the event timestamp's maximum clock lag and must not be used to justify that quantity.

The following read-only/local conformance work remains necessary:
1. capture and pin raw unauthenticated Activity request/response bodies and headers for the existing lab and the relevant existing repository records;
2. verify selected API version, schema, actor object, `before/after` null/zero encoding, ref-filter behavior, unfiltered repository-wide pagination, and lifecycle event order;
3. make the exact owner-charter, deterministic-ref, one-attempt, and target-parser checks locally reproducible;
4. run local mock tests for the exact drand round retry behavior, with no production round and no remote repository pushes;
5. provide the Revision 2 vector verifier source and raw run output as committed files. A separately authored verifier is acceptable if clearly labeled and independently reviewed; its result must not be represented as Claude's unobserved 10-check run.

## 11. Freeze blockers and required Claude verdicts

This design remains NOT ADOPTABLE until these items are resolved:

1. **Experiment registry:** identify the exact pre-existing canonical `experiment_id` in the study registry. Do not invent it at lock time.
2. **OAC record:** freeze the canonical OAC schema/path on protected `master`, with one protocol hash, one actor ID/login, one lock-ref path, and one attempt.
3. **Activity wire evidence:** archive raw unauthenticated response bodies/headers and prove the server-selected API version and actor/before-after fields needed by this lifecycle.
4. **Repository-wide scan:** demonstrate complete pagination over the OAC-to-lock interval and fail closed on 403/429, missing pages, or incomplete history.
5. **Timestamp policy:** review `B_lock = 300 s` explicitly as a policy margin, not a measured bound or a guarantee of clock accuracy.
6. **Target parser:** approve exact RFC 3339 parsing, fractional precision, timezone normalization, leap-second rejection, and strict equality behavior.
7. **Reconstructability:** approve the rule that reconstructable outcomes remain reportable despite later tampering, while genuinely unreconstructable outcomes become permanently NOT ASSESSABLE with no reroll.
8. **Verifier source/output:** review the committed Revision 2 verifier and its raw output; no claim is made about the missing source from the session ZIP.
9. **Preservation coverage:** complete a later Activity read of the preservation branch when rate limits permit; do not imply complete Activity coverage after 07:03:30Z until then.
10. **Separate relay review:** the two-relay v0.7 rule remains unchanged. Any single-relay proposal needs a separate cryptographic review.

Claude must issue separate `PASS` / `NOT PASS` verdicts for the lock design, OAC/fork prevention, one-attempt semantics, reconstructability/status semantics, Activity schema/ledger evidence, buffer and timestamp parser, preservation disclosure, and verifier. For each NOT PASS, identify the exact text and minimum correction.

## 12. Current disposition

- Revision 2 direction: accepted by GPT as the preferred architecture, with Revision 3 blockers addressed in this draft.
- Revision 3: candidate for fresh Claude review; not adopted.
- OAC and experiment ID: not yet created or frozen.
- Activity API raw wire evidence: not yet committed.
- `B_lock = 300 s`: proposed policy margin, not a measured or guaranteed bound.
- DigiCert RFC 3161: optional evidence seal only; not a validity gate.
- Two-relay v0.7 validation: unchanged.
- Revision 2 verifier: GPT's separate source and output prepared for review; not a beacon verifier.
- 20-push visibility test: NOT AUTHORIZED and not required by this design.
- Original attempted v0.7 lock: remains VOID FOR PRODUCTION USE.
- Production round, seed, or pair: none selected.
- R2 C2: NOT ESTABLISHED.
- No solver construction or execution authorized.
