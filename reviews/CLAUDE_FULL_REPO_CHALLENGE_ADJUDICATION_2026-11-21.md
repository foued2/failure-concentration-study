# Full-Repository Challenge Adjudication

**Date:** 2026-11-21  
**Repository snapshot:** master at 33dca9b61d95b9fb750f750919c32c2e08b2ee90  
**Scope:** source, committed pack, report, freeze, Git-history and review-record inspection. No solver execution, CBMC run, provider-side lookup, external chat archive inspection, or hidden-outcome regeneration was performed for this adjudication.

## Executive disposition

Claude identified a real and consequential gap: the repository verifies the bytes and analysis of the retained solver packs more thoroughly than it verifies the claimed process by which the solver bodies originated. The checked-in emitters are deterministic writers of literal source-code bodies, not live LLM-generation clients. The v0.2 pack contains 40 unique literal body templates written three times each, not 120 unique implementations. The repository does not independently substantiate the claimed LLM session, raw single-shot outputs, or no-selection procedure.

This is enough to withdraw population-level claims about natural single-shot LLM submissions. It is not enough to prove that the bodies were manually authored by a named person or never originated from an earlier LLM session outside the repository. The correct provenance status is UNVERIFIED, not “proven human-authored”.

Claude is also right that v0.2 did not identify the incremental predictive value of concentration beyond failure count. It is wrong on several supporting details: seed collisions were not realized; the delta_i/seed row-label error had already been corrected in the findings ledger; and the RLC-0 command explicitly overrides the global unwind of 64 for the 10,000-trip harness loop. The RLC-0 empirical feasibility result remains unestablished, but because the recorded CBMC attempts were incomplete from OOM/timeouts, not because that loop was truncated at 64.

## Finding-by-finding adjudication

| Claude challenge | Adjudication | Repository consequence |
|---|---|---|
| 1. “LLM-generated packs” are hardcoded | **Accepted in substance; authorship inference qualified.** Both emitters store complete bodies as source literals and write them deterministically. No provider/session provenance is retained. The files do not invoke an LLM. The repository cannot establish whether these literals were copied from earlier model outputs. | Withdraw empirical claims about natural LLM populations, single-shot sampling and no-selection. Describe results as conditional on the retained body corpus. |
| 2. Instance axis has one diagnostic probe suite | **Accepted, with LOIO scope correction.** Graph content is invariant to the instance seed. The builders accept only variant v; the seed changes only metadata. | v0.2 cannot test instance-conditional diagnostic variation or unseen-solver generalization. LOIO remains a hidden-suite/instance prediction exercise for a fixed solver corpus, not literally vacuous. |
| 3. Seed collisions and delta_i pairing | **Collision claim rejected as a realized defect; row-mapping issue already corrected.** The frozen formula yields 40 distinct confirmatory seeds, none equal to pilot seeds. The delta_i mapping error in Addendum B was recorded as F6 and corrected in FINDINGS_LEDGER_2026-10-19.md; the statistic, CI and classification were unaffected. The runner repair is real and disclosed. | Record the missing pairwise uniqueness assertion as a latent defensive-code gap, not an observed collision. Retain the frozen-versus-executed runner distinction. |
| 4. v03p inherits unsupported LLM premise | **Accepted.** The Phase 0 design's natural-single-shot population is a proposed future protocol population, not an empirical fact established by v0.1/v0.2. | Add a warning to the Phase 0 document. Any future protocol needs an auditable generation-provenance gate. No later phase is authorized. |
| 5. RLC-0 never tested / unwind bound impossible | **First part accepted; unwind diagnosis rejected.** Phase C was never performed and no six-seed verdicts exist. However, the documented CBMC command uses --unwind 64 plus an explicit --unwindset ...:10001 for the fixed 10,000-trip rlc0_build loop. The override is present in spec.json, FREEZE.md, RESULTS.md and the raw command. | State that full-domain feasibility was not demonstrated because canary proof attempts were incomplete (SAT OOM / wall timeout) and C2 remained open. Do not claim the harness loop was cut off at 64. |
| 6. LC518 allocation “does not exist” | **Overstated.** The reviewed Parts 4–8 do not establish the actual named taxonomy or assignments, but they do contain structural requirements and nominal arithmetic. A standalone annex's existence is unknown, not disproven. | Retain BLOCKED / NOT ASSESSABLE. Do not infer nonexistence, reconstruct assignments, or build from totals. |
| 7. AI-review blind spot | **Accepted with qualification.** The reviewed repository's AI-review records did not independently verify the LLM provenance premise. “Every review was completely credulous” overstates the point: reviews did challenge statistical, scope and governance issues. | Add generation provenance as a first-class audit requirement; do not dismiss other valid internal audits. |

