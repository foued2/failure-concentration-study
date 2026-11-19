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
2. **Under the canonical exposure basis the operation is not even admissible as stated.** The frozen
   exposure vector is `R = (8,8,8,8,8,4,8,8)` — stratum 6 holds four canonical inputs, the rest hold
   eight. A name permutation that leaves `R` attached to positions produces a table in which
   `f_j ≤ R_j` can fail (a permuted `f` of 6 placed over `R_6 = 4`). Permuting `R` with the labels
   restores consistency and changes nothing. So the operation is either inert or ill-formed.
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

### 3.2 But the frozen machinery assumes the multiset is fixed

B1 v1.7 §5.2 defines the resampling unit as the *within-cell `C_D` label*, with the **within-cell `C_D`
multiset held fixed** under `H₀^perm`. Three guarantees are built on that:

| Guarantee | Frozen clause | Why it does not transfer |
|---|---|---|
| Audit equality | §5.3 step 1: the declared audit-equality key `A(b) = A(b_obs)` must be reproduced; a cell that becomes estimable makes the assignment inadmissible | `W_{C,c} = Σ(C_D − C̄_D)²` changes when the multiset changes, so estimability is draw-dependent |
| Permutation-invariant target population | §5.3 step 3 | Scored cells can differ across draws, so the "same rows, same folds" identity is lost |
| Super-uniformity conditional on the availability event | §5.7 V3, V5 | The conditioning event is defined over assignments that share a multiset |

Reallocation is therefore a **family of analyses with draw-dependent target populations**, not a
randomization test on a fixed population. Merging it into §5.3 would break the frozen identity between
observed statistic and null reference. GPT's instruction not to modify B1 v1.7 is well founded, and the
reason is stronger than "it is a different question": it is incompatible with the guarantee that makes
the current test valid.

### 3.3 The unresolved fork

If such a sensitivity is ever specified, it must first choose between two options, and neither is
currently decided:

| Option | Consequence |
|---|---|
| **A. Admissibility by design-only condition.** Declare in advance that a draw is admissible only if it preserves the observed estimability pattern | Keeps a fixed target population, but conditions on a `C_D`-configuration event, so the reference distribution is not the naive "random partition" law |
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
| Shannon entropy of shares | `−Σ p_j log p_j` (with `0 log 0 = 0`) | Decreasing in concentration; distinguishes all shapes in principle |
| Herfindahl / Simpson | `Σ p_j²` | Contains `C_D²` as a component; the quadratic penalty on the dominant share is the distinguishing feature |

**All three sit under the same information ceiling as `C_D`.** Each is `F`-measurable, so each obeys
`I(Y;S|X) ≤ I(Y;F|X)`. The comparison is about which scalar compression is better, never about beating
`F` (see the novelty register §3).

### 4.1 The estimability limit that governs the whole comparison

At fixed `k`, the number of distinct failure **shapes** is the number of integer partitions of `k` into at
most eight parts, and the number of distinct `C_D` values is at most `k`:

| `k` | Distinct shapes | Distinct `C_D` values (≤) |
|---|---|---|
| 3 | 3 | 3 |
| 4 | 5 | 4 |
| 5 | 7 | 5 |
| 6 | 11 | 6 |
| 7 | 15 | 7 |
| 8 | 22 | 8 |

The cell fixes `k`, so the comparison between `C_D` and its alternatives is **only identified where shapes
collide on the same `C_D` value**. The smallest example is `k = 5`:

```
shape 3+2     C_D = 3/5   p_(2) = 2/5   H = 13/25 = 0.520
shape 3+1+1   C_D = 3/5   p_(2) = 1/5   H = 11/25 = 0.440
```

Same `C_D`, different alternatives. Those collisions are the entire identifying variation for "dominance
versus another summary". Consequences, stated as design constraints rather than findings:

1. **Small-`k` cells carry almost no discrimination.** A cell with `k ≤ 4` cannot separate `C_D` from
   `p_(2)` at all in most shapes.
2. **The comparison is not equally estimable across the cell structure.** It concentrates in cells where
   `k` is large enough to admit many shapes — and those cells are also the ones where `C_D` is least
   variable near the top of its range.
3. **No power calculation exists for it**, and one cannot be produced without `σ_u` and `sd(C)`, neither
   of which is estimated anywhere.

### 4.2 A collision-free framing that should not be used

It is tempting to say "if `C_D` beats `p_(2)` and `H` in cells where they collide, dominance is
specific". That is a search over a small subset defined by the observed `k` distribution, and it must be
declared before evaluation or it is not confirmatory. Recorded here as a rejected framing.

---

## 5. The claim ladder

Four levels, each with its own support requirement. The first is B1. The rest are not.

| Level | Claim | What would support it | Status |
|---|---|---|---|
| 1 | `C_D` improves held-out prediction over the exact-cell baseline | The existing B1 primary comparison | Frozen; not executed |
| 2 | The gain reflects something specific to the maximum share, rather than any shape summary | Predeclared comparison against the §4 set, with collisions identified in advance and multiplicity handled | Not specified |
| 3 | The gain depends on the prespecified semantic partition | The §3 reallocation sensitivity, with the §3.3 fork resolved | Not specified; incompatible with §5.3 as written |
| 4 | The gain generalises to independently developed parents | A post-freeze bank under separate custody, plus a parent-population procedure | Explicitly refused by B1 v1.7 §5.7 V4 |

A positive level-1 result does **not** imply levels 2–4, and must never be reported as though it did.
A negative level-1 result makes levels 2–4 moot.

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
- **No extension is authorized.** Levels 2 and 3 are recorded as unspecified, and level 3 additionally as
  incompatible with §5.3 in its current form.
- **No threshold is invented**, including the coverage gate of §6.
- **The useful residue of the review is interpretive:** a positive level-1 result licenses "the
  maximum-share statistic predicts", not "dominance is what matters", and not "the partition is
  validated". That rule is ready to be adopted immediately and needs no new experiment.
- **Open for Claude and GLM on GPT's terms:** the §3.3 fork, the §3.4 checklist, and whether the §4
  collision analysis provides enough identifying variation to make level 2 worth specifying at all.
