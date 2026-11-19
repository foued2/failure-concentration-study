# Fundamental goal — validate the analytical pipeline before building the population

**Date:** 2026-11-18
**Status:** **Owner-designated fundamental goal.** This document sets the order of work for the
programme. It is not a protocol, not a design freeze, not an execution authorization, and it does not
amend any frozen document. No existing authorization is changed by it.
**Provenance:** the critique in Appendix A was written by Claude; Appendix B is GPT's concurrence,
which also corrects GPT's own earlier omission; the owner directed on 2026-11-18 that both be recorded
as the project's fundamental goal. The goal statement in §1–§3 is a faithful condensation. The nine
issues are reproduced with a verification column (§4), because three of their supporting claims do not
match the repository record as written and must not be enshrined uncorrected.

---

## 1. The goal

> **Demonstrate, on synthetic data with a known injected effect, that the analysis pipeline recovers
> that effect under a frozen partition — before any real-data claim about concentration is made.**

Concretely: a simulation must show that the specified estimator, on data generated with a known
concentration effect, returns that effect with an interval excluding zero and with the correct sign
under the primary partition; and that it returns no effect on a matched null, does not manufacture
one under a confound, and reports partition sensitivity rather than hiding it. Until that happens, a
null or a positive result from real data cannot be interpreted.

This replaces "build the 150-variant population" as the **first** task. Population construction is
not cancelled; it is sequenced after the instrument is shown to work.

---

## 2. What changed

The three-world simulation was specified as a **wiring check**, and it failed. It was not a calibrated
positive control: the design fixes defect-reach parameters but defines no true value of `Δ_pred`, so a
small result cannot establish that the method misses a known effect. Both reviewers have since
withdrawn the "positive control" label (see the reviewer-response record in
`reviews/analytical-validity-2026-11-18/`).

`engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md`:

| Quantity | Recorded value |
|---|---|
| Trials × cases | 500 × 5 000 = 2 500 000 per world |
| W1 eligible cases | 2 499 949 |
| Fixed-`k` overlap in W1 | 2 365 022 cases, 49 834 strata, residualized C variance 14 737.3 |
| C gain, domain score | **+1.961346752 × 10⁻⁶**, 95 % [−1.242089975 × 10⁻⁶, +7.581285807 × 10⁻⁶] |
| C gain, alternate partition | **−1 × 10⁻⁶**, 95 % [−3 × 10⁻⁶, +3 × 10⁻⁶] |
| Frozen outcome | **W1 FAILED** — "DOES NOT SURVIVE" |

The identification requirement was satisfied in W1 (2.37 M cases in fixed-`k` cells) and the effect
was still not recovered. This is the only executed analysis in the corpus with genuine fixed-`k`,
different-`C` overlap, and it is a negative control result about the **instrument**, not about
concentration.

Two qualifications must travel with this, and both are in the source:

1. The report's own scope line: "Synthetic-data simulation only. Results show implications of the
   declared assumptions; they are not evidence about real solvers."
2. GPT's caveat (Appendix B §1): before treating W1 as a failed positive control, one must verify that the
   injected effect was injected into **the same estimand the analysis was built to recover**. A
   simulation can contain a parameter called a concentration effect without creating the corresponding
   observable predictive gain. **This verification has since been done and it fails:** the design fixes
   defect-reach parameters (`d_h = 0.8`, `e_h = 0.35`) and defines no true `Δ_pred` anywhere, so W1 is a
   wiring check whose positive-control status is unproven.

Subject to that verification, the implication is the one GPT states: "We have not demonstrated that
our analysis can detect the phenomenon we intend to investigate."

---

## 3. The four gates, in order

These must not be conflated, and the order is a dependency order, not a preference.

| Gate | What must be demonstrated | Current position | Deciding record |
|---|---|---|---|
| **1. Measurement** | The partition captures a reproducible failure pattern; `C` is not merely an artefact of the chosen strata or of the noisy maximum | **Unresolved** | no record; formulation note §7–§8 |
| **2. Mechanism** | Dominant diagnostic failures recur on corresponding held-out inputs | **Not demonstrated** | proposed only (§5 below) |
| **3. Identification** | `C` contributes beyond competing explanations (family, defect identity, realization setting, `F`) | **Not demonstrated** | Gate 1 closed; v0.21 `a(v)` confound admitted |
| **4. Statistical detection** | The analysis recovers prespecified effects with adequate power and controlled false positives | **W1 failed its wiring check; its status as a positive control is unproven** | `11_THREE_WORLD_SIM_RESULT.md` |

