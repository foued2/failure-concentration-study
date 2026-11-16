# GLM Delta-Review Handoff: LC518 Population and Experimental Design v0.20

**Date:** 2026-11-16  
**Reviewer:** GLM (Z.ai)  
**Prepared by:** GPT  
**Status:** READ-ONLY, DESIGN-ONLY DELTA REVIEW REQUEST  
**Active review route:** GLM, until the project subject changes  
**Claude route:** Suspended by owner direction; no Claude review is claimed or implied.

## 1. Exact target and live identity

Please review the v0.20 specification:

`lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.20.md`

Fetch the live branch tip and verify the exact v0.20 blob, line count, final newline, and predecessor identity before reading. Do not assume this handoff's expected state is current.

Immediate predecessor:
- v0.19 path: `lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.19.md`
- v0.19 blob: `9b940e8ea00cd3880c2ca3c63ced620fca547b12`
- v0.19 content commit: `4b12236d8b54179ea9133bbac68138206d9d3f6f`

The v0.19 predecessor must remain unchanged.

## 2. Review scope

This is a focused delta review of the v0.19-to-v0.20 change. Read the complete diff and each changed passage in its surrounding section. Do not repeat the full v0.18 review or the full v0.19 delta review.

The two defects carried forward from the v0.19 review are:

1. **V19-1, §0.22 F3:** replace the unanchored present-tense statement that the header and §8 "now" identify two review streams with a historically pinned statement that this described the v0.18 process state and was superseded by the owner route decision in §0.23.
2. **V19-2, §0.19 closing paragraph:** pin the separate Claude-addressed route to the arrangement in force at v0.18 publication, while accurately recording that §0.23 later suspended that route.

Check that the corrections preserve the historical truth and do not rewrite, erase, or misattribute the prior review decision.

Also verify:
- the new §0.24 accurately records GLM's v0.19 delta review, GPT's adjudication, and the limits of the evidence;
- review-artifact identity information is distinguished as GLM-reported unless the actual artifact bytes are independently available to you;
- the current header and §8 state that GLM is active, Claude is suspended, and GPT separately adjudicates GLM reviews;
- no authentic Claude review is claimed and GLM is not described as a Claude substitute;
- the v0.20-to-v0.19 diff contains only the two tense corrections, the §0.24 review/adjudication record, and necessary version/header/closing metadata;
- the B1 target, estimand, M1-si conditions, LOPO procedure, parent/lineage rules, 30-parent logistics-only status, sample-size-open status, and all authorization gates remain substantively unchanged.

## 3. Prior v0.19 review record

The v0.19 delta review supplied by GLM reports:
- verdict: APPROVE WITH CORRECTIONS;
- no Blocker or Major findings;
- V19-1 Minor (§0.22 F3) and V19-2 Nitpick (§0.19 closing sentence);
- exact live verification of the v0.19 and v0.18 identities, branch/master state, reverse reconstruction, and the v0.18 review-artifact hashes.

The review artifact is reported as Git blob `7fec3118e3da60394329ea576984589a304fbab6`, 111 newline-terminated lines with final newline, and SHA-256 beginning `DABDC6BC` and ending `B32C`. GPT recorded these as GLM-reported because the separate artifact bytes were not available to GPT. If you have retained bytes, you may independently verify them; do not claim to have done so without the bytes.

## 4. Evidence and limits

Distinguish live repository checks performed by you, the exact diff, the supplied prior review text, and claims that remain GLM-reported or owner-reported. No predecessor document needs to be reopened unless a changed statement makes a specific predecessor claim.

## 5. Required output

Return review text for GPT to adjudicate. Include:
- v0.20 blob identity, dimensions, and final-newline status;
- v0.19 immutability;
- exact diff scope;
- findings with severity, exact section, wording, reasoning, evidence, and proposed correction;
- important changed and unchanged areas examined where no defect was found;
- limitations.

Choose one verdict: **APPROVE**, **APPROVE WITH CORRECTIONS**, or **DO NOT APPROVE**. State whether any defect blocks design freeze.

Do not modify the repository or create another specification version.

## 6. Strict boundaries

Read-only, design-only. No repository writes or commits, no solver sourcing or construction, no mutation allocation, no source modification, no compilation or execution, no diagnostic probing, no bank or protected-set access, no outcomes, no fitting, sampling, simulation, power calculation, or scientific analysis.

This handoff requests review only. It is not a freeze record or execution GO.
