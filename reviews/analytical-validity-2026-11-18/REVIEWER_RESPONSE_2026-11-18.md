# Reviewer response ledger — 2026-11-18

Records the external review round on the pushed bundle and the disposition of each point. This is a
provenance record, not a scientific finding. Nothing here changes a frozen document; where a label in
this bundle was wrong, the correction is applied in place and noted below.

**Historical bundle-review snapshot for §§1–6:** branch `audit/analytical-validity-2026-11-18`, head `bec7d60`. This is a record of the original bundle review, not a current-branch-head assertion. Later S1 review rounds identify their own document versions and review objects below.
`master` was `33dca9b` and `research/concentration-math-spec` was `de39291` at that historical snapshot. No merge was made.

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


---

## 11. Round 6 — DeepSeek's direct review of S1 v0.4 and Claude's follow-up, 2026-11-18

**Review materials:** the owner-supplied direct DeepSeek review of v0.4, plus Claude's follow-up challenge to the decision consequence, oracle-S3 limitation, and S6 status.

**Reviewer identity:** DeepSeek remains the direct S1 reviewer. Claude's text is an additional critique, not an independent direct inspection of the v0.4 equations.

### 11.1 DeepSeek's direct v0.4 verdict

DeepSeek states that its v0.3 recommendation still holds: S1 is defensible as a narrow first-stage calibration and has no identified mathematical/statistical defect, but should not be frozen until the decision consequence and precision presentation are explicit. It considers the strengthened inference-transfer wording adequate and the no-unresolved matched null adequate for minimum false-positive calibration.

| Issue | Direct review disposition | Project adjudication |
|---|---|---|
| \(C_D\) is bijective with \(Q\) | **Accepted limitation**, not a defect. No blocker for a narrow machinery check; hard blocker for B1 or general-summary claims. | v0.5 keeps the narrow inference boundary and adds the positive claim a complete pass licenses. |
| Positive inference | Reviewer says v0.4 mostly meets the condition, but should state what passing does license. | **Accepted.** v0.5 states that a pass licenses only recovery of a known binary-proxy predictive gain by the marginal six-cell estimator and parent-cluster procedure under independent parent sampling on the fixed panel. |
| Concrete decision consequence | A proceed/revise/stop structure exists, but reviewer says the downstream project decision needs to be named. | **Accepted.** The decision is whether to retain the current \(M_0/M_1\) plus test-parent cluster-bootstrap procedure as the candidate method for S2-S7. Pass carries it forward for S2-S7 specification; fail requires revision; inconclusive blocks progression. |
| Recovery and bias MCSE | Reviewer says the formulas were not visible in the copy it examined. | **Copy discrepancy recorded.** The v0.4 blob on the review branch immediately before this revision already contained \(MCSE(\bar r)\), \(MCSE(\bar b)\), their 95% Monte Carlo intervals, and explicit pass/fail/inconclusive rules. It is not possible to determine whether the reviewer saw an earlier copy or overlooked those passages. v0.5 displays the formulas together and restates the inconclusive rule to remove ambiguity. |
| False-positive precision | Reviewer asks for MCSE per \(J\). | **Accepted.** v0.5 gives the per-\(J\) formula and a table for \(J=30,60,120\), each with 2,000 planned attempted null replications; the MCSE uses the actual valid denominator, with reference values shown for 2,000 valid replications. |
| Matched null | Direct verdict: **adequate as a minimum false-positive companion**. It preserves diagnostic and parent nuisance structure; both worlds have \(k_{\mathrm{unresolved}}=0\). | **Accepted.** v0.5 explicitly says unresolved-outcome handling remains untested and S6 is required. |
| S3 | Oracle adjustment is appropriate as a first step, but not enough for a feasible-adjustment or real-world claim. | **Accepted.** v0.5 distinguishes S3a (oracle \(H\) adjustment) and S3b (imperfect proxy \(W\)); both remain synthetic and neither validates real solvers. |
| B1 v1.6 | Separate bridge with a multi-valued/non-binary generator, exact B1 estimator and conditional-randomization procedure, matching null, matching uncertainty target and inference boundary. | **Accepted.** Hard blocker for any B1 validation claim; no S1 transfer. |

### 11.2 Claude's follow-up

Claude's central point is adopted: the decision needs to be stated in one concrete sentence, not just described as a general progression rule. The chosen decision is:

> **S1 decides whether the current \(M_0/M_1\) marginal estimator plus test-parent cluster-bootstrap procedure is retained as the candidate method for the S2-S7 validation suite.**

Claude's S3 point is also adopted: the oracle adjustment is not sufficient to assess feasible adjustment when the true common cause is not observed. S3 is now split into an oracle diagnostic (S3a) and an imperfect-proxy stage (S3b). Claude also asked whether S6 exists in the actual specification rather than only in a summary. It does appear in §9 as a required future scenario and is explicitly marked **named but not specified or frozen**. It is not represented as a completed scenario.

### 11.3 S1 v0.5 changes and remaining state

v0.5:
- names the single downstream methods decision and its pass/fail/inconclusive consequences;
- states the positive inference licensed by a pass;
- displays the recovery-ratio and mean-bias MCSE equations with their 95% Monte Carlo intervals and overlap-is-inconclusive rules;
- gives the null false-positive MCSE explicitly for each \(J\);
- distinguishes S3a oracle adjustment from S3b imperfect-proxy adjustment;
- confirms that S6 is only a named future requirement and is not yet specified.

**Important execution boundary:** the specified S1 decision is internal to the analytical-methods programme. It does not change the scientific evidence about concentration or real solvers. A pass only carries the estimator candidate into S2-S7 specification/review; it does not authorize S2-S7 implementation or execution. If the owner does not intend to use this estimator-selection decision, S1 should not be run.

DeepSeek's v0.4 recommendation does not freeze v0.5. The current specification remains a design draft awaiting direct review of v0.5. No freeze, implementation, simulation, model fitting, bank reuse, solver construction, or execution GO follows from this round.


---

## 12. Round 7 — DeepSeek's direct review of S1 v0.5 and Claude's replication/provenance challenge, 2026-11-19

**Review materials:** the supplied DeepSeek review, which reports direct examination of S1 v0.5 and the Round 6 reviewer ledger, plus Claude's follow-up on decision relevance, review-object provenance, and Monte Carlo precision.

### 12.1 DeepSeek's direct v0.5 verdict

DeepSeek's verdict is that S1 v0.5 is defensible as a narrow first-stage machinery check. It found no mathematical or statistical defect that prevents that limited use, and it considers the existing proceed/revise/stop decision operational **provided that the project actually uses it**.

| Issue | DeepSeek's direct assessment | Adjudication |
|---|---|---|
| Decision consequence | The pass/fail/inconclusive consequences are clear. A hard blocker arises if the project would advance to S2 regardless of S1. | **Accepted with the stronger Claude stop rule.** v0.6 states that if S2-S7 proceed unchanged regardless of S1, or choose their estimator independently, S1 must not be run. A separate owner commitment to use this gate is required before execution. |
| Positive inference | Adequate. It licenses only recovery of the binary-proxy gain under the fixed-panel independent-parent generator and says nothing about real solvers or a general summary statistic. | **Accepted.** v0.6 additionally states that the matched null is limited to \(k_{\mathrm{unresolved}}=0\) in both worlds. |
| Recovery/bias MCSE | Formulas and inconclusive logic are acknowledged in the Round 6 ledger. DeepSeek says it could not independently verify the formulas in its rendered copy because of page truncation. | **No missing-formula defect established.** The v0.5 source object and v0.4 predecessor were compared by blob. Their §7.3 text is byte-for-byte identical and contains the \(MCSE(\bar r)\), \(MCSE(\bar b)\), t-based interval formulas, and inconclusive rules. v0.5 also added a separate per-\(J\) false-positive reference table in §7.2. The precise file blob DeepSeek examined remains unconfirmed because its report gives no Git blob SHA. |
| Per-\(J\) false-positive precision | Confirmed in the Round 6 ledger and judged adequate. | **Accepted.** v0.6 retains the per-\(J\) table and clarifies the actual valid denominator. |
| §6 matched null | Adequate as a minimum no-unresolved null. It preserves diagnostic and parent nuisance structure; both worlds have \(k_{\mathrm{unresolved}}=0\). | **Accepted.** It does not test unresolved-outcome handling. |
| S3a/S3b | Oracle S3a is a useful diagnostic; S3b is necessary before a feasible-adjustment claim. | **Accepted.** v0.6 retains both stages and makes their distinct roles explicit. |
| S6 | Correctly named as required future work, but not yet specified. | **Accepted.** S6 remains named but not specified or frozen. |
| General validity | No mathematical/statistical defect prevents the narrow S1 machinery check. B1 v1.6 still needs its own exact-estimator known-truth bridge. | **Accepted.** No S1-to-B1 inference transfer. |

DeepSeek's recommendation was that v0.5 could be frozen for its narrow purpose, conditional on the project genuinely using the downstream estimator-selection decision. It did **not** recommend or imply an execution GO.

### 12.2 Claude's additional challenges and v0.6 response

**A. S1 must have a real stop rule before execution.** Claude asks what S2-S7 discover that S1 cannot. v0.6 now explains that S1 is a baseline known-positive recovery check only. S2 tests null specificity; S3a/S3b test oracle and imperfect-proxy adjustment; S4 tests partition sensitivity; S5 tests crossed dependence; S6 tests unresolved outcomes; and S7 tests degenerate or unsupported support. If those later scenarios and their estimator choices proceed regardless of S1, then S1 has no sequencing value and must not be run. The owner must explicitly commit to using S1's result as the candidate-method gate before execution.

**B. Review-object provenance must be hash-based.** The v0.5 Git blob on the review branch at the start of this round was 6210f8b95a2f9dbceea3606a7aa1f4dad7cb7e21. Its v0.4 predecessor blob was dfca5d9f23b1d42557c0ea1fc4a4bdc0cdad5075. A direct source comparison found the complete §7.3 sections byte-for-byte identical; both contain the recovery/bias MCSE formulas and interval/inconclusive rules. The v0.5 change added the per-J false-positive table in §7.2. DeepSeek's supplied response reports rendering truncation and does not identify the Git blob it reviewed. Therefore the exact review object cannot be cryptographically confirmed from the current record. It is incorrect to claim that the formulas were absent from the committed v0.5 source; it is also not possible to prove that the copy DeepSeek inspected was byte-identical to that object. v0.6 asks the next reviewer to state the exact blob SHA of the reviewed object.

**C. The 2,000-replication plan may yield an inconclusive result.** This cannot be predicted numerically without the replication-level standard deviations and the distance of the true recovery/bias means from their gate boundaries. v0.6 reports the MCSE and 95% half-width multipliers at 2,000 valid replications, then gives planning equations using pilot estimates of the standard deviations and prespecified boundary distances. It states that no finite count guarantees a decisive result when the true quantity is exactly on a boundary. A pilot requires separate authorization and cannot be pooled into the confirmatory run. No numerical replication count is invented.

**D. The positive inference must preserve the unresolved-outcome boundary.** v0.6 states that the S1 positive and matched-null worlds both have \(k_{\mathrm{unresolved}}=0\). A pass does not cover unresolved-outcome handling; S6 remains required and not specified.

### 12.3 Current disposition

S1 v0.6 is a design-only draft returned for direct DeepSeek review. DeepSeek's v0.5 freeze recommendation is conditional and does not freeze v0.6. The key pre-execution condition is owner commitment to use the S1 result to determine whether the current estimator/uncertainty combination proceeds as the candidate for S2-S7. That owner commitment is not evidenced in the repository record. No S1 run, pilot, implementation, freeze, solver construction, or execution GO is authorized by this round.


---

## 13. Round 8 — DeepSeek's supplied v0.5 review and direct repository provenance check, 2026-11-19

**Supplied review scope:** DeepSeek explicitly says it reviewed a 770-line v0.5 document and that it cannot review v0.6. Its substantive assessments are therefore recorded as assessments of v0.5 only. They are not treated as a review of the current v0.6 specification.

### 13.1 Direct repository check

The current GitHub branch and file were checked directly after receiving the review:

| Object | Directly returned repository evidence |
|---|---|
| Branch | `audit/analytical-validity-2026-11-18` |
| Branch head before this ledger update | `722fc315979023b3eee37b276b192e080378bccb` |
| Latest S1 file blob | `13e816a32b4a80f5705d167ff137bf88ffd1136e` |
| Latest S1 file declaration | Version 0.6; 841 lines |
| Parent of `722fc31` | `d945ac2b1551783160319cc87b9c55131944b4ad` |
| S1 blob at that parent | `f32f1c5cb6940fe9f2c13f5650086c510541ded9`; also Version 0.6, 836 lines |
| Reviewer ledger at the parent and branch head before this update | `b7d6220139209738bf9a2017f97d287796a9a701`; 337 lines; includes Round 7 |

The v0.6 scenario table and §7.3 precision/planning text were already present in the parent object `f32f1c5...`; they were not introduced only by the final `722fc31` handoff-question commit. At the current branch head, the v0.6 file includes the S2–S7 scenario table, the per-`J` false-positive precision table, the MCSE equations, the `0.02236 s_r` and `0.02236 s_b` multipliers, the approximate `0.04383 s` 95% half-width factors, the pilot-based replication-count equations, and the boundary/inconclusive rule. The current reviewer ledger contains a Round 7 section documenting the v0.5 review and v0.6 revisions.

Accordingly, the supplied DeepSeek statement that the named branch currently served a v0.5/770-line specification and a ledger without Round 7 does **not** match the repository objects returned for the branch head or its immediate parent. The cause is not established. The review may have used an earlier or cached rendering, a different ref, or another copy; this record does not infer which.

A Git blob SHA is repository metadata. It is not expected to appear inside the file's rendered Markdown, so searching the file body for its own blob SHA is not a valid way to establish its version. The exact blob is obtained from the repository object metadata.

### 13.2 Adjudication of the supplied review

