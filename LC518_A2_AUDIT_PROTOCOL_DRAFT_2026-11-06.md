# LC518 A2-static audit protocol — Rev 11 (text settled by joint sign-off, 2026-11-06)

**Date:** 2026-11-06 (Rev 11 — text settled)
**Status:** TEXT SETTLED — joint GPT–Claude content sign-off recorded 2026-11-06
(companion record §19.1). The signed-off content is the Rev 11 text as reviewed; the
working-tree file additionally carries exactly the pre-authorized bookkeeping repairs
and this factual status update, enumerated in record §19.2. Byte-exact identity is
**not** established by the sign-off: the reviewed object was the pasted text; the
authoritative byte-exact review object is the base64-decoded file at any freeze event
(§11). The sign-off settles the protocol text only: it is not a freeze event and
authorizes nothing — no freeze, no annex inspection, no auditor appointment, no
construction, no execution, no commit. The B1 target and Option W are unchanged.
**Supersedes:** Rev 10 (2026-11-06). Changelog: §12.
**Companion record:** `LC518_A2_STATIC_ANNEX_AUDIT_2026-11-06.md` §19 (joint sign-off
record; verdict: BLOCKED / NOT ASSESSABLE — required allocation artifact unavailable).
**Prepared by:** Qoder CLI (GLM role: record-keeper), incorporating the aligned
GPT–Claude correction list (2026-11-06).

## 1. Why this exists

The A2-static audit must not have its criteria shaped by the artifact it audits. The
criteria below are therefore written while no annex is available to anyone, so that if
one is recovered or supplied, the sequence is fixed: **agree → freeze → inspect →
audit → report**, never inspect-then-criteria.

## 2. Auditor independence

- The auditor must not be an author or co-author of the annex under audit. Step 0 of any
  audit is a non-authorship attestation from the auditor.
- The auditor must not be the agent that performed the availability investigation
  underpinning path selection — that investigation (2026-11-06, audit record §§3, 9) is
  classified as an annex availability and provenance investigation, not an
  allocation-identification audit.
- Before any annex access, the auditor must attest to having had **no role in**:
  defining the mutation taxonomy; assigning the mutation pairs to parents; designing the
  S-extra allocation; deciding which assignments to retain (GPT, 2026-11-06).
- The auditor's identity and conflict statement are recorded in the audit record
  **before annex access**.
- The owner (annex custodian) supplies the annex; the owner does not select the
  auditor's findings or amend criteria post hoc.
- Freezing the protocol does **not** authorize annex inspection (§11).

## 3. Input admission (C0)

- **C0.1** The annex reaches the auditor through a recorded owner channel; the owner
  records its SHA-256 at delivery.
- **C0.2** The auditor re-computes and records the SHA-256 of the received file. A
  mismatch with the owner's recorded digest blocks the audit (BLOCKED — integrity).
- **C0.3** The annex text must not be committed to any public repository ref, any branch,
  or any published archive (work order §4 privacy rule). The audit report records cell
  counts and verdicts, not mechanism-to-parent tables.

## 4. Frozen audit criteria

Each criterion is pass / fail / not-assessable, with the reason recorded. All checks are
static text and arithmetic; no solver source is written, read, or executed.

- **C1 Taxonomy completeness.** Exactly eight mechanisms are defined, each with a written
  defect definition sufficient to state its *intended* stratum reach (which of the eight
  diagnostic strata it can plausibly fail). No invented, renamed, merged, or substituted
  mechanisms (work order :45). Fail if any mechanism lacks a definition or count ≠ 8.
- **C2 Pair schedule shape.** All 28 unordered mechanism pairs appear **at least once**.
  Exactly **two distinct, preselected pairs** each appear **one additional time**, giving
  **30 assignments in total**. The two replications must be preselected — declared before
  construction, not derivable from outcomes. Fail if any pair is absent, if any pair
  appears more than twice, if the two replicated pairs are not distinct, or if
  preselection evidence is absent.
- **C3 Pair-to-parent allocation consistency.** The 30 assignments map **one-to-one onto
  the 30 parent IDs** (no parent ID receives two pair assignments); the annex declares
  the SA/SB orientation rule for each pair (which mechanism is mutation A) and applies it
  consistently. The parent-ID bijection does **not** by itself establish independent
  replication: the effective independent-parent count follows only after applying the C4
  identity rules (including identical-base-source-hash deduplication), and `n(m,z)` uses
  that effective count. Fail on collision, gap, or orientation inconsistency.
- **C4 Incidence-by-family table and parent-group identity.** A **parent group** is one
  distinct base parent implementation, identified by its immutable parent ID together
  with its pinned base-source hash. Every mutation variant inherits its parent's
  identity and its one algorithm-family assignment. Define `n(m,z)` = the number of
  **distinct eligible parent groups** assigned mechanism `m` in family `z`, counting
  only eligible single-mutation roles (**SA, SB, S-extra**), excluding S0 and SAB.
  Counting rules (GPT–Claude rulings, 2026-11-06):
  1. Count distinct base parent implementations, never mutation-version rows.
  2. Multiple eligible versions belonging to the same parent count as **one** group.
  3. An exact duplicate base-source hash appearing under multiple parent IDs counts as
     **one** group — it cannot inflate the independent-parent count. (A bookkeeping
     identity must not masquerade as independent replication.)
  The audit computes and reports `n(m,z)` for **all 40** (mechanism, family) cells,
  **including zeros**. A cell qualifies structurally only at `n(m,z) ≥ 3`. The table is
  reported in full regardless of verdict. The same identity rules govern "distinct
  parent groups" everywhere in this protocol, including §5.
- **C5 S-extra balancing (recorded work-order compliance item).** The 30 S-extra
  assignments are distributed across the 8 mechanisms as closely as integer counts
  permit (six mechanisms at 4, two at 3, under the work-order wording); the annex's
  declared balancing rule is compared against its realized S-extra column, and
  deviations are recorded per mechanism. C5 is a **compliance record, not an
  independent A2 pass/fail gate**: the verdict never turns on C5. The record
  distinguishes **raw assignment counts** (S-extra slots per mechanism) from
  **effective parent counts** (distinct parent groups after the C4 identity rules,
  including same-parent duplication and identical-hash deduplication). A deviation that
  leaves any mechanism below 3 raw S-extra slots is recorded; whether it reduces an
  effective `n(m,z)` below 3 is assessed under C4, not C5.
