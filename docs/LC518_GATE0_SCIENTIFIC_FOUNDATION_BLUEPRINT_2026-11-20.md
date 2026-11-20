# LC518 Gate 0: Scientific Foundation and Measurement-Validity Blueprint

**Document ID:** LC518-G0-SFB-2026-11-20  
**Version:** 0.3  
**Date:** 2026-11-20  
**Status:** DRAFT FOR INDEPENDENT REVIEW; HISTORICAL D1–D8 SEMANTICS ADJUDICATED; CURRENT AUTHORITY AND MEASUREMENT VALIDITY OPEN  
**Base branch:** docs/scientific-roadmap-audit-2026-11-18  
**Base commit:** 26cba397e06fbb72560dda3b68e09b2396300d3b  
**Scope:** Documentation-only scientific review. This is not a protocol amendment, bank specification, mutation allocation, freeze, statistical decision, or execution authorization.

---

## 1. Purpose

This blueprint develops the next Gate 0 investigation in explicit, reviewable steps. Its purpose is to determine whether the current LC518 proposal has:

1. a scientifically meaningful object of study;
2. diagnostic categories that represent defensible input properties;
3. a traceable relationship between the proposed mutations and those properties;
4. a reason to expect diagnostic behaviour to relate to a separate evaluation target;
5. a justified measurement in the Berger–Parker maximum-share index C_D; and
6. a contribution that is genuinely distinguishable from the closest prior work.

It does **not** assume that C_D is useful, that the eight diagnostic strata represent eight independent weaknesses, that mutations will produce the required failure patterns, or that diagnostic concentration predicts correctness on separate inputs.

### 1.1 Candidate question, not an established finding

> Within the engineered solver-version population contemplated by LC518, does the distribution of definite failures across eight prespecified diagnostic input strata, summarized by the Berger–Parker maximum-share index C_D, provide predictive information about correctness on a separate evaluation set beyond the frozen B1 conditioning variables; and, if it does, how much predictive performance does this one-number summary retain relative to the complete eight-component failure vector?

This is a candidate empirical question. The index is established. The predictive relationship is unknown. The scientific value of investigating that relationship must be demonstrated before any solver programme is reconsidered.

### 1.2 What Gate 0 must deliver

Gate 0 must answer:

- What has the closest existing research actually established?
- What important scientific question remains after that work?
- Why does resolving it matter, rather than merely filling an unoccupied space in the literature?
- What precise new knowledge could LC518 contribute?
- What evidence would force the contribution to be narrowed or abandoned?

Measurement validity and design coherence are included because a novelty claim is not meaningful if its core measurement does not represent the proposed construct. This does not convert Gate 0 into an execution-feasibility gate.

### 1.3 What this blueprint does not decide

It does not select parent solvers, operator classes, mutations, realization settings, variant counts, a protected evaluation set, scoring rules, or a new inferential target. It does not amend B1 v1.7 or population-design v0.21. Any recommendation that changes those records must be submitted as a separately versioned amendment under the applicable review process.

---

## 2. Important repository finding: D1–D8 are documented, but current authority is unresolved

An earlier assistant statement that the eight diagnostic strata were simply undefined was too broad. The repository contains an earlier LC518 bank-design artifact that explicitly defines D1–D8.

However, that artifact is on an earlier branch and has not been reconciled with the later population-design specification v0.21 and the accepted B1 v1.7 analysis plan. The correct status is:

**The eight-stratum taxonomy is documented in an earlier LC518 bank-design record; whether those exact definitions remain binding for the current v0.21/B1 population and evaluation target has not been established by the records compared for this blueprint.**

### 2.1 Earlier diagnostic-bank definitions

The earlier file **lc518-150/glm-handoff/BANK_DESIGN.md** defines a 64-record diagnostic bank with eight records assigned to each stratum:

| Earlier label | Name | Stated diagnostic purpose | Construction description in that artifact |
|---|---|---|---|
| D1 | boundary-amount | Boundary handling and off-by-one surfaces | Amounts around 0, 1, 2, the minimum denomination, and twice the minimum denomination |
| D2 | exact-match | Match-versus-miss discrimination | Amount equals one denomination, with distractor coins |
| D3 | unreachable | Zero-answer / empty-result behaviour | Minimum denomination exceeds amount, or a GCD condition makes the amount unreachable |
| D4 | modular-parity | Modular reasoning surfaces | Odd-coin/even-or-odd-amount patterns and GCD-2 sets at odd amounts |
| D5 | non-greedy | Greedy-trap detection | {1, 3, 4}-type examples at amounts where largest-first intuition fails |
| D6 | reorder-pairs | Order invariance | Four canonical instances, each represented in two coin-array orderings |
| D7 | wide-n | Scale in number of denominations | Large coin-array sizes |
| D8 | large-amount | Scale in amount | Large target amounts |

These labels describe predefined input-construction categories and diagnostic purposes. They are **not** eight proven causal mechanisms, eight independently verified defect classes, or eight mutually exclusive latent weaknesses.

### 2.2 Exposure balance is partly specified, but dependence matters

In the earlier bank design, D1–D8 each contain eight diagnostic records. The design is therefore balanced by **record count**.

That does not make all eight records in every stratum independent opportunities. D6 explicitly consists of four canonical instances with two orderings each. Its eight rows represent four canonical input cases subjected to an ordering transformation. Those paired observations can test order sensitivity, but their dependence must be disclosed.

The audit must distinguish:

- record count;
- distinct canonical input count;
- paired/reordered record structure;
- independent challenge opportunities, to the extent that this can be defended; and
- the exact counting rule used by f_j and C_D.

The frozen statistic may count registered record-level failures. This blueprint does not change that definition. It requires the dependence structure to be described so that record balance is not mistaken for independent exposure balance.

### 2.3 The earlier held-out strata are not the diagnostic strata

The same earlier bank-design artifact separately defines held-out H1–H8. They are not D1–D8 repeated under matching labels. The earlier design gives held-out record counts of 12, 12, 8, 8, 10, 10, 8, and 12, respectively, for a total of 80. Their implied record weights are unequal.

A D1-to-H1, D2-to-H2 mapping is therefore prohibited unless the exact construction rules and input properties support it. The crosswalk must be based on input attributes and rules, not matching numerals or similar names.

### 2.4 Version and authority conflict

The later population-design v0.21:

- refers to eight diagnostic strata in the definition of C_D, but does not enumerate D1–D8 names and rules in its own statistic section;
- identifies the existing B1 78-record bank as exposed development material;
- proposes a new protected evaluation set for the newer confirmatory population; and
- states that a separate B1 amendment is required before a new protected set can replace the 78-record set in the accepted analysis plan.

The earlier BANK_DESIGN describes a different bank configuration, including an 80-record held-out bank. These records must not be combined or treated as interchangeable.

**No stratum definition or record count from the earlier BANK_DESIGN is promoted to current authority by this blueprint.** The controlling diagnostic bank, the 78-record B1 development bank, the earlier 80-record held-out design, and the newer protected-set proposal must be reconciled against the actual frozen manifests, hashes, and accepted specifications.

---

## 3. The scientific chain to be examined

The proposed scientific argument has this chain:

\[
\text{input properties}
\longrightarrow
\text{mutation/operator effects}
\longrightarrow
\text{diagnostic failures by stratum}
\longrightarrow
F=(f_1,\ldots,f_8)
\longrightarrow
C_D
\longrightarrow
\text{held-out correctness}.
\]

Each arrow is a separate proposition. None is established merely because the variables can be placed in one diagram.

| Link | Question | Evidence required |
|---|---|---|
| Input properties → solver challenge | What concrete property of an input is varied or stressed? | Frozen stratum rules and input-level classification |
| Mutation/operator → behaviour | What does the source transformation change, and under which input conditions can that matter? | Operator semantics, preconditions, affected program state/control/data, and source-design rationale |
| Behaviour → diagnostic failures | Which diagnostic records can expose the changed behaviour? | Rule-level mapping from operator effect to diagnostic input properties; observed evidence only if later authorized |
| Diagnostic failures → F | Does each record contribute to exactly one defined stratum count? | Frozen membership, outcome taxonomy, duplicate and dependence rules |
| F → C_D | Does maximum share represent the proposed construct, and what does it discard? | Mathematical and construct-validity argument |
| C_D → held-out correctness | Why should the diagnostic pattern transport to separate inputs? | Diagnostic-to-held-out property crosswalk and a defensible transport mechanism |

