# ADDENDUM - RLC-0 ARCHIVAL INTEGRITY NOTE (2026-10-14 B)

Provenance: prepared 2026-10-14 after GPT's independent C3 audit of the published repository
(foued2/failure-concentration-study) found a defect in `evidence/C2/MANIFEST.sha256`, and CLAUDE
reviewed the finding and proposed this append-only record. This note does NOT amend the closure
record (`ADDENDUM_2026-10-14.md`, commit 94fd572) and does NOT modify any frozen file. No seed was
compiled, executed, or submitted to CBMC. No CBMC run, experiment, flag, budget, or protocol change
occurred. The scientific disposition of RLC-0 is unchanged.

## 1. Defect: committed C2 manifest has no filenames (confirmed locally)

GPT's audit finding was reproduced locally on the working tree, which is byte-identical to the
published commit (FREEZE.md section 5 re-verified 26/26 after this note was written):

- `rlc0/evidence/C2/MANIFEST.sha256` has exactly 78 lines; every line is exactly 70 characters and
  has the form `<64-hex>  raw/` — the filename after `raw/` is absent on every line.
- 0 of 78 lines match the format documented in FREEZE.md section 5.4 and section 7
  (`<sha256>  raw/<name>`, sorted by name).
- The manifest's own SHA-256 is unchanged and matches FREEZE.md section 5.4
  (dfe43258d4dc9cec2fac7fb1a1cedfea5ca2996d3f489882a7c177a60451c45d); the defect is in the recorded
  content itself, present since commit 20d9c59, not later corruption. The manifest file was NOT
  edited for this note (editing it would break the recorded hash).

Consequence: as committed, the manifest cannot serve as a per-file name-to-hash record. Anyone
following FREEZE.md section 7 and running `fc.exe` against a correctly regenerated manifest would
get a full-file difference.

## 2. Independent recomputation result: hash multiset matches 78/78

A fresh recomputation (2026-10-14, MIMO, read-only over `evidence/C2/raw/`) with explicit counts:

- Files enumerated in `raw/`: **78** (matches the documented count).
- Hashes parsed from the published manifest: **78**.
- SHA-256 computed over working-tree bytes of each file: **78**.
- Sorted multiset comparison of the two 78-element hash lists: **78 / 78 position matches, 0
  differences, 0 files missing, 0 extra files**.
- Duplicate hashes within each list are explained by genuinely identical file contents (e.g. 12
  empty/identical `base_*.err.txt` sidecars share one hash; 6 identical `r2_*.err.txt` OOM stderr
  texts share one hash; 12 baseline-vs-r2 stdout pairs are byte-identical, consistent with
  RESULTS.md sections 5.2-5.3).

Conclusion: the 78 hashes in the published manifest ARE the hashes of the 78 real evidence files.
The evidence content is intact; only the name-to-hash association was lost at generation.

Sidecar record created (append-only, new file; not part of FREEZE.md section 5):
`rlc0/evidence/C2/MANIFEST_recomputed.sha256` — 78 lines in the documented format
(`<sha256>  raw/<name>`, sorted by name), 7407 bytes, SHA-256
75425e6396a4966d982dbe832b3fb074bb3858b814adce46d4758b233f9ea9e0. This sidecar supplies the mapping
the committed manifest lacks; it does not replace or alter the committed manifest.

## 3. Likely cause (hypothesis; original command not preserved)

No manifest-generation script is committed in the repository. The observed byte pattern (correct
hashes, empty names, uniform 70-character lines = 64 hex + 2 spaces + `raw/`) is consistent with a
PowerShell generation loop in which the filename component evaluated to empty on every iteration —
for example iterating over `Get-ChildItem -Name` output (plain strings, which have no `.Name`
property) while formatting `raw/$($_.Name)`, which interpolates to `raw/`. This is a hypothesis
consistent with the observed file; the original command is not in the record and intent is not
inferred. Recorded as an archival generation defect.

## 4. Correction of the prior internal verification claim

An earlier internal (MIMO) verification report stated the C2 manifest "reproduces 78/78, 0
mismatches". Given the committed manifest contains no filenames, that claim must be read narrowly:
it may have compared hash multisets (which this note now confirms are correct) or it may have been
vacuous — a parse-then-compare loop that asserted only zero mismatches among lines it could parse
without asserting a parse count, which reports "0 mismatches" for a file it never matched. The exact
prior command is not reconstructible from the retained context. What is now established, with
explicit counts (section 2): the hash multiset is correct 78/78; the name mapping was never
verified by anyone, internal or external, until GPT's audit found it absent. Any future verification
of this record must print parse counts and file counts, not only mismatch counts.

## 5. B0.5 run_log.txt encoding caveat (GPT audit finding, recorded)

GPT reproduced the FREEZE.md hash of `evidence/B0.5/run_log.txt` only after reconstructing the
original Windows console (non-ASCII) byte encoding in addition to CRLF line endings. This is an
encoding-provenance caveat of the same class as the documented line-ending provenance (FREEZE.md
section 7; commit 15e040e): the working-tree bytes, not Git blob bytes, are the recorded
convention, and at least this one file additionally carries a legacy console codepage. Recomputers
must reproduce the original byte encoding, not assume UTF-8. Content is unchanged.

## 6. Gate status update

- C3 (independent verification): PARTIALLY SATISFIED, now with one component upgraded. GPT
  independently verified: master at 94fd572, closure commit touches only the addendum, no rlc0*
  tag, bundle and ZIP transfer hashes, all 26 FREEZE.md hashes under the documented byte
  provenance, and the seed-3 witness defect from source. The C2 raw-evidence content integrity is
  now independently checkable and checks out (section 2 multiset result; GPT and MIMO independently
  obtained the same published bytes). What remains unsatisfied: the committed manifest is defective
  as a name-to-hash record (section 1), and full Git-history cloning via bundle was not exercised
  in GPT's environment (not needed; the public repository serves the same history).
- C2 remains NOT SATISFIED for its original purpose (canary FAIL never observed); unchanged.
- Scientific disposition unchanged: full-domain certification was not demonstrated; no seed
  verdicts exist; the seed-3 witness defect remains recorded and uncorrected.

## 7. Security note

A GitHub OAuth credential for the repository owner's account passed through a terminal transcript
during the authorized publication of this repository (owner instruction: "UPLOAD THEM TO GITHUB").
The owner was advised at disclosure time to rotate the token; rotation is the owner's action outside
this record. No credential is stored in this repository.

## 8. Authorization status (unchanged)

- No frozen file was edited by this note; FREEZE.md section 5 hashes remain as recorded there.
- `rlc0-freeze` tag: never created; will not be created.
- Phase C (six-seed execution): never performed; prohibited and moot.
- No CBMC run, experiment, solver/flag/budget change, or successor project is authorized by this
  note. This is an archival integrity record appended to a closed study.

RLC-0 is complete. No follow-up is authorized.