| DeepSeek point | Scope of supplied assessment | Current v0.6 disposition |
|---|---|---|
| Stop rule | Correctly identifies the owner commitment as a necessary execution condition. | **Retained.** v0.6 makes the consequence explicit: if S2–S7 proceed unchanged or select an estimator independently, S1 must not be run. The owner commitment remains unrecorded. |
| S1 versus S2–S7 | The scenario-by-scenario table was not visible in DeepSeek's v0.5 copy. | **Resolved in v0.6.** The table names the distinct question for S2, S3a/S3b, S4, S5, S6 and S7. |
| MCSE and replication planning | DeepSeek accepts the arithmetic but could not verify the formulas in the rendered copy it inspected. | **Present in the current v0.6 object.** §7.3 contains the proportion, recovery and bias MCSE formulas; the 2,000-replication multipliers; the planning equations; the unavailability adjustment; and the zero-distance/no-finite-guarantee caveat. |
| Inconclusive handling | Correctly judged as non-pass. | **Retained.** The v0.6 rule does not convert overlap with a decision boundary into a pass. |
| Provenance | DeepSeek could not identify the exact blob it reviewed. | **Current object identified, reviewed object still unknown.** The current v0.6 blob is `13e816a32b4a80f5705d167ff137bf88ffd1136e`; DeepSeek did not provide a digest for the object it inspected. |
| Positive-inference boundary | Correctly limited to the binary-proxy, fixed-panel, independent-parent machinery check and the no-unresolved positive/null worlds. | **Retained and explicit in v0.6.** A pass does not validate unresolved-outcome handling, real solvers, general concentration, or B1 v1.6. |
| Overall recommendation | Conditional support for v0.5 as a narrow machinery check, not a freeze or execution GO. | **Not transferred to v0.6.** A fresh direct review of the exact v0.6 object is still required. No freeze or execution GO is inferred. |

### 13.3 Claude's answer-key critique

Claude's concern is recorded with a distinction that matters for accuracy:

- The diagnostic measurement is **not noise-free** relative to the latent state. Section 3.2 specifies (P(Q=1\mid H=1)=0.8) and (P(Q=1\mid H=0)=0.2).
- The mapping from the generated binary signal (Q) to the observed concentration (C_D) **is exact and one-to-one**: (C_D=0.75) iff (Q=1), and (C_D=0.50) iff (Q=0). S1 therefore does not test information loss or measurement error in the mapping from a general failure vector to its concentration summary.
- This limitation is already stated in the opening summary (§1), the diagnostic construction (§3.2), and the inference-transfer boundary (§9). The current draft does not claim a general or noisy continuous concentration measure has been validated.

**Adjudication:** Claude's substantive scope warning is accepted. Its suggestion that the point is stated only in the limitations section is not accurate for the current v0.6 text: the exact (Q\leftrightarrow C_D) encoding and the (H\to Q) measurement noise are stated in the opening section. No additional specification change is required for this point.

### 13.4 Current state and next review request

S1 v0.6 remains a **design-only draft**. The current owner commitment to use S1's pass/revise/stop result as the candidate-method gate for S2–S7 is not evidenced. No S1 freeze, pilot, implementation, simulation, model fitting, bank reuse, solver construction, or execution GO is authorized.

The next DeepSeek review must inspect the exact v0.6 source identified by blob `13e816a32b4a80f5705d167ff137bf88ffd1136e` and state the blob SHA or content digest of the actual reviewed object. A response based on v0.5 is not a review of v0.6.

---

## 14. Record-accuracy corrections carried forward (Claude round 3)

Three points from Claude's round-3 message are unaffected by the later S1 rounds and were still
unapplied in the published text at `d8ad246`. They are corrections of record, not of science, and they
change no verdict.

| # | Correction | Applied where |
|---|---|---|
| 1 | The 2026-11-01 NO-GO is a **third-reviewer concurrence with a route-scoped recommendation**, not an owner decision. `worklog.md:284` says "my 07:06 NO-GO was route-scoped"; no owner GO/NO-GO decision and no closure record exist. | `claude-keys-verification` §0 and §12 item 5; bundle `README` item 10 |
| 2 | **30 parents × 5 variants and 150 variants are not adopted.** v0.17 calls 30 "a logistics scenario only, not an adopted confirmatory operating count"; the exploratory protocol states "30 parents × 5 variants is not adopted". The word "roster" is withdrawn. | `claude-keys-verification` §3, the MDE table, and §11; bundle `README` challenges 3 and 8 |
| 3 | The execution gate is **`B1_ANALYSIS_PLAN_2026-11-14_v1.1.md:7`**, not a 2026-11-10 rule. The 2026-11-10 record is the capacity/power addendum, which says "not a GO, not a ratification of B1". Substance unchanged; the citation is corrected so it can be checked. | this section |

**Sequencing consequence of correction 3.** The authorization basis is "bounded GO (design and
mathematics only)". Design and mathematics are authorized now; execution is not. Writing and revising
S1 v0.6 required no new GO; running it requires one.

**Withdrawn in the same pass:** a parallel `S1_SPECIFICATION_DRAFT_2026-11-18.md` was written locally
before the v0.6 line was visible. It reached no remote ref and is superseded by
`S1_KNOWN_GAIN_SPEC_2026-11-18.md`, which states the same information target with an explicit identity
proof. It is not added to the repository; two competing specifications would be worse than one stale
one.

---

## 15. Measurement, novelty, and custody round (2026-11-19)

**Reviewed object:** branch head `28e789c`. Two reviewers plus an owner directive to implement the round
properly in the repository. Four specification documents were produced; this section records what was
verified, what was corrected, and what is new.

### 15.1 Verified against the record

| Claim | Verdict | Source |
|---|---|---|
| Eight strata are diagnostic input categories, not mechanisms | **Verified** | protocol 216, 226 |
| Bank has 64 diagnostic records, 8 per stratum | **Verified** | capacity addendum §1; erratum §1 |
| D6 holds 4 canonical inputs × 2 orderings, so the bank has 60 unique diagnostic canonicals | **Verified** | capacity addendum canonical row; erratum §1 |
| 80 held-out records / 78 unique held-out canonicals | **Verified** | erratum §1 |
| 30×5 / 150 is a logistics scenario, not adopted | **Verified** | v0.17 handoff; feasibility protocol 0.2/0.3 |
| v0.21 requires three qualifying parents in one exact cell | **Verified** | roadmap audit 164 |
| Per-stratum unresolved counts matter | **Verified, and already mandatory** | protocol 107–119 |

### 15.2 Corrected

| Review claim | Correction |
|---|---|
| "The held-out bank was exposed" presented as a finding | Already declared by the frozen plan: "development data, publicly exposed, never sealed" (B1 v1.7 §1, §12). The exposure is a design fact, not a discovery. |
| Claude: LOPO needs a fold-level estimability rule and coverage reporting | Nine of ten requested elements are already frozen in B1 v1.7 §3 and §5.7; one is stricter than requested; only a minimum-coverage verdict gate is missing. See `LOPO_ESTIMABILITY_RECONCILIATION_2026-11-19.md`. |
| Claude: "a sensitivity analysis should include unresolved as a separate class" | Legal only as an **outcome-model** three-category sensitivity. Recoding unresolved to 0/1 is prohibited by protocol 210–211 and by the N4-b channel construction. |
| Claude: "the held-out fold is only about five variants" | The fold scores the held-out parent's variants on all 78 records, so the test set is not five points — but 78 rows per variant are not 78 independent parents. The parent remains the only independent unit and B1 declares its conditional target. **Partly addressed**, not refuted; see §16.3. |
| GPT: CodeScore "ACM TOSEM, 2024" | TOSEM 34(3):1–22, Crossref year 2025, DOI 10.1145/3695991. |
| GPT: "RankEF (ASE 2024)" | Actual title: *Sifting through the Chaff: On Utilizing Execution Feedback for Ranking the Generated Code Candidates*, ASE 2024, pp. 229–241. "RankEF" is the system name. |
| GPT: Almaghairbe & Roper "2016 online / 2017 journal", with an AP figure of 0.79 | **Superseded — see §16.4.** Two papers, both real: ISSRE 2016 (`10.1109/issre.2016.22`) and *Software Quality Journal* 25(3):803–840 (`10.1007/s11219-016-9339-1`), online 2016, issue 2017. The small-cluster ≥60 % finding belongs to the SQJ paper. The 0.79 figure is unattributed and unverified. |
| GPT: AlphaCode "(2023)" | *Science* 2022, 378(6624):1092–1097, DOI 10.1126/science.abq1158. Claude's recollection was right. |
| Claude: bank "publicly downloadable by the entire internet" | Not established. The evidence supports CI artifact exposure with published digests; anonymous download and exploitation are both unproven. GPT's narrower wording is adopted. |

### 15.3 New, and load-bearing

1. **The statistic is named in the frozen protocol.** `C_D` is "the Berger–Parker dominance index"
   (protocol 218). It is a 1970 ecology index (verified DOI 10.1126/science.168.3937.1345). No claim of a
   novel measure survives this.
2. **A theorem constrains the whole programme — but only against `F`.** `C_D` is `F`-measurable, so
   `I(Y;C_D|X) ≤ I(Y;F|X)` and `I(Y;C_D|X,F) = 0`. **Superseded in part — see §16.2.** "C beats F" in
   population information is impossible; "C adds information beyond `X`" is testable and is the B1
   question. The earlier sentence "only compression efficiency, stability, and interpretability remain"
   was an overreach and is withdrawn.
3. **The partition and the bank share an origin.** The eight strata were used to construct the bank.
   "Prespecified" holds with respect to solver outcomes, and the bank's construction does not by itself
   invalidate prespecification. **Narrowed — see §16.3.**
4. **Custody requirement 2**: a replacement bank must be generated *after* the analysis is frozen, or the
   same shared-generation problem recurs. This is the requirement usually omitted.

### 15.4 Unverifiable from this repository

- The Elicit `api_access_denied` result. It is a reviewer-side plan limitation; nothing here depends on
  it, and no Elicit result may be cited.
- Full-text access for Chen & May 2016, both DiGiuseppe papers, and Almaghairbe & Roper 2016. Findings
  attributed to those four rest on abstracts and records.

### 15.5 What did not change

No frozen record, protocol, threshold, bank, plan, or population document was altered. No execution of
any kind. Gate 0 is now recorded as **OPEN** in the goal document; gates 1 and 3 remain unresolved or
undemonstrated; gate 4 remains failed-as-a-wiring-check. The 2026-11-01 reviewer concurrence and the
absence of a route-closure record are unchanged.

---

## 16. Adjudication and second correction pass (2026-11-19)

**Trigger:** GPT's review of `cc9b59e`, independently checking the commit, its changed files, and the B1
v1.7 plan. Three of its five substantive objections are correct and are adopted here. Two require
measured qualification. Nothing is defended beyond what the record supports.

### 16.1 Verdict on the objections

| Objection | Verdict | Action |
|---|---|---|
| Berger–Parker correction is right; the contribution must be the empirical application, not the index | **Accepted** | No change needed; already the register's position |
| The DPI is correct, but "accuracy cannot be the claim" does not follow | **Accepted — the error is ours** | §3 of the register rewritten; goal document §3 corrected; README challenge 9 corrected |
| The B1 target is a conditional LOPO target on the fixed 78-record development bank, not a "fixed held-out input bank" | **Accepted** | The proposition `P` is restated in those terms |
| The LOPO reconciliation is mostly right, but "not five observations" does not establish parent-level precision | **Accepted in substance** | §2 of the reconciliation rewritten; Claude's point marked *partly addressed* |
| The Almaghairbe correction is incomplete: two papers, one with a 2017 journal issue | **Accepted — the error is ours** | Register rows 7–8 split; correction table rewritten |
| Same-generation event does not by itself invalidate prespecification | **Accepted with narrowing** | §3 of the custody document rewritten around four decidable questions |
| "All three branches synchronized" is not supported by the remote branch list | **Qualification, see §16.6** | Claim clarified, not withdrawn |

### 16.2 The information-theory scoping error, corrected

The theorem is:

```
I(Y ; C_D | X)  ≤  I(Y ; F | X)      and      I(Y ; C_D | X, F)  =  0
```

Both correct. The invalid step was from those to "accuracy cannot be the claim". The comparison in the
theorem is `C_D` against **`F`**. The comparison in B1 is `C_D` against **`X`, the exact cell**. The
theorem says nothing about the second, and `I(Y;C_D|X) > 0` is entirely possible.

Corrected position, now carried in the register and the goal document:

| Claim | Status |
|---|---|
| `C_D` carries more **population** information than `F` | Impossible (theorem) |
| `C_D` adds information **beyond the exact cell `X`** | Testable; this is B1's estimand |
| A fitted `C_D` model improves held-out log loss over the exact-cell baseline | Testable |
| A fitted `C_D` model beats a fitted full-vector model **in finite samples** | Empirically testable; a lower-dimensional feature may win on estimation variance without being more informative in the population |

**Consequence for W1:** the `C/F ≈ 1/403` ratio is a result of one fitted simulation under one model class
and one partition. It is not forced by the DPI, and the DPI does not forbid `C` from beating `F` in a
finite sample. The DPI fixes the ordering of *population information*, not the outcome of a fitted
comparison.

**What survives unchanged:** the prohibition on testing `C_D` beyond `F`, and the prohibition on claiming
information superiority over `F`. Those are theorems, not findings.

### 16.3 The LOPO qualification, corrected

The earlier section argued that because each fold scores `variants × 78` rows, "precision per fold is much
better than five points". That is true of *a parent's measured score* and false as a response to the
review. Seventy-eight records per variant do not create seventy-eight parent implementations. The rows
share variant and parent structure; the statistic weights parents equally; and B1 §5.7 V1/V4 deliberately
refuse the parent-population target.

Correct adjudication:

- B1 already contains the fold-estimability procedure (`G ≥ 2`, `D ≥ 2`, `W > 0`), exclusion reasons,
  coverage tables, and equal weight per scored parent — **the review's request is largely already met**.
- The independent unit remains the parent, and the conditional scope is declared, not hidden — but the
  limit is **real and not removed** by row count.
- The review's point is therefore **partly addressed, not dismissed**.
- The one genuinely missing element is a pre-declared minimum-coverage gate with a `NOT ASSESSABLE`
  verdict.

### 16.4 The Almaghairbe conflation, corrected

Two papers exist, and both are verified against Crossref:

| Paper | Record | Content |
|---|---|---|
| *Automatically Classifying Test Results by Semi-Supervised Learning* | ISSRE 2016, pp. 116–126, `10.1109/issre.2016.22` | Semi-supervised classification of passing and failing executions from dynamic execution data |
| *Separating Passing and Failing Test Executions by Clustering Anomalies* | *Software Quality Journal* **25**(3):803–840, `10.1007/s11219-016-9339-1`; online 2016, issue 2017 | Clustering-based separation; small clusters sometimes composed of at least 60 % failures |

