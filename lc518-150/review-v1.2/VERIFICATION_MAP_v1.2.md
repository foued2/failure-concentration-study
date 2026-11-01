# VERIFICATION_MAP_v1.2.md — reading map for Claude's line-challenge of CORRECTIONS_RECORD v1.2-draft

**Status:** navigational aid ONLY — not part of the correction record, not authoritative.
The authoritative text is `CORRECTIONS_RECORD_v1.2-draft.md` in this directory.
**Prepared by:** GLM, 2026-11-01, at the owner's review-chain step "Claude challenges these exact changes → GPT re-reviews".
**Authorization:** unchanged — text preparation and editorial verification only. No solver bodies (0/150), no execution, no commits, no pushes.

---

## 0. Delivery facts (why the draft was "not found in the repository")

- The v1.2 draft has **never been committed or pushed** — no authorization covers it. It exists only in this delivery directory; the owner forwards it. This is why Claude's repo/branch search came up empty.
- **Hash chain (document control per GPT's requirement):**
  | Version state | sha256 | Bytes | Where |
  |---|---|---|---|
  | v1.1-draft (entry 37) | `083cd85a1bfb9abd7afc9f7e19b34cdc8d0cdd61a7592816be2f3479aaa462ae` | 21,985 | changelog record |
  | v1.1.1-draft (entry 38, reviewed by GPT round 3) | `663193006fa3c94a8601eee4b6ac2ed499b0443c342da71914fc572e68d9c78f` | 25,034 | `CORRECTIONS_RECORD_v1.1.md` on disk |
  | v1.2-draft at issue (entry 39; GPT round 4 saw its size/verification report only) | `c97c95e0b80d154997b8ba2be1b0fddc5f1e6125593d4d92af8dcb26be32b08e` | 51,903 | archived byte-identically: `archive/superseded-CORRECTIONS_RECORD_v1.2-draft.entry39-issue-sha256c97c95e0.md` |
  | **v1.2-draft CURRENT (review this one)** | **`120b385c31906afb7ade11eeacc346b5e07f28cc2b15583e5af1417650ca1214`** | **60,796** | `CORRECTIONS_RECORD_v1.2-draft.md` |
- The entry-39 issue was amended BEFORE first full-text delivery (GLM self-check; details §3 below). GPT's quoted "51,903-byte document" therefore refers to the archived bytes, not the current file. The version identifier stays `1.2-draft` (single identifier, supersession documented in the Changelog :299–300).
- Frozen v1.0 trio re-verified unchanged this round: `PARENT_DESIGN.md` `c6138342…`, `BANK_DESIGN.md` `da7f8c1a…`, `ANALYSIS_SPEC.md` `fb24910c…`.

## 1. Where each verification target lives (line numbers = CURRENT file)

### G22 / C1 (:33–77) — state-count proof, not just the loop
| Ask (GPT round 4 / Claude) | Where | What is claimed |
|---|---|---|
| Corrected descending-amount loop | :46–54 | amounts iterate A→1, forward-only pointer; O(n+A); worked example [5,3,1] at :55–59; bisect equivalence at :61 (3,000 randomized trials incl. duplicates, entry-39) |
| Compaction lemma | :63 | f(i,a) = f(u(a),a) for i ≤ u(a), with no-usable-coin-skipped argument |
| Memoization order / amount-zero convention | :65 | pinned order: a=0 returns 1 **before any memo interaction** (never memoized); then compaction → lookup → store; f(n, a>0) = 0 |
| State-count proof | :67 | every memoized key has a ≥ 1 and (i < n ⇒ i ≥ u(a) ⇒ c_i ≤ a ≤ A), so i ∈ {j : c_j ≤ A} ∪ {n} |
| "Skip transitions create no index values outside the set" (GPT's stated obligation) | :67, bolded paragraph | skip successor (i+1, a) re-compacts to i+1 (> u(a)) and c_{i+1} ≤ c_i ≤ a ≤ A; use branch re-enters (i, a−c_i) with u(a−c_i) ≥ u(a). Membership holds for ANY descending list via compaction-at-entry; GPT's u(c_i) = i formulation is subsumed; distinctness is used ONLY for the count |
| Distinctness premise: explicit + counterexample (Claude's ask) | :67 | premise cited to BANK_DESIGN :29 (mirror of LC518's official "all values of coins are unique"); adversarial trace: 40×coin-1, A=1 memoizes (k,1), k = 0…40 → 41 keys, 41 distinct index values vs min(n,A)+1 = 2; set-characterization counterexample: c=[3,3,1], A=3 → key (1,3) outside {u(a)} ∪ {n} = {0,2,3} |
| Tighter bound actually demonstrated | :67 + :71 | counting argument + 4,000-trial simulation (0 violations under distinctness); degraded (n+1)·A bound stated for duplicates |
| Correctness scope | :67, final bold | value-correctness claimed ONLY for distinct denominations (the contract); duplicate behaviour out of contract, not claimed — "valid for arbitrary positive denominations" was an overclaim and is withdrawn (see §3) |
| Complexity without collapse | :71 | O(n log n + nA + A); A=0 → O(1); memo ≤ (min(n,A)+1)·A |
| Recursion-depth mandate | :69 | K3 mandate §3.3 :150–158 inherited; depth_bound ≤ 5301 |

**Suggested independent checks for Claude:** (a) rerun the [5,3,1] table; (b) verify the skip-successor step by hand from the pinned order (:65); (c) recompute the 40×coin-1 trace; (d) attack the claim that membership needs no distinctness while the count does.

### C3 (:97–128) — every contrast and bound
| Ask | Where | What is claimed |
|---|---|---|
| Extremal patterns + uniqueness | :114–121 | max +2 uniquely at losses (S0,SA,SB,SAB) = (1,0,0,1); min −2 uniquely at (0,1,1,0); v1.1.1's ±1 examples withdrawn |
| Per-input unresolved machinery | :123 | k ≤ 2 (≤4 completions) singles; k ≤ 4 (≤16) interaction; resolved components fixed; NO whole-bank enumeration |
| Same procedure for all four contrasts | :112, :123 | Δ_A, Δ_B, Δ_S-extra (d = loss(v₁) − loss(v₀), v₀ = S0) and I(g,A,B) |
| 1/80 aggregate scale | :125–126 | Δ(g), I(g,A,B), and all four bounds carry (1/80)Σ |
| Single-contrast closed form | :126 | **case-conditioned form** (corrected pre-delivery, see §3): m_max = 1 iff S0-side ∈ {res-PASS, UNRES} AND patched-side ∈ {res-FAIL, UNRES}; m_min mirrored; on both-resolved records the record contributes d(x) |
| Two-view separation | :110 | complete-case C(g) per contrast (primary) + all-five C₅ descriptive; conditional-mean normalization pinned; never mixed with the 1/80 bounds |
| Complete-case and full-bank bounds both visible | :108–126 | View 1 and View 2 both pre-declared |

**Suggested independent checks:** (a) re-enumerate the 16 loss patterns; (b) verify the corrected closed form against hand enumeration on a 3-record toy containing one S0-resolved-FAIL + patched-unresolved record (true max contribution 0); (c) verify both defect cases from §3 below.

### C9 (:215–268) — every stratum, RNG, serialization
| Ask | Where |
|---|---|
| Uniform inclusive ranges, width ≥ 2, no degenerate calls | item 1, :231 |
| Per-stratum draw order consistent with dependencies (D1's c_min) | item 2, :233 |
| 16 strata construction algorithms (D1–D8 :239–246, H1–H8 :247–254) with forced records, rejection conditions, consumption rules | item 3 table |
| General redraw discipline + 1,000-attempt cap + instance-level guard for permutation pairs (BANK_DESIGN §7.3) | item 3 preamble, :235 |
| Repetition-mandate predicate pinned EXACTLY (oracle_answer > N₀; "e.g." demoted to illustration) | item 3a, :256 |
| Two independent streams (rng_diag 11052026 / rng_hold 20261101), global consumption order, method whitelist | item 4, :258 |
| Canonical JSON: sort_keys, separators, ensure_ascii, allow_nan, UTF-8, integer grammar, no floats, record_sha256 EXCLUDED from payload, JSONL + "\n" incl. final line, sidecar | item 5, :260 |
| Script freeze / interpreter pin / cross-bank disjointness | items 6–8, :262–266 |

### D6 feature definitions (C6, :163–177) and the rest
- C6 three rows + count/denominator addendum: :170–175 (rate null at zero denominator, never imputed).
- C4 zero sentinel + zero-variance rule: :140–146. C5 other-count + zero-variance rule: :156–159.
- C7 coverage_diag exclusion: :190–192. C2 K5 dot-product: :88–91.
- C8 owner decision slot (untouched): :198–211. Consistency matrix: :272–284. Changelog: :295–300.

## 2. What GLM's verification actually did (receipts)

- Entry-39 script `scripts/verify_v12_math.py` (u-table 3,000 trials; 16-pattern extremes; state-count premise 20,000 draws; D1 magnitude).
- **Entry-40 script `scripts/verify_v12_predelivery.py`** (this round, ALL CHECKS PASSED):
  - A1/A2/A3: corrected C3 closed form vs TRUE per-record enumeration — exhaustive over all 9 status pairs, 20,000 randomized 80-record banks, 0 mismatches; the withdrawn form mismatches in 20,000/20,000 randomized banks (it almost always contains ≥1 defect-case record).
  - B1: G22 value-correctness vs brute force, 2,000 in-contract (distinct-coin) trials, 0 mismatches; memo invariant (a ≥ 1; i ≥ u(a) or i = n) over 4,000 trials incl. duplicates, 0 violations.
  - B2: min(n,A)+1 index-count bound, 4,000 distinct-coin trials, 0 violations.
  - B3: 40×coin-1 → 41 memoized keys / 41 distinct index values vs bound 2; B3b: [3,3,1] → key (1,3) outside the threshold set.
  - C1/C2: D4 defect (t=(3,6) → gcd 6) and the corrected gcd(t)=1 acceptance (2,000/2000 give coin gcd exactly 2).
  - C4: N₀ predicate DP on toy records ({1,3,4}: amount 6 → answer 4, N₀ = 0 → repeated-use satisfied).
  - C5: **42 allowed D5 coin sets** (coin 1 + subset of [2,9], incl. {1,2,3}, {1,2,4}) where greedy coin count = minimum coin count for EVERY amount in [5,30] → the redraw cap is load-bearing.
  - C6: static width audit of 52 pinned randrange call sites — all widths ≥ 2 after the D3/H7 c_min=2 repair.
- Scope discipline: editorial verification only — no solver bodies, no bank generation (no seeded bank reproduction), no pipeline execution, no repo writes.

## 3. Pre-delivery amendments vs the entry-39 issue (what changed and why)

| # | Defect found in the entry-39 bytes | Evidence | Fix in the current text |
|---|---|---|---|
| 1 | C3 single-contrast closed form added |{x : ≥1 unresolved}| unconditionally — over-counts when S0 resolved-FAIL & patched unresolved, or patched resolved-PASS & S0 unresolved (true max 0, not 1) | Deterministic demos + 20,000-bank Monte-Carlo (mismatch 20,000/20,000); the entry-39 cross-check shared the same assumption in its enumeration harness, so it reported 0 mismatches — shared-assumption bug, owned | Case-conditioned m_max/m_min form at :126; withdrawal + ownership note in place; Changelog :300 |
| 2 | "G22 is valid for arbitrary positive denominations" — overclaim: the suffix recursion counts position-combinations under duplicate values (out of LC518 contract) | Value mismatches appear ONLY in duplicate-coin trials; LC518's official constraints guarantee unique coin values (mirrored by BANK_DESIGN :29) | Correctness scoped to the contract at :67 (final bold); duplicates exercised only for the invariant/count claims |
| 3 | Distinctness counterexample asserted but trace not in the document | — | Full trace + the [3,3,1] set-characterization counterexample at :67 (Claude's ask 2) |
| 4 | Skip-successor step implicit (GPT's stated proof obligation) | — | Explicit paragraph at :67 |
| 5 | D1 "amount = PATTERN[k]" indexing ambiguous (k 1-based vs 0-based list) | — | Records 1–8 → PATTERN in order, mapping spelled out; pattern_index = k−1 (:239) |
| 6 | D3/H7 `randrange(1, c_min)` has width 1 when c_min = 2 — violates the draft's own item 1 | Width computation + audit (C3/C6 checks) | c_min = 2 ⇒ amount = 1 deterministic, no RNG (:241, :253) |
| 7 | D4 "FIRST t forced odd" does NOT give coin gcd 2 (frozen :129 declares gcd 2) | t = (3, 6) → coins (6, 12), gcd 6 | gcd(t) = 1 acceptance check with whole-t-set redraw; D4 amount draws pinned to randrange(0,5001)+parity rejection (:242) |
| 8 | D5 divergence redraw can loop forever on canonical sets | 42 allowed sets (e.g. {1,2,3}, {1,2,4}) never diverge on [5,30] | Item-3 general redraw cap (1,000 attempts → abort as generator bug), declared load-bearing (:235, :243) |
| 9 | Pipeline (e) cross-referenced a nonexistent "item 3c-failsafe"; per-record vs per-stratum mandate staging blurred | — | (e) rewritten (:235); repetition mandate isolated in item 3a with the predicate pinned EXACTLY as oracle_answer > N₀ (:256) |
| 10 | H8 rule_params anchor as JSON array violated item 5's int/str/bool schema | — | Anchor pinned as string "1-2-3"/"1-3-4" (:254); H8 answer≥2 wording tightened |
| 11 | Permutation-pair oracle/guard granularity unstated vs BANK_DESIGN §7.3 | — | Instance-level oracle computation and guard verdict pinned in item 3 preamble (:235) |

All eleven are disclosed in the Changelog :300. None of them touches C2/C4/C5/C6/C7/C8 (accepted or open as before).

## 4. Pointers into the frozen v1.0 documents (for citation checking)

- BANK_DESIGN: :29 contract (n ∈ [1,300]; coins distinct ∈ [1,5000]; amount ∈ [0,5000]; int32); :43–45 canonical check; :62–79 generation/seeds/fields/guards; :90–97 H-strata; :102–115 coverage mandates (repetition :105–109, answer≥2 :110); :126–133 D-strata (D1 pattern :126, D4 gcd-2 :129); :136–138 D6/feature xref; §7.3 :146–148 oracle-once-per-instance.
- PARENT_DESIGN: :150–158 K3 recursion-depth mandate (5301); :170 G22 v1.0 row; :271 §4 roster row.
- ANALYSIS_SPEC: :48 L definition; :51–54 v1.0 reporting text; :56–61 four contrasts; :63–68 per-input interaction + loss; :70–72 cancellation; :86–94 feature table; :96–98 aggregates; :116–119 Q + unresolved; :130–134 arms; :140–141 fold-fitted standardization.

## 5. What remains open (unchanged)

1. Claude's line-challenge of THIS text → GPT re-review → owner decisions.
2. C8 E3 rule: Option 1 / 2 / 3 — owner decides before the annex opens (GPT and GLM both recommend Option 1; recommendation is not authorization).
3. Second-commit push of the worklog snapshot (entries 30–40) to the handoff branch — needs the owner's written approval, as would any commit/push of this draft.
4. Token disposition — standing owner instruction "NO REVOKE KEEP IT" remains in force; GLM acts on the owner's word only.
5. Construction 0/150; the mutation-design annex (eight mechanisms + 28 pair assignments) still not received — all solver source remains gated (work order :45/:47).
