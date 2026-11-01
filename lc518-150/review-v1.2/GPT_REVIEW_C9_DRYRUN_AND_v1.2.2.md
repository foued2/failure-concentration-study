# GPT independent review: Claude C9 dry run and v1.2.2 draft

**Date:** 2026-11-01  
**Status:** review artifact; not an accepted specification and not authorization to generate banks.

## Repository provenance inspected

- Claude dry-run branch: `review/lc518-c9-dryrun-claude-2026-11-01`
- Claude branch head: `922af5a383d9ffec4a86b441c84ecaff0df56b19`
- GPT review base: `fa310c0f8dae1c6d3a58456fbb723df3a602bd85`
- GPT v1.2.2 branch: `gpt/lc518-150-v1.2.2-c9-corrections-2026-11-01`
- v1.2.1 source document blob: `559c14c20f3fab554623712176382e2b856f2764`
- Claude report blob: `e7228c89e4b9fd7f7aa4ac9fa11e140fdd5b9711`
- Claude generator blob: `34e391ada87c39b00457adcc375cced9e1ded12a`
- Commit `286157b94cf8f28726bb7f53a0063b3e647a9b08` put the stray report on master. A subsequent master commit `b01b160e64190b27897e6461ed8226cafc3df67b` adds `reviews/AI_REVIEW_2026-11-01.md`, so 286157b is not the current master tip. GPT made no writes to master; no deletion or history rewrite was performed.

## Findings independently confirmed

**F1, D5/H8 cross-bank collision: confirmed.** D5 record 1 in v1.2.1 and H8 record 7 both freeze amount 6 with denominations {1,3,4}. Their canonical identities are equal. The explicit zero-intersection rule makes this a blocking failure.

**F2, D4 parity claim: confirmed.** Odd denominations and an odd amount do not imply an unreachable amount. For example, {3,5} reaches 9 as 3+3+3. The answer-zero claim for D4 records 3–4 was invalid.

**F3, repeated-use predicate: confirmed as a protocol defect.** The committed generator defines an N0 helper but never invokes it, never checks the item-3a predicate, and does not implement a deterministic H1–H4 witness/regeneration rule. Claude's report found no qualifying H4 record in its realized scratch output. The corrected draft replaces post-generation regeneration with fixed witnesses.

## Claude's withdrawn report claims

- D3 gcd construction order is specified as g, then n, then the t/coin set, then amount.
- H2's denomination count n in [2,6] is specified by BANK_DESIGN §5 and applies to records 5–12 as well.
- D5's draw dependency is resolved by the per-stratum dependency rule: choose n and coins before the amount search.
- The earlier report's D4 draw-order description was inconsistent with the committed code; the actual D4 code draws n, then t, then amount.
- Calling H4 "unimplementable" was too strong. The precise issue is that the v1.2.1 failsafe does not specify which record is replaced and the committed generator does not implement the failsafe.

## Additional generator defects

Static inspection of the 343-line committed script found:

1. Internal `while True` loops bypass the outer 1,000-attempt cap. D4's gcd rejection redraws only the t set, contrary to the whole-record restart rule.
2. The pair condition `len(set(map(tuple, [coins, perm]))) >= 1` is tautologically true and does not reject identity permutations.
3. The script reads `sys.argv[1]`, contrary to the production-generator no-arguments rule in C9 item 6.
4. It writes diagnostic and held-out JSONL files before checking their cross-bank canonical intersection. This is acceptable only as a diagnostic dry-run harness, not as production acceptance behavior.
5. The helper `n0()` is defined but never called.
6. The D4 entry in the report's GAPS list says amount→n→coins, while the code actually draws n→t→amount.

The generator is therefore preserved as a reviewer artifact, not endorsed as a conforming implementation.

## Independent arithmetic checks for v1.2.2 witness proposals

GPT independently evaluated the unbounded LC518 combination count and the 0/1 subset count N0 for each proposed fixed witness:

| Stratum | Witness (amount; coins) | Oracle | N0 | Predicate |
|---|---|---:|---:|---|
| H1 record 4 | 12; [2,3] | 3 | 0 | passes |
| H2 record 5 | 60; [2,58] | 2 | 1 | passes |
| H3 record 1 | 100; [50] | 1 | 0 | passes |
| H4 record 3 | 100; [4,96] | 2 | 1 | passes |

The D5 fixed exemplars were also checked against the minimum-coin objective:

| Record | Amount; coins | Largest-first greedy | Minimum |
|---|---|---:|---:|
| D5 record 1 | 8; [1,4,5,6,9] | 3 | 2 |
| D5 record 2 | 9; [1,2,4,5,6] | 3 | 2 |

These are arithmetic checks only. GPT did not generate either bank.

GPT initially proposed [1,5,7] at amount 10, then replaced it with the two five-coin exemplars above because their n, amount and denomination structure excludes them from every held-out stratum and from D1–D4/D6–D8 by the pinned construction rules. The remaining random D5 candidates are still subject to within-bank collision rejection. The full canonical intersection must still be checked as a hard acceptance condition when generation is explicitly authorized.

## v1.2.2 draft changes

The new draft is a separate full-document copy; v1.2.1 is unchanged. It:

- replaces D5 record 1 to remove the known frozen exemplar collision;
- removes the unsupported answer-zero claim for D4 records 3–4;
- makes D4 gcd failure restart the whole candidate record;
- replaces the unspecified H1–H4 post-generation failsafe with four named witnesses;
- defines input_id, canonical_id, stratum, rule_id and pair_id formats;
- pins rule_params values;
- bounds coin-slot, whole-record and whole-pair retry loops;
- requires non-identity reorder permutations;
- requires the cross-bank disjointness check before authoritative bank files are written; and
- distinguishes a diagnostic harness from the no-arguments production generator.

These are proposals for Claude review. C8/E3 remains an owner decision.

## Authorization and scope

Claude reports that it generated both scratch banks despite the v1.2.1 gate and later deleted them. They were not committed and are not study data. GPT has not run Claude's generator, created bank files, opened the private annex, constructed solver bodies, or executed candidate solvers.

Bank generation remains unauthorized. The stray master report remains in place pending the owner's explicit approval for a one-file deletion commit. No master write was performed by GPT.