## 1. Solver-pack provenance: what is established

### v0.1 pilot

generation/_emit_pilot_pack.py contains 20 literal body assignments, SOLVERS["solver_01"] through solver_20. Each is a triple-quoted source-code string. The script's main() writes these strings to generation/pilot_pack/. There is no model/API call, sampling operation, or session capture in the emitter.

specs/generator_spec.json names opencode/mimo-v2.6-flash-free, describes a single generation session, provides a prompt and directives, and declares a retention procedure. Those are protocol/specification assertions, not independent evidence that the named procedure occurred. The repository tree contains no corresponding provider transcript, request ID, raw response archive, or equivalent verification artifact. The emitter and solver files first appear in the same Git commit, 1612b87167 (2026-10-11 11:25:34 UTC), after the freeze timestamp in FREEZE.md (11:21:36 UTC); the emitter itself is not among the frozen file hashes.

The source proves deterministic emission from 20 literal bodies. It does not prove the bodies were manually conceived by the committer, and it does not exclude an unrecorded earlier LLM session. Therefore the correct statement is: LLM origin, single-shot status and no-edit/no-selection history are unverified in the retained repository record.

The pilot's INFEASIBLE gate outcome remains valid for the 20 retained files. Its statement that a population of natural single-shot LLM submissions is the wrong instrument is unsupported and is withdrawn. The retained corpus has 16 files with k=0 and four multi-failure approaches; this is descriptive of the corpus, not an estimate of the named model's natural failure distribution.

### v0.2 pack

v02/generate_pack.py defines 40 distinct literal source bodies in S[1] through S[40]. Its emitter loops over each body three times and writes a separate file with a different submission/replica header. Direct source inspection establishes 40 distinct function-body strings and three files per body. The pack is therefore 40 body templates × 3 deterministic file copies = 120 files. The copies are not distinct solver implementations and do not provide 120 independent solver draws.

The source contains comments explicitly marking several variants as “natural defect” examples. This supports the description “templated and defect-annotated corpus”; it does not prove the external origin of those strings or establish that the observed failure geometry was selected after the pilot. Claude's strongest assertion that the result was deliberately “authored into the pack” to reproduce a particular C=5/k support is not fully established by the emitter alone. The exact observed support must be kept distinct from claims about the generator author's intentions.

The Git chronology is material:

1. 798b446 (2026-10-12 12:56:28 UTC) commits the v0.2 protocol/spec/analysis freeze. It does not contain v02/generate_pack.py or the 120-file pack.
2. 8f83ee8 (13:13:24 UTC) commits all 120 pack files and amends FREEZE_V02.md to add the generator/pack hash records.
3. a6a8439 (14:43:20 UTC) first adds v02/generate_pack.py to Git, together with the disclosed confirmatory-runner repairs.

The generator may have existed in an untracked local workspace before emission, but the Git history does not demonstrate that it was versioned and frozen before emission. The pack's exact literals and deterministic replication are reproducible; its claimed upstream generation process is not independently reproducible from the retained evidence.

### Provenance conclusion

The reports must not claim that 20/120 files are verified unmodified single-shot LLM outputs or that the retained body corpus represents natural model submissions. The reports may describe the named model and generation method as the declared but unverified provenance. The findings concern the retained source-code corpus.

## 2. Probe invariance, identifiability and validation scope

