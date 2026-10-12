# RLC-0 PROCEDURE (DRAFT — NOT FROZEN)

Status: DRAFT. Steps B0-B6 and C1-C5 execute only in the order written. All artifacts go under `rlc0/work/` (git-ignored); curated evidence is copied into `rlc0/evidence/` at C5. This file is frozen with the rest of Phase A.

## B0. Toolchain verification (no seeds)

1. Record `cl.exe` full version banner and path (from the VS developer environment), `cbmc --version`, `goto-cl` presence.
2. Non-seed smoke test: a trivial C++17 program with a std::vector call (linear search, unrelated to binary search) compiled two ways: (a) cl.exe natively, executed, exit code checked; (b) goto-cl /c to a goto object, then cbmc with the frozen flags (unwind 4, unwinding assertions, bounds, pointer checks) on a trivial main. Both must succeed.
3. If either smoke test fails: stop and report the blocker. Do not substitute tools.

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

- Compile seed + frozen harness model (see spec.json tier3_cbmc.harness_model) with goto-cl /c using MSVC headers.
- Per seed, three invocations with the frozen flags: in_f_failure_search, d_f_proof, full_d_proof (the last only claimed for seed 1's NO_FAILURE path; run for all seeds for uniformity).
- Enforce 1800 s wall / 8 GB per invocation. Record exit status, property results, unwinding-assertion status, time, and memory.
- Counterexample traces are saved; the concrete assignment (nums, target) is extracted as the witness and replayed through the B3 harness to confirm the failure independently of CBMC.
- Completeness is judged strictly by spec.json tier3_cbmc.completeness_criteria; any failed criterion yields "incomplete".

## B5. Canary validation (still no seeds)

- Build a canary program set: one correct linear search and one deliberately broken "always return -1" function (neither is a seed).
- Run the full pipeline (B1-B4 machinery) on the canaries: the correct one must yield NO_FAILURE-path evidence; the broken one must yield REFUTED with a D-minus-F witness. Any plumbing failure stops the study before Phase C.

## B6. Freeze gate

- Write FREEZE.md: SHA-256 of every file in rlc0/ except work/, exact tool versions and paths, exact compile/verify command lines, date, git commit hash.
- Path-scoped commit of rlc0/ (git -c user.name=foued2 -c user.email=116307732+foued2@users.noreply.github.com commit -m ... -- rlc0/).
- Create and push tag rlc0-freeze; record the tag commit hash in FREEZE.md and in the session report.
- Only after the freeze gate is Phase C authorized.

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
