# LC518/150 — A2-static annex availability and provenance investigation record

**Date:** 2026-11-06
**Status:** AUDIT RECORD — annex availability and provenance investigation, executed
under the ratified conditional-continuation rule. This record authorizes nothing: no
construction, no execution, no analysis of candidate outcomes, no held-out evaluation,
no commit, no publication.
**File status:** untracked working-tree file, repository root, branch
`research/concentration-math-spec`. Not committed on any ref.
**Record-keeper and availability investigator:** Qoder CLI (GLM role). **No independent
A2 auditor has been appointed and no allocation-level A2 audit has been performed.**
This record is an annex availability and provenance investigation whose result is that
the required annex was not located in the searched sources; the protocol's independence
rules (protocol §2) govern any future allocation-level audit (§11.1).
**Target decision of record:** Claim B1 per
`lc518-150/review-v1.2/AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` at branch head
`2784297` (ref `gpt/lc518-claim-b1-primary-2026-11-05`), fetched to
`origin/gpt/lc518-claim-b1-primary-2026-11-05` in this audit.

## 1. Verdict (operative text, Rev 4 — the Rev 1–3 §1 text is preserved verbatim in §11.4)

- **The private mutation annex was not located in any source searched** (§3; §9.4): all
  repository refs, history paths, and archive members; the generated bank artifact;
  owner-local storage; and the re-checks recorded in §9 (Downloads root and
  `Compressed/`, drive-C Recycle Bin). Claims of global absence are not made; the
  uninspected channels are listed in §9.4.
- **The allocation therefore cannot be assessed**: the decisive incidence-by-family and
  exact-cell tables are annex content (§4).
- **Verdict of record: `BLOCKED / NOT ASSESSABLE` — required allocation artifact
  unavailable.**
- **This is not evidence that the allocation is defective, and not a negative scientific
  result about B1.** The allocation itself has never been examined, because none exists
  to examine.
- **The mutation design remains blocked from construction** (0/150 solver bodies; the
  stop rule of 2026-11-01 remains in force) pending the owner decision in §6. This
  verdict does not authorize any switch to Claim A.

## 2. Chronology verification (counting correction accepted)

Branch `gpt/lc518-claim-b1-primary-2026-11-05` fetched from origin in this audit; the
verified lineage from base `511bc20` is:

`a19653a → 7e47c21 → f2303ad → 6ca0ed4 → cecdf75 → 46189b4 → dda66e7 → 2784297`

That sequence contains **eight commits, with seven ancestors before `2784297`**. The
counting correction is accepted; the sequence itself matches the decision record's §9
lineage, and `2784297` is the current remote branch head. Chronology is consistent; no
repository change is made by this audit.

## 3. Annex search protocol and result

**Searched (2026-11-06):**

1. **All repository refs, history paths, and archive members** — standing result of the
   repo-wide inventory audit (REPOSITORY_STORAGE_INVENTORY_2026-11-05.md §2: annex
   "nowhere in any ref, any history path, or any archive member"; sealed/missing register
   §3: "no such assignments exist anywhere (repo-wide path + content search, 2026-11-05)").
   Re-confirmed today by content search of the working tree and the fetched B1 branch:
   every hit for "pair-allocation" / "eight-mechanism" / "annex" is a reference *about*
   the annex (work order, review record, inventory, audit matrix), not the annex.
2. **The generated bank artifact** (`lc518-bank-run-41591572358-1.zip`, 15 members per
   VERIFICATION_LOG addendum 2): contains only the two input banks, oracle outputs,
   sidecars, generator, launcher, protocol, logs and tests. No solver body, no assignment
   manifest. The generator inspected (`lc518_generator.py`, SHA-256
   `848984cac427547955a04b2e5c379762149ad94a37711a6483008fd55f2c161b`, recomputed from the
   artifact member; equals `logs/run_manifest.json` `generator_sha256` and the
   VERIFICATION_LOG addendum 2 value) is the **input-bank** generator (D1–D8/H1–H8 record
   construction per C9 rev 2.6); it contains no mutation taxonomy, no pair schedule, and
   no per-solver assignment table.
3. **Owner-custody local storage** (the annex is private and was never supplied to GLM,
   but a local owner copy was the remaining possibility): Downloads (including
   `Compressed/`, `Documents/`), Desktop, Documents, OneDrive, PycharmProjects (including
   `doctor-workspace-recovered/`, `doctor-workspace-reoccupied/`, `experiments/`,
   `results/`, `lc518_containment_2026-11-03/`), and the repository working tree
   (tracked and untracked). Filename patterns: `*annex*`, `*mutation*`, `*sealed*`,
   `*ground_truth*`. All ground-truth hits belong to an unrelated project (doctor
   workspace, non-LC518). **No annex, no sealed ground-truth manifest, no
   assignment manifest found.**

**Corroborating record of absence:** `lc518-150/glm-handoff/worklog.md` entry 29
(2026-11-01 ~10:15 UTC, at commit `511bc20`): "STOP RULE INVOKED (work order :45 + :47):
the private mutation-design annex and pair-allocation schedule have NOT reached me…
no solver body, no bank JSON, no oracle file exists yet." PARENT_DESIGN.md v1.0 freeze
attestation states the same. CORRECTIONS_RECORD / VERIFICATION_MAP and the inventory §2
row record 150 solver bodies as 0/150 constructed, "MISSING (by design, pending annex)."

## 4. What the audit can establish annex-free (structural arithmetic only; corrected by §11 Rev 4)

With the annex absent, the audit can verify only the version-structure arithmetic that
is independent of the schedule. Roster (PARENT_DESIGN.md v1.0 §7, frozen): K1 × 7
(G01–G07), K2 × 8 (G08–G15), K3 × 8 (G16–G23), K4 × 5 (G24–G28), K5 × 2 (G29–G30);
30 parent groups, 150 intended bodies (S0/SA/SB/SAB/S-extra each).

Single-mutation arithmetic (B1 primary population = SA + SB + S-extra):

- SA/SB slots: 30 parents × 2 = 60 slots, determined by the 28+2 pair allocation. Each
  mechanism appears in exactly 7 base pairs (complete graph K8). The two preselected
  replicated pairs contribute `r_m` additional SA/SB incidences to mechanism `m`, where
  `r_m ∈ {0, 1, 2}` — mechanism `m` receives +0, +1, or +2 depending on whether it
  appears in neither, one, or both replicated pairs — and `Σ_m r_m = 4`. SA/SB slots
  per mechanism: **7–9**.
- S-extra slots: 30 across 8 mechanisms; under even integer balancing, six mechanisms
  get 4 and two get 3 (exact split is annex content).
- Nominal single-mutation assignment **slots** per mechanism: **10–13**. This is a slot
  total, **not** a distinct-parent-group count: an S-extra assignment may duplicate a
  mechanism already assigned to that parent, and identical base-source hashes
  deduplicate under the protocol's C4 identity rules. Distinct-parent-group counts per
  mechanism are therefore only ≤ the slot total.

What this arithmetic cannot decide, and why the audit halts there:

- The B1 support cell is `(mechanism, parent family Z, k_fail, k_unresolved)`. Whether
  any mechanism has ≥3 of its single-mutation parent groups **within one family**
  depends entirely on which pair was allocated to which parent and how S-extra was
  assigned — annex content. The 10–13 slots per mechanism could in principle concentrate
  inside one family or scatter across all five; both are compatible with the arithmetic.
- Whether the allocation creates structural opportunity within an exact cell is
  assessed at A2 only as potential, under the protocol's C6 rule: for `(m, z, c)`, at
  least **three** effective parent groups able to reach cell `c` (`|P_{m,z,c}| ≥ 3`,
  built from the annex-declared possibility sets) **and** a cross-parent difference
  among annex-declared possible `C_D` values (`∃ a ∈ V_{p,c}, b ∈ V_{q,c} : a ≠ b`) —
  a family-specific, exact-cell, cross-parent assessment (protocol §4 C6, Rev 6).
  Realized variation is A3-dynamic, under the mirrored observed-set rule `O_{p,c}`
  (protocol §5, Rev 6). (Superseded wordings — Rev 1's "≥2 distinct failure vectors",
  which ignored that distinct vectors can share one C_D value, and the intermediate
  per-mechanism formulation of Revs 4–5, which lacked the third-parent condition —
  are preserved in §13.3.)
  *(Rev 8 note: this passage — including its `V_{p,c}`-style indexing and its
  "protocol Rev 6" citation — is **superseded** by protocol Rev 8's mechanism-specific
  witness standard and `V_{p,m,z,c}` indexing; see §15.1. The text is retained intact
  as the record of the Rev 6 formulation; the earlier review chronology is not
  rewritten, and no implication is made that the earlier version always contained the
  revised rule.)*
- The only within-family verdict that is fully annex-free: **K5 can never qualify.**
  With 2 parent groups, no `(mechanism, K5)` cell can reach the three-parent minimum for
  any mechanism under any schedule. The K5 exclusion in the B1 decision record §3 is
  structurally sound and requires no annex.

**Annex-free A2-static conclusion: the allocation's nominal slot arithmetic does not
imply within-family support; the decisive incidence-by-family table is uncomputable
without the annex. No cell can be declared supported or unsupported except the K5
family, which is unsupported by construction.**

## 5. Conditional-continuation outcome (operative text, Rev 4 — the Rev 1–3 §5 text is preserved verbatim in §11.4)

The ratified conditional-continuation rule keeps the mutation design alive only through
the annex audit. Its first gate — "supply the annex" — has not been met: the annex was
not located in any searched source (§3; §9.4). The mutation design therefore remains
**blocked at the annex gate**, where it has been since 2026-11-01. No construction has
occurred (0/150), so there is no realized allocation to audit and nothing to redesign
yet.

Per the B1 decision record §6 and the 2026-11-05 review record's failure rule: this is
a **non-identification / not-assessable condition**, not a null effect, and does not
authorize relabeling the study as Claim A. Claim A remains unadopted; B2 remains
deferred.

## 6. Required owner decision (unchanged, now sole gate)

1. **Supply the private mutation annex** (eight-mechanism taxonomy; the 28+2 pair-to-
   parent allocation; S-extra balancing). A2-static then executes on the supplied text:
   taxonomy verification, assignment/parent compatibility, mechanism × family incidence
   table (all 40 cells, including unsupported and zero-variance candidates), S-extra
   balancing check, and the K5 scope exclusion — still without any claim about realized
   diagnostics, which remain A3-dynamic.
2. **Or formally drop the mutation design.** Claim B1 then has no testable population
   under the current design, and the study's next stage must be re-scoped by a separately
   authorized decision.

**Path separation (added Rev 4):** authorizing a new allocation design (§8.6 path 2) is
a separate new-design process — new frozen assignments, new independent review, its own
authorization — not a continuation or recovery of the current allocation. The present
audit cannot assess a design that does not yet exist.

Silence on this question continues to block the record; no agent may invent, reconstruct,
or substitute the annex (work order :45).

## 7. Non-claims

- This record does not ratify, un-ratify, or narrow Claim B1; the target decision of
  record stands at `2784297`.
- It does not establish or refute any identification claim; no candidate outcome was
  examined (none exists).
- It does not modify any tracked file, any ref, or the decision branch; the fetched ref
  `origin/gpt/lc518-claim-b1-primary-2026-11-05` is a fetch, not a repository change.
- It does not alter the frozen v1.0 specifications, rev 2.6's review-only status, the
  blind E3 pass, or the C9 generation provenance record.
- The `.qoder_a2static/` extraction directory holds hash-verified copies of the artifact's
  generator and run manifest used in §3; it is untracked audit evidence, not study data.

## 8. Revision 1 — GPT adversarial review (2026-11-06, appended; original §§ 1–7 preserved)

GPT's review of this record accepts the evidence and the conditional continuation but
corrects two items and adds governance requirements. The corrections are accepted by the
auditor and recorded here; they change the classification and the evidential status of
§4, not the underlying facts of §§ 2–3.

### 8.1 Verdict reclassified: BLOCKED / NOT ASSESSABLE

§1's framing "cannot pass" is withdrawn as misleading. **A2 has not failed
scientifically; A2 cannot yet be evaluated.** The audit requires the annex; without it,
whether the actual allocation satisfies the within-mechanism × family support requirement
is undetermined, not negative. The verdict of record is:

**BLOCKED / NOT ASSESSABLE — required allocation artifact unavailable.**

Calling this a design failure would be premature: the allocation itself has never been
examined, because none exists to examine.

### 8.2 §4 incidence figures downgraded to structural arithmetic

The 10–13 parent-group-per-mechanism figures are not verified allocation evidence and
must not be cited as such. Decomposition:

- 7 SA/SB parent groups per mechanism: **structural** (complete-graph K8 work-order
  requirement), annex-free.
- +0–2 SA/SB groups (8–9 total): depends on which two pairs are preselected for
  replication — annex content.
- SA/SB parent-group **family** distribution: fully annex content (pair-to-parent
  allocation); uncomputable now.
- S-extra 3–4 per mechanism: depends on the missing balancing rule — annex content.
- Neither total incidence nor nominal balancing establishes the decisive condition:
  three distinct parent groups within the same eligible family and exact observed
  failure-count cell.

K5 stands unaffected and is different in kind: **structurally established** (two parent
groups cannot satisfy a three-parent minimum under any schedule).

*(Rev 4 note: the "+0–2 SA/SB groups (8–9 total)" line above is superseded by §11.3 —
mechanisms can also receive zero repeated-pair incidence, leaving 7; and the 10–13
figures are slot totals, not distinct-parent-group counts. §8 is preserved as history.)*

### 8.3 Programme context: three obstacles, not three negative findings

