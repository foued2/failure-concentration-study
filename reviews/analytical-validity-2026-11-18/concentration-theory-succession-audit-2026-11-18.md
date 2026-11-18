# Theory succession audit — what replaced the concentration question

**Date:** 2026-11-18
**Question audited:** after the original concentration question was posed, where did the programme go,
what was the concentration claim traded against, and which theory actually occupies its place now?
**Method:** the decision-bearing documents were read at their source (local files and remote branch
tips, `git show`), not summarized from other audits. Primary files named per section.
**Scope note:** this is a record audit. It adds no hypothesis of its own and authorizes nothing.

---

## 0. Direct answers

**Where did we go?** Through six formulations of the same claim, then into engineering.
v0.2 → v0.3-P (Phase 0, Rev A–G) → engineered-study H1a → mathematical spec + three-world simulation
→ construct-validity / H3 ranking formulation → LC518 Claim B1 + v0.21 M1-si. The last three of
these are design records; none produced data on the hypothesis. Since roughly 2026-10-25 the
programme's output has been banks, containment harnesses, manifests, hashes and governance
documents, not science.

**What was the theory traded against?** Not against a rival theory. It was traded against **four
control variables**, each of which absorbed the variation `C` was supposed to carry:

| # | The coordinate that took the variation | Where it was admitted |
|---|---|---|
| 1 | algorithm type / task identity | old Doctor; formulation note §4 |
| 2 | failure count `k` | v0.2 (`C = 5/k` on 1200/1200 rows) |
| 3 | family/carrier identity and defect identity | engineered-study Gate 1 |
| 4 | realization setting `a(v)` and mutation mechanism | LC518 v0.21, Claim B1 |

**What theory took place?** None that predicts anything. What took the place of the predictive claim
is a **methodological rule** — "no predictive test until `C` is shown to vary independently of the
design coordinates" — plus one **theorem** and one **reduction** that survived every review:

- **Theorem (settled):** a binary correctness decision cannot be improved by any failure-profile
  statistic, because `k > 0` already decides it and `C` is undefined at `k = 0`.
- **Reduction (settled):** at fixed `k`, `C = max_j f_j / k` is a monotone re-expression of
  `max_j f_j`, and `C` is a deterministic function of the full vector `F`. `C` therefore cannot
  contain information that `F` lacks.

The operative claim today is **B1** — the same hypothesis with four conditioning coordinates bolted
on, no population built, and a pre-committed "non-identification" verdict. That is a claim awaiting
a test, not a theory that has taken over.

---

## 1. The succession, formulation by formulation

| # | Date | Document | Claim as written | Compared against | What it gave up | Outcome |
|---|---|---|---|---|---|---|
| 0 | 2026-10 | `PROTOCOL.md`, `pilot/` | `C` predicts correctness beyond `k` | `k` only | — | INFEASIBLE (yield) |
| 1 | 2026-10-12 | `v02/` | `C` beyond `k` alone | `k` only | — | NEGATIVE, non-identifying |
| 2 | 2026-10-14 → 10-20 | `v03p/PHASE0_DESIGN_*` | "`C` predict[s] hidden-suite correctness beyond what failure count `k` already predicts, **when `k` and `C` vary independently**" | `k` only, but only on identified support | the unconditional claim; it now holds only where variation exists | never frozen (A/B/C/E open) |
| 3 | 2026-10-17 → 10-24 | `engineered-study/00_CLAIM.md` (H1a) | `C` predicts held-out **boundary score** at fixed `k`, "after accounting for `k` and generator identity" | `k` + generator identity | "correctness" → "score"; population → one task | Gate 1 CLOSED, 0 solvers |
| 4 | 2026-10-24 | `engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md` | predictive gain `Δ_pred` of `C` over `k` + `Z` | `k` + `Z`, and the full vector `F` | any claim that `C` carries more than `F` | W1 FAILED |
| 5 | 2026-10-25 | `concentration-formulation/02_..._NOTE_2026-10-25.md` | **H3**: within task × base-algorithm × `k`, higher `C` **ranks** candidates better; concordance vs 0.5 | chance ordering | any claim about a coefficient, and the ratio itself | proposed only |
| 6 | 2026-11-05 | `AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` | `C_D` carries information beyond `k_fail`, `k_unresolved`, **mechanism identity, parent family**, in one exact cell | four coordinates | generalizability; K5 excluded; pooling banned | no population built |
| 7 | 2026-11-16 | `POPULATION_AND_EXPERIMENTAL_DESIGN_..._v0.21.md` | same, on engineered variants inside real parents (M1-si) | + realization setting `a(v)` | natural-solver population | draft; 0 audits run |

