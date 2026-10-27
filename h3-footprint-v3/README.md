# H3 Footprint Gate V3 Harness

This folder is an isolated engineering revision of the invalid version-1 footprint gate. It is not the version-1 frozen artifact set and must never be copied over h3-footprint/.

Version 1 remains preserved on its original tag and audit branch. The version-1 run is INVALID_RUN because its extractor discarded module-level imports and its worker converted module-load errors into 30 failed probes.

Version 2 is frozen but unrun. It repaired extraction, separated module-load validity from probe outcomes, checked unresolved global names, grouped candidate bodies by generation batch, and added planted-bug controls. Version 3 keeps those repairs and replaces the confounded V1/V2 degeneracy statistic with a saturation rate, and adds a predeclared futility rule at batches 100/200/300.

## Local no-model-call validation

From this folder, run:

    python -m unittest discover -s tests -v
    python validate_controls.py
    python freeze.py --verify

These commands do not call any models or generate candidate bodies. They check oracle agreement, extraction, static validation, load-versus-probe classification, known-k planted bugs, unique provenance groups, saturation-based degeneracy, futility checkpoints, and report group counting.

## Candidate generation is a separate step

No candidate generation has been run for V3. Only after the pre-candidate FREEZE.json, the annotated tag, and isolation-report.json exist may generation be considered under the existing bounded footprint-only authorization. Use the approved isolated environment; do not run generated candidates on the development host. A static import/call denylist is not sufficient isolation. Set OPENCODE_EXE in the authorized generation environment if opencode is not on PATH.

The fixed V3 cap is 400 batches by 8 requested bodies, run in 100-batch segments. After each segment, run run_gate.py and stop if futility triggered. The generator schedule and prompt variants are fixed; no outcome-guided prompt changes are allowed. The 150 rejected-body target is reported, not used to alter the budget or the thresholds.

Held-out inputs, held-out scoring, model comparison, power estimation, and changes to the existing review branches remain outside scope.
