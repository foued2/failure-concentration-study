# Feasibility note: random defect-set sampling to test whether C adds held-out predictive value beyond k

**Date:** 2026-10-25  
**Status:** paper-only draft (Claude Doc export, rev 1, committed to a review branch as a record). Nothing in this note authorizes solver generation, mutation building, execution, simulation, model calls, data collection, or repository changes beyond this record. The failure-concentration project remains closed under its existing authorization.  
**Scope:** Idea 1 only (sample defect sets without targeting profiles). Ideas 2 to 6 are out of scope here.

## 1. The one question this note answers

Can random sampling of independently defined defect sets plausibly yield enough variation in `C` and a defensible held-out prediction test, without profile targeting and without leakage?

The note does not propose an experiment. It states what would have to be true for the idea to be worth a separate authorization request, says which of those conditions can be settled on paper, and records what cannot.

## 2. Definitions and estimand

A diagnostic bank has six families with `p` probes each (the natural-solver runs used `p = 5`). For a solver, `f_j` is the number of failed diagnostic probes in family `j`.

- `k = sum_j f_j`
- `C = max_j f_j / k`, defined only for `k > 0`

The held-out score `S` is computed on an evaluation bank that is disjoint from the diagnostic bank and from every probe used to build or select solvers.

**Primary estimand (predictive, not causal).** Let `Z` be a predeclared set of controls that are available at prediction time and do not determine `C`. Let `M0` predict `S` from `k` and `Z`, and let `M1` predict `S` from `k`, `C` and `Z`. With `L` a fixed loss computed on out-of-fold predictions for held-out defect groups:

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

**Operational definition of independent defect.** Two candidates are the same defect if they have identical failure sets on a bounded input domain. Distinct failure sets, established by at least one separating input, are necessary for independence. They are not sufficient: sites in one group that share code are dependent for validation purposes even when their failure sets differ.

**Bounded domain.** The task must have a finite input domain (for example a bound on expression length, digits per integer, and whitespace run length). Then failure sets can be compared exactly in principle. Agreement on a finite diagnostic bank is never accepted as proof of equivalence. The length-7 parentheses domain is finite, but its earlier evaluation families had unequal sizes and would need the family-balanced scoring in Section 8.

**Blindness of the alias check.** Alias detection compares full-domain failure sets, which also determine `S`. To keep it outcome-blind, the check should record equality classes only, for example by comparing set hashes, and no score should be computed or examined until the design is frozen.

**Independent unit.** If solvers share sites, they are dependent. The number of independent units is the number of site groups `G`, not the number of sampled solvers. Sampling more combinations inside a group adds within-group variation in `(k, C)` but does not add independent units.

## 6. Where variation in `(k, C)` could come from

This section matters most, because the earlier data showed no within-`k` variation at all.

**Arithmetic facts (exact).** With six families of `p` probes, `f_j <= p`. For a given `k`, the possible values of `max_j f_j` run from `ceil(k/6)` to `min(p, k)`. With `p = 5`:

- `k = 5`: `C` can take five values, from 0.2 to 1.0.
- `k = 10`: `C` can take four values, 0.2, 0.3, 0.4, 0.5.
- For every `k > 5`: `C <= 5/k`.

So the feasible region is a band, and variation in `C` at a fixed `k` is mathematically available.

**What the saved natural data show.** In the audited v0.1 and v0.2 rows, `C = 5/k` exactly at every observed `k` (5, 10, 20, 25), and every observed `k` is a multiple of five. Since `C <= 5/k` for `k > 5`, every eligible natural row sits on the upper boundary of the feasible band: at least one family had all five probes failing. This is consistent with defects whose footprints are aligned to the diagnostic families (a family either fails entirely or not at all). The saved per-family vectors in the v0.1 report could confirm or reject this reading. It is a hypothesis, not a finding, until checked.

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

- **Score:** `S` is computed on the evaluation bank. To prevent family size from driving the score (the cause of the `paren7` spread), the primary score is the mean over families of the within-family evaluation failure rate. The choice of equal family weights must match the stated target population, and a pooled-rate version is reported as a secondary analysis.
- **Loss:** squared error on `S`, averaged first within each group and then across groups, so each independent unit has equal weight.
- **Small baseline loss:** if `L(M0)` falls below a threshold fixed in advance, relative gain `R` is not used and the absolute gain `Delta_pred` is reported instead.
- **Instrument dependence:** `C` is computed from the diagnostic bank and `S` from a disjoint evaluation bank, but both use the same family taxonomy. A positive result is therefore a statement about this instrument.

