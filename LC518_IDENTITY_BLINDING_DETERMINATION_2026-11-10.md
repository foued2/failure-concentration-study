# LC518 — Identity-blinding determination (response to GPT §5 item 2, 2026-11-10)

**Date:** 2026-11-10
**Author:** Claude (assigned: "independently challenge the identity-blinding alternatives and determine whether either can preserve the frozen B1 estimand")
**Status:** review record. Simulation remains paused; nothing here authorizes execution, unblinding, or a new analysis pass. Owner decisions are identified, not taken.
**Sources examined:** `LC518_CONCENTRATION_ESTIMAND_REVIEW_2026-11-05.md` §5 (the open owner questions, B1/B2 fork, governing constraints); `.qoder_reviewdraft.md` §1 (question 1), §3.1–3.3 (Models A/B/C), :132 (sealing clause), :309–316 (carried-forward protections), §8 (feature reconciliation); `LC518_POPULATION_MODEL_AUDIT_2026-11-10.md` (F1–F4); `C9_GENERATION_SPEC_REVIEW.md` rev 2.6 is referenced by the reviewdraft but is **not present in the repository** — its sealing provisions could not be independently checked (see §6).

## 1. What the frozen documents actually specify

**The phrase "the frozen B1 estimand" has no referent.** Three things are frozen, and B1 is none of them:

1. **The frozen predictive estimand** is the blinded Model A vs Model B comparison: ΔLL with baseline predictors = the k_fail flexible basis, k_unresolved, and family Z (`.qoder_reviewdraft.md` §3.1–3.2). Mechanism identity appears in no model's predictor list.
2. **The frozen support reporting** is M1: within-parent, exact-(k_fail, k_unresolved)-cell criterion (§5.2).
3. **The B1/B2 fork is an undeclared owner question.** From the estimand review §5 item 2: B1 = "beyond individual mechanism identity," "potentially examinable — nominal incidence exists; identifiability conditional on A2-static (allocation, crossing), A3-dynamic (realized profiles), and the predeclared analysis"; B2 = "beyond exact pair composition, including dual-mutant pairs," "poorly supported by the 28+2 schedule … if B2 is essential, the schedule is presumptively inadequate pending redesign." Verdict: "The owner must declare which is required. Silence blocks the record; choosing B1 without declaring it would quietly narrow the claim." Claim B itself is likewise unratified (§5 item 1).

Two further grounding points GPT's §3 needs:

- **The sealing clause literally names only Model C** (`:132`: "Model C does not receive sealed mutation identities, mutation descriptions, version-role labels, …"). Models A/B exclude identity by predictor enumeration, not by an explicit blinding statement, and the four carried-forward protections (§:309) do not address identity at all. The blind E3 pass is, however, a governed object (estimand review, governing constraints: "the blind E3 pass is unchanged by any robustness stage"). So Approach A does not merely "add a predictor" — it touches an enumerated baseline, a governed blind pass, and an undeclared claim fork simultaneously.
- **Terminology collision:** the reviewdraft's decision status ("B1–B3, M2–M3 … corrections are consolidated") uses B1–B3 as *correction labels*, a numbering space entirely separate from the estimand review's claim fork B1/B2. GLM's item-1 wording audit must disambiguate these; a protocol that "keeps B1" could silently mean either.

## 2. Approach A — direct adjustment (baseline includes individual mutation identity q)

**Verdict: cannot preserve the frozen specification. It is an owner-amended design, viable only under four conditions.**

If adopted, it requires:

1. **Amendment of the frozen baseline for all three arms.** Model B and Model C are defined as "Model A plus …" (§3.2–3.3); changing A's predictor list changes every arm and the A-versus-C comparison.
2. **Explicit unblinding authorization.** Models would receive sealed mutation identities, reversing the :132 posture and touching the governed blind pass. Under the estimand review's constraint structure this needs a new owner decision, not a reviewer preference.
3. **Catalogue-level shared q.** A test parent's q indicator is unidentifiable if that q never appears in training. Under parent-grouped CV, Approach A is coherent only if q levels are shared across parents (GPT's own design restriction) and every fold's training set covers all q levels present in test — otherwise the one-frozen-pass protection forces NOT_ESTIMABLE. Fold-wise q coverage becomes a hard design constraint on any allocation.
4. **Prespecified singleton handling.** q levels realized by a single parent must be dropped or level-merged by a rule fixed in advance; dropping is not innocuous if singleton-q variants differ systematically in k_fail or C_D.

