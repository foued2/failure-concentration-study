# Failure-Concentration Predictive Value Study
## Pre-Registered Protocol (DRAFT v1 — not yet frozen)

**Status:** DRAFT. Freeze requires: (1) Foued's ratification of the five open choices in §16,
(2) `FREEZE.md` recording sha256 hashes of this file and the instrument/prompt specs,
(3) a `v0.1-freeze` tag. Freeze must occur BEFORE any confirmatory solver or confirmatory
instance is generated. No protocol amendments after freeze; any deviation is recorded and
forces an INCONCLUSIVE outcome.

**Lineage:** This protocol answers one question left open by the terminated Doctor/C_genuine
work: does family concentration carry predictive information beyond failure count? It imports
no code, data, probe, family label, or result from `Euler_Project/new-doctor` (terminated CRS
archive) or `doctor-workspace-recovered` (read-only historical state). Clean-room repository.

**Roles:** Foued decides. One executor (MIMO) runs the frozen protocol and reports the primary
metric with its CI. Reviewers (GLM, GPT, Claude) record independent judgments of the frozen
protocol before seeing any results. Collaborative analysis, if any, is a separate post-result
decision and cannot alter the primary outcome.

---

## 1. Claim (frozen text)

Among solver submissions failing at least two diagnostic probes, the largest-family failure
share improves prediction of hidden correctness beyond failure count alone, on problem
instances never used to design anything, within the declared problem class, solver generator,
and protocol.

Scope: **predictive value only.** No claim of defect localization. No novelty claim. All
conclusions conditional on the declared problem class, generator (named at freeze), frozen
instrument, and pre-registered threshold.

## 2. Problem class

**Single-source shortest path (SSSP)** on directed graphs with non-negative integer edge
weights. An instance is a graph G = (V, E, w) plus a source s and target t. Instances are
independently generated from a seeded RNG with controlled structural parameters.

Rationale: fresh domain with no Doctor lineage; reference oracle is trivial and brute-force
verifiable; the input space admits pre-hoc, spec-derived failure-mode families with decidable
input predicates (§3).

## 3. Taxonomy (design time, from the problem specification)

Six families. Each has a written defining property and a decidable input predicate. Families
were derived from the problem specification alone. **No probe was ever checked against solver
behavior.** No historical family label is reused.

| ID | Family | Defining property (predicate) |
|----|--------|-------------------------------|
| F1 | unreachable_target | no directed path exists from s to t |
| F2 | zero_weight_edge | at least one edge has w = 0 |
| F3 | parallel_edges | at least one ordered pair (u,v) carries ≥ 2 edge entries |
| F4 | self_loop | at least one edge (v,v) exists |
| F5 | tie_multiplicity | ≥ 2 distinct s–t paths attain the minimum weight |
| F6 | weight_plateau | ≥ 3 edges share a single weight value |

**Isolation interpretation (GPT qualification, binding):** the instrument's automated
partition check verifies only that the constructed probes satisfy exactly one declared
predicate each. It verifies a declared partition property. It does **not** establish that the
families isolate distinct computational properties, and no report may claim otherwise.

## 4. Probes (diagnostic, observable)

Per instance: 30 probes = 5 per family, constructed by deterministic seeded rules specified in
the instrument spec (hashed with this protocol). Probe graphs are built to satisfy exactly
their assigned family predicate and violate the other five. Probe expected outputs are computed
by the reference implementation (§6) and cross-checked by brute-force enumeration on small
graphs (Gate G3). Probes are run against solvers before any hidden-oracle exposure.

Per (solver, instance): k = failed probe count; f_j = failures in family j;
**C = max_j f_j / k** (the single primary feature). Eligibility: k ≥ 2.

## 5. Solver generation

A single solver population of N = 40 LLM-generated Python SSSP implementations (frozen
generator: model identifier, prompt template, sampling parameters — recorded in the prompt
spec hashed at freeze). Every solver is evaluated on every instance. Solvers are never
selected, edited, or discarded after generation except format failures, handled by the
pre-specified rule: unparseable or non-running submissions are excluded from the primary
analysis, counted and reported; if format-failure rate exceeds 20 % of the pack, the study
terminates as INCONCLUSIVE.

A separate pilot solver pack (N = 20, same generator protocol) is used for pipeline shakedown
only (§11) and never enters the confirmatory analysis.

## 6. Oracle and hidden suite (Y)

**Reference implementation:** a trusted SSSP solver, validated against brute-force path
enumeration on ≥ 50 tiny random graphs (Gate G3).

**Hidden suite:** per instance, M = 20 hidden inputs from an independent generator (different
seed stream, different construction code path from the probes), containing random graphs plus
edge cases not built from probe construction rules. The hidden suite never touches family
labels, probe definitions, or features.

**Target:** Y = 1 iff the solver matches the reference output on all M hidden inputs of the
instance. Observations are (solver, instance) pairs.

## 7. Models

Fit on eligible (solver, instance) observations, evaluated held-out by instance:

- **Model A (baseline):** Y ~ restricted cubic spline on log(1 + k), knots fixed in the
  analysis spec. Flexible form prevents baseline misspecification from gifting concentration
  apparent value.
- **Model B:** Model A + C (single linear term).
- **Control:** Model B refit with family labels randomly relabelled within each instance
  (size-preserving permutation, one permutation applied consistently to all solvers of that
  instance), R = 100 relabelings, seeds 1–100 fixed. Specificity check only — not a causal
  randomization test (original labels were not randomly assigned).

