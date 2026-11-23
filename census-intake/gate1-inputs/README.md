# Gate 1 inputs — remaining-gap machinery (2026-11-23)

**Status:** DESIGN-STAGE MACHINERY AND PROPOSALS. This directory contains draft roster/family
metadata, annex-intake checks, and pre-registration machinery. It authorizes nothing and executes
nothing. Gate 1 remains **BLOCKED / NOT ASSESSABLE**. The separate C9 diagnostic and held-out input
banks and oracle outputs were generated under Actions run 41591572358; the artifact is publicly
exposed, including the held-out bank. No solver bodies or diagnostic outcome records have been
produced by this package.

**Exact repair test result:** **84/84 tests passed** on CPython 3.13.18 (59 reviewed v0.3
tests + 25 Gate 1 machinery tests), using the exact candidate repair blob bytes on 2026-11-23.
The suite includes a non-demo builder integration test with synthetic inputs. The earlier GLM
72/72 result predates this repair and is retained only as historical context.

## 1. Remaining-gap map

| # | Manifest input | State before 2026-11-23 | State now | Owner of the residual step |
|---|---|---|---|---|
| 1 | Parent roster (G01–G30 + Z_id) | frozen in `PARENT_DESIGN.md` §4 but not instantiated as a census artifact | `PARENT_ROSTER_G01_G30.json` (derived verbatim from the frozen table; Z_id := family interpretation marked ADOPTION-REQUIRED) | GPT + Claude: adopt or correct the Z_id interpretation |
| 2 | Family map (Z identities) | implicit in frozen design | `FAMILY_MAP.json` (K1–K5 with recurrences, complexity, C7 exclusion) | GPT + Claude: adopt |
| 3 | Mutation allocation (8-mechanism taxonomy E1, pair allocation E2, orientation E3, replications E4, S-extra E5) | Allocation not established; standalone-annex existence/completeness remain unproven | Form + auditor provide structural intake; C4 additionally requires an adopted family-map identity and 30 pinned parent-source hashes; C6 note presence only | Owner-supplied mutation content remains owner-exclusive; agents do not invent or reconstruct it |
| 4 | Variant inventory (150 slots) | absent | emitted by `../build_preregistration_manifest.py`; `variant_id`/`q_id` for real builds assigned at construction (opaque permutation, `PARENT_DESIGN.md` §1) | construction phase, after annex + authorization |
| 5 | q registry | absent | scaffold emitted by the builder; identities annex-gated | annex (owner) then construction |
| 6 | Diagnostic bank identity (64 records, 8 per stratum) | Generated under C9 run 41591572358; artifact 13210063805, SHA-256 `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` | Reconcile its record manifest and hashes against the manifest's 64 diagnostic record IDs; held-out data are publicly exposed | Integrate the exact existing bank identity; do not regenerate by assumption |
| 7 | Run-start ledger | absent | emitted by the builder (150 × NOT_STARTED, first start null) | census execution phase |
| 8 | Coverage thresholds | Open; no global floor justified | `GATE1_SUPPORT_COVERAGE_PROPOSAL_V2_2026-11-23.md`: every global floor NOT SET; three verdict outcomes; Gate 1 support separated from Gate 4 power | GPT review → Claude challenge → owner adoption |
| 9 | Operating limits | open (`PARENT_DESIGN.md` §8.3 prerequisite) | `CENSUS_OPERATING_LIMITS_PROPOSAL_V1_2026-11-23.md` (L1–L6; all numeric caps DESIGN_NOT_CALIBRATED) | same adoption chain |
| 10 | Provenance records (generation/build/run) | absent (execution-gated) | builder takes `--provenance-refs`; demo uses SYNTHETIC refs only | execution phase |
| 11 | Diagnostic results for all variants across D1–D8 | absent (0 collected) | **cannot be produced by machinery** — requires construction + execution authorizations | owner authorization chain |

The owner-supplied mutation design remains an owner-exclusive dependency, but it is not the only
remaining work. Parent bodies, a real 150-row inventory, adopted family mapping, pinned parent
source identities, a full C6 witness-adequacy review, diagnostic execution outcomes, and adopted
coverage floors remain outstanding. The existing C9 banks are inputs, not solver outcomes.

## 2. What was built