The most important missing link is not arithmetic. It is the diagnostic-to-evaluation transport relationship: why a failure profile on the diagnostic bank should carry information about correctness on the evaluation distribution.

A candidate mechanism may involve persistent input-sensitive weaknesses. That phrase is not evidence. It must be grounded in the actual operator definitions, actual input properties, and held-out input distribution. If those materials do not support the mechanism, it must not be invented after seeing outcomes.

---

## 4. Step 0 — Reconcile source authority and versions

**Purpose:** Establish which documents and bank artifacts actually govern the current LC518 design.

### 4.1 Questions to resolve

1. Which exact artifact defines the current D1–D8 diagnostic strata?
2. Does the earlier BANK_DESIGN remain authoritative, or was it superseded by a later C9 bank specification or another accepted document?
3. What are the current diagnostic bank's record count, stratum counts, canonical identities, reorder pairs, and frozen hashes?
4. Which evaluation bank is the target of the current B1 analysis: the accepted 78-record exposed development bank, the earlier 80-record held-out design, or a new protected evaluation set proposed by v0.21?
5. Are the relevant bank-generation and oracle artifacts frozen, verified, and linked to the accepted analysis plan?
6. Does the newer population design require a new B1 amendment because the record population or scoring procedure changes?

### 4.2 Procedure

- Build a source-authority table containing document path, branch, commit, blob hash, version, date, acceptance/freeze status, and the precise decision it controls.
- Retrieve and compare the full source text of the earlier BANK_DESIGN, the applicable C9 generation specification, B1 v1.7, its acceptance record, and population-design v0.21.
- Compare actual bank manifests and hashes only where their repository or authorized artifact identities are available. A design document is not proof that a bank file was generated or validated.
- Record every difference in bank size, stratum definitions, canonical identity rules, held-out membership, score weights, and custody.
- Do not resolve version conflicts by choosing the largest or newest number. The controlling authority must be explicit in an accepted source record.

### 4.3 Deliverables

- **D0.1 Source-of-truth register:** all controlling and superseded records.
- **D0.2 Bank identity register:** authoritative diagnostic and held-out manifest identities and hashes, or an explicit statement that they are unavailable/unverified.
- **D0.3 Version reconciliation:** explanation of the 64/80/78 record references and whether the new protected-set proposal changes the B1 target.
- **D0.4 Authority decision:** explicit disposition of whether the old D1–D8 definitions are binding, superseded, or unresolved.

### 4.4 Pass and stop criteria

**PASS:** every current diagnostic and evaluation record set has one authoritative, versioned source; the bank and analysis-plan relationship is explicit; no conflicting version is silently used.

**STOP / UNRESOLVED:** a source-of-truth or bank-identity conflict remains. Later semantic mapping may be done only as a comparison of historical designs, not as a claim about the current LC518 experiment.

**Prohibited:** regenerating, opening, sampling, or reusing a protected bank or its outcomes to settle a documentary conflict. This step is source-document and manifest reconciliation only, within existing access permissions.

---

## 5. Step 1 — Establish what the diagnostic strata represent

**Purpose:** Determine whether D1–D8 describe meaningful, reproducible input properties, rather than merely convenient labels.

### 5.1 Build the stratum dictionary

For each D stratum, record:

- canonical name and identifier;
- exact construction rule and parameter ranges;
- inclusion and exclusion conditions;
- input features deliberately varied;
- input features held fixed or constrained;
- diagnostic purpose stated by the bank designer;
- number of records and distinct canonical inputs;
- pairs, permutations, or repeated transformations;
- whether the record can possess properties that also appear in other strata;
- what solver behaviour the category is intended to challenge; and
- what evidence supports that intended challenge.

Do not call a stratum a “failure mechanism.” A stratum is an input category. A mechanism is an explanation of how a program or transformation produces an outcome. These are different objects.

### 5.2 Test the partition's semantics

The audit must answer:

1. Is every diagnostic record assigned to exactly one D stratum for the purpose of f_j?
2. Are the strata mutually exclusive as record assignments, even where underlying input properties overlap?
3. Is the classification rule deterministic and independent of observed solver outcomes?
4. Does sum_j f_j = k_fail hold by construction for every eligible record?
5. Are D6 permutation pairs of the same canonical instances, and how is their dependence documented?
6. Do all strata have equal record opportunity? If so, does that conceal unequal numbers of distinct canonical instances or materially different within-stratum dependence?
7. Does a stratum combine several input properties, making a single behavioural interpretation too broad?

### 5.3 Exposure and dependence audit

The earlier bank design reports eight records per D stratum, but record counts alone are insufficient. Produce a table with, for each stratum:

- number of records;
- number of unique canonical identities;
- number and size of paired groups;
- number of distinct rule patterns or subtypes;
- repeated/permuted records;
- maximum number of records contributed by one canonical challenge; and
- exact exposure denominator relevant to any proposed rate or comparison.

If a rate interpretation is proposed, the denominator must reflect the relevant opportunities. C_D is a share of observed failure records, not a rate per independent canonical challenge, and must not be described as the latter.

### 5.4 Deliverables

- **D1.1 D1–D8 dictionary** with exact, current rule references.
- **D1.2 Record-membership audit** showing one assigned stratum per record and classification exceptions.
- **D1.3 Exposure/dependence table** including the D6 canonical-pair structure.
- **D1.4 Construct interpretation note** explaining what each stratum does and does not represent.
- **D1.5 Unresolved-property ledger** for ambiguous or overlapping input properties.

### 5.5 Pass and stop criteria

**PASS:** current stratum membership is authoritative, deterministic, outcome-blind, exposure is described correctly, and the diagnostic categories have defensible input-property interpretations.

**STOP / NARROW:** categories are reproducible but too heterogeneous or weakly justified to support a common behavioural interpretation. A narrow, bank-specific descriptive study may remain possible, but a general “failure concentration” construct is not established.

**STOP / REJECT THE CURRENT MEASUREMENT:** the partition cannot be reconstructed reliably, record membership is outcome-adaptive, or failure counts can be duplicated or missed under the frozen scoring rules.

---

### 5.6 Documentary adjudication of D1–D8 (2026-11-20)

This subsection records the result of a source-level review of the earlier bank design, its later C9 replacement proposal, the earlier analysis draft, the current v0.21 population design, and the November 10 mutation-allocation search report.

#### 5.6.1 Source authority and version disposition

| Record | What it establishes | Authority for the current v0.21 population |
|---|---|---|
| Earlier BANK_DESIGN.md, version 1.0, marked FROZEN on 2026-11-01 | Defines the 64-record diagnostic bank, eight records per D1–D8 stratum, the high-level construction rule for each stratum, the 80-record held-out bank, and the canonical-identity rule | Frozen for the earlier 150-body construction-study package. It is not, by itself, proof that v0.21 adopted the same bank or that the 150-body design remains current |
| C9_GENERATION_SPEC_REVIEW.md, revision 2.6, 2026-11-02 | Provides a much more detailed proposed generator procedure, including exact D1–D8 construction details and corrected D4/D5 rules | Not owner-ratified or frozen. Its own header says it does not modify historical BANK_DESIGN v1.0. It may clarify the proposal, but its changed details cannot be treated as binding |
| ANALYSIS_SPEC_REVIEW_DRAFT.md | Describes eight D1–D8 input strata, 64 records, a separate order-pair feature family, and states that the strata are input categories rather than verified mechanisms | Explicitly review-only and not the design of record. Useful corroboration of intended interpretation, not an authority override |
| Population-design v0.21 | Refers to eight diagnostic strata in the C_D definition; says no parent or mutation mechanism has been selected; requires a future B1 amendment for a new protected evaluation set | Current design-only draft, but it does not enumerate D1–D8 names or explicitly incorporate BANK_DESIGN v1.0 by path/hash |
| November 10 mutation-allocation search review | Reports no named eight-mechanism taxonomy, no M01–M08 definitions, and no pair-to-parent allocation in the five reviewed November 6 conversation PDFs | Bounded evidence that the mutation allocation is not established in the reviewed source set. A standalone annex's existence remains unproven |

**Authority finding:** the intended meanings of D1–D8 can be recovered from the earlier frozen BANK_DESIGN v1.0. The available records do not establish that v0.21 formally adopted that exact bank specification. The count “eight” is not sufficient evidence of identity between two bank versions.

