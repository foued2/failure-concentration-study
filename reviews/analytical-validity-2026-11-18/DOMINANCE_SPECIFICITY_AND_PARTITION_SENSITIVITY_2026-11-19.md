# Dominance specificity and partition sensitivity — 2026-11-19

**Status:** design record and adjudication note. Adds no hypothesis, authorizes nothing, modifies no frozen
document, executes nothing.
**Answers:** the question GPT sharpened — is `C_D` merely *a* compact predictor, or is the
maximum-share property doing the work, and does the prespecified partition matter?
**Does not answer:** whether any of these comparisons would succeed. None can be evaluated before
solvers exist.

---

## 1. Three operations that are easy to confuse

The review round produced one proposal and one correction. Sorting them out requires distinguishing three
operations, only one of which is already frozen.

| # | Operation | What moves | Effect on `C_D` | Status |
|---|---|---|---|---|
| 1 | Within-cell permutation of `C_D` labels | The supplied exposure `C_D` among versions in a cell | Distribution changes across versions; multiset fixed | **Frozen in B1 v1.7 §5.2–§5.3** |
| 2 | Permutation of the eight stratum **names** | Labels `j = 1..8` | **None.** Identically invariant | Inert; see §2 |
| 3 | Reallocation of diagnostic **inputs** to strata | The mapping record → stratum | Changes `f` and therefore `C_D` | Not frozen, not authorized; see §3 |

Operation 1 is the confirmatory randomization test. Operation 2 is what Claude proposed and GPT rejected.
Operation 3 is what GPT substituted, correctly identified as a *different* and as-yet unapproved analysis.

---

## 2. Why name permutation is inert — and slightly worse than inert

For any permutation `π` of `{1,…,8}`:

```
C_D' = max_j f_{π(j)} / Σ_j f_{π(j)} = max_j f_j / Σ_j f_j = C_D
```

The maximum is order-independent and the sum is a sum. So `C_D(v)` is unchanged for every `v`,
whether `π` is drawn once globally or independently per parent, per cell, or per version.

**`C_D` depends on `f` only through the multiset `{f_1,…,f_8}`.** It is invariant under the entire
symmetric group acting on stratum labels. That is not an accident of the index; it is the content of
"dominance". Consequently:

1. **No experiment that permutes names can test whether the partition matters.** It is mathematically
   incapable of producing a difference. GPT's rejection is correct and the reason is the permutation
   invariance itself, not a detail of implementation.
2. **Under the canonical exposure basis, admissibility is a *condition*, not a veto.** The frozen
   exposure vector is `R = (8,8,8,8,8,4,8,8)` — stratum 6 holds four canonical inputs, the rest hold
   eight. A name permutation that leaves `R` attached to positions is admissible only for the
   sub-class that preserves `f_j ≤ R_j` for every `j`; the constraint bites only when a count greater
   than four is moved into the D6 position. Permutations among the seven eight-capacity positions,
   leaving D6 in place, remain admissible, and the identity is always admissible. **Every admissible
   relabelling is still inert with respect to `C_D`.** So the capacity argument does not carry the main
   result — invariance does — and the correct summary is: *some relabellings violate the canonical
   exposure constraints; every relabelling that remains admissible is inert.*
3. **What the invariance does establish:** if a positive B1 result is found, it cannot be attributed to
   *which* diagnostic category dominated. `C_D` records only that some category dominated, and by how
   much. Any interpretive statement of the form "failures concentrate in the concurrency stratum and that
   is what predicts" is outside what `C_D` can carry.

Statement 3 is the useful residue of Claude's proposal, and it belongs in the interpretation rules rather
than in a new experiment.

---

## 3. What input reallocation would test, and why it is not B1

Reallocating diagnostic inputs to different strata changes which failures enter each `f_j`. It therefore
changes `C_D`. The question it addresses is:

> Does the prespecified semantic partition produce more useful predictive information than arbitrary
> partitions with comparable exposure?

That is **partition specificity**. It is a legitimate question, it is not the B1 estimand, and it is not
implementable inside the frozen test. The reason is structural rather than procedural.

### 3.1 The exact cell survives the operation — this is the design's main merit

Reallocation permutes **which record contributes to which `f_j`**; it does not change any record's
outcome. Therefore for every solver body:

- `k_fail = Σ_j f_j` is unchanged,
- `k_unresolved = Σ_j u_j` is unchanged,
- the exact cell `(q, Z, k_fail, k_unresolved)` is unchanged.

