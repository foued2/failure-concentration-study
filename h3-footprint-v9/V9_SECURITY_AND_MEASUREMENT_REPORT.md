# V9 security and measurement report

**Date:** 2026-10-28 (revision 9)
**Branch:** `dev/h3-footprint-v9-implementation-2026-10-28`
**Status:** implementation; not frozen; **no candidate generation or evaluation authorized.**

Revision 3 repaired the two operational blockers found in review of revision 2.
Revision 4 answered the follow-up question — *can this machine run Sandbox at
all?* — and staged the interpreter the preflight needs. Revision 5 applied the
documented enable command in a session elevated through a single approved UAC
consent prompt. Revision 6 is the first with the Sandbox actually running: the
preflight handshake verifies, and the two-token rendezvous **fails**. Revision 7
closes the authorization gap that the handshake exposed and instruments the guest
so the failure can be explained; the failure itself is still unresolved and
evaluation stays blocked. Revision 8 records what the job loop sees on each poll
and makes an immutable per-job request protocol available as an opt-in diagnostic;
the default transport and the FAIL verdict are unchanged. Revision 9 makes that
protocol fail closed on any ambiguous or truncated scan and exercises the
heartbeat state-sharing fix in a second diagnostic run.

## Revision 4: capability, not assumption

The revision-3 evidence showed `WindowsSandbox.exe` absent and stopped there.
That established the feature was not installed, not that the machine was unsuitable.
The read-only diagnostic (`evidence/windows_sandbox_capability.py`) now records:

| Check | Value |
|---|---|
| OS | Windows 10 Pro 22H2, build 19045.7807, x64 |
| Machine | physical, MSI MS-7699, AMI BIOS V1.2 |
| CPU | AMD FX-8350, 4 cores / 8 logical processors |
| Firmware virtualization | enabled |
| VM monitor mode extensions | true |
| Second-level address translation | true |
| RAM / free disk on C: | 16.0 GiB / 23.4 GiB |
| `HypervisorPresent` | false (expected while the feature is off) |
| `Containers-DisposableClientVM` | **Disabled** (`Win32_OptionalFeature` InstallState=2) |
| Session | medium integrity, member of Administrators, UAC-filtered |

`Get-WindowsOptionalFeature` needs elevation, so the state came from
`Win32_OptionalFeature`, which does not. That distinction matters: the feature
was **present and disabled**, not absent, so this was a privilege blocker rather
than a hardware or image blocker. (The table above is the pre-enable diagnosis,
`evidence/sandbox-capability-2026-10-28.json`.)

The pre-enable classification was `BLOCKED_PRIVILEGES`, and the documented
command is:

```
Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -All -NoRestart
```

Running it from an unelevated session returns exactly
`L'opération demandée nécessite une élévation.` (`evidence/sandbox-enable-attempt-2026-10-28.json`,
`applied: false`, rc 2). UAC was not bypassed and nothing was installed then.

## Revision 5: feature enabled, restart pending

Foued approved one ordinary UAC consent prompt. In the resulting elevated
session the documented command was run once, and its result was committed
verbatim as `evidence/sandbox-enable-elevated-2026-10-28.json`:

| Field | Value |
|---|---|
| `elevated` | true |
| `applied` | true |
| `restart_needed` | true |
| `error` | null |
| `before` / `after` | 0 / 2 (raw cmdlet return codes, not feature states) |

No bypass, no policy change, no unofficial installer, no automatic restart. The
elevation was scoped to that one command; the working session is still medium
integrity, which is why the post-enable diagnostic records `elevated: false`.

The post-enable diagnosis
(`evidence/sandbox-capability-post-enable-2026-10-28.json`) is
`ENABLED_RESTART_PENDING`: `Containers-DisposableClientVM` InstallState=1, but
`WindowsSandbox.exe` is still absent and `HypervisorPresent` is false. The
feature is **enabled, not yet effective**. Every Sandbox gate therefore stays
`NOT_RUN`, generation stays `BLOCKED` and evaluation stays `BLOCKED`. The next
action is an operator restart, not a code change.

