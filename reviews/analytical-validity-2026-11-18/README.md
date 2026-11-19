# Analytical-validity review bundle — 2026-11-18

This folder exists so that GPT and the DeepSeek web-chat reviewer can challenge the audits directly, at the source, without
going through a summary. Every file here was written on 2026-11-18 and is a **record audit**: it adds
no hypothesis, authorizes nothing, and modifies no frozen document. The repository's frozen records
(v0.1, v0.2, v0.3-P, Gate 1, three-world simulation, B1 v1.7, v0.21) are unchanged.

## Contents

| File | What it does |
|---|---|
| `claude-keys-verification-2026-11-18.md` | Checks the nine numbered claims in the owner-designated Claude critique against the repository record and against the external literature. Contains the verdict table, the corrections ledger, and the DOI-verified reference list. |
| `concentration-theory-audit-2026-11-18.md` | Eight-stage chronology of the concentration hypothesis, four failure mechanisms (yield, aliasing, attainability, construction), LC518 state, and repository topology. |
| `concentration-theory-succession-audit-2026-11-18.md` | What the original claim was traded against at each step, and whether any theory replaced it. |
| `claim-ledger-verified-2026-11-18.md` | First-pass 22-claim ledger. Superseded by `-v2`; kept for the correction trail. |
| `claim-ledger-verified-2026-11-18-v2.md` | Current ledger. C-09 is recorded as **contradicted**, C-18–C-22 added. |
| `preservation-record-2026-11-18.md` | Byte-level inventory for the `VERIFICATION_LOG.md` collision. No merge implied. |
| `S1_KNOWN_GAIN_SPEC_2026-11-18.md` | Design-only S1 v0.6 draft awaiting direct DeepSeek review. Defines the S1-before-S2-S7 stop rule, per-gate replication planning after an independently authorized pilot, hash-provenance limits, and the no-unresolved inference boundary. No code or runs. |
| `NOVELTY_AND_POSITIONING_REGISTER_2026-11-19.md` | Gate 0. States the proposition once, scoped to the observed parents and the fixed 78-record development bank; records that the statistic is the Berger–Parker dominance index by name in the frozen protocol; separates the population-information ceiling against `F` from the testable incremental claim against the exact cell; verifies 14 prior works by DOI (both Almaghairbe papers separately); lists citation corrections; pre-registers a stopping rule. |
| `CD_MEASUREMENT_SPEC_2026-11-19.md` | Measurement layer. Separates what the protocol already requires (per-stratum unresolved vector), what is legal (three-category outcome sensitivity), and what is prohibited (recoding unresolved to 0/1). Records the record-vs-canonical exposure difference and the `k = 0` convention clash between instruments. |
| `LOPO_ESTIMABILITY_RECONCILIATION_2026-11-19.md` | Maps the review's fold-level request onto B1 v1.7 clause by clause: nine of ten items are already frozen, one clause is stricter than requested, one item (a minimum-coverage verdict gate) is genuinely missing. Records the review's parent-level point as **partly addressed**: 78 records per variant sharpen one parent's score but add no parent-level replication. |
| `CONFIRMATORY_BANK_CUSTODY_REQUIREMENT_2026-11-19.md` | Records that the bank is *already* declared "development data, publicly exposed, never sealed", and states the six requirements a future confirmatory claim would need, including generation after the analysis freeze. |
| `DOMINANCE_SPECIFICITY_AND_PARTITION_SENSITIVITY_2026-11-19.md` | Separates three operations easily confused in review: B1's frozen within-cell `C_D` permutation, stratum-**name** permutation (proved invariant for `C_D`; admissible relabellings inert), and input **reallocation** (changes `C_D`, preserves the exact cell, sits outside B1's frozen resampling law). Adds the alternative-summary set, a capacity-constrained per-competitor *equal-`S`* support table for the Level 2 question with two explicit support measures and exact entropy grouping, and a four-level claim ladder with the exact sentence Level 1 licenses and its upper-tail precondition. |

Repo-root companion: `FUNDAMENTAL_GOAL_ANALYTICAL_VALIDITY_2026-11-18.md` (the owner-designated goal,
with both source critiques reproduced verbatim in Appendices A and B).

## Claims this bundle asserts, and how strongly

**Verified against the record (checkable by `git show`):**

1. W1's `C` gain is +1.961×10⁻⁶ (domain), 95 % `[-1.242×10⁻⁶, +7.581×10⁻⁶]`; the alternate partition
   gives −6.247×10⁻⁷. Frozen outcome: `C` DOES NOT SURVIVE.
