# S1 — Specification for a simulation with a known predictive gain

**Date:** 2026-11-18
**Status:** design draft. **Executes nothing.** No simulation, no fitting, no Monte Carlo, no generator
run. Written under the existing bounded GO (design and mathematics only).
**Supersedes:** nothing. **Authorizes:** nothing.

---

## 0. Why this document exists

Both external reviewers converged on one question: can a simulation be built in which the incremental
predictive gain is **known in advance**, rather than specified as defect reach and hoped to emerge?

The answer is yes, and the construction is not speculative. It follows from an identity that makes the
target exactly computable. This document specifies that construction, six worlds, one estimator, and
predeclared pass/fail rules — all before any run.

It also states, in §10, the conditions under which S1 would fail **as a test**. That section is not
decoration. A simulation that cannot fail is not a test.

---

## 1. What S1 answers, and what it does not

**Answers:** given a data-generating process in which the population predictive gain of adding `C` is
exactly `Δ_pred`, does the complete estimation pipeline recover it with acceptable bias, interval
coverage, and false-positive control?

**Does not answer:** whether real solvers have `Δ_pred > 0`. S1 is an instrument test. A passing S1
says the thermometer works; it says nothing about the patient. The mechanism question is separate and
remains unanswered — LC518's eight input strata are input categories, not verified defect classes, and
cannot be relabelled into causal mechanisms.

**Does not replace:** the 2026-11-01 route-scoped NO-GO recommendation, or the absence of a route-closure
record. S1 does not reopen the frozen `C = max_j f_j / k` route and does not decide it.

---

## 2. Notation, and one collision to avoid

`C = max_j f_j / k` for `k = Σ_j f_j > 0`, over six diagnostic families with five probes each.

**`δ` is already taken.** In v0.2, `δ = 0.01 nats` is the **decision threshold** — a margin, not a gain
(`v02/PROTOCOL_V02.md:65`: "a protocol choice, no decision-shift equivalence claimed"). This document
therefore uses:

| Symbol | Meaning | Domain |
|---|---|---|
| `Δ_pred` | **the quantity S1 must recover** — population predictive gain, nats per input | ≥ 0 |
| `τ` | decision threshold for a future confirmatory test | > 0, owner-set |
| `β` | logistic coefficient on `C` | ℝ |
| `J_par` | number of independent parents | open |
| `n_in` | held-out inputs per variant | open |

Reusing `δ` for both a threshold and a gain would repeat exactly the class of error this audit is
about. It is not reused.

---

## 3. The target, exactly

Let `Z = (X, C)`, where `X` holds the predeclared controls (family indicators, `k`, and — in the
adjusted world — defect identity), and let `Y ∈ {0,1}` be held-out input correctness.

Define

```
Δ_pred  :=  I(Y ; C | X)      (nats per input)
```

**Why this is the right object.** For any joint distribution,

```
E[ log p(Y|X,C) − log p(Y|X) ]  =  Σ_{x,c} p(x,c) · KL( p(·|x,c) ‖ p(·|x) )  =  I(Y;C|X)
```

So `Δ_pred` is *identically* the expected log-loss improvement of an oracle that knows `p(·|x,c)` over
one that knows only `p(·|x)`. It is not a coefficient, not a proxy, and not an approximation. It is the
quantity GPT asked for: the gain must be "calculated under the declared outcome distribution and
scoring rule", and this is that calculation.

**Why a coefficient is not enough.** A logistic `β` is a parameter of an assumed link. The map
`β ↦ Δ_pred` depends on `Var(C|X)`, the base rate, and the link. Reporting `β > 0` as "a gain of X
nats" is the error GPT named. S1 reports `Δ_pred` as primary and `β` as secondary.

*Consistency check, not definition:* for small effects and a probit link, `I(Y;C|X) ≈ ½·β²·Var(C|X)`.
S1 uses this only to catch coding errors, on a declared domain, never to define the target.

