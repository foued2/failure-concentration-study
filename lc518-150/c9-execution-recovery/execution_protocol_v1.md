# LC518 C9 bank-generation execution protocol

**Revision:** v1.0 (final execution protocol; completes and supersedes draft v1.2)  
**Status:** complete execution-configuration protocol, configuration-frozen 2026-11-02 (UTC). This is not a bank-generation GO and authorizes no generation. A separate owner GO naming this file's external SHA-256 and the activation diff in §13 is required before bank generation.  
**Design of record:** C9 revision 2.6 at `511bc2099ecff74b4f850b169ceef7f853c334a0`  
**C9 source SHA-256:** `f291ae879ef6e046c6715bb0e6a84cd5a3f5e69f07ace09e213db9b84d8b87fe`

This protocol does not amend the frozen C9 text. It defines execution controls delegated by C9 items 6–8. Every field that was `PENDING` in draft v1.2 is now resolved from the designated target execution environment and recorded below. The bank-generation GO remains a separate owner act.

## 1. Authority and source identity

The owner ratified and froze the exact C9 text at commit `511bc2099ecff74b4f850b169ceef7f853c334a0` on 2026-11-02. Its source SHA-256 is the value above. The source's historical status wording predates ratification and remains byte-unchanged; this protocol records the later owner act.

The protocol file has been hashed after every pending field was filled and the file reached its final form. To avoid self-reference, the protocol file does not contain its own digest. The resulting digest is recorded beside this file (package `SHA256SUMS` and verification log), pinned in the launcher constant `PROTOCOL_SHA256`, recorded in the run manifest, and named by the separate owner GO.

## 2. Interpreter pin

**Pinned version triple:** CPython `3.13.5`. This is a convention, not a correctness claim.

The target machine's exact identity, captured on 2026-11-02 (UTC) in the designated execution sandbox, is:

- Absolute `sys.executable` path: `/usr/bin/python3.13`
- Complete `sys.version` string: `3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]`
- `platform.platform()` string: `Linux-5.10.134-013.15.kangaroo.al8.x86_64-x86_64-with-glibc2.41`
- SHA-256 of the interpreter binary at that absolute path: `889c603f0d17cb54060951bcf4c4f9b8c9ebd9e52b392c70209bbb9755d797d9`

The production generator contains the hardcoded version-triple constant `EXPECTED_PYTHON_VERSION = (3, 13, 5)` and refuses another triple. The launcher is the authority for the fuller machine-specific identity: it must verify the exact absolute executable, full `sys.version`, platform string, and interpreter-binary SHA-256 before starting the generator, and must invoke that exact binary by absolute path. Any drift in these four values at run time is a stop condition. The launcher does not set or read a generator-side `EXECUTION_PROTOCOL_PYTHON` environment variable. This resolves GLM finding M-2.

The revised artificial acceptance suite was rerun under this exact interpreter on 2026-11-02 (UTC) during recovery verification: 51 tests passed. The earlier Claude/GLM rerun under Python 3.12.3 applied to the prior generator build, not this revised build.

The generator accepts no command-line arguments, reads no environment variables, and reads no configuration files. `EXECUTION_PROTOCOL_PYTHON` is not an environment variable and is not used by the generator. `PYTHONHASHSEED=0` is set by the launcher for the child interpreter before it starts; the generator does not read that variable.

## 3. Output location and run root

The target run root is an absolute path outside the repository. It is unique for this run, and its parent directory exists.

- Absolute `RUN_ROOT`: `/home/z/lc518_run` — proposed by the recovery configuration on 2026-11-02 (UTC); it becomes effective only when the separate owner GO ratifies it. Changing it before the GO produces a new protocol revision, a regenerated two-state hash chain, and a new protocol digest.
- Fixed `OUTPUT_DIR`: exactly `/home/z/lc518_run/bank`, hardcoded as the generator's `OUTPUT_DIR` constant in both configured states (§13).
- Staging directory: exactly `/home/z/lc518_run/bank.staging`.
- Logs directory: exactly `/home/z/lc518_run/logs`.

