# Gate 1 report

**Study:** Work Order v2, H1a engineered task-specific failure-concentration study
**Task:** `paren7_min_insertions`
**Date:** 2026-10-23
**Decision:** **CLOSED — CONSTRUCTION AUDIT FAILED (NO IDENTIFIABLE OPERATIONALIZATION)**
**Gate 2 authorized:** no
**Study solvers generated:** 0
**Model/API calls:** 0
**Primary finding:** the target design does not identify `C` separately from
carrier family or defect identity. The power shortfall is secondary.
**Bounded audit finding:** no genuinely different mechanism pair with matched
`k=5` profiles was demonstrated; see `08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`.
**Reconstruction finding:** the rebuilt power simulation is not behaviorally
equivalent to the lost original; the equivalence question is unresolved.

## 1. Purpose

Gate 1 asks whether the selected task and target design can support the H1a
question before spending the 150-slot generation budget:

> At fixed diagnostic failure count `k`, is higher diagnostic failure
> concentration `C` associated with higher held-out boundary score `S`, after
> accounting for `k` and generator identity?

This Gate 1 is a design and identification audit. It is not a test of H1a and
does not use generated solvers.

## 2. What was built

- One task: minimum parenthesis insertions on length-7 strings over `(` and `)`.
- One exhaustive 128-input declared domain.
- One 30-input diagnostic bank and one disjoint 98-input evaluation bank.
- Six structural families with exact composition and evaluation coverage.
- A complete enumeration of all 46,656 feasible diagnostic profiles and 81
  attainable `(k, C)` cells.
- Seven selected targets totaling 150 slots.
- Eight hand-built calibration controls.
- An offline power and identification analysis.

No prompts, allocation packets, generated solvers, or model calls were created.

## 3. Banks and task verification

The domain is every length-7 string. The primary oracle is
`balance - 2 * minimum_prefix`; the independent oracle counts unmatched closes
from the left and unmatched opens from the right. They agree on all 128 inputs.
Every expected answer is an exact integer.

| Check | Result |
| --- | --- |
| Declared-domain inputs | 128 |
| Diagnostic inputs | 30; 5 per family |
| Evaluation inputs | 98; evaluation counts 9/9/23/23/31/3 |
| Diagnostic/evaluation exact-input overlap | 0 |
| Oracle agreement | 128/128 |
| Adapter contract | exact `int` only; other types fail |

Bank hashes:

```text
domain.json       03a7fb21334909d5cb30fc7a2c5a3ea2a4db8fc425cadb04cad476e620a5559d
diagnostic.json   954be8607889896c2068f21851589060f1ff60ed6347daa24a67dacf0e7a0938
evaluation.json   98a370e0cb174ac4dfa67a4b484354f0050b2699186ea6c5ec05c0927655fc6c
MANIFEST.json     c5b7ef75b55605110fb4ce6b76b34f557e6a7ddef5c09503b138b04345da4f10
```

The bank files are byte-identical to the originally frozen Gate 1 files.

## 4. Target design

At `k = 5`, `C = 1` is attainable only as five failures in one family, and
`C = 0.2` is attainable as `[1,1,1,1,1,0]`.

| Target | Profile | k | C | Slots |
| --- | --- | --- | --- | --- |
| `T0_ONE_CLOSE` | `[5,0,0,0,0,0]` | 5 | 1.0 | 20 |
| `T1_ONE_OPEN` | `[0,5,0,0,0,0]` | 5 | 1.0 | 20 |
| `T2_THREE_CLOSE` | `[0,0,5,0,0,0]` | 5 | 1.0 | 20 |
| `T3_THREE_OPEN` | `[0,0,0,5,0,0]` | 5 | 1.0 | 20 |
| `T4_FIVE_MIXED` | `[0,0,0,0,5,0]` | 5 | 1.0 | 20 |
| `T5_SEVEN_MIXED` | `[0,0,0,0,0,5]` | 5 | 1.0 | 20 |
| `T6_SPREAD` | `[1,1,1,1,1,0]` | 5 | 0.2 | 30 |

Total: **150 slots**. The six `C=1` targets rotate the carrier family. The
single low-C target spans five families and omits `SEVEN_MIXED`.

## 5. Calibration controls

All controls were hand-built and executed through the strict Windows Sandbox,
one input per worker. No expected answer, family label, or bank data was placed
in the guest. A control is a pipeline/calibration check, not a generated solver
and not evidence for H1a.

