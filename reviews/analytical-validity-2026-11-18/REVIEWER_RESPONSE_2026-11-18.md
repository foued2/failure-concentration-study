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

The first-round report's description that §6 was missing was corrected because §6 was present in the v0.1 source. That was recorded as a factual disagreement at the time. In the supplied second-round response, DeepSeek explicitly accepts the correction. The presence dispute is therefore closed; the remaining review question is whether the expanded v0.2/v0.3 null specification is substantively adequate.


---

## 9. Round 4 — independent critique and provisional DeepSeek second-round review, 2026-11-18

**Review materials received:** an owner-supplied combined note containing Claude's critique of the v0.2 handoff and DeepSeek's second-round response.

**Reviewer identity:** Claude is not the S1 reviewer. The active independent reviewer remains DeepSeek in the web chat. Claude's points below are treated as an additional challenge, not as a review approval or a replacement for DeepSeek.

**DeepSeek's evidentiary limit:** DeepSeek stated that it could not fetch the GitHub links in its chat session. Its v0.2 assessment is therefore explicitly provisional and based on the handoff summary, not a direct inspection of the specification, equations, or section text. It is not a freeze approval.

### 9.1 Adjudication

| Point | Raised by | Adjudication | v0.3 treatment |
|---|---|---|---|
| \(C_D\) is a one-to-one recoding of \(Q\); the binary proxy is the actual signal available to the estimator | Claude; consistent with DeepSeek's binary-proxy concern | **Accepted.** This is a favourable proxy-recovery benchmark, not a test that concentration is uniquely informative or that a general maximum statistic is sufficient. | The purpose, §3.2, §4.1, and §9 now state the bijection and its inference limit explicitly. |
| \(I(Y;F\mid X)=I(Y;C_D\mid X)\) is built into the construction | Claude | **Accepted as a limitation, not a mathematical error.** The proof is retained only as a property of this generator. It cannot support a general claim that the full failure vector adds no information. | §4.1 now calls it a generator identity and says the design cannot support an empirical or general compression claim. |
| Whether §6 was missing in v0.1 | DeepSeek's first-round review; correction raised by GPT | **Closed factual issue.** DeepSeek's second-round response says it accepts the correction that §6 was present in v0.1. | The v0.2 history is preserved; the current record states that the presence dispute is closed. The adequacy of the expanded null remains reviewable. |
| The panel-conditional estimand needs a formal fixed-panel expression and explicit \(\eta\) dependence | DeepSeek | **Accepted.** | §2.2.1 averages explicitly over the 60 fixed panel positions; the gain is indexed by \(\eta\). |
| Entropy/KL arithmetic should be independently checkable for every difficulty class and \(\eta\) | DeepSeek | **Accepted.** | §4 gives the class-specific average KL contributions across all three predeclared signal strengths. |
| The coverage target must distinguish average conditional coverage from marginal coverage | DeepSeek | **Accepted.** | §5.5 defines coverage conditional on each training fit and then averaged over training fits. It does not claim coverage of \(\Delta^*\). |
| Tolerances need an explicit \((J,\eta)\) decision structure, absolute bias units, and Monte Carlo precision | DeepSeek | **Accepted with a declared primary-only gate.** | §7 marks \(J=120,\eta=0.12\) as the sole positive-world gate; all other positive cells are report-only; the null false-positive gate applies at all three \(J\) values. Absolute bias equivalents and Monte Carlo standard errors are specified. |
| Ask whether the binary-proxy advantage is acceptable before asking for approval | Claude | **Accepted.** | §10 asks first whether this deliberately favourable proxy-recovery calibration is useful or should be changed. It explicitly requests objections, not approval. |
| A separate confounding control must distinguish an unadjusted proxy association from information remaining after observing the common cause | Claude; also relevant to DeepSeek's proxy/mechanism question | **Accepted as the required S3 design property.** | §8 says S3 must retain the unadjusted association, observe \(H\), and compare \(X,H\) with \(X,H,C_D\); it is not replaced by the \(\eta=0\) matched null. |

### 9.2 What remains unresolved

1. Whether the deliberately favourable binary-proxy calibration is an acceptable first-stage test for the project, or should be redesigned before any implementation.
2. Whether the single primary positive-world gate at \(J=120,\eta=0.12\) and the proposed pass bands are defensible.
3. Whether the test-parent cluster bootstrap has adequate finite-cluster coverage at the primary point.
4. Whether the marginal S1 estimator is a useful preliminary calibration before a separate exact-B1 v1.6 bridge.
5. Whether a misspecification arm should be added to S1 or explicitly specified as a separate later calibration.

### 9.3 Current disposition

S1 v0.3 is a revised design draft returned for direct, section-specific DeepSeek review. The available second-round review is not direct verification because the reviewer could not access the file. No freeze, implementation, simulation, model-fitting, bank-reuse, or execution GO follows from this round. The next review must be based on the actual v0.3 text supplied directly in the DeepSeek chat, not on a GitHub link it cannot fetch.


---

## 10. Round 5 — DeepSeek's direct review of S1 v0.3 and Claude's handoff critique, 2026-11-18

