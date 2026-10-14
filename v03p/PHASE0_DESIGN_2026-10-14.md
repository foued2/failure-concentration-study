# v0.3-P Phase 0 — Preflight Design Document

**Date:** 2026-10-14
**Status:** DRAFT for independent review. Owner-authorized (2026-10-14): Phase 0 document only. No solver generation, no hidden-outcome collection, no code implementation, and no v0.3 authorization follows from this document. v0.1, v0.2, and RLC-0 records are untouched; this file is a new dated artifact.

## 1. Scope and authority

This document specifies the design of a prospective test of the incremental predictive value of family concentration (C) beyond failure count (k). It fixes the estimand, population, outcome, models, score, minimum meaningful effect, identifiability gate, evaluation structure, simulation plan, and stopping rules, so that no critical choice can be postponed until outcomes are seen.

Passing review of this document authorizes nothing by itself. Phase 1 (software simulation) requires a separate decision. Every later phase requires its own decision. Passing a gate never authorizes the next phase.

## 2. Scientific question and estimand

**Question.** Among solver bodies drawn from the prespecified generator population (§3), does family concentration C predict hidden-suite correctness beyond what failure count k already predicts, when k and C vary independently?

**Estimand.** Δ = E[ L(baseline) − L(extended) ], where L is held-out log-loss per hidden input under the joint holdout structure of §7, expectation over the joint population of solver bodies and hidden suites. Positive Δ means C helps. Δ is defined only over the identifiable support of §8.

**Not the estimand.** A formal classification such as v0.2's Positive/Negative rule is secondary; the primary object is Δ with an interval that has demonstrated coverage (§9). No decision rule of the form "CI upper bound < δ ⇒ NEGATIVE" is inherited from v0.2.

## 3. Target population (generation protocol; values frozen only at v0.3 preregistration)

- **Method:** natural, single-shot LLM generation. One preregistered model and version, one prompt, one decoding configuration (temperature, sampling params, seed policy if any).
- **Retention:** every submission is kept. No best-of selection. No replacement packs. No post-generation filtering except prespecified compilation/format criteria, which are counted and reported.
- **Unit:** the solver body is the independent unit. Header replicas of the same body never count as independent. Body identity is established by content hashing at preregistration.
- **Scope of generalization (GPT §1):** the population is bodies produced by the specified generation process — not all software, not all solvers. A positive result generalizes at most to that generator population and the evaluation support actually sampled.

## 4. Outcome and scoring

- Each (body, suite) pair is evaluated on the suite's hidden inputs (frozen generator: 20 per suite; changing this count is a generator change and a separate design decision). Outcome per hidden input: pass/fail under the frozen classifier semantics.
- Body-level outcome for modeling: soft label s/20 with s hidden successes (candidate; final scoring spec frozen at preregistration, not inherited silently from v0.2).
- Score: log-loss, strictly proper, same as the frozen v0.2 convention unless review replaces it.
- Hidden suites are new draws from the frozen generator; none seen in v0.2; suite construction never conditioned on solver behavior.

## 5. Models

- **Baseline:** a prespecified function of k only. Candidate form: logistic regression on RCS(log(1+k)) with the v0.2 knot/ridge/iteration constants, to be confirmed or replaced at review. No C, no family features.
- **Extended:** baseline plus the single scalar C = max_j f_j / k (same definition as `study/features.py:55-60`).
- No other covariates, interactions, or post-hoc terms. The contrast is one degree of freedom.

## 6. Minimum meaningful effect δ* (not inherited from v0.2)

v0.2's δ = 0.01 nats was a protocol choice with no decision argument; it is **not** adopted.

**Decision context.** The extended model is used to break ties among equal-k candidate bodies when choosing which to send to expensive hidden-suite confirmation. The baseline is indifferent between equal-k bodies by construction; only C can change the decision. δ* is the smallest average per-hidden-input log-loss gain that would change such a decision under a prespecified standard.

**Derivation.** A per-input gain of Δ over 20 hidden inputs corresponds to a body-level log-likelihood advantage of 20Δ, i.e. likelihood ratio e^{20Δ}. Prespecifying the smallest operationally meaningful body-level separation as r = 1.5 (a 50% likelihood-ratio separation on a full outcome vector) gives

δ* = ln(1.5) / 20 = 0.020273255405408218 nats per hidden input.