#### 5.6.2 What each earlier diagnostic stratum is designed to challenge

The table below separates the documented input challenge from what can legitimately be inferred. The high-level definitions are in frozen BANK_DESIGN v1.0. Where more exact construction detail is taken from C9 revision 2.6, it is explicitly labelled as an unratified proposal.

| Stratum | Documented input-property challenge | Exact construction detail available in the record | What the label does not establish |
|---|---|---|---|
| **D1 boundary-amount** | Small and threshold-adjacent amounts relative to the smallest denomination; intended to expose boundary and off-by-one mistakes | BANK_DESIGN lists the pattern 0, 1, 2, c_min−1, c_min, c_min+1, 2c_min, 2c_min+1. C9 spells this out as the eight ordered amounts for each drawn coin set | It does not prove that every record is a distinct boundary case. For example, when c_min=1, c_min−1=0. Nor does it identify a particular source mutation or prove an off-by-one defect occurred |
| **D2 exact-match** | A target amount exactly equals one denomination, with other denominations present as distractors; intended to test direct denomination recognition and handling of irrelevant alternatives | BANK_DESIGN: amount equals one denomination with 1–4 distractors. C9 specifies the matching coin is placed in the coin array and amount is set to that coin value | It does not establish a single “exact-match bug” or guarantee that all erroneous algorithms fail this case |
| **D3 unreachable** | Inputs for which no valid combination exists; intended to test zero-answer and empty-result handling | BANK_DESIGN identifies two constructions. C9 specifies (i) minimum denomination greater than amount and (ii) a common denomination GCD g that does not divide the amount. Both guarantee the oracle answer is zero | This is already a heterogeneous stratum: the minimum-denomination rule and the GCD divisibility rule are different mathematical reasons for unreachability. They are not one causal defect |
| **D4 modular-parity** | Parity and modular structure in denomination sets and target amounts | BANK_DESIGN describes all-odd denomination sets paired with even/odd amounts, plus denomination sets with GCD 2 and odd amounts. C9 proposes three construction subtypes: (i) two all-odd/even-amount records, (ii) two all-odd/odd-amount records, and (iii) four all-even-denomination records with GCD exactly 2 and odd amount | This is not a uniform “unreachable” category. Under the unratified C9 proposal, only subtype (iii) is guaranteed to have answer zero. The first two subtypes are parity contrasts whose reachability and combination counts depend on the actual denominations and amount. A pooled f_4 count therefore combines failures from different mathematical subtypes; its value depends partly on which subtype failures occur. The category overlaps conceptually with the GCD-based unreachable subtype of D3. Retaining D4 as a composite would require a specific rationale, fixed subtype definitions and proportions before outcomes, and mandatory subtype-level reporting. The C9 proportions (2:2:4) are proposed, not current authority |
| **D5 non-greedy** | Coin sets and amounts for which largest-first greedy choice does not produce a minimum-coin solution; intended to expose a greedy shortcut or misunderstanding of the task | Frozen BANK_DESIGN describes {1,3,4}-type examples at divergent amounts. C9 proposes replacing fixed examples with [1,4,5,6,9] at amount 8 and [1,2,4,5,6] at amount 9, plus six generated records accepted only when largest-first greedy coin count differs from the minimum-coin count | LC518 asks for the number of unbounded combinations, not the minimum number of coins. Let G be the output of the specified greedy minimum-coin strategy, M the optimal minimum-coin count, and W the correct LC518 combination count. The C9 acceptance condition G ≠ M does not establish that a solver substituting G for the LC518 answer would be wrong: that requires G ≠ W for each admitted item. The two fixed C9 examples satisfy this stronger condition: (G,M,W) = (3,2,5) for [1,4,5,6,9], amount 8, and (3,2,15) for [1,2,4,5,6], amount 9. These W values are direct counts of the unbounded denomination combinations. The six random C9 records are not shown to satisfy G ≠ W merely by the current G ≠ M filter. C9 is unratified and does not supersede the frozen v1.0 {1,3,4}-type wording |
| **D6 reorder-pairs** | Invariance to the order in which denominations are supplied; the same mathematical instance is represented in two array orderings | Four canonical instances, each emitted as an original/permuted pair, for eight records total. Each pair has the same amount and sorted denomination set and differs only in coin-array order | Eight records are four canonical input cases, not eight independent mathematical challenges. The concentration count f_6 is record-based. Each canonical input receives two record-level opportunities to contribute: PASS/PASS contributes 0, PASS/FAIL or FAIL/PASS contributes 1, and FAIL/FAIL contributes 2, even when both failures return the same wrong value. This does not mean every order-sensitive solver has an inflated C_D. It means the failed-record share and the share of distinct canonical inputs with any failure are different quantities. C_D does not itself measure order sensitivity. The earlier analysis draft proposes separate pair-level quantities, including d_order_inconsistent, but that draft is not frozen analysis authority and does not change the record-level C_D definition |
| **D7 wide-n** | Large numbers of denominations, with moderate target amounts; intended to challenge handling and iteration over wide coin arrays | n in [50,300], amount in [50,500] in BANK_DESIGN | It identifies input scale in n. It does not, by itself, establish a runtime or memory stress test, because no execution budget or resource-failure protocol is supplied by this bank definition |
| **D8 large-amount** | Large target amounts with a smaller denomination set; intended to challenge handling and iteration over the amount dimension | Amount in [2000,5000], n in [3,30] in BANK_DESIGN | It identifies input scale in amount. It does not, by itself, establish a measured runtime, memory, or complexity outcome |

#### 5.6.3 The categories are assigned strata, not mutually exclusive scientific properties

The bank uses D1–D8 as **record-assignment labels**. This is different from claiming that their underlying input properties are mutually exclusive.

A particular input can possess multiple properties: an exact-match input can also be near a boundary; an unreachable input can also have parity/GCD structure; a high-amount input can also be unreachable. The generator's stratum/rule_id assigns the record to one construction category. That single assigned label does not mean the record lacks other mathematical properties.

Consequences for interpretation:

1. The eight strata are not eight disjoint failure mechanisms.
2. Equal record counts do not prove equal numbers of independent challenge opportunities.
3. The same underlying algorithmic weakness may affect multiple strata.
4. A stratum may combine distinct mathematical subtypes, especially D3 and D4.
5. The maximum-share statistic discards the identity of the dominant stratum, even though the strata have different input meanings.

The earlier design's eight-record balance is a design fact, not evidence that the categories have equal causal importance, equal difficulty, equal independent exposure, or equal relevance to held-out correctness.

#### 5.6.4 Mutation/operator mapping: no actual mapping can be asserted

The bank strata above describe **inputs**. They do not define source-code mutations.

The current population-design v0.21 says explicitly that no mutation mechanism has been selected or assigned. Its §4 defines what a future operator-class record q must contain: transformation semantics, AST structure, operand roles/types, control-flow effects, read/write footprint, preconditions/postconditions, invariants, and permitted realization fields. That is a required schema, not a catalogue of selected operators.

The November 10 allocation review reports that, within the five reviewed November 6 conversation PDFs:
- no named candidate from the intended eight-mechanism taxonomy was identified;
- no M01–M08 or M1–M8 definitions were found;
- no pair-to-parent assignment was found;
- no per-pair SA/SB orientation or repeated-pair identity was established; and
- the later correction in Part 8 says the allocation's status is unknown and the standalone annex's existence is unproven.

Therefore the mutation column for every D stratum is:

| Diagnostic stratum | Actual selected mutation/operator class q | Parent/pair allocation | Status |
|---|---|---|---|
| D1 | Not specified in the current v0.21 record | Not established | OPEN / NOT ESTABLISHED |
| D2 | Not specified in the current v0.21 record | Not established | OPEN / NOT ESTABLISHED |
| D3 | Not specified in the current v0.21 record | Not established | OPEN / NOT ESTABLISHED |
| D4 | Not specified in the current v0.21 record | Not established | OPEN / NOT ESTABLISHED |
| D5 | Not specified in the current v0.21 record | Not established | OPEN / NOT ESTABLISHED |
| D6 | Not specified in the current v0.21 record | Not established | OPEN / NOT ESTABLISHED |
| D7 | Not specified in the current v0.21 record | Not established | OPEN / NOT ESTABLISHED |
| D8 | Not specified in the current v0.21 record | Not established | OPEN / NOT ESTABLISHED |