The previous entry collapsed these into one ISSRE paper and stated that "no 2017 journal issue exists".
The second half was true only of the ISSRE title; the SQJ paper has a 2017 issue. More importantly, the
**premise-relevant finding** — high failure share in small clusters — belongs to the SQJ paper. The
register now carries it as row 8, the closest prior result in the corpus, and records that it is
observational rather than predictive.

The `0.79` average-precision figure is now marked **unverified**: it was not located in either
Almaghairbe paper during this round, and no down-stream record may cite it until the paper containing it
is identified.

### 16.5 Same-origin restraint, corrected

The earlier claim was that the shared generation event makes the partition "not independent of the
evaluation material" and may inflate apparent reproducibility. That conclusion was too strong. A
stratified bank is normally built from prespecified categories; constructing a bank to realize a
partition is what stratification means.

What replaces it, in the custody document §3, are four decidable questions:

1. Were the stratum predicates fixed before solver outcomes existed? **Yes** — 0/150 solvers evaluated.
2. Were they tuned on outcomes? **No evidence**, and nothing to tune on.
3. Does construction create an accidental dependence between bank and result? **Open**; no evidence of use.
4. Is the claim limited to the generation scheme actually tested? **Must be**, and `P` now says so.

A bank generated after the analysis freeze under separate custody remains valuable for external
confirmation. The shared origin alone does not prove the existing partition invalid, and the record must
not say that it does.

### 16.6 Repository-state statement, clarified

The claim "all three branches in sync" meant **local versus `origin` equality for the three branches
under work**: `master` at `33dca9b`, `research/concentration-math-spec` at `de39291`, and
`audit/analytical-validity-2026-11-18` at `cc9b59e`. It did not mean, and was never a claim about, every
remote branch sharing a head. `foued2-patch-1`, `foued2-patch-2`, and `foued2-patch-3` are separate lines
at `e22da84`, `ef69089`, and `2d5f9c3`, and are expected to differ.

The working-tree cleanliness claim is local-only by nature; it was taken from `git status --porcelain` on
the local clone (0 modified or staged tracked files, 29 untracked exclusions) and cannot be verified
through the remote.

B1 v1.7 is not in the audit commit's tree. It lives on `gpt/lc518-m1si-audit-2026-11-17` at blob
`8c666e501a31726c728447d155045c0b20adc178`, which matches the acceptance record GPT checked. The
reconciliation cites a real source on a separate branch, and that separation is stated rather than
implied.

### 16.7 The proposition, after correction

The claim the programme can actually make:

> Within the observed parent set, does diagnostic failure dominance improve leave-one-parent-out
> predictive log loss on the fixed 78-record development bank, beyond the exact-cell baseline, with the
> parent as the independent unit?

Narrower than external generalisation to a new parent population — which B1 explicitly refuses — and not
vacuous, because it compares against `X`, not against `F`.

### 16.8 Disposition

- No solver construction, no experiment, no numerical evaluation. The pause is unaffected.
- Nothing frozen was altered: protocol Rev 11, B1 v1.7, the bank, the thresholds, and the population
  documents are untouched.
- The revised register is ready for Claude and GLM review on GPT's terms: information-theory
  interpretation, precise B1 target, and Almaghairbe references are all corrected.
- One item remains unresolved that the review round did not settle: whether a one-parameter gain against
  the exact-cell baseline is a scientific contribution or a well-specified ablation. It is recorded as
  open, not argued away.

---

## 17. Dominance specificity round (2026-11-19, second pass)

**Reviewed object:** branch head `d7131d2`. GPT reviewed Claude's review of that commit and issued an
adjudication that accepts one point with correction, one as mostly covered, and one as already
incorporated. `B1_ANALYSIS_PLAN_2026-11-14_v1.7.md` on `gpt/lc518-m1si-audit-2026-11-17` was re-read at
blob `8c666e50` for the clauses cited below.

### 17.1 The central correction is right, and it is provable

GPT rejects the proposed random relabelling of the eight stratum names on the ground that it leaves `C_D`
unchanged. It does, for every permutation:

```
C_D' = max_j f_{π(j)} / Σ_j f_{π(j)} = max_j f_j / Σ_j f_j = C_D
```

The stronger form: `C_D` depends on `f` only through the multiset `{f_1,…,f_8}`, so it is invariant under
the whole symmetric group on labels. This is the content of the word "dominance", not a detail.

Two consequences go beyond the review:

1. **The operation is inert *and* ill-formed under the canonical basis.** The exposure vector is
   `R = (8,8,8,8,8,4,8,8)`. Permuting names without permuting `R` can produce `f_j > R_j`. Permuting `R`
   with the labels restores consistency and changes nothing. So the proposal is either empty or
   inadmissible.
2. **The residue is interpretive, not experimental.** `C_D` cannot attribute a gain to *which* stratum
   dominated. Any claim of the form "failures concentrate in category X and that predicts correctness" is
   outside what the statistic carries. This is now recorded as an interpretation rule.

### 17.2 Input reallocation is a real question and is blocked by more than scope

GPT correctly substitutes reallocation of diagnostic inputs, which changes `C_D`, and correctly labels it
partition specificity rather than dominance specificity. The forensic work adds two findings:

**The exact cell survives reallocation exactly.** Reallocation permutes which record feeds which `f_j`; no
outcome changes. Therefore `k_fail`, `k_unresolved`, and the cell `(q, Z, k_fail, k_unresolved)` are
identical across draws, so the **baseline model is unchanged** and only the supplied feature varies. That
is the strongest argument for the sensitivity ever being run.

**But it is incompatible with §5.3, not merely outside it.** B1 v1.7 §5.2 defines the resampling unit as
the within-cell `C_D` label with the **multiset held fixed**. Three frozen guarantees depend on that:

| Guarantee | Clause | Why reallocation breaks it |
|---|---|---|
| Audit equality, including "a previously excluded cell that becomes estimable makes the assignment inadmissible" | §5.3 step 1 | `W_{C,c} = Σ(C_D − C̄_D)²` changes with the multiset, so estimability becomes draw-dependent |
| Permutation-invariant target population | §5.3 step 3 | Scored cells can differ across draws |
| Super-uniformity conditional on the availability event | §5.7 V3, V5 | The conditioning event is defined over assignments sharing a multiset |

So GPT's instruction not to modify B1 v1.7 is supported by a stronger reason than "different question":
the sensitivity would break the identity between observed statistic and null reference that makes the
current test valid. A fork must be resolved before any draw — admissibility by design-only condition
(preserves the target population, conditions on a `C_D`-configuration event) or per-draw audit (faithful
per draw, but coverage can drive the difference). Neither is decided, and no draw is authorized.

**Arithmetic constraint recorded:** a canonical-basis random partition cannot use equal groups. With 60
unique diagnostic canonicals, the only equal-exposure option is `4 × 7 + 4 × 8`. The record basis
(`8 × 8`) is the comparable choice for the frozen statistic.

### 17.3 The alternative-summary competition is real but weakly identified

**Superseded — see §18.2.** The analysis below used the wrong identifying variation (equal `C_D`, differing
alternatives) for the Level 2 question (equal alternative, differing `C_D`). The shape-count table is
correct; the conclusion drawn from it is not, and the low-`k` claim is withdrawn.

GPT is right that the exact cell leaves the *shape* of `f` free, and that second-largest share, Shannon
entropy, and a Herfindahl/Simpson index are meaningful competitors. All are `F`-measurable, so all sit
under the same ceiling as `C_D`.

New quantitative limit: at fixed `k`, the number of distinct shapes is the partition number of `k` into at
most eight parts, and the number of distinct `C_D` values is at most `k`:

| `k` | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|
| Shapes | 3 | 5 | 7 | 11 | 15 | 22 |
| Distinct `C_D` (≤) | 3 | 4 | 5 | 6 | 7 | 8 |

Because the cell fixes `k`, the comparison is identified only where shapes collide on one `C_D` value. At
`k = 5`, the shapes `3+2` and `3+1+1` both give `C_D = 3/5` but differ on the second share (`2/5` vs
`1/5`) and on Herfindahl (`0.520` vs `0.440`). Those collisions are the whole identifying variation, which
means the comparison is nearly empty at `k ≤ 4` and concentrates in large-`k` cells. No power calculation
exists and none can be produced without `σ_u` and `sd(C)`.

### 17.4 Parent consistency

Adopted as stated: `δ_g = L_{0,g} − L_{1,g}` is already mandatory (§2, §11(a)), equal weight per scored
parent is mandatory (§3 item 4a), coverage tables are mandatory (§3 item 4c), and no parent-majority
decision rule is added. Descriptive influence reporting is recorded as useful but must be declared before
evaluation so it cannot become a post-hoc rescue. The minimum-coverage verdict gate remains missing, and
still has no defensible threshold; none is invented.

### 17.5 Four-level claim ladder, now recorded

| Level | Claim | Support | Status |
|---|---|---|---|
| 1 | `C_D` improves held-out prediction over the exact-cell baseline | B1 primary comparison | Frozen, not executed |
| 2 | The gain is specific to the maximum share rather than another shape summary | Predeclared comparison against the §17.3 set, with collisions identified in advance | Not specified; weakly identified |
| 3 | The gain depends on the prespecified partition | Reallocation sensitivity with the §17.2 fork resolved | Not specified; incompatible with §5.3 as written |
| 4 | The gain generalises to new parents | Post-freeze bank, separate custody, parent-population procedure | Refused by §5.7 V4 |

A positive level-1 result licenses the sentence "the maximum-share statistic predicts" — not "dominance is
what matters", and not "the partition is validated". That rule needs no experiment and is available now.

### 17.6 What changed in the repository

- New: `DOMINANCE_SPECIFICITY_AND_PARTITION_SENSITIVITY_2026-11-19.md` (§§1–7 above in full).
- Novelty register §5 now points to that document for the narrower version of Threat B.
- **B1 v1.7 untouched.** No clause, threshold, fold, or estimability condition modified.
- No extension authorized, no threshold invented, no execution of any kind.
- Open for Claude and GLM: the §17.2 fork, the eight-item requirement checklist, and whether the §17.3
  collision analysis leaves enough identifying variation for level 2 to be worth specifying at all.

---

## 18. Level 2 direction error and the reallocation qualification (2026-11-19, third pass)

**Reviewed object:** branch head `03f950a`. GPT accepted the name-permutation proof, qualified the
reallocation conclusion, corrected the canonical-basis wording, and rejected the Level 2 identification
argument. The Level 2 objection is correct and the error was mine.

### 18.1 The error, stated exactly

Level 2 asks whether `C_D` adds information **beyond** a competing summary `S`. The identifying variation
for that question is:

```
same S, different C_D
```

The previous section used:

```
same C_D, different S
```

That identifies information in the **alternatives beyond `C_D`**, which is the opposite question and is not
what Level 2 claims. The `k = 5` example (`3+2` vs `3+1+1`, both `C_D = 3/5`) demonstrated that the
alternatives separate shapes `C_D` collapses. The "low-`k` support is nearly empty" conclusion then
followed from a collision count in the wrong direction, and it is wrong.

GPT's counter-examples check out exactly:

```
k = 3   2+1     C_D = 2/3   p_(2) = 1/3
        1+1+1   C_D = 1/3   p_(2) = 1/3

k = 4   3+1     C_D = 3/4   p_(2) = 1/4
        2+1+1   C_D = 1/2   p_(2) = 1/4
        1+1+1+1 C_D = 1/4   p_(2) = 1/4
```

Support for the `p_(2)` comparison therefore begins at `k = 3`, not at large `k`.

### 18.2 Rebuilt support table

**Superseded — see §19.1.** The enumeration below applies the "at most eight parts" constraint but not the
per-stratum capacity `f_j ≤ 8`, so its shape counts are unrestricted partition numbers for `k > 8` and its
distinct-`C_D` column is arithmetically impossible. The direction argument and the `k = 3`/`k = 4`
examples stand; the table does not.

Shapes enumerated exactly as integer partitions into at most eight parts; `C_D`, `p_(2)`, and Herfindahl
computed in exact rational arithmetic; Shannon grouped with a numerical tolerance and approximate.

| `k` | Shapes | Distinct `C_D` | `p_(2)`: classes / with ≥2 `C_D` | Herfindahl: classes / with ≥2 `C_D` | Shannon: classes / with ≥2 `C_D` |
|---|---|---|---|---|---|
| 3 | 3 | 3 | 2 / 1 | 3 / 0 | 3 / 0 |
| 4 | 5 | 4 | 3 / 1 | 5 / 0 | 5 / 0 |
| 5 | 7 | 5 | 3 / 2 | 7 / 0 | 7 / 0 |
| 6 | 11 | 6 | 4 / 2 | 9 / 2 | 11 / 0 |
| 7 | 15 | 7 | 4 / 3 | 13 / 2 | 15 / 0 |
| 8 | 22 | 8 | 5 / 3 | 18 / 4 | 21 / 1 |
| 9 | 30 | 9 | 5 / 4 | 21 / 8 | 29 / 1 |
| 10 | 42 | 10 | 6 / 4 | 27 / 12 | 39 / 3 |
| 11 | 56 | 11 | 6 / 5 | 34 / 15 | 52 / 4 |
| 12 | 77 | 12 | 7 / 5 | 39 / 22 | 68 / 8 |

Three findings, none of which was available before the rebuild:

1. **Support is competitor-specific and runs in opposite directions.** `p_(2)` is a weak summary — it
   leaves the maximum free on `[p_(2), 1]` — so it leaves the most `C_D` variation. Shannon entropy is a
   rich functional that nearly separates shapes, so conditioning on it leaves almost none (3 of 39 classes
   at `k = 10`). Herfindahl sits between. **The predeclared comparator set therefore sets the difficulty of
   Level 2 by construction**, which makes it a substantive choice rather than a formality.
2. **No summary is injective on shape.** At `k = 8`, `4+1+1+1+1` and `2+2+2+2` both have Shannon entropy
   `ln 4` while `C_D` is `1/2` and `1/4`. GPT's caution about entropy is confirmed by enumeration.
3. **Combinatorial support is not realised support.** The table counts shapes that could occur at each `k`.
   It says nothing about the `k` distribution across the 150 solvers, which is unknown because 0/150 have
   been evaluated. No power calculation is possible without `σ_u` and `sd(C)`.

### 18.3 Canonical-basis wording corrected

The previous claim that name permutation is "ill-formed" under `R = (8,8,8,8,8,4,8,8)` was too strong. The
correct statement: admissibility is a **condition**, not a veto. Permutations among the seven
eight-capacity positions, leaving D6 in place, are admissible; the identity is always admissible; the
constraint bites only when a count above four is moved into the D6 position. **Every admissible relabelling
is still inert with respect to `C_D`**, so invariance carries the result and the capacity argument does not.

