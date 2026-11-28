# LC518 C2 v0.7 Lock Timing Evidence Clarification

**Date:** 2026-11-28  
**Status:** Draft clarification for Claude review. Not committed. Historical records remain unchanged.

## 1. Purpose

This note separates three different times that were previously conflated:

1. the timestamp written into the attempted owner-adoption record;
2. the Git commit's committer/creation metadata; and
3. the time recorded for the repository push in GitHub's Activity API.

The three must not be treated as interchangeable without evidence.

## 2. Fixed round calculation

The attempted owner record states a lock timestamp of `2026-11-27T16:41:47Z` (Unix second `1795797707`). Under v0.7's pinned Quicknet schedule (genesis `1692803367`, period 3 seconds), the first round strictly after that timestamp is:

- Round: `34331448`
- Scheduled time: `2026-11-27T16:41:48Z` (Unix second `1795797708`)

That calculation is not disputed.

## 3. What the historical records establish

The original adoption commit is `8cfa2bbfa90d868b12958e0b09ea8a5c3360d58e`. Its GitHub commit response reports a commit/committer time of `2026-11-27T16:41:59Z`.

Claude separately reports a GitHub Activity API `push` record with ID `52144406651` and Activity timestamp `2026-11-27T16:41:59Z` for the adoption push.

The value `16:41:59Z` is eleven seconds after the target round's scheduled time. However, the raw Activity API body, response headers, exact `ref`, `before` and `after` values, and unauthenticated read-back are not yet preserved in the durable evidence packet. The commit timestamp alone must not be called GitHub's server receipt time.

## 4. What the disposable Activity API experiment adds

Claude reports the following observations from `foued2/lc518-activity-api-lab-20261127`:

| Activity | Activity timestamp | Commit committer date | Difference |
|---|---:|---:|---:|
| Initial push | 20:13:28Z | 20:13:22Z | +6 s |
| Re-push of the identical commit | 20:14:21Z | 20:13:22Z | +59 s |
| Force-push | 20:14:27Z | 20:14:14Z | +13 s |

This is evidence that the Activity timestamp is not invariably just a copy of the commit's committer date. The re-push of the same commit is particularly informative because its committer date remained fixed while the Activity time changed.

It is consistent with a GitHub-recorded activity/event time. It does not establish, to the second, when GitHub first accepted the ref update, nor when the Activity record first became publicly retrievable.

## 5. Corrected interpretation

The earlier statement that the Git commit's `created_at` timestamp alone proves server-side receipt at `16:41:59Z` is too strong and must be qualified.

The stronger evidence is the separately reported Activity record at `16:41:59Z`. Before treating that value as the authoritative publication time, the following must be preserved and checked:

- raw unauthenticated HTTP response body;
- raw response headers, including `Date`, `ETag`, `Cache-Control`, and `Link` if present;
- exact request URL, query parameters, API-version header and redirect behavior;
- the Activity record's exact identifier, ref, activity type, `before`, `after`, and timestamp field;
- proof that `after` equals the adoption commit SHA;
- independent read-back from a clean unauthenticated network;
- reconciliation of the live response fields with the current GitHub documentation example, which currently displays `pushed_at`, `push_type`, and `pusher`, while observed/live schema reports use `timestamp`, `activity_type`, and `actor`.

A further distinction remains essential: the Activity event timestamp and the first time an independent public observer could retrieve that event are different quantities. A pre-target lock requires evidence that the lock artifact/event was publicly observable before the target beacon was available, not merely a timestamp field that appears to precede it.

## 6. Disposition of the attempted lock

The original attempted v0.7 adoption remains **VOID FOR PRODUCTION USE**. No pre-target public recording has been established in the preserved evidence. This note does not reinstate the attempted lock and does not authorize round `34331448` or any replacement round.

The specific explanation “the commit timestamp proves it was exactly eleven seconds late” must not be repeated as an established server-receipt fact. The Activity API observation is a stronger, separate line of evidence, but its raw response and timing semantics still require evidence preservation and review.

## 7. Scope

This note does not amend the v0.7 selection algorithm, its Quicknet identity, its target-round formula, or its pair-selection mathematics. It does not authorize production randomness, a seed, a pair, a new allocation, solver construction, or solver execution.