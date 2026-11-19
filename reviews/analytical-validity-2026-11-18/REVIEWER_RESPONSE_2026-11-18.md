# Reviewer response ledger — 2026-11-18

Records the external review round on the pushed bundle and the disposition of each point. This is a
provenance record, not a scientific finding. Nothing here changes a frozen document; where a label in
this bundle was wrong, the correction is applied in place and noted below.

**Reviewed object:** branch `audit/analytical-validity-2026-11-18`, head `bec7d60`.
`master` remains `33dca9b`; `research/concentration-math-spec` remains `de39291`. No merge.

---

## 1. Disposition table

| # | Point | Raised by | Disposition | Where applied |
|---|---|---|---|---|
| A | W1 must not be called a failed positive control; no known `Δ_pred` was injected | GPT and Claude, independently | **Accepted** | `FUNDAMENTAL_GOAL...` §2, §4 row 1, gate-4 row; `claude-keys-verification` §0, §1; bundle `README` challenge 2 |
| B | The `F`-vs-`C` advantage is domain-weighted only; equal-weighted fails; domain weighting may favour the dominance pattern by construction | Claude | **Partly accepted — hypothesis recorded, test specified, not run** | Bundle `README` challenge 7 |
| C | The solver-level unit is the most important open item | Claude | **Clarified** — does not apply to W1; decisive for the real design | Bundle `README` challenge 8; `claude-keys-verification` §3 |
| D | "Control or collider?" for `k_unresolved` is unresolved | Claude | **Accepted, remains open** | `claude-keys-verification` §9; bundle `README` challenge 4 |
| E | Publication is not adoption; `/pull/new/` is a creation link, not an existing PR | GPT | **Accepted** — earlier phrasing was ambiguous | this file §2 |
| F | Excluded raw archives must stay documented | GPT | **Accepted** | bundle `README` "What is not here" |
| G | The two commits have different purposes and should stay separate | GPT | **Accepted, no change needed** | this file §2 |

---

## 2. Publication status, stated precisely

- Branch `audit/analytical-validity-2026-11-18` at `bec7d60`, pushed.
- `90a936b` = the audit bundle and the fundamental goal.
- `bec7d60` = 41 previously uncommitted research documents plus four modified tracked files.
- `master` = `33dca9b`; `research/concentration-math-spec` = `de39291`. Neither moved.
- **No pull request exists.** The URL returned by the remote is GitHub's PR *creation* form. Opening
  one is an owner decision.
- Excluded and still local: `three_world/raw/` (~560 MB), `_quarantine/` (~618 MB),
  `per_trial.json` (~31 MB), `stratum_specific_analysis_2026-10-24/`, and 21 `.qoder*` scratch
  entries. Rationale recorded in the bundle `README`.

---

## 3. Point B — the domain-weighting hypothesis, made testable

Claude's conjecture: the domain-weighted score `S_D` rewards cases whose failures already sit in large
families, so the domain arm favours the dominance pattern by construction.

**What the design actually specifies** (`10_THREE_WORLD_SIM_DESIGN.md:21–43`):

```
N = (9, 9, 23, 23, 31, 3),  sum = 98
S_D = 1 - (sum_j e_j) / 98            # weights families by N_j
S_F = 1 - (1/6) sum_j (e_j / N_j)     # weights families equally
```

Diagnostic families are **equal-sized**: five probes each, 30 total. Evaluation families are
**unequal**: 9, 9, 23, 23, 31, 3.

Consequences that bear on the conjecture:

1. The asymmetry is **size weighting**, not dominance weighting as such. A defect in family 6
   (`N = 3`) produces the same expected diagnostic failures `f_6` as a defect in family 5 (`N = 31`),
   but roughly one tenth the evaluation failures. So the two arms disagree most about small families,
   which is where `S_F` amplifies the per-family rate by `1/N_j`.
2. `C` is computed on the equal-sized diagnostic partition. So a defect in family 6 can produce a
   high `C` with little `S_D` damage. That weakens, rather than strengthens, a mechanical
   `C → S_D` advantage.
3. Both the `C` model and the baseline are **family-adjusted** (`M0+fam` vs `M1+fam`). A pure
   size-weighting artefact would have to survive those indicators.

**Test, not yet run:** from `three_world/per_trial.json` (local, ~31 MB), recompute `S_D` with
equalised `N_j` per trial and refit `M0+fam` and `M1+fam`. If the `F` margin is a size-weighting
artefact, it should shrink toward the equal-arm result. If it persists, the equal-arm failure has a
different cause. Either outcome is informative and neither is currently known.

