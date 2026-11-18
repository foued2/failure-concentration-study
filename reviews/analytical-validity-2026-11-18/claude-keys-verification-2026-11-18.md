# Claude's nine keys: checked against the repository and against the external literature

**Date:** 2026-11-18
**Scope:** the nine numbered claims in the Claude critique that the owner designated as the programme's
fundamental goal (`FUNDAMENTAL_GOAL_ANALYTICAL_VALIDITY_2026-11-18.md`, Appendix A), plus GPT's
concurrence (Appendix B). Each claim is checked twice: against the repository record (local tree,
`master`, and three remote branch tips read with `git show`), and against the external literature that
actually governs the claim.
**What this is not:** it is not a second review, not a redesign, and not an authorization. It adds no
hypothesis of its own except where explicitly labelled *new issue*, and those are flagged as unverified
inference, not findings.
**Repository state:** nothing read was modified; nothing committed. All output is in `airScratch`.

---

## 0. Verdict table

Status vocabulary: **On record** = the repo already contains this, with a citation in §4.
**Verified** = checked in this pass and true. **Partly** = true with a material qualification.
**Contradicted** = the repo says something different. **New** = not in the corpus.

| # | Claude's key | Repo status | Literature geometry | Verdict |
|---|---|---|---|---|
| 1 | W1 was a failed positive control | On record since 2026-11-01 | Simulation-study methodology | **Partly** — the failure is real and was already dispositive; "positive control" is not established |
| 2 | `C` depends on the partition; W1 sign flip proves it | On record | Partition-testing theory + MAUP + multiverse | **Verified** — the most solid key |
| 3 | Effective sample size is the number of solvers; solver variation dominates | Hierarchy on record; dominance **contradicted** | Multilevel / design effect | **Direction right, key premise false, case understated** |
| 4 | Small `k` makes `C` degenerate; "most of the eligible range" barely varies | Discreteness on record; range claim **contradicted** | Hill numbers / Berger–Parker | **Partly** — arithmetic right, scope claim false, bias claim needs a qualifier |
| 5 | No mechanism; test stratum recurrence instead | Repo already formulated this as T1/T3 | **Failure clustering**, not diversity theory | **Correct but not new; not runnable on `C_D`** |
| 6 | Competing explanations; mechanism-disjointness may be unachievable | Confounds on record; last clause **contradicted** | Construct validity + operational profile | **Partly** — and it omits the one comparison the repo mandates |
| 7 | Researcher degrees of freedom | Verified, but two sub-claims **contradicted** | Preregistration / forking paths | **Partly** |
| 8 | Decision value undefined | On record, and worse than stated | Decision curve analysis | **Verified** |
| 9 | Unresolved outcomes bias the denominator | On record as a cell coordinate; bias unanalysed | Missing data / selection bias | **Verified, and the repo's own "fix" adds a new problem** |

**Count:** 2 verified as stated (§2, §8), 1 verified and understated (§3), 4 partly (§1, §4, §6, §7),
1 correct but not new (§5), 1 verified with a new consequence (§9). Zero of the nine is a novel
technical finding about the repository, and the most decisive internal result in the corpus — the
full-vector `F` versus `C` comparison — is missing from the list entirely (§10).

**The single most important repo fact for this whole exercise:** the programme's own third reviewer
recorded a **NO-GO** on 2026-11-01 citing exactly W1 + partition fragility + identification failure:

> "DISPOSITION: CONCUR with NO-GO. Rationale: identification failed by three independent routes; the
> one quantitative test failed small and partition-fragile; construct validity sits upstream of all
> infrastructure."
> — `lc518-150/glm-handoff/worklog.md:262` (`origin/gpt/lc518-claim-b1-primary-2026-11-05`)

and, nine minutes later, that **no route-closure record exists anywhere in the repo**
(`worklog.md`, 2026-11-01 07:10 entry). So Claude's central conclusion is a rediscovery of a
disposition already on record seventeen days earlier, and GPT's framing — "it changes how we should
assess the entire proposed research programme" — understates the situation. The programme had already
been assessed and stopped, in writing, on the eve of the LC518 build. What is new is not the
diagnosis; it is that the work continued without a closure record.

---

## 1. Key 1 — "W1 was a failed positive control"

**Status as of this round:** W1 is a **wiring check**, and its status as a positive control is
**unproven**. The design fixes defect-reach parameters and defines no true value of `Δ_pred`, so the
small result cannot be read as "the method missed a known effect". Both reviewers have withdrawn the
"positive control" label; that withdrawal is recorded in `REVIEWER_RESPONSE_2026-11-18.md`.

**What Claude says.** The three-world simulation (500 trials × 5,000 cases) built a concentration
effect into world 1; the `C` gain was ≈2×10⁻⁶, the interval included zero, and an alternate partition
flipped the sign. "Even where the effect was built in, the statistic didn't recover it."

**Repo.** Every number checks, from `engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md`:

| Quantity | Recorded |
|---|---|
| Eligible cases | 2,499,949; `k=0` = 51 |
| Fixed-`k` overlap | 2,365,022 cases, 49,834 strata, residualised `C` variance 14,737.3 |
| `C` gain, domain | **0.000002**, 95 % `[-0.000001, 0.000008]`, 0.804 positive trials |
| `C` gain, equal | 0.000002, 95 % `[-0.000002, 0.000009]`, 0.754 |
| Alternate partition | **−0.000001**, 95 % `[-0.000003, 0.000003]` (precise: −6.2470×10⁻⁷) |
| Frozen outcome | **`C` survives ... DOES NOT SURVIVE** |