### 18.4 Reallocation: "outside the frozen law", not "impossible"

The previous text said reallocation "breaks" the fixed-target and super-uniformity guarantees. That
overstates it. Corrected position, now in the design record:

> Reallocation is incompatible with B1's frozen resampling law and null hypothesis. A separate conditional
> partition-randomization procedure might preserve analogous guarantees, but those would have to be
> established for the new assignment space.

The route is Option A of the record — restricting the admissible space to draws that reproduce the observed
audit-selection key — which *could* hold the scored population fixed while conditioning on a different
assignment space. None of B1's guarantees transfers automatically: different assignment law, different null,
different conditioning event, and super-uniformity would need re-establishing. Not valid under this
procedure; not shown to be impossible. Both halves are load-bearing.

### 18.5 Level 1 sentence tightened

Adopted verbatim as the only licensed report form:

> Within the observed parent set and on the fixed 78-record development bank, the maximum-share statistic
> improves leave-one-parent-out predictive log loss relative to the exact-cell baseline, under the
> prespecified conditional test.

Not "the statistic predicts correctness", and not any inference to a dominance mechanism, partition
validity, or new parents.

### 18.6 Disposition

- **B1 v1.7 untouched.** No clause, threshold, fold, or condition modified.
- **Level 2 reopened**, not settled: the direction error is corrected, and the rebuilt table replaces the
  withdrawn conclusion. Whether any comparator set leaves enough equal-`S` support is now an open design
  question with a computable input, not a claim.
- **Level 3 reclassified** from "incompatible" to "outside B1's frozen law; a separate procedure may be
  designable but inherits nothing".
- **No threshold invented**, no draw taken, no execution of any kind.
- **Record integrity:** §17.3 is marked superseded in place rather than deleted, so the error and its
  correction remain visible in the ledger.

---

## 19. Capacity constraint, support measures, and exact entropy (2026-11-19, fourth pass)

**Reviewed object:** branch head `405fa9f`. GPT accepted the direction correction and found a remaining
arithmetic error in the enumeration, plus two definitional problems. All three are correct.

### 19.1 The capacity error

The rebuilt table claimed to enumerate "partitions into at most eight parts". That is one of **two**
constraints. The record-level exposure is `R = (8,8,8,8,8,8,8,8)`, so a feasible failure vector requires

```
at most 8 parts      (one per stratum)
each part ≤ 8         (records available per stratum)
```

The at-most-eight-parts constraint was applied; the capacity constraint was not. The result was that the
shape counts coincided with unrestricted partition numbers for `k > 8` — 30, 42, 56, 77 at `k = 9..12` —
and the distinct-`C_D` column reported `12` values at `k = 12`, which cannot exist. Since `max_j f_j` ranges
only over `{⌈k/8⌉, …, 8}`, the number of distinct `C_D` values saturates at `9 − ⌈k/8⌉`: seven for
`9 ≤ k ≤ 16`.

Both constraints are now applied. The corrected counts reproduce GPT's independent recomputation exactly:
`28, 38, 48, 63` at `k = 9..12`, with `7` distinct `C_D` values from `k = 9` onward.

### 19.2 An ambiguous ranking, replaced by two defined measures

The previous text said `p_(2)` "leaves the most `C_D` variation" and that Herfindahl "sits between" it and
Shannon. That ordering is not well defined, and the table's own counts contradict it depending on which
quantity is read. Two measures are now defined and reported separately:

| Measure | Definition | What it counts |
|---|---|---|
| `V` | Equality classes containing ≥2 distinct `C_D` values | **Where** the contrast can occur |
| `M` | Maximum number of distinct `C_D` values inside one class | **How much** `C_D` varies once `S` is fixed |

They order the competitors **oppositely**:

| `k` | `p_(2)`: `V` / `M` | Herfindahl: `V` / `M` | Shannon: `V` / `M` |
|---|---|---|---|
| 9 | 4 / **7** | **8** / 2 | 1 / 2 |
| 10 | 4 / **7** | **12** / 2 | 3 / 2 |
| 11 | 5 / **7** | **14** / 3 | 4 / 2 |
| 12 | 5 / **7** | **20** / 3 | 7 / 2 |

By `V`, Herfindahl is far ahead from `k = 9`. By `M`, `p_(2)` dominates throughout, because it leaves the
maximum free on `[p_(2), 1]` while Herfindahl pins the shape much more tightly. Shannon is last on both.

**Therefore no competitor is described as "most informative" or "most permissive".** The earlier ranking is
withdrawn, and the replacement states only that the ordering depends on the measure, that the comparator
set is a substantive choice, and that `V` and `M` are both inputs to any future power argument.

### 19.3 Shannon entropy is now grouped exactly

The approximate grouping is replaced by an integer identity valid for integer counts summing to `k`:

```
H(f) = ln k − (1/k) · ln ∏_j f_j^{f_j}
```

so two shapes have equal entropy **iff** their integer products `∏_j f_j^{f_j}` are equal. Comparison is on
Python big integers; no tolerance is involved. The resulting Shannon column reproduces GPT's exact-grouping
values without adjustment (27/1, 35/3, 44/4, 55/7 at `k = 9..12`), which is an independent check that both
implementations are grouping the same objects.

The `k = 8` coincidence remains the clearest demonstration that no summary is injective on shape:

```
4+1+1+1+1   C_D = 1/2   Shannon = ln 4   product 4^4 · 1^4
2+2+2+2     C_D = 1/4   Shannon = ln 4   product 2^8
```

### 19.4 Canonical basis is asymmetric and is deferred

**Superseded — see §20.** Deferral was unnecessary for the unweighted shape-support table. The canonical
feasibility constraint is slack throughout the displayed range, so the table is already valid for both
bases there; only labelled allocation counts and assignment probabilities require separate treatment.

Under `R = (8,8,8,8,8,4,8,8)` the multiset abstraction fails, because a part above four is feasible in
seven positions but not in the D6 position. Feasibility becomes `max f_j ≤ 8` **and**
`#{j : f_j > 4} ≤ 7`, and the tabulation must be over ordered vectors with a distinguished position rather
than partitions. Only the record basis is tabulated. The canonical variant is a labelled secondary that
would require its own enumeration; substituting it into the same table would be wrong.

### 19.5 Level 1 gains a precondition

GPT's safeguard is adopted. The licensed Level 1 sentence may be used only when **both** hold:

1. the observed `ΔLL` is positive, and
2. the rejection is in the **upper tail**, with `p_R` driving the two-sided decision.

B1 v1.7 §5.6 and §11(d) require the driving tail to be reported precisely because a lower-tail rejection
does not establish positive incremental prediction. A significant two-sided result driven by the lower tail
is a negative or adverse finding and must never be reported as support for level 1.

### 19.6 Two wording boundaries adopted

- Level 2 can establish superiority to a **predeclared set** of competing summaries. It cannot establish
  superiority to every conceivable summary, and a result against three named competitors must not be
  presented as though it exhausted the space.
- The 150 is referred to as the **proposed 150-variant scenario**. It is not an accepted sample size, the
  programme is unapproved, and "0/150 evaluated" is written as "0 evaluated".

### 19.7 Disposition

- **B1 v1.7 untouched.** No clause, threshold, fold, or condition modified.
- **Level 2 remains reopened**, now with a correct capacity-constrained table and two defined support
  measures instead of a ranking.
- **No draw, no fitting, no execution.**
- **Record integrity:** §18.2 is marked superseded in place, so the capacity error and its correction stay
  visible alongside the direction error of §17.3.

---

## 20. Canonical-basis shape support, and two wording bounds (2026-11-19, fifth pass)

**Reviewed object:** branch head `6663083`. GPT accepted the capacity-constrained enumeration, the exact
entropy grouping, the `V`/`M` definitions, and the Level 1 tail condition, after an independent
recomputation that matched through `k = 13`. One overstatement remained.

### 20.1 The overstatement, and the correct result

The previous text said canonical-basis enumeration requires ordered vectors with a distinguished position
and could therefore be deferred. That is true for **labelled allocation counts**. It is not true for the
**unweighted shape-support table**, which is what the document tabulates.

For `R = (8,8,8,8,8,4,8,8)` a multiset is feasible exactly when `max_j f_j ≤ 8` and `#{j : f_j > 4} ≤ 7`:
necessary because D6 holds four canonical inputs, sufficient because the larger parts can be placed in the
other seven positions.

That constraint is slack far beyond the displayed range. Each part above four is at least five, so the
number of them is at most `⌊k/5⌋`, which is `≤ 7` for every `k ≤ 39`. Recomputing both bases confirms the
counts are identical for all `k ≤ 39` and first diverge at `k = 40`, where exactly one shape —
`(5,5,5,5,5,5,5,5)` — becomes infeasible: all eight parts exceed four, and only seven positions can hold
them.

GPT's `k ≤ 13` statement is therefore correct and can be strengthened: **the displayed table is the
canonical-basis shape-support table for every `k` shown, and would remain so up to `k = 39`.** Nothing in
the table needs revision.

### 20.2 Three objects, now separated

| Object | Depends on | Status |
|---|---|---|
| Feasible **shape** support | Multisets plus both capacity constraints | Tabulated; identical across bases for `k ≤ 39` |
| Labelled **allocation** counts | Ordered vectors with the D6 position distinguished | Not tabulated; needed only for multiplicity counts |
| **Assignment probabilities** | A separately declared sampling law | Not defined anywhere in the record |

The measurement bases remain different — `N = 64` versus `N = 60`, and `R` differs at D6 — so realised
failure vectors and statistics will differ for actual solvers. That is a statement about realisation, not
about support.

### 20.3 Two wording bounds adopted

- Replaced "no summary is a one-to-one encoding of shape" with: **none of the three named competing
  summaries is injective over the complete feasible shape space.** The examples establish non-injectivity
  of the named summaries, not of every conceivable summary.
- `V` and `M` are now explicitly labelled **unweighted combinatorial support descriptors**. Every equality
  class counts once regardless of how many shapes realise it, so a class realised by one possible shape and
  a class realised by twenty contribute equally to `V`. That matters when moving from combinatorial support
  to realised sample support.

### 20.4 Disposition

- **B1 v1.7 untouched.** Blob `8c666e50` confirmed unchanged.
- **Level 2 remains open.** Its direction is correct and its combinatorial support is now characterised
  correctly for both bases, but no empirical superiority has been established and none can be without
  realised solvers.
- **The standing distinction is now sharp:** what the statistic *could* distinguish before observing
  solvers is established combinatorially; what it *actually* distinguishes, and whether that distinction
  improves prediction, requires realised evidence that does not exist.
- **Record integrity:** §19.4 is marked superseded in place, alongside §17.3 and §18.2, so all three
  corrections remain visible with the claims they replaced.
- No draw, no fitting, no execution. Project pause unchanged.

---

## 21. Acceptance round — canonical-basis support closed (2026-11-20, sixth pass)

**Reviewed object:** branch head `443b7a9`. GPT accepted the fifth-pass correction after its own
independent verification and reported no remaining substantive objection. The same message carried a copy
of the separate LC518-150 analysis specification, dispositioned in §21.4. Acceptance here means acceptance
of a mathematical correction; it is not evidence for any scientific claim.

### 21.1 Independent recomputation performed here

The central counts were not merely accepted; they were recomputed from the stated constraints by exact
enumeration of non-increasing integer partitions with at most eight parts, each part at most eight, and —
for the canonical basis — at most seven parts above four.

| Claim | Recomputed result |
|---|---|
| Record-level feasible shapes at `k = 40` | `383` |
| Canonical-level feasible shapes at `k = 40` | `382` |
| Identical counts for every `k ≤ 39` | Confirmed; `409` at `k = 39` for both bases |
| First divergence | `k = 40` |
| Sole excluded shape | `(5,5,5,5,5,5,5,5)` |

The predicate applied was `max_j f_j ≤ 8` and `#{j : f_j > 4} ≤ 7`, as stated in §20.1. The recomputation
confirms GPT's independent enumeration rather than deferring to it.

### 21.2 Repository verification

| Reference | Verified head |
|---|---|
| Audit branch, local and `origin` | `443b7a9` (equal) |
| `master` | `33dca9b` (unchanged) |
| `research/concentration-math-spec` | `de39291` (unchanged) |
| B1 v1.7 blob | `8c666e50` (unchanged) |

`443b7a9` changes exactly two files, both in this review directory. It does not touch B1 v1.7, which lives
on `gpt/lc518-m1si-audit-2026-11-17` at
`lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/B1_ANALYSIS_PLAN_2026-11-14_v1.7.md`.

### 21.3 Working-tree statement

`git diff` and `git diff --cached` both return empty: zero modified, staged, or deleted tracked files.
`git status --porcelain` lists 29 untracked entries, the same count recorded in §16.6; they are the
declared exclusions (raw result trees, `_quarantine/`, and `.qoder*` scratch and attachment files). The
tracked tree is therefore clean in the only sense the claim ever used. GPT is correct that the remote
cannot establish this; it is recorded here with the command-level basis, not as a remote fact.

### 21.4 The attached analysis specification

`.qoder_analysisspec.md` has SHA-256 `FB24910CC7712C7E9E27753084AD3683D1FD422A20D875B0B5A4CA33A55F4E78`
and Git blob `d20d3af6f40484453fe19adf5a785d58040c33a0`. That blob is byte-identical to
`lc518-150/glm-handoff/ANALYSIS_SPEC.md` at `3e9a29c`. It is already committed; this round adds no new
document.

It belongs to the separate LC518-150 construction study. Its `1.0 (FROZEN)` header freezes a
preregistered plan; it is not a construction or execution authorization. Its own §1 forbids fitting,
prediction, and dynamic evaluation in the construction phase, §9 lists the execution protocol and the
blind predictive analyst as pending external inputs, and §10 is a freeze record. A frozen analysis plan
therefore does not make the proposed 150-variant scenario approved or executed, and nothing in the
document modifies B1 v1.7 or this audit round.

### 21.5 Disposition

- **Accepted.** No remaining mathematical defect was identified in the canonical-basis support claim.
- **Combinatorial Level 2 is closed for both measurement bases** over the displayed range and, for shape
  support, through `k = 39`. The table needs no further revision.
- **No further combinatorial expansion** unless Claude or GLM identifies a concrete defect. Additional
  shape tables would not advance the scientific question.