The sequence follows: **repair and independently validate the simulation (gate 4), while fixing the
measurement definition it tests (gate 1).** Only then is a defensible operating population and sample
size computable (gate 3). Gate 2 is a scientific question in its own right and can be tested earlier
than the full predictive design, because it needs only a diagnostic bank, a held-out bank with a
predefined stratum correspondence, and executed solvers.

---

## 4. The nine issues, with verification

Status vocabulary: **Verified** (checked against a named record in this pass) / **Argument**
(mathematically or logically sound, not an empirical record) / **Not supported as written** (the
record says something different).

| # | Issue | Status | What the record actually shows |
|---|---|---|---|
| 1 | The simulation that was meant to test the design failed: W1 had the effect built in, C gain ≈2×10⁻⁶, interval includes zero, alternate partition flips the sign | **Numbers verified; "effect built in" not supported** | Exact values in §2. Sign flip is of the **point estimate** (+1.96×10⁻⁶ → −1×10⁻⁶); both intervals include zero, so it is sign instability, not a significant reversal. The design injects defect reach, not a `Δ_pred` truth, so W1 is a wiring check, not a positive control. |
| 2 | `C` depends on the partition; the W1 sign flip shows partition changes can reverse the result; freezing the partition is necessary but not sufficient | **Verified** | `C = max_j f_j / k` exists only after the strata are fixed; W1's partition arm is the empirical instance. Formulation note §8 requires the feasible-support gate on the diagnostic footprints before held-out scores. |
| 3 | Solver-level variables have solver-level sample sizes; the solver random effect can absorb `C`; a 100-solver design has little power for a 0.01–0.02 nat effect | **Verified structurally; one clause not supported** | The hierarchy is correct and the record already names the fix: worklog C4 accepts "crossed RE (generation group / solver / input group / template) primary, grouped bootstrap fallback". **But** "the earlier power work found that solver variation dominates" is not in the record. The recorded assumption is ICC ρ = 0.05, at which 80 % power for β = 0.06 needs ≈20 effective bodies per cell (160 per condition); at 12/cell power is 0.512. That is a clustering cost, not dominance. |
| 4 | Small `k` makes `C` nearly degenerate: `k=1` ⇒ `C=1`; `k=2` ⇒ `{0.5, 1}`; the max of noisy counts is biased upward | **Verified (discreteness) / Argument (bias)** | Formulation note §8: "`C` has no variation at `k = 1` and at every `k` from 25 through 30; at `k = 2`, two levels are possible." The upward bias of a maximum is a property of the estimator, not a repository measurement; its size depends on probe generation and has not been quantified here. |
| 5 | No mechanism says why dominance should transfer; the testable mechanism is that a single defect class drives failures and its errors recur in the same held-out stratum | **New proposal** | Not in the corpus. It is the sharpest falsifiable statement the programme would have had; see §5. |
| 6 | Competing explanations are not all accounted for; diagnostic and held-out inputs must be checked for common generation; the record says mechanism-disjoint held-out populations may not be achievable | **Partly; the last clause is not supported** | The confound is real and is recorded (`CONSTRUCT_VALIDITY_ASSESSMENT` §1.3, §5). The recorded requirement is **input-cluster disjointness** — held-out clusters "independently constructed from, and disjoint from, the diagnostic clusters" (formulation note §7) — not mechanism-disjointness. No repository statement that mechanism-disjoint populations are unachievable was found in this pass. |
| 7 | Researcher degrees of freedom: six reformulations, thresholds 0.01 / 0.02 / 0.04 nats, unresolved knot and tertile choices, two research lines | **Verified** | Six formulations are documented (succession audit §1). Thresholds: δ = 0.01 nats (v0.2), d* = 0.020273255405408218, 2δ* = 0.040546510816436. Knots `{2,8,16,24}` were "frozen pre-data" in the worklog; a `k × within-k C-tertile` support cell is named in C3. |
| 8 | Decision value is undefined: a gain in nats must map to a decision; B1 already does accept/reject; the ranking of rejected solvers needs a threshold in decision terms | **Verified** | v0.3-P §6 ties d* to a decision context (tie-breaking for expensive confirmation), but B1 has no such mapping. The B1 decision record defines support and identification only. |
| 9 | Unresolved outcomes can bias the denominator: if `k_unresolved` correlates with held-out error, excluding it changes both `C` and the outcome | **Argument; structurally guarded, not analysed** | B1 keeps `k_unresolved` as an explicit coordinate in the support cell, which prevents silent exclusion but does not test the correlation. No analysis of that correlation exists. |

