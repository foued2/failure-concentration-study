# Pilot Report — TERMINAL: INFEASIBLE


## Retrospective provenance and scope correction (2026-11-21)

This dated note qualifies the population-level interpretation above; it does not alter the recorded pilot gate outcome or the historical freeze.

The repository's generation/_emit_pilot_pack.py contains 20 solver bodies as literal strings, SOLVERS["solver_01"] through SOLVERS["solver_20"]. Its main() writes those strings to generation/pilot_pack/; it contains no LLM/API invocation, sampling operation, or session capture. The generator specification names a model and describes a single generation session, but the repository does not contain independently verifiable provider/session evidence linking the retained bodies to unmodified single-shot model outputs.

This establishes that the checked-in pack was emitted deterministically from literal source-code bodies. It does not prove that the bodies could not have originated in an earlier LLM session outside the repository. Their authorship and origin therefore remain UNVERIFIED, rather than proven manual or proven model-generated.

Accordingly:

- The result INFEASIBLE remains valid for the retained 20-file corpus and its frozen eligibility gate.
- The statement that this is evidence about a population of “natural single-shot LLM SSSP implementations” is withdrawn as unsupported by the retained provenance record.
- The pilot does not establish that natural LLM-generated populations are unsuitable for this domain.
- The reported count pattern (16 files with k=0; four specified multi-failure approaches) describes this retained corpus only. It is not an estimate of the failure distribution of the named model.

See reviews/CLAUDE_FULL_REPO_CHALLENGE_ADJUDICATION_2026-11-21.md for the source and Git-history audit. No solver was regenerated or executed for this correction.

**Date:** 2026-10-11. **Protocol:** PROTOCOL.md v2 (frozen `v0.1-freeze`, `5bf80b7`).
**Executed:** per frozen protocol; no amendments; nothing changed after seeing results.

## Result

| Pilot instance (seed) | Eligible pairs | Gate (≥ 15) |
|---|---|---|
| 101 | 4 / 20 | FAIL |
| 102 | 4 / 20 | FAIL |
| 103 | 4 / 20 | FAIL |

Format failures: 0/20. Decision per §11: **INFEASIBLE — stop.** All outcomes are terminal
(§9); this is the pre-registered inconclusive branch ("too few eligible observations"),
reported as designed — a cheap, informative end, not a failure of execution.

## What the pack showed

16 of 20 single-shot LLM submissions solved all 30 probes on every instance (k = 0). The four
multi-failure submissions (unit-weight BFS, topological DP, greedy-largest-edge,
unreachable-returns-0) had k ∈ {25, 10, 5, 5} and Y = 0 on every instance. Eligible yield was
exactly 20 % against a 75 % requirement; among eligible pairs there were no Y = 1 cases, so
the predictive question could not even be posed on this pack.

## What this does and does not establish

- It does **not** establish that concentration lacks predictive value. The question was never
  reached: the study terminated at its feasibility gate.
- It establishes that a 20-submission pack of natural single-shot LLM SSSP implementations
  is the wrong instrument for generating eligible observations in this domain: near-perfect
  correctness on small diagnostic graphs leaves ~20 % multi-failure yield, and those failures
  co-occur with Y = 0 only.

## No continuation is authorized

Per §9 and the GPT/Foued ratification, no result authorizes new features, thresholds, or
follow-up studies. A redesigned pilot (e.g., a larger pack or a defect-inclusive generation
directive frozen in advance) would be a new protocol requiring fresh ratification. It has not
been started and is not recommended or opposed here — it is simply outside this study.
