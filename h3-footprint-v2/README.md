# H3 Footprint Gate V2 Harness

This folder is an isolated engineering revision of the invalid version-1 footprint gate. It is not the version-1 frozen artifact set and must never be copied over h3-footprint/.

Version 1 remains preserved on its original tag and audit branch. The version-1 run is INVALID_RUN because its extractor discarded module-level imports and its worker converted module-load errors into 30 failed probes.

Version 2 preserves complete Python code blocks, separates module-load validity from probe outcomes, checks unresolved global names, groups candidate bodies by generation batch, and tests the pipeline against one correct reference plus eight planted-bug controls with precomputed expected counts.

## Local no-model-call validation

From this folder, run:

    python -m unittest discover -s tests -v
    python validate_controls.py

These commands do not call any models or generate candidate bodies. They check oracle agreement, extraction, static validation, load-versus-probe classification, known-k planted bugs, unique provenance groups, and report group counting.

## Candidate generation is a separate step

No candidate generation has been run for V2. Only after the pre-candidate FREEZE.json and annotated tag exist may generation be considered under the existing bounded footprint-only authorization. Use the approved isolated environment; do not run generated candidates on the development host. Set OPENCODE_EXE in the authorized generation environment if opencode is not on PATH.

The fixed V2 cap is 400 batches by 8 requested bodies. The generator schedule and prompt variants are fixed; no outcome-guided prompt changes are allowed. The 150 rejected-body target is reported, not used to alter the budget or the thresholds.

Held-out inputs, held-out scoring, model comparison, power estimation, and changes to the existing review branches remain outside scope.