Each step is a **narrowing**, not a replacement. The null hypothesis and the predicted direction
never changed: higher concentration → better held-out performance at fixed `k`. What changed is the
set of coordinates the claim is conditioned on, and the population it is allowed to speak about.

---

## 2. The one theorem that actually displaced something

`concentration-formulation/02_RESEARCH_FORMULATION_NOTE_2026-10-25.md` §3 is the only place in the
corpus where a proposition about concentration is marked **settled** rather than proposed:

> "A failing test is a counterexample, so a solver with `k > 0` is not universally correct, whatever
> its failure pattern. `C` cannot overturn that."
> "Passing a finite test set does not prove universal correctness, so B1 can accept wrong solvers.
> `C` is undefined at `k = 0`, so it cannot help there either."
> "**Consequence.** Concentration cannot improve B1's binary decision about universal correctness.
> This part is not a hypothesis."

This is what removed the original target. "Does C predict correctness?" has a trivial answer at both
ends: if `k > 0` the solver is already wrong; if `k = 0` there is no `C`. Any non-trivial version of
the question must therefore be about **graded** performance — score, loss, ranking — on inputs the
solver has not seen. Every later formulation is that retreat, made explicit.

The same move appears in the LC518 line: `C_D` is defined over "definite diagnostic failures", and
B1 asks about **held-out correctness** as a graded outcome, not universal correctness.

---

## 3. The one reduction that capped the claim

Two independent documents state the same mathematical fact, and it is the reason no honest version
of the claim can say "concentration is informative" without a comparator:

> "At a fixed `k > 0`, `C = max_j f_j / k`; therefore ranking by `C` is exactly the same ordering as
> ranking by `max_j f_j`. The proposed study would test whether the largest family-specific failure
> count adds information conditional on total failures. **It would not establish a special property
> of the ratio itself.**" — formulation note §4

> "`C = max(F)/k` is a deterministic summary of the entire family-count vector `F`. It cannot be
> varied while holding `F` fixed." — `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` §5

Consequences the records draw from this:

1. `C` must be compared against `F`, not only against `k`. In the one dataset with real overlap, `F`
   won: W1 full-vector-vs-`C` gain `+0.000790`, 95 % `[+0.000692, +0.000886]`, interval excluding zero
   (`11_THREE_WORLD_SIM_RESULT.md` line 44).
2. The LC518 index is not novel: "`C_D` is the Berger–Parker dominance index applied to the
   distribution of failures across the eight diagnostic input strata" (`AGENT_DECISION_CLAIM_B1_...`
   §2).
3. Any baseline that already contains `F` makes `C` redundant by construction; the construct-validity
   assessment therefore forbids `F` inside `Z` for the primary comparison (§1.1).
4. At fixed `k`, the "ratio" framing is decoration. The tested object is `max_j f_j`.

So the theory that took place is partly a **deflation**: from "concentration is a property of
failures" to "the largest family count is a summary that might add information beyond a coarser
baseline, and must be shown to do so against the full vector".

---

## 4. The rival explanation that never lost

Every design in the corpus names the same competitor and none excludes it. The corpus is unusually
candid about this:

> "`C` has tracked a hidden variable in each earlier setting: algorithm type in the old Doctor
> project, failure count in v0.2, and family size and defect identity in the engineered Gate 1 work."
> — formulation note §9

> "Even with variation, a `C` association can reflect family identity, family size, defect mechanism,
> or scoring weights. A useful claim must separate `C` from those alternatives, or explicitly narrow
> the claim to a setting where they are held fixed."
> — `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` §1.3

The engineered-study calibration controls give the clearest numeric warning, though they are controls,
not a test: at fixed `k = 5` and fixed `C = 1`, score varied from **0.683673 to 0.969388** across
carrier families, and the high-`C` control mean **0.833333** was *lower* than the low-`C` control
**0.887755** (`CONSTRUCT_VALIDITY_ASSESSMENT` §3.5). A "concentration effect" of the predicted sign
did not appear even where the design was built to produce one; what appeared was a carrier effect.

Three attempts to separate `C` from that competitor failed at construction, not at statistics:

- **Option B profile ladder** `(5,0) → (4,1) → (3,2)` changes the leading family count 5 → 4 → 3, so
  "`C` is therefore collinear with carrier count within a pair, even though carrier identity is held
  fixed" (`06_OPTION_B_IDENTIFICATION_AUDIT.md` §2).
- **Gate 1**: 257 candidate mechanisms, 14 at `k = 5`, eight cross-mechanism profile matches — "All
  eight are pairs with **identical full-domain failure sets**"; `distinct_mechanism_matches = 0`.
