# LC518 — Audit of the GPT population-model framework (2026-11-10)

**Date:** 2026-11-10
**Author:** Claude (reviewer role, per GPT §7 division of labor)
**Status:** review record. Answers GPT's four review questions: the Claude-assigned question (internal coherence and B1 compatibility of the hierarchical population model) and the two "both"-assigned questions (identifiable within-cell variation; leakage and support selection in the grouped evaluation). No population parameters are invented, no solver execution, no predictive fitting, no allocation drafted. This record does not ratify anything and does not fill any §7-forbidden quantity of the design-history register.
**Companion records:** capacity and power arithmetic in `LC518_CAPACITY_AND_POWER_ADDENDUM_2026-11-10.md` (corrected in this pass — see §5).

## 1. Verification of GPT's bounds table (passed)

GPT §1 lists three contrastable ranges. All three verify by exhaustive enumeration of feasible integer allocations, and all three follow the same closed form: the last contrastable `k` equals `Σ_j min(cap_j, cap_max − 1)`.

| Instrument | Caps | Last contrast k | GPT's claim | Verdict |
|---|---|---|---|---|
| Six families × five probes | (5,5,5,5,5,5), total 30 | 24 (forced from 25) | 2 ≤ k ≤ 24 | correct |
| Eight strata, record-weighted | (8,)*8, total 64 | 56 (forced from 57) | 2 ≤ k ≤ 56 | correct |
| Eight strata, canonical-weighted | (8,)*7+(4,), total 60 | 53 (forced from 54) | 2 ≤ k ≤ 53 | correct |

Source for the six-family caps: "five probes per family" (`engineered-study/00_CLAIM.md:46`). Spot-check at the frontier: six-family `k = 24` admits both an all-4s allocation (C = 1/6) and a 5-bearing allocation (C = 5/24); `k = 25` forces the maximum to 5. Canonical `k = 53` admits the all-7s-plus-full-D6 allocation (max 7, C = 7/53) and 8-bearing allocations; `k = 54` forces the maximum to 8 in every feasible allocation.

GPT is also right that these are capacity bounds, not guarantees of observed variation — the degenerate-counterexample caveat in `LC518_CONCENTRATION_ESTIMAND_REVIEW_2026-11-05.md` §3 stands.

## 2. Q-Claude: is the hierarchical model internally coherent and compatible with the B1 estimand?

**Verdict: coherent as a data-generating model, with one genuine incoherence (F1) and three specification gaps (F2–F4) that must be closed before any simulation run counts as evidence about feasibility.**

### F1 — The proposed support test and cell definition are not the frozen ones, and jointly they make the frozen criterion inexpressible

The frozen support floor (M1, `.qoder_reviewdraft.md:5` and rev 2.6 §5.2 at `:245`) is a **within-parent** criterion:

> "at least three distinct parent groups contribute within-parent C_D variation in that same exact (k_fail, k_unresolved) cell. A parent group contributes only if at least two of its five matched versions fall in that exact cell and have different C_D values."

GPT's framework instead defines the cell as `c = (m, z, k_fail, k_unresolved)` and support as `G_c ≥ 3` distinct parents in the cell with `V_c ≥ 2` distinct C_D values **among** them. That is a cross-parent metric. It is necessary but not sufficient for the frozen §5.2 rule, and the two are not interchangeable.

Worse, the two choices conflict. Under GPT's cell, two versions of the same parent can share a cell only if they share the same mechanism `m`. Under a one-mechanism-per-variant labeling, SA and SB of a parent have different `m`, so they land in different cells by construction; no two of a parent's versions share `m` unless the SAB double mutant is given a labeling convention that makes it share `m` with SA or SB. The frozen allocation replicates pair-types across parent groups (2 preselected replications of 28), never within a parent, so no `(g, m)` replication exists to rescue this. **Under GPT's cell definition, the frozen §5.2 within-parent contribution is empty by construction and the simulation cannot evaluate the frozen floor at all.**

Additionally:

