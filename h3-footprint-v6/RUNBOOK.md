# H3 Footprint V6 Runbook

This runbook separates untrusted candidate execution from generation and from the development host. It is part of the frozen V6 artifact set. Do not start generation or evaluation unless FREEZE.json, the annotated V6 tag, and a passing isolation-report.json all exist.

## Roles

- Operator: runs the local OpenCode generation job and performs the sandbox evaluation.
- Reviewer: checks the frozen harness, the isolation evidence, and the resulting gate report; does not operate the local job.

## Stage A: generation (network allowed, no candidate execution)

Generation runs where OpenCode has the model network access it needs. This stage may be the development host.

1. Use the frozen `generate.py` from this folder.
2. Set `OPENCODE_EXE` if opencode is not on PATH.
3. Run in predeclared segments: `python generate.py --batches 100`, then 200, 300, 400.
4. `generate.py` only parses returned fenced text and writes bodies. It does not import, compile, or execute candidate code. Do not run candidate files, notebooks, or ad hoc probes on the host.
5. After each segment, evaluate futility and support only inside the sandbox (Stage B). If the futility rule triggers, stop generation.

## Host staging (read-only mapping)

Create two host directories:

- `C:\h3-staging`, containing only:
  - the frozen `h3-footprint-v6` harness files (this folder);
  - `h3-footprint-v6/generated/bodies/*.py`;
  - `h3-footprint-v6/generated/attempts.jsonl`;
  - optionally `h3-footprint-v6/generated/raw/` for audit.
- `C:\h3-out`, initially empty. This is the only writable host mapping.

Do not stage `.git`, the project checkout, user profiles, SSH keys, cloud credentials, browser data, or any host directory outside these two roots. `C:\h3-staging` must be mapped read-only; `C:\h3-out` may be mapped writable.

## Stage B: evaluation (sandbox, networking disabled)

Evaluation must run inside Windows Sandbox or an equivalent restricted VM. `run_gate.py` uses ordinary Python subprocesses; starting it on the host does not move those subprocesses into a sandbox.

Use `isolation/windows-sandbox.wsb` as the configuration template. It requires:

- `<Networking>Disable</Networking>`;
- `<ClipboardRedirection>Disable</ClipboardRedirection>`;
- `C:\h3-staging` mapped read-only and `C:\h3-out` mapped writable;
- `<vGPU>Disable</vGPU>`;
- no logon command that copies credentials or opens the host repository.

Inside the sandbox, create a marker file that exists only in the sandbox, for example `C:\h3-sandbox-marker`, and then run the isolation probe before any generation is evaluated:

```
python C:\h3-staging\h3-footprint-v6\isolation_probe.py ^
  --harness-root C:\h3-staging\h3-footprint-v6 ^
  --host-write-target C:\Users\Foued\PycharmProjects\failure-concentration-study\README.md ^
  --repo-path C:\Users\Foued\PycharmProjects\failure-concentration-study ^
  --sandbox-marker C:\h3-sandbox-marker ^
  --out C:\h3-out\isolation-report.json
```

The probe tests, from inside the sandbox:

1. the host repository path is not present;
2. a network connection to `1.1.1.1:443` or `8.8.8.8:53` fails;
3. opening the host write target for append fails;
4. opening `expected_values.json` in the read-only harness for append fails;
5. opening `isolation/fixtures/other_candidate.py` for append fails;
6. a candidate that emits an extra nonce-tagged line at `atexit` is invalidated rather than accepted;
7. a wrong solver still receives k = 30 after the tamper attempts.

If any check is false, stop. Do not run the evaluator.

Then run the evaluator from the read-only harness, writing only to the output mapping:

```
python C:\h3-staging\h3-footprint-v6\run_gate.py ^
  --results-dir C:\h3-out\results ^
  --scratch-dir C:\h3-scratch ^
  --freeze-manifest C:\h3-staging\h3-footprint-v6\FREEZE.json ^
  --isolation-report C:\h3-out\isolation-report.json
```

`run_gate.py` verifies the frozen core artifact hashes before evaluation, refuses to start if any hash differs or if the isolation report fails, runs each candidate in a fresh scratch directory under `C:\h3-scratch`, and re-verifies the hashes afterward. A post-evaluation mismatch forces `verdict: FAIL` with reason `harness_modified_during_run`.

Export only `C:\h3-out\results\footprint.json`, `C:\h3-out\results\REPORT.md`, and `C:\h3-out\isolation-report.json` back to the host. The host copy of the staging root stays read-only to the sandbox.

## Isolation report

`isolation-report.json` is produced by `isolation_probe.py` inside the sandbox and must contain these boolean fields, all true:

- `evaluator_inside_sandbox`;
- `network_blocked`;
- `host_write_blocked`;
- `expected_values_write_blocked`;
- `other_candidate_write_blocked`;
- `extra_output_rejected`;
- `repo_not_present`;
- `correct_result_after_tamper_attempts`.

It also records the sandbox hostname, marker path, harness root, host write target, repository path, timestamp, and probe details. A report that only shows that `WindowsSandbox.exe` exists, without evidence that the probe and evaluator ran inside it, does not satisfy this requirement.

The report is produced before generation is evaluated, lives in the writable output mapping, and is not hashed into FREEZE.json because it is run evidence rather than a frozen harness artifact.

## Segment loop

1. Generate batches 0-99 on the host.
2. Stage the new bodies into the read-only staging root, refresh the read-only mapping, and evaluate in the sandbox.
3. Read `futility` in `results/footprint.json`. If `futility.triggered` is true, stop.
4. Otherwise generate 100-199 and repeat.
5. Continue to 200-299 and 300-399 only while futility has not triggered.
6. Preserve every segment's `attempts.jsonl`, `footprint.json`, `REPORT.md`, and `isolation-report.json`.

The futility rule counts every eligible group, including candidates labelled `other`, although `other` cannot support a cell. This can delay a stop but cannot cause a false PASS.

## Stop conditions

- Isolation report missing or failing: stop; do not evaluate.
- Frozen core hash mismatch: stop; do not trust the run.
- Futility triggered at a checkpoint: stop generation and evaluate the current data.
- 400 batches completed: evaluate and report under the frozen thresholds.
- Any candidate is executed outside the sandbox: discard the run as an isolation failure.

No held-out scoring, power analysis, or H3 inference is part of this runbook.
