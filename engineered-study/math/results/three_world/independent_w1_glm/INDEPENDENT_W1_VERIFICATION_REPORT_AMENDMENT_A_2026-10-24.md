# Independent W1 Verification — Report Amendment A

Field: independent verification (GLM)
Date: 2026-10-24
Supersedes wording in: `INDEPENDENT_W1_VERIFICATION_REPORT.md` (that file is preserved byte-unchanged; SHA-256 `2cd543f662007e7b367b112f442304fa2aa263b7bfe764b9d1936a0adf775b24`)
Trigger: field-lead audit (GPT) identified three wording errors that do not alter any numerical result, any run, or any artifact produced by the verification, but must be corrected before the record is treated as finished.

**Invariants:** The independent source, its hash record, the run, `independent_w1_run.json`, all comparison values, and the disposition (W1 remains FAILED) are unchanged by this amendment. Corrections are text-only, in this separately versioned document.

## Correction 1 — W1 expectation stated backwards

Original report, §1, said:

> The declared W1 wiring check — fitted M1+fam should NOT improve held-out prediction over M0+fam —

This reverses the frozen design. The frozen design states the opposite expectation: "W1 wiring check: expected direction is positive under the declared W1 mechanism. If it fails, mark the simulation check FAILED and investigate code/model mismatch." (`10_THREE_WORLD_SIM_DESIGN.md`, criterion §; consistent with lines 17, 64, 164, 179: "A positive W1 result is expected because the world is constructed to make concentration informative.")

Corrected wording (replaces the quoted sentence):

> The frozen W1 wiring check expected M1+fam to improve held-out prediction over M0+fam. This criterion failed: both primary central 95% simulation-trial intervals include zero, and the alternate diagnostic partition has a negative mean gain.

The numerical outcome is unaffected: primary Δ_pred (domain) mean 1.961346752e-06, equal 1.914362824e-06; wiring check FAILED as recorded. The failure mode is that the frozen interval criterion was not met and the alternate partition reversed the mean direction — not an expectation mismatch of the kind implied by the original sentence.

## Correction 2 — Both primary intervals include zero

Original report, §8, item 2, said:

> Central 95% intervals exclude zero but begin within ∼1.2–1.9e-6 of it

This is wrong. Both primary central 95% simulation-trial intervals include zero:

| Score | Mean gain | Central 95% simulation-trial interval |
|---|---|---|
| Domain-weighted | 1.9613e-06 | [-1.2421e-06, 7.5813e-06] |
| Equal-family | 1.9144e-06 | [-1.8333e-06, 8.9887e-06] |

Corrected wording (replaces the quoted clause):

> ...central 95% intervals include zero, with negative lower bounds of approximately 1.24e-06 (domain) and 1.83e-06 (equal).

The positive-trial fractions (0.804 domain, 0.754 equal; 402/500 and 377/500 trials) are descriptive frequencies. They do not satisfy or substitute for the frozen interval criterion, which the original report's phrasing endangered. Relative effect size, for scale only: mean Δ is about 0.058% (domain) and 0.057% (equal) of the M0+fam baseline loss (0.003387840 / 0.003350860, recorded in `independent_w1_run.json`). The alternate diagnostic partition remains mean-negative (−6.2470e-07 domain, −6.7787e-07 equal), and the represented-k subset does not rescue the result — all as previously computed and unchanged.

## Correction 3 — "Byte for byte" claim is stronger than what was done

Original report, §5, said:

> ...is bit-identical to the original archive, byte for byte in JSON serialization.

Not accurate. Verification A compared JSON-parsed field values, not serialized line bytes: each regenerated case was parsed and compared field by field (17 fields: trial, case, fold, setting, world, F, E, F_alt, k, C, C_alt, carrier, home_counts, defects, S_domain, S_equal, diag_bits) against the parsed saved record (`compare_case`, lines 144–184 of the frozen source). Integer and structural fields required exact equality; float fields additionally tolerated 1e-12 relative agreement — a tolerance that was never used (near-miss count 0). Records with any mismatched field: 0; trailing records after expected count: 0.

