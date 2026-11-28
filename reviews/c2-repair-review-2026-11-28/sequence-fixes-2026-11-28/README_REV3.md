# LC518 C2 Sequence-Fix Review Materials, Revision 3

**Date:** 2026-11-28  
**Branch:** `review/lc518-c2-sequence-fixes-2026-11-28`  
**Status:** Technical review drafts only. No protocol adoption or production authority.

## Preferred design

The primary candidate is the parent-directory file:

`../LC518_C2_ACTIVITY_API_DRAND_REPAIR_AND_CLAUDE_REVIEW_2026-11-28_REV3.md`

It supersedes GPT's earlier TSA/300-second alternative as the preferred design and addresses Claude's three blockers: protocol-hash forked locks, invalid attempt/replacement semantics, and post-lock reconstructability. The earlier TSA draft remains preserved as an audit alternative, not as a competing adopted design.

GPT's adjudication is:

`GPT_ADJUDICATION_OF_CLAUDE_REVIEW_2026-11-28_REV3.md`

Claude's fresh review instructions are:

`../CLAUDE_FOLLOWUP_REVIEW_REQUEST_LC518_C2_REV3_2026-11-28.md`

## Source evidence

- `verify_lc518_c2_v07_vectors_REV2.py`
- `VERIFY_LC518_C2_V07_VECTORS_REV2_OUTPUT_2026-11-28.txt`
- `LC518_C2_PRESERVATION_BRANCH_HISTORY_NOTE_2026-11-28_REV2.md`
- `GIT_BLOB_INVENTORY_REV3.md`

The verifier is GPT-authored. The exact committed source was run locally and produced ten passing checks. It covers deterministic vector/framing/rejection-loop logic only. It does not fetch drand or validate BLS.

## Earlier documents preserved

The Revision 1/2 history, hash/timing corrections, initial review instructions, previous GPT amendment alternative, and earlier adjudication remain in the directory. No historical draft has been overwritten. Refer to the parent `README_REV3.md` for exact mapping to the Revision 2 packet's expected filenames.

## Remaining blockers

The canonical experiment ID is absent from the current reviewed master tree and must be sourced from an earlier study registration. The immutable OAC, raw Activity wire schema/actor fields, full repository-wide Activity pagination, timestamp assumptions, local drand mock tests, later preservation Activity coverage, and offline Git-object bundle remain outstanding.

The 20-push visibility experiment remains NOT AUTHORIZED. No master change, owner adoption, production lock, target round, seed, pair, or solver execution is authorized.