- **The scientific question remains open:** whether maximum-share concentration contributes predictive
  information beyond a predeclared set of alternative summaries on realised solver data. No realised
  solver evidence, no Level 2 power calculation, and no empirical superiority exist.
- **B1 v1.7 remains frozen.** The proposed 150-variant scenario remains unapproved. The project pause
  remains in force: no solver construction, fitting, draws, or execution.
- **Record integrity:** the direction error (§17.3), the capacity error (§18.2), and the canonical-basis
  deferral (§19.4) remain visible in place with their corrections.

---

## 22. Documentary closing round — accepted, with two repository corrections (2026-11-20, seventh pass)

**Reviewed object:** branch head `950fb93` and GLM's documentary closing review of 2026-11-20, as
adjudicated by GPT. GPT closes the analytical review cycle and accepts the narrow §5.3 text verification,
but finds the proposed roadmap addendum not ready: the branch-count reconciliation and the B1 tree
inventory do not hold. Both objections are correct; the verified corrections follow. The attached
`.qoder_analysisspec.md` is unchanged and is dispositioned once in §21.4, not re-recorded here.

### 22.1 Disposition adopted

| Area | Status |
|---|---|
| Combinatorial support audit | Closed |
| Branch ancestry dispute | Closed |
| B1 v1.7 identity and §5.2 | Closed |
| Independent §5.3 text verification | Closed |
| Roadmap addendum | Not yet published |
| Branch-count and B1 tree-inventory reconciliation | **Correction required** |
| Empirical superiority over competing summaries | Untested |

### 22.2 B1 inventory — the word "only" is withdrawn

GLM's §1 row 2 says B1 v1.7 is present in the tip tree of `gpt/b1-computational-plan-2026-11-14` **only**,
while also recording `gpt/lc518-m1si-audit-2026-11-17` at `7365ad5`. Those two statements are
inconsistent, and the second branch does contain the file. Verified this round:

| Branch | Tip | `.../B1_ANALYSIS_PLAN_2026-11-14_v1.7.md` |
|---|---|---|
| `gpt/b1-computational-plan-2026-11-14` | `46d548f` | Present, blob `8c666e50` |
| `gpt/lc518-m1si-audit-2026-11-17` | `7365ad5` | Present, blob `8c666e50` |
| `master` | `33dca9b` | Absent |
| `docs/scientific-roadmap-audit-2026-11-18` | `874915b` | Absent |
| `audit/analytical-validity-2026-11-18` | `950fb93` | Absent |
| `research/concentration-math-spec` | `de39291` | Absent |

The path is identical on both GPT branches:
`lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/B1_ANALYSIS_PLAN_2026-11-14_v1.7.md`.
The blob is identical: `8c666e501a31726c728447d155045c0b20adc178`, content SHA-256
`797bd9f72cf94fdc0eff4a03b1544823d4042f8e530b27f4fb70cbd7f2baca7c`, 111,169 bytes, 331 LF-terminated
lines, final newline present. Across all refs the blob is reachable at exactly this one path, so there is
no same-content/different-path copy. The correct inventory is therefore **same path and same blob on the
two GPT branches; absent from the other four**. The identity and acceptance of B1 v1.7 are unchanged; only
the word "only" was wrong.

### 22.3 Branch count — 63 verified, reference set not archived

`git ls-remote --heads origin` returns **63** heads. The roadmap audit records **60** at its
2026-11-18T08:55:36+01:00 commit, but neither that document nor any other archived file preserves the
60-name enumeration. A true added/deleted/renamed comparison is therefore **not reconstructable from the
primary record**. Any explanation that asserts "two new branches" against a net increase of three is
unsupported; GPT's objection is correct.

What can be verified is which heads carry tip commits after the snapshot:

| Head | Tip | Tip time |
|---|---|---|
| `foued2-patch-3` | `2d5f9c3` | 2026-11-18T12:24:32+01:00 |
| `audit/c09-count-reconciliation-2026-11-18` | `204500e` | 2026-11-18T12:31:26+01:00 |
| `audit/analytical-validity-2026-11-18` | `950fb93` | 2026-11-20T07:19:13+01:00 |
| `research/concentration-math-spec` | `de39291` | 2026-11-18T14:30:05+01:00 (updated head, not a new head) |
| `docs/scientific-roadmap-audit-2026-11-18` | `874915b` | 2026-11-18T08:55:36+01:00 (at the snapshot) |

`60 + 3 = 63` is arithmetically consistent with three additions, but which three cannot be fixed without
the baseline list: the roadmap branch's own inclusion in the 60 is exactly what the missing enumeration
would settle. Two readings survive — (a) roadmap counted, additions are `foued2-patch-3`,
`audit/c09-count-reconciliation-2026-11-18`, and `audit/analytical-validity-2026-11-18`; (b) roadmap not
counted, and three of the post-snapshot heads are the additions. No deletion or rename is detectable from
the current ref set, but absence of a deletion cannot be proven without the same list.

**Requirement for the addendum:** archive GLM's actual `ls-remote` output (if it survives in
`audit_scratch/doc_review_20261120/`) or state that the 60-name baseline is unavailable and mark
added/deleted/renamed entries `UNVERIFIED`. It must not explain a three-head increase by two branches.

### 22.4 Provenance distinction kept strict

Git author and committer identity is self-reported configuration; it does not establish who wrote the
document. Document authorship, Git identity, and owner acceptance remain three separate facts. The counts
themselves check out:

| Branch | Commits ahead of `master` | Authors recorded |
|---|---:|---|
| `audit/analytical-validity-2026-11-18` | 156 | foued2 64, DeepSeek 48, GLM 38, MUSE 4, Codex 2 (`codex@local` 1, `codex@localhost` 1) |
| `gpt/b1-computational-plan-2026-11-14` | 124 | foued2 121, `GLM <glm@review-chain.local>` 3 |

GLM's 21/21 battery is retained as **GLM-reported verification**, not as a result independently
reproduced here. The scripts and raw outputs named in GLM's report are not in this repository, and the
report does not carry the individual check results or hashes of those files. A reproducible archive needs
both. This round's own checks were targeted and independent (§22.2–§22.3), not a rerun of that battery.

### 22.5 What the §5.3 verification closes, and what it does not

The textual gap is closed: the pinned B1 v1.7 text does contain the excluded-cell inadmissibility rule,
the selection-key-only admissibility condition, and the permutation-invariant target population. That is
a statement about the frozen text, not about the statistical validity of the test. The test remains
conditional on its exchangeability assumption and the declared design-support conditions; its null is
stronger than \(\beta_C = 0\); and a rejection alone cannot establish that concentration is the unique
source of predictive information rather than parent quality or unresolved-placement association. This is
an interpretation boundary, not a new defect, and it must accompany any eventual result.

### 22.6 Disposition

- **Analytical review cycle closed** on GPT's terms. The combinatorial audit is not reopened.
- **Roadmap addendum remains unpublished and is not ready.** It is blocked on the missing reference set
  and on the B1 inventory correction in §22.2.
- **B1 v1.7 untouched.** No clause, threshold, fold, or condition modified; no draw, fitting, or
  execution.
- **GLM's report authorizes no repository change, solver construction, or experiment.** This ledger
  records the adjudication only. The project pause remains in force.
- **The scientific position is unchanged:** no solver outcomes, no demonstrated predictive gain, and no
  evidence that `C_D` outperforms the predeclared competing summaries.

---

## 23. Roadmap addendum published; review cycle stopped (2026-11-20)

**Trigger:** GPT's closing adjudication of `15cabef`. It accepted both §22 corrections, added one
precision, and recommended publishing the dated addendum by preserving the known facts and the
uncertainty rather than reconstructing the missing baseline.

### 23.1 The tip-date precision is adopted

A head whose tip commit postdates the snapshot may have been created earlier and updated, or created
later. **Tip dates do not establish branch creation.** The post-snapshot tip table in §22.3 is therefore
metadata only. The phrase "three additions" in §22.3 is withdrawn as a description of the set difference;
only the count difference (60 → 63) and the current listing are factual. No added, deleted, or renamed
head is inferred from timestamps, arithmetic, or guesses.

### 23.2 The dated addendum

| Property | Value |
|---|---|
| Branch | `docs/scientific-roadmap-audit-2026-11-18` |
| Commit | `26cba39`, parent `874915b` |
| File | `docs/SCIENTIFIC_ROADMAP_AUDIT_REVISION_2026-11-20.md` |
| Blob | `3ada9099ec3b68a0c48c9ed35883b7f321baa0d2` |
| Content SHA-256 | `e9aed65aeebd44bbffd7df6e0f2894386d06db1253a9c48646c07250eeff4847` |
| Size | 12,583 bytes, 205 LF lines |

Branch tips in the addendum are recorded as of its publication; the audit branch is shown there at
`15cabef`, which this ledger commit advances. That does not change any B1 presence, absence, path, or blob
finding.

The revision preserves the known facts and marks the limit explicitly:

- the current **63-head** listing is recorded in full (Appendix A), and was checked to match
  `git ls-remote --heads origin` exactly at publication;
- the 60-name baseline was never archived, so the historical added/deleted/renamed comparison is
  **UNVERIFIED**, not reconstructed;
- the B1 v1.7 inventory is corrected to the same path and same blob `8c666e50` on both GPT branches, absent
  from the other four checked branches;
- the analytical-validity closure, the §5.3 text-verification boundary, and the provenance distinction are
  recorded;
- no frozen record, protocol, threshold, bank, population document, or solver is altered.

### 23.3 Cycle closed

- The analytical-validity review cycle is **closed**. No further combinatorial revisions and no further
  branch-history speculation.
- The roadmap addendum was the last outstanding documentary item; it is published with its uncertainty
  intact.
- **No execution, fitting, sampling, solver construction, or bank access.** The project pause remains in
  force.
- **The scientific position is unchanged:** no solver outcomes, no demonstrated predictive gain, and no
  evidence that `C_D` outperforms the predeclared competing summaries. The next substantive work, when
  explicitly reopened, is Gate 0, measurement validity, and the S1 known-effect validation.

---

## 24. Gate 0 scoping round recorded (2026-11-20)

**Trigger:** GPT's Gate 0 memo and Claude's review of it, supplied 2026-11-20. This opens the Gate 0 phase
that the goal document already names as next; the analytical-validity cycle closed at §23 and is not
reopened. No combinatorial revision, no branch-history work, no solver work.

### 24.1 Verified against the publisher records

- **The 2015 AST paper exists and is a genuine precursor.** Almaghairbe & Roper, *Building Test Oracles by
  Clustering Failures*, 2015 IEEE/ACM 10th International Workshop on Automation of Software Test (ICSE),
  pp. 3–7, `10.1109/ast.2015.8`. Its abstract states the hypothesis that "failures will tend to group into
  small clusters", evaluated on two systems, with an order-of-magnitude reduction in outputs needing manual
  examination. It was absent from the register and is now row 8a.
- **The ≥60 % figure is verified.** The publisher abstract of the *Software Quality Journal* paper
  (`10.1007/s11219-016-9339-1`, 25(3):803–840) reads: "in many cases small clusters were composed of at
  least 60 % failures (and often more)". Claude was right that the earlier round had not checked it. The
  qualifier "in many cases" is part of the finding and is now recorded.
- **Both Almaghairbe records match Crossref**, including the online-2016 / issue-2017 split.

### 24.2 Adjudicated

| Claim | Disposition |
|---|---|
| AST 2015 is **closer** to the concentration idea than the SQJ paper | **Partly accepted.** It is the earlier statement and takes priority for the observation; the SQJ paper remains the closest *evidence*. Neither tests `P` |
| The exact cell leaves `C_D` only the "ordering" of the configuration | **Accepted with correction.** `C_D` is label-permutation invariant; within a fixed-`k` cell only the largest part `M` varies, and only through its size — never through which stratum holds it |
| Within-cell distinct-`C_D` counts are needed before power | **Accepted.** B1 v1.7 already makes `W_{C,c}^train > 0` an estimability condition, so this is a census, not a missing design element. Not computed: it needs the LC518 tables, which are not in this tree, and bank access is paused. Pre-registered in register §9.3 with a stop rule |
| Gate 0 carries no power or MDE | **Accepted in part.** The record has illustrative MDE arithmetic, but `σ_u` and `sd(C)` are assumed, and the bank disclaims power. No empirical MDE exists; adopted as a Gate 0 exit condition |
| "No exact match" cannot close Gate 0 | **Accepted; already the record's position.** §7 calls the search non-systematic, §8 calls `P` unproven. The explicit acceptance sentence is now in register §9.5 |
| Citation artifacts in the memo | **Interface artifacts, not record errors.** §4/§6 carry DOI-verified citations only |

### 24.3 Effect on the record

- `NOVELTY_AND_POSITIONING_REGISTER_2026-11-19.md` §9 is the dated amendment (row 8a, the abstract
  verification, the support ceiling, the pre-registered census, the MDE status, the acceptance sentence).
  §1–§8 are unchanged, including the verdict.
- **Gate 0 remains OPEN. `P` remains unproven.** No contribution statement is accepted yet.
- **No execution, fitting, sampling, solver construction, or bank access.** The pause remains in force.
- The next Gate 0 deliverable is the scoping review GPT specified (four comparison groups, evidence matrix,
  backward/forward citation checks), not a solver plan. The first Gate 1 action on reopening is the
  design-only support census of register §9.3.

---

## 25. Follow-up adjudication — full text, B1 eligibility, and Gate 4 separation (2026-11-20)

**Trigger:** continued review of the Gate 0 amendment in register §9 after the independent critiques.
This section corrects over-broad language in §24 without rewriting that dated decision record.

### 25.1 Verified and accepted

- **SQJ full-text qualification.** Accepted. The publisher abstract says “in many cases” small clusters
  contained at least 60 % failures. The full text demonstrates system/version/configuration heterogeneity:
  Sed's §6.2 small-cluster failure density remains below 50 % in the reported analysis, and NanoXML
  version 3 is reported to have most failures in its largest clusters. Failure density within small
  clusters must be distinguished from the fraction of all failures captured by those clusters. Register
  §9.2 now records the distinction.
- **Bibliographic additions.** The DOI/title/venue records for Dickinson et al. (2001), both Wu et al.
  (2004) papers, Herzig (2014), Chen et al. (2017), Xiong et al. (2018), and Tian et al. (2022) are added
  in §9.7. Abstract-only and full-text verification levels are explicit. The additions do not establish
  novelty.
- **Exposure support arithmetic.** Accepted. The record-level formula is not the canonical-level
  attainable-set formula. At k=54, canonical capacities cannot realise M=7 because their maximum total
  under M≤7 is 4+7×7=53; the record basis can realise M=7. The ≤8 distinct-C_D ceiling remains valid
  on both bases.
