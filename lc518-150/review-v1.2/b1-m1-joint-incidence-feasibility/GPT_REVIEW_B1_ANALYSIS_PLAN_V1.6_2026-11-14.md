# GPT review: B1 analysis plan v1.6

**Decision date:** 2026-11-14  
**Reviewed artifact:** `B1_ANALYSIS_PLAN_2026-11-14_v1.6.md`  
**Transfer commit:** `da3182149355a04941d5255b869fff8a5a9abbd3`  
**Repository blob SHA-1:** `0bc9d48d2981fcf8a55d29abae3e30a94efcd0d7`  
**User-reported pre-stage SHA-256:** `47F84308AB3CB7A0BE2BB3A5FD289FDDE2332EB62B8CC105A4EE840640DDE0B1` (109,277 bytes; not independently recomputed by GPT)  
**Review scope:** content review of the exact repository file fetched from the transfer branch.  
**Decision:** HOLD. v1.6 is not accepted or frozen.

## 1. Findings

The v1.6 change to §8(ii) correctly distinguishes the two conditional reference distributions:

- Exact enumeration uses the full `\Omega_{\mathrm{adm}}` reference only when every admissible assignment is fit-available.
- Monte Carlo conditions the observed-plus-sampled comparison set on the symmetric fit-availability event, yielding the comparison-set distribution over `\Omega_{\mathrm{adm}}^{\mathrm{fit}}`.
- The stated no-claim boundary for assignments outside the Monte Carlo comparison set is preserved.

The branch-specific availability rules, comparison-set definition, conditional rank-test argument, N4-a availability qualification, no-replacement rule, evaluated-assignment accounting, design-only sampling-cap assessment, and PRNG documentation are retained from v1.5 and remain consistent with the reviewed design.

## 2. Blocking precision error in §8(ii)

The Monte Carlo sentence says that the rejection-sampler **proposals** are sampled independently and uniformly from `\Omega_{\mathrm{adm}}`. That is not the algorithm defined in §5.4.

Section 5.4 draws independent proposals uniformly from `\Omega`, the full set of distinct within-cell reassignments, and accepts only proposals whose audit-equality key matches the observed key. The accepted draws, not the raw proposals, are independent uniform draws from `\Omega_{\mathrm{adm}}`.

This distinction matters because the subsequent symmetric availability condition operates on the accepted comparison set. The intended law is:

1. Proposals: independent uniform draws from `\Omega`.
2. Audit-equality filter: accept exactly when the declared key equals the observed key.
3. Accepted draws: independent uniform draws from `\Omega_{\mathrm{adm}}`.
4. Symmetric fitting-availability condition on the observed assignment and all accepted draws: conditional comparison-set law over `\Omega_{\mathrm{adm}}^{\mathrm{fit}}`.

The error does not require a new sampling method. It requires §8(ii) to describe the already specified rejection sampler accurately.

## 3. Required correction and disposition

A new v1.7 artifact was created from the fetched v1.6 repository file. It preserves v1.6 and changes only the version/provenance text, a new revision-log entry, §8(ii), the corresponding compliance-map row, and the end banner.

The corrected §8(ii) states that proposals are drawn uniformly from `\Omega`; proposals passing the audit-equality check are the accepted assignments and are uniform on `\Omega_{\mathrm{adm}}`; conditional on the symmetric availability event, the comparison-set members are distributed over `\Omega_{\mathrm{adm}}^{\mathrm{fit}}`. The correction changes no resampling, availability, inferential or execution procedure.

**v1.7 transfer commit:** `a1d3a98978956ec9defce59c135b58719d0f4e79`  
**v1.7 repository blob SHA-1:** `4b2882e4e14fe6fab898de03d97ee0383ac14386`  
**v1.7 dimensions reported by the authoring operation:** 331 LF-delimited lines; 110,383 characters. These are not a SHA-256 byte-verification statement.

A line-level comparison of the fetched v1.6 and committed v1.7 texts showed changes only to the version/provenance header, the new v1.6→v1.7 revision log, §8(ii), the corresponding compliance-map row, and the end banner. The v1.6 repository file was not modified.

## 4. Review status and authorization boundary

- v1.6: **HOLD**, preserved unchanged.
- v1.7: unreviewed draft on the transfer branch; not accepted, frozen, or promoted to the primary review branch.
- Independent Claude content review remains the next review step; GPT retains final adjudication authority.
- No fitting, numerical probability calculation, permutation, Monte Carlo execution, simulation, solver construction, mutation allocation, generator execution, or bank reuse was performed or authorized.
- `master` was not changed.

## 5. Disposition

**HOLD v1.6.** The only identified blocker in the v1.6-specific revision is the proposal-versus-accepted-draw wording in §8(ii). v1.7 corrects it. The complete v1.7 draft still requires independent content review and final GPT adjudication before acceptance, freeze, or promotion.
