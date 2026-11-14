# B1/M1 joint-incidence feasibility specification (symbolic) — Rev 1.3

**Date:** 2026-11-14
**Version:** 1.3 — targeted GPT adjudication draft following review of Rev 1.2; not accepted or frozen
**Prepared by:** GPT (adjudication draft based on GLM Rev 1.2)
**Review chain:** Rev 1.0–Rev 1.2 were archived unchanged on review branch `gpt/b1-m1-rev1.2-review-chain-2026-11-14`, commit `dbdc82984a9259aa6d731bc6a64224373d74673b`. GPT completed the Rev 1.2 adjudication on 2026-11-14 and prepared this targeted correction draft. Claude independent review of Rev 1.3 remains pending.
**Authorization basis:** bounded GO (design and mathematics only) — unchanged. This review draft and archival publication of Rev 1.0–Rev 1.2 do not constitute scientific acceptance or a protocol freeze. **Not authorized and not performed:** numerical probability evaluation, executable simulation, Monte Carlo, solver construction, mutation allocation for real bodies, generator execution, bank reuse, or predictive fitting.
**Predecessors:** v1.0, Rev 1.1, and Rev 1.2 retained unmodified as reviewed artifacts.

---

## 0. Revision log (Rev 1.2 → Rev 1.3)

| # | Rev 1.2 finding | Disposition in this draft |
|---|---|---|
| R1 | §3.2 gives the correct cell-envelope formula, but its proof establishes only a maximum no greater than \(M\), not an allocation with maximum exactly \(M\) | Replace the proof with an explicit failure-vector construction and a separate capacity-slack construction for unresolved outcomes |
| R2 | §2.5 parent effects are common stratum offsets. Conditional on exact \((k,\ell)\), their factors cancel and cannot create within-cell placement confounding | Add centered, stratum-varying parent loadings. N3 uses a nonconstant failure-placement loading coupled to held-out parent quality; a common intercept alone is not treated as N3 |
| R3 | §7.1 does not fully inherit §2.5's parent-specific baseline odds; \(\delta\) is overloaded as both identity shape and affinity penalty | Separate baseline shapes \(b^F,b^U\) from affinity penalties \(\Delta^F,\Delta^U\), and define the affinity path directly on the multinomial log-odds |
| R4 | P-assoc is an association test, not the recorded held-out predictive target; B1 support alone does not guarantee fold-level slope estimability | Make P-pred the sole primary B1 procedure and P-assoc secondary. Define record-level scoring, equal-parent aggregation, training-fold within-cell variation, common scored sets, and extrapolation reporting |
| R5 | Family and identity labels are inserted as scalar arithmetic terms in the truth model | Use categorical effects with predeclared reference or sum-to-zero contrasts; labels are not ordinal covariates |
| R6 | \(\lambda=0\) is called flat although baseline propensities may vary by stratum | Rename it the zero-added-affinity/base-propensity reference and state the extra restrictions for N1's identity-flat control |
| R7 | The argmin set suppresses its dependence on the exact penalty profiles; the generic tie statement is too broad | Index the set by the penalty profiles, require exact regime comparison, and qualify the perturbation claim to full-dimensional perturbations not constrained to preserve ties |
| R8 | The grouped binomial outcome model ignores shared record difficulty across versions evaluated on the same fixed bank | Use per-record correctness as the primary predictive outcome; retain version-level correct counts as descriptive summaries and grouped-binomial analysis only as a labelled sensitivity |
| R9 | Both P-assoc and P-pred were assigned primary alpha conventions | One primary inferential target only: P-pred. P-assoc is secondary and not a second unadjusted confirmatory test |

**Retained from Rev 1.2:** the diverging \(\lambda\)-path; set-valued strong-affinity limit; regime (D)/(T) distinction; M1-si/M1-ci decomposition; corrected envelope formula; multinomial baseline-category probabilities; M1-gen authority caveat; population-versus-conditional weighting; finite-sum/tractability distinction; and the no-execution boundary.
---

## 1. Population structure and held-out outcome unit

