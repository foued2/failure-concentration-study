# LC518 C2 v0.7 Historical Hash Correction Addendum

**Revision date:** 2026-11-28  
**Status:** Revised review copy. The earlier addendum remains preserved unchanged on the preservation branch. This revised copy is not adopted and grants no production authority.  
**Repository status of earlier copy:** committed on `preserve/lc518-c2-repair-packet-2026-11-28` at `6f4b6975dd956ea3303653aa3ac8f7a27be31646`; not merged to `master`; not adopted.

## 1. Purpose

This addendum corrects one transcription error in the protocol SHA-256 recorded in the historical owner-adoption and VOID records for LC518 R2 C2 protocol v0.7.

It does not rewrite Git history, alter the original adoption record, alter the later VOID record, reinstate the attempted lock, or authorize a production draw.

## 2. Correct protocol identity

The corrected v0.7 protocol artifact is:

- Path: `reviews/LC518_R2_C2_SELECTION_PROTOCOL_v0.7_2026-11-27.md`
- Review branch: `review/lc518-c2-v07-corrected-2026-11-27`
- Commit: `ac092ab32023d4821f8bffdf1c188906a7f096e7`
- Correct SHA-256 of the protocol bytes:

  `05f432c1d6caa5eefcf4f8c0d76954aa769e04d1f10f72473daa832855485f3c`

## 3. Historical records containing the typo

The following two historical records contain the same incorrect digest:

1. Original adoption/lock commit `8cfa2bbfa90d868b12958e0b09ea8a5c3360d58e`.
2. Subsequent VOID-record commit `24e973fc8517d5467807446f915841896b65f8a4`.

Both records identify the protocol with this incorrect digest:

`05f432c1d6caa5eefcf4c8d0d76954aa769e04d1f10f72473daa832855485f3c`

The incorrect sequence is `...fcf4c8d0...`; the correct sequence is `...fcf4f8c0...`.

This is a transcription correction to the identity field. It does not indicate that the two historical records refer to different v0.7 protocol versions. The exact v0.7 artifact at the cited commit is the corrected artifact identified in §2.

## 4. Required interpretation

Readers must interpret the historical records as follows:

- The digest printed in those two records is wrong.
- The corrected protocol digest is the one in §2.
- The original adoption record remains preserved as historical evidence of the attempted action.
- The later VOID disposition remains operative for that attempted production selection.
- The hash correction does not cure the separate timing/publication-evidence problem and does not revive the adoption.

No historical file or commit is to be edited, rebased, force-pushed, or deleted to make this correction.

## 5. Timing evidence is separate from the hash correction

The VOID record describes the attempted adoption commit's time as “GitHub's server-side creation time” and records `2026-11-27T16:41:59Z`. That wording must be quoted as the VOID record's own statement. It must not be expanded into a claim that a Git commit's committer timestamp independently proves the exact instant GitHub received the push.

Claude separately reports a GitHub Repository Activity API `push` record:

- Activity record ID: `52144406651`
- Reported event timestamp: `2026-11-27T16:41:59Z`
- Target round: `34331448`
- Target scheduled time: `2026-11-27T16:41:48Z`

The reported Activity timestamp is 11 seconds after the target's scheduled time. It is a distinct Activity event-time field and is stronger evidence for the push event than commit metadata alone. It is not, without a pinned semantic definition, proof of the exact HTTP receipt instant or the first moment an independent observer could retrieve the event.

The raw Activity response body, complete response headers, exact request URL/query parameters, and unauthenticated read-back are not included in the original packet. Claude reports that the record was publicly retrievable on re-query; that observation must remain attributed to Claude unless the raw response and request are separately captured and preserved.

## 6. Disposition

**Historical hash correction:** revised review copy prepared.  
**Original adoption/lock:** remains VOID FOR PRODUCTION USE.  
**Round `34331448`:** must not be used under the attempted lock.  
**Production round, seed, and pair selection:** none authorized or performed.  
**Original R2 C2:** NOT ESTABLISHED.