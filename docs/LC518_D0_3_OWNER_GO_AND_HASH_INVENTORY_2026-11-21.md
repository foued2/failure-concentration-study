# LC518 D0.3 owner GO and pre-inspection artifact inventory

**Record ID:** LC518-D0.3-GO-2026-11-21  
**Date:** 2026-11-21  
**Status:** OWNER GO RECORDED; HASH INVENTORY STARTED; CONTENT COMPARISON NOT YET COMPLETED  
**Repository branch:** `gpt/gate0-scientific-foundation-blueprint-2026-11-20`  
**Scope:** Bounded D0.3 comparison of historical H80 bank rows, canonical identities, oracle outputs, rejection-sidecar attempt history, and the B1 v1.7 78-record development identity source.  
**Authorization source:** Owner instruction in the conversation dated 2026-11-21: (1) AUTHORIZE D0.3 comparison; (2) CONFIRM WITH CONSENT as the selected confirmatory route, subject to consent requirements; (3) PRESERVE exposed artifact 13210063805; (4) NEW 0.21 operational diagnostic-stratum specification. This record documents the owner instruction; it is not a replacement for the formal B1 consent record.

---

## 1. Owner decisions and limits

1. **D0.3 comparison: AUTHORIZED.** The permitted comparison is identity/provenance reconciliation only: H80 raw rows, unique canonical identities, oracle-output keys and row resolution, rejection-sidecar attempt history, and comparison with the B1 v1.7 78-record development identity set where that source can be identified.
2. **Route: CONFIRMATORY, WITH CONSENT.** The route choice is recorded. The accepted B1 v1.7 acceptance record says the joint-consent provenance gap remains open. This owner instruction does not itself create missing historical consent evidence or retroactively cure that gap. Confirmatory evaluation remains blocked until the actual consent record and the other required gates are documented. No outcome evaluation, fitting, calibration, protected-set access, or confirmatory claim is authorized by this D0.3 comparison GO.
3. **Artifact 13210063805: PRESERVE.** Do not delete, alter, replace, or expire it intentionally. Preserve the artifact and its audit metadata. This is a preservation decision, not a determination that the artifact is sealed or that its disclosure can be reversed.
4. **Operational diagnostic strata: NEW v0.21 specification.** Do not silently adopt BANK_DESIGN v1.0 or C9 rev 2.6 as the v0.21 specification. A new versioned v0.21-linked operational specification is the selected route. It must be reviewed and must not change accepted Rev 1.4 or B1 v1.7. No diagnostic manifest is created by this decision.

The present GO does not authorize solver construction, mutation allocation, compilation, execution, diagnostic probing, solver outcome collection, model fitting, simulation, sampling, or power analysis.

## 2. Artifact inventory frozen before content inspection

### 2.1 Historical bank-generation workflow artifact

The GitHub Actions artifact metadata was retrieved before downloading or opening the ZIP.

| Field | Recorded value |
|---|---|
| Repository | `foued2/failure-concentration-study` |
| Workflow run ID | `41591572358` |
| Run head branch | `gpt/lc518-github-recovery-2026-11-02` |
| Run head commit | `a4ec1148698fe6612c5e873f1193069538a206e3` |
| Artifact ID | `13210063805` |
| Artifact name | `lc518-bank-run-41591572358-1` |
| Artifact size | `75,523 bytes` |
| GitHub API digest | `sha256:6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` |
| Created | `2026-11-03T06:43:57Z` |
| Expiry reported by GitHub | `2027-02-01T06:42:22Z` |
| Expired at metadata retrieval | `false` |
| Preservation instruction | Preserve; do not delete |

The digest above is the GitHub Actions artifact archive digest. It is not a substitute for recording SHA-256 hashes of individual files inside the ZIP. No ZIP content has been inspected at the time this inventory was first recorded.

### 2.2 Accepted B1 source records