It would be invalid to infer D1 → boundary mutation, D2 → exact-match mutation, and so on. Those would be invented mappings. A mutation may affect several input strata, and a stratum may be sensitive to multiple mutation classes. The valid mapping must be derived from each actually selected operator's source-level preconditions/effects and the input properties in the authoritative bank. That cannot be done until an owner-authorized, versioned q catalogue and allocation exist.

#### 5.6.5 Stage 2 verdict

The documentary question “what were D1–D8 intended to represent in the earlier frozen BANK_DESIGN v1.0?” is **RESOLVED** by the table in §5.6.2.

The wider question “are those exact strata the binding diagnostic design for population-design v0.21?” remains **OPEN**, because v0.21 does not explicitly incorporate BANK_DESIGN v1.0 or enumerate the D1–D8 rules.

The question “which actual mutation classes are intended to generate the D1–D8 patterns?” remains **BLOCKED / NOT ESTABLISHED**, because no mutation classes have been selected in v0.21 and the reviewed November 6 allocation does not establish names or assignments.

Accordingly:

- **Stage 2 is no longer an unanswered list of questions:** the earlier design's input meanings, mathematical construction logic, and interpretation limits are now documented.
- **Stage 2 is not a current-design PASS:** its applicability to v0.21 and the operator-to-stratum mapping remain unresolved.
- **Gate 0 cannot close on this result alone.** The current bank-authority conflict, mutation specification gap, diagnostic-to-held-out transport, measurement validity, and literature boundary remain separate gates.


#### 5.6.6 Cross-review adjudication of authority, D4, D5 and D6 (2026-11-20)

This subsection records the points on which the GPT adjudication and the subsequent Claude critique/convergence supplied in this conversation agree. Claude corrected its earlier overstatement that D6 necessarily inflates concentration for every order-sensitive solver; GPT's narrower record-weighting formulation was accepted. This is a documentation-level convergence record, **not a formal joint sign-off**, not an owner ratification of a bank design, and not an amendment to B1 v1.7, BANK_DESIGN v1.0, C9 rev 2.6, or population-design v0.21.

**A. Authority: agreement and closure condition**

The current v0.21 design has no established controlling D1–D8 construction specification. BANK_DESIGN v1.0 is frozen for the earlier 150-body package, but its applicability to v0.21 has not been established. C9 rev 2.6 is a detailed proposal whose own status says it is not owner-ratified or frozen and does not modify v1.0. The review-only analysis draft cannot confer authority. The fact that v0.21 refers to eight strata does not prove that it adopts the identity, membership rules, record allocations, or paired structure of the earlier eight strata.

Closure requires an owner-authorized, versioned source decision that:
1. names the exact adopted diagnostic specification, revision, repository path and immutable blob identity;
2. states whether C9 rev 2.6 is adopted, rejected, or only partly adopted, with each changed rule identified;
3. identifies the authoritative diagnostic manifest and its hash, including record IDs, assigned stratum, rule IDs, canonical IDs, subtype labels/parameters, and D6 pair identities;
4. reconciles the diagnostic specification with the applicable B1 analysis plan and the evaluation-target version; and
5. records any required B1 amendment and its separate review/acceptance status.

Until this is done, the eight-stratum object over which C_D would be calculated is not fully specified for v0.21. No diagnostic outcome should be counted or interpreted as current-design evidence on the basis of an assumed v1.0/C9 mixture.

**B. D4: a composite is possible, but it is not yet justified or adopted**

The proposed C9 construction contains three subtypes, with proposed record counts 2, 2 and 4:
- all-odd denominations with an even target amount (2 records);
- all-odd denominations with an odd target amount (2 records); and
- all-even denominations with GCD exactly 2 and an odd target amount (4 records).

Only the third subtype guarantees an oracle answer of zero. The first two are parity contrasts, for which reachability and the number of combinations depend on the actual denominations and amount. The resulting pooled f_4 can therefore be driven by failures in one subtype and cannot, by itself, reveal which subtype contributed those failures.

The reviews agree that D4 **may** be retained as a deliberately composite category only if the design supplies a specific scientific rationale for combining these different input properties, fixes all subtype definitions and their proportions before any outcomes, and requires subtype-level counts and results to be reported alongside any pooled f_4 or C_D result. Subtype reporting is necessary but does not, by itself, establish that pooling is scientifically justified.

No choice has been made to retain the composite or split it. Splitting the three proposed subtypes would change the stratum count from eight to ten unless other strata were also redesigned. A split or any altered weighting would require an explicit versioned diagnostic-design decision and reconciliation with the analysis plan; it must not be introduced as an editorial change. The proposed 2:2:4 allocation is C9 text, not current authority.

**C. D5: validate against the LC518 objective, not only the auxiliary minimum-coin objective**

Define:
- G = output of the specifically declared largest-first greedy minimum-coin strategy;
- M = optimal minimum-coin count;
- W = correct LC518 unbounded-combination count.

The current C9 random-record filter G ≠ M establishes a greedy-versus-optimal minimum-coin counterexample. It does not establish that the greedy result would be wrong when substituted for the LC518 combination-count answer. For a D5 item intended to detect a solver that returns the greedy minimum-coin count in place of the combination count, the item-level validity condition must include **G ≠ W**, and the precise greedy strategy must be specified. G ≠ M alone is insufficient.

For the two fixed C9 examples, direct enumeration gives:
- coins [1,4,5,6,9], amount 8: G = 3, M = 2, W = 5;
- coins [1,2,4,5,6], amount 9: G = 3, M = 2, W = 15.

Both fixed examples therefore distinguish the specified greedy output from the LC518 answer. This verification does not establish G ≠ W for C9's six random records, nor does it ratify C9. A valid future D5 specification must provide W and the relevant G for every admitted record, with the acceptance condition checked before outcomes. It must also state whether the intended construct is specifically failure from substituting greedy minimum-coin output, rather than claiming to measure all possible misunderstandings of combination counting.

D5 failures remain genuine LC518 failures because outcomes are scored against W. The threat is to the interpretation of the diagnostic category and the concentration result, not to the oracle's definition of FAIL. Without the item-level relationship to W, a D5-dominated concentration result would be difficult to interpret as evidence about the intended diagnostic construct.

**D. D6: record weighting is explicit; the intended measurement unit is not decided**

Under the earlier record-level definition, the contributions of one D6 pair to f_6 are:

| Original | Permutation | Contribution to f_6 |
|---|---|---:|
| PASS | PASS | 0 |
| PASS | FAIL | 1 |
| FAIL | PASS | 1 |
| FAIL | FAIL | 2 |

A pair that fails both orderings contributes two failures even when both returned values are the same wrong integer. Such a pair has no value-based order inconsistency. A pair with one PASS and one FAIL contributes one failure and, when both return comparable exact integers, its returned values differ.

Therefore D6 is **record-weighted** in the current historical definition, not weighted by the number of distinct canonical mathematical inputs. Each of the four canonical inputs has two record-level opportunities to contribute to f_6. The claim must not describe C_D as a share of independent canonical challenges, and it must not claim that C_D itself measures order sensitivity. It is also too strong to say that every order-sensitive solver necessarily has inflated C_D: the precise issue is the unit of counting and the paired structure.

The review-only analysis draft defines separate pair-level order features (d_order_pairs_resolved, d_order_pairs_comparable, and d_order_inconsistent). These can describe pair behaviour, but they do not modify the record-level f_6 or C_D. In that draft, d_order_inconsistent is value-based: it counts comparable pairs whose returned exact-integer values differ. Two identical wrong integers are consistent under this definition. These features are not accepted/frozen analysis authority.

No decision has been made between retaining record-level D6 in C_D and redesigning the measurement around canonical pairs. Retaining record-level scoring requires an explicit claim about record weighting and mandatory separate pair-level reporting. Pair-weighting or replacing f_6 would change C_D's definition and requires a formally reviewed B1 amendment before it can be used.

#### 5.6.7 Required closure order

The review convergence establishes the following order. It does not authorize skipping a gate or choosing a design option by default.