§1.1–§1.3 of Rev 1.1 stand as written (symbolic objects; retired allocation not inherited; \(S=8\), \(R_s=8\); \(M(v)=\max_s f_s(v)\), and \(C_D(v)=M(v)/k(v)\) for \(k\ge1\), undefined at \(k=0\)).

**Primary held-out outcome unit (clarified):** per-record correctness \(Y_{v,r}\in\{0,1\}\) for mutant version \(v\) on canonical development record \(r\in\{1,\dots,78\}\). The version-level count \(h_v=\sum_{r=1}^{78}Y_{v,r}\) and mean \(Q_v=h_v/78\) are descriptive summaries, not the primary likelihood unit. The same fixed, publicly exposed 78-record bank is used across versions; it is development data, never sealed. The primary estimand is performance on this fixed bank, not generalization to new records.
---

## 2. Probability model

### 2.1–2.4 — unchanged in substance

Independent reference per version (§2.1 boundary conventions stand); Fisher-type conditional law §2.2; explicit unconditional law §2.3 (population vs conditional distinction stands); no truncation §2.4. Under the parent-effect benchmark, §2.2 uses parent-indexed odds \(\alpha_{g,q,s},\beta_{g,q,s}\), conditional on \((\theta_g,\varphi_g)\); population probabilities are then mixed over these effects.

### 2.5 Parent-effect model — conditional placement dependence made explicit

For the correlated benchmark, let mutant version \(v\) have parent \(g=\operatorname{par}(v)\) and identity \(q=q(v)\). The independent reference is recovered by setting parent effects and stratum-varying loadings to zero. “Correct” is the reference category in a baseline-category multinomial logit. Define

\[
\begin{aligned}
\eta^F_{g,q,s}(\lambda)
&=\mu_s+b^F_{q,s}+\kappa_F\theta_g+\gamma^F_s\theta_g-\lambda\Delta^F_{q,s},\\
\eta^U_{g,q,s}(\lambda)
&=\nu_s+b^U_{q,s}+\kappa_U\varphi_g+\gamma^U_s\varphi_g-\lambda\Delta^U_{q,s}.
\end{aligned}
\]

The diagnostic odds and probabilities are

\[
\alpha_{g,q,s}(\lambda)=e^{\eta^F_{g,q,s}(\lambda)},\qquad
\beta_{g,q,s}(\lambda)=e^{\eta^U_{g,q,s}(\lambda)},
\]
\[
p^{\mathrm{corr}}_{g,q,s}=\frac{1}{1+\alpha_{g,q,s}+\beta_{g,q,s}},\quad
p^{\mathrm{fail}}_{g,q,s}=\alpha_{g,q,s}p^{\mathrm{corr}}_{g,q,s},\quad
p^{\mathrm{unres}}_{g,q,s}=\beta_{g,q,s}p^{\mathrm{corr}}_{g,q,s}.
\]

This is a valid three-category distribution by construction and its odds are exactly those used in §2.2. The identity baseline shapes \(b^F_{q,s},b^U_{q,s}\) are distinct from the nonnegative affinity penalties \(\Delta^F_{q,s},\Delta^U_{q,s}\). The affinity penalties are shared across parents for a given identity; parent effects alter the base odds, not the identity's declared penalty regime.

**Parent effects:**

\[
(\theta_g,\varphi_g)\stackrel{\mathrm{iid}}{\sim}\mathcal N(0,\Sigma),\qquad
\Sigma=\begin{pmatrix}\sigma_\theta^2&\sigma_{\theta\varphi}\\\sigma_{\theta\varphi}&\sigma_\varphi^2\end{pmatrix}.
\]

Require \(\Sigma\) positive semidefinite: \(\sigma_\theta^2\ge0\), \(\sigma_\varphi^2\ge0\), and \(\sigma_{\theta\varphi}^2\le\sigma_\theta^2\sigma_\varphi^2\). Effects are independent and identically distributed across parents (including across families in this benchmark) and shared across all mutant versions of the same parent. The stratum loadings are centered, \(\sum_s\gamma^F_s=\sum_s\gamma^U_s=0\), to distinguish placement effects from common parent intercepts.

