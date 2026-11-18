# B1/M1 joint-incidence feasibility specification (symbolic)

**Date:** 2026-11-12
**Version:** 1.0 — first issue for independent review
**Prepared by:** GLM
**Independent review:** pending (Claude). Adjudication: pending (GPT).
**Authorization basis:** bounded GO, 2026-11-11 (GPT): *design and mathematics only* — mathematical definitions, abstract incidence tables, derivations, and hypothetical examples. **Not authorized and not performed:** executable simulation, Monte Carlo, solver construction, mutation allocation for real bodies, generator execution, bank reuse, predictive fitting, repository publication. This file is an untracked local draft.

**Standing question this specification must answer (GPT, 2026-11-11):**
*Can a newly designed population of independent single-mutant parent solvers produce enough repeated identity-level observations and concentration variation to support B1, without manufacturing the signal through mechanism structure?*

**Provenance notes kept visible:**
- The 2026-11-05 B1 decision record is *record-verified* (blob, delegation quote, lineage, cell definition); **joint consent provenance remains open** and this specification does not rely on consent having been independently verified.
- The current held-out bank is **development data** (publicly exposed per the decision record §4 and the 2026-11-03 exposure verification). It is **never** described as sealed anywhere in this document.
- The frozen blind E3 analysis is untouched by this specification.

---

## 1. Population structure (symbolic; nothing inherited)

### 1.1 Objects

| Symbol | Object | Constraints |
|---|---|---|
| \(g\) | independent parent implementation | \(g \in \{1,\dots,G\}\), \(G\) a **symbolic design parameter** (no assumed value) |
| \(Z(g)\) | parent family of \(g\) | \(Z(g) \in \mathcal{Z}\); \(n_Z = |\{g : Z(g)=Z\}|\) symbolic per family |
| \(v\) | solver version | each parent \(g\) has one control version \(S0(g)\) (intended-correct, outside all mutation strata) and mutant versions \(v \in \mathcal{V}(g)\), \(V_g = |\mathcal{V}(g)|\) **symbolic**, \(V_g \ge 2\) required for any within-parent contrast |
| \(q(v)\) | individual mutation identity of mutant version \(v\) | \(q(v) \in \mathcal{Q}\), \(|\mathcal{Q}| = Q\) **symbolic**; every mutant version carries **exactly one** identity (single-mutant design) |
| \(m(q)\) | broad mechanism category of identity \(q\) | \(m(q) \in \mathcal{M}\), symbolic; plays **no role** in B1 cells (B1 conditions on \(q\) itself); retained only for design-diversity bookkeeping and possible future mechanism-level work |
| \(a\) | assignment rule | \(a : \{(g,j)\} \to \mathcal{Q}\), assigning one identity per mutant version; a **declared design choice**, not inherited from any retired schedule |

### 1.2 Explicit non-inheritance

The retired objects — the eight-mechanism catalogue, the 28+2 pair schedule, the 90-version plan, and the SA/SB/S-extra assignments — are **not** used as facts anywhere in this specification. \(G\), \(\{n_Z\}\), \(\{V_g\}\), \(Q\), and \(a\) are all free design parameters to be fixed by the new design; support results are reported **as functions** of them.

### 1.3 Diagnostic observation structure

Each mutant version \(v\) is run against the frozen diagnostic bank: \(S = 8\) input strata, \(R_s = 8\) records per stratum (\(s = 1,\dots,8\)). These two structural constants are the **only** bank-derived quantities used here; they enter as abstract capacities, and no bank data are executed or reused. Per record \(r\) in stratum \(s(r)\), the outcome class is one of:

\[
\text{correct},\quad \text{definite failure},\quad \text{unresolved}.
\]

### 1.4 Version-level sufficient statistics

For version \(v\), let

\[
f_s(v) = \#\{\text{definite failures in stratum } s\},\qquad
u_s(v) = \#\{\text{unresolved in stratum } s\},
\]

\[
k_{\mathrm{fail}}(v) = \sum_{s=1}^{8} f_s(v),\qquad
k_{\mathrm{unres}}(v) = \sum_{s=1}^{8} u_s(v),
\]

