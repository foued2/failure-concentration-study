# Post-freeze audit: V8 worker trust boundary and generation access

**Review date:** 2026-10-27  
**Reviewed freeze:** `h3-footprint-v8-freeze-2026-10-27`  
**Frozen commit:** `d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff`  
**Review branch:** `review/h3-footprint-v8-postfreeze-audit-2026-10-27`

This note is intentionally outside the V8 freeze manifest. V8 files, tag, and freeze remain unchanged. This branch is not a new frozen release.

## Plain-language result

Two workstreams remain open.

1. The candidate evaluator has an in-process protocol flaw. Candidate code can modify the trusted worker's response function because both run in the same Python interpreter. Low-integrity execution reduces filesystem write risk but does not protect mutable Python globals.
2. The reported loss of all free OpenCode agents is not confirmed as a platform-wide removal. Current official OpenCode documentation still lists the three model IDs frozen in the generation protocol. The real local/account availability may nevertheless be blocked by usage limits, configuration, provider/auth state, CLI age, or service failure. No model substitution is authorized by this observation.

No candidates have been generated under V2–V8. This audit supplies no H3 result.

## Finding A: candidate can replace the trusted response function

### Evidence

In `h3-footprint-v8/probe_worker.py`:

- the worker imports the candidate into the same Python process via `load(path)`;
- the trusted `_emit_answer()` function calls the module-global `_emit` by name at the time the response is sent;
- the candidate can import `sys` under the current static checks and inspect `sys.modules["__main__"]`, which refers to the worker module.

A candidate's module-level code can replace the worker module's `_emit`. The later trusted call to `_emit_answer()` then resolves the replacement. A malicious candidate can make the replacement emit one fabricated nonce-tagged response and suppress the genuine response. The existing “extra output” test catches a second line but does not establish safety against replacing the emitter and producing exactly one accepted line.

This is an evaluator-integrity / measurement-validity finding. It is not evidence that the candidate escaped the Sandbox or wrote to the host.

### Why V8's low-integrity change is insufficient

The integrity-level and output ACL controls aim to stop a candidate from writing to protected filesystem locations. This attack needs no filesystem write: it changes the Python worker's in-memory response path. A file lock cannot make an in-process Python function reference immutable.

### Design constraint for the next revision

Do not declare the issue fixed by merely moving a Python worker into a child process and then trusting arbitrary stdout from that child as proof of the `solve()` return value. A fully untrusted process controls its own stdout. The revision must explicitly specify whether the measured object is (a) the callable's return value or (b) the full black-box process output, and establish a boundary appropriate to that definition.

At minimum, the next design must:

1. include a regression candidate that replaces the emitter, suppresses the normal response, and emits exactly one forged response;
2. show that this attack cannot create a successful probe result for an incorrect `solve()` function;
3. establish which files candidate code can read, not only which files it cannot write;
4. document the threat model and the limits of any Python-level controls; and
5. pass the required real Windows Sandbox isolation probe before any candidate execution.

A static AST denylist is not a security boundary for arbitrary Python code. Do not run generated candidates against V8 while the trust issue is unresolved.

## Finding B: expected values and probe definitions are candidate-readable

This is a confirmed design defect from source inspection, not merely a missing test. The V8 runbook maps the entire harness tree into the Sandbox as read-only, including `expected_values.json` and `instrument.py`. Read-only access blocks changes; it does not block reads. The candidate is executed from a file under that same mapped staging tree. The worker imports `io` and `pathlib`; candidate code can reach them through `sys.modules` even where direct imports are denied. The existing static filter permits `io.open` and `sys.modules` access (the V8 controls themselves exercise `io.open` and `sys.modules["os"]` access).

A source-level attack path is direct: obtain `sys.modules["__main__"].__file__` to find `probe_worker.py`, use `sys.modules["pathlib"].Path` to locate the adjacent `expected_values.json`, and read it with `sys.modules["io"].open` or equivalent. The frozen instrument uses a stable probe order and probe index, so the candidate can map the current index to the key in the answer file. Because `_emit_answer()` resolves the worker module's `_emit` global dynamically, candidate code can also replace that function and write a single nonce-prefixed payload containing the reference answer. Parent-side comparison is not protection when the candidate can read the values being compared.