The final output directory and its sibling staging directory must both be absent at preflight. The launcher refuses an existing run root, log files, final output directory, or staging directory rather than reusing or overwriting them. A rerun therefore requires a new protocol revision and a new absolute run root/output path; seeds, ranges, examples and retry caps do not change.

## 4. Generator publication before generation

C9 item 6 requires the byte-identical, hash-pinned generator script to be published beside the bank files before generation. Because C9 item 8 requires `OUTPUT_DIR` and its staging sibling to be absent at preflight and creates `OUTPUT_DIR` only by final atomic rename, the generator is published in the run-root directory, as a sibling of the output package:

`/home/z/lc518_run/lc518_generator.py`

The launcher copies the exact reviewed generator bytes there before invoking it, verifies the copied SHA-256 against the protocol pin, runs that published copy, and verifies the published copy's SHA-256 again after the process exits. It does not place the script inside `OUTPUT_DIR` or add it to item 8's six-file `artifacts` array. The launcher itself, both acceptance-test files, and the exact protocol JSON are also copied beside the output directory for audit. Their hashes are written to the run manifest; the launcher hash is measured from the exact launcher file and recorded in that manifest.

The locked, unconfigured review-build generator SHA-256 `6e4281b4bfd79783b53d93e132a538dc3d120177405e44012081c6db083c0e2f` remains a development reference only. For the authorized run the launcher must pin the authorized state-2 generator hash from §13 in `EXPECTED_GENERATOR_SHA256`, superseding the review-build value.

## 5. Logs and streamed audit events

Before generator setup or publication starts, the launcher creates `/home/z/lc518_run/logs/` and creates these files exclusively. It then opens the existing empty files in append mode for the child process, so a setup failure before generator invocation still leaves hashable capture files:

- `stdout.log`
- `stderr.log`
- `run_manifest.json`

The generator is invoked with `-u`; stdout and stderr are captured from process start. The launcher sets `PYTHONHASHSEED=0` in the child process environment and records that value. The generator itself does not read environment variables.

The generator writes machine-parseable JSON lines to stderr, with `flush=True` for every line:

- `PREDICATE_LOG {json}` for accepted H1–H4 records, as specified in §6.
- `REJECTION_EVENT {json}` for every rejected whole-record or whole-pair candidate, using exactly the five sidecar fields and one of C9 item 5's closed reason codes.
- `PAIR_VALIDATION {json}` once serialized D6/H6 validation has passed and before the item 8 package step.

The two JSONL sidecars remain the authoritative successful/FAIL package record of candidate rejections. For an item 8 PASS or FAIL package, the launcher requires the streamed rejection events to match the sidecar rows exactly, grouped by bank and preserving event order. On an abort before item 8, streamed events remain in `stderr.log`; any orphan staging directory is preserved, not cleaned up.

A fatal held-out candidate collision with a fixed D5 key is emitted as `REJECTION_EVENT` with reason `CROSS_BANK_COLLISION` immediately before the generator aborts. It is not retried and does not reach item 8. No non-C9 identifier such as `FatalCrossBankContradiction` is used as a reason code.

## 6. Repeated-use predicate accounting

C9 item 3b requires the repeated-use predicate result for every H1–H4 record. The exact predicate is `oracle_answer > N0`, with `N0` the 0/1 subset count.

For each H1–H4 record, the generator emits exactly one `PREDICATE_LOG` line immediately after that record has passed acceptance and has been appended to the in-memory held-out bank. It emits no predicate line for a rejected candidate. The line contains exactly:

`input_id`, `stratum`, `amount`, `coins` (as-given order), `oracle_answer`, `N0`, and `repeated_use_predicate`.

A completed generation must produce exactly 40 lines, with unique IDs and these stratum counts: H1 = 12, H2 = 12, H3 = 8, H4 = 8. The launcher validates the exact ID ranges and count by stratum. For an item 8 PASS package it also cross-checks every `(input_id, stratum, amount, coins)` tuple against `heldout_bank.json` and each `oracle_answer` against `heldout_oracle_outputs.json`.