| Object | Exact source identity | Recorded digest/status |
|---|---|---|
| B1 v1.7 analysis plan | `lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/B1_ANALYSIS_PLAN_2026-11-14_v1.7.md`, branch `gpt/lc518-m1si-audit-2026-11-17`, blob `8c666e501a31726c728447d155045c0b20adc178` | SHA-256 in acceptance record: `797BD9F72CF94FDC0EFF4A03B1544823D4042F8E530B27F4FB70CBD7F2BACA7C` |
| B1 v1.7 acceptance record | `lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/GPT_ACCEPTANCE_RECORD_B1_ANALYSIS_PLAN_V1.7_2026-11-14.md`, branch `gpt/lc518-m1si-audit-2026-11-17`, blob `ea51d72f4f85c5d832d72add561b4c93472c364a` | Acceptance explicitly leaves joint-consent provenance gap open |
| Rev 1.4 Amendment E | `lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/B1_M1_JOINT_INCIDENCE_FEASIBILITY_SPEC_2026-11-12_v1.4.md`, commit `b8b8af042c16eeb9e02077c781ab05c582eeb65d`, blob `3728146356a74363a94fe75a87fd06c483954ee2` | SHA-256 in acceptance record: `C19FC85735072BB8821BD6217B7A2E481BD070B122384026C22BAB358CA03DA6` |
| Rev 1.4 acceptance record | `lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/GPT_ACCEPTANCE_RECORD_REV1_4_AMENDMENT_E_2026-11-14.md`, commit `ca15a29bd25c4c9c2293394f67cb19e1a18f34bd`, blob `074b40980eb96d164cd8411c8995bb1db4af0d46` | Accepted symbolic specification; separate from formal freeze and execution GO |
| Population design v0.21 | `lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.21.md`, branch `gpt/lc518-m1si-audit-2026-11-17`, blob `8af908f6b0ad4cd060194a0a63f4914939f07756` | Design-only draft; new protected evaluation proposal |

### 2.3 B1 identity-source gap

B1 v1.7 and its acceptance record define the fixed development set as 78 canonical records, indexed (r=1,ldots,78), but the reviewed texts do not identify a separate 78-row source manifest by repository path and immutable hash. The analysis plan's symbolic row index is not itself an identity manifest.

The comparison must not silently define the B1 set as the H80 oracle key list merely because the counts match. First inspect the authorized archive to identify its files and provenance. Then determine whether there is a separately identifiable B1 78-record manifest/source. If no such source can be located among the authorized records, record the B1 side of the identity comparison as **NOT ESTABLISHED / SOURCE MISSING**. Do not substitute an assumed source.

## 3. D0.3 comparison protocol

After this inventory is committed, the archive may be downloaded and inspected within the owner-authorized scope.

1. Verify the downloaded ZIP against the recorded GitHub artifact archive digest before extraction.
2. Inventory every ZIP member name, uncompressed byte size and SHA-256. Record those hashes before parsing bank, oracle, or sidecar contents.
3. Identify the exact H80 bank file, H80 oracle-output file, rejection sidecar, and canonical-disjointness/publication report. Record absent files as absent; do not assume C9's proposed schema was implemented.
4. Parse only these named artifacts. Do not inspect solver code, solver outputs, protected E3 contents, other artifacts, or unrelated files.
5. Validate each H80 input against the distinct-denomination task contract. A repeated denomination is an immediate input-domain violation and stops identity reconciliation for the affected source.
6. Compute canonical keys as `(amount, tuple(sorted(coins)))`. Sorting removes order dependence while preserving multiplicity; never use a set to normalize denominations.
7. Reconcile 80 raw H80 rows to the number and exact keys of oracle-output objects. Each accepted raw row must resolve to exactly one oracle object by canonical key; every distinct key must have exactly one oracle object; missing and extra keys are errors.
8. Reconcile rejection-sidecar rows separately as rejected candidate-attempt history, using the actual sidecar schema and pinned generator/publication records. Do not subtract rejected attempts from accepted final rows and do not interpret a sidecar event count as an oracle-output shortfall.
9. Compare H80's exact canonical-key set against an independently identified B1 78-row source using the same key. Report raw rows, unique keys, oracle keys, B1 keys, duplicate multiplicities, intersections, set differences, row-to-oracle resolution, sidecar-attempt reconciliation, and all hashes.
10. Do not inspect E3 or claim E3 contamination. E3 requires its own separately authorized identity/custody review.