It has since been reproduced by an independent stdlib-only reimplementation — all 2,500,000 records
regenerated field-by-field with zero mismatches, all 36 reference rows matching, worst float deviation
2.5×10⁻¹⁵ (`three_world/independent_w1_glm/INDEPENDENT_W1_VERIFICATION_REPORT.md`). So this is not a
contested number.

**Where Claude overstates.** W1 was specified as a **wiring check**, and the design says so twice:

> "A W1 positive result is a wiring check, not evidence for the real-world hypothesis."
> — `10_THREE_WORLD_SIM_DESIGN.md:17`

> "W1's construction is intended to make `C` informative ... `C` can proxy the number/overlap of
> defects and **may** add predictive value at fixed `k`."
> — same, §60 (emphasis added)

A **positive control** in the methodological sense requires a known true value of the estimand on the
estimand's own scale, so that "recovered" is a measurable distance. The W1 design fixes defect *reach
parameters* — diagnostic `d_h = 0.8`, `d_j = 0.05`; evaluation `e_h = 0.35`, `e_j = 0.03` — and defines
**no true value of `Δ_pred` anywhere**. That is exactly GPT's caveat (Appendix B §1), and the repo
cannot currently refute it: there is no mapping from reach parameters to a target `Δ_pred` in any file.

So the accurate statement is: **W1 is a failed directional wiring check whose injected effect was never
calibrated on the analysis scale.** The practical conclusion Claude draws is nonetheless correct, and
the repo had already drawn it: the pipeline has not been shown to recover an effect it is looking for.

**External literature.** The correct frame is simulation-study methodology, which makes the missing
calibration a formal defect rather than a stylistic one. Morris, White & Crowther's ADEMP structure
requires the data-generating mechanism, the **estimand**, and the performance measures to be declared
together; a scenario whose "truth" is not expressed as a value of the estimand cannot serve as a
positive control (Morris et al. 2019, `10.1002/sim.8086`). For inference algorithms validated against
known truth, simulation-based calibration (Talts et al. 2018, arXiv:1804.06788) is the standard
template; the three-world design lacks its central ingredient, a known posterior/truth.

**Verdict:** partly. The evidence is exact and independently reproduced; "positive control" is not
established — W1 is a wiring check; the practical conclusion is right and was already recorded on
2026-11-01.

---

## 2. Key 2 — partition dependence

**What Claude says.** `C = max_j f_j / k` exists only once the six or eight strata are fixed; the W1
sign flip shows a partition change can reverse the result; freezing is necessary but not sufficient;
partition sensitivity must be reported.

**Repo.** Verified in every part.

- The statistic is stratum-defined: six probe families in v0.2 (`PROTOCOL_V02.md:23`, "six family");
  eight input strata in LC518 (`BANK_DESIGN.md:49`, D1–D8; held-out H1–H8).
- The W1 alternate-partition arm flips the point estimate from +1.96×10⁻⁶ to −6.25×10⁻⁷.
- The programme already treats a frozen partition as insufficient: the formulation note requires a
  feasible-support gate on the diagnostic footprint **before** any held-out score is computed.

**One correction of emphasis.** The flip is of the **point estimate**, not of a significant result:
both intervals include zero (`12_POST_RUN_REVIEW_CORRECTIONS_2026-10-24.md` §49–50). "Reversed the
sign" is literally true and rhetorically stronger than "sign instability between two null estimates".
The correct reading is that the partition arm demonstrates **instability of the point estimate**, which
is enough to require reporting, but is not evidence that the true effect is negative.

**External literature — and Claude points at the right body of work, but names the second-best one.**
Three literatures bear on this, in descending aptness:

1. **Partition testing.** The formal question "does the choice of subdomain partition change what a
   test-based estimate says?" is the core of partition-testing theory: Weyuker & Jeng, "Analyzing
   partition testing strategies", *IEEE TSE* 17(9), `10.1109/32.83906`; Jeng & Weyuker, "Some
   observations on partition testing", TAV3 1989, `10.1145/75308.75314`. Their result is the one that
   matters here: partition choice can change both the estimate and the ranking, and no partition is
   privileged without an argument. This is the correct anchor, because `C` is a subdomain statistic.
2. **Stratified sampling of reliability.** Podgurski, Masri & McCleese, "Estimation of software
   reliability by stratified sampling", *ACM TOSEM* 8(3), `10.1145/310663.310667` — the stratum
   definition is part of the estimator, not a presentation choice.
3. **MAUP / modifiable areal unit problem.** Fotheringham & Wong, *Environment and Planning A* 23(7),
   `10.1068/a231025` — aggregation-zone dependence in multivariate statistics. Correct as an analogy,
   weaker as a citation, since MAUP concerns spatial aggregation of areal units.

**Verdict:** verified, and it is the strongest of the nine. The reportable result is not "the sign
flipped"; it is "the point estimate is partition-unstable across defensible partitions", which is a
measurement-validity statement about the statistic.

---

## 3. Key 3 — solver-level sample size

**What Claude says.** `C` is per solver, held-out correctness is per input, inputs are nested in
solvers, so the effective sample size for `C` is the number of solvers. One clause is added: "the
earlier power work found that solver variation dominates". A 100-solver design therefore has little
power for a 0.01–0.02 nat effect "however many held-out inputs it uses".

**Repo: the hierarchy is right and already accepted; the "dominates" clause is false.**

The fix is on record, accepted 2026-10-31:

> "C4 ACCEPTED, named: crossed RE (generation group / solver / input group / template) primary,
> grouped bootstrap fallback."
> — `glm-handoff/worklog.md:239`