2. In v0.2, `C = 5/k` on 1200/1200 rows.
3. `F` beats `C` on W1/domain: +7.90×10⁻⁴ `[+6.92×10⁻⁴, +8.86×10⁻⁴]`, against a `C` gain of ~2×10⁻⁶.
   *Qualifier:* `F`-vs-`C` is domain PASS, equal FAIL, overall FAIL.
4. No variance-component decomposition exists in the local tree or the three remote tips searched.
5. No occurrence of "mechanism-disjoint" as a stated limitation exists in any searched ref.
6. Knots `{2,8,16,24}` and `{1,2,3,4,8,16,32,48}` are frozen pre-outcome; the `k ×` tertile cell is
   pre-registered.
7. Within-`k` `C` variation exists 2 ≤ `k` ≤ 24; `k = 1` and `k ≥ 25` are degenerate.
8. The LC518 bank states explicitly that its sizes are for structural coverage, **not** statistical
   power, and that "previous power figures remain invalidated".
9. The LC518 strata are input categories, not verified mechanisms; `C_D` is not a defect-localization
   measure.
10. A third-reviewer **concurrence with a NO-GO recommendation** was recorded on 2026-11-01
    (`worklog.md:262`), route-scoped to the current operator, on exactly W1 + partition fragility +
    identification failure. It is not an owner decision, and no route-closure record exists.
11. The frozen protocol names the statistic: `C_D` is "the Berger–Parker dominance index of the failure
    distribution" (`LC518_A2_AUDIT_PROTOCOL_DRAFT_2026-11-06.md:218`). It is not a new measure.
12. The per-stratum unresolved vector is **mandatory evidence**, not an optional report: "all eight
    entries supplied", and "an omitted unresolved vector is missing evidence, not an implicit all-zero"
    (protocol 107–119).
13. The held-out bank is declared by the frozen plan as "development data, publicly exposed, never
    sealed" (B1 v1.7 §1, §12). The exposure is a recorded design fact, not a discovery.
14. B1 v1.7 already freezes fold-level estimability with three explicit conditions
    (`G_c^train ≥ 2`, `D_c^train ≥ 2`, `W_{C,c}^train > 0`), exclusion reasons, and coverage tables
    (§3 items 3–4). It refuses parent-population inference explicitly (§5.7 V1).

**Inference, not finding (attackable):**

- The minimum-detectable-effect arithmetic in `claude-keys-verification` §3 uses assumed `σ_u` and
  `sd(C)`. Neither is estimated anywhere in the record. The table is illustrative; the formula is
  standard.
- The reading of `k_unresolved` exact-cell conditioning as a possible collider is a DAG argument; no
  causal diagram is recorded, so the sign is unknown.
- The statement that the differential-unresolvedness bias pushes `C_D`'s maximum toward cleaner strata
  follows from the definition but has not been quantified.

## Specific things worth challenging

If you are reviewing this bundle, these are the load-bearing points, not the prose:

1. **Is `F`-vs-`C` a fair comparison?** The repo's condition 6 mandates it; the equal-score arm fails.
   A reviewer who thinks the domain arm is the wrong target has a real argument.
2. **W1 is a wiring check, not a positive control.** The design fixes defect reach, not a `Δ_pred`
   truth, so "the effect was built in" is an interpretation the design does not support. **That question
   is now answered:** `S1_KNOWN_GAIN_SPEC_2026-11-18.md` does carry a known gain, via
   `I(Y;C_D|X) = I(Y;F|X)` under ancillary randomization, and it computes the population truth
   independently of the fit. Attack whether that identity is doing real work or is an artifact of a
   deliberately favourable generator.
3. **Is the parent or the variant the right `J`?** M1-si is within-parent, which removes the parent
   effect but leaves ≤1 df per parent and confounds `C_D` with the mutation. **Neither 30 nor 150 is
   adopted** — the record calls 30 a logistics scenario and states "30 parents × 5 variants is not
   adopted". The parent is the independent unit; the count is open.
4. **Does conditioning on `k_unresolved` help or hurt?** Control vs collider depends on an unstated DAG.
5. **Is the T1/T2 separation actually possible?** The repo says "unseparated in nature". A proposal
   that claims to separate them must say how family-difficulty is held fixed.
6. **Does the external literature change any verdict?** The DOI list in `claude-keys-verification` §13
   is the intended attack surface. Two references were deliberately omitted rather than guessed.