## 4. Predeclared interpretation

- 80 H80 rows, 78 unique H80 keys, 78 exact oracle keys, and equality with an independently identified B1 key set supports H80/B1 identity equality. It does not make their analytical roles interchangeable.
- 80 unique H80 keys but only 78 oracle keys is a missing-output or schema/acceptance defect; sidecar event count alone cannot repair it.
- 78 H80 keys and 78 oracle keys but a different B1 key set rejects the identity-equality hypothesis.
- Partial intersection means partial overlap; neither complete identity nor disjointness may be claimed.
- If the independent B1 identity source cannot be identified, report only the H80 row-to-oracle reconciliation. The B1 identity relationship remains **OPEN**, notwithstanding a matching count.

## 5. Confirmatory route: consent and remaining gates

The owner selected a confirmatory route **with consent**. The B1 v1.7 acceptance record explicitly states that the joint-consent provenance gap remains open. Before confirmatory evaluation, the project must locate and verify the actual consent evidence, identify whose consent was required, verify its scope and date relative to the B1 decision, and document whether it authorizes the proposed use. A current owner instruction does not retroactively create consent at the time of the earlier decision.

The following remain separate gates and must be closed with evidence:
- consent provenance for the 2026-11-05 B1 decision record;
- independent protected-set custodian identified and appointed;
- trigger-(i) separation interpretation ratified;
- separate B1 amendment defining the new protected evaluation set and changed record population/scoring design;
- independent review and GPT adjudication of that amendment;
- all required isolation, custody, computational and execution safeguards.

No confirmatory evaluation is authorized until those gates close. The current D0.3 comparison is documentary identity reconciliation, not confirmatory testing.

## 6. Artifact preservation

Artifact `13210063805` is to be preserved. Do not delete it as part of this work. Record its current GitHub ID, run ID, name, size, digest, creation time and expiry. If a later owner decision proposes deletion, that is a separate action requiring an explicit new instruction and a prior preservation/custody assessment. Deletion would not reverse prior disclosure.

## 7. Separate v0.21 specification route

A new v0.21-linked operational D1–D8 specification is the selected route. It must be a new, reviewable document with its own version and immutable hash. It must:
- distinguish input-property strata from mutation/operator mechanisms;
- define one deterministic, outcome-blind assigned stratum per diagnostic record;
- preserve the accepted eight-stratum/eight-record symbolic structure unless a separately reviewed B1 amendment changes it;
- specify canonical identities, duplicate/dependence accounting, record counts and pair IDs;
- resolve D4's heterogeneity, D5's actual LC518 combination-count validity, and D6's record-versus-pair measurement without importing unratified C9 details as authority;
- define the relationship to the evaluation target and prohibit diagnostic-to-evaluation leakage;
- state how future manifest hashes, oracle keys, and validation reports will be frozen;
- leave mutation allocation and solver execution outside this specification and outside the present GO.

The specification must not claim that eight strata are eight causal mechanisms, must not invent a mutation-to-stratum mapping, and must not alter B1 v1.7 or Rev 1.4 in place.

---

**Current disposition:** D0.3 comparison GO is recorded; pre-inspection artifact metadata and source hashes are recorded above; archive contents are not yet inspected. Confirmatory route selected but consent/custody/amendment gates remain open. Artifact 13210063805 is preserved. New v0.21 operational specification is selected for separate drafting and review. The exact B1 78-row identity source remains to be identified.