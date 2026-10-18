# Owner Work Order: Implement the Target-Bridge VDraft

**Date:** 2026-10-18  
**From:** Foued, relayed by GPT  
**To:** GLM  
**Target branch:** `review/target-bridge-vdraft`  
**Base draft:** `v03p/VDRAFT_Target_Bridge_and_Research_Decision_2026-10-18.md` at commit `113ec2c4a7acd48f08d93a4cd6313eb4c3459e25`

## Instruction

Implement the VDraft using the concrete review corrections already supplied by GLM, GPT, and Claude. Do not return another request asking Foued to choose among `β = 0.05, 0.10, 0.20`. Use **`β_min` as the designated minimum-signal parameter** throughout the bridge plan and derive its value through the target-translation procedure, rather than treating the candidate grid as an owner choice.

## Required edits

1. Correct Q1/A1.1/A1.3/A2.3/A3 to respect the M3 fixed reference scale `s_ref = 0.12703`. Do not define `β_min` as a slope per one within-`k` SD of `C`. Keep within-`k` variation as an identification/population input, with the M3 bucket weighting and body-count scaling stated explicitly.
2. Preserve the distinction among `δ*`, Revision F's logit coefficient `γ`, the exact M3-defined `β_min`, and `c* = (1.25/β_min)^2`. Do not invent a conversion or call a candidate numeric value authoritative.
3. Mark the controlling M3 addendum / engine-spec definitions as a source precondition. They are reported not to be checked into the repository. Do not fabricate or paraphrase missing controlling text as though it had been retrieved. If the exact text is available in the active review conversation, preserve it verbatim in a clearly labeled source document and record its origin; otherwise state this as an unresolved document dependency and keep the numerical β mapping provisional.
4. For the target bridge, specify the population and support rule for every `Δ`, `γ`, `β_min`, and spread value. Any bucket-local proxy result must be labeled **PROVISIONAL / NOT A COMPLETE-RULE ESTIMATE**. Do not represent it as a complete-rule estimate while Revision F §5A has `P(pass)=0` as drafted.
5. Follow Revision F's stated population-oracle target and calibration convention unless a reviewer-approved change is explicitly documented: `γ*` calibrated to `Δ` with the declared tolerance of `10^-4`, fixed seed, and recorded Monte Carlo size. Distinguish population-oracle calibration from finite-sample Phase 1 procedure performance, and define the exact marginal/probability-scale functional used for `β_min` from the controlling M3 definition.
6. Add the choice of confirmatory procedure as an explicit blocker: Revision F's held-out log-loss comparison versus the separate scale-(i) stratified-permutation procedure described in the in-chat engine specification. Do not blend their estimands or operating characteristics.
7. Remove the unsupported word “selected” for M1/M2/M3; no §5A resolution has been adopted. Add the owner decision about whether power at `δ*` is gated, because Revision F gates power at `2δ*` and only reports power at `δ*`.
8. Add the scenario-scope note: NC1's existing `c` construction covers its `k=5` and `k=10` buckets; do not imply an evaluated NC1 contribution for Revision F scenario (b)'s `k=20` without a separately specified extension. Do not run new NC1 computations to fill threshold-grid gaps.
9. Incorporate the proposed pre-registered `PILOT-DECIDES` branch only as an optional owner-decision path. State explicitly that GO or passing a pilot gate does not confirm the theory and never authorizes a later phase automatically.
10. Keep the document labeled review draft only. No NC2 computation, Phase 1, solver generation, hidden-outcome collection, spending, NC1 rerun, or protocol freeze is authorized by this implementation order.

## Deliverable and close-out

Commit the revised VDraft on this review branch, without merging to `master`. Add a short change summary listing each reviewer finding addressed and any genuine remaining blocker. Do not stop to ask Foued to select a value from the old β candidate grid. If the source-defined numerical `β_min` cannot yet be derived, use `β_min` as the symbolic threshold, show exactly what source definition is still needed, and leave only that mapping marked provisional rather than stalling the entire draft revision.

**Owner instruction:** implement the draft; use `β_min`; resolve the document wording and review amendments without another round asking the owner to choose between candidate β values.