The "dominates" clause is not in the record. The natural-solver power simulation assumes
**ICC ρ = 0.05** and reports: at 12 bodies/cell, power **0.512**; 80 % power for β = 0.06 needs ≈20
effective bodies per cell, 160 per condition (`next-task/10_OFFLINE_POWER_SIMULATION_REPORT_2026-10-22.md`
lines 28–35). The engineered-study power analysis is likewise a fixed SD assumption (0.20), not an
estimated variance. That is a *clustering cost*, not dominance. And there is **no variance-component
decomposition anywhere** in the local tree or the three remote branch tips searched — so the
programme does not know the between-solver variance it is reasoning about.

**Two further corrections Claude needs.**

- **The unit is the parent, not the solver,** for the current design. LC518 supplies 30 parents G01–G30
  in five formulation families (K1×7, K2×8, K3×8, K4×5, K5×2), with five variants each. Variants share a
  parent, so the between-unit clustering level for a `C_D` effect is the parent.
- **M1-si is a within-parent design, and that changes the arithmetic.** M1-si requires ≥2 variants per
  parent with ≥2 distinct `C_D` in one exact cell, precisely to remove the parent effect. A within-parent
  contrast has ≤1 degree of freedom per parent and, as v0.21 itself admits, varies `a(v)` and `C_D`
  together. So Claude's "the effective sample size is the number of solvers" is right for a *between*
  design and does not apply unchanged to the design actually specified — and the specified design has no
  demonstrated power either.

**The arithmetic Claude does not do, which is stronger than his claim.** For a cluster-level covariate
in a random-intercept model with `J` independent units,

  SE(β̂) ≈ σ_u / (sd(C) · √J),   MDE₈₀ ≈ 2.802 · SE  (two-sided α = 0.05)

with σ_u the between-unit residual SD of the outcome. Illustrative values (assumptions stated; **σ_u
and sd(C) are not estimated anywhere in the record**, which is itself a gap):

| σ_u (nats) | sd(`C`) | J = 30 parents | J = 150 variants | J needed for MDE 0.02 |
|---|---|---|---|---|
| 0.20 | 0.25 | **0.409** | 0.183 | ≈ 12,600 |
| 0.05 | 0.25 | **0.102** | 0.046 | ≈ 785 |
| 0.02 | 0.25 | 0.041 | 0.018 | ≈ 126 |

Reading: at the LC518 roster size (30 parents), the minimum detectable cluster-level effect is
**0.10–0.41 nats** on plausible between-unit variation — five to twenty times the highest threshold
the programme ever set (0.02 nats). Even the most favourable row only becomes adequate at ~150
independent units, which is the *variant* count, not the parent count.

**External literature.** The design-effect / effective-sample-size argument is standard:
Austin & Merlo, "Intermediate and advanced topics in multilevel logistic regression analysis",
*Statistics in Medicine* 36(20), `10.1002/sim.7336`; Maas & Hox, "Sufficient sample sizes for multilevel
modeling", *Methodology* 1(3), `10.1027/1614-2241.1.3.86` — both give the result Claude asserts
qualitatively: for a level-2 covariate, precision is governed by the number of level-2 units and the
level-2 variance of the covariate, and level-1 replication cannot repair it.

**Verdict:** the hierarchy is right and already accepted; "solver variation dominates" is contradicted
by the record (ICC 0.05 assumed, no decomposition exists); the quantitative case is materially stronger
than stated, and it lands on the parent count (30), not on 100 solvers.

---

## 4. Key 4 — small-`k` degeneracy

**What Claude says.** `k = 1 ⇒ C = 1`; `k = 2 ⇒ C ∈ {0.5, 1}`; most of the eligible range sits in cells
where `C` barely varies; the maximum of noisy counts is biased upward; the same occupancy problem that
makes the M1-si support rule hard also limits any small-`k` claim.

**Repo: the arithmetic is exact; the scope claim is contradicted; the bias claim needs a qualifier.**

- Arithmetic: six families × five probes ⇒ `C = max_j f_ij / k`; at `k ≥ 25` pigeonhole forces
  `max = 5`, so `C = 5/k` exactly, with zero conditional variation. Verified in v0.2 (1200/1200 rows
  satisfy `C = 5/k`).
- Scope rule, already agreed on 2026-10-31:

  > "Within-k C variation exists 2 ≤ k ≤ 24; ... k = 1 has C ≡ 1 (defined, uninformative for C-effect);
  > k ≥ 25 excluded on the provable zero-conditional-variation ground."
  > — `worklog.md:250` (2026-10-31 10:50 entry)

  So **23 of the 30 k values (2–24) have within-`k` variation**. Claude's "most of the eligible range
  sits in cells where `C` barely varies" is false for the six-family instrument. The degenerate cells
  are `k = 1` and `k ≥ 25`, which the design already excludes.
- Degenerate strata are also handled by construction: `C̃ = C − E[C|k]` means "degenerate strata
  contribute zero by construction" (`worklog.md:239`).
- Bias: valid only if `C` is an **estimator of a latent** dominant-stratum probability. The repo's
  primary estimand is explicitly the **observed** profile, with latent-`C` as a sensitivity:
  "primary estimand = OBSERVED-profile C (application-relevant), latent-C sensitivity via parametric
  bootstrap noise from P itself; attenuation note recorded" (`worklog.md:239`). So "the maximum of
  noisy estimates is biased upward" is true as a statement about estimating `max_j p_j`, and irrelevant
  to the primary estimand as defined. Claude states it unqualified.