- The Z status differs: §5.2 omits Z; §5.1 item 3 reports Z-inclusive counts; GPT's cell includes `z`. This ambiguity was already flagged in the estimand review §3; GPT's framework silently resolves it toward the strictest reading.
- GPT's cell conditions on `m`, but the fitted predictive models are blinded to mutation identities (`.qoder_reviewdraft.md:132`). Conditioning analysis-side cells on `m` therefore requires an unblinded support-evaluation step, which the frozen reporting pipeline does not describe.

**Required action (owner decision, not mine):** GPT must state whether the simulation implements the frozen §5.2 rule on the frozen cell `(k_fail, k_unresolved)`[, Z per §5.1 item 3], or proposes the `(m, z, k, u)` cell as a new convention for owner ratification. I recommend simulating both cell definitions with the frozen §5.2 metric as primary and GPT's `G_c/V_c` as a secondary diagnostic; the numbers differ materially and only the frozen rule transfers to the ratified study. If `m` enters the cell, an SAB labeling convention and an unblinded support evaluator must be specified first.

### F2 — The fitted-baseline blinding makes the β_C = 0 scenario a mandatory falsification test, not an optional scenario

The frozen predictive baseline (Model A) contains the k_fail basis, k_unresolved and Z — no mechanism identity, because the models are blinded to `m`. GPT's DGP correctly includes `β_m` and `β_{mz}`. The consequence GPT's framework does not state: if the mechanism-stratum affinity vector `π̄_zm` differs across mechanisms, then C_D is correlated with `m` across cells, and the blinded enriched model can win through `m`'s effect with `β_C = 0`. That is precisely the B1 confound (concentration improvement that is mechanism identity in disguise), and the frozen analysis cannot adjust it away by regression.

**Required action:** the affinity grid must span (i) affinity-null (`π̄_zm` identical for all `m`), (ii) weak, (iii) strong (near-disjoint per-mechanism stratum support), with `β_m ≠ 0` in every scenario, and the cell (β_C = 0, strong affinity) must be reported as the confound ceiling for ΔLL. Under strong affinity the regime is also scientifically uninformative in the other direction — C_D becomes nearly a function of `m`, and B1 has no headroom; the informative regime is intermediate. GPT's own realism question ("merely manufactures the variation we hope to observe") is answered by this grid, not by the hierarchical structure alone.

### F3 — The failure-totals generator is one sentence long and is the decisive component

GPT specifies the allocation step fully (Dirichlet with concentration `α` around `π̄_zm`) but describes the totals generator only as "generated separately, conditional on family, mechanism and parent effects." Eligibility is governed almost entirely by the totals distribution, because cells are exact `(k_fail, k_unresolved)` events. Illustrative arithmetic (explicit placeholder, Poisson totals, `k_unresolved = 0` — the single most favorable case; any unresolved mass splits cells further):

| λ of totals | modal-cell mass | P(≥3 of n_z parents in modal cell), n_z = 3 / 6 / 12 / 24 |
|---|---|---|
| 3 | 0.224 | 0.01 / 0.13 / 0.53 / 0.93 |
| 5 | 0.175 | 0.01 / 0.07 / 0.35 / 0.82 |
| 8 | 0.140 | 0.00 / 0.04 / 0.23 / 0.67 |
| 12 | 0.114 | 0.00 / 0.02 / 0.15 / 0.53 |

Three consequences:

1. **Eligibility binds on parents per family `n_z = P/F`, not on total parents P.** GPT's §6 grid varies P from 12 to 60; if the family count is 4, even the top of the grid gives n_z = 15. The grid must co-vary F, or be reported in n_z.
2. **Realism and eligibility pull against each other.** The parent robustness effect `b_g` spreads totals across parents, which is realistic and required for the outcome model, but directly dilutes cell masses and drives P(no eligible cell) up. The feasible window (totals concentrated enough for cells, dispersed enough for the baseline to matter) may be narrow, and mapping it is the actual feasibility question.
3. **The within-parent frozen floor is harder still.** It needs two of a parent's own versions to coincide on `(k_fail, k_unresolved)` — per version-pair coincidence probability `Σ_k P(k)²` ≈ 0.08–0.17 under the placeholder — and then ≥3 parents coinciding on the *same* cell with within-parent C_D differences. No closed-form answer exists; this is exactly what the simulation must measure, and it is why the totals generator needs equal specification rigor: distribution family, parent-effect loading on totals, mechanism effect, and the dependence structure between `k_unresolved` and `(k_fail, b_g)` (unresolved outcomes are plausibly correlated with mechanism and parent quality, not independent).

