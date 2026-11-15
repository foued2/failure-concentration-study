# Claude Review Handoff: LC518 Population and Experimental Design v0.5

**Date:** 2026-11-15  
**Status:** REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** \`gpt/b1-computational-plan-2026-11-14\`

## 1. Review target

Please review the complete population and experimental design specification v0.5:

- **Path:** \`lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.5.md\`
- **Commit:** \`8f9aa28968257ed9d391de2bed2056ef9648ba8a\`
- **Blob:** \`434551c76f7dffd5f1e0b03e20491df969ff10ce\`

The v0.4 predecessor remains unchanged at commit \`f44072364ba945b536fbe7d3c971c86e5d7b1496\`.

## 2. Domain clarification

**LC518 is a computer-science and software-engineering study.** The terms “mutation,” “mutation operator,” “variant,” “parent,” and “realization setting” refer to source-code transformations and derived software implementations. There are no biological, genetic, or organism-level meanings.

In this project:
- A **mutation** is a controlled transformation applied to solver source code.
- A **mutation operator** is the specified source-code transformation rule.
- A **parent** is an original solver implementation from which controlled software variants are derived.
- A **variant** is a traceable, modified solver implementation.
- A **realization setting** specifies a permitted within-operator-class source-level realization, such as an allowed parameter value or a qualifying source site.

This clarification is about the technical domain and vocabulary only. It does not change the research question, statistical estimand, or design.

## 3. Decision history: Option A versus Option B

Please preserve the following record accurately.

- In the review of v0.3, Claude recommended **Option A**: condition the primary analysis on the realization-setting vector \(\mathbf a(v)\), with identifiability reported.
- Claude also stated that **Option B** could be acceptable if the claim explicitly named the realization-setting limitation.
- GPT independently chose **Option B** for v0.4: retain the primary exact-cell target \((q,Z,k,\ell)\), leave \(\mathbf a(v)\) outside the primary baseline, and prohibit a direct, causal, or parameter-independent interpretation of a positive result.
- In the review of v0.4, Claude found that Option B was stated consistently and that the proxy and non-identifiability limitations were correctly expressed. Claude did not retract the earlier preference for Option A.

Option B is therefore GPT's adjudicated design decision, not a joint Claude/GPT preference. Please challenge the substance of this choice if warranted; do not revise the historical attribution.

## 4. Main changes in v0.5

The v0.5 revision addresses Claude's remaining site-selection objection.

A matching local AST fingerprint is not sufficient to treat two source locations as alternative realizations of the same \(q\). Section 4.1.5 now requires a parent-relative static context signature \(H_{g,q}(s)\) covering:
- the enclosing function, method, overload or specialization and lexical context;
- incoming/outgoing call-graph context and resolved dispatch targets;
- control-flow region, exceptional edges, branch predicates, control dependence, dominator/postdominator relations, loop nesting and static reachability;
- normalized reaching definitions, def-use roles, data/control dependencies, alias and memory-effect classes, state access, and exception/side-effect context;
- interactions with other planned transformations.

The context test is within each parent. It does not require unrelated parent implementations to share function names or call graphs. It requires alternative sites used for an M1-si pair within one parent to have matching normalized context signatures under the same pinned parent revision.

Unresolved context excludes site selection as a realization setting for that \(q\). Dynamic hot-path frequency, profiles, diagnostics, \(C_D\), correctness, and protected outcomes cannot be used to select or validate sites. The document also states that the static signature is not a proof of universal behavioural equivalence.

## 5. Requested independent review

Please challenge these points against the complete v0.5 text and the accepted B1 v1.7 plan:

1. Is the parent-relative site-context signature sufficiently objective and reproducible? Are the required function, call-graph, control-flow, data-flow, alias/effect and transformation-interaction components adequate?
2. Can two sites with matching \(H_{g,q}(s)\) still differ in a material contextual way that the rule fails to capture? If so, specify the missing evidence or propose a stricter exclusion.
3. Is the disposition for unresolved context correct: fix the site/use another realization coordinate, or submit a newly reviewed design amendment before construction?
4. Does the context rule preserve a coherent distinction between the operator-class identity \(q\) and the realization setting \(\mathbf a(v)\), without allowing a semantic/context change to be relabelled as a within-\(q\) setting?
5. Does Option B remain an honest answer to the stated conditional predictive question, given that the realization setting is outside the primary baseline? Is the proxy interpretation and N5 classification sound?
6. Does the proposed \(q\) coding require any further explicit adoption in the future B1 amendment to remain compatible with frozen B1 v1.7?
7. Identify any remaining internal contradictions, overclaims, or missing pre-construction gates. Distinguish blockers from recommendations.

## 6. Current boundary

v0.5 is an unreviewed design-only draft, not a frozen protocol and not an execution authorization. The independent custodian remains unappointed. Trigger-(i) ratification and joint-consent provenance remain open. No parents, operator classes, sites, realization settings, variants, or allocations have been selected. No solver construction, diagnostics, protected-set access, fitting, sampling, simulation, or analysis is authorized.

A review of v0.5 does not authorize any such work.