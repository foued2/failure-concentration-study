# Feasibility note: random defect-set sampling to test whether C adds held-out predictive value beyond k

**Date:** 2026-10-25  
**Status:** historical paper-only feasibility analysis, revision 2. This note examines mutation-site combinations, not the naturally generated candidate population selected as the working primary target in the formulation note. It is retained as an alternative feasibility record, not the current primary design or an implementation plan. Nothing here authorizes mutation building, solver generation or execution, simulation, model calls, data collection, or repository changes beyond this record. The project remains closed under existing authorization.  
**Scope:** Idea 1 only (sample mutation-site combinations without targeting observed failure profiles). It cannot by itself test the primary claim about naturally generated solvers.

## 1. The one question this note answers

Can untargeted sampling of mutation-site combinations plausibly yield variation in `C` and a defensible held-out prediction test for that mutation-based population?

This is not the working primary research question. A result from mutation-site combinations would concern that constructed population and would not establish predictive value for naturally generated candidates. The note does not propose or authorize an experiment; it records conditions, unresolved risks, and reasons not to treat this route as a substitute for the primary target.

## 2. Definitions and estimand

A diagnostic bank has six families with `p` probes each (the natural-solver runs used `p = 5`). For a solver, `f_j` is the number of failed diagnostic probes in family `j`.

- `k = sum_j f_j`
- `C = max_j f_j / k`, defined only for `k > 0`

**Frozen diagnostic partition and historical exposure.** For any future mutation-combination study, the probe-to-family mapping, family labels, probe counts, and family weights must be fixed before building or measuring candidate combinations. Repartitioning probes after seeing failure profiles changes `max_j f_j` and can create a post hoc pattern. However, the legacy six-family, `p = 5` instrument has already been used in v0.2 and Gate 1 with observed failures, and this record does not establish that its partition was frozen before those outcomes. Unless contemporaneous records prove an earlier freeze, treat that legacy definition as outcome-exposed. Reusing it for a future alternative-population study would be a prospective replication conditional on the legacy taxonomy, not a clean first confirmatory test of a pre-specified partition. A new task-semantics partition chosen without access to prior failure-profile tables could support a cleaner test, but would operationalize a related, not identical, concentration measure.

The held-out score `S` is computed on input clusters disjoint from the diagnostic bank and from every input used to build or select solvers. This feasibility note currently proposes a family-balanced score using the diagnostic taxonomy; that is a same-instrument held-out target, not proof of transfer to an independently defined out-of-instrument domain.

**Mutation-population estimand (predictive, not causal; not the primary H3 target).** Let `Z` be a predeclared set of controls that are available at prediction time and do not determine `C`. Let `M0` predict `S` from `k` and `Z`, and let `M1` predict `S` from `k`, `C` and `Z`. With `L` a fixed loss computed on out-of-fold predictions for held-out defect groups:

`Delta_pred = L(M0) - L(M1)`,  `R = Delta_pred / L(M0)`

A positive `Delta_pred` means `C` improved prediction for new defect groups drawn from the stated population.

**Rule on controls.** `Z` must never contain the full family-count vector `F`, `max_j f_j`, or any quantity that determines `C`. Candidate members of `Z` (to be frozen later): task identifier if more than one task is used, and fixed instrument properties.

**What a positive result would mean.** `C` is a useful predictive feature in this population and instrument. It would not show that concentration causes anything, and it would not show that the underlying defects are independent of what `C` measures.

## 3. What untargeted sampling changes, and what it does not

**Changes.** Earlier engineered designs set target vectors such as `(5,0,0,0,0,0)` versus `(3,1,1,0,0,0)` and tried to build solvers that hit them. The construction audit could not show enough genuinely distinct mechanisms at matched profiles. Here the profile is an outcome, not a target. Exact matched same-`k` pairs are no longer required. What is required is overlapping support of `(k, C)` across independent units.

**Does not change.**

- The population definition moves the targeting upstream. Which defects enter the library, and with what probabilities, determines the distribution of `(k, C)`. The library and sampling probabilities are therefore design choices that could, in principle, be tuned to produce an effect. They must be frozen, with a written rationale that does not use any outcome, before any footprint or score is measured.
- `C` is still a function of the failure vector. At best the design tests predictive usefulness across a population of defect groups.
- The independent unit is not the sampled solver (see Section 5).

## 4. The population

**Defect library.** A fixed list of mutation sites `s = 1..m` applied to a reference implementation of one task. Each site `s` has a diagnostic footprint `D_s` (the probes it makes fail) and an evaluation footprint `E_s`.

**Solver.** A subset of `d` sites applied together, with `d` drawn from a predeclared distribution (for example `d` in `{1, 2, 3}`).

**Footprint of a combination is measured, not assumed.** The union rule `D_{s1,s2} = D_{s1} union D_{s2}` fails whenever mutations interact or mask one another. Any combined solver must have its own footprint measured directly. Treating the union as exact would be an unverified assumption.