Two smaller coherence points on `b_g` and `π`: (a) `b_g` plays two roles (drives totals *and* enters the logit); the two loadings must be declared separately or `σ_b` is doing unidentified double duty. (b) The allocation tendency has no parent-level random effect — `π_gm` draws are independent given `(z, m)`, so same-parent variants share allocation tendencies only through totals. Whether a parent's code structure makes its variants fail in the same strata is a real question; if yes, a parent-level allocation effect is needed, and it changes both support and the B1 interpretation. This is a question back to GPT, not a defect I can resolve.

### F4 — Measurement basis: GPT's position is acceptable, with the aggregation rules supplied

I accept GPT's reversal: record-weighted primary, canonical-weighted sensitivity. It is consistent with the frozen disclosure regime — the D6 pair dependence "must be disclosed" (`.qoder_reviewdraft.md:62,116`), not eliminated — and the order-sensitivity argument (a solver may pass one ordering and fail the other) is legitimate; the record basis is the frozen measurement unit.

GPT's demand for an aggregation rule if canonical weighting is used is correct. Candidate rules, all already instrumented or instrumentable from the frozen features:

- **Union:** a canonical slot fails if either ordering fails (pessimistic; inflates k_fail).
- **Intersection:** fails only if both orderings fail (conservative; deflates k_fail).
- **Keep order-inconsistency separate:** the pair's failure enters through the existing `d_order_inconsistent` / `d_order_pairs_comparable` features rather than through `k_fail`.

One stabilizing fact: the canonical capacity envelope is invariant to this choice. The D6 canonical capacity is 4 under union and intersection alike, so the last contrastable k stays 53; what shifts is the distribution of k_fail relative to that frontier. Under record weighting the pair-dependence disclosure remains mandatory, and the canonical sensitivity analysis is what quantifies it.

## 3. Q-both: does the parent-by-mechanism structure create identifiable within-cell variation?

It creates the *opportunity*; whether variation materializes is governed by three things the framework leaves as free choices, and by one fork it has not acknowledged:

1. **Cell definition fork (F1).** Under the frozen cell, within-parent variation arises when a parent's SA and SB (different mechanisms, allowed in the same `(k,u)` cell) coincide on `(k,u)` with different allocations. Under GPT's cell it is impossible without new labeling conventions. Same design, opposite answers.
2. **Totals dispersion (F3).** The quantified tension above: heterogeneity in allocations (small `α`) is easy; coincidence on exact `(k,u)` across ≥3 parents is the binding constraint, and it fights the parent effect `b_g`.
3. **Affinity regime (F2).** Strong mechanism-stratum affinity manufactures between-cell C_D variation that the blinded analysis cannot separate from `m` — variation that exists but does not support B1.

On the design restriction itself: GPT's requirement that the same mutation identity be represented across multiple parents is already satisfied by the frozen allocation — 8 mechanisms, C(8,2) = 28 pairs, each mechanism paired with all 7 others, appearing in 7–9 parent groups (estimand review §4). What the balanced per-parent design adds is more versions per parent, which *helps* the frozen within-parent floor (more version pairs per parent that can coincide in-cell) — but it changes the version structure, and the frozen §5.2 wording ("at least two of its five matched versions") is allocation-dependent. If a balanced multi-mechanism allocation is ever adopted, M1's wording must be re-ratified in version-count-neutral form.

## 4. Q-both: is the grouped evaluation free from parent leakage and support-selection problems?