- **C6 Within-cell C_D-value feasibility (annex-level screen; family-, mechanism-, and
  cell-specific).** For each qualifying mechanism-family pair `(m, z) ∈ S_W` and each
  exact cell `c = (k_fail, k_unresolved) ∈ D` (§5):
  - **Witnesses (both vectors mandatory).** A *witness* for parent `p` in cell `c`
    under mechanism `m` and family `z` is a complete, checkable object: the
    failure-count vector `f = (f_1, …, f_8)` and the unresolved-count vector
    `u = (u_1, …, u_8)`, both in `ℤ_{≥0}^8` with **all eight entries supplied,
    including explicit zeros**; and the identity of the eligible mutation version, its
    parent, and the mechanism and family it carries. A witness is **admissible** only
    if all of the following hold:
    1. `Σ_j f_j = k_fail` and `Σ_j u_j = k_unresolved` exactly;
    2. `f_j + u_j ≤ R_j` for every stratum `j`, where `R_j` is the frozen
       per-stratum diagnostic-record count (freeze record, §5) — each diagnostic
       record yields at most one outcome;
    3. the named version belongs to parent `p` and carries mechanism `m` in family `z`;
    4. **mechanism reach** (standard below) holds for every nonzero `f_j`, and the
       complete vector is consistent with it.
    An **omitted unresolved vector is missing evidence, not an implicit all-zero
    vector**; a witness lacking it is not assessable as admissible.
  - **Mechanism-reach standard (strengthened).** Every nonzero `f_j` must be supported
    by an **exact, identifiable rule in the written definition of the assigned
    mechanism**, applicable to the particular family and assigned version, establishing
    that the mechanism can produce a definite failure in stratum `j`. The **complete
    vector `f`** — not merely each component considered separately — must be consistent
    with the mechanism's stated limits, exclusions, multiplicity constraints, and
    dependencies across strata.
    **Joint attainability.** Componentwise reach citations are necessary but not
    sufficient. The evidence must establish that the complete failure vector is
    **jointly attainable** under one coherent application of the assigned mechanism to
    the named version. Separate per-stratum reach statements do not establish joint
    attainability unless the written definition also supports their coexistence. This
    is a static structural derivation, not a requirement to construct or execute
    solver source. Where joint attainability is not established, the witness is
    unsupported and inadmissible; that finding does not establish structural
    impossibility.
    If the mechanism explicitly **rules out** a stratum, a
    witness with `f_j > 0` is inadmissible. If the documentation does **not establish**
    that a positive component is reachable, the witness is unsupported and
    inadmissible — and that absence of support must **not** be treated as proof that
    the mechanism cannot reach the stratum. **Ruled out and not established are
    different findings**: the former can support a documented structural-absence
    determination; the latter cannot. This remains a static structural test — no
    source construction, no execution, no claim that a failure was observed — but it
    establishes more than arithmetic compatibility.
    **Frozen rule text.** The applicable rules are those in the annex text **as
    delivered** (hash-pinned at C0). Each witness records its supporting citations;
    citations are judged against the admissibility standard frozen in this protocol
    before inspection; no passage outside the pinned text can add support, and a
    supporting passage may not be located after seeing the witness except within the
    pinned text under the frozen standard.
  - **Unresolved-status provenance.** Every nonzero `u_j` carries documented status
    provenance: if unresolved status is attributed to the mutation mechanism, the
    mechanism-reach standard must support that attribution; if it arises from the
    evaluation or recording process, it must be identified as such. Unresolved
    outcomes are **never silently treated as mutation-induced failures**.
  - `V_{p,m,z,c}` = the set of C_D values **derived from admissible witnesses** by the
    §5 `C_D` formula. Values are never declared alongside or instead of witnesses; a
    scalar declaration without an admissible witness contributes nothing.
  - `P_{m,z,c}` and the treatment of witnesses and absence. For each parent `p` and
    cell `(m, z, c)`:

    | Situation | Treatment |
    |---|---|
    | At least one admissible witness for `p` in the cell | `p` enters `P_{m,z,c}` |
    | A witness fails a validity check | Discard it; record the reason |
    | No admissible witness, with affirmative evidence establishing structural absence for that parent and cell | **Documented absence** |
    | No admissible witness, without an adequate structural-absence basis | **`NOT ASSESSABLE`** |

    An invalid witness does not become evidence of structural impossibility merely
    because it was rejected; nor does a missing record prove absence. `P_{m,z,c}` is
    built from admissible witnesses, not from the family-level `n(m,z)`.
  - C6 **passes** for `(m, z, c)` iff **both**:
    1. `|P_{m,z,c}| ≥ 3`; **and**
    2. `∃ p ≠ q ∈ P_{m,z,c}, a ∈ V_{p,m,z,c}, b ∈ V_{q,m,z,c} : a ≠ b`.
  - **Aggregation rule.** Eligible versions of the same parent are aggregated only
    when they concern the **same mechanism, family, and exact cell**; possibilities
    and observations are **never pooled across mechanisms**.
  - The non-disjointness rule is retained: `V_{p,m,z,c}` and `V_{q,m,z,c}` need not be
    disjoint (`{0.5, 1}` against `{0.5, 0.75}` still permits a cross-parent
    difference, `1 ≠ 0.75`).
  - Safeguards (binding, frozen before inspection):
    1. The differing values must be possible for different effective parent groups in
       the same family `z`, with all three parents able to reach the same exact cell.
    2. Both values must belong to the same exact `(k_fail, k_unresolved)` cell.
    3. Multiple versions of one parent cannot create between-parent variation: all
       versions of a parent collapse into that parent's single witness-derived set.
    4. The witness standard, the mechanism-reach standard, the comparison rule, the
       cell domain, and the possibility-set reading are frozen before inspection; **no
       representative value is chosen after seeing outcomes**.
  - Evidence standard: the annex must actually **document** the witnesses and, where
    relied on, the structural-absence bases. Without admissible witnesses or a
    documented absence, a claimed possibility or absence is **`NOT ASSESSABLE`** —
    never an assumed pass — and missing evidence is never silently treated as proof
    that a cell is impossible.
  - Scope role (binding): C6 informs structural feasibility and the aggregate A2
    verdict only. C6 failure or non-assessability for a particular `(m, z, c)` **never**
    removes the pair from `S_W`, never alters the 40-cell reporting, and never rewrites
    scope after inspection; the scope rule remains C4-based (§7). Realized support is
    exclusively A3-dynamic and is never claimed here.