The current pre-generation isolation probe tests expected-value **write denial**, not **read denial**. Therefore V8 has not established that reference outputs or the diagnostic probe definitions are hidden from candidate code. Do not try to fix this with more static import/call denylist entries. Keep reference answers and any probe bank meant to be hidden outside the candidate-visible filesystem and process boundary, and test read denial in the actual Sandbox.

## Finding C: the five-second timeout does not terminate the candidate process tree

`run_gate.py::evaluate_body()` uses `subprocess.run(..., timeout=5)` separately for preflight and each probe. Python's timeout handling kills the direct subprocess; it does not by itself guarantee that child or grandchild processes launched by that subprocess are terminated. V8 candidates can reach the already-loaded `os` module through `sys.modules`; the V8 lock-removal control explicitly uses `os.system()` to launch external commands, confirming that process spawning remains reachable despite the static import filter.

A candidate can spawn a detached or long-running descendant, let the worker hit its timeout, and leave that descendant running into later probes/candidates. Its low-integrity token and the Sandbox reduce the impact but do not provide a per-candidate process-tree time bound. This can exhaust the Sandbox's memory/CPU, interfere with later evaluations, or leave processes operating on scratch locations after the parent worker is killed. The global Sandbox memory ceiling is not a substitute for killing every descendant at a per-candidate deadline.

The historical Job Object fixture work is not an implementation guarantee: the frozen V8 `evaluate_body()` call path shown above does not create, assign, or close a Windows Job Object around each worker. The next revision must enforce a process-tree kill-on-timeout (for example, by assigning a worker process and descendants to a Windows Job Object with kill-on-job-close, or an equivalently strong container boundary) and resource limits for each candidate invocation. Add a regression candidate that launches a child which outlives the parent; prove the child is gone after timeout. Run that test inside the real Sandbox as well as ordinary tests.

## Finding C: OpenCode free-agent access needs local diagnosis, not an unverified global conclusion

Checked the official documentation on 2026-10-27:

- The [OpenCode Console models page](https://dev.opencode.ai/v2/docs/console/models/) still lists `glm-5.3-flash-free`, `deepseek-v4.1-flash-free`, and `mimo-v2.6-flash-free`, alongside other free models described as available for a limited time.
- The [OpenCode Models guide](https://dev.opencode.ai/v2/docs/models/) says the selector only shows enabled models whose provider is available in the current project. It notes that `OPENCODE_DISABLE_FREE_MODELS=1` hides free models, and that provider/account availability affects what appears.
- The [OpenCode changelog](https://opencode.ai/changelog) entry for v2.1.2 (2026-10-21) describes explicit recovery behavior when free-message limits are exhausted.

These public pages do **not** prove the models work for this account and installation. They do show that the public catalog does not support the broad claim that all listed free models have been removed.

The local block should be diagnosed by recording, without launching a generation batch:

- the exact CLI executable and `opencode --version`;
- whether the frozen IDs appear in the model catalog / `/models`;
- whether `OPENCODE_DISABLE_FREE_MODELS` is set in the calling environment;
- the exact error category and reset/retry information shown by OpenCode; and
- whether the error is “model unavailable,” authentication/provider failure, free limit exhausted, timeout, or network failure.

Do not silently replace any model in the frozen sampling frame. Any replacement would require an explicitly versioned protocol change and a new statement of the population being sampled. A catalog listing alone does not authorize a batch.

## Unchanged scientific status

- V1 remains invalid for its previously recorded extraction/evaluation defect.
- V2–V8 have not run new candidate generation or candidate evaluation.
- The V8 validation report's 57 unit tests and freeze verification are harness checks, not candidate data.
- The Windows Sandbox isolation report has not been produced and passed in the actual mapped-folder configuration.
- No H3 feasibility result, effect estimate, or prediction claim is supported.

## Next work, in order

1. Redesign the trust boundary so expected values and probe definitions are outside the candidate-visible filesystem/process; add the suppression-and-forgery regression test.
2. Add explicit read-access probes for expected values, instrument, harness source, and other candidate files.
3. Add process-tree kill-on-timeout and per-candidate resource controls; prove descendants are gone after timeout.
4. Run the complete isolation probe in a real, configured Windows Sandbox and preserve its report outside the writable output mapping.
5. Separately diagnose the current OpenCode CLI/account state without generating study candidates.
6. Only after items 1–4 pass, revisit whether candidate evaluation is authorized. Only after generation access is confirmed under the frozen model IDs should any generation batch begin.
