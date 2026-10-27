# H3 Footprint V5 Runbook

This runbook separates untrusted candidate execution from generation and from the development host. It is part of the frozen V5 artifact set. Do not start generation or evaluation unless FREEZE.json, the annotated V5 tag, and a completed isolation-report.json all exist.

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

## Staging (no repository, no credentials)

Create a dedicated staging directory on the host, for example `C:\h3-staging`, containing only:

- the frozen `h3-footprint-v5` harness files (this folder);
- `h3-footprint-v5/generated/bodies/*.py`;
- `h3-footprint-v5/generated/attempts.jsonl`;
- optionally `h3-footprint-v5/generated/raw/` for audit;
- an empty `h3-footprint-v5/results/` directory.

Do not stage `.git`, the project checkout, user profiles, SSH keys, cloud credentials, browser data, or any host directory outside this staging root.

## Stage B: evaluation (sandbox, networking disabled)

Evaluation must run inside Windows Sandbox or an equivalent restricted VM. `run_gate.py` uses ordinary Python subprocesses; starting it on the host does not move those subprocesses into a sandbox.

Windows Sandbox configuration requirements:

- `<Networking>Disable</Networking>`;
- `<ClipboardRedirection>Disable</ClipboardRedirection>`;
- no mapped host folder except the staging root, and that mapping must be read-only;
- `<vGPU>Disable</vGPU>`;
- no logon command that copies credentials or opens the host repository.

Inside the sandbox:

1. Copy the staged harness and bodies to a writable sandbox path, for example `C:\h3`.
2. Run the isolation probe and write `isolation-report.json` (schema below).
3. If isolation fails, stop. Do not run the evaluator.
4. Run the evaluator: `cd C:\h3\h3-footprint-v5` then `python run_gate.py`.
5. Export only `results/footprint.json`, `results/REPORT.md`, and `isolation-report.json` back to the host staging results area.

## Isolation report

`isolation-report.json` must be produced inside the sandbox and must record at least:

- `mechanism`: Windows Sandbox, container, or dedicated VM, with the configuration used;
- `evaluator_inside_sandbox`: true, with evidence such as the sandbox hostname, a sandbox-only marker file, or the sandbox working directory;
- `network_blocked`: true, with the probe target and the observed failure;
- `host_write_blocked`: true, with the probed host path and the observed failure;
- `repo_not_present`: true, and the paths checked;
- `staging_root`: the sandbox path used;
- `timestamp_utc`;
- `operator`: name or identifier.

A report that only shows that `WindowsSandbox.exe` exists, without evidence that the evaluator ran inside it, does not satisfy this requirement.

## Segment loop

1. Generate batches 0-99 on the host.
2. Stage and evaluate in the sandbox.
3. Read `futility` in `results/footprint.json`. If `futility.triggered` is true, stop.
4. Otherwise generate 100-199 and repeat.
5. Continue to 200-299 and 300-399 only while futility has not triggered.
6. Preserve every segment's `attempts.jsonl`, `footprint.json`, `REPORT.md`, and `isolation-report.json`.

## Stop conditions

- Isolation report missing or failing: stop; do not evaluate.
- Futility triggered at a checkpoint: stop generation and evaluate the current data.
- 400 batches completed: evaluate and report under the frozen thresholds.
- Any candidate is executed outside the sandbox: discard the run as an isolation failure.

No held-out scoring, power analysis, or H3 inference is part of this runbook.