- **C7 K5 scope.** No (mechanism, K5) cell qualifies; K5 is reportable descriptively
  only, and the audit verdict's inferential scope excludes K5 regardless of the annex's
  own text. (Structural basis, annex-free: K5 has 2 parent groups, below any
  three-parent minimum under any schedule.)
- **C8 Parent-identity and family-assignment consistency.** Each of the following
  ambiguities produces verdict **BLOCKED / UNRESOLVED** pending resolution; none may be
  resolved by discretion inside the audit:
  (i) a parent ID mapping to multiple base-source hashes or multiple family labels;
  (ii) a base-source hash appearing under conflicting family assignments;
  (iii) an ambiguous mutation assignment — it must never be converted into 0 or 1 for
  convenience (GPT–Claude rulings, 2026-11-06).

## 5. The exact-cell support rule (A3-dynamic; not assessable at A2)

**C_D definition (self-contained; the audit criteria operate on this definition).** The
eight diagnostic input strata are indexed `j = 1..8`; `f_j` is the number of definite
diagnostic failures in stratum `j`; `k_fail = Σ_j f_j`. The concentration value is the
Berger–Parker dominance index of the failure distribution:

**`C_D = max_{j=1..8} ( f_j / k_fail )`**, with the convention **`C_D = 0` when
`k_fail = 0`** (labelled **NO OBSERVED FAILURES**).

`k_unresolved` does not enter `C_D`; it is part of the cell identity only. (Consistent
with the decision of record :31 and :70.)

The full B1 support cell is `(m, z, k_fail, k_unresolved)` (decision of record :39).

**Exact-cell domain (frozen before inspection).** The audited domain of exact cells is
`D = { (k_fail, k_unresolved) : k_fail, k_unresolved ∈ ℤ_{≥0}, k_fail + k_unresolved ≤ N }`
— defined over **nonnegative integers**. `N` is the number of **diagnostic bank records
per solver body** — the counting unit of record: bank records as delivered by the
generated study bank, **not** unique mathematical inputs (the distinction matters when
the bank contains repeated or permuted records). `N` and the per-stratum record counts
are design-level quantities taken from the frozen design specification, not annex
content. The **freeze record must state**: (1) the numerical value of `N`; (2) the
counting unit; (3) the number of diagnostic records in each of the eight strata,
`R_1, …, R_8`, with the consistency check `N = Σ_j R_j`; (4) the source design
specification establishing those counts. The per-stratum counts `R_j` are required for
C6 witness admissibility (§4). If any of these cannot be established from the frozen
design documents, the protocol cannot be frozen. All C6 assessments (§4) and A3 support
evaluations range over `D` exactly. Cells outside `D` are reported **`OUT_OF_DOMAIN`** —
never assessed, never treated as failures of assessment.

A qualifying A3 cell requires:

1. at least **three distinct parent groups** (identity per C4) with **nonempty**
   observed-value sets `O_{p,m,z,c}` (below), all within one `(m, z)` and one exact
   cell `c ∈ D`;
2. at least one **cross-parent difference**:
   `∃ p ≠ q, a ∈ O_{p,m,z,c}, b ∈ O_{q,m,z,c} : a ≠ b`;
3. **no pooling** across individual mechanisms, parent families, or exact cells.

**Parent-level observed-value sets (deterministic; mirrors C6).** For exact cell `c`
under mechanism `m` in family `z`, `O_{p,m,z,c}` is the set of observed `C_D` values
among the eligible versions of parent `p` **that carry mechanism `m` in family `z`** in
that cell (realized diagnostic outcomes). Versions are aggregated only when they concern
the same mechanism, family, and cell — never across mechanisms. Every observed value is
recorded as part of the set; **no representative value is chosen after seeing
outcomes**. Within-parent version divergence cannot create a cross-parent difference by
itself — condition 2 requires two different parents — so correlated versions cannot
masquerade as between-parent replication. The structure is parallel to C6: A2 tests
witness-derived possibility sets `V_{p,m,z,c}`; A3 tests realized observation sets
`O_{p,m,z,c}`; both require three parents and a cross-parent difference in the same
exact cell, so an A2 structural pass demonstrates the possibility of the actual B1
support condition rather than a weaker approximation of it.

**`k_fail ≥ 2` is a mathematical consequence, not a separate gate** (GPT ruling,
2026-11-06; Claude concurring). When `k_fail = 0`, the convention gives `C_D = 0` (NO
OBSERVED FAILURES); when `k_fail = 1`, `C_D = 1/1 = 1` in every stratum. A fixed-`k_fail`
cell can contain two distinct observed `C_D` values only if `k_fail ≥ 2`. The decision of
record lists `k_fail ≥ 2` as its first support condition; this protocol records it as
entailed by condition 2. This is a clarification, not an amendment: the admissible
support-cell set and the agreed B1 target are unchanged.

**Reporting rule (two distinct populations; two distinct evidence classes).**

- **Incidence population (descriptive, always reported).** All 40 `(m, z)` incidence
  combinations are reported — including zero counts and nonqualifying combinations
  (C4). This requirement concerns the incidence table, **not** exact-cell inferential
  assessments.