In study/probes.py, each family builder has signature _build_f*(v); none accepts the instance seed. make_probe_suite(instance_seed) passes only v to the builders. The seed is used to compute the returned dictionary's "seed" metadata field. Consequently, graph content, assigned predicates and predicate-satisfaction vectors are invariant across instance seeds; only the metadata value varies. The October interpretability audit independently compared graph-relevant hashes across 11 seeds and reported one unique graph-content hash.

For a given solver body, its probe-failure vector and therefore k and C are constant across instances. Instance-level hidden suites vary, so LOIO still evaluates whether these fixed solver-level measurements predict outcomes on other hidden-suite draws for the same pack. It does not evaluate instance-specific diagnostic features, and it cannot establish generalization to new solver bodies.

The 2026-10-14 interpretability audit directly verified C=5/k in the 90 persisted eligible pilot rows, occupying four (k,C) cells: (5,1), (10,0.5), (20,0.25), and (25,0.2). No within-k concentration variation was observed. The confirmatory report persisted 1,200 as an aggregate eligible-pair count but did not persist the per-solver (k,C) rows. A subsequent audit explicitly records that those rows were not regenerated because that would require executing the solvers. It is therefore inaccurate to describe 1,200/1,200 confirmatory rows as directly recounted from persisted raw rows. The same pack and seed-invariant probe construction make the structural limitation applicable, but the evidence provenance should be stated accurately.

The frozen v0.2 NEGATIVE classification remains a valid output of its decision rule. It is not a test or refutation of concentration's incremental predictive value under equal-k, different-C support. The narrow CI is computationally reproducible from the saved 40 delta_i values; the repo's later audit correctly distinguishes reproduction from coverage. It does not demonstrate precision for the unobserved independent-C contrast. The “not underpowered” sentence in REPORT_V02.md is qualified accordingly.

### Pilot-support wording correction

Claude's first audit stated that no pilot mass lay in the numerical range k in [2,24], while listing observed k values of 5 and 10. Those values are inside that interval. The defensible finding is not “no observations in the interval”; it is “no equal-k, different-C contrast and insufficient useful support”. Numerical eligibility alone does not create identifiability.

### Relabel control and execution record

The v0.1 instrument spec describes a per-instance balanced relabel partition keyed from the instance seed. The v0.2 spec and models_v02.py use one shared balanced partition per replicate across instances. This is a separately frozen v0.2 control design; it is not literally the same control procedure as v0.1.

The frozen confirmatory runner hash is recorded as 19c41047...; the executed repaired runner hash is recorded in the integrity review as b2c02dde.... The documented repairs addressed imports and the solver-path/function pairing, plus defensive initialization. The integrity review says the frozen statistical calculations were not changed. This is a real execution-provenance deviation and is already disclosed; it does not, on the evidence reviewed here, show a post-result change to the estimand or statistical constants.

## 3. Seed and ordering claims

The seed function lacks a pairwise duplicate-seed guard, which is a latent defensive-programming weakness. It is not a realized collision: recomputation of the frozen v0.2 seed formula yields 40 distinct values and none of the pilot seeds {101,102,103}. Claude's own audit also reports 40/40 distinct.

The mismatch between delta_i and seed ordering is not a newly discovered unacknowledged defect. loo_delta_pairs stores values in sorted instance-ID order, while an earlier appendix paired them with derivation order. The repository's v02/FINDINGS_LEDGER_2026-10-19.md records this as F6 and supplies the corrected mapping. It affected per-row labels in the appendix, not the 40-value multiset, Delta, CI or terminal classification.

## 4. RLC-0: no empirical completion, but the cited unwind explanation is wrong

The empirical conclusion is straightforward: rlc0/ADDENDUM_2026-10-14_C.md §9 says Phase C (the six-seed execution) was never performed, was prohibited, and is moot. rlc0/FREEZE.md states that the rlc0-freeze tag was not created and final freezing was not authorized. No seed verdicts exist. The contract's sentence describing the purpose (“determine whether formal behavioral localization is technically feasible”) is a statement of intended purpose, not evidence that the objective was achieved.

