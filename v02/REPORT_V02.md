# v0.2 Final Report — Failure-Concentration Predictive Value (Directed SSSP)


## Retrospective provenance and estimand correction (2026-11-21)

This dated note corrects the scope and provenance interpretation. It does not change the frozen v0.2 decision function, its recorded NEGATIVE classification, or any historical hash.

### What the repository actually retained

The current v02/generate_pack.py defines 40 distinct solver-body strings, S[1] through S[40]. Its main() deterministically loops over those 40 strings three times and writes 120 files. Each triplet has the same solver function body; only the submission/replica header changes. Thus the emitted pack contains 40 distinct body templates represented by 120 files, not 120 distinct implementations or 120 evidenced single-shot generation events.

The source also includes explicit design annotations such as “natural defect: one iteration short” and “natural defect: exit on first sight, not pop”. These establish that the literal templates were organized and annotated in source. They do not, by themselves, establish who originally wrote each body or whether an earlier model session supplied it.

The repository does not retain provider/session transcripts, request identifiers, raw ordered model responses, or equivalent independently verifiable evidence establishing that the 40 body templates are faithful, unmodified outputs of the named LLM procedure. Consequently, the claimed LLM origin, single-shot status, and absence of selection before the templates entered the repository are UNVERIFIED. The repository history strengthens this limitation: the v0.2 protocol/freeze commit 798b446 (2026-10-12 12:56:28 UTC) does not contain the generator script; the 120 emitted files were committed at 8f83ee8 (13:13:24 UTC); the generator script first appears in the repository at a6a8439 (14:43:20 UTC). The freeze file was amended with the generator hash in the pack commit. The script may have existed in an untracked local workspace before then, but the Git history does not establish a versioned generator artifact before emission.

The statement “120 single-shot submissions” must therefore be read only as a historical protocol label and file count, not as verified provenance or 120 independent solver draws. The three copies of each body are not independent implementations. The pack's observed results describe the retained 40-body template corpus under the file-level execution/weighting used by the analysis. Population-level claims about natural single-shot LLM submissions are not supported.

### What the v0.2 result does and does not say

The frozen analysis returned NEGATIVE under its prespecified classification rule. That computational classification is preserved. It is not evidence that concentration has no incremental predictive value, because the eligible observations did not provide the required equal-k, different-C contrast.

The probe builders in study/probes.py accept the variant index, not the instance seed. make_probe_suite(instance_seed) calls those seed-independent builders; the seed affects the probe dictionary's metadata field, not the graph construction. Therefore the graph content, predicate assignments and diagnostic failure vector for a fixed solver body are invariant across instances. The hidden-suite outcomes do vary by instance, so leave-one-instance-out scoring is not literally empty: it can evaluate whether fixed solver-level diagnostic features predict outcomes on other hidden suites for the same fixed pack. It cannot establish that instance-specific diagnostic variation predicts instance-specific correctness, nor does it test unseen-solver generalization.

The v0.2 interpretability audit directly verified C = 5/k on the 90 persisted eligible pilot rows, with no within-k variation. The confirmatory report persisted aggregate counts and instance-level score contributions, not per-solver (k,C) rows; the repository's subsequent audit explicitly records that a direct confirmatory row-level recount was not performable without rerunning the solvers. Given the unchanged body corpus and seed-invariant probe graph construction, the confirmatory features inherit the same structural limitation, but this record does not misstate the 90-row pilot recount as a persisted 1,200-row confirmatory audit.

The narrow interval is reproducible from the persisted instance-level delta_i values. That establishes computational reproduction of the reported score comparison, not demonstrated interval coverage and not precision for an independently varying concentration effect. The “not underpowered” statement in §7 is therefore not a valid argument that the concentration-versus-count estimand was tested with adequate power.

The v0.2 relabel control also differs from the v0.1 instrument specification: v0.1 describes per-instance relabel partitions, while v0.2 freezes one shared partition per replicate across instances. This is a change in the null-control procedure and should not be described as an unchanged control.

### Correct interpretation

The v0.2 outcome is a frozen-rule NEGATIVE model-comparison classification on the retained, replicated source-code corpus. The experiment did not identify whether family concentration predicts hidden-suite correctness beyond failure count when concentration varies independently of count. It does not refute that hypothesis and does not establish performance for a natural LLM-generated solver population.

For the supporting source review, seed and ordering checks, and limits of this adjudication, see reviews/CLAUDE_FULL_REPO_CHALLENGE_ADJUDICATION_2026-11-21.md. No solver was regenerated or executed for this correction.

**Status:** TERMINAL — **NEGATIVE** (2026-10-12)
**Protocol:** v0.2, frozen 2026-10-12 before pack generation (`v0.2-freeze` @ `798b446`; protocol hash `99a7f7f00d14b98e…`).
**Terminal runner outputs:** `v02/confirmatory_v02/confirmatory_v02_report.json`, `v02/confirmatory_v02/RESULT_V02.md`.

## 1. Exposure disclosure (read first)

This analysis was **not entirely unexposed confirmatory work.** During interrupted
execution of the frozen runner, intermediate confirmatory metrics were observed before
the run completed:

- Attempts 1–2 crashed on harness bugs **before any scoring**; no metrics observed.
- Attempt 3 (30-minute tool timeout) scored all 40 instances and **printed the real
  Δ and 95% CI** (`delta≈−0.000000, CI≈(−0.000002, 0.000002)`) before being killed
  inside the relabel loop.
- Runtime profiling additionally observed **3 of the 200 randomized-label draws**
  (`≈[0.00214, −2.9e-7, 0.00214]`) and the exact full-data LOIO Δ.
