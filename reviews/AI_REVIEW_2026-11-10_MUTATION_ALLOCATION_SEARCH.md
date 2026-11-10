# GPT supplemental review: expanded search of the November 6 mutation-design conversations

**Date:** 2026-11-10  
**Status:** Supplemental evidence report for independent Claude review. This report does not alter the A2 protocol, establish an allocation, authorize construction, or ratify any earlier audit record.

## 1. Purpose and scope

Claude asked for three refinements before accepting the all-C classification: (1) broaden the E1 search beyond the word *mechanism* and *taxonomy*; (2) provide a page-indexed audit trail of mentions screened and rejected as mutation-taxonomy evidence; and (3) broaden the E4 search to common repetition wording. Claude also asked for PDF extraction quality and OCR disclosure.

This report re-runs those checks against the five PDFs supplied by the owner as the November 6 conversation sequence, Parts 4 through 8, in that order. It also rechecks the nominal 90 count, the scope of the protocol sign-off, and whether any later material in the five PDFs supplies partial assignments.

The scope is exactly these five uploaded source files:

| Part | File | Pages | SHA-256 |
|---|---|---:|---|
| 4 | `Audit Recovery Steps (4).pdf` | 15 | `306c3a3e546fae308f0f0972db97268ba6fd8546690c83a973c999f0b0b9c010` |
| 5 | `Audit Recovery Steps (5).pdf` | 88 | `63cec5431b417de671515917d8581f131ccd1650006a8c3c26dbff62fe3c3c12` |
| 6 | `Audit Recovery Steps (6).pdf` | 306 | `711c0794e851b6d1d1f14495b4e0aae5ca43abd723756c84d7d071442c140d8c` |
| 7 | `Audit Recovery Steps (7).pdf` | 33 | `5a283729f9afc418bd40d9a73633b7c34efaa646209c5e96442a6e4298642443` |
| 8 | `Audit Recovery Steps (8).pdf` | 21 | `589cd90daec893d2dec403e81da17daf914f9dcc7ea6fabf509381fa3469b1ac` |

Total: **463 pages**. Page references below are PDF page numbers, not printed conversation timestamps.

## 2. Extraction quality and OCR disclosure

Text was extracted from every page using PyMuPDF (`page.get_text("text")`). No OCR was used.

All 463 pages returned extractable text. No page returned fewer than 100 non-whitespace characters. The lowest page-level counts were:

| Part | Lowest page | Extracted characters on that page |
|---|---:|---:|
| 4 | 15 | 229 |
| 5 | 42 | 1,102 |
| 6 | 306 | 1,472 |
| 7 | 33 | 848 |
| 8 | 21 | 447 |

The lowest-text page in each PDF was rendered and visually checked. These pages contained visible text; none was a scanned, image-only page requiring OCR. Part 5 page 42 contains code/output as well as conversation text, and its extracted text is present. The extraction therefore supports a text search across the supplied PDFs, while not claiming that text extraction can recover information that was never present in the PDF itself.

## 3. E1 expanded search

### 3.1 Search vocabulary

Every page in Parts 4-8 was searched for these terms and their listed inflections:

- `class`, `classes`
- `type`, `types`
- `kind`, `kinds`
- `category`, `categories`
- `defect`, `defects`, `defective`
- `failure mode`, `failure modes`
- `fault`, `faults`
- `mechanism`, `mechanisms`
- `taxonomy`, `taxonomies`
- `mutant`, `mutants`
- Additional identifiers/phrases: `eight-mechanism`, `eight mechanisms`, `M01`-`M08`, and `M1`-`M8`

The term `mechanism` produced many generic references to the B1 estimand, support cells, audit criteria and structural arithmetic. It was not treated as evidence of a named mechanism. The candidate-screen ledger below identifies the substantive page groups that could plausibly be confused with taxonomy or fault definitions.

### 3.2 Search counts

Counts below are occurrences and pages containing at least one occurrence, across all five PDFs. Repeated quotations of the same protocol text in successive conversation turns account for many repeats.