- **v0.21**: "The current M1-si structure varies `a` and `C_D` together; it does not guarantee `C_D`
  variation while `a` is held fixed" (§0 item 3).

So the rival is not a theory that won; it is a confound that was never defeated. That distinction is
the difference between "concentration is a proxy for defect identity" (not established) and
"concentration has not been shown to be anything else" (established).

---

## 5. The competing formulations that were explicitly rejected

This matters because "what theory took place" could be answered by a claim that was *considered and
set aside*. The record shows four such decisions, all documented:

| Candidate | Fate | Reason, quoted |
|---|---|---|
| **H2 / hidden structure** (old Doctor) | **retired** | "retired after a cost proxy recovered the boundary without access to the intended structure" (`00_CLAIM.md` §"Why this is not the retired H2 claim") |
| **Claim A** (concentration within the complete constructed mixture) | **not adopted** | "That does not address whether concentration is merely revealing which individual mutation mechanism generated the failures" (`AGENT_DECISION...` §2) |
| **B2** (beyond exact dual-mutant pair composition) | **deferred** | "28 unordered pair types across 30 parent assignments: 26 occur once and two occur twice" — no replication |
| **H1/H2 as loss-reduction estimands** | **secondary** | H3 made "working primary"; H1/H2 kept as mean-prediction and transfer variants |

Two further candidates appear only as cautions, not as adopted theories:

- **Breadth as a secondary comparator**: collinear with concentration — "79.41% inverse / 20.59%
  same-direction among strictly-ordered pairs" (`lc518-150/glm-handoff/worklog.md:196`).
- **Family size / scoring weights**: a construct threat, controlled by requiring equal-family scores
  as a secondary outcome, never a candidate explanation in its own right.

---

## 6. The feasibility ceiling that now constrains every formulation

Independent of identification, the records contain four arithmetic limits. Together they say that
even a perfectly identified design has little room for a detectable effect.

| Limit | Value | Source |
|---|---|---|
| Population-level oracle effect | R1 curves peak **below `2δ* = 0.0405465`** across all four declared scenarios | `v03p/VDRAFT_Target_Bridge_...` §0.2, §4.1 |
| Power at `k=5`, 120 high-C / 30 low-C slots | **0.78565** at residual SD 0.20; **0.62135** at 0.25 | `engineered-study/results/power_analysis.json` |
| Cell occupancy at 150 variants | **4.17** per mechanism-profile cell; **1.39** per mechanism-profile-generator cell | `06_OPTION_B_IDENTIFICATION_AUDIT.md` |
| Attainable `k` | last contrastable `k` = 24 (6×5), 53 (canonical 8-strata), 56 (record-weighted) | `LC518_POPULATION_MODEL_AUDIT_2026-11-10.md` §1 |

The R1 result is the most consequential and the most carefully bounded. The document refuses the
strong reading:

> "The R1 quantity therefore does not reach that level within the declared calibration domain. This
> is a statement about the **population-level oracle-effect curve**, not about the finite-sample
> procedure." (§4.1)
> "Do not conclude 'G6b cannot meet the target' from R1 alone." (§4.1)

So: the best-case, oracle-level signal in the v0.3-P calibration sits below twice the pre-specified
minimum meaningful effect — but that is a statement about a declared simulation, not a refutation.

---

## 7. What actually occupies the place now

Three things, and only one of them is scientific.

**7.1 A claim, fully conditioned and unbuilt — B1.**
`Claim B1`: "Among singly mutated solver versions, does the concentration of definite diagnostic
failures across the eight input strata carry information about held-out correctness beyond total
definite failures and unresolved diagnostic outcomes, conditional on both the identity of the
individual mutation mechanism and the parent algorithm family?"

Support requires `k_fail ≥ 2`, ≥3 distinct parents in one exact `(mechanism, family, k_fail,
k_unresolved)` cell, ≥2 distinct `C_D`, no pooling. Absent that, the mandated verdict is
"NON-IDENTIFICATION / INSUFFICIENT WITHIN-MECHANISM-AND-WITHIN-FAMILY SUPPORT", "not a null
concentration effect". No parent roster exists, so the claim has no population.

**7.2 A measurement rule — M1-si.**
"At least three qualifying parents must contribute to the same exact cell. Cells are never pooled."
Threshold: ≥3 parents × ≥2 own variants × ≥2 distinct exact `C_D` → ≥6 variants in one cell. Audits
executed to date: **0**. Manifests produced: **0**.

**7.3 An engineering programme.**
H3 footprint V2–V9 (containment, isolation, provenance), LC518 bank generation (64 + 80 records),
containment repacks, storage inventory, claim matrix, M1-si tooling, the 2026-11-18 validator
(169 checks). These produce executable machinery and trustworthy provenance. They produce no
evidence about `C`, and each document says so.