| Control | Observed vector | k | C | S | Correct/98 | Profile match | Rows valid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `reference` | `[0,0,0,0,0,0]` | 0 | — | 1.000000 | 98/98 | yes | yes |
| `localized_offbyone_0` | `[5,0,0,0,0,0]` | 5 | 1.0 | 0.908163 | 89/98 | yes | yes |
| `localized_offbyone_1` | `[0,5,0,0,0,0]` | 5 | 1.0 | 0.908163 | 89/98 | yes | yes |
| `localized_offbyone_2` | `[0,0,5,0,0,0]` | 5 | 1.0 | 0.765306 | 75/98 | yes | yes |
| `localized_offbyone_3` | `[0,0,0,5,0,0]` | 5 | 1.0 | 0.765306 | 75/98 | yes | yes |
| `localized_offbyone_4` | `[0,0,0,0,5,0]` | 5 | 1.0 | 0.683673 | 67/98 | yes | yes |
| `localized_offbyone_5` | `[0,0,0,0,0,5]` | 5 | 1.0 | 0.969388 | 95/98 | yes | yes |
| `spread_palindrome` | `[1,1,1,1,1,0]` | 5 | 0.2 | 0.887755 | 87/98 | yes | yes |

All eight profiles matched exactly. All rows were complete, well-formed, and
valid; there were no timeouts, crashes, overflows, malformed answers, or
unaccounted failures. The run used 1,024 worker processes and 684.6 seconds of
wall time. The control `SUMMARY.json` SHA-256 is
`48172ed1414c3cb1b67c0d5d412df959119bc21d6b625ce0a2b97d47f28378ce`; per-control
guest capture hashes are recorded there.

This confirms that `S` is not determined by `k`: at `k=5`, observed control `S`
ranges from **0.683673 to 0.969388**. It does **not** confirm H1a. The high-C
controls are deliberately family-specific, and their mean `S` (0.833333,
sample SD 0.110782) is **lower** than the low-C control's `S` (0.887755).

The high-C range itself is a carrier/defect effect: all six controls have
`k=5` and `C=1`, yet their `S` differs by 0.285715. That range is larger than
the 0.10 effect the power analysis was asked to detect. It is not an empirical
estimate of generator variance, because the controls are one author's
hand-built off-by-one mechanisms, not a sample of generated solvers. It does,
however, show why carrier identity cannot be treated as negligible.

## 6. Identification and power

### 6.1 Identification failure (primary finding)

The target set does not identify `C` separately from carrier family or defect
identity. The six `C=1` targets are six different carrier families, each with a
different family-specific defect mechanism. The only `C=0.2` target is one
spread pattern. There is no within-carrier, fixed-`k` contrast between high and
low `C`.

This is not a sample-size problem. More slots at the same profiles would leave
`C` entangled with carrier family and would not create a counterfactual for the
single spread pattern. The evaluation bank is also unbalanced across families
(3 to 31 inputs), so family-specific difficulty can move `S` independently of
`C`.

The bank structure does permit `C = 0.2, 0.4, 0.6, 0.8, 1.0` at `k=5`, because
the largest family count can be 1 through 5. That is an enumeration fact, not a
construction result. A solver that fails exactly two of five probes in one
family and leaves the others untouched may be a different mechanism from one
that fails all five; mathematical attainability alone does not establish that
the five levels can be realized without changing defect identity.

The controls show the same issue descriptively. At fixed `k=5`, the six `C=1`
controls vary over 0.683673–0.969388, while the single `C=0.2` control scores
0.887755. Any high/low difference could be caused by which defect was
constructed, not by concentration. The controls were built to test the
measurement path; they were not sampled from the intended generator population
and cannot supply an empirical residual variance for that population.

### 6.2 Power (secondary finding)

The offline simulation uses 120 high-C and 30 low-C slots, `k=5`, a
high-minus-low effect of 0.10, 20,000 trials, and seed `20261023`. It is a
sensitivity analysis, not a forecast.

| Residual SD | Power at 0.10 | Null rejection | MDE at 80% |
| --- | --- | --- | --- |
| 0.10 | 0.99925 | 0.04815 | 0.050755 |
| 0.15 | 0.94620 | 0.04840 | 0.076132 |
| 0.20 | 0.78565 | 0.04985 | 0.101510 |
| 0.25 | 0.62135 | 0.04940 | 0.126887 |

