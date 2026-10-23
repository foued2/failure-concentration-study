# Design-option analysis

Status: design-level comparison only. This document does **not** authorize
generation, prompts, allocation packets, or a change to the Gate 1 decision.
The original verdict was **HOLD**. The bounded construction audit subsequently
did not establish Option B separation; see
`08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`. Option B is not adopted.

## 1. Constraints held fixed

- One task: `paren7_min_insertions`.
- One exhaustive 128-input domain; 30 diagnostics; 98 evaluation inputs.
- Six structural families; at least one evaluation input per family.
- `k = 5` for the redesign candidates.
- At most 150 study solvers, 50 from each of three generator identities.
- No solver generation in this analysis.
- The unresolved power reconstruction cannot be used as a launch justification.

## 2. Attainable `k=5` profiles

At `k=5`, every vector with non-negative integer family counts summing to five
is attainable. The 252 vectors split by `C` as follows:

| `C` | Largest family count | Profiles |
| --- | --- | --- |
| 0.2 | 1 | 6 |
| 0.4 | 2 | 120 |
| 0.6 | 3 | 90 |
| 0.8 | 4 | 30 |
| 1.0 | 5 | 6 |
| **Total** | | **252** |

The counts sum to 252, the number of non-negative six-family vectors with
`k=5` (stars and bars, `C(10,5)`). The five concentration levels are therefore
mathematically available. That is an enumeration fact only. It does not show
that plausible independent solver mechanisms can realize each level without
changing defect identity.

For `C=0.6`, `0.8`, and `1.0`, the largest family is unique; call it the leading
or carrier family. At `C=0.2` all five nonzero families tie, and at `C=0.4`
some profiles have two families with two failures, so carrier identity is not
unique at those levels.

## 3. Candidate designs

### Option A: balanced high-versus-low

- Twelve profiles: six `C=1` vectors `[5 at family j]` at 20 slots each, and
  six `C=0.2` spread rotations `[1,1,1,1,1,0]` at 5 slots each.
- Total: `6*20 + 6*5 = 150`.
- Each family receives 25 slots, so family exposure is balanced.
- Still compares two defect classes: six family-localized controls at
  `C=1` versus one spread mechanism class at `C=0.2`.

This improves family balance over the current design but does not separate
concentration from defect mechanism.

### Option B: same-family-pair concentration levels

Use a six-cycle of ordered pairs:

```text
(A,B), (B,C), (C,D), (D,E), (E,F), (F,A)
```

For each pair, use three profiles:

| Profile | Vector on the two families | `C` |
| --- | --- | --- |
| concentrated | `(5,0)` | 1.0 |
| more concentrated | `(4,1)` | 0.8 |
| less concentrated | `(3,2)` | 0.6 |

This yields `6 pairs * 3 profiles = 18 profiles`. Each family appears in five
of the 18 profiles: three as the leading family and two as the secondary
family. Each `C` level appears in six profiles.

A 150-slot allocation with 18 profiles requires eight or nine slots per profile:

```text
6 profiles * 9 slots + 12 profiles * 8 slots = 150
```

If two profiles per `C` level receive nine slots and the other four receive
eight, each `C` level receives `2*9 + 4*8 = 50` slots. This is a balanced
design-level allocation, not a power calculation.

Advantages:

- The leading and secondary family roles are fixed within each pair.
- `C` varies from 0.6 to 1.0 using the same pair, reducing carrier-identity
  confounding relative to Option A.
- Family roles rotate across the six-cycle, and each family appears in five
  profiles.

Limitations:

- Eight or nine solvers per profile is thin; with three generators, a profile
  may have only two or three solvers per generator.
- The three profiles differ in both `C` and the vector of failures. A
  family-localized defect that produces `(5,0)` does not automatically produce
  `(4,1)` or `(3,2)`.
- Within a pair, `C` is collinear with the leading family's failure count:
  `(5,0)`, `(4,1)`, and `(3,2)` have 5, 4, and 3 leading failures. Option B
  holds carrier identity, not carrier count. At `C=0.6` the leading family has
  three failures and the secondary family has two, so this is not a strict
  carrier-only contrast.
- Exact-profile construction may require different trigger coverage or compound
  defects, reintroducing mechanism differences. This must be demonstrated with
  hand-built controls, not assumed.
