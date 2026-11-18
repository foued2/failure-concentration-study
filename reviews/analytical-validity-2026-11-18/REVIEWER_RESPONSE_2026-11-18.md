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
- The NO-GO record of 2026-11-01 and the absence of a route-closure record are unchanged facts.

## 6. Open items and who owns them

| Item | Owner | Blocker |
|---|---|---|
| Run the equalised-`N_j` refit (Point B) | analysis | local `per_trial.json`; no new model calls |
| State the `k_unresolved` DAG (Point D) | design | no causal diagram exists in the record |
| Decide whether to open a PR | owner | publication is not adoption |
| Verify whether any S1 scenario can inject a known `Δ_pred` | design | requires a mapping from reach to estimand |
| Confirmatory vs exploratory route | owner | recorded as "OWNER DECISION OPEN" |


---

## 7. Round 3 — DeepSeek web-chat S1 sequence, 2026-11-18

| Point | DeepSeek's instruction | Disposition |
|---|---|---|
| A | The S1 document is not yet published and must not be listed as an achievement | **Accepted.** The S1 document is now added as a clearly labelled draft for review; no claim of prior publication is made. |
| B | Specify the true outcome model before the estimator; calculate the gain from the generator, not from the estimator | **Implemented in draft.** The outcome model is driven by latent state \(H\), parent effect \(U\), and input difficulty \(X\). \(C_D\) is not in the outcome equation. The population gain is derived by marginalizing the declared generator. A separate exact conditional risk calculation is specified for each fitted training pair. |
| C | Explicitly test and explain circularity | **Implemented in draft.** Section 8 gives the dependency structure and explains the distinction between the generator and the estimator. Whether this is sufficient is explicitly submitted for DeepSeek's web-chat review. |
| D | Fix bias, coverage, and false-positive tolerances before any run | **Proposed in draft.** Section 7 gives numeric thresholds and their Monte Carlo rationale. They are not frozen until independently reviewed. |
| E | Defer the real parent-count decision until S1 variance information exists | **Accepted.** The proposed \(J\) values are calibration-grid dimensions only. They are not a sample-size recommendation or an adoption of the LC518 roster. |
| F | Treat writing generator code as implementation outside design-only authorization | **Accepted.** The draft expressly prohibits code, execution, fitting, and bank reuse under the current scope. |

**Review handoff:** S1_KNOWN_GAIN_SPEC_2026-11-18.md is submitted to DeepSeek in the web chat for a section-specific independent review. The draft remains unaccepted and unfrozen. No code was created and no simulation was run. No execution GO was requested or inferred.


---

## 8. DeepSeek web-chat review of S1 v0.1 and disposition in v0.2 — 2026-11-18

**Reviewed object:** \`S1_KNOWN_GAIN_SPEC_2026-11-18.md\`, v0.1.  
**Reviewer:** DeepSeek web chat. This is not a local-agent review.  
**Disposition:** v0.2 is revised for a second DeepSeek review; it is not accepted or frozen.

| DeepSeek finding | Adjudication | v0.2 response |
|---|---|---|
| §2 target ambiguous between fixed-panel and input-superpopulation gain | **Accepted** | Estimand is explicitly panel-conditional: fixed 60-item panel, 20 per difficulty class, equal class weights; no new-input-panel generalization. |
| §2 log-loss scale lacks rationale | **Accepted** | Strict propriety, information-theoretic identity, natural-log units, and distinction from Brier/AUC/calibration error are stated. |
| §3.1 two-valued \(C_D\) means only a binary proxy is tested | **Accepted** | S1 is explicitly a binary-proxy calibration with \(C_D\in\{0.50,0.75\}\), not a general multi-valued concentration test. |
| §3.2 parent-effect marginalization is not shown | **Accepted** | The full sum over \(H\) and \(U\) is displayed. It shows why the single-variant marginal shift is \(p_x\pm0.6\eta\), while shared-parent dependence remains. |
| §4.1 signal coefficient 0.12 lacks provenance | **Partly accepted** | It is now an explicitly analyst-selected DGP parameter, not an estimated or empirical coefficient. A pre-run \(\eta\in\{0.06,0.12,0.18\}\) grid and exact gains are given. The signal grid remains a synthetic design choice requiring review. |
| §4.2 equality \(I(Y;F\mid X)=I(Y;C_D\mid X)\) is unproven | **Accepted and proved for this DGP** | \(F\) is decomposed into the binary \(Q\) signal and ancillary randomization \(A\). The chain-rule proof is supplied. The document now labels this as a deliberately favourable property, not a general fact. |
| §4.3 gain values need independent recomputation | **Accepted** | Bernoulli-KL formula, class contributions, primary gain, and signal-grid gains are provided with reproducible precision. |
| §5.1 marginal estimator does not validate B1 v1.6 | **Accepted** | A precise inference-transfer boundary is added. S1 pass validates only the specified marginal saturated binary-proxy estimator; a separate B1 bridge is required. |
| §5.2 fitted-pair truth needs formal status | **Accepted** | \(\Delta_{\mathrm{fit}}\) is explicitly the known conditional truth for each fitted training pair, distinct from the Bayes limit \(\Delta^*\). |
| §5.3 bootstrap omits training-fit variability | **Accepted with scope clarification** | The interval is explicitly conditional on the training fit and fixed panel; coverage targets replication-specific \(\Delta_{\mathrm{fit}}\). Training variability is summarized across independent replications. No claim that this interval covers \(\Delta^*\). |
| §6 matched null is missing | **Not accepted as a factual description of v0.1** | Section 6 existed in the actual v0.1 document and stated \(\eta=0\), unchanged diagnostic process, and \(Y=p_x+U_g\). It has nevertheless been expanded to list the complete unchanged hierarchy and why \(\Delta^*=0\). |
| §7.1 parent grid lacks precision rationale | **Partly accepted** | The geometric doubling and relative \(1/\sqrt J\) standard-error scaling are stated. Absolute interval widths remain unknown until the parent-level variance is established; this is explicitly left unresolved rather than fabricated. |
| §7.2 tolerances lack rationale | **Partly accepted** | Rationale and sensitivity reporting are added for learning recovery, relative bias, coverage, detection, false-positive rate, and availability. Values remain provisional for DeepSeek review; no result can select among sensitivity cut-offs post hoc. |
| §8 saturated estimator is favourably matched to generator | **Accepted** | This is now an explicit favourable feature. S1 does not test misspecification robustness. |
| §9 minimum positive inference is unstated | **Accepted** | The exact inference supported by a pass and the claims not transferred to B1 or real solvers are stated. |

### Remaining questions for DeepSeek

1. Is the panel-conditional target the correct first calibration target, or should S1 additionally include a separately defined input-superpopulation target?
2. Is the binary-proxy positive world acceptable as a first calibration, given its deliberately favourable sufficiency of \(C_D\) for \(F\)?
3. Is the \(\eta\) grid defensible, and are the stated calibration tolerances justified?
4. Is the conditional parent-cluster bootstrap adequate for \(\Delta_{\mathrm{fit}}\), or is a different uncertainty procedure required?
5. Is the proposed separation between this marginal calibration and a future exact-B1 bridge the correct sequence?

The full reviewer report's observation that §6 was missing is respectfully challenged: the section was present in the v0.1 source. The v0.2 expansion is supplied to remove any ambiguity about the null construction.