If generation aborts before completion, the partial number of observed predicate lines and partial per-stratum counts are recorded in the manifest. The exact-40 requirement applies to a completed generation; a partial log never makes an aborted run acceptable. An item 8 FAIL is still a completed generation, so its predicate accounting must also contain exactly 40 lines, even though no bank/oracle-output attachments are published.

## 7. D6/H6 pair metadata and validation

The serialized C9 schema stores `pair_id` and `ordering` only inside `rule_params`. They are not separate top-level record fields. The record object contains exactly the C9 record-hash payload fields plus `record_sha256`; the record-hash payload itself remains exactly the fields listed in C9 item 5. `rule_params` is hashed, so the pair metadata in it is covered by `record_sha256`.

The validator runs on the serialized in-memory records before record hashes and item 8, and again after hashes are attached. It rejects undeclared top-level pair fields and requires:

- D6 pair IDs in order D6-P01 through D6-P04; H6 pair IDs in order H6-P01 and H6-P02.
- Both members adjacent, original first and permutation second.
- Exactly one shared `rule_params.pair_id`; `rule_params.ordering` exactly `original` and `permutation` respectively.
- Consecutive input ID ordinals.
- Equal amounts and equal sorted denomination sets, but different as-given coin arrays.
- Shared top-level `canonical_id` and identical `int32_guard` objects.
- No extra top-level pair fields and no undeclared keys in either pair's `rule_params` object.

The top-level `pair_id`/`ordering` comparison proposed in Claude draft v1 is withdrawn: those top-level fields are not in the frozen serialized schema. Direct source inspection of this generator build confirms they are not serialized. The revised artificial tests validate the actual C9 schema and deliberately corrupt each pair property to confirm rejection. GLM finding M-1 is therefore resolved in both the validator and the protocol text.

## 8. Run manifest

`run_manifest.json` is written before generator invocation and updated after the process exits. It records at least:

- Protocol SHA-256; C9 commit and source SHA-256.
- Generator SHA-256 and published path; launcher SHA-256 and published path; full launcher argv and generator argv.
- Both seed literals.
- Both test-suite source SHA-256 values and the passing test count.
- Exact interpreter record: `sys.version`, `platform.platform()`, `sys.executable`, and interpreter binary SHA-256.
- `PYTHONHASHSEED=0`, absolute run root and output directory, start/end times, process exit status.
- stdout and stderr SHA-256 values.
- Observed predicate count and per-stratum counts, including partial counts on abort.
- Streamed rejection-event count and pair-validation status.
- `item8_status` separately from overall acceptance status.
- SHA-256 of `canonical_disjointness_report.json` and every artifact present in the item 8 package.
- Post-run SHA-256 of the published generator and launcher copies.
- Hashes for files in an orphan staging directory, if one exists.

The manifest itself is not self-hashed. It is written atomically before execution and updated atomically afterward. A hard interruption may leave the initial manifest incomplete; the already-created stdout/stderr files and any staging directory are retained for forensic inspection. The protocol digest is external to the protocol file to avoid a self-referential hash.

## 9. Item 8 publication and overall acceptance

Item 8's exact PASS/FAIL behavior remains unchanged:

- **PASS:** the output directory contains the six C9 artifacts (two oracle attachments, two bank files, two rejection sidecars) plus `canonical_disjointness_report.json`. The launcher verifies the report, exact filenames, each listed artifact hash, the report hash, predicate crosswalk, pair validator, and streamed rejection/sidecar reconciliation.
- **FAIL:** a nonempty final intersection produces the two rejection sidecars and a `FAIL` report in the output directory. It produces no bank files and no oracle-output attachments. The run is **NOT_ACCEPTED**. The launcher still hashes the two sidecars and report and records their digests in the manifest.
- **Abort before item 8 final rename:** the final output directory remains absent. An orphan `.staging` directory is retained and hashed in the manifest; it is not accepted output.

