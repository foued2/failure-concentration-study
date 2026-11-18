# B1/M1 joint-incidence feasibility specification (symbolic) — Rev 1.1

**Date:** 2026-11-12
**Version:** 1.1 — revision issued in response to GPT's adjudication (not accepted as final) and Claude's independent verification
**Prepared by:** GLM
**Review chain:** GPT adjudication 2026-11-12 (7-point Rev 1.1 instruction); Claude independent verification 2026-11-12 (confirmed §3 blocking error; found a second error in §7.2; verified the corrected capacity interval by exact enumeration on 200 random capacity vectors).
**Authorization basis:** bounded GO (design and mathematics only) — unchanged. **Not authorized and not performed:** numerical probability evaluation at scale, executable simulation, Monte Carlo, solver construction, mutation allocation for real bodies, generator execution, bank reuse, predictive fitting, repository publication. Untracked local draft.
**Predecessor:** `B1_M1_JOINT_INCIDENCE_FEASIBILITY_SPEC_2026-11-12.md` (v1.0), retained unmodified as the reviewed artifact.

---

## 0. Revision log (every blocking and required item, with disposition)

| # | Finding (source) | Disposition in Rev 1.1 |
|---|---|---|
| 1 | §3 capacity lemma wrong when unresolved outcomes consume per-stratum capacity (GPT §2; counterexample \(u=(8,\dots,8,0)\), \(k=5\); verified by Claude) | §3 rewritten: fixed-\(u\) interval lemma with proof; symbol \(m\) renamed to \(M\); three-level capacity distinction (fixed-\(u\) / cell envelope over \(\ell\) / probability-weighted); realizability condition \(k + \ell \le 64\) |
| 2 | §7.2 proposition false for \(k \ge 9\) as stated: \(C_D \le 8/k < 1\) (Claude, new finding) | §7.3 proposition restated under explicit assumptions via a lexicographic-dominance path: convergence to a deterministic table \(T^*(q,k,\ell)\) for **all** \(k\); conclusions 1–2 restricted and corrected; M1 claim decomposed (M1-si / M1-ci); large-\(k\) case now covered |
| 3 | Population model incomplete: no version-level dependence, no unconditional weighting (GPT §3) | §2.5 defines the correlated parent-effect population model (not merely named); §5 rewritten: explicit unconditional law, population vs conditional probabilities distinguished, per-version DP recurrence stated |
| 4 | Baseline model does not absorb the full joint cell \((q,Z,k,\ell)\); additive example could let \(C_D\) proxy omitted interactions (GPT §4) | §6.1 replaced: primary baseline is the exact-cell conditional (stratified) model, which operationalizes B1 support; reduced baselines only as declared, labelled fallbacks; the previously asserted phrase is now demonstrated by construction |
| 5 | Validation gaps: LOFO not directly estimable with family effects; LOPO may destroy within-cell variation (GPT §4) | §6.2: fold-level estimability reporting required, including per-split survival of training-fold within-cell \(C_D\) variation; declared reduced-form fallback for LOFO; unseen-level handling declared |
| 6 | Held-out generating model and \(\beta_C\) undefined; confounding not modeled (GPT §5) | §7.2: complete held-out outcome model with parent-quality effect \(\theta_g\); four explicit null scenarios (N1–N4) including parent-quality confounding and unresolved-stratum affinity |
| 7 | M1 generalization from 5 versions to \(V_g\) is an operational change without authority (GPT §6) | §4.2: rule renamed **M1-gen** throughout; historical five-version wording recorded as review-only provenance, not auto-authoritative |
| 8 | Smaller required clarifications (GPT §7): outcome unit, scoring, affinity formula, DP recurrence, symbol collision | §1.5 (outcome unit chosen), §6.1 (binomial log-loss/deviance), §7.1 (explicit affinity path formulas), §5.3 (DP state and recurrence), §3 (symbol rename) |

Items marked "Pass" in GPT's adjudication (symbolic architecture, B1/M1 separation, identity/category separation, no inheritance, intersection-not-gate, Fisher starting law with qualifications, held-out bank never sealed, no invented effect size) are retained unchanged except where a numbered item touches them.

---

## 1. Population structure (symbolic; nothing inherited)

### 1.1 Objects