- **Exact-cell assessment population (inferential).** A2 and A3 exact-cell assessments
  are conducted **only over `S_W × D`**. For every `(m, z) ∈ S_W` and exact cell
  `c ∈ D`:
  - **A2 reports (static, declared evidence):** the number of structurally eligible
    parents `|P_{m,z,c}|` and the union of their possible `C_D` values
    `∪_p V_{p,m,z,c}`.
  - **A3 reports (realized evidence):** the parents with observed values and the
    union of their observed `C_D` values `∪_p O_{p,m,z,c}`.

The two evidence classes are distinct and **must not be merged in one table**.

**Status vocabulary (explicit).**

| Status | Meaning |
|---|---|
| `SUPPORTED` | The complete existential support condition is met. |
| `NOT_SUPPORTED` | The assessment is complete, but the support condition is not met. |
| `NOT ASSESSABLE` | Missing or inadequate evidence prevents a determination. |
| `OUT_OF_SCOPE` | The mechanism-family pair is outside `S_W`. |
| `OUT_OF_DOMAIN` | The exact cell is outside `D`. |

`NOT_SUPPORTED` and `NOT ASSESSABLE` are **never interchangeable**: the first is a
completed determination of non-support; the second is the absence of a determination.
A cell that does not meet the support requirement, with its assessment complete, is
reported `NOT_SUPPORTED`. A cell must **never** be merged with adjacent failure-count
cells, another mechanism, or another family to manufacture support — regardless of
whether merging would improve the result.

**Stage qualification.** `SUPPORTED` is stage-qualified in every report: at A2 it
means **structurally supported** under C6 and establishes **possibility only**; at A3
it means **realized supported** under the observed-value rule. The unqualified label
must never be used in a way that obscures the evidence class or stage.

**Reporting population.** All 40 `(m, z)` incidence combinations are reported as
descriptive incidence. Inferential exact-cell assessments run only over `S_W × D`.
Combinations outside `S_W` — including K5 — remain descriptive and **cannot contribute
inferential support**. Outside-`S_W` exact-cell entries, if displayed for transparency,
must be clearly descriptive and marked **`OUT_OF_SCOPE`**, never presented as
inferential results. The report must not make descriptive coverage look like
inferential eligibility.

This condition depends on realized diagnostic outcomes. **A2 cannot demonstrate,
certify, or assume it.** At A2 the condition is labelled *not yet assessable*; it is
never passed by assumption. It is tested only at A3-dynamic against the frozen scope of
§7.

## 6. Verdict categories (frozen at freezing)

| Verdict | Meaning | May progress? |
|---|---|---|
| `ASSESSABLE-PASS` | Complete evidence satisfies the static criteria: C0 admissible; C1–C3 hold; C5 deviations recorded (compliance record only); C4 yields at least one qualifying `(m, z)` pair containing at least one exact cell `c ∈ D` for which **C6 passes**; C7 holds; **no C8 ambiguity exists**. | Yes — to the next separately authorized stage (A3-dynamic predeclaration). Issued with the label **A2 STRUCTURAL PASS** (§8). |
| `ASSESSABLE-FAIL` | Complete evidence demonstrates a failed criterion — including: C1–C3 failure; **a completed C4 incidence table yielding `S_W = ∅`** (no mechanism-family combination reaches three effective parent groups — the bounded design has no inferentially eligible pair); or **all relevant C6 assessments are complete and no cell passes C6** over the domain `{(m, z, c) : (m, z) ∈ S_W, c ∈ D}` (the allocation demonstrably cannot create the comparisons B1 requires). | No. Stop, or redesign as a new design (new frozen assignments, independent review), each separately authorized. |
| `BLOCKED / UNRESOLVED` | Required evidence is missing, ambiguous, or inconsistent — including C0 failure, an unavailable annex, **any C8 ambiguity**, and **no cell passing C6 while at least one relevant C6 assessment remains `NOT ASSESSABLE`**. | No. Not a scientific result and **not a finding that the allocation is defective**. |

- **Three-way disposition over the frozen domain.** PASS: at least one qualifying pair
  and exact cell satisfies C6, subject to the other pass conditions. FAIL: all relevant
  C6 assessments are complete, and none satisfies C6. BLOCKED / UNRESOLVED: no cell
  passes, and at least one relevant assessment remains not assessable. The relevant
  domain `{(m, z, c) : (m, z) ∈ S_W, c ∈ D}` is fixed by formula before inspection, so
  "all cells" is a reproducible stopping condition. Missing evidence is never silently
  treated as proof that a cell is impossible. C6 failure or non-assessability for
  individual cells never removes pairs from `S_W` or from reporting; it bears on the
  verdict only through the aggregate conditions above.
- **Verdict precedence (ordering rule).** Determinations apply in the following order:
  1. **any C0 input-admission failure or any C8 ambiguity** → `BLOCKED /
     UNRESOLVED` — untrusted or ambiguous evidence can never establish a scientific
     design failure;
  2. **demonstrated failure of C1–C3** → `ASSESSABLE-FAIL`;
  3. **C0 admissible, C1–C3 satisfied, C4 complete, C8 unambiguous, and `S_W = ∅`** →
     `ASSESSABLE-FAIL` (the completed incidence evidence establishes the empty scope);
  4. **nonempty `S_W`** → apply the existing C6 cell-level and aggregate verdict rules
     below.
  If C4 cannot be completed because required evidence is missing, the result remains
  `BLOCKED / UNRESOLVED`.
- **Cell-level existential rule.** A cell passes once it has admissible witnesses from
  at least three distinct parents and at least two different exact `C_D` values
  contributed by different parents. Unassessed additional parents do not undo that
  result, but they must remain **disclosed as unassessed**. The precedence across
  cells stands: one qualifying cell establishes the overall PASS; an overall FAIL
  requires complete assessment of all required cells and no passing cell; where no
  cell passes and at least one required assessment remains unresolved, the overall
  verdict is `BLOCKED / UNRESOLVED`.