1. **Resolve authority first.** Identify and ratify the exact D1–D8 specification and diagnostic manifest applicable to v0.21, and reconcile it with B1 and the evaluation target.
2. **Adjudicate D4 against that adopted specification.** Either justify a fixed composite with explicit subtype definitions/proportions and mandatory subtype reporting, or adopt a separately reviewed split/redesign. Do not assume C9's proposed 2:2:4 allocation is binding.
3. **Adjudicate D5 against the actual LC518 objective.** Specify the greedy strategy, calculate G and W for every candidate item, and require G ≠ W for items intended to expose substitution of greedy minimum-coin output. G ≠ M alone is not enough.
4. **Adjudicate D6's measurement unit.** State whether C_D counts records or canonical pairs. If record-based, preserve the record-level formula and describe its unit honestly, with pair-level order analysis reported separately. If pair-based, submit and review a formal analysis-plan amendment before using the changed statistic.
5. **Only then finalize** the current diagnostic dictionary, subtype and pair manifests, and the property-level diagnostic-to-held-out crosswalk. No outcome collection or interpretation precedes these documentary and authority decisions.

This ordering is a review plan only. It does not reopen the paused project, authorize bank access or generation, or permit solver construction, modification, compilation, execution, diagnostics, model fitting, simulation, sampling, or power analysis.

### 5.7 Evidence required to close the remaining Stage 2 items

| Remaining item | Evidence that would close it | Failure / stop condition |
|---|---|---|
| Does v0.21 use these exact D1–D8 definitions? | An accepted, versioned v0.21-linked diagnostic-bank specification or explicit amendment citing the exact BANK_DESIGN revision/blob and current bank manifest hashes | No cross-reference, conflicting rule set, or post-outcome changes to category membership |
| Are the strata assigned reproducibly? | Authoritative diagnostic manifest with each record's exact stratum, rule_id, canonical identity, rule parameters, and a deterministic reconstruction/validation record | Missing records, duplicate or ambiguous membership, outcome-informed classification, or inability to reproduce the stratum assignment |
| Is the D6 dependence correctly represented? | Pair manifest identifying four canonical IDs, original/permutation roles, shared amount and denomination set, and pair-level outcome definitions | Treating eight D6 rows as eight independent instances, or using C_D alone to claim order sensitivity |
| Is D4's composite interpretation defensible? | Adopted specification with explicit subtype labels/rules/proportions fixed pre-outcome, a rationale for pooling distinct parity/reachability properties, and mandatory subtype-level reporting; or a separately reviewed split/redesign | Pooled f_4 with no subtype identity/proportions, post-outcome reweighting, or treating the composite as one homogeneous challenge without justification |
| Does D5 test the intended LC518-related challenge? | Per-item oracle combination count W, fully specified greedy output G, and pre-outcome verification of G ≠ W for every item intended to detect greedy-output substitution | Relying only on G ≠ M, omitting the actual combination-count answer, or claiming the category measures combination-count correctness more broadly than its validated construction supports |
| Is D6's unit of analysis explicit? | Explicit decision that C_D is record-weighted or an approved B1 amendment defining a pair-weighted alternative; if record-weighted, separate pair-level outcome summaries | Calling record-level C_D a share of independent canonical inputs, claiming C_D measures order sensitivity, or changing f_6 without B1 amendment |
| What mutations correspond to these challenge properties? | Owner-authorized operator-class catalogue with complete q fingerprints, preconditions/effects, selected parent/source identities, and a predeclared operator-to-input-property mapping reviewed before any diagnostic outcomes | Missing definitions, reconstruction from aggregate allocation arithmetic, or mapping chosen after viewing outcomes |
| Do the proposed mutations actually expose the intended behaviour? | This requires a later, separately authorized empirical validation design with frozen source/inputs and an independent outcome oracle | No execution evidence; or a claimed effect that does not follow from the operator semantics and declared input conditions |

The last row is deliberately not a Gate 0 documentary result. It identifies a future evidence requirement and does not authorize the required execution.

## 6. Step 2 — Establish what the mutation/operator design changes

**Purpose:** Connect input properties to specified changes in solver behaviour without inventing mutation mechanisms.

### 6.1 Keep the two classification systems separate

- D1–D8 are diagnostic **input strata**.
- q in population-design v0.21 is proposed as a **mutation-operator class** used as a B1 identity coordinate.
- a(v) records permitted within-class realization settings.

A diagnostic stratum is not a mutation mechanism. A mutation operator is not an input category. They must be linked only through an explicit, documented mapping.

### 6.2 Semantic record required for each proposed operator class

Only after authorized mechanism specifications exist, the reviewer should require:

- operator-class name and closed definition;
- source construct or algorithmic operation affected;
- exact semantic transformation intended;
- preconditions for the transformation to alter behaviour;
- relevant input properties or predicates;
- expected change in program state, control flow, data flow, or termination;
- plausible diagnostic strata that exercise those preconditions;
- plausible held-out input properties that may exercise the same or related preconditions;
- realization coordinates a(v), including which code location, literal, threshold, or other setting varies;
- static-analysis/context evidence and its stated limits; and
- alternative explanations and cases where the transformation should have no effect.

Separate three kinds of statement:

1. **Design-intended effect:** what the operator specification says it is intended to alter.
2. **Static semantic implication:** what follows from the source transformation and its preconditions under the reviewed program semantics.
3. **Observed dynamic effect:** what happens when the resulting solver is run on inputs.

Only the first two can be reviewed in this documentary step. The third requires a separately authorized execution stage and is outside this blueprint.

### 6.3 Mutation allocation and provenance

Population-design v0.21 states that no parent has been selected and no mutation mechanism has been selected or assigned. The November 6 allocation review also records that the complete allocation is not established and the existence of a standalone annex is unproven.

Therefore:

- do not invent eight mechanisms to mirror eight diagnostic strata;
- do not reconstruct parent/pair assignments from totals or aggregate arithmetic;
- do not treat a proposed operator-class schema as an actual selected mechanism;
- do not infer that a source-level transformation has a particular dynamic footprint without evidence; and
- do not describe the unestablished allocation as lost, destroyed, recovered, or never created.

### 6.4 Deliverables

- **D2.1 Operator-class catalogue** only if an authorized, complete source record exists.
- **D2.2 Operator-to-input-property matrix** mapping each specified operator precondition/effect to relevant D-stratum properties.
- **D2.3 Realization-setting register** defining a(v) separately from q.
- **D2.4 Static-evidence dossier** for any claimed source-level semantic relationship.
- **D2.5 Unknowns register** showing missing operator definitions, allocation, parent provenance, or unresolved semantic effects.

### 6.5 Pass and stop criteria

**PASS:** each proposed operator class has a reviewable semantic specification and a defensible mapping to input properties. This establishes a design rationale, not observed behaviour.

**STOP / BLOCKED:** operator classes or their allocation are not authoritatively specified. The step remains blocked; no mutation taxonomy is reconstructed.

**REJECT A CLAIMED LINK:** the operator's semantics do not support the claimed diagnostic property, or the claimed effect is only a designer-supplied label.

---

## 7. Step 3 — Establish the diagnostic-to-held-out property connection

**Purpose:** Determine whether held-out inputs challenge the same or meaningfully related properties that the diagnostic strata are intended to expose.

Exact-input disjointness is necessary to prevent reuse of the same records. It does not, by itself, establish behavioural transfer or a useful generalization target.

### 7.1 Build a property-level crosswalk

Do not map D1 to H1 merely because both use the number 1. Use the full, authoritative construction rules and canonical input features.

The crosswalk should include, where relevant:

- boundary amounts and zero/small amounts;
- exact denomination matches and distractor denominations;
- unreachable cases and GCD/divisibility constraints;
- parity and modular structure;
- non-greedy counterexamples;
- coin-array ordering and permutation invariance;
- number of denominations / input scale;
- amount scale;
- repeated use of denominations;
- multiple distinct valid combinations; and
- other properties found in the authoritative bank specifications.

For every property, identify:
- which diagnostic records contain it;
- which held-out records contain it;
- whether the property is exact, partial, or absent in the held-out set;
- the held-out record weight, if the authoritative score uses weighting;
- whether another property co-occurs and could explain the relationship; and
- whether the same mutation/operator precondition can plausibly affect both sides.

### 7.2 Do not assume stratum-label correspondence

The earlier BANK_DESIGN has D1–D8 and separately H1–H8 with different definitions and counts. A legitimate mapping may be many-to-many. An input may be both a boundary case and an unreachable case while being assigned one primary construction stratum. The crosswalk must preserve underlying input attributes rather than force a one-to-one stratum map.