- **B1 eligibility distinction.** Accepted and corrected. Full-population eligibility requires
  k≥2, G_c≥3 distinct parents, and D_c≥2 distinct C_D values. LOPO training-fold estimability separately
  requires G_c^train≥2, D_c^train≥2, and W_C,c^train>0. The earlier two-parent census stop rule did
  not reproduce the full-population gate and is withdrawn. The census now requires the complete
  scored/excluded fold-cell audit, parent coverage, and exact scored-row sets on each exposure basis.
- **Contribution wording.** Accepted with precision. The predictor is version-level C_D(v), but the
  outcome is record-level Y_{v,r} over 78 records. “Held out” refers to parent-grouped LOPO, not a
  sealed bank or a version-level correctness scalar.

### 25.2 MDE adjudication corrected

The previous §24.2 disposition stated that absence of an empirical MDE was a Gate 0 exit condition.
That was an overreach and is corrected here. Gate 0 is literature positioning and contribution scope;
power/MDE and known-effect operating characteristics belong to Gate 4.

The expression MDE₈₀ ≈ 2.802·σ_u/(sd(C)·√J) and its numerical examples are illustrative for a
simplified cluster-level approximation, with assumed inputs. They are **not a B1 v1.7 MDE**. B1's
version-level exposure is nested within parents, and the response is record-level across 78 records per
version, evaluated by LOPO and a conditional randomization pipeline. The simple expression cannot
justify the claims that 30 parents are insufficient, that 150 variants are required, or that 150 is
adequate. A future operating-characteristic assessment would have to simulate the actual frozen B1
pipeline under declared data-generating processes and its exact support/coverage rules. No such
assessment has been run.

### 25.3 Effect on the record

- Register §9.2 now qualifies the ≥60 % abstract finding against full-text exceptions.
- Register §9.3 now separates record-level and canonical-level support and restores the full B1
  eligibility/fold-audit requirements.
- Register §9.4 moves MDE/power to Gate 4 and withdraws any sample-size inference from the simplified
  illustrative formula.
- Register §§9.7–9.8 add the evidence-matrix extension and precise candidate contribution statement.
- **Gate 0 remains OPEN and P remains UNPROVEN.** The citation search remains a scoping review; broader
  database coverage and backward/forward citation checks are outstanding.
- B1 v1.7, Rev 11, the measurement specification, and all other frozen records remain unchanged.
  No bank access, outcome access, solver construction, experiment, fitting, simulation, or execution
  occurred. The project pause remains in force.

---

## 26. Claude follow-up review — Sed DBSCAN and bibliography check (2026-11-20)

**Disposition:** the Sed qualification is accepted and expanded. The earlier register sentence was
correct about the agglomerative result but incomplete: §6.2 also reports very high failure density in
Sed's smallest clusters under DBSCAN, with a reasonable F-measure. The different clustering methods
produce different results; this is evidence of configuration sensitivity, not a reason to remove the
sub-50 % observation. NanoXML version 3 remains the counterexample where larger clusters held most
failures. The register now records all three.

**Bibliography adjudication:**

1. Dickinson et al. (2001): DOI `10.1145/503209.503243` retained. The conflicting `503241.503243`
   secondary entry is not adopted.
2. Wu et al. (2004), input-level model: paper identity and proceedings metadata corroborated, but
   third-party DOI identifiers conflict. The register withholds the DOI pending primary publisher/
   Crossref resolution.
3. Wu et al. (2004), maximum-entropy model: bibliographic record and abstract-level result remain
   corroborated; full text is not claimed as reviewed.
4. Chen et al. (2017): full text confirmed; journal issue corrected to 66(3), pages 806–824.
5. Xiong et al. (2018): the full paper's first-page citation confirms DOI `10.1145/3180155.3180182`.
6. Tian et al. (2022): the publisher postprint and institutional bibliographic record confirm DOI
   `10.1145/3511096`.

**Effect on the record:** register §9.2 adds the DBSCAN result; §9.7 corrects Chen's issue, withholds
Wu input-level DOI pending resolution, and clarifies Dickinson's DOI conflict; §9.9 records this
adjudication. README indexing is updated.

**Gate status:** Gate 0 remains OPEN. The wider scoping review, reproducible search log, and systematic
backward/forward citation checks are incomplete. Foued's conditional Gate 1 instruction is therefore
not triggered as a formal gate transition. No Gate 1 freeze, bank access, design census, or outcome work
is authorized by this entry. No frozen protocol was changed.

---

## 27. Claude verification of the SQJ DBSCAN row and Gate 1 measurement blockers (2026-11-20)

### 27.1 SQJ full-text check

The primary paper confirms the DBSCAN figures in Table 7 for Sed V5: cluster count 48.23 %,
average cluster size 1 %, failure density 83.3 %, and F-measure 0.3091. The DBSCAN parameters
given in the table caption are epsilon = 1.5 and MinPoints = 1 for Sed. The authors state that
DBSCAN generated almost twice the number of small clusters explored under agglomerative
hierarchical clustering. The high density is therefore accompanied by heavy fragmentation; it
must not be described as high recall, broad failure capture, or a generally superior clustering
result. Register §9.2 and §9.9 now record the exact row and caveat.

### 27.2 Repository and design checks

- Commit `f2d57f40313f19335af0b7992318122c19780ab5` exists on branch
  `audit/analytical-validity-2026-11-18`; its parent is
  `ad0f1004d78b28ddb403f96c8ce3a6be07184a00`.
- The frozen bank design specifies 64 diagnostic records, including four D6 canonical inputs
  represented by two orderings each (60 unique diagnostic canonical inputs), and 80 held-out
  records comprising 78 unique canonical inputs. The held-out H6 stratum has two canonical
  pairs plus six singletons. Canonical disjointness between diagnostic and held-out banks and
  the feature firewall are explicit in BANK_DESIGN v1.0 §§2, 7.
- B1 v1.7 §1 defines a binary outcome `Y_{v,r}` on 78 version-by-canonical-record rows and
  primary-cell eligibility `k ≥ 2`, `G_c ≥ 3`, `D_c ≥ 2`. Its §3 fixes LOPO scoring and the
  fold-level design-only support conditions. Claude confirms she had now read this text;
  her earlier uncertainty about B1(c) is withdrawn.

### 27.3 The two held-out ordering pairs: correction to the option list

The phrases **“fail if either ordering fails”** and **“pass only if both orderings pass”**
are logically the same Boolean aggregation rule, not two different options. For a two-record
canonical pair, both say that the canonical input passes only when both orderings pass.

The genuinely distinct choices are:

1. **Conservative all-orderings rule:** canonical PASS only if both raw executions PASS;
   canonical FAIL if either execution is a definite FAIL; otherwise canonical UNRESOLVED.
2. **At-least-one-pass rule:** canonical PASS if either raw execution PASS. This does not
   establish order invariance and can label a canonical input correct despite a definite
   wrong answer on its other ordering.
3. **Separate-record rule:** retain both orderings as separate rows. This changes the outcome
   unit from 78 canonical inputs to 80 raw records and requires a revised dependence/weighting
   treatment; it is not compatible with B1 v1.7's current 78-row estimand without amendment.

The conservative all-orderings rule is the most coherent candidate if the scientific correctness
predicate requires order invariance: PASS iff both pass; FAIL if at least one definitely fails;
UNRESOLVED if no definite failure exists and at least one ordering is unresolved. A singleton
canonical input retains its raw status. **This is a proposed aggregation rule, not a frozen
decision.** B1 v1.7 does not currently specify any pair-to-canonical aggregation.

### 27.4 Unresolved held-out outcomes

Three existing documents agree on the raw status semantics:

- The task contract §5 says an observation lacking sufficient harness/oracle evidence is
  UNRESOLVED, not PASS or FAIL; timeout classification requires a declared execution budget.
- The GLM work order §8 says UNRESOLVED is neither PASS nor FAIL, must be counted separately,
  and must not be collapsed into a binary record. Its §9 resolved-only score, coverage, and
  best/worst bounds apply to its earlier mean-correctness target `Q`, not automatically to
  B1's later record-level log-loss estimand.
- B1 v1.7 fixes binary `Y_{v,r}` and its 78-row log-loss, but contains no rule for converting
  an unresolved held-out observation into `Y`, no missing-outcome likelihood, and no frozen
  resolved-only scoring rule. Its references to `u(v)` and unresolved placement are about
  diagnostic unresolved counts and a named explanatory channel, not held-out `Y` coding.

**Candidate conservative handling, not adopted:** first aggregate raw paired statuses to a
three-state canonical status as in §27.3. Preserve every UNRESOLVED status. The B1 binary
confirmatory analysis is available only when every primary-sample version has a resolved
PASS/FAIL status for all 78 canonical inputs. If any primary target row remains unresolved,
declare the B1 binary test NOT_ESTIMABLE for that dataset; do not delete the row, impute it,
or silently recode it. Report unresolved counts and coverage by held-out stratum and version.
A resolved-only descriptive score with explicit coverage and best/worst correctness bounds may
be shown as a clearly separate descriptive result, but it is not the B1 primary log-loss result.
A three-category outcome model would require a new, separately reviewed B1 version and a
different estimand/model; it is not a sensitivity silently available under v1.7.

The unresolved-rate table must be a predeclared reporting output. It may not be inspected to
choose the aggregation or missingness rule after outcomes are observed. The rule itself must be
fixed first; observed unresolved rates then describe coverage and determine whether the declared
availability condition is met.

### 27.5 Gate disposition

Claude's review confirms that the two held-out measurement gaps are real. The diagnostic
measurement is specified at record level by Rev 11; the diagnostic-to-held-out linkage is by
version ID, with `C_D(v)` supplied to that version's 78 canonical correctness outcomes. The
remaining blockers are (i) the raw-pair-to-canonical outcome aggregation and (ii) unresolved
held-out outcome handling in the B1 binary likelihood.

However, Gate 0 remains OPEN because the scoping review's reproducible search log and
systematic backward/forward citation checks are incomplete. Foued's conditional instruction
“if Gate 0 is done, resolve Gate 1” is therefore not triggered as a formal gate transition.
Sections 27.3–27.4 are design proposals for review, not Gate 1 amendments. No freeze or
implementation authorization follows. Rev 11, B1 v1.7, and the existing measurement
specification remain unchanged; no outcome or bank access, fitting, or solver execution occurred.

---

## 28. B1 78-row identity recovered; Wu ASE DOI resolved (2026-11-21)

**Trigger:** the owner's direct question whether any file identifies B1 v1.7's actual 78
development-bank rows, and the Wu et al. (2004) ASE DOI left open in §26 and register §9.7/§9.9.
Sections 25–27 and register §9 already record the round-2 literature additions, the two exposure
bases, the full-population and fold-level B1 eligibility rules, the Gate 4 relocation of
power/MDE, and the candidate contribution statement. This entry does not re-add those items. It
records only the identity-source recovery and one bibliography resolution.

### 28.1 The B1 78-row identity source is recoverable

The full record is `B1_78_ROW_IDENTITY_RECOVERY_2026-11-21.md`.

**What B1 v1.7 says.** Only the symbolic index `r = 1,…,78`. It does not enumerate keys or cite a
bank path or hash. Its change table item 7 deliberately removed the 138/144/6 erratum counts, so the
chain does not run through the erratum.

**What the record supplies.** Rev 1.1 §1.4 — inherited by Rev 1.4 §1 and carried into B1 v1.7 §1
item 1 — defines the outcome population as "78 unique canonical records of the fixed, publicly
exposed held-out bank." The B1 decision reconciliation §6.1 pins the artifact
(`lc518-bank-run-41591572358-1.zip`, 75,523 B, SHA-256
`6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`, equal to GitHub artifact
`13210063805`, run `41591572358`), and §6.5 records that the artifact containing
`bank/heldout_bank.json` and its oracle answers was publicly downloadable. The erratum §3 pins the
same hash to the same artifact ID.

**What the artifact contains.** `bank/heldout_bank.json` (40,218 bytes, `b273c053…26d6`) has 80 raw
records and 78 unique canonical identities. `bank/heldout_oracle_outputs.json` (15,262 bytes,
`eaae8104…e244`) has 78 objects and an equal key set. The collapse is exactly the two H6 reorder
pairs `H057`/`H058` (`H6-P01`) and `H059`/`H060` (`H6-P02`). The 78 B1 rows are the **78 canonical
identities**, not the 80 raw rows. The sorted key set hashes to `01bb0e4c…3cccd`; the sorted
`(amount, sorted(coins))` payload set hashes to `8b67d1f0…e48fa`.

**Provenance caution.** The Git copy of the ZIP is a later upload (commit `2d5f9c3`, 2026-11-18) on
`origin/foued2-patch-3`. It is not a post-B1 reconstruction: its hash is the hash of the 2026-11-03
artifact, and the erratum pins that hash. The Git upload date is not the generation date.

**Measurement caution.** Identity recovery is not outcome coding. The artifact supplies one oracle
answer per `canonical_id`, but B1 v1.7 does not fix how two raw execution statuses collapse to one
`Y`; §27.3–§27.4 already record that as an open Gate 1 measurement gap. This entry neither adopts an
aggregation rule nor resolves unresolved-status handling.

**Disposition.** The identity source is **RECOVERED**; the B1 identity gate moves from
**source-missing** to **source-recovered / adjudication pending**. This is not a `78 = 78` inference:
it is B1's own definition of its outcome population plus the contemporaneous identification of the
bank. It is not a B1 v1.7 citation, and it does not fix a historical enumeration order; `ω_r` is a
free record effect, so any order is a reporting convention. The gate is not closed unilaterally. The
two lawful paths are: (a) the owner/GPT accepts the chain and records the path/hash in a dated B1
addendum; or (b) a contemporaneous B1-issued manifest is supplied, or B1 design is reopened. No third
path substitutes H80 by cardinality.

### 28.2 Wu et al. (2004), ASE: the withheld DOI is resolved

Section 26 and register §9.7/§9.9 withheld the DOI for "A Statistical Model to Locate Faults at
Input Level" (ASE 2004, pp. 274–277) because third-party records disagreed. The primary registration
record resolves it:

- Crossref `10.1109/ASE.2004.1342745` returns the matching title, authors (Wu Ji, Jia Xiao-xia, Liu
  Chang, Yang Hai-yan, Liu Chao, Jin Mao-zhong), proceedings, pages 274–277, publisher IEEE.