**The estimable region is part of the target.** `C` is undefined at `k = 0`; at `k = 1`, `C ≡ 1`; at
`k ≥ 25`, `max_j f_j = 5` is forced and `C = 5/k` is deterministic. The informative region is
**`2 ≤ k ≤ 24`**, where `C` varies at fixed `k`. `Δ_pred` is defined **on that region**, and the
region is frozen before any run. A target on one population and an estimator on another is a silent
failure mode, so it is closed here rather than discovered later.

---

## 4. From target to generator: imposing `Δ_pred` by construction

**Step 1 — fix the diagnostic marginal `p(z)`.** Reuse the W1 diagnostic generator verbatim
(`10_THREE_WORLD_SIM_DESIGN.md`): defect count `m ~ U{1..4}`; home family `h ~ U{1..6}`; reach
`d_h = 0.8`, `d_j = 0.05` otherwise; `q^D_j = 1 − Π_m(1 − d_mj)`; `f_j ~ Binomial(5, q^D_j)`.
This yields `p(f)`, hence `p(k, C)`.

**Step 2 — impose the outcome model.** Declare a base-rate offset `α_x` per control cell and a slope
`γ`:

```
p(y = 1 | x, c)  =  σ( α_x + γ · s_x · c )
```

where `s_x ∈ {−1,+1}` is a predeclared sign vector (all `+1` except in the sign-reversed world).

**Step 3 — solve for `γ`.** `Δ_pred(γ) := I_γ(Y;C|X)` is computed by **exact enumeration** over the
finite support of `(k, C, Y)`. No sampling. At `γ = 0` the outcome does not depend on `c` given `x`,
so `Δ_pred(0) = 0` exactly. For `γ ≠ 0` the information is positive and increases in `|γ|`.

**Monotonicity is verified, not assumed.** With several `x` strata and different `C` ranges per `k`,
global monotonicity in `γ` is not a theorem. Procedure: evaluate `Δ_pred(γ)` on a coarse grid; if it is
not monotone on the bracket `[0, γ_max]`, either use the smallest `γ` attaining the target or reject
that configuration. Then bisect on the verified bracket to a tolerance of `1e-10` nats.

**Result:** `Δ_pred` is known to machine precision, by construction, before any data are drawn. This is
the whole point. Nothing "emerges".

**What this does not do.** It does not make the generator a model of nature. `γ` is a dial, and setting
it is a decision about what to test, not a claim about solvers. §10 makes that non-negotiable.

---

## 5. Sampling structure: three levels, and what each buys

`PARENT_DESIGN.md` defines 30 parents in five formulation families (K1×7, K2×8, K3×8, K4×5, K5×2), five
variants each. **This hierarchy is the one S1 must model, but it is not an adopted operating count.**
The record is explicit: 30 is "a logistics scenario only, not an adopted confirmatory operating
count" (`CLAUDE_REVIEW_HANDOFF_POPULATION_DESIGN_2026-11-16_v0.17.md:47`), and
"30 parents × 5 variants is not adopted" (`LC518_EXPLORATORY_FEASIBILITY_PROTOCOL_DRAFT_0.2.md:215`).

| Level | Count | Independent? | What it buys |
|---|---|---|---|
| Parent | `J_par`, **open** | yes — the replication unit | generalisation; the only level that increases between-unit df |
| Variant | 5 per parent | nested | precision of within-parent contrasts |
| Held-out input | `n_in` per variant | nested | precision of per-variant rates |

`150` is not `150` independent units. GPT's hierarchy is right; the count is not adopted. S1 is
therefore **parametrised by `J_par`**, and reports results across a grid (e.g. `J_par ∈ {8, 30, 60}`)
rather than pretending one value is the design. That grid is a sensitivity analysis over the open
decision, not a recommendation.

---

## 6. The six worlds

All six share the diagnostic generator of §4 Step 1 and differ only in the outcome model and the
estimator's control set.

