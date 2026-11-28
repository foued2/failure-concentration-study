# LC518 R2 C2 Repair Review and Claude Decision Packet

**Date:** 2026-11-28  
**Prepared by:** GPT technical review  
**Status:** Candidate corrections and test requirements. Not v0.11. Not committed. Not adopted. No production selection is authorized.

## 1. Executive decision

The selection mathematics in v0.7 remain intact. An independent Python recomputation confirmed the canonical 28-pair universe hash and all four listed SHA-256 test vectors. The two normal fixture indices produce `M01/M07` and `M04/M07` exactly as stated.

The current blockers are procedural and evidentiary, not a demonstrated defect in the two-stage pair-selection mapping:

1. Correct the historical digest transcription in a separate addendum.
2. Correct the overstatement that commit metadata alone proves server receipt time.
3. Resolve the raw Activity API response schema and test whether its lock event becomes publicly retrievable before the target round.
4. Define and test same-round drand retrieval behavior, including real HTTP availability failures.
5. Obtain Claude's scoped PASS/NOT PASS on the exact correction texts and any protocol amendment before adoption.

Do not create a canonical composite or label a new protocol version complete until items 3 and 4 have adequate evidence.

## 2. Verified selection-math recomputation

Using the exact v0.7 framing:

`ASCII("LC518-REV11-C2-v1") || 0x00 || seed[32] || 0x00 || ASCII(label) || 0x00 || uint64_BE(counter)`

with the stated synthetic seed, standard-library SHA-256 independently reproduces:

| Label | Counter | n | Digest | Index |
|---|---:|---:|---|---:|
| repeat-1 | 0 | 28 | `996627683d5bd28b1445281d42762ae3c0fafaca315c33deb096582a9970f659` | 5 |
| repeat-1 | 1 | 28 | `c59aff206cf93ecd342e7b6a70af095a0e40ff1d3cfffe38e13b74ec70fd0ddb` | 23 |
| repeat-2 | 0 | 27 | `bce13a787bba4cf2849ecc7f9291e17459543545a9162f34b0f37a7256474881` | 19 |
| repeat-2 | 1 | 27 | `8f096ae539624f40ea1ad9a5bf6272e0673c0e85d33f48971d7719edb55f3561` | 13 |

The canonical pair universe is 28 entries, 224 ASCII bytes including the final LF, with SHA-256 `d5e54cd8a071fde1fd06a897b611fb9d39bfa28f5aeecb06e46537a2f93149bd`. The normal fixture maps to `M01/M07` and `M04/M07`.

This independently checks the published test vectors and universe representation. It does not reproduce the drand verification package or authorize a production draw.

## 3. Historical hash correction

The exact corrected v0.7 SHA-256 is:

`05f432c1d6caa5eefcf4f8c0d76954aa769e04d1f10f72473daa832855485f3c`

Both historical records contain:

`05f432c1d6caa5eefcf4c8d0d76954aa769e04d1f10f72473daa832855485f3c`

Affected commits:

- Original adoption: `8cfa2bbfa90d868b12958e0b09ea8a5c3360d58e`
- Void record: `24e973fc8517d5467807446f915841896b65f8a4`

The separate correction addendum preserves both commits and the existing VOID disposition. It must not be used to imply that the lock is valid.

## 4. Activity API: factual findings and unresolved protocol requirements

### 4.1 Lab existence and lifecycle coverage

The scratch repository is `foued2/lc518-activity-api-lab-20261127`, not `fouda/...`. The earlier 404 resulted from the wrong owner string. Claude reports the repository is public and its Activity ledger contains seven records: one `main` branch creation plus six records for the test branch.

The test-branch ledger reports:

- branch creation;
- push;
- deletion;
- same-name recreation;
- re-push of the identical commit;
- force-push.

A `ref=` query reportedly returns the six test-branch events in order. This is meaningful lifecycle evidence. GPT's earlier withdrawal of the experiment claim was premature and is corrected here.

### 4.2 What the timestamps establish

