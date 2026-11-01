# failure-concentration-study

**Research question (not answered by the completed studies):** does largest-family failure share improve prediction of solver correctness beyond failure count alone, on unseen problem instances?

**Current scientific disposition:** v0.1 stopped at an **INFEASIBLE** pilot gate. v0.2 reached a formal **NEGATIVE** classification under its frozen decision rule, but its eligible support contained no equal-k/different-C comparisons: C = 5/k on all 1,200 confirmatory eligible pairs. Therefore v0.2 does **not** determine whether independently varying family concentration adds predictive information beyond k. The broader hypothesis remains unresolved, neither supported nor refuted. The evidence and limits are consolidated in [the v0.2 findings ledger](v02/FINDINGS_LEDGER_2026-10-19.md).

Clean-room repository. No code, data, or artifacts from `Euler_Project/new-doctor`
(terminated CRS archive) or `doctor-workspace-recovered` (read-only historical state).

- `PROTOCOL.md` — v2, frozen as `v0.1-freeze` (see `FREEZE.md`).
- `pilot/` — pilot executed; terminal outcome **INFEASIBLE** (yield gate failed 4/20 vs ≥15
  required on all three instances). Study stopped per pre-registered §9/§11. No continuation
  authorized.
- `v02/` — v0.2 completed **NEGATIVE under the frozen rule** (2026-10-12). This is the formal classification of the frozen comparison and threshold, not a refutation of the broader concentration hypothesis. The identifiability, model-support, execution-history, and provenance limitations are recorded in `v02/FINDINGS_LEDGER_2026-10-19.md`.

Status: v0.1 **TERMINATED — INFEASIBLE** at the pilot feasibility gate, 2026-10-11. v0.2 **TERMINAL — NEGATIVE under its frozen rule**, with the scientific scope limitation stated above. No successor study is authorized.