The diagnostic ladder now separates the three states that revision 4 conflated:
absent (`InstallState=3`), disabled (`InstallState=2`), and enabled but restart
pending (`InstallState=1` with `WindowsSandbox.exe` missing). It also accepts
`--out`, so a new diagnosis cannot silently overwrite an earlier one.

## Revision 6: the Sandbox runs, the broker does not

After Foued restarted the machine, the post-restart diagnosis
(`evidence/sandbox-capability-post-restart-2026-10-28.json`) is
`SUPPORTED_AND_READY_TO_ENABLE`: `InstallState=1`, `WindowsSandbox.exe` present,
`HypervisorPresent` true. `VMMonitorModeExtensions` and SLAT read false in the
same report because a running hypervisor owns those features — `systeminfo`
says so explicitly ("un hyperviseur a été détecté"). The diagnostic now records
`virtualization_flags_masked_by_hypervisor` and stops treating that masking as a
hardware verdict, which the revision-5 ladder would have reported as
`BLOCKED_HARDWARE_REQUIREMENT` on a host that had just started a Sandbox.

**Preflight passes.** A real Sandbox was launched and the agent replied with the
host nonce as `WDAGUtilityAccount`, `inside_sandbox: true`, computer
`0E3D64FC-DC7E-4`, `jobs_published: 0`, no response files
(`evidence/preflight-sandbox-2026-10-28.json`). This is the first Sandbox
evidence in V9.

**Rendezvous fails.** `evidence/rendezvous-sandbox-2026-10-28.json` records
`ordering_ok: false`. Job A (token 111) was answered in five seconds with
`tree_empty: true`; job B (token 222) was published and never answered, and no
response for B existed four minutes later. The raw job and response files are
committed beside the report. Because B's invisibility is indistinguishable from
a slow refresh, the ordering hazard the harness exists to exclude is **not**
excluded.

Three transport defects surfaced on the way and are fixed, with tests:

1. **A live mapping rejects renames.** `os.replace` inside a mapped folder fails
   with `WinError 32` while the Sandbox holds the view, so the atomic
   write-then-rename pattern could not publish a single job. Publication is now
   an ordered direct write: body flushed and closed, `job.json` last, and the
   agent already retries an unparseable job.
2. **Staging after launch is impossible.** The controller re-staged the runtime
   into the inbox after the handshake and hit the same error. Staging is now
   idempotent and, once an attestation exists, verification-only.
3. **The guest cannot label a mapped folder.** `icacls /setintegritylevel` on
   the scratch directory failed inside the Sandbox (`scratch_low_integrity:
   false`, `boundary_error`), because that directory was inside the moved
   outbox. The scratch now lives on the guest's local disk and the failure text
   is recorded in the response instead of being inferred.

What is *not* established: why job B was never observed. At that point the two
candidates were a stale guest-side view of the rewritten `job.json` and an agent
that stopped after its first job; the harness could not distinguish them, because
nothing on the guest side recorded that it was alive.

## Revision 7: authorization is gated, the guest is instrumented

**The gap.** Revision 6 treated a verified handshake as sufficient for
`evaluate_authorized`. That is too weak: the handshake proves an agent ran as
`WDAGUtilityAccount` and echoed a nonce. It says nothing about job ordering,
isolation probes, resource caps or the verdict layer. It also left a second
door: `Controller.evaluate` would accept an attested Sandbox transport and run a
job with no prerequisite check at all.

**Closed at both entry points.** `gates.py` is now the single decision point and
it fails closed. `evaluate_authorized` calls it after the attestation check;
`Controller.evaluate` refuses every transport that declares `requires_sandbox`;
and the `--transport sandbox` CLI path calls `gates.require_authorized()`
*before* staging the runtime or launching anything. The tests assert that a
refused call publishes zero jobs and creates no inbox, outbox or run directory.

**What the gate requires.** `EXECUTION_PREREQUISITES.json` names five
prerequisite gates and pins each evidence file by SHA-256 (canonicalised CRLF→LF
exactly like `MANIFEST.json`). Four conditions must all hold:

1. every named gate is `PASS` in `STATUS.json`;
2. every evidence file exists and matches its pin;
3. the pinned evidence still *asserts* what the gate claims — a gate flipped to
   PASS cannot override a rendezvous report that records `ordering_ok: false`;