**External literature — the right frame is Hill numbers, and it explains *why* small `k` degenerates.**
`C` is the Berger–Parker dominance index (Berger & Parker, *Science* 168(3937), `10.1126/science.168.3937.1345`),
i.e. `C = P_max = 1/ᴺ∞D`, the reciprocal of the **Hill number of order ∞** (Hill, *Ecology* 54(2),
`10.2307/1934352`; Jost, *Oikos* 113(2), `10.1111/j.2006.0030-1299.14714.x`). This is not a curiosity:
of the Hill family, order ∞ is the member most sensitive to the single largest category by construction,
which is exactly why it collapses at small `k` and why it is partition-fragile. `C` is itself not a
Hill number; `1/C` is. The upstream repo correction is precise on this point and should be preserved.

For the bias claim, the correct name is the **winner's curse / selection bias of the maximum**:
Zöllner & Pritchard, *AJHG* 80(4), `10.1086/512821`; and see Barnett, van der Pols & Dobson,
"Regression to the mean", *IJE* 34(1), `10.1093/ije/dyh299`. Again: these apply to estimating an
extreme latent parameter, not to a descriptive statistic of the observed sample.

**Verdict:** partly. Exact arithmetic, wrong scope claim, unqualified bias claim. The Hill-number
framing is the correct external literature and it *supports* the discreteness point more sharply than
the generic "bias" framing does.

---

## 5. Key 5 — "no mechanism; test stratum recurrence"

**What Claude says.** No mechanism explains why dominance should transfer, so a positive result would
be a correlation with an index. The testable mechanism: if one defect class drives the failures, its
errors should recur on held-out inputs **in the same stratum**. Held-out failures should cluster in the
dominant stratum specifically; if they do not, the concentration story is wrong even when `C` correlates
with error rate.

**Repo: this is already the programme's own leading theory, and it is already explicitly *not* a
finding.** On 2026-11-01 the third reviewer wrote out three candidate theories, marked
"interpretive-not-findings":

> "**T1 mechanism-identity theory** (transfer content of F is label-indexed; W1 record consistent: F
> gain ~23% vs C gain ~0.06% in the wired world; engineered audit's identity-matching failure
> consistent-not-demonstrative). **T2 family-difficulty artifact** (deflationary null; W3 proxy
> caution; honest central statement: T1 vs T2 unseparated in nature). **T3 identity-free/identity-indexed
> mismatch** (C = max_j f_j / k is family-label-permutation-invariant; the estimand is label-indexed →
> any label-free functional acts only via the difficulty channel or a contingent association requiring
> within-k variation (absent: C=5/k) — compression asymmetry is STRUCTURAL, not accidental; scope
> boundary preserved: not a universal impossibility). Each theory carries its falsifier."
> — `worklog.md:285`

Claude's proposal is **T1 restated as a stratum-level prediction**, and T3 is the reason to expect it:
the estimand is indexed by *which* category fails, while `C` is invariant to relabelling those
categories. That is a sharper statement of Claude's point than Claude gives, and it is already in the
record.

Two blockers, both repo-internal:

1. **The current `C_D` cannot carry the test.** The LC518 strata are input categories, and the
   analysis spec says so unambiguously:
   > "The eight strata are not eight proven causal mechanisms. ... The eight diagnostic strata are
   > input categories, not verified mechanisms. `C_D` is not a defect-localization measure."
   > — `lc518-150/review-v1.2/analysis-revision-2026-11-02/ANALYSIS_SPEC_REVIEW_DRAFT.md:62, 302`

   A "dominant diagnostic stratum" is therefore the input category where a solver fails most, not the
   defect class driving the failures. Claude's mechanism test needs a **defect-class** partition, which
   does not exist anywhere in the bank design.
2. **T1 versus T2 is unseparated.** The deflationary rival — a family-difficulty artefact — predicts the
   same sign and is not excluded by any executed analysis. Claude's proposal would separate them, which
   is its real value, but it does not thereby confirm T1.

**External literature — and here Claude points at the wrong body of work.** The right frame is
**failure clustering**, not diversity theory:

- Dickinson, Leon & Podgurski, "Finding failures by cluster analysis of execution profiles", ICSE 2001,
  `10.1109/ICSE.2001.919107`.
- Almaghairbe & Roper, "Separating passing and failing test executions by clustering anomalies",
  *Software Quality Journal* 25, `10.1007/s11219-016-9339-1` — whose stated hypothesis is almost
  verbatim Claude's: **"failures will group into small clusters, whereas passing executions will group
  into larger ones."**
- Podgurski, Masri & McCleese, *ACM TOSEM* 1999, `10.1145/310663.310667` (stratified reliability
  estimation).
- For defect concentration specifically: Fenton & Ohlsson, *IEEE TSE* 26(9), `10.1109/32.879815`;
  Ostrand, Weyuker & Bell, *IEEE TSE* 31(4), `10.1109/TSE.2005.49`.

The repo's own register already classifies this dimension as **"heavily developed prior art"**
(`worklog.md`, 2026-10-31 10:06 entry). Diversity theory tells you what the statistic does; it says
nothing about transfer. Failure clustering is the literature that has actually tested transfer, and it
is where Claude's proposal would land.

**Verdict:** correct science, not new, already present as T1, blocked by the fact that `C_D`'s strata
are input categories rather than defect classes, and pointed at the wrong literature in Claude's
framing.

---

## 6. Key 6 — competing explanations

**What Claude says.** A defect causing both diagnostic failures and held-out errors would make `C` look
predictive without a concentration effect; holding `k` and occupied strata fixed helps but does not
rule it out; the test must check whether diagnostics and held-out inputs were generated by the same
process; and "the record says mechanism-disjoint held-out populations may not be achievable".

**Repo: the confound is real and recorded; the quoted clause does not exist; and the key omits the
comparison the repo makes mandatory.**

