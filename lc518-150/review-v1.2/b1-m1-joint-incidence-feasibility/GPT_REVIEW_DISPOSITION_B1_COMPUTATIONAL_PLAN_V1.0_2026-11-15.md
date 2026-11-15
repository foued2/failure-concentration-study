# GPT Review Disposition: B1 Computational Implementation Plan v1.0

**Date:** 2026-11-15  
**Disposition:** Claude's availability review is accepted. The v1.0 availability section requires no revision on the findings reviewed here. This record is an independent review disposition, not acceptance of v1.0 and not an execution authorization.

## 1. Artifacts checked

The following files were fetched from their recorded commits:

| Artifact | Commit | Blob SHA-1 |
|---|---|---|
| B1 computational implementation plan v1.0 | `3d9006d213c047b21d868d51ddf2f457fbf14b5a` | `8b61952d70a3a4a60cd677e507b78dfae4f568ad` |
| B1 analysis plan v1.7 | `c3abe107acd2a3f8be58bf933eafcd734823a129` | `8c666e501a31726c728447d155045c0b20adc178` |
| v1.7 acceptance record | `ac06c6676982eed795db9cb04c6d91803b591ac7` | `ea51d72f4f85c5d832d72add561b4c93472c364a` |

The fetched v1.0 blob matches its recorded identity. The v1.7 plan and acceptance record remain separate frozen artifacts and were not modified.

## 2. Availability mathematics

The v1.0 definitions are consistent with the v1.7 Monte Carlo comparison set.

Let (q) be the fraction of assignments in the admissible space whose complete required fitting pipeline is unavailable. It is an assignment-level fraction, not a per-fit or per-fold failure probability.

Conditional on the observed assignment being fit-available, the probability that all 9,999 accepted independent uniform draws with replacement are fit-available is:

[
(1-q)^{9999}.
]

The computed illustrations are:

| Assignment-level unavailable fraction (q) | Conditional probability all 9,999 sampled members fit |
|---:|---:|
| (10^{-5}) | 90.4846% |
| (10^{-4}) | 36.7898% |
| (10^{-3}) | 0.0045219% |

For a chosen conditional sampled-set availability target (a), the corresponding sensitivity value is:

[
q_a=1-a^{1/9999}.
]

This gives (q_{0.90}=1.05370498	imes10^{-5}) and (q_{0.95}=5.12982927	imes10^{-6}). If the observed assignment is also treated as a random draw under the conditional null, the exponent is 10,000, giving (1.05359961	imes10^{-5}) and (5.12931628	imes10^{-6}), respectively.

These calculations are correct. They are sensitivity illustrations only. They are not project estimates, priors, forecasts, minimum acceptable availability probabilities, or new acceptance thresholds. No independence assumption is made about folds within an assignment.

The exact-enumeration rule is different and deterministic: every assignment in the full admissible space must fit, equivalently (q=0). One unavailable admissible assignment makes the exact test unavailable. The fit-available subset must not replace the frozen admissible reference space.

## 3. Three headline blockers accepted

Claude correctly identifies three central blockers:

1. **Statistical ratification of the proposed trigger-(i) interpretation.** A valid exact-rational certificate that the enriched ordinary logistic model has no finite MLE is proposed to count as trigger (i), leading to the joint Firth refit of both models. This is not yet ratified. It is a statistical interpretation of v1.7 §4 item 3, not merely a software implementation detail. Generic separation must not be relabelled trigger (ii): a separating direction can have a zero concentration-slope component. The certificate is fit-level only and must not alter the design-only audit key, admissible assignment set, scored rows, or assignment accounting.

2. **Exact-rational separation LP implementation and synthetic validation.** A deterministic solver and its version, resource limits, primal and Farkas certificate checks, failure modes, and LP-to-Krawczyk fallback must be specified and validated on software-only fixtures. Synthetic results cannot estimate project unavailability.

3. **Numerical implementation and validation.** The Arb and Krawczyk path, exact-rational conversion, proposal path, ordinary and Firth optimization, Armijo certification, convergence and fitted-root enclosures, Wald-SE thresholds, matrix operations, stream construction, and assignment accounting remain proposed rather than implemented and validated. The pinned software environment, fixtures, expected outputs, tolerances, and artifact hashes must be fixed before validation. No API behaviour is established merely by citing documentation.

No finding in this review authorizes installing software, running tests, benchmarking, fitting models, sampling assignments, or accessing project data.

## 4. The three blockers are not an exhaustive execution checklist

Claude's three-item summary is accurate as a high-level grouping, but it must not be read as saying that clearing only those three items is sufficient for an execution GO. The v1.0 §9 blocker table and the v1.7 acceptance record preserve additional prerequisites, including:

- Establish the exact design inventory needed to derive (N_{max}) and (p_{max}), including the design-derived dimensions required for the real-data folds and N4-a workloads. This must be done within an expressly authorized data-access scope and without unauthorized outcome inspection.
- Assess the design-only audit-key and admissible-space workload, and establish whether the (10^8) rejection-sampler check cap is feasible. If a declared cap is not met, the applicable branch is unavailable; the cap is not relaxed.
- Pin the numerical stack and LP implementation in an isolated environment, and complete the full synthetic validation suite with frozen expected outputs and recorded versions/hashes.
- Resolve the joint-consent provenance gap separately. Computational correctness does not cure a consent or provenance gap.
- Review and approve the isolation and data-access safeguards, then obtain a separate explicit execution GO.

These are distinct from accepting a computational design document. Passing software tests demonstrates implementation consistency; it does not establish scientific validity, exchangeability, consent, bank integrity, or predictive evidence.

## 5. Binding status

- **v1.0:** remains a design draft, not accepted or frozen, and not an execution GO. It explicitly remains contingent on separate ratification of the trigger-(i) interpretation.
- **v1.7:** remains accepted and frozen as a symbolic analysis plan only. Its trigger wording and acceptance record are not changed by this note.
- **Availability:** mathematics verified; the strict branch-specific all-or-nothing rule is retained.
- **Research result:** the concentration hypothesis remains empirically unresolved. No predictive result follows from these documents.
- **Project activity:** this review performs no software installation, code execution, benchmarking, model fitting, assignment sampling, solver construction, bank access, or outcome evaluation.

No v1.1 computational-plan revision is required solely to address Claude's availability review. Any future change to the computational specification must be additive and preserve v1.0 and all frozen predecessors unchanged.