| # | World | Construction | Expected result |
|---|---|---|---|
| **S1-W0** | Null | `γ = 0` — `Δ_pred = 0` exactly | No gain; FPR at nominal |
| **S1-W1** | Positive | `γ > 0` solved to `Δ_pred ∈ {0.005, 0.010, 0.020}` | Gain recovered, bias small, CI covers |
| **S1-W2** | Sign-reversed | `γ < 0`, same magnitudes | Negative slope recovered; sign never flipped |
| **S1-W3** | Proxy | `Y` depends on latent defect identity `D`; `I(Y;C|X,D) = 0` but `I(Y;C|X) > 0` | Fit **without** `D` shows a gain; fit **with** `D` shows none |
| **S1-W4** | Partition-sensitive | Signal encoded under partition `P1`; `C` recomputed under `P2` | Gains differ; a sign flip is a sensitivity failure, not a refutation |
| **S1-W5** | Parent-dependent | `β_p ~ N(β, τ²)` across parents; inputs nested | Population `β` covered at nominal rate; ignoring the parent effect inflates FPR |

**On W3, Claude's correction is the design.** "No independent contribution after adequate controls"
is only as good as the control set. W3 therefore has no single number: it runs twice, with `D` excluded
and included, and **the contrast between the two runs is the result**. A proxy world that reports only
the adjusted fit hides exactly the failure it is meant to expose.

**On W4, the repo already has a partial precedent.** `W3` of the three-world simulation
(`10_THREE_WORLD_SIM_DESIGN.md`, "concentration-independent evaluation damage") already tests a
concentration-free world with latent defect count as an oracle. S1-W4 is not new ground; it is the
partition half of the same idea, and it should reuse that design rather than invent a variant.

**On W5, the estimand is the population slope**, not any parent's slope. Coverage of `β` under a
random-slope model is the test; a pipeline that reports `β̂` with a fixed-effect interval will
under-cover, and that under-coverage is a finding, not a nuisance.

---

## 7. The estimator

Primary model, on the estimable region `2 ≤ k ≤ 24`:

```
logit Pr(y = 1) = α + fam_j + f(k) + C + u_parent,      u_parent ~ N(0, σ_u²)
```

with `fam_j` family indicators, `f(k)` a predeclared function of `k` (indicator or spline — frozen in
advance), and `u_parent` a random intercept. `C` enters as a **fixed** slope in the primary model and
as a random slope in the W5 variant.

Fitting: leave-one-parent-out (LOPO) cross-fitting, as the B1 plan specifies. Each held-out parent's
inputs are scored by parameters estimated without that parent.

**Two reported quantities, never conflated:**

1. **`Δ̂_pred`** — the realised held-out log-loss improvement, `(1/n) Σ [log p̂₁(y_i|x_i,C_i) −
   log p̂₀(y_i|x_i)]`, in nats per input. This is the primary quantity, because it is the same scoring
   rule that defines the target.
2. **`β̂`** — the coefficient, with its interval, reported secondarily.

---

## 8. Two targets, because the plug-in gain is biased by construction

For any plug-in estimator, `E[Δ̂_pred] ≤ Δ_pred` — Jensen, since the estimated distribution is not the
true one. Comparing `Δ̂_pred` directly to `Δ_pred` would therefore manufacture a negative bias and
call it a defect.

The fix is to report **two** targets:

- **`Δ_pred`** — the population value, known exactly by §4. Used for **coverage**.
- **`Δ_oracle(n)`** — the log-loss improvement achieved by the *true* probabilities on the *same*
  held-out draws. Computable from the generator without fitting. Used for **bias**.

Bias is measured against `Δ_oracle(n)`; coverage is measured against `Δ_pred`. A spec that used one
target for both would be wrong in a direction that flatters or penalises the pipeline depending on `n`,
which is worse than being wrong uniformly.

---

## 9. Pass/fail rules

**Proposed defaults. Not adopted. Changing any of them after seeing results voids the test.**

| Quantity | Criterion | Note |
|---|---|---|
| FPR, W0 at `τ = 0.01` nats | `≤ 0.05` nominal, reported with exact binomial upper bound | 1 000 replicates give MC se ≈ 0.7 % |
| Power, W1 at `Δ_pred = 0.02` | `≥ 0.80` for a "designed to detect" claim | otherwise report achieved power, claim nothing |
| Bias vs `Δ_oracle(n)` | `|bias| ≤ 0.10 · Δ_pred` | relative to target, not to observed |
| Coverage of `Δ_pred` | 95 % CI in `[0.93, 0.97]` | ≈ 3 MC se at 1 000 replicates |
| Sign, W2 | never positive | any positive estimate is a failure |
| W3 contrast | adjusted gain < unadjusted gain, and adjusted ≈ 0 | direction predeclared |
| W4 | gain under `P2` reported, not required to be positive | a flip is recorded as sensitivity failure |
| W5 coverage of `β` | `[0.93, 0.97]` under random slopes | fixed-effect interval under-covers by design |