- **Empty scope and the verdict distinction.** If the completed C4 incidence table
  yields `S_W = ∅`, the verdict is **`ASSESSABLE-FAIL`**: the relevant allocation
  information was assessed, and the completed incidence evidence establishes that the
  bounded design has no inferentially eligible mechanism-family pair. This is a
  demonstrated failure, not missing evidence. The general distinction is
  unmistakable: **missing evidence** for a required criterion means
  `BLOCKED / UNRESOLVED`; a **demonstrated failure** of a required criterion means
  `ASSESSABLE-FAIL`; a **passing C6 cell** can establish `ASSESSABLE-PASS` despite
  unresolved other C6 cells, but only if the other mandatory pass conditions
  (C0–C4, C7, C8) are satisfied — PASS precedence never bypasses unresolved C0–C4 or
  C8 conditions.
- **PASS precedence.** If at least one exact cell passes C6, the structural verdict may
  be PASS even when other cells are `NOT ASSESSABLE`, provided all other PASS
  requirements hold. The unresolved cells must still be **disclosed** and can never be
  treated as supported.
- **Audit immutability.** Once issued, an audit report is immutable. A corrected or
  newly recovered annex requires a **new, versioned audit** against the same frozen
  criteria. Changing the criteria requires a **new protocol version frozen before any
  inspection**.
- Any verdict states explicitly that static allocation evidence does not establish
  realized diagnostic variation or identification.

## 7. Inferential scope — deterministic rule, frozen before annex access

The deterministic bounded-scope rule (Option W, GPT formulation; agreed by Claude,
2026-11-06):

- Definitions: `n(m,z)` as in C4; families `z ∈ {K1, K2, K3, K4}`.
- **`S_W = { (m, z) : n(m, z) ≥ 3, z ∈ {K1, K2, K3, K4} }`**

Binding consequences:

- Include **every** qualifying (mechanism, family) combination. Do not select a
  preferred subset after inspecting the annex.
- Publish all 40 incidence cells, including zeros.
- Report every nonqualifying combination as **outside the inferential scope**. If a
  mechanism has no qualifying family, it is outside the inferential scope, and that
  limitation is disclosed.
- K5 remains descriptive only and never enters the inferential scope.
- **Reporting is not admission.** All 40 mechanism-by-family combinations (8 × 5) are
  reported; reporting all 40 cells must not be mistaken for admitting all 40 into
  inference. The inferential scope is determined mechanically by Option W within
  K1–K4.
- The selection **rule** is frozen before annex access; the resulting **set** is
  computed mechanically after access. No auditor or owner discretion operates between
  the two.
- Post-outcome selection of the covered population is prohibited.
- A3 then applies §5's exact-cell rule to `S_W`. The B1 claim covers only the
  realized-supported part of `S_W`, labelled as bounded.

Rationale of record: an all-eight-mechanism structural gate is stricter than the
bounded-scope B1 decision of record; the deterministic rule implements the already
agreed limitation that inference applies only to supported parts of the constructed
population, without discretionary selection.

## 8. Stage labels

- **`A2 STRUCTURAL PASS`** — an `ASSESSABLE-PASS` verdict at A2-static. Establishes only
  that the allocation creates the **structural opportunity** for B1's comparisons.
- **`A3 REALIZED DIAGNOSTIC-VARIATION SUPPORT PASS`** — the separately audited
  outcome-level condition (§5) applied to the frozen scope `S_W`. Only this label may
  accompany a statement that the **prespecified realized diagnostic-variation support
  condition** is satisfied. It does **not** establish incremental predictive information
  about held-out correctness, a nonzero effect, or the full identification of B1. Those
  require the separately predeclared held-out outcome analysis.

An `A2 STRUCTURAL PASS` must **never** be reported as proof that B1 is identified.

## 9. Failure-handling rules (carried forward)

- `BLOCKED / UNRESOLVED` and `ASSESSABLE-FAIL` are both **non-identification**
  outcomes; only `BLOCKED / UNRESOLVED` is additionally a **not-assessable** condition
  (§6). Neither is a null effect, and neither authorizes relabeling toward Claim A.
- B2 remains deferred; the 28+2 schedule is never presented as supporting B2.
- The blind E3 pass and the frozen v1.0 specifications are untouched by A2 in all
  outcomes.
- Symmetric discipline: a missing or unrecovered annex must not be turned into a
  negative scientific result; a structurally feasible allocation must not be turned
  into a claimed empirical identification result.

## 10. Terminology safeguard

- The **eight mutation mechanisms** are **not** the **eight diagnostic input strata**.
- `C_D` is the **Berger–Parker dominance index** applied to the distribution of failures
  across the eight diagnostic input strata (decision of record :31): the per-stratum
  failure vector is the input; `C_D` is the resulting scalar. The self-contained
  operational definition is in §5.
- The incidence table's axes are **mechanism × parent algorithm family** — different
  axes entirely.
- Confusing these axes invalidates the audit's interpretation. Every report issued under
  this protocol must name its axes explicitly.

## 11. Freezing, review, and authorization boundaries

- **Joint agreement on protocol content is not freezing, and freezing is not
  authorization** (GPT ruling, 2026-11-06; Claude concurring).
- A **freeze event** must separately record: the final file hashes (SHA-256), the
  protocol version, the UTC timestamp, and both reviewers' agreement.
- Byte-exact identity between the reviewed text and the frozen file is established
  through an exact-byte channel agreed before the freeze event. Procedure of record:
  the record-keeper computes the SHA-256 digest of the source file (the **source
  digest**) and pastes the base64 encoding of the exact file bytes together with it;
  reviewers decode the base64, **hash the decoded bytes**, and **compare against the
  source digest**. Matching digests establish that the decoded bytes are identical to
  the source file; any transport corruption is detectable, never silent. Owner-mediated
  file transfer is the alternative. (Basis: plain-text review-anchor digests did not
  reproduce in the Rev 3 round, and the byte discrepancy remains disclosed and
  unexplained — audit record §11.6, §12.) **The base64-decoded file is the
  authoritative review object for any byte-exact sign-off or freeze.** Both reviewers
  must verify its digest against the source digest and confirm that the decoded
  contents are the text being approved. A matching digest alone establishes transfer
  identity, not identity with a previously reviewed paste. Any subsequent edit requires
  a new version and renewed review.
