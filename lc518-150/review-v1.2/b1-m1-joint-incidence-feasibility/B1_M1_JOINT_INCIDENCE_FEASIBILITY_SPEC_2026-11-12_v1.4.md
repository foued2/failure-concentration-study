# B1/M1 joint-incidence feasibility specification (symbolic) — Rev 1.4

**Date:** 2026-11-14
**Version:** 1.4 — targeted GLM revision following Claude's independent review of Rev 1.3 and GPT's declared open analysis decisions; not accepted or frozen
**Prepared by:** GLM
**Review chain:** v1.0–Rev 1.2 archived unchanged on review branch `gpt/b1-m1-rev1.2-review-chain-2026-11-14`, commit `dbdc82984a9259aa6d731bc6a64224373d74673b` (v1.2 byte-identical to the GLM draft, SHA-256 `976DDB18…0B72BC`). Rev 1.3 published at commit `bb4feb1f5d7448cae391cfaa0dbaddbf4725db43`, SHA-256 `367BBEB50D9013198145FB9DDAE96B08D05A8E3A6161C27961697C3B96FD43BE` (hash independently verified by Claude at commit `bb4feb1f5d7448cae391cfaa0dbaddbf4725db43`). Claude independent review of Rev 1.3 completed 2026-11-14: repairs R1 (capacity construction) and R2 (stratum-varying parent loadings) verified in full, R3 (P-pred primary) verified as coherent with open inference; five findings issued — all mapped in §0 below. GPT declared two open analysis decisions (common \(\beta_C\) slope; overlapping-LOPO inference) — also mapped below.
**Authorization basis:** bounded GO (design and mathematics only) — unchanged. This revision is **published on the review branch** `gpt/b1-m1-rev1.2-review-chain-2026-11-14` as an unreviewed draft (Amendment D at commit `52ba3db0ed97ef34f8fb17a68369d8f1c90c65c1`; the Amendment E publication commit is recorded in the branch history) — **not accepted, not frozen, and not merged to `master`**. **Not authorized and not performed:** numerical probability evaluation, executable simulation, Monte Carlo, solver construction, mutation allocation for real bodies, generator execution, bank reuse, or predictive fitting.
**Predecessors:** v1.0, Rev 1.1, Rev 1.2 (archived, commit `dbdc829`), and Rev 1.3 (commit `bb4feb1`) retained unmodified as reviewed artifacts.
**Amendment A (2026-11-14, before first file-level review):** Rev 1.4 was delivered locally (SHA-256 `9F4541D5F222269D71EEB08E7594774CC0460D795574D8000B0C5F7E9260B0F2`) but never published or reviewed. Before review, GPT's adjudication (accepting the free-coordinate tie argument under stated conditions) and Claude's verification required three qualifications to be written **into §7.3 item 4 itself** (genericity; per-identity scope; exact comparisons only) and GPT's slope-estimability reporting requirement into §6.1/§9. This amendment applies those edits; the predecessor artifacts are untouched.
**Amendment B (2026-11-14, before first file-level review; narrow, per GPT's blocking finding and Claude's verification):** GPT found — and Claude independently verified — that Amendment A's Q1 wrongly implied that a tie in a deterministic penalty profile implies regime (T). Counterexample (now recorded in §7.3 item 2): \(s^*=1\), \(\Delta^F_{q,1}=0\), \(\Delta^F_{q,s}=1\) for \(s=2,\dots,8\), \(k=9\), \(\ell=0\) gives seven tied minimizers, all with \(M=8\), \(C_D=8/9\) — ties present, **regime (D)**. Amendment B: (1) Q1 replaced by the ties-vs-regime distinction; (2) the "lower-dimensional/discrete/equality-preserving ⇒ regime (T)" sentence replaced — coverage of the genericity argument is stated, and all such families are classified by the exact audit; (3) the cone wording corrected (measure-zero intersection, not "lower-dimensional set"); (4) the counterexample recorded in §7.3 item 2; (5) §9 item 4 requires per-cell \(|\Psi_q|\) and M-variation reporting; (6) §6.1 slope-identification wording corrected (intercept sets the level; the slope is identified by within-cell variation); (7) reporting terminology fixed to "held-out-parent prediction on the fixed development bank" (§9 item 8). Pre-amendment hash `FD5EDEBB72960FCD7DF939DCEB76CDD68B87A59632DA0FF4242C981AFBDFC215`.
**Amendment C (2026-11-14, before first file-level review; two accepted non-blocking refinements plus one accepted reporting refinement):** (1) GPT's proof-completeness strengthening — §7.3 item 4 now states explicitly that the feasible table set is finite, so there are finitely many pairwise tie hyperplanes and their finite union also has measure zero; *all* ties among distinct tables are broken almost surely. (2) Per GPT's distinction and Claude's recommendation — the N3 interpretation is written into the specification itself (§7.2 N3 row and §9 item 5), not left to the future analysis plan: a positive B1 gain under N3 is consistent with \(C_D\) predicting held-out correctness through the latent parent-quality channel (\(\theta_g\) enters both the placement loading \(\gamma^F_s\theta_g\) and the outcome model) and neither establishes a direct concentration mechanism nor automatically fails the predictive target. (3) GPT's reporting refinement (non-blocking, passed with the two refinements above) — §9 item 5 requires the N3 evaluation to report the association between \(C_D\) and the simulated parent effect \(\theta_g\) within the eligible B1 cells, under a declared weighting convention, showing whether the intended proxy pathway actually operated. Applied in two stages: refinements (1)–(2) first (interim SHA-256 `0CB2DE0BD290005B3BC0F81E0E573D846B2B9C073E5A15D6324B65D6EE054847`), then refinement (3); both stages before any file-level review. Pre-amendment hash `814D51AA95378BC3B8C8164293687D1309E27FD641AE622017B9F571F7340391`.
**Amendment D (2026-11-14, before first file-level review; two narrow wording corrections per GPT's review, Claude concurring, plus provenance completeness):** (1) §7.2 N4-a — "A \(C_D\) gain indicates leakage or model misspecification" replaced: a **reproducible or inferentially supported** \(C_D\) gain **beyond the predeclared finite-sample null variability** is evidence of leakage or model misspecification under the control; an **isolated positive estimate can arise by chance** under a correctly specified null and is not, by itself, evidence of a data leak. (2) Closing paragraph refreshed to acknowledge Amendments B and C and the N3 interpretation (it previously still described the pre-Amendment-B open questions). (3) Provenance completeness (Claude): the Amendment C interim hash is now recorded in the Amendment C paragraph above, not only in the transmittal. Pre-amendment hash `FE7647AAE83867FE9A4B9769C41CBBD511B267F92517C89D14A0C62DE98C5CDA`.
**Amendment E (2026-11-14, after publication of Amendment D at commit `52ba3db0ed97ef34f8fb17a68369d8f1c90c65c1`; three status/provenance corrections per GPT's adjudication HOLD, no mathematical changes):** (1) **N4-a operationalisation deferred to the B1 analysis plan** — the plan must define, before any N4-a evaluation: (i) the null reference procedure; (ii) the calibration statistic for finite-sample null variability; (iii) the replication/resampling structure; (iv) the reproducibility criterion for a "reproducible or inferentially supported" gain; (v) the evidence threshold for declaring leakage or model misspecification; and (vi) the relevant multiplicity handling. Until the plan is frozen, N4-a remains **interpretive only**: no result may be classified as leakage or model misspecification under this control. §6.1's plan scope gains a corresponding item. (2) **Publication status corrected** in both stale places (Authorization basis; closing paragraph): this revision is **published on the review branch** `gpt/b1-m1-rev1.2-review-chain-2026-11-14` as an unreviewed draft — not accepted, not frozen, and not merged to `master`. The removed wording ("untracked local draft"/"has not been published"/"not accepted, frozen, or published") described the pre-`52ba3db` state; the Amendment A paragraph's "never published or reviewed" remains as an accurate historical statement about the delivered pre-amendment state. (3) **Verification provenance kept distinct:** Rev 1.3's hash verification belongs to commit `bb4feb1f5d7448cae391cfaa0dbaddbf4725db43`; Rev 1.4 Amendment D's byte verification was performed by GPT on the commit-pinned raw file at commit `52ba3db0ed97ef34f8fb17a68369d8f1c90c65c1` — SHA-256 `C5955DD0615A917C633951A4EF1D0AE1CB87405545FE5B503E71242793EE7967`, 53,261 bytes, LF line endings, 0 CR characters, final newline present; the commit is unsigned on GitHub, so the verification covers the file's bytes, not the commit author's cryptographic identity. Byte verification, content review, and final acceptance are distinct events and are reported separately in the closing paragraph. Pre-amendment hash `C5955DD0615A917C633951A4EF1D0AE1CB87405545FE5B503E71242793EE7967`.

---

## 0. Revision log (Rev 1.3 → Rev 1.4)

| # | Finding (source) | Disposition in Rev 1.4 |
|---|---|---|
| 1 | **§6.1 inference wording contradicts itself.** "Use one predeclared two-sided primary test at \(\alpha = 0.05\)" stands next to "no confirmatory p-value is claimed until the procedure is frozen" (Claude, 2026-11-14) | §6.1 Inference paragraph rewritten: \(\alpha = 0.05\) applies to the confirmatory test **only after** the parent-level uncertainty procedure is predeclared and frozen in the separate B1 analysis plan; until then \(\Delta LL\) is the primary descriptive estimand and no p-value is claimed. The contradictory sentence is withdrawn |
| 2 | **Tie-perturbation claim (§7.3 item 4) stated in the wrong coordinates.** The anchors are pinned at zero, so the free penalty space is lower-dimensional; "full-dimensional continuous perturbation distribution" is unclear as written (Claude, 2026-11-14) | §7.3 item 4 restated **in the free penalty coordinates**: \(7 + 7 = 14\) free coordinates after the fixed zero anchors (further restricted by declared orderings); ties are proper hyperplane constraints there; a proof is added that under §7.1's single-anchor-per-class declaration **no tie between distinct tables is structurally forced** (two tables agreeing on all free coordinates agree on the anchors too, by the total constraints), so an absolutely continuous perturbation on the free cone breaks every tie a.s. Lower-dimensional/discrete families remain regime (T) and are reported as such — **superseded by item 8 (Amendment B): a tie does not imply regime (T); such families are classified into (D)/(T) by the exact audit** |
| 3 | **No family-level effect in the benchmark.** Parent effects are i.i.d. including across families, which may understate between-family heterogeneity (Claude, 2026-11-14) | Declared limitation recorded in §2.5 and §10; a family-level effect \(\zeta_{Z(g)}\) is recorded as a **labelled candidate extension** admissible only after review-chain approval and before any evaluation — never post hoc |
| 4 | **N4-b overstates what a gain shows.** "Indicates" is too strong; the reading depends on how \(\xi_v\) correlates with \(M\) within a cell (Claude, 2026-11-14) | §7.2 N4-b reworded: a \(C_D\) gain under \(\beta_C = 0\) is **consistent with** concentration proxying omitted unresolved-placement information; the within-cell \(\xi\)–\(C_D\) correlation must be reported; no mechanism-level attribution from the gain alone |
| 5 | **§1 cross-reference dropped Rev 1.1 §1.4** (held-out bank status) (Claude, 2026-11-14) | §1 restored to cite §1.1–§1.4 of Rev 1.1, with the explicit supersession note: Rev 1.3's R8 replaced the version-level binomial primary unit by the per-record unit; the bank-status sentence (development data, never sealed) is retained in force |
| 6 | **Common \(\beta_C\) slope is an explicit modelling assumption**, not established by the B1 decision record (GPT, open decision 1, 2026-11-14) | §6.1 states the assumption explicitly; a **predeclared, labelled cell-specific-slope sensitivity** (\(\beta_{C,c}\), subject to fold-level estimability: at least two cells with \(W_{C,c}^{\mathrm{train}} > 0\)) is declared; never selected or promoted post hoc |
| 7 | **Overlapping-LOPO inference needs a separate B1 analysis plan**; until then \(\Delta LL\) is descriptive (GPT, open decision 2, 2026-11-14) | §6.1 declares the plan's required scope (test design with within-resample refitting, unequal-coverage handling, multiplicity, fold definitions, regularization prespecification); the plan follows the same review chain and GO discipline. Cross-referenced in §9 item 9 |
| 8 | **Tie ≠ regime (T) (blocking, Amendment B).** Amendment A's Q1 implied that a deterministic tie, or a lower-dimensional/discrete/equality-preserving penalty family, implies regime (T). Counterexample: \(s^*=1\), \(\Delta^F_{q,1}=0\), \(\Delta^F_{q,s}=1\) for \(s\ge2\), \(k=9\), \(\ell=0\): seven tied minimizers, all \(M=8\), \(C_D=8/9\) — ties present, regime (D) (GPT, 2026-11-14; counterexample verified by Claude) | Q1 replaced: **ties and regime are distinct** (tie = \(|\Psi|>1\); regime (T) iff \(M\) varies on \(\Psi\); tied constant-\(M\) cells are regime (D), multiplicity reported, no limiting \(C_D\) variation); the "remain regime (T)" sentence replaced (genericity coverage stated; all other families classified by the exact audit); cone wording corrected to measure-zero intersection; counterexample recorded in §7.3 item 2; \(\S\)9 item 4 adds \(|\Psi_q|\) and M-variation reporting |
| 9 | **Accepted refinements (Amendment C): two non-blocking + one reporting refinement.** (a) GPT: state explicitly that the feasible table set is finite, so there are finitely many pairwise tie hyperplanes and their finite union also has measure zero — making "all ties broken a.s." explicit rather than implicit. (b) Claude, endorsing GPT's distinction: the N3 interpretation belongs in the specification, not only the future analysis plan (2026-11-14). (c) GPT (non-blocking, passed with (a)–(b)): §9 item 5 must require the N3 evaluation to report the \(C_D\)–\(\theta_g\) association within eligible B1 cells | (a) §7.3 item 4 adds the finiteness/finite-union statement; (b) §7.2 N3 row and §9 item 5 carry the interpretation: a positive B1 gain under N3 is **consistent with \(C_D\) predicting held-out correctness through the latent parent-quality channel** (\(\theta_g\) enters both placement and outcome) and **neither** establishes a direct concentration mechanism **nor** automatically fails the predictive target; (c) §9 item 5 adds the **N3 proxy-pathway check** — report the association between \(C_D\) and the simulated \(\theta_g\) within the eligible B1 cells, under a declared weighting convention, showing whether the intended proxy pathway actually operated |
| 10 | **Two wording corrections + provenance completeness (Amendment D).** (a) GPT, Claude concurring: N4-a's "A \(C_D\) gain indicates leakage or model misspecification" is too strong — a single positive \(\Delta LL\) can occur by chance under a correctly specified null (2026-11-14). (b) GPT, Claude concurring: the closing paragraph still described the pre-Amendment-B open questions and omitted Amendments B/C and the N3 interpretation. (c) Claude: the Amendment C interim hash was cited only in a transmittal message, not in the document | (a) §7.2 N4-a reworded: a **reproducible or inferentially supported** \(C_D\) gain **beyond the predeclared finite-sample null variability** is evidence of leakage or model misspecification under the control; an **isolated positive estimate** can arise by chance and is not, by itself, evidence of a data leak; (b) closing paragraph refreshed (Amendments B/C and the N3 interpretation acknowledged; review status stated); (c) Amendment C's interim hash `0CB2DE0B…` recorded in the Amendment C header paragraph |
| 11 | **Three status/provenance corrections (Amendment E), per GPT's adjudication HOLD; no mathematical changes.** (a) GPT: N4-a's leakage/misspecification criterion needs explicit operationalisation deferred to the B1 analysis plan — the plan must define the null reference procedure, calibration statistic, replication/resampling structure, reproducibility criterion, evidence threshold, and multiplicity handling; until frozen, N4-a stays interpretive. (b) GPT: "untracked local draft"/"has not been published"/"not accepted, frozen, or published" contradicted the actual published state at commit `52ba3db`. (c) GPT: keep the two verification events distinct — Rev 1.3 verification ↔ commit `bb4feb1`; Rev 1.4 Amendment D verification ↔ commit `52ba3db` — and distinguish byte verification from content review and final acceptance | (a) §7.2 N4-a row and §6.1 plan scope item (vi) carry the operationalisation deferral (interpretive-only until the plan is frozen); (b) Authorization basis and closing paragraph corrected: published on the review branch as an unreviewed draft, not accepted, not frozen, not merged to `master` (Amendment A's historical statement retained as history); (c) Rev 1.3 verification attributed to `bb4feb1` in the review-chain line, GPT's Amendment D byte verification recorded with its parameters (53,261 bytes, LF, 0 CR, final newline; commit unsigned — bytes verified, not author identity), and the closing paragraph now separates byte verification, content review, and final acceptance |

**Retained from Rev 1.3 unchanged:** the diverging \(\lambda\)-path; set-valued strong-affinity limit; regime (D)/(T) distinction and exact per-cell audit; M1-si/M1-ci decomposition; the corrected §3.2 envelope with the exact-maximum construction (Claude-verified); stratum-varying parent loadings with the cancellation explanation; multinomial baseline-category probabilities; P-pred primary / P-assoc secondary; per-record outcome with shared record effect \(\omega_r\); equal-parent \(\Delta LL\); fold-level \(W_{C,c}^{\mathrm{train}}\) estimability; common scored sets and extrapolation flags; M1-gen authority caveat; population-versus-conditional weighting; finite-sum/tractability distinction; the no-execution boundary.

---

## 1. Population structure and held-out outcome unit

§1.1–§1.4 of Rev 1.1 stand as written (symbolic objects; retired allocation not inherited; \(S=8\), \(R_s=8\); \(M(v)=\max_s f_s(v)\), and \(C_D(v)=M(v)/k(v)\) for \(k\ge1\), undefined at \(k=0\); held-out bank = the fixed, publicly exposed 78-record development set, **never sealed**). Of Rev 1.1 §1.4, the bank-status sentence remains in force verbatim; its version-level binomial primary unit is **superseded** by Rev 1.3 (item R8) and retained only as a labelled version-summary.

**Primary held-out outcome unit (clarified; unchanged from Rev 1.3):** per-record correctness \(Y_{v,r}\in\{0,1\}\) for mutant version \(v\) on canonical development record \(r\in\{1,\dots,78\}\). The version-level count \(h_v=\sum_{r=1}^{78}Y_{v,r}\) and mean \(Q_v=h_v/78\) are descriptive summaries, not the primary likelihood unit. The same fixed, publicly exposed 78-record bank is used across versions; it is development data, never sealed. The primary estimand is performance on this fixed bank, not generalization to new records.

---

## 2. Probability model

### 2.1–2.4 — unchanged in substance

Independent reference per version (§2.1 boundary conventions stand); Fisher-type conditional law §2.2; explicit unconditional law §2.3 (population vs conditional distinction stands); no truncation §2.4. Under the parent-effect benchmark, §2.2 uses parent-indexed odds \(\alpha_{g,q,s},\beta_{g,q,s}\), conditional on \((\theta_g,\varphi_g)\); population probabilities are then mixed over these effects.

### 2.5 Parent-effect model — conditional placement dependence made explicit

For the correlated benchmark, let mutant version \(v\) have parent \(g=\operatorname{par}(v)\) and identity \(q=q(v)\). The independent reference is recovered by setting parent effects and stratum-varying loadings to zero. "Correct" is the reference category in a baseline-category multinomial logit. Define

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

**Declared limitation (no family-level effect — new in Rev 1.4):** in this benchmark, parent effects are i.i.d. **including across families**; there is no family-level shared effect \(\zeta_{Z(g)}\). This may understate between-family heterogeneity in a population of related implementations. A family-level effect is recorded as a **labelled candidate extension**: it may be added only after review-chain approval and before any evaluation, never post hoc and never silently. Recorded in §10.

**Status:** this is a stylized random-effects benchmark. It is not evidence that independently developed solver implementations actually follow Gaussian random effects, common identity shapes, or these conditional-independence assumptions.

---

## 3. Capacity and attainable \(C_D\) values

### 3.1 Fixed-\(u\) interval lemma — unchanged

Rev 1.1 §3.1 stands (Claude's exact-enumeration verification remains on record).

### 3.2 Cell envelope — closed form with exact-maximum construction (Claude-verified)

**Claim.** For every realizable pair \(k \ge 1,\ \ell \ge 0\) with \(k + \ell \le 64\):

\[
\boxed{\ \mathcal{A}(k,\ell) = \Big\{ \lceil k/8 \rceil,\ \dots,\ \min(k,8) \Big\}\ }
\]

— a full integer interval, for the \(8 \times 8\) design.

*Proof.* The universal bounds are \(M\le\min(k,8)\) and \(M\ge\lceil k/8\rceil\). Conversely, fix an integer \(M\) in this interval. Construct a failure vector by setting \(f_1=M\) and distributing the remaining \(k-M\) failures among strata 2–8, with each \(f_s\le M\). This is possible because \(k-M\le7M\), which follows from \(k\le8M\); also \(M\le8\), so every \(f_s\le8\). The constructed vector has \(\sum_s f_s=k\) and \(\max_s f_s=M\) exactly.

Now let \(D=64-\ell\). Since \(k+\ell\le64\), the required residual capacity \(D-k\) is an integer between 0 and \(64-k=\sum_s(8-f_s)\). Choose integers \(r_s\) with \(0\le r_s\le8-f_s\) and \(\sum_s r_s=D-k\), and set \(d_s=f_s+r_s\), \(u_s=8-d_s\). Then \(f_s\le d_s\le8\), \(\sum_s d_s=D\), and \(\sum_s u_s=\ell\). Thus this unresolved vector is admissible and the same failure allocation has maximum exactly \(M\). Every integer in the claimed interval is therefore attainable. \(\square\)

*Verification record:* the Rev 1.2 proof established only "maximum at most \(M\)"; the exact-maximum construction above was supplied in Rev 1.3 (item R1) and independently verified by Claude on 2026-11-14.

**Withdrawn (historical):** the Rev 1.1 mini-example (which missed the \(c = (1,\dots,1)\) configuration: at \(k=5, \ell=56\), \(u = (7,\dots,7)\) is admissible and gives \(M = 1\), so \(C_D = 1/5\) is attainable) and the claim that the union "need not be an interval" — for this design it always is.

**Levels kept distinct (as required):** (1) fixed-\(u\) interval (§3.1) — conditional on one unresolved vector; (2) the **closed-form envelope** above — the set of \(M\)-values any cell \((k,\ell)\) could ever contain, a design diagnostic; (3) the probability-weighted distribution of \(u \mid \ell\) under §2.3, which is what realized support accounting uses. The prohibition on presenting a particular \(u\)'s capacity as the cell envelope stands.

---

## 4. Support conditions

§4.1 (B1 cell support), §4.2 (M1-gen with authority note and M1-si/M1-ci decomposition), §4.3 (intersection reported, never a gate), and §4.4 (incidence template) stand unchanged from Rev 1.1. §6 uses full-population B1 cells as the primary candidate sample, but fold-level estimability adds further requirements; B1 support alone is not a guarantee that a particular LOPO fit or score is estimable.

---

## 5. Exact support probabilities

§5.1, §5.2, §5.4, §5.5 — unchanged in substance (population-level targets; reduced statistic \(T_v = (q, Z, k, \ell, M)\); exact finite sum; tractability honesty; structural capacity facts).

### 5.3 Per-version DP recurrence — complexity statement corrected (GPT C4, retained)

The recurrence itself stands (states \((k_s, \ell_s, M_s)\), transition over \((x,y)\), \(x + y \le 8\); output \(dp_8(k,\ell,M)\); marginal over \(M\) gives exact \(\Pr(k,\ell)\)). **Corrected bound:** after \(s\) strata, \(k_s \in [0, 8s]\), \(\ell_s \in [0, 8s]\), \(M_s \in \{0,\dots,8\}\), so the state count is at most \(9\,(8s+1)^2\); at \(s = 8\): \(9 \cdot 65^2 = 38{,}025\) states, at most 45 transitions each. Exact, trivially enumerable; no simulation, no truncation. (Rev 1.1's "\(9 \times 9 \times 9\)" was wrong.)

---

## 6. B1 analysis lane — P-pred primary, P-assoc secondary

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
- **Declared status of the common slope (new in Rev 1.4):** the common \(\beta_C\) is an **explicit modelling assumption of this specification**. It is **not** established by, or derived from, the 2026-11-05 B1 decision record or any other authority; it is adopted for parsimony and predeclared before outcomes are seen. Its adequacy is examined only through the predeclared sensitivity below — never by post hoc comparison or selection.
- **Predeclared slope-heterogeneity sensitivity (labelled, new in Rev 1.4):** refit the enriched model with cell-specific slopes \(\beta_{C,c}\) under the same fold rules and the same scored sets. Within an exact cell, the intercept \(\alpha_c\) only sets the cell's level; \(\beta_{C,c}\) is identified by within-cell \(C_D\) variation (wording corrected per Claude, 2026-11-14). A cell contributes a slope only when \(W_{C,c}^{\mathrm{train}}>0\) in the training fold, and the sensitivity is reported only when at least two cells contribute slopes. Results are reported **alongside** the common-slope primary as a labelled sensitivity; a divergence between the two is reported, not resolved, by this specification. Per GPT's adjudication (2026-11-14): the "at least two cells with \(W_{C,c}^{\mathrm{train}}>0\)" requirement is a **minimal estimability gate, not evidence of reliable estimation** — the sensitivity report must state **how many cells are slope-estimable and each estimable cell's individual support** (per-cell training version counts, \(W_{C,c}^{\mathrm{train}}\), and fitted-slope stability diagnostics), never a bare pass/fail flag.
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
with equal weight per scored parent; positive values favour the enriched model. Define \(\mathcal G_{\mathrm{score}}=\{g:|\mathcal V_g^{\mathrm{score}}|>0\}\); parents with no eligible scored rows are excluded from this average but are counted and their exclusion reasons reported. If \(\mathcal V_g^{\mathrm{score}}\) is the parent's common scored-version set and \(\mathcal R=\{1,\ldots,78\}\), then \(L_{m,g}=(|\mathcal V_g^{\mathrm{score}}||\mathcal R|)^{-1}\sum_{v\in\mathcal V_g^{\mathrm{score}}}\sum_{r\in\mathcal R}[-Y_{v,r}\log\widehat\pi^{(m)}_{v,r}-(1-Y_{v,r})\log(1-\widehat\pi^{(m)}_{v,r})]\). Report the paired parent-level differences and scored-set coverage.
- **Inference (rewritten in Rev 1.4; repairs Claude finding 1):** the primary inferential target is the equal-parent \(\Delta LL\) above. Because LOPO folds have overlapping training sets, a naive paired t-test treating fold scores as independent is **not accepted**. The parent-level uncertainty procedure — including refitting within each resample/permutation, handling of unequal scored-parent coverage, and multiplicity — must be predeclared and frozen in the separate **B1 analysis plan** before any fitting or inspection of held-out outcomes. Once that procedure is frozen, the single confirmatory test is two-sided at \(\alpha=0.05\). Until then, \(\Delta LL\) is the primary **descriptive** estimand and no confirmatory p-value is claimed. (Rev 1.3's present-tense sentence "use one predeclared two-sided primary test at \(\alpha=0.05\)" is withdrawn as self-contradictory.)
- **B1 analysis plan (scope declared, new in Rev 1.4):** the plan must specify, before any fitting or outcome inspection: (i) the confirmatory test for \(\Delta LL\) under overlapping LOPO folds (e.g. bootstrap or permutation with within-resample refitting, and the resampling unit); (ii) treatment of unequal scored-set coverage across parents; (iii) the role of the slope-heterogeneity and other labelled sensitivities (sensitivity only; no data-driven promotion); (iv) fold definitions, regularization, and convergence criteria, all prespecified; (v) multiplicity handling across any co-reported secondary summaries; and (vi) the **operationalisation of the N4-a control** (null reference procedure, calibration statistic for finite-sample null variability, replication/resampling structure, reproducibility criterion, evidence threshold, and multiplicity handling — per Amendment E), without which N4-a remains interpretive only. The plan is itself subject to the recorded review chain (GLM prepares → Claude reviews → GPT adjudicates) and to the same bounded GO discipline.

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
| N3 | Use the N1 settings except: at the zero-added-affinity reference, \(\operatorname{Var}(\theta_g)>0\), \(\theta_g\) enters held-out quality, and \(\gamma^F_s\) is nonconstant; optionally \(\gamma^U_s\) is nonconstant; \(\Sigma\) is declared | Parent-quality confounding that changes within-cell failure/unresolved placement. A common parent intercept alone is not N3 because it cancels after conditioning on \((k,\ell)\). **Interpretation (into the specification per GPT/Claude, 2026-11-14):** under N3, \(\theta_g\) enters **both** the placement loading \(\gamma^F_s\theta_g\) and the held-out outcome model, so \(C_D\) can become a **predictive proxy for latent parent quality** even with no direct concentration mechanism. A positive B1 gain under N3 is therefore **consistent with genuine incremental prediction under the recorded predictive target** — it is neither automatically a false positive, nor evidence of a direct concentration mechanism, nor an automatic failure of the predictive target. The analysis plan must keep these readings distinct; any mechanism-level attribution requires evidence beyond the gain alone |
| N4-a | Use the N1 settings at predeclared positive finite \(\lambda\) values, crossed anchors; \(\beta_{u\to y}=0\); other placement-confounding loadings disabled for this isolated control | There is no unresolved-placement pathway in this declared truth model. **Interpretation (corrected per GPT, Claude concurring, 2026-11-14):** a **reproducible or inferentially supported** \(C_D\) gain **beyond the predeclared finite-sample null variability** is evidence of leakage or model misspecification under this control. An **isolated positive estimate can arise by chance** under a correctly specified null and is not, by itself, evidence of a data leak. **Operationalisation deferred to the B1 analysis plan (Amendment E, per GPT, 2026-11-14):** the plan must define the null reference procedure, the calibration statistic, the replication/resampling structure, the reproducibility criterion, the evidence threshold, and the relevant multiplicity handling before any N4-a evaluation. Until that plan is frozen, N4-a remains **interpretive only**: no result may be classified as leakage or model misspecification under this control |
| N4-b | Use the N1 settings at predeclared positive finite \(\lambda\) values, crossed anchors; \(\beta_{u\to y}\ne0\) | Unresolved placement affects correctness. A \(C_D\) gain under \(\beta_C=0\) is **consistent with** concentration proxying omitted unresolved-placement information, since the exact B1 cell conditions on total \(\ell\), not the vector \(u\). The strength of this reading depends on the within-cell correlation between \(\xi_v\) and \(C_D(v)\) (equivalently \(M(v)\)), which must be reported; a gain may also arise through other channels and is not by itself a mechanism-level attribution |

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

   **A tie does not imply regime (T) (counterexample recorded; GPT 2026-11-14, verified by Claude).** With \(s^*(q)=1\), \(\Delta^F_{q,1}=0\), and \(\Delta^F_{q,s}=1\) for \(s=2,\dots,8\) (\(\ell=0\), so unresolved penalties are inactive), the penalty of a table is \(k-x_1\), and \(x_1\le8\) by \(x_1+y_1\le8\). For \(k=9,\ \ell=0\) every minimizer has \(x_1=8\) and exactly one failure in one of the other seven strata: \(|\Psi_q|=7\), yet \(M=8\) on all of \(\Psi_q\) and \(C_D\to8/9\) is constant. The cell is **regime (D) with ties present**. Therefore: **tie presence means \(|\Psi_q|>1\); the regime is determined solely by whether \(M\) varies on \(\Psi_q\)** — never by tie presence, dimensionality, or discreteness of the penalty family. Tied constant-\(M\) cells are regime (D); their multiplicity is reported but produces no limiting \(C_D\) variation and is never counted as concentration variation.

3. **Exact regime audit:** for every relevant \((q,k,\ell)\), enumerate the finite feasible table set, calculate the argmin set using the exact declared \((\Delta^F,\Delta^U)\), and test whether \(M\) is constant on it. Audit exact symbolic/rational or otherwise comparison-safe penalty values, never rounded floating-point weights. The regime set is indexed by the penalty profiles, as written above.

4. **Tie perturbations (restated in free coordinates in Rev 1.4; repairs Claude finding 2):** for identity \(q\), the declared profiles pin \(\Delta^F_{q,s^*(q)}=\Delta^U_{q,t^*(q)}=0\), leaving **\(7+7=14\) free penalty coordinates** (the non-anchor strata of each class), further restricted by any declared within-class ordering to a cone \(K_q\subseteq\mathbb R^{14}\). For two distinct feasible tables \(t\ne t'\), the tie equality \(\Phi_q(t)-\Phi_q(t')=0\) is a linear constraint on these free coordinates with coefficient vector \(c=(x-x',\,y-y')\) restricted to them. This coefficient vector is **never identically zero under §7.1's single-anchor-per-class declaration**: if two tables agree on all free (non-anchor) coordinates, then by \(\sum_sx_s=k\) and \(\sum_sy_s=\ell\) they agree on the anchored coordinates as well, so \(t=t'\) — contradiction. Hence every tie between distinct tables is a **proper hyperplane** in the free coordinate space; whenever \(K_q\) has nonempty 14-dimensional interior, the tie hyperplane intersected with \(K_q\) is a **measure-zero subset of \(K_q\)**, so a perturbation distribution on \(K_q\) that is absolutely continuous with respect to 14-dimensional Lebesgue measure breaks every tie with probability one. **Finiteness (explicit, per GPT, 2026-11-14):** the feasible table set for fixed \((q,k,\ell)\) is a bounded set of integer tables and therefore **finite**, so there are **finitely many** pairwise tie hyperplanes; a finite union of measure-zero sets is measure zero. Hence *all* ties among distinct feasible tables are broken simultaneously with probability one — the a.s. tie-freedom of the perturbed profile is a statement about the entire argmin set, not merely about each pair in isolation. **Coverage of this argument:** it applies only to absolutely continuous perturbations on the 14-dimensional free cone. Lower-dimensional, discrete, or equality-preserving penalty families are **not** covered by it; their tie structure must be classified into regime (D) or (T) by the exact audit of item 3 — their dimensionality or discreteness never determines the regime. The earlier "full-dimensional continuous perturbation" wording, which did not specify the coordinate space, is withdrawn.

**Three qualifications (required into the proof by GPT's adjudication and Claude's verification, 2026-11-14; Q1 replaced by Amendment B):**
- **(Q1) Ties and regime are distinct.** Deterministic profiles may produce ties. A tie alone does not imply regime (T): if \(|\Psi_q|>1\) but \(M\) is constant on \(\Psi_q\), the cell is regime (D); the multiplicity is reported, but it produces no limiting \(C_D\) variation. Regime (T) applies exactly when \(\Psi_q\) contains tables with at least two distinct values of \(M\). Regime is determined by the exact audit in item 3, not by the dimensionality or discreteness of the penalty family. (The genericity argument above is a statement about tie *occurrence* under a declared perturbation family — it is not a guarantee that deliberately selected deterministic profiles are tie-free, and deliberately chosen penalties can and do tie, as the item-2 counterexample shows.)
- **(Q2) Per-identity scope:** the free coordinate cone \(K_q\) and the perturbation family are declared **per identity** \(q\), because the penalty profiles are shared across parents within an identity; the argument is stated profile by profile, and a perturbation distribution breaking ties under one identity's profile says nothing about another identity's profile.
- **(Q3) Exact comparisons only:** the per-cell regime audit of item 3 remains mandatory and must use exact symbolic/rational or otherwise comparison-safe penalty values. The absence of ties is **never** inferred from rounded numerical values, under any perturbation argument.

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
4. The exact regime audit \(\Psi_q(k,\ell;\Delta^F,\Delta^U)\), \(|\Psi_q|\), M-constancy, regime (D)/(T), and share of support attributable to tie-dependent cells. For **every** cell report \(|\Psi_q|\) and whether \(M\) varies on \(\Psi_q\), so that tied regime-(D) cells (tie present, no concentration variation — see the §7.3 item 2 counterexample) are visible without being counted as concentration variation.
5. N1–N4 results, including the N3 stratum-varying parent loadings and the declared \(\Sigma\); report common-parent-intercept-only checks separately from true placement confounding; for N4-b, report the within-cell correlation between \(\xi\) and \(C_D\) alongside any gain. **N3 reading (per §7.2):** a positive B1 gain under N3 is reported as **consistent with latent parent-quality prediction** through the \(\theta_g\) channel — it must not be described as evidence of a direct concentration mechanism, and it must not be scored as an automatic failure of the predictive target. **N3 proxy-pathway check (GPT, 2026-11-14):** the N3 evaluation must report the association between \(C_D\) and the simulated parent effect \(\theta_g\) **within the eligible B1 cells**, under a **declared weighting convention** (predeclared before evaluation), showing whether the intended proxy pathway actually operated rather than merely reporting that it was possible.
6. P-pred primary \(\Delta LL\), equal-parent weighting, fold-level \(G_c^{\mathrm{train}}\), \(D_c^{\mathrm{train}}\), \(W_{C,c}^{\mathrm{train}}\), fit convergence/separation, scored-set coverage, common baseline/enriched test rows, and extrapolation flags; report the predeclared common-slope primary and the cell-specific-slope sensitivity side by side, with any divergence named, and for the sensitivity report the **number of slope-estimable cells and each cell's individual support** (never a bare pass/fail).
7. P-assoc secondary outcome-discordance and exposure-variation requirements, with no second unadjusted confirmatory claim.
8. Record-level and version-summary outcome diagnostics. **Terminology safeguard (GPT, 2026-11-14):** reports must consistently describe the procedure as **held-out-parent prediction on the fixed development bank** — the 78-record bank is publicly exposed development data, not a sealed confirmatory bank, and prediction holds out parents, not new records. No implication of generalization to unseen records is permitted.
9. The exact parent-level inferential procedure for overlapping LOPO folds and its predeclared assumptions before any predictive fitting, as specified in the separate B1 analysis plan (§6.1).
10. A computational plan that demonstrates practical tractability of the finite support sums at the proposed design size; finiteness alone is not a tractability claim.

## 10. What this specification does not do

- No numerical evaluation beyond the hand-worked arithmetic example in §8; no simulation, Monte Carlo, solver construction, mutation allocation for real bodies, generator execution, bank reuse, or predictive fitting.
- No claim that the stylized Gaussian random-effects benchmark represents independently developed solver implementations; its adequacy is an open model-validity question.
- **No family-level shared effect is modelled** (parent effects are i.i.d. across families); between-family heterogeneity may consequently be understated. A family-level effect is a labelled candidate extension requiring review-chain approval before any evaluation (§2.5).
- The **common \(\beta_C\) slope is a declared modelling assumption**, not established by the B1 decision record; cell-specific slopes enter only as the predeclared labelled sensitivity (§6.1).
- No population-wide anti-manufacturing conclusion in the presence of regime-(T) cells; their contribution must be separately reported and is not treated as genuine feasibility evidence when ties are imposed by design.
- No generalization from the fixed, publicly exposed 78-record development bank to unseen records.
- No resolution of the joint-consent provenance gap for the 2026-11-05 B1 decision record; the gap remains visible.
- No use of retired mutation catalogues, schedules, counts, or assignments as facts; no amendment of frozen blind E3.
- No numerical parameter values, effect sizes, power, or minimum-effect claims are invented by this specification.

## 11. Compliance map

| Requirement | Where |
|---|---|
| A. Symbolic population; retired allocations not inherited | §1 |
| B. B1 primary target is held-out prediction; P-assoc secondary; exact-cell baseline; common slope declared as assumption; predeclared cell-specific-slope sensitivity with per-cell estimable-support reporting | §6 |
| C. B1/M1 support separate; intersection not a gate; population and conditional probabilities distinct | §4–§5 |
| D. Valid three-category multinomial model; parent dependence; no truncation; family-effect limitation declared | §2 |
| E. Unified affinity path; set-valued limit; D/T regime audit; tie perturbations in free coordinates; N1–N4 incl. N3 within-cell parent-quality pathway | §2.5, §7 |
| F. One primary inferential target (\(\Delta LL\), descriptive until the B1 analysis plan is frozen, then two-sided \(\alpha=0.05\)); no unadjusted second confirmatory test | §6.1 |
| Correct cell-envelope formula with exact-maximum construction (Claude-verified) | §3.2 |
| DP recurrence and complexity bound | §5.3 |
| Fold-level within-cell slope estimability, equal-parent predictive scoring, and declared B1-analysis-plan scope | §6 |
| M1-gen authority and M1-si/M1-ci decomposition | §4.2 |
| Held-out bank always identified as development data; consent-provenance gap visible | header, §1, §10 |

---

**End of Rev 1.4.** This revision is **published on the review branch** `gpt/b1-m1-rev1.2-review-chain-2026-11-14` as an unreviewed draft — **not accepted, not frozen, and not merged to `master`**. Per the recorded process: Claude reviews Rev 1.4 independently; GPT adjudicates. **Three distinct review events, kept separate:** (i) *byte verification* — Rev 1.3 at commit `bb4feb1` (Claude), and Rev 1.4 Amendment D at commit `52ba3db` (GPT: SHA-256 `C5955DD0…EE7967` matched against the commit-pinned raw file; Claude's byte verification of this Amendment E text is pending); (ii) *content review* — the ties-vs-regime correction (Amendment B), the free-coordinate tie statement with the explicit finiteness/finite-union step, the rewritten inference paragraph (§6.1), the declared common-slope assumption and B1-analysis-plan scope, the N3 interpretation and proxy-pathway check (Amendment C), and the N4-a finite-sample-variability wording and its deferred operationalisation (Amendments D–E) have passed content-level review by both reviewers to date; (iii) *final acceptance* — pending, and issued only after the byte-verified file-level review of this complete text. The separate B1 analysis plan is the next deliverable after Rev 1.4's disposition. No numerical evaluation, predictive fitting, simulation, construction, allocation, or bank reuse is authorized; that requires a further explicit GO after acceptance of the mathematics and the analysis plan.
