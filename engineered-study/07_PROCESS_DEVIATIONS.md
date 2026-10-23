# Process deviations

Status: factual log. The original Gate 1 verdict was **HOLD**; the authorized
bounded construction audit subsequently closed it for this operationalization.
See `08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`.

## 2026-10-23: Option B audit produced before a recorded authorization

### Context

A limited Option B identification audit was recommended in the review
discussion. The recommendation described design and offline analysis only, with
no generator prompts, study solvers, allocation packets, generation calls, or
new power simulation.

### Deviation

`06_OPTION_B_IDENTIFICATION_AUDIT.md` was produced before an explicit Foued
authorization decision was recorded. The note was created after the audit was
recommended, but it was not retroactively authorized. This is logged as a
process deviation.

### Scope actually executed

- Read existing banks, profiles, controls, and results.
- Recomputed equal-family scores from existing per-control rows.
- Probed simple text predicates against the existing diagnostic and evaluation
  banks.
- Wrote the design-level audit note.
- Wrote no solver, prompt, allocation packet, or generation request.
- Ran no model call, generation call, Windows Sandbox control run, or new power
  simulation.
- Did not change frozen banks, README, the Gate 1 report, or any closed run.

### Scientific effect

The deviation does not invalidate the arithmetic or the source evidence. The
audit remains incomplete and does not satisfy the construction-audit criterion:
no pair of independently built mechanisms was demonstrated. Its negative finding
is evidence about the current operationalization, not proof that H1a is false.

### Corrective action

The authorized bounded audit was subsequently completed; its negative result is
recorded in `08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`. No scoring decision,
budget change, new allocation design, or generation is authorized by that
result. The earlier note is retained as a design/provenance record and must not
be treated as the authorized audit report.

## 2026-10-23: `selected_profiles.json` historical hash unresolved

The current file is semantically consistent with the selected targets, but its
recorded historical SHA-256 has not been recovered. CRLF-to-LF normalization and
a 24-variant reserialization check did not reproduce the historical hash. The
old byte identity must not be claimed as recovered.

A canonical version may be re-frozen later, with the mismatch documented. That
would establish a new provenance baseline; it would not establish that the old
bytes were recovered.
