# VDraft source-dependency record: M3 Rev d addendum and engine spec v1 §2

**Date:** 2026-10-18  
**Companion to:** `v03p/VDRAFT_Target_Bridge_and_Research_Decision_2026-10-18.md` (Revision 2), §2.1 and §0.1 item 1  
**Prepared under:** owner work order `v03p/VDRAFT_IMPLEMENTATION_ORDER_2026-10-18.md` (commit `906dd351e647d3d28a70ae16a01070e34fdca8a6`), item 3  
**Prepared by:** GLM  
**Status:** Documentation only. No computation performed; no protocol authorized by this record. REVIEW CONTEXT: review draft only.  
**UPDATE (2026-10-18, owner-ordered):** Both controlling texts are now preserved **byte-exact at `v03p/source/` — as found, not frozen** — per Foued's explicit authorization; full provenance in §7. The "not checked into the repository" (§1) and "NOT available verbatim" (§2) findings describe the dependency's state at work-order time and are superseded by §7 for present status; the decision trail is retained verbatim. The `β_min` numerical mapping remains PROVISIONAL-PENDING-SOURCE pending reviewer verification of the committed texts. Addendum (same date, second pass): owner dispositions of the M3 §9 open items and the bridge-computation authorization are recorded in §8, which supersedes this line's status label (PROVISIONAL-PENDING-SOURCE → PROVISIONAL (source-committed as-found, unfrozen)).

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

## 7. Provenance addendum: byte-exact preservation of the controlling texts (owner order, 2026-10-18)

**Authorization (Foued, verbatim).** *"Commit the two source files byte-exact to v03p/source/ on review/target-bridge-vdraft, as found and not frozen, with sizes, SHA-256 hashes and last-write times recorded. Do not edit them. No computation; NC1 stays closed and NC2 and Phase 1 stay held."*

**What was committed.** Two files copied byte-exact (verbatim, unedited) from their volatile temp locations into `v03p/source/`:

| Repo path | Origin path (local temp, volatile) | Size (bytes) | SHA-256 (as found; verified equal on the copy) | Last write (UTC) | Byte census |
|---|---|---|---|---|---|
| `v03p/source/ENGINE_SPEC_v1_2026-10-17.md` | `C:\Users\pakla\AppData\Local\Temp\opencode\engine\ENGINE_SPEC_v1_2026-10-17.md` | 23,411 | `9ee6f1ef5fda68a6eb195820f3774b24dc8dcae0a2e40119fb0d0a3fb910c856` | 2026-10-18T06:00:57.5742213Z | CR 0 / LF 329 / no BOM |
| `v03p/source/M3_SPEC_ADDENDUM_DRAFT_2026-10-17.md` | `C:\Users\pakla\AppData\Local\Temp\opencode\m3_cond\M3_SPEC_ADDENDUM_DRAFT_2026-10-17.md` | 19,678 | `f29a13182556b6081794e2c23046e74f61cf7286730c8b5f2e62e58ea4862816` | 2026-10-17T15:44:10.0890014Z | CR 0 / LF 315 / no BOM |

**Byte-exactness verification.** (i) `Copy-Item` verbatim copy (file-system byte level; last-write stamps unchanged after the copy); (ii) SHA-256 recomputed on each repository copy equals the as-found hash measured before the copy (GLM probe, 2026-10-18) — the engine file's hash also matches DeepSeek's earlier recorded revision (23,411 bytes, SHA-256 `9EE6F1EF…C856`) exactly, i.e. no post-record amendment; (iii) staged with per-command `core.autocrlf=false`, so git applied no line-ending normalization (the CR 0 censi above show both files are LF-only, so normalization would have been inert regardless — the override is belt-and-braces); (iv) staged blob ids equal `git -c core.autocrlf=false hash-object` of each working copy (file↔blob identity chain), verified in the preservation commit.

**Status preserved, not upgraded — "as found and not frozen."**

