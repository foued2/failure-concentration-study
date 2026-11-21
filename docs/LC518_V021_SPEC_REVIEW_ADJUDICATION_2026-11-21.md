# LC518 v0.21 diagnostic-strata specification: first review adjudication

**Record ID:** LC518-V021-ODS-REVIEW-2026-11-21  
**Date:** 2026-11-21  
**Review target:** `docs/LC518_V0_21_OPERATIONAL_DIAGNOSTIC_STRATA_SPEC_2026-11-21_v0.1.md`, v0.1 review-base blob `5c9cc5c46f2075948a0564fed5851800755768ed`; current v0.3 blob `299464b2057d352416ddd6db1ee489ac09617394`  
**Adjudication:** GPT direct review of the full v0.1 source, with provisional Claude comments supplied in the conversation.  
**Status:** v0.2 review edits implemented; v0.3 corrected the zero-failure convention to match accepted Rev 1.4 §3.2. Current spec blob is `299464b2057d352416ddd6db1ee489ac09617394`. This record is not an owner acceptance or operational-specification adoption.

---

## 1. Review provenance and scope

Claude explicitly stated that it had **not read the v0.1 specification text directly** and that its six challenges were based on GPT's summary. Accordingly, those comments are treated as candidate review issues, not as a direct independent file-level review. GPT retrieved and read the complete v0.1 source directly from the repository and checked the relevant predicates and the H80 artifact bytes.

The first review did not include execution of a generator, solver, diagnostic bank, model, or experiment. The D1–D8 feasibility checks below are mathematical checks of the written predicates and illustrative examples only.

## 2. Adjudication of Claude's six challenges

### 2.1 Mutual exclusivity

**Disposition: the three alleged overlaps are refuted; explicit proof added.**

The v0.1 rules do not overlap in the combinations Claude alleged:

- D2 requires (n=1); D3 requires (2\le n\le10).
- D1 target values are all at most 1,500 because (3c_{\min}+1\le1,500); D8 requires (a\ge2,000).
- D5 requires (2\le n\le10); D6 requires (11\le n\le30).

The full proof also separates D1/D3 by (a\notin C) versus exact (a\in C); D1/D4 and D3/D4 by gcd 1 versus gcd 2; D1/D5 by (W=N_0) versus (W>N_0); D6/D7 by n ranges; and the remaining pairs by these same disjoint membership, gcd, n, and target constraints.

Therefore no priority rule is needed, and there are no post-generation reassignments to count. The validator should test all eight predicates and reject a candidate that matches zero or multiple predicates. A complete pairwise separator table was added to v0.2 §3.1.

### 2.2 H2 oracle-answer retries

**Disposition: underlying selection observation confirmed; interpretation qualified and documented.**

The SHA-256-verified artifact 13210063805 contains 26 entries in `heldout_bank.rejections.jsonl`. All have `bank=heldout`, `stratum=H2`, and `reason=H2_ORACLE_BELOW_TWO`. Candidate attempt counts are H018: 6, H019: 3, H020: 1, H021: 1, H022: 10, H023: 2, and H024: 3.

The 12 accepted H2 records have exact oracle-answer counts:

`2, 4, 3, 6, 2, 3, 4, 2, 4, 15, 17, 4`.

This is selection on the **true LC518 answer W**, not on candidate solver PASS/FAIL. It conditions accepted H2 records on (W\ge2). Historical BANK_DESIGN v1.0 §5 describes H2 as a small-amount multiple-combination challenge, so the rejection predicate operationalises that design intention. Still, H80 is a fixed finite list, not a representative sample of all small-amount inputs. Descriptive claims on its declared 80-record target remain finite-bank claims; population generalization needs a separately defined conditional sampling estimand.

The new v0.21 taxonomy does not inherit H2's filter. Its D1–D8 (W/N_0) predicates are explicit, pre-outcome diagnostic-construction conditions. Any future protected evaluation bank must separately define its target population and justify/freeze any oracle-answer-conditioned inclusion rule in the B1 amendment. This distinction was added to the H80 result record and v0.2 §6.2.

### 2.3 Record weighting and D6 pairs

**Disposition: concern accepted as a unit-of-analysis distinction; primary record weighting retained.**

D6 contains eight raw record presentations but four canonical mathematical inputs. Under the accepted B1 statistic, both orderings count as two tested records because the primary (f_6) and (C_D) are record-level quantities, and the design deliberately tests both orders. This does not make the two records independent canonical inputs and must not be described as equal weighting over unique inputs.

The v0.2 text now requires:
- explicit rationale that record weighting is the accepted primary estimand over diagnostic presentations;
- pairwise PASS/FAIL/UNRESOLVED reporting; and
- a secondary descriptive canonical-identity-weighted sensitivity (C_D^{(K)}), where each canonical key contributes its mean failure fraction across resolved orderings (0, 1/2, or 1 for D6 pair patterns).