The overall run status is `ACCEPTED` only if all conditions hold: process exit status 0; item 8 status PASS; exactly 40 unique predicate records with the 12/12/8/8 stratum counts; pair validation passed and the serialized package recheck passed; streamed rejection events reconcile exactly with both sidecars; all report/artifact hashes verify; the published generator hash remains the pinned value; and no stop condition or audit error occurred. Item 8 PASS alone is not sufficient.

## 10. Stop conditions and reruns

Stop and mark the run NOT_ACCEPTED on any of the following: interpreter identity mismatch; wrong generator or protocol hash; fixed-key or structural-exclusion preflight defect before RNG construction; pre-existing output/staging path; candidate-slot or whole-record/pair attempt-cap exhaustion; held-out-versus-fixed-D5 `CROSS_BANK_COLLISION`; malformed or incomplete predicate accounting on a completed generation; pair validation failure; item 8 FAIL; streamed/sidecar mismatch; report/artifact hash mismatch; missing report; or I/O/publication error.

Do not change seeds, ranges, quotas, examples or retry caps to obtain a different result. A rerun requires a new protocol revision, a new empty absolute run root/output path, recalculated pins and a separate owner GO naming that protocol SHA-256.

## 11. Authority boundary

This protocol authorizes no bank generation. It authorizes no solver construction, candidate execution, private-annex access, predictive fitting, power study, repository push, or merge to master.

As of configuration freeze on 2026-11-02 (UTC): generator state 1 (`lc518_generator_state1.py`) is configured but locked and refuses to run; state 2 (`lc518_generator_state2.py`) exists only as the pre-declared authorized-execution candidate, has never been executed, and must not be executed before the GO; the launcher remains locked (`BANK_GENERATION_AUTHORIZED = False`); the run root is proposed and pending owner ratification in the GO. A separate owner GO naming this file's external SHA-256 and the exact activation diff is required before bank generation; that same GO enables the launcher authorization literal.

## 12. Configuration record and GO pin values

- C9 source SHA-256: `f291ae879ef6e046c6715bb0e6a84cd5a3f5e69f07ace09e213db9b84d8b87fe`.
- Review-build generator (locked, unconfigured; development reference): `6e4281b4bfd79783b53d93e132a538dc3d120177405e44012081c6db083c0e2f`.
- State 1, configured-but-locked generator (`lc518_generator_state1.py`): SHA-256 `276b9f49f5a3a975c530cc4eca02b0a0f3407ab824d12031f43175a72feb14fe`. Sole change from the review build: `OUTPUT_DIR: str | None = None` → `OUTPUT_DIR: str | None = "/home/z/lc518_run/bank"`. Refuses without authorization.
- State 2, authorized execution generator (`lc518_generator_state2.py`): SHA-256 `1335a42d06d64cf7e847981fc68eee07945655128e82e7f08bc43e774d1cb41c`. Sole change from state 1: `BANK_GENERATION_AUTHORIZED = False` → `True`. Never executed during configuration.
- Activation diff: `activation_diff.txt`, SHA-256 `578d17163701d549d17c19e5e1a785709fd1d08bf3572b77ac7058fbc13c8a64`. Exactly one changed line, reproduced in §13.
- Generator acceptance suite `test_lc518_generator.py`: SHA-256 `d6a322bc9c28a9c5537f89a1bb6395bf52a44f79293c07b4f526ad985dfcdf64`; 51 passed under CPython 3.13.5 on 2026-11-02 (UTC) (recovery verification rerun).
- Launcher acceptance suite `test_lc518_launcher.py`: SHA-256 `febd27e1fd98ed9d27d6e802e50704fa278b504ba2d6555bbab81d0c091953b0`.
- Launcher SHA-256: measured by the launcher itself at run time and recorded in `run_manifest.json`.
- Target interpreter fingerprint (captured 2026-11-02 (UTC)): §2 values — executable `/usr/bin/python3.13`, `sys.version` `3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]`, platform `Linux-5.10.134-013.15.kangaroo.al8.x86_64-x86_64-with-glibc2.41`, interpreter binary SHA-256 `889c603f0d17cb54060951bcf4c4f9b8c9ebd9e52b392c70209bbb9755d797d9`.
- `RUN_ROOT` `/home/z/lc518_run` and `OUTPUT_DIR` `/home/z/lc518_run/bank`: proposed 2026-11-02 (UTC), effective on owner ratification in the GO.
- Final protocol SHA-256: external to this file; recorded in the package `SHA256SUMS` and verification log, pinned in the launcher, and named in the owner GO.
- Launcher constants to set as part of the GO configuration (mechanical, before the run): `RUN_ROOT = "/home/z/lc518_run"`; `OUTPUT_DIR = "/home/z/lc518_run/bank"`; `EXPECTED_PYTHON_EXECUTABLE = "/usr/bin/python3.13"`; `EXPECTED_SYS_VERSION = "3.13.5 (main, Aug 10 2026, 12:06:59) [GCC 14.2.0]"`; `EXPECTED_PLATFORM = "Linux-5.10.134-013.15.kangaroo.al8.x86_64-x86_64-with-glibc2.41"`; `EXPECTED_INTERPRETER_SHA256 = "889c603f0d17cb54060951bcf4c4f9b8c9ebd9e52b392c70209bbb9755d797d9"`; `PROTOCOL_SHA256 = <external digest of this file>`; `EXPECTED_GENERATOR_SHA256 = "1335a42d06d64cf7e847981fc68eee07945655128e82e7f08bc43e774d1cb41c"`.
- Bank-generation authorization: **FALSE** until the owner GO.