| Term | Occurrences | Pages containing term | Result relevant to E1 |
|---|---:|---:|---|
| class/classes | 42 | 30 | Hits refer to verdict categories, evidence classes, ambiguity classes, or document-fidelity incident classes, not the eight mutation mechanisms. |
| type/types | 0 | 0 | No hit. |
| kind/kinds | 9 | 9 | Generic phrases such as “different in kind” or “kind of post-hoc choice”; no mutation taxonomy. |
| category/categories | 10 | 9 | Verdict categories or audit/reporting categories; no mechanism categories. |
| defect/defects/defective | 46 | 46 | Mostly the C1/C6 requirement that an annex define defects, or general remarks that an allocation is not proven defective. No concrete eight-mechanism definitions. Three Part 8 hits concern the separate C9 bank-generator review. |
| failure mode/failure modes | 0 | 0 | No hit. |
| fault/faults | 0 | 0 | No hit. |
| mechanism/mechanisms | 780 | 247 | Generic references to mechanisms as variables or audit axes; no named set appears. |
| taxonomy/taxonomies | 59 | 49 | Mostly references to the required but unsupplied taxonomy. The Part 8 assertion and its subsequent retraction are discussed below. |
| mutant/mutants | 0 | 0 | No hit. |

No `M01`-`M08` or `M1`-`M8` mechanism identifiers were found. No list of eight candidate names was found.

### 3.3 Page-indexed screened mentions and dispositions

This is the candidate-screen list, not a claim that every generic use of the word “mechanism” is separately meaningful. Entries are grouped where the same protocol passage is repeated in later revisions.

| Source pages | Mention screened | Disposition |
|---|---|---|
| Part 4, pp. 2, 4, 11 | “Individual mutation identity/mechanism” in the B1 target and discussion of the support rule. | Generic target variable. No mechanism name, definition, or taxonomy membership. Part 4 p. 11's “repeat it” refers to repeating an earlier reasoning error, not repeating a mutation pair. |
| Part 4, p. 14 | A2-static summary says the bank generator contains “no taxonomy, no pair schedule, no assignments.” | Direct statement of absence in that audit, not taxonomy content. The same page's early “annex does not exist” framing is later corrected in Part 8 p. 15. |
| Part 5, pp. 1-2, 13 | “Different in kind”; “verdict categories”; “ambiguity classes.” | Generic prose, verdict classifications and C8 ambiguity classes, not mutation categories. |
| Part 5, pp. 17-18 | Parent-family roster G01-G30, 28+2 pair arithmetic, “each mechanism appears in exactly seven base pairs,” and S-extra slot totals. | Structural arithmetic only. It gives no mechanism names and no pair-to-parent assignments. G01-G30 occur as family roster ranges, not as rows mapped to a mechanism pair. |
| Part 5, pp. 30, 39 | “Written defect definition” and examples such as `f=(2,0,0,...)` versus `f=(1,1,0,...)`. | C6 audit standard and hypothetical diagnostic distributions. These examples are not definitions of actual mutation mechanisms and do not assign a mechanism to a parent. |
| Part 5, pp. 38-39, 47 | C1 says exactly eight mechanisms must be defined, each with a written defect definition; C2/C3 define pair and orientation checks; C6 defines the required evidence. | Audit criteria describing what a supplied taxonomy/allocation must contain. The required definitions and assignments are not present in these passages. |
| Part 5, pp. 24, 32, 36, 41, 43, 54, 62-63, 70, 80 | “Defective,” “defect,” verdict categories, and “different in kind.” | Verdict or methodological language. No named mutation candidate. Part 5 p. 43 explains that C6 depends on declared defect definitions; it supplies no such definition. |
| Part 6, pp. 3, 55, 75, 110, 133, 170, 237, 263 | Repeated C1 wording: exactly eight mechanisms, each with a written defect definition that indicates intended diagnostic-stratum reach. | Repeated audit criterion. None of these pages supplies the eight definitions or names. |
| Part 6, pp. 10, 16, 48, 50, 63, 71, 103, 118-120, 128, 161, 179-181, 187, 190, 223, 230, 233-234, 246-248, 255, 259, 291, 299, 302, 304 | “Evidence classes,” verdict categories, and “incident/fidelity failure classes.” | These refer to evidence/reporting populations, verdict labels, or document-transport/composition incidents. They are not mutation classes. In particular, Part 6 p. 168 discusses a paste-fidelity failure class, not a candidate mutation. |
| Part 6, pp. 20, 22, 38, 47, 64, 77, 93, 101, 120, 134, 151, 160, 181, 195-196, 213, 221, 248, 265, 281, 290 | “Defect/defective” in the repeated audit record and protocol review. | These say absence of evidence is not evidence that the allocation is defective, or refer to review defects in the record. They do not define mutation mechanisms. |
| Part 6, pp. 29, 84, 141, 203, 272 | “Different in kind.” | Generic comparison of structural exclusions or audit evidence; no mutation type. |
| Part 7, pp. 1-2 | “Taxonomy” and “mechanism” in a summary of the audit input still required. | References to the missing content; no names or assignments. |
| Part 7, p. 8 | “Kind” in the freeze/independence boundary. | Generic wording, not taxonomy evidence. |
| Part 8, pp. 8, 16, 20 | “Defect(s)” in the discussion of C9 generator review issues, including D5/D4 and related bank-design checks. | Separate diagnostic-bank generator review, not the LC518 mutation taxonomy. |
| Part 8, pp. 11, 14 | Assertion that the eight-mechanism taxonomy, pair-to-parent assignment and S-extra allocation “were made in conversation.” | This asserts that decisions existed but does not reproduce a single mechanism name or assignment. It is expressly corrected in Part 8 p. 15 and must not be used as proof of those decisions. |
| Part 8, pp. 15-16 | Correction: status unknown, “fully designed in conversation, partly designed, or never completed”; the complete evidence requirements are listed. | Operative later correction. It supersedes the unsupported assertion on pp. 11 and 14. It does not itself provide partial allocation content. |

