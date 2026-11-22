# LC518 B1 v1.7 outcome-blind support census instrument

**Document ID:** LC518-B1-V1.7-CENSUS-INSTRUMENT-DRAFT-2026-11-22  
**Version:** 0.4-draft  
**Prepared:** 2026-11-22  
**Status:** REVISED AFTER CLAUDE ROUND 3 AND OPUS REVIEW; AWAITING READ-ONLY RE-REVIEW; NOT OWNER-ACCEPTED; NOT FROZEN; NOT EXECUTABLE  
**Scope:** B1 v1.7 outcome-blind full-population and leave-one-parent-out (LOPO) predictor-support census.  
**Reporting mode:** DESCRIPTIVE ONLY. No numeric coverage floors are adopted. For complete validated inputs, the coverage field is `NO COVERAGE VERDICT — DESCRIPTIVE ONLY; THRESHOLDS NOT SET`; `NOT ASSESSABLE` is reserved for incomplete, invalid or contradictory input/instrument conditions. No overall Gate 1 PASS or FAIL is permitted.

---

## 0. Authority and scope boundary

This document turns the frozen B1 v1.7 support rules and the LOPO coverage-reconciliation proposal into a proposed input schema, counting procedure, report format and verdict rule.

The owner has conditionally authorised the outcome-blind census itself once all prerequisites exist. This document is preparatory design only. It does not make those prerequisites exist, does not execute a census, and does not authorise any upstream activity.

The instrument is strictly limited to predictor-support arithmetic. It must not read or accept correctness outcomes, construct the B1 outcome matrix, fit either predictive model, calculate log loss, run the permutation procedure, evaluate operating characteristics, simulate data, or estimate power.

The first census is descriptive-only because no numerical floors have been selected for `rho_min`, `rho_cell` or `rho_rec`. These floors must not be chosen after a realised diagnostic manifest exists. A complete, validated census with floors unset receives the distinct status `NO COVERAGE VERDICT — DESCRIPTIVE ONLY; THRESHOLDS NOT SET`. It is not labelled `NOT ASSESSABLE`: that label is reserved for missing, incomplete, contradictory or invalid inputs/instrument conditions. No overall `SUPPORTED` or `NOT SUPPORTED` coverage verdict, and no overall Gate 1 PASS or FAIL, may be produced while the floors remain unset.

The evaluation route remains `UNRESOLVED / NOT CLEARED`. Nothing in this instrument designates the public 78-record B1 development set as confirmatory or claims that a protected confirmatory route exists. Operating/resource ceilings and all upstream production GOs also remain open.

This instrument uses the exact-cell coordinate already named by B1 v1.7: `(q, Z, k_fail, k_unresolved)`. It does not redefine `q`, invent mutation identities, substitute the M1-si operator-class coding, or add `a(v)` as a cell coordinate. Actual q identities and assignments must be separately operationalised and frozen consistently with B1 v1.7 before diagnostic execution. Parent-family assignments must likewise be frozen before diagnostic execution.

## 1. Controlling sources

The instrument must be checked against these exact records before any freeze:

1. **[B1 analysis plan v1.7](https://github.com/foued2/failure-concentration-study/blob/gpt/b1-m1-rev1.2-review-chain-2026-11-14/lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/B1_ANALYSIS_PLAN_2026-11-14_v1.7.md)**, accepted and frozen as a symbolic analysis plan, not an execution GO. Blob: `8c666e501a31726c728447d155045c0b20adc178`. Its [acceptance record](https://github.com/foued2/failure-concentration-study/blob/gpt/b1-m1-rev1.2-review-chain-2026-11-14/lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/GPT_ACCEPTANCE_RECORD_B1_ANALYSIS_PLAN_V1.7_2026-11-14.md) is blob `ea51d72f4f85c5d832d72add561b4c93472c364a`. Sections 1–3 govern the primary sample, exact-cell support, LOPO folds and fold estimability; §§5 and 12–13 establish the wider boundary and non-authorisation.
2. **[LOPO estimability reconciliation](https://github.com/foued2/failure-concentration-study/blob/gpt/gate1-preparatory-reconciliation-2026-11-22/reviews/analytical-validity-2026-11-18/LOPO_ESTIMABILITY_RECONCILIATION_2026-11-19.md)**, 2026-11-19, blob `9aba50d46cbf9c905a4dc121c1b0b1e460ed739f`. It confirms that fold-level support and coverage reporting already exist in B1 v1.7, while a pre-declared minimum-coverage verdict gate is missing. It proposes the three coverage measures but leaves their numerical floors to an owner/adjudicator decision.
3. **[C_D measurement specification and exposure register](https://github.com/foued2/failure-concentration-study/blob/gpt/gate1-preparatory-reconciliation-2026-11-22/reviews/analytical-validity-2026-11-18/CD_MEASUREMENT_SPEC_2026-11-19.md)**, 2026-11-19, blob `923655f20337b99f11e400f3428d1d18ac34c96d`. It quotes Rev 11's eight-element definite-failure vector `f`, eight-element unresolved vector `u`, record-level exposure basis, and separate `k_fail` / `k_unresolved` definitions. It also records that the diagnostic record basis and the 78-record canonical evaluation basis are distinct measurement layers.
4. **[Gate 1 preparatory reconciliation](https://github.com/foued2/failure-concentration-study/blob/gpt/gate1-preparatory-reconciliation-2026-11-22/reviews/analytical-validity-2026-11-18/GATE1_PREPARATORY_RECONCILIATION_2026-11-22.md)**, 2026-11-22, blob `eeaed8eaa59f2c055b6749a42edb0e2b98cdca91`. It records the conditional census authorisation, readiness blockers, q/M1-si boundary, unresolved evaluation route and prerequisites.

Frozen B1 v1.7 prevails wherever this draft might be read as changing its statistical rules. Any ambiguity found in this review must be resolved before the instrument is frozen, not silently resolved in code.

## 2. Target quantities and unit of counting

### 2.1 Primary B1 cell

For each valid diagnostic variant `v`, the exact B1 cell is:

`c(v) = (q(v), Z(v), k_fail(v), k_unresolved(v))`.

Here:

- `q` is the B1 v1.7 mutation-identity coordinate. It is not supplied by the D1–D8 diagnostic-strata taxonomy.
- `Z` is the parent-family coordinate.
- `k_fail` is the sum of definite failures across the eight diagnostic input strata.
- `k_unresolved` is the sum of unresolved diagnostic records across those same eight strata. It is not part of `C_D`.

There is no pooling across q, Z, `k_fail` or `k_unresolved`.

### 2.2 Diagnostic exposure basis

Use the Rev 11 **record-level diagnostic exposure basis** for the census: 64 diagnostic bank records per variant, eight records in each of the eight strata D1–D8. Do not deduplicate diagnostic presentations or substitute the 60-record canonical diagnostic basis. This does not alter B1's separate 78-canonical-record correctness-row structure; the census does not access that outcome data.

The diagnostic bank identity, version, record IDs, D1–D8 mapping and content hash must be frozen before diagnostic execution. This draft does not invent the contents or identities of a diagnostic bank that has not yet been generated and authorised.

**Exposure disclosure required for interpretation, with historical and future layers kept separate:** the known historical D1–D8 candidate-selection lineage screened diagnostic candidates against the publicly exposed B1 held-out bank. The manifest must preserve that historical fact and the evidence/status of its reconstruction. This is a disclosure about the already-existing selection lineage; it is not an instruction that a future diagnostic-bank generation protocol must again screen newly generated records against the B1 bank. The future generation protocol must separately specify whether its own selection process uses public held-out-bank information, does not use it, or has not yet specified the matter. The eventual manifest must record the actual frozen protocol choice and its protocol reference; NOT_YET_SPECIFIED is permissible in a design/preflight record but blocks a final census run. The historical and future fields must not be conflated. The inference restriction is unconditional: independence_claim_permitted remains false because the known historical candidate-selection lineage was conditioned on an exposed bank, even if the future generation protocol does not reuse that information. Non-overlap of generated diagnostic records with the public bank does not establish independent sampling. This disclosure is mandatory metadata, not an outcome, correctness label or coverage arithmetic input.

### 2.3 Derived quantities

For each valid variant:

- `f_j` = number of definite failures among the eight diagnostic records in stratum `D_j`.
- `u_j` = number of unresolved results among those eight records in `D_j`.
- `p_j` = number of definite passes in `D_j`, if the three terminal states are exhaustive.
- Require `f_j + u_j + p_j = 8` for every stratum when the complete record-level observations are available.
- `k_fail = sum(f_1, ..., f_8)`.
- `k_unresolved = sum(u_1, ..., u_8)`.
- For `k_fail > 0`, `C_D = max(f_1, ..., f_8) / k_fail`.

Retain all eight `f_j` and all eight `u_j` values. A total unresolved count alone is not sufficient evidence for this measurement layer. Unresolved results must never be recoded as definite failures or passes.

For `k_fail = 0`, report the explicit state `NO OBSERVED FAILURES`; it is not a concentration-variation observation and cannot enter a B1 primary cell. B1 v1.7 §3.2 (which cites Rev 1.4 §7.2) and the C_D Measurement Specification Rev 11 §4 document the numeric-zero display convention for this edge case. This instrument preserves the separate `NO OBSERVED FAILURES` state and does not use the display zero as an observed concentration level, a contributor to `D_c`, or a contributor to `W_C`. The B1 primary sample independently requires `k_fail >= 2`, so the display convention does not affect any eligible primary cell. For `k_fail = 1`, the computed ratio is reportable descriptively, but the variant cannot enter a B1 primary cell because the frozen B1 requirement is `k_fail >= 2`.

For every support or coverage decision, use exact arithmetic. Represent each `C_D` as a reduced exact rational number. Compute `D_c` by exact rational identity. Compute `mean_C_D_train` as an exact rational mean and `W_C_train = sum_v (C_D(v) - mean_C_D_train)^2` as an exact rational sum of squares. The decision `W_C_train > 0` must be evaluated exactly; it is always decidable from these rational inputs and has no floating-point fallback. Integer counts (`G_c`, `G_train`, `D_c`, `D_train`, variant counts and row counts) remain exact integers. All eligibility, estimability and coverage-numerator decisions must use these exact values. Decimal values may be added for display only and must never determine a gate, comparison, status or fraction.

## 3. Proposed input schema

The companion `B1_V1_7_CENSUS_MANIFEST_SCHEMA_DRAFT_0_4.json` is a machine-readable JSON Schema draft, not an accepted or frozen schema. It constrains the manifest shape and, for `VALID` variants, the 64-record / eight-per-stratum structure. It does not replace the semantic validator: cross-file identity matching, unique record IDs, complete variant-inventory matching, status logic, exclusion timing, exposure-history interpretation and derived-count checks require explicit semantic tests. The JSON Schema draft and this specification must be reviewed together; both remain unfrozen.

### 3.1 Manifest envelope

The manifest should contain:

| Field | Requirement |
|---|---|
| `schema_version` | Exact version of the B1-specific census schema. |
| `study_id` | Fixed LC518 study identifier. |
| `analysis_plan` | B1 v1.7 identifier, version, Git blob SHA and SHA-256. |
| `measurement_spec` | Rev 11 / measurement-spec identifier and exact version/hash. |
| `measurement_basis` | Literal `record_level_64`; no per-row switching of basis. |
| `evaluation_row_basis` | Frozen expected evaluation-row count N_eval_rows and a version/hash reference to the configuration that supplies it. Current B1 v1.7 development configuration uses 78; this is a count parameter, not a confirmatory-route designation. |
| `diagnostic_bank` | Bank ID, version, content SHA-256, record-manifest hash, exact D1–D8 labels and eight-record-per-stratum exposure vector. |
| `diagnostic_exposure_disclosure` | Separate historical D1–D8 candidate-selection exposure from the future bank-generation protocol selection choice; retain evidence for both; independence_claim_permitted is always false. |
| `parent_roster_ref` | Frozen parent-roster file/version/hash, including all roster parents whether or not they yield an eligible variant. |
| `q_registry_ref` | Frozen B1-consistent q identity register/version/hash and assignment-map reference. This field references identities; the census does not create them. |
| `family_map_ref` | Frozen parent-family Z mapping/version/hash. |
| `variant_inventory_ref` | Frozen expected variant inventory/version/hash, so omissions can be detected rather than silently dropped. |
| `diagnostic_run_start_ledger` | Required frozen-inventory run-start ledger reference, campaign-wide first diagnostic execution timestamp (or explicit null when no variant has started), and ledger snapshot timestamp. The referenced ledger must contain exactly one execution-state row per expected variant, including explicit `NOT_STARTED` rows. A null first-start timestamp is valid only when every ledger row is `NOT_STARTED`; otherwise the timestamp must equal the earliest per-variant start. It is the timing authority for pre-diagnostic status checks. |
| `provenance` | Generator/build/diagnostic-run identifiers and source/artifact hashes, with references to retained evidence. |
| `variants` | One entry for every variant in the frozen inventory, including explicit invalid, excluded, incomplete or expected-not-run states. |
| `outcome_exclusion_assertion` | Explicit statement that no B1 correctness outcome, score, fitted value or outcome label is included or consulted. |

No parent count, variant count, q identity, bank record ID or resource ceiling is invented by this schema. Those are upstream design/owner decisions.

### 3.2 Variant entry

Each variant entry should contain:

| Field | Requirement |
|---|---|
| `variant_id` | Unique stable identity for the runnable study variant. |
| `parent_id` | Stable identity of its source parent implementation. |
| `Z_id` | Frozen B1 parent-family assignment. Must agree with the frozen family map. |
| `q_id` | Frozen B1 v1.7 mutation identity. Must resolve through the frozen q register. |
| `semantic_source_digest` | Digest of the exact semantic source when a source was produced; mandatory for `VALID`, otherwise retained when applicable. |
| `runnable_artifact_digest` | Digest of the exact runnable artifact evaluated diagnostically; mandatory for `VALID`, otherwise retained when an artifact was produced. |
| `validity_status` | One of `VALID`, `INVALID`, `EXCLUDED_BEFORE_DIAGNOSTICS`, `INCOMPLETE`, or `EXPECTED_NOT_RUN`, under the frozen status rules below. |
| `status_reason` | Required explanation for every non-`VALID` status. No silent omission. |
| `status_decision` | For every non-`VALID` status, a dated, evidence-backed reference to the frozen rule and decision record. It separately asserts that terminal result values and derived failure/unresolved counts were not consulted. It may state whether record-presence/identity metadata was consulted, which is permitted only for the post-run completeness audit. |
| `diagnostic_record_results` | Exactly the 64 record-level results for `VALID`; zero for pre-diagnostic `INVALID`, `EXCLUDED_BEFORE_DIAGNOSTICS` or `EXPECTED_NOT_RUN`; up to 63 received records for `INCOMPLETE`. |
| `diagnostic_evidence_ref` | Stable reference/hash for retained diagnostic execution/receipt evidence; mandatory for `VALID` and `INCOMPLETE`. For INCOMPLETE, it identifies retained run/receipt evidence for the received set, including an explicit zero-record receipt when the run started but yielded no records; it is not a substitute for status-decision evidence. |

Each diagnostic result contains `diagnostic_record_id`, `stratum_id` (`D1` through `D8`) and one terminal result status: `DEFINITE_PASS`, `DEFINITE_FAILURE` or `UNRESOLVED`. The record ID and stratum assignment must match the frozen diagnostic-bank manifest exactly.

The schema must not contain `a(v)`, M1-si `OC-A`–`OC-D` classes, or a new operator-class coordinate. It must not require M1-si's within-parent pair condition or its extra distinct-digest construction condition. Source and runnable-artifact digests are retained for traceability and collision checks, not as substitutes for B1's q identity or as new cell coordinates.

### 3.3 Completeness and identity rules

1. The frozen parent roster and expected variant inventory are the census denominators. Every expected parent and variant must be represented, including those with no eligible diagnostic result.
2. A `VALID` variant must have exactly one complete result for every one of the 64 frozen diagnostic records, with exactly eight records assigned to each D1–D8 stratum.
3. `EXCLUDED_BEFORE_DIAGNOSTICS` means a design exclusion whose criterion, affected unit and decision were recorded before any diagnostic execution began in the frozen inventory. Its diagnostic result array must be empty.
4. `INVALID` means failure of a predeclared, objective pre-diagnostic eligibility or integrity rule. The rule, its version/hash, evidence and decision timestamp must be retained; the decision must precede the first diagnostic execution anywhere in the frozen inventory. Its diagnostic result array must be empty. `INVALID` must never be assigned after examining terminal result values, `f_j`, `u_j` or any diagnostic result pattern.
5. `INCOMPLETE` means diagnostic execution for that variant started but did not yield the complete 64-record set. It is not an exclusion and cannot be used to remove the variant from the frozen inventory. It may contain the records actually received (at most 63, including zero). A retained diagnostic execution/receipt evidence reference is mandatory even when zero records were received. Its status may be assigned from execution/run-completion metadata and record-presence/identity metadata only, not from terminal result values or derived failure/unresolved counts.
6. `EXPECTED_NOT_RUN` is a distinct status for a variant present in the frozen expected inventory for which the run-start ledger shows that diagnostic execution had not started as of that ledger snapshot. It is not an exclusion and is not synonymous with a run that started and returned incomplete data. Its diagnostic result array must be empty, and record_presence_identity_metadata_consulted must be false: no diagnostic record receipt/identity metadata is consulted or expected. The status is supported only by timestamped run-ledger execution-state metadata, not by run-completion or record-receipt evidence.
7. Either `INCOMPLETE` or `EXPECTED_NOT_RUN` in the frozen inventory blocks final full-population cell eligibility, final LOPO estimability/scored-set declarations, and all three coverage fractions. A partial appendix may show observed-to-date counts, but every such count must be labelled `PROVISIONAL — INCOMPLETE INVENTORY`; no coverage numerator/denominator/fraction or final `ELIGIBLE`/`ESTIMABLE` status may be issued. This prevents missing or not-yet-run diagnostic data from silently changing the support set or denominators.
8. Missing diagnostic records within a purported `VALID` variant, duplicate record IDs, unknown strata, unrecognised result states, mismatched bank hashes, missing q assignments, missing family assignments or conflicting identity mappings are validation failures, not zero counts. They cannot be converted to `INVALID` after diagnostic outcomes are inspected.
9. `parent_id`, `variant_id`, `Z_id` and `q_id` must be stable and consistent across all referenced files. Each variant's parent and q must resolve through the frozen rosters/registers; Z must agree with the frozen family map. A parent cannot silently change family across variants.
10. The semantic validator must require unique `parent_id` values in the roster; unique `variant_id` values; exact one-to-one coverage of the frozen expected variant inventory; every variant's `parent_id` in the parent roster; every `q_id` in the frozen q registry; every `Z_id` in the frozen family map; and exact agreement between each valid variant's 64 record IDs/strata and the bank record manifest. JSON Schema alone does not enforce these cross-record and cross-file constraints.
11. Duplicate variant IDs or conflicting source/artifact identity records block a clean census until adjudicated. Identical artifact digests are flagged for explicit duplicate-variant adjudication; the validator must not automatically count or collapse them.
12. The census must retain all excluded, invalid, incomplete and expected-not-run rows and their reasons in the output. It must not treat a missing row as a pass, failure, unresolved result or an absent parent.
13. The input must be outcome-blind. Any correctness label, `Y` value, prediction score, log-loss value, model fit, or outcome-derived selection field is prohibited. The validator should reject such fields rather than ignore them.
14. All status rules, exclusion criteria and parent-roster exclusions must be frozen before diagnostic execution. The status decision record must identify its rule/version and timestamp. The manifest must carry a frozen `diagnostic_run_start_ledger` reference, its snapshot timestamp and the campaign-wide first-execution timestamp (which may be null only when no variant has started). The semantic validator must verify that the ledger has exactly one row for every expected variant, that each started row has a variant-level start timestamp, and that the campaign-wide timestamp equals the earliest variant-level start. For `INVALID` and `EXCLUDED_BEFORE_DIAGNOSTICS`, the affected variant's ledger row must show `NOT_STARTED`. If the campaign-wide first-execution timestamp is non-null, `decided_at_utc` must precede it. If it is null, every row must be `NOT_STARTED` and `decided_at_utc` must be no later than the ledger snapshot. These rules are deliberately stricter than comparing against a later variant-specific start time: all pre-diagnostic classifications are frozen before any diagnostic execution in the inventory.
15. `diagnostic_terminal_values_consulted` means reading, evaluating or using any per-record terminal result label (`DEFINITE_PASS`, `DEFINITE_FAILURE`, `UNRESOLVED`) or any equivalent value. It must be `false` for all non-`VALID` status decisions. `derived_failure_unresolved_counts_consulted` means consulting or deriving `f_j`, `u_j`, `k_fail`, `k_unresolved`, or a failure/unresolved pattern for the purpose of assigning a status; it must also be `false` for all non-`VALID` decisions.
16. `record_presence_identity_metadata_consulted` is separate from diagnostic result values. For a `POSTRUN_COMPLETENESS_AUDIT` supporting `INCOMPLETE`, it must be `true` and may cover only the number of received records, diagnostic record IDs, stratum IDs, run start/completion/abort metadata, and whether expected record identities are present. It must not inspect terminal result values or calculate failure/unresolved counts. For `EXPECTED_NOT_RUN`, it must be `false`; the status is based on the run-start ledger's execution-state metadata. For pre-diagnostic `INVALID` and `EXCLUDED_BEFORE_DIAGNOSTICS`, it must be `false`.
17. `EXPECTED_NOT_RUN` requires `decision_basis = EXPECTED_NOT_RUN_INVENTORY_AUDIT` and timestamped ledger-snapshot evidence showing the variant's state was `NOT_STARTED` as of the snapshot; `decided_at_utc` must be no later than `snapshot_as_of_utc`. A missing start record must never be relabelled `INCOMPLETE` merely to satisfy the post-run audit schema.
18. The semantic validator must reconcile each status with its exact per-variant run-ledger state: `VALID` requires `COMPLETED` plus a start timestamp; `INCOMPLETE` requires a start timestamp and a state of `STARTED`, `COMPLETED` or `ABORTED`, with `decided_at_utc` at or after that variant's start and no later than the ledger snapshot; `EXPECTED_NOT_RUN`, `INVALID` and `EXCLUDED_BEFORE_DIAGNOSTICS` require `NOT_STARTED` and no start timestamp. For EXPECTED_NOT_RUN, the decision time must also be no later than the ledger snapshot. Thus every non-VALID pre-diagnostic status is checked against a NOT_STARTED row and must predate the campaign-wide first start (or, if the campaign has not started, the ledger snapshot); EXPECTED_NOT_RUN is checked specifically against a NOT_STARTED row and the snapshot. Any mismatch is a validation failure.
19. A variant with a documented `INVALID` status under a pre-frozen, objectively applied pre-diagnostic rule is an accounted inventory disposition, not by itself a failure of census input validation. It remains visible in the inventory/exclusion ledger and is excluded from the primary sample. An unsupported, contradictory, retrospectively assigned or outcome-informed `INVALID` status is a validation failure and makes the complete census `NOT ASSESSABLE`.
20. The semantic validator must verify that `evaluation_row_basis.row_count` exactly matches the count in its frozen `source_ref`, and that the reference/version/hash identifies the evaluation-row configuration used by this B1 analysis-plan version. The current B1 v1.7 development configuration has 78 canonical evaluation rows. A later change to the evaluation target or row count requires a new frozen configuration and a revised, independently reviewed instrument before any realised diagnostic manifest exists. The row count is a design-count input only; it does not resolve or imply the confirmatory route.
21. The semantic validator must check `diagnostic_exposure_disclosure` against the retained selection-history and generation-protocol evidence. For the current LC518 D1–D8 lineage, the known historical record is that candidates were screened against a publicly exposed B1 held-out bank; do not silently change that history to `NOT_PUBLICLY_EXPOSED` or `false`. The future generation-selection field is distinct: a final census requires `USES_PUBLIC_HELDOUT_INFORMATION` or `DOES_NOT_USE_PUBLIC_HELDOUT_INFORMATION` plus the matching frozen protocol reference. `NOT_YET_SPECIFIED` is permissible only in preflight/design records and makes a final census `NOT ASSESSABLE`. Regardless of either field's value, `independence_claim_permitted` must remain `false`; a future protocol that avoids reusing the exposed bank does not erase the historical candidate-selection dependence.

## 4. Full-population B1 support counting

For each valid variant, derive `k_fail`, `k_unresolved` and the exact `C_D` representation from the complete diagnostic record results. Then group variants by the exact cell `(q, Z, k_fail, k_unresolved)`.

For every observed exact cell, report at minimum:

- the full cell key `(q, Z, k_fail, k_unresolved)`;
- number of valid variants in the cell;
- number of distinct parent IDs, `G_c`;
- number of distinct exact rational `C_D` values, `D_c`;
- the distinct `C_D` values themselves;
- the three separate B1 eligibility checks and the overall eligibility result;
- all variants and parents in the cell;
- any validation or provenance issue affecting the cell.

The frozen B1 full-population eligibility rule is applied without modification:

1. `k_fail >= 2`;
2. `G_c >= 3` distinct parents;
3. `D_c >= 2` distinct observed `C_D` values.

A cell is primary-eligible only when all three conditions hold. No pooling is allowed across q, Z, `k_fail` or `k_unresolved`. Every ineligible cell remains in the audit output with its exact failure reason(s).

The primary sample consists of all valid variants in full-population eligible cells, exactly as B1 v1.7 states. Do not add variants from non-eligible cells to rescue support. Do not impose an additional requirement that each parent contribute two variants or a within-parent pair. Such a requirement belongs to the proposed M1-si construction line and is not part of this B1 v1.7 census.

## 5. LOPO fold-level support counting

### 5.1 Fold construction

Construct exactly one leave-one-parent-out fold for each parent represented in the B1 primary sample. For held-out parent `g`:

- training variants are all primary-sample variants whose parent is not `g`;
- candidate test variants are the primary-sample variants belonging to `g`;
- B1's separate correctness outcome rows are not loaded or read by this census.

For each exact primary cell represented among parent `g`'s candidate test variants, evaluate training support using only the variants from that exact cell in the training portion.

### 5.2 Frozen training-fold estimability rule

For each fold-cell, calculate and report:

- `G_train`: distinct parent IDs represented in that exact cell in the training portion;
- `D_train`: distinct exact rational `C_D` values in that cell in the training portion;
- `W_C_train = sum_v (C_D(v) - mean_C_D_train)^2` over training variants in that exact cell;
- the exact rational value of `W_C_train`, plus an optional decimal display value;
- whether each of the three frozen conditions passes.

A fold-cell is estimable for within-cell concentration information only when all three B1 v1.7 conditions hold:

1. `G_train >= 2`;
2. `D_train >= 2`;
3. `W_C_train > 0`.

Do not remove a condition because it appears redundant in a particular dataset. Do not use model convergence, separation, fit status, prediction quality or correctness outcomes to decide support. Those belong to later B1 analysis stages and are not inputs to this census.

If a fold-cell fails any condition, it is excluded from that fold's scored set with the precise reason recorded. Do not replace the exact-cell baseline, pool cells, zero a slope, or silently add a cell. A held-out `C_D` outside the training range is flagged as extrapolation and reported; it does not remove the test variant or its records from the scored set.

### 5.3 Scored parents and test-row counts

A held-out parent is a scored parent if at least one of its primary-sample variants belongs to a fold-cell that passes all three training estimability conditions. All eligible variants for that parent in supported fold-cells are retained. Under the current B1 v1.7 development configuration, each such variant contributes N_eval_rows = 78 expected canonical-record test rows to the eventual predictive scoring rule. N_eval_rows is supplied by the frozen evaluation-row configuration, not hardcoded as a universal constant.

For census reporting, count expected test rows as N_eval_rows × number_of_scored_variants in the fold. N_eval_rows is read from the frozen evaluation_row_basis input and its referenced configuration; the current B1 v1.7 development configuration has N_eval_rows = 78. This is a design count only, not evidence that correctness outcomes were read, available or successfully scored, and it does not designate the evaluation route as confirmatory. If a later owner decision adopts a different evaluation target or row count, update and freeze the referenced row-count configuration and this instrument before any realised diagnostic manifest exists. Executable logic must not hardcode 78. Any later outcome-completeness checks belong to the separately authorised outcome-analysis stage.

Report every LOPO fold, including folds with no scoreable test variant. Report every fold-cell, including those excluded by training support. Do not silently omit a parent or fold because its support is poor.

## 6. Descriptive coverage measures

The LOPO reconciliation proposes three coverage measures but does not set numerical floors. This draft supplies denominator definitions for review. They are proposed operationalizations, not definitions compelled in full by B1 v1.7 or the reconciliation, and they are not owner-frozen thresholds or a claim that the coverage gate is complete. Each denominator choice must be accepted before the instrument is frozen.

### 6.1 Scored-parent fraction

`rho_min = |G_score| / J`

- `G_score` is the set of distinct held-out parents with at least one primary-sample variant in at least one fold-cell that passes B1 training estimability.
- `J` is the number of distinct parent IDs in the frozen selected-parent roster for this census, including roster parents that yield no valid or no primary-eligible variant. This roster-wide denominator is an explicit conservative operationalization proposed by this draft; it is not specified verbatim by B1 v1.7 or the LOPO reconciliation. The roster and its hash must therefore be fixed before diagnostic execution. Any change to the selected-parent roster before freeze changes J and rho_min; no post-manifest roster change is permitted.
- Report numerator, denominator, fraction, and a list of roster parents not in `G_score`, with reason.
- The schema requires at least one parent in `parent_roster`, so J = 0 is not a schema-valid census input. A J = 0 guard may remain in defensive implementation code only; it must not be used to accept an invalid empty roster.

### 6.2 Scored-cell fraction per fold

For held-out parent `g`:

`rho_cell(g) = C_score(g) / C_candidate(g)`

- `C_candidate(g)` is the number of distinct full-population B1-eligible exact cells containing at least one primary-sample variant for held-out parent `g`.
- `C_score(g)` is the number of those cells whose training portion satisfies all three frozen B1 estimability conditions and therefore contributes the parent's test variants to the scored set.
- Report numerator, denominator, fraction, and each excluded cell with its support failure reason.
- If `C_candidate(g) = 0`, report `NOT DEFINED` and explain that the parent has no primary-sample test cell; do not report zero.

### 6.3 Records-scored fraction per fold (variant-weighted companion)

For held-out parent `g`:

`rho_rec(g) = R_score(g) / R_candidate(g)`, where the frozen configuration supplies N_eval_rows.

- R_candidate(g) = N_eval_rows × V_candidate(g), where V_candidate(g) is the number of that parent's variants in full-population B1-eligible cells before fold-level exclusions.
- R_score(g) = N_eval_rows × V_score(g), where V_score(g) is the number of that parent's variants in fold-cells that pass all three training estimability conditions.
- N_eval_rows is the positive integer in evaluation_row_basis, backed by its frozen source reference. The current B1 v1.7 development configuration gives 78 canonical-record rows. This parameter describes expected version-by-record row counts only; it does not label the evaluation route as confirmatory. A changed evaluation target must supply its own frozen row-count value before the instrument/manifest freeze. These are expected rows, not observed correctness outcomes.
- Because every variant contributes the same 78 expected rows, `rho_rec(g)` reduces algebraically to `V_score(g) / V_candidate(g)`. It is a variant-weighted companion to `rho_cell(g)`: it weights each candidate cell by its number of variants rather than counting each cell equally. It is not an independent source of coverage evidence and must not be described as one.
- Report numerator, denominator, fraction, and variant/cell exclusions.
- If `R_candidate(g) = 0`, report `NOT DEFINED`, not zero.

### 6.4 Coverage reporting status

All three measures are descriptive only in this version. Do not set, infer, tune or back-calculate a floor from realised counts. The report must print `threshold = NOT SET` for each measure. `rho_rec` must be labelled as a variant-weighted companion to `rho_cell`, not an independent coverage dimension. The descriptive denominators above must be challenged during review before they are frozen in a later version.

## 7. Required output package

A future valid census run must produce a versioned, hash-identified output package with these sections or equivalent machine-readable tables:

1. **Run identity:** instrument, schema, validator, runtime/dependencies, input manifest, diagnostic-bank, q/family-register and evaluation_row_basis source hashes; exact N_eval_rows value; timestamp; frozen diagnostic run-start ledger reference/hash, its snapshot timestamp, first-execution timestamp (or null if no run started), and per-variant run-state reconciliation; census mode DESCRIPTIVE_ONLY; separate historical candidate-screening disclosure and actual future bank-generation selection status/protocol reference.
2. **Input integrity:** expected versus received parent/variant counts; status counts; missing/duplicate records; identity collisions; hash mismatches; all incomplete, expected-not-run, invalid and excluded items with reasons.
3. **Variant measurement table:** parent, Z, q, variant ID, any available source/artifact digests (required for `VALID` variants), validity status, `f_1..f_8`, `u_1..u_8` where results exist, derived `k_fail`, `k_unresolved`, exact `C_D` or `NO OBSERVED FAILURES` for complete valid diagnostic vectors, and relevant exclusion/incomplete state.
4. **Full-population cell table:** every exact cell, variant count, distinct-parent count `G_c`, distinct-concentration count `D_c`, each B1 eligibility condition and final cell eligibility.
5. **LOPO fold-cell table:** every held-out parent × exact cell, candidate test variants, `G_train`, `D_train`, `W_C_train`, each support condition, score/exclusion decision, exclusion reason and extrapolation flags.
6. **Parent/fold table:** every roster parent, whether it appears in the primary sample, whether it has a LOPO fold, number of candidate and scored variants, expected candidate/scored rows calculated with N_eval_rows, and reasons for no scored rows. An empty primary sample must report zero LOPO folds explicitly.
7. **Coverage table:** `rho_min`; every fold's `rho_cell` and `rho_rec`; numerators, denominators, fractions, `NOT DEFINED` reasons; explicit `threshold = NOT SET` labels; and a note that `rho_rec` is the variant-weighted companion to `rho_cell`, not an independent evidence dimension.
8. **Exposure and exclusion ledgers:** historical held-out-bank exposure and candidate-filtering disclosure with retained evidence/status; the actual future bank-generation selection choice and its frozen protocol reference (or NOT_YET_SPECIFIED for preflight only); the unconditional prohibition on an independence claim; plus complete counts and identities for every excluded or invalid parent, variant, cell, fold-cell and record, with design/provenance reason codes. No exclusion or exposure fact disappears from the output.
9. **Verdict block:** the exact default verdict language in §8 below.
10. **Integrity record:** cryptographic hashes of all inputs, executable sources, schema, tests, runtime lock/environment and outputs. No hash is represented as proof of authorship or scientific validity.

The output must be reproducible from the frozen inputs and instrument. It must not include fitted model outputs, `Delta LL`, p-values, correctness summaries, or claims about whether concentration predicts correctness.

## 8. Verdict logic and permitted wording

### 8.1 Input/instrument validity

If required inputs are missing, incomplete, contradictory, unhashable, or fail the schema/identity checks, the complete census status is:

`NOT ASSESSABLE — required input or provenance conditions are not met.`

If any expected variant is `INCOMPLETE` or `EXPECTED_NOT_RUN`, the complete census is `NOT ASSESSABLE — frozen variant inventory is incomplete or an expected run has not started`. A partial descriptive appendix may be retained, but it must be labelled `PROVISIONAL — INCOMPLETE INVENTORY`; it may show only observed-to-date counts. It must not print final full-population cell eligibility, final LOPO estimability/scored-set statuses, or any of the three coverage fractions. The appendix cannot be represented as the full census.

A preflight disclosure with `future_bank_generation_selection_status = NOT_YET_SPECIFIED` is not a completed census input: no final census may run until the generation protocol is frozen, its actual selection choice is recorded, and the referenced protocol hash is validated. Likewise, a missing or mismatched `evaluation_row_basis` source/count, or a historical exposure disclosure inconsistent with its retained evidence, makes the input `NOT ASSESSABLE`.

### 8.2 Complete, validated census with floors unset

If all expected parents and variants are represented, all statuses satisfy the frozen rules, all required diagnostic results and provenance checks pass, and the instrument passes validation, the census status is:

`COMPLETE DESCRIPTIVE CENSUS — INPUTS VALIDATED.`

Because numerical coverage floors for `rho_min`, `rho_cell` and `rho_rec` were not predeclared, the coverage-gate field must separately read:

`NO COVERAGE VERDICT — DESCRIPTIVE ONLY; THRESHOLDS NOT SET.`

The report must add:

`No overall Gate 1 PASS or FAIL is issued. No SUPPORTED or NOT SUPPORTED coverage verdict is issued. The reported counts describe support in the realised manifest only and do not establish predictive validity, power, scientific failure or hypothesis rejection.`

This valid descriptive-only state must not be labelled `NOT ASSESSABLE`. The two statuses answer different questions: input completeness/validity versus whether a thresholded coverage verdict can be made.

A complete, validated census may have an empty B1 primary sample. This includes the degenerate case in which every expected variant has a supported pre-diagnostic INVALID or EXCLUDED_BEFORE_DIAGNOSTICS disposition and all run-ledger rows are NOT_STARTED, as well as the case where valid diagnostic results exist but no exact cell meets all three full-population B1 eligibility conditions. In either case, report PRIMARY_SAMPLE_SIZE = 0, ELIGIBLE_CELL_COUNT = 0, LOPO_FOLD_COUNT = 0 and G_score = 0. For J > 0, report rho_min = 0/J = 0. Because no roster parent has a primary-sample candidate test cell, report rho_cell(g) and rho_rec(g) as NOT DEFINED for each roster parent, with C_candidate(g) = 0 and R_candidate(g) = 0; do not report them as zero. Retain every parent/variant disposition and reason. Where all variants were excluded or invalid before diagnostics, state that no diagnostic outcomes were observed for the inventory; the empty primary sample is not a diagnostic failure result, a null predictive result, or evidence against the scientific proposition. This is a complete descriptive inventory/support report, not an overall Gate 1 PASS or FAIL.

### 8.3 No retrospective thresholding

Thresholds must not be chosen after the realised diagnostic manifest exists. No threshold may be inferred from the resulting support counts. If a future owner decision sets numerical floors, that decision must be made and recorded before any realised manifest exists, and the instrument must be revised, independently reviewed, versioned and hash-frozen before the manifest is produced. A descriptive census already run under this version cannot be retrospectively converted into a thresholded PASS/FAIL census.

### 8.4 Cell and fold statuses are not overall verdicts

Only when the frozen expected inventory is complete and validated may the instrument report final `ELIGIBLE` / `INELIGIBLE` statuses for full-population cells and `ESTIMABLE` / `NOT ESTIMABLE` statuses for LOPO fold-cells. When an `INCOMPLETE` or `EXPECTED_NOT_RUN` variant exists, any observed-to-date cell/fold counts must be labelled provisional and no final local support status may be issued. Local B1 statuses must not be conflated with the overall coverage-verdict field or a scientific conclusion.

## 9. Explicit prohibitions

This instrument and its implementation must not:

- inspect, ingest, infer or derive any B1 correctness outcome or the 78-record outcome matrix;
- fit the baseline or enriched model, calculate log loss or `Delta LL`, or run a permutation/randomization procedure;
- run S1, simulation, Monte Carlo, resampling, power, MDE or operating-characteristic work;
- generate diagnostic banks, allocate mutations, acquire/select parents, construct/build/modify solvers, compile, execute solvers or collect new diagnostics;
- invent q identities, infer q from D1–D8, or substitute M1-si `OC-A`–`OC-D` / operator-class or `a(v)` coding;
- impose the M1-si within-parent pair requirement on B1 v1.7;
- pool across exact B1 cells or silently relax a support condition;
- drop incomplete or excluded units without explicit status and reason;
- select numeric coverage floors after the manifest exists;
- declare an overall Gate 1 PASS/FAIL or a `SUPPORTED` / `NOT SUPPORTED` coverage verdict while floors are unset;
- describe this outcome-free census as confirmatory or as evidence of predictive validity.

## 10. Implementation and freeze sequence

This document is a specification draft, not executable code. Before a census can run, the following sequence must be completed:

1. Claude conducts the promised read-only review of this document against B1 v1.7, the LOPO reconciliation, the measurement specification and the latest readiness record. Each objection must cite the affected section and source clause.
2. GPT adjudicates each objection. A revised draft is issued if needed. The document remains unaccepted until the substantive review is closed.
3. The JSON Schema and semantic validator are completed specifically for B1 v1.7. The M1-si validator is not reused as the B1 instrument.
4. Synthetic and adversarial fixtures test schema validation; missing/duplicate records; invalid identity mappings; exact rational C_D, D_c and W_C_train calculations and sign decisions; pre-diagnostic timing against the frozen run-start ledger; post-run outcome-blind completeness audits; EXPECTED_NOT_RUN handling without run-completion or receipt evidence; mandatory diagnostic_evidence_ref for INCOMPLETE; incomplete-inventory blocking; historical versus future exposure-field semantics; future protocol-not-yet-specified blocking; evaluation-row-count parameter sourcing; the empty-primary-sample branch; full-population support; every LOPO exclusion condition; undefined denominators; and the descriptive-only verdict. Fixtures must be clearly labelled synthetic and never represented as observations.
5. An independent reviewer checks the code/specification correspondence. Runtime and dependencies are pinned. Source, schema, fixtures and tests are hash-frozen before any realised diagnostic manifest exists.
6. The required parent, q and family mappings, inventory and resource ceilings are settled under their separate authorities. The diagnostic bank protocol is separately frozen and receives its own generation GO. Solver construction/build and diagnostic execution receive separate GOs.
7. Only after authorised upstream work produces a complete, provenance-linked manifest may the already conditionally authorised census be run. No further census-specific owner GO is required once all prerequisites are met.

No step in this list is evidence that the prerequisites currently exist. This draft does not claim an implementation, validator, test suite, runtime lock, manifest, diagnostic bank, solver, or census output has been produced.

## 11. Open review questions for Claude

Please perform a read-only review of v0.4. The original 13-point checklist remains the settled review record; focus this pass on whether the three round-two changes and their run-ledger edge case are internally consistent. Challenge each point explicitly and cite the relevant B1 v1.7 or measurement-specification clause where applicable.

1. **Coverage denominators:** Are `J`, `C_candidate(g)` and `R_candidate(g)` faithful operational definitions for the LOPO reconciliation's `rho_min`, `rho_cell` and `rho_rec`, especially how roster parents with no primary-eligible variants are handled?
2. **78-row multiplier:** Does counting expected rows as 78 per primary-sample test variant correctly implement B1 v1.7 §3 for an outcome-blind census, without implying that the public 78-record route is confirmatory?
3. **Measurement basis:** Is the 64-record, eight-per-stratum input basis correctly kept separate from B1's 78 canonical-record outcome basis?
4. **Unresolved vector:** Does retaining all eight `u_j` values satisfy Rev 11 and the measurement register without introducing unresolved outcomes into `C_D`?
5. **Zero-failure convention:** Does reporting `NO OBSERVED FAILURES` without using a numeric zero in B1 primary support calculations correctly preserve the convention documented in B1 v1.7 §3.2 / Rev 1.4 §7.2 and Rev 11 §4?
6. **Exact arithmetic:** Is reduced-rational comparison for `C_D`, `D_c` and `W_C_train` sufficiently faithful to the frozen B1 rules?
7. **Incomplete variants:** Does the rule that either `INCOMPLETE` or `EXPECTED_NOT_RUN` blocks final cell/fold statuses and all three coverage fractions correctly prevent an incomplete manifest from looking complete?
8. **Prediagnostic exclusion and invalidity:** Are the required frozen criteria, dated decision evidence and outcome-blind status assignment sufficient to prevent post-diagnostic selection on the failure vector?
9. **Exposure disclosure:** Does the mandatory public-held-out-bank screening disclosure adequately preserve the selection-history limitation without implying statistical independence?
10. **Schema/semantic-validator boundary:** Are the conditional result cardinalities sound, and are the listed semantic checks sufficient for uniqueness, registry membership, parent/variant cross-file consistency and exact diagnostic-record matching?
11. **q scope:** Does the draft correctly use only the B1 v1.7 q coordinate without silently importing M1-si's q/a proposal or presuming that a concrete q inventory already exists?
12. **Verdict:** Are `NOT ASSESSABLE` for incomplete/invalid inputs and `NO COVERAGE VERDICT — DESCRIPTIVE ONLY; THRESHOLDS NOT SET` for a complete valid census correctly separated?
13. **Any omitted B1 v1.7 reporting or support rule:** Identify exact clause(s) and propose the narrowest correction.

## 12. Claude review round 1: GPT adjudication

| Claude objection | Adjudication | Revision in v0.2 (historical) |
|---|---|---|
| 1. `NOT ASSESSABLE` conflated invalid inputs with valid descriptive-only reporting. | **ACCEPTED.** | Separate complete-input status from coverage verdict; §8.2 uses `NO COVERAGE VERDICT — DESCRIPTIVE ONLY; THRESHOLDS NOT SET`. |
| 2. `INCOMPLETE` could silently alter denominators while fractions were still reported. | **ACCEPTED; conservative rule selected.** | Any `INCOMPLETE` variant blocks final cell/fold statuses and all three coverage fractions. Partial counts are provisional only; §§3.3, 8.1 and 8.4. |
| 3. Prediagnostic exclusions and invalidity need frozen criteria and outcome-blind timing. | **ACCEPTED.** | Require pre-frozen status rules, dated evidence and a no-diagnostic-outcomes-consulted assertion; `INVALID` and `EXCLUDED_BEFORE_DIAGNOSTICS` must be assigned before diagnostics; §3.3. |
| 4. Public held-out-bank exposure/filtering disclosure missing. | **ACCEPTED.** | Mandatory disclosure in manifest, run identity and output; record screening-history completeness and prohibit an independence inference from non-overlap; §§2.2, 3.1 and 7. |
| 5. Zero-failure convention citation should cite both sources. | **ACCEPTED.** | Cite B1 v1.7 §3.2 (citing Rev 1.4 §7.2) and C_D Measurement Specification Rev 11 §4; §2.3. |
| 6. `rho_rec` adds little and must not read as independent. | **ACCEPTED.** | Label as variant-weighted companion to `rho_cell`, not independent evidence; §6.3–6.4 and output table. |
| 7. JSON Schema cannot enforce uniqueness, registry membership or cross-file consistency; non-valid statuses need semantic checks. | **ACCEPTED.** | Schema v0.2 tightens status/result cardinalities and makes status decisions explicit; §3.3 enumerates mandatory semantic-validator checks. |


## 13. Claude review round 2: GPT adjudication

| Claude objection | Adjudication | Revision in v0.3 |
|---|---|---|
| 1. Prediagnostic timing rule had no timestamp/ledger field to compare with. | **ACCEPTED.** | The manifest now requires a frozen `diagnostic_run_start_ledger` with a campaign-wide first-execution timestamp (nullable only when no variant has started) and a per-variant execution-state row. The validator checks that `INVALID` and `EXCLUDED_BEFORE_DIAGNOSTICS` decisions predate the first execution and that the affected variant is recorded `NOT_STARTED`. The first-start field is null only when all ledger rows are `NOT_STARTED`; in that case the timestamp is checked against the ledger snapshot; §§3.1 and 3.3. |
| 2. `diagnostic_outcomes_consulted` did not distinguish terminal values from permitted receipt/identity metadata. | **ACCEPTED.** | Replaced it with separate assertions for `diagnostic_terminal_values_consulted` and `derived_failure_unresolved_counts_consulted` (both false), plus `record_presence_identity_metadata_consulted`. The post-run audit may count records and check IDs/strata/run metadata only; §§3.2–3.3. |
| 3. An expected variant that never ran had no valid `INCOMPLETE` evidence path. | **ACCEPTED.** | Added `EXPECTED_NOT_RUN`, supported by a timestamped run-ledger snapshot and not by a run-completion audit. It remains in the frozen inventory and blocks final cell/fold statuses and all coverage fractions; §§3.2–3.3 and 8.1. |

The three changes are narrow corrections to status evidence and completeness reporting. The round-one decisions and the 13-point substantive review checklist remain unchanged. The first census remains descriptive-only; no thresholds, route, operating ceilings or production GOs are decided here.

This adjudication is a design revision only. It does not approve or freeze the instrument, create a validator, authorise upstream production, or run the census.

---

**End state of this draft:** a proposed B1 v1.7-specific outcome-blind census specification, revised after Claude review rounds 1 and 2, not a frozen instrument and not an execution authorisation. The first census remains descriptive-only. A complete validated census uses `NO COVERAGE VERDICT — DESCRIPTIVE ONLY; THRESHOLDS NOT SET`; `NOT ASSESSABLE` is reserved for incomplete or expected-not-run inventory, invalid census inputs, or contradictory instrument/provenance conditions. A properly evidenced variant-level `INVALID` disposition is retained as an accounted inventory status and does not, by itself, make the census inputs invalid.

## 14. Claude round 3 and Opus review: GPT adjudication

This section records adjudication of the next review round. It does not imply owner acceptance or freeze.

### 14.1 Claude consistency points

| Claude point | Adjudication | Treatment in v0.4 |
|---|---|---|
| 1. Ledger timing must be checked against each variant's run-ledger state. | **ALREADY SATISFIED; CLARITY ACCEPTED.** | §§3.3.14, 3.3.17 and 3.3.18 already require one ledger row per expected variant, prediagnostic decisions before campaign start (or before the snapshot if no run has started), EXPECTED_NOT_RUN = NOT_STARTED, and exact status-to-ledger reconciliation. §3.3.18 restates the timing consequence directly. |
| 2. EXPECTED_NOT_RUN must set record_presence_identity_metadata_consulted to false. | **ALREADY SATISFIED; CLARITY ACCEPTED.** | §3.3.16 and the schema conditional already require false. §3.3.6 and the schema description explain that no diagnostic receipt/identity audit is consulted for a never-run variant. |
| 3. EXPECTED_NOT_RUN must block final statuses and coverage fractions. | **ALREADY SATISFIED.** | Both INCOMPLETE and EXPECTED_NOT_RUN are explicitly blocked by §§3.3.7 and 8.1. |
| 4. Review attribution must not imply that Claude posted under his own GitHub identity. | **ACCEPTED.** | The PR Conversation records Claude's review as supplied in the conversation and transcribed by GPT. The GitHub comment author remains the connected repository account; it is not represented as a Claude-authored GitHub event. |

### 14.2 Opus findings

| Opus finding | Adjudication | Treatment in v0.4 |
|---|---|---|
| 1. W_C_train exactness was weakened by 'where practical'. | **ACCEPTED; BLOCKING BEFORE FREEZE.** | §2.3 requires exact arithmetic for every gate/decision quantity. §5.2 requires exact rational W_C_train and exact sign evaluation; floating-point fallback is prohibited. |
| 2. Historical exposure was conflated with future bank-generation selection. | **ACCEPTED; BLOCKING BEFORE FREEZE.** | §§2.2, 3.1 and 7 separate known historical D1–D8 candidate-selection lineage from the future generation protocol selection choice. The future choice is not presupposed. The independence inference prohibition remains unconditional. |
| 3. Complete-input / empty-primary-sample branch was unspecified. | **ACCEPTED.** | §8.2 specifies the zero-primary-sample, zero-fold report; rho_min = 0/J for J > 0; and NOT DEFINED for per-parent rho_cell and rho_rec where no candidate cells exist. It states that this is not a scientific null result. |
| 4. INCOMPLETE did not require retained diagnostic evidence. | **ACCEPTED.** | §§3.2–3.3 and the schema require diagnostic_evidence_ref for INCOMPLETE, including retained run/receipt evidence when zero records were received. |
| 5. Roster-wide J denominator needed to be labelled as an operationalization. | **ACCEPTED.** | §6.1 identifies the roster-wide denominator as this draft's proposed conservative operationalization, not a quantity directly specified by B1 v1.7 or the LOPO reconciliation. Roster changes alter J and rho_min and are prohibited after manifest creation. |
| 6. The 78-row multiplier should be parameterized. | **ACCEPTED.** | §§3.1, 5.3, 6.3 and 7 use N_eval_rows supplied by a frozen, referenced evaluation-row configuration. The current B1 v1.7 development value is 78; this does not designate a confirmatory route. Executable logic must not hardcode 78. |
| 7. J = 0 is unreachable under the schema. | **NO SUBSTANTIVE CHANGE REQUIRED.** | parent_roster has minItems: 1, so a schema-valid manifest has J ≥ 1. The J = 0 guard is defensive only and cannot be used to accept an invalid empty roster. |

### 14.3 Freeze and authority boundary

The two previously blocking matters (exact W_C_train arithmetic and exposure-scope separation) are corrected in this draft, but this does not establish that the whole instrument is ready to freeze. The remaining review and owner-acceptance steps still apply. The 13-point checklist remains the settled baseline. The census remains descriptive-only; no coverage thresholds, evaluation route, operating ceilings or production GOs are selected here.