# Gate 1 support and coverage rule — proposal v2 (2026-11-23)

**Status:** PROPOSAL FOR REVIEW; NOT ADOPTED. Every global numerical coverage floor
remains **NOT SET**. Gate 1 remains **BLOCKED / NOT ASSESSABLE** while floors are
unset or census inputs are incomplete.

**Author:** GPT, corrective revision following Claude's NOT PASS and agreed repair
scope, 2026-11-23.

**Purpose:** separate the frozen per-cell support predicate, a future global Gate 1
coverage rule, and Gate 4 precision/power. They are different questions.

## T0. Census assessability prerequisites

These are closure requirements, not coverage thresholds.

| ID | Condition | Evidence / boundary |
|---|---|---|
| T0.1 | All 150 pre-registered inventory slots have a resolved status. | Frozen 30-parent × 5-role population design and schema 0.6. |
| T0.2 | Each VALID variant has exactly 64 terminal diagnostic records, eight in each D1–D8 stratum. | Schema 0.6 and frozen diagnostic-bank design. |
| T0.3 | Each non-VALID status has its schema-conformant decision and prohibited consultation flags false. | Schema 0.6 and reviewed intake checker. |
| T0.4 | The run-start ledger reconciles one-to-one with all inventory slots; campaign first-start timestamp agrees with the ledger. | Schema 0.6 ledger contract. |
| T0.5 | Every diagnostic record ID reconciles with the generated C9 diagnostic-bank record manifest, with zero unresolved mismatches. | C9 run 41591572358; artifact ID 13210063805; SHA-256 `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2`. Both input banks and oracle outputs exist. The held-out bank is publicly exposed, not sealed confirmatory data. |
| T0.6 | Zero unresolved duplicate-source or runnable-artifact digest adjudications. | Reviewed intake checker duplicate-digest rules. |
| T0.7 | Every VALID variant supplies the full eight-entry unresolved vector; no unresolved outcome is recoded as a failure. | Rev 11 measurement protocol and measurement specification. |

Bank records are input records. They are not solver executions or diagnostic outcome
records. The generated bank artifact does not establish that any parent body exists.

## T1. Measurement basis

The diagnostic bank has 64 records, eight per stratum. Rev 11 defines the record-level
measurement unit; the capacity addendum also reports a canonical-count sensitivity
envelope because D6 includes paired orderings of the same mathematical input.

The primary B1 analysis basis must be stated before analysis. The current measurement
specification records an unresolved alignment between record-level diagnostic C_D
measurement and canonical-record evaluation rows. Therefore:

- **Primary B1 analysis basis: NOT SET.**
- A sensitivity basis must be recomputed from its own full vectors, never averaged or
  selected from paired values.
- This proposal does not silently choose either basis.

## T2. Frozen within-cell support predicate

For a realized exact cell `(m, z, k_fail, k_unresolved)`, the existing protocol gives:

1. `k_fail >= 2`. This is mathematically necessary for two distinct C_D values at
   fixed `k_fail`, not a power or sample-size rule.
2. At least three **distinct effective parent groups** in that same cell contribute
   nonempty observed C_D sets. Parent identity is resolved by parent ID and pinned
   base-source hash; exact duplicate base-source hashes in the same family count once.
3. At least two distinct C_D values occur across different effective parent groups in
   that same exact cell.
4. No pooling across mechanisms, families, or exact cells.

This is the A3 realized-support predicate. A2 witness-derived possibility is not realized
support. An A3 support finding does not establish a predictive effect, B1 model gain,
causality, power, or full identification.

## T3. Global coverage floors

The per-cell predicate does not specify how many qualifying cells, scored parents, or
folds must be covered before an overall Gate 1 verdict may be issued. No global minimum
has been derived from the present evidence.

| Quantity | Status |
|---|---|
| Minimum number of qualifying `(m,z,k_fail,k_unresolved)` cells | **NOT SET** |
| Minimum fraction of selected parents contributing to a qualifying cell | **NOT SET** |
| Minimum per-fold / per-cell coverage floor | **NOT SET** |
| Minimum number of distinct `k_fail` values across the census | **NOT SET** |
| Minimum overall parent count for Gate 1 support | **NOT SET** |

The v1 numerical proposals (three distinct k values, four analysable cells, ten-parent
floor, twenty-parent target) are withdrawn. They were design choices, not consequences
of the frozen support predicate. The ten-/twenty-parent rationale imported power
multipliers into Gate 1 and was not a valid Gate 1 derivation.

## T4. Three-outcome verdict rule

The verdict vocabulary is **PASS / FAIL / NOT ASSESSABLE**, applied in this order:

- **NOT ASSESSABLE** if any T0 prerequisite is incomplete or inconsistent, effective
  parent identities are unresolved, a required measurement-basis decision remains open,
  or global coverage floors are **NOT SET**. A complete census with unset floors is
  reported as `COMPLETE DESCRIPTIVE CENSUS — INPUTS VALIDATED` and
  `NO COVERAGE VERDICT — DESCRIPTIVE ONLY; THRESHOLDS NOT SET`.
- **PASS** only if every T0 prerequisite is met, the global floors were frozen before
  manifest/diagnostic execution, and all required floors are met by the realized A3
  support table.
- **FAIL** only if every T0 prerequisite is met, the same pre-frozen floors are
  available, and at least one required floor is not met. This is a support limitation,
  not evidence that concentration has no predictive value.

Missing evidence is NOT ASSESSABLE, not FAIL. No floor may be invented or
back-calculated after diagnostic execution.

## T5. Gate 1 is not Gate 4

Gate 1 determines whether the prescribed diagnostic population realizes the required
within-cell variation support. It does not decide whether the study has adequate power,
precision, a minimum detectable predictive gain, or enough parents for confirmatory
inference.

Gate 4 is a separate, separately authorized design stage. It may address the parent-level
estimand, target precision, scientifically relevant gain, sidedness, power, sample size,
and operating characteristics. The capacity addendum's paired-t multipliers are Gate 4
planning material only. They do not justify Gate 1 thresholds. No power simulation or
MDE calculation is authorized by this proposal.

## T6. Adoption and authority

1. GPT reviews the support/coverage distinction and source fidelity.
2. Claude independently challenges this proposal.
3. The owner adopts a revised, dated version.
4. Only then can the relevant authorization conditions be considered complete.

This proposal authorizes no parent acquisition, mutation allocation, bank generation,
solver construction, diagnostic execution, outcome collection, census run, fitting,
simulation, or repository merge. Gate 1 remains BLOCKED / NOT ASSESSABLE.