- The DOI handle resolves to `http://ieeexplore.ieee.org/document/1342745/`.
- The competing strings do not identify this paper: `10.1109/ASE.2004.1342763` is a different ASE
  2004 paper (Choi & Heimdahl, "Combination model checking", pp. 354–357);
  `10.1109/ASE.2004.10008` and `10.1109/ASE.2004.7` do not resolve.

Row 8c now carries `10.1109/ASE.2004.1342745`. The verification level remains a bibliographic record
plus DOI handle; the full text was not reviewed, and the paper is not evidence for `P`.

### 28.3 Effect on the record

- `NOVELTY_AND_POSITIONING_REGISTER_2026-11-19.md` §10 is the dated amendment; §1–§9 are unchanged.
- `B1_78_ROW_IDENTITY_RECOVERY_2026-11-21.md` is the standalone provenance record.
- **Gate 0 remains OPEN. `P` remains unproven.** No novelty claim is licensed.
- **B1 v1.7 is unchanged and is not amended.** The identity gate is source-recovered, not closed.
  *(Superseded for current status by §28.4; retained as the 2026-11-21 position.)*
- **No execution, fitting, sampling, solver construction, calibration, or outcome model.** The only
  bank access was read-only identity inspection of the held-out artifact; the project pause remains in
  force.
- The next Gate 0 deliverable remains the scoping review (comparison groups, evidence matrix,
  citation sweep), not a solver plan. The first Gate 1 action on reopening remains the design-only
  support census, on both bases and with the full-population and fold-level B1 audit reproduced.


### 28.4 Subsequent owner adjudication (2026-11-22)

The owner accepted the documentary chain on 2026-11-22. The controlling dated decision is `B1_IDENTITY_ACCEPTANCE_ADDENDUM_2026-11-22.md`. The full recovery reasoning remains in `B1_78_ROW_IDENTITY_RECOVERY_2026-11-21.md`; the v3 audit and its CSV/JSON manifests provide the reconstructed identities and derived-file checksums.

Section 28.1's **source recovered / adjudication pending** language records the position before the owner act and is retained as history. Current identity status is **source-recovered / owner-accepted**. This resolves identity attribution only: historical B1 row ordering, H6 primary presentation/aggregation, unresolved-status handling, and outcome coding remain open. No (Y_{v,r}) matrix exists or is authorized by this acceptance. B1 execution remains unauthorized; Gate 0 remains OPEN; (P) remains unproven. B1 v1.7 is unchanged.

---

## 29. Gate 0 scoping search executed; no direct match to (P) (2026-11-22)

### 29.1 What was executed, and what was not

The approved twelve-query protocol was **not** executed verbatim, and the deviation is recorded here for the same reason the earlier three-query screening was rejected: an unrecorded protocol cannot be audited.

- **Instrument:** the web-search connector returned HTTP 402 on every call. Queries were therefore translated to OpenAlex `title_and_abstract.search` phrase/Boolean expressions, with Crossref used only for DOI verification. The translation is a documented deviation, not a silent substitution.
- **Queries:** 18 informative expressions plus 2 discarded. Two planned strings collided in the Boolean index (one swallowed by an ungrouped `OR "test"`, one returning predictor–corrector numerics), so the four themes were covered by 18 expressions instead. The query log with counts is in the search record §3.
- **Dates:** the 1990-01-01 to 2026-11-22 window was not applied as a filter. No pre-1990 record was judged relevant; the omission is stated rather than assumed harmless.
- **Screening:** title-level on approximately 431 records. Abstracts were retrieved for seven candidates; the IEEE TSE record indexes none. **No full text was read in this pass.**
- **Citation chasing:** forward for three works (Almaghairbe 2017, Song 2022, Hybiscus 2021); backward for two (Song 2022, 98 references; Almaghairbe 2017, 26 references). The TSE 2026 record deposits no references, so its backward chase is not possible from the index.
- **Coverage:** OpenAlex only. No Scopus, Web of Science, ACM DL, or IEEE Xplore subscription access; English-language bias.

### 29.2 Result

**No direct match. No partial match.** Four works are adjacent-close in the defined sense: they share either the per-input correctness target or the failure-concentration observation, never the conjunction.

- Almaghairbe & Roper (2017, *SQJ*, `10.1007/s11219-016-9339-1`): learned clusters, cluster composition, no maximum-share covariate, no held-out per-record model, no parent grouping.
- Almaghairbe & Roper (2019, AITest, `10.1109/aitest.2019.00009`): concentration used as an inspection-ordering device, not as a predictor in a correctness model.
- *Can Open-Weight LLMs Predict Test Outcomes from Traces?* (2026, `10.1145/3843782.3844663`): predicts per-test pass/fail on held-out subjects, but the predictor is a fine-tuned LLM over traces, with no exact-cell baseline and no parent grouping.
- BASHIRI (2025, ASE, `10.1109/ase63991.2025.00372`) and *Striving for Failure* (2015, ICSE, `10.1109/icse.2015.134`): outcome prediction and pre-run failure prediction respectively; neither uses failure composition, neither is a record-level bank, neither is parent-held-out.

The corpus contains a mature concentration *observation*, a mature clustering-for-debugging literature, and a mature per-input outcome-prediction literature. It does not contain a prespecified-partition maximum share evaluated against an exact-cell, failure-count-conditioned baseline with parents held out.

### 29.3 Records added

Register §11 and the search record §6 add the two Systemic Flakiness publications as **distinct** records (EASE 2025 `10.1145/3756681.3756945`, pp. 476–487; IEEE TSE 2026 `10.1109/TSE.2026.3750452`, pp. 1–21, Crossref record created 2026-11-03, Xplore 11773385). Both resolve through Crossref and OpenAlex.

**Correction carried forward.** The 2026-11-22 statement that no IEEE TSE version exists is wrong. The caution behind it — do not cite an unverified DOI — was correct in principle and is now satisfied by the publisher record, not waived.

### 29.4 Effect on the record

- **Added:** `GATE0_LITERATURE_SEARCH_2026-11-22.md`; register §11; rows 20–21.
- **Unchanged:** register §8 verdict, the exposure-basis arithmetic, the two-level B1 eligibility rule, the Gate 4 relocation of power/MDE, and the candidate contribution statement.
- **Gate 0 remains OPEN. `P` remains unproven. No novelty claim is licensed.** A documented non-finding on one index with stated limits is a scoping result, not a priority claim.
- **B1 v1.7 is unchanged.** No solver construction, execution, fitting, sampling, calibration, or outcome model. No bank access in this pass.
- **Superseded language noted:** the sentence in §28.3 reading "The identity gate is source-recovered, not closed" is the 2026-11-21 position and is superseded for current status by §28.4 (**source-recovered / owner-accepted**). It is annotated in place rather than rewritten; register §10.3 carries the same annotation.

### 29.5 What follows

The literature is no longer the binding constraint. The remaining sequence is:

1. **Accept or reject this search record** as the Gate 0 scoping deliverable. Do not describe it as a systematic review.
2. **State the contribution object plainly:** the design — a prespecified-partition dominance covariate tested against an exact-cell, failure-count-conditioned baseline under parent-held-out evaluation, with a pre-registered null-capable outcome. The index is borrowed (Berger–Parker 1970) and the phenomenon is known (Almaghairbe 2015/2017). Register §9.8 already moves this way.
3. **Authorize the design-only support census** — the last Gate 1 prerequisite. It needs the LC518 diagnostic tables, which the pause currently forbids, uses no outcomes, and answers whether B1 has any eligible cell and any scoreable LOPO fold at all.
4. **Do not fund a 150-solver programme before step 3.** The one executed world retained about 0.25 percent of the full vector's gain, with an interval spanning zero. That does not refute `C_D`; it sets the prior that the most likely B1 outcome is a well-identified null.
5. **Do not run further keyword searches over the same object and call the result novelty.** Do not reopen the identity documentation. This section is not an execution GO.

---

## 30. Owner accepts the Gate 0 search record; pause retained (2026-11-22)

### 30.1 The decision, and its provenance

On 2026-11-22 the owner accepted `GATE0_LITERATURE_SEARCH_2026-11-22.md` as the Gate 0 scoping deliverable, and selected the narrower of the available options: **accept the search only**. The design-only support census was **not** authorised and continues to wait on a separate decision.

**Provenance.** This is an owner-authored conversational decision in the project session on 2026-11-22, not a repository artifact. As with the identity acceptance in §28.4, a reviewer who does not hold that conversation cannot authenticate it from the repository alone. It is recorded here as the owner's act, not as corroboration.

### 30.2 Accepted scope

The record is accepted with its protocol deviations and limits intact: substituted instrument (OpenAlex via API; chat web search returned HTTP 402), 18 informative expressions plus 2 discarded, no date filter applied, title-level screening of ~431 records, abstracts for 7, no full-text reading, forward chasing for 3 works and backward for 2, OpenAlex-only coverage with Crossref for DOI verification.

Acceptance does not convert this into a systematic review. Record §8's limits and §9's verdict stand unmodified, including the statement that the search does not establish novelty.

### 30.3 What the acceptance does not do

1. **Not a novelty finding.** `P` remains unproven; register §8 is unchanged.
2. **Not Gate 0 closure.** Closure requires a documented scoping review **and** an adopted contribution decision. The first is now recorded; the second is not. Gate 0 remains **OPEN**.
3. **No census.** The design-only census on the LC518 diagnostic tables remains unauthorised and the project pause remains in force in full.
4. **No downstream authorisation.** No solver construction, execution, diagnostic collection, outcome labelling, `Y` matrix, sampling, fitting, or predictive analysis.
5. **No measurement decision.** H6 primary aggregation, unresolved-status handling, outcome coding, and historical row numbering remain open.
6. **No adopted contribution object.** Register §11.4's statement that the design is the defensible contribution is a recommendation until separately decided.

### 30.4 Effect

- **Added:** register §12; this section.
- **Changed:** nothing in §§1–29, and nothing in the search record itself.
- **Unchanged:** Gate 0 OPEN; `P` unproven; B1 execution unauthorised; B1 v1.7 unchanged; pause in force.

The only remaining Gate 0 item that needs no data access is the contribution decision. The census stays the first Gate 1 action and stays blocked.

---

## 31. Two reviews; four corrections; one open decision (2026-11-22)

### 31.1 What arrived

GPT's Gate 0 review and Claude's response to it, both dated 2026-11-22. GPT resolves the DOI dispute in the record's favour, accepts the search as a bounded scoping deliverable, and proposes splitting Gate 0 into a scoping/contribution decision and a new feasibility gate. Claude concedes the TSE DOI question, disputes the TSE article's scope, questions the authenticability of the owner acceptance, and argues that the support census must precede adoption because a null is uninformative without power.

The applied corrections and the reasoning are in register §13. This section records the ledger-side effect only.

### 31.2 Corrections now in the record

1. **431 is a sum, not a union.** Search record §§2, 3 and 8 now state that 431 is the total of 18 first pages (17 × 25 + 6), that the unique union was never computed, and that only page one of each expression was screened. The supported sentence is bounded accordingly.
2. **The TSE record is title-level only.** Crossref confirms title, four authors, IEEE TSE, pp. 1–21, record created 2026-11-03, no volume or issue. It deposits no abstract. The "24 Java projects" scope belongs to the EASE 2025 paper, which is a separate publication; the TSE title extends to Java and Python. Register row 21 no longer attributes a method or a project count to the TSE article.
3. **The acceptance's authentication limit is stated plainly.** §30.1 already recorded the decision as conversational. Register §13.1(c) now adds that no repository artifact independently attests it and names what would: a dated owner note in the owner's own words. None is manufactured.
4. **The unsupported-sentence bound is restated.** "No such work exists" is not supported, was not claimed, and is now explicitly excluded in both the search record and register §13.1(a).

### 31.3 The structural disagreement, resolved against the frozen gates

GPT proposes a new feasibility gate. The goal document already separates the three questions: Gate 0 holds the tested/novel question and the contribution paragraph; Gate 1 holds support and estimability, beginning with the design-only census; Gate 4 holds power, MDE and operating characteristics. Adding a gate would duplicate Gate 1 plus Gate 4 and contradict `FUNDAMENTAL_GOAL` §3, so no such change is made. The correct statement of GPT's point is that Gate 0 is being asked to wait for feasibility, which is not its question.

Claude's constraint survives in a narrower and stronger form: a null is not automatically informative, and the adopted statement must pre-commit to reporting a null as **inconclusive** unless Gate 1 support and Gate 4 power establish a detectable effect. That is a reporting rule, not a reason to withhold the question.

### 31.4 What remains

Exactly one Gate 0 item: adoption of the contribution paragraph in register §13.4, with the null-interpretation rule attached. It requires no data access and authorises nothing. The census remains unauthorised; the pause remains in force; `P` remains unproven; Gate 0 remains **OPEN**.

No solver construction, execution, fitting, sampling, calibration, or outcome model was performed in this round. The only external calls were two Crossref metadata lookups used to settle the TSE/EASE scope question.

---

## 32. Owner adopts the contribution statement; Gate 0 closed (2026-11-22)

### 32.1 Owner decision

The owner explicitly confirmed adoption of register §13.4 **as written** in the 2026-11-22 project conversation. The owner also declined an additional authentication artifact for the earlier search-record acceptance, leaving the provenance caveat in register §§12.1 and 13.1(c) unchanged.

The adoption is therefore a direct owner decision, not an inference from DeepSeek's pasted report. The earlier search acceptance remains recorded with its existing conversational-provenance limitation.

### 32.2 What was adopted

The complete contribution paragraph in register §13.4 was adopted without modification. It defines the intended contribution as the controlled, null-capable test of incremental predictive value for the version-level maximum-share summary, against the exact-cell baseline, on the fixed publicly exposed B1 development bank under leave-one-parent-out evaluation.

The statement explicitly disclaims novelty for the Berger–Parker index, failure concentration as a phenomenon, and execution-derived correctness prediction. It also disclaims a new-parent-population claim and information superiority over the full failure vector. Its null rule is binding: a null is inconclusive unless Gate 1 support and Gate 4 power establish that a stated effect could have been detected.

The exact adopted wording is controlled by register §13.4; this ledger does not create a second paraphrased version.

### 32.3 Gate 0 disposition

**Gate 0: CLOSED, limited to position and contribution definition.**

The scoping deliverable was accepted in §30; the bounded literature comparison and its limitations are recorded in register §§11–13; the inferential scope is fixed; and the owner has adopted the contribution paragraph. The closure is not a novelty finding. P remains **UNPROVEN**, and the supported search statement remains limited to records screened in the OpenAlex pass.

