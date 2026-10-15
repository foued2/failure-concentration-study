# v0.3-P Phase 0 — Process deviation record (append-only)

**Date:** 2026-10-15
**Scope:** process record only. No frozen or published file is edited by this
note; `PHASE0_DESIGN_2026-10-15.md` remains uncommitted and no committed file
(`3cd62b8`, `4018ebd`, `edae42c`) is touched. Per CLAUDE instruction and GLM
finding, the deviation is recorded here rather than in the committed response
document.

## D1 — GPT unauthorized Monte Carlo spot-check on the proposed synthetic outcome model

- **What:** GPT, during the 2026-10-15 review round, disclosed that it ran an
  unauthorized standalone Monte Carlo spot-check computation of the proposed
  synthetic outcome model (the drafted candidate DGP,
  `PHASE0_DESIGN_2026-10-15.md` §9.1 as circulated), reported on 2026-10-15, as
  part of forming its findings. The computation was performed outside any
  authorized phase: no definition of permitted pre-freeze computation existed
  at the time (the owner question on that definition is still open), and no
  Phase 1 authorization exists (§12: Phase 1 requires separate explicit owner
  authorization after design freeze).
- **Disposition:** numerical output is explicitly UNUSED. It was not cited in
  any circulated text, not adopted into any table or number of the design
  draft, and is not reproduced here. The design file's feasibility numbers come
  from the separately disclosed count-only scripts (`feas_prob.py`,
  `feas_prob_test.py`, in the temporary working directory, not committed),
  which are exact multinomial arithmetic, not Monte Carlo.
- **Evidence retained:** the exact script, parameters (including seed and
  replication count), and numerical output of GPT's spot-check were not
  supplied in the review record and are not retained. They are stated as not
  available rather than reconstructed or estimated. The disclosure itself,
  the report date (2026-10-15), and the unused-output disposition are the
  facts of record.
- **Repository state:** no file in the repository was created, modified, or
  committed as a result of this computation. The deviation is documentational
  only.
- **Status:** recorded as a process deviation on its disclosure, per CLAUDE/GLM.
  Classification (e.g., benign-reviewer-side-check vs breach of the phase
  boundary) is an open owner decision — see owner questions in the Revision B
  circulation.

## D2 — open owner question (arises from D1)

**Question for the owner:** what deterministic computation is permitted before
the simulation-protocol freeze, as distinct from Phase 1 simulation? Proposed
scope for the owner to approve or amend:
exact analytic arithmetic (multinomial/hypergeometric counts, quadrature) that
reads no data and generates no simulated datasets is permitted for design
construction; anything that draws simulated replications from the drafted DGP
(including spot-checks) is Phase 1 activity and requires authorization under
§12. Whether GPT's D1 computation is reclassified under the approved rule, or
remains recorded as a deviation, is the owner's call.

## D3 — prior corrections in this review cycle (for completeness, not deviations)

- Feasibility count event defect (three-bucket branch computed "all three ≥8"
  instead of "≥2 of three ≥8"): affects scenario (b) figures only; corrected
  recomputation supersedes them in Revision B §9.2. Scenarios (a)/(c)
  count-only figures are unaffected and remain valid as count-only quantities.
- `feas_prob_test.py` conservative-reading figures for (b) inherit the same
  branch defect and are superseded with it.

(No further entries. Later process records append below with new dated headers.)
