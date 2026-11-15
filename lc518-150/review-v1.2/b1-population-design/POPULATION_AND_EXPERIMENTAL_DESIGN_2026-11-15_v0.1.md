# LC518 Population and Experimental Design Specification v0.1

**Date:** 2026-11-15  
**Version:** 0.1  
**Status:** UNREVIEWED DESIGN-ONLY DRAFT  
**Prepared by:** GPT  
**Review sequence:** Claude independent review, then GPT adjudication  
**Repository branch:** \`gpt/b1-computational-plan-2026-11-14\`

---

## 0. Status, scope, and authorization boundary

This document starts a new population-and-experimental-design specification. It is not a mutation allocation, a solver-generation specification, an analysis-plan amendment, or an execution authorization.

The population decision is:

> Engineered variants nested within real parent solver implementations.

The target is a deliberately constructed population of variants derived from selected, provenance-traceable parent implementations. The proposed claim is conditional on those selected parents, the realized variants, and the prespecified design variables. It does not generalize to the distribution of naturally occurring solvers.

The following are explicit boundaries:

- The November 6 mutation allocation was **not created**. That matter is closed. There is no allocation to recover or reconstruct.
- Neither the retired 90-version count nor the later proposed 150-variant count is binding on this new design.
- No parent implementations have been selected in this document.
- No mutation mechanism has been selected or assigned.
- No solver body has been created, modified, built, or run.
- No diagnostic probes, outcome records, model fits, simulations, or samples have been generated or evaluated.
- The existing 78-record LC518 bank has not been accessed for this work. It is exposed development data, not a protected confirmatory set.
- The joint-consent provenance gap remains open.
- Statistical ratification of the proposed trigger-(i) separation interpretation remains open.
- No software installation, project-data access, bank access, or execution is authorized by this document.

### 0.1 Binding B1 reference

The current symbolic B1 analysis plan is:

- **B1 analysis plan v1.7:** commit \`c3abe107acd2a3f8be58bf933eafcd734823a129\`, blob \`8c666e501a31726c728447d155045c0b20adc178\`, SHA-256 \`797BD9F72CF94FDC0EFF4A03B1544823D4042F8E530B27F4FB70CBD7F2BACA7C\`.
- **Acceptance record:** commit \`ac06c6676982eed795db9cb04c6d91803b591ac7\`, blob \`ea51d72f4f85c5d832d72add561b4c93472c364a\`.

The acceptance record is authoritative: v1.7 is accepted and frozen as a symbolic analysis plan, not as an execution GO. Its draft-time header text is a provenance snapshot and is superseded by the separate acceptance record.

The accepted v1.7 plan defines the B1 primary-sample cell condition in §1 item 2 and fold-level design estimability in §3 item 3. This document derives design implications from those provisions; it does not amend them.

### 0.2 Consequence of requiring a new protected evaluation set

B1 v1.7 explicitly uses the fixed 78-record bank, identifies it as publicly exposed development data, and does not treat it as sealed. This specification instead proposes a **new protected evaluation set** for the confirmatory claim.

Those are not interchangeable data sources. Substituting a new protected set changes the record set in the likelihood, the outcome vectors, the scoring population, and potentially design-matrix rank and computational dimensions. Therefore:

1. v1.7 remains frozen and unchanged.
2. The new protected set cannot be silently inserted into v1.7.
3. A separate B1 analysis-plan amendment must define the new record population, scoring rule, training and held-out-parent use, estimand implementation, and all affected controls before confirmatory evaluation.
4. The amendment must pass the same independent review and GPT adjudication process before any evaluation.
5. The 78-record bank is not used for the new confirmatory claim.

---

## 1. Claim scope and target population

### 1.1 Population

The study population consists of engineered variants derived from a finite, prespecified set of real parent solver implementations. Each parent is a distinct pre-mutation implementation lineage with a pinned source revision. Each variant is a traceable derivative of exactly one named parent under a prespecified mutation specification.

The study does not sample naturally occurring solver versions as its target population. Existing implementations provide parent material; the variants form the deliberately engineered study population.

### 1.2 Conditional research claim

The research question is:

> Within the studied population of controlled variants derived from the selected parent solver implementations, does diagnostic-failure concentration provide additional predictive information about solver correctness beyond the prespecified design variables, including total definite failures, unresolved outcomes, mutation identity, and parent family?

The claim is conditional on:

- the selected parent implementations and their recorded provenance;
- the variants produced under the frozen mutation specifications;
- the exact diagnostic cells and support actually realized;
- the new protected evaluation procedure and its declared input domain;
- the prespecified B1 model, scoring, and analysis rules, as amended and accepted for the new evaluation set.

A positive finding would support only this conditional claim for the studied engineered population and the declared evaluation domain. It would not establish a universal concentration law, a causal effect of concentration, or generalization to naturally occurring solvers or independently developed parent implementations outside the study.

### 1.3 Statistic and outcome conventions

The diagnostic concentration statistic retains the established definition:

\[
C_D(v)=\frac{\max_j f_j(v)}{k_{\mathrm{fail}}(v)}, \qquad
k_{\mathrm{fail}}(v)=\sum_j f_j(v),
\]

where \(f_j(v)\) is the definite-failure count in diagnostic stratum \(j\). Unresolved outcomes are recorded separately as \(k_{\mathrm{unresolved}}\); they are not included in the numerator or denominator of \(C_D\).

The existing convention \(C_D=0\) for \(k_{\mathrm{fail}}=0\) is a sentinel labelled **NO OBSERVED FAILURES**, not an ordinary observed concentration value for the primary B1 sample. B1 v1.7 excludes \(k_{\mathrm{fail}}=0\) versions and requires \(k_{\mathrm{fail}}\ge2\) for primary-cell eligibility. Versions with \(k_{\mathrm{fail}}=1\) do not satisfy that B1 threshold.

---

## 2. Parent eligibility and selection

This section defines proposed eligibility and selection rules. It does not identify or select actual parents.

### 2.1 Parent unit

A parent is one pinned, pre-mutation solver implementation. Its identity is fixed by, at minimum:

- canonical source-repository identifier;
- immutable commit, release, or archived source snapshot;
- cryptographic source-tree or source-archive digest;
- implementation lineage and known fork/derivation relationships;
- language, compiler or interpreter, and build configuration;
- license identifier, license-text digest, and recorded modification/redistribution permissions;
- source-acquisition date and provenance record.

Two repositories are not automatically two independent parent groups. Forks, copied implementations, and near-identical derivatives must be grouped or adjudicated under a prespecified lineage rule before parent counts are computed. A collection of renamed copies must not inflate \(G_c\).

### 2.2 Eligibility criteria

A candidate parent is eligible only if all of the following are documented:

1. **Task compatibility.** It implements the same frozen problem contract, input semantics, output semantics, and correctness requirements as the study target.
2. **Traceable provenance.** Its source revision, acquisition route, authorship or maintainer information where available, and lineage are recorded.
3. **Usable rights.** Its license and provenance permit the planned research modification, execution, and storage. Public availability alone is not treated as permission.
4. **Reproducible source identity.** The source snapshot can be pinned and independently hashed.
5. **Implementation identity.** It is a substantive solver implementation, not merely a wrapper, generated alias, benchmark harness, or copy of another selected parent.
6. **Predeclared technical compatibility.** Any required language and interface adaptation is specified as a separate, reviewable step and cannot silently change solver semantics.
7. **Outcome-blind selection.** Eligibility and selection do not depend on \(C_D\), failure counts, unresolved counts, correctness on the protected set, or whether a candidate appears likely to satisfy B1 support.

The exact correctness and compatibility checks for the unmutated parent must be set in the design and executed only after a separate authorization. No such check is run by this document.

### 2.3 Exclusion and lineage rules

Exclude or hold for review a candidate when its provenance is unresolved, rights are inadequate, task semantics differ, the implementation cannot be distinguished from another candidate's lineage, or its source revision cannot be pinned.

A fork may count as a separate parent only if a prespecified source-lineage review establishes that it is a substantively distinct implementation for the relevant target. Convenience, repository naming, or a different author label is insufficient.

### 2.4 Reproducible selection procedure

The proposed selection procedure is:

1. Freeze the candidate-frame definition before candidate review: repositories or registries searched, search terms or APIs, date/time cutoff, language and task filters, and capture method.
2. Preserve the complete candidate inventory, including exclusions and reasons. Do not preserve only selected candidates.
3. Apply the eligibility and lineage rules in §§2.2–2.3 without diagnostic or correctness outcomes.
4. Assign each eligible lineage a canonical identifier and pin the exact source revision.
5. Determine the required parent count from the design-support specification and the eligible frame. Do not choose a count merely to reproduce 30 parents or another historical number.
6. If the eligible frame contains more candidates than required, select using a reproducible, outcome-blind procedure declared before selection. A proposed method is to order eligible candidates by a cryptographic hash of a prespecified seed, canonical lineage identifier, and pinned revision, then take the first required number. The seed and full ordered frame are recorded. Any stratification or manual override must be specified and justified before selection.
7. Publish a parent manifest with source identity, lineage decision, eligibility status, license/provenance record, selection rank, and exclusion reasons.

The resulting parents are the studied parent set. Even if selection is randomized within a curated candidate frame, this does not make the set representative of all naturally occurring solvers and does not authorize a parent-superpopulation claim.

### 2.5 Parent count

The frozen B1 cell rule requires at least three distinct parent groups in an eligible cell. Therefore the structural minimum is:

\[
P\ge3.
\]

This is a support minimum, not a power calculation and not a recommendation that three parents are adequate for every scientific purpose. With exactly three parents, each LOPO training fold contains only two parent groups when the cell is present in all three. A larger parent count may be desirable for stability and coverage, but must be justified from the intended conditional design and candidate frame. No fixed parent count is adopted in v0.1.

---

## 3. B1 support derivation before mechanism selection

This section is the design constraint that must be resolved before mutation mechanisms are selected. The rules below distinguish the frozen B1 conditions from a stronger proposed matched-within-parent design target.

### 3.1 Exact B1 cell and full-population eligibility

Use the exact cell definition in B1 v1.7:

\[
c(v)=(q,Z,k,\ell),
\]

where \(k=k_{\mathrm{fail}}\) and \(\ell=k_{\mathrm{unresolved}}\). The symbols \(q\) and \(Z\) retain the meanings assigned by the accepted B1 specification; this document does not redefine them.

For a cell \(c\):

- \(G_c\) is the number of distinct parent groups represented in the cell;
- \(D_c\) is the number of distinct observed \(C_D\) values represented in the cell;
- \(k\) and \(\ell\) are held at their exact cell values.

B1 v1.7 §1 item 2 defines primary-sample cell eligibility by:

\[
k\ge2,\qquad G_c\ge3,\qquad D_c\ge2.
\]

There is no pooling across the exact cell components, mutation identities, families, or exact failure/unresolved totals. Eligibility is determined from design and diagnostic tables, not from solver correctness outcomes.

### 3.2 LOPO fold-level support

B1 v1.7 §3 uses leave-one-parent-out (LOPO) folds. For a held-out parent \(g\), the training part of cell \(c\) must satisfy the declared design-only conditions:

\[
G_{c,-g}^{\mathrm{train}}\ge2,\qquad
D_{c,-g}^{\mathrm{train}}\ge2,\qquad
W_{C,c,-g}^{\mathrm{train}}>0,
\]

where

\[
W_{C,c,-g}^{\mathrm{train}}
=
\sum_{\substack{v\in c\\\operatorname{parent}(v)\ne g}}
\left(C_D(v)-\overline C_{D,c,-g}^{\mathrm{train}}\right)^2.
\]

The values and inclusion decisions are calculated from the training design for that fold. They are not inferred from outcomes or fit results.

For every parent \(g\) intended to contribute a scored held-out fold in cell \(c\), the other parents must therefore supply at least two distinct \(C_D\) values in that cell, and at least two distinct training parents must remain. If a cell loses that support when a parent is held out, the accepted B1 plan's fold audit records the cell as excluded for that fold; it is not silently repaired by dropping rows, zeroing the concentration slope, or changing the baseline.

Equivalently, let

\[
S_{g,c}=\{C_D(v):v\in c,\ \operatorname{parent}(v)=g\}.
\]

For a cell to remain estimable in every intended held-out-parent fold, the design must satisfy, for every such \(g\),

\[
\left|\{h\ne g:S_{h,c}\ne\varnothing\}\right|\ge2
\quad\text{and}\quad
\left|\bigcup_{h\ne g}S_{h,c}\right|\ge2.
\]

The positive-\(W\) condition follows when the training set contains at least two distinct exact \(C_D\) values, but it remains a separately recorded B1 audit quantity.

### 3.3 What the frozen B1 thresholds do and do not imply

The full-population thresholds \(k\ge2\), \(G_c\ge3\), and \(D_c\ge2\) do **not by themselves** require every parent to contribute two variants, or require within-parent \(C_D\) variation.

For example, three parents with one version each and three distinct \(C_D\) values can satisfy the full-population rule and the LOPO training-support conditions for all three held-out parents. No parent has a within-parent pair in that configuration.

Conversely, three parents with one version each and only two \(C_D\) values can satisfy the full-population \(D_c\ge2\) threshold but fail the LOPO support condition for the fold that holds out the only parent carrying one of the values. Full-population eligibility is therefore not sufficient to guarantee that every parent contributes a scored fold.

These examples are structural illustrations of the frozen rules, not proposed variant allocations.

### 3.4 Proposed matched-within-parent support target

The selected population type is engineered variants nested within real parents. To make the design genuinely matched within parent, v0.1 proposes the following **additional design target**, subject to review:

> In at least one common exact B1 cell \(c\), at least three distinct parents each contribute at least two of their own variants, and those variants have at least two different \(C_D\) values within that parent while retaining the same exact cell values.

Formally, for at least three parents \(g\):

\[
|S_{g,c}|\ge2.
\]

This target is stronger than the cell-level thresholds alone. It is a deliberate design requirement for within-parent matched variation; it must not be described as a mathematical consequence of \(G_c\ge3\) and \(D_c\ge2\).

If adopted, it gives a sufficient structure for the stated LOPO support conditions: after any one of the qualifying parents is held out, at least two other qualifying parents remain, and each of those parents supplies at least two distinct \(C_D\) values in the same cell.

Its lower bound is:

\[
V_c\ge2G_c,\qquad G_c\ge3,
\]

so the minimum is six variant instances in one common cell when exactly three parents are used. This is a lower bound for this proposed matched target, not a total-study sample size. It does not imply five variants per parent, 30 parents, 90 versions, or 150 variants.

### 3.5 Historical M1 cross-document check

Earlier project-review context reported a stricter condition in a frozen Rev 2.6 §5.2 M1 clause: at least three parent groups each contribute two of their own five versions to the same exact failure/unresolved cell, with different \(C_D\) values within each parent.

The source bytes and the supersession relationship between that reported clause and accepted B1 v1.7 have not been independently established in this v0.1 preparation. Therefore:

- the reported Rev 2.6 M1 condition is **not silently treated as either binding or superseded**;
- the proposed matched target in §3.4 is recorded as a design proposal that is compatible with the reported stricter condition;
- Claude's review should identify the controlling source, its exact version/hash, and whether its within-parent requirement remains binding;
- GPT will adjudicate that cross-document issue before this specification can be frozen.

If Rev 2.6 M1 remains binding, its exact requirement must be incorporated and cited. If it has been superseded, the superseding decision must be cited. No design count is frozen until this is resolved.

### 3.6 Additional structural checks

The B1 support rules are necessary design constraints, not a complete guarantee of model estimability. The final design must also be checked against all accepted B1 requirements, including:

- exact cell identity and no pooling;
- the full LOPO scored/excluded fold-cell audit;
- exact \(C_D\) variation and positive \(W_C\) within each scored training cell;
- baseline design-matrix rank and the declared independence of the concentration predictor from baseline columns;
- the complete common-record crossing required by the eventual protected evaluation set;
- any other design-only condition in the B1 analysis-plan amendment.

No fitted-model result may be used to define cell eligibility or alter the design after outcomes are known.

---

## 4. Mutation mechanisms and variant construction rules

No mutation mechanism is selected in v0.1. Mechanism selection follows, rather than precedes, acceptance of the support requirements in §3.

### 4.1 Required mechanism record

Before any construction, each proposed mechanism must have a written record containing:

1. Stable mechanism identifier and version.
2. The specific solver or program property it is intended to vary.
3. A technical rationale grounded in the solver's implementation or algorithmic structure.
4. The exact transformation or mutation operator, including all parameters and allowed parameter values.
5. The parent implementations to which it is applicable and any applicability restrictions.
6. Whether the variant contains one mutation or a prespecified combination. Combined mutations must have their own identity and may not be concealed as a single mechanism.
7. The source locations and expected semantic scope of the transformation.
8. A predeclared validity and provenance check to be applied under a future authorization.
9. The relationship between the mechanism identity and the frozen B1 cell variables.
10. A statement explaining why the mechanism is scientifically relevant independent of whether it produces a desired \(C_D\), failure count, unresolved count, or correctness outcome.

### 4.2 Anti-selection rules

Mechanisms must not be selected, tuned, retained, or removed because they make the B1 support conditions pass or because they yield a preferred concentration or correctness result.

The design must not:

- choose mechanisms after inspecting realized \(C_D\) values;
- backfill a missing cell by inventing a new mechanism after seeing the diagnostics;
- drop an inconvenient variant because its \(C_D\) or outcome is undesirable;
- change a mutation's parameters after examining its evaluation outcomes;
- relabel a combined mutation to make it appear to belong to a more useful family.

All planned generated variants are accounted for. Any exclusion must follow a validity rule written before construction and must be reported with its reason. Failure to realize the intended support is a design-feasibility result, not permission to adapt the mechanism catalogue.

### 4.3 Mechanism selection principle

A mechanism is included because it varies a stated property of the solver in a scientifically defensible way, not because it is expected to generate a particular diagnostic concentration. The mechanism rationale and transformation are frozen before construction. The resulting diagnostic support is assessed against the frozen B1 conditions without outcome-informed alteration.

The retired eight-mechanism catalogue is not automatically revived. Its contents require fresh review against the new claim, parent population, exact B1 cells, and the anti-selection rules above.

---

## 5. New protected evaluation-set specification

The confirmatory claim requires a new protected evaluation set. No records are generated or accessed in v0.1.

### 5.1 Target domain and record-generation procedure

Before generating records, the design must specify:

- the formal input domain and admissibility constraints;
- the intended target distribution or explicit weighting scheme over input subdomains;
- the record-generation algorithm and exact version;
- all parameters, input-size ranges, and constraints;
- the method for obtaining and independently verifying expected outputs;
- the canonical record format and stable identifiers;
- the required record count and its design-based justification;
- the cryptographic commitments and custody procedure.

The record count is not assumed to be 78. It must be justified for the new target and frozen before any solver outcome is observed. It may not be chosen after inspecting variant performance.

### 5.2 Separation from exposed development material

The new protected set must be newly generated under its own frozen procedure. It must not be the existing 78-record development bank, a relabelled subset of it, or a collection copied from exposed development fixtures.

Before confirmatory use, an independent custodian must verify non-overlap against a predeclared inventory of exposed development and public fixtures, using exact canonical identity and a prespecified structural near-duplicate check. That check is a future, separately authorized custody operation; this document does not access the 78-record bank or its contents.

The existing 78 records are excluded from confirmatory fitting, scoring, calibration, and outcome claims for the new study. Any later development-only use would require its own declared scope and must remain separate from the confirmatory report.

### 5.3 Custody and access

The proposed custody procedure is:

1. Freeze and hash the record-generation code, environment, parameters, and seed commitment.
2. Generate the new records and expected outputs in a controlled environment administered by a designated custodian who is not involved in mutation design or outcome-informed model choices.
3. Store inputs, labels, and any oracle traces under access control. Preserve encrypted or otherwise protected originals, access logs, and integrity hashes.
4. Keep parent selectors, mutation implementers, and analysts from direct access to protected inputs and labels before the solver variants, source hashes, analysis code, and reporting rules are frozen.
5. Execute the prespecified evaluation in an isolated environment. The analyst receives only the outputs authorized by the frozen reporting plan.
6. Do not reveal record-level labels, input files, or oracle traces during iterative mutation or model tuning.
7. Record every access, export, failed execution, and authorized disclosure.

The precise custodian, technical access-control mechanism, environment, and output-disclosure policy remain open design items. If meaningful separation cannot be maintained, the study must not make the protected-confirmatory claim.

### 5.4 No leakage and no adaptive reuse

The protected-set seed, records, labels, and oracle traces must not enter mutation specifications, parent selection, mechanism tuning, software fixtures, or model selection. Any accidental exposure or access outside the approved protocol is recorded as a protocol deviation and assessed before the confirmatory claim is retained.

The protected set must be used only under one frozen evaluation procedure. Repeated attempts with changed variants, changed models, or changed scoring rules are not permitted unless a new design and analysis amendment explicitly defines the multiplicity and reuse consequences in advance.

### 5.5 Analysis-plan consequence

Because B1 v1.7 fixes the 78-record set, a new protected set requires a separately reviewed B1 amendment. That amendment must update, at minimum, the record index set, outcome notation, log-loss denominator, training/test row definitions, support and rank checks, any synthetic controls dependent on record count, reporting, and computational workload bounds. v1.7 must remain byte-for-byte unchanged as the accepted historical symbolic plan.

---

## 6. Parent and variant counts: derivation and feasibility

No final parent count, per-parent variant count, or total variant count is adopted in v0.1.

### 6.1 Structural lower bounds

The current accepted B1 cell rule gives a minimum of three distinct parent groups in a qualifying cell. If the proposed matched-within-parent target in §3.4 is adopted, each of at least three parents must contribute at least two variants to one common exact cell with within-parent \(C_D\) variation. The minimum for that cell is therefore six variants across three parents.

For \(P\) qualifying parents under that proposed target:

\[
P\ge3,\qquad V_c\ge2P.
\]

This bound applies to the variants in the qualifying common cell, not necessarily to every variant in the study. Additional variants may be required by the eventual mechanism set, but only if justified by the prespecified scientific design.

### 6.2 Counts not fixed by the support arithmetic

The following are not determined by \(G_c\ge3\), \(D_c\ge2\), and \(k\ge2\) alone:

- the number of selected parents above the minimum;
- the number of eligible cells;
- the number of mutation mechanisms;
- the number of variants outside the matched support cell;
- the record count in the protected evaluation set;
- power or precision for the conditional predictive claim.

Those quantities require separate scientific and design justification. The historical 90 and proposed 150 totals are not defaults and are not used as targets.

### 6.3 Design-only incidence feasibility

Once parent candidates and mechanism specifications have been reviewed, construct a design-only incidence table. Each planned variant is represented by its planned parent, mechanism identity, and intended design role. The table must show which variants are intended to contribute to each exact B1 cell, without assigning actual mutation operations or using outcome data.

The feasibility audit must report:

1. whether at least three distinct parents can contribute to an eligible cell;
2. whether the proposed within-parent pairs can be represented in the same exact cell, if §3.4 is adopted;
3. whether every intended held-out-parent fold retains \(G_{c,-g}^{\mathrm{train}}\ge2\), \(D_{c,-g}^{\mathrm{train}}\ge2\), and \(W_{C,c,-g}^{\mathrm{train}}>0\);
4. whether the planned cell structure preserves exact failure/unresolved totals and the required mutation-family or identity distinctions;
5. whether the planned design can satisfy the baseline-rank and concentration-independence checks once the exact model columns and protected record set are specified;
6. which conditions are logically guaranteed by the structure, which are only intended, and which cannot be established without later diagnostic data.

A design-only incidence table cannot establish realized \(C_D\), correctness, fit convergence, or predictive effect. If the realized post-construction diagnostics do not meet the frozen support conditions, no variant may be removed or replaced to manufacture eligibility. The primary B1 test may then be unavailable.

### 6.4 No sample-size or power claim

The lower bounds in §§2.5 and 6.1 are support minima only. They are not a sample-size justification, power guarantee, or assurance that the model will be estimable or useful. No power calculation, simulation, or model fitting is performed in v0.1.

---

## 7. Compatibility with the existing B1 and computational plans

This population specification is a new design layer. It does not rewrite or supersede the accepted B1 analysis plan or the computational-plan draft.

1. **B1 v1.7:** remains accepted and frozen as the symbolic plan for the exposed 78-record development bank. It does not automatically govern a new protected evaluation set.
2. **Computational plan v1.0:** remains an unreviewed computational draft. It cannot be treated as validated for a new record count, new parent/variant incidence, or changed design-matrix dimensions without an explicit update and review.
3. **Trigger (i):** the proposal that certified nonexistence of a finite enriched ordinary-model MLE activates trigger (i) remains unratified. This is a separate statistical decision.
4. **Consent provenance:** the joint-consent provenance gap remains open. Parent source licenses and provenance records do not automatically resolve that separate gap.
5. **Isolation and data access:** no execution environment or data-access authorization is granted by this document.
6. **Execution GO:** a separate explicit GO is required after the design, analysis-plan amendment, computational plan, software validation, consent/provenance, and isolation safeguards have been reviewed and accepted.

---

## 8. Open decisions for independent review

Claude's review should address the following points against the complete accepted B1 v1.7 text and the controlling predecessor specification:

1. **Controlling support rule.** Confirm the exact binding sources for full-cell eligibility and LOPO fold support. Identify whether any stricter frozen Rev 2.6 §5.2 M1 within-parent requirement remains binding, and provide its source path, commit, and content hash.
2. **Matched support.** Decide whether the §3.4 requirement (at least three parents, each with at least two variants in the same exact cell and different within-parent \(C_D\) values) is required for the new engineered-population claim, merely a desirable strengthening, or inconsistent with the frozen target.
3. **Fold derivation.** Check the set-based conditions in §3.2–3.4 against B1 v1.7 §3 item 3, including the distinction between full-population cell eligibility and support in every intended LOPO fold.
4. **Parent unit.** Review whether the proposed parent-lineage and fork rules are adequate to prevent duplicate implementations from inflating \(G_c\).
5. **Selection procedure.** Review the candidate-frame, provenance, rights, and outcome-blind selection rules.
6. **Mechanism selection.** Check that the mechanism-record requirements and anti-selection rules prevent choosing mechanisms to manufacture support.
7. **Protected evaluation set.** Review the custodian, independence, non-overlap, record-generation, access, and disclosure requirements.
8. **Analysis-plan amendment.** Identify the complete set of v1.7 provisions that must change before the new protected set can support a confirmatory claim.
9. **Count derivation.** Check the stated lower bounds and confirm that no fixed parent or variant total is smuggled in from the retired 90 or proposed 150 designs.

GPT will adjudicate Claude's findings. Any substantive change after review must be a new version with its own identity and review; v0.1 is not frozen by publication.

---

## 9. Explicit non-authorization

This draft authorizes no solver source acquisition, solver construction, source modification, mutation allocation, mutation generation, compilation, execution, diagnostic probing, benchmark execution, protected-set generation, bank access, outcome access, fitting, sampling, simulation, or analysis.

It is a document-only design specification for independent review. Passing review of this document would freeze only the population/design specification. All separate statistical, computational, consent, isolation, data-access, and execution gates remain in force.

**End of population and experimental design specification v0.1.**