---

## 5. The mechanism hypothesis (proposed, not adopted)

This is the one genuinely new scientific proposal in the critique, and it is stronger than the
predictive claim because it predicts **where**, not merely **that**.

> If a single defect class drives a solver's diagnostic failures, its errors should recur on held-out
> inputs in the corresponding stratum.

Formally: for solver `s` with dominant diagnostic stratum `j*`, held-out errors should be
disproportionately concentrated in the held-out stratum corresponding to `j*`, relative to other
strata.

Why it matters: it separates two explanations that the current design cannot.

| Explanation | Prediction |
|---|---|
| **Predictive proxy** | `C` correlates with held-out error because one defect causes both; held-out errors need not cluster by stratum |
| **Stratum transfer** | Held-out errors cluster in the dominant diagnostic stratum |

The second is falsifiable even when `C` correlates with error rate. If held-out errors do not cluster
there, the concentration story fails even under a positive `C`–error correlation.

Required before it can be tested (none of these exists yet):

1. a **predefined correspondence** between diagnostic and held-out strata;
2. controls for input difficulty and for the distribution of test opportunities per stratum;
3. a **tie rule** for dominant strata (the corpus already records tied profiles: `T3 = (0,0,0,0,5,5)`
   and `T4 = (0,0,2,2,3,3)` both tie families 5 and 6);
4. a held-out bank built by the same construction rule as the diagnostic bank, or an explicit
   statement that the claim is benchmark-bound.

Note the tension with gate 1: a held-out bank that is stratified to match the diagnostic families
makes the transfer test possible but re-introduces the partition dependence. That trade-off must be
declared, not discovered.

---

## 6. The validation programme (the actual deliverable of this goal)

A simulation suite, run before any new population is built, with these scenarios and acceptance
criteria. All must use the **primary** partition, estimator and threshold; sensitivity arms are
reported, not substituted.

| Scenario | Construction | Pass condition |
|---|---|---|
| **S1. Known positive** | Inject a prespecified concentration effect into the same estimand the estimator targets | Point estimate within the prespecified tolerance of the injected value; 95 % interval excludes zero; correct sign |
| **S2. Known null** | Same generator, no concentration effect | Interval includes zero at the nominal rate; false-positive rate within its prespecified band |
| **S3. Confounded** | Effect produced only by a shared defect (diagnostic and held-out errors from one cause), no concentration effect | Estimator does **not** report a concentration gain, or the confound control absorbs it |
| **S4. Partition sensitivity** | Same data, alternate defensible partitions | Direction and magnitude reported for every prespecified partition; a sign reversal is reported as a result, not smoothed away |
| **S5. Solver-level dependence** | Crossed random effects (generation group / solver / input group / template); varying ICC | Coverage of the interval at the nominal rate; power computed at the solver level, not the input level |
| **S6. Unresolved outcomes** | `k_unresolved` correlated with held-out error | Bias quantified; a prespecified handling rule either bounds it or the design is declared non-robust |
| **S7. Degenerate cells** | `k = 1`, `k = 2`, `k ≥ 25` | Estimator reports unavailability rather than a number; no cell is silently dropped or pooled |

**Acceptance of this goal is not acceptance of any single simulation design.** The scenarios,
tolerances, ICC grid, and pass bands must be specified before S1–S7 are run, and reviewed
independently.

---

## 7. Consequences for the current LC518 plan

1. **150 solvers is not the next step.** Building the population before S1–S7 pass would spend the
   budget on data whose analysis cannot be interpreted.
