# V9 design brief: separate candidate execution from the reference oracle

**Date:** 2026-10-27  
**Base:** immutable V8 tag `h3-footprint-v8-freeze-2026-10-27` (`d5b002cf0802b54b5a18b81e6bb99a9566cdd5ff`)  
**Status:** design specification only; V8 remains frozen and unchanged. No tests run and no candidate execution authorized.  
**Amended:** 2026-10-28, to combine the answer-key disclosure and response-forgery threat.

## 1. Objective

Repair the trust boundary before the next candidate run. The current V8 design executes generated Python inside the same interpreter as the trusted probe worker, and the whole read-only harness tree is mounted into the same Sandbox. This leaves both mutable in-process protocol state and candidate-readable reference data.

The next revision must correct the false frozen-V8 statement in GATE.md item 5 (“the worker cannot read expected values”) by recording it as an erratum without editing V8. It must treat the reference disclosure and response-forgery mechanisms as one combined threat: a candidate that can read the expected values and control the worker's in-process response channel can make an incorrect solver appear correct. The next revision must provide two separate guarantees:

1. **Containment:** executing a solver cannot change the host, repository, credentials, trusted result store, or other candidate files.
2. **Measurement integrity:** candidate-visible files and processes do not contain the reference answers or the full diagnostic-probe bank used to score the candidate. The trusted side computes failure flags and concentration only after it receives candidate outputs.

A successful isolation report for V8 would not cure the currently identified in-process/reference-data design defects. Do not run V8 candidates even if its OS-level probe later passes.

## 2. Define what is being measured

For untrusted Python, there is no Python-level way to guarantee that a value observed by a function call is the untouched return value while also allowing arbitrary code to execute in the same interpreter. A candidate can inspect and mutate Python module globals, callbacks, streams, and frames. A denylist cannot make that interpreter a trustworthy monitor.

The next protocol must therefore define an externally observable contract. Recommended contract:

- A single invocation receives one probe input.
- The candidate process's response to that input is the measured solver answer.
- The candidate does not receive the expected answer, all other diagnostic inputs, the family labels, the score state, or the reference oracle. This must be true in both the candidate's filesystem view and its process/trust domain, not merely enforced by read-only filesystem permissions.
- The trusted controller parses that response, compares it against the expected value kept in its own trust domain, and derives the failure flag. Candidate-side code must never construct the trusted `fails` vector, family counts, `k`, `C`, or verdict.
- Exceptions, timeouts, malformed responses, and non-integer/bool answers follow frozen and explicit outcome rules; they must not be silently conflated with loader/import failures.

If the study specifically needs to measure the Python callable's return value and not the externally visible response of the candidate process, then an active malicious candidate can always interfere with an in-process wrapper. In that case a stronger execution boundary (e.g., separate OS security principal / stronger VM or a dedicated trusted native monitor) is required. Do not claim a normal Python subprocess alone makes its internal return value tamper-proof.

## 3. Trust-domain split

### Trusted controller

The trusted controller, in a process and filesystem view inaccessible to candidate code, owns:

- the expected-output table;
- the authoritative six-family mapping and probe schedule;
- the mapping from each probe to expected answer;
- all candidate rows, failure booleans, family counts, eligibility and verdict computations;
- the immutable manifests and scoring logic;
- the authoritative result record.

The controller must not execute candidate code or import a candidate module. A host-side controller may safely score bounded, untrusted output data returned by the Sandbox because it does not execute that data as code.

### Candidate-visible execution environment

Candidate execution should receive only:

- the current candidate source;
- the single input being tested, through a narrow input channel;
- a minimal wrapper with no expected outputs, probe list, family names, scoring rules, or repository/harness secrets;
- an isolated scratch directory that contains no other candidates or trusted files.

The candidate-visible environment must not contain `expected_values.json`, `instrument.py`, `run_gate.py`, a full harness checkout, a hidden input bank, credentials, or the Git repository. In V8, a read-only mapping is readable by candidate code and therefore does not qualify as secret storage.

### Recommended host/Sandbox broker protocol

Use a trusted controller on the host and a secret-free execution supervisor inside Windows Sandbox. The host controller retains the complete probe bank, expected outputs, family labels, scoring code, and provenance metadata. None of those reference artifacts is mapped into the Sandbox.

For each individual probe invocation:

1. The host controller stages exactly one candidate source file and one probe input in a narrowly scoped active-job folder mapped read-only into the Sandbox. The folder contains no sibling candidate files, no other probe inputs, no expected outputs, and no score or family labels.
2. The secret-free Sandbox supervisor starts a fresh low-integrity candidate process in a dedicated Windows Job Object. A minimal wrapper imports/executes that candidate and provides only the current input. The candidate and its wrapper share an interpreter only inside this untrusted child process; the supervisor is a separate process and does not contain or import the candidate.
3. The supervisor treats the child's externally observed stdout/result as the candidate's answer. It does not try to attest that a Python-level function return was untouched. Candidate stdout is data, never an instruction or a trusted result record.
4. The Job Object enforces the deadline and memory/process limits and kills descendants before the supervisor publishes the response. The candidate runs at low integrity and cannot write to the normal-integrity, ACL-protected output mapping.
5. The supervisor writes one bounded raw-response record to the output mapping only after the candidate process tree has terminated. The host controller receives that record, compares the answer with the expected value it kept locally, and computes the failure flag.
6. Only after the host controller receives and validates the response and confirms that the previous process tree is gone does it replace the active job with the next candidate/input. The active folder must never hold multiple candidates or multiple probes at once.