and, for \(k_{\mathrm{fail}}(v) \ge 1\),

\[
C_D(v) \;=\; \frac{1}{k_{\mathrm{fail}}(v)} \max_{s} f_s(v).
\]

For \(k_{\mathrm{fail}}(v) = 0\), \(C_D\) is **undefined**; such versions lie in no B1 or M1 cell (a control-like result, and the reason \(S0\) is outside all strata). \(u_s\) never enters \(C_D\): concentration is over **definite** failures only, and unresolved outcomes are carried as a separate exact coordinate throughout.

### 1.5 Held-out outcome (development data)

Each version \(v\) also has a held-out development outcome \(Q_v \in [0,1]\) (mean correctness over the fixed, publicly exposed held-out bank, or a per-record variant — declared before any execution). This bank is development data; it supports only fixed-bank developmental evaluation, never a sealed-evaluation claim.

---

## 2. The conditional failure-allocation law (sampler resolution)

### 2.1 Declared generative interpretation

**Declared process (per version \(v\)):** the mutation identity \(q(v)\) induces record-level class propensities that depend on the record's stratum and the identity:

\[
\Pr(\text{record in stratum } s \text{ is definite-fail}) = p^{\mathrm{fail}}_{q,s},\qquad
\Pr(\text{unresolved}) = p^{\mathrm{unres}}_{q,s},
\]

with outcomes **independent across records**. The independence idealization is a declared premise of the feasibility accounting (see §7.3 for the correlation bracketing caveat); it is not a claim about real solver behaviour.

**Conditioning event:** the B1/M1 cells are defined on the **observed exact** totals \((k_{\mathrm{fail}}, k_{\mathrm{unres}})\). Conditioning independent per-record categorical trials on their exact totals yields the Fisher-type conditional law. There is no sequential-depletion mechanism in the declared story: a mutation does not "fire \(k\) times in a fixed order," drawing strata one at a time with depleting weights.

### 2.2 Choice: Fisher's noncentral (multivariate) hypergeometric — with reason

Conditioning on \(k_{\mathrm{fail}}\) alone (for the definite-failure vector) gives

\[
\Pr\!\big(f = x \,\big|\, k_{\mathrm{fail}} = k\big)
= \frac{\prod_{s} \binom{R_s}{x_s}\, w_{q,s}^{\,x_s}}{Z_{k}(w_q)},
\qquad
Z_{k}(w_q) = \sum_{\substack{0 \le x_s \le R_s \\ \sum_s x_s = k}} \prod_{s} \binom{R_s}{x_s} w_{q,s}^{\,x_s},
\]

where \(w_{q,s} = p^{\mathrm{fail}}_{q,s} / (1 - p^{\mathrm{fail}}_{q,s})\) are stratum odds under identity \(q\). This is **Fisher's** noncentral multivariate hypergeometric: independent weighted selection conditioned on a fixed total.

**Wallenius's** distribution would instead represent sequential weighted sampling without replacement: at each successive failure, stratum \(s\) is chosen with probability proportional to \(w_s\,(R_s - x_s^{\text{current}})\), depleting capacities step by step. That is a **different generative process** (ordered draws, capacity depletion, pre-fixed number of fires) and it induces artifactual negative dependence across strata — a manufactured structure of exactly the kind the standing question prohibits.

**Decision:** the specification uses the **Fisher-type conditional law**. Wallenius is rejected with the reason above, recorded so the choice is auditable.

### 2.3 Joint law with unresolved outcomes (separate coordinate)

Conditioning on **both** exact totals \((k_{\mathrm{fail}}, k_{\mathrm{unres}}) = (k, \ell)\):

\[
\Pr\!\big((f,u) = (x,y) \,\big|\, k, \ell\big)
= \frac{\displaystyle\prod_{s} \frac{R_s!}{x_s!\, y_s!\, (R_s - x_s - y_s)!}\; \alpha_{q,s}^{\,x_s}\, \beta_{q,s}^{\,y_s}}{Z_{k,\ell}(\alpha_q, \beta_q)},
\]

