# LC518 state-package verification log

Configuration freeze date: 2026-11-02 (UTC)
Source of generator bytes: `lc518_generator_scratch_GLM_review_v1.2.zip` (SHA-256 `4a7302072fcdda922cad3e9658056af5209e68ed82e26f6420e52e35dc1036f9`, on repository `master`), whose internal `SHA256SUMS` verified 9/9 OK before any file was used.
No bank, run root, staging directory or oracle output exists. State 2 was never executed.

## Deliverables (this package)

| File | SHA-256 |
|---|---|
| `lc518_generator_state1.py` | `276b9f49f5a3a975c530cc4eca02b0a0f3407ab824d12031f43175a72feb14fe` |
| `lc518_generator_state2.py` | `1335a42d06d64cf7e847981fc68eee07945655128e82e7f08bc43e774d1cb41c` |
| `activation_diff.txt` | `578d17163701d549d17c19e5e1a785709fd1d08bf3572b77ac7058fbc13c8a64` |
| `execution_protocol_v1.md` | `64e7f5033eac5dec3d7278bd48695ffe42b19fc047bd79f14145c49f3a45e293` |

The `execution_protocol_v1.md` digest above is the external protocol SHA-256 that the launcher's `PROTOCOL_SHA256` must pin and that the owner GO must name. It is not contained in the protocol file itself.

## Chain

- Review build `lc518_generator.py` = `6e4281b4bfd79783b53d93e132a538dc3d120177405e44012081c6db083c0e2f` (ZIP pin, re-verified).
- state0 -> state1: exactly one literal changed, `OUTPUT_DIR: str | None = None` -> `OUTPUT_DIR: str | None = "/home/z/lc518_run/bank"`; diff verified programmatically (2 changed diff lines, 1 semantic line).
- state1 -> state2: exactly one literal changed, `BANK_GENERATION_AUTHORIZED = False` -> `True`; packaged `activation_diff.txt` equals `diff -u` of the packaged states byte-for-byte.
- Both states compile under the pinned interpreter (`py_compile`, CPython 3.13.5).

## Verification performed on 2026-11-02 (UTC)

1. ZIP extraction and 9/9 internal checksum verification (recovery introspection run).
2. Artificial acceptance suite rerun under `/usr/bin/python3.13`: **51/51 passed** (`RECOVERY_TEST_RERUN.txt`, 51 `ok` lines, exit 0).
3. Captured target fingerprint: executable `/usr/bin/python3.13`; `sys.version` = `3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]`; `platform.platform()` = `Linux-5.10.134-013.15.kangaroo.al8.x86_64-x86_64-with-glibc2.41`; interpreter binary SHA-256 = `889c603f0d17cb54060951bcf4c4f9b8c9ebd9e52b392c70209bbb9755d797d9`.
4. state1 entry-point refusal check: exit status 1, `REFUSED: separate owner authorization for study-bank generation is absent.`; `/home/z/lc518_run` was not created.
5. state2: bytes hashed only; never executed.

## Open owner actions

1. Ratify `RUN_ROOT = /home/z/lc518_run` (or supply a different absolute path; this regenerates the chain before any GO).
2. Publish the four deliverables and record the protocol digest.
3. Issue the separate bank-generation GO naming the protocol SHA-256 and the activation diff; that GO also enables the launcher authorization literal and applies the §12 launcher pin values.

---

## 2026-11-05 append-only supersession record (added by Qoder CLI review; no prior line modified)

The 2026-11-02 statement above — "No bank, run root, staging directory or oracle output exists. State 2 was never executed." — was true when recorded (pre-GO state-package configuration) and is preserved unmodified. It was superseded by the following later, separately authorized event:

- 2026-11-03: Owner GO `LC518-GO-2026-11-03-01` authorized C9 bank generation only; it authorized nothing further and remains consumed by the run below.
- GitHub Actions run `41591572358` (head commit `a4ec114`, recovery branch `gpt/lc518-github-recovery-2026-11-02`) completed successfully; recorded final bank status `ACCEPTED`.
- Owner GO identity: GO-record file `lc518-150/provenance/OWNER_GO_RECORD.md`, SHA-256 `5c4cd6eb81d99cbb67217999a46a7af6aee1ff5f368250f601e7759521ae54c1` (stored at `lc518-containment/recovery-2026-11-02`).
- C9 source digest: `f291ae879ef6e046c6715bb0e6a84cd5a3f5e69f07ace09e213db9b84d8b87fe` — SHA-256 of the ratified C9 text `lc518-150/review-v1.2/analysis-revision-2026-11-02/C9_GENERATION_SPEC_REVIEW.md` rev 2.6 at commit `511bc20` (49,769 bytes), labelled "C9 source SHA-256" in `execution_protocol_v1.md` §1. It is neither the execution-protocol-v2 digest nor a Git object ID.
- Execution protocol v2: `execution_protocol_github_v2.json`, content SHA-256 `9c54ffc2143eef807dad51ee5ba92e494e4588fa4655bd5772f613cec2f343a9` (named in OWNER_GO_RECORD.md and `LC518_GENERATION_HOLD.md`; recorded as a member hash in the bank-artifact `SHA256SUMS`).
- Original GitHub Actions artifact: ID `13210063805` (75,523 bytes), SHA-256 `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`. Externally verified (GPT remote verification, 2026-11-05), **not locally reproduced**: anonymous artifact download returns 401, and the digest is recorded nowhere in repository content.
- Later sanitized redistribution archive: `lc518-bank-artifact-run-41591572358.zip`, SHA-256 `71f1e76b03161d91a443a891ce0a1821b2bdd7ff70cc97115c6c1a0448bc2df1`, stored at `lc518-containment/foued2-patch-1`. It is a containment repack (2026-11-03) of the run's publication set `lc518-publish-set-12-files-run-41591572358.zip` (SHA-256 `16ce5a6a…`, git blob `301e8e16…` at commit `e22da84`) that removed exactly the two neutral-name executable members; every retained member is byte-identical. It is NOT byte-identical to the original Actions artifact.
- Consequence: banks, oracle outputs and run artifacts now exist and are publicly stored, and the state-2 generator bytes were executed in that run. Any later reading of the 2026-11-02 statement as describing the current state is incorrect. See `REPOSITORY_STORAGE_INVENTORY_2026-11-05.md` §2 (exposure register) and claim-matrix rows L02, L09, L27, L28.
- Record provenance: this appended record lives at repository path `VERIFICATION_LOG.md` (repository root, working tree of local branch `research/concentration-math-spec`). The unmodified original (lines 1–37) is byte-identical to blob `a851183eac186911ff3dbbf0a1a9a807fc6e34f3`, the sole committed version of this file (first committed at `552004e`; present at `origin/master` tip `b3e9874`). To avoid self-reference, the SHA-256 of this working-tree file as appended is recorded externally in `REPOSITORY_STORAGE_INVENTORY_2026-11-05.md` §6.

---

## 2026-11-05 addendum 2 (append-only; original Actions artifact retrieved and verified; no prior line modified)

Addendum 1 above recorded the original artifact digest as "**not locally reproduced**". That
characterization is superseded by the authenticated retrieval recorded below; the prior text
is preserved unmodified per the append-only rule.

**Retrieval and verification (2026-11-05).** Artifact `13210063805` (75,523 bytes) was
retrieved through the authenticated GitHub connection; the anonymous download endpoint still
returns 401. The working copy `~/Downloads/lc518-bank-run-41591572358-1.zip` was
independently re-verified in this audit session:

- Archive SHA-256 recomputed: `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` — matches GitHub's recorded artifact digest.
- 15 members: the six bank artifacts plus `bank/canonical_disjointness_report.json`, `execution_protocol_github_v2.json`, `lc518_generator.py`, `lc518_launcher.py`, `logs/run_manifest.json`, `logs/stderr.log`, `logs/stdout.log`, `test_lc518_generator.py`, `test_lc518_launcher.py`.
- All 15 member hashes were independently recomputed and match the manifest's recorded values, including the six bank files, the disjointness report (`839014e0…`), the protocol (`9c54ffc2…`), the generator (`848984ca…`) and the launcher (`014e45c2…`).
- GPT independently retrieved the same artifact and recomputed the archive and member hashes with the same results (2026-11-05).