| Symbol | Object | Constraints |
|---|---|---|
| \(g\) | independent parent implementation | \(g \in \{1,\dots,G\}\), \(G\) symbolic |
| \(Z(g)\) | parent family | \(Z(g) \in \mathcal{Z}\); \(n_Z\) symbolic per family |
| \(v\) | solver version | control \(S0(g)\) (outside all mutation strata) + mutants \(v \in \mathcal{V}(g)\), \(V_g = |\mathcal{V}(g)|\) symbolic, \(V_g \ge 2\) |
| \(q(v)\) | individual mutation identity | \(q(v) \in \mathcal{Q}\), \(Q\) symbolic; exactly one identity per mutant version |
| \(m(q)\) | broad mechanism category | symbolic; **no role in B1 cells**; bookkeeping only |
| \(a\) | assignment rule \((g,j) \mapsto q\) | declared design choice; nothing inherited |
| \(\theta_g\) | parent quality effect (latent) | introduced in Rev 1.1 (§7.2); enters both the diagnostic propensity model (in confounding scenarios) and the held-out outcome model |

Unchanged from v1.0: \(G\), \(\{n_Z\}\), \(\{V_g\}\), \(Q\), \(a\) are free design parameters; the retired eight-mechanism catalogue, 28+2 schedule, 90-version plan, and SA/SB/S-extra assignments are not used as facts (v1.0 §1.2 stands).

### 1.2 Diagnostic observation structure

\(S = 8\) strata, \(R_s = 8\) records per stratum (abstract structural constants; no bank data executed or reused). Per record: outcome class \(\in\) {correct, definite failure, unresolved}.

### 1.3 Version-level sufficient statistics

\[
f_s(v),\ u_s(v),\quad k(v) = \sum_s f_s(v),\quad \ell(v) = \sum_s u_s(v),
\]
\[
M(v) = \max_{s}\, f_s(v),\qquad C_D(v) = M(v)/k(v)\ \ (k(v) \ge 1).
\]

**Symbol note (GPT §7):** the maximum definite-failure count is now \(M\) (capital), because \(m\) denotes the broad mechanism category. \(C_D\) undefined at \(k = 0\); unresolved counts never enter \(C_D\).

### 1.4 Held-out outcome — unit now chosen (GPT §7)

**Primary outcome unit (declared):** version-level — \(h_v\) = number of correct answers among the \(n_h\) held-out development records (\(n_h\) = 78 unique canonical records of the fixed, publicly exposed held-out bank). The held-out bank is **development data; never sealed**. The per-record variant is a separately labelled sensitivity analysis, not the primary unit.

---

## 2. Probability model (complete, population-level)

### 2.1 Independent reference model (per version)

Given the version's identity \(q\) and parent effects (§2.5; zero in the reference model), each of the 64 diagnostic records independently takes class \(c \in \{\text{fail}, \text{unres}, \text{corr}\}\) with

\[
p^{\mathrm{fail}}_{q,s},\quad p^{\mathrm{unres}}_{q,s},\quad
p^{\mathrm{corr}}_{q,s} \;=\; 1 - p^{\mathrm{fail}}_{q,s} - p^{\mathrm{unres}}_{q,s} \;\ge\; 0 .
\]

**Boundary convention (GPT §3):** parameterizations with \(p^{\mathrm{corr}}_{q,s} = 0\) for any \((q,s)\) are **excluded from the declared reference grid** and any exclusion is reported (odds expressions with zero denominators are undefined; limiting cases are treated only as explicit limits, never silently). \(p^{\mathrm{fail}} + p^{\mathrm{unres}} \le 1\) is a parameter admissibility constraint checked before any evaluation.

### 2.2 Conditional law given exact totals (Fisher-type; unchanged in substance)

\[
\Pr\!\big((f,u) = (x,y) \,\big|\, k, \ell\big)
= \frac{\prod_{s} \dfrac{R_s!}{x_s!\,y_s!\,(R_s - x_s - y_s)!}\; \alpha_{q,s}^{\,x_s}\, \beta_{q,s}^{\,y_s}}{Z_{k,\ell}(\alpha_q, \beta_q)},
\]

\(\alpha_{q,s} = p^{\mathrm{fail}}_{q,s} / p^{\mathrm{corr}}_{q,s}\), \(\beta_{q,s} = p^{\mathrm{unres}}_{q,s} / p^{\mathrm{corr}}_{q,s}\). Fisher-type conditioning of independent categorical trials on two linear totals; Wallenius rejected for the reason recorded in v1.0 §2.2 (sequential depletion is a different generative process and would manufacture artifactual structure). Unresolved outcomes stay a separate exact coordinate.

### 2.3 Unconditional (population) law — now explicit (GPT §3, item 3)

Each version's outcome table has the **unconditional** probability

