# H3 Footprint V8 Runbook

This runbook separates untrusted candidate execution from generation and from the development host. It is part of the frozen V8 artifact set. Do not start generation or evaluation unless FREEZE.json, the annotated V8 tag, and a passing read-only isolation-report.json all exist.

## Roles

- Operator: runs the local OpenCode generation job, performs the sandbox probe, and performs the sandbox evaluation.
- Reviewer: checks the frozen harness, the isolation evidence, and the resulting gate report; does not operate the local job.

## Stage A: generation (network allowed, no candidate execution)

Generation runs where OpenCode has the model network access it needs. This stage may be the development host.

1. Use the frozen `generate.py` from this folder.
2. Set `OPENCODE_EXE` if opencode is not on PATH.
3. Run in predeclared segments: `python generate.py --batches 100`, then 200, 300, 400.
4. `generate.py` only parses returned fenced text and writes bodies. It does not import, compile, or execute candidate code. Do not run candidate files, notebooks, or ad hoc probes on the host.
5. After each segment, evaluate futility and support only inside the sandbox (Stage B). If the futility rule triggers, stop generation.

## Host staging (read-only mapping)

Create three host directories:

- `C:\h3-staging`, containing only:
  - the frozen `h3-footprint-V8` harness files (this folder);
  - `h3-footprint-V8/generated/bodies/*.py`;
  - `h3-footprint-V8/generated/attempts.jsonl`;
  - optionally `h3-footprint-V8/generated/raw/` for audit;
  - `h3-footprint-V8-evidence/isolation-report.json` after the probe has been exported (Stage B1).
- `C:\h3-out`, initially empty. This is the only writable host mapping used by the evaluator.
- `C:\h3-scratch`, an initially empty scratch root inside the sandbox. It must be a sandbox-local NTFS directory, not a host mapping, and must not contain a harness, repository, or credentials.

Do not stage `.git`, the project checkout, user profiles, SSH keys, cloud credentials, browser data, or any host directory outside these roots. `C:\h3-staging` must be mapped read-only; `C:\h3-out` may be mapped writable. `C:\h3-scratch` must be sandbox-local so its low-integrity label applies to candidate writes.

## Stage B1: isolation probe (sandbox, networking disabled)

Evaluation must run inside Windows Sandbox or an equivalent restricted VM. `run_gate.py` uses ordinary Python subprocesses; starting it on the host does not move those subprocesses into a sandbox.

Use `isolation/windows-sandbox.wsb` as the configuration template. It requires:

- `<Networking>Disable</Networking>`;
- `<ClipboardRedirection>Disable</ClipboardRedirection>`;
- `C:\h3-staging` mapped read-only and `C:\h3-out` mapped writable;
- `<vGPU>Disable</vGPU>`;
- no logon command that copies credentials or opens the host repository.

Inside the first sandbox session, create a marker file that exists only in the sandbox, for example `C:\h3-sandbox-marker`, and run the isolation probe before any candidate is evaluated:

```
python C:\h3-staging\h3-footprint-V8\isolation_probe.py ^
  --harness-root C:\h3-staging\h3-footprint-V8 ^
  --host-write-target C:\Users\Foued\PycharmProjects\failure-concentration-study\README.md ^
  --repo-path C:\Users\Foued\PycharmProjects\failure-concentration-study ^
  --sandbox-marker C:\h3-sandbox-marker ^
  --output-root C:\h3-out ^
  --out C:\h3-out\isolation-report.json
```

The probe tests, from inside the sandbox:

1. the host repository path is not present;
2. a network connection to `1.1.1.1:443` or `8.8.8.8:53` fails;
3. opening the host write target for append fails;
4. opening `expected_values.json` in the read-only harness for append fails;
5. opening `isolation/fixtures/other_candidate.py` for append fails;
6. a candidate that emits an extra nonce-tagged line at `atexit` is invalidated rather than accepted;
7. a candidate that uses `io.open` against an isolation-report canary and a results canary under the output root cannot change either file, while a wrong solver still receives k = 30 after the tamper attempts;
8. a candidate that reaches the already-loaded `os` module through `sys.modules` and runs `icacls /remove:d`, `icacls /grant`, `icacls /reset`, `takeown`, and `icacls /setintegritylevel` cannot remove the lock or change either canary, because the worker loaded the candidate at low integrity;
9. direct trusted writes to the output root fail while the deny ACE is active, still fail after the lock-removal attempt, and succeed only after the evaluator removes the ACE.

If any check is false, stop. Do not run the evaluator.