**Group.** Sites are partitioned into groups before sampling. Solvers are only formed from sites within one group. The group is the independent unit (Section 5 and Section 7).

## 5. Independence and the bounded-domain requirement

Two requirements from the previous protocol failed on exactly these points, so they are restated precisely.

**Behavioral aliases are not the same as statistical independence.** Two candidates with identical failure sets on a specified bounded domain are behaviorally equivalent on that domain; one separating input shows they differ on that domain. Neither equality nor difference of observed failure sets alone proves statistical independence. Solver-side dependence groups must primarily follow known provenance, such as shared mutation sites, common code ancestry, generation lineage, or shared components. Behavioral-alias checks are supporting evidence and have domain-limited meaning.

**Bounded domain.** The task must have a finite input domain (for example a bound on expression length, digits per integer, and whitespace run length). Then failure sets can be compared exactly in principle. Agreement on a finite diagnostic bank is never accepted as proof of equivalence. The length-7 parentheses domain is finite, but its earlier evaluation families had unequal sizes and would need the family-balanced scoring in Section 8.

**The alias check is not yet resolved as outcome-blind.** Exact comparison of failure sets over the full bounded domain uses behavior on the same domain from which `S` would be computed, so describing it as outcome-blind is not justified. A separate identity-check domain can identify aliases relative to that domain, but cannot prove equivalence over the whole evaluation domain. A future protocol must define disjoint diagnostic, identity-check, and evaluation input clusters, state the limited equivalence claim, and keep evaluation outcomes sealed until grouping rules are frozen. Alternatively, use provenance-based groups without claiming exact behavioral equivalence. This note does not decide between those options.

**Independent unit.** If solvers share sites, they are dependent. The number of independent units is the number of site groups `G`, not the number of sampled solvers. Sampling more combinations inside a group adds within-group variation in `(k, C)` but does not add independent units.

## 6. Where variation in `(k, C)` could come from

This section matters most, because the earlier data showed no within-`k` variation at all.

**Arithmetic facts (exact).** With six families of `p` probes, each `f_j <= p`. At a given total `k`, the maximum family count is an integer between `ceil(k/6)` and `min(p,k)`. With `p = 5`, `k = 5` allows `C` values from 0.2 to 1.0, and `k = 10` allows 0.2, 0.3, 0.4, or 0.5. The general feasible-support implication is important: `C` has no variation at `k = 1` or for `k = 25..30`; at `k = 2`, only `C = 0.5` and `C = 1` are feasible. For every `k > 5`, `C <= 5/k`. Therefore the feasible region is bounded, and variation at fixed `k` is possible only at some strata, not all.

**Reported archived-data pattern; keep records and units separate.** The archived v0.2 audit reports `C = 5/k` throughout the rows it analyzed and all-or-none family counts under that instrument. The v0.2 archive also records 40 solver bodies with three replicas each and only ten eligible bodies; those replicas are not independent candidates. A separate natural-candidate inventory is reported as 90 eligible rows from ten base bodies and also lacked same-`k`, different-`C` support. Do not merge those counts into one dataset or treat row counts as independent solver units. The all-or-none pattern is at least partly instrument-induced because each diagnostic family's probes vary one underlying property. These reports do not establish that naturally generated solvers in general have family-aligned failures; they establish only that the saved setups did not furnish the required support.

**The tension this creates.**

- If sampled defects are family-aligned, `C = 5/k` again and there is no support. Random sampling would reproduce the earlier degeneracy.
- If the library includes sites whose footprints are partial within a family or span several families, then `C` varies at fixed `k`. But then the families no longer correspond one-to-one to defect mechanisms, and the interpretation of `C` as concentration on a mechanism weakens.

Whether the library can contain such sites naturally, and with what frequency, is an empirical property of the task and the mutations. A paper argument can show it is plausible from code structure. It cannot establish it.

**Consequence for the design.** Support has to be checked from measured footprints before any outcome is examined, using an outcome-blind rule (Section 10).

## 7. Held-out design and leakage control

- **Held-out unit:** the site group. All solvers built from a group's sites are held out together.
- **Fold construction:** groups are assigned to folds so that no site appears in both training and test data. Folds are stratified so that each fold contains groups with a range of `(k, C)` support. If that stratification cannot be formed, the design fails.
- **Why site-level, not solver-level, splitting:** random solver-level folds would put combinations containing the same site in both training and test sets, which would let a model reward memorized site identity.
- **Target population:** new defect groups drawn from the same library distribution and task. The result would not generalize to new tasks or new families.

## 8. Score and loss

