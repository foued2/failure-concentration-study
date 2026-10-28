# V9 runbook

Revision 7. Every command below exists and is exercised by the test suite.

**Invariant: nothing that needs model output happens before the Sandbox checks
pass.** Steps 0-2 make no model calls and generate no candidates.

**Generation is not implemented.** `V9_AUTHORIZE_GENERATION=1` unlocks nothing;
the generator exits non-zero with an explicit message. Do not treat this runbook
as authorization to generate.

## Roles

- **Operator** runs the host controller and the Sandbox preflight/rendezvous.
- **Reviewer** verifies hashes, the raw reports and the effective permission
  evidence; does not run the job.

## Step 0: host checks (no model calls, no Sandbox)

```
python -m unittest discover -s tests -v
python make_manifest.py --check
python controller.py --verify-boundary
python generation/generate_v9.py --verify-config --opencode <cli>
```

Expected:

- all tests pass and `MANIFEST.json` matches;
- `--verify-boundary` prints `"inside_sandbox": false` and exits 2 on an ordinary
  host. That is the correct host result, and it is why evaluation is blocked;
- the config evidence shows `agent_loaded: true`, `agent_fully_denied: true`, and
  all three frozen model IDs present.

## Step 0b: is Sandbox even available on this host?

```
python evidence/windows_sandbox_capability.py --out sandbox-capability-post-enable-2026-10-28.json
```

Use `--out` with a distinct name so an earlier diagnosis is preserved; the
default writes `evidence/sandbox-capability-2026-10-28.json`.

Read `classification` in the report:

- `SUPPORTED_AND_READY_TO_ENABLE` — Windows Sandbox is installed and enabled; go
  to step 1.
- `ENABLED_RESTART_PENDING` — the feature is enabled but not effective
  (`WindowsSandbox.exe` absent, `HypervisorPresent` false). Restart Windows, then
  re-run the diagnostic and expect `SUPPORTED_AND_READY_TO_ENABLE`. Nothing else
  in this runbook can pass before that restart.
- `BLOCKED_PRIVILEGES` — the feature exists but is disabled and the session is
  not elevated. Run the documented command from an **elevated** PowerShell:

  ```
  Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -All -NoRestart
  ```

  No restart is performed automatically. If `RestartNeeded` is true, restart and
  re-run the diagnostic; `WindowsSandbox.exe` and the feature state should change.
- `BLOCKED_FIRMWARE_VIRTUALIZATION` — enable VT-x/AMD-V in firmware, then retry.
- `BLOCKED_WINDOWS_FEATURE_OR_POLICY` — the feature is absent from the image;
  this needs servicing, not a hardware change.
- `BLOCKED_HARDWARE_REQUIREMENT` / `UNSUPPORTED_ENVIRONMENT` — stop; use another
  host.

Do not bypass UAC, do not use unofficial installers, and do not treat a disabled
feature as a hardware verdict.

State on 2026-10-28: the command ran in a session elevated through one approved
UAC prompt (`evidence/sandbox-enable-elevated-2026-10-28.json`, `applied: true`,
`restart_needed: true`), and the post-enable diagnosis is
`ENABLED_RESTART_PENDING`. The machine has **not** been restarted by the agent.

## Step 1: stage the Sandbox image (host)

The Sandbox base image has **no Python**. The interpreter must be an official
embeddable distribution, not a normal install and not a virtualenv: a venv keeps
host absolute paths in `pyvenv.cfg`, and a normal install has no relocatable
`python3xx.zip`. The controller rejects both by construction.

