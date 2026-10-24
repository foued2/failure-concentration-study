# Bounded Option B construction audit result

**Status:** NEGATIVE — no separation demonstrated in the bounded audit
**Gate 1:** CLOSED for this operationalization
**Gate 2 authorized:** no
**Study solvers generated:** 0
**Generator prompts/calls:** 0
**Power simulation run:** no

## 1. Authorization and scope

This audit was performed under the bounded construction-audit decision delegated
by Foued to Claude/GPT and selected by GPT. The conversation contains no separate
literal "authorize audit" reply from Foued; the authorization basis and sequence
are recorded in `07_PROCESS_DEVIATIONS.md`. The earlier
`06_OPTION_B_IDENTIFICATION_AUDIT.md` was produced before that decision and is
not the later construction-audit report.

It is design and offline analysis only. It did not create study solvers, prompts,
allocation packets, generator requests, or a new power simulation, and it did not
change the frozen banks.

The audit asked whether at least two genuinely different, non-lookup defect
mechanisms can produce matched diagnostic profiles at more than one
concentration level while leaving held-out performance measurable. The
`selected_profiles.json` file was not modified.

This is a bounded negative result. It shows that the tested hand-built
mechanism families do not establish the required separation. It is not a proof
that no possible mechanism exists and it does not show that H1a is false.

## 2. Method

`audit/construction_audit.py` evaluates 257 hand-built mechanism instances over
the full 128-input domain:

- prefix-minimum termination defects;
- wrong minimum initialization;
- unmatched-close omission;
- stack-recovery defects;
- prefix and suffix truncation;
- wrong minimum-update modes;
- a sign error in the prefix-minimum formula; and
- threshold rules on structural text statistics.

The mechanisms use only text properties and algorithmic rules. They do not
look up exact input strings, diagnostic membership, or evaluation membership.
Every output was checked for exact `int` type and compared with
`core.model.independent_answer` over all 128 inputs.

The audit uses these operational definitions:

- A **mechanism family** is the candidate-name prefix before the first `(`,
  such as `min_tail` in `min_tail(r=1)` or `close_eq` in `close_eq(5)`.
- A **distinct mechanism match** is a pair from different families with the
  same `k=5` diagnostic profile but different full-domain failure sets. A pair
  with identical full-domain failure sets is treated as an equivalent
  predicate, not as independent evidence.
- The threshold values for the `eq`/`ge`/`le` text-statistic candidates are the
  distinct values of each feature observed in the 30 diagnostic inputs.

The threshold search is therefore informed by the diagnostic bank. It does not
look up exact diagnostic or evaluation strings and does not use evaluation-set
membership to define candidates, but the candidate set is not wholly independent
of the diagnostics. The 257-instance set is bounded and hand-coded; it is not an
exhaustive search over all possible programs.

For each mechanism the audit recorded:

- the diagnostic failure profile by family;
- `k` and `C`;
- evaluation failures by family;
- raw and equal-family evaluation scores; and
- the full-domain failure-set hash.

The candidate set is fixed in `audit/construction_audit.py`. It was not
expanded after the final audit output to force a desired profile.

## 3. Results

Of the 257 mechanism instances, 14 produce `k=5`. No mechanism family produced
more than one distinct `k=5` concentration profile:

```text
families_with_multiple_k5_profiles = {}
```

The 14 `k=5` records are:

| Mechanism | Diagnostic profile | C | Eval failures | Raw S | Equal-family S |
| --- | --- | ---: | --- | ---: | ---: |
| `min_tail(r=1)` | `[1,0,2,0,2,0]` | 0.4 | `[4,0,7,0,3,1]` | 0.846939 | 0.803517 |
| `close_eq(5)` | `[0,0,4,0,0,1]` | 0.8 | `[0,0,10,0,6,0]` | 0.836735 | 0.895278 |
| `open_eq(2)` | `[0,0,4,0,0,1]` | 0.8 | `[0,0,10,0,6,0]` | 0.836735 | 0.895278 |
| `bal_eq(-3)` | `[0,0,4,0,0,1]` | 0.8 | `[0,0,10,0,6,0]` | 0.836735 | 0.895278 |
| `close_le(2)` | `[0,0,0,2,1,2]` | 0.4 | `[0,0,0,12,11,1]` | 0.755102 | 0.798348 |
| `open_ge(5)` | `[0,0,0,2,1,2]` | 0.4 | `[0,0,0,12,11,1]` | 0.755102 | 0.798348 |
| `bal_ge(3)` | `[0,0,0,2,1,2]` | 0.4 | `[0,0,0,12,11,1]` | 0.755102 | 0.798348 |
| `pair_eq(0)` | `[0,0,0,0,0,5]` | 1.0 | `[0,0,0,0,0,3]` | 0.969388 | 0.833333 |
| `pair_le(0)` | `[0,0,0,0,0,5]` | 1.0 | `[0,0,0,0,0,3]` | 0.969388 | 0.833333 |
| `max_eq(2)` | `[1,2,1,1,0,0]` | 0.4 | `[4,5,1,5,1,0]` | 0.836735 | 0.784479 |
| `closes_prefix_ge(3)` | `[0,0,0,0,2,3]` | 0.6 | `[0,0,2,0,7,2]` | 0.887755 | 0.836762 |
| `opens_suffix_ge(3)` | `[0,0,0,1,1,3]` | 0.6 | `[0,0,0,1,8,2]` | 0.887755 | 0.838632 |
| `closes_suffix_eq(2)` | `[2,1,0,1,1,0]` | 0.4 | `[3,2,5,1,0,0]` | 0.887755 | 0.863929 |
| `last_open_eq(4)` | `[2,1,0,1,1,0]` | 0.4 | `[3,2,5,1,0,0]` | 0.887755 | 0.863929 |

Eight cross-mechanism profile matches were found. All eight are pairs with
**identical full-domain failure sets**:

| Profile | C | Matched instances |
| --- | ---: | --- |
| `[0,0,4,0,0,1]` | 0.8 | `close_eq(5)`, `open_eq(2)`, `bal_eq(-3)` |
| `[0,0,0,2,1,2]` | 0.4 | `close_le(2)`, `open_ge(5)`, `bal_ge(3)` |
| `[0,0,0,0,0,5]` | 1.0 | `pair_eq(0)`, `pair_le(0)` |
| `[2,1,0,1,1,0]` | 0.4 | `closes_suffix_eq(2)`, `last_open_eq(4)` |

The eight unordered pairs reduce to four unique diagnostic profiles; the
three-instance groups produce multiple pairings within each group. These are
algebraically equivalent predicates on length-seven strings, not independent
mechanisms. The number of matches with **different** full-domain failure sets is:

```text
distinct_mechanism_matches = 0
```

No candidate mechanism family produced two distinct `k=5` profiles at different
concentration levels. The required criterion—two genuinely different
mechanisms, each realized at more than one concentration level, with matched
profiles where comparisons are intended—is therefore not met.

## 4. Scoring observations

Both scoring rules were recorded for every mechanism; neither was adopted as a
new primary estimand here. The records show the same issue as the calibration
controls:

- raw `S` is domain-weighted and moves with the family composition of the
  failure set;
- equal-family `S` removes that weighting but does not make different
  mechanisms comparable; and
- the matched-profile pairs above have identical scores because their
  full-domain failure sets are identical.

Choosing a scoring rule remains a pre-generation decision for Foued. This audit
does not settle it.

## 5. Stop rule and disposition

The bounded audit cannot show the required separation. Under the stated stop
rule, Gate 1 closes for this operationalization without launching the 150
solvers.

What this establishes:

- the current design's concentration levels are not demonstrated to be
  constructible independently of mechanism identity; and
- the current 150-slot allocation cannot be justified by this audit.

What this does not establish:

- that H1a is false;
- that no possible hand-built mechanism could separate the profiles; or
- that a different task or a larger redesign could not be testable.

Any further design work needs a new, explicitly authorized study decision. No
new generation, prompt, packet, solver, or power analysis is authorized by this
result.

## 6. Reproducibility

- `audit/construction_audit.py` — reproducible audit implementation.
- `audit/construction_audit.json` — all 257 candidate records, including each
  candidate's full failure list, failure-set SHA-256, diagnostic profile, `k`,
  `C`, evaluation failures, and both scores; it also contains all 14 `k=5`
  records, the matched-profile summaries, and the operational definitions above.
- `audit/PROVENANCE_SHA256.txt` — SHA-256 manifest for the 57 study files,
  computed from the committed Git blobs. The manifest is omitted from its own
  entries.
- The audit ran with `PYTHONDONTWRITEBYTECODE=1`; `__pycache__` is excluded from
  provenance. The earlier local list under `%TEMP%\opencode\` is superseded by
  the committed manifest.
