# Claude Review Handoff: LC518 Population and Experimental Design v0.6

**Date:** 2026-11-15  
**Status:** READ-ONLY REVIEW REQUEST, NOT A FREEZE RECORD  
**Repository branch:** \`gpt/b1-computational-plan-2026-11-14\`

## 1. Review target and provenance

Please review the complete population and experimental design specification v0.6:

- **Path:** \`lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-15_v0.6.md\`
- **Last content-changing commit for v0.6:** \`66c6117d65b20179c29fb95bb9d43ed87de2f75b\`
- **Blob:** \`367f3fc12956a546e85b39a749bbaf16b8a95fb4\`
- **Predecessor v0.5 blob:** \`434551c76f7dffd5f1e0b03e20491df969ff10ce\`, unchanged.

The v0.5 commit record is clarified in v0.6 §0.7:
- \`8f9aa28968257ed9d391de2bed2056ef9648ba8a\` is the last commit that changed v0.5 content.
- \`667fbca8d3b588068cf0807002422f46868e0b44\` is the later branch snapshot adding the review handoff.
- Both expose the same v0.5 blob \`434551c76f7dffd5f1e0b03e20491df969ff10ce\`.

These are distinct commit roles, not conflicting file identities. The blob identifies the bytes.

## 2. Domain clarification

**LC518 is a computer-science and software-engineering study.** The terms “mutation,” “mutation operator,” “variant,” “parent,” and “realization setting” refer to source-code transformations and derived software implementations. There are no biological, genetic, or organism-level meanings.

In this project:
- A **mutation** is a controlled transformation applied to solver source code.
- A **mutation operator** is the specified source-code transformation rule.
- A **parent** is an original solver implementation from which controlled software variants are derived.
- A **variant** is a traceable, modified solver implementation.
- A **realization setting** specifies a permitted within-operator-class realization, such as an allowed parameter value or a source site that passes the declared equivalence tests.

This clarification concerns technical domain and terminology only. It does not change the research question, statistical estimand, or design.

## 3. Decision history: Option A versus Option B

Please preserve the actual decision history:

- In the review of v0.3, Claude recommended **Option A**: condition the primary analysis on the realization-setting vector \(\mathbf a(v)\), with identifiability reported.
- Claude also said **Option B** could be acceptable if the claim explicitly named the realization-setting limitation.
- GPT independently chose **Option B** for v0.4: retain the primary exact-cell target \((q,Z,k,\ell)\), leave \(\mathbf a(v)\) outside the primary baseline, and prohibit direct, causal, or parameter-independent interpretation of a positive result.
- Claude's v0.4 review found that Option B was stated consistently and that the proxy and non-identifiability limitations were correctly expressed. Claude did not retract its earlier preference for Option A.

Option B remains GPT's adjudicated decision, not a joint GPT/Claude preference. Please challenge its substance if warranted; do not revise the historical attribution.

## 4. Main changes in v0.6

### 4.1 Canonical representation and equivalence

Section 4.1.1a adds:
- a pinned static-analysis profile covering compiler/front-end/parser, build and preprocessing configuration, symbol and dispatch resolution, call-graph mode, points-to/alias configuration, CFG/exception model, abstract domains and analysis options;
- a deterministic typed, edge-labelled graph representation and pinned canonical serializer/graph-labelling implementation;
- canonical UTF-8 serialization and a SHA-256 site-context identifier \(H_{g,q}(s)\);
- exact canonical-byte equality as the equivalence relation, with reflexivity, symmetry and transitivity stated explicitly;
- hash equality as an integrity/index check only, never a substitute for byte comparison.

Please challenge whether this is sufficiently specified without selecting tool versions before the parent language and build configuration are known. The profile must be frozen before candidate-site enumeration.

### 4.2 Control-flow position

Section 4.1.5(B) makes the candidate site a distinguished node in a rooted, edge-labelled canonical CFG. The graph is anchored by region/function entry, normal and exceptional exits, loop headers/latches/exits, and typed branch/exception/call/return edges. It also records the target's dominance, post-dominance, frontier, loop and edge-distance descriptors. The exact target-marked graph serialization, not a subset of summary metrics, is decisive.

### 4.3 Value-level context

Section 4.1.5(C) requires a sound abstract over-approximation of relevant operand values, reaching definitions, path predicates, alias/effect and state information, and the operator's abstract transfer/effect profile.

For site relocation, candidate sites must have exactly equal canonical abstract input/path/state/effect bundles at the same shared operator-parameter settings. TOP/unknown or unresolved information fails closed for site selection.

Deliberate literal/threshold parameter variation is treated separately as an explicit \(\mathbf a(v)\) coordinate. The relation of each allowed parameter value to the reachable input range and its abstract transfer/effect profile must be recorded. Parameter effect may differ across those intentionally varied levels; that is the designed realization variation, not a claim of parameter-independent concentration effect.

### 4.4 Candidate inventory, configuration, and mutation scope

Section 4.1.6 requires a complete candidate-site inventory relative to a frozen syntactic search frame, including rejected sites and reasons, with the profile and output signatures hashed before construction.

The population design also adopts one mutation-operator invocation \(q\) per variant. A single invocation may produce coordinated edit hunks that jointly implement that one operator; independent operator invocations cannot be combined in one variant. Please assess whether this restriction is consistent with the controlling B1/M1 scope and whether the interaction clause is now correctly limited.

## 5. Requested independent review

Please review v0.6 against accepted B1 v1.7 and the controlling Rev 1.4 Amendment E specification. In particular:

1. Is exact canonical-byte equality with a pinned profile sufficient to make the site equivalence relation reproducible and transitive? What normalization remains underdefined?
2. Does the target-marked rooted CFG and its anchors distinguish the positional differences Claude identified? Are any edge classes, region boundaries, or positional invariants missing?
3. Is the abstract interpretation requirement sound and sufficiently precise for value-sensitive operators? Could it still classify materially different contexts as equivalent? Is its fail-closed rule appropriate?
4. Is the distinction between site relocation and intentional parameter-level variation coherent? Are the abstract transfer/effect summaries sufficient to record how threshold/literal settings relate to reachable value ranges?
5. Is the call-graph check useful as a resolution-integrity safeguard, or is any part redundant or misleading?
6. Is the candidate-site inventory complete and frozen in a reproducible way? Are the search frame and rejection reasons sufficiently specified?
7. Is the static-analysis profile complete, including the toolchain, build configuration, call-graph mode, points-to/alias settings, CFG/exception model and abstract-domain options?
8. Is exactly one operator invocation per version compatible with the accepted B1/M1 identity model? Distinguish a single atomic operator invocation with multiple coordinated edit hunks from multiple independent mutations.
9. Identify any remaining contradictions, overclaims, or gates missing before population/design freeze. Classify each finding as blocking or recommended.

Please provide the review only. No repository changes, source acquisition, site enumeration, implementation, or execution is part of this request.

## 6. Current boundary

v0.6 is an unreviewed, design-only draft. It is not frozen and is not an execution authorization. The independent custodian remains unappointed. Trigger-(i) ratification and the joint-consent provenance gap remain open. No parent, operator class, candidate site, realization setting, variant, or allocation has been selected. No solver construction, diagnostics, protected-set access, fitting, sampling, simulation, or analysis is authorized.

A review of v0.6 does not authorize any such work.