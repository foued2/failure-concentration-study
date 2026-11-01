# GPT v1.2.2 held-out-first collision-policy review manifest

**Branch:** `gpt/lc518-150-v1.2.2-heldout-first-claude-fixes-2026-11-01`  
**Parent review branch:** `gpt/lc518-150-v1.2.2-heldout-first-2026-11-01`  
**Direct parent commit:** `d7267b4596ab7909a82838ec1f5e3fdc2b94432f`  
**Purpose:** respond to Claude's independent review of the held-out-first collision policy by disclosing its diagnostic-support exclusions, requiring realized per-stratum collision counts, and clarifying fixed-record exclusion proofs. Review-only. No bank generation or solver work.

**Status:** proposed specification revision, not yet accepted by Claude or authorized for generator execution. The owner's design choice is recorded separately from execution authorization.

## Files covered by this follow-up review

| Path | Git blob SHA |
|---|---|
| `lc518-150/review-v1.2/CORRECTIONS_RECORD_v1.2.2-draft.md` | `46a9ae6314db17c55af3a2befb58541920d5d529` |
| `lc518-150/review-v1.2/GPT_REVIEW_C9_DRYRUN_AND_v1.2.2.md` | `34605e2f404d357e2a69511338da802585663027` |

The GPT independent-review note below is preserved unchanged from the parent branch. It documents the original v1.2.2 review and is not a substitute for review of the follow-up text.

## Source artifacts preserved unchanged

| Path | Git blob SHA |
|---|---|
| `lc518-150/review-v1.2/CORRECTIONS_RECORD_v1.2.1-draft.md` | `559c14c20f3fab554623712176382e2b856f2764` |
| `lc518-150/review-v1.2/c9-dryrun/REPORT_C9_DRYRUN.md` | `e7228c89e4b9fd7f7aa4ac9fa11e140fdd5b9711` |
| `lc518-150/review-v1.2/c9-dryrun/generator_c9_dryrun.py` | `34e391ada87c39b00457adcc375cced9e1ded12a` |

## Follow-up changes

- All fixed canonical identities are checked before either PRNG stream is consumed; D5 random records remain protected from self-collision.
- The held-out bank is generated first. Its complete canonical set is frozen before diagnostic generation. Diagnostic random candidates and reorder pairs matching that set are rejected as whole candidates with `CROSS_BANK_COLLISION`; the held-out stream is never consumed or rewound by diagnostic retries.
- A held-out candidate matching a D5 fixed identity is treated as a fatal contradiction of the preflight proof, not silently retried. The D5 fixed examples are explicitly checked against every held-out stratum's admissible domain.
- The two PRNG streams remain separate, but the accepted diagnostic bank is conditional on the held-out bank. The specification expressly forbids describing the accepted banks as statistically independent samples.
- Exact replacement text for `BANK_DESIGN.md` §7 item 2 is supplied in item 3c; the frozen v1.0 source file is not modified by this review branch.
- Oracle-output attachment names, row schema, file hashes, bank-record hash references, canonical-disjointness report schema and atomic PASS publication rules are retained.
- The repository-authority paragraph is absent; permissions remain governed by separate owner direction.

## Scope

No bank files are included. No solver bodies, candidate execution, private mutation annex, or mutation assignments are included. C8/E3 remains open. The follow-up branch does not alter `master`, the v1.2.1 file, prior review branches, or any frozen v1.0 design document. The read-only master check recorded in the correction document found `master` at `b01b160` with `lc518-150/review-v1.2/c9-dryrun/REPORT_C9_DRYRUN.md` still present.


**Hash notation:** The 40-character identifiers in this manifest are Git blob SHA-1 object IDs. They are not SHA-256 digests of the file bytes. Where the specification requires file-level SHA-256, it explicitly uses 64-character lowercase hexadecimal digests.

## Review lineage

The prior held-out-first review branch was created at base/comparison commit `4169f9b2f6ace5b5a2a7a6d330558d88db8080d1`; its commit ancestry is `4169f9b2` → `ac6a9290` → `c49241c3` → `d7267b45`. The current branch starts at `d7267b45` and adds the Claude-requested support/count/proof amendments. In particular, `c49241c3` is the direct parent of `d7267b45`; `4169f9b2` is the comparison base, not the immediate parent. No rebase occurred.

## Additional review changes

- A D1–D8 by H1–H8 structural support-overlap map records the possible canonical-key intersections for each diagnostic stratum.
- The accepted diagnostic support is explicitly described as conditioned on avoiding the realized held-out set. Raw candidate rules and quotas are unchanged; accepted support is narrowed.
- The final disjointness report now carries exact CROSS_BANK_COLLISION counts for D1–D8 and H1–H8, including zeros, reconciled against sidecar rows.
- The fixed D5 exemplar exclusion proof explicitly lists the distinct reason each held-out stratum cannot contain either exemplar.
- The worked probability for one D5/H8 fixed-key path is corrected to 1/2,184 ≈ 0.000458 per candidate attempt.