\[
\Pr\big((f,u) = (x,y)\big) \;=\; \prod_{s=1}^{8} \frac{R_s!}{x_s!\,y_s!\,(R_s - x_s - y_s)!}\,
\big(p^{\mathrm{fail}}_{q,s}\big)^{x_s} \big(p^{\mathrm{unres}}_{q,s}\big)^{y_s} \big(p^{\mathrm{corr}}_{q,s}\big)^{R_s - x_s - y_s},
\]

and \(\Pr\big((f,u) \mid k,\ell\big) = \Pr(f,u) / \Pr(k,\ell)\) factorizes accordingly. **All support probabilities in §5 are population-level (unconditional) probabilities computed with this weighting; the conditional law §2.2 is a building block, never a substitute for the unconditional weighting.** \(\Pr(k,\ell)\) itself is obtained exactly from the same per-version DP (§5.3).

### 2.4 No truncation

Exact normalization/summation throughout; arbitrary overflow truncation prohibited (v1.0 §2.4 stands).

### 2.5 Correlated parent/version model — now defined, not merely named (GPT §3, item 2; Claude)

The independent model is retained **only as the variation-optimistic reference**. The declared population model for any realistic feasibility claim is the parent-effect extension:

\[
\operatorname{logit}\big(p^{\mathrm{fail}}_{v,s}\big) = \mu_s + c_\theta\,\theta_{\mathrm{par}(v)} + \delta_{q(v),s},
\qquad
\operatorname{logit}\big(p^{\mathrm{unres}}_{v,s}\big) = \nu_s + \varphi_{\mathrm{par}(v)} + \omega_{q(v),s},
\]

