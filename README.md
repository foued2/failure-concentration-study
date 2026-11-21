# failure-concentration-study

## Current scientific status and provenance correction (2026-11-21)

The repository contains completed historical analyses, but the central population claim in the v0.1 pilot and v0.2 study is not established.

- **v0.1 pilot:** the terminal INFEASIBLE gate result remains a valid description of the retained 20-file pilot corpus. The repository emitter stores 20 solver bodies as source-code string literals and writes them to files. The repository does not retain independently verifiable provider/session evidence establishing that those bodies were unmodified single-shot outputs of the named LLM. Claims about a population of natural LLM submissions are therefore unsupported.
- **v0.2:** the frozen decision procedure returned NEGATIVE, but the study did not identify the incremental predictive contribution of concentration beyond failure count. The versioned generator contains 40 literal body templates and deterministically writes three copies of each, producing 120 files. These are 40 distinct function bodies, not 120 distinct solver implementations or 120 evidenced generation events. No provider/session record in this repository verifies their claimed LLM origin.
- **Diagnostic instrument:** the six probe builders depend on the variant index, not the instance seed. The seed changes a metadata field, but not the probe graphs. For a given solver body, its diagnostic failure vector, k and C are therefore constant across instances. LOIO can still assess hidden-suite performance on other instances for this fixed pack, but it does not test instance-conditional diagnostics or generalization to unseen solver bodies.
- **v03p:** the Phase 0 document is a design-only preflight. Its natural-single-shot-LLM population assumption is not supported by the v0.1/v0.2 packs. No successor experiment, solver generation, or hidden-outcome collection is authorized by this correction.
- **RLC-0:** Phase C, the six-seed execution, was never performed. The CBMC evidence records incomplete canary proof attempts (OOM/timeouts), not a completed formal-localization feasibility result. The corrected command includes a per-loop unwindset override for the 10,000-trip harness loop; the failure was resource/proof incompleteness, not an unoverridden global unwind-64 truncation.
- **LC518 mutation allocation:** the reviewed evidence does not establish the complete eight-mechanism taxonomy or pair/parent/S-extra allocation. The standalone annex's existence is unproven, not disproven. The allocation remains BLOCKED / NOT ASSESSABLE; no allocation is reconstructed here.

The detailed evidence and correction of Claude's 2026-11-21 full-repository challenge are recorded in reviews/CLAUDE_FULL_REPO_CHALLENGE_ADJUDICATION_2026-11-21.md.

## Repository map

- PROTOCOL.md and FREEZE.md: historical v0.1 protocol and freeze record.
- generation/_emit_pilot_pack.py and generation/pilot_pack/: literal-body emitter and retained pilot files.
- pilot/PILOT_REPORT.md: pilot outcome plus the dated provenance/scope correction.
- v02/: v0.2 protocol, generator, reports, integrity and interpretability audits.
- generation_v02/pack/: 120 emitted files representing 40 literal body templates, each repeated three times.
- v03p/: Phase 0 design-only preflight; not an executed successor experiment.
- rlc0/: closed archival record; Phase C not performed and full-domain certification not demonstrated.
- reviews/: independent reviews and dated adjudications, including the full-repository challenge response.

## Interpretation rule

Hash identity and deterministic reproduction establish what bytes were retained and processed. They do not establish the origin of those bytes, the claimed sampling process, or population representativeness. Statistical classifications must be reported separately from whether the design identified the scientific estimand.

No frozen historical protocol, analysis result, solver body, or RLC-0 artifact is changed by the 2026-11-21 documentation corrections.
