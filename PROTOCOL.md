# Failure-Concentration Predictive Value Study
## Pre-Registered Protocol (DRAFT v2 — not yet frozen)

**Status:** DRAFT v2. GPT's freeze-blocker amendments (2026-10-11) are recorded below. Freeze
requires: (1) Foued's authorization, (2) gates G1–G3 executed and passed on the built
instrument, recorded in `FREEZE.md` with sha256 hashes of this file, the instrument spec, and
the generator spec, (3) a `v0.1-freeze` tag. Freeze must occur BEFORE any confirmatory solver
or confirmatory instance is generated. No protocol amendments after freeze; any deviation is
recorded and forces an INCONCLUSIVE outcome. Instrument implementation bugs discovered before
confirmatory generation may be fixed only if the frozen specs (predicates, probe rules,
features, thresholds) are unchanged; any spec change requires a new DRAFT and re-ratification.

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

Six families, each with a written defining property and an executable decidable predicate.
Families were derived from the problem specification alone. **No probe was ever checked
against solver behavior.** No historical family label is reused. Exact predicate code and the
probe-to-family construction rules live in the instrument spec, hashed at freeze (§16).

| ID | Family | Defining property (predicate) |
|----|--------|-------------------------------|
| F1 | unreachable_target | no directed path exists from s to t |
| F2 | zero_weight_edge | at least one edge has w = 0 |
| F3 | parallel_edges | at least one ordered pair (u,v) carries ≥ 2 edge entries |
| F4 | self_loop | at least one edge (v,v) exists |
| F5 | tie_multiplicity | ≥ 2 distinct s–t paths attain the minimum weight |
| F6 | weight_plateau | ≥ 3 edges share a single weight value |

**Isolation interpretation (GPT qualification, binding):** the automated partition check
verifies only that each constructed probe satisfies exactly one declared predicate. It
verifies a declared partition property. It does not establish that the families isolate
distinct computational operations, and no report may claim otherwise.

**Overlap rule:** if the partition check (G1) finds any probe satisfying zero or ≥ 2
predicates, the instrument fails. G1 must pass before freeze. Post-freeze G1 re-runs must
pass on every instance; a failure forces INCONCLUSIVE.

## 4. Probes (diagnostic, observable)

Per instance: 30 probes = 5 per family, constructed by deterministic seeded rules specified
in the instrument spec. Probe graphs are built to satisfy exactly their assigned family
predicate and violate the other five. Probe expected outputs are computed by the reference
implementation (§6) and cross-checked by brute-force enumeration on small graphs (G3).
Probes are run against solvers before any hidden-oracle exposure.

## 5. Solver generation

A single solver population of N_s = 40 LLM-generated Python SSSP implementations. Every
solver is evaluated on every instance.

**Generator spec (frozen at freeze):** provider, immutable model snapshot identifier if the
provider exposes one (otherwise that limitation is recorded and exact reproducibility is not
claimed), complete generation prompt including system instructions where controllable,
sampling parameters (temperature, top-p, seed handling), and the output I/O contract for
solvers.

**Retention rule:** every generated submission is retained in generation order; no post-hoc
selection, editing, deduplication-by-quality, or best-of filtering. Unparseable or
non-running submissions are format failures: excluded from the primary analysis, counted and
reported; if format-failure rate exceeds 20 % of the pack, the study terminates as
INCONCLUSIVE.

A separate pilot solver pack (N_s = 20, same generator spec) is used for pipeline shakedown
only (§11) and never enters the confirmatory analysis.

## 6. Oracle, hidden suite, and observational unit (frozen definitions)

**Reference implementation:** a trusted SSSP solver, validated against brute-force path
enumeration on ≥ 50 tiny random graphs (G3).

**Hidden suite:** per instance, M = 20 hidden inputs from an independent generator (different
seed stream, different construction code path from the probes), containing random graphs plus
edge cases not built from probe construction rules. The hidden suite never touches family
labels, probe definitions, or features.

**Observational unit:**

- One *solver* = one generated Python SSSP implementation, never edited after generation.
- One *instance* = one (G, s, t) triple from the frozen instance generator.
- One *observation* = one (solver, instance) pair. Feature vector (k, C) computed from that
  instance's 30 diagnostic probes. Label Y ∈ {0,1}. Observations sharing a solver are
  correlated; observations sharing an instance are correlated.
- *Correctness label:* Y = 1 iff the solver returns the reference-correct distance on **all
  M = 20** hidden inputs of that instance; a crash or wrong output on any hidden input gives
  Y = 0. The hidden suite contributes to one pair-level binary label; it does not create 20
  independent observations. Per-input labels are not used in the primary analysis: the
  feature is pair-level, so per-input rows would duplicate the feature and pseudo-replicate.

**Inference axis:** instances. Models are scored per held-out instance; Δ is the
equal-weighted mean of per-instance loss differences; uncertainty bootstraps instances (§8).
The solver pack is fixed across all instances and part of the declared scope: the claim
generalizes to unseen **instances** for this pack and generator, not to unseen solvers. No
solver identity enters the feature set.

## 7. Models

Fit on eligible (solver, instance) observations (§11 for eligibility), evaluated held-out by
instance:

- **Model A (baseline):** Y ~ restricted cubic spline on log(1 + k), knots fixed in the
  analysis spec. Flexible form prevents baseline misspecification from gifting concentration
  apparent value.
- **Model B:** Model A + C (single linear term).
- **Control:** Model B refit with family labels randomly relabelled within each instance
  (size-preserving permutation, one permutation applied consistently to all solvers of that
  instance), R = 100 relabelings, seeds 1–100 fixed. Specificity check only — not a causal
  randomization test (original labels were not randomly assigned).

