# Sandbox diagnostic-runner integration gate

Status: frozen before implementation. This is a software integration gate only;
it does not authorize model generation or a natural-solver pilot.

## Scope

Exercise the existing 30 diagnostic probes (six fixed families, five probes
each), `study.sssp.dijkstra_ref`, and the existing `k`/`C` definition through
the current Windows Sandbox capture workflow. All fixtures are trusted,
hand-built controls. No model-written source is permitted. The evaluation bank
and expected oracle values are not made available to the worker. Each worker
call receives only its current probe input; a fresh worker process is used for
each call.

Guest output is untrusted transport. The guest supervisor may report only
bounded raw output bytes, exit/timeout state, and a run nonce. The host accepts
one exact expected transport filename in a fresh run folder, rejects links,
reparse points, non-regular files, unexpected files, invalid encoding/JSON,
duplicate or mismatched nonce, and messages above the frozen byte limit. The
host ignores all worker-supplied labels, metrics, paths, and status assertions.
The host independently reconstructs probe outcomes against the reference
oracle and computes family counts, `k`, `C` (`C=0` for `k=0`); authoritative
records are written outside the guest-writable folder only after the Sandbox
session has ended.

## Required cases and expected results

1. Reference fixture, no injected failures: 30 probes, family counts all 0,
   `k=0`, `C=0`.
2. Four selected F1 failures: `[4,0,0,0,0,0]`, `k=4`, `C=1`.
3. Two selected F1 and two selected F2 failures:
   `[2,2,0,0,0,0]`, `k=4`, `C=0.5`.
4. One selected failure each in F1-F4:
   `[1,1,1,1,0,0]`, `k=4`, `C=0.25`.
5. Timeout fixture with a child process: timeout is recorded, both worker and
   descendant are gone before capture is committed.
6. Crash/non-zero exit: recorded as an execution failure, not a pass.
7. Malformed UTF-8/JSON output and output beyond the byte cap: rejected; no
   authoritative scientific record is emitted for that call.
8. Forged worker claims (`correct`, family counts, `k`, `C`, status): ignored;
   host-computed fields match raw output and oracle.
9. Unexpected files and a real reparse-point/junction fixture: rejected
   without following the path. If the guest cannot create a junction, the host
   validator must still be exercised against a real temporary reparse point;
   inability to do either is a failed gate, not a pass.
10. A crafted oversized/malformed transport cannot modify files outside the
    designated fresh output and private host-record directories.

## Pass condition

Every required case must have an inspectable PASS result, the 4 diagnostic
patterns must traverse the actual Sandbox worker/capture path for all 30
probes, the host must independently reconstruct the expected counts, and no
model-generated code may execute. Any unavailable or skipped required case is
FAIL/NOT VERIFIED and blocks pilot execution. This gate does not claim
resistance to VM escapes or a determined guest-kernel attacker.

## Report integrity

The integration report must be derived from retained machine-readable test
records. A validator test must fail if its case count, PASS count, or any
pattern's family counts, `k`, or `C` disagree with those records. Keep this
gate and report separate from frozen v0.1/v0.2 results and natural-solver
evidence.