What is *absent* from the place the theory used to occupy: any alternative mechanism for why
concentration would predict anything. The corpus never proposes one. There is no "concentration
works because defects cluster in one family and clustering transfers" theory, no latent-variable
model, no causal account. `09_CONCENTRATION_MATHEMATICAL_SPEC.md` §5.4 is explicit that a model can
be written to produce any sign, and that choosing one is not evidence.

That absence is itself a finding: **the programme never had a mechanism theory to lose.** It had a
statistic and a predictive claim. When the statistic turned out to be a function of the design
coordinates, there was nothing underneath it to fall back on.

---

## 8. Where the question went, in order

| Period | What the programme did | Theory content |
|---|---|---|
| to 2026-10-12 | two pre-registered studies | full predictive claim, executed, failed for yield then identification |
| 2026-10-14 → 10-20 | v0.3-P, five design revisions, review loop | same claim, redesigned for identification; never frozen |
| 2026-10-17 → 10-24 | engineered-study, Option B, math spec, three-world sim | claim narrowed to one task; construction audit failed; synthetic null |
| 2026-10-21 → 10-25 | natural pilots, next-task, offline inventory | feasibility only; 14 eligible bodies, 0 contrasts; stop rule triggered |
| 2026-10-25 | formulation note, construct-validity assessment | reformulated as ranking (H3); universal-correctness theorem; 10 design conditions |
| 2026-10-26 → 11-01 | H3 footprint V2–V9 | engineering; no H3 result |
| 2026-11-01 → 11-18 | LC518: banks, containment, B1, v0.21, M1-si | claim conditioned on mechanism and family; no population; no audit |

The pivot is 2026-10-25. Before it, documents argue about **what would count as evidence for `C`**.
After it, documents argue about **whether a population capable of producing that evidence can be
built at all**. That is a different question, and it is the one that has consumed the programme since.

---

## 9. The unresolved choice that would let a theory exist again

Every route now terminates in the same owner decision, recorded as open in multiple places:

- **Confirmatory vs exploratory route:** "OWNER DECISION OPEN" (`GPT_ADJUDICATION_S25_GAP_ANALYSIS_
  2026-11-16.md`).
- **Operating parent count:** "the support floor P >= 3 is not an operating-parent-count
  justification, and no confirmatory operating count can be inferred from the current record."
- **Population:** v0.21 records no parent selected, no mechanism assigned, 90/150 not binding.
- **Custody and consent:** no independent custodian; joint-consent provenance open.

Until those are decided, no formulation above can be executed, and no theory — the concentration
claim or any rival — can be tested. That is the accurate description of the present state: **the
programme is not between theories; it is between a claim and the population that could bear it.**

---

## 10. Files relied on

| File | Use |
|---|---|
| `concentration-formulation/02_RESEARCH_FORMULATION_NOTE_2026-10-25.md` (remote) | §3 theorem, §4 H3, §8 H1/H2/H3 table, §9 hidden-variable sentence |
| `v03p/PHASE0_DESIGN_2026-10-14.md` | v0.3-P question and estimand |
| `v03p/PHASE0_DESIGN_2026-10-15_RevF.md` | revision chain and non-freeze status |
| `v03p/VDRAFT_Target_Bridge_and_Research_Decision_2026-10-18.md` | R1 vs G6b; R1 < 2δ* |
| `engineered-study/00_CLAIM.md` | H1a; retired H2 |
| `engineered-study/06_OPTION_B_IDENTIFICATION_AUDIT.md` | collinearity, 4.17 / 1.39 |
| `engineered-study/08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md` | NEGATIVE, 0 distinct mechanisms |
| `engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md` | §5.4 sign-by-construction; §6 identification |
| `engineered-study/math/results/three_world/11_THREE_WORLD_SIM_RESULT.md` | W1 numbers |
| `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` | §1.1 `F` inside `Z`; §1.3 construct threats; §3.5 calibration controls; §5 `C` is a function of `F` |
| `lc518-150/review-v1.2/AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` (remote) | B1 wording; Claim A rejected; B2 deferred; K5 exclusion |
| `lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.21.md` (remote) | `a(v)` confound; support arithmetic |
| `lc518-150/review-v1.2/b1-population-design/GPT_ADJUDICATION_S25_GAP_ANALYSIS_2026-11-16.md` (remote) | open owner decision; capacity envelope |
| `lc518-150/engineering/README.md` (remote) | M1-si is a utility, not an audit |
| `engineered-study/results/power_analysis.json` | 0.78565 / 0.62135 |
| `README.md` | current programme statement |