## 8. Primary analysis

- **Estimand:** Δ = L_A − L_B, where L is mean held-out log-loss on eligible observations;
  per-instance losses are averaged first so every instance carries equal weight.
- **Evaluation (frozen):** the confirmatory instance set is locked before generation (seeds
  derived deterministically from the freeze hash; G4). Evaluation is leave-one-instance-out
  grouped CV across the locked set: for instance i, models A and B are fitted on all eligible
  observations from the other confirmatory instances and scored on instance i's eligible
  observations. No observation from instance i appears in its training fold. The same
  solvers appearing in train and test folds is intentional — the claim is instance
  generalization for a fixed pack — and is not record-level leakage, because instance i's
  probes, hidden inputs, and labels are entirely unseen during its training fold.
- **Uncertainty:** nonparametric bootstrap over instances, 10 000 resamples, 95 % CI. Never
  over solvers.
- **Threshold (pre-registered; GPT amendment adopted):** δ = 0.01 nats per eligible
  prediction, adopted as a **protocol choice**: the minimum mean held-out log-loss improvement
  this study will count as meeting its threshold. It is not derived from an operational
  decision rule or cost model; no equivalence to a decision-shift or percentage-point change
  is claimed. It is fixed here and cannot change after any confirmatory outcome is observed.
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
| Too few eligible observations, failed chain checks, format-failure rate > 20 %, or precision unattainable within resources | Study cannot answer the question reliably | Report as inconclusive and stop |

No result authorizes new features, new partitions, alternate thresholds, or new branches.

## 10. Gates

- **G1 partition check:** automated evaluation of all probe predicates on every instance's
  probe set; passes iff every probe satisfies exactly its assigned family predicate. Must
  pass before freeze and on every confirmatory instance. Interpretation limited to the
  declared partition (§3).
- **G2 measurement chain:** hand-computed toy cases confirm the intended feature, eligibility
  rule, and Y label are what the code computes; output-identity check between feature
  computation paths (LC79 lesson).
- **G3 oracle chain:** reference implementation vs brute-force enumeration on ≥ 50 tiny
  random graphs; zero mismatches required. Must pass before freeze.
- **G4 freeze integrity:** sha256 of this protocol, the instrument spec, and the generator
  spec recorded in `FREEZE.md` together with G1–G3 pass evidence, before confirmatory
  generation; confirmatory instance seeds derived from the freeze hash; no post-unblinding
  additions.

## 11. Pilot (3 instances, excluded from confirmatory)

Pilot instances use fixed seeds 101, 102, 103 and never enter the confirmatory set. Purposes:
(a) pipeline shakedown across instrument, oracle, generator, analysis; (b) eligible-observation
yield; (c) between-instance variance input for the sample-size rule.

**Eligible observation (frozen definition):** a (solver, instance) pair with (a) k ≥ 2
failures on the frozen 30-probe diagnostic suite and (b) a completed hidden-suite evaluation
producing a defined Y. Crashes on hidden inputs count as Y = 0 completions, not missing
labels; a solver that cannot load or run at all is a format failure (§5) and never forms a
pair. Eligibility counts distinct (solver, instance) pairs, never individual probe results.

**Pilot gate:** each of the three pilot instances must yield ≥ 15 eligible pairs. Passing
establishes **feasibility only** (pipeline integrity plus sufficient yield to attempt the §12
precision analysis). It does not establish statistical adequacy or power. Failing the gate
on any pilot instance: stop, report INFEASIBLE — a valid terminal outcome.

## 12. Sample size (frozen rule)

After the pilot and before any confirmatory generation:

1. Estimate the between-instance variance of the per-instance held-out loss difference from
   pilot data, using the upper 80 % confidence bound of that estimate (three instances give
   a weak variance estimate; the rule is deliberately conservative).
2. Required N_c = the smallest instance count whose expected 95 % CI half-width under that
   variance, at the per-instance eligible yield observed in the pilot, is ≤ δ.
3. If N_c exceeds the resource ceiling committed at freeze (default: 20 instances), report
   INFEASIBLE and stop.

The pack size N_s = 40 is a generator-budget choice, not a precision guarantee. Precision is
driven by N_c instances × eligible yield. Do not assume 40 solvers are sufficient; the pilot
determines whether the prespecified precision is achievable.

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

## 16. Ratification state

GPT's five decisions (2026-10-11) and their resolution in this draft:

| Choice | GPT decision | Resolution in v2 |
|---|---|---|
| 1. SSSP + six families | Approve with conditions | Executable predicates + probe mapping frozen in instrument spec (§3); overlap stops the study (G1); exclusivity-only interpretation binding (§3) |
| 2. δ = 0.01 nats | Amend | Retained as pre-registered protocol choice; percentage-point analogy removed; no practical-value equivalence claimed (§8) |
| 3. Single LLM generator | Approve with conditions | Full generator spec frozen: model id or recorded snapshot limitation, complete prompt, sampling params, retention rule, no best-of selection (§5) |
| 4. 40 solvers / 20 hidden inputs | Not yet approved as adequate | Observational unit and correctness label frozen (§6); N_c determined by frozen pilot-based precision rule; 40 is budget not adequacy (§12) |
| 5. Pilot gate ≥ 15 | Amend | Eligible observation defined operationally; per-instance gate; feasibility-only meaning (§11) |

Remaining step: Foued authorizes freeze → gates G1–G3 built and passed → `FREEZE.md` +
`v0.1-freeze` → pilot.