**Windows Sandbox rendezvous is itself a preflight requirement.** Microsoft documents that mapped folders share host paths into Sandbox, but the project must not assume without testing that host-side updates during a live session are seen with the required timing. Add a rendezvous control that stages a unique first token, verifies it in Sandbox, waits for the candidate process tree to terminate, stages a different second token, and verifies that no long-lived process can read the second token until it is made active. If this exact live-update workflow is unreliable, stop and select an equivalent restricted VM/broker design before implementing the study runner. Do not work around failed rendezvous by mapping the full probe bank or entire candidate directory.

This protocol keeps the reference oracle outside both the candidate's filesystem view and its process/trust domain. A different process inside the same Sandbox is not treated as a secret boundary: the supervisor is intentionally secret-free, and all reference comparison remains on the host.

The host controller may parse bounded untrusted output as data but must never execute candidate output, candidate code, or a returned serialization.

## 4. Required adversarial regression tests

The next version must include negative controls for:

1. **Combined reference-disclosure plus response-forgery attack:** candidate uses `sys.modules["__main__"]`, `sys.modules["pathlib"]`, `sys.modules["io"]`, or equivalent introspection to locate and read the reference outputs, then replaces the worker emitter and attempts to produce exactly one forged nonce-prefixed response. The candidate must be unable to recover the reference values in the first place; the trusted result must be computed outside the candidate-visible process. Test this as one end-to-end exploit, not just as independent read and emitter controls.
2. **Reference-output read:** candidate searches common paths and uses permitted introspection/file APIs to read the expected-output table. The table must be absent from the candidate-visible filesystem and process; a read-only mount is insufficient.
3. **Probe-bank read:** candidate attempts to enumerate all probe inputs, family labels, and oracle mappings. Only the one current input may be made available to the candidate invocation.
4. **Other-candidate read:** candidate attempts to inspect a different candidate body or the complete generated-body directory. It must not be exposed through candidate-visible staging.
5. **Trusted-state tampering:** candidate attempts to alter trusted failure flags, family counts, result handles, and the authoritative record through `sys.modules`, frame inspection, or stream monkeypatching. The trusted controller must be in a separate process/trust domain and must compute these independently.
6. **Process-tree/resource boundary:** run each candidate invocation in a Windows Job Object (or equivalently strong mechanism) with process-tree kill-on-timeout, memory/process-count caps, and a regression that spawns a long-lived child. `subprocess.run(timeout=...)` alone does not guarantee descendants are terminated. Verify the child has exited after timeout and before the next candidate starts.
7. **Host and output boundary:** continue the existing host-write, network-block, output-root-lock-removal, low-integrity, and post-run hash checks in the actual Sandbox configuration.
8. **Reference result controls:** known wrong solvers must remain wrong on all frozen probes, correct solvers must remain correct, and malformed or timed-out candidates must follow explicitly specified classifications.

For each check, preserve the attempted action, observed result, artifact hashes, and report fields. A test that passes only under the ordinary development host does not certify the Sandbox boundary.

## 5. Minimal staged layout

Do not mount the entire repository or entire harness tree read-only. Prefer three separate locations:

- **Controller-only:** reference outputs, family/probe mapping, immutable manifests, scoring source and repository records. Never mounted into candidate-visible execution.
- **Candidate staging:** one candidate body and no other candidate/reference files.
- **Per-run output:** only the raw response for the current candidate/probe, with any trusted result write performed by a controller that candidate code cannot modify.

A Windows Sandbox mapped folder grants the guest access to that mapped tree; the mapping's read-only flag only prevents writes. If the output is mounted writable, assume candidate code could attempt writes unless the write occurs only through a separate trusted boundary. Avoid same-user ACL assumptions without testing their exact Windows semantics.

## 6. Authorization gates

No candidate execution until all of the following hold:

- design review accepts the external-response contract and trust-domain split;
- adversarial tests above are added and pass;
- frozen-artifact/hash verification passes for the new version;
- the real Windows Sandbox probe demonstrates network isolation, absent host repo/credentials, no access to reference outputs and probe bank, write isolation, process-tree/time/memory bounds, live one-item rendezvous correctness, and unaltered trusted results;
- the actual OpenCode generation route is separately diagnosed and confirmed under the frozen three-model schedule.

Generation and evaluation are separate authorizations. Solving the executor issue does not authorize model calls, and restoring model access does not authorize candidate execution.

## 7. Frozen scientific constants

Unless a later protocol revision explicitly states otherwise, preserve the existing pilot constants: six family labels with five probes each; eligible (2\leq k\leq24); maximum 400 batches of 8; three fixed model IDs and three predeclared prompt variants; futility checkpoints at 100/200/300 with at least 10/20/30 eligible provenance groups; (m_{\min}=4); PASS at three supported cells over two k values and 40 distinct groups; WEAK at one or two cells; saturation cutoff 0.80. Do not change a threshold to compensate for generation scarcity.

No new candidate data or H3 result is produced by this design note.
