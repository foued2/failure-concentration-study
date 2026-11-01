# BANK_DESIGN.md — LC518 150-Body Construction Study

**Study package:** lc518-150
**Version:** 1.0 (FROZEN)
**Frozen by:** GLM
**Freeze date:** 2026-11-01
**Authorization:** GLM_WORK_ORDER.md v1.0 (commit `4608922`), §5 item 1 and §6.
**Freeze attestation:** This document is frozen before any solver source exists and before
any bank file is generated. The bank JSON files it specifies are mechanical consequences of
the rules below (fixed seeds, fixed construction rules, fixed rejection guards); they will
be generated, hash-recorded, and frozen as files in the next construction step, before any
mutation is applied. No test case may be added, removed, or re-weighted after candidate
outcomes have been observed (work order §5).

---

## 1. Purpose

Two disjoint, valid LC518 input banks:

- **Diagnostic bank** — characterizes observable solver behaviour; supplies the candidate
  enriched features for the secondary analysis (work order §10).
- **Held-out bank** — measures correctness on inputs not used to construct diagnostic
  features; defines the finite target distribution for Q and for all matched contrasts
  (work order §9).

The same banks and the same oracle outputs are used for all 150 bodies. Banks are frozen
before solver-body construction. Every input satisfies the full LC518 contract domain
(n ∈ [1, 300]; coins distinct, ∈ [1, 5000]; amount ∈ [0, 5000]; oracle-verified answer
fits a signed 32-bit integer). Invalid-input behaviour is outside the study contract
(contract §3).

## 2. Canonical identity rule (work order line 79)

An instance's canonical identity is `(amount, tuple(sorted(coins)))`. Consequences:

1. All permutations of one mathematical instance share one canonical identity.
2. Permutation copies are permitted **within** one bank (as separate input records with
   the same canonical identity), to test order invariance.
3. No canonical identity may appear in both banks. Disjointness is enforced over
   canonical identities, not over raw records.

A machine check — `canonical(diagnostic) ∩ canonical(held-out) = ∅`, plus within-bank
canonical-collision accounting — runs at file freeze and is reported in the
static-validation report. The check is part of acceptance criterion 5 (work order §15).

## 3. Bank sizes and the no-power statement

- **Diagnostic bank: 64 input records** (8 strata × 8 records; stratum D6 consists of
  4 canonical instances × 2 orderings).
- **Held-out bank: 80 input records** (8 strata; stratum H6 contains 2 canonical
  instances × 2 orderings = 4 records plus 6 singletons).

Sizes are chosen for **declared structural coverage**, not for statistical power. No
sample-size calculation, power simulation, or minimum-detectable-effect claim is made or
authorized (work order line 66: previous power figures remain invalidated; this phase is
an exploratory construction screen). Any statement of the form "N inputs give X% power"
is out of scope by construction.

## 4. Deterministic generation

- Generator: Python 3.11+ `random.Random` (to be pinned exactly by the execution
  protocol before any solver execution; bank regeneration is deterministic under the
  pinned interpreter).
- Seeds: `SEED_HELDOUT = 20261101`, `SEED_DIAGNOSTIC = 11052026`. Seeded generators are
  created independently per bank; record order follows generation order.
- Every record carries: `input_id`, `amount`, `coins` (as-given order), `canonical_id`,
  `stratum`, `rule_id`, `rule_params`, and a `record_sha256` computed over the canonical
  JSON serialization of the record at file freeze.
- **int32 guard:** at generation time, the primary oracle computes the answer for every
  candidate record; any candidate whose answer exceeds 2,147,483,647 is rejected and the
  generator re-draws (deterministically, under the same seed stream). The guard outcome
  per record (accepted / redrawn k times) is logged in the bank file. This implements the
  contract's guarantee rather than assuming it.
- **Validity guard:** each record is asserted against §1 constraints; assertion failures
  abort bank generation (they would indicate a generator bug, not a study finding).

The bank JSON files are the authoritative artifacts; re-derivation from seeds is a
verification cross-check only.

## 5. Held-out bank: strata, counts, weights

The held-out bank defines a finite, explicit target distribution. Weights are record
counts / 80 (uniform over records). All conclusions about correctness generalize **only**
to this declared distribution — not to all LeetCode submissions, not to all possible
LC518 inputs (contract §7; work order §6).

| Stratum | Records | Weight | Construction rule (rule_id) | Coverage mandate served |
|---|---|---|---|---|
| H1 tiny-amount | 12 | 0.150 | amount ∈ [0, 12]; n ∈ [1, 4]; coins ∈ [1, 20]; ≥ 3 records with amount = 0 or 1 (H1-EDGE) | amount zero; boundary amounts; repeated use of small denominations |
| H2 small-amount | 12 | 0.150 | amount ∈ [13, 60]; n ∈ [2, 6]; coins ∈ [1, 60]; ≥ 4 records contain coin 1 | multiple distinct combinations; repeated use |
| H3 single-coin | 8 | 0.100 | n = 1; amount ∈ [0, 5000]; coin ∈ [1, 50] | exact denomination match; divisibility structure; unreachable-by-divisibility cases |
| H4 two-coin | 8 | 0.100 | n = 2; amount ∈ [20, 5000]; coins ∈ [1, 5000] | two-denomination interaction-free counts; exact matches with distractors |
| H5 many-coins | 10 | 0.125 | n ∈ [30, 120]; amount ∈ [100, 2000]; coins ∈ [1, 5000], distinct | varied denomination counts; order effects under wide sets |
| H6 large-amount | 10 | 0.125 | amount ∈ [3500, 5000]; n ∈ [5, 40]; 6 singletons + 2 canonical instances × 2 orderings (H6-REORDER) | large amounts; **reordered coin arrays** on held-out ground |
| H7 unreachable | 8 | 0.100 | constructed so the oracle answer is exactly 0: min-coin > amount, or all coins share g ≥ 2 with g ∤ amount (H7-ZERO) | unreachable amounts |
| H8 rich-combination | 12 | 0.150 | coins include {1, 2, 3} or {1, 3, 4}-type small sets; amount ∈ [6, 800]; subject to the int32 guard | multiple distinct combinations; **non-greedy counterexample families**; repeated use |
| **Total** | **80** | 1.000 | | |

