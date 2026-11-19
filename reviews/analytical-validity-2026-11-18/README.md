# Analytical-validity review bundle — 2026-11-18

This folder exists so that GPT and Claude can challenge the audits directly, at the source, without
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
| `REVIEWER_RESPONSE_2026-11-18.md` | Disposition ledger for two external review rounds, including the W1 reclassification and the round-3 corrections. |
| `S1_SPECIFICATION_DRAFT_2026-11-18.md` | **Design only, nothing run.** Specification for a simulation whose predictive gain is known by construction: target `Δ_pred = I(Y;C\|X)`, six worlds, one multilevel estimator, predeclared pass/fail rules, and the conditions under which S1 would fail as a test. |

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
   truth, so "the effect was built in" is an interpretation the design does not support. **This is now
   resolved in the negative: no `Δ_pred` was injected, so W1 tests no known effect.** The replacement is
   `S1_SPECIFICATION_DRAFT_2026-11-18.md`, where the gain is imposed by construction and verified by
   exact enumeration. Attack that specification instead — particularly its §10.
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
8. **Does the solver-unit problem apply to W1?** No - W1 cases are independent Bernoulli draws
   conditional on defect reach, and the reported interval is a 500-trial interval, not an
   input-level confidence interval. The design says it "does not preserve input-level dependence".
   So W1 cannot be faulted for missing a solver random effect, and it equally cannot speak to the
   clustered world. The solver-unit problem is decisive for the *real* design, where the unit is the
   parent (count open), not for W1.
9. **Is S1 vacuous?** This is the challenge that matters most to the new specification. The gain is
   imposed, so the risk is that the world tests a tautology: if `Δ_pred = 0.02` can only be reached by
   making `C` reproduce `k`, or by fixing `p(z)` so the outcome is nearly deterministic in `C`, then
   passing proves nothing. `S1_SPECIFICATION` §10 lists four such conditions and treats each as a
   *failing* outcome. A reviewer who can construct a fifth has found a real defect.
10. **Is the target the right target?** `Δ_pred = I(Y;C|X)` is the oracle predictability gain, not the
    decision value of acting on `C`. A reviewer who thinks the programme needs decision value (net of
    the cost of measuring `C`) has a different estimand, and the specification does not supply it.

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

`S1_SPECIFICATION_DRAFT_2026-11-18.md` executes nothing: no simulation, no fitting, no Monte Carlo. It
is inside the standing bounded GO ("design and mathematics only"). Running it requires a further GO
naming its scope. Until that GO exists, S1 is paper design, and that is the correct state.
