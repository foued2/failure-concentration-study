# `C_D` measurement specification and exposure register — 2026-11-19

**Status:** measurement-layer specification. Design only. Adds no hypothesis, executes nothing,
changes no frozen document.
**Scope:** `C_D` as defined in `LC518_A2_AUDIT_PROTOCOL_DRAFT_2026-11-06.md` Rev 11.
**Purpose:** close the three measurement questions raised in review — unresolved outcomes, D6 paired
records, and exposure — by separating what the protocol already fixes, what it prohibits, and what is
genuinely new.

---

## 1. Frozen definitions, quoted

From Rev 11 (`LC518_A2_AUDIT_PROTOCOL_DRAFT_2026-11-06.md`):

| Element | Text | Line |
|---|---|---|
| Strata | "The eight diagnostic input strata are indexed `j = 1..8`" | 216 |
| Numerator | "`f_j` is the number of **definite** diagnostic failures in stratum `j`" | 216–217 |
| Volume | "`k_fail = Σ_j f_j`" | 217 |
| Statistic | "`C_D = max_{j=1..8}( f_j / k_fail )`" | 220 |
| Degenerate case | "with the convention **`C_D = 0` when `k_fail = 0`** (labelled **NO OBSERVED FAILURES**)" | 220–221 |
| Unresolved | "`k_unresolved` does not enter `C_D`; it is part of the cell identity only" | 223 |
| Exact cell | "The full B1 support cell is `(m, z, k_fail, k_unresolved)`" | 226 |
| Counting unit | "`N` is the number of **diagnostic bank records per solver body** … **not** unique mathematical inputs" | 230–233 |

Three facts follow immediately and are not open questions:

1. The strata are **diagnostic input categories**, not mechanisms. The mechanism `m` is a separate
   dimension of the cell. Review statement "eight strata, not eight mechanisms" is **verified** by
   lines 216 and 226.
2. Unresolved outcomes are excluded from the numerator *and* the denominator, because `f_j` counts
   definite failures only. They are retained in the **cell**, not in the statistic.
3. The bank's record count `N` is the counting unit, by explicit choice, with the unique-input
   distinction acknowledged in the same sentence.

---

## 2. Exposure: two statistics, not one

The generated bank's two exposure schemes, from records that already exist:

| Basis | `N` | `R_j` | `D6` uniqueness | Source |
|---|---|---|---|---|
| Record-level | 64 | `(8,8,8,8,8,8,8,8)` | 8 records = 4 canonical × 2 orderings | capacity addendum §1; erratum §1 |
| Canonical | 60 | `(8,8,8,8,8,4,8,8)` | 4 unique | capacity addendum §1, canonical row |

The erratum confirms the same structure on the held-out side: 80 records, 78 unique canonicals, 6
duplicate-canonical rows across the whole bank, 138 distinct oracle answers covering 144 records.

**The two bases are different statistics, not two codings of one.** Changing the basis changes `N`, the
capacity vector `R_j`, and therefore the attainable set of `C_D` at each `k_fail`. A paired record that
is deduplicated changes both the numerator (if both mates fail) and the denominator.

**Consequence for any sensitivity analysis:** canonical-level `C_D` must be **recomputed** from the
canonical failure vector. It must not be obtained by averaging or selecting paired values.

**The repo reached this before the review did.** The capacity addendum already states:

> "The two records of a `D6` ordering pair are the same canonical input reordered; under the frozen
> layout their outcomes are dependent, so counting them as two independent measurements inflates the
> apparent variation."

That is exactly the concern raised in review, recorded on 2026-11-10, and used to recommend the
canonical basis (`2 ≤ k ≤ 53`) for capacity work while keeping record-level as an upper bound. The
protocol nonetheless pins **record-level** counting for `C_D`. Both positions are defensible; they are
about different questions (capacity envelope vs measured statistic), and the difference is now stated
rather than assumed.

**Required, currently unstated:** which basis the **primary** B1 analysis uses. The protocol says
records; B1 v1.7 says "canonical-record row" and scores "all 78 records". The two statements are
compatible only if "canonical-record row" means one row per canonical on the held-out side. That must be
written down explicitly, because it determines whether `C_D` and `Y` are aligned.

---

## 3. Unresolved outcomes: what is legal

Claude's proposal — report unresolved counts by stratum, and run a sensitivity treating unresolved as a
separate class — splits into one part that is already required, one part that is legal and useful, and
one part that is **prohibited by the frozen protocol**.

### 3.1 Already required (input layer)

Protocol line 107–112 requires the witness to supply **both** vectors in full:

> "failure-count vector `f = (f_1,…,f_8)` and the unresolved-count vector `u = (u_1,…,u_8)`, both in
> `Z_{≥0}^8` with **all eight entries supplied**"

