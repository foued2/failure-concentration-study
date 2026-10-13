# RLC-0 PROCEDURE (DRAFT — NOT FROZEN)

Status: DRAFT. Steps B0-B6 and C1-C5 execute only in the order written. All artifacts go under `rlc0/work/` (git-ignored); curated evidence is copied into `rlc0/evidence/` at C5. This file is frozen with the rest of Phase A.

## B0. Toolchain verification (no seeds)

1. Record `cl.exe` full version banner and path (from the VS developer environment), `link.exe` version, `%VCToolsVersion%`, `%WindowsSdkDir%`, `%WindowsSDKVersion%`, `cbmc --version`, `goto-cl` presence, and the winget pin (Microsoft.VisualStudio.BuildTools 18.10.2, installer sha256 5be7256f...).
2. Prove the model shadows the system `<vector>` on the CBMC path: `cl /nologo /std:c++17 /EP /I<repo>\rlc0\model <canary>.cpp` and confirm the model marker (`rlc0_size_t`) is present and the MSVC STL marker (`integral_constant`) is absent. Re-check whenever the header or include order changes.
3. Non-seed smoke through the model route (frozen commands, default output naming; goto-colon `/Fe:`/`/Fo:` forms are forbidden — they silently produce nothing): canary A (correct linear search) must give CBMC VERIFICATION SUCCESSFUL with the model index assertion SUCCESS; canary B (`v[v.size()]` with backing buffer in bounds) must give VERIFICATION FAILED on `rlc0 model vector: index out of range`. Native cl build of canary A must also pass. Expected canary results are recorded in FREEZE.md; deviation stops the study.
4. The model header must declare `__CPROVER_assert` as `extern "C"` (C++ mangling otherwise yields `no body for callee`); `__CPROVER__` is predefined by goto-cl. Any header change re-triggers step 3.
5. If either smoke test fails: stop and report the blocker. Do not substitute tools.
6. If the goto-cl + CBMC smoke test fails against the pinned MSVC release, any fallback to a different toolchain configuration requires a dated addendum written BEFORE the switch, recording the failure output and the reason; the chosen configuration is then written into the freeze record. No silent switching.

## B0.5. Model-versus-real validation (pre-freeze, review condition 1)

- Build one operation-coverage canary driver twice natively with cl: (a) against the real MSVC STL, (b) against `rlc0/model/vector`. The driver exercises every vector operation the seeds use (default construction, `size()`, `operator[]` const and non-const) on defined, in-bounds executions over the frozen Tier 1 and Tier 2 case sets plus the frozen witnesses.
- Both builds must produce byte-identical outputs (return values, no crashes, termination). Any disagreement stops the study; the model may not be used for certificates until resolved and re-approved.
- The bounds assertion is excluded from ordinary-behavior comparison: it is the verification monitor for the study's memory-safety failure category, validated separately by canary B (B0 step 3).
- Result evidence (per-case agreement table summary + exact commands) goes into FREEZE.md. This step is required BEFORE the final freeze; the freeze candidate prepared now must carry it as an open condition.

## B1. Reference oracle (two independent implementations)

- Oracle A: C++17, compiled with cl.exe; straightforward specification: linear scan returning the index of the first exact match, else -1.
- Oracle B: Python 3 (stdlib only), bisect-based.
- Cross-check: both oracles agree on every Tier 1 case (1134) and on 200 additional fixed-seed random cases (seed 20261013). Any disagreement stops the study.

## B2. Case enumerator

- Tier 1: generate all strictly-increasing arrays, lengths 1..6, values [-3,3], crossed with targets [-4,4]. Verify the count equals 1134 (closed form). Mismatch stops the study.
- Tier 2: frozen witnesses from expected.json; boundary cases exactly as frozen in spec.json (two cases per boundary length); 200 random cases with python random.Random(20261012) and the frozen algorithm in spec.json.
- Emit the full case list to `rlc0/work/tier1.json` and `rlc0/work/tier2.json` with per-case ids. These files are hashed into the Phase C log.

## B3. Native harness (per-input execution)

- Compile each seed with cl.exe /std:c++17 /EHsc together with a driver that feeds one case at a time.
- Per input: 1000 ms timeout; record return value, oracle-expected value, wall time, crash/timeout flags.
- A mismatch, crash, safety failure, or timeout is a verified failure; the input is the witness. Witnesses are re-run once through an assertion-checked replay build (bounds checks on) to confirm.

## B4. CBMC harness (Tier 3)

