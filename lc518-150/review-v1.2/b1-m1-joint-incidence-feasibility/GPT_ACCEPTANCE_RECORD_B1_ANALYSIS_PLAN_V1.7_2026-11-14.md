# GPT acceptance record: B1 analysis plan v1.7

**Decision date:** 2026-11-14  
**Accepted artifact:** `B1_ANALYSIS_PLAN_2026-11-14_v1.7.md`  
**Primary review branch:** `gpt/b1-m1-rev1.2-review-chain-2026-11-14`  
**Transfer branch:** `review/b1-analysis-plan-v1.6-transfer-2026-11-14`  
**Transfer repair commit:** `ac38d05f015450c7ff2c63f2f1073df47fcbbdd3`  
**Primary-branch publication commit:** `c3abe107acd2a3f8be58bf933eafcd734823a129`  
**Git blob SHA-1:** `8c666e501a31726c728447d155045c0b20adc178`  
**SHA-256:** `797BD9F72CF94FDC0EFF4A03B1544823D4042F8E530B27F4FB70CBD7F2BACA7C`  
**Dimensions:** 331 LF-delimited lines; 111,169 UTF-8 bytes; 0 CR characters; one final newline.  
**Decision:** ACCEPTED AND FROZEN AS A SYMBOLIC ANALYSIS PLAN. This is not an execution GO.

## 1. Verification and provenance

GPT fetched the committed v1.7 file from the transfer branch, reviewed the complete text, repaired the LaTeX escaping defect, and independently computed the SHA-256 from the exact UTF-8/LF text now published. The resulting SHA-256 and byte count match Claude's reported repaired-file identity exactly: `797bd9f72cf94fdc0eff4a03b1544823d4042f8e530b27f4fb70cbd7f2baca7c`, 111,169 bytes, 331 lines.

The formatting repair changed only five lines: the version header, review-chain line, v1.6→v1.7 revision-log paragraph, the corresponding revision-log table row, and §8(ii). Each doubled LaTeX escape pair in those five lines was reduced to a single backslash. No doubled-backslash sequences remain in the corrected file. The corrected file has LF line endings and a final newline.

GPT also independently recomputed the SHA-256 of the v1.6 predecessor fetched from the transfer branch. It matches the user's pre-stage hash exactly: `47F84308AB3CB7A0BE2BB3A5FD289FDDE2332EB62B8CC105A4EE840640DDE0B1`, 109,277 bytes, 325 lines, LF only, final newline. The v1.6 file remains unchanged.

The v1.7 plan and v1.6 predecessor, together with the v1.6 HOLD review record, are now present on the primary review branch. The transfer branch is retained. The status paragraph inside v1.7 is a draft-time provenance snapshot; this separate acceptance record is the authoritative later decision and supersedes the draft-time statement that acceptance was pending.

Claude supplied the five-line formatting repair. The substantive adjudication and final acceptance in this record are GPT's. No unsupported claim is made that Claude separately completed a full content review of v1.7.

## 2. Substantive adjudication

The v1.7 plan is accepted because the previously identified blockers are resolved:

1. **Selection conditioning:** the audit-equality key specifies the selection decisions that define `\Omega_{\mathrm{adm}}`, while excluding numerical diagnostics that do not determine selection. Scored and excluded fold-cells are both represented.
2. **Inferential scope:** the procedure is explicitly conditional on the observed parents, outcomes, cells, and exposure multisets. It does not claim parent-population or new-parent generalization, and it does not imply that the full parent-level uncertainty requirement has been met.
3. **Permutation semantics:** the exposure supplied to the models is permuted at version level; raw failure/unresolved vectors, parent identities, cell membership, version identities, and outcome vectors remain attached.
4. **Availability:** exact enumeration requires successful fits for every admissible assignment. Monte Carlo requires successful fits for the observed assignment and every accepted sampled assignment in its declared comparison set. Failures make the applicable test run unavailable; assignments are never silently discarded or replaced.
5. **Monte Carlo reference law:** proposals are drawn independently and uniformly from `\Omega`; audit-equal proposals are accepted, yielding independent uniform accepted draws on `\Omega_{\mathrm{adm}}`. Conditional on the symmetric fit-availability event, the comparison-set members are distributed over `\Omega_{\mathrm{adm}}^{\mathrm{fit}}`. No claim is made about unsampled assignments.
6. **N4-a calibration:** §8(ii) now uses the same branch-specific reference law as §§5.3–5.7. The N4-a exceedance bound is availability-conditional, and the no-replacement rule remains binding.
7. **Interpretation:** upper-tail and lower-tail real-data rejections are distinguished; synthetic N4-a calibration does not classify a real-data result as leakage or misspecification; N3 and N4-b rejection rates are operating characteristics, not null calibration.
8. **Fitting/reporting:** the convergence criterion, Jeffreys-penalized objective, singular-information failure rule, undefined N3 correlation handling, evaluated-assignment accounting, and separation-trigger reporting are specified.

The optional additional sentence spelling out that the observed assignment is a draw under the conditional null was not added. Its role is already explicit in §5.2's conditional uniform-reassignment null and in §§5.3–5.4, which include `b_{\mathrm{obs}}` in the comparison set and exact reference.

## 3. Binding implementation notes for any future GO

These notes do not alter the statistical procedure; they prevent implementation from contradicting the frozen plan:

- The observed evaluation `T(b_{\mathrm{obs}})` computed in §5.3 step 0 is the observed member of the comparison set. Reuse that evaluation exactly once. Do not refit or count it twice in exact enumeration or in the Monte Carlo `1+R_{\mathrm{perm}}` comparison set. This interpretation is required by §8(iii)'s evaluation-count formula.
- If the baseline fit alone fails and the enriched-model trigger in §4 item 3 does not activate the joint Firth refit, the unresolved baseline failure makes the applicable test unavailable under §5.7 V5(b). There is no silent baseline fallback.
- Before any execution GO, the separate computational plan must fix the deterministic optimisation implementation for the ordinary and Firth objectives (parameterization, initialization, update/step-acceptance rules, objective/gradient evaluation, and iteration handling), the declared linear-algebra factorization routine and tolerances, and the PRNG algorithm, independent stream allocation, seeding, and draw accounting. The design-only feasibility assessment of the rejection-sampling cap is also required before sampling.
- The frozen 78-record bank remains publicly exposed development data, not sealed confirmatory data. No new-record generalization claim is supported by this plan.

## 4. What acceptance does not authorize

Acceptance freezes the symbolic design and analysis plan only. It does **not** authorize numerical probability evaluation, permutation execution, Monte Carlo execution, model fitting, simulation, solver construction, mutation allocation, generator execution, predictive fitting, or reuse of the held-out bank. Those require a separate explicit GO after the relevant computational and isolation safeguards are reviewed.

The joint-consent provenance gap remains open. The frozen blind E3 remains untouched. The concentration hypothesis remains empirically unresolved. No scientific result is implied by acceptance of this analysis plan.

## 5. Repository disposition

- v1.6: retained unchanged as a HOLD predecessor.
- v1.7: accepted and frozen at the exact SHA-256 above.
- GPT v1.6 review record: published on the primary review branch.
- This acceptance record: authoritative acceptance event for v1.7.
- `master`: not modified by these operations.
