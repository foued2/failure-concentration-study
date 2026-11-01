# PARENT_DESIGN.md — LC518 150-Body Construction Study

**Study package:** lc518-150
**Version:** 1.0 (FROZEN)
**Frozen by:** GLM
**Freeze date:** 2026-11-01
**Authorization:** GLM_WORK_ORDER.md v1.0 (commit `4608922ee08cc579c4bca5b7aef9465504269422`), header line 6: construction of exactly 150 source bodies and supporting design/package files is authorized; execution is not.
**Freeze attestation:** This document is frozen before any solver source file, input bank file, or oracle file exists. No solver body S001–S150 has been generated. No mutation has been assigned. The private mutation-design annex has not been received; per work order line 45, mutation assignment is blocked until it arrives.

---

## 1. Purpose and scope

This document defines the 30 parent implementations of the study population: 30 distinct
intended-correct solver bodies for Coin Change II (LC518_TASK_CONTRACT.md), organized into
five algorithm formulation families. Each parent will later be instantiated as five matched
versions (S0, SA, SB, SAB, S-extra) per work order §3, giving exactly 150 bodies.

What is frozen here: the parent roster (G01–G30), the family assignment, the per-parent
implementation tactic, the family-level correctness arguments, and the complexity analyses
under the full LC518 constraints (n ∈ [1, 300] coins, coin values ∈ [1, 5000] distinct,
amount ∈ [0, 5000], answer fits a signed 32-bit integer).

What is NOT decided here: mutation assignments, pair allocations, version roles, solver IDs
S001–S150 (assigned at construction, opaque, in a fixed unpublished permutation), and any
defect content. Those are governed by the owner's private annex.

## 2. Notation

- `A` — target amount (0 ≤ A ≤ 5000).
- `c_1, …, c_n` — the distinct coin denominations as given (input order is not guaranteed
  to be sorted; correctness must not depend on it).
- `W(a, S)` — the number of multisets over coin set S summing to exactly `a`. This is the
  required output: `change(amount, coins) = W(A, {c_1, …, c_n})`.
- Convention: `W(0, S) = 1` for every S (the empty combination), even S = ∅.
- `c_min` — smallest coin; `c_max` — largest coin.

Family-level facts used repeatedly:

- **(F-ORD)** Coin order is irrelevant to `W`: `W(a, S)` depends on S only as a set.
  Every family below processes coins in *some* fixed order; each such family is correct
  for every input order, including when a parent pre-sorts or reverses.
- **(F-INT)** The contract guarantees the final answer fits int32, but intermediate values
  (e.g., `W(a, S)` for `a < A`, or coefficients of partial products) are **not** bounded
  by that guarantee. Consequence: no parent may use fixed-width machine integers
  (`array('q')`, packed big-int digits, NumPy int64) for DP cells. All parents use Python
  `int` (arbitrary precision). This rejects a whole class of tempting implementations; see §7.

## 3. The five formulation families

The work order (line 39) requires "at least four genuinely distinct correct algorithmic
formulations" and forbids calling cosmetic rewrites different families. This design uses
**five** families whose state spaces, recurrences, traversal orders, and update semantics
genuinely differ. Parents within a family differ in implementation tactic (buffering,
data structure, traversal, normalization); they are labeled by family honestly and the
near-duplicate report (work order §11) will list them as same-family implementations.

| Family | Formulation | State | Recurrence (core) | Time | Space |
|---|---|---|---|---|---|
| K1 | Bottom-up 1-D coin-outer unbounded-knapsack counting | dp[0..A] over amounts | `dp[a] += dp[a − c]`, coin-outer, amount-ascending, in place | O(nA) | O(A) |
| K2 | Bottom-up 2-D coin-index × amount use/skip table | T[i][a], first i coins | `T[i][a] = T[i−1][a] + T[i][a − c_i]` | O(nA) | O(nA) or O(A) rolling |
| K3 | Top-down memoized exact counting over suffix sets | f(i, a), coins[i:] | `f(i, a) = f(i+1, a) + f(i, a − c_i)` | O(nA) | O(nA) memo + stack |
| K4 | Generating-function product: P(x) = ∏ (1 − x^c)^{−1}, truncated | coefficient array P[0..A] | per-coin series multiplication by geometric series | O(nA)–O(nA log A) | O(A) |
| K5 | Coin-set split with single Cauchy product | two half-products P_L, P_R | `W(A) = Σ_t P_L[t] · P_R[A − t]` | O(nA + A²) | O(A) |