And one interpretive trap: with q in the baseline, the strength of the resulting "beyond identity" claim depends on the catalogue's q granularity. Coarse q leaves mechanism-level variation in the residual for C_D to absorb; fine q can absorb nearly all identity signal. The claim would be catalogue-granularity-dependent, which must be declared as part of the estimand.

## 3. Approach B — conditional evaluation (blinded models, ΔLL evaluated within identity strata)

**Verdict: preserves the frozen models, the frozen primary estimand, and the blinding regime verbatim — but it is an additive layer the frozen text does not contain, so it still requires ratification of four pinning decisions.**

Formal check: the fitted functions are unchanged; the conditional layer decomposes the evaluation of the same frozen pass. It therefore stays inside the one-frozen-pass protection **only if prespecified before the pass**. The four decisions:

1. **Stratum definition: q or m.** The frozen claim wording says "individual mechanism identity" — whether that means the broad mechanism (m) or the catalogue-level individual mutation (q) is precisely GPT's open m/q question, and the answer changes both the support requirements and the claim's meaning. The version→identity map must be pinned with it, including the SAB double mutant, which carries two mechanisms and cannot be assigned to a single q-stratum without a convention.
2. **Minimum within-stratum support.** A stratum carries no information if all its observations share one C_D value. Minimum form: ≥2 parents with ≥2 distinct C_D values inside the stratum. Whether the stratum must additionally lie inside one exact (k_fail, k_unresolved) cell — GPT's joint test — is a separate, stricter choice; the two must not be conflated. This is a new support layer, at least as demanding as M1 and compounding with it.
3. **Weighting.** The agreed statistic is per-parent mean ΔLL with equal parent weighting. Two harmonizations exist: (a) keep global equal-parent weighting and restrict the covered observations to supported strata — the conditional figure is then the global statistic over the identity-supported subset; (b) weight strata equally and parents equally within strata — a different, stratum-averaged estimand. Recommend (a) as the primary conditional figure with (b) as sensitivity; whichever is chosen must be fixed before the pass.
4. **Status and multiplicity.** If the frozen global A-vs-B remains primary and the conditional layer is interpretive, both must be prespecified and the conditional layer must not be promoted post hoc. If the owner promotes the conditional layer to primary, that is an estimand change and must be ratified as such.

Two technical caveats that the mandated negative control must cover: (i) the blinded models' omitted-identity bias does not exactly cancel within a stratum — under strong mechanism-to-stratum affinity, within-stratum ΔLL leakage is second-order but nonzero, so the β_C = 0 × strong-affinity scenario must be evaluated **both globally and within strata**; (ii) if few strata achieve within-stratum support, the conditional figure's coverage collapses and its parent weighting diverges from the global statistic — report coverage alongside every conditional result.

## 4. Determination

**Neither approach preserves "the frozen B1 estimand," because no operationalized B1 estimand exists in the frozen documents.** B1 is an undeclared claim fork; what is frozen is the blinded A-vs-B primary, the M1 reporting, and the sealing regime. The owner's actual decision tree:

- **(a) Owner leaves the fork as is (or declares B2):** no amendment needed. The frozen structure already operationalizes "beyond (k_fail, k_unresolved, Z)"; identity is then handled by M1 support reporting plus the mandated negative-control scenario. B1 remains unclaimed, per the estimand review's rule that choosing B1 without declaring it would quietly narrow the claim.
- **(b) Owner declares B1 essential:** an amendment is unavoidable. Approach B is the lower-deviation route — frozen models and blinding untouched, additive layer, four pinning decisions above. I endorse GPT's preference for B as first proposal, conditional on those four being pinned. Approach A is the higher-deviation route — it modifies all three arms, reverses a governed blinding posture, and is coherent only with catalogue-level shared q and demonstrable fold-wise q coverage.
- **What does not depend on this fork:** the data requirement. All routes need the same joint support structure — within-parent version pairs, coinciding on exact (k_fail, k_unresolved) cells, inside shared identity strata. The approaches differ in what claim the analysis can license, not in what data they need. Consequently the paused population-model rebuild can proceed **before** the owner resolves A-vs-B, provided the simulation logs the full joint incidence structure (parents × versions × cells × identities) rather than a single support scalar, so that either estimand resolution can be evaluated against the same generated populations.

