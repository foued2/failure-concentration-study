# GPT v1.2.2 follow-up review manifest (Claude round 2)

**Branch:** `gpt/lc518-150-v1.2.2-claude-round2-fixes-2026-11-01`  
**Parent review branch:** `gpt/lc518-150-v1.2.2-c9-corrections-2026-11-01`  
**Parent commit:** `60021ea34d60e341ccbd02b887bec9a2c6234095`  
**Purpose:** Claude round-2 corrections A–C to the v1.2.2 C9 draft. Review-only. No bank generation or solver work.

## Files covered by this follow-up review

| Path | Git blob SHA |
|---|---|
| `lc518-150/review-v1.2/CORRECTIONS_RECORD_v1.2.2-draft.md` | `2f883f25335732fc0544d089099d6e7a80adb1a2` |
| `lc518-150/review-v1.2/GPT_REVIEW_C9_DRYRUN_AND_v1.2.2.md` | `34605e2f404d357e2a69511338da802585663027` |

The GPT independent-review note below is preserved unchanged from the parent branch. It documents the original v1.2.2 review and is not a substitute for review of the follow-up text.

## Source artifacts preserved unchanged

| Path | Git blob SHA |
|---|---|
| `lc518-150/review-v1.2/CORRECTIONS_RECORD_v1.2.1-draft.md` | `559c14c20f3fab554623712176382e2b856f2764` |
| `lc518-150/review-v1.2/c9-dryrun/REPORT_C9_DRYRUN.md` | `e7228c89e4b9fd7f7aa4ac9fa11e140fdd5b9711` |
| `lc518-150/review-v1.2/c9-dryrun/generator_c9_dryrun.py` | `34e391ada87c39b00457adcc375cced9e1ded12a` |

## Follow-up changes

- Fixed canonical identities are pre-reserved before any random draw; D5 random rows 3–8 are explicitly covered by that collision rule.
- Oracle-output attachment names, row schema, file hashes and bank-record hash references are pinned.
- The canonical-disjointness report schema and PASS/FAIL write sequence are pinned.
- The repository-authority paragraph is removed from the specification; permissions remain governed by separate owner direction.

## Scope

No bank files are included. No solver bodies, candidate execution, private mutation annex, or mutation assignments are included. C8/E3 remains open. The follow-up branch does not alter `master`, the v1.2.1 file, the original parent review branch, or any frozen v1.0 design document.
