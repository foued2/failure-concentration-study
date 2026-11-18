# LC518/150 — Concentration-estimand review record

**Date:** 2026-11-05
**Status:** REVIEW RECORD — AGENTS' RECOMMENDATION, OWNER RATIFICATION PENDING. HOLD in force.
This record authorizes nothing: no construction, no execution, no analysis, no annex
invention, no commit, no publication.
**File status:** untracked working-tree file, repository root, branch
`research/concentration-math-spec`. Not committed on any ref. Persistence here is
record-keeping, not ratification; the owner may remove it.
**Participants:** Claude (scientific memo; A1a draft; estimand fork; Claim B selection),
GPT (adversarial review; identity-vs-composition split and B1/B2; arithmetic verification),
GLM / Qoder CLI (record-keeper: primary-document retrieval, verification passes, arithmetic
correction, this consolidation).

**Provenance of inputs:** the review chain of 2026-11-05 (chat), grounded in primary
documents read directly: `engineered-study/GATE1_REPORT.md`,
`engineered-study/06_OPTION_B_IDENTIFICATION_AUDIT.md`,
`engineered-study/08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md` (working tree of this branch),
and `lc518-150/glm-handoff/ANALYSIS_SPEC.md` (v1.0),
`lc518-150/review-v1.2/analysis-revision-2026-11-02/ANALYSIS_SPEC_REVIEW_DRAFT.md`
(rev 2.6), `lc518-150/glm-handoff/BANK_DESIGN.md` (all at commit `511bc20`, ref
`origin/gpt/lc518-150-analysis-review-2026-11-02`).

## 1. The review chain in one paragraph

Claude's scientific decision memo was checked against the primary documents and corrected
on three points: the Gate 1 raw control spread is a family-weighting artifact (equal-family
scoring collapses the six localized controls to 0.833333 vs spread control 0.829282;
difference 0.004051); the eight cross-mechanism profile matches all had identical
full-domain failure sets (algebraically equivalent predicates;
`distinct_mechanism_matches = 0`); and the Option B ladder's carrier-count collinearity is
structural ("Option B holds carrier identity, not carrier count"). The memo produced the
A1a capacity check and the Claim A/B estimand fork. Claude selected **Claim B** as the
recommended target; GPT accepted it with the identity-vs-composition challenge (B1/B2);
GLM verified the arithmetic and the governance framing. The B1/B2 fork is the open owner
question. Claude's self-correction is part of the record: its earlier word "feasible" for
individual-mechanism comparisons is withdrawn; only nominal incidence is supported.

## 2. Record facts the fork rests on (verified against the sources)

1. The frozen design of record (ANALYSIS_SPEC.md v1.0) contains **no concentration
   feature** in E3; the concentration comparison exists only in review-only revision 2.6
   (Models A/B/C; A-vs-B and A-vs-C; B-vs-B+profile explicitly out of scope, rev 2.6 §1).
   Rev 2.6 §3.7: A-vs-B compares two separately tuned ridge procedures and "does not
   estimate an unrestricted independent effect of concentration."
2. Rev 2.6 §5.2 support floor: an exact (k_fail, k_unresolved) cell with k_fail ≥ 2 has
   concentration-specific support only if at least 3 distinct parent groups contribute
   within-parent C_D variation in that same cell (at least 2 of the five matched versions
   in the cell with different C_D; no pooling across cells). If unmet: label
   INSUFFICIENT_WITHIN_PARENT_SUPPORT — a support limitation, not a null effect; the floor
   gates interpretation, not estimability.
3. Mutation identity/composition is prohibited as a predictive feature (v1.0 §4; rev 2.6
   §7: exclusion because use "would leak construction ground truth"). The injected
   mechanisms are the only **intended** source of diagnostic failures (v1.0 §1: static
   inspection cannot establish that an intended-correct parent is correct). Therefore
   Claim B cannot be tested inside the blind prediction models as written; it requires a
   separately authorized, predeclared robustness stage. Architectural precedent: E1 is
   already the label-using lane; the blind-analyst gate (v1.0 §9 slot 4) covers E3
   fitting.
4. Provenance distinctions: C9 bank generation was owner-ratified on the **generation**
   side only (OWNER_GO_RECORD); the analysis side of record remains v1.0. The strict
   C8/E3 all-resolved gate in rev 2.6 §6 was owner-confirmed in chat on 2026-11-02 —
   recorded provenance, but it does not freeze rev 2.6.