So the **exact-cell baseline is identical across every reallocation draw**. The enriched model differs
only in the supplied feature. That is a clean within-cell comparison, and it is the strongest argument in
favour of ever running the sensitivity.

### 3.2 Why it cannot be inserted into §5.3

B1 v1.7 §5.2 defines the resampling unit as the *within-cell `C_D` label*, with the **within-cell `C_D`
multiset held fixed** under `H₀^perm`. Three guarantees are built on that:

| Guarantee | Frozen clause | Status under reallocation |
|---|---|---|
| Audit equality | §5.3 step 1: the declared audit-equality key `A(b) = A(b_obs)` must be reproduced; a cell that becomes estimable makes the assignment inadmissible | `W_{C,c} = Σ(C_D − C̄_D)²` changes when the multiset changes, so estimability becomes draw-dependent |
| Permutation-invariant target population | §5.3 step 3 | Scored cells can differ across draws unless admissibility is defined to prevent it |
| Super-uniformity conditional on the availability event | §5.7 V3, V5 | The conditioning event is defined over assignments that share a multiset |

**What follows, stated precisely:** reallocation is incompatible with B1's **frozen resampling law and
null hypothesis**. It is not established to be impossible to design a valid procedure.

The distinction matters and an earlier draft of this section blurred it. Option A of §3.3 — restricting
the admissible assignment space to draws that reproduce the observed audit-selection key — is exactly the
route by which a fixed scored population *could* be preserved. If such a space can be defined and its
selection event characterised, a conditional partition-randomization test could in principle be given an
analogous validity argument.

But **none of B1's guarantees transfers automatically to that new space.** The null is different, the
assignment law is different, the conditioning event is different, and super-uniformity would have to be
re-established for the new space rather than inherited. A separate design would need its own defensible
assignment law, null hypothesis, selection conditioning, and proof of conditional validity — all
predeclared, none of which exists.

So: not valid under the frozen procedure, and not shown to be impossible. Both halves are load-bearing.

### 3.3 The unresolved fork

If such a sensitivity is ever specified, it must first choose between two options, and neither is
currently decided:

| Option | Consequence |
|---|---|
| **A. Admissibility by design-only condition.** Declare in advance that a draw is admissible only if it reproduces the observed audit-selection key | Could keep a fixed target population, at the cost of conditioning on a `C_D`-configuration event, so the reference distribution is not the naive "random partition" law. Validity would have to be proved for that space |
| **B. Per-draw audit.** Let each draw fix its own scored cells | Faithful to each draw, but the comparison is then between analyses on different populations, and a draw-level difference can be produced by coverage rather than by the feature |

Option A is closer to the frozen plan's admissibility logic; option B is closer to what a "random
partition" intuition suggests. The choice changes what the sensitivity means, so it cannot be left
implicit.

### 3.4 Requirements if it is ever authorized

Ordered as a checklist, none currently satisfied:

| # | Requirement |
|---|---|
| 1 | **Declared basis.** Record basis (`8 × 8` records) for comparability with the frozen `C_D`; canonical basis as a separately labelled secondary. |
| 2 | **Group sizes fixed.** Record basis: eight groups of eight. Canonical basis: four groups of seven and four of eight, since `60 = 4×7 + 4×8` and equal groups of eight are arithmetically impossible. |
| 3 | **D6 pair integrity.** The four D6 canonical inputs carry paired orderings; either both orderings move together or the canonical basis is used. |
| 4 | **One common partition across all variants.** Not per-variant, not per-parent. Otherwise every solver faces a different instrument and the comparison is meaningless. |
| 5 | **A declared draw law.** Either a fixed number of draws with a seed, or full enumeration where the space is small enough. |
| 6 | **The §3.3 fork resolved before any draw.** |
| 7 | **Multiplicity.** The partition comparison joins the same family as the alternative-summary comparisons of §4, with a predeclared correction. |
| 8 | **Identical downstream pipeline.** Same folds, same fitting rules, same separation rule, same reporting, applied without modification. |

---

## 4. Alternatives to the maximum share

Within an exact cell, `k` and `ℓ` are fixed, so total failure count cannot explain an incremental `C_D`
gain. But the *shape* of `f` can still vary, and other shape summaries are available. GPT is right that
this is the substantive competitor, and it is stronger than the partition question because it needs no new
instrument.

Three candidate summaries, all functions of the same multiset `{f_j}`:

