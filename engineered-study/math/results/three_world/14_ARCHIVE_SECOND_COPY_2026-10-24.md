# Three-world archive — second verified copy (operational record)

**Date:** 2026-10-24
**Trigger:** review-conclusion directive from field lead (GPT) and Claude: secure a second verified copy of the local-only per-trial archive. Operational only; no scientific content changes. GitHub upload prohibited.

## What was copied

| Payload | Destination bytes |
|---|---:|
| 8 raw per-trial archives (`raw\W1.jsonl.gz` … `raw\MIX_1_0.jsonl.gz`) | 560,553,425 |
| `per_trial.json` | 31,466,869 |
| `manifest.json` | 6,243 |
| **Total** | **592,020,294** |

**Source:** `engineered-study\math\results\three_world\` (copy 1)
**Destination:** `C:\Users\pakla\failure-concentration-study-archive-backup\` (copy 2)

## Verification (all items passed)

1. robocopy: 8/8 files, 0 FAILED, 0 MISMATCH, 0 EXTRA.
2. For every payload file: source bytes = destination bytes = manifest bytes; source SHA-256 = destination SHA-256 = manifest SHA-256 (9/9 verified).
3. Source files re-hashed against the committed manifest in the same pass — all match.
4. `manifest.json`: destination copy identical to source (SHA-256 `16af20b8b92856f8a5336737039da43609128caa5eb188ef40e7f3181dca7575`).

Full per-file hash table and method notes: `VERIFICATION_RECORD.txt` inside the backup folder.

## Limitations and unsettled item (recorded, not closed)

Both copies currently reside on the same physical volume (C:). The copy protects against accidental deletion or corruption of the working repository, not against disk failure. It is therefore a **working copy, not yet an off-machine backup**. Transferring one copy to removable or otherwise separately controlled storage remains an open operational item for the controller (only select devices and no network/paste are available on this machine; no such device is currently attached). No GitHub upload, per the local-only freeze on per-trial archives.

## Status

Simulation-phase records remain closed by the review conclusion: **W1 FAILED; no further simulation warranted.** This record documents archive stewardship only.