This disposition does not close the wider research programme or certify empirical feasibility.

### 32.4 What remains open or unauthorised

- **Gate 1:** not started. The design-only support census remains unauthorised and blocked by the project pause.
- **Gate 4:** not started. MDE, power, and operating characteristics remain unestablished.
- A null without adequate Gate 1 support and Gate 4 power must be reported as inconclusive.
- H6 presentation/aggregation, unresolved-status handling, outcome coding, and historical row numbering remain open.
- B1 v1.7 remains unchanged. No solver construction, execution, diagnostic collection, outcome labelling, Y matrix, sampling, fitting, or predictive analysis is authorised.
- The project pause remains in force. Any reopening or Gate 1 work requires a separate explicit owner authorization.

### 32.5 Record effect

This entry supersedes the statements in §§30–31 that the contribution decision remained outstanding and Gate 0 remained open. Those entries are preserved as accurate historical snapshots before the owner's decision. The search record's limits, the unproven status of P, and all non-authorisations remain unchanged.

---

## 33. Owner settles the study population as engineered solvers (2026-11-22)

### 33.1 Direct owner decision

The owner explicitly states that the study is to be framed as a study of **engineered solvers**, rejecting “natural solvers” as a distinct target-population category. The owner's reasoning is that every solver has some authoring, design, construction, or transformation history, including human-authored implementations.

This decision is present directly in the 2026-11-22 project conversation. It supersedes the disputed use of “natural solver population” as the current target label. The decision is not inferred from Claude's recollection or from DeepSeek's report.

### 33.2 Scientific interpretation

For current B1, the target units are engineered solver variants deliberately constructed or modified under a declared study process, nested within selected real parent solver implementations. The parent implementations are source/grouping units; the engineered variants are the tested study units.

The intended inferential scope remains conditional on the selected and observed parents. The study does not thereby claim to represent every solver, all human-authored or model-produced implementations, or a superpopulation of independently developed parents.

This reconciles the current engineered B1 line with the owner's decision without pretending the October natural-solver feasibility exercises never occurred. Those exercises retain their historical results about the specific procedures and samples they tested. “Natural” is not used to describe a separate current target population.

### 33.3 Parent provenance retained as a requirement

The terminology decision does not waive provenance. Before future parent acquisition or selection, source identity, authorship/origin where known, lineage, transformations, outcome-blind selection, family assignment, hashes, permissions, and custody/consent status must be recorded.

Where a parent is specifically claimed to be model-generated, the six-point provenance gate in the 2026-11-21 master-branch adjudication §6 applies before relying on that claim. It requires independently verifiable generation-session evidence, exact model and settings, ordered raw outputs, body/file identity, a reproducible event-to-file manifest, and a fail-closed pre-freeze gate. This is a prerequisite, not authorization to acquire parents or generate solvers.

### 33.4 Notation clarification

The aliases in the adopted contribution statement map to the frozen Rev 11 support cell as follows: q = m (mutation mechanism/operator identity); Z = z (parent algorithm family); k = k_fail (definite failures); ℓ = k_unresolved (unresolved outcomes). The underlying support cell remains (m, z, k_fail, k_unresolved). No statistical variable or conditioning rule is changed.

### 33.5 Measurement questions not decided

- Rev 11 defines the diagnostic counting unit as a bank record, not a unique mathematical input, with N = 64 and eight records per stratum. This remains the protocol-prescribed record-level C_D unless an explicit protocol amendment is adopted. A canonical-level C_D is a distinct recomputed sensitivity, not an alternative to be selected after results.
- The H6 raw-pair-to-canonical correctness aggregation rule remains open. No rule is adopted in this entry. It must be settled before constructing or interpreting the canonical Y matrix.
- That H6 outcome rule is not itself required to compute a strictly outcome-free support census from diagnostic predictor tables. Such a census remains unauthorised while the project pause is in force.
- Unresolved-status handling, final outcome coding, and historical row numbering remain open.

### 33.6 Gate status and authority

Gate 0 remains CLOSED for position and contribution definition only; the population terminology is now explicit. This is not a novelty finding and does not establish P, predictive value, feasibility, or operational readiness. Gate 1 remains NOT STARTED and its census is NOT AUTHORIZED. Gate 4 remains NOT STARTED; MDE and power are unestablished.

B1 v1.7 and Rev 11 remain unchanged. The project pause remains in force. This entry authorizes no parent acquisition, solver construction, generation, mutation allocation, execution, diagnostic collection, outcome labelling, Y-matrix construction, fitting, or predictive analysis. Any reopening requires separate explicit owner authorization.

The earlier conversational acceptance/adoption provenance caveats remain as recorded in the register. This entry records the population decision from the current conversation; it does not create an independent authentication artifact for the prior decisions.

---

## 34. Strategic reset reported — blueprint is not evidence (2026-11-22)

### 34.1 Reported, not verified

The owner forwarded GPT's strategic message on 2026-11-22. PR #9 and revision 0.6 are on other lines of work; this branch contains no artifact against which their state could be checked, so nothing here is independently verified.

### 34.2 Accepted distinction and working approach

- PR #9 is a GitHub review workspace; revision 0.6 is a draft specification for counting diagnostic support, with a JSON Schema describing record structure. A PASS is agreement that the blueprint corrections are sound — not a scientific result, census result, or evidence about `P`.
- The programme has been checking the blueprint rather than building the machine. This ledger's §§29–33 and the register's §§11–15 belong to the paperwork layer; they changed no scientific milestone.
- Working approach recorded: keep 0.6 as reviewed and stop cosmetic revision cycles; scope the semantic validator to getting real diagnostic records safely into the census; measure progress in scientific outputs — parent roster, runnable variants, diagnostic bank, diagnostic measurements, validated manifest, census results, held-out predictive results — not PRs or review comments.

### 34.3 Where the status is already recorded

The scientific presentation and Gate 1 preflight status are in the repository root `README.md`, updated 2026-11-22. It records Gate 1 preflight as **BLOCKED / NOT ASSESSABLE** until a per-variant eight-stratum diagnostic manifest exists, with the owner's instruction limited to the design-only census once that manifest exists. This entry adds no second status table.

### 34.4 Boundary and effect

No authorisation is created here. No parent acquisition, solver work, diagnostic execution, manifest production, outcome collection or predictive analysis was performed. `P` remains unproven; B1 v1.7 unchanged; Gate 0 closed for position and contribution only; Gate 1 not started; pause in force outside the recorded preflight scope. No verdict in §§1–33 changes.

---

## 35. Intake prototype held for independent review (2026-11-22)

### 35.1 Scope of the review

GPT reviewed commit `0060e7b413b709f7ff66f7d9f89780fa2b1a1703` on
`work/b1-census-intake-validator-2026-11-22`. It is unmerged, separate from PR #9 and revision 0.6.
GPT acknowledged the executable artifact as engineering progress but classified it as infrastructure,
not scientific progress, and raised four findings.

### 35.2 Fact-check result

All four findings were independently confirmed against the code:

| # | Finding | Check |
|---|---|---|
| 1 | `canonical` basis admitted as a primary intake basis, despite register §15.5 fixing record-level as primary | Confirmed: two bases defined and both admitted, with a passing canonical test |
| 2 | Supplied `f`/`u` aggregates validated, but no 64 per-result terminal statuses inspected or derivation checked | Confirmed: no status field in the record contract |
| 3 | `source_digest` checked only as a hex string; no bank/artifact or record-ID membership verification | Confirmed: regex-only check, consistent with the no-bank-access scope but not provenance verification |
| 4a | Empty manifest admitted, CLI exits 0 | Confirmed by direct call |
| 4b | Non-string `exposure_basis` raises uncaught `TypeError` | Confirmed by reproduction |

The 18 synthetic tests were re-run locally (18/18). GPT had inspected but not reproduced them.

### 35.3 Governance disposition

The artifact is to be called a **synthetic-tested summary-record intake prototype**, not the B1
semantic validator. GPT's instruction: preserve the branch, do not merge, do not run on real records,
and implement no correction before Claude's agreement. A review packet with the findings,
reproductions and a requested **PASS / NOT PASS** is at
`census-intake/REVIEW_PACKET_FOR_CLAUDE_2026-11-22.md` on the work branch (commit `639ee3f`).
Claude's verdict is outstanding. This ledger does not substitute a local verdict for it.

No validator code was changed after the findings arrived. No bank access, solver work, diagnostics,
manifest, census, fitting or predictive analysis occurred.

### 35.4 Scientific position unchanged

No new LC518 diagnostic measurement exists. Gate 1 preflight remains BLOCKED / NOT ASSESSABLE.
`P` unproven; Gate 0 closed for position and contribution only; B1 v1.7 unchanged; pause in force.
No verdict in §§1–34 changes.

---

## 36. v0.2 intake successor implemented; independent review pending (2026-11-22)

### 36.1 Decision and work

GPT accepted Claude's NOT PASS on `0060e7b` and the two-reviewer correction scope. The local agent
implemented that scope on a separate successor branch, `work/b1-census-intake-validator-v02-2026-11-22`,
commit `fd0b34b`. Prototype `0060e7b` remains held and unchanged; no history rewritten, no merge to
master. Register §18 records the implementation; `census-intake/CORRECTION_RECORD_2026-11-22.md`
records the scope, hashes and non-authorizations.

### 36.2 What the successor does

Validates individual `diagnostic_record_results` under `measurement_basis = record_level_64`, with D1–D8
status checks and per-variant uniqueness; derives f/u/p and `C_D` from terminal statuses; rejects
conflicting or malformed aggregates; accepts record-ID reuse across complete `VALID` variants but
rejects differing ID sets; applies status-specific rules to INCOMPLETE and zero-result statuses; and
emits `SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED` with a `NO OBSERVED FAILURES` zero state.

Twenty-five synthetic tests pass. The earlier 4(b) reproduction was corrected by appending §6 to the
review packet; the original review was not rewritten.

### 36.3 What is not decided

Claude has not reviewed the successor; the synthetic result is not a PASS verdict. No bank membership,
provenance or source integrity was checked. No real manifest, parents, solvers, diagnostics, census,
fitting or predictive analysis occurred. The question whether the earlier conditional census
authorization remains operative or was revoked is deliberately left unanswered; neither interpretation
is recorded here.

### 36.4 Effect

No verdict in §§1–35 changes. Gate 0 closed for position and contribution only; Gate 1 preflight
BLOCKED / NOT ASSESSABLE; `P` unproven; B1 v1.7 unchanged; pause in force outside the recorded
preflight scope.


---

## 37. GPT-owned v0.3 B1 intake rewrite; independent review pending (2026-11-23)

### 37.1 Authorship and historical preservation

HY4 authored the earlier prototype `0060e7b` and the v0.2 successor `fd0b34b`. Both commits and their historical review/audit records remain unchanged. GPT inspected those artifacts and authored the v0.3 rewrite on `gpt/b1-v06-intake-repair-2026-11-23`. Claude agreed to the correction approach and its conditions before implementation in the 2026-11-23 conversation. That was approach agreement only; it was not a code review or PASS. No GitHub action is attributed to Claude.

### 37.2 Work and repository references

The successor branch is three commits ahead of the HY4 v0.2 parent:
- `da1f41fc8a902be01b42257e028f8ad974952905`: GPT v0.3 validator, exact schema package, sidecar schema, tests, requirements and documentation.
- `9caf82819887975e2f03951af58e87f256a369a6`: explicit literal assertion of the reviewed source schema blob in the test suite and a more precise local test limitation.
- `b31c14c4b6f3e99fffc3a72f2609e6bda53927f1`: new Claude review packet.

Draft PR #10 is at https://github.com/foued2/failure-concentration-study/pull/10. Its base is the v0.2 predecessor branch, not master, to isolate the GPT changes from inherited unrelated branch history. It is draft and unmerged. Master is unchanged.

### 37.3 Technical changes

The validator packages and runtime-pins the exact reviewed B1 v1.7 schema draft 0.6 (source commit `f19e2a0ba09f2161f290558da5f61abc9d3ab52a`, blob SHA-1 `0f2865e606fa61400184c09abd01601497637a6b)). It applies Draft 2020-12 validation and explicit local semantic checks. It rejects unknown fields throughout schema-constrained objects, enforces the seven status-decision fields including the two false consultation flags, and rejects null/malformed required digests and evidence references.

The v0.6 schema does not define `f`, `u` or `p` as manifest fields. They are optional assertions in a separate sidecar whose schema blob is pinned at `72fc746c3d6129534aeb2fdbcd866842865f98c7`. The sidecar binds to the raw manifest SHA-256 and sidecar schema blob identity; it cannot alter the manifest decision. Mismatch and malformed reasons are `AGGREGATE_MISMATCH` and `MALFORMED_AGGREGATE`.

C_D is implemented from the measurement specification (2026-11-19) §1, which quotes Rev 11 lines 216–221, and §5. Unresolved outcomes are excluded. Only VALID variants receive complete derived counts, exact cell and C_D. INCOMPLETE data is provisional only and produces no full cell/C_D. INVALID, EXCLUDED_BEFORE_DIAGNOSTICS and EXPECTED_NOT_RUN produce no measurement counts or cell; this corrects v0.2's false-zero cells.

The report explicitly states that bank membership, source provenance, frozen inventory coverage, q registry, family map, per-variant run ledger, historical exposure evidence and other external checks were not performed. The exact label is `SYNTACTIC INTAKE ONLY — PROVENANCE NOT VERIFIED`.

### 37.4 Test limitation and review gate

There are 59 synthetic test methods. The local run recorded 59 passing after temporarily pinning the local validator/test to a locally reconstructed schema file. That file was 7 bytes shorter than the reviewed source, and equivalence was not established. The local result is not an exact-schema run. The branch contains the exact official schema blob, the code pins it, and the test asserts the literal official hash. Claude is requested to independently execute the tests against the exact committed schema and give an explicit PASS or NOT PASS.

PR #10 and the new review packet must remain unmerged pending Claude's independent review. A code PASS would not itself constitute owner freeze or authorization for bank/solver/diagnostic/census work.

### 37.5 Effect

No real manifest was admitted or validated. No bank access, parent acquisition, mutation allocation, solver construction or execution, diagnostics, census, outcomes, fitting or predictive analysis occurred. Gate 1 preflight remains **BLOCKED / NOT ASSESSABLE**; `P` remains **UNPROVEN**. The earlier conditional census-authorization interpretation remains unanswered. No verdict in §§1–36 changes.