Notes on the coverage mandates (work order line 78 list):

- **Amount zero:** H1 (≥ 3 records) — answer must be 1.
- **Exact denomination match:** H3 by construction; H2/H4 rules include match amounts.
- **Unreachable amounts:** H7 (answer 0 verified by oracle at generation).
- **Repeated use of a denomination:** any record whose answer exceeds the number of
  distinct multisets using each coin at most once — the oracle verifies that at least one
  selected record per stratum H1–H4 has a combination requiring repetition (e.g., amount
  > sum of distinct coins, or a coin appearing with multiplicity ≥ 2 in some optimal
  multiset). Verified at generation; logged.
- **Multiple distinct combinations:** H2, H8 (oracle answer ≥ 2 verified and logged).
- **Non-greedy counterexamples:** H8 families include {1, 3, 4}-type sets at amounts where
  largest-first choice diverges from combination structure (e.g., amount 6 with {1,3,4}).
- **Varied denomination counts:** H5 (n up to 120) vs. H3 (n = 1).
- **Large amounts:** H6 (up to 5000).
- **Reordered coin arrays:** D6 (diagnostic) and H6-REORDER (held-out); see §6/§7.

## 6. Diagnostic bank: strata and counts

The diagnostic bank exists to make solver behaviour observable and to supply the
predeclared feature columns of ANALYSIS_SPEC.md §4. Strata are **predeclared**: feature
columns are defined per stratum below, and no stratum may be added, split, or merged after
candidate outcomes are observed (work order §10).

| Stratum | Records | Construction rule (rule_id) | Diagnostic purpose |
|---|---|---|---|
| D1 boundary-amount | 8 | amount ∈ {0, 1, 2, c_min − 1, c_min, c_min + 1, 2·c_min, 2·c_min + 1} pattern over small coin sets | boundary handling; off-by-one surfaces |
| D2 exact-match | 8 | amount equals one denomination; 1–4 distractor coins | match-vs-miss discrimination |
| D3 unreachable | 8 | min-coin > amount, or gcd-structured sets with g ∤ amount; oracle answer 0 | zero-answer behaviour; "empty result" handling |
| D4 modular-parity | 8 | odd-coin sets at even/odd amounts; sets with coin gcd 2 at odd amounts | modular reasoning surfaces |
| D5 non-greedy | 8 | {1, 3, 4}-type sets at divergent amounts (e.g., 6, 10); largest-first intuition fails | classic greedy-trap detection |
| D6 reorder-pairs | 8 | 4 canonical instances × 2 orderings (instance + its permutation, adjacent input_ids) | **order invariance**: does the same solver return the same answer under permutation? |
| D7 wide-n | 8 | n ∈ [50, 300]; amount ∈ [50, 500]; coins ∈ [1, 5000] | scale in n; iteration over many coins |
| D8 large-amount | 8 | amount ∈ [2000, 5000]; n ∈ [3, 30] | scale in amount; depth/space pressure |
| **Total** | **64** | | |

The D6 permutation pairs are diagnostic-only instruments for the order-invariance feature
(ANALYSIS_SPEC.md §4, `d_order_inconsistent`). Permutation records share a canonical id;
the canonical-disjointness check of §2 applies unchanged.

## 7. Bank separation guarantees

1. **Canonical disjointness** (§2) — machine-checked at freeze.
2. **No cross-bank leakage via generation:** the two seeded generators are independent;
   H-strata and D-strata rules draw from disjoint parameter spaces by construction, and
   the canonical check is the backstop, not the only defense.
3. **Oracle outputs are computed once per canonical instance** and attached to every
   record of that instance (both orderings where applicable); oracle output files are
   hash-referenced from the bank files.
4. **Feature firewall:** diagnostic features are functions of diagnostic-bank records
   only. Held-out records, held-out outcomes, and held-out oracle outputs enter no
   feature definition (work order §10; ANALYSIS_SPEC.md §6).

## 8. What the banks do not claim

- They are not a sample of natural LeetCode submissions, nor a representative sample of
  all LC518 inputs (work order §1; contract §7).
- They do not support power or generalization claims; the target distribution is the
  80-record held-out list, declared above, nothing more.
- The int32 guard makes the banks valid under the contract's guarantee; it is not a
  claim that all int32-satisfiable inputs are covered.

## 9. Freeze record

- Frozen content: §1–§8 (sizes, strata, rules, seeds, guards, identity rule, weights).
- Generated later, mechanically, from this design: `diagnostic_bank.json`,
  `heldout_bank.json`, oracle-output attachments, canonical-disjointness report,
  per-record hashes. Their hashes are the file-level freeze.
- Pending external inputs: the pinned execution protocol (interpreter version) is
  required before regeneration cross-checks and before any solver execution; it does not
  affect this design's content.
- Any change to strata, counts, seeds, rules, or weights after candidate outcomes are
  observed is prohibited (work order §5). If a defect is found in the generator, the
  banks are regenerated from the corrected rule set with a new version header and the
  incident is reported to the owner before any candidate construction continues.