### 7.3 Evaluate target coverage and weighting

Once the authoritative evaluation bank is identified:

- report its exact record counts and target weights;
- show which structural properties dominate the target distribution;
- identify properties present diagnostically but absent from evaluation;
- identify properties common in evaluation but weakly represented diagnostically;
- identify input features correlated with each other or with stratum assignment; and
- determine whether concentration can be high because failures are concentrated in a diagnostic category whose corresponding held-out challenge has little or much target weight.

This last point is central: C_D does not identify which stratum supplies the maximum. If the identity of the dominant diagnostic stratum matters because held-out categories have unequal target weights or different behavioural implications, the same C_D value can represent very different potential evaluation risks. The blueprint must not assume away that problem.

### 7.4 Distinguish the kinds of separation

Report separately:

- exact-record disjointness;
- canonical-identity disjointness;
- structural-property overlap;
- operator-precondition overlap;
- target-distribution coverage; and
- independence assumptions, if any.

Diagnostic and held-out records may be disjoint while sharing structural properties by design. That can support a limited transfer question, but it is not evidence that diagnostic and held-out outcomes are independent or identically distributed.

### 7.5 Deliverables

- **D3.1 Diagnostic-to-held-out property crosswalk** with record-level/rule-level provenance.
- **D3.2 Held-out target-weight table** tied to the authoritative bank version.
- **D3.3 Unsupported-property report** listing diagnostic properties with no held-out counterpart and held-out properties without diagnostic coverage.
- **D3.4 Dominant-stratum ambiguity analysis** assessing whether the identity of the maximum matters to the target.
- **D3.5 Transport rationale** explaining what feature of solver behaviour is expected to persist between diagnostic and held-out inputs, with supporting source evidence and explicit assumptions.

### 7.6 Pass and stop criteria

**PASS:** diagnostic and held-out designs share relevant, explicitly documented behavioural properties; the held-out target is authoritative; and the proposed generalization claim is restricted to the overlap actually supported.

**NARROW:** only a subset of properties transfers. Any eventual claim must be restricted to that subset and the declared target distribution.

**STOP / REJECT THE TRANSPORT CLAIM:** no defensible property-level link exists, or the held-out target asks about challenges not meaningfully represented in diagnostics.

---

## 8. Step 4 — Establish whether maximum-share concentration is the right measurement

**Purpose:** Justify the specific summary C_D, not merely the existence of a failure profile.

### 8.1 Preserve the exact definition

For solver version v, let f_vj be its definite-failure count in diagnostic stratum j, j=1,...,8. Then:

\[
k_{\mathrm{fail},v}=\sum_{j=1}^{8} f_{vj},
\qquad
C_D(v)=\frac{\max_j f_{vj}}{k_{\mathrm{fail},v}}
\quad\text{when }k_{\mathrm{fail},v}>0.
\]

Unresolved outcomes remain separate as k_unresolved; they do not enter the numerator or denominator. The existing B1 convention for k_fail=0 is a labelled NO OBSERVED FAILURES sentinel; the primary B1 support rule excludes zero-failure versions and requires k_fail>=2.

### 8.2 State what the statistic captures and discards

C_D captures the largest share of observed diagnostic failures. It does not capture:

- which stratum supplies the maximum;
- the full ordering of stratum counts;
- the second-largest share;
- the remaining distribution after the maximum;
- within-stratum canonical dependence; or
- the semantic cause of a failure.

Different failure vectors can have the same C_D. Different failure vectors can also have the same k_fail but different C_D. These are arithmetic facts, not evidence of a solver-level predictive relationship.

### 8.3 Audit the exposure interpretation

The earlier diagnostic design has eight records per stratum, which balances record counts. It also contains a D6 reorder-pair dependency. The audit must state clearly that the primary C_D is a record-count share under the frozen counting convention, not a failure-rate ratio per independent canonical challenge.

If D1–D8 are not current, or their exposure counts/dependence differ, the audit must use the authoritative current design, not the older counts.

Do not divide by a revised exposure denominator or replace C_D with a rate in this step. Such a change defines a different statistic and requires a separate scientific proposal and protocol review.

### 8.4 Justify the maximum rather than another summary

The review must answer:

1. What specific behavioural property is expected to be reflected by the largest share?
2. Why should the magnitude of the largest share matter independently of the identity of the largest stratum?
3. Why should the maximum be more relevant than the second-largest share, a concentration index using all categories, or the full vector?
4. Does the held-out target give different weights to properties that C_D treats symmetrically?
5. Could the statistic be high because of small counts or a single dominant paired challenge rather than a stable solver property?
6. Is C_D being interpreted as localization, heterogeneity, severity, or simply a distributional summary? Choose only an interpretation supported by the definitions and evidence.

If the scientific rationale depends on which input property fails, the maximum share without its identity may be an inadequate measurement. If the rationale depends on concentration irrespective of category identity, that invariance itself must be defended.

### 8.5 Required comparator logic

The scientific comparison must distinguish:

- **Baseline comparison:** does C_D add predictive value beyond the exact frozen B1 baseline?
- **Full-vector comparison:** how does C_D perform relative to F=(f_1,...,f_8) on the same prediction target?
- **Optional summaries:** second-largest share, Herfindahl concentration, and entropy may be recorded as possible sensitivity summaries, but they are not automatically mandatory arms. They should be elevated only if their constructs are justified before confirmatory outcomes.

Because C_D is a deterministic function of F, it cannot contain more underlying information than F. A compact summary could still yield useful finite-sample predictive performance because it uses fewer degrees of freedom, but that is a model-complexity/estimation argument, not a claim of greater information. A fair empirical comparison must use the same held-out population, folds, outcomes, and suitable complexity control.

**Authority warning:** the full-vector comparison is a scientific requirement proposed by this blueprint. It must not be silently added to frozen B1 v1.7. If adopted for a future study, it requires a separately reviewed B1 amendment and an explicit analysis specification.

### 8.6 Deliverables

- **D4.1 Construct statement:** exact construct claimed for C_D, and explicit non-claims.
- **D4.2 Measurement audit:** formula, exposure, dependence, zero-failure convention, unresolved handling, and data provenance.
- **D4.3 Dominant-category challenge:** whether ignoring the identity of the maximum is defensible.
- **D4.4 Comparator rationale:** B1 baseline, full-vector comparison, and justification for any optional summary.
- **D4.5 Measurement verdict:** retain C_D, retain it only as an exploratory summary, replace the primary representation through a new design, or reject the concentration direction.

### 8.7 Pass and stop criteria

**PASS:** there is a defensible construct-level reason why maximum share represents the intended property, its exposure/counting meaning is clear, and the loss of category identity does not invalidate the proposed interpretation.

**NARROW:** C_D is defensible only as a summary for the exact eight-stratum partition and finite target. No broader failure-concentration construct is claimed.

**STOP / REPLACE:** the scientific rationale requires information discarded by C_D, dominant-category identity is essential but unavailable, or the index is driven by exposure/dependence artifacts. The full vector or another representation may be considered only through a separately justified proposal, not an automatic substitution.

---

## 9. Step 5 — Reassess the novelty boundary against the closest prior work

**Purpose:** Determine whether the proposed LC518 conjunction is a meaningful extension, not merely a new use of a familiar formula.

### 9.1 Separate the constructs

The software-testing precedents identified during Gate 0 study failure structure in execution-profile space and investigate clustering, failure localization, or relationships between clusters and faults. LC518's earlier bank design instead assigns diagnostic records to predefined input-property strata and summarizes a solver version's record-level failures across those strata.

These ideas are related but not equivalent:

- data-driven execution-profile clusters are not predefined input categories;
- failure density in a cluster is not automatically the same statistic as a solver-level share of failures across eight diagnostic strata;
- a cluster's relationship to a fault is not the same question as held-out correctness of a solver version; and
- no prior result about execution-profile clustering proves that C_D predicts LC518 held-out correctness.

### 9.2 Core precedent comparison

For each closest paper, the review must record:

| Dimension | Required coding |
|---|---|
| Analysis unit | Execution, test case, cluster, program, patch, solver version, model, item, person, or response |
| Predictor | Execution profile, failure cluster, failure density, error composition, concentration summary, or full vector |
| Outcome | Failure detection, fault localization, patch correctness, score, or held-out correctness |
| Baseline | Total failure count, total score, binary correctness, other diagnostic features, or none |
| Validation | Same-data fit, random split, item holdout, solver holdout, parent holdout, or other |
| Main limitation | What the study does not establish for LC518 |

