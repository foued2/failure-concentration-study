# Zero-generation decision engine — specification v1 (draft for review)

Status: TEMP design document for reviewer/owner disposition. No repository change, no
publication, no solver generation. The named computations in section 7 (NC1-NC5) have
NOT been run; they require an explicit named authorization under the pre-freeze
computation policy. Every assumption is labelled verified / unverified / [decide].
Amended 2026-10-17 after GPT review: NC1 is gate-conditioned (not unconditional);
NC2 absorbs the controlled null/alternative calibration (Type I error and power)
against the prespecified evaluation procedure; outputs are labelled as calculations
under the reference model only. Amended again 2026-10-17 after further review:
per-gate-stage NC1 tables; per-scenario and per-rule reporting; explicit split of
arithmetic reproduction vs empirical calibration with provenance labels; no
post-hoc selection of thresholds or rules; review checkpoint before NC3-NC5.
Amended again 2026-10-17 after Claude review: pre-run calibration criteria F1-F5
(tolerance bands for Type I and for heuristic-vs-calibrated agreement, stated
consequences, forking-paths guard, proposed default freeze of D2/D3); provenance
tagging required for every reported quantity.
Amended again 2026-10-17 after GPT independent review (targeted amendment, three
blocking issues): permutation strata fixed to k-ONLY with a no-variation reporting
rule and solver-vector permutation unit; exchangeability assumption stated; outcome
model declared bounded by construction (baselines, dependence, no clipping);
c*_calibrated operationally defined with a monotonicity gate; NC1 conditions on
explicit M3 threshold variants. Ledger gains U7-U9.
Amended again 2026-10-17 after Claude review round 2: F2(a) now carries its derived
expectation (Phi(2.5 - 1.96) = 0.705) and declared aggregation weights (O-2
qualifying probabilities); U9 tolerance fixed at 0.02 absolute; achievable size per
configuration reported (F1); permutation-DP verified against brute-force enumeration
(section 4); U7 scope limit stated in section 8; scale-presentation rule added to F5.
Amended again 2026-10-17 after GPT review round 2: F2(a) band labelled as a
PRESPECIFIED ENGINEERING TOLERANCE with recorded rationale (not a mathematical
consequence; discreteness is measured, not assumed); F2(b) aggregation operationalized
as the weighted conditional-power curve Pi(t) over threshold-selection sets S(t);
NC1 adds the pre-concentration-threshold stage (M3 rank only) as a full table.
Author: GLM (implementation agent), 2026-10-17. Basis: A1 rev 3 (f69cc9b), O2 package
rev 2 (4d7517a), M3 addendum Rev d (c70a387), all read-only.

## 1. Purpose

Determine, before any generation spend, whether the concentration hypothesis is
testable under the approved design, at what sample size and cost:
- the distribution of residual concentration variation c the design can actually give;
- the probability of passing the O2 and M3 gates;
- conditional power of the intended predictive comparison (k alone vs k + C);
- minimum detectable effect vs N; attempts-to-qualification cost curve.

## 2. Definitions and the definition check (GPT caveat)

Design column and statistic (M3 addendum Rev d, exact):
    r = (I - P_D) C (unscaled residual), x = r / s_ref, s_ref = 0.12703,
    c = r'r / s_ref^2 = x'x   (raw residual SS divided by s_ref^2 exactly once).
Attainable C levels (A1 CK enumeration): k=5 -> {0.2,0.4,0.6,0.8,1.0};
k=10 -> {0.2,0.3,0.4,0.5}. Floor c_floor(t) = delta_k^2 (t-1)/t / s_ref^2;
ceiling c_ceil(t) = R_k^2 floor(t^2/4)/t / s_ref^2.

Candidate information threshold (M3 addendum):
    c* = (sigma_max * z_req / beta_min)^2,  beta_min = y-units per one reference sd of C.
Definition check performed now (arithmetic, no new computation):
    sigma_max = 0.5, z_req = 2.5 -> sigma_max * z_req = 1.25;
    beta_min .20 -> c* = 39.06; .10 -> 156.25; .05 -> 625.00
    (published 39.1 / 156.3 / 625.0 = same numbers, rounded).
So c and c* DO share one definition of c and one scale for beta_min. What is NOT
established: (a) c* derives from a first-order variance/SE heuristic (Var(beta_hat) =
sigma^2/c under body-level iid errors), not from the actual stratified evaluation
statistic; (b) the illustrative expected c ~ 64 at (k=5, t~40), computed in the M3
probe, is a single unconditional illustrative point, not a gate-conditioned
distribution. GPT's caveat is accepted verbatim: the comparison c vs c* is a
feasibility hypothesis to be measured, not a result.