- Confound recorded: `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` §1.3 and §5, quoted in §0 above.
- The last clause is **contradicted**: `git grep` over the local tree and three remote branch tips
  finds no statement about mechanism-disjointness being unachievable. The only near-hits are
  "operationally achievable" in feasibility protocols. What the record actually requires is
  **input-cluster disjointness** — held-out clusters "independently constructed from, and disjoint
  from, the diagnostic clusters" (formulation note §7), which is a different and weaker condition.
- **Logical error.** Claude writes: "Conditioning on the entire failure vector is impossible for this
  purpose because it determines `C_D`." True. But the repo does not ask for `F` as a *control*; it asks
  for `F` as a *predictive comparator*:

  > "**Compare `C` with the full vector `F`.** Because `C` is a summary of `F`, a claim that `C` is the
  > better representation is not available in principle. The empirical question is whether the summary
  > is useful under a fair, finite-sample predictive comparison."
  > — `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` §6 condition 6

  Conditioning and comparing are different operations. Claude's sentence rules out the first and
  thereby (unintentionally) omits the second, which is the decisive one. See §10.

**External literature.** Construct validity is the governing framework: Cronbach & Meehl, "Construct
validity in psychological tests", *Psychological Bulletin* 52(4), `10.1037/h0040957`. For the "same
generation process" concern, the relevant standard is the **operational profile**: Musa, "Operational
profiles in software-reliability engineering", *IEEE Software* 10(2), `10.1109/52.199724`. Evaluating on
the same operational profile is the *normal* and usually *required* practice for reliability claims;
"mechanism-disjoint held-out population" is not a standard construct in software engineering and would,
if enforced, break the operational-profile guarantee the rest of the design relies on. The correct
statement is the weaker one the repo already makes: the claim is benchmark-bound.

**One confound Claude omits, and the literature names it: coincidental correctness.** A solver can pass
a held-out input for the wrong reason, and can fail a diagnostic probe for a reason unrelated to the
defect class being counted. Both attenuate or distort `C`'s apparent predictive value and are
uncorrelated with the "shared defect" confound Claude lists. It is the standard objection in
spectrum-based fault localisation and it applies directly to a bank of 64 diagnostic records.

**Verdict:** partly. Real confound, one invented clause, one logical conflation, and one missing
confound.

---

## 7. Key 7 — researcher degrees of freedom

**What Claude says.** Six reformulations, thresholds 0.01 / 0.02 / 0.04 nats, unresolved knot and
tertile choices, two research lines; any positive finding would have a multiplicity problem unless one
primary analysis is fixed in advance.

**Repo: the count and the thresholds are right; the "unresolved knot and tertile" clause is
contradicted.**

- Six formulations: confirmed (succession audit §1).
- Thresholds: `δ = 0.01` nats (v0.2 `PROTOCOL_V02.md:65`), `d* = 0.020273255405408218`,
  `2δ* = 0.040546510816436` (`v03p/VDRAFT_Target_Bridge...` §0.2).
- Knots are **not unresolved**. Two sets, both frozen pre-outcome:
  `{2, 8, 16, 24}` ("frozen pre-data", `worklog.md:239`) and the sensitivity basis
  `{1, 2, 3, 4, 8, 16, 32, 48}` ("fixed pre-outcome design conventions",
  `ANALYSIS_SPEC_REVIEW_DRAFT.md:5`).
- The tertile is likewise pre-registered: the supported cell is `k × within-k C-tertile`, fixed in C3
  (`worklog.md:239`).
- There is also an explicit hygiene rule: "Claude 90% power/thresholds INVALIDATED; GPT V1/V3/0.80
  feasibility numbers historical+moot" (`worklog.md:264`). The programme has already retired the
  numbers Claude is now citing.

**The sharper statement Claude almost makes.** The six reformulations are **sequential and
outcome-dependent** — each is conditioned on the previous result. That is adaptive design / optional
stopping, not a family of simultaneous tests, and a multiplicity correction does not repair it. The
remedy is one prospectively registered primary analysis, with the entire sequence disclosed, exactly as
GPT says (Appendix B §5).

**External literature.** Preregistration: Nosek, Ebersole, DeHaven & Mellor, *PNAS* 115(11),
`10.1073/pnas.1708274114`. The "garden of forking paths" — the correct name for the problem when the
analyst does not consciously select — is Gelman & Loken, "The statistical crisis in science",
*American Scientist* 102(6), `10.1511/2014.111.460`. Multiverse analysis: Steegen, Tuerlinckx, Gelman &
Vanpaemel, *Perspectives on Psychological Science* 11(5), `10.1177/1745691616658637`. Specification
curve: Simonsohn, Simmons & Nelson, *Nature Human Behaviour* 4, `10.1038/s41562-020-0912-z`.

Note also that the LC518 `E3` arm already disclaims confirmatory status — "one frozen pass,
NOT_ESTIMABLE, exploratory-only, no δ/LCB/p-values" (`ANALYSIS_SPEC.md`, summarised at
`worklog.md:339`) — so the multiplicity problem, for that arm, is not latent; it is declared.

**Verdict:** partly. Right about the sequence; wrong that knots and tertiles are unresolved.

---

## 8. Key 8 — decision value

**What Claude says.** Even a real gain has to matter for a decision; B1 already performs accept/reject;
whether ranking rejected solvers helps is the question; a minimum effect defined in decision terms, not
nats, has not been set.

**Repo: verified, and the repo concedes more than Claude claims.**

> "Threshold d | 0.01 nats mean log-loss per hidden input — **a protocol choice, no decision-shift
> equivalence claimed**"
> — `v02/PROTOCOL_V02.md:65`