**Run manifest (`logs/run_manifest.json`, SHA-256 `698f4e99…`).** Records: executed
generator path `…/lc518_run/lc518_generator.py`; `generator_sha256` `848984ca…`, identical
before and after the run (`published_generator_sha256_after_run`); `launcher_sha256`
`014e45c2…`; `launcher_argv` `["lc518_launcher_state2.py"]`; `process_exit_status` 0;
`overall_acceptance_status` ACCEPTED; `item8_status` PASS; `c9_commit` `511bc20`;
`c9_source_sha256` `f291ae87…`; `protocol_sha256` `9c54ffc2…`; seeds diagnostic `11052026` /
heldout `20261101`; interpreter CPython 3.13.5 with `sys.executable` binary SHA-256
`9cf89c50…` equal to the protocol's interpreter pin; `rejection_event_count` 63;
`test_suite_pass_count` 57 (the run's 43 generator + 14 launcher tests, per the protocol's
test-suite block). `logs/stdout.log` is empty (SHA-256 `e3b0c442…`, the empty-file digest);
`logs/stderr.log` is non-empty (`76a92c24…`).

**Launcher-hash precision.** The manifest's `launcher_sha256` is the hash of the executed
launcher entry point's own bytes: the launcher resolves its own source path
(`lc518_launcher.py:326`), hashes that file (`:391`), copies those exact bytes to the
published path (`:451`), and overall acceptance requires the published after-run hash to
equal that hash (`:370`). Verified in the executed launcher bytes (`014e45c2…`).

**Consequence.** The exact generator bytes executed by run `41591572358` are established by
the run's own manifest plus independent member-hash recomputation. Generator-execution
provenance is VERIFIED; it must no longer be carried as unresolved. Matrix rows L34 and L35
and the L09/L11 evidence columns are updated accordingly.

**New open discrepancy: runner-image identity (matrix L10, DISCREPANCY_OPEN).** The protocol
pins runner image `ubuntu24` / `20261026.354.1` (`execution_protocol_github_v2.json` runner
block), and the executed launcher enforces exact string equality on `ImageOS`/`ImageVersion`
with hard refusal before RUN_ROOT creation (`lc518_launcher.py:27-28, :319`). Job
`125769272315` succeeded and the manifest records exit 0, so the `ImageVersion` environment
variable at run time must have equaled `20261026.354.1`. GPT's read of the job setup log
(2026-11-05) reports `Runner Image Version: 20261025.353.1`, which conflicts with the pin.
The job log requires admin authentication and could not be retrieved in this audit; and no
release tag `ubuntu24/20261025.353` exists in `actions/runner-images` as of 2026-11-05
(direct tag lookup returns 404; the only ubuntu24 releases in that window are
`20261026.354` and `20261101.360`). Both observations are recorded; the relationship between
the two identifiers is unresolved and requires the authenticated job log. `ubuntu-24.04` is
the workflow's `runs-on` label, not an immutable image selection.

**Ref-census correction.** The §1 classification table in
`REPOSITORY_STORAGE_INVENTORY_2026-11-05.md` summed to 80 memberships against 81 refs. The
exact 81-row census (inventory Appendix A, Rev 3) identifies the unaccounted ref as
`refs/tags/v0.2-freeze` (`798b446`; tree: gates, generation, pilot, scripts, specs, study,
v02 — no v03p, no rlc0, no engineered-study). The H3 row's count of 28 already included the
tag `h3-footprint-freeze-2026-10-26` even though its representative text named only the
v2–v8 tags.

**File status.** This file is an untracked working-tree file on local branch
`research/concentration-math-spec`; it is not committed on any ref as of 2026-11-05. The
sole committed version remains blob `a851183e…` (first committed at `552004e`, present at
`origin/master` tip `b3e9874`). The SHA-256 and line count of this working-tree file after
addendum 2 are recorded externally in `REPOSITORY_STORAGE_INVENTORY_2026-11-05.md` §6 (no
self-reference).