7. **Does domain weighting manufacture the `F` advantage?** Claude's hypothesis: `S_D` rewards cases
   whose failures sit in large families, so the domain arm favours the dominance pattern by
   construction. The design's evaluation sizes are `N = (9, 9, 23, 23, 31, 3)`, while diagnostic
   families are equal at five probes each — so the two arms differ by size weighting, not by
   dominance weighting as such. The models are already family-adjusted. **Test:** recompute `S_D`
   with equalised `N_j` from `three_world/per_trial.json` (local) and see whether the `F` margin
   shrinks. Not yet run.
8. **Does the solver-unit problem apply to W1?** No — W1 cases are independent Bernoulli draws
   conditional on defect reach, and the reported interval is a 500-trial interval, not an
   input-level confidence interval. The design says it "does not preserve input-level dependence".
   So W1 cannot be faulted for missing a solver random effect, and it equally cannot speak to the
   clustered world. The solver-unit problem is decisive for the *real* design, where the unit is the
   parent (count open), not for W1.
9. **What is the contribution — accuracy or parsimony?** `C_D` is a function of `F`, so
   `I(Y;C_D|X) ≤ I(Y;F|X)` and `I(Y;C_D|X,F) = 0` exactly. That is a ceiling against `F`, not against `X`:
   accuracy against the predeclared exact-cell baseline is testable and may well succeed. What cannot be
   claimed is information superiority over `F`. Whether a one-parameter gain is scientifically interesting
   beyond parsimony, stability, and interpretability is a separate question, and no record measures those
   three. A reviewer who can name a fourth consideration should.
10. **Which exposure basis is primary?** The protocol counts records (`N = 64`, `R_j = 8`); the capacity
    record recommends the canonical basis (`N = 60`, `R_j = 8,8,8,8,8,4,8,8`) because D6's paired records
    are dependent. Both are defensible; the primary must be stated, and the other reported as a
    recomputed statistic, not an average.
11. **Is "prespecified partition" doing the work it appears to do?** The eight strata were used to
    construct the bank, so partition and held-out outcomes share an origin. That does not by itself
    invalidate stratification — it is what stratification is. The questions that decide validity are:
    (a) were the predicates fixed before any solver outcome existed (yes, 0 evaluated); (b) were they
    tuned on outcomes (no evidence, nothing to tune on); (c) does construction create an accidental
    dependence between bank and result (open, no evidence of use); (d) is the claim limited to the
    generation scheme actually tested (now stated in the register). External confirmation still requires a
    bank generated after the analysis freeze under separate custody.

## What is not here

The 560 MB `three_world/raw/`, `per_trial.json` (31 MB), `_quarantine/` (618 MB), and `.qoder*` scratch
transcripts are not in this bundle. They remain local. The worklog records that the raw three-world
archive is local-only by design, with hashes committed; this bundle preserves that arrangement rather
than changing it.

## Status

Nothing in this folder is a scientific finding. Every "not established" in the bundle is a statement
about what the existing designs and records show, not a claim that concentration has no predictive
value. Where a claim is inference rather than record, it is labelled as such in the body, not only in
this index.


## S1 review state

reviews/analytical-validity-2026-11-18/S1_KNOWN_GAIN_SPEC_2026-11-18.md is a design-only draft, now at v0.6. DeepSeek directly reviewed v0.5 and found no mathematical/statistical defect for the narrow machinery-check use, conditional on the project actually using the estimator-selection decision. Version 0.6 explains what S2-S7 test beyond S1, prohibits running S1 if downstream work proceeds unchanged regardless, gives MCSE scale factors and pilot-based replication-planning equations, and records the unresolved review-copy hash provenance. It remains unaccepted, unfrozen, and non-executable. The \(J\) grid is a calibration dimension only; it does not select the LC518 operating parent count.


## Reviewer identity and handoff

The active independent reviewer for S1 is **DeepSeek in the web chat**. No local agent is part of this review handoff. Claude supplied additional critiques but is not the S1 reviewer. DeepSeek's direct v0.3, v0.4 and v0.5 reviews are recorded in §§10-12 of the reviewer ledger. Version 0.6 is awaiting DeepSeek's next direct review.

The first-round S1 response is recorded in \`DEEPSEEK_S1_REVIEW_RESPONSE_2026-11-18.md\`; the provisional summary-based second-round adjudication is recorded in §9 of \`REVIEWER_RESPONSE_2026-11-18.md\`, and the direct DeepSeek reviews of v0.3, v0.4 and v0.5 are in §§10-12. The current specification is \`S1_KNOWN_GAIN_SPEC_2026-11-18.md\`, version 0.6. It remains a draft, not frozen and not executable.
