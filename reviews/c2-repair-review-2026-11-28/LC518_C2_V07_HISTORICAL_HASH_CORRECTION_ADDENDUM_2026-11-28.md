# LC518 C2 v0.7 Historical Hash Correction Addendum

**Date:** 2026-11-28  
**Status:** Correction record prepared for independent review. Not committed. Does not amend or replace either historical Git commit.

## 1. Purpose

This addendum corrects one transcription error in the protocol SHA-256 recorded in the historical owner-adoption and void records for LC518 R2 C2 protocol v0.7.

It does not rewrite Git history, alter the original adoption record, alter the later VOID record, reinstate the attempted lock, or authorize a production draw.

## 2. Correct protocol identity

The corrected v0.7 protocol artifact is:

- Path: `reviews/LC518_R2_C2_SELECTION_PROTOCOL_v0.7_2026-11-27.md`
- Review branch: `review/lc518-c2-v07-corrected-2026-11-27`
- Commit: `ac092ab32023d4821f8bffdf1c188906a7f096e7`
- Correct SHA-256 of the protocol bytes, as verified in the prior Luna/Claude evidence record:

  `05f432c1d6caa5eefcf4f8c0d76954aa769e04d1f10f72473daa832855485f3c`

## 3. Historical records containing the typo

The following two historical records contain the same incorrect digest:

1. Original adoption/lock commit `8cfa2bbfa90d868b12958e0b09ea8a5c3360d58e`.
2. Subsequent void-record commit `24e973fc8517d5467807446f915841896b65f8a4`.

Both records identify the protocol with this incorrect digest:

`05f432c1d6caa5eefcf4c8d0d76954aa769e04d1f10f72473daa832855485f3c`

The incorrect sequence is `...fcf4c8d0...`; the correct sequence is `...fcf4f8c0...`.

The correction is a transcription correction to the identity field. It does not indicate that the two historical records refer to different v0.7 protocol versions. The exact v0.7 artifact at the cited commit is the corrected artifact identified in §2.

## 4. Required interpretation

Readers must interpret the historical records as follows:

- The digest printed in those two records is wrong.
- The corrected protocol digest is the one in §2.
- The original adoption record remains preserved as historical evidence of the attempted action.
- The later VOID disposition remains operative for that attempted production selection.
- The hash correction does not cure the separate timing/publication-evidence problem and does not revive the adoption.

No historical file or commit is to be edited, rebased, force-pushed, or deleted to make this correction.

## 5. Timing evidence is a separate issue

The original VOID record also states that the adoption commit's GitHub `created_at`/commit timestamp establishes that the lock was recorded at `2026-11-27T16:41:59Z`, eleven seconds after the target round's scheduled time of `16:41:48Z`.

That statement must not be treated as independently established server-receipt time merely because the commit metadata reports that date. A Git commit timestamp is commit metadata. The separate GitHub Activity API record for push ID `52144406651` was reported by Claude as carrying an activity timestamp of `16:41:59Z`, but its raw response body and headers have not yet been preserved in a durable evidence packet.

The disposable Activity API lab provides evidence that Activity timestamps can differ from the pushed commit's committer date: Claude reports differences of +6 seconds, +59 seconds for a re-push of the same commit, and +13 seconds for a force-push. That supports treating the Activity timestamp as a distinct event-time field, but it does not by itself establish exact receipt-time semantics or first-public-visibility time.

A separate timing-evidence clarification is therefore required. This hash addendum does not decide that issue.

## 6. Disposition

**Historical hash correction: prepared.**  
**Original adoption/lock: remains VOID for production use.**  
**Production round, seed, and pair selection: none authorized or performed.**  
**Original R2 C2: NOT ESTABLISHED.**
