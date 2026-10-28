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
transport has a verified Windows Sandbox attestation. The host-local transport
still exists for scoring-logic tests, is explicitly not a boundary, and marks
every row `authorized: false`.

**This is measured, not assumed.** A low-integrity child on the host can read
`oracle.py` and `expected_values.json`; the `key_reader` fixture uses that to
score `k = 0`. `tests/test_boundary.py::HostBoundaryExposure` asserts that
exposure so it cannot quietly regress into a false sense of safety.

## Layout

```
constants.py        frozen scientific constants (unchanged from V8)
oracle.py           HOST ONLY: 30 probes, expected answers, k/C scoring
controller.py       HOST ONLY: one job at a time, transports, preflight, rendezvous, CLI
backend.py          HOST ONLY: transports, handshake, .wsb config, response trust
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
```

`--verify-boundary` exits 2 on an ordinary host: that is the correct result and
the reason evaluation is blocked.

## Sandbox workflow

First establish whether the host can run Sandbox at all:

```
python evidence/windows_sandbox_capability.py
```

On this machine it reports `BLOCKED_PRIVILEGES`: the hardware prerequisites are
met and `Containers-DisposableClientVM` is present but **disabled**, so enabling
it needs an elevated session:

```
Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -All -NoRestart
```

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

- **Windows Sandbox has never run here.** The optional feature is present but
  disabled and cannot be enabled from this non-elevated session, so no isolation
  report, no live rendezvous and no `WDAGUtilityAccount` handshake exist
  (`NOT_RUN`). See `evidence/sandbox-capability-2026-10-28.json`.
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
