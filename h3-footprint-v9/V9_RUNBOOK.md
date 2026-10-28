# V9 runbook

Revision 3. Every command below exists and is exercised by the test suite.

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

## Step 1: stage the Sandbox image (host)

The Sandbox base image has **no Python**. The interpreter must be a portable /
embeddable distribution, not a normal install and not a virtualenv: a venv keeps
host absolute paths in `pyvenv.cfg`, and a normal install has no relocatable
`python3xx.zip`. The controller rejects both by construction.

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

```
python controller.py --rendezvous --transport sandbox ^
  --inbox C:\v9-stage\in --outbox C:\v9-stage\out ^
  --report C:\v9-stage\rendezvous-log.json
```

The harness publishes token A, requires the answer to be A, requires
`tree_empty: true`, then publishes token B and requires the answer to be B. It
records whether B was visible in the inbox before A completed.

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
With `--transport sandbox` it requires a completed handshake before executing
anything, and the supervisor's response must attest `inside_sandbox: true`.

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