- Attempt 4 was user-aborted during the relabel loop after re-printing the same Δ/CI.
- Attempt 5 completed the frozen pipeline end-to-end (scoring, 10 000-resample
  bootstrap, R = 200 relabelings, classification).

No protocol rule, threshold, model, seed, or analysis constant was changed in response
to anything observed. The statistical code (`v02/models_v02.py`) and its hash predate
all exposure. Full ledger, hash verification, and repair diff:
`v02/INTEGRITY_REVIEW_2026-10-12.md`. The result below is the outcome of the
prespecified decision rule applied to the completed run; its execution history
prevents presenting it as a blind confirmation.

## 2. Terminal classification

Under the frozen decision function (`classify`, pre-exposure hash `65d4b157…`),
δ = 0.01 nats per hidden input, two-sided 95% percentile CI (10 000 instance
bootstrap resamples, seed 99):

| Quantity | Value |
|---|---|
| Δ (L_A − L_B, held-out instances, LOIO) | **−2.639 × 10⁻⁹ nats** |
| 95% CI | **[−1.519 × 10⁻⁶, 1.583 × 10⁻⁶]** |
| Threshold δ | 0.01 nats |
| Confirmatory instances | 40 (seeds from freeze hash; disjoint from pilot) |
| Eligible (solver, instance) pairs | 1200 (k ≥ 2) |
| **Outcome** | **NEGATIVE** (CI upper bound 1.58 × 10⁻⁶ < δ) |

Decision path: the Positive rule fails on both arms (CI lower bound ≤ δ; real Δ
−2.6 × 10⁻⁹ < randomized-label p95 2.1 × 10⁻³). The Negative rule fires:
CI upper bound < δ, i.e. a meaningful gain (≥ 0.01 nats) is excluded in scope.

## 3. Randomized-label control (from the completed run)

R = 200 prespecified balanced relabelings of the 30 probe slots (one shared partition
per r, applied across all instances; same folds and scoring):

| Quantity | Value |
|---|---|
| p95 of relabeled Δ | 0.002138 |
| mean of relabeled Δ | 0.000951 |
| real Δ vs p95 | real < p95 (positive arm fails) |

**Record limitation, disclosed:** the completed run persisted p95 and mean but not
the full 200-draw vector. An export re-execution was started and then **aborted per
integrity directive**; it produced no output. The full vector is therefore not in the
record, and this limitation is not repaired by recomputation after the result was
known.

## 4. Claim (scoped)

> **NEGATIVE: The analysis did not find a meaningful incremental predictive benefit
> from the largest-family failure-share feature beyond the frozen failure-count
> baseline, within the specified SSSP domain, solver pack, generator protocol, and
> evaluation procedure.**

This is a negative result **within the specified SSSP population, solver pack, and
generation protocol.** It does not establish that family concentration lacks
predictive value in every setting. It does not establish that concentration can never
predict correctness, that defect localization is impossible, or that the broader
hypothesis is universally false.

## 5. Execution record

- Pilot gate (frozen thresholds): **PASS** — 30 eligible pairs per instance (≥ 15);
  among eligible pairs' hidden outcomes, correct 0.440/0.475/0.605 and incorrect
  0.560/0.525/0.395 (both ≥ 0.10 required). No gate or pack change after pilot.
- Format failures: 0/120 load errors (limit 20%).
- G1: 180/180 probes exact-one predicate. G2: 4/4 chain checks. G3: 0 mismatches on
  160 gate hidden inputs and on all 800 confirmatory hidden inputs, re-verified
  immediately before pack execution.
- Pack: 120 single-shot submissions (40 base bodies × 3 replicas), emitted once,
  retained in order, no best-of; manifest hash in `FREEZE_V02.md`.
- Terminal run: scoring 40/40 instances; relabel phase 3255 s; classification
  NEGATIVE. Commit chain: freeze `798b446` → pack `8f83ee8` → repairs/generator
  `a6a8439` → pilot `76e2dae` → integrity review `d5715b8` → diagnostics `ee3d1a4`
  → export-abort `c913b89` → this report.

## 6. Post-hoc diagnostics (explicitly post hoc; do not alter the confirmatory result)

Synthetic software checks, run after exposure, on synthetic data only (commit
`ee3d1a4`, `v02/posthoc_diagnostics_v02.json`):

- **P1 positive control:** planted C-signal recovered (Δ = 0.0712 > δ, CI lower
  bound > δ) — the pipeline is not a dead instrument.
- **P2 count-only control:** C uninformative beyond k → Δ ≈ −1 × 10⁻⁸.
- **P3 classify branches:** all five decision branches return expected labels.
- **P4 bootstrap:** degenerate input → degenerate CI, as specified.

## 7. Precision note (exploratory)

Observed CI width ≈ 3.1 × 10⁻⁶ nats vs δ = 0.01 (~3200× margin). The design could
assess the prespecified threshold with high precision; the Negative conclusion is not
an underpowered non-detection. Even a large upward correction for solver-level
dependence (the same pack appears in every instance) would not move the CI upper
bound near δ.

## 8. Scope limits

- Inference axis: unseen **instances** under the fixed solver pack and generator —
  not unseen solvers, not unseen generator models.
- One problem class (directed SSSP, non-negative integer weights), one instrument
  (six-family probe partition, frozen), one pack, one generator protocol.
- δ = 0.01 nats is a protocol choice; no decision-shift equivalence is claimed.
- All conclusions conditional on the frozen protocol, instrument, pack, generator,
  and threshold.

## 9. Termination

Terminal per `PROTOCOL_V02.md` §6. **No follow-up experiment is authorized by this
result.** v0.1 remains terminal (INFEASIBLE, `1612b87`). This report closes v0.2.
No further study version is authorized or contemplated from this conversation.