### 3.4 E1 assessment

No B-level candidate mechanism was identified in the five PDFs. A mention would count as B only if it identifies a named fault/mechanism as a proposed member of the intended eight-mechanism mutation taxonomy, even if the definition or approval remained incomplete. The screened hits above do not do that.

**E1 remains C for the concrete taxonomy content, with a search-scope qualification.** The expanded term search materially reduces the concern that an obvious candidate was missed because it was described as a “class,” “type,” “kind,” “category,” “defect,” or “failure mode.” It does not prove that no named mechanism was discussed in an earlier or separate conversation outside Parts 4-8. It also cannot provide name-by-name verification against a canonical list because no such list is present in these source PDFs.

## 4. E4 expanded repetition search

### 4.1 Search vocabulary and counts

Every page was searched for:

- `duplicate`, `duplicates`, `duplicated`, `duplicating`, `duplication`
- `twice`
- `again`
- `repeat`, `repeats`, `repeated`, `repeating`
- `replicate`, `replicates`, `replicated`, `replicating`, `replication`, `replications`
- `additional time`, `one more time`, `second instance`

Counts:

| Term | Occurrences | Pages containing term |
|---|---:|---:|
| duplicate* | 37 | 35 |
| twice | 7 | 7 |
| again | 2 | 2 |
| repeat* | 30 | 29 |
| replicate* | 85 | 50 |
| additional time | 14 | 14 |
| one more time | 0 | 0 |
| second instance | 0 | 0 |

### 4.2 Page-indexed E4 screening

| Source pages | Mention screened | Disposition |
|---|---|---|
| Part 4, p. 11 | “Repeat it” in the sentence about not repeating an earlier reasoning error. | Not a repeated pair. |
| Part 5, pp. 18, 25-26 | 28+2 schedule, “two preselected replicated pairs,” and corrected replication-incidence arithmetic. | Explicit structural schedule only. No pair identities are named. Part 5 p. 25 specifically corrects the assumption that the repeated pairs necessarily share no mechanism; it still does not identify them. |
| Part 5, pp. 35, 38, 40, 47, 52, 66, 70, 80, 82 | Revisions and repeated renderings of C2: all 28 pairs at least once, two distinct preselected pairs each once more, total 30 assignments. | Audit rule repeated in successive document versions. No actual pair is named. |
| Part 5, pp. 11, 13, 29, 35, 48-49, 61 | “Duplicate” references, principally duplicate base-source hashes, archive fragments, or identity/deduplication rules. | Duplicate parent identity or archive objects, not repeated mutation-pair allocation. |
| Part 5, pp. 25, 70, 80 | “Repeat” or replication wording in revision history and incidence explanations. | Structural rule or correction history only. No repeated pair identity. |
| Part 6, pp. 4, 55, 110, 171, 238 | Explicit C2 text: two distinct, preselected pairs appear one additional time each. | The schedule rule is restated. Pair identities remain unspecified. |
| Part 6, pp. 5, 9, 24, 28, 39-40, 52, 56, 62, 74, 79, 83, 93-95, 111, 118, 132, 137, 141, 151-153, 172, 178, 199, 203, 213, 215, 239, 245, 267-268, 272, 282-283 | Repeated C2/C3 protocol text, duplicate-source identity rules, or revision/changelog references. | Repeated copies of criteria or parent-hash deduplication. No pair-to-parent assignment or repeated-pair identity. |
| Part 6, pp. 8, 19, 29, 50, 61, 84, 94, 116, 142, 152, 177, 193-194, 204, 214, 230, 244, 262, 272, 282, 298 | General “repeat/repeated/again” wording in process, review and document-history discussion. | No specific mutation pair is identified. |
| Part 7, p. 30 | “Repeated checks” in Claude's proposed single hash-verification step for Rev 11. | Repeated verification attempts, not pair replication. |
| Part 8, pp. 4, 9 | “Repeat” in protocol-freeze and process discussion. | Not mutation-pair allocation. |
| Part 8, pp. 15-16 | Repeated references to earlier wording and the required evidence of advance selection for the two repeated pairs. | Corrective/process language and a statement of what proof would be required; no pair identities. |
| Part 8, pp. 18, 20 | “Repeated-use witnesses” in the C9 diagnostic-bank review. | Bank-input reuse witnesses, not the LC518 mutation pair schedule. |