**Review materials:** direct, section-specific DeepSeek review of the complete v0.3 text (owner-supplied file), plus Claude's critique of the preceding handoff.

**Reviewer identity:** DeepSeek is the active independent S1 reviewer. Claude supplied an additional critique of scope and handoff logic; Claude did not review the v0.3 mathematics directly.

### 10.1 DeepSeek's direct assessment

DeepSeek's central verdict was: **"Defensible as a narrow first-stage calibration, with one condition."** It found no mathematical or statistical error in the construction, fixed-panel estimand, KL arithmetic, latent common-cause model, fitted-pair truth, conditional parent-cluster bootstrap target, or generator-specific full-vector equality.

| Issue | DeepSeek's direct assessment | Disposition in v0.4 |
|---|---|---|
| Binary \(Q\) and \(C_D\) | The bijection is algebraically consistent; acceptable for a narrow first stage. It is a blocker only if used to claim that the max statistic is a generally useful summary or to validate B1. | **Accepted.** The scope now says a pass is compatible with \(C_D\) being useless as a general summary statistic. |
| Fixed-panel estimand and KL values | Mathematically correct and reproducible. DeepSeek suggested noting monotonicity over the \(\eta\) grid. | **Accepted.** A derivative argument is added to §2.2.1. |
| Latent common-cause model | Correct for a predictive-proxy benchmark; not a general concentration benchmark. | **Accepted.** §1 now says S1 has no direct real-solver inference. |
| Fitted-pair truth and bootstrap | Correctly defined. The conditional/marginal distinction is properly handled. | **Accepted.** Gate-specific Monte Carlo precision is made explicit. |
| Monte Carlo precision for coverage | The 95% binomial standard error at 2,000 replications is approximately 0.0049. | **Already specified.** §7.3 reports 0.004873 near 95% coverage. |
| 80% recovery tolerance | An engineering choice, not a statistical necessity. Its scientific decision rationale is not established. | **Accepted as provisional.** §7 says this is an engineering tolerance, not a decision threshold. |
| 10% bias tolerance | The absolute margin is stated, but its detectability is unknown without parent-level variance. | **Accepted as provisional.** §7.3 now states the MCSE and confidence interval for the mean recovery ratio and mean bias; results can be inconclusive. No pre-run variance is invented. |
| Full-vector equality | Correct for this generator; effectively vacuous for the scientific question because other vector details are ancillary by construction. Retaining it aids transparency. | **Accepted.** Retained only as a generator identity, not a general or empirical result. |
| Matched null | DeepSeek's direct wording: **"The matched null is adequate as a minimum false-positive companion."** It preserves the diagnostic process, parent clustering and parent-effect distribution. Both positive and null worlds have \(k_{\mathrm{unresolved}}=0\). | **Accepted with an explicit boundary.** §6 now says it is matched only in a no-unresolved setting and does not test unresolved-outcome handling. |
| S3 | DeepSeek's direct wording: **"S3 must demonstrate the incremental information beyond the common cause."** | **Accepted.** §8 keeps the oracle \(H\)-adjustment distinct from the \(\eta=0\) matched null and flags imperfect-proxy adjustment as a separate possible scenario. |
| B1 v1.6 | A separate known-truth calibration is required, including a non-binary/multi-valued generator, the exact B1 estimator and conditional-randomization procedure, matching null, matching uncertainty target, and inference boundary. | **Accepted.** No S1-to-B1 inference transfer is allowed. This is a hard blocker for B1 claims, not for the limited S1 machinery check. |

### 10.2 Claude's additional challenge

Claude's key correction is that the handoff should not imply S1 can answer an empirical question about real solvers. This is accepted. S1 can answer only whether this particular estimator and test-parent uncertainty procedure recover known information under its synthetic setup.

Claude also asked that the project name a decision changed by S1. This is now explicit in §1: a complete pass permits carrying the machinery forward to further synthetic validation; a failure requires revising or rejecting the estimator/uncertainty combination; an inconclusive result does not permit progression. None of those outcomes changes the evidence about real-solver predictive value. If the project will not use this methodological proceed/revise/stop decision, S1 should not be run.

### 10.3 Remaining cautions and disposition

1. The 80% recovery and 10% bias tolerances remain provisional engineering choices. Their achieved Monte Carlo precision is unknown until replication-level variances are measured. Any pilot-based revision requires separate authorization and a distinct confirmatory run; pilot replications are not pooled.
2. The matched null has \(k_{\mathrm{unresolved}}=0\) in both worlds. It does not validate unresolved-outcome handling; S6 must do that.
3. The proposed S3 observes the true common cause \(H\), so it is an oracle adjustment. A design using only imperfect proxies for defect identity may require a further scenario.
4. A pass in S1 remains a machinery result for this favourable binary-proxy generator, not evidence that concentration is a useful general summary and not a result about real solvers.
5. B1 v1.6 remains unvalidated until its exact estimator and conditional-randomization procedure are tested against a matching known-truth generator.

**Current version:** S1 v0.4, recorded in the same branch. It is awaiting direct DeepSeek review of the v0.4 text. The v0.3 review does not approve or freeze v0.4. No freeze, implementation, simulation, model fitting, bank reuse, solver construction, or execution GO follows from this round.