Complexity figures count Python-level cell operations at full constraints
(n = 300, A = 5000); O(nA) ≈ 1.5 × 10^6.

### 3.1 Family K1 — 1-D coin-outer unbounded counting (7 parents: G01–G07)

**Algorithm.** `dp[0..A]`, `dp[0] = 1`, `dp[a>0] = 0`. For each coin `c` in a fixed order:
for `a = c` to `A` ascending: `dp[a] += dp[a − c]`. Output `dp[A]`.

**Correctness argument.** Invariant: after processing coin set S′ ⊆ S, `dp[a] = W(a, S′)`
for all a. Base: S′ = ∅ gives dp[0] = 1 and 0 elsewhere = W(·, ∅). Step: when coin c is
processed with the amount loop ascending, at cell a the value dp[a − c] has already been
updated in this same pass, hence equals W(a − c, S′ ∪ {c}); so dp[a] ← W(a, S′) + W(a − c, S′ ∪ {c}).
Partitioning the multisets of S′ ∪ {c} summing to a by the multiplicity of c (zero vs. at
least one) gives exactly W(a, S′) + W(a − c, S′ ∪ {c}); the ascending order is essential —
a descending amount loop would use pre-pass values and yield 0/1-knapsack semantics (each
coin used at most once), which is the canonical wrong answer for this task. Coin order is
immaterial by (F-ORD). Input order is handled by (F-ORD) for parents that do not sort, and
trivially by sorting for parents that do. Amount 0 returns dp[0] = 1 without entering any
loop (every c ≥ 1 > 0 = A), matching the contract.

**Complexity.** Time O(nA). Space O(A). Designed performance risk: none material.

**Rejected tactic inside K1 (documented, not used):** slice/bulk forms such as
`dp[c:] = [x + y for x, y in zip(dp[c:], dp)]` evaluate all right-hand values pre-pass,
which silently degrades to 0/1-knapsack semantics. Any parent using it would be
intended-wrong; none is used.

| Parent | Tactic (distinct implementation) | Notes |
|---|---|---|
| G01 | K1-canonical: coins in given (unsorted) order; plain list; no filtering | Reference tactic for the family |
| G02 | K1-sorted-asc: `sorted(coins)` then canonical loop | Pre-sorting normalization; correctness by (F-ORD) |
| G03 | K1-sparse-dict: dp as dict keyed by amount, `.get` defaults; ascending amount pass | Sparse structure; unvisited cells stay absent |
| G04 | K1-filtered-while: coins filtered to `c ≤ amount` preserving given order; `while`-loop updates; early return 1 when amount == 0 | Guard-clause tactic; filtering is result-preserving (coins > A cannot appear in any multiset summing to A) |
| G05 | K1-sorted-desc: coins sorted descending, canonical ascending-amount update | Reversed processing order; distinct execution trace |
| G06 | K1-double-buffer: per coin, `cur = prev.copy()`; `cur[a] += cur[a − c]` ascending; swap | Two-buffer semantics: `cur[a − c]` is same-pass value, `prev[a]` is pre-coin value; algebraically identical update, structurally different memory discipline |
| G07 | K1-bisect-cutoff: coins sorted ascending; `bisect_right` locates prefix ≤ A; loop over prefix only; if prefix empty return 1 if A == 0 else 0 | Adds a search element and an explicit empty-prefix branch |

### 3.2 Family K2 — 2-D coin-index × amount use/skip table (8 parents: G08–G15)

**Algorithm (prefix form).** `T[i][a]` = number of multisets over the first i coins
(c_1..c_i) summing to a. `T[0][0] = 1`, `T[0][a>0] = 0`. For i = 1..n, a = 0..A:
`T[i][a] = T[i−1][a] + (a ≥ c_i ? T[i][a − c_i] : 0)`. Output `T[n][A]`.

