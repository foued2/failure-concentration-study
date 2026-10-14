# ADDENDUM - RLC-0 ARCHIVAL INTEGRITY NOTE (2026-10-14 D)

Provenance: prepared after the 2026-10-14 review cycle on ADDENDUM_2026-10-14_C (commit d9dfa8f).
GPT verified the published commit and addendum, checked the reported EOL mechanism against git's
implementation, and corrected its own earlier audit count. CLAUDE reviewed the cycle and recorded
caveats. This note is append-only: it does not amend addenda A-C, the committed manifest, the
sidecar, or any frozen file. No seed was compiled, executed, or submitted to CBMC. No CBMC run,
experiment, flag, budget, or protocol change occurred. The scientific disposition of RLC-0 is
unchanged.

## 1. GPT count correction (recorded)

GPT's follow-up audit originally reported 60 matches and 18 mismatches between the sidecar and
the published ZIP. On re-examination, GPT's mismatch list contained 19 filenames; GPT attributes
the 60/18 figure to its own tally error and records the correct result as 59 byte-identical and
19 EOL-different — the same counts MIMO's independent reconciliation obtained (ADDENDUM C
sections 3-4). The per-file proofs in ADDENDUM C section 3 are unaffected. ADDENDUM C section 4
stated that the direction of the one-file discrepancy could not be resolved from the retained
records; that statement is superseded by GPT's on-the-record self-correction above. ADDENDUM C
is not edited: pushed notes are corrected only by appending.

## 2. Scope of GPT's independent verification (recorded)

GPT independently verified: commit d9dfa8f is published and adds only
rlc0/ADDENDUM_2026-10-14_C.md; the published addendum and the recomputed manifest are retrievable
and correctly distinguish the sidecar's working-tree-byte purpose from a direct ZIP comparison;
the reported transformation is consistent with git's implementation (git archive applies
convert_to_working_tree; core.autocrlf=true yields LF-normalized blobs and CRLF working-tree
representations). GPT did not rerun the 78-file byte comparison against a Windows working tree
in its environment and does not present MIMO's local hash run as its own reproduction. That run
remains MIMO's self-reported result; it is reproducible by anyone following ADDENDUM C section 6
(clone with core.autocrlf=true and hash working-tree files against the sidecar, or compare ZIP
entries after the documented normalize-then-expand transforms). C3 remains PARTIALLY SATISFIED
on exactly the components GPT reran (commit shapes, bundle/ZIP transfer hashes, the 26 FREEZE.md
hashes under the documented byte provenance, the seed-3 witness defect from source) plus the
published-record checks listed above.

## 3. Diagnostic-hygiene note (recorded)

An intermediate MIMO diagnostic during the reconciliation compared git SHA-1 object ids against
SHA-256 content hashes and produced a spurious anomaly. It was detected, corrected by byte-level
blob dumps, and excluded from the published record; every number in ADDENDUM C comes from the
corrected scripts, which print explicit parse, total, match, and mismatch counts. Carried
forward lesson, consistent with ADDENDUM B section 4: a verification that asserts only "0
mismatches" without printing counts can be vacuous; count-printing is mandatory for any future
verification of this record.

## 4. Caveats carried forward (CLAUDE review, recorded)

- The sidecar records working-tree bytes under the documented autocrlf=true convention
  (ADDENDUM C section 6). A checkout on a host that produces LF working-tree bytes yields a
  different hash set; cross-representation comparison requires the documented normalization
  model.
- C3 is independently verified only for the components actually rerun by GPT (section 2). One
  optional further step was noted and not performed, and is not required for closure: a third
  party (or GPT, with a clone) running the sidecar check once on a CRLF checkout.
- Pushed addenda and frozen files are not amended; corrections are append-only (this note).

## 5. Status and outstanding operational item

- Disposition unchanged: full-domain certification was not demonstrated; no seed verdicts
  exist; C2 remains NOT SATISFIED (canary FAIL never observed within the frozen budget); the
  seed-3 witness defect remains recorded and uncorrected; the committed nameless manifest
  remains defective as a name-to-hash record (its hash multiset matches; ADDENDUM B).
- The GitHub OAuth credential exposed during the authorized publication (ADDENDUM B section 7)
  remains unrotated as of this note. Rotation is the owner's action at
  https://github.com/settings/tokens; this is the highest-priority open operational item and the
  new credential must not be pasted into any transcript.
- Closing line, restated per review guidance in place of the formula used in earlier notes:
  RLC-0 is closed with the limitations recorded in addenda B, C, and D. The one outstanding
  follow-up is the owner's token rotation.
