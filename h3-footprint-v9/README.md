# H3 footprint V9: secure measurement boundary

Status: **implementation branch, not frozen, no candidate generation or
evaluation authorized.** See `STATUS.json` for per-gate status.

V9 exists because the frozen V8 harness had evaluator and sampling-control
defects that no amount of Sandbox testing would fix (see
`../h3-footprint-v8/POSTFREEZE_AUDIT_2026-10-27.md`). V8 itself is untouched:
this directory is additive, and `h3-footprint-v8-freeze-2026-10-27` still
points at `d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff`.

## The one design change that matters

V8 let candidate code run inside the same Python process as the trusted worker,
with the answer key mounted read-only beside it. Read-only is not secret, and a
function reference in a shared interpreter is not a boundary.

V9 splits the two roles:

| Component | Runs where | Holds reference data |
|---|---|---|
| `controller.py` | host | **yes** — answers, probe bank, families, scoring |
| `supervisor.py` | Sandbox | no |
| `child_runner.py` | Sandbox, untrusted child | no |
| `oracle.py` | host only | **yes** |

The Sandbox image (`sandbox-runtime/`) is built from four files and contains no
answers, no probe bank, no family labels and no scoring code. The host sends one
body and one probe input at a time, receives a raw value, and does the
comparison itself. A forged response can therefore only be a wrong answer.

## Layout

```
constants.py       frozen scientific constants (unchanged from V8)
oracle.py          HOST ONLY: 30 probes, expected answers, k/C scoring
controller.py      HOST ONLY: publishes one job, verifies, scores
supervisor.py      Sandbox: secret-free, owns the Job Object
child_runner.py    untrusted child: imports the candidate, prints raw answer
winjob.py          Windows Job Object binding (kill-on-close, caps)
protocol.py        atomic job/response records, ACL lock helpers
generation/        enforced no-tools agent + capped, gated generator
tests/             regression suite and hand-authored fixtures
```

## Quick start

```
python -m unittest discover -s tests -v
```

Generation controls (no model call):

```
python generation/generate_v9.py --verify-config --opencode <path-to-opencode-cli>
```

`--batches` is refused unless `V9_AUTHORIZE_GENERATION=1`, which this
implementation never sets.

## What is not done yet

- No Windows Sandbox isolation report has been produced.
- The live mapped-folder rendezvous has not been tested.
- Memory and process-count caps are configured but not adversarially tested.
- Support-cell classification and the PASS/WEAK/FAIL verdict are not ported.
- No generation batch has run; no candidate has been evaluated.