**The pass condition is conjunctive and the threshold is `τ`, not `Δ_pred`.** A world can show a real
`Δ_pred` and still fail the *decision* if `Δ_pred < τ`. Those are different rows and must not be merged.

---

## 10. What would make S1 fail as a test

GPT's closing condition, made operational. S1 fails as a test — and says so — if any of these hold:

1. **No `γ` attains the target.** If `Δ_pred(γ)` saturates below `0.02` nats for every admissible `γ`,
   the world cannot test a 0.02-nat gain. Reported as "not testable at this target", not as a pass.
2. **The target requires the conclusion.** If the only way to reach `Δ_pred = 0.02` is to fix `p(z)`
   so that `C` is nearly deterministic in `Y`, the world tests a tautology. Check: the mutual
   information must be carried by *conditional* variation in `C`, not by `C` reproducing `k`.
3. **The estimable region is too small.** If the `2 ≤ k ≤ 24` region holds too few rows for the
   stratified fit, the world is underpowered for reasons unrelated to `C`. Report the region's share.
4. **W0 fails.** If the null world produces gains above the FPR criterion, the pipeline is broken and
   no positive-world result is interpretable. W0 gates everything.

Criterion 2 is the one that would most likely bite, and it is the one a reviewer should check first.

---

## 11. Execution gate

The B1 plan's authorization basis is **"bounded GO (design and mathematics only)"**, and:

> "Not authorized and not performed: numerical probability evaluation, executable simulation, Monte
> Carlo or permutation *execution*, fitting of any model, ... Execution of anything this plan declares
> requires a further explicit GO after this plan is reviewed and accepted."
> — `B1_ANALYSIS_PLAN_2026-11-14_v1.1.md:7`

*(Claude's round-3 note dates this rule to 2026-11-10; the operative text is in the 2026-11-14 B1 plan.
The 2026-11-10 capacity addendum is a separate record that states "not a GO". Same substance, different
document — corrected here so the citation is checkable.)*

Consequences:

- **Writing this document is inside the existing bounded GO.** Design and mathematics are authorized.
- **Running it is not.** §4's bisection is a numerical evaluation; §9's replicate counts are Monte
  Carlo. Both require a GO naming S1's scope.
- **The GO should be requested only after** this specification is frozen by hash and reviewed, so that
  the thing being authorized is fixed and cannot drift.

A single GO covering "S1-W0 through S1-W5 at the listed targets and replicate counts" is sufficient.
It does not need to cover the operating population, which stays open.

---

## 12. Open decisions, and who owns them

| Decision | Owner | Blocks |
|---|---|---|
| `J_par` grid and the adopted operating count | owner | §5 reporting |
| `n_in` per variant | design | §9 precision |
| `τ` for the confirmatory decision | owner | §9 row 1 |
| Whether `f(k)` is indicator or spline | design | §7 |
| Accept/reject this specification by hash | GPT adjudication, Claude review | §11 GO request |
| Whether to request the S1 GO at all | owner | everything |

Until the last row is decided, S1 is a paper design. That is the correct state, and it is not a
deficiency: the record's failure mode was never a shortage of execution.

---

## 13. What this specification does not claim

- It does not claim the concentration hypothesis is true, testable on real data, or likely.
- It does not claim W1 was a positive control; W1 was a wiring check (§3 of the goal document).
- It does not claim the `F`-versus-`C` result; the equal-weighted arm still fails.
- It does not adopt 30 parents, 150 variants, or any operating count.
- It does not reopen the 2026-11-01 NO-GO recommendation, which remains a reviewer concurrence with no
  owner closure decision and no route-closure record.