**Correctness argument.** Induction on i. Multisets over c_1..c_i summing to a either do
not use c_i (counted by T[i−1][a]) or use it at least once; removing one c_i is a bijection
to multisets over c_1..c_i summing to a − c_i (counted by T[i][a − c_i]). The "same-index"
lookback is what encodes unlimited reuse; the use/skip decomposition counts each multiset
exactly once by construction, so no ordering artifacts arise. The base row encodes
W(0, ∅) = 1. Amount 0 yields T[n][0] = 1 for every n. Coin order affects only which
decomposition path is taken, not the count ((F-ORD) + the bijection is order-symmetric).
Input order: parents either use the given order or normalize by sorting; both correct.

**Complexity.** Time O(nA). Space O(nA) for full-table tactics (≈ 1.5 × 10^6 cells) or
O(A) for rolling-row tactics. **Designed memory risk (full-table parents):** with large
counts held as distinct Python ints, resident memory can reach the several-hundred-MB
range on worst-case inputs. No runtime or memory budget is declared by this study
(contract line 55; work order §8), so this is recorded as a designed risk only, never as
an observed timeout.

| Parent | Tactic | Space | Notes |
|---|---|---|---|
| G08 | K2-full-table: list-of-lists, rows i = 0..n, row-wise fill | O(nA) | Reference tactic |
| G09 | K2-rolling-rows: two rows prev/cur, `cur[a] = prev[a] + cur[a − c_i]`, swap per coin | O(A) | Classic rolling reduction |
| G10 | K2-column-major: amount-outer (a ascending), index-inner fill on the full table | O(nA) | Distinct traversal order; same recurrence |
| G11 | K2-suffix-indexed: coins reversed (descending); T[i][a] = multisets over coins[i:]; fill i descending; `T[i][a] = T[i+1][a] + T[i][a − c_i]`; output T[0][A] | O(nA) | Mirror formulation ("largest part first" reading) |
| G12 | K2-dict-rows: per-index rows as sparse dicts with `.get` defaults | O(nA) worst | Sparse-row tactic |
| G13 | K2-flat-stride: single flat list of (n+1)(A+1) cells, manual stride `i*(A+1)+a` | O(nA) | Explicit memory-layout arithmetic |
| G14 | K2-row-builder: per coin, `cur = prev[:]` then in-row ascending extension `cur[a] += cur[a − c_i]` from a = c_i | O(nA) | Copy-then-extend discipline (vs. G09's swap) |
| G15 | K2-skip-compression: coins sorted ascending; coins > A contribute identity rows (row copied forward: T[i][a] = T[i−1][a]) | O(nA) worst | Skip-equivalence lemma: a coin > A never appears in a multiset summing to A, so its use/skip row reduces to the copy |

### 3.3 Family K3 — top-down memoized exact counting (8 parents: G16–G23)

**Algorithm (suffix form).** f(i, a) = number of multisets over coins[i:] summing to a.
Base: f(i, 0) = 1 for all i; f(i, a>0) = 0 when i = n. Recursion:
`f(i, a) = f(i+1, a) + (a ≥ c_i ? f(i, a − c_i) : 0)`. Output f(0, A). Memoize on (i, a).

**Correctness argument.** Same use/skip bijection as K2, run top-down over the suffix
chain: multisets over coins[i:] either avoid c_i (f(i+1, a)) or contain one c_i plus a
multiset over coins[i:] summing to a − c_i. Memoization is sound because f(i, a) is a pure
function of (i, a). Termination: the skip branch strictly increases i; the use branch
strictly decreases a by c_i ≥ 1; both strictly decrease a + (n − i) · (A + 1) — a bounded
measure. Input order: parents using the given order are correct by (F-ORD); sorting
parents likewise.

**Recursion-depth analysis (applies to all recursive K3 parents).** Along any root-to-leaf
path, skip branches number at most n, and consecutive use branches along one coin index
number at most ⌊A / c_i⌋ ≤ A / c_min. Hence maximum depth ≤ n + ⌊A / c_min⌋ + 1 ≤ 300 +
5000 + 1 = 5301 frames. Python's default recursion limit (1000) is far below this, so
every recursive K3 parent **must** raise the recursion limit to a documented bound
(depth_bound + margin) or use the explicit-stack tactic. Parents that failed to do this
would be intended-wrong (systematic RecursionError); all recursive parents here set
`sys.setrecursionlimit(depth_bound + 200)` with the derivation recorded. The explicit-stack
parent (G18) has no recursion-limit dependence at all.

**Complexity.** O(nA) memoized states, O(1) transition each; memo O(nA); stack O(depth).

| Parent | Tactic | Notes |
|---|---|---|
| G16 | K3-lru-usefirst: `functools.lru_cache(maxsize=None)`; branch order (use, skip); coins as given | Reference tactic |
| G17 | K3-dict-skipfirst: explicit dict memo; branch order (skip, use); coins as given | Memo type + branch order both differ from G16 |
| G18 | K3-explicit-stack: iterative post-order DFS with explicit frames (i, a, phase, accumulator); no Python recursion | Distinct control flow; no recursion-limit dependence |
| G19 | K3-flat-memo: memo as flat list of size (n+1)(A+1) initialized to sentinel −1; key `i*(A+1)+a`; coins sorted ascending | Array-backed memo |
| G20 | K3-desc-largestfirst: coins sorted descending; suffix recursion reads "largest part first"; lru_cache; branch (use, skip) | Natural partition-by-largest-part reading |
| G21 | K3-asc-smallestfirst: coins sorted ascending; suffix recursion; dict memo; branch (skip, use) | Mirror of G20 with different memo + branch order |
| G22 | K3-bisect-prune: coins sorted ascending; at each call, `bisect_left` advances i past all coins > a (skip-run compaction); dict memo | Adds search-based pruning; reduces effective branching |
| G23 | K3-lru-asc-bounded: coins sorted ascending; lru_cache; branch (use, skip); recursion limit set from the explicit depth derivation above | Depth-bound derivation is the distinguishing element |

### 3.4 Family K4 — generating-function product (5 parents: G24–G28)

**Formulation.** The answer is the coefficient of x^A in
P(x) = ∏_{i=1..n} (1 − x^{c_i})^{−1}, truncated at degree A. Each factor is the geometric
series 1 + x^{c_i} + x^{2c_i} + …, so multiplying P by the i-th factor maps coefficient
array P to P′ with P′[a] = Σ_{t ≥ 0, a − t·c_i ≥ 0} P[a − t·c_i]. Starting from
P = [1, 0, 0, …] (the empty product) and multiplying all n factors yields
P[A] = W(A, S). Three update schedules are used (all compute the same per-coin series
multiplication):

1. **Doubling schedule.** Uses the formal identity
   (1 − x^c)^{−1} = ∏_{j ≥ 0} (1 + x^{2^j c}). Per coin: k = ⌈log2(A/c)⌉ + 1 passes;
   pass j does `for a = A down to 2^j·c: S[a] += S[a − 2^j·c]` (descending order
   guarantees each pass uses pre-pass values, i.e., true multiplication by
   (1 + x^{2^j c})). Correctness: every multiplicity t ≤ A/c has a unique binary
   expansion, so the product of the doubling factors is exactly the truncated geometric
   series. A coin with c > A contributes nothing (identity on the truncation) and is
   skipped.
2. **Residue-chain schedule.** Per coin c and residue r ∈ [0, c−1]: walk
   a = r, r+c, r+2c, … ascending with running accumulator `acc += P_old[a]; new[a] = acc`.
   Then new[a] = Σ_{t≥0} P_old[a − t·c]. Fresh output buffer per coin.
3. **Sparse-dict schedule.** Schedule 1 with the polynomial held as a dict
   {degree: coefficient}; shifts become key arithmetic; zero coefficients never stored.

**Correctness argument.** The generating-function identity is standard: expanding
∏ (1 − x^{c})^{−1}, the coefficient of x^a counts exactly the multisets with repetition
numbers (t_1, …, t_n), Σ t_i c_i = a — i.e., W(a, S). Truncation at degree A is sound
because all series have non-negative exponents, so higher-degree terms cannot influence
lower degrees. Each schedule implements the same per-coin multiplication: (1) via the
binary-expansion identity, (2) via direct summation along residue classes, (3) as (1) on
a sparse carrier. Coin order is immaterial (commutative product). Honest derivational
note: schedule 2's running-accumulator form, new[a] = P[a] + new[a − c], coincides
algebraically with K1's update on a fresh buffer; the family's claim to distinct
formulation rests on the multiplicity-indexed derivation and on schedules 1 and 3, which
have genuinely different pass structure. This is stated so the family-diversity claim is
not overstated (work order line 39 discipline).

**Complexity.** Doubling: O(n · A · log2(A / c_min)) ≈ 2 × 10^7 cell operations worst
case — feasible but the heaviest K1–K4 workload; recorded as a moderate designed
performance risk. Residue-chain: O(nA). Space O(A) (or sparse occupancy).

| Parent | Tactic | Notes |
|---|---|---|
| G24 | K4-doubling: schedule 1, coins as given | Reference tactic |
| G25 | K4-doubling-desc: schedule 1, coins sorted descending, c > A skipped | Ordering + guard variant |
| G26 | K4-residue-chains: schedule 2, coins as given | Chain-walk structure |
| G27 | K4-residue-chains-sorted: schedule 2, coins sorted ascending, c > A filtered | Ordering + guard variant |
| G28 | K4-doubling-sparse: schedule 3 (dict carrier) | Sparse carrier variant |

### 3.5 Family K5 — coin-set split with single Cauchy product (2 parents: G29–G30)

**Formulation.** Partition the coin set into two halves L and R (fixed rule per parent).
Compute P_L = ∏_{c ∈ L} (1 − x^c)^{−1} and P_R = ∏_{c ∈ R} (1 − x^c)^{−1}, each truncated
at degree A (each half-product built by the fresh-buffer ascending per-coin update). Then
W(A, S) = Σ_{t=0}^{A} P_L[t] · P_R[A − t] — the Cauchy product identity for coefficients.

**Correctness argument.** The full product P = P_L · P_R over the disjoint coin sets, and
coefficients of a product of two series satisfy P[a] = Σ_t P_L[t] P_R[a − t] by definition
of series multiplication. The half-products are correct by the K4 per-coin argument.
Edge cases: an empty half (n = 1) is the identity series P[0] = 1, P[a>0] = 0, and the
identity convolution returns the other half's coefficient unchanged. Truncation soundness
as in K4.

**Complexity.** O(nA) for both half-products plus O((A+1)²) ≈ 2.5 × 10^7 operations for
the final Cauchy product at A = 5000. **Designed performance risk:** the quadratic final
convolution is the single heaviest step in the population; recorded per contract line 55
discipline as a designed risk, never as an observed timeout.

| Parent | Tactic | Notes |
|---|---|---|
| G29 | K5-split-given: split by given-order index (first ⌈n/2⌉ vs. rest) | Reference tactic |
| G30 | K5-split-sorted: split after sorting ascending (small/large halves) | Sorting + split-rule variant |

## 4. Parent roster summary

| Group | Parent | Family | One-line identity |
|---|---|---|---|
| 1 | G01 | K1 | canonical 1-D coin-outer, given order |
| 2 | G02 | K1 | 1-D, coins sorted ascending |
| 3 | G03 | K1 | 1-D, sparse dict cells |
| 4 | G04 | K1 | 1-D, filtered coins + while-loop |
| 5 | G05 | K1 | 1-D, coins sorted descending |
| 6 | G06 | K1 | 1-D, double-buffer per coin |
| 7 | G07 | K1 | 1-D, bisect cutoff prefix |
| 8 | G08 | K2 | full table, row-wise |
| 9 | G09 | K2 | rolling two rows |
| 10 | G10 | K2 | full table, amount-outer fill |
| 11 | G11 | K2 | suffix-indexed mirror table |
| 12 | G12 | K2 | sparse dict rows |
| 13 | G13 | K2 | flat list with stride arithmetic |
| 14 | G14 | K2 | copy-then-extend row builder |
| 15 | G15 | K2 | sorted coins, skip-row compression |
| 16 | G16 | K3 | lru_cache top-down, use-first, given order |
| 17 | G17 | K3 | dict memo top-down, skip-first |
| 18 | G18 | K3 | explicit-stack iterative DFS |
| 19 | G19 | K3 | flat-array memo, sorted coins |
| 20 | G20 | K3 | largest-part-first suffix recursion |
| 21 | G21 | K3 | smallest-part-first suffix recursion, dict memo |
| 22 | G22 | K3 | bisect skip-run compaction |
| 23 | G23 | K3 | lru top-down, explicit depth-bound |
| 24 | G24 | K4 | geometric doubling, given order |
| 25 | G25 | K4 | geometric doubling, descending coins |
| 26 | G26 | K4 | residue-chain accumulation |
| 27 | G27 | K4 | residue-chain, sorted coins |
| 28 | G28 | K4 | doubling on sparse dict carrier |
| 29 | G29 | K5 | split + Cauchy product, given-order split |
| 30 | G30 | K5 | split + Cauchy product, sorted split |

Family counts: K1 × 7, K2 × 8, K3 × 8, K4 × 5, K5 × 2 = 30. Five genuinely distinct
formulations (§3) satisfy the "at least four" requirement with margin, so the claim does
not hinge on K4's schedule-2 derivational caveat alone.

## 5. Correctness-of-parent caveat (work order §12 discipline)

Every parent here is *intended-correct*: it carries a written argument, not a verification.
Static inspection cannot establish that an intended-correct parent is actually correct over
the full domain (work order line 202). Whether each parent in fact agrees with the study
oracles on the frozen banks is a property established only in the later, separately
authorized execution phase, and it will be reported as observed behavior — never
retro-fitted into this design. Parents are not currently executed, imported, or compared
against anything; the only permitted source checks are AST parsing and syntax compilation
without execution (work order §12).

## 6. Interface and environment conformance (contract §4)

All 30 parents will expose exactly `class Solution` with
`change(self, amount: int, coins: list[int]) -> int`, return exact `int` (never `bool`),
perform no printing, no imports beyond the standard-library pieces named in their tactics
(`functools`, `sys`, `bisect`), no network, no file reads. Input lists are treated as
read-only (the harness supplies a fresh copy; any input mutation would be recorded
separately by the harness, and no parent mutates its input by design). Source comments
will describe algorithms only — never mutation identities, version roles, or
study-internal labels (work order §3).

## 7. Rejected whole-class tactics (pre-registered rationale)

1. **Fixed-width integer cells** (`array('q')`, packed big-int digits, NumPy int64):
   unsound because intermediate counts are not bounded by the int32 guarantee (§2, F-INT).
2. **Slice-assignment bulk K1 updates**: 0/1-knapsack semantics (§3.1) — intended-wrong.
3. **Recursive K3 without recursion-limit management or explicit stack**: systematic
   RecursionError at depth up to 5301 (§3.3) — intended-wrong under default limits.
4. **Exhaustive multiplicity enumeration as a parent**: correct but factorial-scale;
   reserved for the oracle's small-input cross-check domain only (contract §6).
5. **Greedy or floating-point counting**: not exact; excluded by the correctness predicate.

## 8. Pending inputs owned by others (not invented here)

1. The eight-mechanism taxonomy and pair-allocation schedule (owner's private annex) —
   required before any mutation is assigned (work order line 45) and before any solver
   source is written, because the two replicated pairs must be preselected before source
   construction (work order line 47).
2. Per-family mutation-compatibility report (work order §11): requires the taxonomy; will
   be produced at construction time and marked DESIGNED_NOT_VERIFIED.
3. Execution protocol pinning interpreter version, runtime and memory budgets: prerequisite
   to any timeout/resource classification (contract line 55) and to the reserved feature
   columns (work order §10).

## 9. Freeze record

- Frozen content: §1–§8 above.
- Excluded from freeze by design: solver IDs S001–S150 mapping, parent-group → body
  assignment, all mutation content (annex-gated).
- Any later change to this document requires a new version header and a stated reason;
  silent edits are prohibited by the study's own freeze discipline (work order §5).