## 3. Decision surface (engine outputs)

O-1  c-distribution surface: exact distribution of residualized C (c) over admissible
     count patterns and C-value assignments, per (k, t) and pooled, shown step by step
     along the cumulative qualification chain (no-gate baseline, +support, +TrainRa,
     +CVD = O2 event, +M3, +test gates) so that the effect of each gate on the c
     distribution is visible, separately for each prespecified O2 scenario.
O-2  Gate-conditioned composition distribution: exact distribution of qualifying
     datasets (O2 event and M3 criteria) over N in {113,150,450,600} and scenarios
     {a-hist, a-50:50, c-hist, c-50:50} (extending the O2 enumeration).
O-3  Conditional power: power of the frozen evaluation rule, averaged over datasets
     that actually qualify (weighted by O-2 probabilities), vs N and beta_min.
O-4  Minimum detectable effect vs N at fixed power (0.8 nominal), and the P(qualify
     and power >= x) surface.
O-5  Attempts-to-qualification cost curve: expected generation attempts to reach a
     qualifying confirmatory design as a function of (validity rate, duplication rate
     rho, usable-range rate, support rate), with rho = 0.25 and pilot-updatable.
O-6  Pipeline validation: null calibration (Type I error) and known-effect recovery
     under injected effects. Core of this is inside NC2 (controlled null/alternative
     cases); NC5 retains the larger deferred validation. Machinery validation only,
     not evidence about nature.

## 4. Evaluation rule to be specified and frozen (not yet frozen)

- Unit: solver body (its training-block C and k); outcome: the complete solver-level
  test-block correctness vector (per-test-body outcomes, preserving within-solver
  dependence); summary ȳ_i = mean correctness over its te eligible test bodies.
- Comparison: model {k} vs model {k, C} on unseen inputs. Primary scale (i): absolute
  change in test-correctness rate per one reference sd of C. beta_min applies only to
  scale (i). Candidates (ii) extreme-strata mean difference and (iii) logistic
  likelihood-ratio improvement are sensitivity reporting only, have different units,
  and are not interchangeable with (i).
- Strata definition (GPT issue 1). Primary stratification is by k ONLY (k=5 and k=10).
  No stratum may be defined by the failure count vector, its partition, its maximum,
  or any function that determines C: such strata leave C constant within stratum and
  blind the test to the incremental effect. Explicit check: NC2 must verify, for each
  analyzed configuration, that at least two distinct attainable C levels remain within
  every stratum; if not, the configuration is reported NON-TESTABLE and no method
  switch occurs silently.
- Permutation procedure. Exact stratified permutation of C values (equivalently x)
  across solver labels within each k-stratum; permutation unit = the complete
  solver-level outcome vector, so within-solver dependence is preserved. Stated
  exchangeability assumption under H0: conditional on k, solver outcome vectors are
  exchangeable regardless of C; the M3 residual x = r/s_ref absorbs count-pattern
  information linearly, but exchangeability itself is an assumption (U7).
- Statistic. T = sum_s sum_i (x_i - xbar_s)(ybar_i - ybar_s) (stratified
  slope-equivalent, correctness-rate units per reference sd of C); observed effect
  beta_hat = T / sum_s sum_i (x_i - xbar_s)^2. Two-sided exact p-value:
  P_null(|T_perm| >= |T_obs|); nominal alpha = 0.05; exact rejection probabilities
  and denominators reported (F1).
- Exactness. The null distribution of T is computed exactly by dynamic programming
  over permutations of the x-multiset within strata (few distinct x levels), not by
  resampling; seeded MC is only a declared fallback where exact DP is infeasible,
  with reported simulation error. The DP implementation is verified against
  brute-force full permutation enumeration at small configurations before use.
- Pilot/confirmatory separation: pilot outcomes never enter confirmatory inference.

## 5. Engine architecture (stdlib-only, deterministic)

- A1 imported read-only through the pinned absolute path (same convention as O2).
- Exact composition enumerator: summary counts (k, C-level pattern, tra, te) via
  dynamic programming, extending the O2 machinery; verified against brute force at
  N=113/150 before use at N=450/600 (blowup mitigation, see risk R1).
- Gate simulator: S1(4) support, TrainRa, CVD (both readings), M3 rank+variance
  criteria, test gates (>=1 per bucket, >=8 total). O2 event bytes unchanged; this is
  a new read-only computation referencing the frozen package.