The sensitivity is not the accepted primary statistic and cannot receive confirmatory inferential status under B1 v1.7 without a separate B1 amendment.

### 2.4 Finite-sample attainable values of C_D

**Disposition: challenge accepted; exact attainable set added.**

With eight raw records per stratum, (0\le f_j\le8), and (0\le k_{\mathrm{fail}}\le64). For fixed (k\ge1),

[
\left\lceil\frac{k}{8}\right\rceil\le M\le\min(k,8),
qquad
C_D\in\left\{\frac{m}{k}:m=\left\lceil\frac{k}{8}\right\rceil,\ldots,\min(k,8)\right\}.
]

Every integer maximum in that interval is attainable for every unresolved count \(\ell\) satisfying \(k+\ell\le64\); the exact-maximum construction is already proved in accepted Rev 1.4 §3.2. For \(k=57,\ldots,64\), \(M=8\) is forced. At \(k=0\), \(C_D\) is undefined under Rev 1.4 §3.2; report NO OBSERVED FAILURES with no numeric index.

The exact range table is now in v0.3 §1.3. Reports must condition interpretation on \(k_{\mathrm{fail}}\); a discrete or flat \(C_D\) cannot be interpreted as a solver property without these design constraints.

### 2.5 Construct validity and expected differences

**Disposition: concern accepted in part; the premise that all strata must have different failure rates is not accepted.**

The v0.1 table listed intended challenges but did not adequately state their pre-outcome construct rationale. v0.2 now lists a susceptibility hypothesis for each category: boundary handling, single-denomination base case, exact match with distractors, parity/gcd unreachability, unlimited-use recurrence, order invariance, wide-n traversal, and large-target resource stress.

These are hypotheses about potential implementation sensitivities, not claims of causal mechanisms or expected population-wide failure-rate rankings. There is no universal reason every solver population must exhibit different rates across all eight strata. Equal failure rates are empirically possible; that would limit observed concentration and its predictive value, not retroactively invalidate the deterministic input labels.

D1 is especially heterogeneous: it includes eight different target positions, one record per position. v0.2 therefore requires position-specific descriptive reporting, including (W) and (N_0), and prohibits hiding position heterogeneity inside (f_1). Construct validity and diagnostic-to-evaluation transport still require an independent crosswalk; the v0.2 table does not establish them.

### 2.6 The 64-to-60 identity arithmetic

**Disposition: verified arithmetic; not construct-validity evidence.**

The rule requires four D6 pair identities with multiplicity two and 56 other identities with multiplicity one:

(64-4=60) distinct canonical identities.

This is a correct whole-bank consistency requirement, but it does not establish construct validity, generator feasibility, or diagnostic-to-evaluation transport. The exact multiplicity check remains in v0.3 §§3.1 and 5.2.

---

## 3. Independent arithmetic checks of the non-emptiness witnesses

The illustrative examples were recomputed using exact unbounded and 0/1 combination-count dynamic programming. Results:

| Stratum | (n) | (a) | gcd | (W) | (N_0) |
|---|---:|---:|---:|---:|---:|
| D2 | 1 | 5 | 5 | 1 | 1 |
| D3 | 3 | 5 | 1 | 1 | 1 |
| D4 | 2 | 5 | 2 | 0 | 0 |
| D5 | 2 | 6 | 1 | 3 | 0 |
| D6 | 11 | 100 | 1 | 1 | 1 |
| D7 | 50 | 100 | 1 | 1 | 1 |
| D8 | 3 | 2,000 | 1 | 1 | 1 |

D1's witness (C={3,11}) gives (W=N_0) at all eight target positions; (W=1) at target 0 and (W=0) at the other seven targets. This confirms non-emptiness, while also illustrating why D1 position-specific reporting is required.

These checks prove only that the predicates have witnesses. They do not demonstrate a seeded 64-record generator can fill every slot under cross-bank collision, within-bank duplicate, range and retry guards.

## 4. Current scientific disposition

1. The summary-based Claude objections about D2/D3, D1/D8, and D5/D6 overlap are not supported by the actual rule constraints.
2. The H2 oracle-answer selection issue is real and is now explicitly separated from solver-outcome selection and from the H80 oracle-cardinality explanation.
3. D6's duplicate canonical identities create a real difference between raw-record and unique-input weighting; primary record weighting is retained, with a secondary descriptive canonical-key sensitivity added.
4. C_D feasibility has been exactly characterised for every total failure count.
5. The eight construct rationales are clearer, but the proposed categories are not yet empirically validated, and the diagnostic-to-evaluation property crosswalk remains open.
6. The specification remains draft v0.2, not accepted or frozen. No generator, manifest, diagnostic result, solver outcome, model fit, simulation, or experiment was created or run.

**Review boundary:** Claude's comments should not be described as a direct independent file-level review of v0.1. Claude should now retrieve the raw v0.3 file and challenge it directly; GLM should conduct a separate direct review. GPT will adjudicate their source-specific findings.