4. the verdict rules exist and match their pin, and a separate
   `EVALUATION_AUTHORIZATION.json` binds both the policy hash and the status
   ledger hash.

No authorization file is committed. The real repository gate therefore refuses
with seven blockers, and `python controller.py --check-execution-gate` prints
them.

**Guest instrumentation.** The agent now writes diagnostic events as *new*,
uniquely named files (`agent_start`, `heartbeat`, `job_discovered`,
`job_started`, `response_written`, `exception`), written directly, flushed and
closed — never renamed, because a live mapping rejects renames. Events are
emitted only in serve mode, so the preflight cannot publish telemetry. The host
treats them as untrusted: size cap, allowed names, exact schema, nonce and
attested-pid correlation, reparse-point rejection, and filename/content
agreement. Foreign sessions are ignored; anything else becomes an anomaly.

`run_rendezvous` no longer re-raises a job-B failure. The run stays a FAIL, but
the report carries `guest_events`, `telemetry_anomalies` and a `diagnostic` with
one of the named classifications. Telemetry explains a failure; it is never
isolation evidence, and a missing or ambiguous diagnostic remains `unresolved`.
The original rendezvous report and its raw files are unchanged.

**One instrumented run.** Exactly one rerun was made, on `echo_input.py` only, with
no candidate and no evaluation:

- job A was discovered, started and answered (111, `tree_empty: true`), and its
  three lifecycle events are present;
- after job B was published the agent kept heartbeating — 62 heartbeats, with
  event sequence 68 at report time and 100 in the raw outbox;
- it never recorded `job_discovered` for B, never raised, and produced no
  telemetry anomaly;
- the report labelled the failure `inbox_not_refreshed` under the revision-7
  rule, but that rule treated liveness as progress.

That run excludes an agent that stopped after A and a supervisor/response-path
failure for this run. It does **not** show that the guest's view of `job.json`
was stale: the heartbeat thread proves the process lived, not that the job loop
kept scanning or that it saw old contents. Under revision 8's rules the same
observation is `job_loop_progress_unknown`. The raw set — hello, response A, job
B, session and all 100 events — is preserved unchanged and pinned by hash; the
report's own snapshot was taken at 130 s with 68 events.

**Still blocked.** Evaluation remains refused by the gate and by decision. The
isolation probes have not run, the caps are only `PARTIAL`, the verdict layer does
not exist and no authorization file is committed.

## Revision 8: the loop reports what it saw, and an immutable variant is testable

The revision-7 telemetry answered “is the process alive?” but not “is the loop
still looking?”. Revision 8 closes that gap without turning diagnostics into
isolation evidence:

- the job loop records a bounded `poll_state` snapshot — poll count, last-poll
  time, scan success, visible request filenames, outcome (`new_job`,
  `only_handled`, `no_jobs`, `out_of_order`, `error`), last parsed job
  id/sequence, and an error category plus file;
- `heartbeat` carries the last snapshot, but remains explicitly separate from
  loop progress: only `poll_state` is written by the loop itself;
- the host validates snapshots strictly (exact keys, bounded lists, allowed
  outcomes, nonce/pid correlation, size cap) and never accepts them as proof of
  isolation;
- a missing `job_discovered` alone is no longer labelled stale mapping contents.
  `inbox_not_refreshed` now requires observed scanning with no B request listed;
  otherwise the result is `job_loop_progress_unknown`.

Two new classifications make the next failure more specific:
`job_request_unusable` (a B file was listed but failed validation or parsing)
and `job_request_out_of_order` (a future sequence was listed first).

**Opt-in immutable request protocol.** As a diagnostic variant only, each request
is published under a new name, `job-<sequence>-<job_id>.json`, and a body is
stored once under `bodies/<sha256>.py`. Publishing writes the body first, flushes
and closes it, then creates the job file exclusively; nothing is renamed and
nothing is overwritten. The guest rescans, matches the filename against the
payload, enforces the expected sequence, processes each job at most once, and
keeps unique per-job response files. Duplicate ids, conflicting sequences,
malformed requests, filename/payload mismatches and out-of-order requests are
rejected. The legacy `job.json` path remains the default and the production
transport; `--job-protocol immutable` selects the variant on both the controller
and the generated `.wsb`.

