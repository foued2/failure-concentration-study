# Preservation record — untracked files vs incoming master paths

**Date:** 2026-11-18
**Working tree:** `C:/Users/pakla/PycharmProjects/failure-concentration-study`
**Branch:** `research/concentration-math-spec` at `de39291`
**Purpose:** identify which locally untracked files would be overwritten by a merge of
`master` (`33dca9b`) or any of the three branches based on it, and record their bytes
before any such operation.

## Result: one collision, not three

| Path | Local state | Collides |
|---|---|---|
| `VERIFICATION_LOG.md` | untracked, 123 lines | **yes** |
| `SHA256SUMS` | absent locally | no (merge would only add it) |
| `execution_protocol_v1.md` | absent locally | no (merge would only add it) |

The earlier statement that all three were "present locally as untracked files" was
wrong. `Test-Path SHA256SUMS` and `Test-Path execution_protocol_v1.md` both return
False at the repository root. Only `VERIFICATION_LOG.md` is at risk.

Method: union of paths added by `master` and the three branches since merge base
`edae42c` (17 paths), intersected with `git ls-files --others --exclude-standard`
(75 paths) and `git diff --name-only` (4 paths).

## The colliding file

```
path                 VERIFICATION_LOG.md
local state          untracked
master blob          2909 bytes,  37 lines, sha256 dc332b70f16817b5feb38613df5b3e0a102aba813c59348f375b8ec138ce536b
local file          11574 bytes, 123 lines, sha256 09a9393cd60a1639a26ac0dd13439ad6168ed2c3d35bca5545356320907335ea
canonical (LF)      master dc332b70…, local 09a9393c…
byte prefix         master bytes are an exact prefix of local bytes
appended suffix     8665 bytes (the two 2026-11-05 addenda)
identical           no
```

Because master's bytes are an exact prefix, the local file **strictly extends** the
committed version. Committing the local file, if that is ever wanted, preserves every
byte master holds; nothing is lost either way.

## Tracked-path overlap

The only path added by the branches that research already tracks is
`v02/FINDINGS_LEDGER_2026-10-19.md`, and both sides carry the identical blob
`19765efb`. `git merge-tree --write-tree` against each of the three branches reports no
conflicted paths.

A clean merge tree does not cover working-tree collisions; this record does.

## Rule

Until a decision is recorded, `VERIFICATION_LOG.md` must not be deleted, overwritten,
checked out over, or `git clean`ed. Resolution options, in order of safety:

1. Copy it outside the repository first (this record is that copy's inventory).
2. Commit it on a branch before any merge, so Git sees a tracked successor rather than
   an untracked obstruction.
3. Move it aside manually before merging, then reconcile the two versions by hand.

## Superseded claim

The 2026-11-18 statement that the validator's canonical SHA-256 differed from the
committed blob is withdrawn. That comparison passed a Git blob through a PowerShell
text pipeline, which re-encoded it. Byte-level recomputation gives an exact match:
`8e28b45e08a1726831c2bfc9b1f1c6aa8766b579fa6dae87c2004ec708dce630`.
