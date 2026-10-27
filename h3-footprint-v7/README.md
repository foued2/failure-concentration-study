# H3 Footprint Gate V7 Harness

This folder is an isolated engineering revision of the invalid version-1 footprint gate. It is not the version-1 frozen artifact set and must never be copied over h3-footprint/.

Version 1 remains preserved on its original tag and audit branch. The version-1 run is INVALID_RUN because its extractor discarded module-level imports and its worker converted module-load errors into 30 failed probes.

Versions 2 through 6 are frozen but unrun. Version 2 repaired extraction, separated module-load validity from probe outcomes, checked unresolved global names, grouped candidate bodies by generation batch, and added planted-bug controls. Version 3 replaced the confounded V1/V2 degeneracy statistic with a saturation rate and added a predeclared futility rule at batches 100/200/300. Version 4 replaced the raw substring algorithm classifier with a conservative AST classifier. Version 5 keeps other-labelled candidates in all counts and diagnostics but excludes them from supported cells and the PASS group count, preventing a false PASS from pooling unidentified algorithms. Version 6 moves expected-value comparison and fail-flag construction from the candidate process into the parent, runs each candidate in its own scratch directory, requires a read-only harness mapping, and adds a pre-generation isolation probe plus frozen-hash verification. Version 7 closes the output-writing gap: the evaluator pre-opens its result files, applies a deny ACE to the output root while candidates run, writes and verifies results through the pre-opened handles, and requires the isolation report to live outside the output root on a read-only mount. The probe includes an explicit `io.open` control candidate that must fail to alter isolation-report and results canaries.

## Local no-model-call validation

From this folder, run:

    python -m unittest discover -s tests -v
    python validate_controls.py
    python freeze.py --verify

These commands do not call any models or generate candidate bodies. They check oracle agreement, extraction, static validation, load-versus-probe classification, known-k planted bugs, unique provenance groups, saturation-based degeneracy, futility checkpoints, conservative algorithm classification, other-category exclusion, report group counting, and the V7 output-lock boundary.

## Candidate generation is a separate step

No candidate generation has been run for V7. Only after the pre-candidate FREEZE.json, the annotated tag, and a passing read-only isolation-report.json exist may generation be considered under the existing bounded footprint-only authorization. Follow RUNBOOK.md: generate where OpenCode has network access, run the probe in a first sandbox session, export the report to read-only staging, then restart the sandbox and run the evaluator there. Do not run generated candidates on the development host. A static import/call denylist is not sufficient isolation. Set OPENCODE_EXE in the generation environment if opencode is not on PATH.

The fixed V7 cap is 400 batches by 8 requested bodies, run in 100-batch segments. After each segment, run run_gate.py inside the sandbox and stop if futility triggered. The generator schedule and prompt variants are fixed; no outcome-guided prompt changes are allowed. The 150 rejected-body target is reported, not used to alter the budget or the thresholds.

Held-out inputs, held-out scoring, model comparison, power estimation, and changes to the existing review branches remain outside scope.