Host tests cover two immutable jobs in sequence, no overwrite or rename, the
rejection cases, content-addressed bodies, repeated polling, an empty/old/new/
broken scan, tree-empty enforcement and one response per job. This is a
diagnostic protocol, not a change to the production path, and it cannot turn
`sandbox_rendezvous_ordering` into a pass.

**One diagnostic run of the variant.** On 2026-10-28, one rendezvous ran with
`--job-protocol immutable` on `echo_input.py`, after closing the previous
Sandbox and clearing the staging folders. The guest's poll telemetry shows the
handoff stage by stage:

- poll 1: empty scan, `no_jobs`;
- poll 2: `job-000001-…json` visible, `new_job`; A was discovered, started and
  answered with 111, `tree_empty: true`;
- poll 3: A still visible, `only_handled` — it was not processed twice;
- poll 4: both filenames visible, `new_job` for sequence 2; B was discovered,
  started and answered with 222, `tree_empty: true`;
- later polls: `only_handled`, with the last parsed job id/sequence updated.

The diagnostic report records `ordering_ok: true`, `protocol: immutable-v1`, one
agent pid (3696) and 199 raw events. That is evidence the immutable handoff works
for this fixture. It is **not** a clean telemetry run: the heartbeat thread had
been given a detached state object, so 132 of the 199 events are heartbeat
snapshots with `poll_count: 0` and no poll time, which the host rejects; the 67
loop and job events are valid. The defect is fixed after the run by sharing one
`JobLoopState` and validating a pre-first-poll heartbeat separately. The run was
not repeated, so the archived raw set keeps its anomalies and this revision
reports it as `PARTIAL`, not a clean pass.

The result does **not** establish ordering for the production `job.json` path,
does not prove isolation and does not authorize evaluation;
`sandbox_rendezvous_ordering` remains `FAIL` and the gate still refuses. Raw set:
`evidence/rendezvous-immutable-2026-10-28.json`,
`evidence/rendezvous-immutable-*`, the `.wsb`, and
`evidence/rendezvous-immutable-events-2026-10-28/` with its hash index.

## Revision 9: the immutable scan fails closed

Source review found that `_decide_immutable()` could execute the expected job
from a scan that also reported a malformed request, a duplicate job id or a
conflicting sequence, and it did not act on the scan's `truncated` flag. That
contradicted the protocol's promise to reject such requests.

The decision is now fail-closed:

- any `scan["errors"]` entry blocks **all** execution for that poll, even when a
  valid expected-sequence job is present;
- `scan["truncated"]` reports `scan_truncated` and yields no job;
- a transient read failure is retried on the next poll; a permanent malformed,
  duplicate or conflicting condition keeps blocking until repaired.

Regression tests cover a valid next job beside a malformed request, a duplicate
id, a conflicting sequence, and a scan artificially truncated below the visible
count, asserting no runner call and no response while blocked. A `max_polls`
bound keeps the blocked-loop tests from hanging. The ordinary A/B sequence,
filename/payload agreement, content-addressed bodies, one-response-per-job and
tree-empty checks are unchanged.

## Revision 4: the interpreter is now real, pinned and verified

Third-party binaries are not acceptable, so the runtime comes from python.org
and is verified against python.org's own metadata at staging time
(`evidence/stage_python_runtime.py`):

- pinned **CPython 3.14.10**, Windows embeddable package (64-bit);
  3.13.18 was source-only, so it has no Windows binaries to pin;
- the script reads the release API, takes the published SHA-256 and file size
  for that exact file, downloads it, and compares what arrived;
- published and computed SHA-256 are both
  `90905e64a840557d8c1bc4f5b74db3d7ee85e3ffb217611cac1c7813acea4159`;
- only after a match does it extract, then runs `interpreter_preflight` and three
  host checks.

Evidence: `evidence/python-runtime-2026-10-28.json`. The host checks are labelled
host checks, because that is what they are:

1. the staged interpreter runs a trivial program (`cpython 3.14.10`);
2. it starts `sandbox_agent.py`, which polls for a session, echoes the nonce with
   `mode: preflight` and `inside_sandbox: false`, and exits 0 — so the agent
   correctly refuses to claim the boundary on the host;
3. it runs one harmless fixture job end to end (agent → supervisor → Job Object →
   child) and produces `status: ok`, `answer: 7`, `tree_empty: true`, with the
   response body hash matching.

The staged tree is `C:\v9-stage\py-embed`, mapped read-only. The full preflight
then passes the interpreter, config and staging gates and stops exactly at the
launch:

```json
{"ok": false, "error": "FatalBoundaryError",
 "detail": "Windows Sandbox is not installed on this host (...WindowsSandbox.exe is absent); the preflight cannot run here",
 "evaluation_attempted": false, "candidate_files": []}
```

Evidence: `evidence/preflight-staged-runtime-2026-10-28.json`. This is the
honest end state: every gate before the Sandbox passes, and the Sandbox gate
stays `NOT_RUN`.

## Evidence is split by where it was produced

| Scope | What it proves | Files |
|---|---|---|
| **Host** | configs are launchable and bounded, the handshake predicates reject what they must, the response channel is validated, the harness itself works, and a verified interpreter can run the guest-side runtime | `tests/unit-test-log.txt`, `evidence/python-runtime-2026-10-28.json`, `evidence/preflight-staged-runtime-2026-10-28.json` |
| **Sandbox** | the isolation actually holds | **empty — every gate is `NOT_RUN`** |

No host result in this document is evidence that the candidate is contained.

## What changed in revision 3

| Defect | Repair |
|---|---|
| The emitted `.wsb` pointed at `C:\h3-py\python.exe` but mapped only the inbox and outbox | `python_root` is now mandatory and is mapped read-only; `verify_sandbox_config` re-parses the emitted XML and refuses an interpreter or agent script that is not covered by a read-only mapping |
| The agent read `session.json` immediately, so launch order could kill it | The agent polls for the session with a timeout; `--preflight` writes the session *before* launching. Either order now works. |
| There was no preflight-only path — the evaluation CLI was the only way to handshake | `--preflight` handshakes, verifies, records the attestation and exits. It rejects `--bodies` and refuses to continue if any job or response file exists. |
| Two-token ordering had no harness | `--rendezvous` publishes A, requires A's answer and `tree_empty`, then publishes B and requires B's answer; it records whether B was visible early |
| The outbox was read with `json.loads` and no limits | Responses are treated as hostile: 64 KiB cap, reparse-point rejection, strict schema, status whitelist, job-id match |

### The interpreter mapping, stated plainly

The Sandbox base image ships no Python. A normal install is not relocatable and a
virtualenv keeps host absolute paths in `pyvenv.cfg`, so neither can simply be
mapped. The supported option is an **embeddable distribution** mapped read-only.

`interpreter_preflight` checks that the directory contains `python.exe`, a
`python3xx.zip` stdlib, a `python3xx.dll`, and no `pyvenv.cfg`. Run against the
host's own install it correctly fails:

```json
{"python_root": "C:\\Program Files\\Python314",
 "checks": {"interpreter_present": true, "runtime_dll_present": true,
            "stdlib_zip_present": false, "no_venv_marker": true},
 "violations": ["stdlib_zip_present"], "ok": false}
```

That is the gate working: the host install cannot be mapped into the Sandbox, so
the preflight stops before launching anything.

### Preflight ordering

1. `interpreter_preflight` (host) — refuse a non-portable interpreter.
2. Stage the five runtime files into the inbox (the agent itself must arrive
   through the read-only mapping).
3. Build and **re-parse** the `.wsb`; refuse an unmapped interpreter or agent.
4. Write `session.json` (nonce).
5. Launch (optional) or wait for the operator to launch the Sandbox.
6. Accept `hello.json` only if nonce matches, `inside_sandbox` is true, and the
   account is `WDAGUtilityAccount`.
7. Refuse if any `job.json` or `response-*.json` exists; write the report; exit.

