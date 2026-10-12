# Failure-Concentration Predictive Value Study — Protocol v0.2

**Status:** DRAFT → freezes as `v0.2-freeze` after gates pass. v0.1 (tag `v0.1-freeze`,
terminal INFEASIBLE) is immutable and untouched; this is a newly authorized study, not a
repair of v0.1.

**Central change from v0.1:** the outcome is no longer "passes all 20 hidden inputs" (which
left the eligible group with zero variation). The v0.2 target is per-hidden-input correctness.

## 1. Claim (frozen text)

Among solver submissions failing at least two diagnostic probes on an instance, does the
largest-family failure share improve prediction of whether that solver correctly solves a
previously unseen input from that instance, beyond what its diagnostic failure count alone
predicts — on problem instances never used to design anything, within the declared problem
class, solver generator, and protocol?

Scope: predictive value only. No localization claim. No novelty claim. All conclusions
conditional on class, generator (named at freeze), instrument, and threshold.

## 2. Problem class and instrument (reused unchanged)

Directed SSSP, non-negative integer weights — same as v0.1. The instrument (six family
predicates, 30 probes per instance, probe construction, hidden-suite construction, reference
oracle) is reused **without modification**: the exact `study/*.py` files hash-frozen in
v0.1's `FREEZE.md` are imported, not copied or edited. Their hashes are re-recorded in
`FREEZE_V02.md`. G1 verifies the declared partition property only, never construct validity.
If any probe or family changes, the instrument is different and must re-pass its own gates
before solver generation.

G3 (reference vs brute force on tiny graphs) is applied to every hidden test set used in
this study: pilot seeds before freeze; all confirmatory hidden sets immediately after
freeze, before any confirmatory solver execution.

## 3. Observational unit and outcome (frozen definitions)

- One **observation** for eligibility: a (solver, instance) pair with k ≥ 2 failed diagnostic
  probes (crash on a probe = failure; uncallable solver = format failure, excluded and
  counted).
- One **label**: for each eligible pair, 20 binary hidden-input outcomes y_h
  (1 = correct output on hidden input h; crash or wrong output = 0). The 20 inputs are
  **not** 20 independent experimental replications.
- **Scoring aggregation (frozen):** pair loss = mean log-loss over its 20 hidden inputs;
  instance loss = mean over that instance's eligible pairs; every instance carries equal
  weight. Uncertainty resamples instances, never inputs or solvers.
- **Fitting (frozen):** logistic regression at pair level with soft label s/20 (s = hidden
  successes) and row weight 1/(eligible pairs of that instance), so each instance contributes
  equal total weight. This is likelihood-equivalent to input-level fitting under the frozen
  aggregation.
- Inference axis: unseen **instances** under the fixed pack and generator, not unseen solver
  models. The same pack appears across instances by design.

## 4. Design constants

| Component | Value |
|---|---|
| Solver pack | 120 single-shot submissions, generator frozen at freeze, retained in order, no best-of |
| Pilot instances | 3 (seeds 101, 102, 103 — same frozen instance rule as v0.1) |
| Confirmatory instances | 40, seeds derived from the v0.2 protocol freeze hash, none equal to pilot seeds |
| Hidden inputs | 20 per instance (frozen construction, unchanged) |
| Model A | Y_soft ~ RCS(log(1+k)), knots/ridge/iterations exactly as v0.1 instrument spec |
| Model B | Model A + C = max_j f_j / k |
| Control | Model B with family labels relabelled: R = 200 prespecified balanced random partitions of the 30 probe slots, one partition per r **applied consistently across all instances**, same folds and scoring |
| Primary metric | Δ = L_A − L_B on held-out instances, LOIO grouped CV |
| Threshold δ | 0.01 nats mean log-loss per hidden input — a protocol choice, no decision-shift equivalence claimed |
| Uncertainty | 10 000 instance bootstrap resamples, 95 % CI |

## 5. Pilot gate (frozen; both conditions required)

1. ≥ 15 eligible (solver, instance) pairs per pilot instance.
2. Among eligible pairs' hidden-input outcomes in each pilot instance: ≥ 10 % correct
   **and** ≥ 10 % incorrect.

Failure of either condition on any pilot instance → **INFEASIBLE**, stop. No pack increase,
no generator change, no probe redesign after observing the pilot. Condition 2 is a
feasibility threshold, not evidence of predictive power.

## 6. Terminal outcome rules

| Outcome | Rule |
|---|---|
| Positive | 95 % CI lower bound for Δ > δ, and real-family Δ beats the 95th percentile of the 200 relabelings |
| Negative | 95 % CI upper bound < δ (meaningful gain ruled out in scope) |
| Ambiguous | CI suggests meaningful gain but real families do not beat the relabel control |
| Inconclusive | Gate failed, chain checks failed, format-failure rate > 20 %, or CI too wide to classify |

Every outcome is terminal. A positive result supports only the scoped predictive claim.
No follow-up experiment is authorized by any result.

## 7. Execution order

1. Build v0.2 analysis/scoring code; re-run G1–G3 on the reused instrument (evidence in
   `gates/gates_report_v02.json`).
2. Freeze: hash protocol, spec, v0.2 code, and the reused v0.1 instrument files →
   `FREEZE_V02.md`, tag `v0.2-freeze`.
3. Generate the 120-pack per frozen generator spec (G3 on all 40 confirmatory hidden sets
   first); run the 3-instance pilot; apply the gate.
4. Gate pass → run confirmatory once; publish the terminal classification. Gate fail →
   INFEASIBLE, stop.