The test reports Activity times +6 seconds, +59 seconds and +13 seconds relative to commit committer dates for the initial push, identical-commit re-push and force-push. The +59 second re-push is strong evidence that the Activity event time is not merely copied from the unchanged commit's committer date.

Do not overstate this as a proven exact server-receipt timestamp. It is an Activity event-time field. The time an event occurs and the time an independent public observer can first retrieve it are distinct. The latter is the critical property for a pre-target lock.

### 4.3 Response schema discrepancy

Claude reports live response fields:

`id`, `node_id`, `before`, `after`, `ref`, `timestamp`, `activity_type`, `actor`.

The current official GitHub REST documentation example for `GET /repos/{owner}/{repo}/activity` displays:

`id`, `node_id`, `before`, `after`, `ref`, `pushed_at`, `push_type`, `pusher`.

These must not be conflated. The exact raw HTTP body and headers from the lab must be archived, then compared against the current official OpenAPI description and versioned docs. A connector-normalized representation is insufficient to pin a wire schema.

### 4.4 API request contract to test

Endpoint:

`GET https://api.github.com/repos/{owner}/{repo}/activity`

The current GitHub documentation lists:

- `ref`, accepting `refs/heads/BRANCH_NAME` or `BRANCH_NAME`;
- `time_period`, with `day`, `week`, `month`, `quarter`, `year`;
- `direction`, `asc` or `desc`;
- `per_page`, maximum 100;
- `before` / `after` pagination cursors from `Link` headers;
- response status `200` and `422` for validation failure or endpoint spam.

For all controlled tests, explicitly set `ref`, `time_period`, `direction`, and `per_page`. Do not rely on undocumented defaults. Follow the actual `Link: rel="next"` URL, but fail closed if it changes host or leaves the documented API origin. Preserve all pages and headers.

Suggested initial audit query for a one-use lock ref:

`?ref=refs%2Fheads%2F<unique-lock-ref>&time_period=year&direction=asc&per_page=100`

This is a proposed test query, not yet a production protocol clause. The actual `Link` URLs, pagination behavior, query stability, and schema must be captured before the request form is frozen.

Headers to pin and preserve:

- `Accept: application/vnd.github+json`
- `X-GitHub-Api-Version: 2026-03-10`