So the programme itself states that δ has no decision interpretation. For LC518 the situation is
weaker still: the analysis spec has **no δ, no lower confidence bound, no p-values**, and is
"exploratory-only, NOT_ESTIMABLE". There is not merely an unset decision threshold; there is no
inferential threshold in the current line at all.

**External literature.** The right tool is decision curve analysis / net benefit: Vickers & Elkin,
*Medical Decision Making* 26(6), `10.1177/0272989X06295361`. The argument is exactly Claude's: a model's
value is the net benefit of the decisions it changes at a specified threshold probability, and
log-loss/nats do not map onto that without an explicit utility model. The clinical-trials analogue is
the minimal important difference; the general principle is that "statistically detectable" and
"decision-relevant" are separate specifications.

**Verdict:** verified. This is the second of the two keys that survives as stated.

---

## 9. Key 9 — unresolved outcomes

**What Claude says.** If unresolved outcomes correlate with held-out error, excluding them from `k`
changes both `C` and the outcome.

**Repo: verified as a structural risk, and the repo's own remedy creates a second problem.**

- `C_D`'s denominator is `k_fail` only; `k_unresolved` is a separate coordinate.
- B1's support rule conditions on the exact `(mechanism, family, k_fail, k_unresolved)` cell with no
  pooling — so unresolvedness is **not** silently dropped, which is what Claude asks for.
- But the spec also contains the honest caveat that `C_D = 0` at `k_fail = 0` is "a computational
  convention labelled NO OBSERVED FAILURES. It is not a measured concentration of zero"
  (`ANALYSIS_SPEC_REVIEW_DRAFT.md:51`).

**Two consequences the key does not reach.**

1. **Exact-cell conditioning is not the same as "keeping `k_unresolved` explicit".** It conditions the
   analysis on `U`. If unresolvedness shares a cause with held-out error other than defect severity,
   `U` is a collider and the exact-cell restriction induces selection bias. If `U` is only a proxy for
   severity, it is a control and helps. The corpus states no causal diagram, so it cannot say which.
2. **Differential unresolvedness across strata biases the max directly.** `f_j` counts only definite
   failures. A stratum with more unresolved records has a systematically understated `f_j`, so `C_D`'s
   maximum is pushed toward strata with fewer unresolved outcomes. That is a bias in the *predictor*,
   independent of the outcome, and no document analyses it.

**External literature.** Missing-data mechanisms: Sterne, White, Carlin et al., *BMJ* 338:b2393,
`10.1136/bmj.b2393`. Selection bias as a structural (DAG) problem: Hernán, Hernández-Díaz & Robins,
*Epidemiology* 15(5), `10.1097/01.ede.0000135174.63482.43`. Conditioning on a collider:
Elwert & Winship, *Annual Review of Sociology* 40, `10.1146/annurev-soc-071913-043455`.

**Verdict:** verified. The new consequence is that the repo's fix is a different intervention than the
one Claude asks for, and it has not been analysed either way.

---

## 10. What the nine keys omit — and it is the most important thing in the corpus

### 10.1 The `F` versus `C` comparison

Claude's key 6 says conditioning on the full vector is impossible, and stops. The repo instead ran the
comparison, and it is the strongest internal result about `C`:

| Comparison (W1, domain score) | Mean | 95 % interval |
|---|---|---|
| `C` gain over `M0+fam` | **+1.961×10⁻⁶** | `[−1.242×10⁻⁶, +7.581×10⁻⁶]` |
| Full vector `F` over `C` | **+7.90×10⁻⁴** | `[+6.92×10⁻⁴, +8.86×10⁻⁴]` |

Against a full-cohort baseline of 0.004193, that is roughly **0.05 % relative gain for `C` and 18.8 %
for `F`** — about 400× in relative terms, and two intervals that do not overlap. The programme's own
summary is "full vector F beats C summary by ~3 orders of magnitude of relative gain in every
predictive setting: 23 % W1-domain, 25–35 % mixtures vs 0.06 %" (`worklog.md:266`).

**This must be stated with its qualification**, because it is easy to over-read: in W1 the `F`-versus-`C`
criterion is **domain PASS, equal FAIL**, and the overall verdict is FAIL. `F` does not win under every
score. But two facts survive: `C` carries essentially none of the predictive gain that `F` carries under
the same folds, and the repo's construct-validity assessment made this comparison mandatory (condition
6). Any critique of the programme that omits it is answering a weaker question than the one the record
already answered.

External anchor: this is the standard **data compression / sufficiency** question. If `C = g(F)` is a
deterministic summary, the test of `C` is whether `g` is an *approximately sufficient* statistic for the
prediction task — not whether `C` "adds information beyond `k`". The repo's `worklog.md:285` names the
same thing as T3.

### 10.2 The unit of transfer

Claude never says whether the claim is about *held-out solver bodies* or *held-out instances under one
fixed pack*. The repo treats this as a precondition:

> "**Declare the unit and population.** State whether the claim is about held-out solver bodies or
> held-out instances under a fixed pack. Do not mix the two."
> — `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` §6 condition 1

and the third reviewer listed it as the missing fourth column of Claude's own sheet:
"fourth column for Claude's sheet: unit of transfer (held-out solver bodies vs instances)"
(`worklog.md:266`). Without it, key 5's prediction is not well-formed: "errors recur in the dominant
stratum" means different things when the unit is a solver body versus a set of instances.

### 10.3 No power analysis on the estimand's scale