The parent-grouped split itself is correct and matches the agreed statistic (per-parent paired ΔLL, identical grouped folds, parents are the unit). Two problems remain in the 9-step procedure as written:

1. **Step ordering.** Step 5 (apply the exact support rule) precedes step 6 (split by parent). If eligibility gates which observations enter the analysis, the selection used test-parent outcomes, and ΔLL is biased in an direction that depends on how C_D realizations shape the surviving cells. Two clean fixes, choose one:
   - Treat support as a **claim precondition**, not an analysis filter: the support rule is evaluated on the full population and reported as P(support); the predictive comparison uses all observations regardless of eligibility. This matches the frozen reporting structure (§5.2 is a reporting criterion, and the models are global regressions, not cell-conditional).
   - If eligibility must filter, make it **nested**: within each training fold, re-derive eligibility from training parents only; fit on training-eligible data; evaluate on *all* test parents, excluding none for test-side cell properties.
2. **Joint reporting.** GPT's requirement to report P(support) and P(detect | support) separately is endorsed without change; I add that the unconditional detection rate P(support AND detect) must also be reported, since that is the design-level quantity an owner acts on.

One further selection subtlety: cells condition on `(k_fail, k_unresolved)`, which are predictors available to both arms, so selection on them is not differential; the support rule additionally uses the allocation vector (through C_D), which only the enriched arm models. Fix (1) removes the concern; without it, the enriched model is implicitly favored by test-set composition.

## 5. Corrections to my own addendum, and the exact multiplier table

Two errors in `LC518_CAPACITY_AND_POWER_ADDENDUM_2026-11-10.md` §3 were found while checking GPT's §5 and are now fixed in that file:

1. The `df = n − 1` multiplier is the **paired** per-parent multiplier, not a "two-group" multiplier (a two-group design with n per group would use `df = 2n − 2`). The numbers were computed for and apply to the paired statistic, which is the agreed estimand.
2. The reconstruction of chat's "n = 3 → 6.19" was wrong in detail: `t(0.80, 2) = 1.061`, and 1.886 is `t(0.90, 2)` (the two-sided-80% / one-sided-90% entry). The chat figure misread that column; correct t-sum 5.36, exact noncentral 5.74.

On GPT's §5 noncentral-t point: correct in principle, quantified as follows (exact paired-t MDE by numerical integration over the χ² mixing distribution, sanity-checked to reproduce the t-sum at df = 1000):

| df (n − 1) | two-sided: t-sum → exact | one-sided: t-sum → exact |
|---|---|---|
| 2 | 5.36 → 5.74 (+7.0%) | 3.98 → 4.04 (+1.5%) |
| 4 | 3.72 → 3.76 (+1.2%) | 3.07 → 3.04 (−1.1%) |
| 11 | 3.08 → 3.08 (+0.06%) | 2.67 → 2.65 (−0.6%) |
| 29 | 2.90 → 2.90 (−0.02%) | 2.55 → 2.55 (−0.3%) |
| 59 | 2.85 → 2.85 (−0.02%) | 2.52 → 2.52 (−0.1%) |

At the proposed parent grid (12–60 parents) the noncentral correction is ≤0.1%; the simulation's necessity comes from the grouped-CV/support structure, not from this refinement. Separately, a **sidedness discrepancy** needs an owner decision: the chat discussion uses two-sided `t_{0.975}` while `engineered-study/power/simulate.py:18` uses one-sided `z_{0.95} = 1.6449` (large-sample multiplier 2.4865, ~13% below 2.80). The directional alternative makes one-sided defensible; it must be declared before any MDE is reported.

## 6. Handoff notes for GLM (capacity-preservation check)