with \(\alpha_{q,s} = p^{\mathrm{fail}}_{q,s}/p^{\mathrm{corr}}_{q,s}\), \(\beta_{q,s} = p^{\mathrm{unres}}_{q,s}/p^{\mathrm{corr}}_{q,s}\), and \(Z_{k,\ell}\) the normalization over all tables with \(\sum x_s = k,\ \sum y_s = \ell,\ x_s + y_s \le R_s\). This is Fisher-type conditioning on two linear totals (a doubly-conditioned generalized noncentral hypergeometric). **Unresolved outcomes are never merged into definite failures**; they enter only through the exact second total \(\ell\) and through capacity reduction \(x_s + y_s \le R_s\).

### 2.4 No truncation, exact normalization

\(Z_k\) and \(Z_{k,\ell}\) must be computed by **exact** summation over the finite support (integer arithmetic or exact rationals, or floating point with a declared, verified error bound). **Arbitrary overflow truncation is prohibited**; if a numeric range limit is ever reached, the affected quantity is reported as uncomputed, not approximated silently.

---

## 3. \(C_D\) attainable values (derivation)

**Lemma.** Fix a version with \(k = k_{\mathrm{fail}} \ge 1\), and stratum failure capacities \(\tilde R_s = R_s - u_s \le 8\) (unresolved reduce capacity). Then

\[
C_D = \frac{m}{k},\qquad m = \max_s f_s \in \Big\{\big\lceil k / 8 \big\rceil, \dots, \min(k, 8)\Big\},
\]

so the number of attainable \(C_D\) values at fixed \(k\) is

\[
A(k) = \min(k,8) - \big\lceil k/8 \big\rceil + 1
\qquad\big(\text{e.g. } A(2) = 2:\ C_D \in \{\tfrac12, 1\};\ A(8) = 8;\ A(9) = 7\big).
\]

*Derivation:* \(\max_s f_s \ge \lceil k/8 \rceil\) because 8 strata must absorb \(k\) failures; \(\max_s f_s \le \min(k, 8)\) because no stratum holds more than \(k\) or more than its capacity; every intermediate value of \(m\) is attainable by placing \(m\) failures in one stratum and spreading the rest with per-stratum maxima \(< m\). Unresolved records only shrink attainable sets further (capacity reduction). \(\square\)

**Consequences used later:** (i) any \(C_D\) variation inside an exact cell requires \(k \ge 2\) (at \(k = 1\), \(C_D = 1\) deterministically); (ii) at fixed \(k\), the maximum number of distinct \(C_D\) values any cell can contain is \(A(k)\); (iii) variation requires the failure vector to spread across at least two strata for at least one version.

---

## 4. Support conditions (B1 and M1, kept separate)

### 4.1 B1 cell support (cross-parent; per the 2026-11-05 record)

For an exact cell \(c = (q, Z, k, \ell)\) with \(k \ge 2\), let

- \(\mathcal{V}(c) = \{v : q(v) = q,\ Z(\mathrm{par}(v)) = Z,\ k_{\mathrm{fail}}(v) = k,\ k_{\mathrm{unres}}(v) = \ell\}\) (mutant versions only);
- \(G_c = |\{\mathrm{par}(v) : v \in \mathcal{V}(c)\}|\) — distinct parent groups;
- \(D_c = |\{C_D(v) : v \in \mathcal{V}(c)\}|\) — distinct observed \(C_D\) values.

\[
\boxed{\ B1(c) = 1\ \iff\ G_c \ge 3\ \wedge\ D_c \ge 2\ \wedge\ k \ge 2.\ }
\]