**Why the stratum loadings are necessary:** conditional on exact totals \((k,\ell)\), a common parent offset contributes the same multiplicative factor \(e^{\kappa_F\theta_g k+\kappa_U\varphi_g\ell}\) to every feasible table and cancels from the normalized conditional allocation law. Therefore \(\kappa_F\theta_g\) and \(\kappa_U\varphi_g\) alone affect cell-membership probabilities but do **not** confound within-cell \(C_D\). A nonconstant \(\gamma^F_s\theta_g\) (and, optionally, \(\gamma^U_s\varphi_g\)) varies across strata and survives conditioning on \((k,\ell)\); this is the parent-quality placement pathway used by N3.

**Dependence assumptions:** records are conditionally independent given the parent effects and version identity; versions are conditionally independent given their parent's shared effects; different parents' effects and outcomes are independent under this benchmark. Thus dependence among versions of one parent arises through shared \((\theta_g,\varphi_g)\). Population support probabilities mix conditional calculations over the declared bivariate Gaussian distribution by deterministic quadrature, with the quadrature rule and convergence tolerance predeclared at any later evaluation.

**Status:** this is a stylized random-effects benchmark. It is not evidence that independently developed solver implementations actually follow Gaussian random effects, common identity shapes, or these conditional-independence assumptions.
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

*Proof.* The universal bounds are \(M\le\min(k,8)\) and \(M\ge\lceil k/8\rceil\). Conversely, fix an integer \(M\) in this interval. Construct a failure vector by setting \(f_1=M\) and distributing the remaining \(k-M\) failures among strata 2–8, with each \(f_s\le M\). This is possible because \(k-M\le7M\), which follows from \(k\le8M\); also \(M\le8\), so every \(f_s\le8\). The constructed vector has \(\sum_s f_s=k\) and \(\max_s f_s=M\) exactly.

Now let \(D=64-\ell\). Since \(k+\ell\le64\), the required residual capacity \(D-k\) is an integer between 0 and \(64-k=\sum_s(8-f_s)\). Choose integers \(r_s\) with \(0\le r_s\le8-f_s\) and \(\sum_s r_s=D-k\), and set \(d_s=f_s+r_s\), \(u_s=8-d_s\). Then \(f_s\le d_s\le8\), \(\sum_s d_s=D\), and \(\sum_s u_s=\ell\). Thus this unresolved vector is admissible and the same failure allocation has maximum exactly \(M\). Every integer in the claimed interval is therefore attainable. \(\square\)

**Withdrawn:** the Rev 1.1 mini-example (which missed the \(c = (1,\dots,1)\) configuration: at \(k=5, \ell=56\), \(u = (7,\dots,7)\) is admissible and gives \(M = 1\), so \(C_D = 1/5\) is attainable) and the claim that the union "need not be an interval" — for this design it always is.

**Levels kept distinct (as required):** (1) fixed-\(u\) interval (§3.1) — conditional on one unresolved vector; (2) the **closed-form envelope** above — the set of \(M\)-values any cell \((k,\ell)\) could ever contain, a design diagnostic; (3) the probability-weighted distribution of \(u \mid \ell\) under §2.3, which is what realized support accounting uses. The prohibition on presenting a particular \(u\)'s capacity as the cell envelope stands.

---

## 4. Support conditions

§4.1 (B1 cell support), §4.2 (M1-gen with authority note and M1-si/M1-ci decomposition), §4.3 (intersection reported, never a gate), and §4.4 (incidence template) stand unchanged from Rev 1.1. §6 uses full-population B1 cells as the primary candidate sample, but fold-level estimability adds further requirements; B1 support alone is not a guarantee that a particular LOPO fit or score is estimable.

---

## 5. Exact support probabilities

§5.1, §5.2, §5.4, §5.5 — unchanged in substance (population-level targets; reduced statistic \(T_v = (q, Z, k, \ell, M)\); exact finite sum; tractability honesty; structural capacity facts).

### 5.3 Per-version DP recurrence — complexity statement corrected (GPT C4)