5. The frozen record itself pre-declares the composition sparsity: v1.0 §3 ("the 28-pair
   screen is exploratory with only limited replication (two preselected pairs)") and
   v1.0 §8 item 3.

## 3. A1a — abstract within-parent support capacity (verified; capacity only)

Witness (mutation-bearing slots only — S0 is intended-correct; same-family parents across
K1–K4 to cover the Z-inclusive reading of the cell definition; K5 cannot host a
three-parent witness, having 2 parents): three distinct parent groups, two versions each,
with diagnostic failure vectors f⁽ᵃ⁾ = (2,0,0,0,0,0,0,0) and f⁽ᵇ⁾ = (1,1,0,0,0,0,0,0).
Both lie in the exact cell (k_fail, k_unresolved) = (2, 0); C_D = 1 vs 0.5 (rev 2.6 §2: at
k_fail = 2 the attainable C_D values are exactly {1/2, 1}). Both vectors are admissible
(8 diagnostic records per stratum, BANK_DESIGN §6). This meets the three-parent floor in
principle.

Degenerate counterexample: if every nonzero failure vector the mutation system produces is
single-stratum, then C_D = 1 for every failing body and no pair allocation, replication,
or S-extra balancing can create within-cell variation (W2-type degeneracy; S03).

Scope and narrowness: capacity, not feasibility; at k_fail = 2 the contrast is two-level,
not dose-response. The witness does not respect mechanism constraints — whether any
approved mutation of a real parent can produce either vector is unknown and
annex-dependent.

Corrections applied in this record: S-extra arithmetic stated conditionally (the balancing
rule is annex content, L13; "as evenly as possible" is an illustration, not a frozen
rule); "only *intended* source" wording; Z-ambiguity footnote (rev 2.6 §5.1 item 3
includes Z in the reported cell; §5.2 and §5.1 item 5 omit it — A1a uses the §5.2
criterion, and the same-family witness covers the stricter reading); `d_timeout_s` is a
reserved column, not a parameter; the staged early-abort option is recorded in §5.

**A1a conclusion: abstract within-parent support capacity is mathematically possible;
mechanism-constrained support is unknown; this is not a feasibility finding and not a GO.**

## 4. Allocation-support arithmetic (annex-free; verified)

Schedule: 28 unordered mechanism pairs once + 2 preselected replications = 30 parent
assignments.

| Pair-type frequency | Pair types | Parent assignments |
|---|---|---|
| n = 1 | 26 | 26 |
| n = 2 | 2 | 4 |
| Total | 28 | 30 |

- **Exact pair composition (dual-mutant SAB):** maximum replication anywhere is n = 2,
  for exactly 2 of 28 pair types; 26 pair types have a single parent context.
  Composition-conditional comparisons are not supported by this schedule; pair identity
  and parent context are nearly inseparable for most dual-mutant assignments.
- **Individual mechanisms:** the base schedule is the complete graph K8 (each mechanism
  paired once with every other). Each mechanism appears in 7 base pair assignments +
  0–2 replication extras = 7–9 parent groups, plus S-extra assignments (30 across
  8 mechanisms; balancing rule is annex content).
- Adopted wording (GPT): "The allocation provides repeated nominal incidence for
  individual mechanisms, making individual-mechanism comparisons potentially examinable.
  Their identifiability remains conditional on parent-family allocation, realized
  diagnostic-profile overlap, and the predeclared analysis."
- Partner structure: combinatorial partner balance holds in the base schedule; what fails
  is pair-interaction estimability (n = 1 per pair type; two pairs at n = 2) and
  realized-profile balance (unknown before A3-dynamic). GLM's earlier "partner aliasing"
  phrasing is withdrawn as loose: nominal incidence must not be promoted to
  identifiability.

## 5. The open owner questions

1. **Ratify the target?** Agents' unified recommendation: **Claim B** (mechanism-robust
   concentration information) — the claim closest to the original programme question
   (P01; CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md §1.2), which the natural route failed
   to test (E02: C not identified separately from carrier family or defect identity). Not
   ratified. Claim A (population-internal prediction) is the weaker alternative; adopting
   it must not happen silently.
2. **If Claim B is ratified — is B1 or B2 essential?**
   - **B1 (beyond individual mechanism identity):** potentially examinable — nominal
     incidence exists; identifiability conditional on A2-static (allocation, crossing),
     A3-dynamic (realized profiles), and the predeclared analysis.
   - **B2 (beyond exact pair composition, including dual-mutant pairs):** poorly supported
     by the 28+2 schedule (§4). If B2 is essential, the schedule is presumptively
     inadequate pending redesign.
   The owner must declare which is required. Silence blocks the record; choosing B1
   without declaring it would quietly narrow the claim.
3. **Annex:** supply the mutation annex (eight-mechanism taxonomy, 28+2 pair-allocation
   schedule, S-extra balancing rules — L13) or formally drop the mutation design.
4. **Execution protocol** (v1.0 §9 slot 3): interpreter pin, runtime/memory budgets,
   timeout rule; `d_timeout_s` remains a reserved null column until then.
5. *Optional:* a staged early-abort design change (diagnostic execution on a constructed
   subset before all 150 bodies) — under the frozen process the first observable support
   checkpoint is post-construction; introducing an earlier one requires explicit
   authorization.

**Failure rule:** insufficient profile overlap or composition support is a
**non-identification result** — the concentration claim is dropped or the design
redesigned. It is not a null result and does not permit relabeling the study as Claim A.

**Governing constraints:** no record may state "Claim B adopted"; the blind E3 pass is
unchanged by any robustness stage; the robustness stage must be predeclared before
execution and separately authorized (new role, new gate).

## 6. Scientific gaps any adopted memo must carry

Target separation (E1 vs E3; natural vs engineered estimands; P01); construct transfer
(C_D spans eight input strata, not six defect families — the Gate 1 negative does not
transfer automatically); scoring estimand fixed before generation (raw vs equal-family
answer different questions; the 0.004051 equal-family residual on a single spread control
is not a concentration result); D6 reorder-pair dependence (4 canonical instances × 2
orderings — not 8 independent inputs); held-out bank exposure (no sealed confirmatory
use, L27); no power/MDE claims (exploratory; 30 parent groups, not 150 independent bodies;
v1.0 §6 item 8 and §8 item 5).

## 7. What this record does not claim

- It does not ratify Claim B, B1, or B2; it decides no owner question.
- It does not establish identifiability of any mechanism-level quantity; nominal incidence
  is not identifiability.
- It does not authorize construction, execution, annex invention, analysis, or any
  persistence beyond this untracked file.
- It does not modify any tracked audit record; the inventory §4 listing is descriptive
  only.