and line 119:

> "An **omitted unresolved vector is missing evidence, not an implicit all-zero**"

So the per-stratum unresolved profile is **already mandatory evidence** for admissibility. What is *not*
mandated is a **reporting table** of `u` alongside `C_D` in results. That gap is real and small.

### 3.2 Legal and useful (reporting and sensitivity)

- A per-stratum `(P_j, F_j, U_j)` table for every solver body, with `k_fail`, `k_unresolved`, and
  `C_D`, plus the exposure basis. This makes selection visible.
- A sensitivity in which the **outcome model** becomes three-category (pass / definite fail /
  unresolved) instead of binary, with `C_D` unchanged. This tests whether the predictive signal depends
  on how unresolved runs are scored, without touching the feature.
- Reporting the within-cell rank correlation between `u` placement and `C_D` — already required as the
  N4-b channel report in B1 v1.7 §11(f).

### 3.3 Prohibited (and why the reviewers' phrasing needs correcting)

B1 v1.7 and the protocol forbid recoding unresolved outcomes as failures. Protocol line 210–211
requires that an unresolved outcome "must never be converted into 0 or 1 for convenience". B1 v1.7
§5.2 treats unresolved placement `ξ_v` as a **named confounding channel** (N4-b), not as a scoring
choice.

Therefore the suggestion to "treat unresolved outcomes as a separate class" is acceptable **only** as an
outcome-model sensitivity. Any version that adds unresolved counts to `k_fail`, or scores unresolved as
failure, violates a frozen rule and is not a valid sensitivity. This distinction is the whole content of
Claude's point 1 once the protocol is read.

**What remains genuinely open:** whether a three-category primary outcome is scientifically preferable
to the binary one. The repo has never argued for either; it inherited binary scoring from v0.2. That is
a legitimate design question, and it belongs to the measurement gate, not to the frozen record.

---

## 4. The `k_fail = 0` convention is inconsistent across instruments

| Instrument | Treatment of `k = 0` |
|---|---|
| LC518 Rev 11 | `C_D = 0`, labelled **NO OBSERVED FAILURES** |
| Three-world simulation | `C = undefined`; those cases excluded from models using `C`; raw rows retained and summarised separately |

Both conventions are internally defensible. Together they mean the two instruments **do not measure the
same variable**, and results cannot be pooled or compared at `k = 0`.

Three consequences, in increasing order of importance:

1. **Within a cell, harmless.** The B1 cell fixes `k_fail`. A `k_fail = 0` cell has `C_D ≡ 0` with zero
   within-cell variance, so it contributes nothing and fails the `W > 0` estimability gate by
   construction. No bias enters through the cell.
2. **Pooled descriptives are invalid.** Any table or figure that averages `C_D` across `k` mixes
   "undefined" with "no dominance". The protocol's `0` label is a display convention and must be
   reported as a separate category, never as a low value of `C_D`.
3. **Cross-instrument comparison is invalid at `k = 0`.** A statement of the form "the simulation
   excluded 51 cases that the bank scores as 0" is a statement about two different estimands.

**Required:** every reported `C_D` distribution states its `k = 0` convention and reports the count of
such rows separately. The current documents do not do this consistently.

---

## 5. Required reporting table

For each solver body `v`, on a declared exposure basis:

| Column | Definition | Source obligation |
|---|---|---|
| `basis` | `record` or `canonical` | §2; must be stated, not inferred |
| `f_1 … f_8` | definite failures per stratum | protocol 107–112 |
| `u_1 … u_8` | unresolved per stratum | protocol 107–112, 119 |
| `k_fail` | `Σ f_j` | protocol 217 |
| `k_unresolved` | `Σ u_j` | protocol 223 |
| `C_D` | `max f_j / k_fail`, with the `0` convention flagged | protocol 220 |
| `N`, `R_1 … R_8` | exposure per solver body | protocol 235–239 |
| `k = 0` indicator | whether the row is a NO OBSERVED FAILURES row | §4 |

`N = Σ_j R_j` must hold on the stated basis. For the record basis: `64 = 8×8`. For the canonical basis:
`60 = 8×7 + 4×1`.

---

## 6. What this document does not do

- It does not change the frozen `C_D` definition, the cell, or the counting unit.
- It does not adjudicate record vs canonical for the primary analysis; it requires that the choice be
  stated and that the other basis appear as a labelled sensitivity.
- It does not run anything, and it does not assert that any exposure scheme is correct.
- It does not turn the unresolved question into a result. It partitions it into required, legal, and
  prohibited — and leaves the scientific preference open.

**Gate 1 status after this document:** the exposure and unresolved issues are now **specified but not
resolved**. The measurement gate still requires evidence that the partition captures a reproducible
pattern. That evidence does not exist: no solver has been evaluated.