Claude's claim that the global --unwind 64 necessarily truncates the 10,000-trip harness loop overlooks the explicit per-loop override. The recorded command is:

    cbmc.exe <file>.exe --function main --unwind 64 --unwindset "rlc0_build(ptr_struct_tag(identifier=tag-rlc0_input)).0:10001" --unwinding-assertions --bounds-check --pointer-check

That override appears in rlc0/spec.json, rlc0/FREEZE.md, rlc0/evidence/C2/RESULTS.md, and the recorded raw command. The harness loop is the fixed-capacity 10,000-trip loop; the 10001 unwind setting is recorded specifically for it. The global 64 bound remains for the other loops. Thus “every run is structurally incomplete because the harness loop is cut at 64” is refuted by the documented command.

The actual evidence is still insufficient: the C2 canary invocations encountered SAT-solver out-of-memory / verification-error states, and an authorized retry reached a wall timeout. These are incomplete proof attempts, not SUCCESS and not the expected canary FAIL. C2 remained open, full-domain certification was not demonstrated, and Phase C never ran. That is the correct reason RLC-0 does not support an empirical formal-localization feasibility claim.

The repository's OAuth-token rotation note is dated 2026-10-14 and says rotation had not been confirmed then. This review does not establish the credential's present status. The owner should verify that the token was rotated/revoked through GitHub security settings; no credential value is reproduced here.

## 5. LC518 mutation-allocation evidence

The 2026-11-10 mutation-allocation search is explicitly bounded to five supplied conversation PDFs, Parts 4–8. Within that corpus, the review found structural requirements and arithmetic but no named eight-mechanism taxonomy, actual pair-to-parent rows, identities of the two repeated pairs, S-extra assignments, or parent-family compatibility mapping.

The same corpus explicitly supplies a nominal structure: 30 parent IDs, 28 pairs once plus two distinct preselected repetitions, and a nominal 90 singly mutated versions from 30 × 2 + 30. The review says 90 is a nominal design count, not a verified realized count, because S-extra balancing is annex content. These constraints are meaningful design content; “the experiment has no design content at all” is therefore too strong.

The Part 8 correction says the standalone annex's existence and the completeness of any conversation-level allocation are unknown. Absence from the reviewed five PDFs does not prove that no annex or decision ever existed elsewhere. The adopted status remains BLOCKED / NOT ASSESSABLE, with 0/150 bodies and no construction. No allocation is inferred, reconstructed or created by this adjudication.

## 6. Review-system lesson and required future provenance gate

The repo's AI reviews challenged model form, identifiability, interval interpretation, execution exposure, controls and governance. However, the central LLM-generation premise was not independently authenticated in the reviewed records. This is a real validation gap, but it does not erase the valid audits of other issues.

Any future study that makes a population claim about model-generated submissions must require, before protocol freeze:

1. A provider-side or otherwise independently verifiable session record, request IDs or equivalent provenance for every retained generation event.
2. The exact model identifier/version, prompt including relevant system instructions, decoding parameters, seed policy and session boundaries.
3. Raw responses retained in generation order, without silent editing, repair, best-of selection or substitution. Any postprocessing must be separately recorded.
4. A body-level content hash and file-level content hash, with a mapping that distinguishes unique bodies, repeated copies, wrapper-only changes and failed/omitted outputs.
5. An independently recomputable manifest linking generation events to raw responses, parsed bodies and final files.
6. A pre-freeze provenance gate that fails closed when records are missing. Hashing a source literal or emitted file is necessary for byte identity, but is not evidence of model origin.

These are prerequisites for a future population claim, not authorization to run a successor experiment.

## 7. Repository changes made by this adjudication

The accompanying documentation patch:
- adds this adjudication;
- places provenance and scope warnings at the top of the README, pilot report and v0.2 report;
- adds a dated provenance qualification to the v03p Phase 0 design;
- leaves all frozen protocols, hashes, source code, solver bodies, execution outputs and RLC-0 artifacts unchanged.

The correction is retrospective and documentary. It does not authorize solver generation, solver execution, diagnostic collection, hidden-outcome collection, CBMC runs, or LC518 construction.