### 4.3 Additional identifier search

The following identifiers were also checked:

- `G01`-`G30`: found only in the parent-family roster. The roster appears in Part 5 pp. 17-18 and is repeated in Part 6 pp. 24, 40, 79, 95, 137, 153, 199, 215, 267 and 283. No parent ID is mapped to a mechanism pair in those occurrences.
- `S001`-`S150`: no hit.
- `M1`-`M8`: no hit.
- `pair_id`: appears in Part 8 p. 20 in a list of LC518 bank-record serialization fields. It is not a mutation-pair assignment.

### 4.4 E4 assessment

**E4 remains C for the identity of the two repeated pairs.** The count of two, their distinctness, and their preconstruction selection are explicit structural requirements. The two pair identities and evidence of their actual preselection are not supplied. No later passage in Parts 6-8 provides a partial repeated-pair identity.

## 5. The nominal 90 singly mutated versions

The number 90 is **explicitly stated** in the conversation, and its arithmetic decomposition is also stated. It is not merely a number inferred by this review.

- Part 4 p. 1: Claude challenges “90 singly mutated versions” as arithmetic from 30 parents with SA, SB and S-extra, says it is plausible but unverified, and notes S-extra is annex content.
- Part 4 p. 3: the operative wording states: “90 singly mutated versions is the intended nominal count, not a verified realized count, because S-extra balancing is annex content.”
- Part 5 p. 18: the structural decomposition is written out: 30 parents × 2 SA/SB slots = 60; 30 S-extra slots; total nominal single-mutation versions = 90. The same passage states that the exact S-extra split is annex content and that nominal slot totals are not verified distinct-parent counts.

Therefore the register should say: **90 is an explicitly stated nominal design count, supported by the structural arithmetic `30 × 2 + 30 = 90`; it is not a realized count and does not reveal any specific assignments.** The “six mechanisms at four and two at three” distribution is an audit expectation derived from the stated balancing rule, not evidence of the actual S-extra mapping.

## 6. Scope of the joint protocol sign-off

Part 6 pp. 305-306 is decisive.

Part 6 p. 305 records “Joint protocol text sign-off” and enumerates the three post-sign-off changes. It says “No criterion changed.”

Part 6 p. 306 states:

> It settles the protocol text only. It is not a freeze event and authorizes nothing: no freeze, no auditor appointment, no annex inspection, no construction, no execution, no commit.

The same page records the allocation state as `BLOCKED / NOT ASSESSABLE`, with 0/150 bodies and no construction.

Thus the sign-off covers the **audit criteria and protocol text that govern E1-E6**. It does not sign off the actual E1-E6 content. The sign-off cannot turn an audit requirement into an actual taxonomy, pair schedule, orientation table, repeated-pair identity, S-extra assignment or compatibility mapping.

## 7. Did Parts 6-8 add any partial allocation?

I searched the full remaining sequence, not merely the final Rev 11 pages.

- Part 6 through p. 304 contains successive protocol revisions and review records. Later C1-C8 text refines the standards for assessing supplied evidence. No actual mechanism names, pair-to-parent rows, per-pair A/B orientations, repeated-pair identities, S-extra assignments or compatibility mapping appear.
- Part 6 pp. 305-306 records text sign-off only and explicitly says the annex remains unavailable.
- Part 7 contains freeze and byte-verification discussion. It does not supply mutation assignments. Part 7 p. 30 concerns a one-time protocol hash check.
- Part 8 pp. 11 and 14 contain the assertion that the taxonomy, pair assignment and S-extra allocation were made in conversation. Those passages do not display any of the content. Part 8 p. 15 explicitly retracts the presumption that a complete allocation or standalone annex exists and says the status is unknown: fully designed in conversation, partly designed, or never completed. Part 8 p. 16 lists the evidence needed to establish completeness. This later correction supersedes the unsupported assertion; it is not itself a partial allocation.
- Part 8 pp. 18 and 20 discuss repeated-use witnesses and bank-generation checks. These concern the C9 input-bank design, not the mutation pair schedule.