## 13. Generator authorization activation and final hash chain (COMPLETED)

The review-build generator source was intentionally locked: `OUTPUT_DIR = None` and `BANK_GENERATION_AUTHORIZED = False`. The launcher is also locked with `BANK_GENERATION_AUTHORIZED = False`. These are refusal gates, not the final run configuration.

Embedding the exact `OUTPUT_DIR` changed the generator source hash; the pre-declared authorization-literal change changes it again. The deterministic two-state hash chain is now recorded:

1. **Configured-but-locked generator** (`lc518_generator_state1.py`): the exact absolute `OUTPUT_DIR` `/home/z/lc518_run/bank` embedded, `BANK_GENERATION_AUTHORIZED` still `False`. SHA-256 `276b9f49f5a3a975c530cc4eca02b0a0f3407ab824d12031f43175a72feb14fe`. Executed on 2026-11-02 (UTC) only to confirm refusal: exit status 1, `REFUSED: separate owner authorization for study-bank generation is absent.`; no run root was created.
2. **Authorized execution generator** (`lc518_generator_state2.py`): results only from the pre-declared authorization-literal change to `True`, with no other source edits. SHA-256 `1335a42d06d64cf7e847981fc68eee07945655128e82e7f08bc43e774d1cb41c`. The launcher must pin this hash for the run.
3. **Activation diff** (`activation_diff.txt`, SHA-256 `578d17163701d549d17c19e5e1a785709fd1d08bf3572b77ac7058fbc13c8a64`), exactly one changed line:

```text
--- lc518_generator_state1.py
+++ lc518_generator_state2.py
@@ -33,7 +33,7 @@
 # variables, command-line arguments, or configuration files.
 EXPECTED_PYTHON_VERSION = (3, 13, 5)
 OUTPUT_DIR: str | None = "/home/z/lc518_run/bank"
-BANK_GENERATION_AUTHORIZED = False
+BANK_GENERATION_AUTHORIZED = True
 
 JSON_KW = dict(sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
```

The separate owner GO naming this protocol's external SHA-256 must explicitly authorize that exact activation change. The launcher authorization literal is enabled as part of the same GO; its resulting source hash is measured and recorded in the run manifest. No bank-generation source is activated by this protocol file itself: state 2 has never been executed, and no bank, staging directory, or run root exists as of configuration freeze. The hashes above must not be silently changed after the GO; any change requires a new protocol revision, a new chain, and a new GO.