`--preflight` has no code path that publishes a job, and `--bodies` is rejected
outright.

## The measured host exposure (unchanged, and still the reason for the gate)

A low-integrity child on the host, given the repository path, reads:

```
oracle           READ   """Host-only reference oracle.  SECURITY
expected_values  READ   {   "A1": 3,   "A2": 1, ...
controller       READ   """Host controller: the only component t
```

and a second fixture imports that oracle and answers from the key without solving
anything: `k = 0`, `isolation_verified = False`. Low integrity prevents write-up,
not read-down. Only removing the data from the candidate's filesystem view does
that, which is what the Sandbox mapping is supposed to do — **and that has not
been demonstrated yet.**

## Testing what can be tested on the host

- **Config**: interpreter and agent inside read-only mappings; exactly one
  writable mapping and it is the outbox; networking, clipboard, vGPU, audio,
  video, printer disabled; absolute and unique guest paths; preflight vs serve
  mode emits `--handshake-only` only where intended.
- **Preflight**: valid handshake accepted (synthetic `hello.json`), stale nonce
  rejected, wrong identity rejected, untrusted `inside_sandbox: false` rejected,
  timeout recorded, no job or response published, and the agent survives being
  started *before* the session then handshakes.
- **Hostile outbox**: missing fields, unknown status, job-id mismatch, boolean
  answer, oversized file, invalid JSON, and a valid file.
- **Rendezvous harness**: two tokens, ordering checks, and an explicit refusal to
  run on the host without `--allow-host-local`.

What is *not* tested: a real `WDAGUtilityAccount` handshake, guest-side oracle
invisibility, network egress failure, mapping refresh ordering, and
mapped-folder ACL behaviour. The acceptance path is exercised with a synthetic
`hello.json`, which proves the predicate, not the platform.

## Findings and controls

| # | Finding | Control | Test | Where |
|---|---|---|---|---|
| 1 | Shared interpreter let a candidate replace the worker's emitter | host compares a raw value against a private oracle | `test_stdout_hijack_cannot_improve_score` | host |
| 2 | Expected values readable from the candidate | no reference data in the Sandbox image | `test_secrecy.*`, `test_boundary.HostBoundaryExposure` | host |
| 3 | `subprocess.run(timeout=...)` left descendants alive | Job Object kill-on-close, `ActiveProcesses == 0` | `test_process_tree` | host |
| 4 | `--pure` is not a tool boundary | versioned deny-all agent, no `--auto` | `test_generation.*`, `evidence/opencode-config.json` | host |
| 5 | Eight-body cap unenforced; incomplete batches accepted | completeness check + deterministic cap | `test_generation.CompletenessTests` | host |
| 6 | Gate/Runbook ordering conflict | split stop conditions | `V9_RUNBOOK.md` | n/a |
| 7 | Claimed Sandbox boundary was not in the execution path | explicit transport; `evaluate_authorized` refuses unverified transports | `test_backend.TransportTests` | host |
| 8 | **Interpreter path was not mapped** | `python_root` mandatory, mapped read-only, config re-parsed | `test_backend.SandboxConfigMappingTests`, `InterpreterPreflightTests` | host |
| 9 | **Agent could start before `session.json`** | agent polls with timeout; session written before launch | `test_backend.PreflightTests` | host |
| 10 | **No preflight-only path** | `--preflight` records attestation, publishes nothing | `test_backend.CommandLineTests.test_preflight_failure_is_recorded_and_publishes_nothing` | host |
| 11 | **Outbox trusted as data** | size cap, reparse-point rejection, strict schema | `test_backend.ResponseTrustTests` | host |
| 12 | **"Feature absent" was read as "hardware unsupported"** | read-only capability diagnostic; `Win32_OptionalFeature` distinguishes disabled from absent; the pre-enable classification was `BLOCKED_PRIVILEGES` | `evidence/windows_sandbox_capability.py` | host |
| 13 | **The interpreter had to exist before a Sandbox run could mean anything** | official python.org embeddable build, pinned and hash-checked against published metadata before extraction; agent and one-job host checks | `evidence/stage_python_runtime.py` | host |
| 14 | **"Blocked on privileges" is not an outcome** | one documented enable command under an approved UAC prompt, raw result committed verbatim; post-enable diagnosis `ENABLED_RESTART_PENDING`; Sandbox gates unchanged | `evidence/sandbox-enable-elevated-2026-10-28.json`, `evidence/sandbox-capability-post-enable-2026-10-28.json` | host |
| 15 | **The hardware verdict flipped when the hypervisor started** | SLAT/VMX masking recorded as `virtualization_flags_masked_by_hypervisor`; not treated as a hardware failure | `evidence/windows_sandbox_capability.py`, `evidence/sandbox-capability-post-restart-2026-10-28.json` | host |
| 16 | **A live mapping rejects renames, so no job could be published** | ordered direct write (body first, `job.json` last), idempotent verify-only staging | `tests/test_backend.py::PublishTests, StagingTests` | host |
| 17 | **The guest scratch could not take an integrity label on a mapped folder** | scratch moved to the guest's local disk; the `icacls` error is recorded in the response | `supervisor.py`, `sandbox_agent.py` | host |
| 18 | **A verified handshake silently authorized evaluation** | fail-closed gate at both entry points; hash-pinned evidence must still assert its claim; separate authorization bound to policy and status | `tests/test_gates.py`, `test_backend.ExecutionGateTests` | host |
| 19 | **The job-B failure could not be explained** | guest writes bounded lifecycle events to uniquely named files; host validates them as untrusted input and classifies the failure | `test_backend.TelemetryValidationTests`, `RendezvousDiagnosticTests` | host |