At minimum, the software failure-clustering line must include the Dickinson, Leon and Podgurski (2001), Almaghairbe and Roper (2017), and DiGiuseppe and Jones (2012) precedents already identified in Gate 0. Their source-level results and bibliographic details must be checked against the matrix and primary texts before numerical claims are used.

The psychometric, wrong-answer-profile, and LLM response-pattern literature remains relevant to the broader premise that compositions can carry information, but it is not direct evidence for the LC518 unit, measurement, or outcome.

### 9.3 Novelty statement test

A candidate contribution can be considered only if the literature assessment supports a specific distinction across the combination of:

1. solver-version-level unit;
2. failure counts assigned to fixed diagnostic input-property strata;
3. a prespecified maximum-share concentration summary;
4. a separate held-out solver-correctness target;
5. an exact baseline including the frozen B1 cell variables;
6. parent-grouped held-out prediction in the declared engineered population; and
7. comparison with the full diagnostic failure vector.

Finding no paper with exactly the same words is insufficient. Reviewers must search for functional equivalents, including studies that call the inputs categories, test families, execution profiles, failure modes, or test partitions.

### 9.4 Deliverables

- **D5.1 Core precedent table** with all required fields.
- **D5.2 Source-verified claim register** for every reported number or finding used to motivate LC518.
- **D5.3 Search and citation-chase record** with queries, databases, dates, result counts, full exports where available, exclusions, and backward/forward citations.
- **D5.4 Novelty boundary statement** specifying what is already established, what remains unknown, and what exact distinction LC518 might add.
- **D5.5 Withdrawal rules** stating which prior finding would eliminate or narrow the candidate contribution.

### 9.5 Pass and stop criteria

**PASS:** a meaningful, evidence-supported gap remains at the level of unit, measurement, outcome, baseline, and validation, and the contribution has scientific importance beyond a new application of a known index.

**NARROW:** existing work covers some of the conjunction. LC518 may claim only the unsupported remainder, with limitations explicit.

**STOP / NO NOVELTY:** a close precedent already establishes the same substantive contribution, or the only difference is a dataset/label substitution without a defensible scientific advance.

---

## 10. Step 6 — Synthesize the evidence and make an explicit Gate 0 decision

**Purpose:** Prevent the project from moving forward on a collection of individually plausible but disconnected statements.

### 10.1 Required evidence package

The final Gate 0 package must contain:

1. authoritative source/version register;
2. current D1–D8 stratum dictionary;
3. diagnostic exposure and dependence audit;
4. operator-class and realization-setting semantics, or an explicit blocked status if those records do not exist;
5. diagnostic-to-held-out property crosswalk;
6. construct-validity and maximum-share rationale;
7. baseline/full-vector comparator rationale;
8. closest-prior-work table;
9. reproducible search and source-verification record;
10. one-paragraph candidate contribution;
11. independent reviewer challenges and GPT adjudication; and
12. explicit Gate 0 closure or non-closure decision.

### 10.2 Candidate contribution paragraph, only after the evidence package

If the preceding steps pass, the paragraph may take this form:

> Prior software-testing research has shown that failures can exhibit structure in execution-profile space, while also demonstrating that such structure does not automatically identify a unique underlying fault. LC518 examines a distinct representation: definite failures recorded for each engineered solver version across eight fixed, documented input-property strata. It tests whether the Berger–Parker maximum-share summary of that version-level diagnostic distribution adds predictive information about correctness on a separate, explicitly defined input distribution beyond the frozen B1 baseline, using the declared parent-grouped validation, and assesses how much predictive performance the compressed statistic retains relative to the complete eight-component failure vector. The study does not propose a new concentration index, infer a single fault from concentration, or claim a causal effect. Any contribution is conditional on the verified diagnostic taxonomy, operator/input-property mapping, held-out property coverage, and exact engineered population. The literature search must establish whether this combination is genuinely distinct before a novelty claim is made.

This is a drafting template, not an approved novelty statement. If the evidence does not support a clause, remove or narrow it.

### 10.3 Decision outcomes

Gate 0 must end with one explicit outcome:

- **G0-PASS-CANDIDATE:** the scientific object, measurement, transport rationale, literature distinction, and candidate paragraph are defensible. This is not empirical support and not execution GO.
- **G0-PASS-NARROWED:** a contribution remains, but only with a restricted construct, target distribution, population, or analysis claim.
- **G0-REVISE-MEASUREMENT:** the broader failure-profile question remains meaningful, but C_D is not justified as the primary summary. A new measurement proposal requires its own review and amendment.
- **G0-FAIL-NOVELTY:** closest prior work already establishes the relevant substantive contribution, or the remaining difference is not scientifically consequential.
- **G0-BLOCKED-EVIDENCE:** controlling definitions, operator records, bank authority, or primary sources are unavailable, so the decision cannot responsibly be made.

No outcome automatically authorizes solver construction, diagnostic execution, bank access, fitting, simulation, or analysis.

---

## 11. Cross-step evidence ledger

Every statement in the eventual review package must be assigned one status:

| Status | Meaning |
|---|---|
| **VERIFIED-SOURCE** | Directly supported by an identified primary document or artifact with a stable path/hash |
| **VERIFIED-ARITHMETIC** | Follows mechanically from verified source values; not an empirical claim |
| **REPORTED-NOT-REPRODUCED** | Reported by a source or reviewer but not independently reproduced |
| **INFERRED** | Reasoned interpretation from verified facts, with assumptions stated |
| **OPEN** | Not established by available evidence |
| **SUPERSEDED** | Belongs to an earlier design and is not controlling for the current study unless formally reinstated |

Starting statuses at the time this blueprint was drafted:

| Item | Current status |
|---|---|
| Mathematical definition of C_D in current population-design v0.21 | VERIFIED-SOURCE |
| Earlier D1–D8 definitions in BANK_DESIGN.md | VERIFIED-SOURCE, but current authority OPEN |
| Eight records per diagnostic stratum in that earlier design | VERIFIED-SOURCE |
| D6 contains four canonical instances × two orderings in that earlier design | VERIFIED-SOURCE |
| Earlier H1–H8 definitions and 80-record count | VERIFIED-SOURCE for that earlier design only; current authority OPEN |
| Current B1 78-record development-bank status | VERIFIED-SOURCE in v0.21/B1 records; actual bank identity must be reconciled to the governing manifest |
| New protected-set proposal | VERIFIED-SOURCE as a proposal; independent custodian and accepted amendment OPEN |
| Actual parent/operator selection in v0.21 | OPEN; v0.21 says none selected |
| Complete November 6 mutation allocation | OPEN / NOT ESTABLISHED |
| Diagnostic-to-held-out property transport | OPEN |
| Maximum-share construct validity for the current strata | OPEN |
| C_D incremental held-out predictive value | OPEN; no current LC518 result establishes it |
| C_D superiority to the full vector | OPEN; not implied by its mathematical definition |
| Current 150-variant population count | Not adopted by v0.21; do not treat as binding |
| Exposure balance | Eight records per D stratum in the earlier design; canonical/dependence balance and current authority require audit |

---

## 12. Review assignments and questions

### 12.1 GLM: active independent-review route in the current population-design record

The v0.21 record identifies GLM as the active independent-review route, with GPT adjudication. GLM should challenge:

1. whether Step 0 identifies every controlling source and resolves the 64/80/78 record discrepancy without assuming authority;
2. whether the D1–D8 dictionary distinguishes assigned stratum from overlapping input properties;
3. whether D6 dependence changes the interpretation of the record-level concentration share;
4. whether the operator-to-input-property matrix is scientifically sufficient without observing outcomes;
5. whether the D-to-H crosswalk supports an honest transfer claim;
6. whether omission of the dominant-stratum identity makes C_D unsuitable for the target;
7. whether the full-vector comparison is correctly separated from the frozen B1 plan; and
8. whether the pass/stop rules can be applied without post-outcome adaptation.

### 12.2 Claude: scientific challenge subject to current review-route authority

Claude's six-point sequence motivated this blueprint. A further Claude challenge may be useful as a separate scientific critique if the owner reopens that review route. The v0.21 source currently records the Claude route as suspended and GLM as active; this blueprint does not silently override that decision or label an informal challenge as an official review pass.

