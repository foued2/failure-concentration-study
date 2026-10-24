# Process deviations

Status: factual log. The original Gate 1 verdict was **HOLD**; the bounded
construction audit selected through Foued's delegated decision subsequently
closed it for this operationalization. See
`08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`.

## 2026-10-23: Option B audit produced before the delegated decision

### Context

A limited Option B identification audit was recommended in the review
discussion. The recommendation described design and offline analysis only, with
no generator prompts, study solvers, allocation packets, generation calls, or
new power simulation.

### Authorization basis for the later construction audit

Foued instructed Claude/GPT to decide four open items. GPT selected the bounded
construction audit and described it as authorized. The conversation does not
contain a separate literal "authorize audit" reply from Foued. The later
construction audit was performed on the basis of that delegated decision. This
entry records the actual sequence and basis; it does not assert that a separate
explicit authorization message exists.

### Deviation

`06_OPTION_B_IDENTIFICATION_AUDIT.md` was produced before the delegated
construction-audit decision was recorded. The note was created after the audit
was recommended, but no separate explicit Foued authorization was recorded for
it, and it was not retroactively authorized. This is logged as a process
deviation.

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

The bounded audit selected through that delegated decision was subsequently
completed; its negative result is recorded in
`08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`. No scoring decision, budget change,
new allocation design, or generation is authorized by that result. The earlier
note is retained as a design/provenance record and must not be treated as the
later construction-audit report.

## 2026-10-23: `selected_profiles.json` historical hash unresolved

The current file is semantically consistent with the selected targets, but its
recorded historical SHA-256 has not been recovered. CRLF-to-LF normalization and
a 24-variant reserialization check did not reproduce the historical hash. The
old byte identity must not be claimed as recovered.

A canonical version may be re-frozen later, with the mismatch documented. That
would establish a new provenance baseline; it would not establish that the old
bytes were recovered.

## 2026-10-24: committed provenance manifest

`audit/PROVENANCE_SHA256.txt` now records SHA-256 values for the 57 study files,
computed from the committed Git blobs. It supersedes the local temporary
`ENGINEERED_STUDY_HASHES_NO_PYCACHE-20261023-161235.txt`, which was outside the
repository and could not be independently checked from GitHub. The manifest
omits itself from its 57 entries.
