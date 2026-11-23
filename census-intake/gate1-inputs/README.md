# Gate 1 inputs — remaining-gap machinery (2026-11-23)

**Status:** DESIGN-STAGE MACHINERY AND PROPOSALS. This directory closes, to the maximum extent
permitted by the standing authorizations, the input gaps GPT enumerated on 2026-11-23 ("a defined
list of parent algorithms; a frozen list of their variants; diagnostic results; evidence records
satisfy the protocol"). It authorizes nothing and executes nothing. Gate 1 remains **BLOCKED / NOT
ASSESSABLE**.

**Verification at commit time:** full census-intake suite **72/72 OK** (59 reviewed v0.3 tests +
13 new tests in `tests/test_gate1_inputs.py`); the demo-synthetic pre-registration manifest passes
the reviewed intake checker with decision
`LOCAL_SCHEMA_AND_SEMANTIC_CHECKS_PASS_EXTERNAL_CHECKS_NOT_PERFORMED` (exit 0, 150/150 variants,
all `EXPECTED_NOT_RUN`, ledger all `NOT_STARTED`).

## 1. Remaining-gap map

| # | Manifest input | State before 2026-11-23 | State now | Owner of the residual step |
|---|---|---|---|---|
| 1 | Parent roster (G01–G30 + Z_id) | frozen in `PARENT_DESIGN.md` §4 but not instantiated as a census artifact | `PARENT_ROSTER_G01_G30.json` (derived verbatim from the frozen table; Z_id := family interpretation marked ADOPTION-REQUIRED) | GPT + Claude: adopt or correct the Z_id interpretation |
| 2 | Family map (Z identities) | implicit in frozen design | `FAMILY_MAP.json` (K1–K5 with recurrences, complexity, C7 exclusion) | GPT + Claude: adopt |
| 3 | Mutation allocation (8-mechanism taxonomy E1, pair allocation E2, orientation E3, replications E4, S-extra E5) | **never supplied**; owner's private annex never arrived; no-reconstruction rule in force | `../ANNEX_INTAKE_FORM_SCHEMA.json` + `../ANNEX_INTAKE_FORM_TEMPLATE.json` + `../validate_annex.py`: the owner can now fill a machine-readable form and get a mechanical C1–C7 audit instantly | **FOUED (owner), exclusively** — supply annex per protocol C0; no agent may draft this content |
| 4 | Variant inventory (150 slots) | absent | emitted by `../build_preregistration_manifest.py`; `variant_id`/`q_id` for real builds assigned at construction (opaque permutation, `PARENT_DESIGN.md` §1) | construction phase, after annex + authorization |
| 5 | q registry | absent | scaffold emitted by the builder; identities annex-gated | annex (owner) then construction |
| 6 | Diagnostic bank identity (64 records, 8 per stratum) | absent; bank generation/access never authorized | builder takes a `--bank-identity` input; nothing fabricated | separate authorization, then generation phase |
| 7 | Run-start ledger | absent | emitted by the builder (150 × NOT_STARTED, first start null) | census execution phase |
| 8 | Coverage thresholds | **open** (named by GPT as the reason a 0.6 census would be descriptive only) | `GATE1_COVERAGE_THRESHOLDS_PROPOSAL_V1_2026-11-23.md` (T0–T5, each value cited to frozen records; DECISION marks explicit) | GPT review → Claude challenge window → owner ratification |
| 9 | Operating limits | open (`PARENT_DESIGN.md` §8.3 prerequisite) | `CENSUS_OPERATING_LIMITS_PROPOSAL_V1_2026-11-23.md` (L1–L6; all numeric caps DESIGN_NOT_CALIBRATED) | same adoption chain |
| 10 | Provenance records (generation/build/run) | absent (execution-gated) | builder takes `--provenance-refs`; demo uses SYNTHETIC refs only | execution phase |
| 11 | Diagnostic results for all variants across D1–D8 | absent (0 collected) | **cannot be produced by machinery** — requires construction + execution authorizations | owner authorization chain |

Exactly one remaining input is owner-exclusive: **item 3, the mutation-design annex**. Everything
else is either derived here for adoption, emitted mechanically, or gated behind the authorization
chain in a stated order.

## 2. What was built

| File | Role |
|---|---|
| `PARENT_ROSTER_G01_G30.json` | census-form parent roster derived from the frozen design handoff; zero mutation content |
| `FAMILY_MAP.json` | Z identities K1–K5, family counts 7/8/8/5/2, scope constraints (C7, three-parent floor, F-INT) |
| `../ANNEX_INTAKE_FORM_SCHEMA.json` | JSON Schema for the owner annex implementing the frozen C1/C2/C3/C5/C6 structural rules |
| `../ANNEX_INTAKE_FORM_TEMPLATE.json` | fill-in template; every value null; instructions embedded; never a valid submission |
| `../validate_annex.py` | mechanical C1–C7 auditor; fail-closed; reports deviations, repairs nothing |
| `../build_preregistration_manifest.py` | assembles the 17-field pre-execution manifest (all `EXPECTED_NOT_RUN`, outcome-blind assertion false) and emits the q registry, variant inventory and run-start ledger it references, each pinned by SHA-256 + Git blob SHA-1; `--demo-synthetic` mode for machinery verification only |
| `GATE1_COVERAGE_THRESHOLDS_PROPOSAL_V1_2026-11-23.md` | the open numerical thresholds, proposed with citations |
| `CENSUS_OPERATING_LIMITS_PROPOSAL_V1_2026-11-23.md` | execution-protocol pin proposal (interpreter, caps, ledger, retry/unresolved rules) |
| `../tests/test_gate1_inputs.py` | 13 tests: roster/family-map integrity, auditor adversarial cases, end-to-end demo build through the reviewed intake checker |

## 3. Artifact hashes (SHA-256, working-tree bytes at commit time)

| File | SHA-256 |
|---|---|
| `PARENT_ROSTER_G01_G30.json` | `5cf2492943a57ed79fa5fe4abb6d9037a66180d525402611bc33ab2d6e532d01` |
| `FAMILY_MAP.json` | `078d545cbeb49dc67ccb9decf5f46e283ac4abb6384e38ddf7aef03a89d58821` |
| `../ANNEX_INTAKE_FORM_SCHEMA.json` | `5669f0187176be32f1254d7f05b0b60d356f181190a3562cd7baf6f3ba79d694` |
| `../ANNEX_INTAKE_FORM_TEMPLATE.json` | `7def55022b0151ee3716db1915ca99c08af76c6adaceb240b84723cd58ac670a` |
| `../validate_annex.py` | `89e645a7bb6926aa2f86a4f614e273842af30be0e6c0ef4bd7ed7f437f0b35f7` |
| `../build_preregistration_manifest.py` | `5249fcd25969f9b5944f6c5909350e188184aa48a1b6536b71722ab10a3dbd41` |
| `GATE1_COVERAGE_THRESHOLDS_PROPOSAL_V1_2026-11-23.md` | `9f13d93ac7d34f9640624b674bee92822908d4536d8621c7998c11461fe3aec0` |
| `CENSUS_OPERATING_LIMITS_PROPOSAL_V1_2026-11-23.md` | `6f7861f0fb603075bfb8ca7e7efef6e4db5e2db8f03ce1558865c9500d32fdf1` |
| `../tests/test_gate1_inputs.py` | `55e0fb6e2070aefda45d67ce2164f39b98b61054ce963d89ff586a66b156bd39` |

Referenced existing frozen artifacts (identity verified from working-tree bytes):

| Artifact | SHA-256 | Git blob SHA-1 |
|---|---|---|
| `PARENT_DESIGN.md` v1.0 (frozen content) | `c6138342af84fe02a64390c2f6a7f4077f0268aa875ad90ee534c76a725f3437` | — (record §2 source 2) |
| `B1_78_CANONICAL_ID_MANIFEST_2026-11-21_v3.json` (eligible `evaluation_row_basis.source_ref`) | `f3289fec5749b76ec4abc743e23f61b889d8831fc055590b034656f4d6bd1989` | `4d2dfe3cf103f210c63b1e9476edf9b9fecfd131` |
| `B1_V1_7_OUTCOME_BLIND_CENSUS_INSTRUMENT_DRAFT_2026-11-22_REV_0_6.md` (draft, unfrozen) | `9012a52abc424279737feb663418b53342b972c52cf003681dc48dfdb2f90c2a` | `becdcbde88f917307328d0ee448d94c9e962489d` |

## 4. Boundary

A passing intake check on the demo manifest proves schema and local-semantic conformance of the
machinery, nothing more. No bank exists, no parent body exists, no diagnostic record exists, and no
allocation content was invented anywhere in this directory. The no-reconstruction rule (work order
line 45) and the step-1 scope record (2026-11-22) continue to govern every next step.