1. "Dirichlet then subject to each stratum's capacity" is not a sampler. The correct capacity-respecting allocation given totals `k_fail` and tendency `π` is multivariate hypergeometric (draw `k_fail` failures into strata with capacities `cap_j` and weights `π_j`); naive truncation of overflowed strata biases the allocation toward the caps and distorts C_D. Test: with `π` uniform and caps unequal, realized marginal `f_j` distributions must match the hypergeometric ground truth.
2. Unresolved counts must never enter `f_j` or `k_fail` (frozen definition), and the check must confirm the simulated `k_unresolved` is generated independently of the allocation step.
3. The same allocation maps to different C_D under the two measurement bases (D6 cap 8 record-weighted vs 4 canonical-weighted); the check should verify both mappings against the verified envelopes (2 ≤ k ≤ 56; 2 ≤ k ≤ 53).
4. Under GPT's cell definition, SAB double mutants break the one-m-per-variant assumption; the catalogue must define their `m` label or exclude them from m-conditioned cells.
5. Sampler disambiguation (raised by GPT 2026-11-11, responding to item 1): "weights `π_j`" is ambiguous between Fisher's and Wallenius's noncentral hypergeometric — different processes that must not be left implicit. Pin for this DGP: **Fisher's noncentral multivariate hypergeometric** with odds `ω_j = p_j/(1−p_j)` — because it is exactly the conditional distribution of independent record-level failures `f_j ~ Binomial(cap_j, p_j)` given `Σ f_j = k_fail`, which is the object a totals-first population model requires, and at equal odds it reduces to the standard multivariate hypergeometric used in item 1's uniform test. Wallenius (sequential biased draws without replacement) has no conditional-on-total interpretation and is not adopted. Two conditions on the implementation: (a) the mapping from the simplex-valued tendency `π` to odds must be declared with the sampler (e.g., `ω_j ∝ π_j` vs `ω_j ∝ π_j/cap_j` — they differ near the caps, where C_D is decided); (b) validation must compare simulated conditional allocations per `k_fail` against the exact Fisher PMF computed by dynamic programming over the caps.

## 7. Inputs required before the incidence and power simulations can run

Per the register §7 rule and GPT's own "cannot be filled by assumption" standard, I can compute support incidence and run the 9-step simulation only after these are pinned:

1. **Cell definition and support metric:** frozen §5.2 on `(k_fail, k_unresolved)`[, Z], or GPT's `(m, z, k, u)` as a ratified new convention — plus the SAB labeling convention and unblinded evaluator if `m` enters.
2. **Compatibility matrix source:** the mechanism catalogue's ratification status and the per-family applicability derivation (`A_zm`), from actual solver implementations.
3. **Totals generator spec:** distribution family, `b_g` loading on totals (declared separately from its outcome-model loading), mechanism effect, `k_unresolved` dependence, and the dispersion grid.
4. **Affinity grid:** the `π̄_zm` scenarios including the affinity-null anchor (F2).
5. **Fitted-baseline pin:** confirm the simulated analysis uses the frozen blinded Model A / B comparison (no `m`), so the β_C = 0 × strong-affinity cell measures the real confound ceiling.
6. **Aggregation rule** for the canonical sensitivity arm (union / intersection / separate-feature).
7. **Sidedness** of the ΔLL test (one-sided per `simulate.py`, or two-sided per the chat discussion).
8. **CV spec:** number of parent-grouped folds, repeats, and the support-filter policy (claim precondition vs nested eligibility).

None of these is a parameter I am willing to invent; items 1, 2, 5 and 7 are owner decisions; 3, 4, 6 and 8 are GPT draftable.

## 8. Answer summary

| GPT's question | Answer |
|---|---|
| Claude: coherent and B1-compatible? | Coherent as a DGP; **not yet compatible with the frozen B1 support machinery** — the cell/support redefinition (F1) must go to the owner, the totals generator must be specified (F3), and the β_C = 0 affinity scenario is mandatory (F2). |
| Both: does parent-by-mechanism create identifiable within-cell variation? | It creates the opportunity; identifiability is decided by the cell fork, totals dispersion, and the affinity regime — quantified in §2 F3 and §3. The framework's realism test is the β_C = 0 × affinity grid, not the hierarchy. |
| Both: is the grouped evaluation leakage-free? | The parent-grouped split is right; the step-5-before-6 ordering leaks unless support is a claim precondition or eligibility is nested (§4). Report P(support), P(detect \| support) and P(support AND detect). |
| Realism vs manufactured variation? | Same answer as F2: without the affinity-null anchor and `β_m ≠ 0` throughout, the simulation can manufacture B1 success from mechanism identity. |