- **Score:** `S` is computed on the evaluation bank. This mutation-population note proposes a mean over the diagnostic families of within-family evaluation failure rates to control family-size effects, with pooled rate secondary. That reuses the diagnostic family taxonomy, so the target is same-instrument held-out performance. It cannot answer the primary H3 claim about transfer to an independently defined held-out domain unless the evaluation strata and weights are redefined independently before outcomes.
- **Loss:** squared error on `S`, averaged first within each group and then across groups, so each independent unit has equal weight.
- **Small baseline loss:** if `L(M0)` falls below a threshold fixed in advance, relative gain `R` is not used and the absolute gain `Delta_pred` is reported instead.
- **Instrument dependence:** `C` is computed from the diagnostic bank and `S` from disjoint evaluation input clusters, but the proposed family-balanced score reuses the same family taxonomy. A positive result therefore concerns that instrument and same-family target; independence of inputs does not remove this construct overlap.

## 9. Uncertainty and thresholds

- **Primary interval:** compute out-of-fold per-group loss differences, then apply a cluster bootstrap over groups with a 95% percentile interval. Cross-validated intervals can undercover, so a full-procedure bootstrap (refit and re-validate within each replicate) is run as a sensitivity analysis, not assumed to repair coverage.
- **Two thresholds, chosen before data:** evidence of any positive gain if the lower bound of the interval for `R` is above zero, and evidence of a practically meaningful gain if it is above a policy value `R_min`. The previous protocol's 5% would be carried over for continuity. It is a chosen criterion with no empirical basis and should be reviewed by someone who can say what decision a gain of that size would change.
- **Model class:** to be frozen before data. A candidate is a linear model with a separate intercept per `k` level and one common slope on `C`, because the question is about variation within `k`.
- **Secondary, interpretive analyses (declared in advance):** adding the number of inserted sites `d` to `M0`, to see whether `C` is largely a proxy for it. This is interpretation, and cannot rescue a failed primary test.

## 10. Paper feasibility criteria and assessment

| Criterion | What a pass needs | Can paper settle it? | Current assessment |
| --- | --- | --- | --- |
| P1. Footprint heterogeneity | A library that plausibly contains partial-family and cross-family footprints at stated frequencies | No, only plausibility from code structure | **Open.** Key risk (Section 6) |
| P2. Independence rule | Provenance-based dependence groups; bounded diagnostic, identity-check, and evaluation input clusters | No, not fully resolved | **Open.** Full-domain alias checking overlaps the evaluation domain; a separate identity-check domain supports only a domain-limited equivalence claim |
| P3. `(k, C)` support | A support rule applied to measured footprints before outcomes | Rule: yes. Satisfaction: no | **Rule can be stated; satisfaction unknown** |
| P4. Leakage | Group-level folds, no shared sites across folds | Yes | **Pass on paper** |
| P5. Thresholds and precision | Frozen loss, `R_min`, handling of small `L(M0)`, justified number of groups `G` | Partly | **Open:** `G` and the required precision depend on between-group variance that is not known in advance |

**On the number of groups.** No value of `G` is proposed here. A number chosen without a variance source would repeat the earlier unjustified 24-cluster floor. The audit plan must name, before any measurement, how `G` will be derived from observed between-group variance. If no justified value can be given, the criterion fails.

**Support rule (to be frozen).** For each `k` used in the analysis, measured group-level `C` must take at least two distinct levels, each represented by a pre-declared minimum number of groups, with the minimum justified under P5. The rule is applied to footprints measured without examining any `S`.

## 11. Interpretation limits

- A positive gain would show predictive usefulness across this defect distribution and instrument, not a causal effect of concentration and not independence from defect identity.
- The result depends on the library and sampling probabilities. A different but equally reasonable library could change it.
- A null or inconclusive result would say the design lacked power or support. It would not show that `C` has no predictive value.
- Knowing how many mutations were inserted does not establish how many independent behavioral defects resulted. Failure-set equality can establish behavioral equivalence only on the domain checked; it does not prove statistical independence. Solver-side dependence groups should primarily follow provenance and construction.

## 12. Assessment and decision

The paper alone cannot establish whether a mutation-site library will produce sufficient fixed-`k`, varying-`C` support, nor whether the result would generalize to naturally generated solvers. The main issues remain footprint heterogeneity (P1), independence/alias handling (P2), support (P3), and a defensible number of independent groups (P5). As written, this note does not establish that a confirmatory design is ready.

**Disposition.** Do not treat Idea 1 as the implementation route for primary H3. It is a different research question about a mutation-defined population. A separate, narrowly authorized, outcome-blind feasibility audit could be considered only if that alternative population is independently worth studying and if P2 is first resolved; it must not be used as a proxy for naturally generated candidates. Otherwise, leave the project closed and retain this note as a record of feasibility and construct-validity limits.

## 13. Items this note deliberately leaves open

- The task, the defect library, and the sampling probabilities.
- The specific bounded domain.
- The value of `p`, the controls `Z`, and the model class.
- The number of groups `G`, the support minimum, and `R_min`.
- The exact provenance and distinct scope of the natural-candidate inventory versus the archived v0.2 confirmatory table.
- Diagnostic, identity-check, and evaluation input-cluster construction rules.

The population and analysis rules must be frozen before confirmatory scores are inspected. A support gate may use diagnostic footprints only after grouping and domain rules are specified; evaluation scores remain sealed until that gate is complete.