## 9. Uncertainty and thresholds

- **Primary interval:** compute out-of-fold per-group loss differences, then apply a cluster bootstrap over groups with a 95% percentile interval. Cross-validated intervals can undercover, so a full-procedure bootstrap (refit and re-validate within each replicate) is run as a sensitivity analysis, not assumed to repair coverage.
- **Two thresholds, chosen before data:** evidence of any positive gain if the lower bound of the interval for `R` is above zero, and evidence of a practically meaningful gain if it is above a policy value `R_min`. The previous protocol's 5% would be carried over for continuity. It is a chosen criterion with no empirical basis and should be reviewed by someone who can say what decision a gain of that size would change.
- **Model class:** to be frozen before data. A candidate is a linear model with a separate intercept per `k` level and one common slope on `C`, because the question is about variation within `k`.
- **Secondary, interpretive analyses (declared in advance):** adding the number of inserted sites `d` to `M0`, to see whether `C` is largely a proxy for it. This is interpretation, and cannot rescue a failed primary test.

## 10. Paper feasibility criteria and assessment

| Criterion | What a pass needs | Can paper settle it? | Current assessment |
| --- | --- | --- | --- |
| P1. Footprint heterogeneity | A library that plausibly contains partial-family and cross-family footprints at stated frequencies | No, only plausibility from code structure | **Open.** Key risk (Section 6) |
| P2. Independence rule | Bounded domain, failure-set equality, outcome-blind alias check | Yes | **Pass on paper** if a bounded domain is chosen |
| P3. `(k, C)` support | A support rule applied to measured footprints before outcomes | Rule: yes. Satisfaction: no | **Rule can be stated; satisfaction unknown** |
| P4. Leakage | Group-level folds, no shared sites across folds | Yes | **Pass on paper** |
| P5. Thresholds and precision | Frozen loss, `R_min`, handling of small `L(M0)`, justified number of groups `G` | Partly | **Open:** `G` and the required precision depend on between-group variance that is not known in advance |

**On the number of groups.** No value of `G` is proposed here. A number chosen without a variance source would repeat the earlier unjustified 24-cluster floor. The audit plan must name, before any measurement, how `G` will be derived from observed between-group variance. If no justified value can be given, the criterion fails.

**Support rule (to be frozen).** For each `k` used in the analysis, measured group-level `C` must take at least two distinct levels, each represented by a pre-declared minimum number of groups, with the minimum justified under P5. The rule is applied to footprints measured without examining any `S`.

## 11. Interpretation limits

- A positive gain would show predictive usefulness across this defect distribution and instrument, not a causal effect of concentration and not independence from defect identity.
- The result depends on the library and sampling probabilities. A different but equally reasonable library could change it.
- A null or inconclusive result would say the design lacked power or support. It would not show that `C` has no predictive value.
- Knowing how many mutations were inserted does not establish how many independent behavioral defects resulted. Independence is established only by the failure-set rule.

## 12. Assessment and decision

The question in Section 1 cannot be answered "yes" from the paper alone. The decisive quantity is empirical: whether the defect library produces partial-family or cross-family footprints often enough to give `C` variation at fixed `k`. The natural-data pattern (all rows on the upper boundary `C = 5/k`) is a reason for caution, not a reason to expect support.

What the note does establish is that the rest of the design can be specified coherently: independence is operational, the leakage control is clear, the score removes the family-size confound, and the thresholds can be fixed in advance. Two things remain unresolved: footprint heterogeneity (P1) and the justification of `G` (P5).

**Two options for the reviewer.**

- **A. Credible enough to request a narrow authorization.** If an independent reviewer accepts the identification argument and the open items, the next request would be an outcome-blind footprint audit only: build the frozen library, measure diagnostic footprints and failure-set equality classes, apply the support rule, and stop. No score is computed or inspected. This is not a study and not an authorization to run one.
- **B. Not credible.** Leave the project closed and use the methodology write-up fallback, titled for example "Feasibility and construct-validity limits in testing diagnostic failure concentration as a predictive feature."

## 13. Items this note deliberately leaves open

- The task, the defect library, and the sampling probabilities.
- The specific bounded domain.
- The value of `p`, the controls `Z`, and the model class.
- The number of groups `G`, the support minimum, and `R_min`.
- Whether the saved v0.1 and v0.2 per-family vectors confirm the alignment reading in Section 6. This is a read-only check of existing records.

No item above may be settled after any footprint or score has been seen.
