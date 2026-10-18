# VDraft source-dependency record: M3 Rev d addendum and engine spec v1 §2

**Date:** 2026-10-18  
**Companion to:** `v03p/VDRAFT_Target_Bridge_and_Research_Decision_2026-10-18.md` (Revision 2), §2.1 and §0.1 item 1  
**Prepared under:** owner work order `v03p/VDRAFT_IMPLEMENTATION_ORDER_2026-10-18.md` (commit `906dd351e647d3d28a70ae16a01070e34fdca8a6`), item 3  
**Prepared by:** GLM  
**Status:** Documentation only. No computation performed; no protocol authorized by this record. REVIEW CONTEXT: review draft only.

## 1. The dependency

The NC1 rev-3 engine names two controlling texts that are **not checked into the repository**:

- "engine spec v1 section 2"
- "M3 addendum Rev d" (`v03p/nc1/nc1_calc.py:14`)

These texts control the exact definition of the mechanistic channel `x` and, in consequence, the exact population functional prescribing `β_min` and its mapping to `c* = (1.25/β_min)²`. The target-bridge draft (Revision 2) therefore records the numerical `β_min` mapping as **PROVISIONAL-PENDING-SOURCE** and derives nothing else from those texts.

## 2. Verbatim availability assessment (work order item 3, "otherwise" branch)

Per the work order: *"If the exact text is available in the active review conversation, preserve it verbatim in a clearly labeled source document and record its origin; otherwise state this as an unresolved document dependency and keep the numerical β mapping provisional."*

**Finding: the exact controlling text is NOT available verbatim in the active conversation.** The review-thread references to "engine spec v1 §2" and "M3 addendum Rev d" are reviewer paraphrases and summary statements (including by GLM, GPT, and Claude), not verbatim reproductions of the controlling documents. Consequently neither branch of item 3 allows treating the numerical mapping as resolved: the in-conversation material is not verbatim, and the texts are not in the repository. Accordingly:

1. Nothing in this record or in Revision 2 paraphrases missing controlling text *as if it had been retrieved*; the in-chat characterizations above are quoted as characterizations only.
2. The `β_min` numerical mapping remains PROVISIONAL-PENDING-SOURCE in every affected row of the bridge draft.
3. This dependency blocks only the numerical mapping (draft §0.1 item 1). It blocks no other element of the revision; all other procedure elements are specified from in-repo anchors.

## 3. What IS preserved verbatim (in-repo anchors, with provenance)

The engine docstring excerpt naming the definitions — quoted in full, exactly as stored, from `v03p/nc1/nc1_calc.py` lines 14–26:

```
Definitions (engine spec v1 section 2, M3 addendum Rev d, A1 rev 3):
  C levels: k=5 -> {0.2,0.4,0.6,0.8,1.0}; k=10 -> {0.2,0.3,0.4,0.5}
  integer labels g = C/delta_k: k=5 g in 1..5; k=10 g in 2..5
  X_k = t_k * sum_i n_i g_i^2 - (sum_i n_i g_i)^2 = sum_{i<j} (g_i-g_j)^2
  c = (delta_5^2 * X5/t5 + delta_10^2 * X10/t10) / s_ref^2,
      delta_5^2 = 0.04, delta_10^2 = 0.01, s_ref = 0.12703 exactly
      => s_ref^2 = 161366209/1e10 ; every c>=tau comparison is done in
      exact integer arithmetic (see pooled_R0 / ssfloor_x).
  Engine-spec anchors reproduced as checks:
      c_floor(t) = delta^2 (t-1)/t / s_ref^2   (min nonzero c at size t)
      c_ceil(t)  = R_k^2 floor(t^2/4)/t / s_ref^2
  c* exact values (M3 addendum): c* = (1.25/beta)^2, sigma_max*z_req = 1.25:
      beta .20 -> 625/16 = 39.0625; .10 -> 156.25; .05 -> 625.00
```

**Provenance of the excerpt above:**