| Study | Identification problem | Scientific interpretation |
|---|---|---|
| v0.2 | Every eligible observation had C = 5/k | Concentration could not be separated from failure count |
| Gate 1 | Concentration variation confounded with carrier count and construction | The proposed operationalization did not establish independent mechanism variation |
| LC518 | The private mutation allocation is unavailable | The intended B1 identification conditions cannot currently be assessed |

These are obstacles to testing the concentration hypothesis, not evidence against it. The
programme still has no properly identified empirical answer to the central question.

### 8.4 Audit-protocol requirement (carried forward)

The earlier requirement remains binding: **A2 criteria must be frozen before any
recovered or supplied annex is inspected, and the auditor must be independent of the
annex's authorship.** This investigation is classified as an **annex availability and
provenance investigation**, not a completed allocation-identification audit. Draft
criteria for the frozen protocol are in
`LC518_A2_AUDIT_PROTOCOL_DRAFT_2026-11-06.md` (owner ratification required before
freezing).

*(Rev 10 note: the "owner ratification required before freezing" wording above reflects
the earlier governance position. It is **superseded** by the owner's recorded
delegation and the current protocol §11, under which joint GPT–Claude agreement
settles the protocol text without further owner ratification. Any protocol freeze
remains a separate event under §11. §8.4 is retained intact as history; see §17.1.)*

### 8.5 Scope predeclaration question (owner, before any annex inspection)

Whether the intended B1 claim must cover all eight mechanisms or may cover a
predeclared supported subset must be settled **before** any annex is examined. The joint
B1 decision permits a narrower claim where support is limited, but the target population
must not be selected opportunistically after results are examined.

*(Rev 5 note: this §8.5 question is **superseded** by the agreed Option W decision —
see §12.2. The scope rule is frozen in the protocol before any annex access and the
supported set `S_W` is computed mechanically after access; no owner or auditor
discretion operates between rule-freeze and computation. The requirement that scope be
settled before inspection is retained and is now implemented by the frozen rule rather
than by a pending choice.)*

### 8.6 Disposition: B1 target preserved; LC518 implementation on hold; three paths

1. **Recover** the original annex, if it exists outside the searched locations, then
   conduct the frozen independent A2 audit against the ratified protocol.
2. **Authorize a new allocation design**, if the original annex was never created —
   treated as a new design with its own frozen assignments and independent review.
3. **Discontinue the LC518 mutation arm**, if neither recovery nor a defensible new
   allocation is justified.

Governing principle of record: **no candidate bodies until the allocation has
demonstrated that it can create the comparisons required by B1.**

Search-boundary note (honest scope of §3): the search covered the repository (all refs,
history, archives — standing inventory result), the bank artifact, and owner-local
storage by filename and content markers. Two channels cannot be inspected by this
process: the owner's chat/e-mail delivery channel (where an annex would have been
supplied to GLM — and GLM's worklog states it never arrived), and two
`lc518_150_review_work*.zip` files that were present in Downloads at the 2026-11-05
audit snapshot and are no longer present; their deletion is noted, not investigated.
Path 1 therefore also depends on owner knowledge: whether an annex was ever authored at
all is not determinable from artifacts alone.

### 8.7 Standing distinction

The joint B1 decision (`AGENT_DECISION_CLAIM_B1_SCOPE_2026-11-05.md` at `2784297`) is
valid as a **target decision** only. It does not certify the feasibility of the current
mutation design. The two facts are kept separate in all later records.

## 9. Revision 2 — search-boundary correction and fragment reclassification (2026-11-06; original §§ 1–8 preserved)

Prepared by Qoder CLI (GLM role: record-keeper) on GPT's 2026-11-06 review. No prior
section is modified. Local checks recorded here were performed by this record-keeper
identity on 2026-11-06; facts reported by GPT from its remote environment are marked as
GPT-reported and were not independently verifiable from this workspace. The scientific
verdict (§8.1) and the owner decision (§6) are unchanged by everything below.

### 9.1 Correction: review-work ZIP chronology

§8.6 stated that **two** `lc518_150_review_work*.zip` files were "present in Downloads at
the 2026-11-05 audit snapshot" and "no longer present". Corrected:

- Snapshot evidence of record: `.qoder_tmp_downloads.txt` (repository working tree,
  untracked; filesystem timestamp 2026-11-03 18:01 local) lists **three** matching files:
  `lc518_150_review_work.zip`, `lc518_150_review_work (1).zip`,
  `lc518_150_review_work (2).zip`. No snapshot dated 2026-11-05 exists anywhere in the
  record; the "two" figure is unsupported and is withdrawn. The only recorded snapshot
  predates the claimed one.
- The files' contents were never inspected, hashed, or inventoried by this record.
  Nothing about their identity beyond filenames is established.
- Re-check (2026-11-06, this session): no matching files in Downloads root or
  `Downloads/Compressed/`; a drive-C Recycle-Bin scan found no lc518 entries. The
  disappearance mechanism remains unknown; this record infers neither permanent deletion
  nor a destination.
- Also recorded: no `lc518-part*` filenames present in Downloads root at re-check.

### 9.2 `/ProjectTransfer` Library fragments: reclassified as C9 kit parts; not annex evidence

GPT reported (2026-11-06): a persistent ChatGPT file-library folder `/ProjectTransfer`
containing `lc518-part-02.b64` (10,000 bytes), `lc518-part-03.b64` (10,000 bytes),
`lc518-part-04.b64` (7,824 bytes), uploaded 2026-11-03 ~06:39–06:40 UTC; GPT's base64
decode yields opaque binary; no `part-01` or manifest in that folder. Recorded as
GPT-reported, not independently verifiable here.

Identification (verified locally, 2026-11-06, from repository blobs only): the C9
bank-generation kit was assembled from **five** base64 parts committed at `a4ec114` under
`lc518-150/c9-github-generation-package-parts/` as `part-00.b64` … `part-04.b64`
(**0-based** numbering; later removed by the security-containment commits `b0086f1`,
`2627ff8`, `7921e35`, remaining reachable in history; recorded in
`CLAIM_AUDIT_MATRIX_2026-11-05.csv` rows L21/L35 and
`PROJECT_DEVELOPMENT_TREE_2026-11-03.md` §5.4). This session re-verified end to end: the
five committed parts concatenate → base64-decode → a `.tar.xz` whose SHA-256 is
`e0be3f2a91e8d71fc0ecfd6cc8eb4621ddb7e9b3a094ad08152423677c1e0ac5` — exact match to the
recorded package hash — containing **17 members** including
`lc518-150/c9-github-generation/OWNER_GO_RECORD.md`. Verification artifacts were held in
a temporary directory outside the repository and were neither persisted nor committed.

Consistency findings:

- **Size match:** GPT's reported fragment sizes (10,000 / 10,000 / 7,824 bytes) are
  byte-exact matches to the committed **base64 text** sizes of `part-02.b64` /
  `part-03.b64` / `part-04.b64` (their decoded XZ-stream fragment sizes are 7,500 /
  7,500 / 5,868 — consistent with GPT's "opaque binary" decode result).
- **Naming:** Library names `lc518-part-NN.b64` equal the committed `part-NN.b64` names
  under an added `lc518-` prefix.
- **Numbering:** the committed set being 0-based, GPT's "no part-01" observation
  corresponds to committed parts **00 and 01** missing from the Library folder; no
  `part-05` exists in the committed set.
- **Timeline:** the upload window (2026-11-03 ~06:39–06:40 UTC) immediately precedes
  Actions run 41591572358 (started 06:42:21Z, per the development-tree record).

**Classification: likely byte-copies of committed C9 kit parts 02–04; NOT
mutation-annex evidence.** Byte-identity (hash equality between Library fragments and
committed blobs) remains **unverified** and requires hash recomputation on the Library
side or file transfer. Reference digests for that check, computed this session from the
committed blob contents (SHA-256 of the base64 text exactly as committed):

- `part-02.b64` → `1df05f0b5ec27ea050cf8aac98ec65486b3910e2353f95b9c91239d13aceadcc`
- `part-03.b64` → `37831fe3b1816b77d912d9cdd78864e944407c85e1c1bddf4ede2061d6f7e265`
- `part-04.b64` → `94964f05b688ce7646fde84907dd90e6ae2dbb57c1daa9cf82e63a143f0f3323`

GPT's earlier framing of the fragments as a potential annex recovery route is withdrawn
as too broad. They remain an unresolved archival item pending hash confirmation; the
annex-recovery path (§8.6 path 1) gains nothing from them.

### 9.3 Citation correction

GPT's review cited `lc518_artifact_audit_41591572358.md` for the five-part package. No
file of that name exists in the searched tree (repository working tree, Downloads,
Desktop, Documents). The recorded sources are: `CLAIM_AUDIT_MATRIX_2026-11-05.csv` rows
L21 and L35; `PROJECT_DEVELOPMENT_TREE_2026-11-03.md` §5.4 and node H8; Downloads
check-ledger files `lc518_artifact_audit_check_ledger_41591572358.txt/.csv` (2026-11-03).
The substance of the citation — five-part kit, archive hash, OWNER_GO_RECORD membership —
is nonetheless VERIFIED by this session's independent re-assembly, so the citation error
does not affect the classification above.

### 9.4 Search-boundary statement (Rev 2 — supersedes §8.6's note)

Inspected and covered by statements of absence: (a) repository — all refs, history
paths, archive members (standing inventory result), working tree, fetched B1 branch, and
a 2026-11-06 working-tree search for `ProjectTransfer` / `lc518-part` traces (none
found); (b) the bank artifact `lc518-bank-run-41591572358-1.zip` (15 members, §3);
(c) owner-local storage per §3, plus the 2026-11-06 re-check (Downloads root and
`Compressed/` re-listed, drive-C Recycle Bin scanned); (d) the committed C9 kit parts —
present in history, re-verified 2026-11-06, and identified as the bank-generation
package, not the annex.

Not inspected, and not covered by any statement of absence: the owner's chat/e-mail
delivery channel (owner-side knowledge; GPT additionally reports its e-mail connector
was not eligible in its workspace); the ChatGPT file Library beyond the
`/ProjectTransfer` folder GPT reported; the contents and identity of the three
disappeared review-work ZIPs (never inspected or hashed). **Global absence is not
claimed.**

### 9.5 Disposition unchanged

The verdict of record remains **BLOCKED / NOT ASSESSABLE — required allocation artifact
unavailable** (§8.1). §8.6's three paths and the governing principle of record stand
unchanged. The required owner decision (§6) is unchanged. The reclassification removes
from the annex-recovery path the only lead identified to date; it does not create, and
is not, evidence about the allocation.

## 10. Revision 3 — archive identity confirmed (2026-11-06; §§ 1–9 preserved)

Prepared by Qoder CLI (GLM role: record-keeper) on GPT's and Claude's 2026-11-06
review. No prior section is modified.

### 10.1 Byte-identity confirmed

GPT independently computed SHA-256 for the three `/ProjectTransfer` Library files; all
three match the reference digests recorded in §9.2, with matching byte counts
(10,000 / 10,000 / 7,824):

| Library file        | SHA-256                                                            |
| ------------------- | ------------------------------------------------------------------ |
| `lc518-part-02.b64` | `1df05f0b5ec27ea050cf8aac98ec65486b3910e2353f95b9c91239d13aceadcc` |
| `lc518-part-03.b64` | `37831fe3b1816b77d912d9cdd78864e944407c85e1c1bddf4ede2061d6f7e265` |
| `lc518-part-04.b64` | `94964f05b688ce7646fde84907dd90e6ae2dbb57c1daa9cf82e63a143f0f3323` |

GLM's full five-part reconstruction reproduces the recorded package digest
`e0be3f2a91e8d71fc0ecfd6cc8eb4621ddb7e9b3a094ad08152423677c1e0ac5`. The classification
of §9.2 is upgraded from "likely byte-copies" to **confirmed**: the Library files
`lc518-part-02/03/04.b64` are byte-identical to the committed kit parts
`part-02/03/04.b64`.

Attribution chain of record: GLM's local reassembly and reference digests (from the
committed blobs at `a4ec114`, package digest reproduced, 17 members including
`OWNER_GO_RECORD.md`); GPT's independent Library-side hash recomputation; Claude
records the conclusion by citation and does not claim independent recomputation.

### 10.2 Conclusions

- The five-part archive is the LC518 bank-generation package, including
  `OWNER_GO_RECORD.md`.
- The Library contains parts 02, 03, and 04. Parts **00 and 01** are absent from the
  Library — an unresolved **archival** provenance gap. The package itself is complete
  in the repository and hash-verified, so the gap is archival only; it does not affect
  any recorded result.
- There is no `part-05` in the five-part package (0-based naming, `part-00`–`part-04`).
- The fragments are **not** the private mutation annex. GPT's earlier citation to
  `lc518_artifact_audit_41591572358.md` is withdrawn (§9.3 records the corrected
  sources).

### 10.3 Disposition unchanged

The verdict of record remains **BLOCKED / NOT ASSESSABLE — required allocation artifact
unavailable** (§8.1). §8.6's three paths and the governing principle stand unchanged.
Nothing here authorizes annex inspection, auditor appointment, construction, or
execution. The annex availability question is unaffected by the closed archive item.

## 11. Revision 4 — full-text review corrections (2026-11-06; §§ 1–10 preserved, except operative §§ 1, 4, 5 rewritten with originals preserved here)

Prepared by Qoder CLI (GLM role: record-keeper) on GPT's full-text review of Rev 3
(2026-11-06). Rev 3 was **not approved**; Rev 4 implements the review findings. Prior
revision history (§§ 8–10) is preserved unmodified, with one supersession marker added
to §8.2. Claude has not reviewed any complete text of either document yet.

### 11.1 Role separation (accepted finding A)