The power simulations in the corpus model a **probability** effect (`p(k,C) = p_k + β(C − mid)`,
β ∈ {0.03 … 0.20}, Binomial(200, p), ICC ρ) — not a log-loss effect in nats
(`10_OFFLINE_POWER_SIMULATION_REPORT_2026-10-22.md` lines 73–77). The engineered-study analysis models a
boundary **score** with residual SD 0.20. The programme's thresholds are in nats. No power calculation in
the corpus is expressed on the estimand's own scale, which is a stronger statement than "power is low".

---

## 11. Where Claude's list is genuinely useful

Despite the above, three things in the critique are additive and should not be lost:

1. **It names five methodological literatures the project never searched.** The repo's literature
   register is 20 entries, entirely *domain* (failure clustering, defect prediction, code LLM
   correctness). It contains nothing on partition dependence, multilevel power, winner's curse,
   decision value, or selection bias. The novelty gate was run as a domain question; the critique is a
   *methodological* question, and on that axis the project has no register at all.
2. **It separates measurement from detection.** The repo's construct-validity §6 lists ten conditions,
   but they are not ordered as a dependency chain. Claude's four-gate ordering (measurement → mechanism
   → identification → detection) is a genuine improvement in presentation, and GPT's ordering of it is
   correct.
3. **It states the transfer prediction in falsifiable form.** Even though it is T1 restated, writing it
   as "held-out errors cluster in the dominant stratum" makes it testable in a way the corpus's prose
   does not.

---

## 12. Corrections ledger

Every place where a Claude number or clause does not match the record, with the record's version:

| Claude's statement | Record | Severity |
|---|---|---|
| "alternate partition flipped the sign ... −1×10⁻⁶" | −6.2470×10⁻⁷, 95 % `[−3.4517×10⁻⁶, +3.1384×10⁻⁶]`; table rounds to −1×10⁻⁶ | cosmetic |
| "world 1 was built to contain a concentration effect" | Built to contain defect-reach asymmetry; no `Δ_pred` truth defined | material |
| "the earlier power work found that solver variation dominates" | ICC ρ = 0.05 assumed; no variance decomposition exists | **false** |
| "most of the eligible range sits in cells where C barely varies" | Within-`k` variation exists 2 ≤ k ≤ 24; degenerate only k=1 and k≥25 | **false** |
| "the max of noisy estimates is biased upward" | True for latent `p_max`; primary estimand is observed-profile `C` | needs qualifier |
| "the record says mechanism-disjoint held-out populations may not be achievable" | No such record in local tree or 3 remote tips; requirement is input-cluster disjointness | **unsupported** |
| "unresolved knot and tertile choices" | Knots `{2,8,16,24}` and `{1,2,3,4,8,16,32,48}` frozen pre-outcome; tertile cell pre-registered | **false** |
| "100 solvers ... little power for a 0.01–0.02 nat effect" | Correct in direction; the operative count is 30 parents; MDE ≈0.10–0.41 nats | understated |
| "the record says six or eight strata" | Correct, but they are different objects: six probe families vs eight input categories; `C_D` is not mechanism concentration | needs care |
| "positive control" | Repo term is "wiring / positive-direction interval criterion" | label |

---

## 13. External literature: correct list, with verification status

All DOIs below were resolved against Crossref in this pass unless marked. Nothing here is cited from
memory alone.

**Statistic and its properties**

| Reference | DOI | Use here |
|---|---|---|
| Berger & Parker 1970, *Science* 168(3937):1345–1347 | `10.1126/science.168.3937.1345` | `C` is the BP dominance index |
| Hill 1973, *Ecology* 54(2):427–432 | `10.2307/1934352` | `1/C` = Hill number of order ∞ |
| Jost 2006, *Oikos* 113(2):363–375 | `10.1111/j.2006.0030-1299.14714.x` | why order ∞ is the fragile member |

**Partition and strata**

| Reference | DOI | Use here |
|---|---|---|
| Weyuker & Jeng 1991, *IEEE TSE* 17(9) | `10.1109/32.83906` | partition choice changes estimates; correct anchor for key 2 |
| Jeng & Weyuker 1989, TAV3 | `10.1145/75308.75314` | same, earlier |
| Podgurski, Masri & McCleese 1999, *ACM TOSEM* 8(3) | `10.1145/310663.310667` | stratified reliability estimation; strata are part of the estimator |
| Fotheringham & Wong 1991, *EPA* 23(7) | `10.1068/a231025` | MAUP analogy |

**Mechanism and failure structure**

| Reference | DOI | Use here |
|---|---|---|
| Dickinson, Leon & Podgurski 2001, ICSE | `10.1109/ICSE.2001.919107` | failure clustering |
| Almaghairbe & Roper 2016, *SQJ* 25:803–840 | `10.1007/s11219-016-9339-1` | "failures group into small clusters" — Claude's key 5 verbatim |
| Fenton & Ohlsson 2000, *IEEE TSE* 26(9) | `10.1109/32.879815` | defect concentration in real systems |
| Ostrand, Weyuker & Bell 2005, *IEEE TSE* 31(4) | `10.1109/TSE.2005.49` | defect clustering and prediction |
| Musa 1993, *IEEE Software* 10(2) | `10.1109/52.199724` | operational profile; same-profile evaluation is standard |

**Design, power, multiplicity**