- Freezing grants **no permission** to inspect the annex.
- A **joint protocol sign-off** on the Rev 11 text, if issued by both reviewers, records
  that the protocol text is settled. It is **not a freeze event** and authorizes
  nothing: no freeze, no annex inspection, no auditor appointment, no construction, no
  execution, no commit.
- The independent auditor must be appointed and must provide the §2 attestations
  **before** any annex inspection.
- No further owner ratification of the protocol text is required under the owner's
  recorded delegation (GPT ruling, 2026-11-06; Claude concurring), but nothing in that
  delegation authorizes inspection, construction, or execution.

## 12. Non-claims and revision history

**Non-claims.** This draft freezes nothing; it binds no one before a freeze event as
defined in §11. Freezing alone authorizes nothing: no annex inspection, no
construction, no execution, no publication. It does not assert that an annex exists,
ever existed, or can be recovered, and it does not authorize any search beyond what is
already recorded (audit record §§3, 9) or construction of a replacement annex — path 2
requires its own separate authorization.

**Rev 10 → Rev 11 changelog (2026-11-06, on the agreed Rev 10 review corrections; localized
corrections only — the intended final text for joint sign-off).**

1. §8 A3 label renamed `A3 REALIZED DIAGNOSTIC-VARIATION SUPPORT PASS`, and its
   accompanying statement corrected: only this label may accompany a statement that
   the prespecified realized diagnostic-variation support condition is satisfied; it
   does not establish incremental predictive information about held-out correctness, a
   nonzero effect, or the full identification of B1 — those require the separately
   predeclared held-out outcome analysis. Establishing that the predictor varies must
   not quietly become a claim that it predicts the outcome.
2. §6 verdict precedence: the first ordering rule now reads "any C0 input-admission
   failure or any C8 ambiguity" — matching the C0 table exactly, including C0.3's
   public-repository and archive restriction.
3. §11 byte-identity review object: the base64-decoded file is the authoritative
   review object for any byte-exact sign-off or freeze; both reviewers must verify its
   digest against the source digest and confirm the decoded contents are the text
   being approved; a matching digest alone establishes transfer identity, not identity
   with a previously reviewed paste; any subsequent edit requires a new version and
   renewed review.
4. Companion record: §17.3's incident classification corrected — the trailing-LF
   claim was an unverified byte-property assertion (a verification-discipline failure,
   not a demonstrated text mismatch); the Rev 9 §11-bullet drift is the first
   documented composition-side text mismatch; the +1/+2-byte extraction discrepancies
   have undetermined origin and are not labelled as transport failures (record §17.3
   as corrected, §18.1).

**Rev 9 → Rev 10 changelog (2026-11-06, on the agreed Rev 9 review corrections; localized
corrections only — the intended final text for joint sign-off).**

1. §5 stage qualification of `SUPPORTED`: at A2 it means **structurally supported**
   under C6 and establishes **possibility only**; at A3 it means **realized
   supported** under the observed-value rule; the unqualified label must never be used
   in a way that obscures the evidence class or stage.
2. §6 verdict precedence (ordering rule): C0 integrity failure or C8 ambiguity →
   `BLOCKED / UNRESOLVED`; demonstrated failure of C1–C3 → `ASSESSABLE-FAIL`; C0
   admissible, C1–C3 satisfied, C4 complete, C8 unambiguous, and `S_W = ∅` →
   `ASSESSABLE-FAIL`; nonempty `S_W` → the existing C6 cell-level and aggregate rules;
   incomplete C4 evidence → `BLOCKED / UNRESOLVED`. An empty incidence table built on
   untrusted or ambiguous evidence can never establish a scientific design failure.
3. Companion record: the freeze-rule contradiction corrected — joint GPT–Claude
   agreement **settles** the protocol text; any protocol freeze remains a separate
   event under §11 (record §16.1 and the §8.4 marker corrected in place; the
   correction is documented in record §17.1).

**Rev 8 → Rev 9 changelog (2026-11-06, on the agreed Rev 8 review corrections; localized
repairs only — the intended final text for joint sign-off).**

1. §5 reporting-population consistency: the reporting rule now distinguishes the
   **descriptive incidence population** (all 40 `(m, z)` combinations — an
   incidence-table requirement, not an exact-cell assessment requirement) from the
   **inferential exact-cell assessment population** (`S_W × D` only), with an explicit
   five-status vocabulary — `SUPPORTED`, `NOT_SUPPORTED`, `NOT ASSESSABLE`,
   `OUT_OF_SCOPE`, `OUT_OF_DOMAIN`. `NOT_SUPPORTED` (completed determination of
   non-support) and `NOT ASSESSABLE` (no determination possible) are never
   interchangeable. Outside-`S_W` exact-cell entries, if displayed for transparency,
   are marked `OUT_OF_SCOPE` and remain descriptive.
2. §6 empty-`S_W` case: a completed C4 incidence table yielding `S_W = ∅` is
   **`ASSESSABLE-FAIL`** — the relevant allocation information was assessed; this is a
   demonstrated failure, not missing evidence. The general distinction (missing
   evidence → `BLOCKED / UNRESOLVED`; demonstrated failure → `ASSESSABLE-FAIL`) is
   explicit, and PASS precedence never bypasses unresolved C0–C4 or C8 conditions.
3. §4 C6 joint attainability: componentwise reach citations are necessary but not
   sufficient; the complete failure vector must be **jointly attainable** under one
   coherent application of the assigned mechanism to the named version; separate
   per-stratum reach statements do not establish joint attainability unless the
   written definition supports their coexistence; static structural derivation, not
   construction or execution; not-established joint attainability makes the witness
   unsupported and inadmissible without proving impossibility.
4. Companion record: §8.4 forward-facing supersession marker — the earlier
   owner-ratification requirement is superseded by the recorded delegation and the
   current protocol §11; §8.4 is retained intact as history (record §16.1).

**Rev 7 → Rev 8 changelog (2026-11-06, on the agreed Rev 7 review corrections; final
abstract refinement round).**

