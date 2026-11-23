# C4 identity and C6 witness workstream — stage resolution (2026-11-23)

**Status:** GPT working analysis / implementation note. **Not adopted.**
**Scope:** resolve the implementation dependencies around Rev 11 C4 and C6 without
changing the frozen protocol, inventing allocation content, or authorizing source
construction or execution.
**Branch:** \`gpt/gate1-c4-c6-machinery-2026-11-23\`.

## 1. Current evidence

The current Gate 1 package contains a 30-parent roster and K1–K5 family map derived
from the frozen \`PARENT_DESIGN.md\` v1.0. GPT checked the roster and map against the
frozen source: all 30 parent IDs appear exactly once, the family memberships match,
and the counts are K1=7, K2=8, K3=8, K4=5, K5=2. This is a content-consistency
finding only. Both artifacts remain marked pending adoption; they are not adopted by
this note.

The eight-mechanism taxonomy, 30 pair-to-parent assignments, per-pair SA/SB
orientation, the two repeated-pair identities, and the 30 S-extra assignments remain
owner-supplied and unestablished. No values are proposed or reconstructed here.

No real parent solver bodies or parent base-source hashes are available. The existing
C4 intake path previously checked the syntax of the supplied hash strings but did
not establish how those values were obtained. The C4 implementation is now being
separated into source-custody preparation and source-blind A2 intake.

## 2. Governing Rev 11 constraints

Rev 11 §4 defines an effective parent group by immutable parent ID plus pinned
base-source hash. It deduplicates identical source hashes and requires the C4
incidence table over all 40 mechanism-family combinations. The source hash is
therefore not interchangeable with a parent-description hash, a family-map hash,
or a prose design identity.

Rev 11 §4 also states that A2 checks are static text and arithmetic, and that no
solver source is written, read, or executed during the audit. The A2 auditor must
therefore not open source files to recompute their hashes. Any source-byte hashing
must be performed as a separate, explicitly authorized source-custody operation;
the A2 auditor receives and checks the resulting pinned identity manifest only.

Rev 11 C0–C8 and the work-order no-reconstruction rule remain controlling. This note
does not amend either document.

## 3. Proposed C4 preparation sequence

The following is a proposed sequence for resolving the current dependency. It is
**not presently authorized**.

1. **Owner allocation delivery.** The owner supplies the private mutation-design
   annex through the recorded C0 channel. The two repeated pairs must already have
   been preselected before source construction. The annex remains private.
2. **Roster/family-map adoption.** GPT and Claude independently review the roster
   interpretation and family partition. The owner/adoption record must establish
   the family map as ADOPTED and pin its exact SHA-256. The current draft status
   is not sufficient.
3. **Narrow S0-only identity-preparation authorization.** The owner must explicitly
   authorize creation of the 30 unmutated parent source files solely to establish
   base-parent identities. This would create no SA, SB, SAB or S-extra source,
   no opaque S001–S150 variant inventory, no q registry, and no execution or
   diagnostic outcome. The source files must be kept outside the public repository
   unless separately authorized.
4. **Source-custody hash manifest.** A designated custodian uses
   \`build_parent_identity_manifest.py\` with an explicit 30-row parent-to-file
   index. The tool reads exact bytes and computes SHA-256 only; it never imports,
   executes, compiles, parses or modifies source. The resulting manifest records
   the computation method, custodian, UTC time, source-index digest and canonical
   source-bundle digest.
5. **Source-blind C4 intake.** The C4 auditor receives the private owner annex,
   adopted family-map bytes, roster and hash-attested parent identity manifest.
   It does not receive or open source files. It checks manifest completeness,
   identity consistency, family binding, hash format and duplicate-hash rules,
   then computes all 40 n(m,z) cells and the deterministic Option W set.
6. **A2 C6 assessment.** Only after the C4 prerequisites are complete can the C6
   evidence be evaluated over the frozen S_W × D domain.

### Why the narrow S0-only stage needs an owner decision

The parent source hashes required by C4 do not exist before parent source files
exist. Yet the existing stop rule blocks construction pending the allocation gate.
The proposed S0-only identity-preparation stage is intended to resolve that ordering
without constructing any mutation variants.

It is not implied by the earlier general construction authorization. The owner must
explicitly decide whether this limited S0-only step is acceptable before any real
parent source is created. If it is not acceptable, the present C4 dependency cannot
be closed under the current C4 identity rule without a new protocol version and
renewed review. Substituting hashes of design descriptions would change the meaning
of C4 and is not recommended.

## 4. Source-custody tool boundary

The new \`build_parent_identity_manifest.py\` is a preparation tool, not the A2
auditor. Its input index explicitly states which file belongs to each parent; the
tool does not infer parent paths or create source code. It requires an adopted
family map and exact 30-parent coverage. It rejects unsafe relative paths and
symlinks, and it never runs the parent files.

A real invocation is blocked by governance until the owner authorizes the S0-only
identity stage and the real 30 source files and source index exist. Current tests
use synthetic fixture files only; those hashes are not LC518 parent identities.

The A2 C4 checker consumes the resulting manifest. Its attestation fields are
traceability claims from the source custodian, not an assertion that the A2 auditor
independently inspected the source bytes. The exact source index and identity
manifest must be retained and hash-pinned through the recorded private evidence
channel.

## 5. C6 witness adequacy — required content and review split

The existing annex form requires a nonblank \`witness_notes\` field. That check is
only presence detection. It does not satisfy C6.

For each claimed C6 witness, the evidence object must contain:

- the eligible parent, family, mechanism and single-mutation version role (SA, SB
  or S-extra);
- the complete eight-entry failure vector \`f\` and unresolved vector \`u\`, including
  explicit zeros;
- the exact \`(k_fail, k_unresolved)\` cell, with checks
  \`sum(f) = k_fail\`, \`sum(u) = k_unresolved\`, and \`f_j + u_j <= R_j\`;
- evidence for every nonzero failure component, tied to an exact, identifiable
  rule in the pinned definition of the assigned mechanism;
- a joint-attainability rationale showing that the complete vector can arise from
  one coherent application of the mechanism, not merely that each component is
  separately conceivable;
- provenance for every nonzero unresolved component, identifying whether it is
  mutation-attributed or process-attributed;
- any claimed structural absence, supported by affirmative evidence. Omission is
  not evidence of impossibility.

The eight diagnostic strata are not the eight mutation mechanisms. Mechanism reach
must be evaluated against the diagnostic-stratum definitions; those axes must not
be conflated.

### Automated checks versus semantic judgement

Automation can check vector length and type, exact sums, per-stratum budgets,
parent/role/mechanism/family consistency, exact-cell membership in D, quote
presence in the pinned mechanism definition, and exact rational derivation of
C_D from f. It can also group witnesses by effective parent identity after C4 and
test the three-parent/cross-parent-value predicate.

Automation cannot decide whether a quoted mechanism rule genuinely establishes
the claimed stratum reach or whether the complete vector is jointly attainable.
Those decisions require a documented independent human assessment against the
pinned annex text. A quote match is not a semantic pass.

A valid witness requires all nonzero f_j reach findings to be supported and the
joint-attainability finding to be supported. A ruled-out or unsupported component
makes that witness inadmissible. An inadmissible witness is not evidence of
structural impossibility. An absence may be recorded only when its structural basis
is affirmatively documented; otherwise the parent-cell remains NOT ASSESSABLE.

## 6. C6 aggregation and verdict discipline

For each mechanism-family pair in S_W and each exact cell c in D:

1. derive each admissible witness's C_D from its failure vector; do not accept a
   free-standing scalar value;
2. aggregate possible values only within the same effective parent, mechanism,
   family and exact cell;
3. deduplicate effective parent groups by base-source hash within the family;
4. C6 supports the cell only when at least three effective parents have nonempty
   possibility sets and at least two different C_D values occur across different
   parents in that same exact cell;
5. never pool mechanisms, families or adjacent exact cells.

A passing cell can establish the existential C6 condition even if other cells remain
NOT ASSESSABLE, but those unresolved cells must be disclosed. An overall
ASSESSABLE-FAIL requires all relevant C6 cells to have been completely assessed
with no passing cell. If there is no passing cell and at least one relevant cell
remains NOT ASSESSABLE, the aggregate result is BLOCKED / UNRESOLVED.

The semantic review must be performed by an auditor who satisfies Rev 11 §2.
The auditor's independence and conflict attestations must be recorded before annex
access. The validator must not generate or imply those attestations automatically.

## 7. Companion-schema boundary

The pinned v1.0 annex form does not contain structured witness arrays. It must not be
silently altered in place, because its Git blob is pinned by the current auditor.
A structured C6 witness dossier can be developed as a versioned companion artifact,
but its use as part of the C0 annex package requires Claude's review and an explicit
protocol interpretation or new protocol version before any owner annex is inspected.
Until then, the current \`witness_notes\` field remains an intake-presence check only.

## 8. Current state and blockers

| Item | Current state | What closes it |
|---|---|---|
| Roster content | GPT consistency check PASS; adoption pending | Claude independent review, then adoption record |
| Family map content | GPT consistency check PASS; adoption pending | Claude independent review, then adoption record |
| Owner mutation allocation | Not established | Owner-supplied private annex through C0 |
| S0 parent sources | None | Separate owner authorization after allocation delivery |
| Parent source hashes | None | Source-custody hash manifest from authorized S0 files |
| C4 | NOT ASSESSABLE | Adopted family map + complete attested identity manifest + valid allocation |
| C6 | Adequacy not assessed | Versioned witness dossier + independent semantic review |
| Gate 1 | BLOCKED / NOT ASSESSABLE | All controlling prerequisites and separately adopted thresholds |

No solver body has been created by this workstream. No source has been executed.
No diagnostic record or correctness outcome has been collected. No bank was
regenerated or used. No census, predictive fit, simulation or power calculation
was run. No protocol was changed or adopted by this note.

## 7. Owner decision: roster/family adoption and conditional S0 authorization (2026-11-23)

This addendum records the current owner-directed decisions. Earlier sections are retained as historical records of the state at the time they were written; this addendum controls the operative status from this date.

### 7.1 Parent roster and family map adopted

The project owner instructed GPT to finish the outstanding adoption and S0-stage items. Acting on that instruction, the roster and family map are now marked `ADOPTED` in their respective JSON artifacts.

GPT opened the immutable `PARENT_DESIGN.md` v1.0 source at commit `3e9a29c9652a6ab4f6bab0919e386757280b2654`. A row-by-row comparison found all 30 parent IDs and family assignments identical. The family-map membership lists also match exactly. Counts are K1=7, K2=8, K3=8, K4=5, K5=2. The `Z_id` interpretation is adopted as the algorithm-family component (z) of the frozen B1 support key ((m,z,k_{fail},k_{unresolved})); mechanism (m) remains defined only by the owner-supplied annex.

This adoption is limited to the parent roster and family map. It does not establish mutation compatibility, mutation allocations, source identities, source hashes, or solver correctness. Claude's retrospective review remains pending and is not represented as completed.

### 7.2 Narrow S0-only identity-preparation authorization

The owner's instruction is recorded as authorization for a narrowly scoped S0-only identity-preparation stage. **The authorization is conditional and is not yet executable.** Before any parent source file is created, all of the following must be satisfied:

1. The owner supplies the complete private mutation-design annex through the recorded C0 channel.
2. The annex passes the frozen structural intake checks.
3. The identities of the two repeated mechanism pairs and evidence that both were preselected before source construction are recorded in the private annex.

Once those prerequisites are met, the authorized construction scope is exactly 30 unmutated S0 parent source files implementing the frozen G01-G30 design, solely to establish immutable parent base-source identities. Keep the sources outside the public repository. A separately identified source custodian may then create the private hash-only identity manifest from the exact source bytes.

This authorization does **not** authorize SA, SB, SAB or S-extra source construction; S001-S150 variant identities; q IDs or a real variant inventory; source execution, import, test harness evaluation or oracle comparison; bank use or regeneration; diagnostic collection; outcome records; census execution; model fitting; simulation; power or MDE analysis. No source file or source hash has been created by this decision.

### 7.3 C6 and Gate 1 remain blocked

No owner allocation, actual parent source, C4 identity manifest, C4 assessment, C6 witness dossier, eight-stratum witness vector, semantic reach finding, joint-attainability finding or structural-absence finding has been supplied or created. C6 adequacy is therefore **NOT ASSESSED / NOT ASSESSABLE** on current evidence. Mechanical C6 tooling does not replace the independent semantic review required by Rev 11.

Gate 1 remains **BLOCKED / NOT ASSESSABLE**. This decision does not alter the frozen Rev 11 protocol or issue an A2 verdict.