| File | Role |
|---|---|
| `PARENT_ROSTER_G01_G30.json` | census-form parent roster derived from the frozen design handoff; zero mutation content |
| `FAMILY_MAP.json` | Z identities K1–K5, family counts 7/8/8/5/2, scope constraints (C7, three-parent floor, F-INT) |
| `../ANNEX_INTAKE_FORM_SCHEMA.json` | JSON Schema for the owner annex implementing the frozen C1/C2/C3/C5/C6 structural rules |
| `../ANNEX_INTAKE_FORM_TEMPLATE.json` | fill-in template; every value null; instructions embedded; never a valid submission |
| `../validate_annex.py` | schema blob pin; C1-C3 and C7 structural checks; C4 all-40-cell incidence with parent-hash deduplication, requiring actual ADOPTED family-map bytes and matching SHA-256; C5 compliance reporting only; C6 nonblank note presence only, not adequacy |
| `../build_preregistration_manifest.py` | demo mode verifies synthetic machinery; real mode accepts a construction-supplied 150-row inventory, verifies the five roles per parent and q IDs, requires C4 assessment against the same adopted family-map bytes, and emits a populated q registry plus NOT_STARTED ledger. It never invents real IDs |
| `GATE1_SUPPORT_COVERAGE_PROPOSAL_V2_2026-11-23.md` | global Gate 1 coverage floors NOT SET; PASS/FAIL/NOT ASSESSABLE logic; Gate 1 support separated from Gate 4 power |
| `CENSUS_OPERATING_LIMITS_PROPOSAL_V1_2026-11-23.md` | execution-protocol pin proposal (interpreter, caps, ledger, retry/unresolved rules) |
| `../tests/test_gate1_inputs.py` | 25 tests: roster/family-map integrity; C1-C7 boundaries; C4 identity deduplication and adopted-map binding; C5 compliance-only; C6 presence-only; schema pin; real-inventory validation; q-registry crosswalk; demo and non-demo end-to-end builds |

## 3. Artifact identity

The SHA-256 values in the original GLM v1 packet were working-tree values at that commit.
They are historical and must not be reused for files changed by this repair. The changed-file
Git blob IDs below are content identities for this repair.

| Changed file | Git blob SHA-1 |
|---|---|
| `ANNEX_INTAKE_FORM_SCHEMA.json` | `1cc7bd81701c7cdb1c6f43c7058f59943c8ca25b` |
| `validate_annex.py` | `b687dd511ecfe3e323e044bbdf74e166b2158fef` |
| `build_preregistration_manifest.py` | `f40598b20346502bdf01301e60ccba4cac88fbf0` |
| `tests/test_gate1_inputs.py` | `22c8770661181749b12745927087affe9cbeb2d4` |

Referenced existing frozen artifacts (identity verified from working-tree bytes):

| Artifact | SHA-256 | Git blob SHA-1 |
|---|---|---|
| `PARENT_DESIGN.md` v1.0 (frozen content) | `c6138342af84fe02a64390c2f6a7f4077f0268aa875ad90ee534c76a725f3437` | — (record §2 source 2) |
| `B1_78_CANONICAL_ID_MANIFEST_2026-11-21_v3.json` (eligible `evaluation_row_basis.source_ref`) | `f3289fec5749b76ec4abc743e23f61b889d8831fc055590b034656f4d6bd1989` | `4d2dfe3cf103f210c63b1e9476edf9b9fecfd131` |
| `B1_V1_7_OUTCOME_BLIND_CENSUS_INSTRUMENT_DRAFT_2026-11-22_REV_0_6.md` (draft, unfrozen) | `9012a52abc424279737feb663418b53342b972c52cf003681dc48dfdb2f90c2a` | `becdcbde88f917307328d0ee448d94c9e962489d` |

## 4. Boundary

A passing synthetic demo proves only that the machinery can assemble a schema-conformant
pre-execution manifest from invented IDs. The C9 input-bank artifact exists, but no parent solver
body has been built and no diagnostic outcome record has been collected. Mutation allocation is
not established and is not reconstructed here. C4 remains NOT ASSESSABLE until an adopted
family-map reference and pinned base-source hashes are supplied. C6 checks witness-note presence
only; adequacy remains unassessed. The no-reconstruction rule and authorization chain remain in force.


## 5. GPT C4/C6 workstream update (2026-11-23; append-only)

This dated addendum records subsequent GPT work on the separate branch
`gpt/gate1-c4-c6-machinery-2026-11-23`. Sections 1–4 above are retained as the
historical description of the initial package state; this addendum supplies the
current implementation boundaries.

### C4 source identity

- `validate_annex.py` now requires a source-hash attestation in the parent identity
  manifest and checks the complete 30-parent identity rows, safe relative source
  references, exact family-map binding, family consistency and duplicate-hash rules.
- The A2 auditor is source-blind. It consumes the identity manifest only and does
  not open, parse, compile, import or execute solver source. This preserves Rev 11
  §4's static-audit boundary.
- `build_parent_identity_manifest.py` is a separate source-custody utility. It
  reads exact bytes from an explicitly supplied parent-source index, computes
  SHA-256 values and a canonical bundle digest, and emits the C4 identity manifest.
  It rejects path traversal and symlinks and never executes source.
- A real run of that utility is **not authorized** by this commit. It requires a
  separately recorded owner authorization for a narrow S0-only parent identity
  preparation stage after delivery of the owner allocation and preselection of
  both repeated pairs. No real parent sources or hashes were produced here.
- The source-hash attestation is provenance supplied by the source custodian. The
  A2 auditor verifies the manifest's structure and consistency but does not
  independently recompute those source hashes, because that would require opening
  solver source during A2.

### C6 boundary

