# LC518 C2 v0.7 Lock Timing Evidence Clarification

**Revision date:** 2026-11-28  
**Status:** Revised review copy. The earlier clarification remains preserved unchanged on the preservation branch. This revised copy does not amend historical records or authorize a draw.  
**Repository status of earlier copy:** committed on `preserve/lc518-c2-repair-packet-2026-11-28` at `6f4b6975dd956ea3303653aa3ac8f7a27be31646`; not merged to `master`; not adopted.

## 1. Purpose

This note separates four distinct quantities:

1. the timestamp written into the attempted owner-adoption record;
2. the Git commit's author/committer metadata and API `created_at` representation;
3. the server-assigned event-time value reported in GitHub's Repository Activity API; and
4. the time at which an independent public observer first retrieved that Activity record.

These quantities must not be treated as interchangeable.

## 2. Fixed target-round calculation

The attempted owner record states a lock timestamp of `2026-11-27T16:41:47Z` (Unix second `1795797707`). Under v0.7's pinned Quicknet schedule (genesis `1692803367`, period `3` seconds), the first round strictly after that timestamp is:

- Round: `34331448`
- Scheduled time: `2026-11-27T16:41:48Z` (Unix second `1795797708`)

The arithmetic is not disputed.

## 3. What the historical records report

The original adoption commit is `8cfa2bbfa90d868b12958e0b09ea8a5c3360d58e`. Its GitHub commit response reports a commit/committer time of `2026-11-27T16:41:59Z`.

The VOID record describes this value as “GitHub's server-side creation time” for the attempted adoption commit. That is the VOID record's wording. A Git commit timestamp or API representation of commit metadata must not, by itself, be described as the exact HTTP push-receipt time.

Claude separately reports a GitHub Repository Activity API `push` record:

- Record ID: `52144406651`
- Activity event timestamp: `2026-11-27T16:41:59Z`
- Expected ref/commit relationship: the adoption push for commit `8cfa2bbfa90d868b12958e0b09ea8a5c3360d58e`

The reported Activity timestamp is eleven seconds after the target round's scheduled time. This is a distinct server-assigned activity-time field; it must not be relabeled as the exact HTTP receipt instant or first-public-visibility time without evidence establishing those semantics.

The raw Activity API body, complete response headers, exact request URL and query parameters, pagination record, and independent unauthenticated response capture were not preserved in the original packet. Claude reports that the Activity record was re-readable publicly when checked. Until the raw response and request are preserved, the record's existence and field values remain a reported observation from Claude's review, not an independently archived wire artifact in this packet.

## 4. Disposable Activity API observations

Claude reports the following test-repository observations:

| Activity | Activity timestamp | Commit committer date | Difference |
|---|---:|---:|---:|
| Initial push | 20:13:28Z | 20:13:22Z | +6 s |
| Re-push of the identical commit | 20:14:21Z | 20:13:22Z | +59 s |
| Force-push | 20:14:27Z | 20:14:14Z | +13 s |

The re-push observation supports the conclusion that the Activity event-time value is not invariably a copy of the unchanged commit's committer date. It does not establish exact push-receipt time or first public visibility. The Activity record's field semantics must be pinned from the raw response at the actual endpoint and API version.

A further schema discrepancy remains open: GitHub's current REST documentation example shows `pushed_at`, `push_type`, and `pusher`; Claude reports the live response fields as `timestamp`, `activity_type`, and `actor`. The raw live response at the pinned endpoint is the schema authority for the implementation. Do not resolve this discrepancy by assuming either documentation or a third-party mirror matches the actual wire response.

## 5. Corrected interpretation

- The attempted owner-record time, Git commit metadata, Activity event timestamp, and first-public-visibility time are separate.
- The reported Activity record `52144406651` carries a timestamp of `16:41:59Z`, 11 seconds after the target scheduled time `16:41:48Z`.
- This is a server-assigned Activity event-time observation, not a claim that the exact HTTP receipt instant or first public retrieval time has been established.
- `Cache-Control: max-age=60` is a cache freshness lifetime, not a statement about timestamp resolution. It must not be converted into a “60-second timestamp resolution” rule. Record `Date`, `Age` when present, `ETag`, and `Cache-Control` with every raw response.
- A positive response containing the expected event is evidence that the response data existed by the time represented by that response/cache chain. A response that omits the event proves nothing about whether the event occurred; it may be stale, delayed, or incomplete. Absence claims require demonstrably fresh/cache-bypassing retrieval and complete pagination.
- The raw API request/response bundle and its SHA-256 should be preserved. A separate RFC 3161 TSA token may timestamp the evidence-manifest hash, but it does not authenticate the past TLS session or prove the body originated from GitHub. Later live re-query is required for corroboration; a mismatch or missing lifecycle history means `NOT ASSESSABLE / HALT`.

## 6. Disposition of the attempted lock

The original attempted v0.7 adoption remains **VOID FOR PRODUCTION USE**. The reported Activity timestamp is 11 seconds after the scheduled target round. This note does not reinstate the attempted lock and does not authorize round `34331448` or any replacement round.

The previous rule requiring proof that an independent observer retrieved the Activity record before the target is not carried forward in the proposed ledger-based amendment. That amendment is a separate review draft and cannot retroactively validate this attempted lock.

## 7. Scope

This note does not amend the v0.7 selection algorithm, its Quicknet identity, its target-round formula, or its pair-selection mathematics. It does not authorize production randomness, a seed, a pair, a new allocation, solver construction, or solver execution.