2. **The M1-si audit is downstream.** It checks a structural support condition; it cannot establish
   that the estimator detects an effect. A support pass on an unvalidated estimator would be a
   false comfort.
3. **v0.21 population work is not cancelled, only resequenced.** No existing authorization changes;
   this document adds an ordering constraint.
4. **One primary analysis must be named.** Six formulations, three thresholds, knot and tertile
   choices, and two research lines are on record. A confirmatory run requires one partition, one
   estimator, one threshold, one population, fixed before outcomes.
5. **Historical exploration does not invalidate a new study**, but the entire history must be
   disclosed and the new analysis locked independently of its outcomes (GPT, Appendix B §5).

---

## 8. What this goal does not do

- It does not establish that concentration has no predictive value. W1 is synthetic and its
  injection correspondence is unverified.
- It does not establish that the analysis is broken. It establishes that the analysis has not been
  shown to work.
- It does not authorize simulation, solver generation, bank reuse, model calls, or execution.
- It does not change v0.1, v0.2, v0.3-P, B1 v1.7, v0.21, or any frozen record.

---

## 9. Immediate next actions, in order

1. **DeepSeek reviews the S1 specification in the web chat** at `reviews/analytical-validity-2026-11-18/S1_KNOWN_GAIN_SPEC_2026-11-18.md`, with section-specific objections to the true outcome model, estimand, circularity, estimator, uncertainty procedure, and tolerances.
2. **GPT adjudicates the review** and revises the S1 specification. No implementation begins during this step.
3. **Freeze the reviewed S1 specification and its matched-null companion only after review.** The proposed tolerances remain provisional until that review is resolved.
4. **Specify the remaining S2–S7 scenarios** under the same review discipline. No simulation is run merely because a scenario has been written or frozen.
5. **Obtain a separate explicit execution GO** before writing generator code, running simulations, fitting models, or reusing any bank.
6. **Only after validated operating characteristics exist** compute a defensible real-study parent count and decide the owner route (confirmatory versus exploratory). The calibration J grid in S1 is not that parent-count decision.

---

## Appendix A — Claude critique, as supplied by the owner (verbatim)

> CLAUDE/ The main gap is that the design has never shown it can detect the effect it's looking for. The other gaps follow from that.
>
> 1. The simulation that was meant to test this failed. In the three-world simulation (500 trials, 5,000 cases), world 1 was built to contain a concentration effect. Its frozen wiring check failed: the C gain was about 2×10⁻⁶, the interval included zero, and an alternate partition flipped the sign. So even where the effect was built in, the statistic didn't recover it. GPT's account and DeepSeek's audit don't mention this result, and it matters more than any of the points below.
>
> 2. C depends on the partition. C = max_j f_j / k only exists once the six or eight strata are fixed. The W1 sign flip shows that changing the partition can reverse the result. "Frozen before outcomes" is necessary, but it isn't enough. The partition's sensitivity has to be reported as part of the result.
>
> 3. Solver-level variables have solver-level sample sizes. C is computed per solver, but held-out correctness is measured per input. Inputs are nested within solvers, so the effective sample size for C is the number of solvers, not the number of inputs. The solver random effect can absorb C, and the earlier power work found that solver variation dominates. A design with 100 solvers has very little power for a 0.01 to 0.02 nat effect, however many held-out inputs it uses.
>
> 4. Small k makes C nearly degenerate. At k = 1, C = 1. At k = 2, C can only be 0.5 or 1. Most of the eligible range sits in cells where C barely varies, and the max of noisy estimates is biased upward. The same cell-occupancy problem that makes the B1 support rule hard to satisfy also limits any claim about small k.
>
> 5. No mechanism says why dominance should transfer. Without one, a positive result would be a correlation with an index. The mechanism I'd test is this: if a single defect class drives the failures, its errors should recur on held-out inputs in the same stratum. That's a sharper prediction than "C predicts held-out error." It says held-out failures should cluster in the dominant stratum specifically. If they don't, the concentration story is wrong even when C correlates with error rate.
>
> 6. The competing explanations are not all accounted for. A defect that causes both diagnostic failures and held-out errors would make C look predictive without any concentration effect. Holding k and the number of occupied strata fixed helps, but it doesn't rule this out. The test also has to check whether the diagnostics and the held-out inputs were generated by the same process. The record says mechanism-disjoint held-out populations may not be achievable, so any result would apply only to a same-mechanism benchmark.
>
> 7. Researcher degrees of freedom are large. Six reformulations, several thresholds (0.01, 0.02, 0.04 nats), unresolved knot and tertile choices, and two research lines. Any positive finding from this sequence would have a multiplicity problem unless one primary analysis is fixed in advance.
>
> 8. Decision value is undefined. Even a real gain has to matter for a decision. B1 already performs accept/reject. The question is whether the ranking of rejected solvers helps. That needs a minimum effect defined in terms of decisions, not nats, and that threshold hasn't been set.
>
> 9. Unresolved outcomes can bias the denominator. If unresolved outcomes are correlated with held-out error, excluding them from k changes both C and the outcome.
>
> What this means: the question is not yet testable with a valid design. The first step is a simulation that recovers a designed effect under a frozen partition, a multilevel analysis that treats solvers as the unit, and a pre-registered primary analysis with one threshold. Until the simulation recovers a built-in effect, a null or positive result from the real data can't be interpreted.

