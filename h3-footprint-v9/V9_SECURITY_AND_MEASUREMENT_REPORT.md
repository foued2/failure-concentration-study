# V9 security and measurement report

**Date:** 2026-10-28 (revision 5)
**Branch:** `dev/h3-footprint-v9-implementation-2026-10-28`
**Status:** implementation; not frozen; **no candidate generation or evaluation authorized.**

Revision 3 repaired the two operational blockers found in review of revision 2.
Revision 4 answered the follow-up question — *can this machine run Sandbox at
all?* — and staged the interpreter the preflight needs. Revision 5 applied the
documented enable command in a session elevated through a single approved UAC
consent prompt, and records the raw result verbatim. It still contains **no
Sandbox result**: the feature is enabled but not effective until the machine is
restarted, and the agent does not restart it.

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

## Residual risks

1. **No Windows Sandbox run exists.** The optional feature is enabled but not
   effective until the host restarts (`WindowsSandbox.exe` absent,
   `HypervisorPresent` false), so every Sandbox gate is `NOT_RUN`. See
   `evidence/sandbox-capability-post-enable-2026-10-28.json` and
   `evidence/sandbox-unavailable-2026-10-28.json`.
2. **Enabling the feature was a host change made under operator consent, and it
   is not complete.** Foued approved one UAC prompt; the agent ran the documented
   command exactly once and recorded the result
   (`evidence/sandbox-enable-elevated-2026-10-28.json`). A restart is still
   required and the agent does not perform it. Windows 10 Pro 22H2 is out of
   standard support, so whether the restart makes the feature effective is only
   established by trying it, with the outcome recorded either way. ESU coverage
   before running untrusted generated code remains an operator decision.
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
Ran 88 tests in 109.057s
OK
```

Full log: `tests/unit-test-log.txt`. Manifest: `MANIFEST.json`
(`python make_manifest.py --check` → `manifest OK`).

## Generation access, measured

`opencode-cli.exe` v2.2.0, probed without a model call: all three frozen model IDs
are present and `h3-generator` resolves with no permission leak under
last-match-wins resolution (`evidence/opencode-config.json`). This does not
establish that inference succeeds under the required no-tools profile.