| Field | Value |
|---|---|
| File | `v03p/nc1/nc1_calc.py`, lines 14–26 |
| Origin repo | `failure-concentration-study`, branch `review/target-bridge-vdraft` (also present at `4551cac` on `review/a1-package`) |
| Commits containing it | `906dd351e647d3d28a70ae16a01070e34fdca8a6` (and parent `113ec2c4a7acd48f08d93a4cd6313eb4c3459e25`, and `4551cacb757ca39aa31b88338f2abd0a67611cb5`) |
| File SHA-256 | `c23639b85877161ad97186a6a088655ca7c1cce524aaf0b55464f1653725859d` (NC1 rev 3) |
| Validation status of that file | NC1 rev-3 mutation battery M1/M2/M3/M1b passed; evaluation loop closed; documented in `v03p/nc1/RUN.txt` at `4551cac` |

Supporting code anchors from the same file (single-line quotations with line numbers):

- Line 96: `SCENS = ("a-hist", "a-50:50", "c-hist", "c-50:50")`
- Line 103: `SREF2_NUM = 161366209  # s_ref^2 = SREF2_NUM / 1e10  (0.12703^2, exact)`
- Line 106: `DELTA2 = {5: 0.04, 10: 0.01}`
- Line 110: `CSTAR = (39.0625, 156.25, 625.0)`

These excerpts are the only verbatim material available; they are quoted to allow reviewers to check every downstream claim in Revision 2 (§2 terms table, A1.3, A2.4) against in-repo text. They do **not** by themselves resolve the source precondition, because they are excerpts, not the full controlling definitions.

## 4. Exactly what the committed source must pin (mechanical checklist)

Resolving the dependency means committing the controlling texts into the repository so that the following four items are unambiguous. Until then the bridge draft's affected output column stays PROVISIONAL-PENDING-SOURCE.

1. **The exact mechanistic channel** relative to which `β_min` is measured, and its precise relation to the per-body within-bucket departure `(C_i − C̄_k)` used in the engine's `c` construction (dimensionless in Revision 2: `x_{M3,i} = (C_i − C̄_k)/s_ref`, consistent with the excerpt in §3).
2. **The exact marginal/population functional prescribing `β_min`**: the averaging population; whether the slope is a local derivative `γ·p(1−p)` under the declared logistic model or a finite difference of a population mean; and the evaluation point (null baseline `γ = 0` versus calibrated effect `γ = γ*`).
3. **The roles of `σ_max` and `z_req`** in `σ_max·z_req = 1.25`, and their relation to `β_min` — how the fixed factor `1.25` entering `c*` is assembled.
4. **Sign/scale conventions** linking the Revision F outcome model term `γ·C` and the M3 mechanistic channel `β_min·x_M3` — with the explicit disambiguation that `β_min`'s slope attaches to `x_M3` (the `s_ref`-normalized within-bucket departure) and never to Revision F's outcome-model predictor `x_RCS = log(1+k)` (a slope mapped to the wrong predictor would pass every otherwise-plausible sanity check) — including whether and how suite/body random effects (`u`, `v`) enter the definition.

## 5. Resolution procedure

1. The owner (or a reviewer with access) commits the two controlling texts into the repository in any reviewable format, recording their origin and (for any scanned/transcribed copies) a content hash.
2. Reviewers check the four checklist items of §4 against Revision 2 and confirm that the committed text is consistent with the in-repo engine excerpts of §3 (the engine file itself is validated and is not to be rewritten as part of this resolution).
3. If consistent: Revision 2's A2.3 may be executed as specified and affected rows lose the PROVISIONAL-PENDING-SOURCE label.
4. If inconsistent with §3: that discrepancy is itself a blocker requiring explicit owner direction; NC1 stays closed and its validated results are not reopened.

## 6. Explicit non-claims

- No statement in this record asserts that the full text of "engine spec v1 §2" or "M3 addendum Rev d" has been read from any repository file.
- No quantitative `γ ↔ β_min` or `β_min ↔ c*` conversion is asserted as authoritative here. The only numeric relations carried in Revision 2 are (a) the algebraic restatement of the engine's own `c` definition (which follows from the §3 excerpt plus arithmetic) and (b) the clearly labeled candidate mapping quarantined in A2.3, which is absent from this record precisely because it is not source-backed.
- NC1's validated status and its saturation/mutation record are unaffected by this dependency.

**Status line:** Source dependency documented; `β_min` numerical mapping remains PROVISIONAL-PENDING-SOURCE; no computation or protocol authorized by this record.