| Summary | Definition on shares `p_j = f_j/k` | Relationship to `C_D` |
|---|---|---|
| Second-largest share | `p_(2)` | Order statistic; coincides with `C_D` under ties at the maximum, separates shapes that `C_D` collapses |
| Shannon entropy of shares | `−Σ p_j log p_j` (with `0 log 0 = 0`) | Decreasing in concentration; nearly but not always injective on shape — see the `k = 8` coincidence in §4.1 |
| Herfindahl / Simpson | `Σ p_j²` | Contains `C_D²` as a component; the quadratic penalty on the dominant share is the distinguishing feature |

**All three sit under the same information ceiling as `C_D`.** Each is `F`-measurable, so each obeys
`I(Y;S|X) ≤ I(Y;F|X)`. The comparison is about which scalar compression is better, never about beating
`F` (see the novelty register §3).

### 4.1 What identifies each comparison, and why direction matters

Two different questions are easy to swap, and an earlier draft of this section swapped them:

| Question | Relevant variation |
|---|---|
| Do the alternatives add information **beyond `C_D`**? | Same `C_D`, different `S` |
| Does `C_D` add information **beyond `S`**? | Same `S`, different `C_D` |

Level 2 of the claim ladder asks the second question. So the identifying variation is **equal `S` with
differing `C_D`**, and it must be computed **separately for each competitor**. The previous draft used the
first kind of collision (equal `C_D`, differing alternatives), which identifies the wrong thing.

At fixed `k` the number of distinct shapes is the partition number of `k` into at most eight parts, while
`C_D` takes at most `k` distinct values. Enumerating shapes exactly and grouping by each competitor gives:

| `k` | Shapes | Distinct `C_D` | `p_(2)`: classes / with ≥2 `C_D` | Herfindahl: classes / with ≥2 `C_D` | Shannon: classes / with ≥2 `C_D` |
|---|---|---|---|---|---|
| 3 | 3 | 3 | 2 / **1** | 3 / 0 | 3 / 0 |
| 4 | 5 | 4 | 3 / **1** | 5 / 0 | 5 / 0 |
| 5 | 7 | 5 | 3 / **2** | 7 / 0 | 7 / 0 |
| 6 | 11 | 6 | 4 / **2** | 9 / **2** | 11 / 0 |
| 7 | 15 | 7 | 4 / **3** | 13 / **2** | 15 / 0 |
| 8 | 22 | 8 | 5 / **3** | 18 / **4** | 21 / **1** |
| 9 | 30 | 9 | 5 / **4** | 21 / **8** | 29 / **1** |
| 10 | 42 | 10 | 6 / **4** | 27 / **12** | 39 / **3** |
| 11 | 56 | 11 | 6 / **5** | 34 / **15** | 52 / **4** |
| 12 | 77 | 12 | 7 / **5** | 39 / **22** | 68 / **8** |

Shannon classes are grouped with a numerical tolerance and are approximate; the others are exact.

**The support is not uniformly poor at small `k`.** For the second-largest share, it begins at `k = 3`:

```
k = 3   2+1     C_D = 2/3          p_(2) = 1/3
        1+1+1   C_D = 1/3          p_(2) = 1/3      <- same S, different C_D

k = 4   3+1     C_D = 3/4          p_(2) = 1/4
        2+1+1   C_D = 1/2          p_(2) = 1/4
        1+1+1+1 C_D = 1/4          p_(2) = 1/4      <- three distinct C_D at one S
```

So the earlier claim that "a cell with `k ≤ 4` cannot separate `C_D` from `p_(2)`" was simply wrong, and
it is withdrawn.

**The support is competitor-specific and moves in opposite directions.** `p_(2)` is a weak summary — it
leaves the maximum free on `[p_(2), 1]` — so it leaves the most `C_D` variation. Shannon entropy is a rich
functional that very nearly separates shapes, so conditioning on it leaves almost none: at `k = 10` only
3 of 39 entropy classes contain more than one `C_D` value. Herfindahl sits between them.

Its one instructive failure is a coincidence worth recording, because it shows that no summary is a
one-to-one encoding of shape:

```
k = 8   4+1+1+1+1   C_D = 1/2   Shannon = ln 4
        2+2+2+2     C_D = 1/4   Shannon = ln 4
```

Three consequences, stated as design constraints rather than findings:

1. **Which competitors are predeclared materially determines the difficulty of the question.** A rich
   competitor makes level 2 nearly untestable at the population level, by construction. Selecting the
   comparator set is therefore a substantive scientific choice, not a formality, and changing it after
   seeing results is a search.