Power is below 0.80 at residual SD 0.20, and there is no empirical estimate that
justifies using 0.10 or 0.15. The MDE at SD 0.20 is 0.1015, which exceeds the
prespecified meaningful difference of 0.10. Because the simulation does not
condition on carrier family, and the controls show a carrier range larger than
the target effect, there is no basis for assuming residual variation is as
small as the favorable 0.10–0.15 assumptions. The simulation is a sensitivity
analysis, not a forecast.

The pre-deletion planning record recorded power 0.76725 at SD 0.20 and 0.58725
at SD 0.25; the reconstructed simulation gives 0.78565 and 0.62135. The original
simulation bytes were not recovered.

The following table treats the two records as independent seeded runs. The
Monte Carlo SE for each power is `sqrt(p*(1-p)/20,000)`; the difference SE is
`sqrt(SE_pre^2 + SE_new^2)`. The earlier 6.3/9.9 figures divided by the
reconstructed run's SE only and were not a two-run comparison; the correct
two-run values are 4.4 and 7.0.

| Residual SD | Pre-deletion | Reconstructed | Difference | SE pre | SE new | SE difference | Difference / SE difference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0.10 | 0.99920 | 0.99925 | +0.00005 | 0.000200 | 0.000194 | 0.000278 | 0.18 |
| 0.15 | 0.94170 | 0.94620 | +0.00450 | 0.001657 | 0.001595 | 0.002300 | 1.96 |
| 0.20 | 0.76725 | 0.78565 | +0.01840 | 0.002988 | 0.002902 | 0.004165 | 4.42 |
| 0.25 | 0.58725 | 0.62135 | +0.03410 | 0.003481 | 0.003430 | 0.004887 | 6.98 |

The SD 0.20 and 0.25 differences remain far larger than two-run binomial Monte
Carlo noise. The reconstruction is therefore **not behaviorally equivalent** to
the lost simulation script; a different simulation model, random-number
generator, draw order, or implementation detail is a candidate explanation. No
byte-level or behavioral fidelity is claimed. Both versions are below 0.80 at
SD 0.20, so the HOLD decision is unchanged. Neither version supplies an
empirical residual-SD justification.

The standardized gaps are a numerical discrepancy diagnostic, not a clean
equivalence test between two implementations of the same estimator. The
reconstructed simulator is an unadjusted group difference, while the surviving
specification describes a generator-adjusted model; the pre-deletion
implementation is lost. The comparison therefore does not establish which
estimator produced the historical numbers.

### 6.3 Reconstruction audit

The surviving written specification and the reconstructed `power/simulate.py`
were compared on the dimensions that determine the result:

| Dimension | Surviving specification | Reconstructed implementation |
| --- | --- | --- |
| Slots | 120 high-C, 30 low-C | 120/30 |
| `k` | 5 | 5 |
| Effect definition | high-minus-low effect of 0.10 | high-minus-low effect of 0.10, effect-coded 1/0 |
| Noise | residual SD `sigma` on `S` | additive Gaussian noise on `S`; no clipping |
| Estimator | documented primary model includes `k` and generator identity | unadjusted difference of group means; no generator identity |
| Test | one-sided positive-C test | one-sided normal test, critical 1.645; known-SE form |
| Trials | 20,000 | 20,000 |
| Seed/RNG | seed `20261023` recorded; original RNG implementation lost | Python `random.Random(20261023)` |

The estimator mismatch is substantive: the surviving report describes a model
that accounts for generator identity, while the reconstruction uses an
unadjusted group difference. A numeric-`C` coding would also give an 0.08
high-minus-low change at `C=1` versus `C=0.2`, rather than the effect-coded
0.10 actually used. The RNG and draw order are also different from any NumPy- or
other implementation the original may have used. These are candidate causes of
the gap, not a demonstrated explanation.

No surviving artifact establishes which difference produced the pre-deletion
numbers. A search of the repository found only an older, unrelated planning
simulator at `next-task/power_simulation/simulate_next_study_power.py`; it
implements a different natural-solver design (`N_eval=200`, `k` levels
2/6/12/24, a beta grid) and cannot reproduce the H1a table. It is already marked
invalidated for operational planning. No surviving script found in the
repository implements the 120/30 H1a design.

No attempt was made to tune the reconstruction until it matched; doing so would
manufacture agreement rather than establish equivalence. The
reconstruction-equivalence question is therefore **unresolved from surviving
code**.

## 7. Original Gate 1 decision (pre-audit)

