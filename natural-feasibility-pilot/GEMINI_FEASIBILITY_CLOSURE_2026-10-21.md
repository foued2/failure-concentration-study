# Gemini natural-solver feasibility pilot closure

Status: **CLOSED**

- Run: `natural-pilot-gemini-20261021T172103Z`
- Provider: Google Gemini API
- Model: `gemini-3.5-flash-lite`
- Generation config: `temperature=1.0`, `maxOutputTokens=4096`
- Outcome: `FEASIBILITY_NOT_DEMONSTRATED_WITHIN_CAP`
- Generation requests: 100/100
- Generation failures: 0
- Distinct canonical bodies: 25
- Duplicate requests skipped without replacement: 75
- Complete bodies with both suites: 25/25
- Diagnostic result: 30/30 passes for every complete body
- Evaluation result: 20/20 correct for every complete body
- Diagnostic failure count: `k=0` for every complete body
- Concentration value: `C=0` for every complete body
- Eligible fixed-`k`, different-`C` contrasts: none

## Finding

Under this declared generation procedure, task, diagnostic battery, evaluation
bank, and 100-request cap, the generator did not produce the variation required
to test the concentration hypothesis. All 25 distinct bodies were perfect on
both suites, so the fixed-`k` support condition was never satisfied.

This is a generator-specific feasibility finding. It is not evidence that
failure concentration does or does not predict correctness, and no predictive
model was fitted. Distinct source code also does not establish distinct
algorithmic strategies.

The 75 duplicate requests show that the procedure repeatedly returned canonical
bodies already observed. They were retained but not executed again and were not
replaced.

## Integrity verification

`CLOSURE_VALIDATION.json` records a closure check against `INTEGRITY.json` and
the retained artifacts. The check passed:

- All manifest hashes match the retained files.
- All 100 requests used one provider, one model, and one canonical prompt hash.
- All 100 requests were generation successes and passed the source screen.
- All 25 complete bodies have 30 diagnostic records and 20 evaluation records
  in their host-authoritative directories.
- All 25 complete bodies are unique, with `k=0`, `C=0`, and 20/20 evaluation
  correctness.
- The retained result state is
  `FEASIBILITY_NOT_DEMONSTRATED_WITHIN_CAP`; no fixed-`k` contrast is present.

Raw attempt responses, generated sources, source-screen records, guest captures,
host-authoritative records, protocol, and results remain in the run directory.

## Decision

The Gemini run is closed. The prior closed pilot remains closed. Do not repeat
the same natural-solver experiment with identical settings; the relevant
feasibility outcome has already been observed within the authorized budget. A
third identical run would require a specific justification and fresh
authorization.

A separate engineered-solvers study may be considered, but it would answer a
different question. It would not establish that naturally generated solvers
exhibit the same patterns, and it should begin with its own scientific question
and protocol.

## Limitations

- The execution setup allowed a solver to inspect other inputs mounted in its
  suite session. The static source screen was a best-effort restriction, not a
  security guarantee. This does not change the observed absence of contrasts,
  but it matters for interpretation.
- The Gemini backend snapshot/version is unavailable, so no exact
  reproducibility claim is made.
- The generator population changed from the prior Codex route; no equivalence
  or pooling is claimed.

## Scope controls

No frozen study, frozen protocol, decision memo, or `README.md` was modified.
No push, merge, tag, or publication was performed. No predictive or
concentration-effect analysis was run.