- Working outcome model for O-3 and NC2 (declared, bounded by construction, NO
  post-hoc clipping) (GPT issue 2, U8):
  Primary family (linear-in-probability; matches scale (i)):
      P(correct | solver i, evaluation j) = a_k + beta * x_i,
  declared baseline profiles a_k in {0.40, 0.50, 0.60} (symmetric across buckets)
  plus one declared asymmetric sensitivity profile (a_5, a_10) = (0.50, 0.60);
  beta in {0.20, 0.10, 0.05} = beta_min per reference sd of C. Every declared
  (a_k, beta, x-range) combination must satisfy a_k + beta * x in [0.05, 0.95] for
  the entire attainable x-range of the configuration; combinations violating this
  are declared INVALID for the alternative set BEFORE any computation and excluded
  and listed - never clipped.
  Secondary family (sensitivity only, different units - log-odds per reference sd):
      logit P = logit(a_k) + lambda * x, lambda in {0.5, 1.0}; reported separately,
  never substituted for the primary family.
  Dependence (declared): conditionally on solver i, test-body outcomes are iid
  Bernoulli (primary). Clustered sensitivity: solver random effect via beta-binomial
  with intra-solver correlation rho in {0.10, 0.25} (rho = 0 primary).
  Estimation: controlled null and alternative distributions enumerated exactly by
  DP where feasible, reporting exact rejection probabilities and power on the
  controlled cases; seeded MC fallback only where declared infeasible.
- Reporting: single JSON + markdown report, exact counts, no sampling.

## 6. Assumption ledger

| # | Item | Status |
|---|---|---|
| V1 | Attainable C grids; floor/ceiling formulas | verified (A1, M3 Rev d) |
| V2 | c definition and s_ref = 0.12703 | verified (M3 Rev d) |
| V3 | c* arithmetic 39.06/156.25/625.00 from (sigma_max, z_req, beta_min) | verified (this document, section 2) |
| U1 | c* (variance heuristic) corresponds to power of the exact evaluation rule | UNVERIFIED - NC2 |
| U2 | expected c ~ 64 at (k5, t~40) as an unconditional point | illustrative; NC1 replaces it with a distribution |
| U3 | O2 event probabilities (with CVD, TrainRa, support, test) | verified for the stated event only (O2 rev 2) |
| U4 | A1 scenario distributions as the DGP family | model assumption, not empirical truth; pilot updates it |
| U5 | Body-level iid errors behind c*; clustering by solver/instance | UNVERIFIED - NC2 |
| U6 | Enumeration feasibility at N=600 with C-levels | UNVERIFIED - verify vs brute force at N=113/150 first |
| U7 | Exchangeability of solver outcome vectors within k-strata under H0 (count-pattern not stratified) | stated assumption, section 4; untestable pre-pilot |
| U8 | Outcome model families, baselines, dependence, bounded by construction | declared in section 5; family sensitivity reported |
| U9 | Power monotone non-decreasing in c (configuration level) and in t for Pi(t) over the calibration family (tolerance 0.02 absolute) | checked and reported by NC2; if false, scalar c*_calibrated NOT AVAILABLE |
| D1 | beta_min | [decide] sensitivity {0.20, 0.10, 0.05} proposed first |
| D2 | Minimum meaningful improvement scale (i/ii/iii above) | [decide] |
| D3 | Frozen evaluation test family and clustering treatment | [decide] |
| D4 | M3 ridge policy; when c* freezes | [decide] |
| D5 | Generation budget (attempts or money) | [decide] - after O-5 |

## 7. Proposed named computations (awaiting explicit authorization)

All deterministic, read-only, stdlib-only, no generation, no hidden outcomes. Each
produces a temp report + JSON; none touches A1/O2/RevF/published documents.
Reporting rules: every prespecified combination (scenario, beta_min, evaluation-rule
candidate, gate stage) is reported in full; no threshold or rule may be selected
after seeing NC1/NC2 results; every reported quantity is tagged
independently-calculated or reused-from-frozen-package.

Pre-run calibration criteria (Claude's tolerance point; proposed defaults for reviewer
confirmation; must be frozen in the authorization text before the run):

F1  Type I. Nominal alpha = 0.05 (two-sided). Every controlled null case must show
    Type I error <= 0.06 (no anti-conservative excess beyond +0.01); conservative
    values below 0.05 are reported as observed properties of the exact procedure, not
    as failures. Exact rejection probabilities, denominators (permutation counts),
    and the achievable size per configuration (coarseness of the discrete null
    distribution) are reported for every case (GPT, Claude). Any case above 0.06 is
    a disagreement to be resolved before any threshold or rule is used downstream.