The unauthenticated public-resource case must be tested from a clean network. Preserve `Date`, `ETag`, `Cache-Control`, `Vary`, `Link`, `Content-Type`, `Retry-After`, `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, and any other `X-GitHub-*` headers returned. Record redirects; do not silently follow a redirect to an unapproved host.

Rate limits materially constrain the experiment. GitHub documents a primary unauthenticated REST limit of 60 requests per hour per originating IP, plus secondary limits; a 403/429 must be handled using `Retry-After` or `X-RateLimit-Reset`, not by rapid polling. Plan the 20-trial experiment across enough time to remain below the unauthenticated budget, or use an authenticated measurement client plus a separately rate-limited unauthenticated public-observer confirmation. Do not conceal/censor rate-limited trials: record them as censored and do not use them to claim a visibility-latency bound.

### 4.5 Required timing/visibility experiment

Before Activity API can be a production lock witness, run at least 20 controlled pushes in the existing disposable lab, subject to explicit authorization for those writes.

For each trial:

1. Create a unique one-use branch/ref and push one fixed test commit.
2. Record local monotonic time and a UTC clock-health/uncertainty snapshot immediately before and after the push.
3. Poll the Activity endpoint on a predeclared fixed schedule; use an unauthenticated public read from a clean network.
4. Preserve every request URL, response status, raw response body, raw headers, client monotonic send/receive times, and the first response in which the expected activity record appears.
5. Validate that the record's `after` equals the exact expected commit, its `ref` is exact, and its type is the expected `branch_creation` or `push`.
6. Repeat a read after first visibility to test stable ID, timestamp, ordering, and cache behavior.

Report per-trial event timestamp, push time interval, first-visibility interval, `Date` header, cache headers, and latency summaries (min/median/p95/max). Include missing records and 422s; never discard failed trials.

This is an external repository write test. No new refs or pushes should occur until the owner has explicitly authorized the 20-trial run.

### 4.6 Minimum acceptance criteria

Activity API is not acceptable as the sole pre-target lock witness until all of the following are satisfied:

- raw live schema is unambiguous and pinned;
- ref filter returns the expected event and excludes unrelated refs;
- one-use branch creation cannot be mistaken for later pushes, deletion, recreation, or force-push;
- all pages can be retrieved, with no silent truncation;
- independent unauthenticated observer can retrieve the exact lock record before the derived target round;
- the API response `Date` and the observer's time evidence place that successful retrieval before the target;
- visibility delay is measured and an operational cutoff is set from evidence;
- event timestamp semantics are accurately described, without equating it to the exact HTTP receipt instant;
- raw evidence is archived and hashed.

If the record first becomes observable after the target round is scheduled or published, the attempted lock is void even if the Activity timestamp is earlier.

## 5. drand retry: review of current v0.7 and Luna's demonstration

### 5.1 What was demonstrated

Luna reports a testnet-only `quicknet-t` demonstration using `drand-client@1.4.2`, round 42, with Protocol Labs and Cloudflare. Both independently verified responses yielded the same signature and derived seed. A locally injected exception before a request was followed by a successful request to the exact same round/URL.

This establishes a narrow harness capability. It does not test a real HTTP 404, 429, 5xx, connection reset, timeout after a request was sent, or truncated HTTP body.

### 5.2 Existing v0.7 rule

V0.7 currently requires two separately configured relay clients and both responses to pass the complete validation sequence before `RELAY_AGREEMENT`. Its production instruction requires both pinned relay origins and aborts on any verification failure or relay disagreement.

Therefore, retry policy and relay quorum are protocol amendments. They cannot be introduced as implementation details while retaining the old v0.7 PASS.

### 5.3 Candidate transport rule for Claude review

The following is a proposed amendment, not an adopted rule:

- The target round and the exact request path are fixed before retrieval. Every retry uses that same round and chain path. No fallback to `/latest`, no round substitution, no reroll.
- Retry only availability/transport outcomes: DNS failure, connection failure/reset, TLS transport failure, timeout, incomplete/truncated response, HTTP 404, HTTP 408, HTTP 429, and HTTP 5xx. Respect a valid `Retry-After` without extending beyond a separately predeclared terminal deadline.
- Do not retry 200 responses that fail JSON, chain identity, round identity, encoding, signature-format, or BLS verification. Mark that relay response invalid and preserve it.
- Treat other non-retryable 4xx responses and unexpected redirects as terminal configuration/protocol errors.
- The retry schedule, per-attempt timeout, `Retry-After` handling, maximum elapsed window, and terminal behavior must be fixed in the protocol after testnet/mock evidence. Do not invent these values from the current one-shot demonstration.

### 5.4 Candidate relay-availability correction

The existing “both relays must succeed” rule creates an availability veto: one relay can withhold or corrupt its response and force an abort even when the other supplies a valid target beacon.

Candidate rule for Claude's cryptographic review:

- Each relay response is validated independently against the pinned chain and exact target round.
- The first response that passes all cryptographic and identity checks is sufficient to establish the beacon value because validity is checked against the pinned public key, not trusted from the relay.
- The other relay is a corroborating source, not a mandatory availability quorum. If it later supplies a valid response, require byte-identical signature and identical round. A different response that also claims to validate is an integrity alarm and must fail closed.
- An invalid or unavailable second relay must not erase the already validated beacon from the first relay; record that relay as failed/unavailable.

This changes v0.7 §4 `RELAY_AGREEMENT` and §7's “both relay origins” requirement. It requires Claude to examine the BLS uniqueness assumption for the pinned scheme, the implementation's validation path, and whether any trust or availability assumptions are being changed. No silent edit is permitted.

### 5.5 Required local/mock and testnet tests

Use a local mock server for deterministic fault cases:

- 404 for the first N attempts, then a valid same-round response;
- 429 with valid and invalid `Retry-After` values;
- 500/502/503;
- connection refused/reset;
- timeout before response;
- timeout after headers;
- truncated JSON/body;
- 200 malformed JSON;
- wrong chain identity;
- wrong round;
- malformed signature hex;
- wrong signature length;
- well-formed but invalid BLS signature;
- one relay unavailable while the other supplies a valid beacon;
- two relays returning the same valid beacon;
- two relays returning conflicting injected payloads.

Use the testnet `quicknet-t` chain for controlled real publication-behavior checks, not a production mainnet round. Poll a round several rounds ahead of schedule on both relays and record status codes, response headers, actual first publication time, cache behavior, and retry count. Do not query a production target.

The `quicknet-t` testnet chain hash `cc9c398442737cbd141526600919edd69f1d6f9b4adb67e4d912fbc64341a9a5` is distinct from the production Quicknet hash `52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971`. Testnet evidence must never be presented as production-beacon evidence.

### 5.6 Candidate retry schedule is not yet fixed

Do not choose attempt intervals or a terminal deadline until the testnet publication observations and local mock tests are complete. The production protocol must specify finite, deterministic retry times, a per-attempt timeout, maximum elapsed window, and terminal failure. If that window expires, the one draw fails; the protocol must not move to a later drand round under the same lock.

## 6. Publication mechanism: decision remains open

The Events API is not a viable timing gate. The Activity API is promising but not accepted yet.

Do not create the canonical composite until the Activity evidence questions are resolved. A candidate one-use branch could contain a lock manifest with the exact protocol SHA-256 and verifier/evidence hashes, while the Activity record's `after` identifies the immutable commit. The lock manifest must not contain a self-referential Activity timestamp or target round; those are derived from the external record after publication.

A valid lock would require both:

1. the exact immutable lock artifact and matching Activity record; and
2. evidence that an independent public observer retrieved that exact record before the target beacon was available.

If this cannot be demonstrated robustly, choose a simpler timestamping method or revisit whether external randomness is required. Do not compensate by adding more undocumented polling machinery.

## 7. Current decisions and boundaries

- Corrected v0.7 selection math: retained; independently recomputed test vectors pass.
- Historical hash correction: draft addendum prepared separately.
- Timing clarification: draft note prepared separately; no historical file rewritten.
- Activity API: viable candidate for further controlled measurement, not yet approved.
- Events API: rejected as a lock witness.
- drand transport retry: candidate proposal only; policy not yet adopted.
- Relay availability rule: candidate proposal only; it changes v0.7 and requires fresh review.
- v0.10: remains NOT PASS.
- v0.11: not produced.
- Canonical composite: not produced.
- Production drand round, seed, and pair selection: none queried or selected.
- R2 C2: NOT ESTABLISHED.

## 8. Explicit Claude review request

Review the following exact artifacts and issue separate explicit verdicts:

1. `LC518_C2_V07_HISTORICAL_HASH_CORRECTION_ADDENDUM_2026-11-28.md` — PASS/NOT PASS for historical accuracy and preservation of the audit trail.
2. `LC518_C2_V07_TIMING_EVIDENCE_CLARIFICATION_2026-11-28.md` — PASS/NOT PASS for the distinction among commit metadata, Activity event timestamp, and first public visibility; confirm whether the existing VOID wording needs further qualification.
3. This repair-review packet — PASS/NOT PASS for the Activity API test contract, schema qualification, pre-target visibility criterion, drand transport retry proposal, and proposed relay-availability change.

For each NOT PASS, identify the precise sentence or rule, why it fails, and the minimum correction. Do not treat a review of these drafts as review of a canonical v0.11 protocol. Do not grant a PASS to unperformed tests or evidence that is only reported rather than raw and preserved.

## 9. Primary references

- GitHub REST API: List repository activities: https://docs.github.com/en/rest/repos/repos#list-repository-activities
- GitHub REST API pagination: https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
- GitHub REST API rate limits: https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api
- drand developer getting started and chain identities: https://docs.drand.love/developer/
- drand HTTP API and testnet endpoints: https://docs.drand.love/developer/API-v2/drand-http-api/
- drand-client implementation: https://github.com/drand/drand-client
