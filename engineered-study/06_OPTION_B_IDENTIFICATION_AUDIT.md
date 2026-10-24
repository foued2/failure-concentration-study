# Option B identification audit

Status: design and offline analysis only. The original Gate 1 verdict was
**HOLD**; the bounded audit result is recorded in
`08_OPTION_B_CONSTRUCTION_AUDIT_RESULT.md`. No generator prompts, study
solvers, allocation packets, model calls, or simulation runs were produced for
this note.

Authorization note: this note was produced before the delegated
construction-audit decision was recorded, and no separate explicit Foued
authorization was recorded for this note. It is logged as a process deviation in
`07_PROCESS_DEVIATIONS.md`. It is not retroactively authorized, and it does not
satisfy the construction-audit criterion described below.

## 1. Scope

This note tests whether the Option B structure can support a fair fixed-`k`
comparison of concentration that is separate from family identity and defect
mechanism. It does not authorize the 150-slot study.

The audit is incomplete in one decisive respect: no pair of independently
constructed mechanisms has been shown to realize the same target profile across
multiple concentration levels. The evidence below is sufficient to reject the
claim that such a construction has already been demonstrated; it is not a proof
that no construction exists.

## 2. Scoring audit

The current `S` is the fraction of all 98 evaluation inputs that are correct. It
is therefore domain-weighted by the unequal evaluation-family sizes. A
localized control that fails one complete family has

```text
S = 1 - evaluation_inputs_in_family / 98
```

which explains the observed range `0.683673` to `0.969388`.

An equal-family score is a different estimand:

```text
S_equal = (1/6) * sum_family(correct_family / evaluation_inputs_family)
```

Under that score the six localized controls collapse to the same value:

| Control | Raw `S` | Equal-family `S` |
| --- | ---: | ---: |
| Each of the six localized controls | 0.683673-0.969388 | 0.833333 |
| `spread_palindrome` | 0.887755 | 0.829282 |
| `reference` | 1.000000 | 1.000000 |

Equal-family weighting removes the family-size artifact, but it does not repair
the separate mechanism confound and it removes the apparent score variation
among the concentrated controls. The scoring rule must be fixed before any
generation decision; the raw and equal-family outcomes answer different
questions. Equal-family scoring is not justified merely because it produces
cleaner control results. It is appropriate only if the intended estimand gives
the six families equal scientific weight; domain-weighted scoring is appropriate
only if the 98 evaluation strings are the target population.

## 3. Mechanism probe

A family-localized off-by-one defect is a straightforward construction for
`(5,0)`: it fails every diagnostic and evaluation input in its carrier family.
It does not produce `(4,1)` or `(3,2)` without a different trigger or an
exception.

A limited probe over simple text predicates and family interactions found:

- No simple predicate producing an exact `(5,0)` other than the family-localized
  rule itself.
- One contrived exact `(4,1)` rule for the pair `ONE_CLOSE`/`ONE_OPEN`: fail
  `ONE_CLOSE` except when `text.count(")(") == 3`, and fail `ONE_OPEN` when that
  condition holds. It produced evaluation failures `(9,0,0,0,0,0)`.
- No exact `(3,2)` rule in the same probe.

This is not a complete construction audit. The one `(4,1)` example is not
independent replication: it is a single hand-designed exception pattern, and
its evaluation failures do not preserve the diagnostic profile's apparent
family split. It illustrates the central problem: a diagnostic count vector does
not determine evaluation behaviour. A valid audit needs at least two
independently built mechanisms per profile, and the mechanisms must be crossed
with more than one concentration level.

Literal injection of selected diagnostic or evaluation inputs is excluded
because it would manufacture the desired profile rather than test a plausible
solver mechanism.

## 4. Support and identification

Option B has 18 profiles. With two mechanisms per profile, there are 36
mechanism-profile cells. At 150 slots:

```text
150 / 36 = 4.17 slots per mechanism-profile cell
150 / (36 * 3 generators) = 1.39 slots per mechanism-profile-generator cell
```

Each profile has only eight or nine slots, so splitting by mechanism and
generator leaves roughly one to two solvers per cell. That is too little to
estimate mechanism variance, mechanism-by-concentration interaction, and
generator variation while also estimating the concentration effect. Replication
within one profile estimates construction variance only; it does not identify
the `C` effect when `C` remains tied to the profile and mechanism.

The Option B profile ladder `(5,0)`, `(4,1)`, `(3,2)` also changes the leading
family's failure count from five to four to three. `C` is therefore collinear
with carrier count within a pair, even though carrier identity is held fixed.
Option B holds carrier identity, not carrier count.

## 5. Domain and boundary claim

The domain is the exhaustive set of 128 length-seven strings. It contains no
input-scale variation. The current task can support, at most, a narrow
fixed-domain claim. It cannot test a boundary-performance mechanism that depends
on input scale, and no scale-boundary claim should be attached to this task.

## 6. Provenance check

The LF-normalized copy of `selected_profiles.json` does not reproduce the
historical hash:

```text
current raw     05f41bf89d99d46e5b531b00ecffa79b09fd846c0604bab73d31b1dedcaf0de3
CRLF -> LF      cff38ab9ce9f4490447d6767fd639b99875fe17d639979ba41358b07e482b66d
historical      974fe9cd62550fcd1a578eca75a950c1d11205c5d2e779c44af95afc332f02e8
```

The discrepancy remains unresolved. The original file was not modified. A
24-variant JSON reserialization probe also found no match.

The provenance list must exclude `__pycache__` build artifacts. The current
corrected list is saved outside the study at:

```text
C:\Users\pakla\AppData\Local\Temp\opencode\ENGINEERED_STUDY_HASHES_NO_PYCACHE-20261023-161235.txt
```

## 7. Finding

An identifiable Option B design has **not** been established. This does not
show that H1a is false; it shows that the present operationalization has not
established a testable H1a study. The current evidence shows that:

1. the raw score confounds concentration with family size;
2. the equal-family score removes that artifact but makes the localized
   controls indistinguishable;
3. target diagnostic profiles do not determine evaluation behaviour;
4. the 150-slot budget leaves insufficient support for a mechanism-crossed
   audit; and
5. the fixed domain cannot support a scale-boundary claim.

The appropriate disposition is to stop at Gate 1 unless Foued authorizes a
separate, fully specified hand-built construction audit. Do not allocate the
150 slots, generate prompts or solvers, or treat the reconstructed power
figures as launch evidence.

## 8. Required next decision

If a construction audit is authorized, it must be limited and offline, and it
must pre-specify:

- the scoring estimand (domain-weighted or equal-family);
- at least two independently built mechanisms per selected profile;
- a mechanism crossing that includes more than one `C` level;
- support sufficient to estimate the mechanism and generator variance; and
- a stopping rule if the profiles cannot be realized without changing the
  evaluation mechanism.

Without those conditions, Option B is not an identifiable design.