**No pooling:** support is evaluated **per exact cell**; cells are never merged across identities, families, or exact \((k, \ell)\) combinations, in support accounting or in analysis. \(B1_{\mathrm{sup}} = 1\{\exists c : B1(c) = 1\}\); the qualifying-cell count \(N_{B1} = \#\{c : B1(c)=1\}\) is reported, not just the indicator.

### 4.2 M1 support (within-parent; separate condition)

For an exact failure cell \(e = (k, \ell)\) with \(k \ge 2\), let

- \(g \in \mathcal{G}(e)\) iff parent \(g\) contributes **two or more of its own versions** to \(e\) **with different** \(C_D\) values among those versions.

\[
\boxed{\ M1(e) = 1\ \iff\ |\mathcal{G}(e)| \ge 3;\qquad M1_{\mathrm{sup}} = 1\{\exists e : M1(e) = 1\}. }
\]

\(k \ge 2\) is not an extra assumption but a derived necessity (Lemma §3: no \(C_D\) variation at \(k = 1\)). M1 requires **within-parent** replication of an exact cell with divergent concentration; it does **not** require the two versions to share identity \(q\).

### 4.3 Intersection — reported, never a gate

\[
\mathrm{Inter} = 1\{B1_{\mathrm{sup}} = 1 \wedge M1_{\mathrm{sup}} = 1\}.
\]

The intersection is **reported**; it is **not** imposed as an additional B1 eligibility gate (the 2026-11-05 record does not specify one, and adding it would be stricter than the recorded decision). The intersection need not occur in the same cell.

### 4.4 Incidence reporting template (all cells; failures listed, never dropped)

Every realized exact cell is listed with:

| Column | Meaning |
|---|---|
| \(c = (q, Z, k, \ell)\) | exact cell identity |
| \(n_c\) | versions in cell |
| \(G_c\) | distinct parents |
| \(C_D\) multiset | all observed values, with parent labels |
| \(D_c\) | distinct \(C_D\) count |
| \(B1(c)\) | qualify / fail (with failing criterion named) |
| per-parent M1 contribution | for each \(g\): versions in \(e\), within-parent \(C_D\) spread |
| \(M1(e)\) | qualify / fail (with failing criterion named) |

Support **failures** (cells that nearly qualify, e.g. \(G_c = 2\)) are reported explicitly. Silence about a cell is a specification violation.

---

## 5. Probability space and exact computation of the support probabilities

### 5.1 Random elements

1. **Design layer (declared, symbolic):** \(G\), \(\{n_Z\}\), \(\{V_g\}\), \(Q\), family map \(Z\), assignment rule \(a\).
2. **Outcome layer:** for each version \(v\), the conditional law §2.3 given its realized \((k, \ell)\) — equivalently, the unconditional independent-categorical law over the \(8 \times 8 = 64\) diagnostic records with class propensities \((p^{\mathrm{fail}}_{q,s}, p^{\mathrm{unres}}_{q,s})\), parameterized symbolically (see §7 for the affinity parameterization).
3. **Held-out layer:** \(Q_v\) generated from a truth model containing a concentration coefficient \(\beta_C\) (§6). \(\beta_C = 0\) defines the negative control.

### 5.2 Exact (non-simulated) evaluation procedure

Because the conditional law §2.3 has finite support (all tables \((x,y)\) with the given totals), and the design layer is fixed, every support event is a cylinder event in a finite product space:

\[
P(B1_{\mathrm{sup}}) = \sum_{\text{realizations } \omega} \mathbf{1}\{B1_{\mathrm{sup}}(\omega) = 1\} \prod_{v} \Pr\big((f,u)(v) = \omega(v)\big),
\]

and similarly for \(P(M1_{\mathrm{sup}})\) and \(P(\mathrm{Inter})\). This is a **finite exact sum**, computable by stratum-wise dynamic programming over the conditional supports — no Monte Carlo anywhere. All three probabilities are reported **as functions of the symbolic design parameters** \((G, \{n_Z\}, \{V_g\}, Q, a)\) and the propensity regime.

*Execution note:* the procedure is **defined** here; running it at scale is a computation step requiring a further explicit GO. The only numeric evaluations under the current GO are the hand-worked examples in §8.

### 5.3 Structural capacity facts (symbolic; no counts assumed)

- A B1 cell \((q, Z, k, \ell)\) can exist only if \(n_Z \ge 3\) **and** identity \(q\) is assigned in family \(Z\) for at least 3 parents (assignment-level necessary condition). Families with \(n_Z \le 2\) are structurally incapable of hosting a B1 witness and are flagged as such in every incidence report (the analogue of the retired K5 limitation, derived rather than inherited).
- Identities assigned to fewer than 3 parents anywhere contribute to no B1 cell; such identities are listed in the incidence report as structurally excluded.
- \(P(\mathrm{Inter} \mid B1_{\mathrm{sup}})\) and the marginal decomposition \(P(\mathrm{Inter}) = P(B1) + P(M1) - P(B1 \cup M1)\) are reported; the gap \(P(B1) - P(\mathrm{Inter})\) is itself a feasibility diagnostic (it measures how often B1 succeeds precisely where M1 fails).

---

## 6. The B1 analysis lane (separate, explicitly unblinded; frozen E3 untouched)

### 6.1 Model comparison

On the development population (fixed, publicly exposed held-out bank as outcome; never described as sealed):

- **Baseline:** held-out outcome model with flexible terms for \(k_{\mathrm{fail}}\), \(k_{\mathrm{unres}}\), family \(Z\), and individual identity \(q\). "Flexible" means declared before execution from a predeclared family (e.g., exact stratification on \((k_{\mathrm{fail}}, k_{\mathrm{unres}})\) with additive \(Z\) and \(q\) effects under a penalized fit — Firth-type — given the small expected \(n\)); the choice is recorded, not tuned post hoc.
- **Enriched:** baseline \(+\ C_D\).

The scientific target is the incremental information of \(C_D\) **within** exact baseline strata: since identification of a \(C_D\) coefficient comes only from within-cell variation of \(C_D\) (baseline already absorbs \((q, Z, k, \ell)\)), **B1 support (§4.1) is exactly the population-level identification prerequisite.** This is the link between the incidence model and the analysis lane, and the reason they must be reported jointly.

### 6.2 Validation and integrity rules

- **Parent-grouped validation:** leave-one-parent-out and leave-one-family-out folds both reported.
- **Identity coverage:** for every fold, the table of identities appearing in the test partition vs their representation in training is reported. An identity present only in the held-out parents makes its baseline coefficient unidentifiable from training data; such folds are **reported**, not silently reweighted or dropped.
- **Support failures reported:** every cell that fails support is listed (§4.4).
- **Frozen blind E3:** untouched. Nothing in this lane may alter, reinterpret, or "correct" the frozen E3 pass.

### 6.3 Statistical planning

- **Primary convention:** two-sided \(\alpha = 0.05\) for the predeclared paired comparison of baseline vs enriched predictive performance across grouped folds.
- **Sensitivity:** one-sided calculations reported separately and explicitly labelled as sensitivity analyses, never substituted for the primary.
- **No minimum meaningful effect is invented**; no power or MDE claim is derived from the retired 30-parent / 150-variant figures (those numbers are design history, not evidence). Feasibility here means **identification support** (§5), not power against a chosen effect size.

---

## 7. Anti-manufacturing controls (the standing question, formalized)

### 7.1 Affinity parameterization

Single symbolic parameter \(\rho \in [0,1]\) interpolating identity-to-stratum affinity: under \(\rho = 0\) (flat reference) propensities are identity-independent, \(w_{q,s} = w_s\); as \(\rho \to 1\) (strong affinity) each identity \(q\)'s weight concentrates on one stratum \(s^*(q)\). Support probabilities are reported across this range, so the reader can see whether support exists only where variation is injected by mechanism structure.

### 7.2 Negative control (\(\beta_C = 0\), strong affinity) — analytic result, no simulation needed

**Proposition.** In the strong-affinity limit \(\rho \to 1\):
1. For any cell \((q, Z, k, \ell)\) with \(k \ge 2\): \(\Pr(C_D = 1 \mid \text{cell}) \to 1\), hence \(D_c \to 1\) and \(B1(c) \to 0\) for every cell.
2. For any exact cell \(e = (k, \ell)\): every version in \(e\) has \(C_D \to 1\) (regardless of identity), so within-parent \(C_D\) spread \(\to 0\) and \(M1(e) \to 0\).
3. Hence \(P(B1_{\mathrm{sup}}) \to 0\), \(P(M1_{\mathrm{sup}}) \to 0\), \(P(\mathrm{Inter}) \to 0\).
4. Moreover \(C_D \to C_D(q, k)\) is a deterministic function of baseline variables, so the enriched model's **conditional incremental information given the baseline is exactly zero** — the \(\beta_C = 0\) null yields not merely "no detected effect" but structural unidentifiability of any effect.

*Proof sketch:* (1) all \(k\) failures fall in \(s^*(q)\) with probability \(\to 1\) by the odds ratio tending to 0 for \(s \ne s^*(q)\) in the Fisher law §2.2; (2) \(C_D = m/k\) with \(m = k\) a.s.; (3)–(4) immediate. \(\square\)

**Interpretation (this is the anti-manufacturing guarantee):** mechanism structure alone **cannot** create B1 or M1 support in the strong-affinity limit; a design whose support survives only by forcing multi-stratum spread through the identity catalogue is manufacturing signal, and the incidence model will expose it as support existing only at low \(\rho\) driven by the affinity choice. The falsification check for any future numeric evaluation: **support must be reported as a function of \(\rho\), must be evaluated under the flat reference, and must vanish in the strong-affinity limit; the \(\beta_C = 0\) control must be run globally (condition 4) and within identity strata (conditions 1–2, evaluated per \(q\)).**

### 7.3 Correlation bracketing (declared caveat)

The Fisher law's record independence is an idealization. Real mutated solvers plausibly fail **correlated** within strata (one wrong algorithmic choice failing whole strata), which pushes \(C_D\) toward 1 and **reduces** within-cell variation. Therefore: the flat Fisher reference is the *variation-optimistic* bracket, the strong-affinity limit is the *variation-pessimistic* bracket, and a credible feasibility claim requires support under conditions **pessimistic enough to be realistic** — not only under the optimistic reference. A correlated-failure extension of §2.3 (overdispersion parameter) is defined as a required refinement before any execution-grade evaluation.

---

## 8. Hand-worked hypothetical example (abstract incidence table; arithmetic only)

Purely hypothetical realization under the flat reference, family \(Z = \{A, B, C\}\) (\(n_Z = 3\)), two mutants per parent, identities \(q_1, q_2\) each assigned to one mutant per parent; all \(k_{\mathrm{unres}} = 0\) in this example (real cells with \(\ell > 0\) are sparser — that is a reported feasibility cost, see §5.3).

| Parent | Version | \(q\) | failure vector \(f\) | \(k\) | \(C_D\) |
|---|---|---|---|---|---|
| A | A1 | \(q_1\) | (2,0,0,0,0,0,0,0) | 2 | 1 |
| A | A2 | \(q_2\) | (1,1,0,0,0,0,0,0) | 2 | 1/2 |
| B | B1 | \(q_1\) | (1,1,0,0,0,0,0,0) | 2 | 1/2 |
| B | B2 | \(q_2\) | (0,2,0,0,0,0,0,0) | 2 | 1 |
| C | C1 | \(q_1\) | (2,0,0,0,0,0,0,0) | 2 | 1 |
| C | C2 | \(q_2\) | (1,1,0,0,0,0,0,0) | 2 | 1/2 |

**B1 accounting:**
- Cell \((q_1, Z, 2, 0)\): versions {A1, B1, C1}; \(G_c = 3\) ✓; \(C_D\) multiset {1, 1/2, 1}, \(D_c = 2\) ✓; \(k = 2\) ✓ → **B1 qualifies**.
- Cell \((q_2, Z, 2, 0)\): versions {A2, B2, C2}; \(G_c = 3\) ✓; \(D_c = 2\) ✓ → **B1 qualifies**.

**M1 accounting (cell \(e = (2,0)\)):** parent A contributes {A1, A2} with \(C_D\) {1, 1/2} — spread ✓; same for B, C → \(|\mathcal{G}(e)| = 3\) → **M1 qualifies**. **Intersection: holds.**

**Separability illustration:** if the design instead assigned \(q_1\) to parents {A, B} only, cell \((q_1, Z, 2, 0)\) would have \(G_c = 2\) → **B1 fails** (reported with the failing criterion), while M1 could still hold — demonstrating that the two conditions are separate calculations and can diverge in either direction.

All realizations above have strictly positive probability under the flat Fisher reference; the example is illustrative arithmetic under the declared law, not a simulation and not evidence about any real population.

---

## 9. Design-parameter reporting requirements (no assumed counts)

Any future numeric evaluation must report, as functions of symbolic parameters:

1. \(P(B1_{\mathrm{sup}}),\ P(M1_{\mathrm{sup}}),\ P(\mathrm{Inter})\) over the \(\rho\) grid, under the flat reference and the correlated bracket (§7.3).
2. The full incidence table (§4.4) for a representative realization **and** the probability-weighted distribution of \(N_{B1}\) (number of qualifying cells), not just the existence indicator.
3. Structural capacity flags: families with \(n_Z \le 2\); identities with fewer than 3 parent assignments; expected exact-cell collision rates \(\Pr(\text{two versions share } (k,\ell))\) as a function of \(\ell\) — the sparsity cost of conditioning on unresolved totals.
4. The \(\beta_C = 0\) control results, global and within identity strata (§7.2).

---

## 10. What this specification does not do

- No executable simulation, Monte Carlo, or numeric evaluation beyond §8's hand arithmetic; §5.2's procedure is defined, not run.
- No solver construction, no mutation allocation for real bodies, no generator execution, no bank reuse (only the abstract structural constants \(S = 8\), \(R_s = 8\) are cited), no predictive fitting.
- No use of the retired eight-mechanism catalogue, 28+2 schedule, 90-version plan, or SA/SB/S-extra assignments as facts (§1.2).
- No description of the held-out bank as sealed — it is development data throughout.
- No resolution of the joint-consent provenance gap for the 2026-11-05 record; the gap remains open and visible.
- No amendment of the frozen v1.0 specifications or of the frozen blind E3 analysis.
- The per-record outcome independence premise (§2.1) and the propensity parameterization (§7.1) are **modeling premises for feasibility accounting**, not claims about real mutation effects; a per-mechanism realism argument belongs to a future mechanism-level document and is out of scope here.

---

## 11. Compliance map (GPT's A–F structure and the review rubric)

| Requirement | Where |
|---|---|
| A. Population structure, symbolic, nothing inherited | §1 |
| B. B1 analysis: baseline vs enriched, frozen E3 untouched | §6.1, §6.2 |
| C. Joint incidence: three probabilities reported separately, no assumed counts | §4.3, §5, §9 |
| D. Sampler resolution: Fisher vs Wallenius with generative justification; no truncation; unresolved separate | §2 |
| E. \(\beta_C = 0\) strong-affinity control, global and within strata; grouped validation; identity coverage; support failures reported | §7.2, §6.2, §4.4 |
| F. Two-sided \(\alpha = 0.05\) primary; one-sided labelled sensitivity; no invented effect; no power from retired figures | §6.3 |
| Rubric: symbolic only | §1.2 |
| Rubric: Fisher/Wallenius stated with generative justification | §2.1–§2.2 |
| Rubric: three support probabilities separate | §4, §5 |
| Rubric: control global + within identity strata | §7.2 |
| Rubric: held-out bank never sealed | §1.5, §6.1, §10 |
| Rubric: consent-provenance gap visible | header, §10 |
| Rubric: no power/minimum-effect from retired numbers | §6.3 |

---

**End of specification.** Next steps per the recorded process: Claude reviews independently; GPT challenges scientific coherence (especially §7 — whether B1 and M1 can both be satisfied without manufacturing concentration variation); only a further explicit GO authorizes numeric evaluation of §5.2 at scale.