The recurrence itself stands (states \((k_s, \ell_s, M_s)\), transition over \((x,y)\), \(x + y \le 8\); output \(dp_8(k,\ell,M)\); marginal over \(M\) gives exact \(\Pr(k,\ell)\)). **Corrected bound:** after \(s\) strata, \(k_s \in [0, 8s]\), \(\ell_s \in [0, 8s]\), \(M_s \in \{0,\dots,8\}\), so the state count is at most \(9\,(8s+1)^2\); at \(s = 8\): \(9 \cdot 65^2 = 38{,}025\) states, at most 45 transitions each. Exact, trivially enumerable; no simulation, no truncation. (Rev 1.1's "\(9 \times 9 \times 9\)" was wrong.)

---

## 6. B1 analysis lane — two declared procedures (GPT C3)

### 6.1 P-pred (primary) and P-assoc (secondary)

The recorded B1 target is **incremental predictive information about held-out correctness beyond the exact baseline** \((q,Z,k,\ell)\). Therefore P-pred, not P-assoc, is the primary procedure. P-assoc is a secondary within-cell association analysis. Their results are never pooled.

**P-pred — primary held-out prediction procedure.**

- **Primary sample:** mutant-version records belonging to full-population cells with \(B1(c)=1\), where \(c=(q,Z,k,\ell)\), \(G_c\ge3\), \(D_c\ge2\), and \(k\ge2\). Versions in nonqualifying cells are not silently added to the primary B1 estimand; any broader all-population prediction is labelled secondary.
- **Outcome:** per-record correctness \(Y_{v,r}\in\{0,1\}\) on the same 78-record development bank. The version-level count \(h_v\) is derived for reporting only. A shared record effect is included because different versions are evaluated on the same fixed records.
- **Baseline model:**
\[
\operatorname{logit}\Pr(Y_{v,r}=1)=\alpha_{c(v)}+\omega_r.
\]
- **Enriched model:**
\[
\operatorname{logit}\Pr(Y_{v,r}=1)=\alpha_{c(v)}+\omega_r+\beta_C C_D(v).
\]
Here \(\alpha_c\) is the exact-cell intercept for \((q,Z,k,\ell)\), and \(\omega_r\) is a canonical-record effect shared across versions. The common \(\beta_C\) is the predeclared primary enrichment parameter; this imposes a common log-odds slope across eligible cells and must not be replaced after seeing outcomes. Reference/contrast coding for the item effects is fixed in advance. Both models are fitted on training parents only, using the same predeclared fitting/regularization procedure; any tuning is confined to the training fold and cannot use the outer test parent or its outcomes.
- **Fold-level enrichment estimability:** in each leave-one-parent-out (LOPO) training fold and each candidate cell, report \(G_c^{\mathrm{train}}\), \(D_c^{\mathrm{train}}\), and
\[
W_{C,c}^{\mathrm{train}}=\sum_{v\in c,\,\mathrm{train}}\left(C_D(v)-\overline C_{D,c}^{\mathrm{train}}\right)^2.
\]
A cell can contribute within-cell information to estimating \(\beta_C\) only when \(G_c^{\mathrm{train}}\ge2\), \(D_c^{\mathrm{train}}\ge2\), and \(W_{C,c}^{\mathrm{train}}>0\). Cell-intercept estimability alone is insufficient. Report separation, convergence, and the total across-cell training information \(\sum_cW_{C,c}^{\mathrm{train}}\). If the enriched slope is not estimable in a fold, the fold is flagged; it is not treated as a null effect.
- **Scored set:** for every outer test parent, list all candidate versions/records excluded because the exact cell is absent, the training cell lacks concentration variation, or the fit is not estimable. Baseline and enriched models must be scored on exactly the same test version-record rows. Report coverage by parent and cell. Flag any test \(C_D\) outside that cell's training range as extrapolation; report it separately and do not conceal it by dropping the row after seeing its outcome.
- **Primary score:** for model \(m\in\{0,1\}\) and test parent \(g\), compute mean per-record log loss over that parent's common scored set, \(L_{m,g}\). The primary statistic is
\[
\Delta LL=\frac{1}{|\mathcal G_{\mathrm{score}}|}\sum_{g\in\mathcal G_{\mathrm{score}}}(L_{0,g}-L_{1,g}),
\]
with equal weight per scored parent; positive values favour the enriched model. Define \(\mathcal G_{\mathrm{score}}=\{g:|\mathcal V_g^{\mathrm{score}}|>0\}\); parents with no eligible scored rows are excluded from this average but are counted and their exclusion reasons reported. If \(\mathcal V_g^{\mathrm{score}}\) is the parent’s common scored-version set and \(\mathcal R=\{1,\ldots,78\}\), then \(L_{m,g}=(|\mathcal V_g^{\mathrm{score}}||\mathcal R|)^{-1}\sum_{v\in\mathcal V_g^{\mathrm{score}}}\sum_{r\in\mathcal R}[-Y_{v,r}\log\widehat\pi^{(m)}_{v,r}-(1-Y_{v,r})\log(1-\widehat\pi^{(m)}_{v,r})]\). Report the paired parent-level differences and scored-set coverage.
- **Inference:** use one predeclared two-sided primary test at \(\alpha=0.05\). Because LOPO folds have overlapping training sets, a naive paired t-test treating fold scores as independent is not accepted. The parent-level uncertainty procedure, including refitting within each resample/permutation and handling unequal scored-parent coverage, must be specified in a separate B1 analysis plan before fitting or inspecting held-out outcomes. Until that procedure is frozen, \(\Delta LL\) is the primary descriptive estimand and no confirmatory p-value is claimed.

**P-assoc — secondary within-cell association analysis.** Use a conditional logistic/fixed-effect model with exact cell \(c=(q,Z,k,\ell)\) and canonical record \(r\) as the conditioning stratum, with \(C_D(v)\) as the varying covariate. The eligible exposure cells are exactly those satisfying \(B1(c)=1\). B1 support is an exposure-support prerequisite, not a guarantee that the conditional outcome likelihood contains information: each contributing \((c,r)\) stratum must contain outcome discordance across versions as well as within-cell \(C_D\) variation. Report cells/strata with no outcome discordance separately. P-assoc is secondary and does not answer the primary predictive target on its own; any inferential use is exploratory or requires an explicit multiplicity procedure.

**No pooling or silent fallback:** no support pooling across identities, families, or exact totals; no silent recoding of unseen levels; no substitution of a reduced baseline for the primary exact-cell baseline.
---

## 7. Anti-manufacturing controls — unified with the parent-effect model

### 7.1 Affinity path

For each identity \(q\), declare one failure anchor \(s^*(q)\) and one unresolved anchor \(t^*(q)\). Define penalty profiles with unique minima:

\[
\Delta^F_{q,s^*(q)}=0,\quad \Delta^F_{q,s}>0\ (s\ne s^*(q));\qquad
\Delta^U_{q,t^*(q)}=0,\quad \Delta^U_{q,s}>0\ (s\ne t^*(q)).
\]

Any within-class ordering among non-anchor strata is also declared exactly. These penalty profiles are distinct from the baseline identity shapes \(b^F,b^U\) in §2.5. The affinity path is

\[
\alpha_{g,q,s}(\lambda)=\alpha^\circ_{g,q,s}e^{-\lambda\Delta^F_{q,s}},\qquad
\beta_{g,q,s}(\lambda)=\beta^\circ_{g,q,s}e^{-\lambda\Delta^U_{q,s}},\qquad \lambda\in[0,\infty),
\]
where \(\alpha^\circ,\beta^\circ\) are the parent-specific base odds from §2.5 at \(\lambda=0\). Thus \(\lambda=0\) is the **zero-added-affinity/base-propensity reference**, not necessarily a flat or identity-independent propensity model. The strong-affinity limit is \(\lambda\to\infty\). Both aligned \((t^*=s^*)\) and crossed \((t^*\ne s^*)\) anchors are evaluated. The two anchor profiles and all free penalty values are declared before any evaluation.

### 7.2 Held-out correctness model and null scenarios

For version \(v\), parent \(g=\operatorname{par}(v)\), and canonical held-out record \(r\), define \(Y_{v,r}=1\) for a correct answer and 0 otherwise. A record-level truth model is

\[
\operatorname{logit}\Pr(Y_{v,r}=0)=a_0+a_k k(v)+a_\ell\ell(v)+A_Z[Z(g)]+A_Q[q(v)]+\omega_r+\theta_g+\beta_C C_D(v)\mathbf1\{k(v)\ge1\}+\beta_{u\to y}\xi_v.
\]

\(A_Z[\cdot]\) and \(A_Q[\cdot]\) are categorical fixed effects using predeclared reference or sum-to-zero contrasts; numeric category labels are never treated as ordinal covariates. \(\omega_r\) is a fixed canonical-record difficulty effect, with a declared contrast constraint. \(\theta_g\) is the parent-quality effect shared with the diagnostic model. The version summary \(h_v=\sum_rY_{v,r}\) is descriptive; because the 78 records have shared, potentially unequal difficulty across versions, it is not assumed to be an independent identically distributed binomial sample in the primary model.

The \(k=0\) convention is explicit: the \(C_D\) term is gated off when \(k=0\), where \(C_D\) is undefined. Such versions are outside B1/M1 support and outside the primary B1 scoring population; broader scoring is a separately labelled secondary analysis. For \(\ell\ge1\), \(\xi_v=u_{s^*(q)}(v)/\ell(v)\), the unresolved share in the identity's favoured failure stratum; set \(\xi_v=0\) for \(\ell=0\).

**Null scenarios (all have \(\beta_C=0\)):**

| ID | Configuration | What it tests |
|---|---|---|
| N1 | \(\lambda=0\); identity baseline shapes \(b^F_{q,s},b^U_{q,s}\) are constant across strata within each identity; \(\gamma^F=\gamma^U=0\); \(\beta_{u\to y}=0\) | Zero-added-affinity, identity-flat reference and primary false-positive behaviour under this declared DGP |
| N2 | \(\lambda\to\infty\), under the N1 parent-loading settings and with the exact per-cell regime audit in §7.3 | Identity-to-concentration confounding. Zero within-cell information is expected on regime-(D) cells; any persistent variation on regime-(T) cells is tie-dependent and flagged |
| N3 | Use the N1 settings except: at the zero-added-affinity reference, \(\operatorname{Var}(\theta_g)>0\), \(\theta_g\) enters held-out quality, and \(\gamma^F_s\) is nonconstant; optionally \(\gamma^U_s\) is nonconstant; \(\Sigma\) is declared | Parent-quality confounding that changes within-cell failure/unresolved placement. A common parent intercept alone is not N3 because it cancels after conditioning on \((k,\ell)\) |
| N4-a | Use the N1 settings at predeclared positive finite \(\lambda\) values, crossed anchors; \(\beta_{u\to y}=0\); other placement-confounding loadings disabled for this isolated control | There is no unresolved-placement pathway in this declared truth model. A \(C_D\) gain indicates leakage or model misspecification under the control, not automatically a data leak |
| N4-b | Use the N1 settings at predeclared positive finite \(\lambda\) values, crossed anchors; \(\beta_{u\to y}\ne0\) | Unresolved placement affects correctness. A \(C_D\) gain under \(\beta_C=0\) indicates that concentration proxies omitted unresolved-placement information, since the exact B1 cell conditions on total \(\ell\), not the vector \(u\) |

N3 robustness is a precondition for interpreting a positive B1 result. N4-a is an isolated model-control check; N4-b is a declared omitted-placement-confounding scenario. Anchor orientation has no effect at \(\lambda=0\), so N4-a/N4-b are evaluated only at predeclared positive affinity levels. These controls do not represent all possible solver populations.

### 7.3 Strong-affinity limit — set-valued proposition and exact regime audit

Fix identity \(q\), parent \(g\), and exact cell \((q,Z,k,\ell)\), with \(k\ge2\) and \(k+\ell\le64\). A feasible table is \(t=(x,y)\), with \(\sum_sx_s=k\), \(\sum_sy_s=\ell\), and \(x_s+y_s\le8\). Define

\[
\Phi_q(t;\Delta^F,\Delta^U)=\sum_s\left(x_s\Delta^F_{q,s}+y_s\Delta^U_{q,s}\right),\qquad
\Psi_q(k,\ell;\Delta^F,\Delta^U)=\operatorname*{arg\,min}_{t\text{ feasible}}\Phi_q(t;\Delta^F,\Delta^U).
\]

The parent-specific, \(\lambda\)-independent table weight is

\[
w_g^\circ(t)=\prod_s\frac{8!}{x_s!y_s!(8-x_s-y_s)!}(\alpha^\circ_{g,q,s})^{x_s}(\beta^\circ_{g,q,s})^{y_s}.
\]

**Proposition.**

1. **Limit support:** for each fixed parent-effect realization, as \(\lambda\to\infty\),
\[
\Pr(T=t\mid k,\ell,g)\longrightarrow
\frac{w_g^\circ(t)}{\sum_{t'\in\Psi_q}w_g^\circ(t')}\mathbf1\{t\in\Psi_q\}.
\]
The feasible set is finite and all base odds are positive. If the complement of \(\Psi_q\) is nonempty, its minimum positive penalty gap is strictly positive, so mass outside \(\Psi_q\) decays exponentially. If the complement is empty, the formula already gives the exact conditional law. Parent effects alter weights within \(\Psi_q\), but not the argmin set because the penalty profiles are shared across parents.

2. **Regime dichotomy:**
   - **Regime (D):** \(M(t)=\max_sx_s\) is constant on \(\Psi_q\). Then every parent carrying identity \(q\) in the same exact cell has the same limiting \(C_D=M^*/k\); thus \(D_c\to1\), the B1 witness disappears in that cell, and same-identity M1-si variation vanishes. The enriched model has zero limiting within-cell information from \(C_D\), because the predictor is constant within the exact baseline cell.
   - **Regime (T):** \(\Psi_q\) contains tables with at least two distinct \(M\)-values. Since every \(w_g^\circ(t)>0\), the limiting \(C_D\) distribution is non-degenerate for each parent; B1 and M1-si support may persist. Such support is dependent on exact ties in the declared penalty profiles. If those ties were imposed by the design, the resulting variation is **tie-manufactured** and is not evidence that untied or naturally occurring populations provide the variation.

3. **Exact regime audit:** for every relevant \((q,k,\ell)\), enumerate the finite feasible table set, calculate the argmin set using the exact declared \((\Delta^F,\Delta^U)\), and test whether \(M\) is constant on it. Audit exact symbolic/rational or otherwise comparison-safe penalty values, never rounded floating-point weights. The regime set is indexed by the penalty profiles, as written above.

4. **Tie perturbations:** for two distinct feasible tables, equality of their penalty objectives is a linear constraint in the free penalty coordinates. If the declared penalty family has a full-dimensional continuous perturbation distribution and the equality is not structurally forced by its constraints, that tie is broken with probability one. This generic statement does not apply to lower-dimensional or otherwise constrained families that preserve the equality; such families remain regime (T) and must be reported as such.

5. **Population consequence and M1:** if every candidate B1 cell is regime (D), the finite-cell union bound gives \(P(B1_{\mathrm{sup}})\to0\). If any candidate cell is regime (T), no population-wide vanishing claim is made; its contribution is separately measured and flagged. On regime-(D) cells M1-si vanishes while M1-ci may persist; on regime-(T) cells M1-si may also persist and is tie-dependent.

**Interpretation:** the anti-manufacturing guarantee is valid on regime-(D) cells only. Regime-(T) support is exposed by the exact penalty-regime audit and does not count as genuine feasibility evidence when the equality is design-imposed.
---

## 8. Hand-worked example — unchanged

Rev 1.1 §8 (\(k = 2, \ell = 0\)) remains valid; the closed-form envelope gives \(\mathcal{A}(2,0) = \{1, 2\}\), matching the example's \(C_D\) values \(\{1/2, 1\}\). Illustrative arithmetic only.

## 9. Reporting requirements for any future numerical evaluation

Any later evaluation, only after a separate explicit GO, must report:

1. \(P(B1_{\mathrm{sup}})\), \(P(M1\text{-gen}_{\mathrm{sup}})\), and \(P(\mathrm{Inter})\) separately, with population-level unconditional weighting; report the zero-added-affinity reference, the declared \(\lambda\) grid, and the analytic strong-affinity regime results.
2. The full incidence table and probability-weighted distribution of \(N_{B1}\), with all support failures retained and named; report M1-si and M1-ci separately.
3. The closed-form cell envelope \(\mathcal A(k,\ell)\) and the probability-weighted distribution of unresolved placement, keeping fixed-\(u\), cell-envelope, and probability-weighted quantities distinct.
4. The exact regime audit \(\Psi_q(k,\ell;\Delta^F,\Delta^U)\), \(|\Psi_q|\), M-constancy, regime (D)/(T), and share of support attributable to tie-dependent cells.
5. N1–N4 results, including the N3 stratum-varying parent loadings and the declared \(\Sigma\); report common-parent-intercept-only checks separately from true placement confounding.
6. P-pred primary \(\Delta LL\), equal-parent weighting, fold-level \(G_c^{\mathrm{train}}\), \(D_c^{\mathrm{train}}\), \(W_{C,c}^{\mathrm{train}}\), fit convergence/separation, scored-set coverage, common baseline/enriched test rows, and extrapolation flags.
7. P-assoc secondary outcome-discordance and exposure-variation requirements, with no second unadjusted confirmatory claim.
8. Record-level and version-summary outcome diagnostics; the development bank is fixed/publicly exposed and no new-record generalization claim is made.
9. The exact parent-level inferential procedure for overlapping LOPO folds and its predeclared assumptions before any predictive fitting.
10. A computational plan that demonstrates practical tractability of the finite support sums at the proposed design size; finiteness alone is not a tractability claim.

## 10. What this specification does not do

- No numerical evaluation beyond the hand-worked arithmetic example in §8; no simulation, Monte Carlo, solver construction, mutation allocation for real bodies, generator execution, bank reuse, or predictive fitting.
- No claim that the stylized Gaussian random-effects benchmark represents independently developed solver implementations; its adequacy is an open model-validity question.
- No population-wide anti-manufacturing conclusion in the presence of regime-(T) cells; their contribution must be separately reported and is not treated as genuine feasibility evidence when ties are imposed by design.
- No generalization from the fixed, publicly exposed 78-record development bank to unseen records.
- No resolution of the joint-consent provenance gap for the 2026-11-05 B1 decision record; the gap remains visible.
- No use of retired mutation catalogues, schedules, counts, or assignments as facts; no amendment of frozen blind E3.
- No numerical parameter values, effect sizes, power, or minimum-effect claims are invented by this specification.

## 11. Compliance map

| Requirement | Where |
|---|---|
| A. Symbolic population; retired allocations not inherited | §1 |
| B. B1 primary target is held-out prediction; P-assoc secondary; exact-cell baseline | §6 |
| C. B1/M1 support separate; intersection not a gate; population and conditional probabilities distinct | §4–§5 |
| D. Valid three-category multinomial model; parent dependence; no truncation | §2 |
| E. Unified affinity path; set-valued limit; D/T regime audit; N1–N4; N3 within-cell parent-quality pathway | §2.5, §7 |
| F. One two-sided primary inferential target; no unadjusted second confirmatory test | §6.1 |
| Correct cell-envelope formula with exact-maximum construction | §3.2 |
| DP recurrence and complexity bound | §5.3 |
| Fold-level within-cell slope estimability and equal-parent predictive scoring | §6 |
| M1-gen authority and M1-si/M1-ci decomposition | §4.2 |
| Held-out bank always identified as development data; consent-provenance gap visible | header, §1, §10 |

---

**End of Rev 1.3 draft.** This draft is not accepted or frozen. Claude's independent review is still pending. No numerical evaluation, predictive fitting, simulation, construction, allocation, or bank reuse is authorized. A separate explicit GO is required after the mathematics and the B1 analysis plan are accepted.