F2  Power and agreement bands (operational definitions, GPT issue 3; derivation and
    weights per Claude round 2). The primary evaluation procedure and primary outcome
    family (F5, section 4, section 5) are fixed first. Calibration family:
    gate-passing configurations from NC1 under the primary scenario set, primary
    outcome family, declared baselines. For each beta_min:
    (a) measured power at the published heuristic thresholds c*(z_req = 2.5),
        reported configuration by configuration; declared weights for pooling = the
        O-2 qualifying probabilities of the configurations (unweighted values also
        shown). Derived expectation under the heuristic's own model: power =
        Phi(z_req - z_{1-alpha/2}) = Phi(2.5 - 1.96) = 0.705 at two-sided alpha =
        0.05 with sigma = sigma_max = 0.5; the published z_req = 2.5 convention is a
        magnitude convention, not a 0.80-power design. Declared baselines keep the
        Bernoulli sigma at ~0.49-0.50, so sizing is not over-conservative within the
        declared family. Agreement band [0.60, 0.80] is a PRESPECIFIED ENGINEERING
        TOLERANCE (+/- ~0.10 around the derived 0.705), not a mathematical
        consequence of the derivation; recorded rationale: (i) the normal
        approximation is crude relative to exact discrete permutation inference,
        (ii) up to ~0.10 of conservatism or approximation drift is accepted without
        declaring the heuristic invalid, (iii) values above the band indicate an
        error or anti-conservative behavior and are disagreements. Exact-test
        discreteness is MEASURED per configuration (F1) and reported; it is not
        assumed to set the band.
    (b) Aggregation rule (GPT). For each attainable threshold t (the M3 variant v2
        selection c >= t), let S(t) be the qualifying datasets under rank + c >= t;
        define Pi(t) = the O-2-qualifying-probability-weighted mean of exact power
        over S(t) (weights declared, renormalized within S(t)). Define
        c*_calibrated(0.80) = the smallest attainable t with Pi(t) >= 0.80, and ONLY
        IF Pi(t) is monotone non-decreasing in t within tolerance 0.02 absolute
        (checked and reported, U9). If Pi is not monotone within tolerance, or no
        attainable t reaches 0.80, the scalar is declared NOT AVAILABLE and NC2
        reports the Pi(t) curve plus the configuration-level curves instead; F2b is
        then reported as "not supported". Configuration-level power curves are
        reported regardless. R_eff = c*_calibrated(0.80) / c*_heuristic(0.80) when
        defined.
    "heuristic consistent" requires (a) in band and (b) defined and in band.
F3  Consequences, pre-declared. Consistent: heuristic c* retained as an approximation,
    with the measured ratios reported. Outside any band (candidate rejected): all
    downstream feasibility statements and the decision sheet must use the calibrated
    threshold; the uncorrected heuristic is not used further. The bands above are the
    decision rule; no intermediate reading.
F4  Forking-paths guard. beta_min set, scale candidates, rule candidates, gate-stage
    chain, and bands F1-F3 are fixed before NC1+NC2 run; no change after results are
    seen; any deviation requires a new authorization and is recorded as such.
F5  Proposed default freeze for D2/D3 (to be confirmed in the authorization, before
    the run, NOT selected after): primary minimum-improvement scale = (i) change in
    test-correctness rate per reference sd of C (matches c* units; beta_min applies to
    this scale only); primary evaluation test = exact stratified permutation over
    solver labels within k-ONLY strata (per section 4; count-pattern may NOT be
    stratified on), permutation unit = complete solver outcome vector, statistic and
    exactness per section 4. Candidates (ii), (iii) and asymptotic variants are
    sensitivity reporting only, have different units, and cannot replace the frozen
    pair after NC2 results are seen. Scale-presentation rule (Claude): results for
    (ii) and (iii) are reported in separate tables with explicit units and are never
    juxtaposed with (i) in the decision sheet as if comparable.

