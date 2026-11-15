# LC518 Population and Experimental Design Specification v0.8

**Date:** 2026-11-15  
**Version:** 0.8  
**Status:** UNREVIEWED DESIGN-ONLY DRAFT  
**Prepared by:** GPT  
**Review sequence:** Claude independent review, then GPT adjudication  
**Repository branch:** \`gpt/b1-computational-plan-2026-11-14\`  
**Predecessor:** v0.7 at commit \`32bebbff605c2204f24ad400ba6d8d48bab81235\`, blob \`81f4a4dba051883916958713cfa9ee1acd69fc03\` (retained unchanged). The later branch commits \`48898f09bc5a9bb0ef2dad47c2edb445d367439a\` and \`b9e095f871eecb838f59f4c801d801869c18b8e7\` add and newline-correct the v0.7 handoff; neither changes the v0.7 specification blob.
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

The controlling symbolic feasibility specification is also:

- **Rev 1.4 Amendment E:** commit \`b8b8af042c16eeb9e02077c781ab05c582eeb65d\`, blob \`3728146356a74363a94fe75a87fd06c483954ee2\`, SHA-256 \`C19FC85735072BB8821BD6217B7A2E481BD070B122384026C22BAB358CA03DA6\`.
- **GPT acceptance record for Rev 1.4 Amendment E:** commit \`ca15a29bd25c4c9c2293394f67cb19e1a18f34bd\`, blob \`074b40980eb96d164cd8411c8995bb1db4af0d46\`.

Rev 1.4 Amendment E is accepted for the symbolic B1/M1 feasibility specification; its acceptance record distinguishes acceptance from a separate formal freeze. B1 v1.7 is accepted and frozen as a symbolic analysis plan by its own acceptance record. Neither acceptance is an execution GO. Where a source-level population restriction in this document goes beyond those statistical definitions, it is labelled as a new design choice, not attributed to the predecessor specifications.

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

### 0.4 v0.3 → v0.4 adjudication summary

This revision resolves Claude's 2026-11-15 findings as follows:

1. **Option B is adopted.** The primary predictive target remains the accepted B1 exact-cell comparison: incremental prediction from \(C_D\) beyond \(c=(q,Z,k_{\mathrm{fail}},k_{\mathrm{unresolved}})\). The primary model does **not** condition on the within-identity realization setting \(\mathbf a(v)\).
2. The claim is narrowed accordingly. A positive result may include predictive information carried by \(C_D\) as a proxy for \(\mathbf a(v)\). It is not evidence of a direct, causal, or parameter-independent concentration effect.
3. Option A, which would condition the primary model on \(\mathbf a(v)\), is not adopted. It changes the estimand and requires a different support design. The current M1-si structure varies \(\mathbf a\) and \(C_D\) together; it does not guarantee \(C_D\) variation while \(\mathbf a\) is held fixed.
4. The \(q/\mathbf a\) boundary is made objective through a pre-registered operator-class fingerprint, a closed list of permitted variable fields, a deterministic structural check, and a diagnostic-blind review before any diagnostic stage.
5. For this new engineered population, \(q\) is proposed as an **operationally defined mutation-operator class** and \(\mathbf a(v)\) records the permitted realization settings within that class. This coding must be explicitly accepted in the separate B1 amendment; it does not silently redefine the frozen v1.7 plan.
6. N5 remains a proxy-pathway stress control. It is not null calibration for the broad B1 permutation null; its purpose is to show how a positive predictive result can arise with no direct \(C_D\) effect.

No parent, operator class, realization setting, variant, or parameter value has been selected. No solver, diagnostic, evaluation, bank, or outcome has been accessed or constructed.

### 0.5 v0.4 → v0.5 adjudication summary

This revision resolves Claude's 2026-11-15 review of v0.4:

1. It closes the site-selection context gap. A matching AST fingerprint alone is insufficient to treat different source locations as permitted realizations of the same \(q\). Within each parent, candidate sites must also have matching, predeclared static execution-context signatures under §4.1.5.
2. The context test is parent-relative. It does not require different parent implementations to contain the same function names or identical call graphs. It requires the alternative sites used for a within-parent M1-si comparison to occupy the same normalized context class within that parent.
3. Site selection cannot be justified by dynamic hot-path frequency, diagnostic results, \(C_D\), correctness, or protected outcomes. When the static context cannot be resolved, site selection is not an admissible realization field for that \(q\); the site must be fixed or the design must be amended before construction.
4. **Decision-history correction:** Claude's v0.3 review recommended Option A, conditioning the primary analysis on \(\mathbf a(v)\), while stating that Option B was acceptable if the claim explicitly named the realization-setting limitation. GPT independently selected Option B for v0.4. This revision preserves that disagreement. It does not describe Option B as Claude's preferred choice or as a joint GPT/Claude consensus.
5. A separate Claude review handoff carries the domain clarification that LC518 terminology refers to source-code transformations and engineered software variants, not biology. The clarification does not alter the scientific design.

The Option B predictive target, N5 proxy-pathway control, operator-class invariants, and other v0.4 provisions are retained except where expressly amended below. No parent, operator class, site, realization setting, variant, or parameter value has been selected. No solver, diagnostic, evaluation, bank, or outcome has been accessed or constructed.

### 0.6 v0.5 → v0.6 adjudication summary

This revision resolves Claude's 2026-11-15 review of v0.5:

1. **Canonical equivalence (blocker):** “same normalized signature” is replaced by a pinned canonical encoding and exact byte-equality rule. The canonicalization algorithm, graph model, serialization, analysis configuration, parent source digest, and operator-class fingerprint are identified in a content-addressed analysis manifest. Exact canonical-byte equality is reflexive, symmetric, and transitive; a hash is an index and integrity check, not a substitute for comparing the canonical bytes.
2. **Control-flow position (blocker):** the selected site is a distinguished node in a rooted, edge-labelled canonical control-flow graph. The graph is anchored to function/region entries, normal and exceptional exits, loop headers/latches, and branch/exception edges. Its canonical form preserves the target's position relative to these structures; dominance, post-dominance, frontiers, loop relations, and edge-distance descriptors are also encoded.
3. **Value-level context (blocker):** the context signature now includes a sound, pinned abstract interpretation of the operator's relevant input values and controlling path conditions. Site selection is permitted only when candidate sites have the same canonical abstract input and transfer/effect profile for each shared realization setting. A top/unknown or otherwise unresolved value summary fails closed for site selection. Deliberate threshold/literal parameter variation remains permissible as an explicit \(\mathbf a\)-coordinate at a fixed site; its relation to the abstract input range and its abstract effect profile must be recorded. This preserves the distinction between intended parameter variation and a supposedly neutral relocation to a different semantic context.
4. **Call-graph role (recommendation):** the call-graph check is retained as a build-resolution and dispatch-integrity check. Because sites being compared are within the same enclosing program entity, the function-level call-graph node is ordinarily shared; the check guards against unresolved overloads, virtual dispatch, context-sensitive cloning, and tool/configuration drift rather than serving as a substitute for site-position comparison.
5. **Candidate pool (recommendation):** the complete site-search frame and every candidate site, including rejected sites and reasons, must be frozen and hashed before construction. The inventory is complete relative to the explicitly declared source scope and syntactic search rule.
6. **Tool configuration (recommendation):** compiler/front-end/parser, build and preprocessing configuration, call-graph mode, points-to/alias configuration, CFG/exception model, abstract domain and analysis options are pinned in the analysis manifest whose digest enters each \(H_{g,q}(s)\).
7. **Single-mutation scope (recommendation/adopted design restriction):** each variant receives exactly one mutation-operator invocation \(q\). A single invocation may require coordinated edit hunks that jointly implement that one operator; a variant may not combine independent operator invocations. The transformation-interaction check is therefore limited to the coordinated edits within one operator invocation and conflicts with other predeclared candidate edits in the same parent source.
8. **Commit provenance correction:** the v0.5 file's last content-changing commit is \`8f9aa28968257ed9d391de2bed2056ef9648ba8a\`; the later commit \`667fbca8d3b588068cf0807002422f46868e0b44\` is the branch snapshot that adds the handoff. Both expose the same v0.5 blob \`434551c76f7dffd5f1e0b03e20491df969ff10ce\`. This version records those roles separately.

The Option B exact-cell predictive target, its realization-proxy limitation, N5 treatment, the non-waivable operator invariants, and the governance gates are retained. No parent, operator class, candidate site, realization setting, variant, or parameter value has been selected. No solver, diagnostic, evaluation, bank, or outcome has been accessed or constructed.

### 0.7 v0.6 → v0.7 adjudication summary

This revision adjudicates Claude's provisional 2026-11-15 review of v0.6. Claude could not retrieve the full v0.6 specification or the Rev 1.4 Amendment E text during that review; its findings are therefore treated as provisional. GPT independently re-fetched and reviewed the full v0.6 text and the accepted B1/M1 predecessor artifacts.

1. **Canonicalization (blocker):** canonical graph labelling must produce one unique canonical representative for every isomorphism class of the declared typed, directed, edge-labelled graph. The selected implementation, graph model, node/edge labels, canonical serializer, and source/symbol normalization rules are pinned in a per-parent profile. Macro expansion, generated code and source-location treatment are now explicit.
2. **Control-flow position (blocker/recommendation):** the canonical CFG must preserve target position relative to all language-relevant control transfers. The required edge inventory now expressly covers exception propagation, cleanup/finally/RAII, non-local jumps, coroutines/async flow and other language-specific transfers. Unsupported or unresolved control flow fails closed.
3. **Abstract-domain selection (blocker):** the design now separates the frozen analysis contract from its later per-parent toolchain instantiation. Operator-specific abstract-domain adequacy is selected from the declared input contract and operator semantics before candidate-site enumeration. It cannot be refined in response to candidate counts, signatures or preferred site availability. Unknown or unresolved relevant values remain inadmissible for site relocation.
4. **Parameter variation (recommendation):** every intended parameter level must be accompanied by a predeclared abstract input-range relation and abstract transfer/effect summary. This makes level-to-level changes explicit without confusing them with site relocation.
5. **Call graph (recommendation):** the call-graph component is retained as a symbol/overload/dispatch-resolution integrity check. Its role is not to duplicate the same-enclosing-function condition or replace target-position comparison.
6. **Candidate inventory (recommendation):** the syntactic search frame and eligibility predicates are frozen before enumeration; every matching candidate is enumerated, and rejected/unresolved sites and reasons are retained. The completed inventory is hashed before construction.
7. **Profile sequencing (blocker):** the design freeze fixes the static-analysis contract and tool-selection rules. After a parent/source revision is selected, the concrete language/build/tool/domain profile is instantiated and hashed before candidate-site enumeration. The profile is not selected by examining candidate results.
8. **One operator invocation per variant (recommendation/adopted restriction):** the one-invocation rule is retained as a new population-design restriction. It is compatible with the B1 identity coordinate \(q\), but is not represented as a requirement explicitly imposed by B1 v1.7 or Rev 1.4. Multiple coordinated edit hunks may implement one atomic operator invocation; independent invocations cannot be composed in one variant.
9. **B1/M1 authority:** accepted Rev 1.4 Amendment E and its separate acceptance record, together with accepted/frozen symbolic B1 v1.7 and its acceptance record, remain unchanged. v0.7 does not modify either.

No parent, operator class, source site, realization setting, variant or parameter value has been selected. No solver, diagnostic, evaluation, bank or outcome has been accessed or constructed.

### 0.8 Repository identity and predecessor provenance

The v0.6 specification content is identified by blob \`367f3fc12956a546e85b39a749bbaf16b8a95fb4\`. Its last content-changing commit is \`66c6117d65b20179c29fb95bb9d43ed87de2f75b\`. The later branch-snapshot commit \`a592fd532e6e7b5e281af955d5553639096b4611\` contains the same v0.6 specification blob and adds the final-newline correction to the v0.6 review handoff. The v0.7 predecessor pointer uses the last content-changing commit and exact v0.6 blob; the branch-snapshot role is recorded separately in the header.

The accepted predecessor identities are unchanged: Rev 1.4 Amendment E blob \`3728146356a74363a94fe75a87fd06c483954ee2\` with acceptance record blob \`074b40980eb96d164cd8411c8995bb1db4af0d46\`; B1 v1.7 blob \`8c666e501a31726c728447d155045c0b20adc178\` with acceptance record blob \`ea51d72f4f85c5d832d72add561b4c93472c364a\`.

### 0.8 v0.7 → v0.8 adjudication summary

This revision adjudicates Claude's 2026-11-15 review of v0.7. GPT independently retrieved and reviewed the complete v0.7 specification, including §§6.4–9 which Claude's fetch had not returned. Those unseen sections contain no additional scientific blocker: they retain the no-power-claim boundary, deterministic realized-cell shortfall, accurate B1/computational-plan separation, open custodian/trigger-(i)/consent gates, and explicit non-authorization.

1. **Site-context equivalence (blocker):** the complete enclosing-function CFG with a marked TARGET is replaced as the decisive equivalence object by a deterministic target-centred dependency/context slice. The slice preserves all operator-relevant data, control, exception, cleanup, state and effect dependencies and relative position to relevant control/loop/exit anchors, while excluding unrelated function structure and absolute source addresses. Two sites can therefore match without an automorphism of the entire function CFG. This does not guarantee site admissibility; it removes an unintended whole-function symmetry restriction. Site relocation remains optional. No admissibility rate is claimed before the predeclared Stage 2 analysis.
2. **Floating-point semantics (blocker):** float-typed operators are not silently treated as rational arithmetic. The profile must model the applicable IEEE format, rounding, subnormals, signed zeros, infinities, NaNs, conversion and exception semantics, and compiler contraction/reassociation/fast-math settings. Float values in canonical data use typed bit-pattern or exact abstract encodings, never JSON floating-point numbers. If sound modelling is unavailable, float-sensitive site relocation and parameter variation are inadmissible.
3. **External-call soundness (blocker):** every external call that can affect the context must have a versioned sound summary. Without one, the analysis conservatively havocs its return value and all potentially affected externally reachable/global/shared state, and represents possible exceptions, termination, callbacks, synchronization and other control/effect behaviour. If the affected state cannot be bounded soundly, the site comparison is unresolved.
4. **Per-operator predicate/effect catalog (recommendation adopted):** Stage 1 freezes the required catalog schema and selection procedure. After a proposed \(q\) and its input contract are specified, its concrete operator-relevant predicate/effect catalog is frozen before Stage 2 profile selection and before site enumeration. The domain must resolve that predeclared catalog; it cannot be tailored to observed candidates.
5. **Partial parameter-level overlap (recommendation adopted):** a site-location contrast uses only the identical, predeclared parameter settings supported at both sites, holding all other parameter coordinates fixed. The shared set is frozen before variant construction. If there is no common level, no site-location contrast is admitted. A site may still support parameter-only variation at that fixed site if those levels independently pass the declared rules.
6. **One-invocation restriction and Stage 1/Stage 2 sequencing:** retained from v0.7. The one-invocation rule remains a new population-design restriction, not an inherited B1 v1.7/Rev 1.4 requirement. Stage 1 freezes the analysis contract; Stage 2 instantiates and reviews the concrete per-parent profile before enumeration.

The accepted Rev 1.4 Amendment E, its acceptance record, B1 v1.7, and its acceptance record remain unchanged. No parent, operator class, site, realization setting, variant or parameter value has been selected. No solver, diagnostic, evaluation, bank or outcome has been accessed or constructed.

### 0.9 Repository identity and predecessor provenance

The v0.7 specification content is identified by blob \`81f4a4dba051883916958713cfa9ee1acd69fc03\`. Its file was created in commit \`32bebbff605c2204f24ad400ba6d8d48bab81235\`. The later commits \`48898f09bc5a9bb0ef2dad47c2edb445d367439a\` and \`b9e095f871eecb838f59f4c801d801869c18b8e7\` add the v0.7 review handoff and its final newline; they leave the v0.7 specification blob unchanged.

The accepted predecessor identities remain unchanged: Rev 1.4 Amendment E blob \`3728146356a74363a94fe75a87fd06c483954ee2\` with acceptance record blob \`074b40980eb96d164cd8411c8995bb1db4af0d46\`; B1 v1.7 blob \`8c666e501a31726c728447d155045c0b20adc178\` with acceptance record blob \`ea51d72f4f85c5d832d72add561b4c93472c364a\`.

## 1. Claim scope and target population

### 1.1 Population

The study population consists of engineered variants derived from a finite, prespecified set of real parent solver implementations. Each parent is a distinct pre-mutation implementation lineage with a pinned source revision. Each variant is a traceable derivative of exactly one named parent under a prespecified mutation specification.

The study does not sample naturally occurring solver versions as its target population. Existing implementations provide parent material; the variants form the deliberately engineered study population.

### 1.2 Conditional research claim

The primary research question is:

> Within the studied population of controlled variants derived from the selected parent solver implementations, does diagnostic-failure concentration \(C_D\) provide additional predictive information about held-out solver correctness beyond the exact B1 cell \(c=(q,Z,k_{\mathrm{fail}},k_{\mathrm{unresolved}})\), under the prespecified held-out-parent prediction procedure?

The phrase **“beyond the prespecified design variables” has this exact scope in the primary claim**: it means beyond the exact B1 cell coordinates \(q\), parent family \(Z\), definite-failure total \(k_{\mathrm{fail}}\), and unresolved total \(k_{\mathrm{unresolved}}\). It does **not** mean beyond every construction variable in the engineered study. In particular, the primary analysis does not condition on the within-identity realization setting \(\mathbf a(v)\).

Therefore, a positive primary result may arise because \(C_D\) carries information about held-out correctness by proxying \(\mathbf a(v)\). This includes a permitted literal or threshold setting whose value changes the transformation's effect relative to the reachable input-value range. Such a result still answers the stated incremental-prediction question relative to the exact B1 cell. It does not establish that concentration has predictive information independent of the realization settings, and it does not establish a direct or causal concentration effect. Any comparison that varies a source site must separately pass the stricter context and abstract-value equivalence requirements in §4.1.5.

The claim is conditional on:

- the selected parent implementations and their recorded provenance;
- the variants produced under the frozen operator-class and realization-setting specifications;
- the exact B1 cells and support actually realized;
- the new protected evaluation procedure and its declared input domain;
- the prespecified B1 model, scoring, and analysis rules, as amended and accepted for the new evaluation set.

A positive finding would support only this conditional predictive claim for the studied engineered population and the declared evaluation domain. It would not establish a universal concentration law, a causal effect of concentration, an effect independent of \(\mathbf a(v)\), or generalization to naturally occurring solvers or independently developed parent implementations outside the study.

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

**Decision for this specification:** the final operating parent count must be justified above the bare three-parent floor. No exact number is selected in v0.8. Before design freeze, the justification must state:

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

where \(k=k_{\mathrm{fail}}\) and \(\ell=k_{\mathrm{unresolved}}\). The symbol \(q\) retains its role as the mutation-identity coordinate in the accepted B1 cell. For the new engineered population, v0.5 proposes to operationalize that coordinate as a stable mutation-operator class, with concrete within-class realizations recorded separately by \(\mathbf a(v)\). This is a proposed coding for the new population only; it does not retroactively redefine B1 v1.7. The new B1 amendment must explicitly adopt and define this coding before confirmatory analysis. If the amendment retains a finer-grained \(q\) definition under which different realization settings are different mutation identities, they cannot be pooled into one \(q\) cell and the current M1-si construction must be redesigned.

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

### 3.4 Adopted M1-si design requirement: same parent, same operator class, same exact B1 cell

The study's stated scientific rationale for choosing an engineered population is to make matched comparisons within parent possible. This specification therefore **adopts a matched-within-parent requirement** as a new design rule. It is not a theorem implied by the B1 cell thresholds, and it is not inherited as binding authority from the old Rev 2.6 review draft.

The required support is specifically **M1-si**: within-parent variation among variants carrying the **same operationally defined mutation-operator class \(q\)**, but using different predeclared realization settings \(\mathbf a(v)\). In this new design, \(q\) is an identity-level operator class, not a unique concrete source artifact or parameterized realization. It is not M1-ci, which allows a pair to differ in operator-class identity and can therefore reflect differences between mutation classes rather than variation within one class.

For at least one common exact B1 cell

\[
c=(q,Z,k,\ell),
\]

at least three distinct parent groups must each contribute at least two of their own variants to that same cell, with at least two different exact \(C_D\) values within each contributing parent. Because \(q\), \(Z\), \(k\), and \(\ell\) are all fixed by the cell, the pair is matched on operator-class identity, parent family, definite-failure total, and unresolved total. The realization setting \(\mathbf a(v)\) is the intended within-class difference and is not held fixed in the primary M1-si contrast.

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

**Site-relocation feasibility qualification.** M1-si requires at least two distinct predeclared realization-setting vectors \(\mathbf a(v)\) within each qualifying parent-cell; it does **not** require those vectors to differ by source location. A fixed source site with two or more admissible literal/threshold/extent settings may supply the required within-\(q\) variation. Site relocation is an optional realization coordinate, not a necessary condition for M1-si.

The v0.7 whole-function marked-CFG rule was overly restrictive for relocation: two target-marked copies of an entire function generally have identical canonical graphs only when a graph automorphism maps one target position to the other. v0.8 replaces that rule with the target-centred context-slice equivalence in §4.1.5(B). The slice ignores unrelated function structure and absolute source location but retains operator-relevant dependency, control, state, exception and effect context. Consequently, site relocation may be admissible where the relevant contexts match, but it is not assumed to be frequent. No numeric or qualitative admissibility rate is claimed before the predeclared Stage 2 analysis. If no sites pass, the rule is not relaxed; fixed-site parameter variation may still be used if predeclared and admissible.

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

Accordingly, the historical five-version M1 rule is **not binding on this new study by inheritance**. This v0.8 specification retains the new, explicit design choice: adopt the stronger **M1-si** requirement in §3.4, matched on the full B1 cell \((q,Z,k,\ell)\). This is deliberately stricter than the old \((k,\ell)\)-only wording because current B1 conditions on individual identity \(q\) and family \(Z\). It adopts the scientific rationale of within-parent variation without inheriting the historical five-version count or the old 30-parent/150-body architecture.

The source-provenance question was closed in the v0.4 adjudication: the historical wording exists in the cited review-draft blob; it is not treated as binding authority for the new population. The adopted rule is the new study's own proposed design requirement and remains subject to Claude's review and GPT's final freeze.

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

No mutation mechanism is selected in v0.8. Mechanism selection follows, rather than precedes, acceptance of the support requirements in §3.

### 4.1 Required operator-class fingerprint and within-class realization record

For this new engineered population, \(q\) is an **operationally defined mutation-operator class**. A concrete version is represented by its parent \(g\), operator class \(q\), and permitted realization-setting vector \(\mathbf a(v)\). The \(q/\mathbf a\) boundary must be fixed before construction and before any diagnostic result is available.

#### 4.1.1 Canonical operator-class fingerprint

Each \(q\) must have a versioned, machine-readable operator-class specification and canonical fingerprint \(F(q)\). The fingerprint must define, at minimum:

1. the transformation operation or operator token and its semantic role;
2. the abstract-syntax-tree (AST) node types and structural template of the transformed expression or statement;
3. operand roles, operand types, and data-type constraints;
4. the control-flow construct, control-flow context, and affected control-flow edges;
5. the declared read/write or state-transition footprint;
6. the number and order of transformation operations;
7. the preconditions, postconditions, and semantic invariants that define the transformation class;
8. the language, parser, AST-normalization procedure, and tool versions used to generate and compare fingerprints.

The operator-class specification must identify a **closed set of permitted variable fields** \(\mathcal W_q\). These are the only locations in the canonical template that may vary between realizations of the same \(q\). Every permitted field must be listed by AST path or stable structural identifier and assigned a type, unit, allowed values or finite range, and semantic interpretation.

Permitted fields may include, where justified by the operator class, (i) selection among pre-enumerated sites that satisfy the exact within-parent context and abstract-value equivalence criterion in §4.1.5; and/or (ii) literal, threshold, extent, or other operator-parameter values from a predeclared finite set or bounded domain. Site selection and operator-parameter variation are distinct realization dimensions and must be separately typed in \(\mathbf a(v)\). Identical AST shape alone is not sufficient to admit site selection. These are examples, not automatic permissions. The actual permitted field list is specific to each \(q\) and must be frozen in its specification.

The following are **invariant parts of \(q\) and may never be included in \(\mathcal W_q\)**: the operation token and transformation semantics; AST node types; operand roles and operand types; data-type constraints; control-flow form and affected edges; read/write or state-transition footprint; number and order of transformation operations; and the precondition/postcondition class. A change to any invariant creates a different operator class \(q\), even if the changed field was mistakenly listed as a realization setting. No reviewer may waive this rule.

The permitted realization fields \(\mathcal W_q\) are restricted to values or positions that leave every invariant above unchanged. Examples, only when the canonical structural check confirms equivalence, are: selecting among pre-enumerated sites with identical AST node type, operand roles/types, and control-flow signature; or changing a literal, threshold, or extent within a predeclared finite set or bounded domain while preserving the operation and semantic class. A field not explicitly included in \(\mathcal W_q\) is fixed. A field in \(\mathcal W_q\) must still pass the canonical fingerprint check.

#### 4.1.1a Canonical signature encoding and equivalence rule

Each parent/operator/site context is analysed under one **pinned static-analysis profile**, instantiated under the sequencing gate in §4.1.1b. The profile must include, as applicable:

1. language and language-standard version; compiler or interpreter front-end, parser, AST library and versions;
2. the exact parent source-tree digest, generated-source inventory, dependency/interface stubs, compilation database, build mode, target architecture, preprocessing defines, include paths and relevant compiler/front-end flags;
3. symbol-resolution and overload-resolution settings; virtual-dispatch/devirtualization model; call-graph algorithm and context-sensitivity mode;
4. points-to, alias, memory-effect and escape-analysis algorithms and options;
5. control-flow and program-dependence graph construction, including the language-specific exceptional/control-transfer edge inventory and treatment of callbacks, reflection, indirect calls and external functions;
6. abstract-interpretation domains, transfer functions, path/context sensitivity, loop-fixpoint strategy, widening/narrowing, iteration limits, and external-function summaries;
7. canonical graph-labelling algorithm and version; graph model; node/edge label schema; canonical serializer and version; and every configuration value that can affect any reported signature component.

The complete profile is stored as a machine-readable manifest. Its canonical serialization is hashed with SHA-256. The digest, source-tree digest, \(F(q)\) digest, candidate-search-frame digest, and all per-site canonical encodings are retained. A rerun under a different tool version, build configuration, analysis mode, graph model, edge inventory or abstract domain is a different analysis profile and cannot silently reuse the previous site-equivalence result.

**Canonical graph requirement.** Every context graph is a finite typed, directed, edge-labelled multigraph. Node labels, edge labels, multiplicity and semantic attributes are explicitly enumerated by the operator-class specification and instantiated for the selected language. The chosen graph-canonicalization algorithm must be a deterministic **canonical-labelling algorithm**, not merely a deterministic traversal or a hash of an arbitrary traversal. It must satisfy this property: two input graphs are isomorphic under an isomorphism that preserves every declared node label, edge label, edge multiplicity and semantic attribute if and only if their canonical graph representations are byte-identical. The algorithm must return the same canonical representative regardless of input node numbering, insertion order, memory addresses, process order, hash-map iteration order, filesystem traversal order or thread scheduling. If the selected implementation cannot establish this canonical-form property for the declared graph class, site equivalence cannot be used.

For canonical serialization, use the pinned **RFC 8785 JSON Canonicalization Scheme (JCS)** implementation and version, with UTF-8 output and the graph nodes and edges emitted in canonical-label order. Arrays with semantic order retain that order; arrays representing unordered sets are sorted by their canonical element encodings. Floating-point values are prohibited. Exact integers outside the interoperable JSON integer range, rational numbers, intervals and other numeric abstract values are encoded as typed canonical decimal strings or numerator/denominator pairs with explicit endpoint inclusivity. No implementation-dependent numeric formatting is permitted.

**Identifier and source normalization.** Canonicalization must preserve program meaning rather than erase names indiscriminately:

- Global, external, module, package, type, member, field, enum/tag, overload and template/specialization identifiers are represented by their resolved, fully qualified semantic identities, including linkage/signature information required to distinguish different symbols.
- Local lexical variables and parameters may be alpha-normalized to canonical binding identifiers derived from declaration/reference structure only where the selected language and declared execution contract make their source spelling unobservable. If reflection, serialization, debugging hooks, annotations, macros, generated code or another supported language feature makes a local name observable, the name and relevant context must be retained or the site comparison fails closed.
- Member/field names, property names, external API names, string/character literal contents, numeric literal values and other semantically observable tokens are not discarded or normalized as though they were local variable names.
- Identifier normalization follows the selected language standard and the pinned compiler/front-end's resolved symbol identity. There is no blanket Unicode normalization of arbitrary source strings or literal contents. The canonical serializer encodes the resulting exact Unicode scalar sequence or exact source-byte representation according to the pinned source-encoding rule.
- Source paths, line/column offsets, timestamps and filesystem order are retained in the candidate manifest for provenance, but are not canonical graph labels. The candidate target's structural position remains represented by its unique graph marker and graph relationships.

**Macros and generated code.** The pinned profile must retain both the expanded/preprocessed representation and a source-origin map back to the editable source. For macro-expanded code, record the macro definition digest, invocation identity, expansion stack, relevant preprocessing configuration, and a stable mapping from the target AST/CFG node to one source edit location. A candidate site is inadmissible if that mapping is ambiguous or if distinct expansion instances cannot be distinguished. Generated source may enter the search frame only when the generator, generator version, inputs, configuration and generated output are reproducibly included in the source-tree manifest. Compiler-synthesized nodes must be explicitly labelled as synthetic; they are not editable candidate sites unless an unambiguous source mapping exists. Unmodelled or nondeterministic generation fails closed.

The canonical graph and abstract-state bundle is serialized using the pinned JCS implementation. Canonical graph-node identifiers come only from the canonical-labelling result; source traversal order must not assign them. Any normalization step that can affect graph labels, edges, symbols, path predicates, value summaries or operator effects is part of the profile manifest and therefore affects its digest.

For each site \(s\), let \(B_{g,q}(s)\) be the complete canonical byte string for its context bundle, including the pinned profile digest, parent source-tree digest, operator-class fingerprint, site-marked control-flow context, call-resolution integrity data, data-flow/state data, abstract input-value data, and abstract operator-effect profile for the declared shared realization settings. Define the domain-separated content identifier:

\[
H_{g,q}(s)=\operatorname{SHA256}\!\left(
\texttt{LC518-SITE-CONTEXT-v1}\Vert B_{g,q}(s)
\right).
\]

Two candidate sites are equivalent for the declared \(q\) and parent **only when their complete canonical byte strings are exactly equal**. Equal hashes are compact identifiers and integrity checks; before accepting equivalence, the canonical bytes must also compare exactly. If hashes match but bytes differ, treat the sites as non-equivalent and record a hash-collision or encoding defect. Because the selected graph canonicalizer returns one canonical representative per labelled-graph isomorphism class and the final representation is compared byte-for-byte, this equivalence is reflexive, symmetric and transitive. No tolerance-based, reviewer-chosen, partial-field or post hoc equivalence is permitted.

This is an equivalence relation over the **declared canonical static-analysis representation**, not a proof of concrete program or observational equivalence for every runtime input. No stronger semantic-equivalence claim is made.

#### 4.1.1b Two-stage static-analysis profile freeze

The fact that parent languages and build environments have not yet been selected does not permit the static-analysis profile to remain discretionary. It requires two distinct, ordered freeze gates.

**Stage 1 — design-level analysis contract (before population/design freeze).** This specification freezes:
1. the required static-analysis outputs and evidence schema;
2. the canonical graph model and canonical-form property required in §4.1.1a;
3. the minimum language-specific control-flow and exceptional-flow coverage required in §4.1.5;
4. the identifier, source-location, macro and generated-code normalization rules;
5. the schema and pre-enumeration procedure for freezing the operator-specific predicate/effect catalog required by §4.1.1c, together with abstract-domain adequacy criteria and fail-closed rules in §4.1.5;
6. the permitted profile/tool selection rule for Stage 2;
7. the requirement that every profile setting and tool version capable of affecting a signature enter the profile digest.

Stage 1 does not pretend to select a compiler or parser version before the parent language and build environment are known. It freezes the requirements governing that later selection. A design freeze may certify Stage 1 only; it cannot certify that any concrete parent/site profile has already been instantiated.

**Stage 2 — per-parent profile instantiation (after parent/source selection, before candidate-site enumeration).** Once a parent implementation and immutable source revision/tree digest are selected, instantiate the complete profile for that parent and each proposed operator class. The profile must pin actual language standards, compiler/front-end/parser and AST versions, build/preprocessing configuration, dependency/interface inputs, symbol/overload/dispatch resolution, call-graph mode, points-to/alias and memory-effect settings, CFG and exceptional-flow edge model, abstract domains and transfer functions, fixpoint and widening rules, canonical graph-labelling implementation/version, and serializer/version; external-call summaries or conservative havoc policy. The frozen per-\(q\) predicate/effect catalog hash is part of the profile manifest.

The concrete toolchain may be selected to match the already declared language, build system and required static-analysis capabilities. It must not be selected by examining how many candidate sites pass, which sites produce favourable signatures, expected \(C_D\), support, correctness or any other result of site enumeration. The abstract domain for a proposed \(q\) is selected to resolve the already frozen predicate/effect catalog in §4.1.1c, which is derived from the operator's declared semantics, operand types and input contract before Stage 2 and before site enumeration. It is not refined after seeing candidate-site values or acceptance counts. All selection criteria, alternatives considered and reasons for the final tool/domain choice are recorded.

The Stage 2 profile manifest is canonicalized, hashed and independently reviewed **before the syntactic search is run**. Only after that profile hash is fixed may candidate-site enumeration and signature calculation begin. The candidate search frame/predicate is separately frozen before enumeration. The complete resulting inventory, including rejected/unresolved sites, is then hashed before source construction.

If the parent language/build or required static-analysis feature cannot be handled by a reproducible toolchain, no candidate-site enumeration or site-based realization is permitted for that parent/operator. A materially different profile requires a new profile version, review and a complete rerun of the declared search frame. The previous inventory and classifications remain archived and are not selectively combined with the rerun. No profile refinement may be triggered by the number or desirability of sites that pass.

#### 4.1.1c Per-operator predicate and effect catalog freeze

The concrete operator-relevant predicate/effect catalog cannot be specified before a proposed \(q\), its operand types, transformation semantics and declared input contract are defined. Therefore the Stage 1 design contract freezes the **catalog schema and mandatory selection procedure**, while each \(q\)'s actual catalog is frozen at a separate **Operator Contract Gate** before Stage 2 profile instantiation and before candidate-site enumeration.

For each proposed \(q\), its machine-readable catalog must enumerate:
1. every operator-relevant input predicate, including type/range boundaries, guards, comparison outcomes, overflow/underflow or exceptional conditions, alias/state distinctions, and any other condition that changes the operator's abstract effect;
2. every abstract effect partition required to distinguish the operator's behaviour at each allowed realization-parameter level;
3. the required truth/possibility classification for each predicate (true, false, both possible, or unresolved), including path-sensitive combinations where single-predicate summaries are insufficient;
4. the minimum abstract-domain operations and precision required to decide those classifications soundly under the declared input contract;
5. how unsupported language/runtime features and unsummarised external calls force TOP/unknown or a site exclusion;
6. the reason each predicate/effect partition is relevant to preserving the operator's declared semantic class and to assessing site-context equivalence.

The catalog is derived only from the declared operator semantics, operand types, parameter schema and input contract. It is frozen **before** choosing the concrete Stage 2 abstract domain and before enumerating or inspecting candidate sites. Stage 2 selects a domain capable of resolving the frozen catalog. If no available sound domain can do so, site relocation for that \(q\) is not admissible; the catalog may not be reduced after seeing candidate-site values or counts. A proposed change to the operator semantics or catalog requires a new reviewed \(q\) specification before enumeration.

The catalog, its rationale, and its content hash are inputs to the Stage 2 profile manifest and to \(B_{g,q}(s)\).

#### 4.1.2 Deterministic conformance check

Only after the Stage 2 profile and syntactic search frame have been frozen under §§4.1.1b and 4.1.6 may enumeration begin. The pinned profile must then produce, for every enumerated candidate site, a canonical transformed-region AST and operator fingerprint, plus the complete site-context bundle and \(H_{g,q}(s)\). After masking only the exact operator-parameter fields listed in \(\mathcal W_q\), the resulting operator structure must match \(F(q)\) exactly. Each unmasked structural mismatch fails conformance to that \(q\). Where a permitted field selects a source site, the complete canonical context bytes and abstract-value/effect profiles required by §4.1.5 must also match exactly within the parent. Passing the AST fingerprint check does not waive or replace these tests.

The conformance record must contain the parent source revision/tree digest, transformation specification, canonical AST before and after transformation, operator fingerprint, frozen Stage 2 static-analysis profile and manifest digest, declared wildcard fields and realized values, frozen search-frame digest, completed candidate-inventory digest, complete canonical context bytes or content-addressed references, exact source diff, tool versions, and cryptographic hashes. The deterministic check validates syntax and declared operator-class structure; it does not prove semantic correctness or validate the scientific rationale.

A variant that fails the conformance check is not reassigned to another \(q\) after diagnostics. It is classified under the predeclared invalid/inapplicable rule and remains in the complete accounting register. If a distinct semantic class is scientifically warranted, it requires a new versioned \(q\) specification and a design amendment before construction.

#### 4.1.3 Diagnostic-blind identity review

Before any candidate-site enumeration, two reviewers must independently approve the Stage 2 profile and its manifest digest against the frozen Stage 1 contract. Before any diagnostic probing or source construction, the two reviewers must independently assess the operator-class specification, allowed variable fields, AST fingerprints, the pinned profile, the frozen search frame, the complete candidate-site inventory, the frozen per-\(q\) predicate/effect catalog, Stage 2 profile, target-centred context-slice extraction, external-call summaries/havoc dispositions, and all canonical site-context and abstract-value signatures required by §§4.1.1a–4.1.1c and 4.1.5, and proposed source diffs. They may inspect source code, transformation records, static structural signatures, and the declared semantic contract. They must not receive diagnostic tables, \(C_D\), failure or unresolved totals, correctness outcomes, or results from the protected evaluation set.

Each reviewer records whether the variant conforms to the predeclared \(q\), the exact structural basis for the decision, and any disagreement. Unresolved disagreement means the \(q\) assignment is not accepted for M1-si. The disagreement must be resolved by a documented design amendment before diagnostic access; it cannot be settled by looking at the realized concentration or correctness.

The reviewer identities, review date, evidence examined, Stage 1 contract version, Stage 2 analysis-profile digest, frozen search-frame digest, completed candidate-manifest digest, site-signature hashes, and decision are retained. This review is a technical identity-classification safeguard; it is not the independent protected-set custody role.

#### 4.1.4 Required operator-class and realization record

For every proposed \(q\), the design record must also contain:

1. Stable operator-class identifier, version, and precise operational definition.
2. The solver property the transformation class is intended to vary, with a technical rationale grounded in the implementation or algorithmic structure.
3. The exact transformation operator, its fixed semantics, and the canonical fingerprint \(F(q)\).
4. The complete realization-setting vector \(\mathbf a\): every coordinate, type, unit, interpretation, permitted level or range, allowed combination, and constraints between coordinates. Include the concrete per-\(q\) predicate/effect catalog required by §4.1.1c and, for each intended literal/threshold/extent level, its abstract relation to the reachable input range and abstract transfer/effect summary. For each literal/threshold/extent level, include the predeclared abstract relation to the reachable input range and the abstract transfer/effect summary required by §4.1.5(C).
5. A reproducible, predeclared assignment schedule for realization settings across eligible parents. For each parent intended to contribute to M1-si, at least two distinct settings under the same \(q\) must be planned.
6. The closed wildcard-field list \(\mathcal W_q\) and justification for why each permitted field changes only the realization, not the operator-class semantics; any site-selection field must also satisfy the exact canonical graph and abstract-value requirements in §4.1.5 within each contributing parent.
7. The expected functional effect of changing each setting, including code paths, behaviours, or correctness conditions it is expected to affect, based on source-level or algorithmic reasoning.
8. Expected qualitative diagnostic implications, if justifiable: which broad failure manifestations or strata may be affected and why. This is a mechanistic expectation, not a predicted \(C_D\), \(k_{\mathrm{fail}}\), \(k_{\mathrm{unresolved}}\), or exact-cell assignment. Unknown implications must be recorded as unknown.
9. Technical rationale for permitted ranges or levels, including why boundary and intermediate settings are meaningful. Ranges must not be selected by searching for desired concentration values or support.
10. Parent applicability and restrictions.
11. **New population-design restriction, not inherited B1 requirement:** each variant receives exactly one mutation-operator invocation \(q\). This is the population design's chosen strengthening of the one-\(q\)-per-version representation; neither B1 v1.7 nor Rev 1.4 is cited as independently requiring a single source-edit invocation. A single invocation may produce multiple coordinated source-edit hunks only when every hunk is a necessary, predeclared part of that one operator's fixed transformation template; those hunks together constitute one atomic operator application, not separate mutations. A variant may not combine independent operator invocations. No compound multi-operator variant is included in this population design; adding one requires a separately reviewed design amendment before construction.
12. Exact source-level metadata for every planned variant: parent ID, \(q\), \(\mathbf a(v)\), variant ID, source revision, reproducible transformation record, AST fingerprints, exact diff, tool versions, and hashes.
13. Predeclared validity, build, and provenance checks, including inapplicable settings, no-op transformations, and identity-class mismatches.
14. The relationship between \(q\), \(\mathbf a(v)\), and the B1 cell, together with the predictive-interpretation boundary in §5.7.
15. A statement explaining why the operator class and its realization range are scientifically relevant independently of any desired \(C_D\), failure total, unresolved total, cell membership, or correctness outcome.

**M1-si realization requirement.** A pair of versions counts as a same-class realization contrast only if it shares parent \(g\) and operator-class identity \(q\), uses different predeclared \(\mathbf a\) values within \(\mathcal W_q\), passes the deterministic conformance, canonical context/value-equivalence, and diagnostic-blind review checks, and produces distinct source artifacts. Each version contains one operator invocation as specified above. This does not guarantee a common exact diagnostic cell or distinct realized \(C_D\) values; those are audited only after a separately authorized diagnostic stage.

A parameter introduced only to make \(C_D\) vary or to satisfy M1-si is prohibited.

#### 4.1.5 Within-parent site-context equivalence: canonical structural, positional, and value context

A source location is not a semantically neutral realization setting merely because its local AST has the same shape. Two matching expression or statement templates can occur in different functions, control-flow positions, data-flow environments, or reachable value ranges. Site selection therefore requires exact equivalence of a complete, pinned context bundle, not reviewer judgement that two locations “look similar”.

**A. Enclosing entity and call-resolution integrity.** Each candidate site must be within the same fully qualified enclosing function, method, overload, or template specialization for a within-parent M1-si site contrast. Include lexical scope and receiver/type context. The call-graph check is retained primarily to validate symbol and dispatch resolution under the pinned compilation profile: record the resolved enclosing call-graph node, incoming/outgoing call edges, virtual-dispatch targets, context-sensitive clones, and relevant external-call summaries. Since two sites in the same enclosing entity ordinarily share the function-level call-graph node, this component is a resolution-integrity check, not a substitute for the position-specific graph comparison below. Any unresolved indirect call, overload, dynamic dispatch, reflection, callback, or generated-code boundary that could change the resolved context makes site selection unresolved.

**B. Target-centred canonical context slice and language-complete control-flow model.**

A whole-function CFG with one candidate-specific TARGET marker is not the decisive equivalence object. Requiring two such graphs to be identical would generally require a whole-function graph automorphism mapping one source location to the other, which unnecessarily makes site relocation rare. Instead, construct a deterministic, **target-centred, dependency-complete context slice** \(G^{\mathrm{ctx}}_{g,q}(s)\) for each candidate site \(s\). The slice preserves the candidate's relative execution and semantic context but excludes unrelated parts of the enclosing function and absolute source addresses.

The context-slice extraction procedure is frozen in the Stage 1 contract and instantiated by the Stage 2 analysis profile. It must proceed as follows:

1. **Target and operator footprint.** Seed the slice with the target AST/CFG node, all operator operands, relevant reads, declared writes/state effects, and the operation's precondition/postcondition points.
2. **Backward semantic dependency closure.** Add every node and edge that can affect the target's execution, reachability, relevant operand values or read state, including transitive data dependencies, reaching definitions, memory/alias dependencies, path predicates, control dependencies, exception/cleanup dependencies, and relevant call/return effects. Continue to a fixed point under the pinned dependence and alias model. Include explicit typed boundary nodes for inputs or state whose definitions lie outside the analysable source/model.
3. **Control and loop anchors.** For every included node, add the branch predicates and loop headers/latches/exits that govern its execution or the target's execution. Retain branch polarity, path-condition structure, loop nesting and loop entry/exit relationships. Include normal/exceptional exits, cleanup/unwind and function/region boundaries when they are reached by or are necessary to represent the target's relevant control/effect slice.
4. **Forward effect closure.** From the target, add all nodes and edges needed to represent the operator's declared writes, state changes, side effects, exceptions, cleanup/unwind behaviour and their propagation to the first relevant observable boundary (including callers or function exits where required). Include intervening nodes that may alter, observe, alias or invalidate those effects.
5. **Closure and edge retention.** Repeat backward and forward dependency expansion until no additional node, edge, control predicate, state dependency or relevant summary is introduced. Retain all typed CFG, control-dependence, data-dependence, memory/alias, call, exception, cleanup and effect edges among included nodes, plus typed boundary edges to omitted regions. Omit a node only when the pinned analysis establishes that it is outside the transitive dependency/effect closure and cannot affect target reachability, operator inputs, state or effects under the declared input contract.

The slice is rooted at the candidate site with a unique TARGET label. It includes canonical labels for the relevant control predicates, branch outcomes, loop/exception/cleanup anchors, semantic data/state roles and typed boundary nodes. The graph preserves the target's **relative position within its relevant context**: its dependency paths, controlling branch arm, relation to relevant loop headers/latches/exits, exception/cleanup route, and distances/order relative to the included semantic anchors. It does not encode an absolute block number, source line, source path, or an unrelated node's location elsewhere in the function.

The canonical context bundle must encode:
- the complete labelled adjacency and multiplicity of \(G^{\mathrm{ctx}}_{g,q}(s)\), with TARGET distinguished;
- branch predicates, branch polarity and canonical path/control-dependence structure;
- dominator/post-dominator, dominance-frontier and loop relations within the extracted context slice, where defined;
- distances and ordering from TARGET to the included relevant entries, exits, controllers, loop headers/latches/exits, exception and cleanup anchors;
- the AST-to-CFG mapping for the target and relevant operand expressions;
- all typed boundary nodes and summaries for dependencies/effects that enter or leave the slice.

Two distinct source sites within the same enclosing entity may therefore be equivalent when their complete target-centred context slices are isomorphic under the declared node/edge semantics and their canonical bytes are equal, even though the enclosing function's full CFG is not automorphic between those sites. This is intentional: the equivalence criterion compares the operator-relevant context, not irrelevant whole-function structure. It does **not** ignore semantically relevant position. Different branch predicates/polarities, loop/exit relations, dependency structures, state/effect summaries, or exception/cleanup routes produce different context slices and fail equivalence.

The pinned profile must declare a complete edge vocabulary for the selected language and front-end. At minimum, it must distinguish:
- fall-through and sequencing;
- true/false conditional branches and switch/match-case selection, including fall-through where permitted;
- loop-back, loop-entry, loop-exit, break and continue;
- direct and indirect call/return and interprocedural summary edges;
- explicit throws, catch/handler dispatch, uncaught exception propagation through callees, and exceptional exits;
- cleanup, finally/defer/finalizer execution, destructor/RAII scope-exit and exception-unwind effects;
- goto, computed/indirect goto, non-local jumps such as setjmp/longjmp where supported, and other language-specific control transfers;
- coroutine/async await, yield, resume, cancellation and continuation edges where supported;
- language-specific trap, abort, panic or termination edges where they affect reachable control flow.

Every additional transfer construct supported by the selected language and build must receive an explicit edge type or a conservative summary in the profile. A generic OTHER edge cannot collapse distinct control-transfer kinds if those kinds can affect target reachability, cleanup, value state or effect. Calls whose callees may throw or perform cleanup must propagate those possibilities into the caller's exceptional/cleanup graph or a sound, pinned call summary.

If the selected language contains a control-flow, cleanup, exception, concurrency or non-local-transfer construct that the pinned analysis profile cannot model soundly for the candidate's relevant slice, the site is unresolved and site relocation is inadmissible. It is not acceptable to omit the edge type or approximate it as ordinary fall-through merely to retain the site.

**C. Data-flow, state, and value-level context.** Static structure alone is insufficient for operators whose effect depends on surrounding runtime values. Under the declared input contract and Stage 2 static-analysis profile, compute a sound over-approximation of the abstract program state reaching the candidate site. It must cover, as relevant to the operator:
- abstract values for every operand/read input, including exact constants, finite value sets, integer/rational intervals, congruence classes, Boolean predicates, enum/discriminant states, nullness and pointer/reference targets;
- normalized reaching definitions, def-use roles, relevant data and control dependencies, alias/points-to sets, memory/state reads and writes, side effects, and exceptional state;
- path predicates and guards that control reachability of the site and constrain the relevant operands;
- an abstract transfer/effect profile for the operator under every permitted realization-parameter level.

The abstract domain is selected for the operator's declared operand types, semantics, parameter levels and input contract **before candidate-site enumeration**. It must be adequate for the operator-relevant semantic distinctions, not merely sound in a way that returns coarse \`TOP\` values for every candidate. For a numeric threshold operator, the declared domain must at least distinguish exact constants, intervals and any required integer congruence or relational constraints sufficient to determine, for each allowed threshold, whether the threshold is below, within or above the reachable input range and which operator-effect branches are possible. Other operator types require a correspondingly justified set of abstract predicates and effect distinctions.

For each operator class \(q\), the design record must list the finite or otherwise precisely defined set of operator-relevant predicates/effect partitions that the abstract domain must resolve. It must explain why the selected domain and transfer functions are adequate for those distinctions under the declared input contract. The domain and its parameters are frozen in the Stage 2 profile before sites are enumerated. They cannot be made coarser or finer after inspecting candidate values, site counts, support or desired pair availability.

**Floating-point semantic requirement.** If an operator, any relevant operand, or any value in its context slice uses floating-point semantics, the Stage 2 profile and abstract domain must model the language/runtime's applicable floating-point format and execution semantics. At minimum, record:
- the exact format and precision (including binary/decimal format, exponent/significand width and supported extended precision);
- rounding mode and whether it can change dynamically;
- normal and subnormal values, flush-to-zero/denormals-are-zero modes, signed positive/negative zero, positive/negative infinity, quiet/signalling NaN and any payload behaviour observable under the language;
- comparisons and conversions involving NaN, signed zero, overflow, underflow, invalid operations, division by zero and relevant exception/status flags;
- fused multiply-add, contraction, reassociation, excess precision and compiler options such as fast-math or equivalent transformations;
- relevant hardware/runtime floating-point environment and compiler lowering rules.

Floating-point constants and exact values are encoded in canonical data as typed format identifiers plus exact bit patterns (for example, fixed-width hexadecimal encodings), not as JSON floating-point numbers. Abstract intervals and finite sets must be sound for the declared IEEE/language semantics, including rounding and special values; rational interval bounds alone are insufficient where they lose a semantically relevant distinction such as signed zero, NaN, infinity, subnormal behaviour or a rounding boundary. Every allowed floating-point parameter level must also have its exact bit-level value and abstract transfer/effect profile recorded.

If the selected domain or toolchain cannot model a relevant floating-point distinction soundly under the declared build/runtime configuration, a float-sensitive site comparison is UNRESOLVED. Float-typed site relocation and float-parameter variation are inadmissible for that \(q\) under that profile. They cannot be treated as ordinary rational/integer intervals.

**External-call and unknown-effect requirement.** Every external, native, foreign-function, dynamically dispatched, callback or library call that can affect the context slice must have a versioned, content-addressed summary whose soundness scope covers the declared input contract and relevant control/state effects. The summary must record possible return values, memory reads/writes, global and externally reachable state, alias/escape effects, IO or other observable effects, exceptions, nontermination/termination, callbacks, synchronization/concurrency and non-local control transfers as applicable.

If no sound summary is available, use a conservative havoc summary: the return value is TOP; every memory location, global, escaped object, shared state or externally reachable state that the call may affect is havoced to TOP; relevant IO/observable effects and possible exception/cleanup/termination/callback/synchronization/control-transfer behaviours are represented as unknown. Where the set of potentially affected state cannot be bounded soundly, the affected program state is treated as TOP. If this uncertainty can affect any target operand, reachability condition, relevant state/effect or observable operator consequence, the site-context comparison is UNRESOLVED and site relocation is inadmissible. No call may be silently omitted because it is outside the repository or because its implementation is unavailable.

**Site-selection rule:** for two candidate sites to be alternative realizations under one \(q\) within the same parent, their canonical abstract input-state, path-condition, data-flow/state, and operator-effect bundles must be exactly equal after the declared semantic normalization, evaluated at the same shared operator-parameter settings. Equality of interval hulls alone is insufficient where the operator-relevant predicates require congruence, relational or disjunctive distinctions. The analysis must establish the same abstract truth/possibility profile for every predeclared operator-relevant predicate and the same abstract transfer/effect profile at the shared parameter settings. If a relevant value is \`TOP\`/unknown, an alias set is unresolved, a path condition cannot be represented, or a required operator-relevant predicate/effect cannot be resolved by the frozen domain, the site-context comparison is **UNRESOLVED** and site selection is inadmissible for that \(q\). Reviewers cannot waive a failed or unresolved value-context component.

The word “equivalent” here means **equal under the frozen canonical target-centred context-slice representation, static-analysis abstraction and operator-relevant predicate set**. It does not mean that the full concrete runtime state sets, input-frequency distributions or all possible program behaviours have been proved identical. The design and any later report must not upgrade this abstraction-level classification into a proof of concrete semantic equivalence.

**Parameter-setting rule:** deliberate variation of a literal, threshold, extent or other operator parameter is not prohibited. It is a separate typed coordinate of \(\mathbf a(v)\), not a site-location equivalence. For each allowed parameter level, record:
1. the exact parameter value and type;
2. its abstract relation to the reachable input range and relevant path predicates;
3. which predeclared operator-relevant predicates are true, false or unresolved;
4. the operator's abstract transfer/effect profile at that level;
5. any assumptions or language semantics needed to derive that profile.

The effect profile may differ across deliberately varied parameter levels; that is the intended realization variation and remains part of the broad exact-cell predictive target and its proxy interpretation. It must not be misdescribed as a site-neutral comparison or a parameter-independent concentration effect.

Where site relocation is compared, the two sites must support an **identical predeclared parameter-setting vector**: the same values for every realization coordinate other than the site coordinate. If a site admits only a subset of the proposed parameter levels, only the exact intersection supported at both sites may be used for a site-location contrast. That common subset and the intended pair schedule must be frozen before construction, without diagnostic or correctness information. Levels available at only one site cannot be used to claim a site-only contrast. If the intersection is empty, no site-location contrast is admissible between those sites. If the intersection contains one or more common settings, compare the sites at those same settings while holding all other coordinates fixed. Parameter-only variation may still be considered at a fixed site under its own predeclared levels and effect summaries.

The abstract state is a sound over-approximation under the declared model. Equality of two abstract summaries establishes equality only at the frozen abstraction's resolution; it is not a claim that all concrete values or dynamic frequencies are equal. If the abstract interpretation cannot be performed soundly for the relevant values, language constructs or control predicates, the location is fixed rather than admitted as a realization setting. The design may still consider a separate literal/threshold parameter at that fixed location if its domain and effect profile can be declared and audited before enumeration. No empirical diagnostics, dynamically selected test inputs, dynamic profile, \(C_D\), failure totals, correctness outcomes or protected-set data may be used to complete, refine or repair this static analysis.

**E. Transformation interaction under the one-invocation design restriction.** Each variant contains one operator invocation \(q\). The interaction assessment therefore has two limited purposes: (i) record dependencies among coordinated edit hunks that jointly implement that one atomic invocation, including required edit order and preconditions; and (ii) detect whether the declared source footprint overlaps or is data/control-dependent on another candidate site in the same parent's frozen inventory. The latter may affect whether an alternative site remains a valid realization coordinate or whether its edit would conflict with the fixed operator template.

This is not a review of a multi-operator variant. Independent operator invocations are not combined in one version under this population design. If coordinated hunks within one invocation cannot be represented by one fixed, predeclared operator template, the variant does not satisfy the one-invocation restriction. If an edit conflict or dependency cannot be resolved before construction, the affected site/setting is inadmissible. Any proposal to combine independent invocations requires a new reviewed design amendment.

**D. Exact equivalence and disposition.** A site-context signature is the complete canonical byte bundle \(B_{g,q}(s)\) defined in §4.1.1a. The identifier \(H_{g,q}(s)\) is SHA-256 of the domain-separated bundle. Two candidate sites are equivalent only when the canonical bytes compare exactly; hash equality alone is insufficient. Exact byte equality is a genuine equivalence relation and therefore transitive. The site identifier, raw line/column location, timestamps, and filesystem traversal order are retained in the candidate manifest but excluded from the context bytes except insofar as the marked CFG/AST position is represented structurally.

If the candidate sites differ on any required component or their equivalence cannot be resolved, they cannot be treated as alternative \(\mathbf a\)-settings within the same \(q\) for M1-si. Fix the site and use another scientifically justified realization coordinate, or propose a new operator-class design in a reviewed amendment before construction. Do not rely on local AST similarity, partial matching, reviewer discretion, or post hoc execution-frequency explanations.

The comparison is **within each parent**, not across parent implementations. Different parents may have different function names, call graphs, data-flow structure and source layouts. For each parent intended to contribute an M1-si pair, its alternative sites must pass the exact within-parent canonical equivalence rule under the same pinned parent source revision and analysis profile.

The signature is a reproducible static exclusion/equivalence test over the declared analysis abstraction. It is not a proof of full program or observational equivalence for every possible runtime input. The study's claim is not broadened on the basis of this static signature.

#### 4.1.6 Frozen candidate-site search frame, inventory and analysis-profile record

The following order is mandatory for each parent and proposed \(q\):

1. Select and freeze the parent source revision/tree digest and the declared source/build/input contract.
2. Freeze the Stage 2 static-analysis profile, including tool versions, graph model, full control-transfer edge vocabulary, abstract domain, analysis options and canonicalization/serialization implementation, under §4.1.1b.
3. Freeze the **syntactic candidate-site search frame and predicate** before running the search. It must state source directories, tracked/generated-source treatment, file/type exclusions, language/build boundaries, AST node/operator patterns, syntactic match rule, macro/source-mapping rules, and any source-region extraction limits.
4. Run the frozen search predicate once over the declared source frame. Enumerate every site that satisfies that syntactic predicate, not merely sites expected to pass the context audit.
5. Compute the canonical operator and site-context signatures for every enumerated candidate under the already frozen profile.
6. Record pass/fail/unresolved status and the reason for each rejection or unresolved result. Hash and freeze the completed inventory before source construction or variant assignment.

“Complete” means complete relative to the frozen syntactic search frame and predicate. It is not a claim that every conceivable semantic mutation opportunity in the repository has been discovered.

For every enumerated candidate site, retain:
- stable candidate-site identifier and parent source path/range;
- source revision and tree digest;
- enclosing entity and preliminary operator fingerprint;
- the complete \(H_{g,q}(s)\) and canonical bytes or immutable content-addressed references;
- pass/fail/unresolved status for each structural, target-centred context-slice, control-flow/exception/cleanup, data-flow, alias/effect, value-range (including floating-point where relevant), external-call summary and reachability component;
- accepted/rejected/unresolved status and a specific reason for every rejected or unresolved site;
- whether it is eligible as a realization setting and the exact frozen rule supporting that decision.

The inventory must include rejected and unresolved candidates, not just sites eventually selected. The complete inventory, frozen search-frame definition, Stage 2 profile manifest, tool/version records and per-site signature references are serialized canonically and hashed. The candidate-site assignment schedule, including selected and rejected sites and their realization-setting coordinates, must be frozen before source construction. No subset of the candidate pool may be selected after diagnostic \(C_D\), support, correctness, fitting or score results are known.

The Stage 2 static-analysis manifest digest is an explicit input to \(B_{g,q}(s)\) and \(H_{g,q}(s)\), not merely a note in the conformance log. A rerun under a different parser, compiler profile, call-graph mode, points-to/alias configuration, control-flow edge inventory, abstract domain or graph-canonicalization implementation receives a different profile digest and must be reviewed as a new profile. The previous candidate inventory remains archived; a new profile requires a complete new enumeration and signature computation over the entire declared search frame.

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

The confirmatory claim requires a new protected evaluation set. No records are generated or accessed in v0.8.

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

**Current gate status: NOT SATISFIED. No independent custodian has been identified or appointed, and no access mechanism has been demonstrated.** No person or institution is named in v0.8 because none has been evidenced in the project record. The project owner, mutation designers, solver constructors, outcome analysts, and AI reviewers cannot be relabelled as an independent custodian merely by assigning them a different project role.

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

### 5.7 Adopted Option B: exact-cell predictive target, with realization-proxy limitation

Let \(\mathbf a(v)\) denote the predeclared within-class realization-setting vector from §4.1. The accepted B1 primary cell remains:

\[
c(v)=(q,Z,k,\ell).
\]

**The primary model does not condition on \(\mathbf a(v)\).** This is an explicit adoption of Claude's Option B, not an unresolved choice. The primary claim is incremental prediction beyond the exact B1 cell, not incremental prediction beyond every source-construction parameter.

If a realization setting affects both diagnostic failure placement and held-out correctness, then \(C_D\) may predict by proxying \(\mathbf a(v)\). A positive result through that pathway is valid evidence of incremental predictive information relative to the declared exact-cell baseline. It is **not** evidence that concentration itself causes correctness, that the association is direct, or that concentration adds predictive information independently of \(\mathbf a(v)\).

The new B1 analysis-plan amendment must adopt this wording and predeclare the interpretation before protected outcomes are accessed. At minimum, it must:

1. keep the primary exact-cell baseline \((q,Z,k,\ell)\) and explicitly leave \(\mathbf a(v)\) outside that baseline. It must not describe the primary target as adjusted for all construction variables or as prediction beyond \(\mathbf a(v)\);
2. retain a predeclared **N5 realization-parameter proxy stress control** with \(\beta_C=0\), in which \(\mathbf a(v)\) affects both diagnostic failure placement (and therefore the distribution of \(C_D\)) and held-out correctness at fixed \((q,Z,k,\ell)\). N5 asks whether the primary B1 procedure detects prediction carried by \(C_D\) as a proxy for the realization setting when there is no direct \(C_D\) effect;
3. classify N5 as a **proxy-pathway operating-characteristic scenario**, not as null calibration for the broad B1 permutation null. Because \(C_D\) is predictive through \(\mathbf a(v)\), N5 violates the broad null of no incremental predictive content through any channel by construction. Its rejection rate is reported as detection/operating behaviour for the proxy pathway, not as a Type-I error rate;
4. report the predeclared relationship between \(\mathbf a(v)\) and \(C_D\), and between \(\mathbf a(v)\) and held-out correctness, by \(q\), parent, and exact B1 cell;
5. include a labelled sensitivity model that adjusts for \(\mathbf a(v)\), where its coding and support make the sensitivity estimable. Report rank, collinearity, and loss of support. If \(C_D\) has no residual variation after conditioning on \(\mathbf a(v)\) and the exact cell, the parameter-independent contribution is **not identifiable**. It must not be claimed, and the primary result must not be silently reinterpreted as such;
6. retain the v1.7 restriction that outcomes, fit stability, and score favourability cannot define the permutation/admissibility set. Any revised admissibility rule must be declared in the B1 amendment before evaluation.

The conclusion language is fixed:

- A supported primary result may be described as **incremental predictive information from \(C_D\) beyond the exact B1 cell in the studied engineered population**.
- It must also state that the information may be carried through the predeclared realization settings \(\mathbf a(v)\).
- It must not be described as a direct, causal, or realization-setting-independent concentration effect unless a separately predeclared, identifiable analysis supports that stronger statement.
- If the adjusted sensitivity is not estimable, the direct/parameter-independent question remains unanswered; it does not invalidate or erase the broader exact-cell predictive result.

Option A, conditioning the primary model on \(\mathbf a(v)\), remains unadopted in v0.8. Claude recommended it, but GPT selected Option B for the current primary target. It would be a different estimand and would require a different design-support condition, an amended baseline and resampling null, and evidence of \(C_D\) variation at fixed realization settings. M1-si as currently defined varies \(\mathbf a(v)\) and \(C_D\) together and does not guarantee that stronger support. Any future proposal for that target must be a separately reviewed amendment, not an interpretation imposed after results are observed.

## 6. Parent and variant counts: derivation and feasibility

No final parent count, per-parent variant count, or total variant count is adopted in v0.8.

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

The lower bounds in §§2.5 and 6.1 are support minima only. They are not a sample-size justification, power guarantee, or assurance that the model will be estimable or useful. No power calculation, simulation, or model fitting is performed in v0.8. The operating parent count remains open and must be justified before design freeze; the three-parent support floor is not a substitute for that justification.

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
- If B1 support exists but M1-si does not, report the B1 and M1-si results separately. B1-only results cannot be relabelled as successful M1-si evidence. A B1-only confirmatory analysis may proceed only if that alternative is explicitly defined in a separately reviewed B1 amendment **before any diagnostic outcomes used to determine realized support are accessed**. It cannot be introduced after observing the shortfall.
- If M1-si is realized but particular LOPO fold-cell conditions fail, apply the accepted B1 fold-audit and exclusion rules exactly. No cell is repaired by changing the scored set, pooling, zeroing the slope, or replacing a variant.
- No variants may be added, removed, reassigned, retuned, or replaced after diagnostic outcomes are observed to make support pass. A redesigned study requires a new versioned design, new independent review, and a separate authorization. Its data must not be pooled with the original confirmatory attempt as though it were one frozen design.

A realized support shortfall is a design-feasibility result, not evidence that concentration has no predictive value. The outcome report must distinguish **B1 support**, **M1-si realization**, **LOPO estimability**, and **outcome-side informativeness** as separate statuses.

## 7. Compatibility with the existing B1 and computational plans

This population specification is a new design layer. It does not rewrite or supersede the accepted B1 analysis plan or the computational-plan draft.

1. **B1 v1.7:** remains accepted and frozen as the symbolic plan for the exposed 78-record development bank. It does not automatically govern a new protected evaluation set.
2. **Computational plan v1.0:** remains an unreviewed computational draft. It cannot be treated as validated for a new record count, new parent/variant incidence, or changed design-matrix dimensions without an explicit update and review.
3. **M1-si:** the same-operator-class, same-full-cell matched-support requirement in §3.4 is a new design choice in this specification. It is not represented as a requirement of B1 v1.7 itself and does not inherit the old five-version count.
4. **Protected custodian:** no independent custodian has been identified or appointed. This is a current blocker to freezing and implementing the protected-confirmatory route, not a routine execution detail.
5. **q and realization coding:** the new B1 amendment must explicitly adopt or reject the proposed operator-class coding of \(q\) and the closed \(q/\mathbf a\) boundary in §4.1. It must not silently alter v1.7's frozen coding.
6. **Option B target:** the future B1 amendment must retain the exact-cell primary baseline without \(\mathbf a(v)\), state the proxy limitation, and include N5 plus the adjusted sensitivity required by §5.7.
7. **Outcome-side variation:** the B1 amendment must include the outcome-side reporting audit in §5.6 without making outcome variation a design-selection or admissibility criterion.
8. **Trigger (i):** the proposal that certified nonexistence of a finite enriched ordinary-model MLE activates trigger (i) remains unratified. This is a separate statistical decision.
9. **Consent provenance:** the joint-consent provenance gap remains open. Parent source licenses and provenance records do not automatically resolve that separate gap.
10. **Isolation and data access:** no execution environment or data-access authorization is granted by this document.
11. **Execution GO:** a separate explicit GO is required after the design, analysis-plan amendment, computational plan, software validation, consent/provenance, custodian appointment, and isolation safeguards have been reviewed and accepted.

## 8. Open decisions for independent review

Claude's next review should address the complete v0.8 text against accepted B1 v1.7 and accepted Rev 1.4 Amendment E, including their separate acceptance records:

1. **Target-centred site-context equivalence.** Verify that the deterministic dependency-complete context-slice procedure preserves all relevant control, data, state, exception, cleanup and effect relationships while excluding unrelated whole-function CFG structure. Does it avoid the whole-function automorphism barrier without discarding a semantically relevant position difference?
2. **Canonical form and source normalization.** Verify canonical-labelling uniqueness, JCS use, source/symbol normalization, alpha-renaming limits, macro/generated-code mapping and path/address exclusion.
3. **Floating-point semantics.** Challenge the IEEE/runtime requirements, exact bit encodings, abstract domains, compiler transformation settings and fail-closed rule. Identify any unsound treatment of NaNs, signed zeros, rounding, subnormals, overflow or FMA.
4. **External-call soundness.** Verify that versioned summaries cover all relevant effects and that an unsummarised call causes conservative havoc/TOP and unresolved site context whenever it could matter.
5. **Per-operator predicate/effect catalog.** Check that Stage 1 freezes the schema/procedure and each concrete q-specific catalog is frozen before Stage 2 profile choice and before enumeration. Is the order logically sound and protected from candidate-driven tuning?
6. **Abstract-domain adequacy and honesty.** Verify that the selected domain resolves the frozen catalog and that equivalence is explicitly limited to the declared abstraction, not concrete behavioural equivalence.
7. **Partial parameter-level overlap.** Check that site-location contrasts use identical common predeclared parameter vectors, that empty intersections exclude the site contrast, and that any permitted common subset is fixed before construction.
8. **Two-stage profile freeze and inventory.** Verify Stage 1, Stage 2, syntactic search frame, candidate inventory, rejected-site records and profile/content hashes are properly ordered.
9. **Control-flow completeness.** Review exception propagation, cleanup/finally/RAII, non-local jumps, coroutines/async, and unsupported-transfer handling.
10. **Call-graph role.** Confirm the call-graph check is a symbol/overload/dispatch-resolution safeguard distinct from target-centred context position.
11. **One operator invocation per version.** Confirm this remains explicitly a new population-design restriction, not an inherited B1 v1.7/Rev 1.4 requirement; assess atomic multi-hunk clarity.
12. **B1/M1 and governance.** Check the q/a identity coding, M1-si same-parent/same-cell rule, Option B proxy target, N5, shortfall rule, parent count, custodian, trigger-(i), joint-consent, isolation and execution gates. Verify that §§6.4–9 remain consistent with the predecessor approvals.

GPT will adjudicate Claude's findings. Any substantive change after review must be a new version with its own identity and review; v0.8 is not frozen by publication.

## 9. Explicit non-authorization

This draft authorizes no solver source acquisition, solver construction, source modification, mutation allocation, mutation generation, compilation, execution, diagnostic probing, benchmark execution, protected-set generation, bank access, outcome access, fitting, sampling, simulation, or analysis.

It is a document-only design specification for independent review. Passing review of this document would freeze only the population/design specification. All separate statistical, computational, consent, isolation, data-access, and execution gates remain in force.

**End of population and experimental design specification v0.8.**