**HOLD.**

Failed checks, in priority order:

1. `C` is confounded with carrier family and defect identity in the target set.
2. There is no within-carrier fixed-`k` contrast between high and low `C`.
3. The carrier/family spread in the controls is larger than the target effect,
   and carrier is not conditioned in the estimator or power model.
4. Power is below 0.80 at residual SD 0.20.
5. The MDE at residual SD 0.20 exceeds the prespecified meaningful difference.
6. No empirical residual-SD estimate exists; the calibration control spread is
   not a population estimate.
7. The reconstructed power simulation is not behaviorally equivalent to the
   lost original; the cause of the discrepancy is unresolved.

Passing checks:

- The domain is exhaustive and deterministic.
- The two oracles agree on all 128 inputs.
- The diagnostic/evaluation split is exact-input disjoint.
- The output contract is exact.
- The Sandbox control runs are complete and profile-consistent.
- `S` varies at fixed `k`.

Gate 1 does not support spending the 150-slot budget on the current design. No
Gate 2, prompt, allocation packet, or solver generation is authorized.

## 8. Proposals for a future design (not authorized)

These are options for review, not decisions. They require Foued's authorization
and a new Gate 1 before any generation. Detailed enumeration and allocation
arithmetic are in `05_DESIGN_OPTIONS.md`.

The leading candidate for investigation is **Option B**: hold a two-family pair
fixed and compare `k=5` profiles `(5,0)`, `(4,1)`, `(3,2)`, giving
`C=1.0, 0.8, 0.6`. A six-cycle of pairs gives 18 profiles and a 150-slot
allocation of eight or nine solvers per profile. This is a candidate, not an
approved protocol. It still requires an independent construction audit: a
single family-localized rule produces `(5,0)`, while `(4,1)` and `(3,2)` require
different trigger coverage or compound defects. The bounded audit in §10 did
not establish the required separation; Option B is not adopted.

1. **Balanced high/low design (Option A).** Use six `C=1` family-localized
   profiles at 20 slots each and all six rotations of
   `[1,1,1,1,1,0]` at 5 slots each. This is 150 slots and 25 slots per
   family. It balances family slot exposure, but still compares two defect
   classes and does not remove the defect-identity confound.
2. **Carrier-blocked or within-identity design.** Hold the leading family
   identity fixed and compare profiles at different leading-family counts, or
   treat carrier as a blocking factor in allocation and analysis. Because `C`
   is defined by the leading count, no fixed-`k` design can hold that count
   constant while changing `C`; only carrier identity can be held fixed. At
   `C=0.2` there is no unique carrier, and some `C=0.4` profiles tie. Option B
   uses the identity idea at `C=0.6`, `0.8`, and `1.0`, but it is not a strict
   carrier-only contrast. If the task cannot support the needed contrast, stop
   rather than manufacture one.
3. **Intermediate cells and dose-response.** The 81-cell table already contains
   options such as `k=4, C=0.5` and lower-`k` cells. A dose-response design may
   be more informative than a two-point `C=1` versus `C=0.2` contrast, but it is
   a different study and must be fixed before generation.
4. **Independent power assessment.** Justify the meaningful effect without
   choosing it to fit the 150-slot budget; include carrier blocking, duplicate
   behavior, and failure to attain assigned profiles. A new power analysis
   should be run only after the identification design is fixed.
5. **Narrower claim.** If carrier cannot be separated from `C` in this task,
   narrow H1a to a within-carrier question or stop. Do not silently redesign the
   authorized study.

A fresh freeze would be required for banks, profiles, allocation, estimator, and
stop rules before any solver is generated. If no construction design can
demonstrate separation of `C` from defect mechanism before generation, stopping
at Gate 1 is the correct result. It should be recorded as the outcome, not as a
failed attempt to be retried without a new design.

## 9. Provenance and integrity notes

An accidental local cleanup deleted the working files after the first Gate 1
run. The package was rebuilt and the controls were rerun. Hash comparison can
establish identity only for artifacts whose original hashes were recorded; it
cannot prove that every reconstructed script is byte-identical to its lost
version.

Status summary:

- **Verified:** diagnostic/evaluation banks, manifest, and Sandbox supervisor
  match recorded hashes.
- **Semantically reconciled, byte identity unresolved:** `selected_profiles.json`
  contains the documented targets and 150-slot allocation, but its historical
  hash still does not match.