(Alternates if review prefers: r = 1.25 → 0.011157177565710488; r = 2.0 → 0.03465735902799726. The r = 1.25 value is numerically close to v0.2's 0.01 by coincidence of the formula, not by inheritance; the argument, not the number, is what is prespecified.)

**Explicit review items (constants of the argument, not after-the-fact knobs):** the choice r = 1.5; the 20-input count; the tie-break usage rule. **If review rejects the rationale, the estimand is not ready to freeze and Phase 1 does not start.** δ* is fixed here before any feasibility data are seen.

## 7. Evaluation structure (hold out both axes)

The claim concerns new solver bodies **and** new hidden suites, so evaluation holds out both:

- Primary split unit: solver body. Header replicas of one body always land in the same fold.
- Secondary split unit: hidden suite. No suite contributes training and test rows simultaneously for a given prediction.
- Dependence from shared suites and from bodies evaluated on common inputs must be handled by the resampling design, not ignored.
- **Any bootstrap or resampling interval must demonstrate coverage in Phase 1 simulation before use on real data.** The v0.2 overlapping-fold percentile bootstrap (addendum B: dependent contributions, coverage unestablished) is not reused without that test.

## 8. Instrument adequacy and identifiability gate

**Verified structure (MIMO, 2026-10-14, source-checked).** Six families, five probes each, 30 diagnostic probes (`study/families.py:35-44`, `study/probes.py:73-97`). C = max_j f_j / k (`study/features.py:55-60`), so f_j ≤ 5 forces C ≤ 5/k, with equality whenever any family is fully failed. Pigeonhole: k ≥ 25 forces a fully failed family, hence **C = 5/k for all k ≥ 25**; k = 24 still admits C_min = 4/24 = 0.166667. The boundary is exact.

**Identifiable support.** Within-k variation in C is possible only for k ≤ 24 on this instrument. The analysis support is bodies with k in a prespecified subrange of [1, 24]; bodies with k ≥ 25 are counted, reported, and excluded from the contrast — never silently dropped. Changing the probe design to widen support is a separate instrument decision, not part of this preflight.

**Gate (structure fixed now; numeric thresholds set at preregistration after Phase 2 measurement, before hidden outcomes exist).** Reported with explicit counts:

1. Full k-by-C table over all bodies, with the identifiable-support region marked.
2. Distinct body count per k (and per k×C cell).
3. Rank increase from adding C: rank(basis | k, C) − rank(basis | k) on the realized design matrix.
4. Counts inside vs outside identifiable support.
5. Distinction between instrument-forced C = 5/k (k ≥ 25: variation impossible by construction) and within-support variation absent in the sampled population (k ≤ 24: variation possible but not observed).

**Named risk (CLAUDE).** Natural LLM bodies may fail either very few or very many probes, placing little mass in k ≤ 24; the gate would then fail for population-mass reasons alone. That outcome is a finding about this generator population under this instrument — not a verdict on the theory.

**Gate failure handling.** A failed gate is recorded as: "the specified population, generator settings, and diagnostic instrument do not provide sufficient support for the proposed test." It does not authorize constructed solvers, probe redesign, or generator changes within this preflight.

## 9. Phases 1–3 (plan and stop rules) and Phase 4 (separate authorization)

**Phase 1 — software simulation (no solvers).** Planted null and planted effect at δ*. Report false-positive rate, interval coverage, and power, each with explicit counts (e.g. "power 0.83 = 832/1000"). Resampling unit = solver body, matching the true independent unit. Coverage of every candidate interval method is tested here. **Stop if** power at δ* is below the preregistered target or the null false-positive rate is outside its preregistered band. That is an instrument failure, recorded as such.

**Phase 2 — feasibility sample (diagnostic probes only; hidden outcomes untouched).** One fixed, preregistered generation configuration. No best-of, no replacement. Produce the gate outputs of §8 with counts. **Stop if** analyzable support has too few distinct bodies per cell or no within-k C variation in the identifiable range.

**Phase 3 — design-specific simulation.** Simulate on the measured support with the intended sampling structure. Report power at δ* with counts. **Stop if** power is insufficient. Record: "design cannot identify the effect at δ* on the measured support" — never "theory false."

**Phase 4 — authorization decision (owner).** Only if Phases 1–3 pass may a frozen v0.3 with its own preregistration and independent review be considered. Hidden outcomes are collected only after that freeze. The decision is made after a deliberate pause, as a separate act — not as the next step of this conversation (GLM's condition). FOUED's decision at each boundary is required; reviewer agreement is never a substitute.

## 10. Governance

- v0.1, v0.2, and RLC-0 records stay untouched. Each phase produces a new, dated, append-only artifact.
- Every verification prints counts, so a silent no-op cannot pass.
- Failed gates are design failures and are never converted into theory verdicts.
- No phase authorizes the next. The owner decides at every boundary.
- Open items to settle **at review/preregistration, not after data**: δ* constants (§6), baseline functional form (§5), scoring spec (§4), gate thresholds (§8), generation configuration values (§3).

## Appendix — verified instrument arithmetic

```text
families=6 probes_per_family=5 total_probes=30 (len(PREDICATES)=6, range(5) in make_probe_suite)
  k min_max_fam_fails     C_min  C_if_full_family  C=5/k forced
 24                 4  0.166667          0.208333        False
 25                 5  0.200000          0.200000         True
 30                 5  0.166667          0.166667         True
delta_star: r=1.5 n_inputs=20 ln(1.5)/20=0.020273255405408218
```
