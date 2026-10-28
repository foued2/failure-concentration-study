# V9 implementation work order

**Issued:** 2026-10-28  
**Base:** review branch `review/h3-footprint-v8-postfreeze-audit-2026-10-27`; immutable V8 freeze target `d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff`  
**State:** implementation requested; no V9 code or tests claimed complete by this document. No candidate generation or evaluation authorized.

## Mission

Build a versioned V9 implementation that repairs the documented V8 evaluator-integrity and generation-control defects without editing any V8 frozen artifact. The immediate target is a testable, auditable feasibility runner, not an H3 result. Keep all candidate generation/evaluation disabled until the new runner passes local unit tests, freeze checks, and an actual Windows Sandbox isolation test.

## Safe branch and file boundary

1. Fetch origin and verify the V8 annotated tag still resolves to commit `d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff`.
2. Create a fresh implementation branch named `dev/h3-footprint-v9-implementation-2026-10-28` from the current review branch. Do not switch, reset, clean, or overwrite the existing local branch `review/feasibility-protocol-2026-10-25`, including its unpushed commit.
3. Copy V8 forward into a new `h3-footprint-v9/` directory. Do not modify V8 source, V8 manifest, V8 tag, V8 validation report, or the already-published V1–V8 tags.
4. Preserve the frozen scientific constants unless a protocol owner separately authorizes a versioned change: six families x five probes; eligible (2\leq k\leq24); up to 400 batch IDs x eight accepted bodies; exact three model IDs and prompt schedule; futility 10/20/30 groups at checkpoints 100/200/300; (m_{min}=4); PASS thresholds of three supported cells across at least two k levels and 40 independent provenance groups; saturation cutoff 0.80.

## Workstream A: secure external measurement boundary

### Trusted host controller

Implement a controller that runs on the host and never executes or imports candidate code. It alone owns:

- the complete probe bank, family labels, expected outputs and oracle checks;
- candidate provenance, failure vectors, family counts, (k), (C), eligibility, saturation, support, futility and verdict computation;
- accepted candidate rows and final report;
- hashes and run-state transitions.

The reference oracle and complete probe bank must never be mapped into Windows Sandbox or passed to the candidate process. Keep the original GATE.md claim (“the worker cannot read expected values”) as a post-freeze erratum in the run record; do not edit the frozen V8 file.

### One-item active job

At any point, expose only one candidate body and one current probe input to the Sandbox. The candidate process must have no access to:

- `expected_values.json`, `instrument.py`, the complete probe bank, family mappings, scoring code, `run_gate.py`, prior candidate bodies, future probe inputs, the Git repository, or credentials;
- earlier response files or the host controller's process/state.

Read-only access is not secrecy. The current active-job directory must not contain other candidates, other probes, answers or scoring fields.

### Secret-free Sandbox supervisor

The supervisor is a separate process, contains no expected values and no full probe bank, and receives one active job. It must start the candidate in a **separate untrusted child process**, not import candidate code into the supervisor interpreter. A minimal child wrapper may import the candidate because that whole child process is untrusted; its stdout is treated as the externally observed solver response, not as a trusted protocol envelope.

For each probe:

1. Read the single active candidate/input job.
2. Create a fresh child process and assign it and all descendants to a Windows Job Object configured to kill on job close; enforce per-probe wall-clock, memory and process-count limits.
3. Capture bounded raw stdout and process status. Do not expect the child to authenticate its own result with a nonce or failure flag.
4. On timeout or failure, terminate the complete process tree and verify descendants are gone.
5. Only after the tree is gone, have the secret-free supervisor write one bounded raw-response record via a protected output channel.
6. The host controller compares this result against its private expected value, derives failure flags, and updates study state.
7. Advance the active job only after the host confirms receipt of the preceding record and completion of the preceding process tree.

The supervisor and candidate may be in the same Sandbox, but the supervisor must be secret-free. Different process IDs or low-integrity labels alone are not the oracle confidentiality boundary; the reference data remains on the host outside the candidate's filesystem view and process domain.

### Live staging rendezvous test

Before relying on a long-lived Sandbox session, test whether the mapped active-job folder reflects host updates during the session with the needed timing. Use two distinct harmless tokens. Verify that the first is seen by the Sandbox, that the candidate's process tree is terminated, and only then replace it with the second. Prove no surviving descendant can read the second token before it becomes active.

If this fails or proves ambiguous, stop. Do not map the full probe bank or all candidate files as a workaround. Use a separately reviewed restricted VM/broker arrangement that can guarantee one-item delivery and output return.

## Workstream B: regression suite

Add focused deterministic tests for all the following:

1. **Compound disclosure/forgery attack:** a candidate attempts to read an expected output via worker/module paths and then emits a forged correct response. It must have no route to reference values, and only host-side scoring determines correctness.
2. **Probe-bank secrecy:** candidate attempts to enumerate all probes/family labels or future active jobs; only the current job exists in candidate-visible staging.
3. **Other-candidate secrecy:** candidate attempts to read another candidate body or a full generated-body directory.
4. **Emitter/protocol tampering:** candidate modifies stdout, environment, module state and exit handlers. The supervisor must capture only the child process's external output, and the host must compare it as untrusted data.
5. **Process-tree timeout:** candidate spawns a long-lived child/grandchild. On timeout the Job Object kills the entire tree, a process check proves the child is gone, and the next active job is not published first.
6. **Memory and process count:** candidates that exceed each configured cap are terminated and classified according to the frozen invalid/timeout rules.
7. **Output boundary:** the candidate child cannot write/replace/delete the response record or change the output-root permissions. The supervisor publishes only after tree termination.
8. **Rendezvous ordering:** prove the second active job is not visible while the first process tree is alive. A failure stops the runner.
9. **Oracle controls:** known correct and deliberately wrong solver fixtures produce the exact expected failure counts, including all 30 failures for a constant-wrong solver. Exceptions/timeouts follow explicit frozen rules.
10. **No candidate-side scoring:** no candidate-visible code or file has the expected values, complete instrument, fail vector, (k), (C), saturation or verdict.
11. **Run reproducibility:** manifests and result records identify candidate hash, provenance group/batch, probe index, exit status, timeout status, and bounded raw output hash. The host controller can recompute the entire report from recorded raw result artifacts.
12. **Host containment:** no network, repository, profile, credentials, or unrestricted host path is exposed to the Sandbox. All relevant checks run inside the actual Sandbox configuration, not only in ordinary unit tests.

## Workstream C: generation controls

Create a dedicated OpenCode generation agent/config with a versioned permission profile. Use the documented `opencode agent create --permissions` interface where appropriate, or checked-in agent frontmatter to express the full supported permission set. Include `read`, `edit`, `glob`, `grep`, `list`, `bash`, `external_directory`, `task`, `todowrite`, `webfetch`, `websearch`, `lsp`, `skill`, `question`, `doom_loop`, and wildcard/custom tools in the effective policy as supported by the installed CLI. Never pass `--auto`.

Sanitize/pin `OPENCODE_PERMISSION`, `OPENCODE_CONFIG_CONTENT`, `OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`, and other inherited config paths. Verify the actually loaded agent and permissions without making a model call. Preserve the full JSON event stream and reject any batch with executed tool use, external file access, shell, web, task/subagent activity, or a permission-policy event.

**Free-tier compatibility caveat:** upstream reports exist of OpenCode free models rejecting certain hard-deny configurations with HTTP 403. This does not authorize enabling tools. If the fixed models reject the required no-tools profile, stop and record operational incompatibility; do not replace models or weaken permissions silently.

Enforce the output ceiling in code, not just the prompt: at most the first eight valid modules in response order are accepted per batch. Reject nonzero-exit or incomplete responses in full; never accept partial JSON text just because it contains code. Record all overflow blocks/hashes but do not count them as candidates. Use a separate working directory for each model call; do not share the V8 `generated/work` directory across concurrent calls.

## Workstream D: authorization sequence and outputs

Reconcile Gate/Runbook order so the required real Sandbox isolation test passes before model generation starts. The initial no-model-call checks should establish:

- V9 code and manifest hashes match;
- agent configuration is loaded as expected;
- CLI/model catalog and auth/provider state are recorded without generation;
- the Sandbox starts with network and clipboard disabled and no host repository/credentials;
- one-item rendezvous and output boundary controls pass;
- process-tree kill, time, memory and process-count controls pass.

Deliver these artifacts on the implementation branch:

- V9 source directory with a complete manifest and frozen constants;
- unit tests and their full logs;
- `V9_SECURITY_AND_MEASUREMENT_REPORT.md` mapping each threat to the implementing control and regression test;
- `V9_RUNBOOK.md` with exact host/Sandbox responsibilities and artifact-flow sequence;
- a signed/hashed isolation report from the actual Sandbox preflight;
- an explicit status record: `NOT_RUN`, `BLOCKED`, or `PASS` per gate.

Do **not** generate study candidates, do not evaluate any generated body, and do not run the 400-batch schedule while implementing or testing V9. Use only hand-authored adversarial fixtures with no connection to the study sampling frame. Do not tag or publish V9 as frozen until GPT's scientific/security review and the local integrity verification are both complete.

## Completion rule

V9 is not ready merely because ordinary unit tests pass. It is ready for a separate authorization review only when the trust-boundary design, all adversarial controls, the actual Sandbox rendezvous, process-tree enforcement, effective OpenCode permissions and full manifest all pass and are independently reviewable. This work order itself authorizes no candidate generation or evaluation.