No partial allocation was identified in Parts 6-8.

## 8. Revised classification

| Element | Explicit structural rule | Actual content in Parts 4-8 | Classification |
|---|---|---|---|
| E1. Eight-mechanism taxonomy | Exactly eight mechanisms, each with a defect definition and intended stratum reach | No named candidate list or actual definitions found. Broadened lexical screen complete for Parts 4-8; no canonical list exists for name-by-name comparison. | **C, qualified** |
| E2. Pair-to-parent allocation | 28 pairs once + two distinct preselected repetitions; 30 assignments mapped one-to-one to 30 parent IDs | No pair-to-parent rows found. G01-G30 occur as roster only. | **C** |
| E3. SA/SB orientation | SA/B role semantics explicit; per-pair orientation rule required | No per-pair orientation or pair assignment found. | **C** |
| E4. Repeated pairs | Two distinct pairs, selected before construction, each one additional time | No identities or preselection evidence found. | **C** |
| E5. S-extra | 30 slots, balanced across eight mechanisms; six-at-four/two-at-three is the arithmetic expectation | No mechanism-to-parent assignments or exact distribution identities found. | **C** |
| E6. Parent-family compatibility | Compatibility report required; incompatible mutations must not be silently rewritten or substituted | No mechanism-to-family mapping found. | **C** |

**Overall finding:** The five supplied conversations contain explicit structural requirements, nominal arithmetic, audit criteria and procedural sign-off. They do not contain the actual six allocation contents. E1's earlier qualification is retained: no named candidate was found after broadening the vocabulary, but the claim is bounded to these five PDFs and cannot be checked against a canonical list of eight names that is absent from the record.

## 9. Limitations and review request

1. This search covers Parts 4-8 only. It does not search earlier or separate conversations, owner email, other machines, or backups.
2. The lexical search does not prove that a semantically described mutation could not appear without any of the searched words. The candidate-screen list makes the substantive ambiguous hits visible, but it is not a substitute for a source list supplied by the author of the taxonomy.
3. PDF page numbers are reliable source locators. Individual message timestamps are not supplied consistently by these PDF exports, so this report does not invent them.
4. No mutation allocation was reconstructed, inferred from the 30×5 total, or generated from the arithmetic.

**Requested Claude review:** please challenge (a) the E1 candidate-screen dispositions, especially Part 8 pp. 11 and 15; (b) the E4 classification of every repetition hit as non-assignment evidence; (c) the distinction between the explicit nominal 90 count and its unverified realization; and (d) the statement that Part 6 pp. 305-306 signed off criteria but not allocation content. Please report any specific overlooked candidate with its exact Part and PDF page.

## Appendix A. Complete lexical hit-page index

The following page lists are the mechanical search result, included so Claude can spot-check the screen without relying on my summary. `P4:11` means Part 4, PDF page 11. Lists are for the broadened terms in §§3.1 and 4.1. Pages can contain several terms. A hit is not itself evidence of allocation content.

### A1. E1 term-page index

| Term | Part/page locations |
|---|---|
| class/classes | P5: 13; P6: 2, 10, 16, 48, 50, 63, 71, 103, 118, 119, 128, 161, 168, 179, 180, 187, 190, 223, 230, 233, 234, 246, 247, 255, 259, 291, 299, 302, 304 |
| type/types | No hits |
| kind/kinds | P5: 1, 2, 70; P6: 29, 84, 141, 203, 272; P7: 8 |
| category/categories | P5: 2, 31, 41, 53; P6: 11, 63, 120, 180, 248 |
| defect/defects/defective | P5: 24, 30, 32, 36, 38, 39, 41, 43, 47, 54, 62, 63, 80; P6: 3, 11, 20, 22, 38, 47, 55, 64, 75, 77, 93, 101, 110, 120, 133, 134, 151, 160, 170, 181, 195, 196, 213, 221, 237, 248, 263, 265, 281, 290; P8: 8, 16, 20 |
| failure mode/failure modes | No hits |
| fault/faults | No hits |
| mechanism/mechanisms | 247 pages; 780 occurrences. The large count is dominated by repeated generic estimand, criterion, support-cell and arithmetic references. The substantive candidate passages are itemized in §3.3. |
| taxonomy/taxonomies | P4: 14; P5: 18, 26, 36, 37, 38, 46, 47, 62, 65, 68, 82, 86; P6: 3, 21, 23, 26, 27, 41, 45, 54, 55, 75, 78, 81, 95, 100, 109, 110, 133, 136, 139, 154, 158, 170, 195, 198, 201, 215, 220, 237, 263, 266, 270, 284, 288; P7: 1; P8: 11, 14 |
| mutant/mutants | No hits |
| M01-M08 / M1-M8 | No hits |

