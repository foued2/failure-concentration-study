# V9 security and measurement report

**Date:** 2026-10-28 (revision 3)
**Branch:** `dev/h3-footprint-v9-implementation-2026-10-28`
**Status:** implementation; not frozen; **no candidate generation or evaluation authorized.**

Revision 3 repairs the two operational blockers found in review of revision 2
and adds the workflow and validation needed for a real Sandbox session. It does
**not** contain a Sandbox result: Windows Sandbox is not installed on this host
(`evidence/sandbox-unavailable-2026-10-28.json`).

## Evidence is split by where it was produced

| Scope | What it proves | Files |
|---|---|---|
| **Host** | configs are launchable and bounded, the handshake predicates reject what they must, the response channel is validated, the harness itself works | `tests/unit-test-log.txt`, `evidence/preflight-attempt-2026-10-28.json` |
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

## Residual risks

1. **No Windows Sandbox run exists.** Windows Sandbox is not installed on this
   host; every Sandbox gate is `NOT_RUN`. See
   `evidence/sandbox-unavailable-2026-10-28.json`.
2. **The interpreter must be staged by the operator.** V9 cannot fetch or verify a
   portable Python distribution without network access; the check only rejects
   obviously non-portable layouts.
3. **Mapped-folder guest paths and ACL behaviour are unverified.** The config sets
   `SandboxFolder` explicitly, but whether the guest sees the mapping at that path
   and whether ACL edits are rejected there must be recorded in the preflight.
4. **`<ProtectedClient>` is not emitted.** Support varies by SKU and an
   unsupported element can stop the Sandbox from starting; it is a documented
   manual hardening step, not something V9 can assert.
5. **The host-local transport can read the oracle**, by design and by
   measurement. Rows it produces carry `authorized: false`.
6. **Process and memory caps are configured but not stress-tested.**
7. **No verdict layer.** `k`, `C`, `max_f`, eligibility and saturation exist;
   support-cell classification and PASS/WEAK/FAIL do not, and must be committed
   and hashed before generation.
8. **Throughput is unmeasured.** One Sandbox at a time and slow cold starts may
   make a 400-batch schedule impractical if a fresh Sandbox per item is required.

## Test evidence

```
python -m unittest discover -s tests -v
Ran 88 tests in 121.097s
OK
```

Full log: `tests/unit-test-log.txt`. Manifest: `MANIFEST.json`
(`python make_manifest.py --check` → `manifest OK`).

## Generation access, measured

`opencode-cli.exe` v2.2.0, probed without a model call: all three frozen model IDs
are present and `h3-generator` resolves with no permission leak under
last-match-wins resolution (`evidence/opencode-config.json`). This does not
establish that inference succeeds under the required no-tools profile.