- *Engine spec.* Header: "Zero-generation decision engine — specification v1 (draft for review)"; a TEMP design document carrying its own 2026-10-17 amendment ledger through several review rounds. Its hash matches the previously recorded revision exactly (above), so no post-record amendment exists.
- *M3 addendum.* Header: "M3 specification addendum (draft)"; status line "TEMP / read-only draft for reviewer disposition. Not committed, not part of the O2 package, Revision F unaltered, no complete-rule probability computed"; ledger Rev b → Rev c → "Rev d, 2026-10-17 (annotation; no mathematical changes)", recording GPT's disposition of Rev c ("derivation and threshold counts check out; provisionally accepted") and a follow-up noting Rev d consistent. **No earlier recorded hash exists for this file**; the preservation records the as-found state only and asserts no unchangedness claim beyond what the file itself states.
- *Sibling artifacts noted, not copied* (temp-only; characterized in GLM's probe report of 2026-10-18): `m3_cond\m3_cond_probe.py` (12,874 bytes) and `m3_cond\m3_cond_results.json` (5,706 bytes), both last written 2026-10-17.

**Effect on dependency status (deliberately not oversold, per CLAUDE's caution).** This preservation removes only the source-hygiene blocker: two controlling texts now leave volatile temp storage, are hash-recorded on the review branch, and are unedited. It does not freeze, sign off, or validate them; the M3 addendum's own status remains reviewer-disposition-pending. Per GPT's disposition of the same date, the next step is review of the actual committed texts against the §4 checklist (and §2.1's checklist in the bridge draft); even after that review, "the precise population functional linking `γ` to `β_min` may remain to be established" — that mapping is the bridge's own A1/A2 work. The numerical `β_min` mapping therefore stays **PROVISIONAL-PENDING-SOURCE**. NC1 remains closed; NC2 and Phase 1 remain held; no computation was run to produce this preservation, and none is authorized by it.

## 8. Owner dispositions and bridge authorization (2026-10-18)

**Decision (Foued, verbatim): "CONFIRMED AND AUTHORIZED."** Recorded in the context of the 2026-10-18 review round, where the open owner items were (i) confirming the engine-spec F5 defaults as the dispositions of the M3 §9 open items and (ii) deciding whether the A2 bridge computation is authorized (CLAUDE's stated decision order). Transcription: (1) the F5 defaults are confirmed as written and recorded as the owner's dispositions below, and (2) the A2 bridge computation is authorized in the ordered sequence — calibrate `γ*` to `δ*` (A2.2 convention), compute `β_pop` on the row's supported population (A2.3 definition), map to `c* = (1.25/β_pop)²`, and report the gap from the heuristic. If the owner intended a different scope, the owner's correction governs and this transcription is wrong.

**(1) F5 defaults confirmed as written — recorded M3 §9 dispositions (items 1–4).**

- **β scale:** per reference SD — correctness-rate units per reference standard deviation of `C` (M3's committed primary scale). The §9 alternative (original-`C`-unit scaling) is declined.
- **`z_req` (§9 item 1):** a pure effect-magnitude factor (2.5 in `σ_max·z_req = 1.25`); by itself not a power guarantee; power handled by the study's calibration.
- **`σ_max` = 0.5:** worst-case bound for any correctness probability in [0, 1]; errs conservative-side; the magnitude of the conservatism is unverified.
- **Primary estimator (§9-item-4 context):** the stratified exact permutation convention of the engine-spec scale-(i) alternative is confirmed as M3's estimator convention. The study-level confirmatory-procedure choice (Revision F's held-out log-loss comparison vs the scale-(i) permutation) is the separate established blocker (§6/§8 of the bridge draft) and is **not** settled by this confirmation.
- The worked `c*` constants (39.0625 / 156.25 / 625) remain illustrative, not frozen: M3's own text marks them "not acceptable for freeze" pending its §9/freeze cycle.

**(2) Boundaries unchanged.** NC1 stays closed (no rerun). NC2 stays held. Phase 1 stays unauthorized — the bridge-computation authorization is not Phase 1 or NC2 authorization. Solver generation and hidden-outcome collection remain unauthorized. The preserved source files remain as-found and **unfrozen**: the confirmations and authorization recorded here are owner decisions about the contained open questions, not a freeze, sign-off, or edit of the document texts.

**(3) Label effect.** The `β_min`/`β_pop` mapping's label advances from PROVISIONAL-PENDING-SOURCE to **PROVISIONAL (source-committed as-found, unfrozen)** in the bridge draft; complete-rule labels and Revision F §5A statuses are untouched.

**(4) Execution state.** The bridge computation has not been run as of this record's commit; its execution report is a separate product under its own review round. The authorization interpretation ("CONFIRMED AND AUTHORIZED" → the scope above) is stated explicitly so the owner can correct it in one line if read differently.

**Status line (updated 2026-10-18, §8).** Both controlling texts preserved byte-exact at `v03p/source/` — as found, not frozen; reviewer disposition pending. Owner dispositions of the M3 §9 open items confirmed per the F5 defaults; the A2 bridge computation authorized and not yet run (§8). The `β_min`/`β_pop` numerical mapping remains **PROVISIONAL (source-committed as-found, unfrozen)**. No computation performed yet under this record at any point; NC1 closed; NC2 and Phase 1 held; no protocol authorized by this record beyond the bridge-computation authorization transcription in §8.