The Rev 3 header described this record-keeper identity as "record-keeper/auditor".
Under the protocol's independence rules (protocol §2: the auditor must not be the agent
that performed the availability investigation), the same identity cannot hold both
roles. The header is corrected: this identity is the **record-keeper and availability
investigator**; **no independent A2 auditor has been appointed and no allocation-level
A2 audit has been performed.** What exists is an annex availability and provenance
investigation whose result is that the required annex was not located in the searched
sources. This is not a criticism of the search itself (§3, §9); it is a necessary
separation of roles.

### 11.2 Operative verdict and continuation text rewritten (accepted finding B)

§1 and §5 now carry the operative conclusions directly:

- The annex was not located in the sources searched (§3; §9.4).
- The allocation therefore cannot be assessed.
- The verdict is `BLOCKED / NOT ASSESSABLE`.
- This is not evidence that the allocation is defective or that B1 has failed
  scientifically.
- The existing allocation remains blocked from construction pending the relevant
  decision (§6).

The Rev 1 framing ("cannot pass"; "the mutation design cannot be kept alive on current
evidence") is superseded and preserved verbatim in §11.4. §8.1 remains the
reclassification record. A reader no longer needs to reconstruct the revision history
to reach the operative verdict.

### 11.3 Arithmetic corrections (accepted finding C)

§4 is rewritten with corrected structural arithmetic:

- Replicated-pair incidence: `r_m ∈ {0, 1, 2}` with `Σ_m r_m = 4`; SA/SB slots per
  mechanism 7–9. The Rev 1 statement that the two replications "add +1 SA/SB incidence
  to each of their 4 mechanisms" assumed the two replicated pairs share no mechanism;
  that assumption cannot be made annex-free.
- §8.2's "+0–2 SA/SB groups (8–9 total)" figure is **superseded**: it omits mechanisms
  receiving no repeated-pair incidence (`r_m = 0`, leaving 7).
- "10–13 distinct parent groups per mechanism" is downgraded to a nominal **slot**
  total: an S-extra assignment can duplicate a mechanism already assigned to that
  parent, and identical base-source hashes deduplicate under the protocol's C4 identity
  rules. Distinct-parent-group counts are ≤ slot totals and are annex content.
- K5's structural exclusion is unaffected.

### 11.4 Preserved superseded operative texts (verbatim, as of Rev 3)

```
## 1. Verdict (one paragraph)

**(§1 original issue; verdict reclassified by §8 Rev 1 — read §8 as controlling.)**

**A2-static cannot pass: the private mutation annex does not exist in any location
accessible to this audit.** The stop rule invoked by GLM on 2026-11-01 (worklog entry 29;
work order :45/:47) remains in force; 0/150 solver bodies exist. The conditional
continuation therefore fails at its first gate ("supply the annex"), and per the ratified
rule the mutation design cannot be kept alive on current evidence. The required owner
decision (review record 2026-11-05 §5 item 3) is unchanged and now decisive: **supply the
private annex, or formally drop the mutation design.** This is not a null result and does
not authorize any switch to Claim A.

## 4. What the audit can establish annex-free (static allocation arithmetic only)

With the annex absent, the audit can verify only the version-structure arithmetic that is
independent of the schedule, extending review-record §4 to the B1 within-family rule.

Roster (PARENT_DESIGN.md v1.0 §7, frozen): K1 × 7 (G01–G07), K2 × 8 (G08–G15),
K3 × 8 (G16–G23), K4 × 5 (G24–G28), K5 × 2 (G29–G30); 30 parent groups, 150 intended
bodies (S0/SA/SB/SAB/S-extra each).

Single-mutation incidence (B1 primary population = SA + SB + S-extra):

- SA/SB slots: 30 parents × 2 = 60 slots, determined by the 28+2 pair allocation. Each
  mechanism appears in exactly 7 base pairs (complete graph K8); the two preselected
  replicated pairs add +1 SA/SB incidence to each of their 4 mechanisms. SA/SB incidence
  per mechanism: 7–9 parent groups.
- S-extra slots: 30 across 8 mechanisms; under even integer balancing, six mechanisms get
  4 and two get 3 (exact split is annex content).
- Total single-mutation versions per mechanism: 10–13, across 10–13 distinct parent
  groups — nominal incidence alone, not within-family incidence.

What this arithmetic cannot decide, and why the audit halts there:

- The B1 support cell is `(mechanism, parent family Z, k_fail, k_unresolved)`. Whether any
  mechanism has ≥3 of its single-mutation parent groups **within one family** depends
  entirely on which pair was allocated to which parent and how S-extra was assigned —
  annex content. The 10–13 parent groups per mechanism could in principle concentrate
  inside one family or scatter across all five; both are compatible with the arithmetic.
- Whether the same mechanism can produce ≥2 distinct failure vectors `(k_fail,
  k_unresolved)` — the prerequisite for within-cell `C_D` variation — is a property of the
  mechanism definitions (taxonomy) and ultimately of realized diagnostics; neither is
  available statically (A1a's conclusion stands: capacity, not feasibility).
- The only within-family verdict that is fully annex-free: **K5 can never qualify.** With
  2 parent groups, no `(mechanism, K5)` cell can reach the three-parent minimum for any
  mechanism under any schedule. The K5 exclusion in the B1 decision record §3 is
  structurally sound and requires no annex.

**Annex-free A2-static conclusion: the allocation's nominal incidence (10–13 parent
groups per mechanism) does not imply within-family support; the decisive incidence-by-
family table is uncomputable without the annex. No cell can be declared supported or
unsupported except the K5 family, which is unsupported by construction.**

## 5. Conditional-continuation outcome

The ratified rule was: keep the mutation design alive only through the annex audit; if the
allocation cannot plausibly support B1, stop or redesign before construction proceeds
further. The audit's required input does not exist, so the audit cannot pass; the mutation
design remains **blocked at the annex gate**, where it has been since 2026-11-01. No
construction has occurred (0/150), so there is no realized allocation to audit and nothing
to redesign yet.

Per the B1 decision record §6 and the 2026-11-05 review record's failure rule: absence of
support is a **non-identification / insufficient-support condition**, not a null effect,
and does not authorize relabeling the study as Claim A. Claim A remains unadopted; B2
remains deferred.
```

### 11.5 Owner-decision path separation (accepted finding D)

§6 now states explicitly that authorizing a new allocation design (§8.6 path 2) is a
separate new-design process — new frozen assignments, new independent review, its own
authorization — not a continuation or recovery of the current allocation. The present
audit cannot assess a design that does not yet exist.

### 11.6 Review-anchor digest status

GPT reported (2026-11-06) that the SHA-256 digests GLM cited as review anchors for the
Rev 3 pasted texts do not reproduce from the pasted content. Local re-verification
(this session): the working-tree files are LF-only and **do** end with a single trailing
LF (verified byte-level this session). Full-file digests reproduce as
`f1c73922d67431f8f8ee5a35e77ee2220928937f18691d96d0051e3ae2c16ce2` (protocol) and
`274ff836131500ccd99698f3436ce6212079e37752513e31bdbbe1f2895e1f64` (record). GPT's
extraction is consistently **+1 byte** relative to the file contents (protocol 18,283
extracted vs 18,282 content bytes; record 24,837 extracted vs 24,836), with
non-matching digests both with and without a final LF. The discrepancy is therefore
**not** a final-newline artifact: the pasted/extracted text differs from the
working-tree bytes by at least one byte, origin undetermined (paste-path transport or
extraction artifact).

Process correction of record: GLM asserted the trailing-LF property in the Rev 3
exchange **without prior byte-level verification** (only CR-count and fence-count were
checked). The property happens to hold; the practice failure is acknowledged.

Consequence: **pasted texts are content-review artifacts, not verified byte anchors.**
Byte-exact identity between reviewed text and working-tree file will be established
through an exact-byte channel agreed before the freeze event — proposal of record: GLM
pastes a base64 encoding of each final file; reviewers decode, recompute SHA-256, and
compare. Transport corruption of a base64 transfer is detectable, never silent.
Owner-mediated file transfer is the alternative.

### 11.7 Disposition (mirrors the joint review status of 2026-11-06)

| Item | Disposition |
|---|---|
| B1 target and agreed support rules | Agreed in substance |
| Protocol Rev 3 | Not approved; Rev 4 issued with C6, C_D-definition, and counting corrections |
| Audit record Rev 3 | Not approved; Rev 4 issued with role, verdict, and arithmetic corrections |
| Bank-generation archive identity | Closed (hash evidence; §10) |
| Mutation annex | Still unavailable; verdict `BLOCKED / NOT ASSESSABLE` |
| Independent A2 auditor | Not appointed |
| Freeze / annex inspection / construction / execution | Not authorized |

The corrections in this revision address the rules of evidence and their
implementation; the B1 scientific target is not reopened.

## 12. Revision 5 — C6 formalization and reclassification corrections (2026-11-06; §§ 1–11 preserved, except the title and a §8.5 marker)

Prepared by Qoder CLI (GLM role: record-keeper) on the correction list on which GPT and
Claude are aligned (2026-11-06). Rev 4 remains unapproved; Rev 5 is issued for joint
full-text review of both documents. The B1 target and Option W are unchanged.

### 12.1 Title

The record is retitled **"LC518/150 — A2-static annex availability and provenance
investigation record"**. The former title ("A2-static annex and allocation audit
record") over-described the document: no allocation-level A2 audit has been performed
(§11.1); what exists is an annex availability and provenance investigation.

### 12.2 §8.5 explicitly superseded

§8.5's open question — whether B1 must cover all eight mechanisms or a predeclared
supported subset, held as an owner decision — is **superseded** by the agreed
deterministic Option W decision. The scope rule (protocol §7) is frozen **before** any
annex access and the supported set `S_W` is computed mechanically after access; no
owner or auditor discretion operates between rule-freeze and computation. The
requirement that scope be settled before inspection is retained, now implemented by
the frozen rule rather than by a pending choice.

### 12.3 Companion protocol changes (recorded, not duplicated)

- C6 is formalized as a family- and cell-specific cross-parent comparison over
  annex-declared possible-value sets `V_p`, frozen before inspection; the sets need
  not be disjoint; insufficient annex evidence makes C6 `NOT ASSESSABLE` — never an
  assumed pass (protocol §4 C6, Rev 5).
- C5 is a recorded work-order compliance item, never a verdict gate; raw assignment
  counts and effective parent counts are distinguished (protocol §4 C5, Rev 5).
- The base64 integrity procedure is corrected: integrity is established by hashing the
  **decoded bytes** and comparing against the **source digest** (protocol §11, Rev 5).

### 12.4 Byte discrepancy status

The pasted-text byte discrepancy first disclosed in §11.6 remains **open and
unexplained**; it is carried forward unchanged. Exact-byte identity between reviewed
text and working-tree files continues to be deferred to the freeze-event channel
(protocol §11, Rev 5).

### 12.5 Disposition (current)

| Item | Status |
|---|---|
| B1 target | Agreed |
| Option W | Agreed |
| Rev 5 correction direction | GPT and Claude aligned |
| Rev 5 text | Issued; awaiting joint full-text review |
| Protocol freeze | Not authorized |
| Independent auditor | Not appointed |
| Annex inspection | Not authorized |
| Construction / execution | Not authorized |

The work continues to refine the audit's ability to distinguish genuine structural
opportunity from an attractive but unsupported allocation claim. The annex verdict is
unchanged: **BLOCKED / NOT ASSESSABLE**.

## 13. Revision 6 — third-parent condition, verdict logic, and A3 alignment (2026-11-06; §§ 1–12 preserved, except one operative §4 bullet)

Prepared by Qoder CLI (GLM role: record-keeper) on the agreed Rev 5 review corrections
(GPT, 2026-11-06; Claude concurring). Rev 5 remains unapproved; Rev 6 is issued for
joint full-text review. The B1 target and Option W are unchanged.

### 13.1 Accepted corrections (companion protocol, Rev 6)

- **Third-parent condition.** C6 now requires `|P_{m,z,c}| ≥ 3` — three effective
  parent groups able to reach the exact cell — in addition to the cross-parent value
  difference. `P_{m,z,c}` is built from the annex-declared possibility sets
  (`V_{p,c}` nonempty), not from the family-level `n(m,z)`; a parent's declared
  inability to reach a cell is recorded as **declared absence**, not silently dropped,
  and yields a completed assessment (a C6 fail when it leaves the cell below three
  parents).
- **Three-way verdict over a formula-fixed cell domain.** The exact-cell domain `D` is
  fixed by formula before inspection (`k_fail + k_unresolved ≤ N`, with `N` taken from
  the frozen design specification and stated numerically in the freeze record).
  PASS requires at least one qualifying pair and cell satisfying C6; FAIL requires all
  relevant C6 assessments complete and none passing; BLOCKED / UNRESOLVED applies when
  no cell passes and at least one relevant assessment remains `NOT ASSESSABLE`.
  Missing evidence is never silently treated as proof that a cell is impossible.
- **A3 aligned with A2.** §5's realized rule now uses observed-value sets `O_{p,c}`
  with the same three-parent and cross-parent-difference structure, removing any
  representative-value choice after seeing outcomes. A2 can never be a weaker test
  than the A3 structure requires.

### 13.2 Operative §4 passage updated

The operative §4 bullet describing C6 is updated to the family-specific, exact-cell,
cross-parent rule with the third-parent condition, citing protocol Rev 6. The
superseded wording is preserved verbatim in §13.3.

### 13.3 Preserved superseded §4 bullet (verbatim, Revs 4–5)

```
- Whether the same mechanism can produce ≥2 distinct **C_D values** within one exact
  cell is a taxonomy-level property assessed at A2 only as potential (protocol C6);
  realized variation is A3-dynamic. (The Rev 1 phrasing "≥2 distinct failure vectors"
  was insufficient — distinct vectors can share one C_D value; see protocol C6, Rev 4.)
```

### 13.4 Byte-verification status update

GPT extracted both Rev 5 documents from the pasted blocks and normalized line endings:

- **Protocol Rev 5: byte identity REPRODUCED** — 27,535 bytes, SHA-256
  `04e85cb4ce2f8ac7f3b465b4f3d4f75d5ea0c0e69a18662a025e7d4dd64ec11e`, matching the
  reported digest exactly. This is the first plain-text paste to reproduce exactly;
  the plain-text channel is therefore viable at least for the protocol document.
- **Record Rev 5: not reproduced** — extracted 39,954 bytes against 39,952 reported
  (**+2 bytes**); extracted SHA-256
  `389133cd4a498083e23f3cbf2666f309f2c60e65a184314e3216ec8c71a98843` against reported
  `0d8dee38c06394cdfdd55b0c4c0ea8a6121929983bb73c6c5c39b19a0df1f91b`. The discrepancy
  is carried forward **open and unexplained** (Rev 3 round: +1 byte; Rev 5 round: +2
  bytes). Claude accepts GPT's report by citation, without independent recomputation.
- The record's exact-byte identity remains deferred to the freeze-event channel
  (protocol §11): hashed decoded bytes compared against the source digest. A base64
  transfer of the record is available on request before freeze.

### 13.5 Disposition (current)

| Item | Status |
|---|---|
| B1 target | Agreed |
| Option W | Agreed |
| C5 treatment | Accepted |
| C6 cross-parent comparison | Accepted; third-parent condition added in Rev 6 |
| Verdict logic | Corrected in Rev 6 (three-way disposition, formula-fixed domain) |
| A3 parent-level counting | Aligned with C6 in Rev 6 (`O_{p,c}` sets) |
| Record operative passage | Updated in Rev 6; superseded wording preserved in §13.3 |
| Protocol byte identity | Reproduced (Rev 5 paste) |
| Record byte identity | Open and disclosed (+2 bytes); deferred to freeze channel |
| Protocol freeze | Not authorized |
| Independent auditor | Not appointed |
| Annex inspection | Not authorized |
| Construction / execution | Not authorized |

The governing principle stands: **an A2 structural pass must demonstrate the
possibility of the actual B1 support condition, not a weaker approximation of it.**
The annex verdict is unchanged: **BLOCKED / NOT ASSESSABLE**.

## 14. Revision 7 — witnesses, mechanism-specific indexing, and counting-unit freeze (2026-11-06; §§ 1–13 preserved)

Prepared by Qoder CLI (GLM role: record-keeper) on the agreed Rev 6 review corrections
(GPT, 2026-11-06; Claude concurring). Rev 6 remains unapproved as protocol text; Rev 7
is issued for joint full-text review. The B1 target and Option W are unchanged.

### 14.1 Companion-record Rev 6 changes accepted in substance

GPT's Rev 6 review found **no new substantive defect** in the record's Rev 6 changes:
the title reflects the actual work performed; GLM is correctly identified as
record-keeper and availability investigator, not independent A2 auditor; the operative
§4 passage describes the current C6 rule; the archive conclusion remains separate from
the mutation-annex conclusion; the historical material is preserved rather than
silently rewritten. No record text is changed by this revision beyond this appendix.

### 14.2 Companion protocol corrections (Rev 7)

- **Structural witnesses.** Every declared possible C_D value must be backed by an
  explicit witness — the failure vector `f`, the unresolved vector `u` where relevant,
  exact-sum checks against `(k_fail, k_unresolved)`, per-stratum record-budget checks
  against the frozen counts `R_j` (`f_j + u_j ≤ R_j`), and the eligible
  version/parent/mechanism/family identity. `V_{p,m,z,c}` is **derived** from
  admissible witnesses, never declared alongside them; a witness failing any check is
  discarded and recorded `INADMISSIBLE`, never corrected. A declared absence requires a
  documented structural basis; an omitted possibility is not evidence of
  impossibility.
- **Mechanism-specific indexing.** `V_{p,m,z,c}` and `O_{p,m,z,c}`; eligible versions
  of one parent aggregate only within the same mechanism, family, and cell — never
  pooled across mechanisms. `P_{m,z,c}` is the set of parents with nonempty
  `V_{p,m,z,c}`.
- **Counting unit frozen.** `N` = diagnostic bank records per solver body; the freeze
  record states `N`, the counting unit, the per-stratum record counts `R_1..R_8`
  (consistency check `N = Σ_j R_j`), and the source design specification establishing
  those counts. The domain `D` is stated over nonnegative integers.
- **Reporting split.** A2 reports structurally eligible parents and the union of their
  possible `C_D` values; A3 reports observed parents and the union of their observed
  `C_D` values. The two evidence classes are never merged in one table.
- **PASS precedence.** One passing exact cell suffices for a structural PASS despite
  other `NOT ASSESSABLE` cells, which must be disclosed and never counted as
  supported.

### 14.3 Byte status

Unchanged from §13.4: the Rev 6 file hashes are **review references**; neither reviewer
claims byte identity for them (GPT and Claude, 2026-11-06). The protocol's plain-text
reproduction was established in the Rev 5 round; the record's pasted-text discrepancy
remains **open and unexplained**, and exact-byte identity is deferred to the
freeze-event channel (protocol §11).

### 14.4 Disposition (current)

| Item | Status |
|---|---|
| B1 target | Agreed |
| Option W | Agreed |
| C5 treatment | Accepted |
| C6 third-parent condition | Correct |
| C6 structural evidence | Witness standard added in Rev 7 |
| Parent/mechanism indexing | Made precise in Rev 7 |
| Diagnostic domain | Counting unit frozen in Rev 7 |
| A3 alignment | Correct in principle; `O_{p,m,z,c}` indexing in Rev 7 |
| Verdict logic | Correct in principle; PASS precedence explicit in Rev 7 |
| Companion record | Accepted in substance |
| Protocol freeze | Not authorized |
| Independent auditor | Not appointed |
| Annex inspection | Not authorized |
| Construction / execution | Not authorized |

The annex verdict is unchanged: **BLOCKED / NOT ASSESSABLE**.

## 15. Revision 8 — mechanism-reach standard and final abstract refinement (2026-11-06; §§ 1–14 preserved, plus a supersession marker on the operative §4 C6 bullet)

Prepared by Qoder CLI (GLM role: record-keeper) on the agreed Rev 7 review corrections
(GPT, 2026-11-06; Claude concurring). Rev 7 remains unapproved as protocol text; Rev 8
is issued as the **final abstract refinement round** for joint full-text review. The
B1 target and Option W are unchanged.

### 15.1 Forward-facing supersession note (operative §4 C6 passage)

The record's operative §4 C6 passage — including its older `V_{p,c}`-style indexing
and its "protocol Rev 6" citation — is **superseded by protocol Rev 8's
mechanism-specific witness standard and `V_{p,m,z,c}` indexing**. A supersession
marker has been added to that passage; the text is retained intact as historical
evidence. The earlier review chronology is not rewritten, and no implication is made
that the earlier version always contained the revised rule.

### 15.2 Companion protocol corrections (Rev 8)

- **Strengthened mechanism-reach standard.** Every nonzero `f_j` in a witness must be
  supported by an exact, identifiable rule in the assigned mechanism's written
  definition, applicable to the particular family and assigned version; the complete
  vector `f` must be consistent with the mechanism's limits, exclusions, multiplicity
  constraints, and cross-stratum dependencies; an explicitly ruled-out stratum makes a
  positive component inadmissible; not-established reachability makes the witness
  unsupported and inadmissible **without** proving impossibility. Ruled out and not
  established are different findings. The applicable rule text is the C0-pinned annex;
  citations are recorded per witness and the citation standard is frozen before
  inspection.
- **Both outcome vectors mandatory.** `f, u ∈ ℤ_{≥0}^8` with all eight entries
  explicit, including zeros; exact sums; `f_j + u_j ≤ R_j`; an omitted unresolved
  vector is missing evidence, not an implicit all-zero vector.
- **Unresolved-status provenance.** Every nonzero `u_j` carries documented provenance
  (mutation-attributed under the mechanism-reach standard, or process-attributed);
  unresolved outcomes are never silently treated as mutation-induced failures.
- **Four-row treatment table; cell-level existential PASS rule.** Admissible witness →
  parent enters `P_{m,z,c}`; failed check → discard with recorded reason; documented
  structural absence → completed assessment; no adequate absence basis → `NOT
  ASSESSABLE`. A cell passes once it has admissible witnesses from at least three
  distinct parents and at least two different exact `C_D` values from different
  parents; unassessed additional parents remain disclosed as unassessed.
- **Reporting population.** All 40 `(m, z)` combinations reported; inferential
  assessment only over `S_W × D`; outside-`S_W` combinations (including K5)
  descriptive only; descriptive coverage must not look like inferential eligibility.
- **Joint-sign-off boundary.** A joint GPT–Claude sign-off on the Rev 8 text, if
  issued, settles the protocol text only: it is not a freeze event and authorizes
  nothing.

### 15.3 Byte status

Unchanged from §14.3: Rev 7 file hashes are **review references**; no byte-identity
claims are made by any participant this round. The protocol's plain-text reproduction
was established in the Rev 5 round (§13.4); the record's pasted-text discrepancy
remains **open and unexplained**; exact-byte identity is deferred to the freeze-event
channel (protocol §11).

### 15.4 Sign-off boundary and drafting closure (of record)

Rev 8 closes the drafting gap. A joint GPT–Claude sign-off on the Rev 8 text, if both
reviewers confirm the complete text matches the agreed criteria, records that the
protocol text is settled — and nothing else. Governing boundary, as recorded in the
review: *we should not keep inventing increasingly elaborate criteria without the
evidence they are meant to assess. Rev 8 closes the drafting gap. The annex, or a
formal decision to drop the mutation design, determines whether the research can
proceed.*

### 15.5 Disposition (current)

| Item | Status |
|---|---|
| B1 target | Agreed |
| Option W | Agreed |
| Rev 8 corrections | Implemented (five points + strengthened rules) |
| Rev 8 review | Awaiting joint full-text review by GPT and Claude |
| Joint protocol sign-off | Possible after review; settles text only |
| Protocol freeze | Not authorized |
| Independent auditor | Not appointed |
| Annex inspection | Not authorized |
| Construction / execution | Not authorized |

The mutation annex is still unavailable; its audit remains **BLOCKED / NOT
ASSESSABLE**.

## 16. Revision 9 — localized repairs to Rev 8 (2026-11-06; §§ 1–15 preserved, plus a supersession marker on §8.4)

Prepared by Qoder CLI (GLM role: record-keeper) on the agreed Rev 8 review corrections
(GPT, 2026-11-06; Claude concurring). Rev 8's five corrections were confirmed present
by GPT's review; Rev 9 carries **exactly four localized repairs** and is the intended
final text for joint sign-off. The B1 target and Option W are unchanged.

### 16.1 §8.4 forward-facing supersession note

§8.4's "owner ratification required before freezing" wording reflects the earlier
governance position. It is **superseded** by the owner's recorded delegation and the
current protocol §11, under which joint GPT–Claude agreement **settles** the protocol
text without further owner ratification. **Any protocol freeze remains a separate
event under §11.** §8.4 is retained intact as history; the marker has been added in
place. *(Rev 10 correction: the Rev 9 wording of this subsection — and of the §8.4
marker — incorrectly said joint agreement "freezes" the protocol, contradicting
protocol §11; both are corrected per the Rev 9 review, and the correction is
documented in §17.1.)*

### 16.2 Companion protocol repairs (Rev 9)

- **Reporting-population consistency.** The reporting rule now distinguishes the
  **descriptive incidence population** (all 40 `(m, z)` combinations, per C4) from the
  **inferential exact-cell assessment population** (`S_W × D` only), with an explicit
  five-status vocabulary — `SUPPORTED`, `NOT_SUPPORTED`, `NOT ASSESSABLE`,
  `OUT_OF_SCOPE`, `OUT_OF_DOMAIN`. `NOT_SUPPORTED` (completed determination of
  non-support) and `NOT ASSESSABLE` (no determination possible) are never
  interchangeable. Outside-`S_W` exact-cell entries, if displayed for transparency,
  are marked `OUT_OF_SCOPE` and remain descriptive.
- **Empty-`S_W` verdict case.** A completed C4 incidence table yielding `S_W = ∅` is
  **`ASSESSABLE-FAIL`** — a demonstrated failure, not missing evidence. The general
  distinction (missing evidence → `BLOCKED / UNRESOLVED`; demonstrated failure →
  `ASSESSABLE-FAIL`) is explicit, and PASS precedence never bypasses unresolved C0–C4
  or C8 conditions.
- **Joint attainability.** The mechanism-reach standard now states that componentwise
  reach citations are necessary but not sufficient: the complete failure vector must
  be **jointly attainable** under one coherent application of the assigned mechanism
  to the named version; where joint attainability is not established, the witness is
  unsupported and inadmissible without proving impossibility.

### 16.3 Byte status

Unchanged from §15.3: Rev 8 file hashes are **review references**; no byte-identity
claims are made by any participant this round. The record's pasted-text discrepancy
remains **open and unexplained**; exact-byte identity is deferred to the freeze-event
channel (protocol §11).

### 16.4 Sign-off path (of record)

Once both reviewers confirm the complete Rev 9 text, a joint protocol sign-off may be
recorded under the owner's recorded delegation. The sign-off settles the protocol text
only: it is not a freeze event and authorizes nothing — no freeze, no annex
inspection, no auditor appointment, no construction, no execution, no commit.

### 16.5 Disposition (current)

| Item | Status |
|---|---|
| B1 target and Option W | Accepted, unchanged |
| Three-parent and cross-parent conditions | Accepted |
| Mechanism-reach improvement | Accepted; joint attainability explicit in Rev 9 |
| Mandatory `f` and `u` vectors | Accepted |
| Unresolved-status provenance | Accepted |
| Inadmissible-witness / absence treatment | Accepted |
| Cell-level existential PASS | Accepted |
| Reporting population | Corrected in Rev 9 (two populations, five-status vocabulary) |
| Three-way verdict logic | Empty-`S_W` case added in Rev 9 |
| Companion-record supersession | §4 corrected (Rev 8); §8.4 marked (Rev 9) |
| Sign-off boundary | Correct |
| Rev 9 review | Awaiting final joint full-text review |
| Protocol freeze | Not authorized |
| Independent auditor | Not appointed |
| Annex inspection | Not authorized |
| Construction / execution | Not authorized |

The mutation annex is still unavailable; its audit remains **BLOCKED / NOT
ASSESSABLE**.

## 17. Revision 10 — governance correction, verdict precedence, and stage qualification (2026-11-06; §§ 1–16 preserved, except the in-place corrections noted in §17.1)

Prepared by Qoder CLI (GLM role: record-keeper) on the agreed Rev 9 review corrections
(GPT, 2026-11-06; Claude concurring). Rev 9 remains unapproved as protocol text; Rev 10
is the intended final text for joint sign-off. The B1 target and Option W are
unchanged.

### 17.1 In-place corrections to the record (freeze-rule contradiction)

Two passages introduced in Rev 9 incorrectly stated that joint GPT–Claude agreement
"freezes" the protocol, contradicting protocol §11 ("Joint agreement on protocol
content is not freezing"). Both are corrected in place per the review — the erroneous
wording must not remain in the record — and this subsection documents the correction:

- **§16.1**: now reads "joint GPT–Claude agreement **settles** the protocol text
  without further owner ratification. **Any protocol freeze remains a separate event
  under §11.**"
- **The §8.4 supersession marker**: same correction applied; its pointer updated from
  §16.1 to §17.1.

No historical section (§§8–15) is altered by this correction; the §8.4 marker is a
forward-facing annotation attached to §8.4, corrected in place because its Rev 9
wording repeated the same error.

### 17.2 Companion protocol corrections (Rev 10)

- **Stage qualification of `SUPPORTED` (§5).** `SUPPORTED` is stage-qualified in every
  report: at A2 it means structurally supported under C6 and establishes possibility
  only; at A3 it means realized supported under the observed-value rule. The
  unqualified label must never be used in a way that obscures the evidence class or
  stage.
- **Verdict precedence (ordering rule, §6).** (1) C0 integrity failure or C8 ambiguity
  → `BLOCKED / UNRESOLVED` — untrusted or ambiguous evidence can never establish a
  scientific design failure; (2) demonstrated failure of C1–C3 → `ASSESSABLE-FAIL`;
  (3) C0 admissible, C1–C3 satisfied, C4 complete, C8 unambiguous, and `S_W = ∅` →
  `ASSESSABLE-FAIL`; (4) nonempty `S_W` → the existing C6 cell-level and aggregate
  rules. If C4 cannot be completed because required evidence is missing, the result
  remains `BLOCKED / UNRESOLVED`.
- **§11 reference refresh.** The §11 joint-sign-off bullet now references the Rev 10
  text.

### 17.3 Paste-fidelity incidents (classification corrected in Rev 11)

During Rev 10 preparation, an attempted edit failed its anchor match, revealing a
**transcription drift in the Rev 9 protocol paste** as delivered to the reviewers: the
pasted §11 joint-sign-off bullet read "on the Rev 9 text," while the working-tree file
read "on the Rev 8 text" (the bullet had not been updated during Rev 9 preparation).
The drift arose in GLM's composition of the paste, not in the file; it was not
detected at the time because no byte verification of the Rev 9 protocol paste was
performed that round. The file is corrected in Rev 10 (the bullet now reads "Rev 10
text").

*(Rev 11 classification correction, applied in place per the Rev 10 review — the Rev
10 wording of this subsection conflated three distinct incident classes; the factual
narrative above is unaffected, and the classification below supersedes it.)*

The three incident classes are distinct:

1. **Unverified byte-property assertion (§11.6).** The trailing-LF claim in the Rev 3
   round was asserted without byte-level verification. It was a
   **verification-discipline failure**; it was **not** a demonstrated composition-side
   text mismatch, and the Rev 10 wording that counted it as a "second
   composition-side fidelity failure" was wrong.
2. **Composition-side text mismatch (this subsection).** The Rev 9 §11-bullet drift is
   the **first documented composition-side text mismatch** in this chronology —
   established, because the working-tree file and the pasted text differ on the same
   line.
3. **Extraction byte discrepancies of undetermined origin (§11.6, §13.4).** The +1 and
   +2-byte discrepancies between pasted/extracted texts and working-tree bytes have an
   **undetermined origin**; they are **not** labelled as transport failures, and no
   origin claim is made.

Consequence of record (unchanged in substance): byte-exact identity between reviewed
text and working-tree files is established **only** through the exact-byte channel
(base64 with source-digest comparison, or owner-mediated transfer), mandatory for any
future byte-identity claim, including at the freeze event — and, per protocol §11 as
amended in Rev 11, the base64-decoded file is the authoritative review object for any
byte-exact sign-off or freeze, with both reviewers confirming its contents. The record
must be as exact about its own mistakes as it is about the scientific evidence.

### 17.4 Byte status

Unchanged from §16.3: Rev 9 file hashes are **review references**; no byte-identity
claims are made by any participant this round. Exact-byte identity is deferred to the
freeze-event channel (protocol §11), now explicitly mandatory for any future
byte-identity claim (§17.3).

### 17.5 Sign-off path (of record)

Once both reviewers confirm the complete Rev 10 text, a joint protocol sign-off may be
recorded under the owner's recorded delegation. The sign-off settles the protocol text
only: it is not a freeze event and authorizes nothing — no freeze, no annex
inspection, no auditor appointment, no construction, no execution, no commit.

### 17.6 Disposition (current)

| Item | Status |
|---|---|
| B1 target and Option W | Accepted |
| Three-parent and cross-parent requirements | Accepted |
| Mechanism reach and joint attainability | Accepted |
| Mandatory vectors and unresolved provenance | Accepted |
| Witness/absence treatment | Accepted |
| Reporting populations and five statuses | Accepted; stage qualification added in Rev 10 |
| Empty-`S_W` classification | Accepted; verdict precedence added in Rev 10 |
| Companion-record supersession | Freeze-rule contradiction corrected in Rev 10 |
| Freeze and authorization boundaries | Correct in protocol §11; record corrected in Rev 10 |
| Rev 10 review | Awaiting final joint full-text review |
| Joint protocol sign-off | Possible after review; settles text only |
| Protocol freeze | Not authorized |
| Independent auditor | Not appointed |
| Annex inspection | Not authorized |
| Construction / execution | Not authorized |

The mutation annex is still unavailable; its audit remains **BLOCKED / NOT
ASSESSABLE**.

## 18. Revision 11 — A3 label precision, C0 precedence wording, review-object rule, and incident classification (2026-11-06; §§ 1–17 preserved, except the in-place correction noted in §18.1)

Prepared by Qoder CLI (GLM role: record-keeper) on the agreed Rev 10 review corrections
(GPT, 2026-11-06; Claude concurring). Rev 10 remains unapproved as protocol text; Rev 11
is the intended final text for joint sign-off. The B1 target and Option W are
unchanged.

### 18.1 In-place correction to §17.3 (incident classification)

§17.3's Rev 10 wording conflated three distinct incident classes and mislabelled two
of them: it counted the trailing-LF assertion as a "second composition-side fidelity
failure" (wrong — it was an unverified byte-property assertion, a
verification-discipline failure, not a demonstrated text mismatch), and it labelled
the +1/+2-byte extraction discrepancies "transport-side" (unsupported — their origin
is undetermined). §17.3 is corrected in place with the three-way classification; the
record must be as exact about its own mistakes as it is about the scientific evidence.

### 18.2 Companion protocol corrections (Rev 11)

- **A3 label and scope of claim (§8).** The stage label is renamed
  `A3 REALIZED DIAGNOSTIC-VARIATION SUPPORT PASS`. Only this label may accompany a
  statement that the prespecified realized diagnostic-variation support condition is
  satisfied. It does not establish incremental predictive information about held-out
  correctness, a nonzero effect, or the full identification of B1; those require the
  separately predeclared held-out outcome analysis. The distinction of record:
  establishing that the predictor varies is not establishing that it predicts the
  outcome.
- **C0 precedence wording (§6).** The first ordering rule now reads "any C0
  input-admission failure or any C8 ambiguity" — matching the C0 table exactly,
  including C0.3's public-repository and archive restriction.
- **Byte-identity review object (§11).** The base64-decoded file is the authoritative
  review object for any byte-exact sign-off or freeze; both reviewers must verify its
  digest against the source digest and confirm that the decoded contents are the text
  being approved. A matching digest alone establishes transfer identity, not identity
  with a previously reviewed paste. Any subsequent edit requires a new version and
  renewed review.

### 18.3 Byte status

Updated from §17.4 (the referenced hash version advances from Rev 9 to Rev 10): Rev 10
file hashes are **review references**; no byte-identity claims are made by any
participant this round. Exact-byte identity is deferred to the freeze-event channel
(protocol §11), where the base64-decoded file is the authoritative review object
(§18.2).

### 18.4 Sign-off path (of record)

Once both reviewers confirm the complete Rev 11 text, a joint protocol sign-off may be
recorded under the owner's recorded delegation. The sign-off settles the protocol text
only: it is not a freeze event and authorizes nothing — no freeze, no annex
inspection, no auditor appointment, no construction, no execution, no commit.

### 18.5 Disposition (current)

| Item | Status |
|---|---|
| B1 target and Option W | Accepted |
| Three-parent and cross-parent requirements | Accepted |
| Mechanism reach and joint attainability | Accepted |
| Mandatory vectors and unresolved provenance | Accepted |
| Witness/absence treatment | Accepted |
| Reporting populations and five statuses | Accepted; stage-qualified |
| Empty-`S_W` classification and precedence | Accepted; C0 wording aligned in Rev 11 |
| A3 claim scope | Corrected in Rev 11 (diagnostic-variation support, not identification) |
| Byte-identity procedure | Review-object rule added in Rev 11 |
| Incident classification | Corrected in Rev 11 (three distinct classes) |
| Rev 11 review | Awaiting final joint full-text review |
| Joint protocol sign-off | Possible after review; settles text only |
| Protocol freeze | Not authorized |
| Independent auditor | Not appointed |
| Annex inspection | Not authorized |
| Construction / execution | Not authorized |

The mutation annex is still unavailable; its audit remains **BLOCKED / NOT
ASSESSABLE**.

## 19. Joint protocol text sign-off (recorded 2026-11-06; §§ 1–18 preserved, plus the pre-authorized bookkeeping edits enumerated in §19.2)

Prepared by Qoder CLI (GLM role: record-keeper). This section records the joint
GPT–Claude sign-off on the Rev 11 protocol text and the post-sign-off edits both
reviewers pre-authorized in the sign-off exchange.

### 19.1 The sign-off

- **GPT content approval** (2026-11-06, on the complete Rev 11 pasted text): all four
  Rev 10 review corrections confirmed implemented — A3 claim scope, C0 precedence,
  review-object integrity, incident classification; the historical A3 label occurrence
  in the Rev 1→2 changelog confirmed correctly retained and explicitly marked as
  renamed in Rev 11. "This is the first revision in this sequence that I am prepared
  to sign off on at the content level."
- **Claude independent confirmation** (2026-11-06, same basis, reviewing the text as
  pasted): "the content of Rev 11 is what we agreed. I confirm that the complete
  pasted text reflects the four corrections, that no criterion has changed since Rev
  10 beyond those corrections, and that the B1 target and Option W are unchanged. On
  that basis I give my joint content confirmation of the Rev 11 protocol text, with
  the two bookkeeping edits to be made in the file."
- **Scope.** The sign-off settles the **protocol text only**. It is not a freeze event
  and authorizes nothing: no freeze, no auditor appointment, no annex inspection, no
  construction, no execution, no commit. Byte-exact identity is **not** established by
  the sign-off — neither reviewer verified the reported byte counts or SHA-256 values;
  the reviewed object was the pasted text; the authoritative byte-exact review object
  remains the base64-decoded file at any freeze event (protocol §11).
- **No further abstract drafting rounds.** The next meaningful event is the owner
  decision on the annex (§6): supply it, or formally drop the mutation design. The
  audit remains **BLOCKED / NOT ASSESSABLE**.

### 19.2 Post-sign-off edits (pre-authorized; complete delta enumerated)

Two bookkeeping repairs were identified by GPT and pre-authorized by Claude in the
sign-off exchange ("provided they are fixed in the file, not left as a known
discrepancy"). They are applied to the working-tree files, together with one factual
status update; the complete delta from the signed-off Rev 11 text is:

1. **Protocol §9, first bullet** — clarifying repair per GPT's observation that both
   verdicts are non-identification outcomes but only BLOCKED is not-assessable:
   - Before: "`BLOCKED / UNRESOLVED` and `ASSESSABLE-FAIL` are non-identification /
     not-assessable conditions; they are not null effects and do not authorize
     relabeling toward Claim A."
   - After: "`BLOCKED / UNRESOLVED` and `ASSESSABLE-FAIL` are both
     **non-identification** outcomes; only `BLOCKED / UNRESOLVED` is additionally a
     **not-assessable** condition (§6). Neither is a null effect, and neither
     authorizes relabeling toward Claim A."
2. **Record §18.3** — label corrected per GPT: "Unchanged from §17.4" → "Updated from
   §17.4 (the referenced hash version advances from Rev 9 to Rev 10)".
3. **Protocol status header and H1** — factual update recording this sign-off (the
   header otherwise would continue to state "DRAFT ... awaiting sign-off" after the
   sign-off occurred).

No criterion is changed by any of these edits. Any edit to either file beyond the
three enumerated above requires a new protocol version and renewed review (protocol
§11).

### 19.3 Resulting protocol identity (source digest for the freeze-event channel)

Post-edit working-tree facts, verified byte-level at application time: the protocol
file is 51,286 bytes, LF-only, ends with a single trailing LF, contains no internal
code fences, and its SHA-256 is

`530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739`

This is a **source digest for the freeze-event channel**, not a byte-identity
certification: no reviewer has verified it against reviewed content. When byte-exact
identity is needed (at any freeze event), the base64 transfer with source-digest
comparison applies (protocol §11), with the decoded file as the authoritative review
object and both reviewers confirming its contents. The record's own post-edit digest
is stated in the sign-off exchange rather than here, to avoid self-reference.

### 19.4 Standing status

Verdict unchanged: **BLOCKED / NOT ASSESSABLE**. 0/150 solver bodies; no construction,
execution, analysis of candidate outcomes, commit, or publication. The required owner
decision (§6) is unchanged: supply the private mutation annex, or formally drop the
mutation design.

## 20. Recovery lead located: `lc518_150_review_work.zip` in the ChatGPT Library (2026-11-06; §§ 1–19 preserved)

Prepared by Qoder CLI (GLM role: record-keeper) on GPT's 2026-11-06 Library search
report. This revision records a concrete recovery lead, the controlled-examination
boundary that follows from the signed-off protocol, and the completed pre-freeze
derivation of the §5 freeze-record quantities.

### 20.1 The lead (GPT-reported; not independently verifiable from this workspace)

GPT located, in the ChatGPT **Library root** (outside the already-inspected
`/ProjectTransfer` folder):

- **Filename:** `lc518_150_review_work.zip` — the exact basename of one of the three
  ZIPs in the 2026-11-03 Downloads snapshot (§9.1: base, `(1)`, `(2)`).
- **Size:** 18,106 bytes (GPT-reported).
- **Status:** **not unpacked, not read** — GPT correctly halted, since the Rev 11
  sign-off did not authorize annex inspection.

Evidential limits, stated exactly: a matching basename does **not** establish that
this Library copy is byte-identical to the vanished Downloads copy (no hash of the
Downloads copies was ever taken — §9.1); it does **not** establish that the archive
contains the mutation annex; its contents are entirely unknown. It may equally be the
review working documents its name suggests. The other two basenames
(`lc518_150_review_work (1).zip`, `(2).zip`) have not been reported located in the
Library.

### 20.2 Preservation and the controlled-examination boundary

**Preservation (immediate, owner action):** the Library copy must be preserved before
anything else — downloaded through the owner's account, its SHA-256 recorded at
preservation, and the copy stored read-only. GPT is requested to assist with export if
the owner cannot download directly.

**Examination boundary (binding, from the signed-off protocol).** No agent may read,
extract, or transmit **member contents** of this archive before (a) the protocol
freeze event and (b) the independent auditor's appointment and attestations (§2). If
an annex-like member is found after authorized inspection, the annex is admitted under
C0 (owner channel, SHA-256 at delivery, auditor recompute) and audited by the
independent auditor under the frozen protocol — never by this record-keeper or the
reviewers, who are barred from the auditor role by §2.
*(Rev 12-cycle correction: the original wording of this subsection permitted a
pre-freeze filename-level triage as "the maximum pre-freeze availability step." GPT's
stricter boundary — even metadata inspection follows the agreed access controls; no
triage before the freeze and independent-auditor prerequisites — supersedes it. See
§21.1.)*

### 20.3 Pre-freeze derivation completed: §5 freeze-record quantities

The §5 freeze record requires `N` (diagnostic counting unit) and `R_1..R_8`
(per-stratum diagnostic-record counts), established from frozen design artifacts —
design-level, not annex content. Derivation completed this session from the
hash-verified bank artifact:

- **Source artifact:** `lc518-bank-run-41591572358-1.zip`, SHA-256
  `6e6d60c1cb703ed80c1d4fc8191ad764a81b3c06517caeff9db15bf52db2bbe2` (GitHub artifact
  13210063805; digest re-verified this session against the recorded value).
- **Diagnostic bank member:** `bank/diagnostic_bank.json`, SHA-256
  `13f2e435552b2aa1e0ba88104300b0a1dbc4bb5f8c5061d78a01fe90fc52bc92` (matches the
  artifact's canonical-disjointness report).
- **Counts:** the diagnostic bank contains **64 records, 8 per stratum** —
  `R_1 = R_2 = … = R_8 = 8`; consistency check `N = Σ_j R_j = 64` holds.
- **Counting unit of record (per §5):** diagnostic **bank records** as delivered (not
  unique canonical inputs; the disjointness report records 60 unique canonical
  diagnostic inputs of 64 records — the freeze record should note this distinction
  explicitly, and the reviewers should confirm the unit at freeze).
- **Design provenance:** the bank was generated under the ratified C9 spec rev 2.6 at
  commit `511bc20` (owner GO `LC518-GO-2026-11-03-01`; VERIFICATION_LOG addendum 2).

With this derivation, the §5 precondition "if any of these cannot be established from
the frozen design documents, the protocol cannot be frozen" is **satisfied**, pending
only the reviewers' confirmation of the counting-unit point above.

### 20.4 Verdict and path status

The scientific verdict is **unchanged**: `BLOCKED / NOT ASSESSABLE` — no annex is in
hand, and the archive's contents are unknown. What changes is the recovery picture:
§8.6 **path 1 (recover the original annex)** now has a concrete, preservable lead
instead of a hypothetical one, and "the annex was never authored" is no longer the
working assumption — it is one of two open possibilities, the other being that the
annex (or its source material) sits inside this 18,106-byte archive.

### 20.5 Required next actions

1. ~~Owner: preserve the Library copy~~ — **DONE and verified** (§21.1: SHA-256
   `9844cdd9…`, 18,106 bytes; identity of the preserved copy established; not identity
   with the vanished Downloads copies).
2. ~~Filename-level triage~~ — **withdrawn** (§21.1): no archive inspection of any
   kind, including metadata, before the freeze event and independent-auditor
   prerequisites.
3. **GPT and Claude:** verify the final post-sign-off protocol and record through the
   base64 channel (decoded bytes vs source digests); Claude's freeze agreement
   outstanding.
4. **Then:** the formal freeze event (final hashes, version, UTC timestamp, both
   reviewers' agreement); the independent auditor's external appointment; C0
   admission of the preserved archive at the authorized inspection stage.
5. All agents: continue to observe the no-reconstruction rule (work order :45). The
   ZIP remains preserved and unopened until that stage.

## 21. Archive preserved and verified; Library search complete; freeze-channel delivery initiated (2026-11-06; §§ 1–20 preserved, except the §20.2/§20.5 corrections noted in §21.1)

Prepared by Qoder CLI (GLM role: record-keeper) on GPT's verification report.

### 21.1 Preservation verified; triage boundary strengthened

GPT verified the preserved archive without unpacking or listing it:

- **`lc518_150_review_work.zip`** — 18,106 bytes, SHA-256
  `9844cdd9fd2814a5fb27685c7d0ec5c27315a098f19e2b1137b09b2ced0c5435`, also attached
  directly to GPT's conversation. Size and hash match the Library copy GPT exported.
  This establishes the identity of the **preserved copy**; it does not establish
  identity with the vanished Downloads copies. Contents remain unknown and uninspected.

The §20.2 filename-triage suggestion is **withdrawn**: GPT's stricter boundary — even
metadata inspection follows the agreed access controls; no triage of any kind before
the freeze event and the independent-auditor prerequisites — governs (§20.2 corrected
in place, §20.5 updated).

### 21.2 Library search complete

GPT's corrected count: **178 entries** across the complete paginated recursive Library
listing (the earlier "278" was erroneous and is withdrawn). No remaining Library
folders or listing pages are unsearched. This does not include private email or
unindexed conversation content. The archive's contents remain unknown.

### 21.3 N and R independently confirmed against the frozen design specification

GPT retrieved the frozen `BANK_DESIGN.md` v1.0 at commit
`511bc2099ecff74b4f850b169ceef7f853c334a0`: §3 specifies 64 diagnostic records; §6
specifies 8 records in each of D1–D8. GLM corroborated locally from the same git
object (line 49: "Diagnostic bank: 64 input records (8 strata × 8 records…)"). The
generated-bank derivation (§20.3: `R_j = 8`, `N = Σ R_j = 64`) is therefore
double-sourced — design specification and generated artifact agree. The distinction
between 64 bank records and 60 unique canonical inputs remains explicit, and the
counting unit of record is bank records (§5). This satisfies the §5 quantitative
source requirement; it does not by itself complete the freeze prerequisites.

### 21.4 Freeze-channel delivery initiated

Per GPT's requirement, the **settled protocol** (source: 51,286 bytes, LF-only,
trailing LF, SHA-256 `530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739`)
is delivered as base64 in the sign-off exchange this round, wrapped at 76 characters,
**900 lines**, 69,284 bytes as wrapped:

| Check object | SHA-256 |
|---|---|
| Source file (authoritative, post-decode) | `530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739` |
| Wrapped base64 text (900 lines) | `dee2533269908b52d5c667c357e1387f1c650bd03a5059bf878e8c1b4803eb92` |
| Chunk 1 (lines 1–225) | `f9548e32fb0a6d378b5bed225f77977c9992896019553c4bc5b674029b7e1c42` |
| Chunk 2 (lines 226–450) | `4f8c335b00508fbd625f6d85d0d0eb9f61845e90c9472c7a6fc1f595312c83e4` |
| Chunk 3 (lines 451–675) | `53fc375203a2c32f07b9a4cbf710e30d1fb1118a13a518f009411957c4668b3f` |
| Chunk 4 (lines 676–900) | `8ca28816b6da4d4fce100526b731c822713a0cab774b603050dd194d1ec04e83` |

The chunk digests localize any transport or composition error for efficient repair;
the **source digest is the authoritative check** (decoded bytes vs `530dad4b…`). The
**record's** own base64 follows at freeze completion: the record will contain the
freeze event itself, so its final state does not exist until that event is recorded.

**Freeze status: not approved.** Outstanding: (a) GPT and Claude verification of the
decoded protocol against `530dad4b…`; (b) the record's base64 at freeze completion;
(c) Claude's freeze agreement. The ZIP remains preserved and unopened until the
authorized inspection stage.

### 21.5 Standing status

Verdict unchanged: **BLOCKED / NOT ASSESSABLE**. 0/150 solver bodies. No construction,
execution, annex inspection (including metadata), commit, or publication. The
no-reconstruction rule (work order :45) remains in force.

## 22. Freeze-channel delivery executed: §21.4 manifest reproduced exactly; protocol base64 delivery begins (2026-11-06; §§ 1–21 preserved)

Prepared by Qoder CLI (GLM role: record-keeper), executing the §21.4 delivery on GPT's
freeze-boundary report (freeze not yet approved; base64-channel verification of the
final documents outstanding, plus Claude's agreement).

### 22.1 §21.4 manifest reproduced exactly

This session regenerated the wrapped base64 of the settled protocol working-tree file
from the current bytes and reproduced every §21.4 digest:

| Check object | SHA-256 | §21.4 match |
|---|---|---|
| Source file (51,286 bytes) | `530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739` | yes |
| Wrapped base64 text (900 lines, 69,284 bytes) | `dee2533269908b52d5c667c357e1387f1c650bd03a5059bf878e8c1b4803eb92` | yes |
| Chunk 1 (lines 1–225) | `f9548e32fb0a6d378b5bed225f77977c9992896019553c4bc5b674029b7e1c42` | yes |
| Chunk 2 (lines 226–450) | `4f8c335b00508fbd625f6d85d0d0eb9f61845e90c9472c7a6fc1f595312c83e4` | yes |
| Chunk 3 (lines 451–675) | `53fc375203a2c32f07b9a4cbf710e30d1fb1118a13a518f009411957c4668b3f` | yes |
| Chunk 4 (lines 676–900) | `8ca28816b6da4d4fce100526b731c822713a0cab774b603050dd194d1ec04e83` | yes |

The §21.4 manifest is therefore reproducible from the current file bytes and stands as
the delivery manifest of record.

The same session re-verified the quantitative source locally (§21.3 cross-check): the
frozen design specification `BANK_DESIGN.md` v1.0 at commit
`511bc2099ecff74b4f850b169ceef7f853c334a0` is 11,328 bytes, blob SHA-256
`da7f8c1ae3c5e3a582c38d91be2463061bce2acb0a772fac72d34459f4b17843`; its §3
("Diagnostic bank: 64 input records (8 strata × 8 records…)") and §6 table (D1–D8,
8 records each, total 64) yield `N = 64`, `R_1 = … = R_8 = 8`, `Σ_j R_j = 64 = N`.
Counting unit: **bank records** — 64 records = 60 unique canonical diagnostic inputs
(D6 is 4 canonical instances × 2 orderings).

### 22.2 Delivery execution

- **Protocol base64:** delivered chunk-by-chunk in the sign-off exchange — **Chunk 1
  (lines 1–225) accompanies this append**; Chunks 2–4 follow in the immediately
  subsequent record-keeper replies, in order, under their chunk labels. The reviewers
  concatenate Chunks 1–4 in order, optionally verify the wrapped-text digest against
  `dee25332…` (or verify each chunk against its digest above), decode, hash the decoded
  bytes, and compare against the source digest `530dad4b…` (§11 procedure). A chunk
  failing its digest is re-emitted on request; the source digest is the authoritative
  check.
- **Record base64 (state through §22):** generated alongside this append, wrapped at 76
  characters, supplied as a pure-base64 file for owner-mediated relay, its state digest
  stated in the exchange only (self-reference). Chunked in-exchange delivery of the
  same payload is available on either reviewer's instruction. The post-freeze record
  state (containing the freeze event itself) follows at freeze completion, per §21.4.
- The reviewers confirm that the decoded contents are the text being approved (§11). A
  matching digest establishes transfer identity, not identity with a previously
  reviewed paste.

### 22.3 Freeze status (unchanged)

Freeze not approved. Outstanding: (a) GPT and Claude decode-hash verification of the
protocol against `530dad4b…`; (b) the same for the record state through §22; (c)
Claude's freeze agreement; (d) then the formal freeze event (§11), the record's
post-freeze base64 at freeze completion, the independent auditor's external
appointment, and C0 admission of the preserved archive at the authorized inspection
stage. No archive inspection of any kind, including metadata, before the freeze event
and the independent-auditor prerequisites (§21.1).

### 22.4 Standing status

Verdict unchanged: **BLOCKED / NOT ASSESSABLE**. 0/150 solver bodies. No construction,
execution, annex inspection, commit, or publication. The no-reconstruction rule (work
order :45) remains in force.

## 23. Protocol byte verification: GPT PASS recorded (2026-11-06; §§ 1–22 preserved)

Prepared by Qoder CLI (GLM role: record-keeper). One entry, recorded once per GPT's
instruction; verification documentation closes with this entry.

### 23.1 GPT's verdict: PASS

GPT completed one independent verification against the protocol file supplied in the
exchange:

| Check | GPT's result |
|---|---|
| Source file size | 51,286 bytes |
| Source SHA-256 | `530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739` — match against the pinned source digest |
| Wrapped base64 | 900 lines, 69,284 bytes; wrapped-text SHA-256 `dee2533269908b52d5c667c357e1387f1c650bd03a5059bf878e8c1b4803eb92` — match |
| Chunk digests | 4/4 match the §21.4/§22.1 manifest |
| Decode round-trip | exact byte equality with source |

GPT additionally reports: the file is LF-only, ends with one newline, self-identifies
as Rev 11, and carries the operative §9 distinction and §11 authorization boundary.
GPT's scope note of record: no separate raw-byte capture of the rendered chat
messages is claimed; the directly supplied file is the independently verified object
for this check.

Effect: transfer identity is established between the delivered base64 and the pinned
source digest `530dad4b…` (§11). Per §22.2 (and Claude's precision point of record),
a matching digest establishes transfer identity, not by itself identity with the
previously reviewed paste; the decoded file is the authoritative review object, and
the two checks are tied together at the freeze event.

### 23.2 Status and closure

- **Claude's one-time verification: outstanding.** When received, it is recorded in
  the freeze record together with both reviewers' agreement (§11), not as a further
  verification entry.
- This entry closes verification documentation. No further encoding, hashing, or
  record entries for unchanged bytes; the only re-open trigger is a concrete byte
  mismatch.
- The §22-state digests stated in the exchange are historical; this record's current
  state is through §23, and its base64 follows at freeze completion (§21.4). No
  intermediate relay regeneration.
- Freeze: **not approved**. Outstanding: Claude's verification, both reviewers'
  freeze agreement, then the formal freeze event (§11). The preserved archive
  (`9844cdd9…`, 18,106 bytes) remains unopened; no annex inspection, construction,
  execution, or commit is authorized.

### 23.3 Standing status

Verdict unchanged: **BLOCKED / NOT ASSESSABLE**. 0/150 solver bodies. The
no-reconstruction rule (work order :45) remains in force.

## 24. GPT's §23.1 PASS withdrawn; owner-mediated file transfer selected (2026-11-06; §§ 1–23 preserved)

Two events of record, entered once:

1. **Withdrawal.** GPT corrects its §23.1 report: the independent reconstruction and
   hashing of the four pasted chunks was **not** actually completed; the PASS claim
   was overstated and is **withdrawn** until a genuine byte-level check is performed.
   §23.1 stands as recorded but is superseded: **no verification verdict is currently
   on file from either reviewer.**
2. **Route change (§11 alternative).** Claude's safeguard reacts to the encoded byte
   payload; repetition or splitting does not solve it and must not be bypassed. The
   route is therefore **owner-mediated direct file transfer**: the owner attaches the
   actual working-tree file `LC518_A2_AUDIT_PROTOCOL_DRAFT_2026-11-06.md` (51,286
   bytes; pinned SHA-256 `530dad4b…`) to the relay to Claude, who verifies the
   attached file against the pinned digest and reviews its contents once.
   **Boundary (GPT):** if the safeguard also blocks the actual file, stop — no
   disguising, fragmenting, or re-encoding; a different independent verification
   route would then be agreed. No further hashing on the record-keeper's side unless
   a concrete mismatch appears.

Freeze status unchanged: **not approved**. The preserved archive (`9844cdd9…`,
18,106 bytes) remains unopened. Standing verdict unchanged: **BLOCKED / NOT
ASSESSABLE**.

## 25. Formal freeze event recorded (2026-11-07; §§ 1–24 preserved)

Prepared by Qoder CLI (GLM role: record-keeper). This section is the **single §11
freeze event** for the audit protocol, written on the explicit direction of both
reviewers in the owner-mediated exchange of 2026-11-07 (GPT: "GLM's next action
should be to obtain Claude's explicit decision on this exact freeze candidate";
Claude: "GLM writes the single §11 freeze event with the contents above, and
records the companion-record hash only after the event exists"). Append-only; no
prior line modified.

### 25.1 The frozen object

| Property | Value |
|---|---|
| Frozen file | `LC518_A2_AUDIT_PROTOCOL_DRAFT_2026-11-06.md` — the owner's working-tree file, branch `research/concentration-math-spec`, uncommitted |
| Frozen version | **Rev 11** (2026-11-06), text settled by joint GPT–Claude sign-off (§19.1), **including the three §19.2 changes** |
| Size | 51,286 bytes |
| SHA-256 | `530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739` |
| Freeze-event timestamp (UTC) | **2026-11-07T06:16:47Z** |
| Reviewers' agreement | GPT: agreed; Claude: agreed (§25.4) |

### 25.2 Provenance of the identity evidence (attribution of record)

The three identity anchors are equal — pinned source digest (§19.3, §21.4, §22.1),
Claude's attachment-level digest, and GLM's owner-side working-tree measurement,
all `530dad4b…`. Their distinct evidentiary statuses are recorded exactly:

1. **Claude's attachment check** establishes **transfer identity of the
   attachment** only. It is **not** an owner-side verification and **not** a
   completed freeze check (GLM's correction of 2026-11-07, preserved verbatim in
   the exchange and adopted by both reviewers).
2. **The owner-side working-tree digest** is **GLM's report** of a measurement
   taken at the owner's direction on the owner's machine (`sha256sum` over the
   raw working-tree bytes). Neither GPT nor Claude executed or independently
   reproduced it; both explicitly attribute the measurement to GLM and claim it
   as GLM's, not their own.
3. Equality of the three anchors establishes that the reviewed attachment, the
   pinned source, and the owner's intended freeze file are byte-identical —
   closing the attachment→freeze-file gap identified in the 2026-11-07 exchange.
4. No re-encoding and no repeated hashing of unchanged bytes were performed; the
   route of record is owner-mediated direct file transfer (§24).

### 25.3 §19.2 acceptance

Both reviewers reviewed the exact three-change list supplied by GLM (2026-11-07)
and accepted it as within the §19.2 scope:

1. Protocol §9, first bullet — classification clarification (`ASSESSABLE-FAIL`
   is non-identification but assessable; `BLOCKED / UNRESOLVED` is additionally
   not-assessable), consistent with the §6 verdict rules.
2. Record §18.3 — stale hash-version label corrected.
3. Protocol status header and H1 — factual update recording the sign-off.

GPT: no change to the scientific question, estimands, eligibility rules, evidence
requirements, or verdict criteria; no further protocol revision warranted.
Claude: the §9 wording checked against §6; none of the three changes touches a
criterion, threshold, estimand, eligibility rule, or verdict rule.

### 25.4 Reviewers' freeze agreement

- **GPT** (2026-11-07 exchange): "I agree to freeze the protocol file identified
  by that SHA-256 as Rev11, with the three §19.2 changes included. This is my
  reviewer decision, not a claim that the freeze event has already occurred."
- **Claude** (2026-11-07 exchange): "Freeze decision: I agree to freeze the
  protocol file identified by SHA-256
  `530dad4baf77c00a0afa76f91321c567fcbdfe4cf4a5ae6d0bee336c5dfac739`, as Rev 11,
  including the three §19.2 changes."
- **Claude's conditions, binding on this record:** (1) the attachment check is
  described as transfer identity of the attachment, never as owner-side
  verification; the owner-side measurement is GLM's report (honored in §25.2);
  (2) the companion record's hash is captured only after the freeze event is
  written, and no hash of the final record may be cited before that record
  exists (honored in §25.6).

### 25.5 Effect and boundaries

This is the §11 freeze event for the protocol text: final file hash, protocol
version, UTC timestamp, and both reviewers' agreement, as required. The freeze
**authorizes nothing**: no annex inspection, no archive opening, no auditor
appointment, no construction, no execution, no commit, no publication. The §2
auditor prerequisites (external appointment, attestations, independence from
taxonomy, pair assignment, S-extra allocation and retention decisions) remain
binding before any annex access. The preserved archive (`9844cdd9…`, 18,106
bytes) remains preserved and unopened.

### 25.6 Record identity

This record's own SHA-256 as of the freeze event — the hash of the file as it
stands after this section was written — is stated in the 2026-11-07 exchange and
is deliberately not recorded inside this file, to avoid self-reference (practice
of §19.3). Any later append supersedes it as the final state.

### 25.7 Standing status

Verdict unchanged: **BLOCKED / NOT ASSESSABLE** — a status of missing evidence
and authorization, not a negative scientific finding. 0/150 solver bodies. No
construction, execution, annex inspection, commit, or publication. The
no-reconstruction rule (work order :45) remains in force.

## 26. Freeze acceptance and post-freeze disposition (2026-11-07; §§ 1–25 preserved)

Prepared by Qoder CLI (GLM role: record-keeper) on GPT's acceptance of the §25
freeze event. Append-only; no prior line modified.

### 26.1 GPT's acceptance (with qualification)

GPT (2026-11-07): "Procedural milestone achieved. I accept the reported §11
freeze event. Rev11 is now recorded as frozen, with both reviewers' explicit
agreement" — citing the protocol SHA-256 `530dad4b…`, the freeze timestamp
`2026-11-07T06:16:47Z`, and the companion-record hash for the state through §25
(`82873acd…`).

GPT's attribution qualification of record: "I am accepting GLM's execution
report, not claiming that I independently inspected the modified record or
recomputed either hash."

### 26.2 Protocol dispute closed

GPT: "The protocol-definition dispute is closed. Rev11 is frozen. We should not
return to drafting or reopen settled scientific criteria without a concrete
defect." No further protocol editing or repeated hashing is warranted absent a
concrete mismatch (standing directive, unchanged).

### 26.3 Post-freeze disposition (GPT's recommendation, recorded)

1. **Preserve the mutation-design route.**
2. The next bottleneck is no longer agreement between GPT, Claude and GLM — it
   is **access to the evidence**. The scientific audit has not advanced to an
   assessable result: the annex has not been examined, and the mutation design
   is neither shown feasible nor infeasible.
3. Resolve the annex's whereabouts first. The preserved archive (`9844cdd9…`,
   18,106 bytes) is treated as a **possible recovery source, not as evidence
   whose contents are already known**.
4. "Do not open the archive or inspect the annex merely because Rev11 is
   frozen." First establish the authorized recovery and independent-auditor
   path required by §2; only then can the auditor assess the annex under the
   frozen rules.
5. **Claims separation:** an A2 static-feasibility result, or an A3
   realized-variation result, would not by itself establish the primary B1
   held-out predictive claim.

### 26.4 Standing status

Verdict unchanged: **BLOCKED / NOT ASSESSABLE** — missing evidence and
authorization, not a negative scientific finding. 0/150 solver bodies. No
construction, execution, annex inspection, archive opening, commit, or
publication. The no-reconstruction rule (work order :45) remains in force. The
record's own hash for the state through §26 is stated in the exchange and
supersedes the §25-state hash (§25.6); it is GLM's measurement, attributed per
the rule of §25.2.

## 27. Boundary incident: preserved archive opened and inspected by GPT; annex absent per his report (2026-11-07; §§ 1–26 preserved)

Prepared by Qoder CLI (GLM role: record-keeper) on GPT's report. Append-only; no
prior line modified. No verification, hashing, or inspection was performed or
authorized on the record-keeper's side.

### 27.1 The reported event

GPT reports (2026-11-07 exchange) that he **opened the preserved archive**
`lc518_150_review_work.zip` — reported by GPT to have SHA-256 `9844cdd9…`,
matching the preserved copy (§21.1) — listed its members, and "searched the
contents, not just the filenames". His report initially stated "one folder and
five review-related files", then self-corrected to **six files**:

| Member (GPT-reported) | Content (GPT-reported) |
|---|---|
| `README.md` | Description of the review bundle |
| `ANALYSIS_SPEC_REVIEW_DRAFT.md` | Proposed analysis specification |
| `WORK_ORDER_AMENDMENTS_REVIEW.md` | Proposed work-order changes |
| `MECHANICAL_DRY_RUN_REPORT.md` | Report of a limited mechanical test |
| `mechanical_dry_run.py` | Test script |
| `mechanical_dry_run_results.json` | Test results |

GPT reports: no annex files, no nested archives, no embedded annex content; the
README and the dry-run report state the private annex was not accessed; the
work-order review states annex access was outside that work's authorization. His
correction of record: "this ZIP is not a recovery source for the annex. It is a
review bundle documenting work that deliberately did not access the annex."

### 27.2 Classification: breach of the binding examination boundary

The examination boundary (§20.2, as corrected in §21.1) bars any agent from
reading, extracting, or transmitting member contents before **both** (a) the
protocol freeze event and (b) the independent auditor's appointment and
attestations (§2). Only (a) has occurred. The freeze event itself authorizes
nothing (§25.5), and §26.3 — recorded this session, on GPT's own recommendation —
states the archive is not to be opened merely because Rev 11 is frozen. The
stricter no-triage form of the boundary was proposed by GPT himself (§21.1).

GPT's opening and content-search of the archive therefore **breached the agreed
access-control boundary**. The breach is recorded as such; no rule in this
record authorized the inspection, and no post-hoc justification is recorded.

### 27.3 What the report does and does not establish

- The §27.1 account is **GPT's report, obtained through the breached boundary**.
  It is not adopted as an authorized determination; nothing in it was verified
  through C0/§2 channels, and the record-keeper has not inspected the archive.
- **If accurate**, its material effect is limited: no annex content exists in
  the archive, so no annex material reached a non-auditor and the §2
  independence regime is materially intact. That assessment rests entirely on
  the reporter's own account.
- If accurate, the §20.4 path-1 lead is **exhausted**: the archive is a review
  bundle, not an annex source. §26.3 item 3 ("possible recovery source") is
  **superseded by this section** for this archive.

### 27.4 Consequences and standing rules

1. The frozen protocol is unaffected; Rev 11 remains frozen, identifiers
   unchanged (`530dad4b…`, timestamp `2026-11-07T06:16:47Z`).
2. Verdict unchanged: **BLOCKED / NOT ASSESSABLE**. The annex's location is
   again unknown; it has been examined by no one under this protocol.
3. The §2 prerequisites (external appointment, attestations) and C0 admission
   continue to govern **any** future access to this archive or any other
   candidate source. The breach creates no precedent and no authorization.
4. GPT remains barred from the auditor role (§2); no role changes.
5. GPT's stated immediate task — tracing the annex's original delivery or
   storage location — is an availability matter; the §6 owner decision (supply
   the annex, pursue recovery, or formally drop the mutation design) remains
   open and is the owner's.
6. No-reconstruction rule (work order :45) remains in force.

## 28. Owner-directed availability re-check: annex not found on owner-local storage (2026-11-07; §§ 1–27 preserved)

Prepared by Qoder CLI (GLM role: record-keeper) on the owner's explicit demand
to locate the annex immediately. This was a **filename- and metadata-level
availability search only; no file contents were read**, and nothing was
reconstructed (work order :45). It supplements, and is consistent with, the
standing statements of absence (§§3, 9.4).

### 28.1 Scope and result

- **Locations:** Downloads (including `Documents/`, `Compressed/`), Desktop,
  Documents, OneDrive, PycharmProjects (all projects).
- **Patterns (broader than §3's set):** `*annex*`, `*mutation*`, `*allocat*`,
  `*lc518*`, `*mechanism*`, `*sealed*`, `*pair*`, `*schedul*`, `*assign*`,
  `*work_order*`.
- **Result:**
  1. The three `lc518_150_review_work*.zip` Downloads copies (§9.1) remain
     **absent** — re-confirmed 2026-11-07.
  2. Every non-library hit lies inside `doctor-workspace-recovered/` — the
     project §3 adjudicated unrelated to the LC518 A2 design. Its
     lc518/mutation-named files (mutants M01–M12, `MECHANISM_CHARTER.md`,
     `PHASE2_MUTATION_AUDIT.md`, `PROV-001/mutation_manifest_original.json`,
     `generator_assignment_v1.json`, …) all carry **June 2026** timestamps —
     months before the A2 mutation design existed (2026-11-06, §2) — and
     **cannot be the annex**. No content was read; classification rests on
     §3's standing adjudication plus the timestamps.
  3. All remaining hits are package-library noise or git refs/logs in the
     study repository.

**No annex, no allocation manifest, no candidate document was found.**

### 28.2 Standing coverage picture (unchanged by this re-check)

Covered by statements of absence: the repository (all refs, history paths,
archive members); the bank artifact; owner-local storage (§3 plus this
re-check); the preserved Library archive (contents per GPT's §27 report, a
breached-boundary account). **Still not covered, and owner-actionable only:**
the owner's chat/e-mail delivery channel; the owner's conversation history —
the 2026-11-06 design decisions (taxonomy, pair assignment, S-extra,
retention) exist there even if the annex was never materialized as a file;
any other machine or backup. **Global absence is not claimed.**

### 28.3 Status

Verdict unchanged: **BLOCKED / NOT ASSESSABLE**. The §6 owner decision (supply
the annex, pursue recovery, or formally drop the mutation design) remains the
sole gate. A replacement annex remains path 2 — separate authorization, a new
design, not a reconstruction (§12). No commit; no construction; no execution;
no annex inspection by any agent.

## 29. Temp-directory sweep; committed message archives identified and classified (2026-11-07; §§ 1–28 preserved)

Prepared by Qoder CLI (GLM role: record-keeper), continuing the owner-directed
availability search (§28) on the owner's instruction to check `C:` local Temp.
Filename- and metadata-level only; **no member contents extracted or read**;
nothing reconstructed (work order :45).

### 29.1 User-local Temp sweep

- **Location searched:** `C:\Users\pakla\AppData\Local\Temp` — eight LC518
  extraction/review trees (`arch_5db757e`, `arch_7679c98`, `arch_caa008b`,
  `arch_test`, `lc518-verify-41591572358`, `lc518-verify-local`, `lc518r2`,
  `lc518r3`), **3,126 files** in total. Every file is a replica of known
  repository/review-package content: the containment review packages r2/r3,
  the generator scratch ZIP, the bank artifact, the solver population
  (`solver_01`–`solver_120`), banks and oracle outputs, canary/probe run logs,
  phase documents and manifests. The bank-artifact copy's SHA-256 equals the
  recorded sanitized-repack digest `71f1e76b…` (VERIFICATION_LOG addendum 1),
  confirming artifact identity. Extended patterns (`*pair*`, `*schedul*`,
  `*assign*`, `*work_order*`, `*ground_truth*`, `*taxonomy*`) hit only
  package-library noise. **No annex, no allocation manifest, no candidate
  document.**
- `C:\Temp` does not exist; `C:\Windows\Temp` is access-denied to this process
  (not searched; noted for completeness).

### 29.2 Committed message archives identified; inventory gap closed

- The repository contains **two binary archives not itemized in
  `REPOSITORY_STORAGE_INVENTORY_2026-11-05.md`**: `message-70b0882f-9d72-402f-a641-36fa9f386b75.zip`
  (30,077 bytes) and `message-73aed204-bc5d-400e-8910-47557479f75e.zip`
  (49,622 bytes), added by owner upload (GitHub user `foued2`, commit
  `d1b7351`, 2026-11-01, "Add files via upload"). Members are compressed, so
  the inventory's text-level content search could not reach inside them; the
  blanket §2 absence claim is supplemented by this section.
- **Member listing (names and sizes only; no extraction):**
  - Archive 1: `CORRECTIONS_RECORD_v1.1.md` (25,034 B);
    `CORRECTIONS_RECORD_v1.2-draft.md` (51,903 B).
  - Archive 2: `superseded-CORRECTIONS_RECORD_v1.2-draft.entry39-issue-sha256c97c95e0.md`
    (51,903 B); `CORRECTIONS_RECORD_v1.2-draft.md` (60,796 B);
    `VERIFICATION_MAP_v1.2.md` (13,922 B).
- Classification: these are the **corrections-record / verification-map
  bookkeeping family cited in §3** — the documents that themselves record the
  annex as MISSING (0/150 solver bodies; stop rule, work order :45/:47). Two
  different sizes for the v1.2 draft across the archives are consistent with
  successive drafts; recorded as observed. **Not annex-bearing at the metadata
  level.** Contents remain unread; any content-level verification follows the
  authorized channels.

### 29.3 Status

Verdict unchanged: **BLOCKED / NOT ASSESSABLE**. The §28.2 coverage picture
now additionally covers user-local Temp and the two committed message archives
(at the metadata level). The remaining owner-actionable coverage is unchanged:
the chat/e-mail delivery channel, the conversation history, other machines or
backups. No commit; no content reading; no reconstruction.

## 30. Reclassification of record: annex existence unproven; search reframed as design-history investigation (2026-11-07; §§ 1–29 preserved)

Prepared by Qoder CLI (GLM role: record-keeper) on GPT's correction. Append-only;
no prior line modified.

### 30.1 GPT's correction

GPT (2026-11-07): "Nobody has shown us proof that this annex was ever created.
I treated its existence as established when the evidence does not establish
that. That was my mistake." He withdraws his previous statements that an
existing annex needed to be recovered: "That premise has not been demonstrated.
Rev11 remains frozen, but its freeze does not validate that premise."

**Corrected description of record (GPT's formulation):** "The LC518 mutation
allocation is a required design input for A2. Its existence as a completed,
standalone annex has not been established. It may have been fully designed in
conversation, partially designed, or never completed. We must not choose among
those possibilities without evidence."

GPT's cited documentary basis:

1. The frozen protocol's own non-claim (Rev 3 §12, carried through Rev 11):
   "It does not assert that an annex exists, ever existed, or can be
   recovered."
2. Record §8.6: the two paths — recover the original annex *if it exists*, or
   authorize a new allocation design *if the original was never created* — and
   the explicit line: "Whether an annex was ever authored at all is not
   determinable from artifacts alone."
3. Worklog entry 29 (2026-11-01, commit `511bc20`): establishes **non-delivery
   to GLM** at that point — not creation by anyone else.

GPT's finding of record: no primary evidence in the examined material shows
who authored an annex, when, under what filename or storage location, any
attachment or delivery event, or any hash or identity record for an original
annex. The record-keeper concurs: the searches of §§3, 9, 28, 29 surfaced no
creation evidence either.

### 30.2 Record-keeper corroboration from the primary commissioning document

The work order (`.qoder_workorder.md`, repo root, untracked; v1.0, 2026-11-01;
21,266 bytes; SHA-256 `5cba2fc2ae30e2d77dcf9037953c6f47ed220e853b4bf89c732080297c9bdb65`)
independently corroborates the reclassification at its §4:

- "The owner **will supply** GLM a separate private mutation-design annex
  containing the **approved** eight-mechanism taxonomy and the fixed
  pair-allocation schedule."
- "If GLM has not received it, stop and request it; do not invent, rename,
  merge or substitute mechanisms."

The annex is thereby a **commissioned future artifact requiring owner
approval** — and the recorded stop rule (worklog entry 29) shows the
commissioned delivery never occurred. The commissioning text contains no
evidence of creation.

### 30.3 How the drift happened (diagnosis adopted)

The term "private mutation-design annex" in the work order, protocol and audit
record defined a **required audit input**. Through repeated use, reviewers and
record-keeper began speaking of that required artifact as an existing document
that had gone missing. GPT's diagnosis — "That inference was unjustified" — is
adopted of record.

### 30.4 Effect on prior sections (supersession; append-only)

- The recovery framing of §20.4, §26.3 (items 3–4) and the "trace the
  delivery/storage location" task is **superseded in premise**: the object of
  the next investigation is the **design history**, not a file whose creation
  was never proved.
- The §28 and §29 search results **stand as absence evidence** for any
  standalone annex artifact on owner-reachable storage; their recovery framing
  is corrected by this section.
- §27 stands a fortiori: the preserved archive is not a recovery source, and
  it remains **sealed** under §20.2/§21.1 pending the §2 prerequisites. The
  §27 breach sets no precedent and authorizes no design-history access to it.

### 30.5 What does not change

Rev 11 remains frozen — it governs whatever artifact, if any, is ever supplied
through C0. Verdict: **BLOCKED / NOT ASSESSABLE**. Boundaries unchanged: no
annex inspection, archive opening, construction, execution, commit,
publication. The no-reconstruction rule (work order :45) remains in force. The
§6 owner decision structure remains, reframed: the owner may first establish
from the design history whether the allocation was ever completed, then choose
among supply / drop / separately-authorized new design.

### 30.6 Next task of record (GPT's reframing)

Investigate the original design history to establish what was actually decided.
Reachable sources:

1. The work order itself (identity pinned in §30.2).
2. Repository design artifacts: `PARENT_DESIGN.md` v1.0 (roster G01–G30,
   frozen), `BANK_DESIGN.md` v1.0, `LC518_TASK_CONTRACT.md`, and the
   lc518-150 git history (e.g., `glm-handoff/worklog.md`).
3. The preserved review-work archive — **sealed**; its design-history
   documents (analysis-spec draft, work-order amendments review) stay
   inaccessible pending §2 prerequisites.
4. The owner-side conversation history — the primary source for GPT's
   "fully designed in conversation" possibility — owner-actionable only.

The record-keeper has not launched this investigation; its scope and
authorization belong to the owner and the reviewers. Claude's concurrence with
this reclassification is requested but not required for its recording.