## Appendix B — GPT concurrence, as supplied by the owner (verbatim, abridged at the marked point)

> GPT/ Claude has identified a more fundamental problem than the ones we discussed earlier. I agree with its central conclusion, and I should correct an omission in my previous assessment: the failed W1 simulation should have been the first issue I raised.
>
> It changes how we should assess the entire proposed research programme.
>
> 1. W1 is the first problem to resolve. The three-world simulation was supposed to examine whether the analytical machinery could recover a known concentration effect. According to Claude's account, W1 had an effect built into its data-generating process, yet the reported gain was approximately 2×10⁻⁶, its interval included zero, and an alternative partition reversed the sign. That is a failed positive-control test. There is one qualification: we must verify that the effect was genuinely injected into the same estimand the analysis was designed to recover. A simulation can contain a parameter called a concentration effect without necessarily creating the corresponding observable predictive gain. But assuming W1 was intended as that positive control, the implication is serious: we have not demonstrated that our analysis can detect the phenomenon we intend to investigate. A real experiment analysed using an unvalidated procedure could produce a misleading positive or negative result. This does not disprove the hypothesis. It invalidates confidence in the current analytical pipeline.
>
> 2. The actual independent sample size is the number of solvers. Claude is right about the hierarchy. … A dataset with 100 solvers and 200 held-out inputs per solver has 20,000 observations, but it does not have 20,000 independent measurements of concentration. The repeated inputs improve measurement of each solver's performance. They do not manufacture additional independent solvers. The power simulation therefore needs to represent solver-level variation, input-level variation, their dependence, and the number of independent parent groups. A random-effects model must also address whether solver-specific effects are correlated with C_s. Simply adding a solver random intercept does not automatically solve that problem.
>
> 3. We need to test what concentration actually represents. Claude's partition criticism is important. C_D depends on how diagnostic inputs are divided into strata. Changing that partition can change the index and potentially its relationship with held-out performance. Freezing the partition prevents researchers from changing it after seeing results. It does not establish that the chosen partition captures a stable property of solver behaviour. The mathematical discreteness is another limitation: at k = 1, concentration must equal 1; at k = 2, only 0.5 and 1 are possible. Consequently, some failure-count cells offer very little concentration variation. The maximum of noisy stratum counts can also be upward-biased relative to the underlying failure probabilities when those counts are treated as samples.
>
> 4. Claude's mechanism proposal is stronger than the original predictive claim. This is the most interesting scientific development in the critique. … If one defect class drives most diagnostic failures, its errors should recur on held-out inputs in the same stratum. … This needs a predefined correspondence between diagnostic and held-out strata, with controls for input difficulty and the distribution of test opportunities. It also needs a rule for ties between dominant strata. Why is this important? Because it distinguishes two explanations: predictive proxy, and stratum-transfer mechanism. The second is a much more informative scientific result. It would not automatically establish causality, but it would provide evidence for the proposed transfer mechanism.
>
> 5. The remaining issues are connected. Confounding: controlling k and the number of occupied strata is necessary but does not control defect identity or realization settings. Conditioning on the entire failure vector is impossible for this purpose because it determines C_D. Unresolved outcomes: k_unresolved must remain explicit. Excluding unresolved outcomes without examining their relationship to held-out errors risks selection bias. Multiplicity: six reformulations, several thresholds, and two different research lines make it essential to designate one confirmatory question, one partition, one primary analysis and one threshold before new outcomes are collected. Decision value: a statistically detectable improvement is not necessarily useful. The intended benefit of ranking rejected solvers needs to be stated in operational terms.
>
> I would add one qualification to the multiplicity issue: historical exploratory analyses do not automatically invalidate a genuinely new confirmatory study. But the entire history must be disclosed, and the new analysis must be locked independently of its outcomes.
>
> **Consolidated scientific verdict — current analytical validity not established.** The research programme has four gates that should not be confused:
>
> | Gate | What must be demonstrated | Current position |
> |---|---|---|
> | Measurement | The partition captures a reproducible failure pattern | Unresolved |
> | Mechanism | Dominant diagnostic failures recur on corresponding held-out inputs | Not demonstrated |
> | Identification | Concentration contributes beyond competing explanations | Not demonstrated |
> | Statistical detection | The analysis recovers prespecified effects with adequate power | W1 failed its reported positive-control check |
>
> The sequence matters. The first task is not building 150 solvers. It is repairing and independently validating the simulation. That validation must include known positive effects, genuine null cases, confounded cases, partition changes, solver-level dependence, and unresolved outcomes. The analysis must recover the injected effects under the primary partition and correctly distinguish them from null and confounded scenarios. Only then can we calculate a defensible operating population and sample size.
>
> One final distinction: Claude says the question is not yet testable with a valid design. I would phrase it more precisely: the scientific hypothesis is testable in principle. The project has not yet demonstrated a design and analysis pipeline capable of testing it reliably. That is the central obstacle. And it is finally much clearer than another debate over whether to use 30 or 150 solver variants.