## 5. Verification of GPT's Cases A and B

Both illustrations are correct, with one precision point. Case A (M1 passes, mechanism-conditioned layer fails) passes M1 only under the frozen cell, which does not condition on m — and only if the three parents' version pairs coincide on the **same exact (k,u) cell across parents**, not merely within each parent. If the case is read as within-parent coincidence alone, M1 does not pass (different cells). Case B (cross-parent variation, no within-parent variation) correctly fails M1. The joint test in GPT §2 is the correct intersection structure; note it compounds: per-parent in-cell version pairs, ≥3 parents coinciding on the same (k,u), *and* shared identity conditioning — each factor dilutes cell masses further (audit §2 F3), which is why the identity stratum must be shared across parents by construction for the joint test to be reachable at all.

## 6. Sources not independently checkable

`C9_GENERATION_SPEC_REVIEW.md` rev 2.6 is cited by the reviewdraft as pinning the C9 held-out-first protocol, but the file is not present in the repository working tree. Statements attributed to it (including any sealing provisions it may contain) were not verified here. Provenance of that document should be confirmed before the rebuilt population model is reviewed against it.

## 7. Provenance corrections and responses to GPT's four decisions

**Provenance.** Two items in GPT's message are attributed to GLM but originated in my audit record: (i) the "approximately 12 parents per family" figure is the illustrative arithmetic in `LC518_POPULATION_MODEL_AUDIT_2026-11-10.md` §2 F3, with assumptions: Poisson(λ) totals per parent, λ ∈ {3, 5, 8, 12}; k_unresolved ≡ 0 (the single most favorable case — any unresolved mass splits cells further); evaluation at the modal cell only; binomial P(≥3 of n_z parents in that cell), giving n_z = 12 → 0.53 / 0.35 / 0.23 / 0.15 and n_z = 6 → 0.13 / 0.07 / 0.04 / 0.02 for λ = 3 / 5 / 8 / 12. GPT is right to refuse adoption: it is a placeholder demonstrating the eligibility–realism tension, not a population-size requirement. (ii) The eight-input list in audit §7 is likewise mine, and its split stands: items 1, 2, 5, 7 are owner decisions (cell/support-metric fork; catalogue status; fitted-baseline pin; sidedness), items 3, 4, 6, 8 are GPT-draftable.

**The four decisions:**

| Decision | Response |
|---|---|
| Keep frozen M1 primary; do not relax | Endorse. Matches audit F1; relaxation would need owner ratification in any case. |
| Mechanism catalogue provisional; inherit nothing | Endorse. Consistent with register §7 (no allocation content from convenience) and with estimand review §5 item 3 (supply the annex or formally drop the mutation design — that owner action is what creates the catalogue). |
| Preserve blinding only if conditional evaluation is defined and feasible | Endorsed as first proposal per §3–4 here, with the four pinning decisions (stratum definition incl. m/q and the SAB mapping; minimum within-stratum support; weighting; interpretive status) and the two-variant negative control (global and within-strata). Approach A only under explicit owner amendment. |
| Two-sided α = 0.05 primary; one-sided as labelled sensitivity | Endorse. Resolves the sidedness discrepancy flagged in the audit §5. Consequences: planning multipliers are the two-sided columns (exact paired: df 11 → 3.08, df 29 → 2.90, df 59 → 2.85); the rebuilt `simulate.py` must switch its critical value from one-sided 1.6449 to the df-appropriate two-sided t quantile, keeping the one-sided table under a separate label. |