- The six nine-slot profiles must be assigned to avoid concentrating extra
  slots on one family; equal profile counts alone do not guarantee equal slot
  exposure. Because each `(5,0)` profile exposes only one family, family slot
  exposure cannot be exactly equal at this allocation.

### Option C: full multi-level

- Use many or all of the 252 `k=5` profiles across `C=0.2` through `1.0`.
- Average support is `150/252 = 0.60` slots per profile, and many
  profiles would receive one solver or none.
- Rotating vectors and families would spread support too thinly to separate
  concentration, family, generator, and construction effects.
- Useful as an exploratory ideal, not as a 150-solver design.

## 4. Identification condition

Let `m` denote the construction mechanism and `f(m)` its diagnostic profile. The
target is the effect of `C` while the mechanism is held comparable. If `C` is
uniquely determined by `m`, then `C` and mechanism are collinear and no amount
of additional slots at the same profiles identifies the effect.

A sufficient construction would replicate profiles across at least two
independently built mechanisms **and cross those mechanisms with more than one
concentration level**, then treat mechanism as a block or random factor.
Replication within a single profile only estimates construction variance; it
does not identify the `C` effect. This has a direct support cost:

| Design | Profiles | Mechanisms | Cells | Average slots per cell |
| --- | --- | --- | --- | --- |
| A | 12 | 2 | 24 | 6.25 |
| B | 18 | 2 | 36 | 4.17 |
| C | up to 252 | 2 | up to 504 | < 1 |

The cell counts assume mechanisms can be crossed with profiles. With three
generators and 150 slots, the Option B audit would have roughly 1-2 solvers per
mechanism-profile-generator cell. That may be too thin even before failures to
attain assigned profiles are modeled. The construction audit must determine
whether mechanisms can be shared across profiles without changing evaluation
behaviour; if not, Option B is not identified at this sample size.

## 5. Structural comparison

| Property | Option A | Option B | Option C |
| --- | --- | --- | --- |
| Profiles | 12 | 18 | up to 252 |
| `C` levels | 0.2, 1.0 | 0.6, 0.8, 1.0 | 0.2-1.0 |
| Slots per profile | 20 high, 5 low | 8 or 9 | mostly 0 or 1 |
| Family balance | each family 25 slots | each family in 5 profiles | uneven |
| Same family pair across `C` | no | yes | partly |
| Main remaining confound | defect mechanism and family | defect mechanism and construction | sparse support |

Option B is the leading **candidate for investigation**, not an approved
protocol. It improves the family-pair structure but does not by itself solve the
identification problem.

## 6. Construction audit required before adoption

For each selected profile, at least two independently constructed mechanisms
must be shown to produce the same diagnostic vector. In particular:

- `(5,0)` can be produced by a family-localized off-by-one rule.
- `(4,1)` and `(3,2)` require different trigger coverage or compound rules; a
  single family-localized rule cannot produce them.
- If the only way to realize `(4,1)` or `(3,2)` is to change the defect mechanism
  in a way that also changes evaluation performance, the profile contrast is
  not identified.

The audit should test whether evaluation score varies within the same profile
across mechanisms, and whether family effects can be separated from the
concentration contrast. It must not inject exact evaluation inputs into a
control.

## 7. Power and feasibility

No power claim is made here. The original power reconstruction is unresolved,
and the current reconstructed simulation is not behaviorally equivalent to the
lost one. A new power analysis should be run only after:

1. the construction audit demonstrates profile/mechanism separation;
2. a defensible residual-variation model exists;
3. the estimator and allocation are frozen.

With 18 profiles and eight or nine solvers per profile, the 150-slot budget is
already sparse. If the construction audit or a subsequent power analysis shows
that the design cannot separate concentration from mechanism, the correct
outcome is to stop at Gate 1 and record that the 150-solver study is not
adequately identified.

## 8. Recommendation

Option B was investigated under the bounded construction audit. The audit did
not demonstrate two genuinely different mechanisms with matched profiles at
more than one concentration level, so the stop rule was met and Option B was
not adopted. Do not generate solvers, prompts, or allocation packets. Do not
treat the original Gate 1 HOLD as a launch decision.