1. §4 C6 mechanism-reach standard strengthened: every nonzero `f_j` must be supported
   by an exact, identifiable rule in the assigned mechanism's written definition,
   applicable to the family and assigned version; the complete vector `f` must be
   consistent with the mechanism's limits, exclusions, multiplicity constraints, and
   cross-stratum dependencies; an explicitly ruled-out stratum makes a positive
   component inadmissible; not-established reachability makes the witness unsupported
   and inadmissible **without** proving impossibility — ruled out and not established
   are different findings. The applicable rule text is the C0-pinned annex; citations
   are recorded per witness and the citation standard is frozen before inspection; no
   post-hoc search beyond the pinned text can add support.
2. §4 C6 witnesses: `f` and `u` both mandatory over `ℤ_{≥0}^8` with all eight entries
   explicit, including zeros; an omitted unresolved vector is missing evidence, not an
   implicit zero vector.
3. §4 C6 unresolved-status provenance: every nonzero `u_j` carries documented
   provenance — mutation-attributed (under the mechanism-reach standard) or
   process-attributed (evaluation/recording); unresolved outcomes are never silently
   treated as mutation-induced failures.
4. §4 C6 four-row treatment table for witnesses and absence; invalid witnesses and
   missing records are never evidence of impossibility; cell-level existential PASS
   rule with unassessed parents disclosed as unassessed.
5. §5 reporting population: all 40 `(m, z)` combinations reported; inferential
   assessment only over `S_W × D`; outside-`S_W` combinations (including K5)
   descriptive only; descriptive coverage must not look like inferential eligibility.
6. §6 cell-level existential rule and cross-cell precedence restated; §11 joint
   protocol sign-off defined (settles the text only; authorizes nothing).
7. Companion record: forward-facing supersession note added — the record's operative
   §4 C6 passage (including its older `V_{p,c}`-style indexing) is superseded by Rev
   8's mechanism-specific witness standard and `V_{p,m,z,c}` indexing (record §15.1);
   the earlier text is retained intact as historical evidence.

**Rev 6 → Rev 7 changelog (2026-11-06, on the agreed Rev 6 review corrections).**

1. §4 C6 witnesses: every declared possible C_D value must be backed by an explicit
   structural witness — failure vector `f`, unresolved vector `u`, exact-sum checks
   against `(k_fail, k_unresolved)`, per-stratum record-budget checks against the
   frozen counts `R_j` (`f_j + u_j ≤ R_j`), and the eligible
   version/parent/mechanism/family identity. `V_{p,m,z,c}` is **derived** from
   admissible witnesses; a witness failing any check is discarded and recorded
   `INADMISSIBLE`, never corrected. Declared absence requires a documented structural
   basis; an omitted possibility is not evidence of impossibility.
2. §4/§5 mechanism-specific indexing: `V_{p,m,z,c}` and `O_{p,m,z,c}`; eligible
   versions of one parent aggregate only within the same mechanism, family, and cell —
   never pooled across mechanisms. `P_{m,z,c}` = the parents with nonempty
   `V_{p,m,z,c}`.
3. §5 domain frozen over nonnegative integers with the counting unit fixed: `N` =
   diagnostic bank records per solver body; the freeze record states `N`, the unit,
   the per-stratum record counts `R_1..R_8` (consistency check `N = Σ_j R_j`), and the
   source design specification.
4. §5 reporting rule split into two evidence classes: A2 reports eligible parents and
   the union of possible values; A3 reports observed parents and the union of observed
   values; the classes are never merged in one table.
5. §6 PASS precedence: one passing exact cell suffices for a structural PASS despite
   other `NOT ASSESSABLE` cells, which must be disclosed and never counted as
   supported.
6. Companion record: Rev 6 accepted in substance (record §14); byte status unchanged
   (record §14).

**Rev 5 → Rev 6 changelog (2026-11-06, on the agreed Rev 5 review corrections).**

1. §4 C6 third-parent requirement: C6 now passes only if `|P_{m,z,c}| ≥ 3` **and** the
   cross-parent value difference holds. `P_{m,z,c}` is built from the annex-declared
   possibility sets, not from the family-level `n(m,z)`; a parent's declared inability
   to reach a cell is recorded as **declared absence** and yields a completed
   assessment, not a silent drop.
2. §5 exact-cell domain: `D = { c : k_fail + k_unresolved ≤ N }` fixed by formula
   before inspection, with `N` taken from the frozen design specification and stated
   numerically in the freeze record; out-of-domain cells are reported
   `OUT_OF_DOMAIN`, never assessed.
3. §6 verdict logic: three-way disposition over the frozen domain — PASS; FAIL (all
   relevant assessments complete, none passes); BLOCKED / UNRESOLVED (no pass, at
   least one `NOT ASSESSABLE`). Missing evidence is never silently treated as proof
   that a cell is impossible.
4. §5 A3 rule aligned with C6: observed-value sets `O_{p,c}` with the same
   three-parent and cross-parent-difference structure; no representative value chosen
   after seeing outcomes; A2 can never be a weaker test than the A3 structure
   requires.
5. §5 reporting rule ranges over qualifying pairs and cells `c ∈ D`.
6. Companion record: operative §4 passage updated to the Rev 6 C6 rule (superseded
   wording preserved in record §13.3); byte-verification status updated (protocol
   Rev 5 paste reproduced exactly; record discrepancy open, +2 bytes — record §13.4).

**Rev 4 → Rev 5 changelog (2026-11-06, on the aligned GPT–Claude correction list).**

1. §4 C6 formalized as a family- and cell-specific cross-parent comparison: for
   `(m, z) ∈ S_W` and exact cell `(k_fail, k_unresolved)`, C6 passes iff two different
   effective parent groups have annex-declared possible C_D values `a ∈ V_p`,
   `b ∈ V_q` with `a ≠ b`. Four binding safeguards; the rule is frozen before
   inspection and no representative value is chosen after seeing outcomes.
