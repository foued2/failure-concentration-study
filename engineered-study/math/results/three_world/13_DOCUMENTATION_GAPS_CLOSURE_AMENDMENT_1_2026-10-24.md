# Closure-document amendment 1 (W3 oracle distinction; stratum-specific contrasts status)

**Date:** 2026-10-24
**Supersedes:** one sentence and one claim in `13_DOCUMENTATION_GAPS_CLOSURE_2026-10-24.md` (preserved byte-unchanged)
**Trigger:** field-lead (GPT) audit; verified against the frozen design by GLM. No rerun, no parameter change, no scientific-result change.

## Correction 1 — W3: the oracle check was conflated with the other W3 comparisons

The closure document said:

> ...W3 is an **oracle null check** (FAIL for primary, alternate, and full-vector comparisons)

This conflates distinct tests. Per the frozen design (§"World W3", criteria, and oracle-model specification):

- The **oracle check** is the standalone comparison adding *latent defect count* to M1+fam (categorical k + anchor-family indicators + C + latent defect count). Its recorded result (`11_THREE_WORLD_SIM_RESULT.md`): domain mean ≈ −2.8e-07, 95% interval [−2e-06, 2e-06], positive fraction 0.284; equal mean ≈ −6.0e-07, 95% interval [−3e-06, 3e-06], positive fraction 0.238. **Both intervals include zero: the oracle check holds (PASS), as designed.** This is the W3 "null check" and it did not fail.
- The **primary, alternate-partition, and full-vector comparisons in W3** are ordinary effect-size/mechanism probes. Design §"W3 primary check" explicitly states the primary k+family comparison must not be required to be exactly zero (C may proxy the omitted latent count: "Any primary gain must be interpreted as indirect proxy information"). Their recorded intervals also include zero (W3 primary C gain: domain mean −1e-06, [−5e-06, 5e-06]; equal mean −1e-06, [−7e-06, 6e-06]; alternate-partition means −1.2237e-06 / −1.6349e-06, per the review record). They are therefore not "failures of the oracle check"; the review §1 table's "(oracle null check)" parenthetical was shorthand overlapping labels, and sentence in the closure document reproduced that bundling in error.

Corrected statement (replaces the quoted sentence):

> W3 is a negative-control world whose dedicated oracle check (C after latent defect count) holds as designed; the primary, alternate-partition, and full-vector W3 comparisons have intervals that include zero and are interpreted as proxy/mechanism information, not as failures of the oracle check, per the frozen design's distinction between the two tests.

The scientific conclusion is unchanged: W1 remains the governing result and remains FAILED; W3's mechanism behaved as constructed.

## Correction 2 — stratum-specific contrasts: status stated plainly

The closure document implied every frozen reporting requirement was closed. Audit against the frozen design shows one prescribed reporting item was **not** reported:

| Frozen requirement | Status |
|---|---|
| Pooled per-(world, k, C) eligible-case counts | **Reported** — `12_overlap_by_k_c.md` (74 W1 pairs; 1 W2 pair; 73 W3; 72–74 mixtures) |
| Stratum-specific contrasts as descriptive overlap checks (design §"Descriptive reporting": "Report stratum-specific contrasts as descriptive overlap checks") | **NOT reported** — no fixed-k-descriptive contrast table appears in the original report, the review record, or the appendix |
| Counts of usable fixed-k, different-C comparisons *within carrier family* (design §"Reporting requirements" item 4) | **NOT reported** — the appendix pools eligible cases across carrier families; no per-carrier-family usable-comparison table exists in the records |

Both omissions are correctable offline from the saved local-only records without any simulation (each record carries F, E, k, carrier). They are recorded here as the **outstanding reporting item** of the three-world phase; the phrase "every frozen reporting requirement is closed" is withdrawn. Producing those descriptive tables requires field-lead authorization and remains optional to the failed W1 determination, which rests on the primary, alternate-partition, represented-k, and oracle-consistent analyses already reported and independently verified for W1.

## Invariants unchanged

The frozen design, original run record, review-corrections record, all amendments, the independent verification record, and every recorded number are unchanged by this amendment. W1 remains FAILED. No additional simulation is warranted; the scientific disposition stands as stated in `13_DOCUMENTATION_GAPS_CLOSURE_2026-10-24.md`.