2. **Combinatorial support is not realised support.** The table counts shapes that *could* occur at each
   `k`; it says nothing about which `k` values the 150 solvers actually have, or how often each shape
   occurs. No solver has been evaluated, so the realised distribution is unknown.
3. **No power calculation exists**, and one cannot be produced without `σ_u` and `sd(C)`, neither of which
   is estimated anywhere. The table describes where the comparison is *identifiable*, not where it is
   *detectable*.

### 4.2 The subset framing that should not be used

It is tempting to say "compare `C_D` and `S` only on the shapes where they differ", since those are the
only informative rows. That is a subset defined by the observed shape distribution, and selecting it after
inspection converts a confirmatory comparison into a search over subsets. If such a restriction is used at
all it must be declared before evaluation, with the selection rule fixed and reported. Recorded here as a
rejected framing.

---

## 5. The claim ladder

Four levels, each with its own support requirement. The first is B1. The rest are not.

| Level | Claim | What would support it | Status |
|---|---|---|---|
| 1 | `C_D` improves held-out prediction over the exact-cell baseline | The existing B1 primary comparison | Frozen; not executed |
| 2 | The gain reflects something specific to the maximum share, rather than any shape summary | Predeclared per-competitor comparison on the equal-`S` support of §4.1, with the comparator set fixed and multiplicity handled | Not specified; competitor-dependent support, no power calculation |
| 3 | The gain depends on the prespecified semantic partition | A separately specified conditional partition-randomization procedure | Not specified; outside B1's frozen law, not shown impossible |
| 4 | The gain generalises to independently developed parents | A post-freeze bank under separate custody, plus a parent-population procedure | Explicitly refused by B1 v1.7 §5.7 V4 |

A positive level-1 result does **not** imply levels 2–4, and must never be reported as though it did.
A negative level-1 result makes levels 2–4 moot.

**The exact sentence level 1 licenses**, and the only form in which it may be reported:

> Within the observed parent set and on the fixed 78-record development bank, the maximum-share statistic
> improves leave-one-parent-out predictive log loss relative to the exact-cell baseline, under the
> prespecified conditional test.

It may not be shortened to "the statistic predicts correctness", and it does not establish a dominance
mechanism, the validity of the semantic partition, or generalisation to new parent implementations.

---

## 6. Parent-level consistency: what is settled and what is not

The review asked for parent consistency. Most of the machinery already exists.

| Element | Position |
|---|---|
| Per-parent paired differences `δ_g = L_{0,g} − L_{1,g}` | **Already mandatory** — B1 v1.7 §2 and §11(a) |
| Equal weight per scored parent | **Already mandatory** — §2, §3 item 4(a) |
| Coverage diagnostics per fold and per dataset | **Already mandatory** — §3 item 4(c), §11(e) |
| A parent-majority decision rule | **Not adopted, and not justified.** The confirmatory decision is the conditional randomization test, not a vote |
| Descriptive influence reporting (`δ_g` range, median, count positive/negative, leave-one-parent summary) | **Useful, unobjectified.** Should be declared before evaluation so it cannot become a post-hoc rescue |
| Minimum-coverage verdict gate with `NOT ASSESSABLE` | **Still missing.** Threshold remains an owner decision; no number is invented here |

The distinction that matters: reporting the `δ_g` distribution is **diagnostic**; requiring a fraction of
positive parents **is a different test** with different operating characteristics, and adopting it silently
would replace the predeclared inference. GPT's position — make the distribution visible, do not add an
arbitrary majority threshold — is adopted.

The conditional-target limit is unchanged: this is inference given the observed parents, not uncertainty
over a population of independently developed ones.

---

## 7. Disposition

- **B1 v1.7 is not modified.** No clause, threshold, fold, or estimability condition changes.
- **No extension is authorized.** Level 2 is recorded as unspecified and competitor-dependent; level 3 is
  recorded as outside B1's frozen resampling law — *not* as impossible to design, and not as inheriting
  B1's guarantees.
- **No threshold is invented**, including the coverage gate of §6.
- **The useful residue of the review is interpretive:** a positive level-1 result licenses the sentence of
  §5 and nothing shorter. That rule is ready to be adopted immediately and needs no new experiment.
- **Open for Claude and GLM on GPT's terms:** the §3.3 fork, the §3.4 checklist, and whether any
  predeclared comparator set leaves enough equal-`S` support to make level 2 worth specifying at all.
  The §4.1 table is the input to that decision, not an answer to it.
