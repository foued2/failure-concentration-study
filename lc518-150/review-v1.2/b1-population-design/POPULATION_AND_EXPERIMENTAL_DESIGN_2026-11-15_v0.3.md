# LC518 Population and Experimental Design Specification v0.3

**Date:** 2026-11-15  
**Version:** 0.3  
**Status:** UNREVIEWED DESIGN-ONLY DRAFT  
**Prepared by:** GPT  
**Review sequence:** Claude independent review, then GPT adjudication  
**Repository branch:** \`gpt/b1-computational-plan-2026-11-14\`  
**Predecessor:** v0.2 at commit \`5da41cec3f27b28c80cd0cfedba614ce96cbccf3\`, blob \`d378de288e98c1191c9f1c0958e163f81cdacade\` (retained unchanged).
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
- No independent protected-set custodian has been identified or appointed. The protected-confirmatory route is currently blocked.
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

### 0.3 v0.2 → v0.3 adjudication summary

This revision addresses Claude's 2026-11-15 review of v0.2:

1. It distinguishes the stable mutation identity \(q\) from a predeclared within-identity realization setting \(\mathbf a(v)\), and requires actual realization-setting variation in every M1-si parent-cell contribution.
2. It requires each mutation record to specify the realization-setting dimensions, allowed range or levels, assignment schedule, expected functional and diagnostic implications, and a rationale independent of any desired \(C_D\) or support result.
3. It defines the realized-cell audit and shortfall rule. All planned variants are accounted for; exact-cell membership is determined after diagnostics; there is no post-diagnostic pair selection, replacement, tuning, or pooling.
4. It states that \(C_D\) may predict by proxying the within-identity realization setting. That can satisfy the stated B1 predictive question, but it cannot establish a direct or parameter-independent concentration effect. The future B1 amendment must include a parameter-proxy control and the corresponding sensitivity reporting.
5. It specifies the required elements of a prospective operating-parent-count justification. No numerical parent count is selected.

No parent or mechanism has been selected, no realization parameter has been assigned, and no project data, solver, diagnostic bank, or outcome has been accessed or evaluated.

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

A positive finding would support only this conditional claim for the studied engineered population and the declared evaluation domain. The primary B1 baseline is the exact cell \((q,Z,k,\ell)\); it does not automatically adjust for within-identity realization settings \(\mathbf a(v)\). Consequently, \(C_D\) may contribute predictive information by proxying a realization setting that also affects correctness. That remains a predictive result for the declared baseline, not evidence of a direct, causal, or parameter-independent effect of concentration. The new B1 amendment must preserve this distinction and include the proxy-pathway controls in §5.7. The finding would not establish a universal concentration law or generalization to naturally occurring solvers or independently developed parent implementations outside the study.

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

### 2.5 Parent count: support floor versus operating design

The frozen B1 cell rule requires at least three distinct parent groups in an eligible cell. The mathematical support floor is therefore:

\[
P\ge3.
\]

This is not an acceptable default operating sample size for a confirmatory study. With exactly three parents, there are only three LOPO test folds, and each training fold contains only two parents if the cell is represented in all three. Satisfying the cell-count threshold does not establish stable estimation, useful precision, or an informative held-out-parent comparison.

**Decision for this specification:** the final operating parent count must be justified above the bare three-parent floor. No exact number is selected in v0.3. Before design freeze, the justification must state:

1. the intended estimand and scope of parent-level inference, including the number of LOPO test parents and the fact that the accepted B1 randomization test is conditional on the observed parents rather than a parent-superpopulation test;
2. the prospective precision objective or minimum practically relevant predictive gain, or an explicit statement that the study is exploratory and has no confirmatory precision target;
3. the assumed distribution and plausible range of between-parent variation in parent-level predictive loss differences, with the source or elicitation basis for those assumptions;
4. the expected within-parent dependence among variants and the number of variants/realization settings expected to contribute to the qualifying exact cell;
5. plausible rates of cell support, M1-si realization, LOPO fold exclusions, score coverage, and fitting unavailability, with conservative as well as central scenarios;
6. sensitivity of the resulting precision and coverage to the parameter-proxy pathway in §5.7 and to plausible departures from the assumed parent heterogeneity;
7. the rule for selecting the operating (P) from those prospective scenarios, including the precision/coverage criterion it must meet.

The operating count must be selected before protected outcomes are generated or inspected, and it must not be chosen to maximize realized (C_D) support after diagnostics are observed. Any numerical simulation used to support the count requires its own authorization and must be based on declared assumptions, not outcomes from this study. If no defensible variance assumptions or precision objective can be supplied, no confirmatory operating count can be justified; the study must be labelled exploratory rather than presenting the three-parent floor as adequate. A count of three remains only the mathematical support boundary, not a sample-size recommendation.

## 3. B1 support derivation before mechanism selection

This section states the frozen B1 support constraints and the additional M1-si matched-within-parent design requirement adopted for this study. The additional requirement is a design choice, not a consequence of the B1 thresholds.

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

Equivalently, let \(\mathcal V_{g,c}\) be the set of version identifiers from parent \(g\) in cell \(c\), and let

\[
S_{g,c}=\{C_D(v):v\in\mathcal V_{g,c}\}
\]

be the **set of distinct concentration values** contributed by that parent in that cell. Repeated copies of the same value appear once in \(S_{g,c}\); \(|S_{g,c}|\) counts distinct values, not version records.

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

### 3.4 Adopted M1-si design requirement: same parent, same identity, same exact B1 cell

The study's stated scientific rationale for choosing an engineered population is to make matched comparisons within parent possible. This specification therefore **adopts a matched-within-parent requirement** as a new design rule. It is not a theorem implied by the B1 cell thresholds, and it is not inherited as binding authority from the old Rev 2.6 review draft.

The required support is specifically **M1-si**: within-parent variation among variants carrying the **same individual mutation identity**. It is not M1-ci, which allows a pair to differ in mutation identity and can therefore reflect identity-driven rather than same-identity variation.

For at least one common exact B1 cell

\[
c=(q,Z,k,\ell),
\]

at least three distinct parent groups must each contribute at least two of their own variants to that same cell, with at least two different exact \(C_D\) values within each contributing parent. Because \(q\), \(Z\), \(k\), and \(\ell\) are all fixed by the cell, the pair is matched on individual mutation identity, parent family, definite-failure total, and unresolved total.

For each parent \(g\) and cell \(c\), define the set of distinct within-identity realization settings

\[
\mathcal A_{g,c}=\{\mathbf a(v):v\in\mathcal V_{g,c}\},
\]

where the setting vector \(\mathbf a(v)\) is defined in §4.1. Formally, there must be a set of at least three distinct parents \(\mathcal G_c^{\mathrm{M1-si}}\) such that for every \(g\in\mathcal G_c^{\mathrm{M1-si}}\),

\[
|\mathcal V_{g,c}|\ge2,\qquad
|\mathcal A_{g,c}|\ge2,\qquad
|S_{g,c}|\ge2.
\]

Here \(\mathcal V_{g,c}\) is the set of version identifiers from parent \(g\) in cell \(c\), \(\mathcal A_{g,c}\) is the set of distinct predeclared realization-setting vectors, and \(S_{g,c}\) is the set of distinct realized \(C_D\) values. All three conditions are required: two source variants must differ in their declared within-identity realization setting and must actually realize different \(C_D\) values in the same exact cell. Merely having multiple versions or multiple settings is insufficient if \(C_D\) does not vary.

This adopted rule is stricter than the full-population B1 thresholds \(G_c\ge3\), \(D_c\ge2\), and \(k\ge2\). The full-population thresholds alone do not require within-parent pairs or same-identity variation. The stronger rule is chosen here because the engineered-population design is intended to obtain matched within-parent and within-identity comparisons, not merely cross-parent concentration variation.

If the condition holds for at least three parents, then after holding out any one of those qualifying parents, at least two other qualifying parents remain in the training set. Each remaining parent contributes at least two distinct \(C_D\) values to the same exact cell. This supplies the LOPO training support conditions in §3.2 for that cell, subject to the other B1 audit and model-rank requirements.

Define \(V_c\) as the total number of variant instances in cell \(c\):
\[
V_c=\sum_g|\mathcal V_{g,c}|.
\]
The structural lower bound is

\[
V_c\ge2G_c^{\mathrm{M1-si}},\qquad
G_c^{\mathrm{M1-si}}\ge3,
\]

so at least six variant instances must occupy the common cell when exactly three parents qualify. This is a lower bound for one support cell only. It is not the total-study sample size, and it does not imply five variants per parent, 30 parents, 90 versions, or 150 variants.

A design that reaches only B1 cell support but not this adopted M1-si target has not met the engineered study's matched-support design requirement. It must be reported as a design-feasibility shortfall, not repaired by pooling cells, changing identities, or selecting variants after seeing diagnostics.

### 3.5 Historical M1 provenance and authority ruling

The historical Rev 2.6 source has now been fetched from its historical review branch and its Git blob identity verified:

- Branch: \`gpt/lc518-150-analysis-review-2026-11-02\`
- Path: \`lc518-150/review-v1.2/analysis-revision-2026-11-02/ANALYSIS_SPEC_REVIEW_DRAFT.md\`
- Git blob SHA-1: \`c47760b1ca9121291f600db87b1e90665d57b8f6\`
- Relevant text: §5.1 item 5 and §5.2, “Fixed minimum within-parent support criterion”.

That review draft states a floor of at least three distinct parent groups, each contributing at least two of their own five matched versions to the same exact \((k_{\mathrm{fail}},k_{\mathrm{unresolved}})\) cell, with different \(C_D\) values. It also says that the less restrictive same-\(k\) count does not satisfy the exact-cell rule.

**Authority is separate from textual existence.** The file is a review draft, not an accepted B1 analysis plan. The contemporaneous GLM review labelled M1 a “proposal, pending owner”. The later \`B1_M1_JOINT_INCIDENCE_FEASIBILITY_SPEC_2026-11-12_v1.1.md\` explicitly records that the historical five-version M1 wording came from a review-only analysis specification and was **not ratified for a new symbolic population**; its generalized M1-gen form was a proposed operational change pending authority. Accepted B1 v1.7 does not itself add a within-parent M1 requirement.

Accordingly, the historical five-version M1 rule is **not binding on this new study by inheritance**. This v0.2 specification instead makes a new, explicit design choice: adopt the stronger **M1-si** requirement in §3.4, matched on the full B1 cell \((q,Z,k,\ell)\). This is deliberately stricter than the old \((k,\ell)\)-only wording because current B1 conditions on individual identity \(q\) and family \(Z\). It adopts the scientific rationale of within-parent variation without inheriting the historical five-version count or the old 30-parent/150-body architecture.

The source-provenance question is therefore closed for this v0.2 adjudication: the historical wording exists in the cited review-draft blob; it is not treated as binding authority for the new population. The adopted rule is the new study's own proposed design requirement and remains subject to Claude's review and GPT's final freeze.

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

No mutation mechanism is selected in v0.3. Mechanism selection follows, rather than precedes, acceptance of the support requirements in §3.

### 4.1 Required mechanism and within-identity realization record

A mutation identity \(q\) must be a stable, operationally defined transformation family. A version-specific realization setting is recorded separately as \(\mathbf a(v)\). The distinction is substantive:

- \(q\) defines the invariant transformation rule and its semantic class.
- \(\mathbf a(v)\) identifies how that same rule is instantiated in one version, through predeclared settings such as permitted locations, operands, thresholds, extents, or other operator parameters, where applicable.
- Different \(\mathbf a\) settings do **not** create a new \(q\) only when an independent technical review confirms that the core transformation and intended semantic class remain the same. If a setting changes the mutation's identity or mechanism class, it must receive a different \(q\) and cannot be used as an M1-si within-identity contrast.

For every proposed identity \(q\), the design record must contain:

1. Stable identity identifier, version, and a precise operational definition of the invariant transformation rule.
2. The solver or program property the transformation is intended to vary, with a technical rationale grounded in the implementation or algorithmic structure.
3. The exact transformation operator, including source locations or location-selection rule, operation order, and all fixed semantics.
4. The within-identity realization-setting vector \(\mathbf a\): every coordinate, type, unit, interpretation, permitted level or range, allowed combination, and any constraints between coordinates. Categorical settings must have a closed list of levels; continuous settings must have finite declared bounds and a prespecified value-generation rule.
5. A predeclared assignment schedule for realization settings across eligible parent implementations. The schedule must be reproducible and fixed before any diagnostic outcome is observed. For each parent intended to contribute to M1-si, at least two distinct realization settings must be planned under the same \(q\).
6. The reason the different settings remain realizations of the same \(q\), together with an independent technical review of that identity boundary. Settings that change the transformation's semantic class must not be retained under one \(q\) merely to create M1-si support.
7. The expected functional effect of changing each setting, including the code paths, behaviors, or correctness conditions it is expected to affect, based on source-level or algorithmic reasoning.
8. The expected qualitative diagnostic implications, if they can be justified: which broad failure manifestations or diagnostic strata may be affected and why. This is a mechanistic expectation, not a predicted \(C_D\), \(k_{\mathrm{fail}}\), \(k_{\mathrm{unresolved}}\), or exact-cell assignment. Where the diagnostic implication is genuinely unknown, record it as unknown rather than inventing a directional claim.
9. The technical rationale for the permitted parameter range or levels, including why boundary and intermediate settings are scientifically meaningful. The range must not be chosen by searching for settings that produce desired concentration values or support.
10. The parent implementations to which the identity and each realization setting apply, plus applicability restrictions.
11. Whether the version contains one transformation or a prespecified combination. Combined transformations must have their own identity and cannot be concealed as a realization parameter.
12. Exact source-level realization metadata for every planned variant: parent ID, \(q\), \(\mathbf a(v)\), variant ID, source revision, reproducible transformation record, exact diff, and hashes of the resulting source artifact.
13. A predeclared validity, build, and provenance check, including rules for a setting that is inapplicable, fails to produce a distinct source change, or changes the identity class.
14. The relationship between \(q\), \(\mathbf a(v)\), and the frozen B1 cell variables, together with the predictive-interpretation limitation in §5.7.
15. A statement explaining why the identity and its realization-setting range are scientifically relevant independently of any desired \(C_D\), failure total, unresolved total, exact cell, or correctness outcome.

**M1-si realization requirement.** A pair of versions can be considered same-identity variants only when they share the same parent \(g\) and stable identity \(q\), use different predeclared realization-setting vectors \(\mathbf a\), pass the identity-boundary review, and produce distinct source artifacts under the frozen validity checks. This makes the design contrast operational. It does not guarantee that the resulting versions will share an exact diagnostic cell or have different \(C_D\) values; those are realized properties audited only after a separately authorized diagnostic stage.

The presence of a parameter is not itself evidence of a scientifically meaningful variant. A parameter introduced only to make \(C_D\) vary, or whose only rationale is to satisfy M1-si, is prohibited.

### 4.2 Anti-selection rules

Mechanisms must not be selected, tuned, retained, or removed because they make the B1 support conditions pass or because they yield a preferred concentration or correctness result.

The design must not:

- choose mechanisms, identities, realization-setting dimensions, parameter levels, or parameter values after inspecting realized \(C_D\), failure totals, unresolved totals, or exact-cell membership;
- select realization settings because they are expected to attain a target \(C_D\), \(k_{\mathrm{fail}}\), \(k_{\mathrm{unresolved}}\), or qualifying cell;
- backfill a missing cell by inventing a new identity or realization setting after diagnostic outcomes are known;
- select only the most favourable pairs from a larger collection of realized variants;
- drop an inconvenient variant because its \(C_D\) or correctness outcome is undesirable;
- change a mutation's parameters after examining diagnostic or evaluation outcomes;
- relabel a combined mutation or broaden \(q\) after construction to make variants appear to share one identity.

Before diagnostics, freeze the complete list of planned variants and their parent, identity, realization-setting vectors, validity rules, source transformations, and hashes. Every planned variant must remain in the accounting register. Any invalid or inapplicable variant is classified only under a rule written before construction and is reported with its reason; it is not replaced.

Failure to realize the intended support is a design-feasibility result, not permission to adapt the mechanism catalogue or realization-setting schedule.

### 4.3 Mechanism selection principle

An identity \(q\) is included because its invariant transformation varies a stated solver property in a scientifically defensible way. Its within-identity realization settings are included because they create controlled, reproducible variants of that same transformation family. Neither the identity nor its settings may be selected because they are expected to generate a particular concentration value or a passing support cell. The expected functional and diagnostic implications are documented from mechanistic reasoning before construction, while the actual \(C_D\), exact cell, and support are allowed to remain uncertain. The complete transformation and realization schedule are frozen before construction; realized support is assessed afterward without outcome-informed alteration.

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

**Current gate status: NOT SATISFIED. No independent custodian has been identified or appointed, and no access mechanism has been demonstrated.** No person or institution is named in v0.2 because none has been evidenced in the project record. The project owner, mutation designers, solver constructors, outcome analysts, and AI reviewers cannot be relabelled as an independent custodian merely by assigning them a different project role.

Before this population-and-design specification can be frozen for a protected-confirmatory study, the project must identify an actual human custodian or institution outside the variant-construction and outcome-analysis team and record:

- identity, institution, role, and written acceptance of the custodial responsibility;
- a conflict-of-interest and independence attestation;
- the exact access-control and storage mechanism, including who can read protected inputs, labels, and oracle traces;
- the independent generation and non-overlap verification procedure;
- the execution arrangement and the exact output interface available to analysts;
- access logging, retention, incident handling, and disclosure rules.

The custodian must not be a solver constructor or an analyst making outcome-informed design or modelling decisions. AI reviewers are not custodians and cannot hold or attest to human institutional responsibility.

Until a qualified custodian and working access mechanism are documented, the new protected set cannot be treated as protected and the confirmatory claim is blocked. If no genuinely independent custodian can be secured, this design cannot make the protected-confirmatory claim; the team must either stop that claim or explicitly redesign the study as non-confirmatory. There is no waiver by wording alone.

### 5.4 No leakage and no adaptive reuse

The protected-set seed, records, labels, and oracle traces must not enter mutation specifications, parent selection, mechanism tuning, software fixtures, or model selection. Any accidental exposure or access outside the approved protocol is recorded as a protocol deviation and assessed before the confirmatory claim is retained.

The protected set must be used only under one frozen evaluation procedure. Repeated attempts with changed variants, changed models, or changed scoring rules are not permitted unless a new design and analysis amendment explicitly defines the multiplicity and reuse consequences in advance.

### 5.5 Analysis-plan consequence

Because B1 v1.7 fixes the 78-record set, a new protected set requires a separately reviewed B1 amendment. That amendment must update, at minimum, the record index set, outcome notation, log-loss denominator, training/test row definitions, support and rank checks, any synthetic controls dependent on record count, reporting, and computational workload bounds. v1.7 must remain byte-for-byte unchanged as the accepted historical symbolic plan.

### 5.6 Outcome-side variation risk and non-adaptive reporting

The M1-si design requirement creates exposure-side variation in \(C_D\). It does **not** guarantee variation in held-out correctness. Even a design that fully satisfies B1 and M1-si may produce identical correctness outcomes across variants, or no outcome discordance in the strata used by the secondary association analysis. Diagnostic-support feasibility and outcome-side informativeness are separate properties.

The protected evaluation procedure and the B1 analysis-plan amendment must therefore predeclare an outcome-side reporting audit, including:

1. the count of correct and incorrect outcomes across the full scored version-record set;
2. outcome variation by parent and by exact B1 cell;
3. for each exact cell and canonical record, whether correctness is discordant across its contributing variants;
4. the number of \((c,r)\) strata that contain both outcome classes and within-stratum \(C_D\) variation;
5. any outcome patterns that trigger a declared fitting failure or test unavailability under the accepted B1 fitting rules.

This audit is **not** a parent-selection rule, mutation-selection rule, cell-eligibility condition, or admissibility-key component. It must not be used to drop variants, parents, cells, or records, to add variants, to reassign mutations, or to change the protected set after the outcomes are observed.

The secondary P-assoc procedure can obtain information only from \((c,r)\) strata that contain outcome discordance across versions as well as within-stratum exposure variation. Strata without outcome discordance must be counted and reported as non-contributing; they are not evidence of a null association and must not be silently omitted. The primary P-pred procedure remains governed by its frozen model, common scored-set, fit, and availability rules. Any fit failure is handled under the applicable B1 plan; there is no outcome-driven fallback or replacement.

If correctness is constant across the relevant scored variants, the report must say that the realized outcomes supplied no variation for the intended predictive contrast. That result is not to be converted into a claim that concentration has no predictive value in other populations or evaluation sets. Conversely, outcome variation is not evidence of a concentration effect by itself. No outcome-side criterion may be invented after the protected data are seen.

### 5.7 Within-identity realization settings and the predictive-interpretation boundary

Let \(\mathbf a(v)\) denote the frozen realization-setting vector from §4.1. This is a construction variable, not an additional component of the accepted exact B1 cell:

\[
c(v)=(q,Z,k,\ell).
\]

The primary B1 comparison in v1.7 is the predictive comparison against this exact-cell baseline. It does not automatically condition on \(\mathbf a(v)\). Accordingly, if a realization setting affects both the diagnostic failure distribution and held-out correctness, \(C_D\) may carry predictive information by acting as a proxy for that setting.

That pathway is **within the declared predictive target** of incremental information beyond the exact cell, provided the future B1 amendment retains that target. It is not evidence that concentration itself causes correctness, nor that \(C_D\) adds information independently of the realization setting. A positive result must not be described as a direct concentration mechanism or as parameter-independent.

Because the within-identity setting is deliberately varied to make distinct versions of the same \(q\), the new B1 amendment must address this pathway explicitly before protected outcomes are accessed. At minimum, it must:

1. preserve the primary exact-cell target and state explicitly whether \(\mathbf a(v)\) remains outside the primary baseline, as in v1.7, or whether a different target conditioning on \(\mathbf a(v)\) is proposed. It must not silently change the estimand;
2. add a predeclared **N5 realization-parameter proxy control** in which \(\beta_C=0\), while the realization setting affects diagnostic failure placement and held-out correctness at fixed \((q,Z,k,\ell)\). The control must report when \(C_D\) predicts through this proxy pathway. Such a result is not a false positive for the broad predictive target, but it would be a false attribution if described as a direct concentration effect;
3. report the predeclared relationship between \(\mathbf a(v)\) and \(C_D\), and between \(\mathbf a(v)\) and held-out correctness, by identity, parent, and exact cell;
4. include a labelled sensitivity model that adjusts for \(\mathbf a(v)\), when its coding and within-setting \(C_D\) support make that sensitivity estimable. Report rank, collinearity, and loss of support explicitly. If \(\mathbf a(v)\) and \(C_D\) are inseparable under the realized design, the parameter-independent contribution is **not identifiable**; do not claim it and do not silently revert to a different primary target;
5. retain the v1.7 restriction that outcome patterns, fit stability, and score favourability cannot define the permutation/admissibility set. Any revised admissibility rule must be declared in the B1 amendment before evaluation.

This specification therefore treats \(\mathbf a(v)\) as a required and reported design dimension, while retaining the current B1 predictive target as conditional on the exact cell rather than as a causal or parameter-adjusted effect. If the scientific objective changes to concentration information *beyond* the within-identity realization settings, that is a different estimand and requires a separately reviewed design and analysis amendment. It cannot be inferred from the present target.

## 6. Parent and variant counts: derivation and feasibility

No final parent count, per-parent variant count, or total variant count is adopted in v0.3.

### 6.1 Structural lower bounds

The accepted B1 cell rule gives a mathematical minimum of three distinct parent groups in a qualifying cell. The adopted M1-si design requirement in §3.4 adds that each of at least three parents must contribute at least two of its own variants to one common exact \((q,Z,k,\ell)\) cell, with different within-parent \(C_D\) values. The minimum for that cell is therefore six variants across three parents.

For \(P\) qualifying parents under the adopted M1-si requirement:

\[
P\ge3,\qquad V_c\ge2P.
\]

This bound applies to the variants in the qualifying common cell, not necessarily to every variant in the study. Additional variants may be required by the eventual mechanism set, but only if justified by the prespecified scientific design. The exact parent count must also satisfy §2.5's operating-sample justification; three is not accepted as a confirmatory operating target by arithmetic alone.

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
2. whether at least three parents can each contribute an M1-si pair with two distinct \(C_D\) values in the same exact \((q,Z,k,\ell)\) cell;
3. whether every intended held-out-parent fold retains \(G_{c,-g}^{\mathrm{train}}\ge2\), \(D_{c,-g}^{\mathrm{train}}\ge2\), and \(W_{C,c,-g}^{\mathrm{train}}>0\);
4. whether the planned cell structure preserves exact failure/unresolved totals and the required mutation-family or identity distinctions;
5. whether the planned design can satisfy the baseline-rank and concentration-independence checks once the exact model columns and protected record set are specified;
6. which conditions are logically guaranteed by the structure, which are only intended, and which cannot be established without later diagnostic data.

A design-only incidence table cannot establish realized \(C_D\), correctness, fit convergence, or predictive effect. If the realized post-construction diagnostics do not meet the frozen support conditions, no variant may be removed or replaced to manufacture eligibility. The primary B1 test may then be unavailable.

### 6.4 No sample-size or power claim

The lower bounds in §§2.5 and 6.1 are support minima only. They are not a sample-size justification, power guarantee, or assurance that the model will be estimable or useful. No power calculation, simulation, or model fitting is performed in v0.3. The operating parent count remains open and must be justified before design freeze; the three-parent support floor is not a substitute for that justification.

### 6.5 Realized-cell audit and shortfall rule

Exact-cell membership cannot be known from the parent and mutation design alone. The design can predeclare \(q\), the realization settings \(\mathbf a(v)\), the complete variant roster, and each source transformation, but the realized \(k_{\mathrm{fail}}\), \(k_{\mathrm{unresolved}}\), and \(C_D\) are known only after the diagnostic stage. This uncertainty is accepted in advance.

After a separately authorized diagnostic stage, the support audit must:

1. account for every planned variant, including invalid, inapplicable, or non-executable variants under the frozen validity rules;
2. derive each valid variant's exact \((q,Z,k,\ell)\) cell and \(C_D\) from the frozen diagnostic outcomes;
3. enumerate all variants in every realized parent-cell set \(\mathcal V_{g,c}\), all distinct realization settings \(\mathcal A_{g,c}\), and all distinct \(C_D\) values \(S_{g,c}\);
4. calculate B1 full-population and fold-level support separately from M1-si support;
5. determine M1-si by the frozen set conditions in §3.4, across the complete planned and valid variant register. Pair selection after seeing diagnostics is not permitted;
6. report every failure of B1, M1-si, and LOPO fold support, including which parents, cells, settings, and criteria were absent.

**Shortfall disposition is frozen as follows:**

- If no exact cell satisfies M1-si across at least three parents, report **M1-si NOT REALIZED / MATCHED-SUPPORT DESIGN FAILURE**. Do not claim that the adopted engineered matched-support design was achieved.
- If B1 support is also absent, the B1 concentration-specific analysis is unavailable for insufficient diagnostic support.
- If B1 support exists but M1-si does not, report the B1 and M1-si results separately. B1-only results cannot be relabelled as successful M1-si evidence. A B1-only confirmatory analysis may proceed only if a future B1 amendment explicitly defines that alternative in advance; it cannot be chosen after seeing the shortfall.
- If M1-si is realized but particular LOPO fold-cell conditions fail, apply the accepted B1 fold-audit and exclusion rules exactly. No cell is repaired by changing the scored set, pooling, zeroing the slope, or replacing a variant.
- No variants may be added, removed, reassigned, retuned, or replaced after diagnostic outcomes are observed to make support pass. A redesigned study requires a new versioned design, new independent review, and a separate authorization. Its data must not be pooled with the original confirmatory attempt as though it were one frozen design.

A realized support shortfall is a design-feasibility result, not evidence that concentration has no predictive value. The outcome report must distinguish **B1 support**, **M1-si realization**, **LOPO estimability**, and **outcome-side informativeness** as separate statuses.

## 7. Compatibility with the existing B1 and computational plans

This population specification is a new design layer. It does not rewrite or supersede the accepted B1 analysis plan or the computational-plan draft.

1. **B1 v1.7:** remains accepted and frozen as the symbolic plan for the exposed 78-record development bank. It does not automatically govern a new protected evaluation set.
2. **Computational plan v1.0:** remains an unreviewed computational draft. It cannot be treated as validated for a new record count, new parent/variant incidence, or changed design-matrix dimensions without an explicit update and review.
3. **M1-si:** the same-identity, same-full-cell matched-support requirement in §3.4 is a new design choice in this specification. It is not represented as a requirement of B1 v1.7 itself and does not inherit the old five-version count.
4. **Protected custodian:** no independent custodian has been identified or appointed. This is a current blocker to freezing and implementing the protected-confirmatory route, not a routine execution detail.
5. **Within-identity parameter:** the future B1 amendment must address the \(\mathbf a(v)\)-proxy pathway and include the N5 control and parameter-adjusted sensitivity required by §5.7.
6. **Outcome-side variation:** the B1 amendment must include the outcome-side reporting audit in §5.6 without making outcome variation a design-selection or admissibility criterion.
7. **Trigger (i):** the proposal that certified nonexistence of a finite enriched ordinary-model MLE activates trigger (i) remains unratified. This is a separate statistical decision.
8. **Consent provenance:** the joint-consent provenance gap remains open. Parent source licenses and provenance records do not automatically resolve that separate gap.
9. **Isolation and data access:** no execution environment or data-access authorization is granted by this document.
10. **Execution GO:** a separate explicit GO is required after the design, analysis-plan amendment, computational plan, software validation, consent/provenance, custodian appointment, and isolation safeguards have been reviewed and accepted.

## 8. Open decisions for independent review

Claude's review should address the following points against the complete accepted B1 v1.7 text and the controlling predecessor specification:

1. **M1-si realization condition.** Verify that \(\mathbf a(v)\) is operationally separated from \(q\), and that requiring at least two distinct realization settings plus two distinct realized \(C_D\) values in each of at least three parent-cell contributions is coherent.
2. **Identity boundary.** Challenge the rule for deciding whether parameter changes remain within the same \(q\) or constitute a different mutation identity. Verify that the required independent technical review is sufficient.
3. **Mechanism control record.** Review whether §4.1 requires enough information about parameter domains, allowed levels, expected functional effects, qualitative diagnostic implications, reproducibility, and source diffs without selecting settings to target \(C_D\).
4. **Predictive proxy interpretation.** Review §5.7 against B1 v1.7's exact-cell baseline and conditional-randomization null. In particular, check that an \(\mathbf a\)-to-\(C_D\)-to-correctness proxy pathway is correctly treated as predictive information under the declared baseline but not as a direct concentration effect.
5. **N5 control.** Review the requirement for a predeclared within-identity realization-parameter proxy control and an adjusted sensitivity, including when that sensitivity is not estimable.
6. **Realized-cell shortfall.** Verify that §6.5 gives a deterministic no-repair rule, accounts for every planned variant, prevents post-diagnostic pair selection, and distinguishes B1 support from M1-si realization and LOPO estimability.
7. **Parent count.** Review the prospective precision/stability checklist in §2.5. Confirm that it does not imply a parent count or power claim without defensible assumptions.
8. **Custodian.** Confirm that the protected-confirmatory route remains blocked until an independent human or institutional custodian and functioning access mechanism are documented.
9. **Parent unit and selection.** Review the parent-lineage, fork, candidate-frame, provenance, rights, and outcome-blind selection rules.
10. **Protected evaluation set.** Review non-overlap, record generation, access, execution, and disclosure requirements.
11. **Analysis-plan amendment.** Identify the complete set of v1.7 provisions that must change before the new protected set and realization-setting design can support a confirmatory claim.
12. **Count derivation.** Check the structural lower bounds and confirm that no fixed parent or variant total is smuggled in from the retired 90 or proposed 150 designs.

GPT will adjudicate Claude's findings. Any substantive change after review must be a new version with its own identity and review; v0.3 is not frozen by publication.

## 9. Explicit non-authorization

This draft authorizes no solver source acquisition, solver construction, source modification, mutation allocation, mutation generation, compilation, execution, diagnostic probing, benchmark execution, protected-set generation, bank access, outcome access, fitting, sampling, simulation, or analysis.

It is a document-only design specification for independent review. Passing review of this document would freeze only the population/design specification. All separate statistical, computational, consent, isolation, data-access, and execution gates remain in force.

**End of population and experimental design specification v0.3.**