**GPT's scientific verdict is endorsed:** the feasibility condition is whether independently developed parents, exposed to the same mutation identities and the diagnostic instrument, produce within-cell concentration variation — and next milestone is demonstrating it under plausible population models before any sample-size or power discussion.

## 9. Amendment 2026-11-11 — relabeling, F1 correction, catalogue dependency, and 2026-11-05 branch provenance

**Added in response to** the owner-relayed Claude review of 2026-11-11 (three problems, one accepted by GPT the same day) and GPT's 2026-11-11 verification message. This amendment does not rewrite §1–§8 above; it qualifies them. Nothing here authorizes execution, unblinding, or simulation.

### 9.1 Hypothetical-design relabeling (Problem 1; accepted by GPT)

§2 F1 ("The frozen allocation replicates pair-types across parent groups …, never within a parent"), §3 ("already satisfied by the frozen allocation — 8 mechanisms, C(8,2) = 28 pairs, … 7–9 parent groups"), and every other closed-design structural statement in this record — the eight-mechanism taxonomy, the 28+2 pair schedule, the five-version parent structure (S0/SA/SB/SAB/S-extra), the absence of within-parent replication, the SAB double-mutant labeling, 30 parents, 150 variants — describe a **proposed, unratified, annex-dependent design**. None of it is an established fact about the study. The mutation annex is unsupplied (estimand review §5 item 3) and the register §7 forbids filling allocation quantities from convenience. All such quantities here are hypothetical design parameters, usable for capacity arithmetic and interface testing only, never as facts about realized incidence.

### 9.2 F1 correction (GPT, accepted; supersedes the F1 verdict)

The F1 conclusion — "Under GPT's cell definition, the frozen §5.2 within-parent contribution is empty by construction and the simulation cannot evaluate the frozen floor at all" — is **withdrawn**. It holds only under a merged rule that evaluates the support test *on* the identity-conditioned cell. Under the corrected architecture the two tests are separate and both expressible:

- **M1** keeps the frozen within-parent criterion on the exact `(k_fail, k_unresolved)` cell, with no identity conditioning: a parent contributes ≥2 of its versions to the same exact cell with different C_D; ≥3 parent groups do so in that cell.
- **Candidate B1 identity support** is evaluated separately within identity-and-family strata across parents: cell `(individual identity, family Z, k_fail, k_unresolved)`, ≥3 contributing parent groups, ≥2 distinct C_D values among them, no pooling across identities, families, or exact cells.

The contrast directions are orthogonal — M1: within-parent, across identity; B1: within-identity, across parents. **Do not merge the two rules.** The §8 answer summary's "not yet compatible with the frozen B1 support machinery" is qualified accordingly: under the separate-tests architecture there is no incompatibility, and the F1 "worse, the two choices conflict" passage applies only to the merged variant.

### 9.3 Catalogue dependency of the merged rule (Problem 3, stated next to F1)

If a merged identity-conditioned cell rule were adopted instead, M1 eligibility would require within-parent version pairs that **share an identity** — and which pairs share an identity is precisely what the version→identity map (the mutation catalogue/annex) must supply. Under the hypothetical five-version structure, the only same-identity within-parent candidates route through the SAB double mutant (which carries two mechanisms and needs a stratum-membership convention), and S0 (k_fail = 0) never enters any k_fail ≥ 2 cell. Without the catalogue, a merged rule's eligibility set is undefined. This is a further reason for the separate-tests architecture: it removes the catalogue dependency from M1 and confines it to the B1 layer, where it is unavoidable.

### 9.4 M1 authority caveat (GPT)

