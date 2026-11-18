# B1/M1 joint-incidence feasibility specification (symbolic) — Rev 1.2

**Date:** 2026-11-13
**Version:** 1.2 — targeted revision per GPT's adjudication of Rev 1.1 ("not accepted"; targeted Rev 1.2, not a rewrite)
**Prepared by:** GLM
**Review chain:** GPT adjudication 2026-11-12 of v1.0; Claude verification 2026-11-12 (confirmed §3 error, found §7.2 large-\(k\) error, verified corrected interval by exact enumeration); GPT adjudication 2026-11-13 of Rev 1.1 (two blocking mathematical errors in §7.1–§7.3; five further corrections).
**Authorization basis:** bounded GO (design and mathematics only) — unchanged. **Not authorized and not performed:** numerical probability evaluation, executable simulation, Monte Carlo, solver construction, mutation allocation for real bodies, generator execution, bank reuse, predictive fitting, repository publication. Untracked local draft.
**Predecessors:** v1.0 and Rev 1.1 retained unmodified as reviewed artifacts.

---

## 0. Revision log (Rev 1.1 → Rev 1.2)

| # | Finding (GPT, 2026-11-13) | Disposition in Rev 1.2 |
|---|---|---|
| B1 | **Affinity path does not diverge (blocking).** With \(\rho \in [0,1]\) and \(w = e^{-\rho\Delta}\), non-favoured weights tend to \(e^{-\Delta} > 0\), not 0; the claimed deterministic limit does not follow; the v1.1 proof is invalid | §7.1 repaired: concentration parameter \(\lambda \in [0,\infty)\), weights \(e^{-\lambda\Delta}\); the \(\rho\)-path and the v1.1 proof are **withdrawn**; §7.3 proposition rebuilt with a correct gap argument |
| B2 | **Joint maximizer not unique (blocking).** A1/A2 order the two classes separately; the joint allocation can have multiple maximizers with different \(M\) (example: \(k=2,\ \ell=7\), aligned anchors, equal second-stratum penalties) — and where that happens, within-cell \(C_D\) variation **persists in the limit**, so the anti-manufacturing conclusion fails there | §7.3 rebuilt as a **regime dichotomy**: the exact condition for the vanishing conclusion is \(M\)-constancy on the argmin set \(\Psi(q,k,\ell)\); regime (T) (tie) cells are a first-class case where support may persist, must be classified exactly per cell, and variation existing only in tie regimes is flagged as **tie-manufactured**; no global uniqueness assumption is asserted |
| C1 | §3.2 envelope miscomputed; full closed form \(\{\lceil k/8\rceil,\dots,\min(k,8)\}\); my \(\ell=56\) example wrong; "need not be an interval" wrong for this design | §3.2 replaced with the closed form **and a proof** (attainability via \(\min(64-\ell,\ 8M) \ge k\)); the v1.1 example and the non-interval caveat are withdrawn |
| C2 | §2.5 incomplete: two independent logits may give \(p_F + p_U > 1\); random-effect distribution undeclared; dependence assumptions implicit | §2.5 rebuilt: baseline-category multinomial logit (exact odds alignment with §2.2), declared bivariate Gaussian \((\theta_g,\varphi_g)\) with covariance and explicit conditional-independence assumptions; relabelled a **stylized random-effects benchmark** |
| C3 | §6.1 not accepted: cell-inclusion rule (\(D_c \ge 2\)) conflicts with B1 support (\(G_c \ge 3 \wedge D_c \ge 2\)); conditional logistic is an association test, not a calibrated prediction procedure | §6.1 rebuilt as **two declared procedures**: P-assoc (primary, eligibility exactly \(B1(c)=1\)) and P-pred (calibrated binomial prediction with cell intercepts); fold-level reporting extended to parent support (§6.2) |
| C4 | §5.3 state-space bound wrong (\(9\times9\times9\) per stratum) | §5.3 corrected: \(\le 9\,(8s+1)^2\) states after \(s\) strata; \(9 \cdot 65^2 = 38{,}025\) at \(s = 8\) |
| C5 | Truth model does not handle \(k = 0\) (\(C_D\) undefined); N4 lacks a pathway from unresolved placement to held-out correctness | §7.2: explicit \(k=0\) convention (\(C_D\)-term gated by \(1\{k \ge 1\}\), labelled alternative); N4 split into N4-a (no pathway) and N4-b (declared placement pathway \(\xi_v\) with \(\beta_{u\to y} \ne 0\)) |

