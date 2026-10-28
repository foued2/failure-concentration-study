# H3 footprint V9: secure measurement boundary

Status: **implementation branch, not frozen, no candidate generation or
evaluation authorized.** See `STATUS.json` for per-gate status and
`V9_SECURITY_AND_MEASUREMENT_REPORT.md` for the evidence split.

V9 exists because the frozen V8 harness had evaluator and sampling-control
defects that no amount of Sandbox testing would fix (see
`../h3-footprint-v8/POSTFREEZE_AUDIT_2026-10-27.md`). V8 itself is untouched:
this directory is additive, and `h3-footprint-v8-freeze-2026-10-27` still points
at `d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff`.

## The one design change that matters

V8 let candidate code run in the same Python process as the trusted worker, with
the answer key mounted read-only beside it. Read-only is not secret, and a
function reference in a shared interpreter is not a boundary.

V9 splits the two roles, and *requires* the split in the execution path:

| Component | Runs where | Holds reference data |
|---|---|---|
| `oracle.py`, `controller.py`, `backend.py` | host | **yes** (oracle, controller) |
| `supervisor.py`, `sandbox_agent.py` | Sandbox | no |
| `child_runner.py` | Sandbox, untrusted child | no |
| `winjob.py`, `protocol.py` | Sandbox | no |

`Controller.evaluate_authorized` raises `BoundaryNotEstablished` unless the
transport has a verified Windows Sandbox attestation, and then requires the
committed fail-closed gate in `gates.py`: every prerequisite gate `PASS`,
hash-pinned evidence that still asserts its claim, committed verdict rules, and a
separate `EVALUATION_AUTHORIZATION.json`. A handshake alone authorizes nothing.
The host-local transport still exists for scoring-logic tests, is explicitly not
a boundary, and marks every row `authorized: false`.

**This is measured, not assumed.** A low-integrity child on the host can read
`oracle.py` and `expected_values.json`; the `key_reader` fixture uses that to
score `k = 0`. `tests/test_boundary.py::HostBoundaryExposure` asserts that
exposure so it cannot quietly regress into a false sense of safety.

## Layout

```
constants.py        frozen scientific constants (unchanged from V8)
oracle.py           HOST ONLY: 30 probes, expected answers, k/C scoring
controller.py       HOST ONLY: one job at a time, transports, preflight, rendezvous, CLI
gates.py            HOST ONLY: fail-closed prerequisite gate for authorized evaluation
backend.py          HOST ONLY: transports, handshake, .wsb config, response trust, event validation
supervisor.py       Sandbox: secret-free, owns the Job Object
sandbox_agent.py    Sandbox: one-item broker; polls for the session, refuses to run outside Sandbox
child_runner.py     untrusted child: low integrity, prints a raw answer
winjob.py           Job Object bindings + token-derived identity
protocol.py         atomic job/response records, ACL lock helpers
generation/         enforced no-tools agent + strictly gated generator
tests/              regression suite and hand-authored fixtures
evidence/           measured host facts: capability classification, verified interpreter, preflight attempts
```

## Quick start (host, no model calls)

```
python -m unittest discover -s tests -v
python make_manifest.py --check
python controller.py --verify-boundary
python controller.py --check-execution-gate
```

`--verify-boundary` exits 2 on an ordinary host: that is the correct result and
the reason evaluation is blocked. `--check-execution-gate` exits 2 as well, and
prints every prerequisite blocker. A verified handshake is necessary but never
enough: the gate also requires hash-pinned evidence that still asserts what its
gate claims, committed verdict rules and a separate
`EVALUATION_AUTHORIZATION.json`, which this revision deliberately does not
commit.

## Sandbox workflow

First establish whether the host can run Sandbox at all:

```
python evidence/windows_sandbox_capability.py
```

On 2026-10-28 the pre-enable diagnosis was `BLOCKED_PRIVILEGES` (hardware
prerequisites met, feature present but disabled), the enable command was then run
once under an approved UAC prompt, and after the operator restarted the machine
the diagnosis is `SUPPORTED_AND_READY_TO_ENABLE`. While the hypervisor runs, the
CPU SLAT/VMX flags read false; that is masking, not a hardware change. The
command, for reference:

```
Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -All -NoRestart
```

Windows Sandbox has now run here. The preflight handshake is verified
(`evidence/preflight-sandbox-2026-10-28.json`) and the two-token rendezvous
**failed** (`evidence/rendezvous-sandbox-2026-10-28.json`): job A was answered,
job B was never answered, and the cause is unresolved. The measured mapping
behaviour is in `STATUS.json` under `sandbox_mapping_write_constraints`.

Revision 7 instruments the guest so that the next rendezvous can say *where* it
stopped. The agent writes bounded diagnostic events (`agent_start`, `heartbeat`,
`job_discovered`, `job_started`, `response_written`, `exception`) as uniquely
named files in the outbox, written directly and closed. The host validates them
as untrusted input and attaches the classification to the failing report:

| observation | classification |
| --- | --- |
| heartbeat continues, B never discovered | `inbox_not_refreshed` |
| heartbeat stops before B | `agent_stopped` |
| B discovered and started, no response | `supervisor_or_response_path` |
| B response recorded, host saw none | `response_written_but_not_visible` |
| no instrumentation even for A | `agent_not_instrumented` |
| telemetry fails validation | `ambiguous_telemetry` |

Telemetry explains a failure; it never establishes isolation, and a missing or
ambiguous diagnostic stays `unresolved`.

The base image ships no Python, so stage an **embeddable** distribution next — a
normal install or a venv keeps host paths and is rejected. The staging script
refuses to extract anything whose SHA-256 does not match python.org's published
value:

```
python evidence/stage_python_runtime.py --dest C:\v9-stage\py-embed
```

Then the preflight:

```
python controller.py --preflight ^
  --inbox C:\v9-stage\in --outbox C:\v9-stage\out ^
  --python-root C:\v9-stage\py-embed ^
  --report C:\v9-stage\preflight-attestation.json --launch
```

`--preflight` verifies the interpreter, stages the five runtime files, builds and
re-parses the `.wsb`, writes the session nonce **before** launching, verifies the
handshake, records the attestation and exits. It publishes no job and rejects
`--bodies`.

Then the ordering test and evaluation:

```
python controller.py --rendezvous --transport sandbox --inbox C:\v9-stage\in --outbox C:\v9-stage\out
python controller.py --bodies <staging> --transport sandbox --inbox C:\v9-stage\in --outbox C:\v9-stage\out
```

## What is not done yet

- **The one-item broker is not proven.** A Sandbox handshake verifies
  (`evidence/preflight-sandbox-2026-10-28.json`), but the two-token rendezvous
  failed: job A was answered, job B was published and never answered. The cause
  is unresolved; the guest was not instrumented in that run. Until an
  instrumented run explains it, no isolation report, no live ordering result and
  no authorized evaluation exist (`sandbox_rendezvous_ordering: FAIL`).
- **A live mapping constrains the host.** The host cannot `os.replace` inside a
  folder a running Sandbox maps (`WinError 32`), and the guest cannot label a
  mapped folder with an integrity level. Staging is now idempotent and job
  publication is an ordered direct write; the guest scratch lives on its local
  disk.
- The handshake *acceptance* path has only been exercised with a synthetic
  `hello.json`; the staged interpreter echoes a real nonce on the host, where
  `inside_sandbox` is correctly false.
- The staged interpreter's **Sandbox mapping** is untested: read-only behaviour,
  mapped-folder ACLs and refresh ordering are exactly what the preflight is meant
  to measure.
- Memory and process-count caps are configured and one fixture job exercises the
  Job Object path, but they are not adversarially stress-tested (`PARTIAL`).
- Support-cell classification and the PASS/WEAK/FAIL verdict are not ported, and
  must be committed and hashed before generation.
- Generation is not implemented. `V9_AUTHORIZE_GENERATION=1` enables nothing.
- No candidate has been generated or evaluated.