**Status:** open. The audit reports the domain result and the equal-arm failure; it does not claim a
mechanism for the difference.

---

## 4. Point C — why the solver-unit problem does not apply to W1

Claude is right that a solver-level covariate needs a solver-level sample size. Two separate facts
must not be conflated:

1. **W1 has no solver clustering.** Cases are drawn as
   `f_j ~ Binomial(5, q^D_j)` and `e_j ~ Binomial(N_j, q^E_j)`, "independently conditional on the
   defect reaches" (`10_THREE_WORLD_SIM_DESIGN.md:58`). The design states outright that it "does not
   preserve input-level dependence". So there is no solver random effect in W1 to omit, and the
   2.5 M-case fit is internally valid for the world it defines.
2. **The reported interval is a trial-level interval**, not an input-level confidence interval:
   "central 95 % simulation-trial intervals, not confidence intervals about a real population"
   (`11_THREE_WORLD_SIM_RESULT.md`). It describes variation across 500 trials, not precision per
   input.

Therefore: W1 cannot be faulted for missing a solver effect, **and it cannot speak to the clustered
world at all**. That is a narrower and more damaging limitation than the one Claude states, and it is
the reason the future S1–S7 suite must carry crossed random effects.

For the real design the unit is the **parent** (30 in the LC518 roster), not the solver, because
variants are nested within parents. The MDE arithmetic in `claude-keys-verification` §3 stands.

---

## 5. What did not change

- No frozen record, protocol, threshold, bank, or population document was altered.
- No claim in the audit bundle was reversed. Point A changes a label that the bundle had already
  flagged as an overstatement; it does not change the W1 numbers or the fact that the pipeline has
  never been shown to recover an effect.
- `F`-versus-`C` remains reported with its qualification: domain PASS, equal FAIL, overall FAIL.
- The 2026-11-01 reviewer concurrence with a NO-GO recommendation, the absence of any owner GO/NO-GO
  decision, and the absence of a route-closure record are unchanged facts.

## 6. Open items and who owns them

| Item | Owner | Blocker |
|---|---|---|
| Run the equalised-`N_j` refit (Point B) | analysis | local `per_trial.json`; no new model calls |
| State the `k_unresolved` DAG (Point D) | design | no causal diagram exists in the record |
| Decide whether to open a PR | owner | publication is not adoption |
| ~~Verify whether any S1 scenario can inject a known `Δ_pred`~~ | design | **resolved — see §7** |
| Confirmatory vs exploratory route | owner | recorded as "OWNER DECISION OPEN" |

---

# Round 3 — GPT and Claude, on S1

**Reviewed object:** branch `audit/analytical-validity-2026-11-18`, head `4f9ee8c`. Both reviewers
accepted the W1 correction and turned to the next question: can a simulation carry a *known* gain?

## 7. Disposition table, round 3

| # | Point | Raised by | Disposition | Where applied |
|---|---|---|---|---|
| H | "November 1 NO-GO still stands" overstates the record — it was a recommendation, not a decision | Claude | **Accepted** | `claude-keys-verification` §0, §12 item 5; bundle `README` item 10; this file §2 |
| I | 30 parents × 5 variants is **not adopted**; the hierarchy was described as if it were | Claude | **Accepted** | `claude-keys-verification` §3 and the MDE table |
| J | An injected gain tests the estimator only under the generator's assumptions | Claude | **Accepted; made structural** | `S1_SPECIFICATION` §10 |
| K | The proxy world depends on the control set; show it both ways | Claude | **Accepted; contrast is the result** | `S1_SPECIFICATION` §6, S1-W3 |
| L | The 2026-11-10 rule forbids Monte Carlo and predictive fitting until an explicit GO | Claude | **Accepted in substance, date corrected** | `S1_SPECIFICATION` §11 |
| M | The target must be `Δ_pred = E[L₀−L₁]`, in nats, not a coefficient | GPT | **Accepted; identified exactly** | `S1_SPECIFICATION` §3 |
| N | Compute the true gain by Monte Carlo from the generator, same scoring rule; include solver random effects; report bias, coverage, FPR | Claude | **Partly accepted** — exact enumeration instead of Monte Carlo; random effects in W5; all three reported | `S1_SPECIFICATION` §4, §6, §9 |
| O | Three distinct questions for the `F`-vs-`C` test: equal weighting, family indicators, independent parents | GPT | **Accepted; enumerated** | this file §7.3 |

## 7.1 Point L — the gate, with the right citation

Claude places the rule on 2026-11-10. The operative text is in the B1 plan:

> "Not authorized and not performed: numerical probability evaluation, executable simulation, Monte
> Carlo or permutation *execution*, fitting of any model, … Execution of anything this plan declares
> requires a further explicit GO after this plan is reviewed and accepted."
> — `B1_ANALYSIS_PLAN_2026-11-14_v1.1.md:7`

The 2026-11-10 record is the capacity/power addendum, which states "not a GO, not a ratification of
B1". Same substance, different document, four days apart. The citation is corrected because a reviewer
who checks 11-10 for that sentence will not find it.

**One consequence matters for sequencing:** the authorization basis is *"bounded GO (design and
mathematics only)"*. Design and mathematics are **authorized now**. Executing is not. So writing the S1
specification required no new GO, and running it requires exactly one.

## 7.2 Point M — the target, identified rather than approximated

GPT's formulation is right and has an exact closed form:

```
Δ_pred = I(Y ; C | X)   (nats per input)
```

because `E[log p(Y|X,C) − log p(Y|X)] = Σ p(x,c) KL(p(·|x,c)‖p(·|x)) = I(Y;C|X)`.

This does better than the request. GPT asked that the gain be *calibrated* to a target by tuning
parameters. It can instead be **imposed**: fix the diagnostic marginal, declare
`p(y=1|x,c) = σ(α_x + γ c)`, and bisect on `γ` until the enumerated information equals the target. The
gain is then known to machine precision before a single data row is drawn, and it is not a Monte Carlo
estimate of itself.

That closes the recursion GPT's caution implies — a simulated gain estimated by Monte Carlo, then used
to validate an estimator, is two layers of estimate stacked. Exact enumeration removes one.

## 7.3 Point O — GPT's three questions, made into three runs

GPT is right that these are three questions and not one. They map onto distinct analyses, only the
first of which can be run from the local archive:

| Question | How it is answered | Status |
|---|---|---|
| Does the `F` advantage survive equal family weighting? | already reported: **no** — the equal arm fails (`11_THREE_WORLD_SIM_RESULT.md`) | answered, negative |
| Does it survive family indicators in the model? | both arms are already family-adjusted (`M0+fam` vs `M1+fam`), so the *domain* result is conditional on indicators; the equal arm failing *with* indicators is the live question | partly answered |
| Does it generalise across independent parents? | **cannot be answered from W1** — W1 has no parent level by construction (independent Bernoulli draws). Requires S1-W5 | impossible in the current corpus |

The third row is the important one: it is not an unrun analysis of existing data, it is a missing level
of the existing design. No amount of reweighting `per_trial.json` supplies it.

## 7.4 Point J — how the "tests only the generator" objection is handled

Claude's objection is correct and cannot be argued away. The specification therefore does three things
rather than one:

1. **States the scope in the header** — S1 is an instrument test; passing says the thermometer works.
2. **Makes vacuity a failing outcome** (§10): if reaching the target requires `C` to reproduce `k`, or
   if `Δ_pred(γ)` saturates below the target, S1 reports "not testable", not "pass".
3. **Separates the mechanism question entirely** — whether real solvers have `Δ_pred > 0` is untouched,
   and the LC518 strata are still input categories, not mechanisms.

## 7.5 Point N — why exact enumeration rather than Monte Carlo

Claude asks that the true gain be computed by Monte Carlo from the generator. The intent is right — the
gain must be computed, not asserted — but Monte Carlo is the weaker instrument here, because the
support is finite and small: `k ∈ {0..30}`, `C` a rational with denominator `k`, six families. The
information integral is a finite sum. Enumerating it gives the exact value; sampling gives that value
plus error. The only place sampling remains necessary is the *fitting* stage, which is where the
estimator's behaviour is measured.

## 7.6 Point I — what the unit actually is, now

The hierarchy is accepted as **structure** and rejected as **count**:

- parent = independent unit (generalisation);
- variant = nested, buys within-parent precision;
- input = nested, buys per-variant precision.

`J_par` is left open and reported as a grid. The MDE table in `claude-keys-verification` §3 now labels
`J = 30` as a logistics scenario rather than a roster.

## 7.7 What remains genuinely unresolved

| Item | Why it cannot be closed here |
|---|---|
| `F`-vs-`C` equal-weight mechanism | needs the equalised-`N_j` refit on local `per_trial.json`; not run |
| Parent-level generalisation of any `F` result | W1 has no parent level; needs S1-W5 |
| `k_unresolved` control-vs-collider | no DAG recorded; both roles remain possible |
| Adopted operating count | no prospective precision objective exists |
| Any claim about real solvers | no mechanism theory, and LC518 has 0/150 solvers evaluated |