- **Unresolved:** the power discrepancy’s cause, including estimator
  implementation, effect coding, and random-number draw order.

| Artifact group | Provenance status |
| --- | --- |
| `banks/domain.json`, `diagnostic.json`, `evaluation.json`, `MANIFEST.json` | Hash-verified against pre-deletion hashes. The bank split was also rechecked: 128 = 30 + 98, zero overlap. |
| `03_TASK_SPEC.md`, `core/model.py`, `build_banks.py` | Reconstructed, then hash-verified through the original `MANIFEST.json` hash (`c5b7ef75…`). |
| `runner/sandbox_suite_supervisor.ps1` | Hash-verified against the previously recorded `17011c2c…` hash. |
| `00_CLAIM.md`, `01_TASK_SELECTION_RUBRIC.md`, `02_TASK_SELECTION.md`, `04_DOMAIN_ENUMERATION.md`, `GATE1_REPORT.md` | Reconstructed from the recorded specification; no original byte hash. |
| `profiles/selected_profiles.json` | Reconstructed. The pre-deletion hash was `974fe9cd…`; the rebuilt file is `05f41bf8…`. The seven targets and 150-slot allocation are unchanged, but this file is **not** hash-verified. |
| `profiles/attainable_profiles.csv`, `attainable_cells.csv` | Reconstructed; no original byte hash. Counts rechecked at 46,656 profiles and 81 cells. |
| `core/__init__.py`, `build_profiles.py`, `build_controls.py`, `run_controls.py`, `runner/python_adapter.py`, `power/simulate.py` | Reconstructed; no original byte hash. |
| `controls/` source files and `results/gate1-controls/` | Regenerated and rerun; no original source/capture bytes. All 8 profiles matched and all 1,024 rows were valid. Capture hashes changed because the Sandbox nonce changed. |
| `results/power_analysis.json`, `power_table.csv` | Rerun with the reconstructed simulation; no original byte hash. The pre-deletion record differs beyond Monte Carlo noise (see §6.2), so the reconstruction is not behaviorally equivalent; the HOLD decision is unchanged. |
| `00_CLAIM_DRAFT.md` | Lost in the cleanup and not reconstructed. It is a known loss, not a Gate 1 result. |

The `selected_profiles.json` hash mismatch is the clearest provenance gap. A
semantic comparison against the documented target list gives a bounded answer:

- Current targets are exactly the six `[5 at family j]` vectors with 20 slots
  each, plus `[1,1,1,1,1,0]` with 30 slots; total 150.
- Every vector is attainable under the six-family, five-probe constraint.
- No target, profile value, or slot allocation differs from the documented
  design.

The mismatch therefore cannot be attributed to a substantive target change.
It is consistent with serialization, field ordering, metadata, or generated
file-hash differences, but the original bytes are lost, so the report cannot
prove that those are the only differences. The pre-deletion hash
(`974fe9cd…`) and current hash (`05f41bf8…`) remain separate records.

- No study solver was generated and no model/API was called while preparing this
  report. The later review publication is a separate documentation commit.
- The repository `README.md` still records the pilot as **TERMINATED — INFEASIBLE**
  and says no continuation is authorized. This Gate 1 HOLD does not revive that
  status or authorize generation.
- The original gate decision was **HOLD**. After the bounded construction audit
  in §10, Gate 1 is **CLOSED** for this operationalization; this does not show
  H1a is false.
- This amendment preserves the original HOLD findings and requires another
  review before any generation.

## 10. Bounded Option B construction audit outcome

The bounded audit selected through the delegated decision is recorded in
`08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`, with reproducible implementation and
records in `audit/construction_audit.py` and
`audit/construction_audit.json`. The authorization sequence and basis are stated
in `07_PROCESS_DEVIATIONS.md`.

The audit evaluated 257 hand-built mechanism instances over all 128 inputs
against the independent oracle. Fourteen instances produced `k=5`. No mechanism
family produced more than one distinct `k=5` concentration profile. Eight
cross-mechanism profile matches were found, but all had identical full-domain
failure sets and were algebraically equivalent predicates; there were zero
matches between genuinely different mechanisms. No mechanism family produced
the required two distinct concentration levels.

The stop rule is therefore met. Gate 1 closes for this operationalization
without launching the 150 solvers. This is a bounded negative construction
result, not proof that no possible mechanism exists and not evidence that H1a
is false. Scoring, allocation, and power were not re-frozen; any further design
requires a new authorized study decision.
