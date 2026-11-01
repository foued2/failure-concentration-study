# CORRECTIONS_RECORD_v1.1.md — LC518 150-Body Construction Study

**Study package:** lc518-150
**Version:** 1.1 (DRAFT FOR REVIEW — not yet accepted; draft amended 2026-11-01 per GPT's stated conditions — changelog at end)
**Prepared by:** GLM
**Date:** 2026-11-01
**Authorization scope (owner, 2026-11-01):** preparation of a corrected specification ONLY. This record does NOT authorize generating the 150 solver bodies, executing anything, or pushing any commit.
**Status of v1.0 documents:** UNCHANGED and UNTOUCHED. Byte-identical to pushed commit `3e9a29c9652a6ab4f6bab0919e386757280b2654`:
- `PARENT_DESIGN.md` sha256 `c6138342af84fe02a64390c2f6a7f4077f0268aa875ad90ee534c76a725f3437`
- `BANK_DESIGN.md` sha256 `da7f8c1ae3c5e3a582c38d91be2463061bce2acb0a772fac72d34459f4b17843`
- `ANALYSIS_SPEC.md` sha256 `fb24910cc7712c7e9e27753084ad3683d1fd422a20d875b0b5a4ca33a55f4e78`

Each correction below quotes the v1.0 text verbatim (file, line numbers), states the defect, gives exact replacement text, and a justification. Review chain per owner: Claude challenges this record line-by-line → GPT final scientific review → owner accepts → only then construction (still gated on the private annex, work order :45/:47).

---

## C1 — G22 algorithm description incoherent (PARENT_DESIGN §3.3 :170, §4 :271)

**v1.0 text (:170):**
> `| G22 | K3-bisect-prune: coins sorted ascending; at each call, bisect_left advances i past all coins > a (skip-run compaction); dict memo | Adds search-based pruning; reduces effective branching |`

**Defect.** In an ascending suffix recursion over `coins[i:]`, coins `> a` occupy the TAIL of the suffix. `bisect_left(coins, a+1) = j` bounds the usable PREFIX `[0, j)`; "advancing i past all coins > a" would advance `i` over the smallest coins and retain the oversized tail — the opposite of the stated purpose. Confirmed independently by GPT, Claude, and GLM (Claude initially could not reach the text; later verified directly).

**Replacement text (exact, for §3.3 parent table and expanded in a new §3.3.1):**

> **G22 — K3-desc-firstusable-prune.** Coins sorted **descending** `c_1 ≥ c_2 ≥ … ≥ c_n` (0-indexed `c[0] ≥ … ≥ c[n−1]`). Suffix recursion as in family K3: `f(i, a) = f(i+1, a) + (a ≥ c_i ? f(i, a − c_i) : 0)`, `f(i, 0) = 1`, `f(n, a>0) = 0`, dict memo. Before transitioning at any state `(i, a)` with `a > 0`, the index is compacted to `i' = max(i, u(a))`, where `u(a)` is the **precomputed first usable index**: `u(a) = min{ i : c_i ≤ a }`, `u(a) = n` if none. `f(i, a) = f(i', a)`; recursion proceeds from `i'` only.
>
> **Precomputation.** `u(a)` for `a = 1..A` by two pointers: `j = 0`; `for a in 1..A: while j < n and c[j] > a: j += 1; u[a] = j`. Cost O(n + A) (each index advanced once), plus O(n log n) for the descending sort. Equivalent one-shot derivation: with `d = (−c_1, …, −c_n)` ascending, `u(a) = bisect_left(d, −a)` (GPT's formulation), evaluated per amount during precomputation rather than per memoized state.
>
> **Compaction lemma.** For `a > 0` and `i ≤ u(a)`: `f(i, a) = f(u(a), a)`. Proof: descending order gives `c_j > a` for all `j < u(a)` (else `u(a)` smaller). At any such `j`, the use branch requires `a ≥ c_j` — false — so `f(j, a) = f(j+1, a)` (skip only). Chaining over `j = i, …, u(a)−1` gives the claim. Since the use branch strictly decreases `a`, every deeper state `(i'', a'')` reachable from `(u(a), a)` has `a'' ≤ a`, hence `c_j > a ≥ a''` for `j < u(a)` remains dead at all deeper states: no usable coin is ever skipped. ∎
>
> **Boundary conditions.** `f(i, 0) = 1` for all `i` (empty multiset; checked before compaction — compaction is defined only for `a > 0`). `f(n, a>0) = 0`. If `max(i, u(a)) = n` and `a > 0`, return 0 (suffix exhausted, amount unmet). Termination measure unchanged from §3.3 (`a + (n−i)(A+1)` strictly decreases).
>
> **Recursion depth (GPT's condition 1).** G22 remains a top-down recursive algorithm — no explicit stack — so it inherits the family K3 mandate (§3.3 :153–158) in full: `sys.setrecursionlimit(depth_bound + 200)` with `depth_bound = n + ⌊A/c_min⌋ + 1 ≤ 5301`, derivation recorded in the source header. Compaction shortens skip chains and reduces realized depth, but the declared worst-case bound is unchanged and the limit mandate is not waived by the pruning.
>
> **Complexity.** Reachable memo keys after compaction have `i`-coordinates in `{u(a) : a} ∪ {n}` — at most `min(n, A) + 1` values — so states ≤ O(min(n,A)·A) ⊆ O(nA). Each state costs O(1) (compaction is a table lookup). Total: **O(n log n + n + A + nA) = O(nA)** time, O(nA) memo + O(A) table + O(depth) stack. The per-state-bisect alternative `O(nA log n)` (GPT's objection) is avoided by the O(A) precomputation.
>
> **Near-duplicate disclosure (work order §11 discipline; corrected per Claude's review, re-ranked per GPT's condition 2).** PRINCIPAL affinity: **G20** (descending-order suffix recursion, largest-part-first reading, lru_cache). The corrected G22 is best understood as an optimization of the G20 approach — the threshold precomputation `u(a)` is a data-structural accelerator for exactly G20's traversal — and the near-duplicate report will present it as such, same-family K3. SECONDARY affinity (separate explanation, as GPT requires): **G17** shares only the sparse dict memo carrier; it differs from G22 in sort normalization (given order vs descending), branch mechanics (skip-first vs compacted use/skip), and has no compaction — G22 is not principally a G17 derivative and will not be described as one. The v1.0 text's apparent affinity to **G21** (ascending, dict memo) was an artifact of the defective description and lapses with this correction.

Also apply to §4 roster (:271): `| 22 | G22 | K3 | descending coins, precomputed first-usable-index compaction, dict memo |`

**Justification.** GPT's remedy (precompute per amount, O(1) per state) adopted; per-state bisect rejected on his complexity objection. Claude's pair correction adopted: disclosure names G20/G17 for the corrected design, with the G21 relation of the v1.0 text recorded as an artifact. No correctness impact on any other parent (G07 `:101` prunes against fixed `A` over a coin-outer loop and is sound; G15 `:134` likewise).

---

## C2 — K5 final-step complexity and risk ranking (PARENT_DESIGN §3 table :64, §3.5 :236–239)

**v1.0 text (:236–239):**
> `**Complexity.** O(nA) for both half-products plus O((A+1)²) ≈ 2.5 × 10⁷ operations for the final Cauchy product at A = 5000. **Designed performance risk:** the quadratic final convolution is the single heaviest step in the population; recorded per contract line 55 discipline as a designed risk, never as an observed timeout.`

**Defect.** The formulation itself (:227) computes only the target coefficient `W(A,S) = Σ_{t=0}^{A} P_L[t]·P_R[A−t]` — one dot product of two length-(A+1) arrays. Cost O(A) ≈ 5 × 10³, not O(A²) ≈ 2.5 × 10⁷. Confirmed by GPT and Claude; GLM concurs (own error).

**Replacement text (exact):**
> `**Complexity.** O(nA) for both half-products plus O(A) ≈ 5 × 10³ operations for the final coefficient (one dot product Σ_{t=0}^{A} P_L[t]·P_R[A−t]; the full convolution array is never formed). **Designed performance risk:** none material; the K5 parents are among the lightest in the population. The heaviest declared workload in the population is the K4 doubling schedule, O(n · A · log2(A / c_min)) ≈ 2 × 10⁷ cell operations (§3.4), which therefore carries the population's principal designed performance risk, recorded per contract line 55 discipline, never as an observed timeout.`

Also apply to the §3 family table (:64): change `O(nA + A²)` to `O(nA + A)`.

**Justification.** Algebra per GPT; consequence per GPT §1: K4-doubling becomes the computationally demanding formulation. No correctness claim changes.

---

## C3 — E1 matched contrasts: two-view reporting with pattern-enumerated bounds (ANALYSIS_SPEC §3 :48–68)

**v1.0 text (:51–54):**
> `All five versions of a parent use identical held-out records, identical oracle outputs, and identical execution conditions (work order §9). Because unresolved records are neither pass nor fail, L is reported on the resolved subset with coverage, together with worst/best bounds over unresolved records (worst: all unresolved are FAIL; best: all are PASS). No unresolved record is silently counted either way.`

**Defect.** "Reported on the resolved subset" implies per-version denominators; resolved subsets can differ across versions, so contrasts are not strictly matched. The per-input interaction (:65–68) is undefined where any of the four versions is unresolved, with no aggregation rule. Confirmed by GPT; adopted.

**Replacement text (exact, replaces :51–54 and extends :63–72):**
> All five versions of a parent use identical held-out records, identical oracle outputs, and identical execution conditions (work order §9). Unresolved records are never counted as pass or fail. Two pre-declared reporting views are used; neither is constructed after seeing outcomes.
>
> **View 1 — complete-case matched estimates.** For each contrast, let `C(g)` be the set of held-out records resolved by **every** version entering that contrast (2 versions for the A-only, B-only and S-extra contrasts; 4 versions for the pair contrast). The contrast-specific definition is PRIMARY — it maximizes matched coverage per contrast (GPT's question answered). The alternative single all-five convention is also computed and reported descriptively: `C₅(g) = ∩ of all five versions' resolved sets`, with `|C₅(g)|/80` beside it; both coverages appear in every table so the two conventions are never confused. The matched estimate of each contrast is computed on `C(g)` only, and `|C(g)|/80` is reported beside it. Per version, `L(g, v)` is additionally reported descriptively as the resolved-subset rate with its own coverage — descriptive only, never contrasted against a different version's denominator.
>
> **View 2 — full-bank bounds with unresolved retained as unknown.** Over all 80 records, unresolved outcomes are retained as unknown and bounded by enumerating the outcome patterns consistent with the resolved components, per record.
>
> For the per-input interaction `i(g, A, B, x) = loss(SAB,x) − loss(SA,x) − loss(SB,x) + loss(S0,x)`: each loss ∈ {0, 1}, hence `i ∈ {−2, −1, 0, 1, 2}` (GPT: max 2 = SAB fails, S0/SA/SB pass; min −2 = SAB passes, S0/SA/SB fail). For a record where all four versions resolve, `i(x)` is determined. Where `k` of the four are unresolved, `i(x)` ranges over the `2^k` patterns assigning PASS/FAIL to the unresolved components with the resolved components fixed. `k` is the PER-INPUT count of unresolved outcomes among the four versions, `k ≤ 4`, hence at most 16 patterns per input (GPT's clarification adopted); enumeration of all unresolved assignments across the entire 80-input bank is explicitly NOT performed. The record contributes the interval `[min i, max i]` over those patterns. Aggregate bounds: `I_min = Σ_x min-pattern i(x)`, `I_max = Σ_x max-pattern i(x)`, reported with the per-version and common coverage. Bounds are computed **per record by pattern enumeration**, never by independently combining four version-level averages, which would ignore that the unresolved records are the same matched records across versions and produce incorrect joint bounds. The full per-input distribution (determined records) and the list of undetermined records with their intervals are reported; the cancellation rule (:70–72) is unchanged.

**Justification.** Preserves matching (GPT's two-view structure); bounds are exact over the binary outcome model; Claude's confirmation of the {−2,…,2} range is recorded.

---

## C4 — Deviation features: fixed zero sentinel + defined indicator (ANALYSIS_SPEC §4 :93–94)

**v1.0 text (:93–94):**
> `| d_meandev_s | mean of |returned − expected| over wrong integer outputs in s; NaN + defined=False when undefined |`
> `| d_maxdev_s | max of |returned − expected| over wrong integer outputs in s; NaN + defined=False when undefined |`

**Defect.** NaN values enter a ridge design matrix with no specified treatment. Confirmed by GPT and Claude.

**Replacement text (exact):**
> `| d_meandev_s | mean of |returned − expected| over wrong integer outputs in s; **0 when undefined** (no wrong integer outputs in s), with companion indicator d_meandev_s_defined = False |`
> `| d_maxdev_s | max of |returned − expected| over wrong integer outputs in s; **0 when undefined**, with companion indicator d_maxdev_s_defined = False |`

**Justification.** A wrong integer output has `|returned − expected| ≥ 1`, so 0 is never a genuine deviation value (GPT): the sentinel is out-of-domain by construction and unambiguous, avoiding fold-specific imputation. The indicator columns carry the missingness; ridge absorbs the collinearity. Standardization remains fitted on training data only, inside every fold (:140–141 unchanged). No imputation is "fitted" because none is needed — the sentinel is fixed before any data exists.

---

## C5 — `other` failure-manifestation count added (ANALYSIS_SPEC §4 :86–94)

**v1.0 context.** §2 (:32–34) permits manifestations "wrong answer, invalid return type, exception, timeout/resource breach, other explicitly defined status"; the §4 table counts only wrong answer / invalid return / exception (+ unresolved coverage).

**Defect (GPT, detail 1).** A permitted manifestation class has no feature column; the enriched arm would be blind to it while the typed record retains it.

**Replacement text (exact):** add row after `d_exception_s`:
> `| d_other_s | count of FAIL records in s whose typed manifestation is classified other (explicitly defined status, excluding timeout/resource, which remain reserved columns until the execution protocol exists) |`

**Justification.** Keeps the feature table coextensive with the typed-record taxonomy of §2. If `other` never occurs, the column is constant 0; after fold-fitted standardization a constant column is 0 with a well-defined zero coefficient — harmless, and the column is reported rather than dropped (consistent with :101–102).

---

## C6 — `d_order_inconsistent` defined and added to the enriched arm (ANALYSIS_SPEC §4, §6 :131–134; BANK_DESIGN §6 :136–138)

**v1.0 text (BANK_DESIGN :136–137):**
> `The D6 permutation pairs are diagnostic-only instruments for the order-invariance feature (ANALYSIS_SPEC.md §4, d_order_inconsistent).`

**Defect.** The referenced feature does not exist anywhere in ANALYSIS_SPEC v1.0 (table :86–94, aggregates :96–98, enriched arm :131–134). Confirmed by GPT and Claude.

**Replacement text (exact; amended per GPT's comparability condition):** add three rows to the §4 table:
> `| d_order_pairs_resolved | count of D6 canonical pairs (of 4) where BOTH orderings resolved (status PASS or FAIL, any manifestation) |`
> `| d_order_pairs_comparable | count of D6 canonical pairs where both executions resolved AND both returned comparable values — exact int return values (PASS, or FAIL with a wrong-integer output). Pairs where either execution ended in invalid return type or exception have no comparable value and are excluded here while remaining visible in d_order_pairs_resolved |`
> `| d_order_inconsistent | count of D6 canonical pairs, among the comparable pairs, whose two returned integer values differ. Value-based only |`

**Justification.** GPT's comparability condition adopted: a FAIL does not imply a comparable return value exists (invalid return type and exception leave no integer to compare), so the inconsistency count is restricted to comparable pairs — the only well-defined value comparison — with the evaluation count recorded separately at two levels (resolved, comparable). Correctness and order invariance remain separate measurements: status outcomes feed the correctness features of §4; `d_order_inconsistent` is purely value-based. A correct solver is order-invariant by (F-ORD), so any value difference on one canonical instance is diagnostic signal; identical wrong values under both orderings count as consistent (an order-invariant bug) — stated so the feature is not over-read. Enriched arm (:131–134) is amended to include all three columns alongside the per-stratum columns. BANK_DESIGN's cross-reference becomes true.

---

## C7 — `coverage_diag`: definition written, excluded from both arms (ANALYSIS_SPEC §4 :96–98, §6 :130)

**v1.0 text (:96–98):**
> `Aggregate baseline columns: k_fail (total diagnostic FAIL count), k_unresolved (total diagnostic UNRESOLVED count), family (parent algorithm family Z from PARENT_DESIGN.md §4 — prespecified context variable), coverage_diag.`
**v1.0 text (:130):**
> `- **Baseline arm:** ridge regression on k_fail, k_unresolved, family.`

**Defect.** Column list and arm specification disagree (GPT's extra point 1; Claude's "partly right" resolved in GPT's favour on line-by-line reading).

**Replacement text (exact):**
> `Aggregate columns: k_fail, k_unresolved, family, coverage_diag, where coverage_diag = (resolved diagnostic records)/64 = 1 − k_unresolved/64 per solver (Coverage definition of §2 applied to the 64-record diagnostic bank).`
> `- **Baseline arm:** ridge regression on k_fail, k_unresolved, family. coverage_diag is REPORTED but EXCLUDED as a predictor in both arms: it is an affine function of k_unresolved (1 − k_unresolved/64) and would add no information while duplicating a column (GPT).`

**Justification.** GPT's identity holds under the §2 coverage definition; exclusion is pre-declared before any data exists. Reporting keeps coverage_diag visible (§7 rule 1).

---

## C8 — E3 target under unresolved held-out outcomes: OWNER DECISION SLOT (ANALYSIS_SPEC §6, with §5 :116–119)

**v1.0 gap.** §5 defines Q and its unresolved-case reporting (Q_resolved + coverage + bounds), but §6 never states which target the E3 regression fits.

**Options (written before any data exists, per GPT and Claude):**
- **Option 1 (GPT — strict).** E3 proceeds only if all 150 bodies have complete, resolved held-out outcomes on all 80 records; otherwise E3 = `NOT_ESTIMABLE` with the precise reason, and unresolved counts + Q bounds are reported descriptively. Pro: single well-defined target Q for every body; no subset scoring. Con (Claude): timeout classification needs an execution protocol that does not yet exist, so unresolved counts are unknown and Option 1 may be NOT_ESTIMABLE by construction.
- **Option 2 (Claude — threshold).** Pre-declare a maximum unresolved fraction τ (e.g., 0.025 = 2/80 per body); E3 proceeds only if every body is at or under τ. Requires a target definition for bodies with unresolved records — which reintroduces either subset scoring (rejected by GPT) or a convention that §5 currently forbids (counting unresolved as wrong). Any threshold rule must also specify the target exactly, before data.
- **Option 3 (Claude — descriptive only).** E3 is declared descriptive-only from the outset: no baseline-vs-enriched model comparison is fitted; the §4 features and Q outcomes are reported descriptively. Removes the estimand entirely; nothing to gate.

**GLM recommendation:** Option 1, for one reason: it is the only option whose target is exactly the preregistered Q with no redefinition, and an honest `NOT_ESTIMABLE` is an acceptable outcome for an exploratory secondary estimand (§6 item 9 already provides the machinery). The descriptive fallback under Option 1 is exactly Option 3's content, so nothing is lost.

**STATUS: OPEN — OWNER DECIDES BEFORE ANY DATA EXISTS OR THE ANNEX OPENS.** No default is applied; until the owner decides, E3 has no runnable target specification. (Claude's addition adopted: the decision is scheduled before the annex, as step 5 of the agreed sequence.)

---

## C9 — Bank generation pinned to byte-reproducibility (BANK_DESIGN §4 :62–79)

**v1.0 text (:62–64):**
> `- Generator: Python 3.11+ random.Random (to be pinned exactly by the execution protocol before any solver execution; bank regeneration is deterministic under the pinned interpreter).`

**Defect (GPT, finding F).** Seeds + ranges + guards do not fully determine the sampling process: within-range distributions, per-record draw order, distinctness handling, and redraw RNG consumption are unspecified; seed re-derivation could not reproduce the banks byte-for-byte.

**Replacement text (exact, added to §4):**
> Sampling conventions (pinned before any bank file exists):
> 1. Every range in §5/§6 is inclusive and sampled uniformly: `[lo, hi]` via `rng.randrange(lo, hi + 1)`.
> 2. Per-record field draw order is fixed: `amount`, then `n`, then the `n` coins (each coin a fresh uniform draw from the stratum's coin range; distinctness enforced by redraw of colliding coins only — a collision redraw consumes exactly one RNG call per attempt).
> 3. Stratum-specific constructions (H7 gcd/min-coin zero-answer construction, H8 small-set anchoring, D6 permutation generation by Fisher–Yates under the same generator) consume the same single RNG stream in stratum order D1→D8 / H1→H8, records in generation order.
> 4. int32-guard redraw (:70–74) redraws the ENTIRE record — the same RNG calls a fresh candidate would consume — and logs the redraw count per record.
> 5. The generator script itself is a frozen artifact: at bank generation it is hash-recorded (sha256) and published beside the bank files. Byte-reproducibility claim = frozen script + frozen seeds (:65–66) + pinned interpreter; the bank JSON files remain the authoritative artifacts (:78–79).
> 6. The interpreter pin is required before bank GENERATION (not only before solver execution): bank generation does not start until the execution protocol names the exact interpreter version.

**Justification.** Makes the re-derivation cross-check (:78–79) actually performable; ties bank freeze to the protocol pin so no regeneration ambiguity can arise. Legal under the freeze discipline: no bank file exists yet, and BANK_DESIGN §9 (:172–174) contemplates versioned correction before outcomes.

---

## Consistency matrix and effect summary

| Correction | File touched | v1.0 lines | Other sections affected |
|---|---|---|---|
| C1 G22 | PARENT_DESIGN | :170, :271 | §11 near-duplicate report (construction time) |
| C2 K5 | PARENT_DESIGN | :64, :236–239 | §3.4 risk note becomes population-max (no text change needed) |
| C3 E1 | ANALYSIS_SPEC | :51–54, :63–68 | §7 rule 1 reporting unchanged |
| C4 dev sentinel | ANALYSIS_SPEC | :93–94 | :131–134 arm list unchanged (indicators already listed) |
| C5 other count | ANALYSIS_SPEC | :86–94 | reserved timeout columns :100–102 unchanged |
| C6 order feature | ANALYSIS_SPEC (+BANK_DESIGN xref) | :131–134 | BANK_DESIGN :136–137 becomes consistent |
| C7 coverage_diag | ANALYSIS_SPEC | :96–98, :130 | §7 rule 1 unchanged |
| C8 E3 target | ANALYSIS_SPEC | §6 | §5 unchanged; item 9 machinery reused |
| C9 bank pinning | BANK_DESIGN | :62–64 | §9 :168–170 satisfied earlier |

**Explicit non-authorizations (owner, 2026-11-01):** no solver bodies (0/150), no execution, no commits, no pushes. v1.0 documents remain byte-frozen as the historical reference; this record is the sole correction instrument until the review chain completes.

**Open owner decisions (none blocking the Claude → GPT review of this record):**
1. C8: E3 unresolved rule — Option 1 / 2 / 3 (needed before the annex opens, not before this review).
2. Second-commit push of the updated worklog snapshot (entries 30–37) to the handoff branch — per work order :217.
3. GitHub token disposition — recommendation to revoke stands on record (GPT, Claude, GLM); owner's standing instruction is to keep it; GLM acts on the owner's word only.

---

## Changelog of the draft

- **2026-11-01, initial draft (v1.1-draft):** C1–C9 as issued. sha256 `083cd85a1bfb9abd7afc9f7e19b34cdc8d0cdd61a7592816be2f3479aaa462ae`.
- **2026-11-01, amendment (v1.1.1-draft), responding to GPT's conditions:** C1 + explicit recursion-limit mandate (G22 stays top-down; §3.3 :153–158 inherited verbatim — depth bound ≤ 5301, setrecursionlimit required); C1 near-duplicate re-ranked — PRINCIPAL G20 ("threshold precomputation is an optimization of that approach"), G17 secondary with separate explanation, G21 affinity recorded as v1.0 artifact. C3 + `2^k` clarified as per-input (k ≤ 4, ≤ 16 patterns per input; bank-wide enumeration excluded) + both complete-case conventions stated (contrast-specific `C(g)` primary; all-five `C₅(g)` descriptive). C6 + comparability distinction (FAIL does not imply a comparable integer): three columns — resolved / comparable / value-based inconsistent; correctness and order invariance separated.