C6 still has **not** been assessed. The existing owner-annex schema continues to
require only nonblank `witness_notes`; the auditor reports presence only. The new
`C4_C6_STAGE_RESOLUTION_2026-11-23.md` records the exact Rev 11 witness requirements,
the automation-versus-semantic-review split, and the proposed companion-dossier
boundary. No C6 adequacy verdict, witness vector, mechanism reach, joint-attainability
finding, or structural-absence finding was created.

### New and revised files

| File | Change |
|---|---|
| `../build_parent_identity_manifest.py` | New source-custody hash-manifest tool; hash-only, no import or execution |
| `../tests/test_parent_identity_builder.py` | New synthetic tests for hash computation, duplicate bytes, path safety, symlink rejection and non-execution |
| `C4_C6_STAGE_RESOLUTION_2026-11-23.md` | New unadopted stage-sequencing and C6 review proposal |
| `../validate_annex.py` | C4 consumes a hash-attested identity manifest and remains source-blind |
| `../tests/test_gate1_inputs.py` | Synthetic C4 fixtures updated to include manifest attestation; no real source files |

The C4/C6 workstream does not adopt the roster or family map, supply or infer the
owner mutation allocation, create S0 or mutated solver bodies, emit real variant
IDs or q IDs, execute code, collect outcomes, run the census, fit a model, or
authorize any experiment. Gate 1 remains **BLOCKED / NOT ASSESSABLE**.


## 6. GPT C4/C6 follow-up (2026-11-23; append-only)

This addendum records the additional roster and C6 report-integrity checks. Earlier
sections remain as the historical description of the package at their respective
dates.

### Parent roster adoption is now a separate C4 prerequisite

The source-custody identity manifest now binds both:
- the exact raw bytes of the adopted parent roster (artifact ID, version, SHA-256);
- the exact raw bytes of the adopted family map (artifact ID, SHA-256).

The source-custody builder refuses a roster whose status is not `ADOPTED`. The
source-blind A2 C4 checker also refuses to assess C4 unless the supplied roster is
adopted and its exact-byte SHA-256 matches the identity manifest's roster adoption
reference. A family-map adoption does not imply roster adoption.

Both current repository artifacts remain marked adoption-pending. Consequently,
this additional rule does not change the current verdict: C4 is still
**NOT ASSESSABLE** on current repository inputs.

### C6 dossier bindings strengthened

The proposed C6 dossier schema now pins the exact adopted roster bytes as well as
the annex, parent identity manifest, family map and C4 report. The C6 mechanical
checker requires the roster to be explicitly supplied, adopted and byte-bound to
the identity manifest and C4 report.

Before inspecting witness rows, it validates:
- the C4 report tool identity and version;
- the C4 report's binding to the exact annex bytes;
- all 40 mechanism-by-family incidence rows, including zeros;
- uniqueness and coverage of the 40 cells;
- consistency of each structural-qualification flag with the effective-parent count;
- agreement between the incidence rows and the qualifying-cell list;
- K5's nonqualifying status.

These are report-integrity checks, not a substitute for A2 semantic assessment.
C6 still requires independent human judgement on mechanism reach and joint
attainability. The dossier checker cannot establish structural absence or complete
the full `S_W × D` assessment and never issues the A2 verdict.

No roster or family map was adopted by this addendum. No owner mutation allocation,
real parent source, source hash, witness vector, semantic witness decision, solver,
variant inventory, execution outcome or census was created. The real S0-only identity
preparation stage remains separately unauthorized. Gate 1 remains
**BLOCKED / NOT ASSESSABLE**.


## 7. Latest synthetic CI verification (2026-11-23; append-only)

The complete census-intake unittest discovery suite passed **112 tests** on CPython
3.13.18 at branch head
`3a87cdca7603574a981b43e843f6877538f93137`.

- Workflow run: `45207331100`
- Event: pull request for PR #13
- Test step: `Run census intake and Gate 1 tests`
- Result: `Ran 112 tests ... OK`
- Run URL: https://github.com/foued2/failure-concentration-study/actions/runs/45207331100

This result covers the exact branch head above. The tests use synthetic identifiers,
digests, source-text fixtures, annex definitions, witness vectors and reviewer
attestations. They verify software mechanics only. They do not verify any real
parent-source identity, owner allocation, mutation definition, C6 semantic reach,
joint attainability, structural absence or A2 verdict.

The PR description records the same evidence. Any subsequent commit requires a
new CI result before that result can be described as passing for the newer head.


## 8. C6 protocol and intake-contract pinning (2026-11-23; append-only)

The proposed C6 witness dossier now carries the frozen A2/A3 Rev 11 protocol SHA-256
`530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739` and the
owner-annex intake schema Git blob SHA-1
`1cc7bd81701c7cdb1c6f43c7058f59943c8ca25b`.

The C6 checker enforces both pins and independently checks the exact packaged annex
intake schema blob before validating the owner-supplied annex. A dossier cannot pass
schema validation while naming a different protocol or intake schema.

These are dossier provenance bindings. They do not amend Rev 11, authorize annex
inspection, replace the independent auditor's §2 attestations, or turn mechanical
validation into a semantic reach/joint-attainability decision.