Stage and verify the pinned interpreter (it refuses to extract unless the
SHA-256 and file size match python.org's published values):

```
python evidence/stage_python_runtime.py --dest C:\v9-stage\py-embed
```

Evidence: `evidence/python-runtime-2026-10-28.json`. It records the published and
computed SHA-256, the extracted file hashes, `interpreter_preflight`, and two
host-only checks: the staged interpreter starts the agent (nonce echoed, `mode:
preflight`, `inside_sandbox: false`) and runs one fixture job through the
supervisor and Job Object (`status: ok`, `tree_empty: true`).

Then run the preflight:

```
python controller.py --preflight ^
  --inbox  C:\v9-stage\in ^
  --outbox C:\v9-stage\out ^
  --python-root C:\v9-stage\py-embed ^
  --wsb-out C:\v9-stage\v9-preflight.wsb ^
  --report  C:\v9-stage\preflight-attestation.json ^
  --handshake-timeout 600
```

`--preflight`:

1. runs `interpreter_preflight` on `--python-root` (interpreter, stdlib zip,
   runtime DLL, no `pyvenv.cfg`) and refuses to continue if it is not portable;
2. copies the five runtime files (`supervisor.py`, `child_runner.py`,
   `protocol.py`, `winjob.py`, `sandbox_agent.py`) into the inbox — the agent
   itself must arrive through the read-only mapping;
3. builds the `.wsb` and re-parses it, checking that the interpreter and the agent
   script are covered by read-only mappings, that exactly one mapping is writable
   (the outbox), that networking/clipboard/vGPU/audio/video/printer are disabled,
   and that guest paths are absolute and unique;
4. writes `session.json` **before** anything launches;
5. waits for `hello.json` and verifies nonce, `inside_sandbox`, and the
   `WDAGUtilityAccount` account;
6. refuses to proceed if any `job.json` or `response-*.json` exists;
7. writes the attestation JSON and exits. **It never publishes a job and cannot
   evaluate a candidate.**

Add `--launch` to start `WindowsSandbox.exe` after the session file is written.
Without `--launch`, start the Sandbox yourself with the emitted `.wsb`; the agent
polls for `session.json`, so either order works.

### What ("Sandbox") must be recorded, as raw files

Each item needs a **paired positive control**, so a broken probe cannot pass as
"the boundary held":

| Probe | Negative result expected | Positive control |
|---|---|---|
| read `C:\Users\<host>\...\oracle.py` and the repo root | denied / not found | read `C:\...\h3-in\protocol.py` succeeds |
| open a TCP connection | fails | not applicable — record the exact error |
| write into the read-only inbox | denied | write into the outbox succeeds |
| spawn a child that outlives the parent | tree killed, `tree_empty: true` | a child that exits normally is reaped |
| plant a junction/symlink in the outbox | host rejects with `reparse point` | a normal response file is accepted |
| read token B before it is published | B absent from the inbox | token A is present and readable |

The fixture reports must be saved verbatim (file hashes included), not summarised.

## Step 2: two-token rendezvous (Sandbox)

Order matters, and it cost three runs to establish it:

1. close every running Sandbox first - only one instance can exist, and a
   stopping instance keeps the mapped folder locked;
2. stage the runtime into the inbox and write `session.json` **before** the
   Sandbox starts, because the host cannot rename files inside a live mapping;
3. start the controller (it writes `session.json`, then waits), and only then
   launch `WindowsSandbox.exe` with the serve-mode `.wsb`;
4. the guest scratch is on the guest's local disk; a mapped folder cannot take
   an integrity label, and the supervisor refuses to run without it.

```
python controller.py --rendezvous --transport sandbox ^
  --inbox C:\v9-stage\in --outbox C:\v9-stage\out ^
  --report C:\v9-stage\rendezvous-log.json
```

Result on 2026-10-28: **FAIL**. Job A was answered correctly (111,
`tree_empty: true`) five seconds after launch; job B was published and never
answered, and no response for B appeared four minutes later. `ordering_ok` is
false and the cause is unresolved. Do not proceed to step 3 or 4 on this result.

The harness publishes token A, requires the answer to be A, requires
`tree_empty: true`, then publishes token B and requires the answer to be B. It
records whether B was visible in the inbox before A completed.

Revision 7 adds guest instrumentation to the same harness, so a failing run now
carries `guest_events`, `telemetry_anomalies` and a named `diagnostic` in its
report. Read the tree before changing anything:

| observation | classification | next question |
| --- | --- | --- |
| heartbeat continues, B never discovered | `inbox_not_refreshed` | how do inbox updates become visible? |
| heartbeats stop before B | `agent_stopped` | did the agent exit, crash or stall? |
| B discovered and started, no response | `supervisor_or_response_path` | supervisor execution or response publication |
| B response recorded, host saw none | `response_written_but_not_visible` | outbox visibility |
| no instrumentation even for A | `agent_not_instrumented` | the run cannot explain anything |
| telemetry fails validation | `ambiguous_telemetry` | the cause stays unresolved |

Telemetry is evidence of what the agent did, never of isolation. A missing or
ambiguous diagnostic is still a FAIL.

Stop if `ordering_ok` is false or if the mapping's refresh behaviour is
ambiguous. Do **not** substitute a slower or weaker transport; that decision goes
back to design review.

## Step 3: generation — **NOT IMPLEMENTED / BLOCKED**

```
set V9_AUTHORIZE_GENERATION=1
python generation/generate_v9.py --batches 100
```

This exits non-zero with "Generation is NOT IMPLEMENTED in V9". The batch runner
has not been written. The controls that *are* implemented:

- one workspace per batch; deny-all agent; no `--auto`;
- a batch is rejected if it contains a tool event, a permission event, a
  malformed event line, a nonzero exit, or fewer than the requested eight valid
  bodies;
- surplus bodies are capped at eight in response order and recorded as overflow.

**Before any generation run**, the support-cell classification and PASS/WEAK/FAIL
rules must be committed and their hash recorded, so the verdict layer cannot be
shaped by results. That pre-commitment does not exist yet.

## Step 4: evaluation (Sandbox only)

```
python controller.py --bodies <staging> --transport sandbox ^
  --inbox C:\v9-stage\in --outbox C:\v9-stage\out
```

The controller refuses `--transport host-local` unless `--allow-host-local` is
passed explicitly, and rows produced that way are marked `authorized: false`.
With `--transport sandbox` it refuses **before staging anything** unless the
fail-closed gate passes (`python controller.py --check-execution-gate` prints
why). A verified handshake is necessary but never sufficient: the gate also
requires every prerequisite gate to be PASS, hash-pinned evidence that still
asserts the claimed result, committed verdict rules and a separate
`EVALUATION_AUTHORIZATION.json` binding the policy and the status ledger. None of
that exists in this revision, so this command exits 2.

It refuses to publish a new job unless the previous response exists and reports
`tree_empty: true`. Every response is treated as hostile input: bounded size, no
reparse points, strict schema. Any `boundary_error`, `staging_mismatch` or
supervisor error aborts the run; it is never scored.

## Stop conditions

**To start a preflight or rendezvous test** (steps 1-2): stop only on a manifest
mismatch, a failing unit test, an unusable interpreter mapping, or a permission
leak. `NOT_RUN` Sandbox gates are expected at this point — they are the thing the
test is meant to fill in.

**To authorize generation or evaluation**: stop unless steps 1-2 are `PASS` with
raw recorded evidence, the manifest matches, the verdict rules are committed and
hashed, and a reviewer has signed off. A `NOT_RUN`, `PARTIAL` or
`NOT_IMPLEMENTED` gate blocks authorization, not testing.

## Throughput, before committing to 400 batches

Windows Sandbox runs one instance at a time and takes tens of seconds to become
usable. If per-item rendezvous ordering cannot be demonstrated, the safe fallback
is a fresh Sandbox per item, which changes the cost of a 400-batch schedule by an
order of magnitude. Measure the cold-start and per-job cost in step 2 and record
it; do not discover this after generation is authorized.

## Artifacts

Per run: `preflight-attestation.json`, `rendezvous-log.json`, the isolation
probe reports and their positive controls, generation `attempts.jsonl`, per-probe
response records (job id, body hash, probe index, exit status, timeout,
tree-empty, bounded stdout hash, `inside_sandbox`), and the controller's scored
rows. The report must be recomputable from these records alone.
