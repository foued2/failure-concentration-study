# H3 footprint V9: secure measurement boundary

Status: **implementation branch, not frozen, no candidate generation or
evaluation authorized.** See `STATUS.json` for per-gate status.

V9 exists because the frozen V8 harness had evaluator and sampling-control
defects that no amount of Sandbox testing would fix (see
`../h3-footprint-v8/POSTFREEZE_AUDIT_2026-10-27.md`). V8 itself is untouched:
this directory is additive, and `h3-footprint-v8-freeze-2026-10-27` still
points at `d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff`.

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
controller.py       HOST ONLY: one job at a time, verification, scoring, CLI
backend.py          HOST ONLY: transports, handshake, .wsb config
supervisor.py       Sandbox: secret-free, owns the Job Object
sandbox_agent.py    Sandbox: one-item broker; refuses to start outside Sandbox
child_runner.py     untrusted child: low integrity, prints a raw answer
winjob.py           Job Object bindings + token-derived identity
protocol.py         atomic job/response records, ACL lock helpers
generation/         enforced no-tools agent + strictly gated generator
tests/              regression suite and hand-authored fixtures
```

## Quick start (host, no model calls)

```
python -m unittest discover -s tests -v
python make_manifest.py --check
python controller.py --verify-boundary
```

`--verify-boundary` exits 2 on an ordinary host: that is the correct result and
the reason evaluation is blocked.

Evaluate only through the Sandbox:

```
python controller.py --write-sandbox-config runs/v9.wsb --inbox C:\h3-in --outbox C:\h3-out
python controller.py --bodies <staging> --transport sandbox --inbox C:\h3-in --outbox C:\h3-out
```

The Sandbox image ships no Python; stage a portable interpreter into the
read-only mapping (see `V9_RUNBOOK.md`).

## What is not done yet

- No Windows Sandbox isolation report has been produced (`NOT_RUN`).
- The live mapped-folder rendezvous has not been tested (`NOT_RUN`).
- The handshake *acceptance* path has not run; only rejections are tested.
- Memory and process-count caps are configured but not stress-tested (`PARTIAL`).
- Support-cell classification and the PASS/WEAK/FAIL verdict are not ported.
- Generation is not implemented. `V9_AUTHORIZE_GENERATION=1` enables nothing.
- No candidate has been generated or evaluated.