The central Claude challenge should be: **does the actual LC518 design contain a scientifically meaningful diagnostic-to-held-out connection, or does it merely place an established index on an arbitrary partition?**

### 12.3 GPT adjudication

GPT will adjudicate substantive disagreements against:
- accepted B1 v1.7 and its acceptance record;
- accepted Rev 1.4 Amendment E and its acceptance record;
- population-design v0.21 and its authority limits; and
- primary evidence cited in the Gate 0 literature record.

Reviewer agreement cannot substitute for absent source evidence. If a point remains unresolved, preserve it as OPEN rather than forcing consensus.

---

## 13. Stop rules and prohibited shortcuts

The following shortcuts are prohibited:

- Inferring causal mechanisms from diagnostic-stratum labels.
- Treating execution-profile clusters in prior papers as equivalent to predefined input strata.
- Treating the eight D categories as eight mutation mechanisms.
- Mapping D1 to H1 by label number.
- Treating eight records per stratum as eight independent canonical challenges where paired/reordered records exist.
- Interpreting C_D as a rate per independent input without a denominator and dependence argument.
- Assuming high concentration is inherently good or bad for held-out correctness.
- Ignoring the identity of the dominant stratum when held-out target weights or properties make it relevant.
- Claiming a direct or causal effect of concentration.
- Treating C_D as a novel statistic.
- Claiming C_D contains more information than the full failure vector.
- Importing the older six-family parenthesis-task mathematics or results into the current eight-stratum Coin Change design.
- Reconstructing the unestablished mutation allocation from aggregate counts, schedules, or recollection.
- Replacing missing primary evidence with abstract-only claims or unverified numerical summaries.
- Treating mathematical attainability as evidence that real solver variants can realize the required contrasts.
- Treating design feasibility as evidence of predictive value.
- Treating a successful Gate 0 review as authorization to run an experiment.

If any critical arrow in the scientific chain lacks evidence, the chain must be reported as incomplete. It may not be filled with a plausible narrative.

---

## 14. Explicit authorization boundary

This blueprint authorizes **documentary review only**.

It does not authorize:
- selecting or acquiring parent solver source;
- inspecting or modifying solver source code;
- selecting or assigning mutation mechanisms;
- reconstructing or creating the mutation allocation;
- constructing, generating, compiling, or executing solver variants;
- diagnostic probing or benchmark execution;
- accessing protected banks, oracle records, held-out outcomes, or record-level results;
- fitting models, evaluating probabilities, running permutations, simulation, sampling, or power calculations;
- running the M1-si audit on a produced manifest;
- changing B1 v1.7, Rev 1.4, population-design v0.21, bank definitions, thresholds, or scoring rules; or
- merging this blueprint into master.

The existing project pause remains in force. A later reopening requires a separate explicit owner instruction and all relevant source, provenance, custody, isolation, statistical, computational, and execution gates.

---

## 15. Source records inspected for this blueprint

The following records were retrieved from the repository. Branch and blob identities are included to make the evidence trail reproducible.

| Source | Branch | Blob SHA-1 | Use and authority limit |
|---|---|---|---|
| lc518-150/glm-handoff/BANK_DESIGN.md | gpt/lc518-claim-b1-primary-2026-11-05 | d91b8dcee05808926262c3636a891b776c03ab44 | Earlier D1–D8 and H1–H8 definitions; current authority unresolved |
| lc518-150/review-v1.2/b1-population-design/POPULATION_AND_EXPERIMENTAL_DESIGN_2026-11-16_v0.21.md | gpt/lc518-m1si-audit-2026-11-17 | 8af908f6b0ad4cd060194a0a63f4914939f07756 | Current population-design draft, conditional claim, q/a distinction, M1-si support, non-authorization |
| lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/B1_ANALYSIS_PLAN_2026-11-14_v1.7.md | gpt/lc518-m1si-audit-2026-11-17 | 8c666e501a31726c728447d155045c0b20adc178 | Symbolic B1 analysis plan; interpret with separate acceptance record |
| lc518-150/review-v1.2/b1-m1-joint-incidence-feasibility/GPT_ACCEPTANCE_RECORD_B1_ANALYSIS_PLAN_V1.7_2026-11-14.md | gpt/lc518-m1si-audit-2026-11-17 | ea51d72f4f85c5d832d72add561b4c93472c364a | Authoritative acceptance/freeze of symbolic B1 v1.7; explicitly not execution GO |
| lc518-150/review-v1.2/analysis-revision-2026-11-02/C9_GENERATION_SPEC_REVIEW.md | gpt/lc518-claim-b1-primary-2026-11-05 | bd9f13fee63ee2716345447461bf3b8bcd904eaa | Earlier bank-generation review and identified construction issues; not by itself proof of current bank authority |
| lc518-150/glm-handoff/ANALYSIS_SPEC_REVIEW_DRAFT.md | gpt/lc518-claim-b1-primary-2026-11-05 | c47760b1ca9121291f600db87b1e90665d57b8f6 | Review-only analysis draft; corroborates D1–D8 input-category interpretation and D6 pair-dependence treatment; not a frozen analysis authority |
| lc518-150/engineering/README.md | gpt/lc518-m1si-audit-2026-11-17 | bd4083bdbfdc099367535aa1effbe8620310e371 | M1-si utility scope and limits; does not establish scientific validity or authorize execution |
| reviews/AI_REVIEW_2026-11-10_MUTATION_ALLOCATION_SEARCH.md | master | 51bff158b28da12d005675b29545274c582fc1f8 | Bounded review of five supplied conversation PDFs; complete allocation not established within reviewed scope |
| engineered-study/09_CONCENTRATION_MATHEMATICAL_SPEC.md | research/concentration-math-spec | 9da18a096ef6ae9c53fa96fe85121c7727cd9dac | Historical six-family parenthesis-task math-only document; not the current eight-stratum Coin Change task |
| docs/SCIENTIFIC_ROADMAP_AUDIT_2026-11-18.md | docs/scientific-roadmap-audit-2026-11-18 | e6c1a21815794a20f08bad45342fd6cff3858ee6 | Existing documentation-only repository roadmap |
| docs/SCIENTIFIC_ROADMAP_AUDIT_REVISION_2026-11-20.md | docs/scientific-roadmap-audit-2026-11-18 | 3ada9099ec3b68a0c48c9ed35883b7f321baa0d2 | Dated roadmap revision; future updates remain separate dated records |

### 15.1 External literature cited as motivation

The Gate 0 literature record identifies:
- Dickinson, Leon and Podgurski (2001), on failure clustering in execution-profile space;
- Almaghairbe and Roper (2017), on failure enrichment in smaller execution-profile clusters and variation across systems/settings; and
- DiGiuseppe and Jones (2012), on the non-equivalence of execution-profile clusters and single underlying faults.

These are relevant motivation and limitation sources. Their measurement units and predictors differ from LC518's predefined input strata. No numerical claim from them is promoted here without the primary-source verification recorded in the Gate 0 evidence matrix.

---

## 16. Review disposition

This document remains a blueprint for critique and is not accepted merely because the cross-review has converged on several findings. The convergence recorded in §5.6.6 is technical agreement on the identified issues and closure conditions, not a formal joint sign-off or owner ratification.

The next review work is ordered, not open-ended:

1. Resolve the current source-authority question by identifying the exact diagnostic specification and manifest that v0.21 is to use.
2. Adjudicate D4 against that adopted source: a composite is possible only with a specific rationale, fixed pre-outcome subtype definitions/proportions, and mandatory subtype reporting; otherwise a separately reviewed redesign is required.
3. Adjudicate D5 using the actual LC518 combinations-count answer W. For a greedy-substitution probe, G ≠ W must be checked per item; G ≠ M alone is inadequate.
4. Decide whether D6 contributes to C_D as records or canonical pairs. The historical formula is record-weighted; pair-level measures are separate and do not silently change it.
5. Complete the diagnostic-to-held-out property crosswalk only after the controlling diagnostic and evaluation sources are established.

The mutation-to-stratum map remains blocked until actual operator classes are authoritatively specified. No mapping may be invented from stratum names. The exact closure evidence and stop conditions are in §§5.6.6–5.7.

**Current status: DRAFT FOR INDEPENDENT REVIEW. Current measurement design is NOT ACCEPTED; Gate 0 remains OPEN. Project pause unchanged.**

**End of blueprint.**
