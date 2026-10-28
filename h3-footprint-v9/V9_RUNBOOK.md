# V9 runbook

Revision 2. Every command below exists and is exercised by the test suite.

**Invariant: nothing that needs model output happens before the Sandbox checks
pass.** Steps 1 and 2 make no model calls and generate no candidates.

**Generation is not implemented.** `V9_AUTHORIZE_GENERATION=1` unlocks nothing;
the generator exits non-zero with an explicit message. Do not treat this runbook
as an authorization to generate.

## Roles

- **Operator** runs the host controller, the Sandbox preflight, and the
  non-generating CLI checks.
- **Reviewer** verifies hashes, the isolation report and the effective
  permission evidence; does not run the job.

## Step 0: local integrity and configuration (host, no model calls)

```
python -m unittest discover -s tests -v
python make_manifest.py --check
python controller.py --verify-boundary
python generation/generate_v9.py --verify-config --opencode <cli>
```

Expected:

- all tests pass and `MANIFEST.json` matches;
- `--verify-boundary` prints `"inside_sandbox": false` and exits 2 on a normal
  host. That is the correct host result, and it is why evaluation is blocked.
- the config evidence shows `agent_loaded: true`, `agent_fully_denied: true`, and
  all three frozen model IDs present.

## Step 1: Sandbox preflight (Sandbox, networking disabled) — **NOT RUN**

Prerequisites to *start* this test: Step 0 passes. Nothing else. A `NOT_RUN`
Sandbox gate is not a reason to skip the test; it is the test.

Stage into `C:\h3-in` (read-only mapping):

- `supervisor.py`, `child_runner.py`, `sandbox_agent.py`, `protocol.py`,
  `winjob.py` (the five runtime files)
- a portable Python at `C:\h3-py\python.exe` — **the Sandbox base image has no
  interpreter**
- exactly one candidate body under `body.py` and one `job.json`
- `session.json` (the controller writes this during `start()`)

`C:\h3-out` is the only writable mapping. Never stage `oracle.py`,
`constants.py`, `controller.py`, `backend.py`, the repository, or other
candidates.

Generate the config and launch:

```
python controller.py --write-sandbox-config runs/v9.wsb --inbox C:\h3-in --outbox C:\h3-out
WindowsSandbox runs\v9.wsb
```

Record, from inside the Sandbox, in `isolation-report.json`:

1. the host repository and credentials are not present;
2. network egress fails;
3. a child cannot write to `C:\h3-in` or `C:\h3-out`;
4. `icacls /remove:d`, `/reset`, `/grant` and `takeown` all fail, with exit codes
   (`5` = access denied) and output recorded, not merely a nonzero status;
5. the grandchild-spawner fixture leaves no live descendant after timeout;
6. the child cannot read any reference answer (there is none to read);
7. `whoami` is `WDAGUtilityAccount` and `hello.json` echoed the nonce.

Stop unless every item is recorded.

## Step 2: rendezvous test (Sandbox, no candidates) — **NOT RUN**

Publish harmless token A, confirm the Sandbox observes it, kill the process tree,
confirm the tree is gone, then publish token B. Prove no surviving descendant
observed B before it became active.

Stop if the mapping does not reflect host updates with the required ordering.

## Step 3: generation — **NOT IMPLEMENTED / BLOCKED**

```
set V9_AUTHORIZE_GENERATION=1
python generation/generate_v9.py --batches 100
```

This currently exits non-zero with "Generation is NOT IMPLEMENTED in V9". The
batch runner has not been written. The controls that *are* implemented:

- one workspace per batch; deny-all agent; no `--auto`;
- a batch is rejected if it contains a tool event, a permission event, a
  malformed event line, a nonzero exit, or fewer than the requested eight valid
  bodies;
- surplus bodies are capped at eight in response order and recorded as overflow.

The runner must not be written until Steps 1 and 2 pass and a reviewer accepts
them.

## Step 4: evaluation (Sandbox only)

```
python controller.py --bodies <staging> --transport sandbox --inbox C:\h3-in --outbox C:\h3-out
```

The controller refuses `--transport host-local` unless `--allow-host-local` is
passed explicitly, and rows produced that way are marked `authorized: false`.
With `--transport sandbox` it requires a completed handshake before it will
execute anything.

It refuses to publish a new job unless the previous response exists and reports
`tree_empty: true`. Any `boundary_error`, `staging_mismatch` or supervisor error
aborts the run; it is never scored.

## Stop conditions

**To start a preflight test** (Step 1 or 2): stop only on a manifest mismatch, a
failing unit test, or a permission leak. `NOT_RUN` Sandbox gates are expected at
this point.

**To authorize generation or evaluation:** stop unless Steps 1 and 2 are `PASS`
with recorded evidence, the manifest matches, and the reviewer has signed off.
A `NOT_RUN`, `PARTIAL` or `NOT_IMPLEMENTED` gate blocks authorization, not
testing.

## Artifacts

Per run: `isolation-report.json`, the rendezvous log, generation `attempts.jsonl`,
per-probe response records (job id, body hash, probe index, exit status, timeout,
tree-empty, bounded stdout hash, `inside_sandbox`), and the controller's scored
rows. The report must be recomputable from these records alone.