| Reference | DOI | Use here |
|---|---|---|
| Morris, White & Crowther 2019, *Stat Med* 38(11) | `10.1002/sim.8086` | ADEMP; positive control needs truth on the estimand scale |
| Austin & Merlo 2017, *Stat Med* 36(20) | `10.1002/sim.7336` | level-2 covariates; number of clusters governs precision |
| Maas & Hox 2005, *Methodology* 1(3):86–92 | `10.1027/1614-2241.1.3.86` | sufficient cluster counts |
| Nosek et al. 2018, *PNAS* 115(11) | `10.1073/pnas.1708274114` | preregistration |
| Gelman & Loken 2014, *American Scientist* 102(6) | `10.1511/2014.111.460` | garden of forking paths |
| Steegen et al. 2016, *PPS* 11(5) | `10.1177/1745691616658637` | multiverse reporting |
| Simonsohn et al. 2020, *Nat Hum Behav* 4 | `10.1038/s41562-020-0912-z` | specification curve |
| Talts et al. 2018, arXiv:1804.06788 | arXiv (no Crossref DOI) | simulation-based calibration |
| Cronbach & Meehl 1955, *Psych Bull* 52(4) | `10.1037/h0040957` | construct validity |

**Bias, missingness, decision**

| Reference | DOI | Use here |
|---|---|---|
| Zöllner & Pritchard 2007, *AJHG* 80(4) | `10.1086/512821` | winner's curse for a maximum |
| Barnett, van der Pols & Dobson 2005, *IJE* 34(1) | `10.1093/ije/dyh299` | regression to the mean |
| Hernán, Hernández-Díaz & Robins 2004, *Epidemiology* 15(5) | `10.1097/01.ede.0000135174.63482.43` | selection bias as structure |
| Elwert & Winship 2014, *Annu Rev Sociol* 40 | `10.1146/annurev-soc-071913-043455` | conditioning on a collider |
| Sterne et al. 2009, *BMJ* 338:b2393 | `10.1136/bmj.b2393` | missing-data mechanisms |
| Vickers & Elkin 2006, *Med Decis Making* 26(6) | `10.1177/0272989X06295361` | decision curve / net benefit |

**Two references deliberately omitted.** Hamlet & Taylor's "Partition testing does not inspire
confidence" is the natural companion to Weyuker & Jeng, but no DOI could be resolved in this pass and
a guessed identifier is worse than no identifier. Magurran's *Measuring Biological Diversity* is the
standard text on sample-size sensitivity of dominance indices, but it has no DOI; cite as a book if
needed.

---

## 14. Bottom line

1. **Two keys survive as written:** partition dependence (§2) and decision value (§8). One survives and
   is understated (§3). One survives with a serious new consequence (§9).
2. **One key is correct science but not new and not runnable as stated (§5).** It is the repo's own T1,
   blocked because `C_D`'s eight strata are input categories, not defect classes.
3. **Three keys contain a false premise:** "solver variation dominates" (§3), "most of the eligible
   range barely varies" (§4), "knots and tertiles unresolved" (§7). One contains an invented record
   citation (§6).
4. **The most important omission is not in the list at all:** the `F`-versus-`C` comparison, where `C`
   carries ~0.05 % relative gain against `F`'s ~19 % under the same folds in W1, with the qualification
   that `F` wins on domain and fails on equal. Claude's key 6 rules out the *wrong* operation
   (conditioning on `F`) and thereby skips the right one (comparing against `F`).
5. **The diagnosis is not new.** The repo recorded a NO-GO on 2026-11-01 on exactly these grounds, and
   recorded that no closure record was ever created. The scientific position in the two appendices is
   correct; its novelty is a function of how much of the programme's own record was read.
6. **What is genuinely new in the critique is methodological, not empirical.** It names five literatures
   the project never searched — partition theory, multilevel power, winner's curse, decision value,
   selection bias — and on those axes the repo is exposed. That is the durable contribution, and it is
   the part that should go into the register.

**What this document does not establish.** It does not show that `C` has no predictive value; the one
executed comparison is synthetic, and its injection correspondence is still unverified. It does not
show the analysis is broken; it shows the analysis has never been shown to work, which the repo already
said. It does not adjudicate T1 against T2. And it adds nothing to the record beyond the arithmetic in
§3 and the two consequences in §9, both of which are labelled as inference, not findings.

---

## 15. Files and refs relied on

| Source | Use |
|---|---|
| `engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md` | W1 table, criteria, overlap |
| `.../12_POST_RUN_REVIEW_CORRECTIONS_2026-10-24.md` | precise partition values, sign-flip scope |
| `.../independent_w1_glm/INDEPENDENT_W1_VERIFICATION_REPORT.md` | bit-exact independent reproduction |
| `engineered-study/math/10_THREE_WORLD_SIM_DESIGN.md` | W1 reach parameters; "wiring check" wording; `Δ_pred` |
| `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` | §1.3, §5, §6 conditions 1/3/5/6/8 |
| `v02/PROTOCOL_V02.md` | six families; δ = 0.01 nats; "no decision-shift equivalence" |
| `next-task/10_OFFLINE_POWER_SIMULATION_REPORT_2026-10-22.md` | ICC 0.05; β on probability scale |
| `lc518-150/glm-handoff/worklog.md` (remote) | NO-GO 11-01; T1/T2/T3; k-range rule; knots; crossed RE; compression asymmetry |
| `lc518-150/glm-handoff/BANK_DESIGN.md` (remote) | 64/80 records; 8 strata; no-power statement |
| `lc518-150/review-v1.2/analysis-revision-2026-11-02/ANALYSIS_SPEC_REVIEW_DRAFT.md` (remote) | strata are input categories; knots; `C_D` convention |
| `lc518-150/review-v1.2/AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` (remote) | exact-cell support rule |
| `git grep` over `origin/review/concentration-formulation-2026-10-25`, `origin/gpt/lc518-claim-b1-primary-2026-11-05`, `origin/gpt/lc518-m1si-audit-2026-11-17` | negative check for "mechanism-disjoint" |
| Crossref REST (`api.crossref.org`) | DOI resolution for every reference in §13 |
