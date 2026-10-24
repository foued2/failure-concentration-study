# Independent W1 Verification — Report Amendment B

Field: independent verification (GLM)
Date: 2026-10-24
Supersedes one table entry in: `INDEPENDENT_W1_VERIFICATION_REPORT_AMENDMENT_A_2026-10-24.md` (Amendment A is preserved byte-unchanged as committed in `d2c4d7c`)
Trigger: field-lead audit (GPT) identified an arithmetic error in the post-push addendum of Amendment A. No numerical result, no run, no source, and no other artifact is affected.

## Correction — CR counts in the line-ending-normalization table

Amendment A's addendum table gave the byte-count note for both JSON artifacts as
"exact (502,577 bytes incl. 14,533 CR → 488,044 LF)" for `independent_w1_run.json`
and "exact (same CR count)" for `independent_w1_run.attach.json`. The parenthetical
"same CR count" wrongly implied that the attachment also shed 14,533 CR bytes. The
recorded sizes contradict that: the attachment changed by 393 bytes
(19,864 local → 19,471 committed), not 14,533.

Corrected addendum, with per-file counts re-verified locally (both files contain one
CR and one LF per line, so CR count = LF count = number of text lines; all other
artifacts stored byte-identically):

| Artifact | Local working-copy bytes | CR bytes removed on commit | LF-normalized bytes | LF-normalized SHA-256 (= committed blob hash) |
|---|---|---|---|---|
| `independent_w1_run.json` | 502,577 | 14,533 | 488,044 | `156b0cdeca37650cfd052300d7867be50ff59e83c905f80142adf1447688bfde` |
| `independent_w1_run.attach.json` | 19,864 | 393 | 19,471 | `f3187295a56ec9502c70689e82a402a9a855d820f3cbd1ddfdc9a0738c8d6510` |

Both LF-normalized hashes equal the committed blob hashes recorded in Amendment A
and independently re-verified by the field lead against commit `d2c4d7c`, confirming
that CRLF→LF normalization is the sole content transformation for both files and
that the two hash variants describe the same logical content.

## Invariants

Unchanged by this amendment: the independent source (blob hash identical,
`4454ae9f5bca940f3c8253273d1bf198a70bfe4270b553464401855403542aae`), `source_sha256.txt`,
the original report, the run record, every recorded value, and the disposition.

## Disposition

Unchanged, per field-lead audit: the independent W1 verification is reproducible from
the committed record; no result-changing implementation defect found; **W1 wiring check
FAILED** (primary intervals include zero; gain ~0.058%/0.057% of baseline loss;
alternate partition reverses the mean direction; represented-k subset does not rescue
the result). Review status remains **reviewed, corrections pending** until this
normalization-table error is closed and the earlier documentation gaps are closed.
No additional simulation, tuning, source change, or rerun is warranted.