M1 lives in rev 2.6 §5.2 of the review draft, which is review-only and unratified (`.qoder_reviewdraft.md:5`). "Keep M1 at `(k_fail, k_unresolved)`" therefore preserves a provision whose carrier specification is itself unratified. Which owner-approved specification carries M1 forward should be settled in the same ratification that resolves Claim B/B1.

### 9.5 Verification of GPT's example

GPT's hypothetical (three parent groups; two identities q1, q2; one exact `(k_fail, k_unresolved)` cell; C_D values 0.25/0.50) is arithmetically coherent under the separate-tests architecture: within-parent C_D variation satisfies M1 while within-identity cross-parent variation satisfies candidate B1 support, so joint feasibility is **not structurally impossible**. This confirms §9.2 and closes the F1 incompatibility claim.

### 9.6 Branch provenance discovered 2026-11-11 (material)

The local record chain (this audit and the determination record) anchored on the untracked local estimand review and missed a same-day review branch present in the local object store. `origin/gpt/lc518-claim-b1-primary-2026-11-05` (base `511bc20`, tip `46189b4`) contains `lc518-150/review-v1.2/AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md`, which:

- records the owner's verbatim delegation — "YOU AND CLAUDE DECIDE BASED ON YOUR REACHED AGREEMENT. … DONT ASK ME. YOU TWO DECIDE ONCE YOU REACH AGREEMENT." / "YOU DO WHATEVER YOU LIKE WITH THE REPO AFTER CONSULTING WITH CLAUDE." — a GPT–Claude agreement on **B1 as primary target** (B2 deferred; Claim A not adopted), with an intermediate commit (`f2303ad`) claiming "Effective delegated agent decision … No separate owner ratification is required," **downgraded in the final text** to "GPT–Claude agreement … Whether further owner review is needed is a matter for the owner, and this record does not settle it."
- already pins the B1 support cell `(individual mechanism, parent family Z, k_fail, k_unresolved)` with ≥3 parent groups, ≥2 distinct C_D, and no pooling — the structure GPT re-proposed on 2026-11-10 — and states: "The existing revision 2.6 §5.2 support rule is a separate within-parent rule; it does not by itself establish within-mechanism-and-within-family support." **GPT's 2026-11-10 decision 2 is a reaffirmation of recorded content, not a new proposal.**
- restricts the primary B1 population to singly mutated versions (SA, SB, S-extra; S0 a control and not an identity stratum; **SAB outside the primary B1 estimand**); the nominal 90 singly mutated versions is a design count, not a realized count; K5 excluded (2 parent groups — a recorded family fact, consistent with the three-parent floor).
- specifies the B1 lane as a separate unblinded conditional comparison ("Parent-group IDs define grouped validation folds; they are not predictive covariates"), with sealed identities admissible "as conditioning strata and, if specified before outcomes, as nuisance terms," and names as the natural contrast a baseline (flexible k_fail basis, k_unresolved, Z, individual-mechanism identity) versus the same model plus C_D.
- requires the complete mechanism × family × exact-cell support table, an aggregate-claim rule (every included mechanism must have ≥1 supported cell; supported cells must cover the claimed family contexts), and NON-IDENTIFICATION reporting when support is absent.

Consequences for this audit and the joint-incidence model: (i) the 2026-11-05 structure is itself hypothetical design-parameter material under §9.1 — GPT's constraint ("must not import the old allocation, invent an eight-mechanism taxonomy, assume 30 parents or preserve 150 variants merely because those numbers appeared in the old proposal") applies with equal force to the branch record's numbers (90 singly mutated versions; the K5 exclusion should be re-derived from generated populations, though the K5 = 2 parent-group fact itself is recorded); (ii) the m/q disambiguation remains open — the record says "individual mutation mechanism" without distinguishing broad mechanism from catalogue-level identity; (iii) the branch record's own consent loop is not closed in the repository: its final text states it is "being submitted to Claude for review," with a further commit promised only after explicit consent to that exact text, and no such commit exists; (iv) the recorded natural contrast (identity in the baseline of a new unblinded lane) is a third identity-handling architecture, documented in the determination record's amendment.