- NC1  Gate-conditioned c-distribution (O-1). Inputs: A1 CK grids, s_ref, the O2 gate
       machinery read-only. Output: exact distribution of residualized C / c along the
       cumulative gate chain (baseline, +support, +TrainRa, +CVD, +M3 rank
       (pre-concentration threshold), +M3 rank + c threshold per variant, +test
       gates), per (k,t), pooled, and separately for each prespecified O2 scenario
       {a-hist, a-50:50, c-hist, c-50:50}; every stage reported, no cherry-picking.
       M3 threshold variants (GPT): (v1) M3 rank criterion only; (v2) M3 rank + c >=
       c* at each published candidate {39.1, 156.3, 625.0}. The pre-threshold
       distribution (M3 rank only, before any concentration threshold) is a full table
       of its own; each (v2) threshold variant is reported separately. If a calibrated
       threshold is later adopted, its qualification consequences are reported as a
       separate new table and are NOT inferred from the heuristic-threshold tables.
       This replaces the single illustrative point c ~ 64.
- NC2  Heuristic-vs-evaluation calibration (U1, U5; core of O-6), in two clearly
       separated parts. Part (a): simple arithmetic reproduction of c* for each
       beta_min (already straightforward; reported for completeness). Part (b), the
       decisive part: empirical calibration of the actual evaluation statistic -
       compares the variance heuristic against the prespecified exact stratified
       evaluation procedure on the discrete C levels, running all three scale
       candidates (D2 open), for each beta_min in {0.20, 0.10, 0.05}; reports Type I
       error under controlled null cases and power under controlled alternative cases
       on engineered/synthetic outcomes (no solver generation); reports the
       configuration-conditional power curves, the monotonicity check (U9), and the
       operational c*_calibrated(0.80) with R_eff only where F2's monotonicity and
       definition conditions hold; reports any NON-TESTABLE configuration (no usable
       within-stratum C variation) explicitly, without switching methods. Every
       quantity tagged independently-calculated or reused-from-frozen-package.
       Machinery validation only, not evidence about natural solvers.
- NC3  Conditional power surface (O-2, O-3, O-4). Extends O2 exact enumeration with
       M3 and the evaluation rule; reports power vs N, scenario, beta_min.
- NC4  Cost curve (O-5) under pilot-updatable yield parameters; zero-generation.
- NC5  Deferred full pipeline validation (remainder of O-6) on engineered/synthetic
       bodies, beyond NC2's controlled cases.

Suggested order: NC1, NC2 (cheapest, one session), then stop for review as recommended;
NC5 then NC3, NC4 only if warranted. Each NC reports its own verification (brute-force
cross-checks, exact counts).

## 8. Boundaries

No solver generation; no Phase 1 activity; no complete-rule probability claim beyond
the frozen O2 event; no edits to RevF, the O2 package, A1, or published Revision G;
no publication or repository change from this specification. Results of NC1-NC5, when
authorized, will be provisional temp artifacts referenced to the frozen packages.
All engine outputs are calculations under the reference model (A1 distributions plus
the working outcome model of section 5); none is evidence about natural solvers, and
the specification itself is not authorization to run the study.
Scope limit of the machinery validation (Claude; U7): Type I control and power
calibrated by NC2 are conditional on within-k-stratum exchangeability. NC2 validates
the machinery under that assumption and does NOT establish that a real effect of C is
separable from a real effect of count pattern on natural solvers; its outputs must
not be presented as if it did. That separability is a property of the world, only
partially addressable by pilot data, and belongs to the decision sheet's stated
limitations.

## 9. Open items for owner/reviewers

1. Authorize NC1 per both reviewers' current recommendation, or NC1+NC2 if the F2(b)
   aggregation rule in this amendment is accepted; NC3-NC5 remain unrun pending
   review.
2. beta_min sensitivity set {0.20, 0.10, 0.05} - confirm or amend (D1).
3. Confirm or amend bands F1-F3 and the F5 default freeze (D2/D3) in the
   authorization text BEFORE the run; Claude review of this spec precedes it.
4. Risk R1 (enumeration blowup at N=600) - if it materializes, subset DP with
   stratification will be proposed as an amendment, not silently substituted.
5. GPT review outcome: three blocking issues addressed in the targeted amendment
   (k-only strata + solver-vector unit + no-variation rule; declared bounded outcome
   model; operational c*_calibrated with monotonicity gate) and the NC1 M3-threshold
   variants.
6. Claude review round 2: F2(a) now carries its derived expectation and declared
   weights; U9 tolerance fixed at 0.02; achievable size and DP brute-force check
   added; U7 scope limit stated in section 8; scale-presentation rule added.
7. GPT review round 2: F2(a) band labelled as prespecified engineering tolerance with
   recorded rationale; F2(b) aggregation operationalized as the Pi(t) weighted
   conditional-power curve; NC1 adds the pre-concentration-threshold stage as a full
   table. The stated NC2 hold condition is resolved if this amendment is accepted;
   the owner may still prefer the NC1-only route.