---

## Appendix C — files checked for §4

| Claim | File checked |
|---|---|
| W1 numbers, partition arm, scope line | `engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md` |
| Discreteness at `k=1,2,25+` | `concentration-formulation/02_RESEARCH_FORMULATION_NOTE_2026-10-25.md` §8 (remote) |
| Crossed random effects, knots, tertile | `lc518-150/glm-handoff/worklog.md:239` (remote) |
| Input-cluster disjointness requirement | formulation note §7 |
| Confound list | `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` §1.3, §5 |
| Power / ICC numbers | `next-task/10_OFFLINE_POWER_SIMULATION_REPORT_2026-10-22.md` lines 28–44 |
| Thresholds 0.01 / 0.020273 / 0.0405465 | `v02/PROTOCOL_V02.md`; `v03p/VDRAFT_Target_Bridge...` §0.2, §4.1 |
| Six formulations | `concentration-theory-succession-audit-2026-11-18.md` §1 |
| B1 `k_unresolved` coordinate | `AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` §3 (remote) |


---

## 12. Design-only state update — 2026-11-18, round 3

The W1 injection correspondence check is complete. The W1 generator specifies defect-reach parameters but does not define a true value of the predictive estimand \(\Delta_{\mathrm{pred}}\). W1 is therefore a wiring check, not a calibrated positive control. The earlier action to verify this correspondence is closed.

A separate S1 known-gain specification has been prepared at:

reviews/analytical-validity-2026-11-18/S1_KNOWN_GAIN_SPEC_2026-11-18.md

It is a mathematical design draft for DeepSeek's independent web-chat review. It specifies a latent common-cause outcome model, derives its population log-loss gain independently of the fitted estimator, defines a candidate estimator and parent-cluster test procedure, and proposes calibration tolerances. It is **not accepted, frozen, or executable**.

DeepSeek's web-chat sequence is adopted for this draft:
1. review the S1 mathematical specification;
2. resolve circularity and estimator-target alignment;
3. adjudicate the proposed bias, coverage, detection, and false-positive tolerances;
4. only after review, specify the remaining validation scenarios and obtain a separate execution GO.

No generator code has been written. No S1 or S2 simulation has been run. No model has been fitted. Writing generator code is implementation and is outside the current design-only scope.

The calibration values of \(J\) in the S1 draft are simulation dimensions for measuring estimator behavior, not an operating parent-count decision. The required real-study parent count remains undecided and must not be inferred from this draft.