### A2. E4 term-page index

| Term | Part/page locations |
|---|---|
| duplicate* | P5: 11, 13, 25, 29, 35, 38, 48, 49, 61, 66, 80; P6: 4, 5, 19, 25, 39, 52, 56, 74, 79, 94, 111, 132, 137, 152, 171, 172, 194, 199, 214, 238, 239, 262, 268, 282 |
| twice | P5: 38, 47; P6: 4, 55, 110, 171, 238 |
| again | P5: 29, 38 |
| repeat* | P4: 11; P5: 25, 70, 80; P6: 8, 29, 39, 50, 61, 84, 94, 116, 142, 152, 177, 204, 214, 230, 244, 272, 282, 298; P7: 30; P8: 4, 9, 15, 16, 18, 20 |
| replicate* | P5: 1, 18, 25, 26, 29, 31, 38, 40, 47, 48, 52, 66, 70, 80, 82; P6: 4, 5, 9, 24, 28, 39, 40, 55, 56, 62, 79, 83, 93, 95, 110, 111, 118, 137, 141, 151, 152, 153, 171, 178, 199, 203, 213, 215, 238, 239, 245, 267, 272, 282, 283 |
| additional time | P5: 35, 38, 47, 60; P6: 4, 19, 55, 74, 110, 131, 171, 193, 238, 262 |
| one more time | No hits |
| second instance | No hits |

### A3. Assignment-identifier page index

- Parent IDs `G01`-`G30`: P5: 17, 18, 66, 81; P6: 24, 40, 79, 95, 137, 153, 199, 215, 267, 283. These occurrences reproduce the parent-family roster, not parent-to-pair assignments.
- Solver IDs `S001`-`S150`: no hits.
- Pair label `pair_id`: P8: 20 only, in the C9 bank-record serialization checklist, not the mutation schedule.
- Mechanism IDs `M1`-`M8`: no hits.

### A4. Complete page index for `mechanism` / `mechanisms`

Because `mechanism` is by far the most frequent E1 term, the complete hit-page index is provided separately. These are all pages containing the lexical term, whether or not the occurrence is about the intended mutation taxonomy. The substantive screen and dispositions remain in §3.3.

- P4: 2, 4, 11, 14.
- P5: 1, 2, 5, 6, 10, 12, 18, 25, 26, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 47, 48, 49, 50, 52, 53, 55, 56, 60, 61, 62, 64, 66, 67, 68, 69, 70, 71, 74, 80, 81, 82, 86.
- P6: 1, 3, 4, 5, 6, 7, 9, 10, 12, 13, 14, 15, 16, 18, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 32, 39, 40, 41, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 69, 70, 73, 75, 77, 79, 80, 81, 83, 84, 85, 87, 93, 94, 95, 96, 100, 101, 102, 103, 104, 105, 107, 108, 109, 110, 111, 112, 113, 114, 115, 117, 119, 120, 121, 122, 123, 124, 126, 127, 128, 131, 132, 133, 135, 137, 138, 139, 141, 142, 143, 145, 152, 153, 154, 158, 159, 160, 161, 162, 163, 166, 170, 171, 172, 173, 174, 175, 176, 178, 179, 180, 181, 182, 183, 184, 185, 188, 189, 190, 193, 194, 195, 197, 199, 200, 201, 203, 204, 205, 207, 213, 214, 215, 216, 220, 221, 222, 223, 224, 225, 228, 232, 233, 237, 238, 239, 240, 241, 242, 243, 245, 247, 248, 249, 250, 251, 252, 256, 257, 258, 259, 261, 263, 266, 267, 268, 269, 270, 271, 272, 273, 275, 282, 283, 284, 288, 290, 291, 292, 293, 296, 297, 301, 303.
- P7: 1, 2.
- P8: 11, 15.