Corrected wording (replaces the quoted sentence):

> Every field of every W1 record matched exactly after JSON parsing, with zero mismatches and zero near-misses across the 2,500,000 records.

No byte-level serialization comparison was performed, and none is claimed. (Note: exact float equality held anyway for all four float fields — C, C_alt, S_domain, S_equal — because both sender and verifier compute them deterministically from identical integer outcomes; the tolerance was a safeguard only.)

## Provenance chain re-confirmation

| Artifact | SHA-256 | Status |
|---|---|---|
| Run-producing source `independent_w1_verify.py` (51,927 bytes) | `4454ae9f5bca940f3c8253273d1bf198a70bfe4270b553464401855403542aae` | unchanged since the run; re-verified |
| Freeze record `source_sha256.txt` | `06cf1ef8dbce30a208bce0d394eebbf6817c4ce8bd7cb4f34f4ecf55ce67dfb8` | unchanged |
| Run record `independent_w1_run.json` (502,577 bytes) | `1152b9ad187135da1658c363702d5c77f55bd1ed2a213c7d8293c47c63b6f80e` | unchanged |
| Console log `run_500_console.log` | (retained as run evidence) | unchanged |
| Original report `INDEPENDENT_W1_VERIFICATION_REPORT.md` | `2cd543f662007e7b367b112f442304fa2aa263b7bfe764b9d1936a0adf775b24` | preserved byte-unchanged; wording superseded by this amendment |

## Addendum (post-push, 2026-10-24): line-ending normalization of committed hashes

The hashes in the table above refer to **local working-copy bytes** (as recorded before first execution and at run time). On commit, git normalized CRLF → LF for the two JSON artifacts written through Python text-mode I/O on Windows; all other artifacts (including the run-producing source, whose local bytes are LF) stored byte-identically. Verified against the pushed commit `e7a9a16`:

| Artifact | Local working-copy hash (CRLF) | Committed blob hash (LF) | LF-normalized correspondence |
|---|---|---|---|
| `independent_w1_run.json` | `1152b9ad187135da1658c363702d5c77f55bd1ed2a213c7d8293c47c63b6f80e` | `156b0cdeca37650cfd052300d7867be50ff59e83c905f80142adf1447688bfde` | exact (502,577 bytes incl. 14,533 CR → 488,044 LF) |
| `independent_w1_run.attach.json` | `0ce6afbe09f4074327e59861c805abdc5327946609e8b9cc15d491b3956d62d6` | `f3187295a56ec9502c70689e82a402a9a855d820f3cbd1ddfdc9a0738c8d6510` | exact (same CR count) |
| `independent_w1_verify.py` | `4454ae9f5bca940f3c8253273d1bf198a70bfe4270b553464401855403542aae` | identical hash in blob | byte-identical |
| `source_sha256.txt`, `INDEPENDENT_W1_VERIFICATION_REPORT.md`, `run_500_console.log` | as above | identical hash in blob | byte-identical |

Both JSON blob hashes equal the SHA-256 of the local file with CR bytes removed, confirming the two hash variants describe the same content. Analysis results recorded in the JSON are unaffected. This mirrors the convention already in use for the frozen design record ("SHA-256 (UTF-8 bytes returned by GitHub for the committed file)").

## Record (post-push)

Commit `e7a9a16` "Record independent W1 verification run and report" pushed to `origin/research/concentration-math-spec` (parent `780daa5`) with exactly the seven artifacts of this directory. All original/local-only records (`per_trial.json`, `raw/`) remain untracked by design.

Review status remains: reviewed, corrections pending. Disposition unchanged: W1 wiring check FAILED, independently confirmed reproducible; no implementation defect; no further simulation, tuning, or commit; no parameters, seeds, or criteria changed.
