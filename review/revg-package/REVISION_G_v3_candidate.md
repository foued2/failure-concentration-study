# Revision G v3 — CANDIDATE (documentation only; PUBLISHED on branch `review/revg-package`)

Status: Content approved by Foued for this candidate ("ALL APPROVED", chat, 2026-10-17, given in response to GPT's review of the candidate and its correction instructions). Published on branch `review/revg-package` under the owner's explicit PUBLISH instruction (2026-10-17); see the package README.txt and MANIFEST.sha256 for the commit record and hash chain. Stage 1 simulation-protocol freeze has NOT occurred. Phase 1 is NOT AUTHORIZED. RevF text is not edited.

Provenance: this text was finalized by the implementation agent from the verbatim reviewed text relayed through the review channel, because CLAUDE's original local files were not accessible on the implementation machine; byte-level equality with the pre-finalization local file is not assumed. The content is the reviewed text with only the specified M3 reference updates and publication-status metadata corrections.

## 0. References (pinned)

| Item | Reference |
|---|---|
| A1 Revision 3 package | branch `review/a1-package`, commit `f69cc9ba9cf54562df2269f066465f7957c6ccde` |
| RevF design text | `v03p/PHASE0_DESIGN_2026-10-15_RevF.md`, blob `c9ad2e1e19540e79d06a415e2eb5ab731c1a0daf`, 100679 bytes (unchanged at `f69cc9b` and `4d7517a`) |
| O2 review package (rev 2) | branch `review/o2-package`, commit `4d7517a1a30f47d3c41fb9f0ee6eed4397e8e05e`, directory `review/o2-package/` |
| M3 addendum, Rev d | branch `review/m3-addendum`, commit `c70a3870bc23fb973de4c8c7632f84ce0331bb33`, path `review/m3-addendum/M3_SPEC_ADDENDUM_DRAFT_2026-10-17.md`, blob `737c5e574a9af6eb977484011681a1e05e91d203`, file SHA-256 `462DAB4CC7E792B36E2DBD1A233CA348369660B9C8461F425388213162E2E959` (19864 bytes; provisional, not frozen; opening status metadata corrected to record the commit) |

Step 1 (A1 Revision 3 integrity) is closed as a technical integrity result only. It is not scientific validation of the concentration theory. The `.gitattributes` BOM warning remains a documented, non-blocking housekeeping issue and is left untouched.

## 1. Owner decisions (approved by Foued)

| # | Decision | Recorded wording |
|---|---|---|
| 1 | Pre-freeze computation policy | Limited to named, deterministic calculations needed for the adopted design. No wider grid, solver generation or hidden-outcome access. |
| 2 | Model direction | M3 approved as the model direction. The exact conditioning criterion and the ridge-on-dummies policy remain open. |
| 3 | Support rule | S1(4): n >= 8 and n - max_c n_c >= 4, as the selected candidate support rule. |
| 4 | Split rules | N1 = R-a (global membership). N2 = P-i (every globally included bucket represented in training). B_split = 8 as the proposed total test-block minimum. |

Consequences recorded with these decisions:

- S1(4) replaces S0 as the support rule in the design record; RevF text is not edited. S0 implies S1(4), so S1(4) is the weaker condition. It guarantees only four off-modal bodies per included bucket. At k = 20 only two C values are attainable (0.20 and 0.25). Whether S1(4) yields enough variation to detect an effect is a Phase 1 question that support probabilities do not answer.
- B_split = 8 is the currently approved proposed total test-block minimum. Its feasibility cost in scenario (c) is reported in section 3. It is revisited only if the owner explicitly reopens that decision; the published O2 package is not changed.
- O2 training rule: every globally included bucket represented in training; at least 8 in-support training bodies; at least two distinct C values in at least one included training bucket (RevF section 5B reading; the "every included bucket" reading is kept as a sensitivity result). The CVD training-variation check is applied per split. M3 matrix-conditioning and residual-information criteria are excluded from the O2 event. Failure of any condition makes the split INFEASIBLE.
- O2 test rule: at least one eligible test body per included bucket and at least 8 eligible test bodies in total.

## 2. What A1 established

All A1 figures are support-only probabilities under the specified model, with no rank/conditioning conjunct. They are not yield predictions and not full-study feasibility.

- Rule definitions: S0 is n >= 8, at least 2 distinct C values, and at least 4 bodies at each observed C extreme. S1(m) is n >= 8 and n - max_c n_c >= m (both conjuncts are part of the rule). S2(m) uses z_k strata from attainable C values, defined only for k = 5, 10, 20.
- Nesting: S0 implies S1(4). No other nesting is claimed.
- B_min = 8 is redundant under S0, S2-m4 and S2-m6 and binds under S2-m2. The redundancy table does not cover S1.
- S1(4) support probability at N_b = 450: a-hist 0.998754, b-hist 0.807087, c-hist 0.527411 (S0: 0.0635, 0.0197, 0.0078).
- Not computed in A1: the 3-bucket joint (global, train, test), R-b. Scenario (d) is a structural zero.

## 3. O2 exact calculation (provisional, pre-freeze)

Reference artifacts: `review/o2-package/` at commit `4d7517a1a30f47d3c41fb9f0ee6eed4397e8e05e`. The package bytes are not regenerated, altered or replaced by this record.

| File | Bytes | SHA-256 |
|---|---|---|
| o2_calc.py | 23233 | 2A85CDA2F59982D963198B708D1C8DCB5364D303DAF60FDD397F2ED014024EEA |
| o2_results.json | 17085 | 78AEC5D9B3577AC162E5C8EC39B414221AAA40B1FBAFFF736B6EFFD46732D237 |
| o2_report.md | 8133 | 172C3803350A0EE42CF4EE6A047D2652B3E48B5CEC11C57735210766F1E6F3EC |
| o2_review.zip | 13850 | 4BA69FBCA15F96689FEF50B27156A4690E24E57EB9F501861FDB2CF334D47BCE |

Event (2-bucket scenarios only; S1(4) support; R-a): both in-range buckets (k = 5 and k = 10) pass S1(4) globally; training block (NTR = N - (N+2)//4) has tra >= 1, trb >= 1, tra + trb >= 8; training-variation condition (CVD) in two readings; test block has tea >= 1, teb >= 1, tea + teb >= 8. Matrix rank/conditioning is excluded. Scenarios (b) and (d) are excluded.

Method: exact, deterministic, standard-library arithmetic; no sampling. "RS" is the package's own route label and does not mean rejection sampling; the calculation is exact and deterministic. The main route (the package's "RS" route) uses the identity that, for independent identically distributed bodies with a fixed-size body split, the training and test compositions are independent. The validation routes are a direct hypergeometric-split enumeration (which uses A1's multinomial and hypergeometric helper functions together with brute-force bucket tables) and A1's h-table machinery for the T0 event (before CVD).

### 3.1 Primary result: P_atleastone (at least one included training bucket with two distinct C values)

| Scenario | N=113 | N=150 | N=450 | N=600 |
|---|---|---|---|---|
| a-hist | 0.0148433 | 0.106541 | 0.992713 | 0.999462 |
| a-50:50 | 0.0271793 | 0.161121 | 0.996447 | 0.999929 |
| c-hist | 3.58278e-7 | 1.50442e-5 | 0.145462 | 0.425301 |
| c-50:50 | 4.87848e-7 | 2.02296e-5 | 0.164025 | 0.449300 |

### 3.2 Sensitivity: P_each (every included training bucket has two distinct C values)

| Scenario | N=113 | N=150 | N=450 | N=600 |
|---|---|---|---|---|
| a-hist | 0.0146473 | 0.105896 | 0.992684 | 0.999460 |
| a-50:50 | 0.0268079 | 0.160236 | 0.996446 | 0.999929 |
| c-hist | 3.37379e-7 | 1.43030e-5 | 0.144575 | 0.424524 |
| c-50:50 | 4.59263e-7 | 1.92253e-5 | 0.163060 | 0.448620 |

### 3.3 Reading the results

- Identities: P_atleastone = T0 - T_HH and P_each = T0 - T_HF - T_FH + T_HH hold in all 16 cells (no violation above 1e-15). Ordering P_each <= P_atleastone <= T0 holds in all cells.
- The 5e-6 bound applies to T0 - P_atleastone (= T_HH), whose maximum over the 16 cells is approximately 3.985e-7. It does not apply to P_atleastone - P_each, which ranges from about 1.5e-8 to about 9.653e-4. Choosing between the two readings changes results by at most about 1e-3 absolute (relative gap at most about 6%, only in the c cells at N = 113 and 150 where probabilities are below 3e-5).
- Scenario (c) at N = 113 and N = 150 is effectively infeasible under this O2 event (all values at most about 2.1e-5). This wording is not extended to scenario (a): a-scenarios give 0.0148 to 0.0272 at N = 113 and 0.107 to 0.161 at N = 150, and at least 0.9927 at N >= 450.
- At N = 450 and 600, scenario (c) O2 event probabilities are approximately 14.5% to 16.4% and 42.5% to 44.9%, respectively, depending on the CVD interpretation. These probabilities include CVD. The corresponding T0 quantity excludes CVD and represents the support, TrainRa and test event before that condition is applied.
- The 8-body test-block total is the binding condition in scenario (c): for c-hist at N = 450, A1's one-body-per-bucket event gives 0.488 and the approved O2 event gives 0.145.
- Plausibility bounds (not proofs): every reported value lies below both P(Bin(T, M) >= 8), with M the in-range mass and T the test-block size, and A1's published one-body-per-bucket value.

### 3.4 Validation record (56 records = 52 PASS + 4 VACUOUS + 0 FAIL)

- V1 at N = 32 compares all six quantities (T0, T_HF, T_FH, T_HH, P_atleastone, P_each) between the direct route and the RS route, for the real a-hist table and a harness table. Measured relative deviations are about 5e-15 to 1e-14 for all six quantities in both tables. The real a-hist event mass at N = 32 is small (T0 about 2.4e-10); the harness table carries mass about 4.7e-3 and is the more substantive comparison.
- V1 at N = 16 and N = 20 is VACUOUS: the test block (4 and 5 bodies) is smaller than 8, so the event mass is identically zero. These records are not validation evidence. N = 32 is the first informative comparison.
- V0 compares the F-arrays used in the calculation with A1's FTABLE entries. FTABLE is built from the same f_s1 function, so V0 shows function/table consistency only, not independent mathematical validation.
- V3 compares A1's h-table route with the RS route for the T0 event (before CVD) at N = 113 (a-hist and c-hist). It validates T0 only, not the CVD terms. V4 brackets T0 between A1's published cons and lib values; the bracket is valid but wide.
- Reviewer reproduction: a clean rerun of the unmodified calculation logic in CPython 3.13.13 (Linux) against the pinned A1 sources reproduced all 56 check statuses and all 16 result cells (maximum relative difference 1.45e-15). This verifies reproducibility, not independent derivation. Pinned interpreter is 3.14.0.
- The package imports A1 through a machine-specific absolute path and is not self-contained.

## 4. Random N_b

Estimand: unique normalized valid bodies. All generation attempts stay in provenance; each canonical body counts once. N_b = 113 and 450 are plug-in proxies under rho = 0.25 (duplicate-only), not guaranteed sample sizes. No attempt-budget probability is claimed until validity and deduplication are modeled.

## 5. M3 disposition (provisional; not frozen)

Status is taken from the M3 addendum, Rev d (branch `review/m3-addendum`, commit `c70a3870bc23fb973de4c8c7632f84ce0331bb33`, path `review/m3-addendum/M3_SPEC_ADDENDUM_DRAFT_2026-10-17.md`, blob `737c5e574a9af6eb977484011681a1e05e91d203`, file SHA-256 `462DAB4CC7E792B36E2DBD1A233CA348369660B9C8461F425388213162E2E959`), as provisionally accepted mathematically and NOT frozen.

- Cell-means coding with unit-normalized columns gives kappa_2 = 1 under the specified full-rank design. This diagnostic does not establish adequate information.
- c >= c* remains a candidate information criterion. Its constants and inferential rationale await owner decisions.
- A fixed reference-cell condition-number threshold is representation-dependent and must not silently redefine the O2 event.
- M3 is excluded from the O2 probability results. No complete-rule probability is calculated or claimed.
- The RevF section 5A structural impossibility of kappa <= 30 applies to the current extended matrix (rank at most 4 of 6) and is not claimed to apply to M3's design. The complete-rule probability is not established.

## 6. Open items

RevF section 11 items not addressed here: O1/O3/O4/O5 resolution, G6a-fix vs G6a-id vs G6b, estimand conditioning (N4), suite counts, DGP parameter acceptance, generation budget, and the 3-bucket joint. The M3 ridge policy and the information-criterion constants are owner decisions.

## 7. Boundaries and publication

- No edit to RevF; no change to A1 or O2 package bytes; no solver generation; no wider grid; no Phase 1 activity.
- Content approval of this text is separate from permission to publish. The approvals in section 1 authorize bounded design work only; they do not authorize Phase 1 or solver generation. The M3 reference is pinned in section 0; the owner's explicit PUBLISH instruction was given on 2026-10-17.
- Publication: document-only commit with a hash manifest on branch `review/revg-package` (2026-10-17). Step 5 hash verification is run from a clean fetch of the published commit and reported separately; any later byte-changing correction requires a fresh Step 5 run naming the new commit.
- "INCONCLUSIVE: NOT FEASIBLE AT AN AFFORDABLE N" remains an acceptable terminal outcome.