with \(\theta_g, \varphi_g\) parent-level random effects (shared across all of a parent's versions — the source of same-parent dependence), identity shapes \(\delta_q, \omega_q\), and \(c_\theta\) the confounding coupling set to a nonzero value only in null scenario N3 (§7.2). Consequences declared:

1. Same-parent versions are **positively dependent** through \((\theta_g, \varphi_g)\); the §5 exact sums then hold conditionally on the parent effects and are mixed over their distribution (deterministic Gauss–Hermite quadrature with a declared node count — **not** Monte Carlo).
2. Same-parent positive dependence raises the probability that a parent's versions collide in the same exact cell \((k,\ell)\) — it changes \(P(\text{M1-gen})\) in both directions and must be reported, not assumed.
3. No feasibility conclusion is drawn from the independent reference alone (GPT's "defensible model of independently developed parent solvers" requirement).

---

## 3. Capacity and attainable \(C_D\) values (corrected)

### 3.1 Capacity conditional on a fixed unresolved vector

Fix a realized unresolved vector \(u = (u_1,\dots,u_8)\), \(0 \le u_s \le 8\), and let \(c_s = 8 - u_s\) be the **remaining failure capacity** of stratum \(s\). A failure allocation \(f\) is feasible iff \(0 \le f_s \le c_s\) and \(\sum_s f_s = k\), which requires

\[
k \;\le\; \sum_s c_s \;=\; 64 - \ell .
\]

Define, following GPT's correction:

\[
M_{\min}(u;k) = \min\Big\{ t \in \mathbb{Z}_{\ge 0} : \sum_s \min(c_s, t) \ge k \Big\},
\qquad
M_{\max}(u;k) = \min\big(k, \max_s c_s\big).
\]

**Lemma (corrected; replaces v1.0 §3).** If \(1 \le k \le \sum_s c_s\), the attainable values of \(M = \max_s f_s\) are exactly the integers

\[
\big[\, M_{\min}(u;k),\; M_{\max}(u;k) \,\big],
\]

and the attainable \(C_D\) values are \(\{ M/k : M \in [M_{\min}, M_{\max}] \}\), with \(A(u;k) = M_{\max} - M_{\min} + 1\) of them.

*Proof.* For any \(t\), an allocation with \(\max_s f_s \le t\) exists iff \(\sum_s \min(c_s, t) \ge k\) (greedy fill). Hence \(t \ge M_{\min}\) is necessary and sufficient for "max \(\le t\)", giving \(M \ge M_{\min}\); \(M \le \min(k, \max_s c_s) = M_{\max}\) is immediate. For attainment of each integer \(M \in [M_{\min}, M_{\max}]\): choose a stratum \(s_0\) with \(c_{s_0} \ge M\) (exists since \(M \le \max_s c_s\)), set \(f_{s_0} = M\), and fill the remaining \(k - M\) failures across other strata with per-stratum caps \(\min(c_s, M)\); total remaining capacity is \(\sum_s \min(c_s,M) - M \ge k - M\) (since \(M \ge M_{\min}\)), so the fill completes with max exactly \(M\). \(\square\)

*Independent verification:* Claude reproduced the interval by exact enumeration on 200 random capacity vectors with no violations (2026-11-12); GPT's counterexample is a special case: \(u = (8,8,8,8,8,8,8,0)\), \(k=5\): \(c = (0,\dots,0,8)\), \(M_{\min} = M_{\max} = 5\), so \(C_D = 1\) is the **only** attainable value — v1.0's lemma wrongly claimed five.

**Consequences (restated):** (i) no \(C_D\) variation at \(k = 1\) (\(M_{\min} = M_{\max} = 1\)); (ii) variation requires \(M_{\min} < M_{\max}\), i.e. spread capacity; (iii) \(C_D < 1\) is possible only when \(M_{\max} < k\), in particular \(C_D \le 8/k < 1\) for all \(k \ge 9\).

### 3.2 Capacity at the cell level: cells condition on \((k, \ell)\), not on \(u\) (GPT §2, subtlety)

A B1/M1 cell fixes only the totals \((k, \ell)\). The unresolved **distribution** across strata is random. Three distinct levels, never conflated:

1. **Fixed-\(u\) capacity** (§3.1): conditional on one particular unresolved vector. Used only when the \(u\)-vector is itself conditioned, which cells do **not** do.
2. **Cell envelope** (design-level diagnostic):
\[
\mathcal{A}(k,\ell) \;=\; \bigcup_{u\,:\,\sum_s u_s = \ell} \big[\, M_{\min}(u;k),\, M_{\max}(u;k) \,\big]
\]
over all unresolved compositions with total \(\ell\) (a finite set, enumerated exactly). The union need not be an interval in general; it is computed exactly, not asserted. *Mini-example (\(\ell = 56\), \(k = 5\)):* \(u = (8,8,8,8,8,8,8,0)\) gives \(\{5\}\); \(u = (8,8,8,8,8,8,6,2)\) gives \([3,5]\); the envelope is their union \(\{3,4,5\}\). The envelope bounds the number of distinct \(C_D\) values any cell \((k,\ell)\) could ever contain; it is a diagnostic, not a probability.
3. **Probability-weighted capacity:** the distribution of \(u \mid \ell\) under the law §2.3 (itself Fisher-type in the \(y\)-coordinates), which is what the realized support accounting in §5 uses.

**Prohibition (GPT):** inserting one particular unresolved vector into a capacity formula and presenting the result as the envelope for a cell defined only by \((k,\ell)\) is a specification violation.

### 3.3 Renaming

The maximum definite-failure count is \(M\) throughout (v1.0 used \(m\), which collided with the mechanism-category symbol).

---

## 4. Support conditions (separate; M1 authority clarified)

### 4.1 B1 cell support (unchanged from v1.0 §4.1)

For an exact cell \(c = (q, Z, k, \ell)\), \(k \ge 2\): \(B1(c) = 1\) iff \(G_c \ge 3\) (distinct parents) and \(D_c \ge 2\) (distinct observed \(C_D\)); no pooling across identities, families, or exact \((k,\ell)\); \(B1_{\mathrm{sup}} = 1\{\exists c\}\) with qualifying-cell count \(N_{B1}\) reported; incidence template per v1.0 §4.4 (failures listed, never dropped), now with the \(C_D\) column labelled by \(M/k\) values.

### 4.2 M1-gen (within-parent; authority clarified — GPT §6)

\[
M1\text{-gen}(e) = 1 \iff |\{g : \text{parent } g \text{ contributes } \ge 2 \text{ of its own versions to } e=(k,\ell),\ k \ge 2,\ \text{with different } C_D\}| \ge 3.
\]

**Authority note (recorded, not hidden):** the historical five-version M1 wording comes from the review-only analysis specification (C9/revision line) and was **not** ratified for a new symbolic population. Generalizing "two of the parent's five versions" to "\(\ge 2\) of the parent's \(V_g\) versions" is a **proposed operational change**, named **M1-gen** throughout this revision until its authority and intended scope are established by the review chain. It is not described as the unchanged frozen five-version rule anywhere.

**Decomposition (new; required by the §7.3 corrected proposition):** each qualifying (or near-qualifying) within-parent pair is classified as
- **M1-si:** the two versions share the same identity \(q\) — the \(C_D\) difference is stochastic placement variation, the kind that can carry within-cell information in the B1 lane;
- **M1-ci:** the versions carry different identities — the \(C_D\) difference may be identity-driven (deterministic under strong affinity) and is **invisible to the B1 estimand**, which conditions on \(q\).

The incidence report gives \(|\mathcal{G}_{\mathrm{si}}(e)|\) and \(|\mathcal{G}_{\mathrm{ci}}(e)|\) separately. Only the M1-si component is direct evidence relevant to B1's identification prerequisite; this is formalized in §7.3 (Proposition, part 5).

### 4.3 Intersection — reported, never a gate (unchanged)

\(\mathrm{Inter} = 1\{B1_{\mathrm{sup}} \wedge M1\text{-gen}_{\mathrm{sup}}\}\), reported separately with the marginal decomposition of v1.0 §5.3; not an eligibility gate.

---

## 5. Exact support probabilities: population law, reduced statistic, DP recurrence

### 5.1 Random elements and target probabilities

Design layer fixed (symbolic); outcome layer per §2.3/§2.5; held-out layer per §7.2. Targets:

\[
P(B1_{\mathrm{sup}}),\quad P(M1\text{-gen}_{\mathrm{sup}}),\quad P(\mathrm{Inter}),
\]

each a **population-level (unconditional) probability** under §2.3 weighting (and, in the correlated model, a mixture over parent effects per §2.5).

### 5.2 Reduced per-version statistic and exact factorization (independent reference)

In the independent reference model, version outcomes are mutually independent, and the support event depends on a version only through its reduced statistic

\[
T_v = \big(q(v),\, Z(\mathrm{par}(v)),\, k(v),\, \ell(v),\, M(v)\big),
\]

so

\[
P(\text{support event}) \;=\; \sum_{(t_v)} \Big[\prod_v \Pr(T_v = t_v)\Big]\,\mathbf{1}\{\text{event}(t_1,\dots,t_n) = 1\},
\]

a **finite exact sum**. The distinction demanded by GPT is recorded explicitly: this is a finite mathematical sum; whether its memoized evaluation is *practically* tractable at a given design size is a separate computational-plan question, **demonstrated, not assumed** (§5.4).

### 5.3 Per-version DP recurrence (GPT §7)

\(\Pr(T_v = (q, Z, k, \ell, M))\) is computed exactly by dynamic programming over strata:

- **State after strata \(1..s\):** \(\big(k_s, \ell_s, M_s\big)\) = cumulative definite failures, cumulative unresolved, running maximum; value = accumulated probability.
- **Initialization:** \(dp_0(0,0,0) = 1\).
- **Transition** (stratum \(s+1\), capacity \(R = 8\)): for \(x, y \ge 0\), \(x + y \le 8\),
\[
dp_{s+1}\big(k_s + x,\ \ell_s + y,\ \max(M_s, x)\big) \;\mathrel{+}=\; dp_s(k_s, \ell_s, M_s)\cdot
\frac{8!}{x!\,y!\,(8 - x - y)!}\,
\big(p^{\mathrm{fail}}_{q,s+1}\big)^{x}\big(p^{\mathrm{unres}}_{q,s+1}\big)^{y}\big(p^{\mathrm{corr}}_{q,s+1}\big)^{8 - x - y}.
\]
- **Output:** \(\Pr(T_v = (q,Z,k,\ell,M)) = dp_8(k, \ell, M)\); marginalizing over \(M\) gives the exact \(\Pr(k, \ell)\) used for the unconditional weighting §2.3.
- **Complexity:** states \(O(9 \times 9 \times 9)\) per stratum, 8 strata, \(\le 45\) transitions per state — exact, trivially enumerable; **no simulation, no truncation**.

### 5.4 Population-level aggregation and tractability honesty

The outer sum §5.2 is over tuples of reduced statistics. Exact evaluation proceeds by memoized DP over per-cell occupancy profiles (per cell: set of parents present, multiset of \(M\) values). The state space grows combinatorially with \(G\) and the number of cells; therefore:

- the **mathematical** statement (finite exact sum) is unconditional;
- **practical tractability** at a given symbolic design size must be established by a computational plan (state-space bound, memoization proof, or decomposition), and is **not asserted** here;
- in the correlated model (§2.5), the same structure holds conditionally on parent effects, mixed by deterministic quadrature over \((\theta_g, \varphi_g)\).

No numerical evaluation is performed under the current GO (§8's hand arithmetic excepted).

### 5.5 Structural capacity facts (unchanged in substance)

Family-level necessary conditions (\(n_Z \ge 3\); identity assigned in family for \(\ge 3\) parents), structural-exclusion listing, intersection decomposition — v1.0 §5.3 stands, with M1 read as M1-gen and the M1-si/M1-ci decomposition added to reporting.

---

## 6. B1 analysis lane (aligned to the exact conditioning cell)

### 6.1 Baseline that absorbs the full joint cell (GPT §4 — blocking correction)

**Primary baseline (declared):** the **exact-cell conditional (stratified) model** — the likelihood is conditioned on the full joint cell \((q, Z, k, \ell)\), i.e., conditional logistic regression with the cell as the stratification factor and \(C_D\) as the only covariate varying within cells.

- By construction, the baseline **absorbs** the entire joint cell structure — identity, family, and both exact totals, with all interactions — because it conditions on the cell itself. The v1.0 assertion "the baseline already absorbs \((q, Z, k, \ell)\)" is now demonstrated by the model specification rather than asserted.
- A cell contributes to the conditional likelihood **iff it contains within-cell \(C_D\) variation** (\(D_c \ge 2\)); cells without variation contribute zero terms. **B1 support (§4.1) is therefore exactly the operational condition for the primary analysis to be estimable** — the link between incidence and inference is now structural, not rhetorical.
- The v1.0 additive example (exact stratification on \((k,\ell)\) with additive \(Z\) and \(q\) effects) is **withdrawn** as a primary specification: it does not absorb the joint cell and could let \(C_D\) proxy omitted identity×family×totals interactions. Reduced baselines survive only as **declared, separately labelled sensitivity specifications**, each reported alongside the primary with its deviation stated.

**Outcome model and scoring (GPT §7):** \(h_v \mid n_h \sim \mathrm{Binomial}\big(n_h,\ 1 - \pi_v\big)\) with the truth model §7.2. Primary scoring rule: grouped **binomial deviance / log-loss** on held-out folds; concordance reported as a labelled secondary. Primary comparison: enriched vs baseline by the predeclared paired test across grouped folds, two-sided \(\alpha = 0.05\); one-sided results only as labelled sensitivity (v1.0 §6.3 stands; no invented effect size; no power from retired figures).

### 6.2 Validation and integrity rules (expanded per GPT §4)

1. **Leave-one-parent-out (LOPO):** reported for every split, including **whether training-fold within-cell \(C_D\) variation survives the split** — i.e., per fold, the count of cells retaining \(D_c^{\text{train}} \ge 2\) after removing the held-out parent's versions. A support condition in the full population does **not** guarantee fold-level estimability (one parent may carry the only distinctive concentration value); this must be measured and reported, never assumed.
2. **Leave-one-family-out (LOFO):** with the exact-cell primary baseline, the held-out family's \((Z, q)\) levels are absent from training, so the full conditional model is **not directly estimable** for those folds. Declared handling: LOFO results are reported under an explicitly labelled **reduced-form fallback** (cell strata without \(Z\), i.e., \((q, k, \ell)\) stratification), with the deviation from the primary estimand stated in the report. LOFO is never silently equated with the primary analysis.
3. **Unseen-level handling:** any fold encountering an unseen \(Z\) or \(q\) level is reported with the level named; no silent recoding or dropping.
4. **Identity coverage:** per-fold table of identities in test vs training representation (v1.0 stands).
5. **Support failures:** every cell and fold failure listed (v1.0 §4.4 stands).
6. **Frozen blind E3:** untouched (v1.0 stands).

---

## 7. Anti-manufacturing controls (corrected and expanded)

### 7.1 Explicit affinity path (GPT §7)

For each identity \(q\), declare a favoured failure stratum \(s^*(q)\) and a favoured unresolved stratum \(t^*(q)\), with strictly ordered gaps:

\[
w_{q,s}(\rho) \;=\; \exp\!\big(-\rho\,\Delta_{q,s}\big),\qquad
\Delta_{q,s^*(q)} = 0,\quad 0 < \Delta_{q,s_1} < \Delta_{q,s_2} \ \text{for ordered non-favoured strata},
\]
\[
\beta_{q,s}(\rho) \;=\; \exp\!\big(-\rho\,\Delta^{u}_{q,s}\big),\qquad
\Delta^{u}_{q,t^*(q)} = 0 \text{ similarly},
\]

embedded in the odds of §2.2 via \(\alpha_{q,s}(\rho) = \alpha^{\circ}_{q,s}\, w_{q,s}(\rho)\) with a fixed base \(\alpha^{\circ}\). Two anchor configurations are declared and both reported: **aligned** (\(t^* = s^*\)) and **crossed** (\(t^* \ne s^*\); this is null scenario N4). The formulas are explicit enough to reproduce every limiting argument below.

### 7.2 Complete held-out outcome model and the four null scenarios (GPT §5)

**Truth model (declared, complete):** per held-out record of version \(v\),

\[
\operatorname{logit}\big(\Pr(\text{incorrect})\big) \;=\; a_0 + a_k\,k(v) + a_\ell\,\ell(v) + a_{Z}\,Z(v) + a_{q}\,q(v) + \theta_{\mathrm{par}(v)} + \beta_C\, C_D(v),
\]

with \(\theta_g\) the parent-quality effect (variance symbolic), and, in confounding scenarios, the diagnostic propensities coupled to \(\theta_g\) via \(c_\theta\,\theta_g\) in the §2.5 logit-linear model. Version-level outcome: \(h_v \sim \mathrm{Binomial}(n_h, 1-\pi_v)\) with the record-level logit above (a declared aggregation).

**Null scenarios — all with \(\beta_C = 0\), each examined globally and, where defined, within identity strata:**

| ID | Configuration | What it tests |
|---|---|---|
| N1 | \(\beta_C = 0\), flat reference (\(\rho = 0\)), no parent-quality coupling (\(c_\theta = 0\)) | Basic false-positive behaviour of the B1 lane (should match the nominal \(\alpha\) under the predeclared test) |
| N2 | \(\beta_C = 0\), strong identity affinity (\(\rho \to 1\)) | Identity-to-concentration confounding: \(C_D\) becomes a deterministic function of \((q,k,\ell)\); under the exact-cell baseline the enriched model's gain must be **exactly zero** (Proposition, part 4) — any nonzero detected gain under the reduced fallback baseline indicates leakage of the kind GPT identified in v1.0 §6.1 |
| N3 | \(\beta_C = 0\), parent effects coupled to diagnostic outcomes (\(c_\theta \ne 0\)) | Parent-quality confounding: within a cell, \(C_D\) variation may proxy \(\theta_g\). Required reporting: whether the predeclared test controls size under N3; **any positive B1 result must be accompanied by the N3 control result**, and robustness to N3 is a declared precondition for interpreting a positive finding |
| N4 | \(\beta_C = 0\), crossed unresolved anchor (\(t^* \ne s^*\)) | Whether concentration proxies unresolved-outcome placement: within-cell covariance between failure placement and unresolved placement induced by crossed affinities, with \(\ell\) conditioned |

### 7.3 Corrected strong-affinity proposition (replaces v1.0 §7.2; repairs Claude's finding)

**Assumptions (explicit):**
- **(A1)** the failure path §7.1 with strictly ordered gaps \(\Delta_{q,s}\) (distinct values; strict total order of strata under identity \(q\));
- **(A2)** the unresolved path §7.1 with strictly ordered gaps \(\Delta^{u}_{q,s}\);
- **(A3)** conditioning totals satisfy \(k \ge 2\) and \(k + \ell \le 64\) (cell realizability, §3.2);
- **(A4)** propensities are interior for \(\rho < 1\) (bounded away from 0 and 1).

**Proposition.** Under (A1)–(A4), for every cell \((q, Z, k, \ell)\) and **every** \(k \ge 2\) (large \(k\) included):

1. The conditional table converges in probability to a deterministic limit:
\[
(f, u) \mid (k, \ell) \;\xrightarrow{\ P\ }\; T^*(q, k, \ell),
\]
the unique weight-maximizing feasible table (unique by the strict orders in A1–A2; finiteness of the support makes the maximum's probability tend to 1 as all competing weight ratios tend to 0).
2. Hence \(C_D \to C_D^{\infty}(q,k,\ell) = M^*(q,k,\ell)/k\), a deterministic function of baseline variables, with \(M^* \le \min(8, k)\) — so \(C_D^{\infty} \le 8/k < 1\) for \(k \ge 9\) (Claude's observation is consistent: the limit is **not** \(C_D = 1\) at large \(k\); the v1.0 claim of "m = k a.s." was wrong outside the restricted domain \(k \le\) favoured-stratum capacity).
3. **B1:** all versions in a cell share \(q\), so their \(C_D\) values converge to the same \(C_D^{\infty}(q,k,\ell)\); \(D_c \to 1\) and \(B1(c) \to 0\) for every cell; since the number of cells is finite, \(P(B1_{\mathrm{sup}}) \to 0\).
4. **Unidentifiability (the core anti-manufacturing result):** \(C_D \to\) a deterministic function of \((q,k,\ell)\), which the exact-cell baseline absorbs entirely; the enriched model's conditional incremental information given the baseline is **exactly zero in the limit**, for every \(k\).
5. **M1-gen — restricted and decomposed (corrects v1.0 claim 2):** within-parent versions in the same cell may carry **different identities**, whose limits \(M^*(q,k,\ell)\) may differ; therefore \(P(M1\text{-gen})\) need **not** tend to 0 in general. Persistence of M1-gen support under strong affinity, when it occurs, is **identity-driven (M1-ci)** and does not indicate within-cell stochastic variation. The stochastic component **M1-si** (same-identity pairs) does vanish, since it requires \(C_D\) variation at fixed \(q\), which converges to zero by parts 1–2. Reporting requirement: the M1-si / M1-ci decomposition of §4.2 in the strong-affinity limit, with only M1-si treated as B1-relevant.

*Proof of part 1:* the conditional law §2.2–§2.3 puts mass proportional to product-weights; under A1–A2 the ratio of any non-maximal table's weight to the maximal table's weight is a product of factors \(\exp(-\rho\,\Delta)\) with total exponent \(\ge \rho \cdot \delta_{\min} > 0\), hence tends to 0 while the number of tables is finite; normalization then concentrates on the unique maximizer. Parts 2–5 follow. \(\square\)

**Interpretation (anti-manufacturing guarantee, now correctly scoped):** mechanism structure alone cannot create **B1** support or within-cell stochastic variation in the strong-affinity limit, at any \(k\); support reported only at low \(\rho\), vanishing as \(\rho \to 1\), is the required shape of any credible feasibility claim. The v1.0 proposition's unrestricted "m = k a.s." and unqualified M1 conclusions are **withdrawn**; the scoped statement above replaces them.

---

## 8. Hand-worked example (unchanged in content; re-checked against §3)

The v1.0 §8 table (\(k = 2\), \(\ell = 0\) throughout) remains valid: with \(u = 0\), \(c_s = 8\) for all \(s\), \(M_{\min} = 1\), \(M_{\max} = 2\), so the attainable set \(\{1/2, 1\}\) matches the example's \(C_D\) values; both B1 cells and M1-gen qualify as computed there, and the separability illustration stands. No simulation; illustrative arithmetic only.

---

## 9. Reporting requirements for any future numeric evaluation (updated)

1. \(P(B1_{\mathrm{sup}})\), \(P(M1\text{-gen}_{\mathrm{sup}})\), \(P(\mathrm{Inter})\) — population-level (§5.1), over the \(\rho\) grid, under the independent reference **and** the correlated model (§2.5), with aligned and crossed anchors.
2. Full incidence tables (§4.1, §4.2 with M1-si/M1-ci decomposition), plus the probability-weighted distribution of \(N_{B1}\).
3. Cell envelopes \(\mathcal{A}(k,\ell)\) (§3.2) and exact-cell collision rates as a function of \(\ell\), computed exactly.
4. All four null scenarios N1–N4 (§7.2), global and within identity strata; fold-level estimability reports (§6.2), including per-split survival of training-fold within-cell variation.
5. Explicit statement of the computational plan demonstrating practical tractability of the §5 sums at the evaluated design size.

---

## 10. What this specification does not do

Unchanged from v1.0 §10, plus: no numerical evaluation of §5 beyond §8's hand arithmetic; no claim that the independent reference model represents a population of related solver implementations — realistic feasibility claims require the correlated model §2.5; the M1-gen authority question remains open pending the review chain.

## 11. Compliance map (updated)

| Requirement | Where |
|---|---|
| A. Symbolic population, nothing inherited | §1 |
| B. B1 baseline aligned to the exact cell; frozen E3 untouched | §6.1, §6.2 |
| C. Three probabilities reported separately; no assumed counts; population vs conditional distinguished | §4.3, §5.1–§5.2 |
| D. Fisher vs Wallenius with generative justification; complete \(p^{\mathrm{corr}}\) and boundary conventions; no truncation; unresolved separate | §2.1–§2.4 |
| E. Corrected strong-affinity proposition (explicit assumptions, all \(k\), M1 decomposition); four null scenarios; correlated population model; grouped validation with fold-level estimability; support failures reported | §7.1–§7.3, §2.5, §6.2, §4.2 |
| F. Two-sided \(\alpha = 0.05\) primary; labelled sensitivity; no invented effect; no power from retired figures | §6.1, §6.3 (v1.0) |
| Capacity theory correct and three-level | §3 |
| M1 authority clarified (M1-gen) | §4.2 |
| DP state and recurrence explicit; finite-sum vs practical-tractability distinction | §5.3–§5.4 |
| Outcome unit and scoring declared | §1.4, §6.1 |
| Held-out bank never sealed; consent-provenance gap visible | header, §1.4, §10 |

---

**End of Rev 1.1.** Per the recorded process: Claude reviews this revision independently; GPT challenges scientific coherence — in particular whether the corrected §3/§7 now supports the claim that B1 and M1 can be satisfied without manufacturing concentration variation, and whether the correlated population model §2.5 is a defensible model of independently developed parent solvers. Only a further explicit GO authorizes numeric evaluation of §5 at scale.
