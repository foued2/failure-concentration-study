# GPT review: B1 analysis plan v1.5 and required v1.6 correction

**Decision date:** 2026-11-14  
**Reviewed source:** complete v1.5 text pasted in the review-chain conversation  
**Claimed source identity:** `D8C25893B5C6FC78A68D91EFAE81957CE133E443805BA931DA1379EE91BBBB75`; 319 lines / 104,268 bytes  
**Byte-verification status:** not independently verified. The v1.5 file is not present on this repository branch or in the mounted workspace. This review is therefore a content review of the pasted text, not a byte-level review of a repository artifact.  
**Decision:** HOLD. v1.5 is not accepted or frozen by this record. No execution is authorized.

## 1. Findings

The v1.5 corrections to the v1.4 availability semantics are accepted in substance:

1. The Monte Carlo comparison set is explicitly the observed assignment plus the 9,999 accepted assignments.
2. The same complete fitting procedure and deterministic availability rule are applied to every member of that set.
3. A fitting failure in the applicable evaluation set makes the run unavailable; no assignment is silently discarded or replaced.
4. The Monte Carlo rank-test guarantee is stated conditionally on the symmetric availability event and independent uniform draws from the admissible space.
5. The Monte Carlo branch does not claim to have checked unsampled admissible assignments.
6. The exact branch requires successful fitting for every enumerated admissible assignment.
7. The reporting and GO-time RNG, sampling-cap, and availability requirements are carried into the plan.

The symmetric availability argument is accepted with the declared scope. Conditional on the event that the observed assignment and every sampled assignment are fit-available under the same deterministic rule, the comparison-set assignments remain exchangeable under the stated conditional randomization null. The resulting Monte Carlo reference is over the fit-available subset, not necessarily all of the design-admissible set.

## 2. Remaining blocker: §8(ii) does not match the revised availability semantics

The current §8(ii) says the reference distribution is uniform on the dataset's `\Omega_{\mathrm{adm}}`. That statement is incomplete for Monte Carlo. Under that branch, conditional on the symmetric availability event, the comparison-set members are distributed over the fit-available subset:

\[
\Omega_{\mathrm{adm}}^{\mathrm{fit}}
=
\{b\in\Omega_{\mathrm{adm}}:F(b)=1\},
\]

where `F(b)=1` means the complete §§3–4 fitting procedure succeeds for assignment `b`.

The exact branch and Monte Carlo branch must be described separately. Under exact enumeration, the reference is uniform on `\Omega_{\mathrm{adm}}` only when every admissible assignment is fit-available; otherwise the replication is unavailable. Under Monte Carlo, the conditional reference is over `\Omega_{\mathrm{adm}}^{\mathrm{fit}}`, conditional on the observed assignment and all sampled assignments being fit-available. The Monte Carlo branch makes no claim about unsampled assignments.

## 3. Required replacement for §8(ii)

Replace the current §8(ii) calibration-statistic paragraph with the following text. No other methodological section is reopened by this review.

> **(ii) Calibration statistic.** The calibration statistic is \(\Delta LL\) itself, computed by the frozen pipeline (§§3–5) on each generated dataset. Its finite-sample null variability is quantified by the within-dataset conditional randomization procedure of §§5.2–5.5. The reference distribution is branch-specific:
>
> - **Exact-enumeration branch.** When every assignment in that dataset's \(\Omega_{\mathrm{adm}}\) is fit-available under the complete §§3–4 procedure, the reference distribution is uniform on \(\Omega_{\mathrm{adm}}\), with every distinct admissible assignment evaluated once. If any admissible assignment has an unresolved fitting failure, that replication is unavailable under §5.7 V5(b); no partial exact reference distribution is used.
> - **Monte Carlo branch.** Draws are independent and uniform on \(\Omega_{\mathrm{adm}}\). The comparison set is the observed assignment plus the \(R_{\mathrm{perm}}\) accepted sampled assignments (§5.3 step 2). Conditional on the symmetric availability event that every member of this comparison set succeeds under the same complete fitting procedure, the comparison-set members are distributed uniformly over the fit-available subset \(\Omega_{\mathrm{adm}}^{\mathrm{fit}}=\{b\in\Omega_{\mathrm{adm}}:F(b)=1\}\), where \(F(b)=1\) denotes successful completion of the full §§3–4 procedure for assignment \(b\). The Monte Carlo branch does not claim to have enumerated, or verified the fitting availability of, assignments outside its comparison set. If the symmetric availability event fails, the replication is unavailable and no p-value is claimed (§5.7 V3, V5(b)).
>
> Each synthetic replication uses its own audit, admissible space, branch-specific reference, and availability decision. No unavailable replication is replaced; §8(vii) governs the resulting \(\lambda\)-specific and Holm-family status. The same prespecified pipeline that calibrates the real-data test is therefore audited under the synthetic null, without substituting a different calibration procedure.

## 4. Required versioning and repository handling

- The correction belongs in a **new complete v1.6 file**. The v1.0–v1.5 predecessor artifacts must remain unchanged.
- This record is a review decision and patch specification. It is **not** the complete v1.6 analysis plan and must not be cited as though it were.
- The repository currently contains the published v1.1 plan on the review branch. The v1.5 draft was delivered in chat as a local, unpublished artifact; no exact v1.5 source file was found in the repository or mounted workspace. Consequently, this record does not claim byte-preservation or hash verification for v1.5.
- Do not create a purported full v1.6 by reconstructing missing v1.5 bytes and then claiming the predecessors were preserved. A complete v1.6 can be committed only from an available full v1.5 source or from a clearly labelled reconstruction whose provenance and byte status are explicit.
- No numerical probability evaluation, fitting, permutation execution, Monte Carlo execution, simulation, solver construction, mutation allocation, generator execution, or bank reuse is authorized or performed.
- `master` is untouched. This record is confined to the review branch.

## 5. Disposition

**HOLD.** The v1.5 plan is substantially resolved, but §8(ii) must be brought into alignment with §§5.3, 5.4, 5.7 V3/V5, and §8(iv) before the complete plan can be accepted. The replacement above is the sole required methodological text correction identified in this review. A complete v1.6 must undergo independent content review and GPT adjudication before acceptance or freeze.
