# Closure record: feasibility-first protocol design

**Date:** 2026-10-25
**Branch:** `review/feasibility-protocol-2026-10-25`
**Reviewed snapshot:** `2aa6faf`
**Corrected draft:** `28ae637`
**Disposition:** **INFEASIBLE UNDER THIS DESIGN**

This is a document-only closure record. It does not authorize Gate B, solver generation, model or API calls, execution, simulation, a confirmatory study, or Step 2. No existing artifact, bank, score, protocol, or result was changed.

## Decision

Independent reviews of the actual protocol at `28ae637` agreed that it fails the written feasibility gate. The protocol's own stop rule (§8.1) is triggered because Gate A cannot show a credible multi-`k`, distinct-mechanism construction with the required independent support.

The design attempt is therefore closed as infeasible under this design. This is not a negative scientific finding about concentration `C`. The existing evidence still establishes neither that `C` adds predictive value beyond `k` nor that it lacks such value.

## Defects that triggered closure

1. **The `k=10` worked construction does not meet the protocol's minimum support.** Section 5 requires at least two mechanism families at each `k`, at least three independent clusters per mechanism family in each `k x C` cell, and at least 24 independent clusters overall. The `k=10` example supplies only `T3` and `T4`, both tokenizer/lexer mutations. It does not demonstrate a second mechanism family at `k=10`, let alone the required independent clusters in each cell. The document is transparent that the full design is unverified, but that means Gate A has not met its own criterion.

2. **The bootstrap resampling unit is not coherent.** Section 3.2 defines an independent cluster as a distinct mutation site with a distinct full-domain failure set, and also says a low-`C`/high-`C` pair for one mechanism is a single unit. A low-`C` and high-`C` solver have different failure sets, so they are two clusters under that definition. Section 7.2 then stratifies resampling by `k x C x mechanism family` while requiring the pair to be resampled together. No single `C` stratum can contain that pair. Repeating the full cross-validation procedure does not resolve an incorrectly specified resampling unit.

3. **The full-domain alias check is not operational.** The example task permits arbitrary whitespace and multi-digit integers, so its input domain is not finite as written. Gate B requires verification of distinct full-domain failure sets, but the protocol does not specify a bounded domain or a proof method. The independence and alias checks are therefore not reproducible.

4. **`C` remains nested in the mutation site.** In the worked tables, `P1`/`R1` and `T1`/`T2` are different code sites. Every `C` contrast therefore compares different sites, and no site appears at two `C` levels. This moves the defect-identity confound from family to site: the protocol controls for coarse mechanism family but not for site.

5. **Tied profiles make "dominant family" ambiguous.** `T3 = (0,0,0,0,5,5)` and `T4 = (0,0,2,2,3,3)` both tie F5 with F6 for the maximum. The text calls the tokenizer family dominant in both, but under a tie that is not well defined.

## Interpretive note, not an established result

Across the designs considered, `C` changes only when the solver's failure profile changes or when the probe partition into families changes. At a fixed mechanism, `C` can move only if the probe partition moves, and then `C` describes the instrument as much as the solver. The W1 alternate-partition sign flip is consistent with this reading. This note is offered as a possible explanation for why several designs hit the same wall; it is not a demonstrated finding and should not be cited as one.

## Preserved records

- `2aa6faf` — unchanged review snapshot of the protocol.
- `28ae637` — corrected draft that was reviewed and failed.
- `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` — accepted assessment at `8bb2e82`.
- `natural-feasibility-pilot/offline-inventory-2026-10-25/INVENTORY_REPORT_2026-10-25.md` — closed inventory evidence.
- `engineered-study/math/results/three_world/` — frozen three-world results and descriptive stratum contrasts.

## Archive preservation trigger

The roughly 592 MB three-world raw/per-trial archive remains local-only. The first time the other machine is reachable, copy the archive to storage independent of the C: drive and verify it against its manifest. This is a preservation obligation, not a reauthorization to run anything.

## Final authorization boundary

No further protocol revision, Gate B work, solver generation, model/API call, simulation, bank change, or confirmatory study is authorized. Any future work requires a new, explicit authorization.
