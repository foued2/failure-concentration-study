# C9 dry-run report (Claude, review artifact)

**Scope.** A private dry run of the C9 bank-generation procedure in CORRECTIONS_RECORD_v1.2.1, items 1-8. The bank files were written to a private scratch location and are NOT published (they are bank-like output; the v1.2.1 scope excludes bank generation). This report and the generator script are published for review. No solver bodies, no execution of candidate solvers, no annex opened.

**Generator.** `generator_c9_dryrun.py` (17,682 bytes). Python 3.13 random.Random, seeds 11052026 (diagnostic) and 20261101 (held-out), one stream per bank, per-stratum construction as written in C9 item 3.

## Results

| Check | Result |
|---|---|
| Record counts | diagnostic 64 (D1-D8), held-out 80 (H1-H8) - match the bank design |
| Reproducibility (two separate processes, same implementation) | BYTE-IDENTICAL: diagnostic.jsonl sha256 prefix e675aeddce9f58c0, heldout.jsonl 6034ee3cfc1a296e; sidecars and report.json identical across runs |
| Mandate checks (amount-0 answer 1; D3/H7 answer 0; D4 odd-amount answer 0; H2 answer >= 2 with whole-record redraw) | pass in the dry run |
| Cross-bank canonical disjointness (item 8) | **FAILS: 1 collision** (see F1) |
| Repetition predicate (item 3a), oracle > N0 | H1 1/12, H2 12/12, H3 1/8, **H4 0/8** (see F3) |

Determinism shows only that this implementation is deterministic. It does not show that the specification is reproducible by another implementer; that needs the spec gaps below closed.

## Findings against the specification (for GPT and owner)

**F1 - Cross-bank collision (blocking).** The frozen non-greedy exemplar (amount 6, coins {1,3,4}) appears twice: as D5 record 1 (diagnostic) and as H8 record 7 (held-out, frozen verbatim by C9 H8). Item 8 and the section-2 disjointness check require zero collisions, so acceptance must abort. Remedy requires a spec change: keep the exemplar in one bank only, or pin a distinct held-out exemplar. Owner decision.

**F2 - D4 records 3-4 do not force answer 0 by construction.** They use all-odd coin sets with odd amounts. Odd coins can sum to odd amounts (e.g. coins {3,5}, amount 9 = 3+3+3), so answer 0 is not guaranteed. The generator passes only because the random coin values are large. Parity unreachability requires all-even coins, as records 5-8 already do. Spec fix: records 3-4 need a different mechanism or the answer-0 claim must be removed.

**F3 - Repetition predicate, H4 has no satisfying record.** Item 3a says that if a stratum has no record with oracle > N0, its records are regenerated one whole record at a time until one satisfies the predicate. The spec does not say which record is replaced or how the RNG consumption works. H4 is 0/8, so the rule is unimplementable as written. Not implemented here.

## Spec gaps the generator had to fill (chosen conventions, recorded in the generator's GAPS list)

- D2: as-given coin order (match coin first) not pinned; chosen [c*] + distractors.
- D3 gcd records: draw order of n versus g not pinned beyond the amount-last rule.
- D4 records 3-8: coin-set size n not specified; chosen randrange(2,7).
- D4 records 1-4: draw order not pinned; chosen amount, n, coins.
- D5 records 3-8: draw order not stated; chosen n, coins, amount.
- H2 records 5-12: n not specified; chosen randrange(2,7).
- H8 records 8-12: count of further coins not specified; chosen n = randrange(3,9) as records 1-6.
- Global: input_id, canonical_id and rule_id string formats are not defined; as-given coin order is taken as the draw order for every stratum.

## Interpretation for review

The C9 procedure is far more concrete than v1.0, and this dry run shows it can be implemented and is deterministic. It is not yet a reproducible specification: two blocking defects (F1, F2) and one unimplementable rule (F3) remain, plus several unpinned draw orders. Bank generation should stay gated until these are corrected in a versioned record (v1.2.2 or later), as item 3 requires.

## Not done

No bank files published. No candidate solver written or executed. No E3 decision made. Owner decisions still open: E3 (C8); F1 exemplar choice; F2 and F3 spec corrections.

## Process note

This report was first written to `master` (commit 286157b) by mistake: the branch creation and file write were issued in one batch, and the file write ran before the branch existed, so the tool fell back to the default branch. The review copy is on this branch. The `master` copy needs owner approval to revert.
