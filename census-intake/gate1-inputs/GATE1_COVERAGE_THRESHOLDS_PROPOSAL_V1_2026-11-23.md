# Gate 1 coverage thresholds — proposal v1

**Status:** PROPOSAL FOR ADOPTION. Nothing here is adopted, ratified, or binding until GPT and Claude
approve it and the owner records the adoption. Until adoption, Gate 1 remains **BLOCKED / NOT
ASSESSABLE** for the reason GPT stated on 2026-11-23: the numerical thresholds were open, so even a
completed census under revision 0.6 could be descriptive only.
**Author:** GLM (independent verification role), 2026-11-23.
**Inputs:** every number below is taken from repository records, cited inline. No value is invented;
where a value is a design choice that only the adoption chain can make, it is marked DECISION.

---

## T0. Scope and the assessability precondition

Gate 1 asks whether the diagnostic data contain enough variation to make the later predictive study
possible. It can only be assessed on a census over a complete, provenance-clean inventory. The
following closure conditions are prerequisites for any Gate 1 verdict (they restate what the schema
and validator already enforce, plus the frozen records):

| ID | Condition | Source |
|---|---|---|
| T0.1 | 150/150 inventory slots carry a resolved `validity_status` (VALID, INVALID, EXCLUDED_BEFORE_DIAGNOSTICS, INCOMPLETE, EXPECTED_NOT_RUN) | `PARENT_DESIGN.md` §1 (30 parents x 5 bodies); manifest schema `variants[]` |
| T0.2 | Every VALID variant carries exactly 64 terminal diagnostic records, 8 in each stratum D1–D8 | manifest schema 0.6 VALID conditional (`0f2865e6…`) |
| T0.3 | Every non-VALID status carries a schema-conformant status decision with the correct decision basis and both consultation flags false | schema 0.6; `validate_records.py` semantic checks |
| T0.4 | Run-start ledger reconciles 1:1 with the inventory; `first_diagnostic_execution_started_at_utc` null iff all rows NOT_STARTED | schema 0.6 ledger description |
| T0.5 | Every diagnostic record ID reconciles against the frozen bank record manifest; 0 unreconciled records | `validate_records.py` §5 (external check), bank custody requirement |
| T0.6 | 0 unresolved duplicate-digest adjudications (`semantic_source_digest` / `runnable_artifact_digest` collisions) | `validate_records.py` DUPLICATE_ARTIFACT_DIGEST_REQUIRES_ADJUDICATION |
| T0.7 | Unresolved vector u supplied in full for every VALID variant (8/8 entries); 0 unresolved outcomes recoded | `CD_MEASUREMENT_SPEC_2026-11-19.md` §1 (protocol lines 107–112, 119), §3.3 prohibition |

T0.5 and the bank identity fields additionally require the frozen B1 v1.7 diagnostic bank artifact to
exist and be hash-identified; bank generation and access are not authorized as of this proposal.

## T1. Basis and counting window (fixed by frozen records, restated)

- Primary counting basis for `C_D` exposure: **record-level, N = 64, R_j = (8,8,8,8,8,8,8,8)**, as
  pinned by the manifest schema constants.
- Contrast window: the canonical envelope **2 ≤ k_fail ≤ 53** holds contrast; **2 ≤ k_fail ≤ 56** is
  the record-level upper bound (`LC518_CAPACITY_AND_POWER_ADDENDUM_2026-11-10.md` §2). At k ≥ 57
  (record-level) the maximum is forced, so such rows carry no concentration information.
- DECISION (already flagged by the measurement spec §2, still open): whether the primary analysis
  basis is record-level or canonical. This proposal does not decide it; it only requires that the
  choice be stated and the other basis reported as a labelled sensitivity.

## T2. Variation thresholds for a Gate 1 PASS (PROPOSAL — the open item)

Gate 1 PASS requires ALL of:

| ID | Threshold | Proposed value | Basis |
|---|---|---|---|
| T2.1 | Distinct `k_fail` values among VALID variants inside the contrast window | **≥ 3** | With only 1–2 distinct k values the concentration-vs-count contrast has no support to compare models on; 3 is the minimum for a non-degenerate within-parent contrast grid. DECISION. |
| T2.2 | Analysable (m, z) cells with ≥ 3 VALID parents carrying non-degenerate `C_D` variation | **≥ 4 cells** | Frozen three-parent same-cell floor (estimand review §3; protocol C7). K5 is excluded a priori (2 parents). The population model (GPT, pending) must predict where mass lands; 4 cells is the minimum grid for a grouped-parent contrast. DECISION. |
| T2.3 | Distinct `C_D` values within at least one analysable cell at a fixed k_fail | **≥ 2** | The research question is about concentration *given* count; a cell in which every parent realizes the same `C_D` carries zero within-cell variance and fails the `W > 0` estimability gate by construction (measurement spec §4). |
| T2.4 | Parent grid for the predictive comparison | **floor n ≥ 10 parents** in analysable cells; **target n ≥ 20** | Capacity addendum §3 exact multipliers: df 9 → 3.15 (+12%), df 19 → 2.95, df 29 → 2.90. Below n = 10 the paired multiplier inflates ≥ 12% and the test is close to uninformative (n = 3 → 5.36/5.74). DECISION on the exact floor. |
| T2.5 | Sidedness pinned before any MDE is reported | **required** | Capacity addendum §3 ("Sidedness must be pinned"); one-sided vs two-sided changes the multiplier by ≈ 13%. |

Gate 1 FAIL (assessable and failed): T0 complete AND (T2.1–T2.3 unmet) — i.e., the census ran clean
and the variation simply is not there (for example, the degenerate single-stratum outcome the
estimand review §3 constructs as a counterexample).

## T3. Reporting thresholds (carry-over from the measurement spec §4–§5)

- Every reported `C_D` distribution states its k = 0 convention and reports NO OBSERVED FAILURES rows
  as a separate category, never as a low numeric value.
- Every reported distribution states its exposure basis (record vs canonical) and `N = Σ_j R_j` holds.
- Canonical-basis `C_D` is recomputed from the canonical failure vector, never averaged or selected
  from paired records.

## T4. What these thresholds do NOT do

They do not authorize any execution. They do not substitute for the population model (GPT, pending,
capacity addendum §5) or for the owner-annex allocation. They do not make Gate 1 assessable today:
T0.5 cannot even be evaluated until the bank artifact exists. They become operative only through the
adoption chain: GPT review → Claude challenge window → owner ratification, with any change issued as
v2 of this proposal.

## T5. Adoption checklist

1. GPT: review values and DECISION marks; state the primary-basis choice (T1).
2. Claude: challenge window on the threshold logic and the frozen-record citations.
3. Owner: ratify v1 as-is or with amendments; record the adoption in a dated governance note.
4. Only after 1–3: the census authorization conditions ("inputs, thresholds and operating limits") are
   complete, and a completed census can carry a Gate 1 verdict instead of being descriptive only.