One constraint on the rebuilt population model (GPT §5 item 3): "five versions per parent" must respect that S0 is intended-correct and carries k_fail = 0, so it never enters any k_fail ≥ 2 cell; the mutation-bearing versions (SA, SB, SAB, S-extra) are the only M1 candidates, and their identity mapping must be pinned before version-pair incidence means anything.

## 8. Amendment 2026-11-11 — authorship evidence, relabeling, B1-fork status, and C9 verification

**Added in response to** the owner-relayed Claude review of 2026-11-11 (three problems) and GPT's 2026-11-11 verification message. This amendment qualifies §1–§7 above without rewriting them. Nothing here authorizes execution, unblinding, or simulation.

### 8.1 Authorship (Problem 2) — evidence recorded, Author line retained

The relayed review states this record was written in the GLM session and asks that the Author line be corrected. Evidence gathered before amending:

- The on-disk file is **byte-identical** to the content written in the Claude/Qoder CLI session on 2026-11-10 in response to GPT's turn-3 assignment ("Independently challenge the identity-blinding alternatives…").
- The file's mtime was touched 2026-11-11 07:19 with **no content change** — consistent with a record-keeper pass (GLM's recorded role) or an editor opening the file, not with a different document being written.
- The 2026-11-05 review branch (`origin/gpt/lc518-claim-b1-primary-2026-11-05`, `46189b4`) documents a **GLM local write set** consisting of the untracked root-level `LC518_CONCENTRATION_ESTIMAND_REVIEW_2026-11-05.md` and a modification to `REPOSITORY_STORAGE_INVENTORY_2026-11-05.md`. The estimand review — not this determination — is the GLM-authored record (its header lists "GLM / Qoder CLI (record-keeper: … this consolidation)").

**Resolution:** the Author line remains Claude, now supported by the evidence above. If a separate GLM-session determination document exists elsewhere, its metadata should be corrected in that document; the owner can point to it and this record will note the cross-reference. The relayed three-problems review is recorded as Claude's in `LC518_CLAUDE_REVIEW_IDENTITY_DETERMINATION_2026-11-11.md`, per the reviewer's instruction.

### 8.2 Hypothetical-design relabeling (Problem 1; accepted by GPT)

Every closed-design structural statement in this record — the eight mechanisms, C(8,2) = 28 pair types, the 28+2 schedule, the five-version parent structure (S0/SA/SB/SAB/S-extra), no within-parent replication, 7–9 parent groups per mechanism, 30 parents, 150 variants, and §7's final paragraph — describes a **proposed, unratified, annex-dependent design**. These are hypothetical design parameters, not facts about the study. The mutation annex is unsupplied and the design unratified (estimand review §5 item 3; register §7). The B1/B2 fork quotations in §1 item 3 inherit this label for every structural quantity they mention.

### 8.3 B1-fork status correction

§1 item 3 and §4 describe the B1/B2 fork as an undeclared owner question, on the authority of the local estimand review. The same-day review branch supersedes that in part: `lc518-150/review-v1.2/AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` (tip `46189b4` on `origin/gpt/lc518-claim-b1-primary-2026-11-05`) records the owner's verbatim delegation ("YOU AND CLAUDE DECIDE BASED ON YOUR REACHED AGREEMENT. … DONT ASK ME. YOU TWO DECIDE ONCE YOU REACH AGREEMENT."), a GPT–Claude agreement on **B1 as primary target** (B2 deferred, Claim A not adopted), and — in intermediate commit `f2303ad` — "Effective delegated agent decision … No separate owner ratification is required," downgraded in the final text to "GPT–Claude agreement … Whether further owner review is needed is a matter for the owner, and this record does not settle it." The fork is therefore **agent-decided under a recorded owner delegation**, with the final record itself leaving owner review open, and the branch record's own exact-text consent loop unclosed in the repository. The owner should confirm the delegation stands or supersede it; until then GPT's current "formal owner declaration still required" is the conservative reading, and §4's framing stands as amended rather than as originally written. The local estimand review's "owner must declare" wording reflects the state **before** the delegation commits (20:43–21:04 on 2026-11-05) and is stale on this point.

### 8.4 Third identity-handling architecture (amends §4(b))