## 13. Design-only state update — 2026-11-18, round 4

S1 has been revised to v0.3 at \`reviews/analytical-validity-2026-11-18/S1_KNOWN_GAIN_SPEC_2026-11-18.md\`.

The revision:
- makes the target an explicit average over the 60 fixed panel positions and indexes it by \(\eta\);
- tabulates per-difficulty KL contributions for all three signal strengths;
- states that \(C_D\) is a one-to-one recoding of the binary signal \(Q\), so S1 is a favourable proxy-recovery calibration rather than evidence that concentration is uniquely informative;
- retains the full-vector information equality only as a generator-specific identity;
- defines average conditional parent-bootstrap coverage across training fits;
- specifies the \((J,\eta)\) reporting matrix, the single primary positive-world gate, absolute bias equivalents, and Monte Carlo standard-error reporting;
- states the required S3 contrast between the unadjusted proxy association and the incremental information remaining after \(H\) is observed.

The supplied DeepSeek second-round assessment is provisional: DeepSeek could not fetch the GitHub v0.2 text and did not verify the specification directly. It is not a freeze approval. DeepSeek has explicitly accepted the factual correction that §6 was present in v0.1; the remaining question concerns the adequacy of the expanded matched-null specification.

The active reviewer remains DeepSeek in the web chat. The next review must be based on the actual v0.3 text supplied directly to that chat. No generator code has been written, no simulation or model fit has been run, no bank has been reused, and no execution GO has been requested or inferred.


## 14. Design-only state update — 2026-11-18, round 5

DeepSeek has now directly reviewed the complete S1 v0.3 specification. It found no mathematical or statistical error in the declared narrow predictive-proxy calibration and considers it defensible as a first-stage calibration, subject to a stronger inference-transfer statement and explicit Monte Carlo precision for the 80% recovery and 10% bias gates.

S1 has been revised to v0.4 at \`reviews/analytical-validity-2026-11-18/S1_KNOWN_GAIN_SPEC_2026-11-18.md\`. The revision:
- states that S1 is a synthetic analytical-machinery check, not an empirical test of real solvers;
- states that a pass is compatible with \(C_D\) being useless as a general summary statistic because \(Q\leftrightarrow C_D\) is an error-free bijection;
- defines the limited methodological proceed/revise/stop consequences and says not to run S1 if no such decision will be used;
- marks the 80% learning-recovery and 10% bias tolerances as provisional engineering choices and specifies their Monte Carlo standard errors, intervals, and inconclusive outcomes;
- makes clear that both the positive and matched-null worlds have \(k_{\mathrm{unresolved}}=0\), so the null does not test unresolved-outcome handling;
- labels the proposed S3 as an oracle adjustment for observed \(H\), with imperfect-proxy control potentially requiring another scenario.

DeepSeek's direct assessment of §6 was: "The matched null is adequate as a minimum false-positive companion." It preserves the same diagnostic and parent nuisance structure, but only for a no-unresolved setting. Its direct S3 assessment was: "S3 must demonstrate the incremental information beyond the common cause." These points are recorded in the reviewer ledger.

The 80% and 10% tolerance choices still have no empirical variance basis before a permitted pilot. They remain provisional engineering tolerances, not scientific or decision-theoretic thresholds. Any pilot requires a separate authorization; its replications cannot be pooled with a later confirmatory calibration.

The current specification is v0.4 and awaits direct DeepSeek review. The direct v0.3 review does not freeze v0.4. No generator code has been written, no simulation or model fit has been run, no bank has been reused, and no execution GO has been requested or inferred.


## 16. Design-only state update — 2026-11-18, round 6

DeepSeek directly reviewed S1 v0.4. Its recommendation remained that S1 is defensible as a narrow first-stage machinery check, with no mathematical/statistical defect identified, but it should not be frozen until the downstream decision is named and precision presentation is explicit. DeepSeek accepted the stronger inference-transfer limit and judged the matched null adequate as a minimum false-positive companion because positive and null worlds preserve the same diagnostic and parent nuisance structure. It explicitly recognized that both worlds set \(k_{\mathrm{unresolved}}=0\), so unresolved-outcome handling remains untested.

S1 has been revised to v0.5 at \`reviews/analytical-validity-2026-11-18/S1_KNOWN_GAIN_SPEC_2026-11-18.md\`.

The one-sentence methods decision is: **S1 decides whether the current \(M_0/M_1\) marginal estimator plus test-parent cluster-bootstrap procedure is retained as the candidate method for the S2-S7 validation suite.** If all primary gates pass with the specified Monte Carlo precision, the method is carried forward for S2-S7 specification and review; if a gate fails, the method is revised before that suite is specified around it; if a gate is inconclusive, there is no progression without separately authorized precision work or redesign. This is a methods decision only and has no empirical implication about real-solver correctness.

The v0.5 revision:
- states the positive inference licensed by a complete pass, while retaining the boundary that \(C_D\) may be useless as a general summary statistic;
- displays the recovery-ratio and mean-bias MCSE formulas and their 95% Monte Carlo intervals, with an explicit overlap-is-inconclusive decision rule;
- reports reference false-positive MCSE values separately for each \(J=30,60,120\);
- distinguishes S3a's oracle adjustment for observed \(H\) from S3b's imperfect-proxy adjustment using a prespecified noisy measurement \(W\);
- identifies S6 as a required future unresolved-outcome scenario that is named but not yet specified or frozen.

The direct DeepSeek review said the MCSE formulas and inconclusive rule were not visible in the copy it examined. The v0.4 blob on the review branch already contained those formulas and rules; the record cannot establish whether DeepSeek saw a different copy or overlooked the passages. v0.5 makes them prominent and adds the per-\(J\) false-positive precision table.

DeepSeek's v0.4 recommendation does not freeze v0.5. The next step is direct review of the actual v0.5 text. No generator code has been written, no simulation or model fit has been run, no bank has been reused, and no execution GO has been requested or inferred.


## 17. Design-only state update — 2026-11-19, round 7

DeepSeek directly reviewed S1 v0.5 and concluded that it is defensible as a narrow first-stage machinery check, with no identified mathematical/statistical defect, provided that the project genuinely uses the estimator-selection decision. Its direct assessment was that §6 is adequate as a minimum no-unresolved null; S3b is needed before any feasible-adjustment claim; S6 is correctly named but not yet specified; and no S1 pass validates B1 v1.6 or real-solver concentration claims. DeepSeek did not issue or recommend an execution GO.

S1 has been revised to v0.6 at \`reviews/analytical-validity-2026-11-18/S1_KNOWN_GAIN_SPEC_2026-11-18.md\`.

The pre-execution stop rule is now explicit. S1 is a baseline known-positive recovery check. S2-S7 address distinct threats not represented by S1: matched-null specificity, oracle/imperfect-proxy adjustment, partition sensitivity, crossed dependence, unresolved outcomes, and degenerate/unsupported support. If S2-S7 would proceed unchanged regardless of S1, or would choose an estimator independently, S1 must not be run. A separate owner commitment to use S1's pass/revise/stop result to select the candidate method is required before execution; no such commitment or execution GO is recorded.

The v0.6 precision section states the MCSE and 95% half-width multipliers at 2,000 valid replications, with pilot-based formulas for estimating a confirmatory replication requirement. It makes clear that a numerical replication count cannot be justified without the replication-level standard deviations and the true distance from the decision thresholds. No finite count guarantees a decisive classification at a boundary. A planning pilot requires separate authorization and cannot be pooled into a later confirmatory run.

Review-object provenance was checked by comparing Git blob sources. The v0.5 candidate blob was \`6210f8b95a2f9dbceea3606a7aa1f4dad7cb7e21\`; its v0.4 predecessor was \`dfca5d9f23b1d42557c0ea1fc4a4bdc0cdad5075\`. Their §7.3 sections are byte-for-byte identical and contain the MCSE formulas, intervals and inconclusive rules. The v0.5 per-\(J\) false-positive reference table was added in §7.2. DeepSeek did not provide the Git blob SHA of the exact object it examined, so the review-copy identity remains unconfirmed. A missing-formula defect is not supported by the committed source evidence.

No code has been written, no pilot or confirmatory simulation has been run, no model has been fitted, no bank has been reused, and no execution GO has been requested or inferred.