## Residual risks

1. **No isolation report and no ordering proof.** A Sandbox handshake verifies,
   but the two-token rendezvous failed: job B was never answered, so a mapping
   that exposes a later job early cannot be excluded. Every isolation probe is
   still `NOT_RUN` (`evidence/rendezvous-sandbox-2026-10-28.json`,
   `evidence/preflight-sandbox-2026-10-28.json`).
2. **Enabling the feature was a host change made under operator consent.** Foued
   approved one UAC prompt; the agent ran the documented command exactly once,
   recorded the result, and did not restart anything. Windows 10 Pro 22H2 is out
   of standard support, so the fact that the feature works on this build is
   observed, not guaranteed. ESU coverage before running untrusted generated
   code remains an operator decision.
3. **The interpreter is staged and hash-verified, but its Sandbox mapping is not
   exercised.** The host checks prove the embeddable layout can run the agent and
   one job; they do not prove the read-only mapping or mapped-folder ACL behaviour
   inside the guest.
4. **Mapped-folder guest paths and ACL behaviour are unverified.** The config sets
   `SandboxFolder` explicitly, but whether the guest sees the mapping at that path
   and whether ACL edits are rejected there must be recorded in the preflight.
5. **`<ProtectedClient>` is not emitted.** Support varies by SKU and an
   unsupported element can stop the Sandbox from starting; it is a documented
   manual hardening step, not something V9 can assert.
6. **The host-local transport can read the oracle**, by design and by
   measurement. Rows it produces carry `authorized: false`.
7. **Process and memory caps are configured but not adversarially stress-tested.**
   One fixture job confirmed the Job Object path under the staged interpreter.
8. **No verdict layer.** `k`, `C`, `max_f`, eligibility and saturation exist;
   support-cell classification and PASS/WEAK/FAIL do not, and must be committed
   and hashed before generation.
9. **Throughput is unmeasured.** One Sandbox at a time and slow cold starts may
   make a 400-batch schedule impractical if a fresh Sandbox per item is required.

## Test evidence

```
python -m unittest discover -s tests -v
Ran 167 tests in 121.690s
OK
```

Full log: `tests/unit-test-log.txt`. Manifest: `MANIFEST.json`
(`python make_manifest.py --check` → `manifest OK`).

## Generation access, measured

`opencode-cli.exe` v2.2.0, probed without a model call: all three frozen model IDs
are present and `h3-generator` resolves with no permission leak under
last-match-wins resolution (`evidence/opencode-config.json`). This does not
establish that inference succeeds under the required no-tools profile.
