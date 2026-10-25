# Concentration research-formulation record (2026-10-25)

Entry point for three working documents exported from Claude web-chat docs. They record the post-closure re-formulation of the failure-concentration question. They are working notes, not frozen artifacts.

## Boundaries

- The failure-concentration study remains closed under its existing authorization.
- Nothing here authorizes solver generation, solver execution, simulation, model calls, new data collection, or any experiment.
- This branch is a record. It adds only files under `concentration-formulation/`. No existing file was modified, and `README.md` is untouched.
- Related material elsewhere in the repository, not merged here: `CONSTRUCT_VALIDITY_ASSESSMENT_2026-10-25.md` (commit `8bb2e82`, on `research/concentration-math-spec`) and the protocol draft on `review/feasibility-protocol-2026-10-25` (commits `2aa6faf`, `28ae637`).

## Files

| File | What it is | Export revision | Role |
| --- | --- | --- | --- |
| `02_RESEARCH_FORMULATION_NOTE_2026-10-25.md` | Hypotheses H1 to H4, reference model, units of independence, feasible support | rev 3 (revised after GPT review) | Intended single research record |
| `03_LITERATURE_SCAN_2026-10-25.md` | Focused scan of prior work, with counter-evidence and gaps | rev 1 | Evidence base. Abstract-level, not a systematic review |
| `01_FEASIBILITY_NOTE_IDEA1_RANDOM_DEFECT_SETS_2026-10-25.md` | Paper-only assessment of random defect-set sampling (Idea 1) | rev 1 (unrevised) | Proposal, partly stale (see item 2 below) |

Suggested reading order: 02, then 03, then 01.

At export, only the status lines of files 01 and 02 were adjusted: file 01 said "Not committed", which stopped being true, and both now say they are exports. No other text was changed.

## Known conflicts and gaps (not resolved here)

1. **Two versions of the formulation note.** GPT designated a local, uncommitted `CONCENTRATION_RESEARCH_FORMULATION_2026-10-25.md` as the canonical candidate, with a SHA-256 reported by DeepSeek of `7C67AB21D4DDFDFDCF8A966AEBDA3ED70D1F1411F65B26AB2F367BE909F70DF3`. That hash has not been independently reproduced, and file 02 here is the Claude Doc version, which may differ. Reconcile before either is treated as final.
2. **File 01 predates later findings.** It does not include the verified v0.2 result (all 90 eligible rows have all-or-none family counts, from ten base bodies), the instrument-level cause (each family's probes are variations of one property), or the repair for the alias check, which is not fully outcome-blind when it uses the evaluation domain and needs a separate identity-check domain.
3. **Stale literature status in file 02.** Section 10 lists three titles as not independently checked. File 03 has since checked them and corrects the descriptions of two.
4. **No primary hypothesis is marked in file 02.** The working proposal is H3: ranking of same-`k` rejected candidates by `C` on independently constructed held-out inputs, with held-out average performance secondary.
5. **Population mismatch.** File 01 uses engineered candidates built from sampled mutations. The proposed primary question uses naturally generated candidates. This decides whether fixed-`k` variation in `C` can exist.
6. **Wording.** Use "held-out", not "unseen".

## Open decisions

- Reconcile the local file with file 02.
- Decide which hypothesis is primary.
- Decide the bounded held-out domain and the smallest practically meaningful gain.
- Complete the search of the neighboring areas listed in file 03, Section 8, before any novelty claim.