Export only `C:\h3-out\isolation-report.json` to the host and place it at `C:\h3-staging\h3-footprint-V8-evidence\isolation-report.json`. Inspect that `ok` is true and that every required boolean is true. Then shut down the sandbox.

## Stage B2: evaluation (fresh sandbox, networking disabled)

Start a fresh sandbox session with the same two mappings. `C:\h3-staging` is read-only, so the exported isolation report is now read-only. `C:\h3-out` is writable. Remove any old results from `C:\h3-out` before the run, leaving only the report in staging.

Run the evaluator from the read-only harness:

```
python C:\h3-staging\h3-footprint-V8\run_gate.py ^
  --results-dir C:\h3-out\results ^
  --scratch-dir C:\h3-scratch ^
  --freeze-manifest C:\h3-staging\h3-footprint-V8\FREEZE.json ^
  --isolation-report C:\h3-staging\h3-footprint-V8-evidence\isolation-report.json
```

`run_gate.py` refuses to start if the isolation report is inside the output root, is writable, fails a required check, or if any frozen core hash differs. It verifies the report and hashes before creating the result handles, opens `footprint.json` and `REPORT.md`, locks `C:\h3-out` with a deny ACE for the current user, evaluates all candidates, writes through the open handles, reads both files back while the lock is active, re-verifies the core hashes, and removes the lock in a `finally` block. A post-evaluation hash mismatch forces `verdict: FAIL` with reason `harness_modified_during_run`.

Every candidate scratch directory is set to low integrity before any worker runs. Each `probe_worker.py` process drops its own token to low integrity before it loads or executes a candidate module. The output root and harness stay at the sandbox user's normal integrity. A low-integrity candidate therefore cannot write up to `C:\h3-out`, cannot change its DACL through owner `WRITE_DAC`, and cannot raise its integrity. If the low-integrity drop or scratch relabel fails, candidates are invalidated and the probe check fails; do not treat that run as isolated.

The lock denies existing children and inherited write/delete access for new children. If the evaluator is interrupted before its `finally` block runs, restore access from inside the sandbox with:

```
icacls C:\h3-out /remove:d %USERNAME% /T
```

If the sandbox has already been shut down, run the equivalent command on the host copy of `C:\h3-out` before using it again.

Export only `C:\h3-out\results\footprint.json` and `C:\h3-out\results\REPORT.md` back to the host. The host copy of the staging root stays read-only to the sandbox.

## Isolation report

`isolation-report.json` is produced by `isolation_probe.py` inside the sandbox and must contain these boolean fields, all true:

- `evaluator_inside_sandbox`;
- `network_blocked`;
- `host_write_blocked`;
- `expected_values_write_blocked`;
- `other_candidate_write_blocked`;
- `output_write_blocked`;
- `candidate_output_write_blocked`;
- `output_lock_removal_blocked`;
- `candidate_output_lock_removal_blocked`;
- `extra_output_rejected`;
- `repo_not_present`;
- `correct_result_after_tamper_attempts`.

It also records the sandbox hostname, marker path, harness root, host write target, repository path, output root, lock detail, lock-removal detail, timestamp, and probe details. A report that only shows that `WindowsSandbox.exe` exists, without evidence that the probe and evaluator ran inside it, does not satisfy this requirement.

The report is produced before generation is evaluated. It is stored in read-only staging for the evaluation session and is not hashed into FREEZE.json because it is run evidence rather than a frozen harness artifact.

## Segment loop

1. Generate batches 0-99 on the host.
2. Stage the new bodies into the read-only staging root, refresh the read-only mapping, and evaluate in a fresh sandbox.
3. Read `futility` in `results/footprint.json`. If `futility.triggered` is true, stop.
4. Otherwise generate 100-199 and repeat.
5. Continue to 200-299 and 300-399 only while futility has not triggered.
6. Preserve every segment's `attempts.jsonl`, `footprint.json`, `REPORT.md`, and `isolation-report.json`.

The futility rule counts every eligible group, including candidates labelled `other`, although `other` cannot support a cell. This can delay a stop but cannot cause a false PASS.

## Stop conditions

- Isolation report missing, writable, inside the output root, or failing: stop; do not evaluate.
- Frozen core hash mismatch: stop; do not trust the run.
- Output-root lock failure: stop; do not evaluate.
- Futility triggered at a checkpoint: stop generation and evaluate the current data.
- 400 batches completed: evaluate and report under the frozen thresholds.
- Any candidate is executed outside the sandbox: discard the run as an isolation failure.

No held-out scoring, power analysis, or H3 inference is part of this runbook.