2. §4 C6 non-disjointness clarification: `V_p` and `V_q` need not be disjoint
   (`{0.5, 1}` vs `{0.5, 0.75}` permits a cross-parent difference); a disjointness
   requirement would wrongly reject valid structural possibilities.
3. §4 C6 evidence standard: the annex must document the possible values; insufficient
   evidence makes C6 `NOT ASSESSABLE` for that pair and cell — never an assumed pass.
   Declared structural possibilities, not verified solver behavior; A3 determines
   realized support.
4. §4 C5 reclassified as a recorded work-order compliance item — never a verdict gate —
   with raw assignment counts distinguished from effective parent counts; effective
   `n(m,z)` shortfalls are assessed under C4.
5. §6: verdict conditions restated at exact-cell granularity; universal C6
   non-assessability maps to `BLOCKED / UNRESOLVED`, not `ASSESSABLE-FAIL`.
6. §11: base64 integrity procedure corrected — integrity is established by hashing the
   **decoded bytes** and comparing against the **source digest**.
7. Companion record retitled as an availability and provenance investigation; its
   historical §8.5 is explicitly superseded by the agreed Option W decision (record
   §12).
8. The unexplained pasted-text byte discrepancy remains disclosed (record §11.6, §12.4);
   no change.

**Rev 3 → Rev 4 changelog (2026-11-06, on GPT's full-text review).**

1. §4 C6 restated. The Rev 3 test ("≥ 2 distinct intended failure vectors") could pass
   mechanisms that cannot produce the required C_D variation, because distinct failure
   vectors can share one Berger–Parker value — `(2,0,0,…)` and `(0,2,0,…)` both give
   `C_D = 1`. C6 now tests whether at least two **different intended C_D values** are
   possible **within the same exact `(k_fail, k_unresolved)` cell**, with an explicit
   evidence standard from the mechanism definition, and a binding scope role: C6 is a
   feasibility screen only and does not modify `S_W` (any change to the `S_W` formula
   requires renewed GPT–Claude agreement and a new frozen protocol version).
2. §5: self-contained `C_D` definition written into the criteria — strata `j = 1..8`,
   `f_j`, `k_fail = Σ f_j`, `C_D = max_j f_j / k_fail`, zero-failure convention,
   `k_unresolved` excluded from the value but part of the cell identity. Parent-level
   value counting added: the two distinct observed values must come from two different
   parent groups; a parent's multiple versions in one cell are recorded but contribute
   one observation; within-parent divergence is correlated variation and never counts
   toward the requirement.
3. §4 C2: unambiguous schedule wording — all 28 unordered pairs at least once; exactly
   two distinct preselected pairs one additional time each; 30 assignments total.
4. §4 C3: the one-to-one assignment-to-parent-ID mapping distinguished from the
   effective independent-parent count after identical-base-source-hash deduplication;
   `n(m,z)` uses the effective count.
5. §6: ASSESSABLE-PASS references C6 in the corrected sense; ASSESSABLE-FAIL states the
   aggregate condition explicitly; C6's verdict role clarified as aggregate-only (no
   silent scope narrowing).
6. §11: byte-exact identity channel for the freeze event added (base64 proposal).
7. Status header updated (Rev 3 reviewed by GPT, not approved; Rev 4 issued for joint
   review).

**Rev 2 → Rev 3 changelog (2026-11-06; retained from Rev 3).**

1. §4 C4: parent-group identity defined — immutable parent ID plus pinned base-source
   hash; variants inherit parent identity and one algorithm-family assignment; counting
   by distinct base parent implementations, never mutation-version rows; same-parent
   versions count once; duplicate-hash dedup.
2. §4 C8 (new): parent-identity and family-assignment ambiguity produces
   BLOCKED / UNRESOLVED (parent ID ↔ multiple hashes or family labels; hash under
   conflicting families; ambiguous mutation assignment never coerced).
3. §5: `k_fail ≥ 2` removed as a separate listed gate and recorded as a mathematical
   consequence of the two-distinct-`C_D`-values requirement, with the documentary note
   that the decision of record lists it; admissible cell set unchanged. Per-cell
   reporting of parent-group and `C_D`-value counts; `NOT_SUPPORTED` label; merging
   prohibited regardless of outcome impact.
4. §6: ASSESSABLE-PASS condition extended to require absence of C8 ambiguity; BLOCKED
   triggers extended accordingly.
5. §7: "reporting is not admission" wording — all 40 cells reported, scope determined
   mechanically within K1–K4; no-qualifying-family mechanisms disclosed as out of scope.
6. §10: `C_D` stated precisely as the Berger–Parker dominance index per the decision of
   record.
7. §11 (new): freeze-event definition (final hashes, version, UTC timestamp, both
   reviewers' agreement) and the agreement ≠ freeze ≠ authorization boundary; auditor
   appointment prerequisite.

**Rev 1 → Rev 2 changelog (2026-11-06; retained from Rev 2).**

1. §7: removed the open Option S/W choice; froze the deterministic bounded-scope rule
   `S_W` (rule frozen pre-access, set computed mechanically post-access).
2. §5: exact-cell A3 support rule — `(m, z, k_fail, k_unresolved)` with ≥ 3 distinct
   parent groups, ≥ 2 distinct observed C_D values; no pooling; not assessable at A2.
3. §8: distinct stage labels `A2 STRUCTURAL PASS` / `A3 REALIZED SUPPORT PASS`.
4. §6: `BLOCKED` renamed `BLOCKED / UNRESOLVED`, with the explicit no-go-but-not-a-
   defect meaning, audit immutability, and the new-versioned-audit / new-protocol-
   version rules.
5. §10: terminology safeguard (mechanisms ≠ diagnostic strata).
6. §2: extended auditor independence attestations (taxonomy, pairs, S-extra, retention)
   and pre-access recording of identity and conflict statement.
7. Freezing basis: joint GPT–Claude agreement under the owner's recorded delegation
   (replacing Rev 1's owner-ratification wording); freezing alone authorizes nothing.

Rev 1 text is preserved in the review exchange of 2026-11-06 and is superseded; no
signed-off frozen version of any prior revision exists.