**Retained unchanged (GPT's "what survives" list):** B1/M1-gen separation and intersection-not-gate; the M1-si/M1-ci split; M1-gen's explicit not-inherited status; the population-vs-conditional probability distinction and the finite-sum/tractability distinction; the no-execution rule.

---

## 1. Population structure — unchanged from Rev 1.1

§1.1–§1.4 of Rev 1.1 stand as written (symbolic objects; retired allocation not inherited; \(S=8\), \(R_s = 8\); \(M(v) = \max_s f_s(v)\), \(C_D(v) = M(v)/k(v)\) for \(k \ge 1\), undefined at \(k=0\); primary held-out outcome unit = version-level binomial \((h_v, n_h)\), \(n_h = 78\), development data, never sealed).

---

## 2. Probability model

### 2.1–2.4 — unchanged in substance

Independent reference per version (§2.1 boundary conventions stand); Fisher-type conditional law §2.2; explicit unconditional law §2.3 (population vs conditional distinction stands); no truncation §2.4.

### 2.5 Parent-effect model — completed (GPT C2)

**Parameterization (baseline-category multinomial logit; replaces Rev 1.1's two independent logits, which could violate \(p_F + p_U \le 1\)):** for version \(v\) (identity \(q(v)\), parent \(g = \mathrm{par}(v)\)) and stratum \(s\), with corrected baseline "correct":

\[
\log\frac{p^{\mathrm{fail}}_{v,s}}{p^{\mathrm{corr}}_{v,s}} = \eta^{F}_{v,s} = \mu_s + c_\theta\,\theta_g + \delta_{q,s},
\qquad
\log\frac{p^{\mathrm{unres}}_{v,s}}{p^{\mathrm{corr}}_{v,s}} = \eta^{U}_{v,s} = \nu_s + c^{u}_\theta\,\varphi_g + \omega_{q,s},
\]

\[
p^{\mathrm{corr}}_{v,s} = \frac{1}{1 + e^{\eta^F_{v,s}} + e^{\eta^U_{v,s}}},\qquad
p^{\mathrm{fail}}_{v,s} = e^{\eta^F_{v,s}} p^{\mathrm{corr}}_{v,s},\qquad
p^{\mathrm{unres}}_{v,s} = e^{\eta^U_{v,s}} p^{\mathrm{corr}}_{v,s}.
\]

This is valid by construction (\(p_F + p_U + p_C = 1\)) and aligns **exactly** with the §2.2 odds: \(\alpha_{v,s} = p^F/p^C = e^{\eta^F_{v,s}}\), \(\beta_{v,s} = e^{\eta^U_{v,s}}\). The confounding coupling \(c_\theta\) is nonzero only in null scenario N3.

**Random-effect distribution (declared):** \((\theta_g, \varphi_g) \sim \mathcal{N}(0, \Sigma)\) i.i.d. across parents, with \(\Sigma = \begin{pmatrix} \sigma^2_\theta & \sigma_{\theta\varphi} \\ \sigma_{\theta\varphi} & \sigma^2_\varphi \end{pmatrix}\) symbolic; shared across all of a parent's versions.

**Dependence assumptions (explicit):** (i) record outcomes are conditionally independent given \((\theta_g, \varphi_g, q(v))\); (ii) versions are conditionally independent given their parents' effects; (iii) hence same-parent version dependence arises **only** through the shared effects. Mixing over effects uses deterministic Gauss–Hermite quadrature with a node count declared at evaluation time (not Monte Carlo).

**Status label (GPT's position, adopted):** §2.5 is a **stylized random-effects benchmark** — a fully specified hierarchical framework, whose adequacy as a representation of independently developed solver implementations is a separate validity question and is **not** claimed as established.

---

## 3. Capacity and attainable \(C_D\) values

### 3.1 Fixed-\(u\) interval lemma — unchanged

Rev 1.1 §3.1 stands (Claude's exact-enumeration verification remains on record).

### 3.2 Cell envelope — corrected to the closed form (GPT C1)

**Claim.** For every realizable pair \(k \ge 1,\ \ell \ge 0\) with \(k + \ell \le 64\):

\[
\boxed{\ \mathcal{A}(k,\ell) = \Big\{ \lceil k/8 \rceil,\ \dots,\ \min(k,8) \Big\}\ }
\]

— a full integer interval, for the \(8 \times 8\) design.

*Proof.* Universal bounds: \(M \le \min(k, 8)\) (no stratum exceeds 8 failures or the total) and \(M \ge \lceil k/8 \rceil\) (8 strata must absorb \(k\) failures), independently of \(u\). Attainability of each \(M\) in the interval: write \(d_s = c_s = 8 - u_s\), so \(\sum_s d_s = 64 - \ell =: D\). An allocation with \(\max_s f_s \le M\) exists under capacity vector \(d\) iff \(\sum_s \min(d_s, M) \ge k\); maximizing the left side over admissible \(d\) (sum \(D\), \(0 \le d_s \le 8\)) gives exactly \(\min(D,\ 8M)\) (spread \(d\) evenly with \(d_s \le M\) while capacity remains). Hence a \(u\)-configuration admitting max exactly \(M\) exists iff \(\min(D, 8M) \ge k\). For every \(M \in [\lceil k/8\rceil, \min(k,8)]\): \(8M \ge k\) (by \(M \ge \lceil k/8 \rceil\)) and \(D = 64 - \ell \ge k\) (realizability), so the condition holds. \(\square\)

**Withdrawn:** the Rev 1.1 mini-example (which missed the \(c = (1,\dots,1)\) configuration: at \(k=5, \ell=56\), \(u = (7,\dots,7)\) is admissible and gives \(M = 1\), so \(C_D = 1/5\) is attainable) and the claim that the union "need not be an interval" — for this design it always is.

**Levels kept distinct (as required):** (1) fixed-\(u\) interval (§3.1) — conditional on one unresolved vector; (2) the **closed-form envelope** above — the set of \(M\)-values any cell \((k,\ell)\) could ever contain, a design diagnostic; (3) the probability-weighted distribution of \(u \mid \ell\) under §2.3, which is what realized support accounting uses. The prohibition on presenting a particular \(u\)'s capacity as the cell envelope stands.

---

## 4. Support conditions

§4.1 (B1 cell support), §4.2 (M1-gen with authority note and M1-si/M1-ci decomposition), §4.3 (intersection reported, never a gate), §4.4 (incidence template) — unchanged from Rev 1.1, with one addition: the analysis-eligibility alignment of §6.1 (below) makes "B1 support = primary-analysis eligibility" literal, removing the mismatch GPT identified.

---

## 5. Exact support probabilities

§5.1, §5.2, §5.4, §5.5 — unchanged in substance (population-level targets; reduced statistic \(T_v = (q, Z, k, \ell, M)\); exact finite sum; tractability honesty; structural capacity facts).

### 5.3 Per-version DP recurrence — complexity statement corrected (GPT C4)

The recurrence itself stands (states \((k_s, \ell_s, M_s)\), transition over \((x,y)\), \(x + y \le 8\); output \(dp_8(k,\ell,M)\); marginal over \(M\) gives exact \(\Pr(k,\ell)\)). **Corrected bound:** after \(s\) strata, \(k_s \in [0, 8s]\), \(\ell_s \in [0, 8s]\), \(M_s \in \{0,\dots,8\}\), so the state count is at most \(9\,(8s+1)^2\); at \(s = 8\): \(9 \cdot 65^2 = 38{,}025\) states, at most 45 transitions each. Exact, trivially enumerable; no simulation, no truncation. (Rev 1.1's "\(9 \times 9 \times 9\)" was wrong.)

---

## 6. B1 analysis lane — two declared procedures (GPT C3)

### 6.1 P-assoc (primary) and P-pred (co-reported) — separated

Rev 1.1 conflated association testing with calibrated prediction. Rev 1.2 declares two distinct procedures with distinct roles; results are reported side by side, **never pooled**.

**P-assoc — within-cell association test (primary scientific test of the B1 estimand).**

- **Sample rule (mismatch repaired):** the analysis sample consists **exactly** of the cells with \(B1(c) = 1\), i.e. \(G_c \ge 3\) **and** \(D_c \ge 2\). Cells with \(D_c \ge 2\) but \(G_c < 3\) are **analysis-ineligible** and are listed in the incidence report as failing the B1 parent-count condition — never silently included. (Rev 1.1's \(D_c \ge 2\)-only rule is withdrawn.) "B1 support = primary-analysis eligibility" is now literally true.
- **Model:** conditional logistic regression stratified by the exact cell \((q, Z, k, \ell)\), covariate \(C_D\); the conditioning removes cell intercepts and absorbs the full joint cell structure by construction.
- **What it licenses:** a test of within-cell incremental association of \(C_D\) with held-out correctness (the B1 estimand), two-sided \(\alpha = 0.05\). **It does not by itself produce calibrated per-version probabilities** — that is P-pred's role.

**P-pred — calibrated prediction procedure (co-reported; decision-relevant).**

- **Model:** \(h_v \sim \mathrm{Binomial}(n_h, 1 - p_v)\) with
\[
\text{Baseline: } \operatorname{logit}(p_v) = \alpha_c, \qquad
\text{Enriched: } \operatorname{logit}(p_v) = \alpha_c + \beta_C\, C_D(v), \qquad c = (q, Z, k, \ell),
\]
cell intercepts fitted on **training parents only**.
- **Scoring:** grouped binomial deviance / log-loss on held-out versions; concordance as labelled secondary.
- **Fold rules:** a cell intercept is fold-estimable iff the training fold contains \(\ge 1\) version of that cell and the fit is non-separated; estimability is reported per fold. Predictions for cells absent from training are **listed and excluded from the scored set with the exclusion named** — never silently scored or dropped.

**Primary convention:** two-sided \(\alpha = 0.05\) for each procedure's predeclared paired comparison across grouped folds; one-sided results only as labelled sensitivity (v1.0 §6.3 stands; no invented effect size; no power from retired figures).

### 6.2 Validation and integrity rules (extended per GPT)

1. **LOPO:** for every split and every cell, report \(G_c^{\text{train}}\) (**training-fold parent support** — new, per GPT) and \(D_c^{\text{train}}\); full-population support does not imply fold-level estimability.
2. **LOFO:** under the exact-cell procedures the held-out family's levels are absent from training; results are reported only under the explicitly labelled reduced-form fallback and **must not be presented as validation of the family-conditional B1 estimand** (label strengthened per GPT).
3. **Unseen levels:** named and reported; no silent recoding or dropping.
4. **Identity coverage**, **support-failure listing**, **frozen blind E3 untouched** — unchanged (Rev 1.1 §6.2).

---

## 7. Anti-manufacturing controls — repaired

### 7.1 Affinity path — corrected to a genuinely diverging family (GPT B1)

Rev 1.1's \(\rho \in [0,1]\) path and its proof are **withdrawn**: \(e^{-\rho\Delta} \to e^{-\Delta} \ne 0\), so no concentration occurs. Declared path: for identity \(q\), anchors \(s^*(q)\) (failures) and \(t^*(q)\) (unresolved), strictly ordered gaps \(\delta_{q,s} \ge 0\), \(\varepsilon_{q,s} \ge 0\) (zero at the respective anchors), and a **concentration parameter \(\lambda \in [0, \infty)\)**:

\[
\alpha_{q,s}(\lambda) = \alpha^{\circ}_{q,s}\, e^{-\lambda \delta_{q,s}},
\qquad
\beta_{q,s}(\lambda) = \beta^{\circ}_{q,s}\, e^{-\lambda \varepsilon_{q,s}} .
\]

Flat reference: \(\lambda = 0\). Strong-affinity limit: \(\lambda \to \infty\), where non-favoured odds genuinely vanish. Reporting is on a finite \(\lambda\)-grid, with the limit treated analytically (§7.3). Aligned (\(t^* = s^*\)) and crossed (\(t^* \ne s^*\)) anchor configurations both declared, as before.

### 7.2 Truth model — \(k=0\) convention and the N4 pathway (GPT C5)

For version \(v\), \(h_v \sim \mathrm{Binomial}(n_h, 1 - \pi_v)\), record-level

\[
\operatorname{logit}\big(\Pr(\text{incorrect})\big) = a_0 + a_k k(v) + a_\ell \ell(v) + a_Z Z(v) + a_q q(v) + \theta_{\mathrm{par}(v)} + \beta_C\, C_D(v)\,\mathbf{1}\{k(v) \ge 1\} + \beta_{u\to y}\, \xi_v .
\]

- **\(k = 0\) convention (declared):** the \(C_D\) term is gated off for \(k = 0\) versions (where \(C_D\) is undefined); these versions remain in the population, contribute to no B1/M1 cell, and are scored in P-pred. A labelled alternative convention (separate \(k=0\) intercept) is a declared sensitivity.
- **Placement statistic:** \(\xi_v = u_{s^*(q)}(v)/\ell(v)\) for \(\ell \ge 1\) (share of unresolved outcomes in the identity's favoured failure stratum), \(\xi_v = 0\) for \(\ell = 0\).
- **Null scenarios (all \(\beta_C = 0\); each global and, where defined, within identity strata):**

| ID | Configuration | What it tests |
|---|---|---|
| N1 | flat (\(\lambda = 0\)), \(c_\theta = 0\), \(\beta_{u\to y} = 0\) | Basic false-positive behaviour (nominal \(\alpha\)) |
| N2 | strong affinity (\(\lambda \to \infty\)) | Identity-to-concentration confounding. **Update per §7.3:** the exactly-zero-gain expectation holds on regime-(D) cells; the evaluation must include the per-cell regime audit, and any gain attributable to regime-(T) cells is flagged as tie-manufactured |
| N3 | \(c_\theta \ne 0\) | Parent-quality confounding; robustness to N3 is a declared precondition for interpreting any positive B1 finding |
| N4-a | crossed anchors, \(\beta_{u\to y} = 0\) | Pure diagnostic co-location control: any detected C_D gain indicates a leak (there is no pathway from unresolved placement to correctness) |
| N4-b | crossed anchors, \(\beta_{u\to y} \ne 0\) | **Confounding pathway (new):** unresolved placement genuinely affects correctness; a C_D gain under \(\beta_C = 0\) shows the lane picks up unresolved-placement information through \(C_D\) — which the exact-cell baseline cannot absorb (it conditions on total \(\ell\), not the placement vector) |

### 7.3 Strong-affinity limit — corrected proposition (replaces Rev 1.1 §7.3 entirely)

Fix an identity \(q\) and a cell \((q, Z, k, \ell)\), \(k \ge 2\), \(k + \ell \le 64\), under the §7.1 path with the §2.5 benchmark propensities (interior for finite \(\lambda\)). Define

\[
\Phi(t) = \sum_{s} \big( x_s\,\delta_{q,s} + y_s\,\varepsilon_{q,s} \big),
\qquad
\Psi(q,k,\ell) = \operatorname*{arg\,min}_{(x,y)\ \mathrm{feasible}} \Phi ,
\]

over feasible tables \((\sum x_s = k,\ \sum y_s = \ell,\ x_s + y_s \le 8)\), and \(w^{\circ}(t) = \prod_s \frac{8!}{x_s!\,y_s!\,(8-x_s-y_s)!}\,(\alpha^{\circ}_{q,s})^{x_s} (\beta^{\circ}_{q,s})^{y_s}\) (the \(\lambda\)-independent weight).

**Proposition.**
1. **Limit support (general, all \(k\)):** as \(\lambda \to \infty\), the conditional table \((f,u) \mid (k,\ell)\) converges in distribution to the law concentrated on \(\Psi(q,k,\ell)\) with
\[
\Pr(T = t \mid k,\ell) \;\longrightarrow\; \frac{w^{\circ}(t)}{\sum_{t' \in \Psi} w^{\circ}(t')}\ \mathbf{1}\{t \in \Psi\} .
\]
*Proof:* the support is finite; every table outside \(\Psi\) has \(\Phi \ge \min\Phi + g\) with \(g > 0\) the minimal positive gap of \(\Phi\) over the finite table set, so its relative mass is \(O(e^{-\lambda g}) \to 0\); within \(\Psi\) the \(\lambda\)-dependent factors cancel, leaving weights proportional to \(w^{\circ}\). (Interior propensities keep \(w^\circ > 0\).) \(\square\)

2. **Regime dichotomy (replaces the v1.1 uniqueness claim):**
   - **Regime (D)** — \(M = \max_s x_s\) is **constant on \(\Psi\)** (in particular when \(\Psi\) is a singleton): then \(C_D \to M^*/k\) deterministically; \(D_c \to 1\), \(B1(c) \to 0\), and M1-si vanishes for this cell; the enriched model's conditional incremental information given the exact-cell baseline is **exactly zero**.
   - **Regime (T)** — \(\Psi\) contains tables with at least two distinct \(M\)-values (GPT's canonical example: \(k=2, \ell=7\), aligned anchors, equal second-stratum penalties; two argmin tables with \(M = 1\) and \(M = 2\)): then the limit of \(C_D\) is non-degenerate, and neither \(B1(c)\) nor M1-si need vanish. The persistent variation is a **knife-edge property of exact penalty ties**: any generic perturbation of \((\delta_q, \varepsilon_q)\) collapses the cell to regime (D). Variation that exists **only** in regime-(T) cells is flagged **tie-manufactured** and does not count as genuine feasibility evidence.

3. **No global uniqueness assumption is asserted.** Instead, the regime of every relevant cell is **exactly computable** — enumerate the finite feasible table set, compute \(\Phi\), extract \(\Psi\), check \(M\)-constancy — and this per-cell regime audit is a mandatory component of any future evaluation (§9). The Rev 1.1 assumptions (A1)–(A2) are retained only as gap-ordering inputs to \(\Phi\); the false uniqueness inference is withdrawn.

4. **Consequences:** on regime-(D) cells (and hence population-wide iff every cell containing a candidate B1 witness is in regime (D)): \(P(B1_{\mathrm{sup}}) \to 0\) as \(\lambda \to \infty\) (finite cell count, union bound). Population-wide conclusions in the presence of regime-(T) cells are **not claimed**; their contribution is measured and reported instead.

5. **M1-gen:** on regime-(D) cells, M1-si \(\to 0\) while M1-ci may persist (identity-driven, invisible to the B1 estimand) — Rev 1.1's part 5, now scoped per regime. On regime-(T) cells even M1-si may persist, by the same tie mechanism as B1; the M1-si/M1-ci decomposition plus the regime audit together determine what any realized M1-gen support is evidence of.

**Interpretation (anti-manufacturing guarantee, correctly scoped at last):** mechanism structure alone cannot create B1 support or within-cell stochastic variation **on regime-(D) cells**, at any \(k\); the guarantee's boundary is now mathematical (the tie regime), visible, exactly checkable per cell, and reported — rather than assumed away.

---

## 8. Hand-worked example — unchanged

Rev 1.1 §8 (\(k = 2, \ell = 0\)) remains valid; the closed-form envelope gives \(\mathcal{A}(2,0) = \{1, 2\}\), matching the example's \(C_D\) values \(\{1/2, 1\}\). Illustrative arithmetic only.

## 9. Reporting requirements for any future numeric evaluation (updated)

Adds to Rev 1.1 §9: (6) the **per-cell regime audit** — \(\Psi(q,k,\ell)\), \(|\Psi|\), \(M\)-constancy, regime (D)/(T) — for every cell, with the (T)-share reported; support attributable only to (T) cells flagged tie-manufactured; (7) the \(k=0\) convention and N4-a/N4-b results; (8) P-assoc and P-pred fold reports including training-fold parent support (\(G_c^{\text{train}}\)) and P-pred cell-intercept estimability and scored-set exclusions.

## 10. What this specification does not do

Rev 1.1 §10 stands, plus: no numerical evaluation beyond §8's hand arithmetic; the §2.5 benchmark's adequacy as a model of independent solver development is open and not claimed; no population-wide anti-manufacturing conclusion is asserted in the presence of regime-(T) cells.

## 11. Compliance map (updated)

| Requirement | Where |
|---|---|
| A. Symbolic population, nothing inherited | §1 |
| B. B1 analysis aligned to exact cell; association vs prediction separated; eligibility = \(B1(c)=1\) | §6.1 |
| C. Three probabilities separate; population vs conditional; finite-sum vs tractability | §4.3, §5 |
| D. Fisher vs Wallenius; valid multinomial parameterization; boundary conventions; no truncation | §2 |
| E. Repaired affinity path and regime-scoped strong-affinity proposition; N1–N4-a/b incl. \(k=0\) and placement pathway; correlated benchmark with declared distribution; fold-level parent-support reporting | §7, §2.5, §6.2 |
| F. Two-sided \(\alpha = 0.05\) primary; labelled sensitivity; no invented effect | §6.1 |
| Corrected cell envelope (closed form, proved) | §3.2 |
| Corrected DP complexity bound | §5.3 |
| M1-gen authority; M1-si/M1-ci; regime audit | §4.2, §7.3 |
| Held-out bank never sealed; consent-provenance gap visible | header, §1.4, §10 |

---

**End of Rev 1.2.** Per the recorded process: Claude reviews this revision independently; GPT challenges scientific coherence — in particular whether the regime-scoped §7.3 now establishes the no-manufacturing claim on its stated domain, and whether the completed §2.5 benchmark is defensible for feasibility conclusions. No numerical evaluation is authorized; that requires a further explicit GO after acceptance of the mathematics.