## 8. Primary analysis

- **Estimand:** Δ = L_A − L_B, where L is mean held-out log-loss; per-instance losses are
  averaged first so every instance carries equal weight.
- **Evaluation:** locked confirmatory instance set. Pre-specified fallback if the locked set
  cannot be scored as a unit: leave-instances-out grouped CV (instances, never solvers, are
  the grouping unit).
- **Uncertainty:** nonparametric bootstrap over instances, 10 000 resamples, 95 % CI.
  Never over solvers.
- **Threshold (pre-registered):** δ = 0.01 nats per eligible prediction. Justification: at
  eligibility base rates in the 0.2–0.8 band, 0.01 nats shifts the posterior correctness
  probability of a borderline case by roughly one percentage point — the smallest shift that
  changes a symmetric-cost accept/reject decision for a non-negligible share of submissions.
  Effects below δ are practically null regardless of statistical detectability.
- **Control comparison:** the positive outcome additionally requires Δ_real to exceed the
  95th percentile of the 100 relabeling Δ values.
- **Cost function:** symmetric loss (λ = 1) is the only decision cost in the primary analysis.
  AUC, calibration, the λ sweep, and the original C_genuine accept/reject rule are secondary
  descriptive reports only and cannot rescue a negative primary result.

## 9. Outcomes (all terminal)

| Outcome | Meaning | Action |
|---|---|---|
| CI lower bound above δ, and Δ_real beats the relabel control | Incremental predictive value specific to this partition, generator, and class | Report and stop |
| CI excludes improvements ≥ δ | Meaningful predictive gain ruled out in the stated scope | Report and stop |
| Δ apparent but does not beat the relabel control | Gain not attributable to the family structure | Report as ambiguous and stop |
| Too few eligible submissions, failed chain checks, format-failure rate > 20 %, or precision unattainable within resources | Study cannot answer the question reliably | Report as inconclusive and stop |

No result authorizes new features, new partitions, alternate thresholds, or new branches.

## 10. Gates

- **G1 partition check:** automated evaluation of all probe predicates; instrument passes iff
  every probe satisfies exactly its assigned family predicate. Interpretation limited to the
  declared partition (§3).
- **G2 measurement chain:** hand-computed toy cases confirm the intended feature and the
  eligibility rule are what the code computes; output-identity check between feature
  computation paths (LC79 lesson).
- **G3 oracle chain:** reference implementation vs brute-force enumeration on ≥ 50 tiny
  random graphs; zero mismatches required.
- **G4 freeze integrity:** sha256 of this protocol, the instrument spec, and the generator
  prompt spec recorded in `FREEZE.md` before confirmatory generation; confirmatory instance
  seeds derived deterministically from the freeze hash; no post-unblinding additions.

## 11. Pilot (3 instances, excluded from confirmatory)

Pilot instances use fixed seeds 101, 102, 103 and never enter the confirmatory set. Purposes:
(a) pipeline shakedown across instrument, oracle, generator, analysis; (b) eligible-solver
yield; (c) between-instance variance for the sample-size calculation.

**Pilot decision gate:** proceed to confirmatory generation only if every pilot instance
yields ≥ 15 eligible (solver, instance) observations and the required instance count from §12
is within the committed resource budget. Otherwise the study terminates as INFEASIBLE — a
valid terminal outcome, not a failure.

Three instances cannot establish between-problem variability on their own; the pilot variance
estimate enters §12 with that caveat, and the confirmatory CI remains the inference.

## 12. Sample size

Confirmatory instance count N is the smallest count whose expected 95 % CI half-width (from
pilot between-instance variance) is ≤ δ. Planning guess 10–15 instances; the guess is not
binding — N is fixed from the pilot analysis and recorded before confirmatory generation.

## 13. Process

One executor; frozen protocol; single execution. Reviewers record protocol judgments before
reading each other's. The executor reports the primary metric with CI and the four-outcome
classification. Anything further is a separate, explicitly authorized decision.

## 14. Workspace and archival boundaries

Clean-room repository only. No code, data, probes, family labels, or results imported from
`Euler_Project/new-doctor` or `doctor-workspace-recovered`. The historical three-line record
(measured: family concentration; claimed: localization; established: claim unvalidated,
predictive value never confirmed) lives in the session record of 2026-10-11; it is not copied
into either frozen repository.

## 15. Honest assessment (pre-result)

Cost: 2–4 weeks, dominated by instrument, oracle, and generation. Likely outcome: null,
ambiguous, or pilot-infeasible is plausible (prior: compressibility finding — a reconstructed
prior, not a result). Novelty: unverified and unclaimed. This study answers one falsifiable
question; it is not a rescue of C_genuine.

## 16. Open choices requiring Foued's ratification before freeze

1. **Problem class:** SSSP on directed non-negative weighted graphs (§2). Veto here means
   redesign before freeze.
2. **Threshold:** δ = 0.01 nats (§8).
3. **Generator:** single LLM pack of 40 solvers, model identifier and prompt frozen at
   freeze time (§5). Alternative: scripted mutation generator — a veto of LLM generation.
4. **Confirmatory pack size:** N = 40 solvers, M = 20 hidden inputs per instance (§§5–6).
5. **Pilot gate:** ≥ 15 eligible observations per pilot instance (§11).