The recorded B1 lane is neither Approach A nor Approach B as defined in §2–§3: a **separate unblinded conditional comparison**, with sealed identities admissible "as conditioning strata and, if specified before outcomes, as nuisance terms," and the natural contrast named as a baseline (flexible k_fail basis, k_unresolved, Z, individual-mechanism identity) versus the same model plus C_D. It avoids Approach A's objections 1–2 (no amendment of the frozen arms' baseline; no unblinding of the governed blind pass — it is a new lane with its own analyst and access rules) but inherits objections 3–4 and the granularity trap of §2. Approach B (conditional evaluation of the frozen blinded models within strata) remains inside the recorded envelope ("as conditioning strata") but is not the contrast the record names as natural. The §3 four pinning decisions apply to either variant; the m/q disambiguation remains open (the record says "individual mutation mechanism" without splitting broad mechanism from catalogue identity); and the SAB stratum convention is needed only if SAB is admitted to a stratum — under the recorded architecture SAB is **outside the primary B1 population**, with S0 a control and not an identity stratum, and 90 singly mutated versions a design count, not a realized count.

### 8.5 M1 relabeling

"Frozen M1" throughout this record means rev 2.6 §5.2 of the review draft — review-only and unratified (`.qoder_reviewdraft.md:5`). Which owner-approved specification carries M1 forward is an owner question. The 2026-11-05 branch record itself names M1 "a separate within-parent rule" that "does not by itself establish within-mechanism-and-within-family support" — the separate-tests architecture (M1 on `(k_fail, k_unresolved)`; B1 identity support on `(individual identity, family Z, k_fail, k_unresolved)`) that GPT re-proposed on 2026-11-10 with "Do not merge the two rules."

### 8.6 §5 relabel

§5's closing observation — "the identity stratum must be shared across parents by construction for the joint test to be reachable at all" — is a **design requirement on any allocation**, not a property of the (hypothetical) frozen allocation. Likewise §5's reference to "the frozen cell" describes the reviewdraft's proposed cell, per §8.5.

### 8.7 §6 superseded — C9 verified locally

The §6 unverifiability is closed. Verified 2026-11-11 in the local object store: commit `511bc2099ecff74b4f850b169ceef7f853c334a0` and blob `bd9f13fee63ee2716345447461bf3b8bcd904eaa` both resolve; the path `lc518-150/review-v1.2/analysis-revision-2026-11-02/C9_GENERATION_SPEC_REVIEW.md` exists on `origin/gpt/lc518-150-analysis-review-2026-11-02` and `origin/gpt/lc518-claim-b1-primary-2026-11-05`, and does not exist in `master` or `HEAD` (branch tip `3e7c66d`). Content: "Consolidated review revision 2.6, 2026-11-02," generation-side only (per-stratum draw orders, rejection reason codes, held-out-first protocol), marked "not owner-ratified or frozen," with an explicit authority boundary and a statement that no bank was generated in its preparation. **It contains no M1 rule and no mutation-identity sealing provisions** — the only identity-sealing text on the analysis side remains reviewdraft `:132` (Model C). This corroborates GPT's independent GitHub fetch and corrects the §6 assessment: C9 rev 2.6 existed historically as a review-only, generation-side document, is absent from master and this branch, and its absence does not undermine the sealing analysis in §2, which never relied on C9.

### 8.8 Bearing on §4's recommendations

§4(b) stands in amended form: if B1 governs, an amendment or additive layer is unavoidable, and the recorded 2026-11-05 lane (§8.4) is a third route — lower-deviation than Approach A, complementary to Approach B — whose four pinning decisions of §3 still apply. §4's final paragraph (the population rebuild can proceed before the fork is resolved, provided the simulation logs the full joint incidence structure) stands, with the incidence fields extended to GPT's 2026-11-10 deliverable spec: per-record (parent, version, q, m, pair composition p, family z, k_fail, k_unresolved, C_D), M1 and candidate B1 support evaluated independently, then joint feasibility — and with every structural number, including those in the 2026-11-05 branch record, treated as hypothetical design parameters per §8.2.