- Compile seed + frozen harness (see spec.json tier3_cbmc.harness_model) with goto-cl against `rlc0/model/vector` (model route; NOT the MSVC STL, which CBMC cannot parse — ADDENDUM_2026-10-13), using default output naming.
- Before any certificate claim, audit the harness (spec.json semantic_correspondence.full_domain_harness_audit): it must represent the entire declared domain (symbolic n in [1,10000], symbolic elements with strict-increase and range constraints, symbolic target), not finite case sets; the audit is recorded in the Phase B evidence. Finite Tier 1/2 results are refutation-side only.
- Per seed, three invocations with the frozen flags: in_f_failure_search, d_f_proof, full_d_proof (the last only claimed for seed 1's NO_FAILURE path; run for all seeds for uniformity, diagnostic only on seeds 2-6 per CONTRACT section 13).
- Enforce 1800 s wall / 8 GB per invocation. Record exit status, property results, unwinding-assertion status, time, and memory.
- Counterexample traces are saved; the concrete assignment (nums, target) is extracted as the witness and replayed through the B3 harness to confirm the failure independently of CBMC.
- Completeness is judged strictly by spec.json tier3_cbmc.completeness_criteria; any failed criterion yields "incomplete".

## B5. Canary validation (still no seeds)

- Build a canary program set: one correct linear search and one deliberately broken "always return -1" function (neither is a seed).
- Run the full pipeline (B1-B4 machinery) on the canaries: the correct one must yield NO_FAILURE-path evidence; the broken one must yield REFUTED with a D-minus-F witness. Any plumbing failure stops the study before Phase C.

## B6. Freeze gate

- Write FREEZE.md as a freeze candidate first; it must capture: (a) exact model-header contents and SHA-256 plus the include-path-order proof that the model shadows real `<vector>`; (b) the exact preprocessing, goto-cl, and CBMC commands including the default-output-naming workaround and the `extern "C"` `__CPROVER_assert` requirement; (c) pinned compiler, linker, Windows SDK, CBMC versions, flags, and proof-completeness settings; (d) raw results of both canaries, distinguishing the successful positive verification from the expected failing model index assertion in the negative canary; (e) the remaining semantic-correspondence obligations (S1, S2/B0.5, S3, harness audit) and how each will be verified.
- SHA-256 of every file in rlc0/ except work/, exact tool versions and paths, exact compile/verify command lines, date, git commit hash.
- FREEZE.md must contain a "Hash recomputation" block with the exact PowerShell commands (Get-FileHash -Algorithm SHA256 per frozen file, plus the git commands to resolve the rlc0-freeze tag to its commit) so a reviewer can recompute every value independently.
- Path-scoped commit of rlc0/ (git -c user.name=foued2 -c user.email=116307732+foued2@users.noreply.github.com commit -m ... -- rlc0/).
- Conditions before the final freeze and tag: (1) B0.5 model-versus-real validation completed with agreement recorded in FREEZE.md; (2) harness domain-audit procedure defined and open as specified in B4; (3) a reviewer other than the author has recomputed every FREEZE.md hash and confirmed the rlc0-freeze tag resolves to the reviewed commit. Only then: create and push tag rlc0-freeze; record the tag commit hash in FREEZE.md and in the session report.
- Only after the freeze gate is Phase C authorized. Phase C additionally requires that the independent review above has reported agreement. Until that confirmation exists, Phase C stays unauthorized.

## C1. Single execution

- One run of B3 and B4 over all six seeds, exactly once, under the frozen configuration. No tuning, no reruns, no bound changes after the first seed result exists. Timeouts stand.

## C2. Classifier

- Produce one evidence record per seed with the frozen flags (in_f_failure_verified, outside_f_failure_verified, d_f_proof, full_d_proof).
- Labels come only from rlc0/classifier.py applied to the evidence records.

## C3. Independent checker

- A second implementation of the label rules, written directly from CONTRACT.md section 5 (not imported from classifier.py), re-derives all six labels from the same evidence records.
- The checker also recomputes the specification-correct answer for every recorded witness (native replay against Oracle A) and re-verifies domain membership of every witness.
- Any disagreement stops the study and is reported.

## C4. Report

- rlc0/REPORT.md: per-seed outcomes vs expected, witnesses, proof-completeness status, timing, tool versions, checker agreement, the complexity limitation (prominent), and the standard limitations: one problem, one language, one verification tool, one seed set; seeds cleaner than real submissions; the oracle may diverge from the platform judge; the target-present family is a human choice; behavioral localization is not causal localization and not evidence that repair is safe or effective; no evidence that certification improves repair decisions.
- The report ends with exactly: "RLC-0 is complete. No follow-up is authorized."

## C5. Evidence and close

- Copy curated evidence (case lists, per-seed evidence records, checker output, tool banners) into rlc0/evidence/.
- Path-scoped commit; tag rlc0-final; record the hash.

## Deviation rule

Any harness, tooling, or procedure defect discovered at or after C1: stop the entire study immediately, write a dated addendum rlc0/ADDENDUM_YYYY-MM-DD.md describing the defect and the stop point, commit it, and report. No silent reruns, no fixes-and-retry, no resumption without a separate decision.
