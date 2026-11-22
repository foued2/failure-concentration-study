# failure-concentration-study

Research question: does largest-family failure share (concentration, `C`) improve
prediction of solver correctness beyond failure count (`k`)?

## The programme has two different estimands — do not merge them

- **Natural-solver v0.2 (executed):** the frozen comparison was **C beyond k alone** (no
  context covariates). It terminated NEGATIVE under its frozen rule and was
  non-identifying for concentration (see §1).
- **Programme-level / LC518 target (designed, never executed):** **C beyond k and context
  Z** (`CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` §1.2: baseline predicts score from
  `k` and `Z`; augmented adds `C`). The LC518 E3 baseline additionally includes
  `k_unresolved` and parent family. The frozen LC518 analysis spec v1.0 contains **no
  `C_D` arm**; review-only revision 2.6 proposes one. **No stored study has tested C
  beyond k-and-Z.**

Pre-registration scope: the v0.1 protocol was frozen as `v0.1-freeze` (`PROTOCOL.md`,
`FREEZE.md`); the v0.2 protocol hash `99a7f7f0…` was recorded in `v02/FREEZE_V02.md`
before pack generation. Later research lines are design/pilot documents, not
pre-registered confirmatory protocols.

Clean-room statement (recorded assertion from the original README; no contrary record
found in the 2026-11-05 audit searches): no code, data, or artifacts from
`Euler_Project/new-doctor` (terminated CRS archive) or `doctor-workspace-recovered`
(read-only historical state).

**The original concentration hypothesis is unresolved.** No stored study establishes or
refutes incremental predictive value of C beyond k, or beyond k and Z.

## Status overview — what was planned, generated, executed, measured, established

### 1. Natural-solver studies — TERMINAL

- `pilot/` — v0.1 (protocol v2, frozen as `v0.1-freeze`): executed; terminal outcome
  **INFEASIBLE** at the pilot feasibility gate (2026-10-11; yield 4/20 vs ≥15 required on
  all three instances). Stopped per pre-registered §9/§11.
- `v02/` — v0.2: completed **NEGATIVE** under its frozen decision rule (2026-10-12);
  estimand: **C beyond k alone**. Interpretability limitation (record): every eligible
  observation had C = 5/k — C was aliased with k on the eligible support — and only ten
  distinct eligible base bodies existed, so the realized predictor comparison could not
  identify an independent concentration contribution. The reported interval is
  computationally reproducible, but its statistical coverage is not established. The
  general predictive hypothesis remains neither established nor refuted.

### 2. Subsequent mathematical, feasibility and construction research — no positive predictive result

- `rlc0/` — formal-localization track; closed with a bounded negative conclusion
  (full-domain CBMC certification not demonstrated). Not a concentration test.
- `engineered-study/` — Gate 1 closed **CONSTRUCTION AUDIT FAILED** before any study
  solver was generated (0 solvers). C was not identified separately from carrier family
  or defect identity in that design.
- `engineered-study/math/` — three-world simulation: frozen result **W1 FAILED**; W2
  unidentifiable (C constant on eligible support); W3 a null check. Stratum-specific
  contrasts are descriptive only.
- H3 footprint (`h3-footprint-*`) — **no completed or confirmatory H3 result exists.**
  Designs V2–V8 are frozen but were never run (a post-freeze audit found evaluator and
  sampling defects in V8); V9 is not frozen and authorizes nothing. Partial exploratory
  screens do exist: a Copilot-Auto screen produced 0 eligible bodies from 9 unique
  solvers, and a GLM screen produced 1 eligible body (k=9, C=4/9, 21/30 correct; 0
  supported cells because m_min=4). Neither is a test of H3.
- `natural-feasibility-pilot/`, `next-task/` — offline inventories: 14 protocol-eligible
  k≥2 bodies across retained natural data, zero same-k different-C pairs.

These are design, pilot, mathematical, analytical and infrastructure records. They are
not evidence that the concentration hypothesis is resolved in either direction.

### 3. LC518-150 construction study — banks generated; NO solver experiment executed

- Diagnostic bank (64 records) and held-out bank (80 records) were **generated and
  structurally verified** (canonical disjointness, independently reproduced oracle
  answers, int32 guard). Banks and oracle outputs are **publicly exposed through the
  12-file publication ZIP at `origin/foued2-patch-1`**, which also contains two
  neutral-name executable copies; the sanitized repack that removed them exists only on
  a local containment branch (not pushed), and the original Actions artifact is
  401-gated. The original artifact was subsequently retrieved through authenticated
  access (2026-11-05): its run manifest records the executed generator and launcher
  hashes, both matching the published bytes (inventory §6; matrix L34–L35). Runner-image
  identity for that run remains an open discrepancy (matrix L10).
- **No LC518 solver bodies have been constructed: 0/150.** No LC518 candidate outcomes
  and no predictive analyses exist.
- The exposed held-out bank is suitable for **development and debugging only** — it
  cannot serve as a sealed confirmatory evaluation set.
- Frozen analysis design: v1.0 (`lc518-150/glm-handoff/ANALYSIS_SPEC.md`) defines E3 as
  a baseline-versus-enriched-profile comparison (baseline `k_fail`, `k_unresolved`,
  family) and contains **no `C_D` concentration feature**. Review-only revision 2.6
  proposes a separate three-model structure with a `C_D` arm; it is not the design of
  record.
- Two distinct revision-2.6 documents exist and must not be merged:
  - **C9 generation specification rev 2.6** (`lc518-150/review-v1.2/analysis-revision-2026-11-02/C9_GENERATION_SPEC_REVIEW.md`) — its exact source was owner-ratified for bank generation (`LC518-GO-2026-11-03-01`; banks generated under it). The source header's "pending ratification" wording is **stale**, superseded by the 2026-11-03 owner act recorded in `OWNER_GO_RECORD.md` and in the execution protocol's `design_of_record` block.
  - **Analysis specification rev 2.6** (`ANALYSIS_SPEC_REVIEW_DRAFT.md`, same directory) — still a **review-only draft**, not the frozen analysis design; frozen v1.0 remains the design of record.

## Where to look

- `REPOSITORY_STORAGE_INVENTORY_2026-11-05.md` — what this repository stores, where
  (branch/commit/archive member), hashes where established, exposure class, exact ref
  census (Appendix A), and the claim-status vocabulary.
- `CLAIM_AUDIT_MATRIX_2026-11-05.csv` — 77 sourced claims with evidence pointers and
  explicit non-support notes.
- `reviews/analytical-validity-2026-11-18/B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md` — owner acceptance of the 78-record B1 documentary identity chain, with historical row numbering, H6 aggregation, unresolved handling, outcome coding, and execution explicitly left open.
- `reviews/analytical-validity-2026-11-18/B1_78_IDENTITY_AUDIT_2026-11-21_v3.md` — byte-level reconstruction and audit of the 78 canonical identities.
- `reviews/analytical-validity-2026-11-18/B1_78_CANONICAL_ID_MANIFEST_2026-11-21_v3.csv` and `B1_78_CANONICAL_ID_MANIFEST_2026-11-21_v3.json` — derived identity manifests; join by `canonical_id`, not reporting index.
