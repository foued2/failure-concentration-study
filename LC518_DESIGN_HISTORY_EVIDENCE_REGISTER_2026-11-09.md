# LC518/150 — Design-history evidence register (mutation-allocation design inputs)

**Date:** 2026-11-09
**Status:** AUDIT RECORD — design-history evidence register, executed under the
authorization and scope conditions of audit record §30.6 (launch directed by the owner
via the 2026-11-09 relayed review instruction: "Then produce the design-history evidence
register. Do not begin constructing variants yet."). This record authorizes nothing:
no construction, no execution, no annex inspection, no commit, no publication.
**File status:** untracked working-tree file, repository root, branch
`research/concentration-math-spec`. Not committed on any ref. Per the 2026-11-09
instruction, this is a working evidence register — it becomes an authoritative record
only after its findings and wording are owner-reviewed and ratified.
**Record-keeper:** Qoder CLI (GLM role).
**Revision 2 (2026-11-09):** precision corrections applied in place per owner-relayed
review: (i) explicit structural constraints distinguished from allocation details in the
summary; (ii) the owner-channel claim narrowed — conversation history is the primary
*identified* source, not the only possible one; (iii) quotations and hashes made
transparent (full hashes where available). Rev 1 hash
`2d9ddecca004fef78787355fcf090b7f95e5025a14daadfb68afebe3cffb2533` (16,224 bytes) is
superseded; no finding was removed or weakened by these corrections.
**Revision 3 (2026-11-09):** committed locally as `594f1ab` on branch
`research/concentration-math-spec` on the owner's direct instruction ("push it"),
following the owner-relayed review round that produced Rev 2. The push attempt failed
because this environment had no GitHub credentials (no `gh` CLI, no configured
credential helper, no stored HTTPS credential, no SSH key). **Remote publication
remains pending.** The "untracked / not committed on any ref" statement above was true
when written and is superseded by this note. No ratification beyond the owner's own
review is claimed by this record.
**Revision 4 (2026-11-09):** correction commit per owner-relayed review: Rev 3 as
committed in `594f1ab` stated that the record had been pushed to `origin`; that was
false at commit time — the push had failed. An audit record must describe the actual
state, not the intended outcome. Rev 3's text above has been corrected accordingly in
this revision; evidentiary content (§§ 1–7) is unchanged.
**Governing interpretation:** audit record §30 reclassification (2026-11-07): the
mutation allocation is a required design input whose completion as a standalone annex
has not been established; not a lost artifact.
**Boundary compliance:** the sealed preserved archive `lc518_150_review_work.zip` was
not opened; the owner-side conversation history, chat/e-mail delivery channel, private
accounts, and any other machine or backup were not accessed; no channel was searched
beyond the §30.6-reachable sources; no allocation content was reconstructed, proposed,
or pre-filled (work order :45 no-reconstruction rule remains in force).

## 1. Question and method

For each required mutation-design input, classify the examined sources:

- **Explicit** — the element is concretely fixed by a ratified/frozen source.
- **Proposed, not final** — a concrete proposal exists in an examined source without
  final ratification.
- **Not specified** — no examined source contains the element's content.

The examined source set is exactly the §30.6 list, supplemented only by the frozen
protocol (to record its audit-rule expectations) and the B1 decision / C9 review records
(commit-scanned). No other archive, branch content, or channel was opened.

## 2. Sources examined and provenance verification

| # | Source | Location | Identity verification performed 2026-11-09 |
|---|---|---|---|
| 1 | `GLM_WORK_ORDER.md` v1.0 (2026-11-01) | working-tree copy `.qoder_workorder.md` = committed `lc518-150/GLM_WORK_ORDER.md` at `4608922` (+264 lines per worklog entry 29) | SHA-256 recomputed: `5cba2fc2ae30e2d77dcf9037953c6f47ed220e853b4bf89c732080297c9bdb65` = §30.2 pin. VERIFIED |
| 2 | `PARENT_DESIGN.md` v1.0 (FROZEN 2026-11-01) | git object `3e9a29c:lc518-150/glm-handoff/PARENT_DESIGN.md` | sha256 recomputed from git object: `c6138342af84fe02a64390c2f6a7f4077f0268aa875ad90ee534c76a725f3437` = `MANIFEST.md` table and worklog entry 29 freeze hash. VERIFIED. Single-commit file; never revised on any ref |
| 3 | `BANK_DESIGN.md` v1.0 (FROZEN 2026-11-01) | `3e9a29c:lc518-150/glm-handoff/BANK_DESIGN.md` | `da7f8c1ae3c5e3a582c38d91be2463061bce2acb0a772fac72d34459f4b17843`. VERIFIED |
| 4 | `ANALYSIS_SPEC.md` v1.0 (FROZEN 2026-11-01) | `3e9a29c:lc518-150/glm-handoff/ANALYSIS_SPEC.md` | `fb24910cc7712c7e9e27753084ad3683d1fd422a20d875b0b5a4ca33a55f4e78`. VERIFIED |
| 5 | `glm-handoff/worklog.md` (29 entries) | identical at `3e9a29c` and `511bc20` (byte-identical; sha256 `6ee55d9d02b2123ce1bda3243fc8a51e5e312544994f2a724ffddc1ff300990b` recomputed from git objects at both commits) | VERIFIED. Entry 29 = 2026-11-01 ~10:15 UTC LC518-150 round |
| 6 | `LC518_TASK_CONTRACT.md` | `4608922:lc518-150/LC518_TASK_CONTRACT.md` | Keyword scan: contains no mutation-design content (only an unrelated harness note about input-list mutation). Task definition only |
| 7 | Frozen A2/A3 protocol Rev 11 (frozen 2026-11-07) | local base64 `.qoder_b64_protocol.txt`; decoded 51,286 bytes | SHA-256 `530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739` = record §21.4/§25 freeze pin. VERIFIED. Read for audit-rule expectations only |
| 8 | `AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` | `2784297:lc518-150/review-v1.2/AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` | Commit-scanned: defines B1 target and A2-static scope; contains no taxonomy/allocation content. Treats S-extra assignments as annex-dependent (see E5) |
| 9 | `C9_GENERATION_SPEC_REVIEW.md` rev 2.6 | `511bc20:lc518-150/review-v1.2/analysis-revision-2026-11-02/` | Keyword scan: only an authority-boundary mention of private-annex access. Bank-generation spec; no mutation-design content |
| 10 | `LC518_A2_STATIC_ANNEX_AUDIT_2026-11-06.md` | working tree (untracked) | §§ 8.6, 9.4, 30 read directly from file |

`lc518-150/` history: 88 commits across all refs. Reviewed classes: design handoff
`3e9a29c` (2026-11-01); C9 review chain ending `511bc20` (2026-11-02); recovery/containment
chain (2026-11-02–04); B1 decision chain ending `2784297` (2026-11-05). No commit in this
history decides any element in §3.

## 3. The six design elements — register

### E1. Eight-mechanism taxonomy — **NOT SPECIFIED in examined sources**

- Commissioned as owner-supplied (work order :45, verbatim): "The owner **will supply**
  GLM a separate private mutation-design annex containing the **approved** eight-mechanism
  taxonomy and the fixed pair-allocation schedule."
- Pending-slot entry (`ANALYSIS_SPEC.md`, pending-slots table): "Eight-mechanism taxonomy |
  owner's private annex | mutation assignment; §11 compatibility report" — and: "No content
  of the owner's annex is anticipated, invented, or pre-filled."
- `PARENT_DESIGN.md` freeze attestation (header, verbatim): "The private mutation-design
  annex has not been received; per work order line 45, mutation assignment is blocked until
  it arrives."
- Worklog entry 29 (verbatim): "STOP RULE INVOKED (work order :45 + :47): the private
  mutation-design annex and pair-allocation schedule have NOT reached me. I have not
  invented, renamed, merged, or substituted any mechanism."
- No mechanism name, definition, or count-8 list occurs in any examined source. (Frozen
  protocol C1 requires of any supplied annex: "Fail if any mechanism lacks a definition or
  count ≠ 8" — an audit expectation, not taxonomy content.)
- **Conflation guards (record-keeper note):** (a) `BANK_DESIGN.md` strata D1–D8 are
  diagnostic *input strata* (64 bank records), not mutation mechanisms; (b) the 2026-10-31
  "six-family taxonomy (v0.2 instrument)" recorded in earlier worklog entries belongs to the
  pre-LC518 study and is not the eight-mechanism mutation taxonomy. Neither may stand in
  for the taxonomy in any later plan.

### E2. Pair-to-parent allocation — **NOT SPECIFIED** (structural frame explicit; assignment absent)

- Work order :47 (verbatim): "The fixed schedule must cover all 28 unordered pairs of the
  eight mechanisms once, plus two preselected pair replications."
- `ANALYSIS_SPEC.md` pending-slot (verbatim): "Pair-allocation schedule: all 28 unordered
  pairs once + two preselected replications + S-extra balancing | owner's private annex |
  all source construction (replications must be preselected before source construction,
  work order line 47)".
- `PARENT_DESIGN.md` §1 (verbatim): "What is NOT decided here: mutation assignments, pair
  allocations, version roles, solver IDs S001–S150 … Those are governed by the owner's
  private annex."
- Frozen protocol C2 (verbatim, shape rule only): "All 28 unordered mechanism pairs appear
  **at least once**. Exactly **two distinct, preselected pairs** each appear **one
  additional time**, giving **30 assignments in total**." and "Fail if any pair is absent,
  if any pair appears more than twice, if the two replicated pairs are not distinct, or if
  preselection evidence is absent."
- Frozen protocol C3 (verbatim): "The 30 assignments map **one-to-one onto the 30 parent
  IDs** (no parent ID receives two pair assignments)…"
- No examined source maps any pair to any parent G01–G30.

### E3. SA/SB orientation — **NOT SPECIFIED** (role semantics explicit; per-pair rule is annex-declared)

- Work order §3 table (verbatim): "SA | Parent with mutation A only"; "SB | Parent with
  mutation B only"; "SAB | Same parent with mutations A and B together"; "S-extra | Parent
  with one additional single mutation".
- Frozen protocol C3 (verbatim): "the annex declares the SA/SB orientation rule for each
  pair (which mechanism is mutation A) and applies it consistently."
- No examined source declares an orientation rule for any pair.

### E4. Repeated pairs (replications) — **NOT SPECIFIED** (count and timing explicit; identity absent)

- Work order :47 (verbatim): "The two replicated pairs must be chosen before source
  construction, not after outcomes are observed."
- Frozen protocol C2 (verbatim): "The two replications must be preselected — declared
  before construction, not derivable from outcomes."
- No examined source names the two replicated pairs.

### E5. S-extra balancing — **ASSIGNMENTS NOT SPECIFIED** (balancing requirement and target arithmetic explicit; per-parent assignments absent)

- Work order :47 (verbatim): "S-extra assignments must be balanced across the eight
  mechanisms as closely as integer counts permit."
- Frozen protocol C5 (verbatim, recorded work-order compliance item): "The 30 S-extra
  assignments are distributed across the 8 mechanisms as closely as integer counts permit
  (six mechanisms at 4, two at 3, under the work-order wording); the annex's declared
  balancing rule is compared against its realized S-extra column, and deviation…" — the
  six-at-4/two-at-3 arithmetic (6×4 + 2×3 = 30) is an **audit expectation derived from the
  work-order wording**. It is not an allocation and must not be used to fill assignments.
- B1 decision record at `2784297` (verbatim): "The intended nominal count is **90 singly
  mutated versions**: 30 parent groups with three intended single-mutation slots each
  (`SA`, `SB`, and `S-extra`). This is a design count, not a verified realized count. The
  `S-extra` assignments and balancing depend on the private annex."
- No examined source assigns an S-extra mechanism to any parent.

### E6. Parent-family compatibility — **NOT SPECIFIED** (reporting duty explicit; mapping construction-time and taxonomy-gated)

- Work order §11 (verbatim): "Report which intended mutation patterns are compatible with
  each parent family. A mutation that cannot be applied without changing unrelated logic
  must be marked incompatible for that parent; do not silently rewrite the mutation or
  substitute a different mechanism."
- `PARENT_DESIGN.md` §8.2 (verbatim): "Per-family mutation-compatibility report (work
  order §11): requires the taxonomy; will be produced at construction time and marked
  DESIGNED_NOT_VERIFIED."
- Frozen protocol C6: within-cell C_D-value feasibility is an "annex-level screen"; "the
  annex must actually **document** the witnesses". Frozen protocol C7 (verbatim): "No
  (mechanism, K5) cell qualifies; K5 is reportable descriptively only… (Structural basis,
  annex-free: K5 has 2 parent groups, below any three-parent minimum under any schedule.)"
  — the K5 exclusion is explicit and annex-independent.
- No compatibility mapping exists in any examined source.

### Summary table

| Element | Status in examined sources | Explicit frame (sources) |
|---|---|---|
| E1 Eight-mechanism taxonomy | not specified | commissioned owner-supplied (WO :45; AS pending-slot; PD §8/attestation) |
| E2 Pair-to-parent allocation | not specified | 28+2 → 30 structure (WO :47; AS pending-slot; protocol C2/C3) |
| E3 SA/SB orientation | not specified | role semantics (WO §3); annex declares per-pair rule (protocol C3) |
| E4 Repeated pairs | not specified | count = 2, preselection timing (WO :47; protocol C2) |
| E5 S-extra balancing | assignments not specified | balancing wording (WO :47); 6×4+2×3 arithmetic expectation (protocol C5) |
| E6 Parent-family compatibility | not specified | §11 duty (WO; PD §8.2; protocol C6/C7) |

**Overall:** no complete mutation-allocation element is specified in the examined
sources. Certain structural constraints and audit expectations are explicit — the 28+2
pair-count structure and preselection timing (work order :47; protocol C2), the
one-to-one pair-to-parent bijection rule (protocol C3), the 6×4+2×3 S-extra distribution
as an audit expectation (protocol C5), and the K5 scope exclusion (protocol C7) — but
none of them establishes any missing assignment or identity. No element's detailed
content (taxonomy, pair-to-parent assignment, per-pair orientation, replication
identities, S-extra assignments, compatibility mapping) reaches "explicit" or
"proposed, not final" in the examined sources. All six are commissioned-but-unspecified
pending an owner-supplied annex that is not evidenced to exist.

## 4. Verification of §30's documentary bases (provenance check requested 2026-11-09)

1. **Work order** — SHA-256 recomputed
   `5cba2fc2ae30e2d77dcf9037953c6f47ed220e853b4bf89c732080297c9bdb65` = §30.2 pin. VERIFIED.
2. **Worklog entry 29** at `511bc20` — file byte-identical at `3e9a29c` and `511bc20`
   (SHA-256 `6ee55d9d02b2123ce1bda3243fc8a51e5e312544994f2a724ffddc1ff300990b` at both).
   Stop-rule text verbatim in E1. It establishes **non-delivery to GLM** on 2026-11-01 —
   not creation by anyone else. VERIFIED.
3. **Record §8.6 paths text** — read from working tree (lines 274–294): three paths
   (recover if it exists / new allocation design if never created / discontinue) and the
   line "Path 1 therefore also depends on owner knowledge: whether an annex was ever
   authored at all is not determinable from artifacts alone." PRESENT AS QUOTED IN §30.4.
4. **Frozen-protocol non-claim** — decoded protocol (51,286 bytes) SHA-256
   `530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739` = §21.4/§25 pin.
   Full sentence (verbatim, whitespace-normalized): "It does not assert that an annex
   exists, ever existed, or can be recovered, and it does not authorize any search beyond
   what is already recorded (audit record §§3, 9) or construction of a replacement annex —
   path 2 requires its own separate authorization."
   **Note for the record:** §30.1 quotes this sentence truncated at "…can be recovered."
   The quote is accurate as far as it goes; the protocol sentence additionally bars search
   beyond the recorded scope and restates path 2's separate-authorization requirement.
5. **Owner-side statements** (§30.1 GPT correction wording) — not locally verifiable;
   recorded as owner-channel statements consistent with the verified documentary bases.

## 5. Channels not examined (unchanged from §§9.4, 28.2, 29.3)

- The owner's chat/e-mail delivery channel (owner-actionable only).
- The owner's conversation history — the primary *identified* source under §30.6 for
  the "fully designed in conversation" possibility (owner-actionable only). It is
  **not** established as the only possible source: the owner's chat/e-mail delivery
  channel, and any other machine or backup, could equally contain contemporaneous
  design decisions or the annex artifact itself.
- Any other machine or backup.
- `C:\Windows\Temp` (access-denied to this process; §29).
- Contents of the two committed message archives (metadata-level classification only; §29).
- The sealed preserved archive `lc518_150_review_work.zip` — contents known only through
  GPT's breached-boundary report (record §27), which is **not adopted as evidence** by this
  register.

## 6. Non-claims

- "Not specified in examined sources" is not "never specified anywhere." The §28.2
  residual channels remain open; global absence is not claimed.
- This register does not establish that the taxonomy or allocation was never designed; it
  establishes that no examined artifact contains it.
- Nothing here reconstructs, proposes, or pre-fills design content. The no-reconstruction
  rule (work order :45) and the frozen protocol's C0–C8 rules continue to govern any
  supplied or recovered annex.
- If owner-side evidence establishes a completed allocation, its delivery follows C0
  (recorded owner channel; no public commit of annex text). Re-deriving the content would
  be a **new design** (path 2), requiring its own separate authorization — not a recovery.
- This register does not choose among the §6 routes (supply / drop / separately
  authorized new design); it records only what the examined sources establish for each.
  Failure to locate the allocation in the examined sources does not, by itself, justify
  dropping the design.
- Verdict unchanged: **BLOCKED / NOT ASSESSABLE**; 0/150 solver bodies; no construction,
  execution, or commit authorized by this record.

## 7. Planning consequence (record-keeper statement)

Until the owner chooses a §6 route, none of the six elements may be filled from: the 30×5
population total, the 6×4+2×3 S-extra arithmetic, the family counts (K1×7, K2×8, K3×8,
K4×5, K5×2), symmetry, or convenience. Those quantities are frame or audit expectations,
not allocation content. This register is the evidentiary input to the owner's §6 decision;
it does not make that decision, and no 150-variant construction plan may be drafted while
its inputs remain unspecified, except as an explicitly hypothetical planning aid if the
owner requests one.
